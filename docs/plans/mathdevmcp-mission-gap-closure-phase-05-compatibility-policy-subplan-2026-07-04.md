# Phase 5 Subplan: Compatibility Policy

Date: 2026-07-04

Status: `COMPLETE_LOCAL_CHECKS_AND_BOUNDED_FALLBACK_REVIEW_AGREED`

## Phase Objective

Define and test the packet compatibility policy so additive fields such as
`agent_handoff` are safe for repo-local consumers while exact-schema external
consumer limits remain explicit.

## Entry Conditions Inherited From Previous Phase

- Phase 4 result records any compatibility observations from regression/replay.
- Phase 4 added an existing-artifact v2 regression guard and did not collect
  new model/API responses.
- Product packet shape after Phases 1-3 is fixed for this lane.
- No unresolved hard-veto regression remains.
- Additive `agent_handoff` behavior is the repo-local consumer path to protect;
  unknown exact-schema external consumers remain an explicit risk.

## Required Artifacts

- Compatibility policy doc or section in an existing operator/developer doc.
- Stable minimal contract tests for required packet fields.
- Optional strict-schema note or future-work item if exact-schema consumers
  need a mode.
- Phase result:
  `docs/plans/mathdevmcp-mission-gap-closure-phase-05-compatibility-policy-result-2026-07-04.md`
- Refreshed Phase 6 readiness-boundary subplan.

## Required Checks, Tests, And Reviews

- Focused compatibility tests, likely in existing packet or CLI/MCP tests.
- `python3 -m pytest tests/test_math_review_packet.py tests/test_prepare_review_packet.py tests/test_mcp_facade.py tests/test_mcp_server.py`
- `git diff --check -- src/mathdevmcp tests docs`
- Bounded Claude read-only review if compatibility wording changes product or
  release boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP state and guard additive packet compatibility without claiming unknown external closed-schema compatibility? |
| Baseline/comparator | Phase 1-4 packet behavior and reviewer note that additive local compatibility is not exact-schema external compatibility. |
| Primary criterion | Docs/tests define stable required fields, allow additive fields for local consumers, and preserve explicit caveat for unknown exact-schema consumers. |
| Veto diagnostics | Claiming universal compatibility, breaking repo-local consumers, hiding additive-field behavior, or changing packet schema without tests. |
| Explanatory diagnostics | Minimal field list, tests touched, external-consumer caveats. |
| Not concluded | No guarantee for unknown external closed-schema consumers unless a strict mode is implemented and tested. |

## Forbidden Claims And Actions

- Do not claim external compatibility without evidence.
- Do not remove additive fields to satisfy hypothetical consumers.
- Do not silently introduce strict schema behavior.
- Do not make release readiness claims from compatibility docs alone.

## Exact Next-Phase Handoff Conditions

Phase 6 may start only if:

- Compatibility policy and tests pass.
- Phase 5 result states remaining exact-schema risk.
- Phase 6 subplan is refreshed with compatibility status and remaining
  blockers.

## Stop Conditions

Stop if:

- Compatibility policy implies a breaking schema or API decision requiring
  human approval.
- Tests reveal current consumers depend on closed schemas.
- A strict schema mode is required but out of scope for this program.
