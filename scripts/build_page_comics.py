#!/usr/bin/env python3
"""Build the page-by-page xkcd visual system from an editorial mapping."""

from __future__ import annotations

import argparse
import csv
import json
import re
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets/xkcd"
META_DIR = ROOT / "research/xkcd-source-metadata"

# Every rendered source page receives an editorially selected comic. The
# selection rationales are editorial notes kept outside the public repository.
ASSIGNMENTS: dict[str, int] = {
    "index.qmd": 59,
    "status.qmd": 910,
    "chapters/part-01/01-phd-and-good-enough.qmd": 1052,
    "chapters/part-01/02-first-90-days.qmd": 1425,
    "chapters/part-01/03-provisional-plan.qmd": 974,
    "chapters/part-02/04-roles-and-expectations.qmd": 1028,
    "chapters/part-02/05-meetings-and-records.qmd": 1860,
    "chapters/part-02/06-feedback-and-independence.qmd": 481,
    "chapters/part-03/07-problem-gap-contribution.qmd": 2368,
    "chapters/part-03/08-topic-due-diligence.qmd": 1205,
    "chapters/part-03/09-questions-and-pivots.qmd": 1282,
    "chapters/part-04/10-search-ladder.qmd": 386,
    "chapters/part-04/11-reproducible-searching.qmd": 979,
    "chapters/part-04/12-reading-and-synthesis.qmd": 1447,
    "chapters/part-05/13-design-alignment.qmd": 552,
    "chapters/part-05/14-sampling-measurement-pilots.qmd": 882,
    "chapters/part-05/15-rigour-and-variation.qmd": 1478,
    "chapters/part-06/16-ethics-privacy-consent.qmd": 263,
    "chapters/part-06/17-integrity-governance-ai.qmd": 1838,
    "chapters/part-06/18-authorship-collaboration-corrections.qmd": 2025,
    "chapters/part-07/19-data-management-storage.qmd": 2347,
    "chapters/part-07/20-data-states-provenance.qmd": 2582,
    "chapters/part-07/21-reproducible-workflows.qmd": 1172,
    "chapters/part-08/22-minimum-viable-stack.qmd": 927,
    "chapters/part-08/23-analysis-review-quarto.qmd": 1654,
    "chapters/part-08/24-git-github-ai.qmd": 1597,
    "chapters/part-09/25-milestones-weekly-work.qmd": 1205,
    "chapters/part-09/26-risks-blocked-change.qmd": 722,
    "chapters/part-09/27-collaboration-handoffs-scope.qmd": 1782,
    "chapters/part-10/28-writing-and-argument.qmd": 2456,
    "chapters/part-10/29-reviewable-work-feedback.qmd": 2025,
    "chapters/part-10/30-publishing-review-communication.qmd": 2304,
    "chapters/part-11/31-failed-studies.qmd": 349,
    "chapters/part-11/32-technical-failure-perfectionism.qmd": 1691,
    "chapters/part-11/33-decide-and-stuck.qmd": 1282,
    "chapters/part-12/34-independence-contribution.qmd": 451,
    "chapters/part-12/35-examination-corrections.qmd": 2025,
    "chapters/part-12/36-closure-transition.qmd": 910,
    "resources.qmd": 2601,
    "checklists/index.qmd": 2601,
    "checklists/doctoral-journey.qmd": 59,
    "checklists/starting-candidature.qmd": 1425,
    "checklists/first-90-day-review.qmd": 1205,
    "checklists/before-study-commitment.qmd": 1205,
    "checklists/research-question-stress-test.qmd": 974,
    "checklists/search-ladder.qmd": 386,
    "checklists/pilot-readiness.qmd": 882,
    "checklists/before-ethics-submission.qmd": 263,
    "checklists/before-data-collection.qmd": 397,
    "checklists/backup-restore.qmd": 2347,
    "checklists/before-analysis.qmd": 552,
    "checklists/git-github-starter.qmd": 1597,
    "checklists/ai-use-decision.qmd": 1838,
    "checklists/before-study-write-up.qmd": 2456,
    "checklists/before-manuscript-submission.qmd": 2025,
    "checklists/good-enough-rubric.qmd": 974,
    "checklists/pivot-continue-stop.qmd": 1282,
    "checklists/before-thesis-submission.qmd": 2456,
    "checklists/project-closure-handover.qmd": 910,
    "templates/supervisor-expectations.qmd": 1028,
    "templates/supervision-agreement.qmd": 1028,
    "templates/meeting-agenda.qmd": 1860,
    "templates/meeting-record.qmd": 910,
    "templates/matters-arising.qmd": 1782,
    "templates/action-register.qmd": 1425,
    "templates/decision-log.qmd": 1282,
    "templates/unresolved-questions.qmd": 2368,
    "templates/risk-issues-register.qmd": 2368,
    "templates/topic-due-diligence.qmd": 1205,
    "templates/topic-case.qmd": 2368,
    "templates/contribution-statement.qmd": 2456,
    "templates/search-concepts.qmd": 979,
    "templates/search-log.qmd": 979,
    "templates/citation-chaining.qmd": 979,
    "templates/paper-triage-extraction.qmd": 1447,
    "templates/evidence-matrix.qmd": 1447,
    "templates/synthesis-argument-map.qmd": 1447,
    "templates/method-options.qmd": 263,
    "templates/method-decision.qmd": 1282,
    "templates/protocol-deviation.qmd": 263,
    "templates/data-management-plan.qmd": 2582,
    "templates/folder-file-naming.qmd": 910,
    "templates/data-dictionary.qmd": 2582,
    "templates/repository-readme.qmd": 225,
    "templates/ai-use-log.qmd": 1838,
    "templates/supervisor-review-cover-note.qmd": 1860,
    "templates/feedback-response.qmd": 481,
    "templates/authorship-conversation.qmd": 2025,
    "templates/journal-due-diligence.qmd": 2304,
    "templates/reviewer-response.qmd": 2025,
    "templates/escalation-message.qmd": 1028,
    "templates/thesis-contribution-map.qmd": 2456,
    "stuck/index.qmd": 722,
    "stuck/starting-or-expectations.qmd": 1425,
    "stuck/topic-or-question.qmd": 974,
    "stuck/endless-searching.qmd": 386,
    "stuck/method-paralysis.qmd": 1282,
    "stuck/waiting-or-blocked.qmd": 303,
    "stuck/study-failure.qmd": 349,
    "stuck/technical-failure.qmd": 371,
    "stuck/writing-or-perfectionism.qmd": 1691,
    "stuck/relationship-or-authorship.qmd": 1028,
    "stuck/good-enough.qmd": 974,
    "stuck/wellbeing-or-safety.qmd": 828,
    "support.qmd": 2368,
    "contributions/index.qmd": 1060,
    "contributions/how-to-help.qmd": 2601,
    "contributions/editorial-workflow.qmd": 1319,
    "contributions/ai-and-editorial-practice.qmd": 2173,
    "contributions/visuals-and-credit.qmd": 14,
    "references.qmd": 2086,
}


def book_pages() -> list[str]:
    config = yaml.safe_load((ROOT / "_quarto.yml").read_text())
    pages: list[str] = []

    def walk(items: list[object]) -> None:
        for item in items:
            if isinstance(item, str):
                pages.append(item)
            elif isinstance(item, dict):
                walk(item.get("chapters", []))

    walk(config["book"]["chapters"])
    return pages


def fetch_metadata(comic_id: int) -> dict[str, object]:
    META_DIR.mkdir(parents=True, exist_ok=True)
    path = META_DIR / f"{comic_id}.json"
    if not path.exists():
        url = f"https://xkcd.com/{comic_id}/info.0.json"
        with urllib.request.urlopen(url) as response:
            path.write_bytes(response.read())
    return json.loads(path.read_text())


def download_image(meta: dict[str, object]) -> str:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    comic_id = int(meta["num"])
    source = str(meta["img"])
    suffix = Path(source).suffix or ".png"
    safe = re.sub(r"[^a-z0-9]+", "-", str(meta["safe_title"]).lower()).strip("-")
    filename = f"{comic_id}-{safe}{suffix}"
    path = ASSET_DIR / filename
    if not path.exists():
        with urllib.request.urlopen(source) as response:
            path.write_bytes(response.read())
    return f"assets/xkcd/{filename}"


def lua_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def write_lua_data(rows: list[dict[str, str]]) -> None:
    out = ["-- Generated by scripts/build_page_comics.py; do not edit by hand.", "return {"]
    for row in rows:
        out.append(f"  [{lua_string(row['page_path'])}] = {{")
        out.append(f"    page_path = {lua_string(row['page_path'])},")
        for key in ("comic_id", "title", "asset_path"):
            out.append(f"    {key} = {lua_string(row[key])},")
        out.append("  },")
        out.append(f"  [{lua_string('title:' + row['page_title'])}] = {{")
        out.append(f"    page_path = {lua_string(row['page_path'])},")
        for key in ("comic_id", "title", "asset_path"):
            out.append(f"    {key} = {lua_string(row[key])},")
        out.append("  },")
    out.append("}")
    (ROOT / "filters/page-comics-data.lua").write_text("\n".join(out) + "\n")


def write_register_include(rows: list[dict[str, str]]) -> None:
    placements: dict[str, list[str]] = defaultdict(list)
    titles: dict[str, str] = {}
    for row in rows:
        placements[row["comic_id"]].append(row["page_title"])
        titles[row["comic_id"]] = row["title"]
    lines = [
        "## The xkcd comics used in this handbook",
        "",
        "Every embedded xkcd comic is by Randall Munroe and is reused from "
        "[xkcd](https://xkcd.com/) under the "
        "[Creative Commons Attribution–NonCommercial 2.5 licence](https://creativecommons.org/licenses/by-nc/2.5/). "
        "The comics are excluded from the handbook's CC BY 4.0 content licence. "
        "Each appearance links to the original comic and transcript.",
        "",
        "| Comic | Used on |",
        "|---|---|",
    ]
    for comic_id in sorted(placements, key=int):
        pages = placements[comic_id]
        page_text = "; ".join(pages)
        lines.append(f"| [xkcd #{comic_id}: {titles[comic_id]}](https://xkcd.com/{comic_id}/) | {page_text} |")
    lines.extend([
        "",
        "The machine-readable page-by-page placement and asset path are recorded in the "
        "[`page-visuals register`](https://github.com/hareshsuppiah/handbook-for-the-recently-enrolled/blob/main/research/page-visuals.csv).",
        "",
    ])
    (ROOT / "includes/xkcd-register.qmd").write_text("\n".join(lines))


def update_visual_register(unique: dict[int, tuple[dict[str, object], str]]) -> None:
    path = ROOT / "research/visual-assets-register.csv"
    with path.open(newline="", encoding="utf-8") as handle:
        existing = [row for row in csv.DictReader(handle) if not row["asset_id"].startswith("VIS-XKCD-")]
        fieldnames = list(existing[0].keys())
    for comic_id in sorted(unique):
        meta, asset_path = unique[comic_id]
        existing.append({
            "asset_id": f"VIS-XKCD-{comic_id}",
            "path": asset_path,
            "title": f"xkcd #{comic_id}: {meta['safe_title']}",
            "creator_or_rightsholder": "Randall Munroe / xkcd",
            "source_url": f"https://xkcd.com/{comic_id}/",
            "license_or_reuse_basis": "Creative Commons Attribution-NonCommercial 2.5; excluded from the handbook CC BY 4.0 licence",
            "license_url": "https://creativecommons.org/licenses/by-nc/2.5/",
            "changes": "Resized responsively by the website; otherwise unmodified",
            "alt_text": f"xkcd comic titled {meta['safe_title']}; a full transcript is available at the linked original",
            "caption": f"xkcd #{comic_id}, {meta['safe_title']}, by Randall Munroe",
            "placement": "See research/page-visuals.csv",
            "date_checked": "2026-08-30",
            "review_status": "approved for non-commercial attributed use",
        })
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(existing)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true", help="Fetch missing official metadata and images")
    args = parser.parse_args()

    pages = book_pages()
    missing = sorted(set(pages) - set(ASSIGNMENTS))
    extra = sorted(set(ASSIGNMENTS) - set(pages))
    if missing or extra:
        raise SystemExit(f"Mapping mismatch. Missing={missing}; extra={extra}")

    metadata: dict[int, dict[str, object]] = {}
    assets: dict[int, str] = {}
    for comic_id in sorted(set(ASSIGNMENTS.values())):
        meta_path = META_DIR / f"{comic_id}.json"
        if not meta_path.exists() and not args.fetch:
            raise SystemExit(f"Missing {meta_path}; rerun with --fetch")
        meta = fetch_metadata(comic_id)
        asset = download_image(meta) if args.fetch else next(ASSET_DIR.glob(f"{comic_id}-*"), None)
        if asset is None:
            raise SystemExit(f"Missing local image for xkcd #{comic_id}; rerun with --fetch")
        metadata[comic_id] = meta
        assets[comic_id] = asset if isinstance(asset, str) else str(asset.relative_to(ROOT))

    rows: list[dict[str, str]] = []
    for page in pages:
        comic_id = ASSIGNMENTS[page]
        source = (ROOT / page).read_text()
        title_match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', source, re.M)
        if not title_match:
            raise SystemExit(f"No title in {page}")
        rows.append({
            "page_path": page,
            "page_title": title_match.group(1),
            "comic_id": str(comic_id),
            "title": str(metadata[comic_id]["safe_title"]),
            "asset_path": assets[comic_id],
            "source_url": f"https://xkcd.com/{comic_id}/",
            "creator": "Randall Munroe / xkcd",
            "license": "CC BY-NC 2.5",
            "license_url": "https://creativecommons.org/licenses/by-nc/2.5/",
        })

    with (ROOT / "research/page-visuals.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["page_path", "page_title", "comic_id", "title", "asset_path", "source_url", "creator", "license", "license_url"]
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    write_lua_data(rows)
    write_register_include(rows)
    update_visual_register({comic_id: (metadata[comic_id], assets[comic_id]) for comic_id in metadata})

    counts = Counter(row["comic_id"] for row in rows)
    print(f"pages={len(rows)} unique_comics={len(counts)}")
    print("most_reused=" + ",".join(f"{comic}:{count}" for comic, count in counts.most_common(8)))


if __name__ == "__main__":
    main()
