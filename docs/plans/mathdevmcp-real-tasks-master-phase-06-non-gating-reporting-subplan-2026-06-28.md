# MathDevMCP Real-Task Master Phase 6 Subplan: Non-Gating Reporting

## Phase Objective

Confirm and, if needed, improve non-gating public and structural scored reports
so benchmark signals are inspectable without becoming workflow, gate, or release
evidence.

## Entry Conditions Inherited From Previous Phase

- Phase 5 loader/validator contract is stable.
- Public cases are sufficient for meaningful inventory and structural summaries.
- Precision/recall metrics are deferred unless candidate outputs and scoring are
  calibrated enough to make them meaningful.

## Required Artifacts

- `src/mathdevmcp/real_tasks_report.py`
- `src/mathdevmcp/real_tasks_scored_report.py`
- `src/mathdevmcp/real_tasks_scoring.py`
- `tests/test_real_tasks_report.py`
- `tests/test_real_tasks_scored_report.py`
- `tests/test_real_tasks_candidate_fixtures.py`
- `benchmarks/real_tasks/fixtures/public_candidate_answers.json`
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-06-non-gating-reporting-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-07-pilot-calibration-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_report.py tests/test_real_tasks_scored_report.py tests/test_real_tasks_candidate_fixtures.py`
  - live public report and public scored summary.
- Review:
  - Codex self-review required.
  - Claude read-only review required if report policy boundaries, summaries, or
    scoring outputs change materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are current reports useful for benchmark inspection while preserving non-gating boundaries? |
| Baseline/comparator | Existing report/scored-report modules and tests. |
| Primary pass criterion | Reports surface inventory, structural status, hard-veto counts, warnings, and policy boundaries without gate/release wording. |
| Veto diagnostics | Reports imply readiness, hide false-confidence-veto failures, or present proxy precision/recall as calibrated quality. |
| Explanatory diagnostics | Case totals, family/status counts, missing candidate IDs, warnings. |
| Not concluded | Free-form model performance, semantic evaluation, workflow/gate/release readiness. |
| Artifacts | Phase result, live report summaries, refreshed Phase 7 subplan. |

## Forbidden Claims And Actions

- Do not connect real-task reports to `benchmark_gate`.
- Do not call structural fixture scoring semantic benchmark execution.
- Do not add global score authority.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 7 only if:

- report and scored-report tests pass;
- report policy boundaries remain explicit;
- live summaries are recorded;
- Phase 7 subplan states execution mode clearly.

## Stop Conditions

- Stop if hard-veto failures are hidden or aggregated away.
- Stop if reports imply policy authority.
- Stop if missing candidate coverage is not surfaced.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 7 subplan.
4. Review the Phase 7 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
