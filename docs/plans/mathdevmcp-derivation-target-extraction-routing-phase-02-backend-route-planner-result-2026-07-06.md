# Phase 2 Result: Backend Route Planner

Date: 2026-07-06

Status: `PASSED`

## Objective

Add a deterministic route planner that classifies extracted targets into
candidate backend routes and records what can be attempted, what is unavailable,
and what requires formalization.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can route planning prefer deterministic backends while preserving non-certifying boundaries? |
| Baseline/comparator | Current implicit router inside `derive_or_refute`. |
| Primary criterion | Passed: planner emits symbolic, counterexample, Sage/matrix-domain, and Lean/formalization candidates without proof promotion. |
| Veto diagnostics | Passed: no route candidate is marked as proof; backend absence is diagnostic; formalization path is explicit; every candidate names a tool and evidence contract. |
| Explanatory diagnostics | Planner records candidate count, ready/available count, unavailable count, and formalization count. |
| Not concluded | No route is executed by this planner; no theorem proving or parallel execution is introduced. |
| Artifact | `src/mathdevmcp/backend_route_planner.py`, `tests/test_backend_route_planner.py`. |

## Implementation Summary

- Added `plan_backend_routes`, a non-certifying route-plan packet for direct
  targets or extracted target dictionaries.
- Added route candidates for:
  - `sympy:symbolic_identity` via `derive_or_refute`;
  - `bounded_counterexample:counterexample_search` via `find_counterexample`;
  - `sage:matrix_domain_symbolic` via `derive_or_refute`;
  - `lean:formal_proof` via `lean_check`.
- Attached each route candidate to an evidence contract and expected artifact.
- Added `route_plan_not_certificate` non-claim and a shared boundary string.
- Used injected capability dictionaries in tests so Lean/Sage availability does
  not make tests environment-dependent.

## Repair During Phase

The first route-planner test run found that `A*B = B*A` was selected for scalar
SymPy because the scalar grammar permitted uppercase identifiers. The planner
was patched so matrix/domain hints veto scalar symbolic routing and prefer the
bounded counterexample candidate. This matches the existing low-level router's
conservative discipline.

## Checks Run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_backend_route_planner.py -q` | Passed: 4 passed after the scalar-routing repair. |
| `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_derive_or_refute.py -q` | Passed: 13 passed. |
| `python3 -m compileall -q src/mathdevmcp/backend_route_planner.py src/mathdevmcp/derive_or_refute.py` | Passed. |

## Boundary

Route planning does not execute the route. It does not prove, refute, repair, or
edit any source. Proof/refutation promotion still requires downstream scoped
backend evidence or a concrete counterexample artifact.

## Next-Phase Handoff

Proceed to Phase 3 because:

- route planner schema is stable enough for report integration;
- tests cover scalar proof-route planning, matrix counterexample planning,
  risky-debt formalization planning, and backend-unavailable diagnostics;
- Phase 3 subplan states that route plans attach to reports without changing
  proof/refutation boundaries.
