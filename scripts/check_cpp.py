#!/usr/bin/env python3
from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    *sorted((ROOT / "docs").rglob("*.md")),
    *sorted((ROOT / "includes" / "problems").glob("*.md")),
]
FENCE = re.compile(r"^(?P<indent>\s*)```(?:cpp|c\+\+)(?:\s+.*)?$")
HEADERS = """#include <algorithm>
#include <array>
#include <bitset>
#include <cassert>
#include <chrono>
#include <climits>
#include <cmath>
#include <cstdint>
#include <deque>
#include <functional>
#include <iomanip>
#include <iostream>
#include <limits>
#include <map>
#include <numeric>
#include <queue>
#include <random>
#include <set>
#include <stack>
#include <string>
#include <string_view>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
"""

compiler = os.environ.get("CXX")
if not compiler:
    compiler = next((name for name in ("g++", "clang++", "c++") if shutil.which(name)), None)
if not compiler:
    print("未找到 C++ 编译器", file=sys.stderr)
    raise SystemExit(1)

snippets: list[tuple[Path, int, str]] = []
for path in FILES:
    lines = path.read_text(encoding="utf-8").splitlines()
    start = 0
    block: list[str] = []
    in_cpp = False
    skip = False
    indent = ""
    for number, line in enumerate(lines, 1):
        match = FENCE.match(line) if not in_cpp else None
        if match:
            in_cpp = True
            start = number
            block = []
            indent = match.group("indent")
            skip = number > 1 and lines[number - 2].strip() == "<!-- compile:skip -->"
        elif in_cpp and line.strip() == "```":
            if not skip:
                snippets.append((path, start, "\n".join(block) + "\n"))
            in_cpp = False
        elif in_cpp:
            block.append(line[len(indent):] if line.startswith(indent) else line)

failures: list[str] = []
with tempfile.TemporaryDirectory(prefix="algo-cpp-") as directory:
    temp = Path(directory)
    (temp / "bits").mkdir()
    (temp / "bits" / "stdc++.h").write_text(HEADERS, encoding="utf-8")
    for index, (path, line, source) in enumerate(snippets, 1):
        target = temp / f"snippet-{index}.cpp"
        target.write_text(source, encoding="utf-8")
        result = subprocess.run(
            [compiler, "-std=c++23", "-fsyntax-only", "-I", str(temp), str(target)],
            capture_output=True,
            text=True,
        )
        if result.returncode:
            failures.append(f"{path.relative_to(ROOT)}:{line}\n{result.stderr.strip()}")

if failures:
    print("\n\n".join(failures), file=sys.stderr)
    raise SystemExit(1)
print(f"C++ 检查通过：{len(snippets)} 个代码块，编译器 {compiler}")
