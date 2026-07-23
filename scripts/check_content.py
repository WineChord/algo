#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
FENCE = re.compile(r"^```(?:cpp|c\+\+)(?:\s+.*)?$")
errors: list[str] = []

for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_cpp = False
    fence_line = 0
    for number, line in enumerate(lines, 1):
        if not in_cpp and FENCE.match(line):
            in_cpp = True
            fence_line = number
            continue
        if in_cpp and line == "```":
            in_cpp = False
            continue
        if in_cpp and not line.strip():
            errors.append(f"{path.relative_to(ROOT)}:{number}: C++ 代码块不能包含空行（起始于第 {fence_line} 行）")
        if "leetcode.com" in line:
            errors.append(f"{path.relative_to(ROOT)}:{number}: 请链接到 leetcode.cn")
    if in_cpp:
        errors.append(f"{path.relative_to(ROOT)}:{fence_line}: C++ 代码块未闭合")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"内容检查通过：{len(FILES)} 个 Markdown 文件")
