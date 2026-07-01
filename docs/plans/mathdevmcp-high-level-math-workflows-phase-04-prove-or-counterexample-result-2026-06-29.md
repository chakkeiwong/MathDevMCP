# Phase 4 Result: Prove Or Counterexample Workflow

Date: `2026-06-29`

## Status

`PASS`

## Objective

Implement `prove_or_counterexample(claim)` for scoped "Can we prove X?"
questions.

## Artifacts

- `src/mathdevmcp/prove_or_counterexample.py`
- `tests/test_prove_or_counterexample.py`

## Implemented Behavior

- Packages low-level proof evidence as scoped backend-certified `proved`.
- Packages refutation as `refuted` only when a counterexample artifact is
  present.
- Downgrades backend refutation without a counterexample artifact to
  `inconclusive`.
- Preserves backend-unavailable and not-encodable outcomes as non-claims.
- Handles malformed claims as `not_encodable`, not false.

## Checks

| Check | Result |
| --- | --- |
| `python -m pytest tests/test_prove_or_counterexample.py tests/test_derive_from.py tests/test_high_level_workflows.py tests/test_high_level_contracts.py` | `33 passed`. |
| `python -m py_compile src/mathdevmcp/prove_or_counterexample.py src/mathdevmcp/derive_from.py src/mathdevmcp/high_level_workflows.py src/mathdevmcp/high_level_contracts.py` | Passed. |
| `python -m pytest tests/test_prove_or_refute.py tests/test_counterexample_search.py tests/test_math_debugging_router.py` | `16 passed`. |
| `git diff --check` | Passed. |

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Met for backend proof, counterexample-backed refutation, backend/not-encodable non-claims, and false-confidence trap for refutation without counterexample. |
| Veto diagnostics | Failure to prove is not treated as disproof; backend/encoding absence is not treated as math failure. |
| Not concluded | Completeness of proof search. |

## Phase 5 Handoff

Proceed to `assumptions_for`, preserving route-required/not-minimal assumption
semantics and set/rubric-style tests.
