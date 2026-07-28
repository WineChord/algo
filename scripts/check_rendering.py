#!/usr/bin/env python3
"""Validate Markdown structure and mathematics from source through browser output."""

from __future__ import annotations

import argparse
import contextlib
import re
import shutil
import subprocess
import sys
import threading
from dataclasses import dataclass
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterable, Optional, Sequence


EXPECTED_MATHJAX_VERSION = "3.2.2"
BACKTICK = "`"
BARE_COMMANDS = (
    "alpha",
    "beta",
    "gamma",
    "delta",
    "epsilon",
    "theta",
    "lambda",
    "mu",
    "pi",
    "rho",
    "sigma",
    "tau",
    "phi",
    "psi",
    "omega",
    "widehat",
    "hat",
    "tilde",
    "bar",
    "overline",
    "underline",
    "frac",
    "dfrac",
    "sqrt",
    "sum",
    "prod",
    "nabla",
    "partial",
    "left",
    "right",
    "operatorname",
    "mathrm",
    "mathbf",
    "mathbb",
    "mathcal",
    "mathsf",
    "mathit",
    "mathtt",
)
BARE_FUNCTIONS = ("log", "exp", "sin", "cos", "tan", "tanh", "softmax")
TEXT_COMMAND = re.compile(
    r"\\(?:text|operatorname|mathrm|mathbf|mathit|mathtt)\{[^{}]*\}"
)
SNIPPET = re.compile(r'(?m)^[ \t]*--8<-- "([^"]+)"[ \t]*$')


@dataclass(frozen=True)
class Expression:
    path: Path
    line: int
    kind: str
    tex: str


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def mask_range(chars: list[str], start: int, end: int) -> None:
    for index in range(start, end):
        if chars[index] != "\n":
            chars[index] = " "


def fence_marker(line: str) -> Optional[str]:
    stripped = line.lstrip(" ")
    if not stripped:
        return None
    char = stripped[0]
    if char not in (BACKTICK, "~"):
        return None
    length = 0
    while length < len(stripped) and stripped[length] == char:
        length += 1
    return char * length if length >= 3 else None


def mask_markdown_code(text: str, path: Path, errors: list[str]) -> list[str]:
    chars = list(text)
    offset = 0
    active_char: Optional[str] = None
    active_length = 0
    active_line = 0
    for line in text.splitlines(keepends=True):
        marker = fence_marker(line)
        if active_char is not None:
            mask_range(chars, offset, offset + len(line))
            if marker and marker[0] == active_char and len(marker) >= active_length:
                active_char = None
                active_length = 0
                active_line = 0
            offset += len(line)
            continue
        if marker:
            active_char = marker[0]
            active_length = len(marker)
            active_line = line_number(text, offset)
            mask_range(chars, offset, offset + len(line))
            offset += len(line)
            continue
        cursor = 0
        while cursor < len(line):
            if line[cursor] != BACKTICK:
                cursor += 1
                continue
            run = 1
            while cursor + run < len(line) and line[cursor + run] == BACKTICK:
                run += 1
            marker = BACKTICK * run
            end = line.find(marker, cursor + run)
            if end < 0:
                cursor += run
                continue
            mask_range(chars, offset + cursor, offset + end + run)
            cursor = end + run
        offset += len(line)
    if active_char is not None:
        errors.append(f"{path}:{active_line}: unclosed fenced code block")
    return chars


def unescaped_dollars(line: str) -> list[int]:
    result = []
    for index, char in enumerate(line):
        if char != "$":
            continue
        slashes = 0
        cursor = index - 1
        while cursor >= 0 and line[cursor] == "\\":
            slashes += 1
            cursor -= 1
        if slashes % 2 == 0:
            result.append(index)
    return result


def validate_tex(expression: Expression, errors: list[str]) -> None:
    tex = expression.tex
    label = f"{expression.path}:{expression.line}"
    if not tex.strip():
        errors.append(f"{label}: empty {expression.kind} expression")
        return
    braces: list[int] = []
    for index, char in enumerate(tex):
        if char not in "{}":
            continue
        slashes = 0
        cursor = index - 1
        while cursor >= 0 and tex[cursor] == "\\":
            slashes += 1
            cursor -= 1
        if slashes % 2:
            continue
        if char == "{":
            braces.append(index)
        elif braces:
            braces.pop()
        else:
            errors.append(f"{label}: unmatched closing brace in TeX")
            break
    if braces:
        errors.append(f"{label}: unmatched opening brace in TeX")
    left_count = len(re.findall(r"\\left\b", tex))
    right_count = len(re.findall(r"\\right\b", tex))
    if left_count != right_count:
        errors.append(
            f"{label}: \\left/\\right count differs "
            f"({left_count} versus {right_count})"
        )
    environments: list[str] = []
    for match in re.finditer(r"\\(begin|end)\{([^{}]+)\}", tex):
        operation, name = match.groups()
        if operation == "begin":
            environments.append(name)
        elif not environments or environments[-1] != name:
            errors.append(f"{label}: unmatched \\end{{{name}}}")
            break
        else:
            environments.pop()
    if environments:
        errors.append(f"{label}: unclosed environment {environments[-1]}")
    heuristic = tex
    while True:
        updated = TEXT_COMMAND.sub("", heuristic)
        if updated == heuristic:
            break
        heuristic = updated
    command_pattern = re.compile(
        r"(?<![\\A-Za-z])(" + "|".join(BARE_COMMANDS) + r")(?![A-Za-z])"
    )
    match = command_pattern.search(heuristic)
    if match:
        errors.append(
            f"{label}: probable missing backslash before {match.group(1)!r}"
        )
    function_pattern = re.compile(
        r"(?<![\\A-Za-z])(" + "|".join(BARE_FUNCTIONS) + r")(?=\\|\s*\()"
    )
    match = function_pattern.search(heuristic)
    if match:
        errors.append(
            f"{label}: probable missing backslash before function "
            f"{match.group(1)!r}"
        )


def scan_markdown(path: Path, text: str) -> tuple[list[Expression], list[str]]:
    errors: list[str] = []
    code_mask = mask_markdown_code(text, path, errors)
    outside_math = code_mask.copy()
    visible = "".join(code_mask)
    expressions: list[Expression] = []
    for match in re.finditer(r"\\[()]", visible):
        errors.append(
            f"{path}:{line_number(text, match.start())}: "
            "legacy \\(...\\) delimiter; use $...$"
        )
    for match in re.finditer(r"(?m)^\s*\\[\[\]]\s*$", visible):
        errors.append(
            f"{path}:{line_number(text, match.start())}: "
            "legacy display delimiter; use a standalone $$ line"
        )
    for match in re.finditer(r"(?m)^\$\$\n\$\$$", visible):
        errors.append(
            f"{path}:{line_number(text, match.start())}: "
            "separate adjacent display blocks with a blank line"
        )
    offset = 0
    display_start: Optional[int] = None
    display_line = 0
    display_tex: list[str] = []
    for line in visible.splitlines(keepends=True):
        body = line[:-1] if line.endswith("\n") else line
        dollars = unescaped_dollars(body)
        standalone = body.strip() == "$$"
        if standalone:
            delimiter_at = body.index("$$")
            absolute = offset + delimiter_at
            if delimiter_at != 0:
                errors.append(
                    f"{path}:{line_number(text, absolute)}: "
                    "display $$ delimiters must start at column 1"
                )
            if display_start is None:
                display_start = absolute
                display_line = line_number(text, absolute)
                display_tex = []
            else:
                expression = Expression(
                    path,
                    display_line,
                    "display",
                    "".join(display_tex).strip(),
                )
                expressions.append(expression)
                mask_range(outside_math, display_start, offset + len(body))
                display_start = None
                display_tex = []
            offset += len(line)
            continue
        if display_start is not None:
            if dollars:
                errors.append(
                    f"{path}:{line_number(text, offset + dollars[0])}: "
                    "nested dollar delimiter inside display math"
                )
            display_tex.append(line)
            offset += len(line)
            continue
        adjacent = [
            index
            for index in dollars
            if (index + 1 in dollars) or (index - 1 in dollars)
        ]
        if adjacent:
            errors.append(
                f"{path}:{line_number(text, offset + adjacent[0])}: "
                "display $$ delimiters must occupy their own lines"
            )
            offset += len(line)
            continue
        if len(dollars) % 2:
            errors.append(
                f"{path}:{line_number(text, offset + dollars[-1])}: "
                "unclosed inline dollar delimiter or unescaped currency sign"
            )
            offset += len(line)
            continue
        for index in range(0, len(dollars), 2):
            start, end = dollars[index], dollars[index + 1]
            expression = Expression(
                path,
                line_number(text, offset + start),
                "inline",
                body[start + 1 : end].strip(),
            )
            expressions.append(expression)
            mask_range(outside_math, offset + start, offset + end + 1)
        offset += len(line)
    if display_start is not None:
        errors.append(f"{path}:{display_line}: unclosed display math delimiter")
    for expression in expressions:
        validate_tex(expression, errors)
    plain = "".join(outside_math)
    for match in re.finditer(r"\\[A-Za-z]+", plain):
        errors.append(
            f"{path}:{line_number(text, match.start())}: "
            "TeX command appears outside math or code delimiters"
        )
    if len(re.findall(r"(?i)<details(?:\s[^>]*)?>", plain)) != len(
        re.findall(r"(?i)</details\s*>", plain)
    ):
        errors.append(f"{path}: unbalanced <details> elements")
    return expressions, errors


def canonicalize_legacy_math(path: Path, text: str) -> tuple[str, int]:
    errors: list[str] = []
    mask = mask_markdown_code(text, path, errors)
    visible = "".join(mask)
    output: list[str] = []
    replacements = 0
    offset = 0
    for line in text.splitlines(keepends=True):
        masked_line = visible[offset : offset + len(line)]
        ending = "\n" if line.endswith("\n") else ""
        body = line[:-1] if ending else line
        masked_body = masked_line[:-1] if ending else masked_line
        if masked_body in ("\\[", "\\]") and body == masked_body:
            output.append("$$" + ending)
            replacements += 1
            offset += len(line)
            continue
        cursor = 0
        while cursor < len(line):
            if (
                cursor + 1 < len(line)
                and masked_line[cursor] == "\\"
                and masked_line[cursor + 1] in "()"
            ):
                output.append("$")
                cursor += 2
                replacements += 1
            else:
                output.append(line[cursor])
                cursor += 1
        offset += len(line)
    return "".join(output), replacements


def expand_snippets(root: Path, text: str, seen: frozenset[Path]) -> str:
    def replace(match: re.Match[str]) -> str:
        target = (root / match.group(1)).resolve()
        if target in seen or not target.is_file():
            return match.group(0)
        payload = target.read_text(encoding="utf-8")
        return expand_snippets(root, payload, seen | {target})

    return SNIPPET.sub(replace, text)


class GeneratedPageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.article_depth = 0
        self.math_depth = 0
        self.math_tag: Optional[str] = None
        self.math_kind = ""
        self.math_buffer: list[str] = []
        self.skip_depth = 0
        self.visible_buffer: list[str] = []
        self.expressions: list[str] = []
        self.kinds: list[str] = []

    @staticmethod
    def classes(attrs: Sequence[tuple[str, Optional[str]]]) -> list[str]:
        return (dict(attrs).get("class") or "").split()

    def handle_starttag(
        self, tag: str, attrs: Sequence[tuple[str, Optional[str]]]
    ) -> None:
        classes = self.classes(attrs)
        if tag == "article" and "md-content__inner" in classes:
            self.article_depth += 1
        if not self.article_depth:
            return
        if self.math_tag is not None:
            self.math_depth += 1
        elif "arithmatex" in classes:
            self.math_tag = tag
            self.math_kind = "display" if tag == "div" else "inline"
            self.math_depth = 1
            self.math_buffer = []
        elif tag in ("pre", "code", "script", "style"):
            self.skip_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.math_tag is not None:
            self.math_depth -= 1
            if self.math_depth == 0:
                payload = "".join(self.math_buffer).strip()
                if payload.startswith(r"\(") and payload.endswith(r"\)"):
                    payload = payload[2:-2].strip()
                elif payload.startswith(r"\[") and payload.endswith(r"\]"):
                    payload = payload[2:-2].strip()
                self.expressions.append(payload)
                self.kinds.append(self.math_kind)
                self.math_tag = None
                self.math_kind = ""
                self.math_buffer = []
        elif self.article_depth and tag in ("pre", "code", "script", "style"):
            self.skip_depth = max(0, self.skip_depth - 1)
        if tag == "article" and self.article_depth:
            self.article_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.math_tag is not None:
            self.math_buffer.append(data)
        elif self.article_depth and not self.skip_depth:
            self.visible_buffer.append(data)

    @property
    def visible_text(self) -> str:
        return " ".join(self.visible_buffer)


def generated_path(site_dir: Path, relative: Path) -> Path:
    if relative == Path("index.md"):
        return site_dir / "index.html"
    if relative.name == "index.md":
        return site_dir / relative.parent / "index.html"
    return site_dir / relative.with_suffix("") / "index.html"


def compare_generated_site(
    root: Path,
    site_dir: Path,
    source_paths: list[Path],
    errors: list[str],
) -> int:
    total = 0
    docs_root = root / "docs"
    for source in source_paths:
        try:
            relative = source.relative_to(docs_root)
        except ValueError:
            continue
        output = generated_path(site_dir, relative)
        if not output.is_file():
            errors.append(f"{relative}: generated page is missing at {output}")
            continue
        expanded = expand_snippets(
            root,
            source.read_text(encoding="utf-8"),
            frozenset({source.resolve()}),
        )
        expected, source_errors = scan_markdown(relative, expanded)
        errors.extend(source_errors)
        parser = GeneratedPageParser()
        parser.feed(output.read_text(encoding="utf-8"))
        total += len(parser.expressions)
        expected_tex = [item.tex for item in expected]
        expected_kinds = [item.kind for item in expected]
        if expected_tex != parser.expressions or expected_kinds != parser.kinds:
            errors.append(
                f"{relative}: source and generated HTML math differ "
                f"({len(expected_tex)} versus {len(parser.expressions)})"
            )
        if re.search(r"\\(?:[A-Za-z]+|[\[\]()])", parser.visible_text):
            errors.append(f"{relative}: generated page leaks raw TeX into prose")
    return total


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format_string: str, *args: object) -> None:
        pass


@contextlib.contextmanager
def serve_directory(directory: Path) -> Iterable[str]:
    class Handler(QuietHandler):
        def __init__(self, *args: object, **kwargs: object) -> None:
            super().__init__(*args, directory=str(directory), **kwargs)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def chrome_binary(explicit: Optional[str]) -> Optional[str]:
    candidates = [
        explicit,
        shutil.which("google-chrome"),
        shutil.which("chromium"),
        shutil.which("chromium-browser"),
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    return next(
        (
            candidate
            for candidate in candidates
            if candidate and Path(candidate).is_file()
        ),
        None,
    )


def chromedriver_binary(browser: str) -> Optional[str]:
    result = subprocess.run(
        [browser, "--version"],
        capture_output=True,
        text=True,
        check=False,
    )
    match = re.search(r"\b(\d+)\.", result.stdout + result.stderr)
    browser_major = match.group(1) if match else None
    candidates = [shutil.which("chromedriver")]
    cache = Path.home() / ".cache" / "selenium" / "chromedriver"
    if cache.is_dir():
        candidates.extend(
            str(path)
            for path in sorted(cache.glob("*/*/chromedriver"), reverse=True)
        )
    return next(
        (
            candidate
            for candidate in candidates
            if candidate
            and Path(candidate).is_file()
            and (
                browser_major is None
                or any(
                    part == browser_major
                    or part.startswith(browser_major + ".")
                    for part in Path(candidate).parts[-3:]
                )
            )
        ),
        None,
    )


def browser_audit(
    site_dir: Path,
    explicit_chrome: Optional[str],
    errors: list[str],
) -> tuple[int, str, int]:
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.support.ui import WebDriverWait
    except ImportError:
        errors.append("browser audit requires Selenium")
        return 0, "unknown", 0
    binary = chrome_binary(explicit_chrome)
    if binary is None:
        errors.append("browser audit could not find Chrome or Chromium")
        return 0, "unknown", 0
    pages = sorted(site_dir.glob("**/index.html"))
    options = Options()
    options.binary_location = binary
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.set_capability("pageLoadStrategy", "eager")
    options.set_capability("goog:loggingPrefs", {"browser": "ALL"})
    driver_path = chromedriver_binary(binary)
    service = Service(executable_path=driver_path) if driver_path else Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(45)
    driver.set_script_timeout(30)
    wait = WebDriverWait(driver, 30)
    rendered = 0
    version = "unknown"
    visits = 0
    with serve_directory(site_dir) as base_url:
        try:
            for width, height, mobile in (
                (1440, 1000, False),
                (390, 844, True),
            ):
                driver.execute_cdp_cmd(
                    "Emulation.setDeviceMetricsOverride",
                    {
                        "width": width,
                        "height": height,
                        "deviceScaleFactor": 1,
                        "mobile": mobile,
                    },
                )
                for page in pages:
                    relative = page.relative_to(site_dir)
                    route = (
                        "/"
                        if relative == Path("index.html")
                        else "/" + relative.parent.as_posix() + "/"
                    )
                    visits += 1
                    try:
                        wrappers = 0
                        for attempt in range(3):
                            try:
                                driver.get_log("browser")
                                driver.get(base_url + route)
                                wrappers = driver.execute_script(
                                    "return document.querySelectorAll("
                                    "'.arithmatex').length"
                                )
                                if wrappers:
                                    wait.until(
                                        lambda current: current.execute_script(
                                            "return !!(window.MathJax && "
                                            "window.MathJax.version)"
                                        )
                                    )
                                    ready = driver.execute_async_script(
                                        """
                                        const done = arguments[0];
                                        Promise.resolve(
                                          window.MathJax.startup.promise
                                        )
                                          .then(() => document.fonts
                                            ? document.fonts.ready
                                            : Promise.resolve())
                                          .then(() => new Promise((resolve) =>
                                            requestAnimationFrame(() =>
                                              requestAnimationFrame(resolve))))
                                          .then(() => done(true))
                                          .catch((error) =>
                                            done(String(error)));
                                        """
                                    )
                                    if ready is not True:
                                        raise RuntimeError(
                                            f"MathJax startup failed: {ready}"
                                        )
                                else:
                                    driver.execute_async_script(
                                        """
                                        const done = arguments[0];
                                        Promise.resolve(document.fonts
                                          ? document.fonts.ready
                                          : Promise.resolve())
                                          .then(() => requestAnimationFrame(() =>
                                            requestAnimationFrame(() =>
                                              done(true))));
                                        """
                                    )
                                images_ready = driver.execute_async_script(
                                    """
                                    const done = arguments[0];
                                    const images = [
                                      ...document.querySelectorAll(
                                        'article.md-content__inner img'
                                      )
                                    ];
                                    images.forEach((image) => {
                                      image.loading = 'eager';
                                    });
                                    const pending = images.map((image) => {
                                      if (image.complete && image.naturalWidth) {
                                        return Promise.resolve();
                                      }
                                      return new Promise((resolve, reject) => {
                                        const finish = () => {
                                          image.removeEventListener(
                                            'load',
                                            finish
                                          );
                                          image.removeEventListener(
                                            'error',
                                            fail
                                          );
                                          resolve();
                                        };
                                        const fail = () => reject(
                                          new Error(
                                            `image failed: ${image.currentSrc}`
                                          )
                                        );
                                        image.addEventListener(
                                          'load',
                                          finish,
                                          {once: true}
                                        );
                                        image.addEventListener(
                                          'error',
                                          fail,
                                          {once: true}
                                        );
                                      });
                                    });
                                    Promise.race([
                                      Promise.all(pending),
                                      new Promise((_, reject) =>
                                        setTimeout(
                                          () => reject(
                                            new Error('image load timeout')
                                          ),
                                          8000
                                        )
                                      ),
                                    ])
                                      .then(() => done(true))
                                      .catch((error) =>
                                        done(String(error)));
                                    """
                                )
                                if images_ready is not True:
                                    raise RuntimeError(
                                        f"image loading failed: {images_ready}"
                                    )
                                break
                            except Exception:
                                driver.get_log("browser")
                                if attempt == 2:
                                    raise
                        stats = driver.execute_script(
                            """
                            const wrappers = [
                              ...document.querySelectorAll('.arithmatex')
                            ];
                            const article = document.querySelector(
                              'article.md-content__inner'
                            );
                            const parseColor = (value) => {
                              const normalized = value.trim().toLowerCase();
                              const values = normalized.match(
                                /-?(?:\\d+(?:\\.\\d*)?|\\.\\d+)%?/g
                              );
                              if (!values || values.length < 3) return null;
                              const percentage = (item, scale) =>
                                item.endsWith('%')
                                  ? Number.parseFloat(item) * scale / 100
                                  : Number.parseFloat(item);
                              if (normalized.startsWith('color(srgb')) {
                                return {
                                  r: percentage(values[0], 1) * 255,
                                  g: percentage(values[1], 1) * 255,
                                  b: percentage(values[2], 1) * 255,
                                  a: values[3]
                                    ? percentage(values[3], 1)
                                    : 1,
                                };
                              }
                              if (normalized.startsWith('rgb')) {
                                return {
                                  r: percentage(values[0], 255),
                                  g: percentage(values[1], 255),
                                  b: percentage(values[2], 255),
                                  a: values[3]
                                    ? percentage(values[3], 1)
                                    : 1,
                                };
                              }
                              return null;
                            };
                            const composite = (front, back) => {
                              const alpha = front.a + back.a * (1 - front.a);
                              if (!alpha) {
                                return {r: 0, g: 0, b: 0, a: 0};
                              }
                              return {
                                r: (
                                  front.r * front.a
                                  + back.r * back.a * (1 - front.a)
                                ) / alpha,
                                g: (
                                  front.g * front.a
                                  + back.g * back.a * (1 - front.a)
                                ) / alpha,
                                b: (
                                  front.b * front.a
                                  + back.b * back.a * (1 - front.a)
                                ) / alpha,
                                a: alpha,
                              };
                            };
                            const effectiveBackground = (element) => {
                              const chain = [];
                              for (
                                let node = element;
                                node instanceof Element;
                                node = node.parentElement
                              ) {
                                chain.push(node);
                              }
                              let color = {r: 255, g: 255, b: 255, a: 1};
                              for (const node of chain.reverse()) {
                                const layer = parseColor(
                                  getComputedStyle(node).backgroundColor
                                );
                                if (layer) color = composite(layer, color);
                              }
                              return color;
                            };
                            const luminance = (color) => {
                              const channel = (value) => {
                                const normalized = value / 255;
                                return normalized <= 0.04045
                                  ? normalized / 12.92
                                  : Math.pow(
                                    (normalized + 0.055) / 1.055,
                                    2.4
                                  );
                              };
                              return (
                                0.2126 * channel(color.r)
                                + 0.7152 * channel(color.g)
                                + 0.0722 * channel(color.b)
                              );
                            };
                            const contrast = (front, back) => {
                              const foreground = composite(front, back);
                              const a = luminance(foreground);
                              const b = luminance(back);
                              return (
                                Math.max(a, b) + 0.05
                              ) / (Math.min(a, b) + 0.05);
                            };
                            const figureIssues = [];
                            const previousScheme = document.body.getAttribute(
                              'data-md-color-scheme'
                            );
                            for (const scheme of ['default', 'slate']) {
                              document.body.setAttribute(
                                'data-md-color-scheme',
                                scheme
                              );
                              void document.body.offsetWidth;
                              for (const figure of document.querySelectorAll(
                                'article.md-content__inner .knowledge-figure'
                              )) {
                                const label = figure.id || '<missing-id>';
                                const caption = figure.querySelector(
                                  'figcaption'
                                );
                                const image = figure.querySelector('img');
                                const media = figure.querySelector(
                                  'a.knowledge-figure__image-link[href]'
                                );
                                if (!caption || !image || !media) {
                                  figureIssues.push(
                                    `${scheme}:${label}: incomplete figure`
                                  );
                                  continue;
                                }
                                const background = effectiveBackground(caption);
                                const foreground = parseColor(
                                  getComputedStyle(caption).color
                                );
                                if (!foreground) {
                                  figureIssues.push(
                                    `${scheme}:${label}: unreadable color`
                                  );
                                } else {
                                  const ratio = contrast(
                                    foreground,
                                    background
                                  );
                                  if (ratio < 4.5) {
                                    figureIssues.push(
                                      `${scheme}:${label}: caption contrast `
                                      + `${ratio.toFixed(2)}:1`
                                    );
                                  }
                                }
                                const rect = figure.getBoundingClientRect();
                                const imageRect = image.getBoundingClientRect();
                                const viewport =
                                  document.documentElement.clientWidth;
                                if (
                                  rect.left < -1
                                  || rect.right > viewport + 1
                                  || imageRect.width > rect.width + 1
                                ) {
                                  figureIssues.push(
                                    `${scheme}:${label}: viewport overflow`
                                  );
                                }
                                if (
                                  !image.complete
                                  || !image.naturalWidth
                                  || !image.naturalHeight
                                ) {
                                  figureIssues.push(
                                    `${scheme}:${label}: image unavailable`
                                  );
                                } else {
                                  const intrinsic =
                                    image.naturalWidth / image.naturalHeight;
                                  const rendered =
                                    image.clientWidth / image.clientHeight;
                                  if (
                                    !Number.isFinite(rendered)
                                    || Math.abs(intrinsic - rendered) > 0.02
                                  ) {
                                    figureIssues.push(
                                      `${scheme}:${label}: distorted image`
                                    );
                                  }
                                }
                              }
                            }
                            if (previousScheme === null) {
                              document.body.removeAttribute(
                                'data-md-color-scheme'
                              );
                            } else {
                              document.body.setAttribute(
                                'data-md-color-scheme',
                                previousScheme
                              );
                            }
                            const clone = article ? article.cloneNode(true) : null;
                            if (clone) {
                              clone.querySelectorAll(
                                'pre, code, script, style, .arithmatex'
                              ).forEach((node) => node.remove());
                            }
                            const raw = clone
                              ? /\\\\(?:[A-Za-z]+|[\\[\\]()])/.test(
                                  clone.textContent
                                )
                              : false;
                            const invalid = wrappers.filter((element) =>
                              element.querySelectorAll(
                                ':scope > mjx-container'
                              ).length !== 1
                              || element.querySelectorAll(
                                'mjx-assistive-mml mjx-container'
                              ).length !== 0
                            ).length;
                            const mathErrors = [
                              ...document.querySelectorAll(
                                'mjx-merror, .MathJax_Error'
                              )
                            ].map((node) => node.textContent.trim());
                            const badOverflow = wrappers.filter((element) => {
                              if (element.tagName !== 'DIV') return false;
                              if (element.scrollWidth <= element.clientWidth + 1) {
                                return false;
                              }
                              const overflow = getComputedStyle(element).overflowX;
                              return overflow !== 'auto'
                                && overflow !== 'scroll';
                            }).length;
                            const inlineMathIssues = wrappers.filter((element) => {
                              if (element.tagName !== 'SPAN') return false;
                              const style = getComputedStyle(element);
                              const shift = Number.parseFloat(style.verticalAlign);
                              const fontSize = Number.parseFloat(style.fontSize);
                              const ratio = shift / fontSize;
                              return style.display !== 'inline-block'
                                || style.overflowX !== 'visible'
                                || style.overflowY !== 'visible'
                                || !Number.isFinite(ratio)
                                || ratio < -0.24
                                || ratio > -0.20;
                            }).length;
                            const displayMathIssues = wrappers.filter((element) => {
                              if (element.tagName !== 'DIV') return false;
                              const overflow = getComputedStyle(element).overflowX;
                              return overflow !== 'auto'
                                && overflow !== 'scroll';
                            }).length;
                            const brokenImages = [
                              ...document.querySelectorAll(
                                'article.md-content__inner img'
                              )
                            ].filter((image) =>
                              image.complete && image.naturalWidth === 0
                            ).length;
                            const codeElements = [
                              ...document.querySelectorAll(
                                'article.md-content__inner pre, '
                                + 'article.md-content__inner pre > code'
                              )
                            ];
                            const codeOverflow = codeElements.filter((element) =>
                              element.scrollWidth > element.clientWidth + 1
                            ).length;
                            const unwrappedCode = [
                              ...document.querySelectorAll(
                                'article.md-content__inner pre > code'
                              )
                            ].filter((element) => {
                              const style = getComputedStyle(element);
                              return style.whiteSpace !== 'pre-wrap'
                                || !['anywhere', 'break-word'].includes(
                                  style.overflowWrap
                                );
                            }).length;
                            const viewportWidth =
                              document.documentElement.clientWidth;
                            const documentOverflow =
                              document.documentElement.scrollWidth
                              > viewportWidth + 1;
                            const overflowNodes = documentOverflow
                              ? [...document.querySelectorAll('body *')]
                                .map((element) => {
                                  const rect = element.getBoundingClientRect();
                                  const style = getComputedStyle(element);
                                  const className =
                                    typeof element.className === 'string'
                                      ? element.className.trim()
                                      : '';
                                  return {
                                    label: element.tagName.toLowerCase()
                                      + (element.id ? `#${element.id}` : '')
                                      + (className
                                        ? `.${className.replace(/\\s+/g, '.')}`
                                        : ''),
                                    right: Math.round(rect.right * 10) / 10,
                                    width: Math.round(rect.width * 10) / 10,
                                    scrollWidth: element.scrollWidth,
                                    clientWidth: element.clientWidth,
                                    overflowX: style.overflowX,
                                  };
                                })
                                .filter((item) =>
                                  item.width > 0
                                  && item.right > viewportWidth + 1)
                                .sort((left, right) =>
                                  right.right - left.right)
                                .slice(0, 8)
                              : [];
                            return {
                              version: window.MathJax
                                && window.MathJax.version
                                ? window.MathJax.version
                                : null,
                              wrappers: wrappers.length,
                              invalid,
                              mathErrors,
                              badOverflow,
                              inlineMathIssues,
                              displayMathIssues,
                              brokenImages,
                              codeOverflow,
                              unwrappedCode,
                              figureIssues,
                              raw,
                              article: !!article,
                              documentOverflow,
                              overflowNodes,
                            };
                            """
                        )
                        if stats["version"]:
                            version = stats["version"]
                        rendered += stats["wrappers"]
                        if (
                            stats["wrappers"]
                            and stats["version"] != EXPECTED_MATHJAX_VERSION
                        ):
                            errors.append(
                                f"{route}: expected MathJax "
                                f"{EXPECTED_MATHJAX_VERSION}, loaded "
                                f"{stats['version']}"
                            )
                        if not stats["article"]:
                            errors.append(f"{route}: missing documentation article")
                        if stats["invalid"]:
                            errors.append(
                                f"{route}: {stats['invalid']} formulas were not "
                                "rendered exactly once"
                            )
                        if stats["mathErrors"]:
                            errors.append(
                                f"{route}: MathJax errors: "
                                + "; ".join(stats["mathErrors"])
                            )
                        if stats["raw"]:
                            errors.append(f"{route}: visible prose leaks raw TeX")
                        if stats["badOverflow"]:
                            errors.append(
                                f"{route}: {stats['badOverflow']} formulas "
                                f"overflow at {width}px without scrolling"
                            )
                        if stats["inlineMathIssues"]:
                            errors.append(
                                f"{route}: {stats['inlineMathIssues']} inline "
                                "formulas violate the shared baseline or "
                                "clipping contract"
                            )
                        if stats["displayMathIssues"]:
                            errors.append(
                                f"{route}: {stats['displayMathIssues']} display "
                                "formulas lack horizontal overflow handling"
                            )
                        if stats["brokenImages"]:
                            errors.append(
                                f"{route}: {stats['brokenImages']} broken images"
                            )
                        if stats["figureIssues"]:
                            errors.append(
                                f"{route}: figure audit: "
                                + "; ".join(stats["figureIssues"])
                            )
                        if stats["documentOverflow"]:
                            overflow_detail = "; ".join(
                                f"{item['label']} right={item['right']} "
                                f"width={item['width']} "
                                f"scroll/client={item['scrollWidth']}/"
                                f"{item['clientWidth']} "
                                f"overflow-x={item['overflowX']}"
                                for item in stats["overflowNodes"]
                            )
                            errors.append(
                                f"{route}: page has horizontal overflow at "
                                f"{width}px"
                                + (
                                    f": {overflow_detail}"
                                    if overflow_detail
                                    else ""
                                )
                            )
                        if mobile and stats["codeOverflow"]:
                            errors.append(
                                f"{route}: {stats['codeOverflow']} code containers "
                                f"overflow at {width}px"
                            )
                        if mobile and stats["unwrappedCode"]:
                            errors.append(
                                f"{route}: {stats['unwrappedCode']} code blocks "
                                f"lack pre-wrap/overflow-wrap at {width}px"
                            )
                        logs = driver.get_log("browser")
                        severe = [
                            item["message"]
                            for item in logs
                            if item["level"] == "SEVERE"
                            and re.search(
                                r"mathjax|tex-mml-chtml",
                                item["message"],
                                re.IGNORECASE,
                            )
                        ]
                        if severe and stats["wrappers"]:
                            errors.append(
                                f"{route}: browser reported MathJax load errors: "
                                + "; ".join(severe)
                            )
                    except Exception as exc:
                        errors.append(
                            f"{route}: browser audit failed at {width}px "
                            f"after three attempts: {type(exc).__name__}: {exc}"
                        )
            problem_page = site_dir / "problems" / "index.html"
            changelog_page = site_dir / "changelog" / "index.html"
            if problem_page.is_file() and changelog_page.is_file():
                try:
                    driver.execute_cdp_cmd(
                        "Emulation.setDeviceMetricsOverride",
                        {
                            "width": 1440,
                            "height": 1000,
                            "deviceScaleFactor": 1,
                            "mobile": False,
                        },
                    )
                    visits += 1
                    driver.get(base_url + "/problems/")
                    problem_stats = wait.until(
                        lambda current: current.execute_script(
                            """
                            const details = [
                              ...document.querySelectorAll('details.problem')
                            ];
                            const anchors = [
                              ...document.querySelectorAll(
                                '.problem-anchor[id^="problem-"]'
                              )
                            ];
                            return {
                              details: details.length,
                              anchors: anchors.length,
                              open: details.filter((item) => item.open).length,
                            };
                            """
                        )
                    )
                    if (
                        not problem_stats["details"]
                        or problem_stats["anchors"] != problem_stats["details"]
                    ):
                        errors.append(
                            "/problems/: problem details and stable anchors "
                            "must have equal nonzero counts"
                        )
                    if problem_stats["open"]:
                        errors.append(
                            "/problems/: problem details must be collapsed "
                            "without a fragment"
                        )
                    visits += 1
                    driver.get(base_url + "/changelog/")
                    link = wait.until(
                        lambda current: current.find_element(
                            By.CSS_SELECTOR,
                            'a[href*="/problems/#problem-"]',
                        )
                    )
                    target_url = link.get_attribute("href")
                    fragment = target_url.partition("#")[2]
                    link.click()
                    wait.until(
                        lambda current: current.current_url.endswith(
                            "#" + fragment
                        )
                    )
                    driver.execute_async_script(
                        """
                        const done = arguments[0];
                        requestAnimationFrame(() =>
                          requestAnimationFrame(() =>
                            setTimeout(done, 300)));
                        """
                    )
                    deep_link_stats = wait.until(
                        lambda current: current.execute_script(
                            """
                            const fragment = decodeURIComponent(
                              window.location.hash.slice(1)
                            );
                            const anchor = document.getElementById(fragment);
                            const details = anchor?.nextElementSibling;
                            return {
                              target: !!anchor,
                              opened: details instanceof HTMLDetailsElement
                                && details.classList.contains('problem')
                                && details.open,
                              openCount: document.querySelectorAll(
                                'details.problem[open]'
                              ).length,
                              top: anchor
                                ? anchor.getBoundingClientRect().top
                                : null,
                            };
                            """
                        )
                    )
                    if not driver.current_url.endswith("#" + fragment):
                        errors.append(
                            f"/problems/#{fragment}: another navigation "
                            "behavior replaced the stable fragment"
                        )
                    if not deep_link_stats["target"]:
                        errors.append(
                            f"/problems/#{fragment}: target anchor is missing"
                        )
                    if (
                        not deep_link_stats["opened"]
                        or deep_link_stats["openCount"] != 1
                    ):
                        errors.append(
                            f"/problems/#{fragment}: deep link must open only "
                            "its target disclosure"
                        )
                    top = deep_link_stats["top"]
                    if top is None or not -1 <= top <= 180:
                        errors.append(
                            f"/problems/#{fragment}: target is outside the "
                            f"expected viewport position ({top})"
                        )
                except Exception as exc:
                    errors.append(
                        "problem deep-link browser audit failed: "
                        f"{type(exc).__name__}: {exc}"
                    )
            driver.execute_cdp_cmd("Emulation.clearDeviceMetricsOverride", {})
        finally:
            driver.quit()
    return rendered, version, visits


def source_paths(root: Path) -> list[Path]:
    paths = [root / "README.md"]
    paths.extend(sorted((root / "docs").rglob("*.md")))
    includes = root / "includes"
    if includes.is_dir():
        paths.extend(sorted(includes.rglob("*.md")))
    return [path for path in paths if path.is_file()]


def validate_fixtures(errors: list[str]) -> None:
    bad = {
        "legacy": r"Bad \(x\).",
        "unclosed": "Bad $x.",
        "brace": "$x_{i$",
        "plain": r"Bad \frac{1}{2}.",
    }
    for name, text in bad.items():
        _, fixture_errors = scan_markdown(Path(f"<fixture:{name}>"), text)
        if not fixture_errors:
            errors.append(f"checker fixture did not reject {name}")
    good = "$x_i$.\n\n$$\n\\frac{1}{2}\n$$\n\n`$code$`\n"
    _, fixture_errors = scan_markdown(Path("<fixture:good>"), good)
    if fixture_errors:
        errors.append(
            "checker rejected its valid fixture: " + "; ".join(fixture_errors)
        )


def parse_args(argv: Optional[Sequence[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--site-dir",
        type=Path,
        help="compare source mathematics with an existing MkDocs output",
    )
    parser.add_argument(
        "--browser",
        action="store_true",
        help="render every generated page at desktop and mobile widths",
    )
    parser.add_argument(
        "--chrome-binary",
        help="explicit Chrome or Chromium executable for --browser",
    )
    parser.add_argument(
        "--fix-legacy-delimiters",
        action="store_true",
        help="replace legacy math delimiters outside code with canonical dollars",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    root = Path(__file__).resolve().parents[1]
    paths = source_paths(root)
    if args.fix_legacy_delimiters:
        changed = 0
        replacements = 0
        for path in paths:
            text = path.read_text(encoding="utf-8")
            updated, count = canonicalize_legacy_math(
                path.relative_to(root),
                text,
            )
            if updated != text:
                path.write_text(updated, encoding="utf-8")
                changed += 1
                replacements += count
        print(
            f"canonicalized {replacements} delimiters across {changed} files"
        )
    errors: list[str] = []
    validate_fixtures(errors)
    expression_total = 0
    math_files = 0
    for path in paths:
        expressions, path_errors = scan_markdown(
            path.relative_to(root),
            path.read_text(encoding="utf-8"),
        )
        expression_total += len(expressions)
        math_files += bool(expressions)
        errors.extend(path_errors)
    print(
        f"source: {expression_total} expressions in {math_files} "
        f"of {len(paths)} Markdown files"
    )
    site_dir: Optional[Path] = None
    if args.site_dir:
        site_dir = args.site_dir
        if not site_dir.is_absolute():
            site_dir = root / site_dir
        if not site_dir.is_dir():
            errors.append(f"generated site directory does not exist: {site_dir}")
        else:
            generated = compare_generated_site(root, site_dir, paths, errors)
            print(f"generated HTML: {generated} Arithmatex expressions")
    if args.browser:
        if site_dir is None:
            site_dir = root / "site"
        if not site_dir.is_dir():
            errors.append(f"browser site directory does not exist: {site_dir}")
        else:
            rendered, version, visits = browser_audit(
                site_dir,
                args.chrome_binary,
                errors,
            )
            print(
                f"browser: {rendered} rendered expressions across "
                f"{visits} page visits with MathJax {version}"
            )
    if errors:
        print("\nRendering check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Rendering check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
