# 项目简介

## WAS 是什么

**WAS（World Airliner Set，世界客机集）** 是一个为 [OpenTTD](https://www.openttd.org/) 开发的
**NewGRF**（New Graphics Resource File，新图形资源包）。它的核心目标是：

> 把现实世界中近期与历史上的客机、货机带进 OpenTTD，并让每架飞机都能改装成真实航空公司的涂装。

WAS 与普通的「飞机替换包」最大的区别在于——它不只替换飞机外形，而是把**真实涂装**作为可改装项
（cargo subtype）提供。你在购买飞机后，点击「改装（Refit）」按钮，就能在货物列表里看到一排涂装名称，
选择其一即可让这架飞机披上对应航空公司的外观。

## 历史与来源

- 大部分原始飞机图形由 **PikkaBird** 绘制，最初随 **AV8** 套装发布。
- WAS 团队在 AV8 的基础上加入真实涂装，并自行绘制了部分机型。
- 使用本套装时，请务必为 **PikkaBird** 署名。

## 技术能力

| 能力 | 说明 |
| --- | --- |
| 机型数量 | 最多可包含 **65535** 架（OpenTTD 引入 NewGRF 引擎池后支持，需 OpenTTD > 0.7.0） |
| 真实涂装 | 每架飞机对应一组真实航空公司涂装，通过改装（refit）切换 |
| 兼容性 | 可与其他飞机 NewGRF 同时加载；**不支持 TTDPatch** |
| 语言 | 内置 14 种语言（含简体中文），界面文字随游戏语言变化 |
| 音效 | 内置涡桨/喷气起降音效（`.wav`） |

## 已知限制（Known Issues）

WAS 仍有一些尚未处理的问题，开发团队已知悉，通常无需再重复反馈。更完整的已知问题清单，
请参考上游发布对应的 wiki 页面：
<http://dev.openttdcoop.org/projects/worldairlinersset/wiki>

## 计划中功能（Future Features）

以下功能计划在后续的 Beta 版本中加入：

- **ECS/FIRS 兼容性**（与新经济系统/工业替换集对接）
- **购买飞机时随机涂装选择**
- **Skylift 150 广告涂装**
- **购买列表（purchase list）中更清晰的图片**

## 联系与社区

- 开发主页：<https://dev.openttdcoop.org/projects/worldairlinersset>
- 官方论坛：<http://worldairlinerset.forumotion.com/>
- tt-forums 讨论串：<http://www.tt-forums.net/viewtopic.php?t=39227>

## 上游与本项目分支

- 上游仓库：`RvP93/WorldAirlinersSet`（<https://github.com/RvP93/WorldAirlinersSet>）
- 本仓库（中文文档/翻译分支）：`Maicarons/WorldAirlinersSet-zh`

下一步：[安装与使用 →](/guide/installation)
