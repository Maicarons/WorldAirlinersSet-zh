# 下载模型

WAS 的核心产物是一个 **NewGRF 资源包文件** `WorldAirlinersSet.grf`，它包含了本项目收录的全部飞机模型与真实涂装，可直接放入 OpenTTD 使用。下面提供几种获取方式，按需选择。

<p align="center">
  <a class="download-btn" href="https://github.com/Maicarons/WorldAirlinersSet-zh/releases/latest" target="_blank" rel="noopener">
    ⬇️ 下载最新版 WorldAirlinersSet.grf
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/github/v/release/Maicarons/WorldAirlinersSet-zh?label=%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC&color=blue" alt="最新版本" />
  <img src="https://img.shields.io/github/downloads/Maicarons/WorldAirlinersSet-zh/total?label=%E6%80%BB%E4%B8%8B%E8%BD%BD%E9%87%8F" alt="总下载量" />
</p>

## 方式一：下载 Release（推荐，含中文）

从本仓库的 GitHub Release 获取编译好的 `.grf` 文件，包含完整简体 / 繁体中文界面。点击上方的蓝色按钮会 **自动跳转到最新版本的 Release 页面**，在其中下载 `WorldAirlinersSet.grf` 即可。

也可手动前往：

- 📦 最新版（自动定位）：[WorldAirlinersSet.gh releases/latest](https://github.com/Maicarons/WorldAirlinersSet-zh/releases/latest)
- 🗂 全部历史版本：[Releases 列表](https://github.com/Maicarons/WorldAirlinersSet-zh/releases)

下载后放入 OpenTTD 的 `newgrf` 目录即可，详见下方「安装到 OpenTTD」或 [安装与使用](/guide/installation)。

## 方式二：从 BaNaNaS 下载（仅稳定版，英文）

在 OpenTTD 游戏内的「内容下载（Content）」列表中搜索 **World Airliner Set**，点击「下载」。该渠道提供上游英文原版，**不含中文翻译**。

## 方式三：从源码自行构建

如果你想获取最新的未发布改动，或自行修改机型与涂装，可参考 [从源码构建](/guide/building) 自行编译 `.grf`。

## 安装到 OpenTTD

1. 将 `WorldAirlinersSet.grf` 放入 OpenTTD 的 `newgrf` 文件夹：
   - **Windows**：`文档/OpenTTD/newgrf`
   - **其他系统**：OpenTTD 用户数据目录下的 `newgrf`
2. 打开 OpenTTD →「新图形」→「添加」，选择 **World Airliner Set** 并启用。
3. 在语言设置中选择 **简体中文** 或 **繁体中文**，中文名称即可显示。

::: tip
Greyscale 是默认的灰阶基底涂装，不带任何航空公司标识，适合作为基础外观。
:::

## 常见问题

**Q：下载后游戏里看不到中文？**
A：需要在 OpenTTD 的语言设置中切换为简体 / 繁体中文，中文名称才会生效。

**Q：版本过低无法加载？**
A：WAS 需要 OpenTTD 1.2.0 及以上（含中文界面）。请升级 OpenTTD 后再试。

**Q：能否与其他飞机 NewGRF 同时使用？**
A：可以，WAS 与其他飞机 NewGRF 互不冲突。

<style>
.download-btn {
  display: inline-block;
  padding: 14px 28px;
  font-size: 1.1rem;
  font-weight: 600;
  color: #fff !important;
  background: #2563eb;
  border-radius: 10px;
  text-decoration: none !important;
  box-shadow: 0 4px 14px rgba(37, 99, 235, 0.35);
  transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.download-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(37, 99, 235, 0.45);
}
</style>
