#!/usr/bin/env python3
"""Shared language boundary for reader-visible daily solution pages."""

from __future__ import annotations

import re


CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
HEADING = re.compile(r"^(#{2,4})\s+(.+?)\s*$")
FENCE = re.compile(r"^\s*```")
BLOCK_MATH_DELIMITER = re.compile(r"(?<!\\)\$\$")
ENGLISH_WORD = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")
URL = re.compile(r"https?://[^)\s]+")
LINK_ONLY = re.compile(r"^\s*[-*]?\s*\[[^\]]+\]\([^)]*\)\s*[。.]?\s*$")
OFFICIAL_ENGLISH_START = {
    "Complete English statement",
    "Official English entry and short excerpt",
}
ALLOWED_ENGLISH_HEADINGS = {"Reference", "Sources"}


def _is_english_analysis_line(line: str) -> bool:
    """Return whether one non-code line looks like reader-facing English prose."""

    if CJK.search(line):
        return False
    stripped = line.strip()
    if not stripped or stripped.startswith(("<!--", "![", "$$", "\\")):
        return False
    if re.fullmatch(r"# \[(?:atcoder|codeforces)\] .+", stripped):
        return False
    if stripped.startswith(("<nav", "</nav", "<a ", "<p ", "<span", "<img")):
        return False
    if LINK_ONLY.fullmatch(stripped):
        return False
    without_urls = URL.sub("", re.sub(r"<[^>]+>", "", stripped))
    heading = HEADING.match(without_urls)
    if heading:
        label = heading.group(2).strip()
        return (
            label not in ALLOWED_ENGLISH_HEADINGS
            and len(ENGLISH_WORD.findall(label)) >= 2
        )
    if stripped.startswith(">"):
        return False
    prose = re.sub(r"[`$\\{}_^=<>+*|&\[\](),.!:;?0-9-]", " ", without_urls)
    words = ENGLISH_WORD.findall(prose)
    return len(words) >= 8 and sum(map(len, words)) >= 45


def non_chinese_solution_lines(text: str, kind: str) -> list[tuple[int, str]]:
    """Find English analysis outside the allowed contest statement layer."""

    contest = kind in {"AtCoder", "Codeforces"}
    in_frontmatter = False
    in_fence = False
    in_block_math = False
    in_official_english = False
    findings: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if line_number == 1 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line.strip() == "---":
                in_frontmatter = False
            continue
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        block_math_delimiters = len(BLOCK_MATH_DELIMITER.findall(line))
        if in_block_math or block_math_delimiters:
            if block_math_delimiters % 2 == 1:
                in_block_math = not in_block_math
            continue
        heading = HEADING.match(line)
        if contest and heading:
            label = heading.group(2).strip()
            if label in OFFICIAL_ENGLISH_START:
                in_official_english = True
                continue
            if in_official_english and "中文" in label:
                in_official_english = False
                continue
        if in_official_english:
            continue
        if _is_english_analysis_line(line):
            findings.append((line_number, line.strip()))
    return findings
