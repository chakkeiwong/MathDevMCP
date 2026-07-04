# Phase 4 Result: Derive-From Route Plans

Date: 2026-07-02

Status: `PASSED_AFTER_REPAIR`

## Phase Objective

Make `derive_from` return route plans with givens, assumptions, backend route
status, proof obligations, and route gaps instead of only packaging low-level
results.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | `derive_from` can expose useful derivation route artifacts without inventing unsupported steps. |
| Baseline/comparator | Existing `derive_from` behavior and benchmark cases RLHLB-04/RLHLB-09. |
| Primary criterion | Passed after repair locally: results distinguish context givens, explicit assumptions, backend route status, obligations, route gaps, and existing proof/refutation evidence, with route plans segregated into diagnostic evidence items. |
| Veto diagnostics | No unchecked derivation chain, no silent givens-to-assumptions promotion, no route gap reported as proof. |
| Explanatory diagnostics | Route plan, obligation list, assumption ledger, route gaps. |
| Not concluded | No general derivation capability, no scientific validation, no proof beyond scoped evidence. |

## Artifacts

- `src/mathdevmcp/derive_from.py`
- `tests/test_derive_from.py`
- Refreshed Phase 5 subplan:
  `docs/plans/mathdevmcp-tool-improvement-phase-05-math-code-trace-subplan-2026-07-02.md`

## Local Checks

| Check | Result |
| --- | --- |
| `python3 -m pytest tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py tests/test_high_level_contracts.py tests/test_high_level_workflows.py` | Passed after review repair: 44 tests. |
| `python3 -m pytest tests/test_derive_or_refute.py tests/test_prove_or_refute.py tests/test_debug_derivation.py` | Passed: 22 tests. |
| `git diff --check` over touched Phase 4 implementation/tests/docs | Passed. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 5 | Passed after review repair | No veto triggered | Route plan is explanatory and depends on existing low-level route quality | Add math-to-code trace artifacts | No unchecked derivation or general proof claim |

## Phase 5 Handoff

Phase 5 may embed derivation route plans in review context only from the
separate diagnostic `review_packet` evidence item, not from certifying
proof/refutation evidence. Math-to-code trace artifacts must remain structural
diagnostics rather than proof that code implements documented math.
