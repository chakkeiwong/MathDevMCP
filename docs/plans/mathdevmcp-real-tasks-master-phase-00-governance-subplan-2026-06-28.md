# MathDevMCP Real-Task Master Phase 0 Subplan: Governance

## Phase Objective

Confirm that the real-task benchmark program has a stable purpose, safety
invariant, evidence boundary, and non-claim contract before downstream phases
consume it.

## Entry Conditions Inherited From Previous Phase

- User goal is to execute the real-task benchmark master program under visible
  gated supervision.
- No previous phase exists.
- Current governing artifact:
  `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`.

## Required Artifacts

- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-audit-2026-06-17.md`
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-00-governance-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-01-category-scoring-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - `rg -n "False certification remains a hard veto|not.*release certificate|not.*scientific validation|Phase-completion boundary" docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
  - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_manifest.py`
- Review:
  - Codex self-review required.
  - Claude read-only review optional because this phase is document-governance
    only and already has a prior audit.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the program define the benchmark purpose and non-claims strongly enough for downstream execution? |
| Baseline/comparator | Master program plus prior audit. |
| Primary pass criterion | Safety invariant, evidence boundary, and phase-completion boundary are explicit and compatible. |
| Veto diagnostics | Any wording that makes benchmark pass imply proof, convergence, scientific validity, workflow gate, or release readiness. |
| Explanatory diagnostics | Existing case counts, dashboard status, and current benchmark results. |
| Not concluded | Benchmark maturity, public or holdout representativeness, workflow readiness, gate readiness, or release readiness. |
| Artifacts | Phase result, ledger entry, refreshed Phase 1 subplan. |

## Forbidden Claims And Actions

- Do not claim the benchmark is complete.
- Do not claim governance approval authorizes any later phase by itself.
- Do not edit code in this phase unless a local check exposes a direct
  governance-artifact import or test failure.
- Do not move benchmark results into `benchmark_gate` or release policy.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only if:

- the master program retains explicit hard-veto and non-claim language;
- the phase-completion boundary remains visible;
- local manifest tests pass or any failure is documented as unrelated and
  non-blocking for governance;
- this phase result is written;
- the Phase 1 subplan exists and has been reviewed for boundary safety.

## Stop Conditions

- Stop if the master program implies policy authority before Phase 9 or Phase 10.
- Stop if governance requires a project-direction decision not already given by
  the user.
- Stop if local checks reveal repository breakage that makes the benchmark
  manifest unreadable.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 1 subplan.
4. Review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
