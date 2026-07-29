#!/usr/bin/env python3
"""Publish one verified 14-problem workday into the chronological archive."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
ARCHIVE = DOCS / "daily"
MANIFEST = ARCHIVE / "archive.json"
OFFICIAL_ASSETS = DOCS / "assets" / "daily" / "official"
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
FULLWIDTH_PUNCTUATION = "，。！？；：、（《【「『"
REMOTE_MARKDOWN_IMAGE = re.compile(
    r"(?P<prefix>!\[[^\]]*\]\()(?P<url>(?:https?:)?//[^)\s]+)(?P<suffix>\))",
    re.IGNORECASE,
)
REMOTE_HTML_IMAGE = re.compile(
    r"(?P<prefix><img\b[^>]*\bsrc\s*=\s*[\"'])"
    r"(?P<url>(?:https?:)?//[^\"']+)"
    r"(?P<suffix>[\"'][^>]*>)",
    re.IGNORECASE,
)
OFFICIAL_IMAGE_HOSTS = (
    "assets.leetcode.com",
    "leetcode.cn",
    "atcoder.jp",
    "img.atcoder.jp",
    "codeforces.com",
    "codeforces.org",
    "espresso.codeforces.com",
)
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".webp"}
MAX_IMAGE_BYTES = 10 * 1024 * 1024


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


def typographic_prose(line: str) -> str:
    """Apply source-aware fixes to prose while fenced source stays byte-stable."""
    if line.startswith("- Submission contract"):
        contract = line.partition(":")[2].split(";", 1)[0].strip().rstrip(".")
        line = f"- Program interface: {contract}."
    line = line.replace(
        "图像来自官方题面资产并应在邮件发送后检查是否仍可见。",
        "图像来自官方题面资产。",
    )
    line = line.replace("第K个", "第 K 个")
    line = line.replace("BFS不再", "BFS 不再")
    line = re.sub(r"\*\*([^*\n]+)：\*\*[ \t]*", r"**\1**：", line)
    line = re.sub(r"__([^_\n]+)：__[ \t]*", r"__\1__：", line)
    line = re.sub(rf"[ \t]+([{FULLWIDTH_PUNCTUATION}》】」』])", r"\1", line)
    line = re.sub(rf"([{FULLWIDTH_PUNCTUATION}])([*_]{{2}})[ \t]+", r"\1\2", line)
    line = re.sub(rf"([{FULLWIDTH_PUNCTUATION}])[ \t]+", r"\1", line)
    return line


def is_official_image_host(host: str) -> bool:
    host = host.casefold().split(":", 1)[0]
    return any(host == allowed or host.endswith(f".{allowed}") for allowed in OFFICIAL_IMAGE_HOSTS)


def vendor_official_image(url: str) -> str:
    if url.startswith("//"):
        url = f"https:{url}"
    parsed = urlparse(url)
    if parsed.scheme != "https" or not is_official_image_host(parsed.netloc):
        raise ValueError(f"remote image is not hosted by an allowed official source: {url}")
    suffix = Path(parsed.path).suffix.casefold()
    if suffix not in IMAGE_SUFFIXES:
        raise ValueError(f"unsupported official image suffix {suffix!r}: {url}")
    basename = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(parsed.path).name).strip("-")
    digest = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    filename = f"{digest}-{basename}"
    target = OFFICIAL_ASSETS / filename
    if not target.is_file():
        request = Request(url, headers={"User-Agent": "Algo daily archive publisher/1.0"})
        with urlopen(request, timeout=20) as response:
            final = urlparse(response.geturl())
            if final.scheme != "https" or not is_official_image_host(final.netloc):
                raise ValueError(f"official image redirected outside allowed sources: {url}")
            content_type = response.headers.get_content_type()
            if not content_type.startswith("image/") or content_type == "image/svg+xml":
                raise ValueError(f"official asset is not an allowed raster image: {url}")
            payload = response.read(MAX_IMAGE_BYTES + 1)
        if len(payload) > MAX_IMAGE_BYTES:
            raise ValueError(f"official image exceeds {MAX_IMAGE_BYTES} bytes: {url}")
        OFFICIAL_ASSETS.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(f"{target.suffix}.tmp")
        temporary.write_bytes(payload)
        temporary.replace(target)
    return f"../../assets/daily/official/{filename}"


def vendor_remote_images(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        local = vendor_official_image(html.unescape(match.group("url")))
        return f"{match.group('prefix')}{local}{match.group('suffix')}"

    text = REMOTE_MARKDOWN_IMAGE.sub(replace, text)
    return REMOTE_HTML_IMAGE.sub(replace, text)


def normalize_math_delimiters(text: str) -> str:
    """Convert email-oriented TeX delimiters to the repository MathJax contract."""
    lines = text.splitlines()
    result: list[str] = []
    in_fence = False
    in_display = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            result.append(line)
            continue
        if in_fence:
            result.append(line)
            continue
        stripped = line.strip()
        if stripped == r"\[":
            if in_display:
                raise ValueError("nested legacy display-math delimiter")
            result.append("$$")
            in_display = True
            continue
        if stripped == r"\]":
            if not in_display:
                raise ValueError("legacy display-math close without open")
            result.append("$$")
            in_display = False
            continue
        line = re.sub(r"(?<!\\)\\\(", "$", line)
        line = re.sub(r"(?<!\\)\\\)", "$", line)
        result.append(line)
    if in_display:
        raise ValueError("unclosed legacy display-math delimiter")
    normalized = "\n".join(result).strip() + "\n"
    normalized = normalized.replace("$2^b+1`", "$2^b+1$`")
    normalized = normalized.replace(
        "$[left,right]$",
        r"$[\mathtt{left},\mathtt{right}]$",
    )
    return normalized


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
    if len(items) != 14:
        raise ValueError(f"a workday must contain exactly 14 items, found {len(items)}")
    kinds = [item.kind for item in items]
    expected = [
        "AtCoder",
        *(["力扣 Top"] * 10),
        "力扣竞赛",
        "Codeforces",
        "力扣每日一题",
    ]
    if kinds != expected:
        raise ValueError(f"invalid 1+10+1+1+1 order: {kinds}")
    if len({item.title for item in items}) != 14:
        raise ValueError("daily subjects must be unique")


def strip_section(lines: list[str], index: int, level: int) -> int:
    cursor = index + 1
    while cursor < len(lines):
        match = HEADING.match(lines[cursor])
        if match and len(match.group(1)) <= level:
            break
        cursor += 1
    return cursor


def sanitize_source(text: str) -> str:
    lines = text.replace("\r\n", "\n").splitlines()
    output: list[str] = []
    in_fence = False
    index = 0
    first_heading_seen = False
    while index < len(lines):
        line = lines[index]
        if FENCE.match(line):
            in_fence = not in_fence
            output.append(line.rstrip())
            index += 1
            continue
        if in_fence:
            output.append(line.rstrip())
            index += 1
            continue
        match = HEADING.match(line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            title_lower = title.casefold()
            is_source_heading = (
                "官方原始信息" in title
                or title_lower.startswith("official source")
            )
            if not first_heading_seen and level == 1 and not is_source_heading:
                first_heading_seen = True
                index += 1
                continue
            first_heading_seen = True
            if (
                title in {"今日提交与打卡", "提交与打卡", "Algo 状态"}
                or "algo status" in title_lower
                or "submission status" in title_lower
            ):
                index = strip_section(lines, index, level)
                continue
            if title == "来源与 Algo 状态":
                output.append(f"{match.group(1)} Reference")
                index += 1
                continue
            if title == "来源":
                output.append(f"{match.group(1)} Reference")
                index += 1
                continue
        if "{{ALGO_STATUS}}" in line or STATUS_LINE.match(line.strip()):
            index += 1
            continue
        if any(pattern.search(line) for pattern in PRIVATE_PATTERNS[2:]):
            index += 1
            continue
        output.append(typographic_prose(line.rstrip()))
        index += 1
    while output and not output[-1]:
        output.pop()
    normalized = "\n".join(output).strip() + "\n"
    for pattern in PRIVATE_PATTERNS[:2]:
        if pattern.search(normalized):
            raise ValueError(f"source contains private material matching {pattern.pattern!r}")
    return normalized


def normalize_headings(text: str) -> str:
    lines = text.splitlines()
    in_fence = False
    levels: list[int] = []
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING.match(line)
        if match:
            levels.append(len(match.group(1)))
    if not levels:
        raise ValueError("source has no Markdown headings")
    shift = 2 - min(levels)
    result: list[str] = []
    in_fence = False
    for line in lines:
        if FENCE.match(line):
            in_fence = not in_fence
            result.append(line)
            continue
        match = None if in_fence else HEADING.match(line)
        if match:
            level = min(6, max(2, len(match.group(1)) + shift))
            line = f"{'#' * level} {match.group(2)}"
        result.append(line)
    return "\n".join(result).strip() + "\n"


def annotate_cpp_blocks(text: str) -> str:
    """Attach invisible harness metadata to every independently checked block."""
    lines = text.splitlines()
    result: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not CPP_FENCE.match(line):
            result.append(line)
            index += 1
            continue
        end = index + 1
        while end < len(lines) and lines[end].strip() != "```":
            end += 1
        if end == len(lines):
            raise ValueError("unterminated C++ fence in archive source")
        source = "\n".join(lines[index + 1 : end])
        previous = result[-1].strip() if result else ""
        if not COMPILE_DIRECTIVE.fullmatch(previous):
            if "TreeNode" in source and not re.search(r"\bstruct\s+TreeNode\b", source):
                result.append("<!-- compile:leetcode-tree -->")
            elif "ListNode" in source and not re.search(r"\bstruct\s+ListNode\b", source):
                result.append("<!-- compile:leetcode-list -->")
            else:
                result.append("<!-- compile:leetcode -->")
        result.extend(lines[index : end + 1])
        index = end + 1
    return "\n".join(result).strip() + "\n"


def relative_topic(item: Item) -> str:
    return item.topic


def render_problem_page(work_date: str, item: Item, items: list[Item]) -> str:
    source = sanitize_source(item.source.read_text(encoding="utf-8"))
    source = normalize_math_delimiters(source)
    source = normalize_headings(vendor_remote_images(source))
    source = annotate_cpp_blocks(source)
    links = "\n".join(
        [
            f"- [官方题目]({item.official})",
            f"- [对应知识专题]({relative_topic(item)})",
        ]
    )
    if "## Reference" not in source:
        source = source.rstrip() + "\n\n## Reference\n\n" + links + "\n"
    else:
        source = source.rstrip() + "\n\n### 延伸阅读\n\n" + links + "\n"
    previous_item = items[item.position - 2] if item.position > 1 else None
    next_item = items[item.position] if item.position < len(items) else None
    links: list[str] = []
    if previous_item:
        links.append(
            f'<a class="daily-archive-pager__previous" '
            f'href="{html.escape(previous_item.page_name)}">← '
            f'{html.escape(previous_item.title)}</a>'
        )
    else:
        links.append('<span class="daily-archive-pager__empty"></span>')
    if next_item:
        links.append(
            f'<a class="daily-archive-pager__next" '
            f'href="{html.escape(next_item.page_name)}">'
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
                f"第 {item.position}/14 题 · {item.kind}</p>"
            ),
            "",
            (
                '<p class="daily-archive-utility">'
                f'<a href="index.md">返回 {work_date} 题目列表</a>'
                f' · <a href="{html.escape(relative_topic(item))}">进入知识专题</a>'
                "</p>"
            ),
            "",
            source.rstrip(),
            "",
            '<nav class="daily-archive-pager" aria-label="当日题目导航">',
            *links,
            "</nav>",
            "",
        ]
    )


def render_date_index(work_date: str, items: list[dict[str, object]]) -> str:
    rows = []
    for item in items:
        rows.extend(
            [
                f'<li id="daily-{html.escape(str(item["key"]))}">',
                (
                    f'<span class="daily-run-source">{html.escape(str(item["kind"]))}</span> '
                    f'<a href="{html.escape(str(item["page"]))}">'
                    f'{html.escape(str(item["title"]))}</a>'
                ),
                "</li>",
            ]
        )
    return "\n".join(
        [
            f"# {work_date} · 每日 14 题 {{ .daily-archive-date-heading }}",
            "",
            (
                "本日按固定顺序收录 AtCoder 1 题、力扣高频 10 题、"
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
        "# 每日 14 题档案",
        "",
        (
            "这里按工作日期保存每日完整训练批次，与按知识模型组织的"
            "[题解索引](../problems/index.md)形成互补：前者用于回看某一天的完整训练，"
            "后者用于沿稳定专题系统学习。"
        ),
        "",
        "日期按新到旧排列。进入任意题目后，左侧导航只展开当前日期，"
        "可以在同一天的 14 道题之间连续阅读。",
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
        "  - 每日 14 题:",
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
    target.mkdir(parents=True, exist_ok=True)
    item_records: list[dict[str, object]] = []
    for item in items:
        page = target / item.page_name
        page.write_text(render_problem_page(args.date, item, items), encoding="utf-8")
        item_records.append(
            {
                "position": item.position,
                "key": item.key,
                "title": item.title,
                "kind": item.kind,
                "page": item.page_name,
                "official": item.official,
                "topic": item.topic,
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
    dates.append({"date": args.date, "items": item_records})
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
