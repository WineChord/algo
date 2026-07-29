#!/usr/bin/env python3
"""Validate chronological daily-archive structure, content, and navigation."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT / "docs" / "daily"
MANIFEST = ARCHIVE / "archive.json"
MKDOCS = ROOT / "mkdocs.yml"
TOP_KEY = re.compile(r"^leetcode-top-(\d+)-lc\d+$")
LEETCODE_KEY = re.compile(r"lc(\d+)$")
PRIVATE = (
    "/Users/",
    "{{ALGO_STATUS}}",
    "语义无关占位",
    "奇怪变量",
    "for this workflow",
    "local compilation and testing only",
    "邮件发送后",
    "投递状态",
)
EMAIL_ADDRESS = re.compile(
    r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+\b"
)
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


if not MANIFEST.is_file():
    fail("docs/daily/archive.json does not exist")
    payload: dict[str, object] = {"dates": []}
else:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))

dates = payload.get("dates")
if payload.get("version") != 1 or not isinstance(dates, list):
    fail("daily archive manifest must use version 1 and a dates array")
    dates = []

date_values = [str(entry.get("date")) for entry in dates if isinstance(entry, dict)]
if date_values != sorted(date_values, reverse=True):
    fail("daily archive dates must be newest first")
if len(date_values) != len(set(date_values)):
    fail("daily archive dates must be unique")

all_pages: set[Path] = set()
all_keys: set[tuple[str, str]] = set()
expected_nav_lines = [
    "  # DAILY_ARCHIVE_NAV_START",
    "  - 每日 14 题:",
    "      - 总览: daily/index.md",
]
for entry in dates:
    if not isinstance(entry, dict):
        fail("daily archive date entry must be an object")
        continue
    work_date = str(entry.get("date"))
    items = entry.get("items")
    if not isinstance(items, list) or len(items) != 14:
        fail(f"{work_date}: expected exactly 14 items")
        continue
    kinds = [str(item.get("kind")) for item in items if isinstance(item, dict)]
    expected_kinds = [
        "AtCoder",
        *(["力扣 Top"] * 10),
        "力扣竞赛",
        "Codeforces",
        "力扣每日一题",
    ]
    if kinds != expected_kinds:
        fail(f"{work_date}: invalid 1+10+1+1+1 item order")
    positions = [item.get("position") for item in items if isinstance(item, dict)]
    if positions != list(range(1, 15)):
        fail(f"{work_date}: positions must be 1 through 14")
    titles = [str(item.get("title")) for item in items if isinstance(item, dict)]
    if len(titles) != len(set(titles)):
        fail(f"{work_date}: subjects must be unique")
    top_ranks = []
    for item in items:
        if not isinstance(item, dict):
            fail(f"{work_date}: item must be an object")
            continue
        key = str(item.get("key"))
        marker = (work_date, key)
        if marker in all_keys:
            fail(f"{work_date}: duplicate key {key}")
        all_keys.add(marker)
        if item.get("kind") == "力扣 Top":
            match = TOP_KEY.fullmatch(key)
            if not match:
                fail(f"{work_date}: malformed Top key {key}")
            else:
                top_ranks.append(int(match.group(1)))
        page_name = str(item.get("page"))
        page = ARCHIVE / work_date / page_name
        all_pages.add(page.resolve())
        leetcode = LEETCODE_KEY.search(key)
        if leetcode:
            canonical = ROOT / "includes" / "problems" / f"lc-{leetcode.group(1)}.md"
        else:
            canonical = ROOT / "includes" / "problems" / f"{key}.md"
        if not canonical.is_file():
            fail(
                f"{work_date}/{key}: canonical problem snippet does not exist at "
                f"{canonical.relative_to(ROOT)}"
            )
        if not page.is_file():
            fail(f"{page.relative_to(ROOT)}: page does not exist")
            continue
        text = page.read_text(encoding="utf-8")
        title_heading = re.compile(
            rf"^# {re.escape(str(item.get('title')))}$",
            re.MULTILINE,
        )
        if len(title_heading.findall(text)) != 1:
            fail(f"{page.relative_to(ROOT)}: missing unique title heading")
        if not re.search(
            r"官方原始信息|Official source (?:information|record|and metadata)",
            text,
            re.IGNORECASE,
        ):
            fail(f"{page.relative_to(ROOT)}: missing official source information")
        if not re.search(
            r"最优结论|最佳实用解|最优：|最优解|推荐解|推荐统一模板|"
            r"Optimal O?\(|Optimal solution|recommended",
            text,
            re.IGNORECASE,
        ):
            fail(f"{page.relative_to(ROOT)}: missing optimal-solution section")
        if "Reference" not in text:
            fail(f"{page.relative_to(ROOT)}: missing Reference")
        if f'href="index.md"' not in text:
            fail(f"{page.relative_to(ROOT)}: missing date-index return link")
        if str(item.get("official")) not in text:
            fail(f"{page.relative_to(ROOT)}: missing official problem link")
        if str(item.get("topic")) not in text:
            fail(f"{page.relative_to(ROOT)}: missing canonical-topic link")
        if text.count("```cpp") < 2:
            fail(f"{page.relative_to(ROOT)}: expected at least two complete C++ blocks")
        for private in PRIVATE:
            if private.lower() in text.lower():
                fail(f"{page.relative_to(ROOT)}: contains private marker {private!r}")
        if EMAIL_ADDRESS.search(text):
            fail(f"{page.relative_to(ROOT)}: contains an email address")
        if re.search(r"提交 [`0-9a-f]{7,}", text):
            fail(f"{page.relative_to(ROOT)}: contains private submission evidence")
    if top_ranks and top_ranks != list(range(top_ranks[0], top_ranks[0] + 10)):
        fail(f"{work_date}: Top ranks must be ten consecutive values")
    date_index = ARCHIVE / work_date / "index.md"
    if not date_index.is_file():
        fail(f"{work_date}: missing date index")
    else:
        date_text = date_index.read_text(encoding="utf-8")
        for item in items:
            if isinstance(item, dict) and str(item.get("page")) not in date_text:
                fail(f"{date_index.relative_to(ROOT)}: missing {item.get('page')}")
    expected_nav_lines.append(f'      - "{work_date}":')
    expected_nav_lines.append(f"          - 当日总览: daily/{work_date}/index.md")
    for item in items:
        if not isinstance(item, dict):
            continue
        title = json.dumps(str(item.get("title")), ensure_ascii=False)
        expected_nav_lines.append(
            f"          - {title}: daily/{work_date}/{item.get('page')}"
        )

expected_nav_lines.append("  # DAILY_ARCHIVE_NAV_END")
mkdocs_text = MKDOCS.read_text(encoding="utf-8")
expected_nav = "\n".join(expected_nav_lines)
if expected_nav not in mkdocs_text:
    fail("mkdocs.yml daily archive navigation does not match the manifest")

actual_pages = {
    path.resolve()
    for path in ARCHIVE.glob("20??-??-??/*.md")
    if path.name != "index.md"
}
for page in sorted(actual_pages - all_pages):
    fail(f"{page.relative_to(ROOT)}: page is absent from archive.json")
for page in sorted(all_pages - actual_pages):
    fail(f"{page.relative_to(ROOT)}: manifest page is absent from docs")

archive_index = ARCHIVE / "index.md"
if not archive_index.is_file():
    fail("docs/daily/index.md does not exist")
else:
    index_text = archive_index.read_text(encoding="utf-8")
    for work_date in date_values:
        if f"[{work_date}]({work_date}/index.md)" not in index_text:
            fail(f"docs/daily/index.md: missing {work_date}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"每日档案检查通过：{len(date_values)} 个日期，{len(all_pages)} 道完整题解")
