# Phase 5 Subplan: CLI/MCP Parity For Derivation Reports

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Expose `audit_and_propose_derivations` through the existing CLI and MCP facade
so agents can request the report workflow directly.

## Entry Conditions Inherited From Previous Phase

- Phase 4 result is `PASSED_WITH_RECORDED_LIMITATION`.
- Library workflow `audit_and_propose_derivations` exists and generated a
  risky-debt report.
- Focused derivation report tests pass.

## Required Artifacts

- Updated `src/mathdevmcp/cli.py`.
- Updated `src/mathdevmcp/mcp_facade.py`.
- Updated `src/mathdevmcp/mcp_server.py` if server wrappers are explicit.
- Updated tests:
  - `tests/test_mcp_facade.py`
  - `tests/test_mcp_server.py` if server wrapper is added.
  - optionally `tests/test_derivation_audit_report.py` for CLI smoke.
- Phase 5 result record:
  `docs/plans/mathdevmcp-derivation-audit-proposal-phase-05-cli-mcp-parity-result-2026-07-06.md`

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py -q`
- `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
- `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`
- `git diff --check -- src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py tests/test_derivation_audit_report.py tests/test_mcp_facade.py tests/test_mcp_server.py docs/plans/mathdevmcp-derivation-audit-proposal-phase-05-cli-mcp-parity-result-2026-07-06.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can agents call the derivation report workflow through public CLI/MCP surfaces with the same structured contract as the library path? |
| Baseline/comparator | Existing `audit_and_propose_assumptions` CLI/MCP pattern. |
| Primary criterion | CLI and MCP facade expose `audit_and_propose_derivations`, return `derivation_audit_report_result`, accept direct targets and root/labels, and preserve output-path behavior. |
| Veto diagnostics | Public wrapper drops labels, source locations, validation boundaries, or tool-use arguments; wrapper changes proof/refutation status semantics; MCP/server tests fail. |
| Explanatory diagnostics | Tool spec metadata, output contract, CLI smoke output, server wrapper status. |
| Not concluded | No backend proof improvement; no automatic source edits; no guarantee of full-document correctness. |
| Artifact | Updated public surfaces, tests, Phase 5 result. |

## Forbidden Claims And Actions

- Do not change the library workflow semantics.
- Do not add broad or unrelated CLI/MCP refactors.
- Do not expose a command that silently edits the audited document.
- Do not claim CLI/MCP parity proves the report quality beyond tested surfaces.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 only if:

- public surfaces pass tests;
- generated risky-debt report remains valid;
- Phase 6 subplan focuses on smaller equation/proof-obligation extraction for
  backend proof attempts.

## Stop Conditions

Stop if:

- MCP server wrappers require a broader contract change than the facade;
- CLI parser changes conflict with existing commands;
- public exposure would require changing report semantics to satisfy wrappers.
