"""从 WAS .pnml 源文件提取全部机型与涂装数据，裁切预览图并生成 VitePress 机队图鉴页面。

用法:
    python tools/gen_aircraft_md.py
"""
from __future__ import annotations

import os
import re
import shutil
from collections import OrderedDict
from pathlib import Path

from PIL import Image

ROOT = Path(r"G:/GitHub/WorldAirlinersSet")
DOCS = ROOT / "docs"
PUBLIC = DOCS / "public"
WAS = ROOT / "WAS.pnml"
LANG_EN = ROOT / "lang" / "english.lng"
LANG_ZH = ROOT / "lang" / "chinese_simplified.lng"
OUT_PUBLIC = PUBLIC / "aircraft"
OUT_DOCS = DOCS / "aircraft"

MFR_ZH = {
    "Airbus": "空中客车",
    "Antonov": "安东诺夫",
    "ATR": "ATR",
    "BAC": "BAC",
    "BAe": "BAe",
    "Boeing": "波音",
    "Bombardier": "庞巴迪",
    "Embraer": "巴航工业",
    "Fokker": "福克",
    "Ilyushin": "伊留申",
    "Lockheed": "洛克希德",
    "McDonnell_Douglas": "麦克唐纳·道格拉斯",
    "SUD": "SUD 宇航",
    "Tupolev": "图波列夫",
}

AIRCRAFT_TYPE_ZH = {
    "AIRCRAFT_TYPE_SMALL": "小型",
    "AIRCRAFT_TYPE_MEDIUM": "中型",
    "AIRCRAFT_TYPE_LARGE": "大型",
    "AIRCRAFT_TYPE_HELICOPTER": "直升机",
}

# 预览图放大倍数（保持像素风）
SCALE = 3


def load_lang(path: Path) -> dict[str, str]:
    d: dict[str, str] = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = re.match(r"^(STR_\w+)\s*:(.*)$", line.rstrip("\r\n"))
            if m:
                d[m.group(1)] = m.group(2).strip()
    return d


lang_en = load_lang(LANG_EN)
lang_zh = load_lang(LANG_ZH)


def safe_filename(name: str) -> str:
    """把涂装文件名/ID 转成安全文件名。"""
    s = re.sub(r"[^\w\-]+", "_", name)
    s = s.strip("_")
    return s or "unknown"


def make_transparent(im: Image.Image, trans: tuple[int, int, int] = (0, 0, 255)) -> Image.Image:
    """将 OpenTTD 标准透明蓝 (#0000FF) 转成 Alpha 透明。"""
    if im.mode != "RGBA":
        im = im.convert("RGBA")
    px = im.load()
    rt, gt, bt = trans
    for yy in range(im.height):
        for xx in range(im.width):
            r, g, b, a = px[xx, yy]
            if a and r == rt and g == gt and b == bt:
                px[xx, yy] = (0, 0, 0, 0)
    return im


def parse_switch_block(text: str, switch_name: str) -> str | None:
    """提取 switch (FEAT_AIRCRAFT, SELF, name, ...) { body } 的 body。"""
    pattern = re.compile(
        r"switch\s*\(\s*FEAT_AIRCRAFT\s*,\s*SELF\s*,\s*" + re.escape(switch_name) + r"\b.*?\{(.*?)^\s*\}",
        re.S | re.M,
    )
    m = pattern.search(text)
    return m.group(1) if m else None


def parse_aircraft(rel: str) -> dict | None:
    """解析单个机型 .pnml，返回包含属性、涂装、购买帧坐标等信息的字典。"""
    pnml_path = ROOT / rel
    text = pnml_path.read_text(encoding="utf-8", errors="replace")

    # 机型 ID
    m = re.search(r"item\s*\(\s*FEAT_AIRCRAFT\s*,\s*(\w+)\s*\)", text)
    if not m:
        print(f"  跳过 {rel}：未找到 item(FEAT_AIRCRAFT, ...)")
        return None
    ac_id = m.group(1)

    # 购买帧裁切坐标
    m = re.search(r"purchase_sprite\(\s*\w+\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)", text)
    if not m:
        print(f"  跳过 {rel}：未找到 purchase_sprite")
        return None
    px, py, pw, ph = (int(g) for g in m.groups())

    # 涂装源图路径（按 IMAGEFILE 出现顺序）
    image_files = re.findall(r'#define\s+IMAGEFILE\s+"([^"]+)"', text)
    if not image_files:
        print(f"  跳过 {rel}：未找到 IMAGEFILE")
        return None

    # 机型名 key
    name_key = None
    m = re.search(r"name:\s*string\(\s*(STR_AIRV_\w+)\s*\)", text)
    if m:
        name_key = m.group(1)

    # 基础属性
    intro_year = None
    m = re.search(r"introduction_date:\s*date\s*\(\s*get_plane_year\(\s*([0-9]+)\s*\)", text)
    if m:
        base = int(m.group(1))
        intro_year = base - 2  # get_plane_year(year) = year - 2

    passenger = re_search_int(text, r"passenger_capacity:\s*([0-9]+)")
    mail = re_search_int(text, r"mail_capacity:\s*([0-9]+)")
    accel = re_search_int(text, r"acceleration:\s*([0-9]+)")
    cost_factor = re_search_int(text, r"cost_factor:\s*([0-9]+)")
    base_range = re_search_int(text, r"range:\s*([0-9]+)")

    aircraft_type = None
    m = re.search(r"aircraft_type:\s*(AIRCRAFT_TYPE_\w+)", text)
    if m:
        aircraft_type = m.group(1)

    speed_kmh = None
    m = re.search(r"purchase_speed:\s*plane_speed_kmh\(\s*([0-9]+)\s*\)", text)
    if m:
        speed_kmh = int(m.group(1))

    # cargo_subtype_text 映射 index -> STR_VLIV key
    vkey_by_index: dict[int, str] = {}
    body = parse_switch_block(text, f"{ac_id}_cargo_subtype_text")
    if body:
        for idx, vkey in re.findall(r"\b(\d+):\s*string\(\s*(STR_VLIV_\w+)\s*\)", body):
            vkey_by_index[int(idx)] = vkey

    # cargo_subtype_capacity 映射 index -> capacity
    cap_by_index: dict[int, int] = {}
    body = parse_switch_block(text, f"{ac_id}_cargo_subtype_capacity")
    if body:
        for idx, cap in re.findall(r"\b(\d+):\s*return\s*([0-9]+)", body):
            cap_by_index[int(idx)] = int(cap)

    # 制造商：从 include 路径 src/gfx/<Mfr>/... 取第一段
    mfr_en = rel.split("/")[2]

    liveries: list[dict] = []
    for i, rel_img in enumerate(image_files):
        basename = Path(rel_img).stem
        # 去掉常见前缀
        label = re.sub(r"^\(0\)", "", basename).strip()
        vkey = vkey_by_index.get(i)
        name_en = lang_en.get(vkey, label) if vkey else (label if i == 0 else "")
        name_zh = lang_zh.get(vkey, name_en) if vkey else (name_en if i == 0 else "")
        if i == 0 and not vkey:
            name_en = name_zh = "灰阶（默认）"
        liveries.append(
            {
                "index": i,
                "src": rel_img,
                "basename": basename,
                "vkey": vkey,
                "name_en": name_en,
                "name_zh": name_zh,
                "capacity": cap_by_index.get(i),
                "filename": f"{i:03d}_{safe_filename(basename)}.png",
            }
        )

    return {
        "id": ac_id,
        "name_key": name_key,
        "name_en": lang_en.get(name_key, ac_id) if name_key else ac_id,
        "name_zh": lang_zh.get(name_key, lang_en.get(name_key, ac_id)) if name_key else ac_id,
        "mfr_en": mfr_en,
        "mfr_zh": MFR_ZH.get(mfr_en, mfr_en),
        "intro_year": intro_year,
        "passenger": passenger,
        "mail": mail,
        "accel": accel,
        "cost_factor": cost_factor,
        "base_range": base_range,
        "aircraft_type": aircraft_type,
        "aircraft_type_zh": AIRCRAFT_TYPE_ZH.get(aircraft_type or "", aircraft_type or ""),
        "speed_kmh": speed_kmh,
        "purchase": {"x": px, "y": py, "w": pw, "h": ph},
        "liveries": liveries,
    }


def re_search_int(text: str, pattern: str) -> int | None:
    m = re.search(pattern, text)
    return int(m.group(1)) if m else None


def crop_and_save(src_png: Path, crop: dict, dest: Path) -> None:
    """裁切购买帧、去蓝底、放大并保存。"""
    with Image.open(src_png) as im:
        im = im.crop((crop["x"], crop["y"], crop["x"] + crop["w"], crop["y"] + crop["h"]))
        im = make_transparent(im)
        im = im.resize((crop["w"] * SCALE, crop["h"] * SCALE), Image.NEAREST)
        dest.parent.mkdir(parents=True, exist_ok=True)
        im.save(dest, "PNG")


def make_attr_table(ac: dict) -> str:
    lines = ["| 属性 | 数值 |", "|---|---|"]
    if ac["intro_year"] is not None:
        lines.append(f"| 引入年份 | {ac['intro_year']} |")
    if ac["passenger"] is not None:
        lines.append(f"| 乘客容量 | {ac['passenger']} |")
    if ac["mail"] is not None:
        lines.append(f"| 邮件容量 | {ac['mail']} |")
    if ac["speed_kmh"] is not None:
        lines.append(f"| 巡航速度 | {ac['speed_kmh']} km/h |")
    if ac["base_range"] is not None:
        lines.append(f"| 设计航程 | {ac['base_range']} |")
    if ac["accel"] is not None:
        lines.append(f"| 加速性能 | {ac['accel']} |")
    if ac["aircraft_type_zh"]:
        lines.append(f"| 机型类别 | {ac['aircraft_type_zh']} |")
    if ac["cost_factor"] is not None:
        lines.append(f"| 成本系数 | {ac['cost_factor']} |")
    return "\n".join(lines)


def make_livery_grid(ac: dict) -> str:
    if not ac["liveries"]:
        return "_本机型暂无额外涂装。_\n"
    parts = ['<div class="livery-grid">']
    for livery in ac["liveries"]:
        img_path = f"/aircraft/{ac['id']}/{livery['filename']}"
        en = livery["name_en"]
        zh = livery["name_zh"]
        label = f"{zh}" if zh == en or not en else f"{zh}<br><small>{en}</small>"
        parts.append(
            f'  <div class="livery-card">\n'
            f'    <img src="{img_path}" alt="{zh or en}" loading="lazy">\n'
            f'    <div class="livery-name">{label}</div>\n'
            f"  </div>"
        )
    parts.append("</div>")
    return "\n".join(parts)


def build_mfr_page(mfr_en: str, aircrafts: list[dict]) -> str:
    mfr_zh = aircrafts[0]["mfr_zh"]
    total_liv = sum(len(a["liveries"]) for a in aircrafts)
    lines = [
        f"# {mfr_zh} ({mfr_en})",
        "",
        f"本页收录 **{mfr_zh}** 制造的 {len(aircrafts)} 款机型，共 {total_liv} 张涂装预览图（含默认灰阶）。",
        "",
        "---",
        "",
    ]
    for ac in aircrafts:
        lines.extend(
            [
                f"## {ac['name_zh']} <small>({ac['name_en']})</small> {{#{ac['id'].lower()}}}",
                "",
                f"- **内部 ID**：`{ac['id']}`",
                f"- **英文名**：{ac['name_en']}",
                "",
                make_attr_table(ac),
                "",
                f"### 涂装预览（{len(ac['liveries'])} 种）",
                "",
                make_livery_grid(ac),
                "",
                "---",
                "",
            ]
        )
    return "\n".join(lines)


def build_index(mfr_groups: OrderedDict[str, list[dict]], total_ac: int, total_liv: int) -> str:
    lines = [
        "# 机队图鉴",
        "",
        "World Airliner Set 收录了来自多家制造商的真实世界客机。本图鉴按制造商分类，展示全部机型与涂装预览。",
        "",
        "## 统计",
        "",
        f"- **机型总数**：{total_ac}",
        f"- **涂装总数**：{total_liv}（含默认灰阶基础图）",
        f"- **制造商数**：{len(mfr_groups)}",
        "",
        "## 制造商索引",
        "",
        "| 制造商 | 机型数 | 涂装数 | 图鉴页 |",
        "|---|---|---|---|",
    ]
    for mfr_en, aircrafts in mfr_groups.items():
        mfr_zh = aircrafts[0]["mfr_zh"]
        n_ac = len(aircrafts)
        n_liv = sum(len(a["liveries"]) for a in aircrafts)
        page = f"[查看]({mfr_en.lower()}.md)"
        lines.append(f"| {mfr_zh} ({mfr_en}) | {n_ac} | {n_liv} | {page} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 全部机型速览")
    lines.append("")
    lines.append("| 机型 | 制造商 | 引入年份 | 涂装数 | 详情 |")
    lines.append("|---|---|---|---|---|")
    for mfr_en, aircrafts in mfr_groups.items():
        mfr_zh = aircrafts[0]["mfr_zh"]
        for ac in aircrafts:
            year = ac["intro_year"] if ac["intro_year"] is not None else "—"
            link = f"[详情]({mfr_en.lower()}.md#{ac['id'].lower()})"
            lines.append(
                f"| {ac['name_zh']} | {mfr_zh} | {year} | {len(ac['liveries'])} | {link} |"
            )
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    # 1. 读取 WAS 的机型 include 列表
    was_text = WAS.read_text(encoding="utf-8", errors="replace")
    includes = []
    for line in was_text.splitlines():
        m = re.search(r'#include\s+"([^"]+\.pnml)"', line)
        if m and m.group(1).startswith("src/gfx/"):
            includes.append(m.group(1))
    print(f"发现 {len(includes)} 个机型源文件")

    # 2. 解析每个机型
    aircrafts: list[dict] = []
    for rel in includes:
        ac = parse_aircraft(rel)
        if ac:
            aircrafts.append(ac)
    print(f"成功解析 {len(aircrafts)} 个机型")

    # 3. 清空并重建 public/aircraft 输出目录
    if OUT_PUBLIC.exists():
        shutil.rmtree(OUT_PUBLIC)
    OUT_PUBLIC.mkdir(parents=True, exist_ok=False)
    OUT_DOCS.mkdir(parents=True, exist_ok=True)

    # 4. 裁切涂装预览图
    skipped = 0
    for ac in aircrafts:
        for livery in ac["liveries"]:
            src = ROOT / livery["src"]
            dest = OUT_PUBLIC / ac["id"] / livery["filename"]
            if not src.exists():
                print(f"  源图不存在: {src}")
                skipped += 1
                continue
            try:
                crop_and_save(src, ac["purchase"], dest)
            except Exception as e:
                print(f"  裁切失败 {src}: {e}")
                skipped += 1
    total_liv = sum(len(a["liveries"]) for a in aircrafts)
    print(f"生成 {total_liv - skipped} 张预览图，跳过 {skipped} 张")

    # 5. 按制造商分组
    mfr_groups: OrderedDict[str, list[dict]] = OrderedDict()
    for ac in aircrafts:
        mfr_groups.setdefault(ac["mfr_en"], []).append(ac)
    # 按预设顺序排序制造商
    ordered = OrderedDict()
    for key in MFR_ZH:
        if key in mfr_groups:
            ordered[key] = mfr_groups[key]
    for key, val in mfr_groups.items():
        if key not in ordered:
            ordered[key] = val

    # 6. 生成制造商页面
    for mfr_en, group in ordered.items():
        page = build_mfr_page(mfr_en, group)
        (OUT_DOCS / f"{mfr_en.lower()}.md").write_text(page, encoding="utf-8")
        print(f"生成 {mfr_en.lower()}.md ({len(group)} 个机型)")

    # 7. 生成索引页
    total_ac = len(aircrafts)
    total_liv_all = sum(len(a["liveries"]) for a in aircrafts)
    index = build_index(ordered, total_ac, total_liv_all)
    (OUT_DOCS / "index.md").write_text(index, encoding="utf-8")
    print(f"生成 aircraft/index.md")

    # 8. 写摘要 JSON（方便调试/其他脚本使用）
    summary = {
        "total_aircraft": total_ac,
        "total_liveries": total_liv_all,
        "manufacturers": [
            {"en": k, "zh": v[0]["mfr_zh"], "aircraft": len(v), "liveries": sum(len(a["liveries"]) for a in v)}
            for k, v in ordered.items()
        ],
    }
    import json

    (OUT_DOCS / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("完成")


if __name__ == "__main__":
    main()
