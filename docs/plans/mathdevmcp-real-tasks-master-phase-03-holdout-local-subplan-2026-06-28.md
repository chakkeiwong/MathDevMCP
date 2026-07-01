# MathDevMCP Real-Task Master Phase 3 Subplan: Holdout-Local

## Phase Objective

Maintain a non-public holdout-local tier that reduces public-set overfitting
pressure while preserving local-only boundaries and avoiding generalization
claims.

## Entry Conditions Inherited From Previous Phase

- Phase 2 public corpus is loader-clean and broad enough to identify public-set
  tuning pressure.
- Holdout-local additions must differ by at least one meaningful disjointness
  axis: source area, label/chapter neighborhood, task template, or benchmark
  author exposure status.

## Required Artifacts

- `docs/plans/mathdevmcp-holdout-local-corpus-subplan-2026-06-17.md`
- `benchmarks/real_tasks/holdout_local/README.md`
- `benchmarks/real_tasks/manifests/holdout_local_cases.template.json`
- `benchmarks/real_tasks/fixtures/holdout_local_candidate_answers.template.json`
- `src/mathdevmcp/real_tasks_holdout_local.py`
- `src/mathdevmcp/real_tasks_holdout_local_scoring.py`
- `.local/mathdevmcp/holdout_local_cases.json` if present locally
- `.local/mathdevmcp/holdout_local_candidate_answers.json` if present locally
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-03-holdout-local-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-04-private-external-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_holdout_local.py tests/test_real_tasks_holdout_local_scoring.py`
  - live local holdout fixture score using `score_local_holdout_candidate_fixtures(...)` when local files exist.
- Review:
  - Codex self-review required.
  - Claude read-only review required for any new local family, judgment shape, or
    failure shape.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the holdout-local tier add representativeness value beyond the public corpus while staying local-only? |
| Baseline/comparator | Current public corpus, holdout-local policy, local seed if present. |
| Primary pass criterion | Holdout-local policy/scaffold exists, local scoring is bounded/non-gating, and additions add a new family/judgment/failure shape. |
| Veto diagnostics | Local artifacts committed by default, local evidence treated as public evidence, public-like duplicates added as holdout, missing candidate coverage hidden. |
| Explanatory diagnostics | Local case count, family mix, scored coverage, mismatch/veto signal. |
| Not concluded | Holdout-backed generalization, policy readiness, representative task distribution. |
| Artifacts | Phase result, local score summary if available, refreshed Phase 4 subplan. |

## Forbidden Claims And Actions

- Do not commit populated local holdout artifacts by default.
- Do not claim local holdout evidence is public benchmark evidence.
- Do not add a holdout case that differs only by filename or path placement.
- Do not rank configurations by local scores if veto diagnostics fail.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 only if:

- holdout-local policy and local-only boundary are explicit;
- local discovery/initialization/scoring tests pass;
- any local seed state is summarized without exposing private content;
- Phase 4 subplan distinguishes local holdout from private/external policy.

## Stop Conditions

- Stop if a proposed local addition does not add a new judgment or failure shape.
- Stop if local scoring requires committing non-public artifacts.
- Stop if local/public boundaries become ambiguous.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 4 subplan.
4. Review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
