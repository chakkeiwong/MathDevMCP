# Phase 6 Subplan: Debug Derivation Workflow

## Phase Objective

Implement `debug_derivation(steps)` for "Where does this derivation first
fail?" questions.

## Entry Conditions Inherited From Previous Phase

- Contract, kernel, and assumption/proof workflows exist.
- Low-level proof-gap localization is available.

## Required Artifacts

- `debug_derivation` function.
- Tests for first bad step, all-valid simple chain, not-encodable/inconclusive
  step, and backend-unavailable boundary.
- Rubric/set-based tests for acceptable failing-transition localization.
- Phase 6 result record.
- Refreshed Phase 7 subplan.

## Required Checks, Tests, Reviews

- Workflow tests.
- Contract/kernel tests.
- Low-level proof-gap tests if impacted.
- `python3 -m py_compile`.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the workflow identify the first unsupported/refuted step without overclaiming global theorem failure? |
| Baseline/comparator | Direct `localize_proof_gap` outputs. |
| Primary pass criterion | First bad transition is localized and reported with nested evidence; all-valid chains do not produce false failures; acceptable decompositions are scored by step-index/evidence criteria. |
| Veto diagnostics | Later failures reported before first failure; local gap treated as global theorem refutation; unsupported syntax hidden. |
| Explanatory diagnostics | Step index, previous step, failing step, low-level evidence. |
| Not concluded | Completeness of whole proof search. |
| Artifact | Function/tests/result. |

## Forbidden Claims And Actions

- Do not rewrite proof chains silently.
- Do not treat a local bad step as a claim about unrelated theorem variants.
- Do not expose CLI/MCP yet.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 7 if first-gap localization is stable and boundary preserving.

## Stop Conditions

Stop if first-gap evidence cannot be represented deterministically.
