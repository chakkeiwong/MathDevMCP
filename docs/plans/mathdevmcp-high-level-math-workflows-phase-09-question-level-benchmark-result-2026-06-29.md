# Phase 9 Result: Question-Level Benchmark

Date: `2026-06-29`

## Result

`PASS`

## Phase Objective

Add a seeded question-level benchmark for all high-level workflows, including
quality metrics and false-confidence mutation checks.

## Entry Conditions Verified

- Phase 8 high-level workflow implementations and focused tests had passed.
- Existing benchmark gate and workbench quality infrastructure were available.
- Phase 10 CLI/MCP exposure remained gated on this phase result.

## Skeptical Plan Audit

- Baseline/comparator was the existing low-level benchmark/workbench quality
  infrastructure plus focused high-level workflow tests.
- Pass rate was not treated as the sole quality measure; seeded coverage,
  negative controls, deterministic rerun, and mutation probes were required.
- Benchmark outputs used the same `high_level_workflow_result` contract that
  Phase 10 would expose.
- Public-release hypothesis state was not used as a promotion or veto criterion
  for high-level workflow benchmark quality.

## Artifacts

- `src/mathdevmcp/benchmarks.py`
- `tests/test_context_and_fixtures.py`

Implemented benchmark/report artifacts:

- Category: `high_level_math_workflows`
- Runner: `run_high_level_math_workflow_benchmark`
- Quality report: `build_high_level_workflow_quality_report`
- Integrated gate/report fields in `build_benchmark_report` and
  `benchmark_gate_report`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Do the high-level workflows answer realistic question-level cases while resisting false-confidence regressions? |
| Primary criterion | Passed. The benchmark has seeded cases for all six workflows, quality thresholds, deterministic rerun, and mutation probes. |
| Veto diagnostics | Passed. Diagnostic/structural/review-packet evidence is not promoted to proof; backend unavailable is not treated as refutation. |
| Explanatory diagnostics | Category/focus summaries, high-level quality report, negative-control rate, and mutation results were recorded. |
| Not concluded | External benchmark validity, release readiness, scientific validity, and broad theorem-proving ability. |

## Checks Run

- `python -m pytest tests/test_context_and_fixtures.py tests/test_mcp_facade.py::test_call_mcp_tool_run_benchmarks_aggregates_results tests/test_mcp_facade.py::test_call_mcp_tool_benchmark_gate_returns_ci_shape tests/test_release_smoke.py::test_cli_benchmark_gate_module_command_passes tests/test_release_smoke.py::test_cli_workbench_benchmark_quality_module_command_passes`
  - Result: `38 passed`
- `python -m mathdevmcp.cli benchmark-gate --root .`
  - Result: passed `70/70`
- `python -m mathdevmcp.cli workbench-benchmark-quality --root .`
  - Result: passed
- `git diff --check`
  - Result: passed

## Quality Evidence

- High-level benchmark cases: `14`
- High-level workflows covered: `6`
- Negative controls: `12`
- Negative-control rate: `0.8571428571428571`
- Deterministic rerun: stable
- Mutation probes: all passed
- Benchmark gate: `70/70`

## Known Non-Blocking Caveat

The broader release smoke slice had a known public-release hypothesis failure:

- `tests/test_release_smoke.py::test_release_hypotheses_script_public_mode_passes`

This was already documented in Phase 0 as a dirty/public-release hypothesis
caveat. It is not a high-level workflow benchmark blocker and was not used to
claim release readiness.

## Decision

Proceed to Phase 10. Public CLI/MCP exposure is allowed only for the six
benchmarked high-level workflows and the high-level quality report.

## Refreshed Phase 10 Subplan Review

Phase 10 remains consistent with this result:

- Entry condition is satisfied by the passing question-level benchmark and
  stable high-level contract.
- Required artifacts cover CLI, MCP facade/server, tests, result, and next
  subplan review.
- Boundary safety requires preserving non-claims and exposing no unbenchmarked
  workflows.
- Stop condition remains correct: stop if public surfaces cannot preserve
  non-claims or evidence classes.
