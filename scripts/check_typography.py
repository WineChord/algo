#!/usr/bin/env python3
from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    ROOT / "README.md",
    ROOT / "mkdocs.yml",
    *sorted((ROOT / "docs").rglob("*.md")),
    *sorted((ROOT / "includes").rglob("*.md")),
]
AUTOCORRECT = ROOT / "node_modules" / ".bin" / "autocorrect"
AUTOCORRECT_TARGETS = (
    "README.md",
    "mkdocs.yml",
    *[
        str(path.relative_to(ROOT))
        for path in sorted((ROOT / "docs").rglob("*.md"))
        if not path.is_relative_to(ROOT / "docs" / "daily")
    ],
    "includes",
)

HAN = r"\u3400-\u4dbf\u4e00-\u9fff"
MIXED_SCRIPT = re.compile(
    rf"(?:[{HAN}](?=[A-Za-z0-9])|[A-Za-z0-9](?=[{HAN}]))"
)
SPACE_BEFORE_FULLWIDTH = re.compile(r"\S[ \t]+[，。！？；：、）》】」』]")
SPACE_AFTER_FULLWIDTH = re.compile(r"[，。！？；：、（《【「『][ \t]+\S")
FULLWIDTH_DIGIT = re.compile(r"[\uff10-\uff19]")
NUMBER_UNIT = re.compile(
    r"(?<![A-Za-z0-9_.])"
    r"\d+(?:\.\d+)?"
    r"(?:KiB|MiB|GiB|TiB|KB|MB|GB|TB|bit|bits|byte|bytes|"
    r"ns|us|ms|sec|secs|Hz|kHz|MHz|GHz|Kbps|Mbps|Gbps|"
    r"px|pt|em|rem)"
    r"\b"
)

FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
REFERENCE_DEFINITION = re.compile(r"^\s{0,3}\[[^\]]+\]:\s+\S")
SNIPPET_DIRECTIVE = re.compile(r'^\s*--8<--\s+"[^"]+"\s*$')
INLINE_CODE = re.compile(r"(`+)(.+?)\1")
INLINE_MATH = re.compile(r"(?<!\\)\$(?!\$).*?(?<!\\)\$")
PAREN_MATH = re.compile(r"\\\(.+?\\\)|\\\[.+?\\\]")
MARKDOWN_DESTINATION = re.compile(
    r"\]\((?:\\.|[^()\n]|\([^()\n]*\))*\)"
)
MARKDOWN_REFERENCE = re.compile(r"(\[[^\]\n]+\])\[[^\]\n]*\]")
MARKDOWN_IMAGE = re.compile(
    r"!\[[^\]\n]*\]\((?:\\.|[^()\n]|\([^()\n]*\))*\)"
)
FOOTNOTE = re.compile(r"\[\^[^\]\n]+\]")
AUTOLINK = re.compile(r"<(?:https?://|mailto:)[^>\n]+>")
BARE_URL = re.compile(r"https?://[^\s<>)]+")
HTML_VOID = re.compile(r"<(?:br|hr|img|input)\b[^>]*?/?>", re.IGNORECASE)
HTML_TAG = re.compile(r"</?[A-Za-z][^>\n]*>")
ATTRIBUTE_LIST = re.compile(r"\{(?:[^{}\n]|\\.)*\}")
ENTITY = re.compile(r"&(?:#[0-9]+|#x[0-9A-Fa-f]+|[A-Za-z][A-Za-z0-9]+);")
PATH = re.compile(
    r"(?<![A-Za-z0-9_])(?:\.{0,2}/|/)"
    r"(?:[A-Za-z0-9_.%+@~-]+/)*[A-Za-z0-9_.%+@~-]+"
)
ANCHOR = re.compile(r"(?<![A-Za-z0-9_])#[A-Za-z][A-Za-z0-9_.:-]*")
BLOCK_PREFIX = re.compile(
    r"^\s{0,3}(?:(?:#{1,6}|[-+*]|\d+[.)]|>|:)\s+)+"
)
PROTECTED = "\ue000"


def code_token(match: re.Match[str]) -> str:
    content = match.group(2)
    if re.search(r"[A-Za-z0-9]", content):
        return "A"
    if re.search(rf"[{HAN}]", content):
        return "中"
    return PROTECTED


def mask_math(line: str, in_display_math: bool) -> tuple[str, bool]:
    result: list[str] = []
    position = 0
    while position < len(line):
        marker = line.find("$$", position)
        if marker < 0:
            if not in_display_math:
                result.append(line[position:])
            break
        if not in_display_math:
            result.append(line[position:marker])
        result.append(PROTECTED)
        in_display_math = not in_display_math
        position = marker + 2
    return "".join(result), in_display_math


def prose_segments(line: str, in_display_math: bool) -> tuple[list[str], bool]:
    line, in_display_math = mask_math(line, in_display_math)
    if not line:
        return [], in_display_math
    line = BLOCK_PREFIX.sub("", line)
    line = MARKDOWN_IMAGE.sub(PROTECTED, line)
    line = MARKDOWN_DESTINATION.sub("]", line)
    line = MARKDOWN_REFERENCE.sub(r"\1", line)
    line = FOOTNOTE.sub(PROTECTED, line)
    line = AUTOLINK.sub(PROTECTED, line)
    line = BARE_URL.sub(PROTECTED, line)
    line = INLINE_CODE.sub(code_token, line)
    line = INLINE_MATH.sub(PROTECTED, line)
    line = PAREN_MATH.sub(PROTECTED, line)
    line = HTML_VOID.sub(PROTECTED, line)
    line = HTML_TAG.sub("", line)
    line = ATTRIBUTE_LIST.sub(PROTECTED, line)
    line = ENTITY.sub(PROTECTED, line)
    line = PATH.sub(PROTECTED, line)
    line = ANCHOR.sub(PROTECTED, line)
    line = re.sub(r"[*_~=^\\]", "", line)
    line = line.replace("[", "").replace("]", "")
    return line.split(PROTECTED), in_display_math


def report(path: Path, number: int, message: str, errors: list[str]) -> None:
    errors.append(f"{path.relative_to(ROOT)}:{number}: {message}")


def run_autocorrect(errors: list[str]) -> int:
    if not AUTOCORRECT.is_file():
        errors.append("AutoCorrect 不可用，请先运行 `npm ci`")
        return 0
    result = subprocess.run(
        [
            str(AUTOCORRECT),
            "--lint",
            "--strict",
            "--format",
            "json",
            "--quiet",
            *AUTOCORRECT_TARGETS,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if not result.stdout.strip():
        detail = result.stderr.strip() or f"退出状态 {result.returncode}"
        errors.append(f"AutoCorrect 未生成检查报告：{detail}")
        return 0
    try:
        result_json = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        errors.append(f"AutoCorrect 返回了无效 JSON：{exc}")
        return 0
    issue_count = 0
    for message in result_json.get("messages", []):
        path = message.get("filepath", "<unknown>")
        if message.get("error"):
            errors.append(f"{path}: {message['error']}")
        for issue in message.get("lines", []):
            issue_count += 1
            old = issue.get("old", "").strip()
            new = issue.get("new", "").strip()
            errors.append(
                f"{path}:{issue.get('l', '?')}:{issue.get('c', '?')}: "
                f"建议将 {old!r} 改为 {new!r}"
            )
    if result.returncode not in {0, 1}:
        detail = result.stderr.strip() or "未知错误"
        errors.append(f"AutoCorrect 运行失败（状态 {result.returncode}）：{detail}")
    return issue_count


errors: list[str] = []
autocorrect_issues = run_autocorrect(errors)
for path in FILES:
    fence_char = ""
    fence_length = 0
    in_display_math = False
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if not fence_char:
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char = ""
                fence_length = 0
            continue
        if fence_char or REFERENCE_DEFINITION.match(line) or SNIPPET_DIRECTIVE.match(line):
            continue
        segments, in_display_math = prose_segments(line, in_display_math)
        for segment in segments:
            cells = segment.split("|")
            for cell in cells:
                text = cell.strip()
                if not text:
                    continue
                if MIXED_SCRIPT.search(text):
                    report(path, number, "中文与英文或数字之间需要一个空格", errors)
                    break
                if NUMBER_UNIT.search(text):
                    report(path, number, "数字与普通单位之间需要一个空格", errors)
                    break
                if FULLWIDTH_DIGIT.search(text):
                    report(path, number, "正文数字请使用半角字符", errors)
                    break
                if SPACE_BEFORE_FULLWIDTH.search(text):
                    report(path, number, "全角标点前不能有多余空格", errors)
                    break
                if SPACE_AFTER_FULLWIDTH.search(text):
                    report(path, number, "全角标点后不能有多余空格", errors)
                    break

if errors:
    print("\n".join(errors), file=sys.stderr)
    raise SystemExit(1)

print(
    f"文案排版检查通过：{len(FILES)} 个正文与站点配置文件，"
    f"AutoCorrect {autocorrect_issues} 个问题"
)
