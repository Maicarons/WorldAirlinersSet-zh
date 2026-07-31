# 涂装与图形

WAS 最大的特色是「真实涂装」。本页介绍飞机图形与涂装是如何组织、渲染和切换的。

## 核心概念

- 每架飞机（一个 `.pnml` 文件）定义若干 **spriteset（精灵集）**，分别对应不同的飞行状态：
  `Flight`（飞行）、`Grounded`（地面）、`Climbing`（爬升）、`Touchdown`（触地）、`Landing`（降落）。
- 每一种**涂装**对应一组独立的精灵集（如 `ATR_42_300_AerLingusRegional_Flight`），引用各自独立的 PNG 文件。
- 涂装切换通过 **cargo_subtype** 实现：改装（refit）时选择的「货物项」实际上就是涂装编号，
  而每个涂装名字由 `cargotable.pnml` 中定义的 `STR_VLIV_*` 字符串提供。

## 一个机型的文件构成

以 `src/gfx/ATR/ATR42/42-300/` 为例：

```text
42-300/
├── (0)Greyscale.png        # 灰阶基底（cargo_subtype 0）
├── AerLingusRegional.png   # 涂装 1
├── AirSouthwest.png        # 涂装 2
├── AurignyAirServices.png  # 涂装 3
├── ...                     # 更多航空公司涂装
└── 42-300.pnml             # 飞机逻辑
```

## `.pnml` 中的工作方式（节选）

`42-300.pnml` 用一个宏定义了每个状态下 8 帧精灵的取图位置：

```c
#define ATR_42_300_sprite_layout_template(name)        \
spriteset (name##_Flight, IMAGEFILE)                   \
{                                                      \
  [  1, 1, 46, 22, -23, -11, ANIM]                     \
  [ 52, 1, 38, 19, -19, -10, ANIM]                     \
  ...                                                  \
}                                                      \
spriteset (name##_Grounded, IMAGEFILE) { ... }         \
spriteset (name##_Climbing, IMAGEFILE) { ... }         \
spriteset (name##_Touchdown, IMAGEFILE) { ... }        \
spriteset (name##_Landing,  IMAGEFILE) { ... }
```

随后为每个涂装切换 `IMAGEFILE` 宏并实例化模板：

```c
#define IMAGEFILE "src/gfx/ATR/ATR42/42-300/(0)Greyscale.png"
purchase_sprite(ATR_42_300, 285, 1, 46, 23, -23, -12)
ATR_42_300_sprite_layout_template(ATR_42_300_Greyscale)
#undef IMAGEFILE

#define IMAGEFILE "src/gfx/ATR/ATR42/42-300/AerLingusRegional.png"
ATR_42_300_sprite_layout_template(ATR_42_300_AerLingusRegional)
#undef IMAGEFILE
```

状态切换由 `flight_state()` 宏（读取车辆变量 `0xE2`）驱动：

```c
switch (FEAT_AIRCRAFT, SELF, ATR_42_300_Greyscale, flight_state())
{
  15: ATR_42_300_Greyscale_Climbing;
  18: ATR_42_300_Greyscale_Flight;
  21: ATR_42_300_Greyscale_Landing;
  22: ATR_42_300_Greyscale_Touchdown;
      ATR_42_300_Greyscale_Grounded;
}
```

而「选择哪个涂装」由 `cargo_subtype` 决定：

```c
switch (FEAT_AIRCRAFT, SELF, ATR_42_300_sprites, cargo_subtype)
{
  1: ATR_42_300_AerLingusRegional;
  2: ATR_42_300_AirSouthwest;
  ...
     ATR_42_300_Greyscale;   // 默认灰阶
}
```

## 如何新增一个涂装

1. 在对应机型目录下放入一张 PNG（尺寸需与现有涂装一致，通常为水平拼接的多帧精灵表）。
2. 在 `.pnml` 中新增一组 `IMAGEFILE` + 模板实例化（参考现有涂装写法）。
3. 在 `cargotable.pnml` 中为该涂装定义一个 `STR_VLIV_*` 字符串。
4. 在机型 `.pnml` 的 `cargo_subtype` 切换中为新涂装分配一个编号，并在 `cargo_subtype_text` /
   `cargo_subtype_capacity` 中补充对应的显示文本与（货机）容量。
5. 在 `lang/*.lng` 中为新字符串提供各语言翻译。

## 灰阶（Greyscale）

`greyscales/` 目录保存了各机型的灰阶 PNG，作为不带航空公司标识的基础外观（`(0)Greyscale.png`）。
它是所有机型的 `cargo_subtype 0`，也是绘制新涂装时的常用底图。

返回：[从源码构建 →](/guide/building) ｜ 下一步：[语言翻译 →](/guide/translating)
