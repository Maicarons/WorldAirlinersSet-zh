---
layout: home

hero:
  name: "World Airliner Set"
  text: "WAS 文档中心"
  tagline: 为 OpenTTD 打造的真实世界客机与涂装 NewGRF 项目
  actions:
    - theme: brand
      text: 项目简介
      link: /guide/introduction
    - theme: alt
      text: 从源码构建
      link: /guide/building

features:
  - title: 真实客机 + 真实涂装
    details: 收录 140+ 种真实世界客机/货机型号，并可改装（refit）为对应航空公司的真实涂装。
    icon: ✈️
  - title: 基于 NewGRF + NML
    details: 使用 NML 语言编写，通过 C 预处理器组织 1000 多个源文件，由 CMake 驱动一站式构建。
    icon: 🛠️
  - title: 多语言支持
    details: 内置 14 种语言文件（含简体中文），可在游戏中以玩家语言显示飞机与涂装的本地化名称。
    icon: 🌐
  - title: GPL-3.0 开源
    details: 项目以 GNU General Public License v3.0 发布，欢迎自由学习、修改与再分发。
    icon: ⚖️
---

## World Airliner Set（WAS）是什么？

**WAS（World Airliner Set，世界客机集）** 是一个 [OpenTTD](https://www.openttd.org/) 的 **NewGRF**（新图形资源包）。
它的目标是把现实世界中近期与历史上的客机与货机带进 OpenTTD，并且让每一架飞机都能改装（refit）成
对应航空公司的**真实涂装**。

- 大部分原始飞机图形由 **PikkaBird** 创作，最初包含在 AV8 套装中；WAS 在此之上加入了真实涂装，
  部分机型也由 WAS 团队自行绘制。
- WAS 最多可包含 **65535** 架飞机（得益于 OpenTTD 对 NewGRF 引擎池的支持），
  而不再受旧版 48 架的限制。
- 可以与其它飞机 NewGRF 同时加载，互不冲突。

> 本项目仓库 `Maicarons/WorldAirlinersSet-zh` 是上游 `RvP93/WorldAirlinersSet` 的中文翻译与文档分支，
> 文档以简体中文编写，并采用 VitePress 进行管理。

## 快速导航

| 你想做的事 | 去这里 |
| --- | --- |
| 了解项目背景与目标 | [项目简介](/guide/introduction) |
| 把 WAS 装进 OpenTTD 玩游戏 | [安装与使用](/guide/installation) |
| 了解可调节的游戏参数 | [NewGRF 参数](/guide/parameters) |
| 搞清楚目录里都是什么 | [项目结构](/guide/project-structure) |
| 从源码自己编译 `.grf` | [从源码构建](/guide/building) |
| 给飞机加涂装 / 画图 | [涂装与图形](/guide/liveries) |
| 帮忙翻译界面文字 | [语言翻译](/guide/translating) |
| 提交代码或反馈问题 | [贡献指南](/guide/contributing) |

## 许可证

WAS 以 **GNU General Public License version 3.0** 发布。详情见 [许可协议](/guide/license)。
使用本套装时，请务必为原作者 **PikkaBird** 署名（大部分图形来自其 AV8 套装）。
