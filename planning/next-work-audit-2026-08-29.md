# Current work and review audit

Date: 29 August 2026

This audit distinguishes content that exists from work that has actually passed its intended editorial or workflow test.

## Implemented and verified

- The authoritative brief, PRD, 226-row requirements ledger, decision log and source manifest exist. The ledger retains the 223 original rows and adds three later requirements from 29 August 2026.
- All 36 planned chapters, 82 topics and 53 original practical resources have rendered destinations.
- The Quarto book, search, desktop sidebars, mobile navigation, citations, internal links, accessibility checks and GitHub Pages deployment have an automated verification route.
- The public GitHub reader-suggestion form exists and opens directly from the handbook.
- The private Editorial Desk reads the GitHub queue and currently reports that it is connected.
- Cloudflare Web Analytics is installed.
- The publication identifies the project as human-led and AI-assisted.
- A single chronological checklist now runs from pre-start decisions through candidature, repeated study cycles, submission, examination, closure and post-completion obligations.
- The reader contribution guide now explains the actual GitHub sequence, the information requested, public-privacy boundaries, credit choices and the editorial outcome.
- One cropped instructional screenshot shows what the GitHub form looks like after sign-in.
- A visual-assets policy and register now control humour, third-party reuse, AI-assisted visuals, attribution, alternative text and licence exclusions.
- One original light editorial illustration is embedded in the chronological checklist.
- The new checklist and contribution guide pass the repository verifier and desktop and mobile browser inspection. Both sidebars remain visible in the desktop reading view after scrolling; mobile uses the expected drawer navigation.

## Still to complete or review

1. **Reader-focused rewrite of all 36 chapters.** `planning/editorial-reader-rewrite-audit.md` contains the preservation rules and proposed reader-facing titles, but the chapter bodies have not received that full rewrite. The current 94-file uncommitted change mainly replaces broad-beta labels with public-working-edition labels.
2. **Apply and review the chapter-title map.** Part names are reader-facing, but most chapter titles and repeated section headings still use the older abstract wording.
3. **Review the 94-file status-language change.** Confirm the wording, run the content verifier and commit it separately from new feature work.
4. **Run the disposable Editorial Desk acceptance test.** The live dashboard is connected and request `#1` is waiting. Approve it for drafting, confirm that Copilot opens only the disposable pull request, then reject that pull request without merging it.
5. **Finish team-editor configuration.** Role logic exists for project lead, managing editor, editor and observer, but editor email allow-lists, onboarding, responsibility boundaries and a multi-user acceptance test remain.
6. **Provide a no-GitHub reader route.** The GitHub form is the only active public intake route. A no-login form remains blocked until an approved public form and privacy pathway are selected.
7. **Test the contribution tutorial with real graduate researchers.** Observe whether readers can reach the form, understand that it is public, choose the right category and submit a useful suggestion without coaching.
8. **Expand visuals gradually.** Add only where a visual improves understanding or recall. Each asset must pass the visual-assets register and page-level review before publication.
9. **Review time-sensitive content.** Software, AI, policy, ethics, privacy, outlet and funder guidance needs scheduled rechecking even when the current structural verifier passes.

## Recommended order

1. Complete the disposable dashboard-to-Copilot test.
2. Review and commit the public-working-edition status-language pass.
3. Run the 36-chapter reader-focused rewrite in bounded Parts, with citation and safety preservation checks after every Part.
4. Conduct a five-reader contribution usability test before building the no-GitHub intake route.
5. Add further original or openly licensed visuals during the Part-by-Part editorial pass.
