# Phase 9 Subplan: Question-Level Benchmark

## Phase Objective

Add a seeded question-level benchmark for all high-level workflows, including
quality metrics and false-confidence mutation checks.

## Entry Conditions Inherited From Previous Phase

- All high-level workflows exist and pass focused tests.
- Existing workbench benchmark/quality infrastructure exists.

## Required Artifacts

- `high_level_math_workflows` benchmark category or equivalent report section.
- At least two seeded cases per high-level function.
- Per-workflow baseline ladder covering refusal/insufficient-evidence,
  structural-only or diagnostic-only evidence, backend-certified positive cases
  where applicable, and backend-unavailable/non-claim cases where applicable.
- Quality report or threshold section for high-level workflows.
- Mutation/negative-control tests.
- Phase 9 result record.
- Refreshed Phase 10 subplan.

## Required Checks, Tests, Reviews

- Benchmark runner tests.
- Quality metric tests.
- Deterministic rerun check.
- Mutation-probe tests without editing repo files.
- `benchmark-gate --root .` if category is integrated.
- `git diff --check`.
- Claude review for benchmark quality/promotion boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the high-level workflows answer realistic question-level cases while resisting false-confidence regressions? |
| Baseline/comparator | Existing low-level workbench benchmark and direct workflow tests. |
| Primary pass criterion | Every workflow has seeded question cases and a baseline ladder; negative-control rate >=40%; deterministic rerun stable; mutation family detects proof-boundary promotions; outputs use the same schema that Phase 10 will expose. |
| Veto diagnostics | Pass rate used as sole quality measure; benchmark omits negative controls; diagnostic evidence promoted to proof; benchmark integrated before quality thresholds pass. |
| Explanatory diagnostics | Category/focus summaries, quality report, mutation results. |
| Not concluded | External benchmark validity or broad theorem-proving ability. |
| Artifact | Benchmark code/tests/result. |

## Forbidden Claims And Actions

- Do not add external borrowed cases in this phase.
- Do not weaken expected statuses after seeing failures.
- Do not make CLI/MCP exposure depend on unreviewed benchmark output.
- Do not score `assumptions_for`, `debug_derivation`, or
  `prepare_review_packet` with brittle single-string gold answers where
  set/rubric scoring is required.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 10 only if question-level benchmark and quality thresholds
pass.

## Stop Conditions

Stop if the benchmark cannot distinguish correct scoped answers from
false-confidence overclaims, or if gold/rubric quality is not adjudicable.
