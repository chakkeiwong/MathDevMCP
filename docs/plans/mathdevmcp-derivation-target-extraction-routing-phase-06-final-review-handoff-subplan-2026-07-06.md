# Phase 6 Subplan: Final Review And Handoff

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Run final focused regression, review claims and residual limitations, update the
mission/reset handoff, and stop with a clear artifact list.

## Entry Conditions Inherited From Previous Phase

- Phase 5 passed.
- V2 report and tests exist.

## Required Artifacts

- Phase 6 result:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-06-final-review-handoff-result-2026-07-06.md`
- Optional final review bundle/result under `docs/reviews`.
- Reset memo update if needed:
  `docs/plans/mathdevmcp-mission-reset-memo.md`

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
- `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py -q`
- `git diff --check`
- Claude read-only final review if approval/availability permits; otherwise
  Codex fallback review with explicit limitation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the extraction/routing lane ready for handoff with accurate claims and artifacts? |
| Baseline/comparator | Master program objectives and all phase result artifacts. |
| Primary criterion | Tests/diff pass; final claims match evidence; residual limitations are explicit. |
| Veto diagnostics | Unsupported scientific claim; missing result artifact; failed public-surface test; unrecorded review blocker. |
| Explanatory diagnostics | Final test counts, review status, artifact list. |
| Not concluded | No source edits, no proof of risky-debt note, no release readiness. |
| Artifact | Final result and handoff. |

## Forbidden Claims/Actions

- Do not commit/push unless explicitly requested.
- Do not edit unrelated dirty work.
- Do not claim Claude review if fallback was used.

## Exact Next-Phase Handoff Conditions

No next phase in this program. Handoff should state:

- final phase reached;
- status;
- artifacts;
- tests run;
- unresolved blockers;
- what was not concluded.

## Stop Conditions

Stop if:

- final tests fail and cannot be repaired within scoped changes;
- review finds a material blocker needing human decision;
- git state requires destructive action.
