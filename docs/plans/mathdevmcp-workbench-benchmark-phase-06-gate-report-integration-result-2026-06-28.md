# Phase 6 Result: Gate And Report Integration

Date: `2026-06-28`

## Status

`PASSED`

## Objective

Expose the seeded workbench benchmark and Phase 3 quality metrics in benchmark
reports while keeping external adapted packs diagnostic and non-gating.

## Work Completed

- Added `workbench_quality` as a separate quality-evidence field in the full
  benchmark report.
- Added `workbench-benchmark-quality` CLI command.
- Added `workbench_benchmark_quality` MCP facade/server tool.
- Kept the formal CI gate at `56` cases and did not combine external adapted
  packs with seeded totals.
- Added CLI/MCP/report tests for the new quality surface.

## Evidence

| Check | Result |
| --- | --- |
| `PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root .` | `56/56 passed` |
| `PYTHONPATH=src python -m mathdevmcp.cli run-benchmarks --root .` | `56/56`, includes `workbench_quality` |
| `PYTHONPATH=src python -m mathdevmcp.cli workbench-benchmark-quality --root .` | `quality_thresholds_passed` |
| Focused benchmark/MCP/schema/release-packaging tests | `80 passed` |
| Release-caveat tests excluding dirty-worktree public-profile assertion | `16 passed, 1 deselected` |
| CLI benchmark quality/gate smoke subset | `3 passed, 2 deselected` |
| Compile check | passed |
| `git diff --check` | passed |

## Release-Policy Caveat

`tests/test_release_caveat_closure.py::test_public_profile_omits_strict_profile_caveat_noise`
fails in the current dirty worktree because public release readiness reports
`not_ready` under the publication invariant. This is a dirty-worktree release
publication condition, not a regression in benchmark gate/report integration.

## Boundary Notes

- The benchmark gate remains a seeded/local formal gate.
- External adapted packs are absent and non-gating.
- The quality report is separate evidence; it does not claim release readiness,
  external benchmark performance, or broad theorem-proving capability.

## Next Handoff

Proceed to Phase 7: document operator interpretation, CLI/MCP commands,
seeded-vs-external boundaries, and the dirty-worktree release-publication
caveat.
