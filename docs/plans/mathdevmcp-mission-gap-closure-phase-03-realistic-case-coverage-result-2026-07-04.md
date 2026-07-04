# Phase 3 Result: Realistic Case Coverage

Date: 2026-07-04

Status: `COMPLETE_LOCAL_CHECKS_AND_READ_ONLY_REVIEW_AGREED`

Subplan:

- `docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-subplan-2026-07-04.md`

## Phase Objective Result

Phase 3 added compact handoff coverage for realistic hard cases. The phase also
found and repaired an actual handoff surface bug: high-level workflow actions
use `code`, while low-level packet actions use `kind`; compact handoff
`next_actions` now normalizes both into a stable `kind`.

## Product Capability Changed

Compact review handoffs now preserve action identity across high-level and
low-level evidence sources. This makes handoffs more reliable for agents that
consume `next_actions` directly.

## Evidence Changed

Added/updated test:

- `tests/test_prepare_review_packet.py::test_prepare_review_packet_handoff_covers_realistic_case_matrix`

Cases covered:

| Case | Expected handoff behavior |
| --- | --- |
| Missing assumptions | Gap ledger includes `missing_assumptions`; action includes `human_review`. |
| Route gap | Gap ledger includes `gap_found`; action includes `human_review`. |
| Backend unavailable | Gap ledger includes `backend_unavailable`; action includes `configure_backend`. |
| Not encodable | Gap ledger includes `not_encodable`; action includes `formalize_claim`. |
| Math/code mismatch | Gap ledger includes `structural_mismatch`; action includes `human_review`. |
| Notation conflict | Packet remains `needs_human_review`; action includes `human_review` or conservative fallback. |
| Deterministic refutation | Low-level packet is `blocked_by_refutation`; packet remains a diagnostic handoff. |
| Deterministic verification | Low-level packet is `review_ready`; packet remains a diagnostic handoff. |

## Repair Record

Initial check failed because compact handoff `next_actions` projected only
`kind`, while high-level workflow actions use `code`.

Repair:

- Added `_action_kind(action)` in `src/mathdevmcp/math_review_packet.py`.
- `_action_target(action)` now also accepts `description` and `code`.
- Compact handoff action projection now emits a stable `kind` for high-level
  and low-level actions.

Focused repair checks passed after expectations were aligned with existing
conservative actions.

First read-only review returned `REVISE` because the written Phase 3 scope
included backend-unavailable coverage, but the bounded test covered only
not-encodable behavior. The repair added an explicit validated
`backend_unavailable` high-level evidence fixture to the case matrix. This is a
local deterministic fixture and does not depend on whether Lean, Sage, or any
external backend happens to be installed.

## Local Checks Run

Commands and results:

- `python3 -m pytest tests/test_prepare_review_packet.py::test_prepare_review_packet_handoff_covers_realistic_case_matrix tests/test_math_review_packet.py tests/test_prepare_review_packet.py`
  - initial result after action-normalization repair: `13 passed in 0.30s`
  - result after backend-unavailable coverage repair: `13 passed in 0.27s`
- `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py`
  - initial result: `42 passed in 83.39s`
  - result after backend-unavailable coverage repair: `42 passed in 83.11s`
- `python3 -m py_compile src/mathdevmcp/math_review_packet.py src/mathdevmcp/prepare_review_packet.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`
  - result: passed
- `git diff --check -- src/mathdevmcp tests docs/plans/mathdevmcp-mission-gap-closure-phase-03-realistic-case-coverage-subplan-2026-07-04.md`
  - result: passed

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Phase 3 complete: local checks passed after focused repairs and bounded read-only review r2 agreed. |
| Primary criterion status | Passed locally: selected hard cases preserve status, gaps/risks, non-claims, and next actions through compact handoff. |
| Veto diagnostic status | No veto remains: false verification was not introduced; non-claim/certification boundaries remain visible. |
| Main uncertainty | Case coverage is local and focused; it does not prove comprehensive theorem-proving ability or downstream-agent reliability. |
| Next justified action | Advance to Phase 4 v2 regression guard using existing artifacts only unless human approval is requested. |
| Not concluded | No release readiness, public benchmark validity, scientific validation, broad product readiness, semantic code proof, or model reliability. |

## Phase 4 Subplan Refresh

Phase 4 was refreshed to record:

- Phase 3 repaired compact handoff action normalization;
- new model/API response collection is not authorized by Phase 4;
- if new collection is needed, Phase 4 must stop and request explicit approval.

## Regression Guard

Keep the realistic case matrix as a guard that compact handoff output preserves
action identity and conservative status boundaries across hard cases.

## Read-Only Review Trail

First Phase 3 review:

- `REVIEW_STATUS=revise`
- `VERDICT=REVISE`
- `RUN_DIR=/home/chakwong/python/MathDevMCP/.claude_reviews/20260704-043604-mathdevmcp-mission-gap-closure-phase-03-sonnet-r1`
- Material finding: backend-unavailable coverage was promised by the subplan
  but missing from the test/result.

Repair:

- Added explicit backend-unavailable case to
  `tests/test_prepare_review_packet.py::test_prepare_review_packet_handoff_covers_realistic_case_matrix`.
- Reran focused packet and MCP wrapper checks.

Second Phase 3 review:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- `RUN_DIR=/home/chakwong/python/MathDevMCP/.claude_reviews/20260704-044348-mathdevmcp-mission-gap-closure-phase-03-sonnet-r2`
- `SUMMARY_JSON=/home/chakwong/python/MathDevMCP/.claude_reviews/20260704-044348-mathdevmcp-mission-gap-closure-phase-03-sonnet-r2/status.json`
- Reviewer confirmed the backend-unavailable repair closes the r1 coverage
  mismatch for Phase 3's handoff-surface goal.

## Forbidden Claims Retained

This result does not claim:

- proof or semantic implementation correctness;
- release readiness;
- downstream-agent reliability;
- broad product readiness;
- public benchmark validity;
- scientific validation;
- Claude as execution authority.
