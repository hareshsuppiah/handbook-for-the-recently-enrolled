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
- One owner-dependent item remains: an approved no-GitHub feedback-form URL.

## Preview locally

Install [Quarto](https://quarto.org/) and run:

```bash
quarto preview
```

Build the complete HTML book with:

```bash
quarto render
```

The rendered site is written to `_site/`.

## Project map

- `chapters/`: the 36 navigation chapters across 12 Parts.
- `stuck/`: diagnostic routes for readers who do not know what to do next.
- `checklists/`: short read-do and do-confirm safety resources.
- `templates/`: reusable research and supervision records.
- `examples/`: completed examples for priority resources.
- `research/`: questions, coverage, sources, community requests, decisions, and audit records.
- `research/visual-assets-register.csv`: image provenance, licence, credit, alternative text, and placement review.
- `research/page-visuals.csv`: the comic selected for every rendered page and the editorial reason it belongs there.
- `planning/`: authoritative requirements, decisions, roadmap, style, and maintenance plans.
- `contributions/`: plain-language routes for sharing feedback and understanding the editorial workflow.

## Contributing

You do not need to know Git, GitHub, or coding to improve this handbook. See [CONTRIBUTING.md](CONTRIBUTING.md) and the rendered **Suggest an improvement** section. Do not post participant data, confidential supervision material, credentials, unpublished sensitive findings, or personal information in a public issue.

## Evidence standard

Factual and instructional claims must be traceable to verified sources in `research/source-register.csv` and `references.bib`. Local rules must be labelled as local rather than presented as universal.

## Licence

Prose and reusable non-code content are licensed under CC BY 4.0. Code, configuration, and scripts are licensed under MIT. See `LICENSE-CONTENT.md` and `LICENSE-CODE`.
