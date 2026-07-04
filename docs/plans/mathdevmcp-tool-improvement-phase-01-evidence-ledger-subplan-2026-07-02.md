# Phase 1 Subplan: Workflow Evidence Ledger

Date: 2026-07-02

Status: `DRAFT_NEXT`

## Phase Objective

Extend high-level workflow results with self-contained evidence-ledger fields
that downstream agents can inspect without rediscovering context, and add a
scoped handoff-packet fixture showing how the ledger improves case-local
reviewability without claiming general downstream usefulness.

## Entry Conditions

- Phase 0 result passed.
- Current high-level workflow contract tests pass.
- No benchmark baseline artifacts are mutated.

## Required Artifacts

- Updated `src/mathdevmcp/high_level_contracts.py` and/or
  `src/mathdevmcp/high_level_workflows.py`.
- Focused tests in `tests/test_high_level_workflows.py` or a new focused test.
- One scoped handoff-packet or benchmark-like fixture exercising the new ledger
  fields on an existing local case without mutating the repaired benchmark
  baseline.
- Phase 1 result record.
- Refreshed Phase 2 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_high_level_workflows.py tests/test_agent_workflows.py`
- `python3 -m pytest tests/test_mcp_surface_sync.py`
- focused fixture check that the evidence ledger appears in a self-contained
  case handoff and preserves source/provenance/non-claim fields
- `git diff --check` over touched implementation/tests/docs
- Claude read-only review of material API/contract changes

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can high-level workflow results carry richer evidence ledgers and expose them in a scoped self-contained handoff fixture without breaking existing contracts? |
| Baseline/comparator | Existing `high_level_workflow_result` contract and tests. |
| Primary criterion | Existing tests pass, new optional fields validate when present, old consumers remain compatible, and the scoped fixture shows case-local provenance/non-claim information that was absent from the baseline envelope. |
| Veto diagnostics | Mandatory breaking schema change; empty evidence fields accepted as meaningful; non-claim boundaries weakened; packet polish or schema conformance treated as proof or general usefulness. |
| Explanatory diagnostics | Test coverage for optional fields, validation failures, and the scoped fixture diff against the baseline envelope. |
| Not concluded | No proof correctness, release readiness, product capability, public benchmark validity, broad downstream-agent usefulness, or general model reliability. |

## Forbidden Claims/Actions

- Do not make optional fields required unless all call sites are updated and
  reviewed.
- Do not treat richer envelope fields as backend evidence.
- Do not claim schema/test success establishes downstream-agent usefulness
  beyond the scoped fixture.
- Do not change benchmark scores.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if the richer result envelope is validated, existing
workflow tests pass, the scoped fixture records case-local usefulness evidence
without overclaiming, and Phase 2 can reuse the ledger without schema ambiguity.

## Stop Conditions

Stop if compatibility breaks across MCP/server/tool tests, if schema changes
require broad refactors outside this phase, or if non-claim validation weakens.
