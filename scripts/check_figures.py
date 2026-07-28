#!/usr/bin/env python3
"""Validate visual assets, provenance, Markdown placements, and generated HTML."""

from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
FIGURES = DOCS / "assets" / "figures"
MANIFEST = FIGURES / "manifest.json"
SHA256 = re.compile(r"^[0-9a-f]{64}$")
SLUG = re.compile(r"^figure-[a-z0-9][a-z0-9-]*$")
FIGURE_BLOCK = re.compile(
    r"<figure\b(?P<attrs>[^>]*)>(?P<body>.*?)</figure>",
    re.DOTALL,
)
HTML_ATTR = re.compile(
    r"""(?P<name>[A-Za-z_:][A-Za-z0-9_.:-]*)
        (?:\s*=\s*(?:"(?P<double>[^"]*)"|'(?P<single>[^']*)'))?""",
    re.VERBOSE,
)
IMG = re.compile(r"<img\b(?P<attrs>[^>]*)>", re.DOTALL)
LINK = re.compile(r"<a\b(?P<attrs>[^>]*)>", re.DOTALL)
CAPTION = re.compile(r"<figcaption\b[^>]*>(?P<body>.*?)</figcaption>", re.DOTALL)
TAG = re.compile(r"<[^>]+>")
REFERENCE = re.compile(r"(?m)^## Reference\s*$")
MD_LINK = re.compile(r"\[[^\]\n]+\]\((?:https://|http://)[^)\n]+\)")
REMOTE_IMAGE = re.compile(
    r"!\[[^\]]*\]\((?:https?:)?//|<img\b[^>]*\bsrc=[\"'](?:https?:)?//",
    re.IGNORECASE,
)
PRIVATE = re.compile(
    r"/Users/|(?:^|[/\\])\.codex(?:[/\\]|$)|"
    r"(?:private|hidden)\s+(?:prompt|instruction)|conversation history",
    re.IGNORECASE,
)
SVG_FORBIDDEN_TAGS = {
    "script",
    "foreignObject",
    "iframe",
    "object",
    "embed",
    "image",
    "audio",
    "video",
}


class DuplicateKey(ValueError):
    pass


def no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKey(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def attrs(raw: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for match in HTML_ATTR.finditer(raw):
        value = match.group("double")
        if value is None:
            value = match.group("single")
        result[match.group("name")] = value or ""
    return result


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def number(value: str | None, label: str, errors: list[str]) -> float | None:
    try:
        return float(value or "")
    except ValueError:
        errors.append(f"{label}: expected a numeric SVG coordinate")
        return None


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def geometry_bounds(
    root: ET.Element,
    width: float,
    height: float,
    label: str,
    errors: list[str],
) -> None:
    """Reject generated primitives whose declared coordinates leave the viewport."""

    def check(values: list[float], axis: str, element: str) -> None:
        limit = width if axis == "x" else height
        if any(value < -0.01 or value > limit + 0.01 for value in values):
            errors.append(
                f"{label}: <{element}> has {axis}-coordinates outside "
                f"the {int(width)}×{int(height)} viewport"
            )

    for element in root:
        tag = local_name(element.tag)
        if tag in ("title", "desc", "defs"):
            continue
        if tag == "rect":
            x = number(element.get("x", "0"), label, errors)
            y = number(element.get("y", "0"), label, errors)
            w = number(element.get("width"), label, errors)
            h = number(element.get("height"), label, errors)
            if None not in (x, y, w, h):
                check([x, x + w], "x", tag)
                check([y, y + h], "y", tag)
        elif tag == "circle":
            cx = number(element.get("cx"), label, errors)
            cy = number(element.get("cy"), label, errors)
            radius = number(element.get("r"), label, errors)
            if None not in (cx, cy, radius):
                check([cx - radius, cx + radius], "x", tag)
                check([cy - radius, cy + radius], "y", tag)
        elif tag == "line":
            xs = [
                number(element.get("x1"), label, errors),
                number(element.get("x2"), label, errors),
            ]
            ys = [
                number(element.get("y1"), label, errors),
                number(element.get("y2"), label, errors),
            ]
            if None not in xs:
                check([value for value in xs if value is not None], "x", tag)
            if None not in ys:
                check([value for value in ys if value is not None], "y", tag)
        elif tag == "text":
            x = number(element.get("x"), label, errors)
            y = number(element.get("y"), label, errors)
            if x is not None:
                check([x], "x", tag)
            if y is not None:
                check([y], "y", tag)
        elif tag == "path":
            values = [
                float(value)
                for value in re.findall(r"-?(?:\d+(?:\.\d*)?|\.\d+)", element.get("d", ""))
            ]
            check(values[0::2], "x", tag)
            check(values[1::2], "y", tag)


def validate_svg(path: Path, record: dict[str, Any], errors: list[str]) -> None:
    label = str(path.relative_to(ROOT))
    if digest(path) != record.get("sha256"):
        errors.append(f"{label}: SHA-256 differs from manifest")
    if PRIVATE.search(path.read_text(encoding="utf-8")):
        errors.append(f"{label}: contains private path or workflow language")
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        errors.append(f"{label}: invalid XML: {exc}")
        return
    if local_name(root.tag) != "svg":
        errors.append(f"{label}: root element must be <svg>")
        return
    width = number(root.get("width"), label, errors)
    height = number(root.get("height"), label, errors)
    if width is None or height is None:
        return
    if width != record.get("width") or height != record.get("height"):
        errors.append(f"{label}: SVG dimensions differ from manifest")
    if root.get("viewBox") != f"0 0 {int(width)} {int(height)}":
        errors.append(f"{label}: viewBox must match width and height")
    if root.get("role") != "img" or not root.get("aria-labelledby"):
        errors.append(f"{label}: SVG needs role=img and aria-labelledby")
    title = next((item for item in root if local_name(item.tag) == "title"), None)
    desc = next((item for item in root if local_name(item.tag) == "desc"), None)
    if title is None or not "".join(title.itertext()).strip():
        errors.append(f"{label}: SVG needs a non-empty title")
    if desc is None or not "".join(desc.itertext()).strip():
        errors.append(f"{label}: SVG needs a non-empty description")
    for element in root.iter():
        tag = local_name(element.tag)
        if tag in SVG_FORBIDDEN_TAGS:
            errors.append(f"{label}: forbidden SVG element <{tag}>")
        for name, value in element.attrib.items():
            local = local_name(name).lower()
            if local.startswith("on"):
                errors.append(f"{label}: event-handler attribute {local} is forbidden")
            if local in ("href", "src") and value and not value.startswith("#"):
                errors.append(f"{label}: external SVG reference is forbidden: {value}")
            if re.search(r"(?:https?:|javascript:|data:|file:|//)", value, re.I):
                errors.append(f"{label}: unsafe or external SVG attribute: {local}")
    geometry_bounds(root, width, height, label, errors)


def generated_html_path(site_dir: Path, markdown: Path) -> Path:
    relative = markdown.relative_to(DOCS)
    if relative == Path("index.md"):
        return site_dir / "index.html"
    if relative.name == "index.md":
        return site_dir / relative.parent / "index.html"
    return site_dir / relative.with_suffix("") / "index.html"


def rendered_asset_href(page: Path, asset: Path) -> str:
    relative_page = page.relative_to(DOCS)
    route_directory = (
        relative_page.parent
        if relative_page.name == "index.md"
        else relative_page.with_suffix("")
    )
    target = asset.relative_to(DOCS)
    return Path(os.path.relpath(target, route_directory)).as_posix()


class HtmlFigures(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.figures: dict[str, dict[str, Any]] = {}
        self.current: dict[str, Any] | None = None
        self.in_caption = False

    @staticmethod
    def attr_map(values: list[tuple[str, str | None]]) -> dict[str, str]:
        return {name: value or "" for name, value in values}

    def handle_starttag(self, tag: str, values: list[tuple[str, str | None]]) -> None:
        data = self.attr_map(values)
        if tag == "figure" and "knowledge-figure" in data.get("class", "").split():
            self.current = {"attrs": data, "images": [], "links": [], "caption": []}
            key = data.get("id", "")
            self.figures[key] = self.current
        elif self.current is not None and tag == "img":
            self.current["images"].append(data)
        elif self.current is not None and tag == "a":
            self.current["links"].append(data)
        elif self.current is not None and tag == "figcaption":
            self.in_caption = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "figcaption":
            self.in_caption = False
        elif tag == "figure":
            self.current = None

    def handle_data(self, data: str) -> None:
        if self.current is not None and self.in_caption:
            self.current["caption"].append(data)


def load_manifest(errors: list[str]) -> list[dict[str, Any]]:
    try:
        payload = json.loads(
            MANIFEST.read_text(encoding="utf-8"),
            object_pairs_hook=no_duplicate_keys,
        )
    except (OSError, json.JSONDecodeError, DuplicateKey) as exc:
        errors.append(f"{MANIFEST.relative_to(ROOT)}: {exc}")
        return []
    if set(payload) != {"schema_version", "generated_by", "assets"}:
        errors.append("figure manifest has missing or unknown top-level fields")
    if payload.get("schema_version") != 1:
        errors.append("figure manifest schema_version must be 1")
    if payload.get("generated_by") != "scripts/render_visuals.py":
        errors.append("figure manifest generated_by is unexpected")
    assets = payload.get("assets")
    if not isinstance(assets, list):
        errors.append("figure manifest assets must be an array")
        return []
    return [record for record in assets if isinstance(record, dict)]


def validate_source(site_dir: Path | None) -> list[str]:
    errors: list[str] = []
    process = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "render_visuals.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if process.returncode:
        errors.append((process.stdout + process.stderr).strip())
    records = load_manifest(errors)
    expected_keys = {
        "file",
        "title",
        "description",
        "kind",
        "width",
        "height",
        "license",
        "source",
        "sha256",
        "placements",
    }
    files: set[Path] = set()
    placements: dict[tuple[Path, str], tuple[dict[str, Any], Path]] = {}
    for index, record in enumerate(records):
        label = f"manifest asset #{index + 1}"
        if set(record) != expected_keys:
            errors.append(f"{label}: missing or unknown fields")
        raw_file = record.get("file")
        if not isinstance(raw_file, str) or not raw_file.startswith("docs/assets/figures/"):
            errors.append(f"{label}: invalid file path")
            continue
        path = ROOT / raw_file
        if path.suffix != ".svg" or not path.is_file():
            errors.append(f"{label}: SVG asset is missing: {raw_file}")
            continue
        if path in files:
            errors.append(f"{label}: duplicate asset file: {raw_file}")
        files.add(path)
        if record.get("kind") != "original-svg":
            errors.append(f"{label}: kind must be original-svg")
        if record.get("license") != "MIT":
            errors.append(f"{label}: original diagrams must record the repository MIT license")
        if record.get("source") != "Repository-authored explanatory diagram":
            errors.append(f"{label}: source description is unexpected")
        if not isinstance(record.get("sha256"), str) or not SHA256.fullmatch(record["sha256"]):
            errors.append(f"{label}: invalid SHA-256")
        validate_svg(path, record, errors)
        raw_placements = record.get("placements")
        if not isinstance(raw_placements, list) or not raw_placements:
            errors.append(f"{label}: placements must be a non-empty array")
            continue
        for placement in raw_placements:
            if not isinstance(placement, dict) or set(placement) != {"page", "id"}:
                errors.append(f"{label}: invalid placement object")
                continue
            page_value, anchor = placement.get("page"), placement.get("id")
            if not isinstance(page_value, str) or not page_value.startswith("docs/"):
                errors.append(f"{label}: invalid placement page")
                continue
            page = ROOT / page_value
            if not page.is_file() or page.suffix != ".md":
                errors.append(f"{label}: placement page is missing: {page_value}")
                continue
            if not isinstance(anchor, str) or not SLUG.fullmatch(anchor):
                errors.append(f"{label}: invalid placement id: {anchor}")
                continue
            key = (page, anchor)
            if key in placements:
                errors.append(f"{label}: duplicate placement {page_value}#{anchor}")
            placements[key] = (record, path)
    actual_files = set(FIGURES.glob("*.svg"))
    for path in sorted(actual_files - files):
        errors.append(f"{path.relative_to(ROOT)}: unregistered SVG asset")
    for path in sorted(files - actual_files):
        errors.append(f"{path.relative_to(ROOT)}: registered SVG asset is missing")
    found: set[tuple[Path, str]] = set()
    ids: set[str] = set()
    for page in sorted(DOCS.rglob("*.md")):
        text = page.read_text(encoding="utf-8")
        if REMOTE_IMAGE.search(text):
            errors.append(f"{page.relative_to(ROOT)}: remote image hotlink is forbidden")
        if PRIVATE.search(text):
            errors.append(f"{page.relative_to(ROOT)}: contains private path or workflow language")
        for match in FIGURE_BLOCK.finditer(text):
            figure_attrs = attrs(match.group("attrs"))
            if "knowledge-figure" not in figure_attrs.get("class", "").split():
                continue
            anchor = figure_attrs.get("id", "")
            key = (page, anchor)
            found.add(key)
            if anchor in ids:
                errors.append(f"{page.relative_to(ROOT)}: duplicate figure id {anchor}")
            ids.add(anchor)
            if key not in placements:
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: unregistered placement")
                continue
            record, asset = placements[key]
            body = match.group("body")
            images = list(IMG.finditer(body))
            links = list(LINK.finditer(body))
            captions = list(CAPTION.finditer(body))
            if len(images) != 1 or len(links) != 1 or len(captions) != 1:
                errors.append(
                    f"{page.relative_to(ROOT)}#{anchor}: expected one image, one link, and one caption"
                )
                continue
            image_attrs = attrs(images[0].group("attrs"))
            link_attrs = attrs(links[0].group("attrs"))
            wanted = rendered_asset_href(page, asset)
            if image_attrs.get("src") != wanted or link_attrs.get("href") != wanted:
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: asset path or high-resolution link differs from manifest")
            if not image_attrs.get("alt", "").strip():
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: alt text is empty")
            if image_attrs.get("width") != str(record.get("width")) or image_attrs.get("height") != str(record.get("height")):
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: intrinsic dimensions differ from manifest")
            if image_attrs.get("loading") != "lazy" or image_attrs.get("decoding") != "async":
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: image must use lazy loading and async decoding")
            if "knowledge-figure__image-link" not in link_attrs.get("class", "").split() or not link_attrs.get("aria-label"):
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: image link needs class and accessible label")
            caption_html = captions[0].group("body")
            caption_text = TAG.sub("", caption_html).strip()
            if not caption_text:
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: caption is empty")
            if re.search(r"\$|`|\\(?:mathrm|operatorname|mathbin|frac|sqrt)\b", caption_html):
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: caption contains raw Markdown or TeX")
        if any(key[0] == page for key in placements):
            refs = list(REFERENCE.finditer(text))
            if len(refs) != 1:
                errors.append(f"{page.relative_to(ROOT)}: visualized teaching page needs exactly one ## Reference")
            elif not MD_LINK.search(text[refs[0].end() :]):
                errors.append(f"{page.relative_to(ROOT)}: Reference needs a descriptive external link")
    for page, anchor in sorted(set(placements) - found, key=lambda item: (str(item[0]), item[1])):
        errors.append(f"{page.relative_to(ROOT)}#{anchor}: manifest placement is missing from Markdown")
    if site_dir is not None:
        for key, (record, asset) in placements.items():
            page, anchor = key
            output = generated_html_path(site_dir, page)
            if not output.is_file():
                errors.append(f"{page.relative_to(ROOT)}: generated HTML is missing")
                continue
            parser = HtmlFigures()
            parser.feed(output.read_text(encoding="utf-8"))
            figure = parser.figures.get(anchor)
            if figure is None:
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: generated figure is missing")
                continue
            if len(figure["images"]) != 1 or len(figure["links"]) != 1:
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: generated image/link cardinality differs")
            elif (
                not figure["images"][0].get("alt")
                or not figure["links"][0].get("aria-label")
            ):
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: generated accessibility metadata is missing")
            if not " ".join(figure["caption"]).strip():
                errors.append(f"{page.relative_to(ROOT)}#{anchor}: generated caption is empty")
            site_asset = site_dir / asset.relative_to(DOCS)
            if not site_asset.is_file() or digest(site_asset) != record.get("sha256"):
                errors.append(f"{asset.relative_to(ROOT)}: built asset is missing or changed")
    return [error for error in errors if error]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-dir", type=Path)
    args = parser.parse_args()
    site_dir = args.site_dir.resolve() if args.site_dir else None
    if site_dir is not None and not site_dir.is_dir():
        raise SystemExit(f"site directory does not exist: {site_dir}")
    errors = validate_source(site_dir)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        raise SystemExit(1)
    suffix = " with generated HTML" if site_dir else ""
    print(f"Figure checks passed: {len(list(FIGURES.glob('*.svg')))} SVG assets{suffix}")


if __name__ == "__main__":
    main()
