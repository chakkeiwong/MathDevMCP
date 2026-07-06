# Phase 5 Subplan: Public Surface Regression

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Ensure CLI/MCP public surfaces continue to expose the improved report workflow
and preserve output contract, extracted target fields, and validation boundary.

## Entry Conditions Inherited From Previous Phase

- Phase 4 risky-debt v2 experiment passed or recorded acceptable limitation.
- CLI/MCP currently expose `audit_and_propose_derivations`.

## Required Artifacts

- Updated public-surface tests if needed:
  - `tests/test_derivation_audit_report.py`
  - `tests/test_mcp_facade.py`
  - `tests/test_mcp_server.py`
- Phase 5 result:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-05-public-surface-regression-result-2026-07-06.md`

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py -q`
- `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py -q`
- `python3 -m compileall -q src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`
- `git diff --check -- tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-05-public-surface-regression-result-2026-07-06.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do public surfaces preserve improved extracted-obligation reporting? |
| Baseline/comparator | Phase 5 of prior derivation audit/proposal lane. |
| Primary criterion | CLI/MCP tests pass and assert output contract plus extracted target coverage. |
| Veto diagnostics | Public output drops extracted targets, validation, locations, or tool uses. |
| Explanatory diagnostics | Test counts and command smoke result. |
| Not concluded | No release readiness or scientific correctness. |
| Artifact | Tests/result. |

## Forbidden Claims/Actions

- Do not broaden public API beyond necessary regression support.
- Do not edit source docs.
- Do not change route semantics to satisfy public wrappers.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 only if:

- public-surface checks pass;
- final review bundle can summarize implementation and residual limitations.

## Stop Conditions

Stop if:

- MCP wrapper changes require a broader product decision;
- public output schema would break existing tests without reviewed migration.
