# Phase 5 Result: Public Surface Regression

Date: 2026-07-06

Status: `PASSED`

## Objective

Ensure CLI/MCP public surfaces continue to expose the improved report workflow
and preserve output contract, extracted target fields, and validation boundary.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Do public surfaces preserve improved extracted-obligation reporting? |
| Baseline/comparator | Prior derivation audit/proposal public surface with `audit_and_propose_derivations`. |
| Primary criterion | Passed: CLI/MCP tests pass; MCP facade now asserts route plans and extracted target coverage. |
| Veto diagnostics | Passed: public output preserves metadata contract, extracted targets, route plans, validation, locations, and tool uses. |
| Explanatory diagnostics | 49 public-surface tests passed; 8 extraction/planner tests passed. |
| Not concluded | No release readiness or scientific correctness. |
| Artifact | Updated `tests/test_mcp_facade.py` and this result record. |

## Implementation Summary

- No public wrapper implementation change was required:
  - CLI already passes `root`, `labels`, `givens`, `assumptions`, `backend`, and
    `output_path`;
  - MCP facade and MCP server already forward labels/root/output into
    `audit_and_propose_derivations`.
- Updated MCP facade regressions so direct derivation reports expect
  `plan_backend_routes` as the first tool-use record.
- Added an MCP facade label-path regression that checks extracted target
  coverage and the backend route-plan boundary for `prop:risky-pricing`.

## Checks Run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py -q` | Passed: 49 passed. |
| `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py -q` | Passed: 8 passed. |
| `python3 -m compileall -q src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py` | Passed. |

## Boundary

The public contract name remains `derivation_audit_report_result`. The richer
fields are additive report content; no release readiness or scientific
correctness claim is made.

## Next-Phase Handoff

Proceed to Phase 6 because:

- public-surface checks pass;
- final review/handoff can summarize implementation and residual limitations.
