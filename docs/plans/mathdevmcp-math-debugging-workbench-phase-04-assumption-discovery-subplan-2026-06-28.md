# Phase 4 Subplan: Assumption Discovery

## Phase Objective

Implement `assumptions_required` diagnostics that identify route-required or
sufficient assumptions for divisions, inverses, logdet/determinant, square roots,
differentiation, shape, rank, positivity, and support restrictions.

## Entry Conditions Inherited From Previous Phase

- Kernel and router exist.
- Counterexample records exist for obvious violations where applicable.

## Required Artifacts

- `src/mathdevmcp/assumption_discovery.py`
- `tests/test_assumption_discovery.py`
- CLI/MCP exposure if stable.
- Phase 4 result record.
- Refreshed Phase 5 subplan.

## Required Checks, Tests, Reviews

- Tests for division by nonzero, inverse invertibility, logdet SPD/square
  requirements, sqrt nonnegativity, matrix shape constraints.
- Existing assumption and shape diagnostic tests.
- `git diff --check`.
- Claude review for necessary-vs-sufficient language.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the workbench report assumptions needed by a proof route without overclaiming necessity? |
| Baseline/comparator | Existing typed/shape diagnostics and assumption manifest support. |
| Primary pass criterion | Diagnostics distinguish `required_by_route`, `sufficient`, `missing`, `provided`, and `unknown_necessity`. |
| Veto diagnostics | Claiming an assumption is mathematically necessary without proof; hiding missing assumptions. |
| Explanatory diagnostics | Assumption table and source operation. |
| Not concluded | Minimality or necessity of assumptions unless separately certified. |
| Artifact | Assumption discovery module/tests/result. |

## Forbidden Claims And Actions

- Do not claim minimal assumption sets by default.
- Do not silently accept contradictory assumptions.
- Do not promote domain heuristics to proof.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 if assumption diagnostics can be attached to derive/refute
results.

## Stop Conditions

Stop if assumption statuses remain ambiguous or tests cannot prevent necessity
overclaims.
