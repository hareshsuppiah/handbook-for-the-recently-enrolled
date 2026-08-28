# Broad-beta release verification

Date: 28 August 2026  
Release target: `v0.1.0-beta`

This record supersedes the readiness conclusions in `incomplete-work-audit-2026-08-28.md`. That earlier audit correctly identified the incomplete structural prototype and is retained as corrective history. The findings below apply to the subsequent complete broad-beta build.

## Content coverage

- 36 of 36 planned chapters contain substantive guidance.
- All 82 original topics have a chapter destination and meaningful treatment.
- All 53 practical resources are substantive and rendered in the book.
- Eleven situation-based “I’m stuck” pathways are rendered and cross-linked.
- Every chapter identifies its candidature stage, gives a direct answer, explains failure modes and boundaries, links practical resources, records a review date, and cites at least one verified source.
- Five initial coverage passes and two external-discovery passes are recorded in `research/content-audit.md`.

## Automated verification

`python3 scripts/verify_book.py` passes and checks:

- chapter count and minimum substantive depth;
- the recurring chapter contract;
- 82 topic and 53 resource ledger entries;
- rendered pages for all checklists, templates and stuck pathways;
- citation keys against `references.bib`;
- internal links and heading fragments;
- absence of raw `.qmd` links in rendered HTML; and
- alternative text for content images.

## Responsive visual inspection

Representative chapter inspected at desktop and mobile widths in the in-app browser:

- 1440 × 900: 320 px left book rail, 760 px reading column and right “On this page” rail remain separate; no overlap or horizontal overflow; cover and search are visible.
- 390 × 844: desktop rails are hidden; a fixed **Contents** control opens a scrollable book-contents drawer; a compact “On this page” list appears in the reading column; no horizontal overflow.
- The compact page-contents link moved to the correct heading fragment.
- Full-book search returned the requested rendered resource for “risk and issues register”.
- Browser console reported no errors during the representative checks.

## Contribution control

Reader submissions are suggestions, not direct edits. Haresh retains the accept/defer/decline decision. An approved suggestion can be assigned to an agent for drafting, then reviewed before merge and release. The owner-approved no-GitHub form URL remains the only external dependency and is clearly labelled as unavailable until supplied.

## Release boundary

Broad beta means the complete handbook is usable and reviewable. It does not mean permanently complete, universally applicable or a substitute for local policy and specialist advice. Future questions and corrections enter the maintained editorial workflow.
