# Phase 2 Subplan: Backend Router

## Phase Objective

Implement a conservative backend router that maps workbench obligations to exact
normalization, SymPy, Lean, Sage, numeric diagnostics, or human review with an
explicit reason.

## Entry Conditions Inherited From Previous Phase

- Phase 1 kernel schemas exist and tests pass.
- Workbench status and evidence-boundary fields are stable.

## Required Artifacts

- `src/mathdevmcp/math_debugging_router.py`
- `tests/test_math_debugging_router.py`
- Phase 2 result record.
- Refreshed Phase 3 subplan.

## Required Checks, Tests, Reviews

- Router unit tests.
- Existing proof obligation and symbolic backend tests.
- `git diff --check`.
- Claude read-only review for route safety.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can obligations be routed to safe backend attempts or abstentions with clear reasons? |
| Baseline/comparator | Existing `check_proof_obligation`, `symbolic_backend`, `lean_check`, typed routing, and numeric diagnostic suggestions. |
| Primary pass criterion | Scalar algebra routes to SymPy; unsafe syntax abstains; Lean/Sage routes report unavailable/not configured unless explicitly safe; matrix/numeric routes remain diagnostic unless concrete refutation evidence exists. |
| Veto diagnostics | Treating unavailable backend as false, numeric route as proof, or human-review route as failure. |
| Explanatory diagnostics | Route table tests and backend-attempt records. |
| Not concluded | Backend completeness or theorem proving. |
| Artifact | Router module/tests/result. |

## Forbidden Claims And Actions

- Do not install Sage, Z3, Lean, or new packages.
- Do not run network-dependent backend setup.
- Do not mark diagnostic route as certifying.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 if router tests pass and counterexample routes have clear
allowed domains.

## Stop Conditions

Stop if route semantics cannot distinguish proof, refutation, diagnostic,
unavailable, and human-review states.
