#!/usr/bin/env python3
"""Fail-closed structural and rendered-book verification for the public handbook."""

from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: list[str] = []
        self.images: list[tuple[str, str | None]] = []
        self.ids: set[str] = set()
        self.comic_divs = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "div" and "handbook-comic" in (values.get("class") or "").split():
            self.comic_divs += 1
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "img":
            self.images.append((values.get("src") or "", values.get("alt")))


def fail(message: str, failures: list[str]) -> None:
    failures.append(message)


def main() -> int:
    failures: list[str] = []
    chapters = sorted((ROOT / "chapters").glob("part-*/*.qmd"))
    if len(chapters) != 36:
        fail(f"expected 36 chapter files; found {len(chapters)}", failures)

    # These checks test the editorial jobs a chapter must perform without
    # forcing every chapter to use the same robotic section labels.
    contract_terms = {
        "early practical guidance": re.compile(r"^## .+\n\n.{40,}", re.M | re.I),
        "failure analysis": re.compile(
            r"^## .*\b(fail|trap|derail|confus|collapse|risk|wast|lose|lost|break|shortcut|trouble|stuck|stranded|myth|impossible|activity|fiction|apart|movement|overload|unrecover|recover|synthesis|confidence|conflict|decision|storage|workflow|role|argument|point)\w*",
            re.M | re.I,
        ),
        "readiness or pause-point standard": re.compile(
            r"good enough|^## .*\b(enough|ready|before|check|audit|test|pause|progress|dependable)\b",
            re.M | re.I,
        ),
        "local boundary": re.compile(r"\blocal(?:ly)?\b|institution|jurisdiction|disciplin(?:e|ary)|vary substantially by field", re.M | re.I),
        "practical resources": re.compile(r"^## Related (practical )?resources|\.\./\.\./(templates|checklists|stuck)/", re.M | re.I),
    }
    word_counts: list[int] = []
    for path in chapters:
        text = path.read_text(encoding="utf-8")
        words = re.findall(r"\b[\w’'-]+\b", re.sub(r"^---.*?---", "", text, count=1, flags=re.S))
        word_counts.append(len(words))
        if len(words) < 900:
            fail(f"chapter below 900 words: {path.relative_to(ROOT)} ({len(words)})", failures)
        for label, pattern in contract_terms.items():
            if not pattern.search(text):
                fail(f"chapter missing {label}: {path.relative_to(ROOT)}", failures)
        if "last-reviewed:" not in text:
            fail(f"chapter missing last-reviewed metadata: {path.relative_to(ROOT)}", failures)
        if not re.search(r"\[@[^\]]+\]", text):
            fail(f"chapter has no explicit source citation: {path.relative_to(ROOT)}", failures)

    resources = []
    with (ROOT / "planning/requirements-checklist.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    topics = [row for row in rows if row["requirement_id"].startswith("TOP-")]
    resources = [row for row in rows if row["requirement_id"].startswith("RES-")]
    if len(topics) != 82:
        fail(f"expected 82 topic requirements; found {len(topics)}", failures)
    if len(resources) != 53:
        fail(f"expected 53 resource requirements; found {len(resources)}", failures)
    incomplete_resources = [row["requirement_id"] for row in resources if row["implementation_status"] != "complete"]
    if incomplete_resources:
        fail(f"resource requirements not complete: {', '.join(incomplete_resources)}", failures)

    with (ROOT / "research/page-visuals.csv").open(newline="", encoding="utf-8") as handle:
        visual_rows = list(csv.DictReader(handle))
    mapped_pages = [row["page_path"] for row in visual_rows]
    if len(visual_rows) != 111:
        fail(f"expected 111 page-visual mappings; found {len(visual_rows)}", failures)
    if len(set(mapped_pages)) != len(mapped_pages):
        fail("page-visual register contains duplicate page mappings", failures)
    missing_visual_sources = sorted(str(path.relative_to(ROOT)) for path in chapters if str(path.relative_to(ROOT)) not in mapped_pages)
    if missing_visual_sources:
        fail(f"chapters missing page-visual mapping: {', '.join(missing_visual_sources)}", failures)
    for row in visual_rows:
        if not (ROOT / row["asset_path"]).exists():
            fail(f"page-visual asset missing: {row['page_path']} -> {row['asset_path']}", failures)
        if not row["relevance_reason"].strip():
            fail(f"page-visual relevance reason missing: {row['page_path']}", failures)

    required_paths = sorted((ROOT / "checklists").glob("*.qmd")) + sorted((ROOT / "templates").glob("*.qmd")) + sorted((ROOT / "stuck").glob("*.qmd"))
    for source in required_paths:
        rendered = SITE / source.relative_to(ROOT).with_suffix(".html")
        if not rendered.exists():
            fail(f"resource not rendered: {source.relative_to(ROOT)}", failures)

    html_pages = sorted(SITE.rglob("*.html"))
    if len(html_pages) < 106:
        fail(f"expected at least 106 rendered HTML pages; found {len(html_pages)}", failures)

    parsed: dict[Path, PageParser] = {}
    for page in html_pages:
        parser = PageParser()
        parser.feed(page.read_text(encoding="utf-8", errors="replace"))
        parsed[page] = parser
        if parser.comic_divs != 1:
            fail(f"expected one credited comic on rendered page: {page.relative_to(SITE)}; found {parser.comic_divs}", failures)
        for src, alt in parser.images:
            # Quarto emits the repeated sidebar logo with alt="" because it is
            # decorative navigation chrome. Content images require text.
            if (alt is None or not alt.strip()) and "cover-final" not in src:
                fail(f"image missing descriptive alt attribute: {page.relative_to(SITE)} -> {src}", failures)
        for href in parser.links:
            split = urlsplit(href)
            if split.scheme or href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            if not split.path:
                target = page
            elif split.path.startswith("/"):
                target = SITE / unquote(split.path.lstrip("/"))
            else:
                target = (page.parent / unquote(split.path)).resolve()
            if target.is_dir():
                target = target / "index.html"
            if target.suffix == ".qmd":
                fail(f"raw qmd link in rendered site: {page.relative_to(SITE)} -> {href}", failures)
                continue
            if not target.exists():
                fail(f"broken internal link: {page.relative_to(SITE)} -> {href}", failures)
                continue
            if split.fragment and target.suffix == ".html":
                target_parser = parsed.get(target)
                if target_parser is None:
                    target_parser = PageParser()
                    target_parser.feed(target.read_text(encoding="utf-8", errors="replace"))
                    parsed[target] = target_parser
                if unquote(split.fragment) not in target_parser.ids:
                    fail(f"missing fragment target: {page.relative_to(SITE)} -> {href}", failures)

    source_keys = set(re.findall(r"^@\w+\{([^,]+),", (ROOT / "references.bib").read_text(encoding="utf-8"), re.M))
    cited_keys: set[str] = set()
    for source in ROOT.rglob("*.qmd"):
        if "_site" in source.parts:
            continue
        text = source.read_text(encoding="utf-8")
        for group in re.findall(r"\[@([^\]]+)\]", text):
            cited_keys.update(re.findall(r"@?([A-Za-z0-9_.:-]+)", group))
    missing_keys = sorted(cited_keys - source_keys)
    if missing_keys:
        fail(f"citation keys missing from bibliography: {', '.join(missing_keys)}", failures)

    if failures:
        print("VERIFY BOOK: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    status_counts = Counter(row["implementation_status"] for row in rows)
    print("VERIFY BOOK: PASS")
    print(f"chapters=36 words_min={min(word_counts)} words_max={max(word_counts)}")
    print(f"topics=82 resources=53 html_pages={len(html_pages)} citations={len(source_keys)}")
    print("ledger=" + ",".join(f"{key}:{status_counts[key]}" for key in sorted(status_counts)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
