#!/usr/bin/env python3
"""Static regression checks for the GitHub editorial approval workflow."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "approved-suggestion.yml"
text = WORKFLOW.read_text(encoding="utf-8")
failures: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        failures.append(message)


def step(name: str) -> str:
    match = re.search(
        rf"(?ms)^      - name: {re.escape(name)}\n(.*?)(?=^      - name:|^  [A-Za-z0-9_-]+:|\Z)",
        text,
    )
    require(match is not None, f"missing workflow step: {name}")
    return match.group(1) if match else ""


require("issues:\n    types: [labeled]" in text, "manual approval labels must trigger the workflow")
require("issue_comment:\n    types: [created]" in text, "owner approval comments must trigger the workflow")
require("github.event.comment.body == '/approve'" in text, "the exact /approve command must be recognised")
require(
    "group: editorial-decision-${{ github.repository_id }}-${{ github.event.issue.number }}" in text,
    "approval runs must be serialised per issue",
)
require("cancel-in-progress: false" in text, "a later command must not cancel an active decision run")

state = step("Inspect existing handoff state")
require("id: issue_state" in state, "the existing issue state must be exposed to later steps")
for marker in (
    "handbook-agent-handoff",
    "handbook-missing-copilot-token",
    "work: in-progress",
    "work: owner-review",
    "work: released",
    "copilot-swe-agent[bot]",
):
    require(marker in state, f"state inspection must check {marker}")

label = step("Record approval label from owner command")
require("github.event_name == 'issue_comment'" in label, "/approve must record the approval label")

same_run_steps = {
    "Mark the issue as agent-ready": "steps.issue_state.outputs.work_started",
    "Record the agent handoff": "steps.issue_state.outputs.handoff_exists",
    "Assign the approved issue to GitHub Copilot": "steps.issue_state.outputs.work_started",
    "Record a missing Copilot credential": "steps.issue_state.outputs.missing_token_notice_exists",
}
for name, guard in same_run_steps.items():
    block = step(name)
    require("github.event_name == 'issues'" not in block, f"{name} must also run for /approve comments")
    require(guard in block, f"{name} must use its idempotency guard")

handoff = step("Record the agent handoff")
require("<!-- handbook-agent-handoff -->" in handoff, "handoff comments need a durable duplicate marker")

assignment = step("Assign the approved issue to GitHub Copilot")
require("id: assign_copilot" in assignment, "Copilot assignment needs a step id for failure handling")
require("<!-- handbook-copilot-assigned -->" in assignment, "assignment comments need a durable marker")

failure = step("Record a failed Copilot handoff")
require(
    "steps.assign_copilot.outcome == 'failure'" in failure,
    "the failure notice must only describe a failed Copilot assignment",
)

if failures:
    print("VERIFY EDITORIAL WORKFLOW: FAIL")
    for failure_message in failures:
        print(f"- {failure_message}")
    raise SystemExit(1)

print("VERIFY EDITORIAL WORKFLOW: PASS")
print("approval routes=/approve,manual-label duplicate-guards=handoff,assignment,missing-token")
