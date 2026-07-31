# NewGRF 参数

WAS 在 `.grf` 中定义了若干个可调参数（GRF parameters），可在 NewGRF 设置窗口中调整，
用以改变全机队的飞行范围、造价与运营成本等行为。

参数定义位于 [`src/header.pnml`](https://github.com/RvP93/WorldAirlinersSet/blob/master/src/header.pnml)。

## 参数一览

| 参数位 | 名称 | 类型 | 取值范围 | 默认值 | 说明 |
| --- | --- | --- | --- | --- | --- |
| `param 0` | `enable_standard_planes` | 布尔（bool） | 0 / 1 | `0`（关闭） | 是否启用所有标准飞机 |
| `param 1` | `BCosts`（基础造价系数） | 整数（int） | 0 – 8 | `4` | 控制**购买造价**变化（0 = 1/16，4 = 不变，8 = ×16） |
| `param 2` | `RCosts`（基础运营成本系数） | 整数（int） | 0 – 8 | `4` | 控制**运营成本**变化（0 = 1/16，4 = 不变，8 = ×16） |
| `param 3` | `Ranges`（飞行范围） | 整数（int） | 0 – 2 | `1` | 为所有飞机关闭 / 启用飞行范围（详见下表） |

## 飞行范围（Ranges）取值含义

| 取值 | 含义 | 效果 |
| --- | --- | --- |
| `0` | Ranges Off | 关闭飞行范围限制（所有飞机 `range: 0`） |
| `1` | Normal Ranges（默认） | 启用正常飞行范围 |
| `2` | Long Ranges | 启用「远程」飞行范围（约为正常的 1.5 倍） |

> 示例：ATR 42-300 在正常范围下 `range: 165`，在远程模式下被放大到 `range: 245`，关闭时为 `0`。

## 造价 / 运营成本系数（BCosts / RCosts）

这两个参数调节整组飞机的**价格**与**日常运营成本**：

- `0` → 1/16（最便宜）
- `4` → 不变（基准，默认值）
- `8` → ×16（最贵）

它们通过 NewGRF 在每架飞机的 `cost_factor` / `purchase_running_cost_factor` 计算时整体缩放，
方便你平衡游戏经济。

## 如何调整

在 OpenTTD 的 **NewGRF 设置**窗口中选中 World Airliner Set，点击「参数（Parameters）」，
即可逐项修改并实时查看说明文本（这些说明来自 [`lang/*.lng`](https://github.com/RvP93/WorldAirlinersSet/tree/master/lang)）。

返回：[项目简介 →](/guide/introduction) ｜ 下一步：[项目结构 →](/guide/project-structure)
