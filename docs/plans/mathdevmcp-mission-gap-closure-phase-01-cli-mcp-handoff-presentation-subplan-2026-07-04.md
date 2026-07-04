# Phase 1 Subplan: CLI/MCP Handoff Presentation

Date: 2026-07-04

Status: `COMPLETE_LOCAL_CHECKS_AND_READ_ONLY_REVIEW_AGREED`

## Phase Objective

Make the newly added `agent_handoff` easy for coding agents to consume through
CLI/MCP without hiding the full JSON packet or weakening diagnostic boundaries.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result exists and records local artifact checks plus read-only review
  agreement.
- Master program and visible runbook are the active execution authority.
- `agent_handoff` product-improvement result is complete and reviewed.

## Required Artifacts

- Minimal implementation in current CLI/MCP packet surfaces, expected targets:
  - `src/mathdevmcp/cli.py`
  - `src/mathdevmcp/mcp_facade.py`
  - `src/mathdevmcp/mcp_server.py`
  - optional helper module if local code shape warrants it.
- Focused tests in:
  - `tests/test_prepare_review_packet.py`
  - `tests/test_mcp_facade.py`
  - `tests/test_mcp_server.py`
  - `tests/test_release_smoke.py`
- Phase result:
  `docs/plans/mathdevmcp-mission-gap-closure-phase-01-cli-mcp-handoff-presentation-result-2026-07-04.md`
- Refreshed Phase 2 subplan if Phase 1 changes the expected workflow surface.

## Required Checks, Tests, And Reviews

- `python3 -m pytest tests/test_prepare_review_packet.py`
- `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py`
- `python3 -m pytest tests/test_release_smoke.py::test_cli_prepare_review_packet_preserves_phase6_packet_fields`
- `python3 -m py_compile src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py src/mathdevmcp/math_review_packet.py src/mathdevmcp/prepare_review_packet.py`
- `git diff --check -- src/mathdevmcp tests docs/plans/mathdevmcp-mission-gap-closure-phase-01-cli-mcp-handoff-presentation-subplan-2026-07-04.md`
- Bounded Claude read-only review for material implementation/result diffs.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can CLI/MCP expose the review handoff compactly while preserving full diagnostic packet access and proof boundaries? |
| Baseline/comparator | Current `prepare-review-packet` CLI and `prepare_review_packet` MCP return full JSON containing nested `agent_handoff`. |
| Primary criterion | A coding agent can request or access compact handoff content from CLI/MCP, and tests show non-claims plus certification boundary remain visible. |
| Veto diagnostics | Full JSON output is removed; handoff omits non-claim/certification boundary; status/certification semantics change; MCP/CLI wrapper breaks; docs-only change without product surface. |
| Explanatory diagnostics | Output shape, test snapshots/assertions, whether helper code is reusable for Phase 2. |
| Not concluded | No downstream usefulness promotion, release readiness, proof certificate, or external schema compatibility guarantee. |

## Forbidden Claims And Actions

- Do not claim the formatted handoff is proof.
- Do not remove full JSON packet behavior.
- Do not change scoring criteria or run new model benchmarks.
- Do not break existing CLI/MCP command names.
- Do not modify unrelated dirty files.

## Exact Next-Phase Handoff Conditions

Phase 2 may start only if:

- Compact CLI/MCP handoff behavior is implemented or a justified no-op result
  explains why existing behavior already satisfies the contract.
- Required local checks pass.
- Material result review returns `VERDICT: AGREE` or no material review is
  justified and the result says why.
- Phase 1 result states the exact command/tool surface Phase 2 should consume.
- Phase 2 subplan is refreshed to use that surface.

## Stop Conditions

Stop if:

- Implementation would require a breaking CLI/MCP API change not already
  approved.
- The only feasible change is docs without product workflow effect.
- Local tests reveal a deeper packet schema issue requiring a separate design
  decision.
- Claude and Codex do not converge after five review rounds for the same
  material issue.
