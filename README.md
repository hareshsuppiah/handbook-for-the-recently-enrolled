# The Handbook for the Recently Enrolled

**An Operating Manual for Graduate Researchers**  
**Project lead and founding editor: Haresh Suppiah**

This repository contains a living public edition of an institution-neutral, evidence-informed Quarto handbook for graduate researchers. It is a maintained decision-support resource, not institutional, legal, ethical, medical, counselling, or emergency guidance.

## Current status

- The canonical source has been preserved privately and verified.
- The full PRD and 226-row requirements ledger are in `planning/` (223 original requirements plus three later requirements recorded on 29 August 2026).
- All 36 chapters contain substantive, sourced guidance covering the 82 original topics.
- All 53 practical resources and 11 situation-based “I’m stuck” pathways are rendered in the book.
- A single chronological checklist links the doctorate from pre-start decisions through final handover.
- Five coverage passes, two external-discovery passes and automated content/link/render checks are recorded.
- Readers can suggest improvements through one structured GitHub form.
- The September review covers all 113 pages, with real GitHub screenshots, optional checklist memory, 33 editable blank downloads, worked practice prompts and an offline EPUB.
- See [the audit and its evidence limits](planning/audit-2026-09-08.md) and [the shared editorial contract](AGENTS.md) before extending the book.

## Preview locally

Install [Quarto](https://quarto.org/) and run:

```bash
quarto preview
```

Build the complete HTML and EPUB editions with:

```bash
quarto render
```

The rendered site and EPUB are written to `_site/`. The build generates blank downloads and repairs EPUB cross-references from the same source. Before publishing, run:

```bash
python3 scripts/verify_book.py
python3 scripts/verify_editorial_workflow.py
python3 scripts/test_editorial_agent.py
python3 scripts/test_finish_epub.py
python3 scripts/verify_reader_experience.py
```

For an HTML-only iteration that preserves an existing EPUB, use `quarto render --to html --no-clean`. Always build both formats for release.

## Project map

- `chapters/`: the 36 navigation chapters across 12 Parts.
- `stuck/`: diagnostic routes for readers who do not know what to do next.
- `checklists/`: short read-do and do-confirm safety resources.
- `templates/`: reusable research and supervision records.
- `examples/`: completed examples for priority resources.
- `research/`: questions, coverage, sources, community requests, decisions, and audit records.
- `research/visual-assets-register.csv`: image provenance, licence, credit, alternative text, and placement review.
- `research/page-visuals.csv`: the seven retained optional comic placements and their editorial reasons.
- `resources/downloads/`: generated blank Markdown templates; edit their source in `templates/`.
- `.agents/skills/handbook-editor/`: reusable editorial workflow for future agents.
- `planning/`: authoritative requirements, decisions, roadmap, style, and maintenance plans.
- `contributions/`: plain-language routes for sharing feedback and understanding the editorial workflow.

## Contributing

Use [Suggest an improvement](https://github.com/hareshsuppiah/handbook-for-the-recently-enrolled/issues/new?template=share-feedback.yml) to propose a missing topic or resource, correction, removal, source, example or accessibility fix. The form asks where the problem appears, what you noticed, what you would change and why it would help. You do not need to edit files or know how Git works.

Suggestions are public. Remove participant data, confidential supervision material, passwords, unpublished sensitive findings and personal information before submitting. [CONTRIBUTING.md](CONTRIBUTING.md) explains the process and links to a first-time GitHub guide.

## Evidence standard

Factual and instructional claims must be traceable to verified sources in `research/source-register.csv` and `references.bib`. Local rules must be labelled as local rather than presented as universal.

## Licence

Prose and reusable non-code content are licensed under CC BY 4.0. Code, configuration, and scripts are licensed under MIT. See `LICENSE-CONTENT.md` and `LICENSE-CODE`.
