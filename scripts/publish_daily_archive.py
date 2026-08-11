#!/usr/bin/env python3
"""Publish one verified daily work batch into the chronological archive."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

from daily_language import non_chinese_solution_lines


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARCHIVE = DOCS / "daily"
MANIFEST = ARCHIVE / "archive.json"
MKDOCS = ROOT / "mkdocs.yml"
NAV_START = "  # DAILY_ARCHIVE_NAV_START"
NAV_END = "  # DAILY_ARCHIVE_NAV_END"
SITE_PREFIX = "https://www.wineandchord.com/algo/"
PRIVATE_PATTERNS = (
    re.compile(r"/Users/"),
    re.compile(r"@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    re.compile(r"\b(?:prompt|automation|Codex)\b", re.IGNORECASE),
    re.compile(r"语义无关(?:的)?(?:占位|变量)"),
    re.compile(r"奇怪(?:的)?变量"),
)
STATUS_LINE = re.compile(
    r"^(?:已发布到|Algo 状态：|网站状态：|提交\s+[`0-9a-f])"
)
HEADING = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
FENCE = re.compile(r"^\s*(```|~~~)")
CPP_FENCE = re.compile(r"^```(?:cpp|c\+\+)(?:\s+.*)?$")
COMPILE_DIRECTIVE = re.compile(r"^<!-- compile:[a-z-]+ -->$")
TOP_KEY = re.compile(r"^leetcode-top-(\d+)-lc\d+$")
REMOTE_IMAGE = re.compile(
    r"!\[[^\]]*\]\((?:https?:)?//[^)\s]+\)"
    r"|<img\b[^>]*\bsrc\s*=\s*[\"'](?:https?:)?//",
    re.IGNORECASE,
)
FORBIDDEN_SOURCE_TEXT = (
    "官方英文原文请从上方链接查看",
    "完整官方英文原文请从上方链接查看",
    "Faithful complete statement semantics",
    "Complete statement semantics",
)


@dataclass(frozen=True)
class Item:
    key: str
    title: str
    source: Path
    official: str
    topic: str
    kind: str
    position: int

    @property
    def page_name(self) -> str:
        return f"{self.key}.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Asia/Shanghai work date")
    parser.add_argument(
        "--specs",
        action="append",
        required=True,
        type=Path,
        help="JSON array containing key, subject, source, official, and site",
    )
    parser.add_argument(
        "--source-dir",
        action="append",
        default=[],
        type=Path,
        help="Search root for legacy specs without a source field",
    )
    return parser.parse_args()


def load_json_array(path: Path) -> list[dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        payload = payload.get("items") or payload.get("entries")
    if not isinstance(payload, list):
        raise ValueError(f"{path}: specs must be a JSON array")
    result: list[dict[str, object]] = []
    for index, raw in enumerate(payload, 1):
        if not isinstance(raw, dict):
            raise ValueError(f"{path}: item {index} is not an object")
        result.append(raw)
    return result


def classify(key: str) -> tuple[int, str]:
    if key.startswith("atcoder-"):
        return 0, "AtCoder"
    match = TOP_KEY.fullmatch(key)
    if match:
        return 1, "力扣 Top"
    if key.startswith("leetcode-weekly-") or key.startswith("leetcode-biweekly-"):
        return 2, "力扣竞赛"
    if key.startswith("codeforces-"):
        return 3, "Codeforces"
    if key.startswith("leetcode-daily-"):
        return 4, "力扣每日一题"
    raise ValueError(f"unsupported daily archive key: {key}")


def source_candidates(key: str, roots: list[Path]) -> list[Path]:
    names = [f"{key}.md"]
    top = TOP_KEY.fullmatch(key)
    if top:
        leetcode_id = key.rsplit("lc", 1)[1]
        names.append(f"lc-{leetcode_id}.md")
    candidates: list[Path] = []
    for root in roots:
        for name in names:
            candidates.extend(sorted(root.rglob(name)))
    return list(dict.fromkeys(path.resolve() for path in candidates))


def resolve_source(
    raw: dict[str, object],
    key: str,
    roots: list[Path],
) -> Path:
    value = raw.get("source")
    if isinstance(value, str) and value:
        source = Path(value).expanduser().resolve()
        if not source.is_file():
            raise ValueError(f"{key}: source does not exist: {source}")
        return source
    candidates = source_candidates(key, roots)
    if len(candidates) != 1:
        listing = ", ".join(str(path) for path in candidates) or "none"
        raise ValueError(f"{key}: expected one source candidate, found {listing}")
    return candidates[0]


def topic_path(site: str) -> str:
    if not site.startswith(SITE_PREFIX):
        raise ValueError(f"topic URL is outside Algo: {site}")
    parsed = urlparse(site)
    path = parsed.path.removeprefix("/algo/").strip("/")
    if not path:
        return "../index.md"
    candidates = [
        DOCS / f"{path}.md",
        DOCS / path / "index.md",
    ]
    matches = [candidate for candidate in candidates if candidate.is_file()]
    if len(matches) != 1:
        listing = ", ".join(str(candidate.relative_to(ROOT)) for candidate in candidates)
        raise ValueError(f"topic URL does not map to exactly one document: {site} ({listing})")
    relative = matches[0].relative_to(DOCS).as_posix()
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""
    return f"../../{relative}{fragment}"


def typographic_title(title: str) -> str:
    """Normalize reader-visible spacing without changing title semantics."""
    return re.sub(r"第([A-Za-z])个", r"第 \1 个", title)


def validate_math_delimiters(text: str) -> None:
    """Reject legacy delimiters; canonical mathematical source is never repaired."""
    in_fence = False
    for line_number, line in enumerate(text.splitlines(), 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if not in_fence and re.search(r"(?<!\\)\\(?:\(|\)|\[|\])", line):
            raise ValueError(
                f"source line {line_number}: use $...$ or $$...$$; "
                "the publisher does not convert mathematical source"
            )
    if in_fence:
        raise ValueError("unclosed Markdown fence")


def source_error(item: Item, line: int, message: str) -> ValueError:
    return ValueError(f"{item.key}: source line {line}: {message}")


def validate_canonical_source(item: Item, text: str) -> str:
    """Reject unsafe or unfinished source; never rewrite reader-visible content."""
    if "\r" in text:
        raise source_error(item, 1, "use LF line endings")
    if not text.endswith("\n"):
        raise source_error(item, len(text.splitlines()) or 1, "missing final newline")
    if text.startswith("---\n"):
        raise source_error(item, 1, "front matter belongs to the archive shell")
    if text != text.strip("\n") + "\n":
        raise source_error(item, 1, "leading or trailing blank lines are not canonical")
    for phrase in FORBIDDEN_SOURCE_TEXT:
        match_at = text.casefold().find(phrase.casefold())
        if match_at >= 0:
            line = text[:match_at].count("\n") + 1
            raise source_error(item, line, f"replace placeholder text {phrase!r}")
    for pattern in PRIVATE_PATTERNS:
        match = pattern.search(text)
        if match:
            line = text[: match.start()].count("\n") + 1
            raise source_error(
                item,
                line,
                f"private or workflow material matches {pattern.pattern!r}",
            )
    for line_number, line in enumerate(text.splitlines(), 1):
        if STATUS_LINE.match(line.strip()):
            raise source_error(
                item,
                line_number,
                "publication status belongs in private state",
            )
    remote_image = REMOTE_IMAGE.search(text)
    if remote_image:
        line = text[: remote_image.start()].count("\n") + 1
        raise source_error(
            item,
            line,
            "download and verify official images before publication; use a local path",
        )

    lines = text.splitlines()
    first_heading = next(
        (
            (index, match)
            for index, line in enumerate(lines, 1)
            if (match := HEADING.match(line))
        ),
        None,
    )
    if first_heading is None:
        raise source_error(item, 1, "canonical source needs Markdown headings")
    first_line, first_match = first_heading
    if len(first_match.group(1)) != 2:
        raise source_error(
            item,
            first_line,
            "canonical body must begin with a level-2 heading",
        )
    for index, line in enumerate(lines, 1):
        match = HEADING.match(line)
        if match and len(match.group(1)) == 1:
            raise source_error(item, index, "level-1 title belongs to the archive shell")

    in_fence = False
    previous_nonempty = ""
    for index, line in enumerate(lines, 1):
        if FENCE.match(line):
            if not in_fence and CPP_FENCE.match(line):
                if not COMPILE_DIRECTIVE.fullmatch(previous_nonempty):
                    raise source_error(
                        item,
                        index,
                        "every C++ block needs an explicit compile directive",
                    )
            in_fence = not in_fence
            previous_nonempty = line
            continue
        if not in_fence and line.strip():
            previous_nonempty = line
    if in_fence:
        raise source_error(item, len(lines), "unclosed Markdown fence")
    validate_math_delimiters(text)

    if item.official not in text:
        raise source_error(item, 1, "canonical source must contain the official URL")
    if item.kind in {"AtCoder", "Codeforces"}:
        required = (
            "Complete English statement",
            "Input",
            "Output",
            "constraint",
            "sample",
            "中文",
        )
        missing = [label for label in required if label.casefold() not in text.casefold()]
        if missing:
            raise source_error(
                item,
                1,
                "self-contained contest statement is missing " + ", ".join(missing),
            )
        if item.kind == "AtCoder" and "https://atcoder.jp/tos" not in text:
            raise source_error(item, 1, "AtCoder source needs its copyright boundary")
        if (
            item.kind == "Codeforces"
            and "https://codeforces.com/blog/entry/967" not in text
        ):
            raise source_error(item, 1, "Codeforces source needs its usage licence")
    language_errors = non_chinese_solution_lines(text, item.kind)
    if language_errors:
        line_number, line = language_errors[0]
        raise source_error(
            item,
            line_number,
            "solution prose must be Chinese outside the AtCoder/Codeforces "
            f"official English statement layer: {line[:120]!r}",
        )
    return text


def build_items(spec_paths: list[Path], roots: list[Path]) -> list[Item]:
    raw_items: list[dict[str, object]] = []
    for path in spec_paths:
        raw_items.extend(load_json_array(path))
    by_key: dict[str, dict[str, object]] = {}
    for raw in raw_items:
        key = raw.get("key")
        if not isinstance(key, str) or not key:
            raise ValueError("every item needs a non-empty key")
        if key in by_key:
            raise ValueError(f"duplicate key in specs: {key}")
        by_key[key] = raw
    sortable: list[tuple[tuple[int, int], dict[str, object]]] = []
    for key, raw in by_key.items():
        group, _ = classify(key)
        rank = int(TOP_KEY.fullmatch(key).group(1)) if TOP_KEY.fullmatch(key) else 0
        sortable.append(((group, rank), raw))
    sortable.sort(key=lambda pair: pair[0])
    items: list[Item] = []
    for position, (_, raw) in enumerate(sortable, 1):
        key = str(raw["key"])
        title = raw.get("subject")
        official = raw.get("official")
        site = raw.get("site")
        if not all(isinstance(value, str) and value for value in (title, official, site)):
            raise ValueError(f"{key}: subject, official, and site are required")
        _, kind = classify(key)
        items.append(
            Item(
                key=key,
                title=typographic_title(str(title)),
                source=resolve_source(raw, key, roots),
                official=str(official),
                topic=topic_path(str(site)),
                kind=kind,
                position=position,
            )
        )
    validate_ledger(items)
    return items


def validate_ledger(items: list[Item]) -> None:
    top_count = len(items) - 4
    if top_count not in {1, 10}:
        raise ValueError(
            "a workday must contain either 5 or 14 items, "
            f"found {len(items)}"
        )
    kinds = [item.kind for item in items]
    expected = [
        "AtCoder",
        *(["力扣 Top"] * top_count),
        "力扣竞赛",
        "Codeforces",
        "力扣每日一题",
    ]
    if kinds != expected:
        raise ValueError(f"invalid 1+{top_count}+1+1+1 order: {kinds}")
    if len({item.title for item in items}) != len(items):
        raise ValueError("daily subjects must be unique")


def relative_topic(item: Item) -> str:
    return item.topic


def deployed_route(markdown_href: str, extra_parent_levels: int = 0) -> str:
    """Convert a source-relative Markdown path for use inside raw built HTML."""
    parsed = urlparse(markdown_href)
    if parsed.scheme or parsed.netloc:
        return markdown_href
    path = parsed.path
    if not path.endswith(".md"):
        raise ValueError(f"expected a Markdown route, found {markdown_href!r}")
    if Path(path).name == "index.md":
        path = path[: -len("index.md")]
    else:
        path = path[:-3] + "/"
    path = "../" * extra_parent_levels + path
    query = f"?{parsed.query}" if parsed.query else ""
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""
    return f"{path}{query}{fragment}"


def render_problem_page(work_date: str, item: Item, items: list[Item]) -> str:
    source = validate_canonical_source(
        item,
        item.source.read_text(encoding="utf-8"),
    )
    source_sha256 = hashlib.sha256(source.encode("utf-8")).hexdigest()
    links = "\n".join(
        [
            f"- [官方题目]({item.official})",
            f"- [对应知识专题]({relative_topic(item)})",
        ]
    )
    if "## Reference" not in source:
        reference = "## Reference\n\n" + links
    else:
        reference = "### 延伸阅读\n\n" + links
    previous_item = items[item.position - 2] if item.position > 1 else None
    next_item = items[item.position] if item.position < len(items) else None
    links: list[str] = []
    if previous_item:
        links.append(
            f'<a class="daily-archive-pager__previous" '
            f'href="{html.escape(deployed_route(previous_item.page_name, 1))}">← '
            f'{html.escape(previous_item.title)}</a>'
        )
    else:
        links.append('<span class="daily-archive-pager__empty"></span>')
    if next_item:
        links.append(
            f'<a class="daily-archive-pager__next" '
            f'href="{html.escape(deployed_route(next_item.page_name, 1))}">'
            f'{html.escape(next_item.title)} →</a>'
        )
    else:
        links.append('<span class="daily-archive-pager__empty"></span>')
    frontmatter = json.dumps(item.title, ensure_ascii=False)
    return "\n".join(
        [
            "---",
            f"title: {frontmatter}",
            "---",
            "",
            f"# {item.title}",
            "",
            (
                f'<p class="daily-archive-kicker">{work_date} · '
                f"第 {item.position}/{len(items)} 题 · {item.kind}</p>"
            ),
            "",
            (
                '<p class="daily-archive-utility">'
                f'<a href="{deployed_route("index.md", 1)}">'
                f"返回 {work_date} 题目列表</a>"
                f' · <a href="{html.escape(deployed_route(relative_topic(item), 1))}">'
                "进入知识专题</a>"
                "</p>"
            ),
            "",
            f"<!-- DAILY_CANONICAL_BODY_START sha256={source_sha256} -->",
            source.rstrip(),
            "<!-- DAILY_CANONICAL_BODY_END -->",
            "",
            reference,
            "",
            '<nav class="daily-archive-pager" aria-label="当日题目导航">',
            *links,
            "</nav>",
            "",
        ]
    )


def render_date_index(work_date: str, items: list[dict[str, object]]) -> str:
    top_count = sum(item["kind"] == "力扣 Top" for item in items)
    rows = []
    for item in items:
        rows.extend(
            [
                f'<li id="daily-{html.escape(str(item["key"]))}">',
                (
                    f'<span class="daily-run-source">{html.escape(str(item["kind"]))}</span> '
                    f'<a href="{html.escape(deployed_route(str(item["page"])))}">'
                    f'{html.escape(str(item["title"]))}</a>'
                ),
                "</li>",
            ]
        )
    return "\n".join(
        [
            f"# {work_date} · 每日题目 {{ .daily-archive-date-heading }}",
            "",
            (
                f"本日按固定顺序收录 AtCoder 1 题、力扣高频 {top_count} 题、"
                "力扣竞赛 1 题、Codeforces 1 题和力扣每日一题 1 题。"
                "每页都保留完整题面信息、约束推导、从朴素到最优的解法、"
                "正确性、完整 C++ 与高价值变种。"
            ),
            "",
            '<ol class="daily-run-list">',
            *rows,
            "</ol>",
            "",
            "[返回每日训练总览](../index.md)",
            "",
        ]
    )


def render_archive_index(dates: list[dict[str, object]]) -> str:
    sections = [
        "# 每日题目",
        "",
        (
            "这里按工作日期保存每日完整训练批次，与按知识模型组织的"
            "[题解索引](../problems/index.md)形成互补：前者用于回看某一天的完整训练，"
            "后者用于沿稳定专题系统学习。"
        ),
        "",
        "日期按新到旧排列。进入任意题目后，左侧导航只展开当前日期，"
        "可以在同一天的完整训练题目之间连续阅读。",
        "",
    ]
    for entry in dates:
        work_date = str(entry["date"])
        items = entry["items"]
        assert isinstance(items, list)
        top_items = [item for item in items if item["kind"] == "力扣 Top"]
        top_range = ""
        if top_items:
            first = TOP_KEY.fullmatch(str(top_items[0]["key"]))
            last = TOP_KEY.fullmatch(str(top_items[-1]["key"]))
            assert first and last
            top_range = f"力扣 Top {first.group(1)}–{last.group(1)}"
        sections.extend(
            [
                f"## [{work_date}]({work_date}/index.md)",
                "",
                (
                    f"{len(items)} 道完整题解 · AtCoder · {top_range} · "
                    "力扣竞赛 · Codeforces · 力扣每日一题"
                ),
                "",
            ]
        )
    return "\n".join(sections).rstrip() + "\n"


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_nav(dates: list[dict[str, object]]) -> str:
    lines = [
        NAV_START,
        "  - 每日题目:",
        "      - 总览: daily/index.md",
    ]
    for entry in dates:
        work_date = str(entry["date"])
        lines.append(f"      - {yaml_quote(work_date)}:")
        lines.append(f"          - 当日总览: daily/{work_date}/index.md")
        for item in entry["items"]:
            assert isinstance(item, dict)
            lines.append(
                f"          - {yaml_quote(str(item['title']))}: "
                f"daily/{work_date}/{item['page']}"
            )
    lines.append(NAV_END)
    return "\n".join(lines)


def update_nav(dates: list[dict[str, object]]) -> None:
    text = MKDOCS.read_text(encoding="utf-8")
    block = render_nav(dates)
    if NAV_START in text or NAV_END in text:
        if text.count(NAV_START) != 1 or text.count(NAV_END) != 1:
            raise ValueError("daily archive nav markers are unbalanced")
        start = text.index(NAV_START)
        end = text.index(NAV_END, start) + len(NAV_END)
        updated = text[:start] + block + text[end:]
    else:
        anchor = "nav:\n  - 首页: index.md\n"
        if anchor not in text:
            raise ValueError("cannot locate mkdocs nav insertion point")
        updated = text.replace(anchor, anchor + block + "\n", 1)
    MKDOCS.write_text(updated, encoding="utf-8")


def load_manifest() -> dict[str, object]:
    if not MANIFEST.is_file():
        return {"version": 1, "dates": []}
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if payload.get("version") != 1 or not isinstance(payload.get("dates"), list):
        raise ValueError("unsupported daily archive manifest")
    return payload


def main() -> None:
    args = parse_args()
    date.fromisoformat(args.date)
    items = build_items(args.specs, args.source_dir)
    target = ARCHIVE / args.date
    rendered_pages = {
        item.page_name: render_problem_page(args.date, item, items)
        for item in items
    }
    item_records: list[dict[str, object]] = []
    for item in items:
        item_records.append(
            {
                "position": item.position,
                "key": item.key,
                "title": item.title,
                "kind": item.kind,
                "page": item.page_name,
                "official": item.official,
                "topic": item.topic,
                "source_sha256": hashlib.sha256(
                    item.source.read_bytes()
                ).hexdigest(),
            }
        )
    expected_pages = {item.page_name for item in items}
    unexpected = sorted(
        path.name
        for path in target.glob("*.md")
        if path.name != "index.md" and path.name not in expected_pages
    )
    if unexpected:
        raise ValueError(f"{args.date}: unexpected archive pages: {unexpected}")
    target.mkdir(parents=True, exist_ok=True)
    for page_name, rendered in rendered_pages.items():
        (target / page_name).write_text(rendered, encoding="utf-8")
    (target / "index.md").write_text(
        render_date_index(args.date, item_records),
        encoding="utf-8",
    )
    manifest = load_manifest()
    dates = [
        entry
        for entry in manifest["dates"]
        if isinstance(entry, dict) and entry.get("date") != args.date
    ]
    top_count = sum(item["kind"] == "力扣 Top" for item in item_records)
    dates.append(
        {
            "date": args.date,
            "expected_count": len(item_records),
            "top_count": top_count,
            "items": item_records,
        }
    )
    dates.sort(key=lambda entry: str(entry["date"]), reverse=True)
    manifest["dates"] = dates
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (ARCHIVE / "index.md").write_text(render_archive_index(dates), encoding="utf-8")
    update_nav(dates)
    print(f"published {args.date}: {len(items)} archive pages")


if __name__ == "__main__":
    main()
