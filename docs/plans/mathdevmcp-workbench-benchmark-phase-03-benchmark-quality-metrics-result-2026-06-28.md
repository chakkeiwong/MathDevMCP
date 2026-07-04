# Phase 3 Result: Benchmark Quality Metrics

Date: `2026-06-28`

## Status

`PASSED`

## Objective

Add benchmark-quality metrics for the actual seeded workbench benchmark so the
suite measures false-confidence resistance and not pass rate alone.

## Work Completed

- Added an explicit expected seeded workbench tool set.
- Extended the quality report to consume actual seeded cases and actual seeded
  runner results.
- Added exact threshold reporting for tool coverage, oracle coverage,
  negative-control rate, boundary checks, result/case alignment, deterministic
  rerun stability, mutation sensitivity, and run-manifest completeness.
- Added an in-memory fixed mutation panel for proof-promotion failures without
  editing repo files.
- Added focused tests for actual seeded quality reporting, determinism drift,
  case/result misalignment, and explicit tool-set coverage.

## Quality Evidence

| Threshold | Result |
| --- | --- |
| Tool coverage | `11/11`, passed |
| Required oracle coverage | `9/9`, passed |
| Negative-control rate | `14/15 = 0.9333333333333333`, passed |
| Boundary checks | `15/15`, passed |
| Case/result alignment | `15/15`, passed |
| Deterministic rerun | two immediate runs stable, passed |
| Fixed mutation family | `4/4`, passed |
| Run manifest | `9/9` required fields, passed |

Mutation probes detected:

- `backend_unavailable_to_refuted`;
- `structural_only_to_proved`;
- `numeric_supported_to_backend_proved`;
- `missing_assumptions_to_proved`.

## Checks

| Check | Result |
| --- | --- |
| `PYTHONPATH=src python -m pytest -q tests/test_workbench_benchmark_schema.py tests/test_context_and_fixtures.py` | `39 passed` |
| `PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root .` | `56/56 passed` |
| `python3 -m py_compile src/mathdevmcp/benchmarks.py src/mathdevmcp/workbench_benchmark_schema.py` | passed |
| `git diff --check` | passed |

## Claude Review

- Round 1 returned `VERDICT: REVISE`.
- Fixed issues by adding exact thresholds/denominators, explicit mutation
  diagnostic limits, manifest/backend-matrix requirement, and broader handoff
  failure handling.
- Round 2 compact prompts hung after a successful tiny `OK` probe, so the
  reviewer was recorded as unavailable for the repaired re-review. Local
  skeptical audit passed after the repairs.

## Boundary Notes

- The fixed mutation family is a diagnostic panel, not a complete adversarial
  benchmark.
- Seeded benchmark quality does not establish external validity.
- This report does not claim broad theorem-proving ability, release readiness,
  or scientific validity.

## Next Handoff

Proceed to Phase 4: create the external source provenance protocol without
fetching, redistributing, or gating external benchmark data.
