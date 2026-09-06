# Operating the editorial assistants

Readers use the issue form. Triage proposes scope and evidence work; it does not
grant approval. The authorised editor comments `/approve` to assign Copilot.
The draft-review workflow can request at most two revisions before returning the
decision to the editor. No workflow calls a merge or publication endpoint.

## Credentials

`COPILOT_USER_TOKEN` remains the private issue-assignment and revision-comment
credential. The CLI also needs the account permission **Copilot Requests** and
available Copilot access. A separate `COPILOT_AGENT_TOKEN` can supply that CLI
permission; otherwise the runner tries `COPILOT_USER_TOKEN`. Never put either
value in source, issues, prompts or logs.

Run **Editorial triage and draft review → Run workflow** to test authentication
and structured output without modifying a suggestion. Assignment succeeding does
not prove the CLI permission is present. See the official
[CLI authentication guide](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli).

## Limits and review

- Three triage responses per suggestion and twelve workflow runs per UTC day.
  Skipped runs count towards the daily limit conservatively.
- Two automatic revision requests per pull request, with commit-specific records.
- Oversized requests or diffs, non-text changes, protected files and missing
  approvals stop automation or return work to an editor.
- Only trusted default-branch code runs with credentials. PR files are read as
  diff data, never checked out or executed by this privileged workflow.
- The CLI has no tools or repository custom instructions in its temporary work
  directory. Its output must match a schema before trusted code can post it.
- AI review examines the supplied diff and evidence note. It is not independent
  verification of the underlying sources. Rendering runs separately, without
  repository write permissions, in the pull-request quality workflow.

The authorised account remains `hareshsuppiah`. Adding editors requires deliberate
changes to the account allowlists and GitHub permissions; prose does not grant
access. Main-branch protection must be configured separately if enforcement
against direct human pushes is required. No dashboard connection is implied by
these GitHub workflows.
