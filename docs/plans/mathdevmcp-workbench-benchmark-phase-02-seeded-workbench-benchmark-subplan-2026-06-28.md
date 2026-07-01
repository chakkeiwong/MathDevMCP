# Phase 2 Subplan: Seeded Workbench Benchmark

## Phase Objective

Add deterministic local benchmark cases for the newly implemented workbench
functions and integrate the category into the formal benchmark report.

## Entry Conditions Inherited From Previous Phase

- Case schema and quality rubric exist.
- Current benchmark baseline and dirty-worktree boundaries are recorded.

## Required Artifacts

- `math_debugging_workbench` benchmark category in `src/mathdevmcp/benchmarks.py`.
- Seeded cases for all new workbench functions.
- Required seeded negative-control cases for hidden assumptions, notation
  conflicts, backend unavailable, structural-only evidence, numeric evidence,
  generated tests, review packets, impact missing links, and theorem
  applicability gaps/conflicts.
- Updated benchmark expected totals/summaries in tests.
- Phase 2 result record.
- Refreshed Phase 3 subplan.

## Required Checks, Tests, Reviews

- New benchmark category test.
- `tests/test_context_and_fixtures.py`
- `tests/test_mcp_facade.py` benchmark report expectations.
- Focused workbench tests as needed.
- `benchmark-gate --root .`
- `python3 -m py_compile src/mathdevmcp/benchmarks.py`
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the formal benchmark gate include deterministic cases for each new workbench tool? |
| Baseline/comparator | Existing `41/41` benchmark gate and `84` focused workbench tests. |
| Primary pass criterion | Benchmark total increases by the expected seeded case count and every seeded case passes with explicit oracle-class and boundary quality checks. |
| Veto diagnostics | Seeded cases accept proof-boundary violations; hard/optional external cases enter gated suite prematurely. |
| Explanatory diagnostics | Category/focus summary and per-case quality checks. |
| Not concluded | External benchmark validity or broad theorem-proving ability. |
| Artifact | Benchmark code/tests/result. |

## Forbidden Claims And Actions

- Do not add external borrowed cases in this phase.
- Do not mark diagnostic evidence as proof to make benchmark pass.
- Do not omit mandatory negative controls to keep the benchmark easy.
- Do not silently update expected totals without explaining case count changes.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 if seeded benchmark cases pass, include mandatory negative
controls, and expose enough quality signals for mutation/false-confidence
checks.

## Stop Conditions

Stop if any new benchmark case needs unavailable network/backend state or if
quality checks cannot catch expected false-confidence regressions.
