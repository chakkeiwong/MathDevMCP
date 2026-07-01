# MathDevMCP Real-Task Master Phase 2 Subplan: Public Corpus

## Phase Objective

Confirm and, if needed, improve the committed public real-task corpus so it has
meaningful coverage across benchmark families while remaining public-safe,
loader-clean, and below readiness claims.

## Entry Conditions Inherited From Previous Phase

- Phase 1 category scoring contracts are stable enough to determine required
  public case fields and gold expectations.
- The public corpus remains a development/calibration surface, not holdout or
  policy evidence.

## Required Artifacts

- `benchmarks/real_tasks/manifests/public_cases.json`
- `benchmarks/real_tasks/README.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`
- `src/mathdevmcp/real_tasks_manifest.py`
- `tests/test_real_tasks_manifest.py`
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-02-public-corpus-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-03-holdout-local-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_manifest.py tests/test_real_tasks_report.py`
  - live public report summary using `real_task_public_report(...)`.
- Review:
  - Codex self-review required.
  - Claude read-only review required if new public cases or gold semantics are
    added.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the public corpus broad and stable enough to feed holdout-local design and reporting? |
| Baseline/comparator | Current committed public manifest and category scoring contracts. |
| Primary pass criterion | Public manifest validates, all major families have meaningful coverage, and gold fields preserve hard-veto boundaries. |
| Veto diagnostics | Absolute/private paths, missing referenced files, unstable gold semantics, public cases treated as holdout/generalization evidence. |
| Explanatory diagnostics | Case counts by family, repo, difficulty, expected status, and false-confidence-veto count. |
| Not concluded | Representativeness of the full task space, holdout-backed generalization, readiness. |
| Artifacts | Phase result, public report summary, refreshed Phase 3 subplan. |

## Forbidden Claims And Actions

- Do not add private or sensitive material to the public manifest.
- Do not claim public corpus growth is product readiness.
- Do not optimize case selection only to improve current structural scores.
- Do not weaken path-policy tests.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only if:

- public manifest validation passes;
- public report is non-gating and warning-free or warnings are documented;
- public corpus coverage is sufficient to identify what should remain holdout;
- Phase 3 subplan defines disjointness and local-only boundaries.

## Stop Conditions

- Stop if candidate public cases require private paths or unpublished content.
- Stop if adding public cases would overfit to an already-known scorer weakness
  without representativeness value.
- Stop if manifest validation fails and cannot be fixed locally.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 3 subplan.
4. Review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
