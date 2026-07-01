# Phase 3 Subplan: Benchmark Quality Metrics

## Phase Objective

Add a benchmark-quality report that measures coverage, oracle-class coverage,
negative-control rate, boundary sensitivity, determinism, failure locality, and
a fixed mutation-sensitivity probe family for the actual seeded workbench
benchmark.

## Entry Conditions Inherited From Previous Phase

- Seeded benchmark category exists and passes formal benchmark checks.
- Per-case quality checks expose boundary-related booleans.

## Required Artifacts

- Benchmark-quality reporting function or module.
- A report path or API that consumes the actual Phase 2 seeded workbench cases
  and actual seeded runner results.
- Tests for coverage and quality metrics.
- Fixed simulated mutation family:
  `backend_unavailable -> refuted`, `structural_only -> proved`,
  `numeric_supported -> backend_proved`, `missing_assumptions -> proved`.
- Run manifest/scoring rubric version artifact.
- Phase 3 result record.
- Refreshed Phase 4 subplan.

## Exact Thresholds And Denominators

- Tool coverage denominator: the explicit seeded workbench tool set recorded in
  code; pass iff every expected seeded tool has at least one case.
- Oracle coverage denominator: the required seeded oracle-class set; pass iff
  every required oracle class is present in the actual seeded cases.
- Negative-control denominator: all valid actual seeded cases; pass iff at
  least `40%` have `negative_control=true`.
- Boundary-check denominator: actual seeded result records; pass iff every
  result has `boundary_preserved=true` and a supported oracle class.
- Result/case alignment denominator: actual seeded cases; pass iff result ids
  exactly match case ids.
- Determinism denominator: two immediate seeded-category runs in the same
  environment; pass iff case ids, observed statuses, pass/fail values, and
  expected-abstention flags are identical.
- Mutation denominator: the fixed four-member simulated mutation family; pass
  iff all four known proof-promotion mutations are detected as failures without
  editing repo files.
- Manifest denominator: the required run-manifest field set; pass iff all
  fields are present and backend availability plus scorer/rubric versions are
  recorded in the report used for threshold evaluation.

The fixed mutation family is a diagnostic panel, not a complete adversarial
benchmark. No threshold may be justified solely by these four known failures.

## Required Checks, Tests, Reviews

- Quality metric tests over both synthetic schema fixtures and actual seeded
  workbench cases/results.
- Seeded benchmark tests.
- Determinism check by running seeded category twice.
- Focused mutation-probe checks that do not modify committed files, or static
  probe tests that simulate bad outputs.
- `git diff --check`.
- Claude review for quality metric adequacy.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we measure whether the benchmark itself is good enough to catch false-confidence regressions? |
| Baseline/comparator | Phase 2 seeded category and current benchmark summary. |
| Primary pass criterion | Quality report over the actual seeded benchmark meets the exact thresholds above for tool coverage, oracle-class coverage, negative-control rate, boundary checks, result/case alignment, determinism, run manifest completeness, and fixed mutation sensitivity. |
| Veto diagnostics | Pass rate used as sole benchmark-quality measure; mutation probes mutate real repo files; quality report promotes benchmark to scientific validity; fixed mutation family not detected. |
| Explanatory diagnostics | Quality scorecard, threshold denominators, backend matrix, and simulated bad-output failures. |
| Not concluded | Benchmark completeness or external validity. |
| Artifact | Quality report code/tests/result. |

## Forbidden Claims And Actions

- Do not edit code under test just to run mutation probes.
- Do not claim benchmark quality is final from seeded cases alone.
- Do not hide low negative-control coverage.
- Do not proceed to formal seeded gate integration unless all Phase 3
  thresholds are recorded as passing.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 if seeded benchmark quality can be reported and known
false-confidence failures are detectable in simulation. Phase 6 formal gate
integration remains blocked unless all seeded-gate promotion thresholds pass.
If any threshold fails, write a blocker or repair record; do not narrow the
handoff to only the known mutation family.

## Stop Conditions

Stop if quality metrics cannot distinguish positive capability from
false-confidence resistance.
