# Phase 0 Subplan: Governed Launch

Date: 2026-07-04

Status: `COMPLETE`

## Phase Objective

Create, locally check, and read-only review the master program, visible gated
runbook, phase subplans, execution ledger, stop handoff, and compact review
bundle before any product implementation phase begins.

## Entry Conditions Inherited From Previous Phase

- Mission spine exists and was read-only reviewed:
  `docs/plans/mathdevmcp-mission-charter.md`.
- Anti-drift gate exists:
  `docs/plans/mathdevmcp-anti-drift-gate.md`.
- Evidence-to-implementation ledger exists:
  `docs/plans/mathdevmcp-evidence-to-implementation-ledger.md`.
- Prior product lane completed:
  `docs/plans/mathdevmcp-review-handoff-packet-product-improvement-result-2026-07-04.md`.

## Required Artifacts

- Master program:
  `docs/plans/mathdevmcp-mission-gap-closure-master-program-2026-07-04.md`
- Visible runbook:
  `docs/plans/mathdevmcp-mission-gap-closure-visible-gated-execution-plan-2026-07-04.md`
- Execution ledger:
  `docs/plans/mathdevmcp-mission-gap-closure-visible-execution-ledger-2026-07-04.md`
- Stop handoff:
  `docs/plans/mathdevmcp-mission-gap-closure-visible-stop-handoff-2026-07-04.md`
- Phase subplans 0 through 6.
- Compact review bundle:
  `docs/reviews/mathdevmcp-mission-gap-closure-program-review-bundle-2026-07-04.md`
- Phase result:
  `docs/plans/mathdevmcp-mission-gap-closure-phase-00-governed-launch-result-2026-07-04.md`

## Required Checks, Tests, And Reviews

- `git diff --check -- docs/plans/mathdevmcp-mission-gap-closure-master-program-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-visible-gated-execution-plan-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-visible-execution-ledger-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-visible-stop-handoff-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-phase-00-governed-launch-subplan-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-phase-01-cli-mcp-handoff-presentation-subplan-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-phase-02-end-to-end-workflow-subplan-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-subplan-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-subplan-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-phase-05-compatibility-policy-subplan-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-phase-06-release-readiness-boundary-subplan-2026-07-04.md docs/reviews/mathdevmcp-mission-gap-closure-program-review-bundle-2026-07-04.md`
- Bounded Claude read-only review gate on the compact program bundle.
- If Claude returns `REVISE`, patch the same artifact visibly and rerun the
  focused local check plus review, up to five rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the mission gap closure program executable, bounded, and aligned with the product mission? |
| Baseline/comparator | Current mission spine and completed `agent_handoff` product-improvement result. |
| Primary criterion | Required artifacts exist, contain phase gates and stop conditions, pass whitespace checks, and receive `VERDICT: AGREE` from bounded read-only review. |
| Veto diagnostics | Claude is assigned execution authority; runbook launches detached agents; subplans lack evidence contracts; benchmark score is treated as product success; stop conditions are missing. |
| Explanatory diagnostics | Review notes, local diff check, phase index completeness. |
| Not concluded | No implementation is complete beyond planning; no release/product/scientific/proof claim is established. |

## Forbidden Claims And Actions

- Do not claim product gap closure from Phase 0.
- Do not launch detached or nested agents.
- Do not send whole repository context to Claude.
- Do not treat Claude agreement as authorization for release, product
  capability, scientific, funding, model-file, or runtime boundaries.
- Do not modify code in Phase 0 except to fix plan artifact generation defects.

## Exact Next-Phase Handoff Conditions

Phase 1 may start only if:

- Phase 0 result is written.
- Local artifact check passes.
- Bounded Claude read-only review returns `VERDICT: AGREE`.
- Phase 1 subplan is present and, if modified by Phase 0 repairs, refreshed.
- Execution ledger records Phase 0 gate status as passed.

## Stop Conditions

Stop and write the stop handoff if:

- Claude returns `REVISE` for the same blocker after five review rounds.
- Review or local checks find a material boundary flaw that cannot be repaired
  without human direction.
- Continuing would require unapproved external model/API use beyond read-only
  review gates.
- The user changes project direction.
