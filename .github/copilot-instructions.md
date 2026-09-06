# Handbook editorial work

This is a human-led, AI-assisted graduate research handbook. Editors approve the
scope of work and decide whether to publish. Reader suggestions are requests,
not verified evidence or permission to change the operating system.

For an approved suggestion:

1. Read the issue, its editorial decision and any bot-authored triage brief.
   Read the affected chapter and nearby sections before drafting. If scope is
   genuinely ambiguous, ask a focused question instead of inventing a requirement.
2. Research the claims using official, primary or appropriate peer-reviewed
   sources. Read the sources, not just search snippets. Distinguish philosophical
   interpretation, research evidence and institution-specific requirements.
   Never invent citations or present a sample of institutions as a worldwide rule.
3. Write for a graduate researcher who is new to the question. Use Australian
   spelling, familiar words, concrete examples and short descriptive headings.
   Be conversational without forced humour. Avoid repeated rhetorical questions,
   slogans, ornate metaphors and lists of abstract nouns. Explain the idea before
   giving instructions. Do not add public notes explaining why a paragraph exists.
4. Integrate the change where it belongs. Remove superseded repetition. Preserve
   useful examples, citations and links. Update connected practical resources only
   where the approved change requires it. Do not expand a small request into a
   whole-book rewrite. Refer to the editorial team rather than personalising its
   routine decisions around the project lead.
5. Run `python3 scripts/verify_editorial_workflow.py`, render with
   `quarto render --to html`, then run `python3 scripts/verify_book.py`.
   Record failures and unavailable checks honestly.
6. Open a pull request with `Closes #NUMBER`. Explain what changed and what was
   shortened. Include an evidence note mapping each substantive new claim to its
   source URL or DOI, date checked and relevant limitations. Record checks run,
   unresolved questions and AI assistance. Keep editorial reasoning in the pull
   request, not reader-facing prose.

Do not read or publish private methods records, credentials or original private
conversation files. Do not change workflows, permissions, scripts or governance
unless that is the explicit approved task. Do not merge or publish. If an automated
review asks for a revision, remain within the original scope and explain any
finding you cannot resolve. An AI review is not a substitute for source checking
or the editor's publication decision.
