# Phase 4 Subplan: V2 Regression Guard

Date: 2026-07-04

Status: `COMPLETE_LOCAL_CHECKS_AND_READ_ONLY_REVIEW_AGREED`

## Phase Objective

Use the v2 downstream-agent usefulness diagnostic as a bounded regression guard
after product work, not as the mission or a prompt-tuning target.

## Entry Conditions Inherited From Previous Phase

- Phase 3 result has realistic case coverage and no unresolved boundary bug.
- Phase 3 found and repaired compact handoff action normalization: high-level
  action `code` now maps to handoff action `kind`.
- Product surfaces to evaluate are fixed for this phase.
- Scoring criteria and hard-veto interpretation are frozen before any new
  outputs are inspected.

## Required Artifacts

- Regression guard plan or replay note.
- Existing v2 artifacts reused when possible:
  `.mathdevmcp/downstream_agent_usefulness_v2/`.
- New model/API response collection is not authorized by this subplan. If
  needed, Phase 4 must stop with an explicit approval request.
- Phase result:
  `docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-result-2026-07-04.md`
- Refreshed Phase 5 compatibility-policy subplan.

## Required Checks, Tests, And Reviews

- Local artifact/schema checks for any replayed v2 data.
- Focused comparison script/test if one already exists locally; otherwise write
  a bounded manual result note and stop before new model collection.
- `git diff --check -- docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-subplan-2026-07-04.md`
- Bounded Claude read-only review for the regression interpretation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Did the product work preserve or improve the v2 handoff usefulness signals without introducing hard-veto regressions? |
| Baseline/comparator | Prior final v2 bounded local diagnostic: C tied B on 5/6 and improved on `V2-PRP-01-gaussian-score-review-packet`, hard vetoes 0/0/0. |
| Primary criterion | A frozen, bounded replay or approved rerun records whether the new product surface regresses, improves, or remains neutral under the existing interpretation discipline. |
| Veto diagnostics | Scoring changed after outputs; benchmark score treated as release/product proof; hard veto ignored; new external collection run without approval. |
| Explanatory diagnostics | Per-case score deltas, hard-veto table, malformed-output handling, no-hidden-retry evidence. |
| Not concluded | No public benchmark validity, downstream-agent reliability, release readiness, or general model reliability. |

## Forbidden Claims And Actions

- Do not call this a public benchmark.
- Do not change scoring after seeing outputs.
- Do not collect new model/API responses without explicit approval.
- Do not use a benchmark win to weaken product boundaries.

## Exact Next-Phase Handoff Conditions

Phase 5 may start only if:

- Regression result is recorded or the phase stops with a clear approval
  request for new model/API collection.
- Hard-veto-first interpretation is preserved.
- Phase 5 subplan is refreshed with compatibility issues observed during
  regression/replay.

## Stop Conditions

Stop if:

- New external response collection is needed and approval is not yet granted.
- Existing artifacts are insufficient and cannot support a bounded replay.
- A hard-veto regression appears and requires product repair before continuing.
