# 安装与使用

## 支持的版本

WAS 目前**仅支持 OpenTTD > 0.7.0**，因为该版本引入了对更多车辆模型的支持，使 NewGRF 可包含多达
65535 架飞机。WAS **不支持 TTDPatch**（原因同上）。

WAS 可以与其它飞机 NewGRF 同时加载，互不冲突。

## 获取 WAS

- **稳定版**：通过游戏内 **BaNaNaS** 内容下载器获取（仅含稳定版本）。
- **最新构建**：从开发主页下载 nightly 构建的 `.tar` 包。
- **源码编译**：见 [从源码构建](/guide/building)。

## 安装方式

### 方式一：手动安装

1. 从开发主页下载 `.tar` 包。
2. 将其放入 OpenTTD 的 `data` 目录：
   - **Windows**：通常是 `文档/OpenTTD` 文件夹。
3. 如果没有 `.tar` 文件，把下载的 `.zip` 解压到 `data` 目录即可。

### 方式二：通过 BaNaNaS 安装

1. 打开 OpenTTD 的「内容下载（Content）」列表。
2. 找到 **World Airliner Set** 条目，点击「下载（Download）」。

## 在游戏中启用

1. 打开 **NewGRF 设置**窗口。
2. 点击「添加（Add）」。
3. 在列表中选择 **World Airliner Set**。
4. 应用设置并启动或重载游戏。

## 使用 WAS

使用非常简单：

1. 建造你想要的飞机。
2. 点击**改装（Refit）**按钮，你会看到一列货物（cargo），每一项后面都带有对应的涂装名称。
3. 列表中第一个涂装通常是 **Greyscale（灰阶）**。
4. 选择某个涂装，点击「改装车辆（Refit Vehicle）」即可应用。

::: tip
Greyscale 是默认的灰阶基底涂装，不带任何航空公司标识，适合自定义或作为基础外观。
:::

下一步：[了解 NewGRF 参数 →](/guide/parameters)
