# Algo

一份持续生长的算法竞赛知识库：从朴素思路到最优解，覆盖基础技巧、数据结构、图论、动态规划、数学与字符串算法。

**在线阅读：[www.wineandchord.com/algo](https://www.wineandchord.com/algo/)**

[![Deploy site](https://github.com/WineChord/algo/actions/workflows/pages.yml/badge.svg)](https://github.com/WineChord/algo/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-8a2942.svg)](LICENSE)

## 内容特点

- 从约束和暴力解出发，解释优化动机，而不是只给模板。
- 每道在线评测题都可点击展开题意、思路、复杂度与完整 C++ 实现。
- 同时记录正确性依据、复杂度、易错点、追问与相关题目。
- C++ 实现保持简洁、可读、贴近竞赛现场。
- 通过知识地图、题型索引和双向链接连接零散题目。
- 每日 14 题档案按日期保存完整训练批次，并与稳定知识专题互相链接。

## 本地预览

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm ci
python scripts/check_content.py
python scripts/check_daily_archive.py
python scripts/check_typography.py
python scripts/check_figures.py
python scripts/check_cpp.py
python scripts/check_rendering.py
mkdocs build --strict
python scripts/check_figures.py --site-dir site
python scripts/check_rendering.py --site-dir site --browser
mkdocs serve
```

浏览器打开 `http://127.0.0.1:8000/algo/`。

## 目录

- `docs/`：网站正文
- `docs/daily/`：按工作日期生成的每日 14 题完整档案
- `docs/assets/figures/`：可复现 SVG 图示与来源清单
- `includes/problems/`：可跨专题复用的折叠题目详情
- `mkdocs.yml`：站点配置与导航
- `scripts/check_content.py`：内容规范检查
- `scripts/publish_daily_archive.py`：从每日规范源生成档案页面、日期索引与导航
- `scripts/check_daily_archive.py`：校验日期顺序、每日账目、完整页面与专题链接
- `scripts/check_typography.py`：中英文、数字、单位与全角标点排版检查
- `scripts/render_visuals.py`：确定性生成站内 SVG 图示与哈希清单
- `scripts/check_figures.py`：校验图示安全性、来源、页面锚点与构建结果
- `scripts/check_cpp.py`：逐个编译 C++ 代码块
- `scripts/check_rendering.py`：校对 Markdown、公式、构建产物与浏览器渲染
- `.github/workflows/pages.yml`：GitHub Pages 自动发布

## License

[MIT](LICENSE)
