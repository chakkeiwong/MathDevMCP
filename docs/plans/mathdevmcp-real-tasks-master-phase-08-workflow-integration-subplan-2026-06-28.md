# MathDevMCP Real-Task Master Phase 8 Subplan: Workflow Integration

## Phase Objective

Audit whether the real-task benchmark should enter routine developer workflow as
a non-gating, advisory surface after first diagnosing boundary/failure semantics
and calibration-policy options from Phase 7.

## Entry Conditions Inherited From Previous Phase

- Phase 7 pilot calibration has been reviewed.
- The benchmark has an explicit dominant uncertainty and non-claim boundary.
- The public and local mismatch/false-confidence-veto failures from Phase 7 are
  treated as first-class blockers to gate/default-policy movement until their
  mechanisms are characterized.
- Workflow integration must remain non-gating.

## Required Artifacts

- `src/mathdevmcp/cli.py` if a CLI surface is proposed
- Existing report/scoring modules if a library-only workflow is retained
- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-08-workflow-integration-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-09-gate-candidate-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - If no CLI/workflow code changes are made:
    `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_report.py tests/test_real_tasks_scored_report.py`
  - If CLI/workflow changes are made, add focused CLI/workflow tests before
    executing them.
- Review:
  - Codex self-review required.
  - Claude read-only review required for any proposed workflow integration
    change.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is a routine non-gating workflow surface justified now after first characterizing Phase 7 boundary/failure semantics, and what exact form should it take? |
| Baseline/comparator | Existing library/report surfaces and Phase 7 calibration result. |
| Primary pass criterion | Workflow decision is justified by calibration value, first-class mismatch/veto diagnosis, and does not create gate, default-policy, or release authority. |
| Veto diagnostics | CLI/CI integration becomes required pass/fail policy, workflow hides non-claims, noisy surface encourages overinterpretation. |
| Explanatory diagnostics | Test stability, command ergonomics, report readability. |
| Not concluded | Gate candidacy, release integration, scientific validity. |
| Artifacts | Phase result, workflow note or code/tests if justified, refreshed Phase 9 subplan. |

## Forbidden Claims And Actions

- Do not add real-task benchmark results to release policy or required CI gates.
- Do not make a CLI surface imply pass/fail readiness.
- Do not add workflow integration merely for convenience if it does not improve
  calibration use.
- Do not treat the Phase 7 public or local mismatch/false-confidence-veto
  failures as ordinary noise or secondary details.
- Do not create required checks, blocking statuses, merge expectations,
  readiness labels, or dashboard prominence that makes the advisory workflow a
  de facto gate before Phase 9 and human approval.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 9 only if:

- workflow integration decision is documented;
- boundary/failure-semantics diagnosis is documented before any advisory
  workflow recommendation;
- any workflow surface is stable, non-gating, and tested;
- observed flakiness/maintenance characteristics are documented or explicitly
  unavailable;
- Phase 9 subplan treats gate-candidate selection as optional and evidence-bound.

## Stop Conditions

- Stop if workflow design would alter product defaults or CI policy without
  explicit human approval.
- Stop if pilot calibration does not justify routine workflow integration.
- Stop if workflow tests are noisy or misleading.
- Stop if mismatch or false-confidence-veto mechanisms have not been
  characterized enough to support even advisory workflow use.
- Stop if the proposed non-gating surface would likely become a de facto gate
  through check naming, CI placement, dashboard wording, or reviewer norms.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 9 subplan.
4. Review the Phase 9 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
