# Phase 2 Subplan: Backend Route Planner

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Add a deterministic route planner that classifies extracted targets into
candidate backend routes and records what can be attempted, what is unavailable,
and what requires formalization.

## Entry Conditions Inherited From Previous Phase

- Phase 1 target extraction passed.
- Extracted targets include lhs/rhs/provenance and fallback status.
- Existing `derive_or_refute`, route router, and counterexample search remain
  green.

## Required Artifacts

- New module:
  `src/mathdevmcp/backend_route_planner.py`
- New tests:
  `tests/test_backend_route_planner.py`
- Phase 2 result:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-02-backend-route-planner-result-2026-07-06.md`
- Refreshed Phase 3 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_backend_route_planner.py -q`
- `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_derive_or_refute.py -q`
- `python3 -m compileall -q src/mathdevmcp/backend_route_planner.py src/mathdevmcp/derive_or_refute.py`
- `git diff --check -- src/mathdevmcp/backend_route_planner.py tests/test_backend_route_planner.py docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-02-backend-route-planner-result-2026-07-06.md`
- Claude read-only review if planner changes proof/refutation boundary language.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can route planning prefer deterministic backends while preserving non-certifying boundaries? |
| Baseline/comparator | Current implicit router inside `derive_or_refute`. |
| Primary criterion | Planner emits route candidates for symbolic, counterexample, matrix/domain, Lean/formalization, and unavailable-backend cases without proof promotion. |
| Veto diagnostics | Route candidate marked proof without backend certificate; backend absence treated as refutation; missing formalization path; no tool-use record. |
| Explanatory diagnostics | Candidate route count, selected first route, backend availability flags. |
| Not concluded | No parallel route execution yet unless already safe and bounded; no general theorem proving. |
| Artifact | Planner module/tests/result. |

## Forbidden Claims/Actions

- Do not claim route availability proves or refutes a target.
- Do not install Sage/Lean dependencies.
- Do not run network-dependent backend setup.
- Do not hide unavailable backends.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only if:

- route planner schema is stable;
- tests cover scalar proof, matrix counterexample, risky-debt formalization,
  and backend-unavailable cases;
- Phase 3 subplan states how route plans attach to reports.

## Stop Conditions

Stop if:

- planner requires changing low-level proof semantics;
- backend availability checks are environment-dependent without stable
  diagnostic fallback;
- planner encourages unsafe or expensive backend calls.
