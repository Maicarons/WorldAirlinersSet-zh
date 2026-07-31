# 项目结构

WAS 是一个由 **CMake** 驱动的 NewGRF 工程，源码以 **NML** 编写，并通过 C 预处理器（`.pnml` 文件中的
`#include` 与 `#define`）组织成上千个源文件。下面按目录梳理整个仓库的构成。

```
WorldAirlinersSet/
├── CMakeLists.txt          # 顶层构建定义（NML / GRF / Bundles 各目标）
├── CMakePresets.json       # CMake 预设（Ninja / Make / VS 生成器）
├── Makefile                # CMake 生成的构建入口（make / make clean）
├── WAS.pnml                # 主入口：用 #include 汇总所有飞机源文件
├── custom_tags.txt         # 构建期生成的版本/标识信息
├── bin/                    # 构建输出：生成的 .grf 与 .nml
├── build/                  # CMake 生成的中间目录
├── docs/                   # 本 VitePress 文档（含原 readme.txt / license.txt / changelog.txt）
├── documentation/          # 杂项文档、xlsx 跟踪表、Logo 等
├── greyscales/             # 各机型的灰阶（基础）涂装 PNG，按制造商分类
├── lang/                   # 14 种语言文件（*.lng）
├── scripts/                # 3 个 CMake 脚本，驱动 NML/GRF/文档处理
├── sprites/                # 历史/辅助精灵资源（pcx / nfo / png / examplenfo）
└── src/                    # 核心源码
    ├── *.pnml              # 顶层定义（header / check / basecost / cargotable ...）
    ├── gfx/                # 所有飞机，按 制造商/系列/型号 三级目录
    └── sound/              # 起降音效（.wav）
```

## 核心源码（`src/`）

| 文件 | 作用 |
| --- | --- |
| `header.pnml` | GRF 头定义：`grfid`、`name`、`url`、版本号，以及 4 个可调参数 |
| `check.pnml` | 编译器/环境检查宏 |
| `basecost.pnml` | 基础成本相关定义 |
| `cargotable.pnml` | 货物（cargo）表定义，对应可改装项 |
| `definition.pnml` | 通用宏：`get_model_life`、`get_retire_early`、`plane_speed_kmh`、`plane_RC`、`flight_state` 等 |
| `graph_templates.pnml` | 图形模板（精灵集模板宏） |
| `disable_origin.pnml` | 禁用原版飞机等开关 |
| `sort_order.pnml` | 购买列表中飞机的排序定义 |
| `gfx/` | 每个机型一个目录，内含 `.pnml`（飞机逻辑）与若干 `.png`（涂装精灵） |
| `sound/` | 起降音效文件（`av_turbogo.wav`、`av_landturbo.wav`） |

## 飞机源文件（`src/gfx/`）

- 采用三级目录结构：`制造商 / 系列 / 具体型号`。
  例如 `Boeing / B737 / B737-800 /`。
- 每个型号目录下包含：
  - 一个 **`型号.pnml`**：定义该飞机的精灵集（spriteset）、状态切换（switch）、属性（property）与图形（graphics）。
  - 若干 **`.png` 涂装文件**：每个 PNG 对应一种航空公司涂装（含一个 `(0)Greyscale.png` 作为灰阶基底）。
- 当前约有 **145** 个机型 `.pnml` 文件、约 **1743** 个涂装 PNG。

```text
src/gfx/Boeing/B737/B737-800/
├── (0)Greyscale.png      # 灰阶基底涂装
├── B737-800.pnml         # 飞机逻辑 + 精灵引用
├── AerLingus.png         # 各航空公司涂装
├── Lufthansa.png
└── ...
```

## 语言文件（`lang/`）

- 14 个 `.lng` 文件，覆盖 catalan、chinese_simplified、croatian、czech、dutch、english、finnish、
  german、indonesian、italian、korean、polish、russian、spanish。
- 通过 `##grflangid` 声明语言 ID，提供所有 STR_* 字符串的本地化（GRF 名称、参数说明、机型名、涂装名等）。

## 构建脚本（`scripts/`）

| 脚本 | 作用 |
| --- | --- |
| `Compile.cmake` | 调用 `nmlc` 把 `.nml` 编译为最终 `.grf` |
| `GenerateCustomTags.cmake` | 生成 `custom_tags.txt`（版本号、GRF 文件名、日期等） |
| `ProcessDocs.cmake` | 调用 `grfid` 计算 MD5，并把 `docs/` 下三个文本文件配置进发布包 |

## 资源目录说明

- `greyscales/`：各机型灰阶涂装的 PNG 备份/来源，按制造商分类（129 个 `.png`）。
- `sprites/`：历史与辅助资源，包含 `pcx/`、`png/`、`nfo/`、`examplenfo/`。其中 `nfo/` 保留了旧 NFO 流程的字符串/精灵定义，
  `examplenfo/` 含 callback 示例（`callback36.txt`、`xx.nfo`）。
- `documentation/`：开发用的跟踪表（xlsx）、Logo 源文件、旧英文 lng 等参考资料。

返回：[NewGRF 参数 →](/guide/parameters) ｜ 下一步：[从源码构建 →](/guide/building)
