#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = sorted((ROOT / "docs").rglob("*.md"))
PROBLEMS = sorted((ROOT / "includes" / "problems").glob("*.md"))
FILES = [ROOT / "README.md", *DOCS, *PROBLEMS]
FENCE = re.compile(r"^\s*```(?:cpp|c\+\+)(?:\s+.*)?$", re.MULTILINE)
PROBLEM_URL = re.compile(
    r"https://leetcode\.cn/problems/[a-z0-9-]+/"
    r"|https://www\.luogu\.com\.cn/problem/[A-Za-z0-9]+"
    r"|https://(?:www\.)?codeforces\.com/(?:contest/\d+/problem/[A-Za-z0-9]+|problemset/problem/\d+/[A-Za-z0-9]+)"
    r"|https://atcoder\.jp/contests/[A-Za-z0-9_-]+/tasks/[A-Za-z0-9_-]+"
    r"|https://ac\.nowcoder\.com/acm/problem/\d+"
    r"|https://www\.acwing\.com/problem/content/\d+/"
)
SNIPPET = re.compile(r'--8<-- "(includes/problems/[^"]+\.md)"')
PROBLEM_ANCHOR = re.compile(
    r'^<div class="problem-anchor" id="(problem-[a-z0-9-]+)"></div>$'
)
MARKDOWN_LINK = re.compile(r"\[([^\]\n]+)\]\(([^)\n]+)\)")
CHANGELOG_PROBLEM_LABEL = re.compile(
    r"LeetCode\s+\d+"
    r"|AtCoder\s+ABC\d+\s+[A-Z]\b"
    r"|\b\d{4}[A-Z]\b"
    r"|第\s*\d+\s*场周赛\s*Q\d+"
)
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
        if in_cpp and line.strip() == "```":
            in_cpp = False
            continue
        if in_cpp and not line.strip():
            errors.append(f"{path.relative_to(ROOT)}:{number}: C++ 代码块不能包含空行（起始于第 {fence_line} 行）")
        if "leetcode.com" in line:
            errors.append(f"{path.relative_to(ROOT)}:{number}: 请链接到 leetcode.cn")
    if in_cpp:
        errors.append(f"{path.relative_to(ROOT)}:{fence_line}: C++ 代码块未闭合")

referenced: set[Path] = set()
for path in [ROOT / "README.md", *DOCS]:
    text = path.read_text(encoding="utf-8")
    if PROBLEM_URL.search(text):
        errors.append(f"{path.relative_to(ROOT)}: 题目原始链接必须放入默认折叠的题目详情片段")
    for snippet in SNIPPET.findall(text):
        target = ROOT / snippet
        if not target.is_file():
            errors.append(f"{path.relative_to(ROOT)}: 引用的题目详情不存在：{snippet}")
        else:
            referenced.add(target.resolve())

required = ("**题意**", "**思路**", "**复杂度**", "**C++ 实现**")
urls: dict[str, Path] = {}
anchors: set[str] = set()
for path in PROBLEMS:
    text = path.read_text(encoding="utf-8")
    if path.resolve() not in referenced:
        errors.append(f"{path.relative_to(ROOT)}: 题目详情未被任何页面引用")
    nonempty = [line for line in text.splitlines() if line.strip()]
    expected_anchor = f"problem-{path.stem}"
    anchor_line = nonempty[0] if nonempty else ""
    anchor_match = PROBLEM_ANCHOR.fullmatch(anchor_line)
    if not anchor_match or anchor_match.group(1) != expected_anchor:
        errors.append(
            f"{path.relative_to(ROOT)}: 首行必须提供稳定锚点 "
            f'<div class="problem-anchor" id="{expected_anchor}"></div>'
        )
    else:
        anchors.add(expected_anchor)
    disclosure = nonempty[1] if len(nonempty) > 1 else ""
    if not disclosure.startswith('??? problem "'):
        errors.append(f"{path.relative_to(ROOT)}: 题目详情必须使用默认折叠的 ??? problem")
    if disclosure.startswith("???+"):
        errors.append(f"{path.relative_to(ROOT)}: 题目详情不得默认展开")
    for marker in required:
        if marker not in text:
            errors.append(f"{path.relative_to(ROOT)}: 缺少 {marker}")
    if not FENCE.search(text):
        errors.append(f"{path.relative_to(ROOT)}: 缺少 C++ 实现代码块")
    found = PROBLEM_URL.findall(text)
    if len(found) != 1:
        errors.append(f"{path.relative_to(ROOT)}: 必须且只能包含一个题目原始链接")
    elif found[0] in urls:
        errors.append(
            f"{path.relative_to(ROOT)}: 与 {urls[found[0]].relative_to(ROOT)} 重复收录同一题目"
        )
    else:
        urls[found[0]] = path

changelog = ROOT / "docs" / "changelog.md"
changelog_text = changelog.read_text(encoding="utf-8")
masked = list(changelog_text)
for match in MARKDOWN_LINK.finditer(changelog_text):
    label, target = match.groups()
    if CHANGELOG_PROBLEM_LABEL.search(label):
        if not target.startswith("problems/index.md#problem-"):
            errors.append(
                f"{changelog.relative_to(ROOT)}:{changelog_text.count(chr(10), 0, match.start()) + 1}: "
                "题目名称应链接到站内题目详情"
            )
        elif target.partition("#")[2] not in anchors:
            errors.append(
                f"{changelog.relative_to(ROOT)}:{changelog_text.count(chr(10), 0, match.start()) + 1}: "
                f"题目详情锚点不存在：{target}"
            )
    for index in range(match.start(), match.end()):
        if masked[index] != "\n":
            masked[index] = " "
unlinked = "".join(masked)
for match in CHANGELOG_PROBLEM_LABEL.finditer(unlinked):
    errors.append(
        f"{changelog.relative_to(ROOT)}:{changelog_text.count(chr(10), 0, match.start()) + 1}: "
        f"题目名称应为可点击的站内详情链接：{match.group(0)}"
    )

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"内容检查通过：{len(DOCS)} 个页面，{len(PROBLEMS)} 个默认折叠题目详情")
