# Phase 5 Subplan: Assumptions For Workflow

## Phase Objective

Implement `assumptions_for(target)` for "What assumptions are required for X?"
questions.

## Entry Conditions Inherited From Previous Phase

- Contract, kernel, and proof/derive workflows exist.
- Low-level assumption discovery is available.

## Required Artifacts

- `assumptions_for` function.
- Tests for logdet, inverse/division, theorem applicability gap/conflict, and
  no-silent-assumption behavior.
- Set/rubric-based scoring tests for acceptable assumption sets.
- Phase 5 result record.
- Refreshed Phase 6 subplan.

## Required Checks, Tests, Reviews

- Workflow tests.
- Contract/kernel tests.
- Low-level assumption discovery tests if impacted.
- `python3 -m py_compile`.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the workflow make required assumptions explicit and traceable? |
| Baseline/comparator | Direct `assumptions_required` and literature/local audit outputs. |
| Primary pass criterion | Known assumption needs are listed with reasons and affected terms; conflicts remain conflicts; acceptable assumption sets are scored by set/rubric criteria rather than a brittle single string. |
| Veto diagnostics | Assumptions silently inserted as proof conditions; conflicts hidden; assumptions reported without traceable reason. |
| Explanatory diagnostics | Required assumptions, affected terms, source low-level evidence. |
| Not concluded | Sufficiency of assumptions for all mathematical settings. |
| Artifact | Function/tests/result. |

## Forbidden Claims And Actions

- Do not claim the returned assumptions are minimal unless proved.
- Do not retry and promote a proof under assumptions silently.
- Do not expose CLI/MCP yet.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 if missing assumptions and conflicts are explicit in the
high-level contract.

## Stop Conditions

Stop if the workflow cannot distinguish missing assumptions from proof.
