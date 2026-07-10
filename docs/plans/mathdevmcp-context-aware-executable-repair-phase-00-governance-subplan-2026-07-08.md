# Phase 00 Subplan: Governance And Review Gate

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Create and review the master program, phase subplans, visible runbook, ledger,
and compact review bundle before implementation.

## Entry Conditions Inherited From Previous Phase

- The previous display-equation lane passed but still produces proposals that
  are not yet mathematically substantive enough.
- `prop:interior-foc` exposed the key limitation: proposition labels are not
  first-class repair targets in the high-level report.
- Existing modules already include proposition target extraction and typed
  obligation diagnostics.

## Required Artifacts

- Master program:
  `docs/plans/mathdevmcp-context-aware-executable-repair-master-program-2026-07-08.md`
- Phase subplans 00-06 under `docs/plans`.
- Visible runbook:
  `docs/plans/mathdevmcp-context-aware-executable-repair-visible-runbook-2026-07-08.md`
- Ledger:
  `docs/plans/mathdevmcp-context-aware-executable-repair-visible-ledger-2026-07-08.md`
- Stop handoff:
  `docs/plans/mathdevmcp-context-aware-executable-repair-visible-stop-handoff-2026-07-08.md`
- Review bundle:
  `docs/reviews/mathdevmcp-context-aware-executable-repair-plan-review-bundle-2026-07-08.md`
- Phase result:
  `docs/plans/mathdevmcp-context-aware-executable-repair-phase-00-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- Local artifact/content check.
- `git diff --check` on new plan and review artifacts.
- Claude review gate if allowed.
- If Claude review is blocked or unavailable, record why and use fresh Codex
  read-only fallback review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the program target the real gap: context-aware executable repair proposals, not prettier templates? |
| Baseline/comparator | Current Phase 04 display-equation reports from `mathdevmcp-substantive-document-derivation`. |
| Primary criterion | Plan phases require proposition context extraction, context graph, typed IR, executable/blocked backend attempts, repair branch search, and document-ready report regression. |
| Veto diagnostics | No frozen targets; no external-tool-first discipline; no stop conditions; detached execution despite visible template; Claude treated as execution authority. |
| Explanatory diagnostics | Claude blocked by environment policy; optional backend absence; dirty worktree. |
| Not concluded | No implementation or report-quality claim in Phase 00. |
| Artifact | Phase 00 result and review trail. |

## Forbidden Claims Or Actions

- Do not claim any target document is fixed.
- Do not launch detached execution from this visible runbook.
- Do not let Claude edit files, run commands, or authorize scientific claims.
- Do not install packages or fetch network resources.

## Exact Next-Phase Handoff Conditions

Advance to Phase 01 only if:

- local artifact checks pass;
- Claude review or Codex fallback review converges to `AGREE`;
- Phase 00 result records review trail, non-claims, and remaining risks.

## Stop Conditions

Stop if:

- review identifies a material plan flaw requiring human project direction;
- implementation would require unapproved package installation or network
  access before Phase 01;
- the runbook cannot be reconciled with the visible-execution template.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 00 result / close record.
3. Draft or refresh Phase 01 subplan.
4. Review Phase 01 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
