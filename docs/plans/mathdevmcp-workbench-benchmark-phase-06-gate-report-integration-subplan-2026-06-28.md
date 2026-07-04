# Phase 6 Subplan: Gate And Report Integration

## Phase Objective

Integrate seeded workbench benchmark and quality metrics into benchmark reports
only if Phase 3 seeded-gate thresholds pass, while keeping external adapted
packs diagnostic unless explicitly promoted.

## Entry Conditions Inherited From Previous Phase

- Seeded benchmark is implemented and quality-scored with all Phase 3
  seeded-gate thresholds passing.
- External pack ingestion either produced diagnostic packs or a blocker record.

## Required Artifacts

- Updated benchmark report/gate output and docs if needed.
- Optional diagnostic external-pack report entry that is non-gating.
- Tests for gate totals, summaries, and diagnostic/non-gating separation.
- Phase 6 result record.
- Refreshed Phase 7 subplan.

## Required Checks, Tests, Reviews

- `benchmark-gate --root .`
- `run-benchmarks --root .`
- Benchmark summary tests.
- MCP benchmark facade tests.
- Release-policy tests affected by benchmark totals.
- `git diff --check`.
- Claude review for gate/promotion boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can reports expose the new benchmark evidence without promoting diagnostic external packs? |
| Baseline/comparator | Existing benchmark gate/report contracts. |
| Primary pass criterion | Seeded workbench category is reflected in formal totals only after threshold evidence; diagnostic external packs are reported separately by source/oracle class or explicitly non-gating. |
| Veto diagnostics | External diagnostic failures fail release gate; benchmark total mismatch hidden; report claims release readiness from benchmark addition; Phase 3 threshold failure is bypassed. |
| Explanatory diagnostics | Gate/report JSON and summary diffs. |
| Not concluded | Release readiness or external benchmark performance. |
| Artifact | Report/gate integration tests/result. |

## Forbidden Claims And Actions

- Do not change benchmark policy after seeing failures.
- Do not promote external cases to gated status without Phase 3 quality metrics
  and Phase 4 provenance satisfaction.
- Do not claim release readiness.
- Do not report an aggregate external score across heterogeneous source
  families.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 7 if operator-facing docs can accurately describe seeded vs
diagnostic external benchmark evidence.

## Stop Conditions

Stop if Phase 3 seeded-gate thresholds are not satisfied, if benchmark totals
are inconsistent across CLI/MCP/tests, or if diagnostic external packs cannot be
separated from gate policy.
