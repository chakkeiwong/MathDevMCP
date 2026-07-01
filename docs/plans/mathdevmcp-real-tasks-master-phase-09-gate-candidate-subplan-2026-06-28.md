# MathDevMCP Real-Task Master Phase 9 Subplan: Gate-Candidate Selection

## Phase Objective

Determine whether any narrow, stable, safety-relevant subset of the real-task
benchmark is mature enough to be considered for future policy use.

## Entry Conditions Inherited From Previous Phase

- Phase 8 workflow integration has produced stable non-gating operational
  experience, or has explicitly declined integration.
- Gate-candidate selection is optional and cannot proceed from convenience alone.

## Required Artifacts

- Phase 8 workflow result
- Current report/scoring tests and any workflow stability notes
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-09-gate-candidate-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-10-release-policy-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_report.py tests/test_real_tasks_scored_report.py tests/test_real_tasks_scoring.py`
  - any workflow-specific checks introduced in Phase 8.
- Review:
  - Codex self-review required.
  - Claude read-only review required for any gate-candidate recommendation.
  - Human approval required before any real-task subset is made gating.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is any real-task benchmark subset stable and well-understood enough to nominate as a future gate candidate? |
| Baseline/comparator | Phase 8 workflow stability evidence and current non-gating report behavior. |
| Primary pass criterion | Gate-candidate decision is conservative, narrow, and justified by stability plus safety relevance. |
| Veto diagnostics | Unstable, overfitted, semantic-immature, or representativeness-limited subsets are promoted. |
| Explanatory diagnostics | Pass stability, hard-veto relevance, maintenance burden, known flakiness. |
| Not concluded | Release-policy adoption, gate activation, scientific correctness. |
| Artifacts | Phase result, gate-candidate shortlist or explicit no-candidate decision, refreshed Phase 10 subplan. |

## Forbidden Claims And Actions

- Do not activate a gate in this phase.
- Do not use aggregate scores as gate authority.
- Do not nominate any subset with unresolved veto or flakiness issues.
- Do not bypass human approval for policy movement.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 10 only if:

- a narrow gate-candidate shortlist exists and has passed review;
- human approval exists for policy-design work;
- Phase 10 subplan keeps release integration conditional and narrow.

If no subset qualifies, write a no-candidate result and stop the program before
Phase 10.

## Stop Conditions

- Stop if Phase 8 did not produce stable operational experience.
- Stop if any candidate depends on immature semantic scoring.
- Stop if human approval for policy-design work is absent.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 10 subplan if and only if handoff conditions pass.
4. Review the Phase 10 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
