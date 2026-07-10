# Phase 2 Result: CLI And MCP Exposure

Date: 2026-07-07

Status: `PASSED`

## Objective

Expose the document-rigor audit workflow through CLI, MCP facade, and FastMCP
server without changing the library evidence contract.

## Implementation Artifacts

- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/mcp_server.py`
- `tests/test_math_document_rigor_interfaces.py`

## Interface Names

- CLI: `plan-math-document-rigor-audit`
- CLI: `audit-math-document-rigor`
- MCP facade: `plan_math_document_rigor_audit`
- MCP facade: `audit_math_document_rigor`
- FastMCP wrappers with the same preferred names.

## Local Checks

`python3 -m pytest -q tests/test_math_document_rigor_interfaces.py`

- Result: `3 passed in 87.10s`

`python3 -m mathdevmcp.cli plan-math-document-rigor-audit docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex --max-labels 2`

- Result: succeeded.
- Exact target file localized `224` equation rows.
- Selected labels: `eq:proposal-objective`, `eq:state-kernel-panel`.

`git diff --check -- src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py tests/test_math_document_rigor_interfaces.py`

- Result: passed.

## Gate Assessment

Primary criterion:

- Met.

Veto diagnostics:

- Interface omits backend provenance: not observed.
- Tool name not discoverable: MCP facade test covers names/contracts.
- Markdown/JSON output not reproducible: CLI test writes both.
- CLI claims proof/product/science: not present.

## Non-Claims

- Interface exposure does not prove any document.
- Interface exposure does not certify scientific/product/release readiness.
- LeanDojo remains proof-search evidence only.

## Next Handoff

Proceed to Phase 3: apply the tool to the credit-card NPV document.
