# 贡献指南

欢迎为 WAS（以及本中文文档分支）做出贡献！无论是修图、加机型、翻译还是改进文档。

## 报告问题（Bug Report）

1. 到开发主页 <https://dev.openttdcoop.org/projects/worldairlinersset> 注册账号。
2. 先查看 **Issues** 标签，确认该问题尚未被报告。
3. 在 **New Issue** 中提交，并尽量包含：
   - WAS 版本号
   - OpenTTD 版本号
   - 复现步骤 / Bug 详情
   - 必要时附上存档与截图
   - 若是「某版本更新后才出现」，请注明**最后一个正常的版本**与**第一个出问题的版本**，便于定位改动

## 提交代码

本仓库（`Maicarons/WorldAirlinersSet-zh`）是上游的中文文档/翻译分支：

- **上游**：<https://github.com/RvP93/WorldAirlinersSet>
- 修改前建议先 `git fetch upstream` 并 rebase，避免与上游大幅偏离。

一般流程：

```bash
git checkout -b my-fix
# 修改源码 / 文档
git commit -m "简述改动"
git push origin my-fix
# 在 GitHub 上发起 Pull Request
```

::: warning 多人游戏兼容性
如果你修改了源码（哪怕只改一个像素），编译出的 `.grf` 将无法与官方版本的 WAS 在多人游戏中兼容，
不同版本的 `grfcodec`/`nmlc` 也会改变校验和。请确保只在「个人使用」或「协调一致的群体」场景下替换。
:::

## 改进本 VitePress 文档

文档位于 `docs/`，用 [VitePress](https://vitepress.dev/) 管理：

- 页面为 `docs/*.md` 与 `docs/guide/*.md`。
- 站点配置在 `docs/.vitepress/config.js`（导航、侧边栏、页脚等）。

本地预览文档：

```bash
npm run docs:dev      # 开发服务器（热更新）
npm run docs:build    # 构建静态站点到 docs/.vitepress/dist
npm run docs:preview  # 本地预览构建结果
```

> 在本机运行 Node 构建时，若遇到沙箱环境注入的安全删除 shim 报错，可在命令前加 `NODE_OPTIONS=""`
> （详见 [从源码构建](/guide/building) 的注意事项）。用户本机正常构建即可，无需此步。

## 贡献类型

| 想贡献什么 | 去哪里 |
| --- | --- |
| 新增/修正机型或涂装 | `src/gfx/` 下对应目录，参考 [涂装与图形](/guide/liveries) |
| 翻译界面文字 | `lang/*.lng`，参考 [语言翻译](/guide/translating) |
| 调整成本/范围等参数 | `src/header.pnml`、`src/basecost.pnml` |
| 改善文档 | `docs/` 下 Markdown 文件 |

返回：[语言翻译 →](/guide/translating) ｜ 下一步：[更新日志 →](/guide/changelog)
