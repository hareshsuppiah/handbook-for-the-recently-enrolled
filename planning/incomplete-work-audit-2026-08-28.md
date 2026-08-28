# Incomplete-work audit

**Audit date:** 28 August 2026  
**Source of status:** `planning/requirements-checklist.csv`  
**Repository state audited:** corrective working tree following commit `5509d38`

## Finding

The current repository is a structural prototype. It is not the broad beta described in the PRD.

Of the 223 tracked requirements:

| Status | Count |
|---|---:|
| Complete | 20 |
| In progress | 12 |
| Planned | 188 |
| Blocked | 1 |
| Superseded by a later decision | 2 |

The status ledger is conservative for some technical features that exist but have not completed their documented acceptance checks. The content findings below were verified directly from the files and are substantive failures, not stale labels.

## Unfinished requirements by group

| Group | Unfinished | What remains |
|---|---:|---|
| Core source authority | 1 | Apply the authority order consistently when implementation files conflict with the full source brief. |
| Editorial and writing principles | 12 | Question-led organisation, decision support, supervisor prompts, phase-appropriate checklists, stuck pathways, progression, scope labels, verified evidence, writing quality, reproducibility and maintenance. |
| Original topics | 82 | Every original topic has a destination, but none is marked complete. The current chapter shells do not meet the chapter content contract. |
| Practical resources | 53 | Nine requirements are now in progress through substantive phase-gated checklists; the other 44 remain planned. None has yet passed its full evidence and scenario test. The 33 template bodies remain placeholders. |
| Coverage loops | 8 | Student phase, student variation, stakeholder, failure mode, usability, coherence, external discovery and continuous maintenance loops. |
| Technical requirements | 20 | Several features exist, but the required accessibility, link, print, citation, alt-text and clean-build evidence has not been completed and recorded. |
| Contribution and support | 2 | A non-GitHub feedback route remains blocked pending an approved URL. Support and private-escalation routes remain incomplete. |
| Quality gates | 23 | Meaningful chapter content, checklist quality, completed examples, citations, scope labels, time-sensitive review dates, accessibility, links, mobile, print and release checks. |

The two superseded requirements are public GitHub Discussions and direct reader pull requests. Later decisions make GitHub Issues the public editorial record and remove direct editing as the ordinary reader route.

## Direct file evidence

### Chapters

- The repository contains 36 chapter files.
- Chapter length ranges from 353 to 375 words.
- No chapter contains a citation key.
- The same generic workflow, failure modes and supervisor paragraph recur across the chapters. Three repeated passages appear 108 times in total.
- The chapters do not yet provide the required worked examples, claim-level evidence, meaningful disciplinary variation or completed practical resources.

### Checklists

- The 19 identical placeholder checklists have been removed.
- Ten substantive checklists now cover starting candidature, the first 90-day review, study commitment, ethics submission, data collection, analysis, study write-up, manuscript submission, thesis submission and project closure.
- Each names its pause point, failure prevented, read-do or do-confirm mode, stop condition, evidence to retain and local boundary.
- The checklist-system rationale now cites Atul Gawande and the World Health Organization, and both sources are recorded in the source register.
- These resources remain **in progress**, not complete, until they have been tested against realistic scenarios and checked against specialist and local requirements.

### Templates

- The repository contains 33 template files.
- After the title block, all 33 template bodies are identical.
- A meeting agenda, data dictionary, authorship record and reviewer-response matrix therefore present the same generic fields despite serving different decisions.

### Evidence and discovery

- The question bank contains 20 seeded questions rather than completed coverage of the full candidature lifecycle and major variations.
- The source register contains 12 foundation sources.
- The coverage ledger still marks all eight required coverage loops as planned.
- No chapter links its factual claims to the source register through citations.

### Contribution route

- The GitHub approval and agent-handoff workflow exists.
- The handbook now links directly to one reader-language feedback form. GitHub still supplies the fixed heading "Create new issue" on its hosted page; that platform wording cannot be changed by this repository.
- A non-GitHub form cannot be completed until Haresh supplies or approves a form URL.

## Work that is genuinely complete

The complete requirements cover preservation and hashing of the full source brief, creation of the PRD and requirement ledger, recording later decisions, the reader feedback form, privacy warnings, the visible editorial workflow, labels and basic governance records.

The Quarto project also renders and deploys, but the corresponding technical and quality requirements remain open until their full acceptance checks are recorded.

## Immediate corrections from this audit

1. The book and README must describe the public site as a structural prototype until substantive content gates pass.
2. Placeholder resources must not be labelled "usable beta".
3. Checklist architecture must be based on consequential pause points across candidature and study cycles rather than filenames such as "Day One".
4. A resource counts as complete only when it has a specific purpose, trigger, checklist type, critical items, evidence, stop condition, local boundary, linked explanation and realistic test.
5. A chapter counts as complete only when it meets the chapter contract and its important claims are supported by verified sources.

The row-by-row record remains `planning/requirements-checklist.csv`. Filter `implementation_status` for `planned`, `in_progress` or `blocked` to see every unfinished requirement.
