# Phase 1 Subplan: Schema And Quality Rubric

## Phase Objective

Define the benchmark case schema, adapted external case manifest schema, and
quality scorecard used to judge whether the benchmark is good rather than merely
passing.

## Entry Conditions Inherited From Previous Phase

- Phase 0 recorded current benchmark/workbench baselines.
- No network/download requirement is needed for schema design.

## Required Artifacts

- Schema or module updates for workbench benchmark cases and quality metrics.
- Explicit oracle-class enumeration for seeded and external adapted cases.
- Run manifest fields for command, environment, backend matrix, timeout policy,
  seed policy, normalization rules, mutation-set version, and scoring-rubric
  version.
- Tests for schema validation and quality-score computation.
- Phase 1 result record.
- Refreshed Phase 2 subplan.

## Required Checks, Tests, Reviews

- Schema/quality tests.
- Existing benchmark schema tests.
- `python3 -m py_compile` for changed modules.
- `git diff --check`.
- Claude read-only review for quality rubric and false-confidence coverage.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the benchmark program represent seeded and adapted cases with enough metadata to measure quality and prevent boundary overclaims? |
| Baseline/comparator | Existing `BenchmarkResult` structure and benchmark manifest. |
| Primary pass criterion | Schema records source/provenance, oracle class, expected status, expected abstention, quality checks, run manifest fields, and non-claims. |
| Veto diagnostics | Quality score treats pass count as validity; missing provenance for adapted cases; no false-confidence metrics; backend unavailable not distinguished as non-claim. |
| Explanatory diagnostics | Schema validation results and scorecard fields. |
| Not concluded | Quality of any actual cases before they are populated. |
| Artifact | Schema/quality code/tests/result. |

## Forbidden Claims And Actions

- Do not score external packs without source manifests.
- Do not use pass rate alone as benchmark quality.
- Do not allow cases without an oracle class.
- Do not allow backend unavailable to be scored as refutation.
- Do not promote external diagnostic packs to release-gated status.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 if seeded benchmark cases can be represented with oracle
classes and quality metrics can be computed over a case set.

## Stop Conditions

Stop if schema cannot distinguish gated seeded cases from diagnostic adapted
external cases, if oracle classes cannot represent non-claim outcomes, or if
quality metrics cannot encode false-confidence controls.
