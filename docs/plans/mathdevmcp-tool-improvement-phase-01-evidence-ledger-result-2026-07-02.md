# Phase 1 Result: Workflow Evidence Ledger

Date: 2026-07-02

Status: `PASSED`

## Phase Objective

Extend high-level workflow results with self-contained evidence-ledger fields
that downstream agents can inspect without rediscovering context, and add a
scoped handoff-packet fixture showing how the ledger improves case-local
reviewability without claiming general downstream usefulness.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | High-level workflow results can carry richer evidence ledgers and expose them in a scoped fixture without breaking existing contracts. |
| Baseline/comparator | Existing `high_level_workflow_result` contract and tests. |
| Primary criterion | Passed after repair: existing tests pass, optional fields validate when present, legacy projections can omit producer-emitted ledgers, extension metadata is preserved in ledger items, and the scoped fixture records case-local provenance/non-claim information absent from the baseline envelope. |
| Veto diagnostics | No breaking schema requirement, no benchmark score change, and no schema/fixture success promoted to general usefulness or proof. |
| Explanatory diagnostics | Focused contract tests, workflow wrapper tests, MCP surface sync, and scoped fixture assertion. |
| Not concluded | No proof correctness, release readiness, product capability, public benchmark validity, broad downstream-agent usefulness, or general model reliability. |

## Artifacts

- `src/mathdevmcp/high_level_contracts.py`
- `src/mathdevmcp/derive_from.py`
- `src/mathdevmcp/prove_or_counterexample.py`
- `src/mathdevmcp/assumptions_for.py`
- `src/mathdevmcp/debug_derivation.py`
- `src/mathdevmcp/audit_math_to_code.py`
- `src/mathdevmcp/prepare_review_packet.py`
- `tests/test_high_level_contracts.py`
- `tests/test_high_level_workflows.py`
- Refreshed Phase 2 subplan:
  `docs/plans/mathdevmcp-tool-improvement-phase-02-assumption-taxonomy-subplan-2026-07-02.md`

## Local Checks

| Check | Result |
| --- | --- |
| `python3 -m pytest tests/test_high_level_contracts.py tests/test_high_level_workflows.py tests/test_agent_workflows.py tests/test_mcp_surface_sync.py` | Passed before review repair: 35 tests. |
| `python3 -m pytest tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py` | Passed: 32 tests. |
| `git diff --check` over touched Phase 1 implementation/tests/docs | Passed. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 2 | Passed | No veto triggered | Ledger improves case-local reviewability only; downstream-agent usefulness still requires benchmark evidence | Implement scoped assumption route taxonomy | No broad usefulness or proof claim |

## Phase 2 Handoff

Phase 2 may reuse `evidence_ledger` for route-category provenance. It must use
a predeclared scoped taxonomy oracle for benchmark-like cases and must not claim
global minimal assumptions or general semantic correctness beyond that oracle.
