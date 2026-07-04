# Phase 6 Result: Debug Derivation Workflow

Date: `2026-06-29`

## Status

`PASS`

## Objective

Implement `debug_derivation(steps)` for "Where does this derivation first
fail?" questions.

## Artifacts

- `src/mathdevmcp/debug_derivation.py`
- `tests/test_debug_derivation.py`

## Implemented Behavior

- Wraps low-level proof-gap localization into Phase 1 envelopes.
- All-valid chains preserve scoped backend proof.
- Counterexample-backed bad transitions are refuted.
- Refuted low-level transitions without counterexample artifacts are not
  promoted to high-level refutation.
- Missing/unsupported transitions become local `gap_found` evidence, not global
  theorem failure.
- Adds a rubric helper for step-index/status scoring.

## Checks

| Check | Result |
| --- | --- |
| `python -m pytest tests/test_debug_derivation.py tests/test_high_level_workflows.py tests/test_high_level_contracts.py tests/test_proof_gap.py` | `32 passed`. |
| `python -m py_compile src/mathdevmcp/debug_derivation.py src/mathdevmcp/high_level_workflows.py src/mathdevmcp/high_level_contracts.py` | Passed. |
| `python -m pytest tests/test_prove_or_refute.py tests/test_math_debugging_router.py` | `12 passed`. |
| `git diff --check` | Passed. |

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Met for all-valid, counterexample-backed refuted, no-counterexample non-promotion, missing-assumption gap, short-chain inconclusive, and rubric cases. |
| Veto diagnostics | Local gaps are not global theorem failures; later steps are not promoted ahead of the first gap. |
| Not concluded | Completeness of whole proof search. |

## Phase 7 Handoff

Proceed to `audit_math_to_code`, preserving structural-only evidence as
diagnostic rather than proof.
