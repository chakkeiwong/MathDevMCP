# Phase 0 Subplan: Plan And Review Gate

Date: 2026-07-06

Status: `DRAFT`

## Phase Objective

Create the master program, phase subplans, visible runbook, overnight execution
plan, ledger, and compact review bundle for the derivation target extraction and
backend routing lane.

## Entry Conditions Inherited From Previous Phase

- Prior derivation audit/proposal Phase 5 passed.
- `audit_and_propose_derivations` exists and is exposed through CLI/MCP.
- Risky-debt report exists and records full-block target limitation.

## Required Artifacts

- Master program:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-master-program-2026-07-06.md`
- Phase subplans 0 through 6 under `docs/plans`.
- Visible runbook:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-visible-gated-execution-runbook-2026-07-06.md`
- Gated overnight plan:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-gated-overnight-execution-plan-2026-07-06.md`
- Execution ledger:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-visible-execution-ledger-2026-07-06.md`
- Review bundle:
  `docs/reviews/mathdevmcp-derivation-target-extraction-routing-plan-review-bundle.md`
- Phase 0 result:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-00-plan-review-result-2026-07-06.md`

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
- `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py -q`
- `git diff --check -- docs/plans/mathdevmcp-derivation-target-extraction-routing-* docs/reviews/mathdevmcp-derivation-target-extraction-routing-plan-review-bundle.md`
- Claude read-only review gate on compact bundle if approved/available.
- Codex fallback review if Claude is unavailable or approval is rejected.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the target extraction/routing program planned with correct gates, evidence contracts, artifacts, and boundaries? |
| Baseline/comparator | Prior derivation audit/proposal program and current risky-debt report limitation. |
| Primary criterion | Plan artifacts exist, local baseline checks pass, review gate agrees or fallback review records no material blocker. |
| Veto diagnostics | Missing stop conditions; Claude as executor; no repair loop; detached launch without approval; no checks that answer the phase question. |
| Explanatory diagnostics | Review status, baseline test counts, diff check. |
| Not concluded | No implementation behavior change in Phase 0. |
| Artifact | Phase 0 result and review record. |

## Forbidden Claims/Actions

- Do not implement extractor/router in Phase 0.
- Do not run detached overnight execution without explicit approval.
- Do not edit the risky-debt LaTeX source.
- Do not claim Claude review happened if it is blocked.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only if:

- plan artifacts exist;
- required baseline checks pass or blockers are recorded;
- Phase 1 subplan is reviewed for consistency and boundary safety;
- Claude or fallback review status is recorded.

## Stop Conditions

Stop if:

- Claude review/export approval is required and rejected, and Codex fallback
  finds a material blocker;
- local baseline tests fail in a way unrelated to this lane and no safe
  progress-making path exists;
- the plan requires external installs, credentials, or destructive actions.
