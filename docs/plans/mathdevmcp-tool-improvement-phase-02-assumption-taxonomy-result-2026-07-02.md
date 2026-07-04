# Phase 2 Result: Assumption Route Taxonomy

Date: 2026-07-02

Status: `PASSED_AFTER_REPAIR`

## Phase Objective

Upgrade assumption discovery from keyword-style output toward route-specific
assumption ledgers for scoped generic operator fixtures. The broader
likelihood, score, neural-solver, and affine-recursion route families remain
future extensions unless separately covered by scoped oracles.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | MathDevMCP can report route-required assumptions in reusable typed categories for scoped generic operator fixtures. |
| Baseline/comparator | Existing `assumptions_for` behavior, Phase 1 evidence ledger, and repaired benchmark cases RLHLB-02, RLHLB-05, RLHLB-09. |
| Primary criterion | Passed after repair: assumption outputs match the predeclared scoped taxonomy oracle for route categories, provided route assumptions remain non-proof diagnostics, and non-minimality boundaries are preserved. |
| Veto diagnostics | No global minimality claim, no benchmark-score mutation, and no route category promoted to proof or semantic sufficiency. |
| Explanatory diagnostics | Scoped oracle tests, high-level ledger propagation tests, and workflow wrapper regression tests. |
| Not concluded | No proof of sufficiency unless separately established; no general semantic correctness; no scientific validation. |

## Artifacts

- `src/mathdevmcp/assumption_discovery.py`
- `src/mathdevmcp/math_debugging.py`
- `src/mathdevmcp/high_level_contracts.py`
- `tests/test_assumption_discovery.py`
- `tests/test_assumptions_for.py`
- Refreshed Phase 3 subplan:
  `docs/plans/mathdevmcp-tool-improvement-phase-03-proof-counterexample-evidence-subplan-2026-07-02.md`

## Local Checks

| Check | Result |
| --- | --- |
| `python3 -m pytest tests/test_assumption_discovery.py tests/test_assumptions_for.py tests/test_high_level_workflows.py tests/test_high_level_contracts.py` | Passed: 35 tests. |
| `python3 -m pytest tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py` | Passed: 27 tests. |
| `git diff --check` over touched Phase 2 implementation/tests/docs | Passed. |

## Scoped Taxonomy Oracle

The oracle is local to tests and currently covers:

- `x / y`: denominator nonzero maps to `domain_condition`.
- `logdet(A) + inv(A)`: invertibility maps to `domain_condition` and
  `shape_condition`; logdet domain maps to `covariance_condition` and
  `domain_condition`.
- `sqrt(x) + grad(f) + trace(A)`: square-root domain maps to
  `domain_condition`; differentiability maps to `smoothness_condition`;
  trace conformability maps to `shape_condition`.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 3 | Passed after review repair | No veto triggered | Taxonomy remains a scoped oracle, not a semantic authority | Strengthen proof/counterexample evidence surfaces | No global minimality, sufficiency, or proof claim |

## Phase 3 Handoff

Phase 3 may display scoped route-category assumption metadata, but proof and
refutation must still be governed by backend certificates, concrete
counterexamples, or contract-valid scoped contradictions. Route categories are
not proof evidence.
