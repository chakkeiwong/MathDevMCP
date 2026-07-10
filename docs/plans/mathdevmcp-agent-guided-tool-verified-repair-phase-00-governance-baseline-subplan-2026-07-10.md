# Phase 00 Subplan: Governance, Baseline, And Review Gate

Date: 2026-07-10

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Create the governed lane artifacts, lock the baseline failure mode, review the
plan, and launch only after the plan survives local and read-only review gates.

## Entry Conditions Inherited From Previous Phase

- Current Phase 06 reports localize targets and typed blockers but can still
  render blocked ranked branches as repair-like prose.
- Existing derivation-tree, branch-controller, backend-adapter, and document
  report modules are available.
- The repo policy already requires external-tool-first mathematical search.

## Required Artifacts

- Master program:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-master-program-2026-07-10.md`
- Phase subplans 00-09 under `docs/plans`.
- Visible runbook:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-runbook-2026-07-10.md`
- Execution ledger:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-ledger-2026-07-10.md`
- Stop handoff:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-stop-handoff-2026-07-10.md`
- Review bundle:
  `docs/reviews/mathdevmcp-agent-guided-tool-verified-repair-plan-review-bundle-2026-07-10.md`
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-00-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- Local artifact/content sanity check with `rg`.
- `git diff --check`.
- Claude read-only review gate when available.
- If Claude is unavailable after the review gate probe/fallback, record the
  status and use a fresh Codex read-only fallback review.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the lane target the real problem: agent creativity must enter as candidate branches, while reports publish only tree/tool-grounded evidence? |
| Baseline/comparator | Current Phase 06 context-aware repair reports and tests. |
| Primary criterion | Master program, subplans, runbook, ledger, stop handoff, and review bundle exist; each subplan has objective, entry conditions, artifacts, checks/reviews, evidence contract, forbidden claims/actions, next-phase handoff, stop conditions, and end-of-subplan actions. |
| Veto diagnostics | Missing phase artifacts; detached execution despite visible template; Claude treated as executor; no exact stop conditions; no baseline failure lock; no external-tool-first discipline. |
| Explanatory diagnostics | Claude unavailable, dirty worktree, optional backend unavailable. |
| Not concluded | No implementation correctness, no improved report quality, no backend certification, no release readiness. |
| Artifact | Phase 00 result and review trail. |

## Forbidden Claims Or Actions

- Do not claim the repair tool is implemented.
- Do not launch detached overnight execution from the visible runbook.
- Do not let Claude edit files, run implementation, or authorize claims.
- Do not install packages, fetch network resources, or mutate backend
  environments.

## Exact Next-Phase Handoff Conditions

Advance to Phase 01 only if:

- local checks pass;
- Claude review or Codex fallback review converges to `AGREE`;
- Phase 00 result records review status, non-claims, and remaining risks.

## Stop Conditions

Stop if:

- review identifies a material plan flaw requiring human project direction;
- the runbook cannot be reconciled with the visible-execution template;
- continuing requires unapproved external service, package installation, or
  detached execution.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 00 result / close record.
3. Draft or refresh Phase 01 subplan.
4. Review Phase 01 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
