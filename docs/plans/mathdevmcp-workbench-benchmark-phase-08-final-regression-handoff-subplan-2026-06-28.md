# Phase 8 Subplan: Final Regression And Handoff

## Phase Objective

Run final focused regression and write the final visible stop handoff for the
benchmark program.

## Entry Conditions Inherited From Previous Phase

- Docs/operator UX phase passed.
- Seeded benchmark is integrated and external packs are either diagnostic or
  blocked with explicit source-path/approval requirements.

## Required Artifacts

- Phase 8 result record.
- Final visible stop handoff.
- Final ledger entries.

## Required Checks, Tests, Reviews

- Full benchmark gate.
- Focused benchmark tests.
- Focused workbench regression tests if impacted.
- MCP benchmark/report tests.
- Docs forbidden-claim grep.
- `git diff --check`.
- Claude final read-only review if material changes remain.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the benchmark program complete enough to hand off with accurate evidence and limits? |
| Baseline/comparator | Phase 0 baseline and phase results. |
| Primary pass criterion | Required artifacts exist, checks pass, result records are written, and final handoff states residual risks. |
| Veto diagnostics | Final handoff claims release readiness, external benchmark performance, or broad proof automation. |
| Explanatory diagnostics | Final test/benchmark outputs and ledger. |
| Not concluded | Release readiness, external leaderboard score, or scientific validity. |
| Artifact | Final result and stop handoff. |

## Forbidden Claims And Actions

- Do not hide blockers.
- Do not claim external adapted packs are complete unless they passed promotion
  gates.
- Do not conflate benchmark passing with product/release readiness.

## Exact Next-Phase Handoff Conditions

No next phase. Handoff must state final status, artifacts, checks, residual
risks, and safest next human decision.

## Stop Conditions

Stop if final checks fail and cannot be repaired locally, or if final status
would require a human decision about external data, release policy, or
redistribution.
