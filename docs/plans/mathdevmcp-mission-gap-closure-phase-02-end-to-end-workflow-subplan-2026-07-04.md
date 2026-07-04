# Phase 2 Subplan: End-To-End Workflow

Date: 2026-07-04

Status: `COMPLETE_LOCAL_CHECKS_AND_READ_ONLY_REVIEW_AGREED`

## Phase Objective

Create one representative workflow from source/code input to compact
agent-facing report, including provenance, obligations or diagnostics, route or
backend evidence/abstention, non-claims, and next action.

## Entry Conditions Inherited From Previous Phase

- Phase 1 result names the CLI/MCP handoff surface to consume:
  - CLI: `python3 -m mathdevmcp.cli prepare-review-packet ... --handoff`;
  - MCP facade/server: `prepare_review_packet` with `handoff=True`;
  - library/high-level packet result: top-level `agent_handoff`.
- Phase 1 review noted that MCP handoff output may include the standard MCP
  success wrapper; Phase 2 should compare semantic handoff fields, not
  byte-identical CLI/library/MCP output.
- Full packet JSON remains available.
- Handoff presentation preserves certification and non-claim boundaries.

## Required Artifacts

- One representative fixture or scripted workflow using existing local
  fixtures where possible and consuming the Phase 1 compact handoff surface.
- Product code only if existing workflows cannot produce a coherent report.
- Focused end-to-end test or CLI smoke test.
- Phase result:
  `docs/plans/mathdevmcp-mission-gap-closure-phase-02-end-to-end-workflow-result-2026-07-04.md`
- Refreshed Phase 3 subplan listing realistic cases and expected handoff
  fields.

## Required Checks, Tests, And Reviews

- Focused end-to-end pytest or CLI smoke test added by this phase.
- `python3 -m pytest tests/test_prepare_review_packet.py tests/test_mcp_facade.py tests/test_mcp_server.py`
- `python3 -m py_compile src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py src/mathdevmcp/prepare_review_packet.py`
- `git diff --check -- src/mathdevmcp tests docs/plans/mathdevmcp-mission-gap-closure-phase-02-end-to-end-workflow-subplan-2026-07-04.md`
- Bounded Claude read-only review if product behavior or workflow claims are
  materially changed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP demonstrate one coherent source/code-to-review-report workflow without overclaiming proof? |
| Baseline/comparator | Phase 1 handoff presentation (`--handoff`/`handoff=True`/top-level `agent_handoff`) plus existing high-level workflows. |
| Primary criterion | A representative workflow produces a compact report with provenance/evidence, gaps/risks, explicit abstention or backend evidence, non-claims, and next action; MCP/CLI/library handoff outputs are semantically consistent. |
| Veto diagnostics | Report claims verification without deterministic backend evidence; source/code provenance is missing; next action is absent; workflow only tests isolated packet formatting. |
| Explanatory diagnostics | Fixture coverage, command used, emitted handoff fields, backend availability notes. |
| Not concluded | No release readiness, broad product capability, semantic code proof, or downstream-agent reliability. |

## Forbidden Claims And Actions

- Do not claim the single workflow generalizes to all mathematical documents.
- Do not fabricate backend evidence.
- Do not require external repositories, package installs, or network fetches
  without explicit approval.
- Do not change default proof status semantics.

## Exact Next-Phase Handoff Conditions

Phase 3 may start only if:

- Phase 2 result records a representative workflow artifact and its command or
  test using the compact handoff surface, with semantic rather than
  byte-identical comparison across CLI/MCP/library if multiple surfaces are
  checked.
- The result identifies which gaps/cases remain uncovered.
- Phase 3 subplan is refreshed with the exact case list and expected fields.
- Required checks pass and any material review converges.

## Stop Conditions

Stop if:

- Existing fixtures cannot support a representative workflow and creating new
  fixtures would require a domain decision from the user.
- The workflow can pass only by weakening proof/abstention boundaries.
- Required checks fail in unrelated dirty files that cannot be safely touched.
