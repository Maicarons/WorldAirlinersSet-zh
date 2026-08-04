import { defineConfig } from 'vitepress'

const repo = 'Maicarons/WorldAirlinersSet-zh'

export default defineConfig({
  // 部署到 GitHub Pages 项目页（https://<user>.github.io/<repo>/）时，
  // 所有资源/路由必须以仓库名为 base，否则 CSS/JS/图片路径全部 404。
  base: '/WorldAirlinersSet-zh/',
  title: 'World Airliner Set (WAS)',
  description: 'World Airliner Set —— 为 OpenTTD 提供的真实世界客机与涂装 NewGRF 项目中文文档',
  lang: 'zh-CN',
  lastUpdated: true,
  cleanUrls: true,

  head: [
    ['link', { rel: 'icon', href: '/WorldAirlinersSet-zh/logo.png' }],
    // SEO / 社交分享
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'World Airliner Set (WAS) 中文文档' }],
    ['meta', { property: 'og:description', content: '为 OpenTTD 打造的真实世界客机与涂装 NewGRF 项目中文文档' }],
    ['meta', { property: 'og:site_name', content: 'WAS 中文文档' }],
    ['meta', { property: 'og:locale', content: 'zh_CN' }],
    ['meta', { name: 'twitter:card', content: 'summary_large_image' }]
  ],

  themeConfig: {
    logo: '/WorldAirlinersSet-zh/logo.png',

    editLink: {
      pattern: `https://github.com/${repo}/edit/main/docs/:path`,
      text: '在 GitHub 上编辑此页'
    },

    nav: [
      { text: '首页', link: '/' },
      { text: '指南', link: '/guide/introduction' },
      { text: '构建', link: '/guide/building' },
      { text: '贡献', link: '/guide/contributing' },
      {
        text: '外部链接',
        items: [
          { text: '开发主页 (dev.openttdcoop)', link: 'https://dev.openttdcoop.org/projects/worldairlinersset' },
          { text: '本项目 GitHub 仓库', link: `https://github.com/${repo}` },
          { text: '上游仓库 (RvP93)', link: 'https://github.com/RvP93/WorldAirlinersSet' },
          { text: '许可协议 GPL-3.0', link: '/guide/license' }
        ]
      }
    ],

    sidebar: {
      '/guide/': [
        {
          text: '入门',
          items: [
            { text: '项目简介', link: '/guide/introduction' },
            { text: '安装与使用', link: '/guide/installation' },
            { text: 'NewGRF 参数', link: '/guide/parameters' }
          ]
        },
        {
          text: '开发',
          items: [
            { text: '项目结构', link: '/guide/project-structure' },
            { text: '从源码构建', link: '/guide/building' },
            { text: '涂装与图形', link: '/guide/liveries' },
            { text: '语言翻译', link: '/guide/translating' }
          ]
        },
        {
          text: '项目信息',
          items: [
            { text: '贡献指南', link: '/guide/contributing' },
            { text: '更新日志', link: '/guide/changelog' },
            { text: '致谢名单', link: '/guide/credits' },
            { text: '许可协议', link: '/guide/license' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: `https://github.com/${repo}` }
    ],

    search: {
      provider: 'local'
    },

    docFooter: {
      prev: '上一页',
      next: '下一页'
    },

    outline: {
      label: '目录',
      level: [2, 3]
    },

    lastUpdatedText: '最后更新',
    darkModeSwitchLabel: '主题',
    sidebarMenuLabel: '菜单',
    returnToTopLabel: '返回顶部',
    langMenuLabel: '多语言'
  }
})
