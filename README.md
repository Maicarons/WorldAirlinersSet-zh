# World Airliner Set（世界客机集）— 中文版

> 本仓库 `Maicarons/WorldAirlinersSet-zh` 是上游 [`RvP93/WorldAirlinersSet`](https://github.com/RvP93/WorldAirlinersSet) 的**中文翻译与文档分支**：界面文字已完整翻译为简体中文与繁体中文，并配套了中文文档站。代码与图形内容均来自上游，本仓库不改动机型与图形，仅做本地化与文档维护。

[![GitHub Release](https://img.shields.io/github/v/release/Maicarons/WorldAirlinersSet-zh?label=Release)](https://github.com/Maicarons/WorldAirlinersSet-zh/releases)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL--3.0-blue.svg)](docs/license.txt)

---

## 这是什么？

**WAS（World Airliner Set，世界客机集）** 是一个 [OpenTTD](https://www.openttd.org/) 的 **NewGRF**（新图形资源包）。
它收录了现实世界中近期与历史上的客机与货机，并且让每一架飞机都能通过**改装（refit）**换上对应航空公司的**真实涂装**。

- 大部分原始飞机图形由 **PikkaBird** 创作，最初包含在 AV8 套装中；WAS 在此基础上加入了真实涂装，部分机型由 WAS 团队自行绘制。
- 借助 OpenTTD 的 NewGRF 引擎池支持，WAS 最多可包含 **65535** 架飞机，而不再受旧版 48 架的限制。
- 可与其他飞机 NewGRF 同时加载，互不冲突。
- 项目以 **GNU General Public License v3.0** 发布。

## 文档中心

完整的安装、参数、构建、涂装、翻译与贡献指南都在中文文档站：

👉 **[WAS 中文文档站](docs/index.md)**（VitePress 源码位于 `docs/`，可在本地 `npm run docs:dev` 预览）

| 你想做的事 | 去这里 |
| --- | --- |
| 了解项目背景与目标 | [项目简介](docs/guide/introduction.md) |
| 把 WAS 装进 OpenTTD 玩游戏 | [安装与使用](docs/guide/installation.md) |
| 了解可调节的 NewGRF 参数 | [NewGRF 参数](docs/guide/parameters.md) |
| 搞清楚目录里都是什么 | [项目结构](docs/guide/project-structure.md) |
| 从源码自己编译 `.grf` | [从源码构建](docs/guide/building.md) |
| 给飞机加涂装 / 画图 | [涂装与图形](docs/guide/liveries.md) |
| 帮忙翻译界面文字 | [语言翻译](docs/guide/translating.md) |
| 提交代码或反馈问题 | [贡献指南](docs/guide/contributing.md) |

---

## 下载与安装

### 方式一：下载 Release（推荐，含中文）

从本仓库的 [GitHub Releases](https://github.com/Maicarons/WorldAirlinersSet-zh/releases) 页面下载 `WorldAirlinersSet.grf`，放入 OpenTTD 的 `newgrf` 目录（Windows 下通常在 `文档/OpenTTD/newgrf`），然后在游戏内「新图形」窗口中点击「添加」并启用即可。

> 中文名称需要你在 OpenTTD 的语言设置中选择**简体中文**或**繁体中文**后才会显示。

### 方式二：从 BaNaNaS 下载（仅稳定版，英文界面）

在 OpenTTD 游戏内的「内容下载」列表中搜索 *World Airliner Set*，点击「下载」即可。该渠道提供的是上游英文原版。

### 启用与游玩

1. 打开 OpenTTD →「新图形」设置窗口 →「添加」，选择 **World Airliner Set**。
2. 点击「应用设置」并新建游戏。
3. 建造任意一架飞机后，点击**改装（Refit）**按钮，会看到货物列表，每种货物后方标注了对应的航空公司涂装。选择想要的涂装，点击「改装车辆」即可。

---

## NewGRF 参数

在「新图形」窗口选中 WAS 后，可设置以下参数（设置入口：选中后点击「参数」或「设置」）：

| 参数 | 说明 |
| --- | --- |
| **启用标准飞机** | 是否同时启用 OpenTTD 自带的默认飞机。 |
| **启用航程设置** | 是否限制飞机的「最大飞行距离」。关闭后所有飞机航程不限。 |
| **航程限制** | 在「启用航程设置」打开时生效：`正常航程` / `加长航程` / `关闭航程`。 |
| **购买成本系数** | 调整购买价格：`0` = 1/16 倍，默认 `4` = 不变，`8` = 16 倍。 |
| **运营成本系数** | 调整运营成本：`0` = 1/16 倍，默认 `4` = 不变，`8` = 16 倍。 |

---

## 从源码编译（进阶）

> 通常你**不需要**自己编译，直接下载 Release 即可。只有当你想获取最新改动或自行修改时才需要。

构建管线为：`.pnml` →（C 预处理器）→ `.nml` →（nmlc）→ `.grf`。所需工具：

- **C 预处理器**（GCC / clang 均可，用于展开 `.pnml` 中的 `#include` 与宏）
- **nmlc**（NewGRF 编译器，`pip install nml`）
- 构建环境：make / cmake 等（CMake 已配置好 `NML`、`GRF`、`Bundles` 等目标）

简略步骤（以本仓库已验证的手动管线为例）：

```bash
# 1. 计算 REPO_REVISION（自 2000-01-01 起的天数），预处理生成 .nml
gcc -D REPO_REVISION=$(python3 -c "import datetime;print((datetime.datetime.now(datetime.timezone.utc)-datetime.datetime(2000,1,1,tzinfo=datetime.timezone.utc)).days)") \
    -D NEWGRF_VERSION=1.0 -C -E -nostdinc -x c-header \
    -o bin/WorldAirlinersSet.nml WAS.pnml

# 2. 编译为 .grf
nmlc --grf=bin/WorldAirlinersSet.grf -c bin/WorldAirlinersSet.nml
```

更完整的说明见 [从源码构建](docs/guide/building.md)。

> 注意：语言文件（`.lng`）不被 `.pnml` `#include`，而是由 nmlc 在 `lang/` 目录中自动拾取。因此**修改了翻译后必须重新运行 nmlc**，新译文才会被烘焙进 `.grf`。

---

## 翻译说明

本仓库已包含两种中文译文：

- `lang/chinese_simplified.lng` — 简体中文（`##grflangid 0x56`）
- `lang/chinese_traditional.lng` — 繁体中文（`##grflangid 0x62`，采用台湾用字，由 OpenCC `s2tw` 转换 + 台湾航司命名规则生成）

翻译原则：航司与机型以**官方/通用中文名**为准；同国多家航司（如西班牙、委内瑞拉、葡萄牙）靠音译或全称区分，避免玩家在涂装列表里混淆。机型代号（ATR/BAC/波音/空客等）按航空领域惯例保留拉丁原名。

想参与翻译或订正，请参见 [语言翻译](docs/guide/translating.md)。

---

## 许可证与版权

- **代码与图形**：GNU General Public License v3.0，详见 [docs/license.txt](docs/license.txt)。
- **原始图形归属**：大部分飞机图形源自 **PikkaBird** 的 AV8 套装，使用时请为其署名。
- 本中文翻译与文档：同样以 GPL-3.0 发布。

---

## 致谢与链接

- 开发主页：<https://dev.openttdcoop.org/projects/worldairlineset>
- 官方论坛：<http://worldairlinerset.forumotion.com/>
- TT-Forums 讨论帖：<http://www.tt-forums.net/viewtopic.php?t=39227>
- 上游代码仓库：<https://github.com/RvP93/WorldAirlinersSet>

**WAS 团队**（上游）：Beardie、DJNekkid、Frank、Yorick、Faddypainter、RvP93、Aras、Audigex（开发）；EXTSpotter、Dimme、Simozzz、Trainboy2004、Firzafp 等（美术）。

**特别感谢**：PikkaBird（原始图形）、ludde（创造 OpenTTD）、Petern（加入 NewGRF 引擎池，使海量飞机成为可能）、Chris Sawyer（创造 Transport Tycoon），以及所有译者与问题反馈者。

---

*本 README 由中文分支维护，若与上游 `readme.txt` 存在差异，以本文件为准。*
