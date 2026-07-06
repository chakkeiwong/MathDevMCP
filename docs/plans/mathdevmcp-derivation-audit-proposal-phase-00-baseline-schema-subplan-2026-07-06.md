# Phase 0 Subplan: Baseline, Schema, Review Gate

Date: 2026-07-06

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Freeze current derivation-tool behavior, define the target derivation
gap/proposal schema, create the execution runbook artifacts, and get material
read-only review before implementation changes.

## Entry Conditions Inherited From Previous Phase

- User approved the derivation-audit/proposal lane direction.
- Assumption gap/proposal behavior has a working reference artifact.
- Current repo contains dirty work from assumptions and audit/fix lanes; this
  phase must preserve it.
- Claude review guide is available at
  `/home/chakwong/python/claudecodex/docs/claude-review-gate-agent-guide.md`.
- Visible gated execution template is available at
  `/home/chakwong/python/claudecodex/docs/templates/visible-gated-execution-runbook-template.md`.

## Required Artifacts

- Master program:
  `docs/plans/mathdevmcp-derivation-audit-proposal-master-program-2026-07-06.md`
- Phase 0 subplan:
  `docs/plans/mathdevmcp-derivation-audit-proposal-phase-00-baseline-schema-subplan-2026-07-06.md`
- Phase 1 draft subplan:
  `docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-subplan-2026-07-06.md`
- Visible runbook:
  `docs/plans/mathdevmcp-derivation-audit-proposal-visible-gated-execution-runbook-2026-07-06.md`
- Detached/overnight launch plan:
  `docs/plans/mathdevmcp-derivation-audit-proposal-gated-overnight-execution-plan-2026-07-06.md`
- Execution ledger:
  `docs/plans/mathdevmcp-derivation-audit-proposal-visible-execution-ledger-2026-07-06.md`
- Review bundle:
  `docs/reviews/mathdevmcp-derivation-audit-proposal-plan-review-bundle.md`
- Phase 0 result:
  `docs/plans/mathdevmcp-derivation-audit-proposal-phase-00-baseline-schema-result-2026-07-06.md`

## Required Checks, Tests, Reviews

- Baseline direct derivation checks:
  - `python3 -m pytest tests/test_derive_from.py tests/test_derive_or_refute.py -q`
- Existing assumptions reference check:
  - `python3 -m pytest tests/test_assumptions_for.py -q`
- Plan artifact whitespace check:
  - `git diff --check -- docs/plans/mathdevmcp-derivation-audit-proposal-master-program-2026-07-06.md docs/plans/mathdevmcp-derivation-audit-proposal-phase-00-baseline-schema-subplan-2026-07-06.md docs/plans/mathdevmcp-derivation-audit-proposal-phase-01-gap-builder-subplan-2026-07-06.md docs/plans/mathdevmcp-derivation-audit-proposal-visible-gated-execution-runbook-2026-07-06.md docs/plans/mathdevmcp-derivation-audit-proposal-gated-overnight-execution-plan-2026-07-06.md docs/plans/mathdevmcp-derivation-audit-proposal-visible-execution-ledger-2026-07-06.md docs/reviews/mathdevmcp-derivation-audit-proposal-plan-review-bundle.md`
- Claude read-only review gate on master, Phase 0, Phase 1 draft, and runbook
  artifacts.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the derivation audit/proposal lane planned with correct baselines, schema direction, gates, artifacts, and review boundaries? |
| Baseline/comparator | Current `derive_from`, `derive_or_refute`, `assumptions_for`, and assumptions report pattern. |
| Primary criterion | Plan artifacts exist, baseline tests pass, review gate agrees or documented Codex fallback agrees, and Phase 1 has enough detail to execute safely. |
| Veto diagnostics | Missing stop conditions; Claude treated as execution authority; detached launch hidden inside visible runbook; plan claims proof capability without backend evidence; no artifact path for phase result. |
| Explanatory diagnostics | Dirty worktree state, current test counts, review comments, and template path correction. |
| Not concluded | No implementation behavior change yet, no proof capability improvement, no launch of detached overnight supervisor. |
| Artifact | Phase 0 result and review bundle/log path. |

## Forbidden Claims And Actions

- Do not claim derivation behavior improved in Phase 0.
- Do not run detached overnight execution during Phase 0.
- Do not use Claude as execution authority.
- Do not send whole large source files to Claude.
- Do not revert unrelated dirty files.
- Do not treat review fallback as equivalent to full Claude review.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only if:

- master program, Phase 0 subplan, Phase 1 draft subplan, visible runbook, and
  launch plan exist;
- baseline tests pass or failures are recorded as pre-existing blockers;
- review gate returns `AGREE` or documented Codex fallback review returns no
  material blocker;
- Phase 0 result records template path correction and launch boundary.

## Stop Conditions

Stop if:

- review gate and Codex fallback both find material blockers in the master
  direction;
- required baseline tests fail in a way that invalidates Phase 1 assumptions;
- user approval is needed for detached launch or network/model access and not
  granted;
- plan artifacts cannot be written without touching unrelated dirty work.
