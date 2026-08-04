#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
克隆已有 donor 机型的 .pnml（精灵模板 + 占位像素图引用 + 涂装），
生成模组里缺失的最新机型变体。图形暂复用 donor 的占位精灵表，
待真实像素图绘制完成后替换 IMAGEFILE 指向即可，逻辑无需改动。

仅用于“拉平最新机型清单”的一次性生成；真实新增机型仍需美术资产。
"""
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# donor 前缀（整体替换，避免误伤路径里的 /A320neo/）
# newid 不含 donor 子串，故不会二次替换。
PLAN = [
    {
        "donor_pnml": "src/gfx/Airbus/A320/A320neo/A320neo.pnml",
        "donor_stem": "Airbus_A320neo",
        "new_id": "Airbus_A321neo",
        "new_dir": "src/gfx/Airbus/A321/A321neo",
        "str_airv": "STR_AIRV_AIRBUS_A321NEO",
        "aircraft_type": "AIRCRAFT_TYPE_SMALL",
        "year": 2016, "month": 5, "day": 25,
        "capacity": 220, "range": 1400, "cruise": 833,
        "cost": 108, "run": 74, "veh_life": 26, "life_end": 2050,
    },
    {
        "donor_pnml": "src/gfx/Airbus/A330/A330-300/A330-300.pnml",
        "donor_stem": "Airbus_A330_300",
        "new_id": "Airbus_A330_900neo",
        "new_dir": "src/gfx/Airbus/A330/A330-900neo",
        "str_airv": "STR_AIRV_AIRBUS_A330_900NEO",
        "aircraft_type": "AIRCRAFT_TYPE_LARGE",
        "year": 2018, "month": 11, "day": 26,
        "capacity": 300, "range": 2600, "cruise": 926,
        "cost": 190, "run": 168, "veh_life": 25, "life_end": 2050,
    },
    {
        "donor_pnml": "src/gfx/Airbus/A350/A350-900/A350-900.pnml",
        "donor_stem": "Airbus_A350_900",
        "new_id": "Airbus_A350_1000",
        "new_dir": "src/gfx/Airbus/A350/A350-1000",
        "str_airv": "STR_AIRV_AIRBUS_A350_1000",
        "aircraft_type": "AIRCRAFT_TYPE_LARGE",
        "year": 2018, "month": 1, "day": 15,
        "capacity": 366, "range": 2950, "cruise": 945,
        "cost": 235, "run": 200, "veh_life": 30, "life_end": 2050,
    },
    {
        "donor_pnml": "src/gfx/Airbus/A320/A320neo/A320neo.pnml",
        "donor_pnml_note": "A220 用窄体 neo 模板占位",
        "donor_stem": "Airbus_A320neo",
        "new_id": "Airbus_A220_300",
        "new_dir": "src/gfx/Airbus/A220/A220-300",
        "str_airv": "STR_AIRV_AIRBUS_A220_300",
        "aircraft_type": "AIRCRAFT_TYPE_SMALL",
        "year": 2016, "month": 12, "day": 21,
        "capacity": 145, "range": 1090, "cruise": 840,
        "cost": 92, "run": 66, "veh_life": 26, "life_end": 2050,
    },
    {
        "donor_pnml": "src/gfx/Boeing/B737/B737MAX8/B737MAX8.pnml",
        "donor_stem": "Boeing_737_MAX8",
        "new_id": "Boeing_737_MAX9",
        "new_dir": "src/gfx/Boeing/B737/B737MAX9",
        "str_airv": "STR_AIRV_BOEING_737_MAX9",
        "aircraft_type": "AIRCRAFT_TYPE_SMALL",
        "year": 2018, "month": 2, "day": 21,
        "capacity": 178, "range": 1250, "cruise": 975,
        "cost": 106, "run": 73, "veh_life": 30, "life_end": 2272,
    },
    {
        "donor_pnml": "src/gfx/Boeing/B787/B787-9/B787-9.pnml",
        "donor_stem": "Boeing_787_9",
        "new_id": "Boeing_787_10",
        "new_dir": "src/gfx/Boeing/B787/B787-10",
        "str_airv": "STR_AIRV_BOEING_787_10",
        "aircraft_type": "AIRCRAFT_TYPE_LARGE",
        "year": 2018, "month": 3, "day": 26,
        "capacity": 330, "range": 2400, "cruise": 943,
        "cost": 230, "run": 175, "veh_life": 30, "life_end": 2266,
    },
    {
        "donor_pnml": "src/gfx/Airbus/A320/A320neo/A320neo.pnml",
        "donor_stem": "Airbus_A320neo",
        "new_id": "Airbus_A319neo",
        "new_dir": "src/gfx/Airbus/A320/A319neo",
        "str_airv": "STR_AIRV_AIRBUS_A319NEO",
        "aircraft_type": "AIRCRAFT_TYPE_SMALL",
        "year": 2017, "month": 4, "day": 1,
        "capacity": 160, "range": 1200, "cruise": 833,
        "cost": 95, "run": 66, "veh_life": 26, "life_end": 2050,
    },
    {
        "donor_pnml": "src/gfx/Boeing/B737/B737MAX9/B737MAX9.pnml",
        "donor_stem": "Boeing_737_MAX9",
        "new_id": "Boeing_737_MAX10",
        "new_dir": "src/gfx/Boeing/B737/B737MAX10",
        "str_airv": "STR_AIRV_BOEING_737_MAX10",
        "aircraft_type": "AIRCRAFT_TYPE_SMALL",
        "year": 2021, "month": 5, "day": 1,
        "capacity": 230, "range": 1300, "cruise": 975,
        "cost": 112, "run": 76, "veh_life": 30, "life_end": 2275,
    },
    {
        "donor_pnml": "src/gfx/Boeing/B777/B777-300ER/B777-300ER.pnml",
        "donor_stem": "Boeing_777_300ER",
        "new_id": "Boeing_777X",
        "new_dir": "src/gfx/Boeing/B777/B777X",
        "str_airv": "STR_AIRV_BOEING_777X",
        "aircraft_type": "AIRCRAFT_TYPE_LARGE",
        "year": 2020, "month": 1, "day": 25,
        "capacity": 426, "range": 3400, "cruise": 905,
        "cost": 305, "run": 240, "veh_life": 30, "life_end": 2272,
    },
    {
        "donor_pnml": "src/gfx/Embraer/E195/E195LR/E195LR.pnml",
        "donor_stem": "Embraer_E195LR",
        "new_id": "Embraer_E195_E2",
        "new_dir": "src/gfx/Embraer/E195/E195_E2",
        "str_airv": "STR_AIRV_EMBRAER_E195_E2",
        "aircraft_type": "AIRCRAFT_TYPE_SMALL",
        "year": 2019, "month": 4, "day": 15,
        "capacity": 146, "range": 1050, "cruise": 890,
        "cost": 44, "run": 69, "veh_life": 26, "life_end": 2052,
    },
]


def clone(cfg):
    src = os.path.join(ROOT, cfg["donor_pnml"])
    dst_dir = os.path.join(ROOT, cfg["new_dir"])
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, os.path.basename(dst_dir) + ".pnml")
    txt = open(src, "r", encoding="utf-8").read()

    stem = cfg["donor_stem"]
    nid = cfg["new_id"]
    # 1) 整体替换标识符前缀（宏名 / 各 switch / spriteset / item id）
    txt = txt.replace(stem, nid)
    # 2) 机型名
    txt = re.sub(r"name:\s*string\(STR_AIRV_[A-Z0-9_]+\);",
                 f"name: string({cfg['str_airv']});", txt, count=1)
    # 3) 引入年份
    txt = re.sub(r"introduction_date:\s*date\(get_plane_year\(\d+\),\s*\d+,\s*\d+\);",
                 f"introduction_date: date(get_plane_year({cfg['year']}), {cfg['month']}, {cfg['day']});",
                 txt, count=1)
    # 4) vehicle_life
    txt = re.sub(r"vehicle_life:\s*\d+;", f"vehicle_life: {cfg['veh_life']};", txt, count=1)
    # 5) model_life / retire_early 起始年
    txt = re.sub(r"get_model_life\(\d+,", f"get_model_life({cfg['year']},", txt)
    txt = re.sub(r"get_retire_early\(\d+,", f"get_retire_early({cfg['year']},", txt)
    # 6) passenger_capacity（property 里的字面量）
    txt = re.sub(r"passenger_capacity:\s*\d+;", f"passenger_capacity: {cfg['capacity']};", txt, count=1)
    # 7) mail_capacity
    mail = max(9, round(cfg["capacity"] / 10))
    txt = re.sub(r"mail_capacity:\s*\d+;", f"mail_capacity: {mail};", txt, count=1)
    # 8) cost / running / purchase_speed
    txt = re.sub(r"cost_factor:\s*\d+;", f"cost_factor: {cfg['cost']};", txt, count=1)
    txt = re.sub(r"purchase_running_cost_factor:\s*\d+;", f"purchase_running_cost_factor: {cfg['run']};", txt, count=1)
    txt = re.sub(r"purchase_speed:\s*plane_speed_kmh\(\d+\);",
                 f"purchase_speed: plane_speed_kmh({cfg['cruise']});", txt, count=1)
    # 9) range：第1个为 property 默认=r1，其后三个 if 块为 0 / r1 / r2（保持 donor 设计）
    r1 = cfg["range"]
    r2 = round(r1 * 1.5)
    def range_repl(m):
        range_repl.i += 1
        vals = [r1, 0, r1, r2]
        return f"range: {vals[min(range_repl.i, 4) - 1]};"
    range_repl.i = 0
    txt = re.sub(r"range:\s*\d+;", range_repl, txt)
    # 10) cargo_subtype_capacity 全部 return 数字 -> 新座级
    txt = re.sub(r"return\s+\d+;", f"return {cfg['capacity']};", txt)

    # 头部注释
    header = (
        f"// {nid}\n"
        f"// 自动克隆自 donor {os.path.basename(src)}（占位像素图 + 精灵模板）。\n"
        f"// 真实 {nid} 像素图绘制完成后，把下方 IMAGEFILE 指向改回本目录 PNG 即可。\n\n"
    )
    txt = header + txt

    open(dst, "w", encoding="utf-8").write(txt)
    # 校验无残留 donor 前缀
    assert stem not in txt, f"残留 donor 前缀 {stem} 在 {dst}"
    return dst


if __name__ == "__main__":
    for c in PLAN:
        d = clone(c)
        print("generated:", d)
