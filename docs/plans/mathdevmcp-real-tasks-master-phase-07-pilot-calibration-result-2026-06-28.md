# MathDevMCP Real-Task Master Phase 7 Result: Pilot Execution And Calibration

## Status

`PASSED_WITH_CAVEATS`

## Phase Objective

Run and interpret a bounded pilot calibration pass, explicitly distinguishing
normalized fixture scoring from bounded normalization and true workflow
execution.

## Execution Mode

`normalized candidate fixture structural scoring`

This was not free-form workflow execution and not semantic model-output
evaluation.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What does the bounded pilot currently say about benchmark calibration, and what is the dominant remaining uncertainty? |
| Baseline/comparator | Current public report, public scored fixtures, and local-only holdout scored fixtures. |
| Primary criterion | Met with caveats. The execution mode is explicit, veto diagnostics are visible in both public and local scored tiers, and the dominant remaining uncertainty is still holdout representativeness plus semantic-boundary interpretation. The observed public and local mismatch/false-confidence-veto failures must be treated as first-class calibration blockers for any workflow/gate drift. |
| Veto diagnostics | Passed. Public results were not treated as holdout evidence; local-only results were not treated as public evidence; fixture scoring was not treated as workflow performance; veto failures were preserved. |
| Explanatory diagnostics | Public scored: `12/12`, `11 consistent`, `1 mismatch`, false-confidence-veto failures `1`. Local scored: `8/8`, `7 consistent`, `1 mismatch`, false-confidence-veto failures `1`. |
| Not concluded | Holdout-backed generalization, semantic maturity, workflow readiness, gate readiness, release readiness. |

## Commands Run

```bash
git status --short
test -f docs/plans/mathdevmcp-real-tasks-master-phase-07-pilot-calibration-subplan-2026-06-28.md && test -f docs/plans/mathdevmcp-real-tasks-master-phase-08-workflow-integration-subplan-2026-06-28.md
PYTHONPATH=src python -m pytest -q tests/test_real_tasks_report.py tests/test_real_tasks_scored_report.py tests/test_real_tasks_holdout_local_scoring.py tests/test_real_tasks_answer_normalization.py
PYTHONPATH=src python -c '... public report; public scored; local holdout scored ...'
```

## Check Results

- Required Phase 7 and Phase 8 handoff artifacts were present.
- `tests/test_real_tasks_report.py`, `tests/test_real_tasks_scored_report.py`,
  `tests/test_real_tasks_holdout_local_scoring.py`, and
  `tests/test_real_tasks_answer_normalization.py`: `29 passed`.
- Public report:
  - public case total: `12`;
  - status: `consistent`.
- Public scored structural fixture summary:
  - public case total: `12`;
  - scored candidate total: `12`;
  - missing candidate case IDs: none;
  - by status:
    - `consistent`: `11`;
    - `mismatch`: `1`;
  - false-confidence-veto failures: `1`.
- Local holdout scored structural fixture summary:
  - holdout case total: `8`;
  - scored candidate total: `8`;
  - missing candidate case IDs: none;
  - by status:
    - `consistent`: `7`;
    - `mismatch`: `1`;
  - false-confidence-veto failures: `1`;
  - local-only: `true`.

## Calibration Interpretation

The benchmark is sufficiently structured for bounded calibration-policy review,
contingent on first-class treatment of mismatch and false-confidence-veto
failures, with no gate activation or default-policy promotion:

- public scored coverage is complete for the current committed fixture set;
- local holdout scored coverage is complete for the current local seed;
- both tiers expose a mismatch/veto-shaped signal;
- local holdout is broader than the older seven-case notes and currently has
  eight local-only cases.

The dominant remaining uncertainty is not execution stability. It is whether the
current local holdout seed is representative enough, what mechanisms explain the
observed public and local mismatch/false-confidence-veto failures, and where
current structural scoring stops being adequate without richer semantic
interpretation.

## Schema Review From Phase 5

Phase 7 does not reveal a schema/loader blocker for current non-gating reports.
The schema remains fit for current structural reporting, but it is still not a
final long-term semantic evaluation contract.

## Phase 8 Handoff

Proceed to Phase 8 only as a decision/audit phase focused first on boundary and
failure-semantics diagnosis plus calibration-policy options, not as workflow
implementation or gate activation. Phase 8 must keep any workflow surface
non-gating and must stop immediately if outputs start being treated as pass/fail
workflow gates, release evidence, public benchmark evidence, or default-policy
promotion.

## Claude Review

Required because this phase includes calibration interpretation.

- Round 1 verdict: `VERDICT: REVISE`.
- Repair: tightened language from broad calibration health to bounded
  calibration-policy review contingent on first-class mismatch/veto treatment;
  reframed Phase 8 as decision/audit only.
- Round 2 verdict: `VERDICT: AGREE`.

## Freshness And Dirty-Worktree Note

The worktree remains dirty with pre-existing benchmark docs and visible
execution artifacts. Phase 7 did not edit benchmark code, fixtures, or local
holdout artifacts.

## Non-Claims

This Phase 7 pass does not conclude that:

- normalized fixture scoring is free-form workflow performance;
- the local holdout seed proves generalization;
- the benchmark is semantically mature;
- workflow, gate, release policy integration, or default-policy promotion is
  justified.
