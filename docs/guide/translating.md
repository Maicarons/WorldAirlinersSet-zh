# 语言翻译

WAS 通过 `lang/` 目录下的 `.lng` 文件实现多语言。所有界面文字——GRF 名称、参数说明、机型名、涂装名——
都来自这些文件中的 `STR_*` 字符串。

当前内置 14 种语言：catalan、chinese_simplified、croatian、czech、dutch、english、finnish、german、
indonesian、italian、korean、polish、russian、spanish。

## 翻译文件格式

每个 `.lng` 文件以语言 ID 开头，随后是 `字符串标识 : 本地化文本` 的键值对：

```text
##grflangid 0x01
STR_GRF_NAME                 :WAS {VERSION}
STR_GRF_DESCRIPTION          :{ORANGE}The World Airliner Set (WAS){}...
STR_PARAM_BCOSTS_NAME        :Base cost factor
STR_AIRV_AIRBUS_A300_600R    :Airbus A300-600R
...
```

::: warning 注意
- **`.lng` 文件中不要使用 Tab 缩进**，只用空格。
- 占位符（如 `{VERSION}`、`{ORANGE}`、`{SILVER}`）需原样保留。
:::

## 新增一种语言

1. 从 `lang/english.lng` 复制出 `7F_english.lng` 的同类文件，命名为
   `{语言ID}_{语言名}.lng`（参考上游旧流程 `sprites/nfo/00strings`）。
2. 到 <http://wiki.ttdpatch.net/tiki-index.php?page=Action4#language_id> 查找你的语言 ID。
3. 把文件中所有 `english` 改成你的语言名称，并在 `#define LANG .` 后填入对应语言常量
   （可用值见 `docs/readme.txt` 第 6 节，例如 `CHINESE_SIMPLIFIED`、`KOREAN` 等）。
4. 翻译 `"..."` 中的所有内容；**未翻译的行在行首加 `U`**，以节省 NewGRF 体积与内存。

## 更新现有语言

直接编辑对应的 `lang/*.lng`，保持字符串标识不变、仅更新右侧文本即可。新增了机型/涂装后，
别忘了为新加入的 `STR_AIRV_*` / `STR_VLIV_*` 补充翻译。

返回：[涂装与图形 →](/guide/liveries) ｜ 下一步：[贡献指南 →](/guide/contributing)
