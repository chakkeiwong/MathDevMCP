# MathDevMCP Real-Task Master Phase 7 Subplan: Pilot Execution And Calibration

## Phase Objective

Run and interpret a bounded pilot calibration pass, explicitly distinguishing
normalized fixture scoring from bounded normalization and true workflow
execution.

## Entry Conditions Inherited From Previous Phase

- Phase 6 non-gating reports pass local checks.
- Report policy boundaries are explicit.
- Pilot execution mode must be declared before interpreting results.

## Required Artifacts

- `docs/plans/mathdevmcp-real-tasks-benchmark-public-pilot-calibration-note-2026-06-17.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-structural-scoring-calibration-note-2026-06-18.md`
- `docs/plans/mathdevmcp-benchmark-calibration-milestone-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-calibration-result-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-comparative-calibration-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-comparative-calibration-note-ii-2026-06-19.md`
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-07-pilot-calibration-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-08-workflow-integration-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_report.py tests/test_real_tasks_scored_report.py tests/test_real_tasks_holdout_local_scoring.py tests/test_real_tasks_answer_normalization.py`
  - live public, public scored, and local holdout scored summaries.
- Review:
  - Codex self-review required.
  - Claude read-only review required for calibration interpretation or any
    changed current-state synthesis note.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What does the bounded pilot currently say about benchmark calibration, and what is the dominant remaining uncertainty? |
| Baseline/comparator | Current public report, public scored fixtures, and local-only holdout scored fixtures. |
| Primary pass criterion | Calibration interpretation identifies the execution mode and one dominant remaining uncertainty without overclaiming. |
| Veto diagnostics | Public-set success treated as holdout evidence, local-only evidence treated as public evidence, veto failures ignored, fixture scoring treated as workflow performance. |
| Explanatory diagnostics | Case totals, mismatch/veto counts, missing coverage, family asymmetry. |
| Not concluded | Holdout-backed generalization, semantic maturity, workflow readiness, gate readiness, release readiness. |
| Artifacts | Phase result, live summary, reviewed next Phase 8 subplan. |

## Forbidden Claims And Actions

- Do not claim calibration proves generalization.
- Do not promote a public or local fixture score into model/workflow performance.
- Do not change thresholds after seeing results without a separate reviewed
  recalibration note.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 8 only if:

- pilot/calibration result clearly states execution mode;
- veto diagnostics are interpreted before secondary summaries;
- current dominant uncertainty is stated;
- Phase 8 subplan keeps workflow integration non-gating.

## Stop Conditions

- Stop if current results are too stale or inconsistent to interpret.
- Stop if the comparison is still dominated by obvious coverage imbalance and a
  stronger claim is being considered.
- Stop if a semantic evaluator would be required to answer the phase question.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 8 subplan.
4. Review the Phase 8 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
