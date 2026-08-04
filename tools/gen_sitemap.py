#!/usr/bin/env python3
"""生成 VitePress 构建产物（dist）的 sitemap.xml 与 robots.txt。

用法: python tools/gen_sitemap.py
需在 `vitepress build` 之后运行，因为要先扫 docs/.vitepress/dist 下的 .html。

约定：
- VitePress 开启了 cleanUrls，路由形如 /guide/installation -> 实际文件 installation.html
- 首页 index.html -> 站点根
- 站点 base 为 /WorldAirlinersSet-zh/（部署到 GitHub Pages 项目页）
"""
import os

DIST = os.path.join(os.path.dirname(__file__), "..", "docs", ".vitepress", "dist")
BASE = "/WorldAirlinersSet-zh/"
SITE = "https://maicarons.github.io"

# 不希望被收录的页面（如有）
EXCLUDE = set()


def iter_html(root):
    for dirpath, _, files in os.walk(root):
        for fn in files:
            if fn.endswith(".html"):
                yield os.path.join(dirpath, fn)


def url_for(html_path):
    rel = os.path.relpath(html_path, DIST).replace(os.sep, "/")
    if rel == "index.html":
        route = ""
    else:
        route = rel[: -len(".html")]
        # 去掉末尾的 /index（cleanUrls 下 xxx/index.html -> /xxx）
        if route.endswith("/index"):
            route = route[: -len("/index")]
    return BASE + route


def main():
    if not os.path.isdir(DIST):
        raise SystemExit("dist 目录不存在: %s，请先运行 vitepress build" % os.path.abspath(DIST))

    urls = []
    for p in iter_html(DIST):
        u = url_for(p)
        if u in EXCLUDE:
            continue
        urls.append(u)
    urls.sort()

    # sitemap.xml
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for u in urls:
        lines.append("  <url>")
        lines.append("    <loc>%s</loc>" % u)
        lines.append("  </url>")
    lines.append("</urlset>")
    sitemap = "\n".join(lines) + "\n"
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap)

    # robots.txt
    robots = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "Sitemap: %s%s\n" % (SITE, BASE + "sitemap.xml")
    )
    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots)

    print("已生成 sitemap.xml (%d 条) 与 robots.txt -> %s" % (len(urls), os.path.abspath(DIST)))


if __name__ == "__main__":
    main()
