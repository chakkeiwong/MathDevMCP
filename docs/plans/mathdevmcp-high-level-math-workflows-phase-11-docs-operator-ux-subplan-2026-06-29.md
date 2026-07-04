# Phase 11 Subplan: Docs And Operator UX

## Phase Objective

Document the high-level workflows, usage examples, benchmark interpretation,
and evidence boundaries.

## Entry Conditions Inherited From Previous Phase

- CLI/MCP surfaces exist and pass tests.
- Question-level benchmark status is known.

## Required Artifacts

- README/operator-guide docs updates.
- CLI examples for all high-level workflows.
- Benchmark interpretation notes.
- Phase 11 result record.
- Refreshed Phase 12 subplan.

## Required Checks, Tests, Reviews

- Docs forbidden-claim grep.
- CLI help/command smoke for documented commands.
- `git diff --check`.
- Claude review for docs overclaim risk.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can operators understand how to use the high-level workflows and interpret evidence safely? |
| Baseline/comparator | Current README/operator guide and workbench benchmark docs. |
| Primary pass criterion | Docs show commands, explain statuses/evidence classes, and state non-claims for proof/release/external validity. |
| Veto diagnostics | Docs imply general theorem proving, release readiness, leaderboard performance, or silent assumption insertion. |
| Explanatory diagnostics | Grep hits and command smoke outputs. |
| Not concluded | External pack promotion or release readiness. |
| Artifact | Docs/result. |

## Forbidden Claims And Actions

- Do not present high-level workflows as a general theorem prover.
- Do not hide backend-unavailable or diagnostic-only boundaries.
- Do not imply benchmark pass equals release readiness.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 12 if docs pass forbidden-claim review and commands are
discoverable.

## Stop Conditions

Stop if docs cannot describe workflows without overclaiming.
