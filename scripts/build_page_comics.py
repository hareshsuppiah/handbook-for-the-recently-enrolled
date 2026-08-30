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

# Every rendered source page receives an editorially selected comic and a short
# explanation of the connection. Reuse is deliberate when several resources
# perform the same job; it is not a fallback for missing review.
ASSIGNMENTS: dict[str, tuple[int, str]] = {
    "index.qmd": (59, "The opening page introduces graduate research as a journey whose purpose is not always obvious at the start."),
    "status.qmd": (910, "A living handbook needs durable links and records even while its contents continue to change."),
    "chapters/part-01/01-phd-and-good-enough.qmd": (1052, "The joke about an undeclared doctorate captures the early uncertainty this chapter turns into stage-appropriate decisions."),
    "chapters/part-01/02-first-90-days.qmd": (1425, "An apparently simple task can hide years of work, which is why the first 90 days focus on testing assumptions before promising outcomes."),
    "chapters/part-01/03-provisional-plan.qmd": (974, "The comic warns against solving a grand general problem when the project first needs a workable next step."),
    "chapters/part-02/04-roles-and-expectations.qmd": (1028, "Supervision expectations only help when they are communicated in a way the other person can actually use."),
    "chapters/part-02/05-meetings-and-records.qmd": (1860, "A meeting record is partly a defence against the confident belief that miscommunication is always the listener's fault."),
    "chapters/part-02/06-feedback-and-independence.qmd": (481, "Reading feedback aloud can reveal whether a comment names a real problem or merely sounds authoritative."),
    "chapters/part-03/07-problem-gap-contribution.qmd": (2368, "The presence of many important problems does not make the specific research problem disappear."),
    "chapters/part-03/08-topic-due-diligence.qmd": (1205, "Due diligence asks whether the likely value of a project justifies the time and complexity required."),
    "chapters/part-03/09-questions-and-pivots.qmd": (1282, "A research pivot is a decision under uncertainty, and the apparent choices can change once the structure of the problem is understood."),
    "chapters/part-04/10-search-ladder.qmd": (386, "Endless searching often continues because stopping feels like allowing someone on the internet to remain wrong."),
    "chapters/part-04/11-reproducible-searching.qmd": (979, "A useful search record is written for the future researcher who finds the same problem after the original discussion has gone quiet."),
    "chapters/part-04/12-reading-and-synthesis.qmd": (1447, "Meta-analysis is a reminder that combining studies requires an argument about what can legitimately be combined."),
    "chapters/part-05/13-design-alignment.qmd": (552, "The famous correlation joke is a compact warning against making a stronger causal claim than the design supports."),
    "chapters/part-05/14-sampling-measurement-pilots.qmd": (882, "Repeated testing can manufacture a striking result, which is why sampling, measures and pilot decisions must be planned together."),
    "chapters/part-05/15-rigour-and-variation.qmd": (1478, "A result does not become rigorous because a familiar threshold appears beside it."),
    "chapters/part-06/16-ethics-privacy-consent.qmd": (263, "Absolute certainty is a poor substitute for identifying the actual authority, risk and consent process."),
    "chapters/part-06/17-integrity-governance-ai.qmd": (1838, "Machine learning is not magic; responsible use requires knowing what went in, what came out and how the result was checked."),
    "chapters/part-06/18-authorship-collaboration-corrections.qmd": (2025, "Publication systems can create perverse incentives, making transparent contribution and correction records essential."),
    "chapters/part-07/19-data-management-storage.qmd": (2347, "A research archive is only as recoverable as the dependencies and tools needed to open it."),
    "chapters/part-07/20-data-states-provenance.qmd": (2582, "A data pipeline can destroy meaning while appearing to produce a cleaner dataset."),
    "chapters/part-07/21-reproducible-workflows.qmd": (1172, "A workflow is not reproducible merely because it works in the environment where it was created."),
    "chapters/part-08/22-minimum-viable-stack.qmd": (927, "Adding another universal tool often creates one more standard rather than a simpler research system."),
    "chapters/part-08/23-analysis-review-quarto.qmd": (1654, "A tool chain that installs everything everywhere is the opposite of a deliberate, reviewable publishing workflow."),
    "chapters/part-08/24-git-github-ai.qmd": (1597, "Git becomes manageable when changes are small and inspectable instead of being rescued by mysterious commands."),
    "chapters/part-09/25-milestones-weekly-work.qmd": (1205, "Time-saving work is worth doing only when its future benefit exceeds the effort of setting it up."),
    "chapters/part-09/26-risks-blocked-change.qmd": (722, "Before fixing a blockage, describe the smallest actual problem rather than the entire history of the project."),
    "chapters/part-09/27-collaboration-handoffs-scope.qmd": (1782, "Team communication tools multiply quickly, so ownership and handoff rules need to remain clearer than the chat system."),
    "chapters/part-10/28-writing-and-argument.qmd": (2456, "Scientific papers take recognisable forms, but a familiar form cannot replace a clear argument."),
    "chapters/part-10/29-reviewable-work-feedback.qmd": (2025, "Peer review works better when the request, evidence and response are visible rather than hidden inside the publication system."),
    "chapters/part-10/30-publishing-review-communication.qmd": (2304, "Preprints illustrate how publication routes affect access, timing and the audience that can inspect the work."),
    "chapters/part-11/31-failed-studies.qmd": (349, "A striking outcome can be real, misleading or badly framed; failure diagnosis begins by separating the result from the claim."),
    "chapters/part-11/32-technical-failure-perfectionism.qmd": (1691, "Premature optimisation is a useful caricature of work that expands long after the original problem has been solved."),
    "chapters/part-11/33-decide-and-stuck.qmd": (1282, "When a project is stuck, the first task is to understand the real choice rather than repeatedly selecting from the wrong options."),
    "chapters/part-12/34-independence-contribution.qmd": (451, "Impostor feelings are not evidence that a researcher lacks expertise; independence is demonstrated through inspectable decisions."),
    "chapters/part-12/35-examination-corrections.qmd": (2025, "Examination is a structured form of peer review, not a demand that a thesis become immune to criticism."),
    "chapters/part-12/36-closure-transition.qmd": (910, "Closure decisions determine whether files, links and responsibilities remain usable after the people and systems change."),
    "resources.qmd": (2601, "A practical resource is useful when its instructions help the reader act rather than adding another layer of theory."),
    "checklists/index.qmd": (2601, "A checklist needs clear instructions and a defined pause point, not an attempt to contain every possible task."),
    "checklists/doctoral-journey.qmd": (59, "The full doctoral journey can be visible even when the reason for taking every later step is not yet clear."),
    "checklists/starting-candidature.qmd": (1425, "Starting well means discovering the hidden complexity of apparently simple setup tasks before they become blockers."),
    "checklists/first-90-day-review.qmd": (1205, "The 90-day review asks whether early systems and decisions are saving more time than they consume."),
    "checklists/before-study-commitment.qmd": (1205, "Commitment should follow a realistic comparison between expected value and the time needed to obtain it."),
    "checklists/research-question-stress-test.qmd": (974, "A stress test keeps one research question from quietly expanding into the general problem of everything."),
    "checklists/search-ladder.qmd": (386, "A stopping rule protects the search from becoming an endless duty to correct the whole internet."),
    "checklists/pilot-readiness.qmd": (882, "A pilot should test planned decisions rather than offer repeated chances to find a convenient result."),
    "checklists/before-ethics-submission.qmd": (263, "Ethics readiness comes from explicit safeguards and authority, not a claim of complete certainty."),
    "checklists/before-data-collection.qmd": (397, "A procedure can look scientific while skipping the controls that make its evidence trustworthy."),
    "checklists/backup-restore.qmd": (2347, "A backup is useful only if the files and their dependencies can actually be restored."),
    "checklists/before-analysis.qmd": (552, "The analysis pause point protects the study from turning association into a stronger claim than the data support."),
    "checklists/git-github-starter.qmd": (1597, "A calm Git workflow begins before the project needs an emergency command copied from the internet."),
    "checklists/ai-use-decision.qmd": (1838, "The machine-learning pile is funny because it hides the inputs, checks and limits that this checklist makes explicit."),
    "checklists/before-study-write-up.qmd": (2456, "Before writing, decide which kind of scientific paper the evidence can honestly support."),
    "checklists/before-manuscript-submission.qmd": (2025, "Submission readiness includes the integrity of the review and access system, not only the manuscript file."),
    "checklists/good-enough-rubric.qmd": (974, "Good-enough criteria stop a bounded task from becoming a perfect solution to a much larger problem."),
    "checklists/pivot-continue-stop.qmd": (1282, "A pivot decision improves when the candidate can see how the options and evidence are structured."),
    "checklists/before-thesis-submission.qmd": (2456, "A thesis is ready when its actual contribution is defensible, not when it resembles every possible kind of scientific paper."),
    "checklists/project-closure-handover.qmd": (910, "Handover is the moment to prevent today's convenient names and links becoming tomorrow's permanent mystery."),
    "templates/supervisor-expectations.qmd": (1028, "An expectations guide exists because communication is measured by shared understanding, not by how clearly one person believes they spoke."),
    "templates/supervision-agreement.qmd": (1028, "A supervision agreement turns private assumptions into communication that both sides can inspect."),
    "templates/meeting-agenda.qmd": (1860, "A decision-oriented agenda reduces the chance that everyone leaves a good conversation with a different interpretation."),
    "templates/meeting-record.qmd": (910, "A short meeting record gives decisions a life beyond the temporary systems and memories that produced them."),
    "templates/matters-arising.qmd": (1782, "A matters-arising register keeps actions visible when the surrounding conversation is split across many channels."),
    "templates/action-register.qmd": (1425, "An action register breaks work that looks simple from a distance into visible owners, evidence and dependencies."),
    "templates/decision-log.qmd": (1282, "A decision log preserves which options were available and why one route was chosen."),
    "templates/unresolved-questions.qmd": (2368, "Recording one unresolved question prevents every other problem in the world from being used to avoid it."),
    "templates/risk-issues-register.qmd": (2368, "A risk register gives each real problem a boundary rather than treating the existence of other problems as a response."),
    "templates/topic-due-diligence.qmd": (1205, "The canvas makes the time, cost and likely value of a proposed topic visible before commitment."),
    "templates/topic-case.qmd": (2368, "A one-page topic case must name the particular problem instead of relying on the fact that many problems matter."),
    "templates/contribution-statement.qmd": (2456, "A contribution statement names what this work adds instead of hiding inside the conventions of a paper type."),
    "templates/search-concepts.qmd": (979, "A concept table leaves a useful trail for the future person trying to reconstruct the search."),
    "templates/search-log.qmd": (979, "A search log is the message that prevents future readers from finding an abandoned question with no answer."),
    "templates/citation-chaining.qmd": (979, "Citation chaining becomes defensible when the trail is recorded for the next reader."),
    "templates/paper-triage-extraction.qmd": (1447, "Structured extraction makes comparison possible before a collection of papers is treated as a synthesis."),
    "templates/evidence-matrix.qmd": (1447, "An evidence matrix shows what can and cannot sensibly be combined across studies."),
    "templates/synthesis-argument-map.qmd": (1447, "The map turns a stack of studies into a visible argument about agreement, difference and limitation."),
    "templates/method-options.qmd": (263, "Comparing methods openly is more defensible than expressing certainty about the first familiar option."),
    "templates/method-decision.qmd": (1282, "A methodological decision record preserves the evidence and alternatives behind the selected door."),
    "templates/protocol-deviation.qmd": (263, "A deviation log replaces false certainty with an accurate record of what changed and who authorised it."),
    "templates/data-management-plan.qmd": (2582, "A living data plan protects meaning while information moves through the research pipeline."),
    "templates/folder-file-naming.qmd": (910, "Names chosen for today's convenience often become permanent interfaces used by many future files."),
    "templates/data-dictionary.qmd": (2582, "A codebook prevents a clean-looking dataset from losing the information needed to interpret it."),
    "templates/repository-readme.qmd": (225, "A README is part of the social infrastructure that lets open work remain understandable and reusable."),
    "templates/ai-use-log.qmd": (1838, "An AI-use log records what happened inside the apparent machine-learning magic."),
    "templates/supervisor-review-cover-note.qmd": (1860, "A cover note makes the review request the writer's responsibility instead of assuming the reader will infer it."),
    "templates/feedback-response.qmd": (481, "A response matrix helps the writer hear what a comment actually says before reacting to how it sounds."),
    "templates/authorship-conversation.qmd": (2025, "Authorship conversations matter because publication systems do not automatically reveal who contributed what."),
    "templates/journal-due-diligence.qmd": (2304, "Journal selection changes access and timing, as the preprint route makes especially visible."),
    "templates/reviewer-response.qmd": (2025, "A response matrix makes peer review inspectable comment by comment."),
    "templates/escalation-message.qmd": (1028, "An escalation message succeeds when the decision-maker can understand and act on it."),
    "templates/thesis-contribution-map.qmd": (2456, "A contribution map separates what the thesis adds from the many familiar forms a scientific paper can take."),
    "stuck/index.qmd": (722, "The fastest way out of 'everything is broken' is to identify the smallest problem that can be described and tested."),
    "stuck/starting-or-expectations.qmd": (1425, "An unclear starting point often hides a task whose complexity has not yet been unpacked."),
    "stuck/topic-or-question.qmd": (974, "A topic becomes manageable when it stops trying to solve the general problem and names the next researchable one."),
    "stuck/endless-searching.qmd": (386, "Endless searching can feel like a duty, especially when another source might prove someone wrong."),
    "stuck/method-paralysis.qmd": (1282, "Method paralysis eases when the real structure of the decision replaces an intimidating row of doors."),
    "stuck/waiting-or-blocked.qmd": (303, "Waiting can contain legitimate work, but it should not become the research equivalent of doing something else while the code compiles."),
    "stuck/study-failure.qmd": (349, "A failed study is not interpreted by the headline result alone; the design and claim still need diagnosis."),
    "stuck/technical-failure.qmd": (371, "A bizarre error message is easier to solve once it is reduced to a reproducible failing case."),
    "stuck/writing-or-perfectionism.qmd": (1691, "Perfectionism often disguises itself as optimisation work that must be completed before the real writing can begin."),
    "stuck/relationship-or-authorship.qmd": (1028, "A stuck relationship problem needs communication that creates shared understanding, not another private assumption."),
    "stuck/good-enough.qmd": (974, "The good-enough decision protects a bounded piece of work from expanding into the general problem."),
    "stuck/wellbeing-or-safety.qmd": (828, "The comic rejects the idea that distress is a personal failure; wellbeing and safety concerns deserve real support and action."),
    "support.qmd": (2368, "The comic distinguishes the problem you can work through yourself from the one that needs someone with authority or specialist expertise."),
    "contributions/index.qmd": (1060, "Crowdsourcing only improves the handbook when suggestions enter a real editorial process with owners and decisions."),
    "contributions/how-to-help.qmd": (2601, "Clear instructions make it easier for a reader to turn an observation into a usable suggestion."),
    "contributions/editorial-workflow.qmd": (1319, "Automation can reduce repetitive work, but the editorial decision still needs a named human owner."),
    "contributions/ai-and-editorial-practice.qmd": (2173, "Calling something a neural net does not remove the human responsibility to train, check and approve its work."),
    "contributions/visuals-and-credit.qmd": (14, "A page about visual reuse should confront copyright directly and then make the permitted route clear."),
    "references.qmd": (2086, "A reference list preserves the sources that allow later readers to revisit and reinterpret the handbook's claims."),
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
        for key in ("comic_id", "title", "asset_path", "reason"):
            out.append(f"    {key} = {lua_string(row[key])},")
        out.append("  },")
        out.append(f"  [{lua_string('title:' + row['page_title'])}] = {{")
        out.append(f"    page_path = {lua_string(row['page_path'])},")
        for key in ("comic_id", "title", "asset_path", "reason"):
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
        "Each appearance links to the original comic and explains why it was selected for that page.",
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
        "The machine-readable page-by-page placement, relevance explanation and asset path are recorded in the "
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
    for comic_id in sorted({value[0] for value in ASSIGNMENTS.values()}):
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
        comic_id, reason = ASSIGNMENTS[page]
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
            "relevance_reason": reason,
            "reason": reason,
        })

    with (ROOT / "research/page-visuals.csv").open("w", newline="", encoding="utf-8") as handle:
        fields = ["page_path", "page_title", "comic_id", "title", "asset_path", "source_url", "creator", "license", "license_url", "relevance_reason"]
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
