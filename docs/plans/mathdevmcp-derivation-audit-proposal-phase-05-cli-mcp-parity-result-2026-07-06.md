# Phase 5 Result: CLI/MCP Parity For Derivation Reports

Date: 2026-07-06

Status: `PASSED`

## Objective

Expose `audit_and_propose_derivations` through public CLI and MCP surfaces while
preserving the library workflow contract and proof/refutation boundaries.

## Skeptical Plan Audit

Audit result: `PASSED_WITH_BOUNDARY`.

Boundary preserved:

- Public wrappers delegate to the same library workflow.
- No source edits are applied.
- Wrapper code does not alter validation semantics.
- CLI/MCP exposure does not claim backend proof improvement.

## Artifacts Changed

- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/mcp_server.py`
- `tests/test_derivation_audit_report.py`
- `tests/test_mcp_facade.py`
- `tests/test_mcp_server.py`

## Behavior Added

CLI:

- `audit-and-propose-derivations`

MCP facade/server:

- `audit_and_propose_derivations`

Output contract:

- `derivation_audit_report_result`

## Required Checks

Passed:

- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py -q`
  - `47 passed`
- `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
  - `24 passed`
- `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`
  - passed

Pending until this result file is included:

- `git diff --check -- src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-05-cli-mcp-parity-result-2026-07-06.md`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can agents call the derivation report workflow through CLI/MCP with the same structured contract as the library path? |
| Primary criterion | Passed. CLI writes Markdown; MCP facade and server expose the report with `derivation_audit_report_result`. |
| Veto diagnostics | No wrapper dropped labels, validation boundaries, locations, or tool-use arguments in tested paths. No proof/refutation semantics changed. |
| Not concluded | No backend proof improvement; no automatic source edits; no full-document correctness guarantee. |

## Next Handoff

Phase 6 should improve source target extraction so report workflows can send
smaller equation/proof-obligation targets to deterministic backends instead of
full LaTeX proposition blocks.
