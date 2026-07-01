# Phase 4 Subplan: Prove Or Counterexample Workflow

## Phase Objective

Implement `prove_or_counterexample(claim)` for "Can we prove X?" questions.

## Entry Conditions Inherited From Previous Phase

- Contract, kernel, and `derive_from` workflow exist.
- Low-level `prove_or_refute` behavior is available.

## Required Artifacts

- `prove_or_counterexample` function.
- Tests for proof, counterexample/refutation, backend unavailable, not
  encodable, diagnostic-only evidence, and phase-local false-confidence traps.
- Phase 4 result record.
- Refreshed Phase 5 subplan.

## Required Checks, Tests, Reviews

- Workflow tests.
- Contract/kernel tests.
- Low-level `prove_or_refute` tests if impacted.
- `python3 -m py_compile`.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the workflow produce proof/refutation/counterexample outcomes without confusing backend failure with math failure? |
| Baseline/comparator | Direct `prove_or_refute` outputs. |
| Primary pass criterion | Backend proof/refutation is preserved; backend unavailable and not-encodable are non-claims; local negative controls catch backend-unavailable-to-refutation promotion. |
| Veto diagnostics | Backend unavailable treated as refutation; Lean/Sage absence treated as product failure; diagnostic evidence treated as certificate. |
| Explanatory diagnostics | Backend route, nested evidence, counterexample if any. |
| Not concluded | Completeness of proof search. |
| Artifact | Function/tests/result. |

## Forbidden Claims And Actions

- Do not claim failure to prove is disproof unless a refutation/counterexample
  exists.
- Do not require optional external backends to pass seeded tests.
- Do not expose CLI/MCP yet.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 if proof/refutation and backend-boundary cases are stable.

## Stop Conditions

Stop if backend status cannot be represented without overclaiming.
