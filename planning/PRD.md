# Product requirements document

## Document control

**Product:** The Handbook for the Recently Enrolled  
**Subtitle:** An Operating Manual for Graduate Researchers  
**Founding author and editor:** Haresh Suppiah  
**Status:** Authoritative implementation brief for the broad beta  
**Canonical source:** `planning/private/source-brief-v2.txt`  
**Source integrity:** See `planning/source-manifest.md`  
**Requirement ledger:** `planning/requirements-checklist.csv`

This PRD translates the complete Version 2 source into an implementable product specification. It does not replace the source. Every requirement must remain represented in the requirement ledger, including requirements deferred beyond the first beta.

## 1. Product purpose

Create a public, institution-neutral, evidence-informed online operating manual for PhD students and other graduate researchers. It must guide readers from preparing to enrol through completion and transition while answering practical, intellectual, methodological, technical, relational, governance, failure, and wellbeing questions.

The handbook must strengthen judgement rather than merely present information. Readers should be able to decide what to do next, conduct proportionate due diligence, approach supervisors with evidence and options, maintain a defensible research record, recognise failure modes, recover from disruption, and grow towards independent research practice.

## 2. Audience and boundaries

The primary audience is PhD students, particularly early in candidature. Secondary audiences are research master's students, supervisors, graduate research coordinators, librarians, methodologists, data stewards, research software staff, integrity and ethics advisers, and institutional support staff.

The core must work across disciplines, methods, institutions, jurisdictions, study modes, and project types. The handbook must visibly distinguish:

- broadly applicable research practice;
- method- or discipline-specific variation;
- institution-specific rules and services;
- jurisdiction-specific legal, ethical, cultural, and governance requirements;
- time-sensitive software, platform, publisher, funder, and AI guidance.

The handbook is not legal, medical, counselling, emergency, complaints, ethics-approval, or research-integrity casework. High-risk pages must direct readers to the relevant local services and formal processes.

## 3. Product principles

1. **Questions before topics:** organise content around real student questions, decisions, uncertainties, and failure modes.
2. **Decision support:** provide next actions, decision rules, trade-offs, thresholds, examples, escalation criteria, and definitions of good enough for the current stage.
3. **Due diligence before dependency:** teach students to approach supervisors with the problem, checks completed, evidence, options, a provisional recommendation, and a precise request.
4. **Checklists as safety infrastructure:** use short read-do or do-confirm checklists at meaningful pause points; never replace explanation or judgement.
5. **Stuck triage as navigation:** diagnose the problem, give the smallest useful next action, link to the right content and resources, and state escalation signs.
6. **Progressive independence:** show novice, developing, and independent forms of practice without implying that support is weakness.
7. **Universal core with explicit variation:** never present a local rule or one methodological tradition as universal.
8. **Evidence and verification:** use real, verified sources and map claims to evidence; never invent references, policies, quotations, URLs, DOIs, capabilities, or requirements.
9. **Practical and humane writing:** clear, precise, serious, non-patronising, concrete, and occasionally dry; no generic motivational filler or canned AI prose.
10. **Model the advice:** version control, source tracking, accessible publishing, transparent decisions, reproducible builds, change history, and clear contribution processes.
11. **Low-friction participation:** allow non-technical readers to suggest improvements without knowing Git or GitHub.
12. **Continuous evolution:** treat every release as a maintained edition; bounded saturation ends an audit cycle, not the project.

## 4. Core reader questions

The product must answer the complete question set in Source Section 2.2 and the questions discovered through coverage audits. Core examples include where to start, whether the student is on track, whether a topic or gap is defensible, what due diligence is sufficient, which form of literature searching is proportionate, how to choose and justify methods, how to document decisions, what good enough means, how to work with supervisors, what to do when work fails, how to use technology and AI responsibly, when to escalate, and how to become independent.

## 5. Information architecture

Use 12 Parts and 36 substantial navigation chapters. The original 82 provisional chapters remain the topic inventory and must all map to a chapter section, cross-cutting resource, stuck pathway, or documented later release.

### Part I: Recently enrolled

1. What a PhD asks you to do and what good enough means.
2. Day one, week one, the first 30 days, and the first 90 days.
3. Turning a proposal into a provisional plan and research operating system.

### Part II: Working with supervisors

4. Roles, expectations, boundaries, and supervision agreements.
5. Meeting cadence, agendas, matters arising, decisions, actions, and unresolved items.
6. Asking better questions, using feedback, handling disagreement and delay, escalating, and becoming independent.

### Part III: Finding and defending a research direction

7. From interest to a consequential problem, meaningful gap, and contribution.
8. Topic due diligence, feasibility, scope, and the case for proceeding.
9. Questions, aims, objectives, hypotheses, contribution, and decisions to narrow, pivot, pause, or stop.

### Part IV: Finding, reading, and synthesising evidence

10. The search ladder: orientation, citation chaining, and intellectual neighbourhoods.
11. Focused, scoping, systematic, and reproducible searching, including stopping decisions.
12. Reading with purpose, reference management, evidence tables, synthesis, argument, and citation integrity.

### Part V: Designing defensible research

13. Question-design-data-analysis-inference alignment and method comparison.
14. Sampling, measurement, adequacy, pilot work, and feasibility.
15. Assumptions, bias, validity, credibility, robustness, reflexivity, and method-specific pathways.

### Part VI: Ethics, integrity, and governance

16. Ongoing ethics, consent, privacy, confidentiality, minimisation, burden, and power.
17. Research integrity, transparent reporting, conflicts, AI use, and local governance.
18. Authorship, contribution, collaboration, partnerships, deviations, mistakes, corrections, and difficult disclosures.

### Part VII: Data, code, and reproducibility

19. Data management plans, approved storage, access, backup, and restore testing.
20. Raw, clean, derived, and analysis-ready data; naming, metadata, codebooks, and provenance.
21. Reproducible computational environments, automation, checks, qualitative and non-computational audit trails, and handoff readiness.

### Part VIII: Graduate research technology stack

22. Choosing tools by purpose and building a minimum viable research stack.
23. R, Python, jamovi, review platforms, reference managers, data-capture tools, and Quarto.
24. Git, GitHub, AI and agents, privacy, governance, verification, disclosure, and specialist support.

### Part IX: Running the project

25. Milestones, dependencies, buffers, weekly work, next actions, and visible progress.
26. Risks, issues, waiting, blocked work, contingencies, and change control.
27. Multi-study theses, collaboration, handoffs, shared ownership, project memory, and scope control.

### Part X: Writing, publishing, and communicating

28. Writing early, thinking through writing, building arguments, and thesis/paper architecture.
29. Producing reviewable work, revision levels, supervisor feedback, and response tracking.
30. Publication strategy, journals, reporting guidelines, authorship, review, rejection, resubmission, open outputs, and communication beyond academia.

### Part XI: When the plan meets reality

31. Null, ambiguous, unexpected findings, failed recruitment, inaccessible data, and broken studies.
32. Technical failure, irreproducible analysis, perfectionism, endless searching, and scope creep.
33. Persist, simplify, redesign, pivot, pause, or stop, plus the complete stuck triage system.

### Part XII: Completion and independence

34. Independent judgement, intellectual position, networks, collaboration, career direction, and contribution mapping.
35. Thesis integration, examination or viva, examiner questions, corrections, and response tracking.
36. Archiving, retention, repository deposit, handover, project closure, unfinished outputs, and post-PhD transition.

## 6. Chapter contract

Each major chapter must include the useful subset of the 19-element source contract: exact student questions, importance, difficulty, judgement required, plain-language explanation, novice/developing/independent practice, workflow, decision rules, worked example, failure modes, a short checklist, a reusable template, before-you-ask guidance, escalation, variations, local checks, stuck links, verified references, and a review date where needed.

Every beta chapter must at minimum provide a direct answer, a practical next action, the decision involved, evidence-informed guidance, common failure modes, local/method boundaries, related resources, content status, and review metadata. Priority chapters must satisfy the full contract.

## 7. Practical resource library

Track and deliver all 53 items in Source Section 2.6. Priority resources require a blank version, completed example, use instructions, explanatory chapter link, meaningful pause point, failure prevented, and local-policy labels. The resource inventory is enumerated individually in `planning/requirements-checklist.csv` and later in `research/resource-register.csv`.

## 8. Stuck triage system

The five-minute entry point must diagnose the type of stuck and route the reader. Every pathway follows the same eight-part structure: what this feels like, likely problem type, five-minute diagnostic, smallest useful next action, relevant links, what to bring to a supervisor, escalate-now signs, and an example request.

Required pathways include unclear starting point, topic scope, meaningful gap, endless searching, inability to synthesise, method paralysis, supervisor disagreement, waiting for feedback/access, recruitment/data/equipment failure, code or analysis failure, writing blockage, endless revision, lost versions, integrity/authorship/governance concerns, workload or wellbeing concerns, project pivot, and uncertainty about enough.

## 9. Evidence and source protocol

Research precedes factual claims. Prioritise primary and official sources, peer-reviewed methodological and doctoral-education research, recognised standards and reporting guidelines, official institutional/publisher/funder/software documentation, and established practical resources where appropriate.

For each source verify title, author or organisation, date, DOI or URL, authority, jurisdiction, currency, supported claim, and limitations. Use author-date citations through `references.bib`. Add last-reviewed and review-by metadata to time-sensitive pages. Do not copy proprietary templates or long copyrighted passages.

## 10. Coverage and evolution

Run all eight source-defined loops: student phase, student variation, stakeholder, failure mode, usability, coherence/saturation, external discovery/lived experience, and continuous community/maintenance.

For the initial edition run up to five full passes. At least two student-phase passes are required. Stop early only after two consecutive passes find no substantive new question, decision, failure mode, resource, stakeholder need, or external gap. Run external discovery before substantive drafting and again after it. Record every pass in `research/content-audit.md`.

## 11. Public contribution and editorial system

Provide an owner-approved no-GitHub form when its URL is available and five structured GitHub suggestion forms: missing content, correction, source, accessibility or technical problem, and local adaptation. Ordinary readers are not asked to edit files, fork the repository, use a command line or prepare a pull request. The founding editor may use Discussions internally if they reduce administrative work, but Discussions are not required for public intake.

Only Haresh Suppiah can approve implementation. Applying `decision: approved` records that decision and prepares the issue for assignment to an agent or maintainer. The assignee returns a linked pull request for Haresh's review. Approval does not authorise merge or publication.

All routes feed: submission, privacy check, duplicate/coverage check, triage, evidence review, accepted/needs evidence/local adaptation/declined/duplicate, drafting, review, release, and contributor notification.

The public contribution page, issue forms, governance, support policy, contributor credit, privacy warnings, labels, status model, and maintainer close-the-loop duties must satisfy Source Sections 2.11, 4.3, 4.6, 4.7, and 11.1.

## 12. Quarto and reading experience

Build an accessible HTML Quarto book modelled structurally on *R for the Rest of Us*: portrait cover and local full-text search in a roughly 340 px left sidebar, collapsible Parts, roughly 760 px reading column, roughly 250 px sticky right-side `On this page` contents, page-level repository actions, and previous/next navigation.

Use citations, cross-references, responsive navigation, print-friendly resources, descriptive alt text, high contrast, original styling, safe execution defaults, local reproducible build, GitHub Pages deployment, link checking, and a visible contribution route. Mobile must retain access to search, navigation, and page contents.

## 13. Cover and visual identity

Generate three original portrait variants. Use a distressed dark-brown or oxblood manual, cream block `THE HANDBOOK FOR THE`, dusty-pink italic `Recently Enrolled`, exact subtitle and author, divider, and a lower oil-painted vignette of a graduate researcher approaching an uncanny library/archive/institutional threshold.

Generate the illustration without lettering and compose the exact typography deterministically. Do not copy the film prop's figures, exact illustration, typography, logo, layout proportions, or branded details. Produce full cover, sidebar derivative, social image, favicon, and alt text. Haresh selects the permanent cover.

## 14. Repository and governance

Create the public repository `hareshsuppiah/handbook-for-the-recently-enrolled`, main branch, README, Quarto configuration, chapters, stuck system, resources, examples, research registers, planning records, contribution pages, issue forms, workflows, governance, support, contributors, code of conduct, citation metadata, changelog, and separate licence notices.

The raw source remains private and Git-ignored until Haresh approves release. Prose and non-code material use CC BY 4.0; code/configuration/scripts use MIT. Contributor terms must state the applicable inbound licence.

## 15. Release definition

Development is public from the first pushed commit. The first tagged broad beta is `v0.1.0-beta`. It is not ready until the source is preserved, every requirement is represented, all 82 topics have a destination, all 53 resources are tracked, all 36 chapters have meaningful content, priority work satisfies the full contract, the book renders, search and navigation work, sources support claims, high-risk questions include escalation, contribution/privacy processes exist, accessibility and link checks pass, and remaining gaps are explicit.

## 16. Delivery sequence

1. Preserve source and complete planning checkpoint.
2. Initialise the public-ready repository and governance.
3. Run coverage discovery and seed the registers.
4. Research and verify the evidence foundation.
5. Generate cover options and build the visual prototype.
6. Draft the broad beta in four content rounds.
7. Build and test public contribution routes.
8. Render, inspect, audit, fix, and tag the beta.
9. Maintain targeted and periodic review loops.
