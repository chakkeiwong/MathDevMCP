# Phase 4 Subplan: CLI, MCP, And Operator Docs

Date: 2026-07-01

Status: `READY_WITH_PHASE_3_VALIDATED_PACKET_REPORT`

## Phase Objective

Expose the packet standard through the appropriate local CLI/MCP/operator
surfaces and document how to use it safely.

## Entry Conditions Inherited From Previous Phase

- Phase 3 integration passes focused tests.
- The packet standard's runtime shape is known.
- Exposure must remain local and diagnostic unless the phase explicitly records
  a narrower claim.
- Claude review gates are waived for this execution window by explicit user
  direction; Codex-only docs/interface review and local checks remain required.

## Required Artifacts

- Phase 4 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-04-cli-mcp-docs-result-2026-07-01.md`.
- Scoped docs changes, likely `docs/mathdevmcp-operator-guide.md` and/or
  README/MCP docs if existing conventions require them.
- Scoped CLI/MCP changes only if supported by existing patterns.
- Focused tests for any changed CLI/MCP surface.
- Updated visible execution ledger.

## Required Checks, Tests, Reviews

- If CLI changes: focused CLI tests or existing CLI smoke tests relevant to the
  changed path.
- If MCP changes: focused MCP facade/server tests relevant to the changed path.
- Always rerun packet tests:
  `python3 -m pytest tests/test_agent_handoff_packet.py tests/test_prepare_review_packet.py tests/test_real_local_high_level_benchmark.py -q`.
- Text review that docs state packet boundaries and non-claims.
- Claude read-only review is waived for this execution window by explicit user
  direction. Codex-only review of operator-facing boundary wording is required
  if docs change materially.

Preferred Phase 4 scope:

- document the reusable `agent_handoff_packet` standard and durable packet
  validation in `docs/mathdevmcp-operator-guide.md`;
- avoid new CLI/MCP commands unless a small existing tested path clearly fits;
- preserve the diagnostic/non-certificate boundary in user-facing wording.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can users and local MCP/CLI callers access or understand the packet standard without boundary confusion? |
| Baseline/comparator | Existing operator docs, CLI, and MCP packet surfaces. |
| Primary criterion | Docs and any exposed interface clearly present packet use, required inputs/outputs, and non-claims; focused tests pass. |
| Veto diagnostics | Docs imply proof/release/scientific validation; CLI/MCP surface bypasses validator; tests absent for changed runtime path; unrelated docs churn. |
| Explanatory diagnostics | Interface inventory, docs snippets, test output, Claude wording findings. |
| Not concluded | Product readiness, public API permanence, downstream-agent improvement. |

## Forbidden Claims Or Actions

- Do not add marketing language or broad capability claims.
- Do not expose a new interface if existing local patterns do not support it
  with focused tests.
- Do not change network, credentials, package installation, or model settings.
- Do not edit unrelated documentation sections.

## Exact Next-Phase Handoff Conditions

Advance to Phase 5 only if:

- all changed CLI/MCP/docs surfaces are covered by local checks;
- operator docs preserve diagnostic/non-certificate boundaries;
- Phase 4 result lists exact user-visible behavior;
- Phase 5 regression scope is refreshed against the final exposed surfaces.

## Stop Conditions

Stop and write a blocker if:

- exposing the standard safely would require a product/API decision outside the
  reviewed plan;
- local tests for changed runtime paths cannot be written without broader
  infrastructure work;
- docs cannot describe the boundary without overclaiming.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 4 result/close record;
3. draft or refresh the Phase 5 subplan;
4. review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
