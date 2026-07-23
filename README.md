# Algo

一份持续生长的中文算法竞赛知识库：从朴素思路到最优解，覆盖基础技巧、数据结构、图论、动态规划、数学与字符串算法。

**在线阅读：[www.wineandchord.com/algo](https://www.wineandchord.com/algo/)**

[![Deploy site](https://github.com/WineChord/algo/actions/workflows/pages.yml/badge.svg)](https://github.com/WineChord/algo/actions/workflows/pages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-8a2942.svg)](LICENSE)

## 内容特点

- 从约束和暴力解出发，解释优化动机，而不是只给模板。
- 同时记录正确性依据、复杂度、易错点、追问与相关题目。
- C++ 实现保持简洁、可读、贴近竞赛现场。
- 通过知识地图、题型索引和双向链接连接零散题目。

## 本地预览

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/check_content.py
mkdocs serve
```

浏览器打开 `http://127.0.0.1:8000/algo/`。生产构建使用：

```bash
mkdocs build --strict
```

## 目录

- `docs/`：网站正文
- `mkdocs.yml`：站点配置与导航
- `scripts/check_content.py`：内容规范检查
- `scripts/check_cpp.py`：逐个编译 C++ 代码块
- `.github/workflows/pages.yml`：GitHub Pages 自动发布

## License

[MIT](LICENSE)
