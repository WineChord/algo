#!/usr/bin/env python3
"""Validate chronological daily-archive structure, content, and navigation."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

from daily_language import non_chinese_solution_lines


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
FORBIDDEN_PLACEHOLDERS = (
    "官方英文原文请从上方链接查看",
    "完整官方英文原文请从上方链接查看",
    "Faithful complete statement semantics",
    "Complete statement semantics",
)
CANONICAL_BODY = re.compile(
    r"<!-- DAILY_CANONICAL_BODY_START "
    r"sha256=([0-9a-f]{64}) -->\n"
    r"(.*?)\n"
    r"<!-- DAILY_CANONICAL_BODY_END -->",
    re.DOTALL,
)
FORMULA_REGRESSIONS = {
    "codeforces-2247-a": (
        r"a_i\leftarrow-a_i,\qquad a_{i+1}\leftarrow-a_{i+1}",
    ),
    "atcoder-abc468-c": (
        r"P=(P_1,P_2,\ldots,P_N),\qquad Q=(Q_1,Q_2,\ldots,Q_N)",
        r"P<R<Q",
        r"P\ge Q",
    ),
}
EMAIL_ADDRESS = re.compile(
    r"\b[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@"
    r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
    r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+\b"
)
errors: list[str] = []
RAW_HTML_HREF = re.compile(
    r"<a\b[^>]*\bhref\s*=\s*[\"']([^\"']*)[\"']",
    re.IGNORECASE,
)


def fail(message: str) -> None:
    errors.append(message)


def deployed_route(markdown_href: str, extra_parent_levels: int = 0) -> str:
    parsed = urlparse(markdown_href)
    path = parsed.path
    if not path.endswith(".md"):
        raise ValueError(f"expected Markdown route, found {markdown_href!r}")
    if Path(path).name == "index.md":
        path = path[: -len("index.md")]
    else:
        path = path[:-3] + "/"
    path = "../" * extra_parent_levels + path
    query = f"?{parsed.query}" if parsed.query else ""
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""
    return f"{path}{query}{fragment}"


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
    "  - 每日题目:",
    "      - 总览: daily/index.md",
]
for entry in dates:
    if not isinstance(entry, dict):
        fail("daily archive date entry must be an object")
        continue
    work_date = str(entry.get("date"))
    items = entry.get("items")
    if not isinstance(items, list):
        fail(f"{work_date}: items must be an array")
        continue
    expected_count = entry.get("expected_count", len(items))
    top_count = entry.get(
        "top_count",
        sum(item.get("kind") == "力扣 Top" for item in items if isinstance(item, dict)),
    )
    if (expected_count, top_count) not in {(5, 1), (14, 10)}:
        fail(
            f"{work_date}: expected_count/top_count must be 5/1 or 14/10"
        )
        continue
    if len(items) != expected_count:
        fail(f"{work_date}: expected exactly {expected_count} items")
        continue
    kinds = [str(item.get("kind")) for item in items if isinstance(item, dict)]
    expected_kinds = [
        "AtCoder",
        *(["力扣 Top"] * top_count),
        "力扣竞赛",
        "Codeforces",
        "力扣每日一题",
    ]
    if kinds != expected_kinds:
        fail(f"{work_date}: invalid 1+{top_count}+1+1+1 item order")
    positions = [item.get("position") for item in items if isinstance(item, dict)]
    if positions != list(range(1, expected_count + 1)):
        fail(f"{work_date}: positions must be 1 through {expected_count}")
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
        for placeholder in FORBIDDEN_PLACEHOLDERS:
            if placeholder.casefold() in text.casefold():
                fail(
                    f"{page.relative_to(ROOT)}: contains statement placeholder "
                    f"{placeholder!r}"
                )
        title_heading = re.compile(
            rf"^# {re.escape(str(item.get('title')))}$",
            re.MULTILINE,
        )
        if len(title_heading.findall(text)) != 1:
            fail(f"{page.relative_to(ROOT)}: missing unique title heading")
        if not re.search(
            r"官方原始信息|官方来源(?:信息|与元数据)|"
            r"Official source (?:information|record|and metadata)",
            text,
            re.IGNORECASE,
        ):
            fail(f"{page.relative_to(ROOT)}: missing official source information")
        if not re.search(
            r"最优结论|最佳实用解|最优：|最优.*解|推荐解|推荐统一模板|"
            r"（推荐）|"
            r"Optimal O?\(|Optimal solution|recommended",
            text,
            re.IGNORECASE,
        ):
            fail(f"{page.relative_to(ROOT)}: missing optimal-solution section")
        if not re.search(r"Reference|参考资料", text):
            fail(f"{page.relative_to(ROOT)}: missing Reference")
        if '<a href="../">' not in text:
            fail(f"{page.relative_to(ROOT)}: missing date-index return link")
        if str(item.get("official")) not in text:
            fail(f"{page.relative_to(ROOT)}: missing official problem link")
        if str(item.get("topic")) not in text:
            fail(f"{page.relative_to(ROOT)}: missing canonical-topic link")
        expected_topic_route = deployed_route(str(item.get("topic")), 1)
        if f'href="{expected_topic_route}"' not in text:
            fail(
                f"{page.relative_to(ROOT)}: missing deployed canonical-topic route "
                f"{expected_topic_route}"
            )
        for href in RAW_HTML_HREF.findall(text):
            if not href:
                fail(f"{page.relative_to(ROOT)}: raw HTML link has an empty href")
            if re.search(r"\.md(?:[?#]|$)", href):
                fail(
                    f"{page.relative_to(ROOT)}: raw HTML href uses a source "
                    f"Markdown path instead of a deployed route: {href}"
                )
        kind = str(item.get("kind"))
        for line_number, line in non_chinese_solution_lines(text, kind):
            fail(
                f"{page.relative_to(ROOT)}:{line_number}: solution prose must be "
                f"Chinese outside the AtCoder/Codeforces official English "
                f"statement layer: {line[:120]!r}"
            )
        if kind in {"AtCoder", "Codeforces"}:
            required_statement_parts = (
                "Complete English statement",
                "Input",
                "Output",
                "constraint",
                "sample",
                "中文",
            )
            for part in required_statement_parts:
                if part.casefold() not in text.casefold():
                    fail(
                        f"{page.relative_to(ROOT)}: self-contained contest "
                        f"statement is missing {part!r}"
                    )
            if kind == "AtCoder" and "https://atcoder.jp/tos" not in text:
                fail(
                    f"{page.relative_to(ROOT)}: missing AtCoder copyright boundary"
                )
            if (
                kind == "Codeforces"
                and "https://codeforces.com/blog/entry/967" not in text
            ):
                fail(
                    f"{page.relative_to(ROOT)}: missing Codeforces materials licence"
                )
        for formula in FORMULA_REGRESSIONS.get(key, ()):
            if formula not in text:
                fail(
                    f"{page.relative_to(ROOT)}: formula regression lost "
                    f"{formula!r}"
                )
        source_sha256 = item.get("source_sha256")
        if source_sha256 is not None:
            if not isinstance(source_sha256, str) or not re.fullmatch(
                r"[0-9a-f]{64}",
                source_sha256,
            ):
                fail(f"{page.relative_to(ROOT)}: invalid source_sha256")
            matches = CANONICAL_BODY.findall(text)
            if len(matches) != 1:
                fail(
                    f"{page.relative_to(ROOT)}: expected one canonical body marker"
                )
            else:
                marker_sha256, body = matches[0]
                actual_sha256 = hashlib.sha256(
                    (body + "\n").encode("utf-8")
                ).hexdigest()
                if marker_sha256 != source_sha256:
                    fail(
                        f"{page.relative_to(ROOT)}: marker hash differs from manifest"
                    )
                if actual_sha256 != source_sha256:
                    fail(
                        f"{page.relative_to(ROOT)}: canonical body changed in transit"
                    )
        if text.count("```cpp") < 2:
            fail(f"{page.relative_to(ROOT)}: expected at least two complete C++ blocks")
        for private in PRIVATE:
            if private.lower() in text.lower():
                fail(f"{page.relative_to(ROOT)}: contains private marker {private!r}")
        if EMAIL_ADDRESS.search(text):
            fail(f"{page.relative_to(ROOT)}: contains an email address")
        if re.search(r"提交 [`0-9a-f]{7,}", text):
            fail(f"{page.relative_to(ROOT)}: contains private submission evidence")
    if top_ranks and top_ranks != list(
        range(top_ranks[0], top_ranks[0] + top_count)
    ):
        fail(f"{work_date}: Top ranks must be {top_count} consecutive values")
    date_index = ARCHIVE / work_date / "index.md"
    if not date_index.is_file():
        fail(f"{work_date}: missing date index")
    else:
        date_text = date_index.read_text(encoding="utf-8")
        if f"# {work_date} · 每日题目 " not in date_text:
            fail(f"{date_index.relative_to(ROOT)}: missing current reader-visible title")
        for item in items:
            if not isinstance(item, dict):
                continue
            route = deployed_route(str(item.get("page")))
            if f'href="{route}"' not in date_text:
                fail(f"{date_index.relative_to(ROOT)}: missing deployed route {route}")
        for href in RAW_HTML_HREF.findall(date_text):
            if not href:
                fail(f"{date_index.relative_to(ROOT)}: raw HTML link has an empty href")
            if re.search(r"\.md(?:[?#]|$)", href):
                fail(
                    f"{date_index.relative_to(ROOT)}: raw HTML href uses a source "
                    f"Markdown path instead of a deployed route: {href}"
                )
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
    if not index_text.startswith("# 每日题目\n"):
        fail("docs/daily/index.md: missing current reader-visible title")
    for work_date in date_values:
        if f"[{work_date}]({work_date}/index.md)" not in index_text:
            fail(f"docs/daily/index.md: missing {work_date}")

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)
print(f"每日档案检查通过：{len(date_values)} 个日期，{len(all_pages)} 道完整题解")
