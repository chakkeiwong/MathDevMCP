# Phase 6 Subplan: Final Decision And Handoff

Date: 2026-07-01

Status: `READY_WITH_PHASE_5_REGRESSION_EVIDENCE`

## Phase Objective

Make the final bounded decision for this runbook: freeze the operational
packet standard as a local candidate, revise it, expand calibration, or stop
with a blocker.

## Entry Conditions Inherited From Previous Phase

- Phase 5 has recorded regression and benchmark-hook evidence.
- All implementation and exposure phases have result artifacts or blockers.
- Claude review trail records the human waiver and any prior failed probe
  attempts.
- Claude review gates are waived for this execution window by explicit user
  direction; Codex-only final-decision review and local checks remain required.

## Required Artifacts

- Phase 6 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-06-final-decision-handoff-result-2026-07-01.md`.
- Updated visible execution ledger.
- Updated Claude review trail or waiver record.
- Final visible stop handoff:
  `docs/plans/mathdevmcp-agent-handoff-packet-standardization-visible-stop-handoff-2026-07-01.md`.

## Required Checks, Tests, Reviews

- Verify all phase result/blocker artifacts exist.
- Verify required local tests from the final executed implementation scope are
  recorded.
- Claude read-only final-decision review is waived for this execution window by
  explicit user direction. Codex-only final-decision review is required because
  this phase makes the bounded standardization decision.
- Focused patch/review loop if Codex identifies artifact coverage or boundary
  wording issues.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What bounded decision is justified by this runbook's actual artifacts? |
| Baseline/comparator | Whole-run artifacts, tests, Claude review trail, and prior calibration non-claims. |
| Primary criterion | Final decision matches the artifacts, preserves non-claims, and identifies exact remaining gaps or next actions. |
| Veto diagnostics | Decision overstates tests; C-over-B superiority claimed; release/scientific/public benchmark/product claims; Claude waiver not recorded; missing phase artifacts; unresolved blocker ignored. |
| Explanatory diagnostics | Phase summary table, test matrix, remaining gaps, final Codex review findings. |
| Not concluded | Any claim outside local operational standardization and actual executed checks. |

## Forbidden Claims Or Actions

- Do not mark complete unless all required phase results or blockers exist.
- Do not claim release readiness or public benchmark validity.
- Do not claim downstream-agent improvement unless a separately approved
  downstream-agent measurement phase actually ran and supports that bounded
  claim.
- Do not use Claude as an authority to cross human/project boundaries.

Required Phase 6 local checks:

- verify all phase result/blocker artifacts exist;
- confirm packet/report tests and regression tests are listed accurately;
- confirm the prior calibration tie/non-claim remains explicit;
- confirm no new downstream-agent responses were collected under this program.

## Exact Next-Phase Handoff Conditions

This is the final phase. Completion requires:

- Phase 6 result written;
- stop handoff refreshed;
- review trail updated through final waiver-aware review record;
- tests/benchmarks actually run are listed;
- unresolved blockers and non-claims are explicit.

## Stop Conditions

Stop with blocker status if:

- final artifacts are incomplete;
- Codex-only review finds a final-decision blocker that cannot be fixed within
  the phase boundary;
- a human project-direction decision is required before a bounded final
  decision can be made.

## Phase Close Protocol

At phase close:

1. run required artifact and local checks;
2. write the Phase 6 result/close record;
3. refresh the final stop handoff;
4. review the final artifacts for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. run Codex-only final-decision review and patch until convergence or blocker.
