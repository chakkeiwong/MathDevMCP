# Phase 2 Subplan: CLI And MCP Exposure

Date: 2026-07-07

Status: `EXECUTED`

## Phase Objective

Expose the core document-rigor workflow through CLI, MCP facade, and FastMCP
server using the same library contract.

## Entry Conditions

- Phase 1 library tests pass.
- Core workflow contract is stable enough for interface exposure.

## Required Artifacts

- CLI command in `src/mathdevmcp/cli.py`.
- MCP facade handler/spec in `src/mathdevmcp/mcp_facade.py`.
- FastMCP server wrapper in `src/mathdevmcp/mcp_server.py`.
- Interface tests.
- Phase 2 result record.

## Required Checks/Tests/Reviews

- CLI smoke test writing JSON/Markdown to a temp directory.
- MCP facade test for `plan_math_document_rigor_audit` and/or
  `audit_math_document_rigor`.
- FastMCP wrapper test if local patterns support it.
- `python3 -m pytest -q` on focused new and surface-sync tests.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can agents consume the workflow through stable CLI/MCP names without losing the library evidence contract? |
| Baseline/comparator | Existing high-level workflow CLI/MCP exposure patterns. |
| Primary criterion | CLI and MCP return the same contract shape, write requested artifacts, and appear in tool matrix/surface tests. |
| Veto diagnostics | Interface omits backend provenance; tool name not discoverable; Markdown/JSON output not reproducible; CLI claims proof/product/science. |
| Explanatory diagnostics | CLI output, MCP facade/server results, surface-sync tests. |
| Not concluded | No improvement to mathematical content beyond access path; no proof/document/scientific/product claim. |

## Forbidden Claims/Actions

- Do not create an alias-only wrapper without tests.
- Do not change existing tool semantics unexpectedly.
- Do not hide partial coverage in CLI/MCP output.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only if CLI/MCP focused tests pass and the tool can write
both JSON and Markdown reports for a small fixture.

## Stop Conditions

Stop if interface exposure would require broad registry refactoring or if the
library contract changes materially enough to require Phase 1 redesign.
