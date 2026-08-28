# Content audit

## Corrective audit: scaffold mistaken for content

Date: 28 August 2026

The initial audit overstated implementation. Creating a route, filename or generic shell did not satisfy the source requirement.

Direct inspection found:

- 36 short chapter shells with no citation keys and extensive repeated generic prose;
- 19 checklist files with identical bodies;
- 33 template files with identical bodies;
- no implemented distinction between read-do and do-confirm checklists;
- no Atul Gawande source in the bibliography or source register;
- all 82 topic requirements and all 53 resource requirements still marked planned;
- all eight coverage-loop requirements still marked planned.

The earlier Pass 1 and External-discovery Pass 1 entries record preliminary scaffolding only. They do not count as completed coverage passes. Future passes must record the questions tested, gaps found, files changed, evidence added and acceptance checks completed.

See `planning/incomplete-work-audit-2026-08-28.md` for the counted repository audit.

## Initial state

Date: 28 August 2026

- Canonical Version 2 source preserved and verified.
- Twenty core student questions seeded from Source Section 2.2.
- All 82 provisional topics mapped to 36 navigation chapters in the requirement ledger.
- All 53 practical resources tracked.
- Full coverage passes remain pending.

## Pass record

### Pass 0: source translation

Purpose: ensure the source conversation, consolidated design brief, information architecture, repository requirements, master prompt, contribution system, and owner note remain represented.

Result: 223 unique requirements recorded. No source topic, practical resource, coverage loop, technical group, contribution group, or release-gate group was intentionally removed.

Next: run Student-phase Pass 1 without using the existing chapter list as the question generator, then compare generated questions against the current bank.

### Pass 1: student phase and usability

Date: 28 August 2026

Coverage walked from accepting an offer through orientation, confirmation or progression, active study, disruption, examination, corrections, archiving and transition. Each phase was tested for a direct answer, next action, decision, record, supervisor prompt, escalation route and variation boundary.

Material additions or confirmations:

- Added a homepage situation router rather than forcing readers to understand the Parts first.
- Created a five-minute stuck diagnostic that classifies clarity, evidence, decision, permission, access, skill, capacity, relationship and risk blockages.
- Made support boundaries and escalate-now conditions available as rendered book pages.
- Established all 53 resource destinations, including evidence-of-done and escalation prompts.
- Confirmed the need to expand disruption, leave, remote candidature, disability, caring responsibilities, international candidature and practice-led research in the next variation pass.

This pass found substantive work, so saturation has not been reached.

### External-discovery pass 1: pre-drafting foundation

Date: 28 August 2026

Verified an initial primary-source set covering Australian research integrity, systematic-review reporting, data practice, contributor roles, accessibility, GitHub Pages and Quarto. The pass reinforced three boundaries: reporting guidance is not automatically a method manual; contributor-role taxonomies do not decide authorship alone; and national or institutional guidance must be labelled rather than universalised.

Next: run the student-variation and stakeholder passes, then add claim-level evidence to priority chapters before calling them complete.

## Broad-beta coverage passes after substantive drafting

### Pass 2: student phases and variations

Date: 28 August 2026

**Coverage tested:** pre-enrolment; first day/week/30/90 days; provisional planning; progression; active studies; analysis; writing; publication; disruption; examination; corrections; closure; transition. Variations included full- and part-time, campus and remote, international and local, novice and experienced, qualitative, quantitative, mixed, computational, creative/practice-led, single- and multi-study, individual and team projects, disability, health and caring constraints, community/partner work and culturally governed knowledge.

**Gaps found and changes made:**

- Added sixteen phase/variation questions (`Q0021`–`Q0036`) to the question bank.
- Made local authority and method/discipline variation explicit in every chapter; the structural verifier now fails when a chapter contains no local or variation boundary.
- Added capacity, wellbeing and safety as a distinct stuck pathway rather than treating these as productivity failures.
- Expanded multi-study integration, part-time/remote planning, practice-led variation, community authority and candidate-versus-team contribution guidance.

**Acceptance evidence:** all 36 chapters contain a reader question, direct answer, failure modes, stage/pause-point standard, local boundary and practical route; minimum chapter length is 942 words after stripping front matter.

### Pass 3: stakeholders and authority

Date: 28 August 2026

**Stakeholders tested:** candidate, principal and co-supervisors, examiner, librarian, methodologist/statistician, ethics/governance body, research integrity adviser, privacy/data steward, software specialist, collaborator, partner, funder, publisher/reviewer, affected community and future custodian.

**Gaps found and changes made:**

- Separated advice, recommendation, access control, review and formal approval across Chapters 16–18, 25–27 and 33–36.
- Added authority-before-action checks to risk/change, AI, data, ethics, failure, escalation and correction workflows.
- Added output-specific authorship/contribution records and independent routes for power-sensitive disputes.
- Made recipient testing—not file transfer—the completion test for handoff and closure.

**Acceptance evidence:** every chapter names a supervisor or relevant specialist preparation route; high-risk pathways direct readers outside ordinary supervision when that route is implicated or lacks authority.

### Pass 4: failure modes and usability

Date: 28 August 2026

**Questions tested:** can the reader obtain a direct answer, smallest next action, worked example, failure modes, good-enough test, resource, supervisor/specialist prompt, escalation threshold, variation boundary and evidence of done?

**Gaps found and changes made:**

- Replaced all three remaining baseline Part XI chapters with failure classification, technical recovery and seven-route decision guidance.
- Created eleven distinct stuck pathways and the escalation-message builder.
- Completed all 53 tracked resources with purpose-specific fields, completed examples/scenarios, stop conditions, evidence and local boundaries.
- Reframed checklists around consequential pause points and read-do/do-confirm use rather than trivial calendar labels.

**Acceptance evidence:** the requirements ledger contains exactly 53 `RES-` rows and every row is `complete`; all checklist/template/stuck source pages have corresponding rendered HTML.

### Pass 5: coherence, duplication and publication delivery

Date: 28 August 2026

**Checks run:** chapter count and length; repeated baseline prose; citation keys; local-scope language; resource destinations; raw `.qmd` links; internal links and fragments; image alternative text; rendered page count; status-language consistency.

**Material defect found:** the initial book manifest rendered only the selected phase checklists. Links to the other completed resources exposed raw `.qmd` source rather than reader-facing HTML.

**Changes made:** split the resource library into visible checklist, template and stuck-pathway Parts; added every resource file to the Quarto manifest; expanded the HTML book from 54 to 106 pages; added `scripts/verify_book.py` as a fail-closed structural and rendered-link test; added explicit source notes so all 36 chapters now cite verified evidence while identifying editorial synthesis.

**Acceptance evidence:** `python3 scripts/verify_book.py` passes with 36 chapters, 82 topic rows, 53 completed resource rows, 106 rendered HTML pages, no raw-source link, no missing internal target, no missing bibliography key and no unlabelled content image.

The five-pass initial maximum has been reached. The passes continued to find substantive implementation defects through Pass 5, so no early saturation claim is made. Remaining review is release-gate verification and post-release maintenance, not a claim that no future question exists.

### External-discovery pass 2: post-drafting comparison

Date: 28 August 2026

**Authoritative comparisons:** current AQF and QAA doctoral descriptions; Australian Code supporting data and publication guides; National Statement 2025; current OAIC guidance; DOAJ/COPE/OASPA/WAME transparency principles; DOAJ application guidance; EQUATOR reporting-guideline library; NASEM reproducibility; The Turing Way; official Quarto, Git/GitHub and research-software documentation.

**Additions and exclusions:**

- Added current outlet-transparency, reporting-guideline, doctoral-contribution and closure/custody sources (`SRC0042`–`SRC0048`).
- Added journal due diligence, reviewer-response, thesis-contribution, examination and closure workflows.
- Did not convert reporting checklists into method standards, qualification frameworks into local examination rules, CRediT into an authorship test, FAIR into automatic openness, or software documentation into evidence of methodological validity.

**Remaining external dependency:** a non-GitHub feedback URL requires owner selection. The public GitHub reader-feedback route, privacy screen and owner-approval workflow remain functional meanwhile.
