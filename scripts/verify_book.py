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
        self.visual_divs = 0
        self.text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if values.get("id"):
            self.ids.add(values["id"] or "")
        if tag == "div" and "handbook-visual" in (values.get("class") or "").split():
            self.visual_divs += 1
        if tag == "a" and values.get("href"):
            self.links.append(values["href"] or "")
        if tag == "img":
            self.images.append((values.get("src") or "", values.get("alt")))

    def handle_data(self, data: str) -> None:
        self.text_parts.append(data)


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
            r"^## .*\b(fail|trap|derail|drift|confus|collapse|risk|wast|lose|lost|break|shortcut|trouble|stuck|stranded|myth|impossible|activity|fiction|apart|movement|overload|unrecover|recover|synthesis|confidence|conflict|decision|storage|workflow|role|argument|point)\w*",
            re.M | re.I,
        ),
        "readiness or pause-point standard": re.compile(
            r"good enough|^## .*\b(enough|ready|before|check|audit|test|pause|progress|dependable|follow|trace)\b",
            re.M | re.I,
        ),
        "practical resources": re.compile(
            r"^## (?:Related (?:practical )?resources|Try these resources|Useful templates)|\.\./\.\./(templates|checklists|stuck)/",
            re.M | re.I,
        ),
    }
    word_counts: list[int] = []
    for path in chapters:
        text = path.read_text(encoding="utf-8")
        words = re.findall(r"\b[\w’'-]+\b", re.sub(r"^---.*?---", "", text, count=1, flags=re.S))
        word_counts.append(len(words))
        # A length floor cannot establish coverage and encourages padding.
        # This catches empty stubs only; editorial coverage is reviewed separately.
        if len(words) < 250:
            fail(f"chapter appears to be a stub: {path.relative_to(ROOT)} ({len(words)})", failures)
        for label, pattern in contract_terms.items():
            # Some reviewed sections teach the same requirement without a stock
            # heading. Accept their specific headings, not a forced prose formula.
            reviewed_sections = {
                "failure analysis": {
                    "21-reproducible-workflows.qmd": "## Test more than successful execution",
                    "23-analysis-review-quarto.qmd": "## Example: the manually updated table",
                    "24-git-github-ai.qmd": "## Respond to sensitive-data exposure immediately",
                    "35-examination-corrections.qmd": "## If you discover an error after submission",
                },
                "readiness or pause-point standard": {
                    "33-decide-and-stuck.qmd": "## Choose one next action",
                    "34-independence-contribution.qmd": "## Look for evidence of independence",
                },
            }
            alternative = reviewed_sections.get(label, {}).get(path.name)
            if not pattern.search(text) and not (alternative and alternative in text):
                fail(f"chapter missing {label}: {path.relative_to(ROOT)}", failures)
        if "last-reviewed:" not in text:
            fail(f"chapter missing last-reviewed metadata: {path.relative_to(ROOT)}", failures)
        if re.search(r"^:::\s*\{#refs\}", text, re.M):
            fail(f"chapter repeats the book-wide bibliography: {path.relative_to(ROOT)}", failures)
        if not re.search(r"\[@[^\]]+\]", text):
            fail(f"chapter has no explicit source citation: {path.relative_to(ROOT)}", failures)

    # Standing limits belong on support.qmd, not in a warning box repeated on
    # every page. Specific stop conditions may remain where the risk occurs.
    boundary_page = (ROOT / "support.qmd").read_text(encoding="utf-8")
    if 'title: "Local rules and specialist help"' not in boundary_page or "{#who-decides-what}" not in boundary_page:
        fail("support.qmd is missing the consolidated local-rule guidance", failures)
    deprecated_boundary_patterns = {
        "manual-status box": re.compile(r"^:::\s*\{\.manual-status\}", re.M),
        "Check locally callout": re.compile(r'^:::\s*\{\.callout-warning title="(?:Stop and check locally|Check locally)"\}', re.M),
        "Check locally heading": re.compile(r"^## Check locally$", re.M),
        "Check locally label": re.compile(r"\*\*Check locally:\*\*"),
        "generic substitute disclaimer": re.compile(r"This is not a substitute for", re.I),
    }
    reader_sources = [ROOT / "index.qmd", ROOT / "support.qmd"]
    reader_sources.extend(sorted((ROOT / "chapters").rglob("*.qmd")))
    reader_sources.extend(sorted((ROOT / "checklists").rglob("*.qmd")))
    reader_sources.extend(sorted((ROOT / "templates").rglob("*.qmd")))
    for source in reader_sources:
        text = source.read_text(encoding="utf-8")
        for label, pattern in deprecated_boundary_patterns.items():
            if pattern.search(text):
                fail(f"reader-facing source retains deprecated {label}: {source.relative_to(ROOT)}", failures)

    # Desktop and tablet readers must keep both navigation columns visible.
    # These hooks also clear Quarto's stored reader-mode state, which otherwise
    # turns the two sidebars into compact dropdown bars after a previous visit.
    navigation_script = (ROOT / "includes/responsive-navigation.html").read_text(encoding="utf-8")
    navigation_styles = (ROOT / "styles.scss").read_text(encoding="utf-8")
    required_navigation_hooks = {
        "reader-mode reset": 'localStorage.setItem("quarto-reader-mode", "false")' in navigation_script,
        "left dropdown removal": "#quarto-sidebarnav-toggle" in navigation_script and "#quarto-sidebarnav-toggle" in navigation_styles,
        "right dropdown removal": "#quarto-toc-toggle" in navigation_script and "#quarto-toc-toggle" in navigation_styles,
        "desktop sidebar restoration": "restorePersistentSidebars" in navigation_script,
    }
    for label, present in required_navigation_hooks.items():
        if not present:
            fail(f"persistent desktop navigation is missing {label}", failures)

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
    if len(set(mapped_pages)) != len(mapped_pages):
        fail("page-visual register contains duplicate page mappings", failures)
    for row in visual_rows:
        if not (ROOT / row["page_path"]).exists():
            fail(f"page-visual source missing: {row['page_path']}", failures)
        if not (ROOT / row["asset_path"]).exists():
            fail(f"page-visual asset missing: {row['page_path']} -> {row['asset_path']}", failures)
    if "relevance_reason" in (visual_rows[0] if visual_rows else {}):
        fail("public page-visual register contains private editorial rationales", failures)

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
        if "Why it fits" in " ".join(parser.text_parts):
            fail(f"internal visual rationale leaked into rendered page: {page.relative_to(SITE)}", failures)
        if parser.visual_divs > 1:
            fail(f"rendered page contains more than one registered page visual: {page.relative_to(SITE)}; found {parser.visual_divs}", failures)
        for src, alt in parser.images:
            # Quarto emits the repeated sidebar logo with alt="" because it is
            # decorative navigation chrome. Content images require text.
            if (alt is None or not alt.strip()) and not any(cover in src for cover in ("cover-final", "cover-2026-09")):
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
