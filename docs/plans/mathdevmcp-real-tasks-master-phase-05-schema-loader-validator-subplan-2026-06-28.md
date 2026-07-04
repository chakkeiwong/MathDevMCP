# MathDevMCP Real-Task Master Phase 5 Subplan: Schema, Loader, Validator

## Phase Objective

Confirm and, if needed, harden machine-checkable manifest contracts, path
policy, malformed-input behavior, and tier-aware validation semantics.

## Entry Conditions Inherited From Previous Phase

- Phase 4 private/external policy is dependency-managed and does not block public
  manifest hardening.
- Public schema fields are stable enough for validation.
- Any Phase 4 changes to admissibility, provenance, privacy, or redaction
  constraints have either been re-audited against Phase 2/3 artifacts or recorded
  as deferred future-tier work.

## Required Artifacts

- `src/mathdevmcp/real_tasks_manifest.py`
- `tests/test_real_tasks_manifest.py`
- `benchmarks/real_tasks/manifests/public_cases.json`
- `benchmarks/real_tasks/manifests/holdout_local_cases.template.json`
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-05-schema-loader-validator-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-06-non-gating-reporting-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_manifest.py`
  - live load/validate summary using `load_real_task_public_manifest(...)` and
    `validate_real_task_public_manifest(...)`.
- Review:
  - Codex self-review required.
  - Claude read-only review required if schema rules or path policy change.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are real-task benchmark artifacts machine-checkable, portable, and stable enough for reporting? |
| Baseline/comparator | Existing public manifest loader/validator and tests. |
| Primary pass criterion | Valid public manifest loads consistently; malformed and unsafe manifests fail predictably; schema stability is provisional until pilot calibration reviews it. |
| Veto diagnostics | Absolute paths accepted, missing files hidden, malformed cases treated as valid, private tier assumptions baked into public loader. |
| Explanatory diagnostics | Number and kind of validation findings. |
| Not concluded | Benchmark execution quality, semantic scoring maturity, release readiness. |
| Artifacts | Phase result, validation summary, refreshed Phase 6 subplan. |

## Forbidden Claims And Actions

- Do not relax path policy to make fixtures pass.
- Do not add private/external assumptions to the public loader.
- Do not treat loader pass as benchmark execution pass.
- Do not treat Phase 5 schema/validator behavior as a final long-term contract
  before Phase 7 pilot calibration confirms it remains fit for purpose.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 only if:

- public manifest validation is clean;
- malformed input tests pass;
- path policy is portable and enforced;
- schema/validator status is labeled provisional pending post-pilot review unless
  Phase 7 has already confirmed it;
- Phase 6 subplan consumes stable loader/report contracts.

## Stop Conditions

- Stop if public manifest cannot load or validate.
- Stop if path-policy failures require a human privacy decision.
- Stop if fixing schema behavior would invalidate category contracts.
- Stop if Phase 5 would freeze convenience fields as defaults before pilot
  calibration has reviewed whether they answer the benchmark question.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 6 subplan.
4. Review the Phase 6 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
