# Contribution workflow and PhD concern coverage

Checked 5 September 2026. Local changes in this audit are drafts, not a deployment.

## Copilot: implementation exists; end-to-end operation is unverified

The local checkout was clean at the start. Local HEAD and live GitHub main both resolved to `245eee7a30ac3bc2d340a5c27b120c60027b1874`.

`.github/workflows/approved-suggestion.yml` listens for Haresh's exact `/approve` comment or his `decision: approved` label. It prepares a handoff and attempts assignment to `copilot-swe-agent[bot]` using `COPILOT_USER_TOKEN`. Only Haresh can trigger it: another editor's approval is not sufficient. Copilot is instructed to make actual file changes on a branch and return a tested pull request, with a separate human merge/publication decision.

Live evidence:

- [Issue #1](https://github.com/hareshsuppiah/handbook-for-the-recently-enrolled/issues/1) is the sole issue/PR returned by the all-state endpoint. It is the disposable workflow test, open, needs-triage, unassigned, with no comments.
- Approval workflow runs `33226280258` and `33226280124` were both skipped. No successful handoff or Copilot-authored PR was observed.
- The repository-secret metadata endpoint returned HTTP 401. This does not prove that the credential is missing: its presence, scope and Copilot entitlement could not be checked.
- The GitHub Issues tracker is enabled and accessible; Discussions is disabled. `has_projects: true` does not establish that an actual GitHub Project board exists.
- The private Editorial Desk was not exercised in this audit. Older planning notes describing it as connected are not fresh verification.

To close the remaining acceptance test, use an authenticated owner session to inspect the credential/agent availability, approve the already-created disposable issue, verify assignment and an actual bounded file-change PR, inspect checks, then close the disposable PR without publication. Posting the approval comment is an external message and was not authorised by this status-check request, so it was not posted.

Official behaviour reference: [Using Copilot cloud agent on GitHub](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github). The configured intent is real editing, not merely advice; configuration is not proof of a successful run.

## Tracker and contributor experience

The reader guide had a single form, sequential instructions, privacy boundaries and examples, but explicitly omitted screenshots. The stored screenshot used older field names and was not embedded. Added two original schematic diagrams matching the current form and decision sequence; these are labelled as diagrams, not screenshots. Added a category comparison table, a GitHub glossary and a route for academics/students offering prose, expertise or review without coding.

Added a navigable tracker guide with live filters and explanations of issue, PR and publication states. Later workflow labels are not fully automated; the guide says to inspect the actual issue and PR. The local community request CSV was header-only at the start and is not a live synchronised queue. Reddit observations belong in their own research register, not fictitious contributor submissions.

Corrected the maintenance plan's obsolete Discussions and no-GitHub intake language. A no-account contribution route remains absent. Real novice usability testing remains necessary before claiming contributors fully understand the process.

## Reddit method and coverage

Opened the public r/PhD Top / This Year listing. Its visible first page was dominated by image and meme posts, so it was unsuitable as a ranked list of substantive doctoral problems. Supplemented it with targeted searches for supervision, exhaustion, isolation, funding, comparison, leaving and careers. Reviewed nine selected thread records at the access level recorded in `research/reddit-topic-scan-2026-09-05.csv`. Search-reported scores are snapshots, not live verified rankings; no prevalence or exhaustive top-N claim is made. One comparison post was only available as a search excerpt.

No usernames or verbatim personal accounts were copied into the book. The question bank records editorial paraphrases, not supposed direct submissions. Reddit identifies reader questions; local institutional sources support formal process examples. Forum advice was not adopted as clinical, legal, funding or immigration authority.

Added seven practical sections in `stuck/life-during-a-phd.qmd`: isolation, exhaustion, funding, supervision, comparison, pausing/leaving and careers. Linked them from seven relevant chapters, the stuck index and the book navigation. Existing citations, safety warnings, local caveats and resource links were preserved; no old chapter content was removed.

Priority is editorial: consequences of an unanswered question and gaps in existing coverage. It is not an estimate of the most common PhD concerns on Reddit. A broader reproducible Reddit ranking would require a defined sampling window, accessible pagination and consistent engagement data.

## Verification outcome

- `quarto render --to html`: passed; 113 rendered HTML pages.
- `python3 scripts/verify_book.py`: passed, including chapter/resource coverage, citation keys, local links, fragment targets and image alternative text.
- `python3 scripts/verify_editorial_workflow.py`: passed. This is a static workflow check, not a live Copilot acceptance test.
- `git diff --check`: passed.
- Browser inspection: contribution page and both original diagrams render legibly at desktop size; tracker appears in the contribution sidebar. No mobile or real-reader comprehension test was performed in this audit.
- All original chapter material was retained. Changes add targeted links rather than replacing existing citations, resource links, safety or escalation guidance.
- Changes remain local and uncommitted; no deployment, GitHub comment, issue approval or agent assignment was performed.
