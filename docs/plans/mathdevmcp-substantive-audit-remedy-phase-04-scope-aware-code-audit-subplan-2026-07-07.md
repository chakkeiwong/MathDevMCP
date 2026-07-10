# Phase 4 Subplan: Scope-Aware Math-To-Code Audit

Date: 2026-07-07

Status: `DRAFT_PENDING_PHASE_3`

## Phase Objective

Refine `audit_math_to_code` so scope mismatches, especially function-level
math versus value-level code snippets, are distinguished from formula
contradictions.

## Entry Conditions

- Phase 3 passed, so abstention payload vocabulary is available.

## Required Artifacts

- Updated `audit_math_to_code` classification.
- Tests for fixed-point instance-only likelihood bridge.
- Updated high-level contract/status validation if needed.
- Phase 4 result record.

## Required Checks/Tests/Reviews

- `tests/test_audit_math_to_code.py`.
- High-level contract tests affected by new status.
- MCP facade/server surface tests if output contract changes.
- `git diff --check`.
- Review next Phase 5 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the code audit separate scope mismatch from formula mismatch? |
| Baseline/comparator | Current `structural_mismatch` for D447 likelihood bridge. |
| Primary criterion | Value-level snippets against function-level math return a scope-specific unverified status with matched terms, missing variable, supports/does-not-support, and safe wording. |
| Veto diagnostics | Formula contradiction wording for scope mismatch; structural match promoted to proof; lost nonclaim boundary. |
| Explanatory diagnostics | Matched terms, missing arguments, extra/missing code terms. |
| Not concluded | Code correctness over all parameter values. |

## Forbidden Claims/Actions

- Do not execute arbitrary code.
- Do not treat snippet-level agreement as function-level proof.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 only if D447-style likelihood bridge receives a
scope-specific diagnostic instead of generic structural mismatch.

## Stop Conditions

Stop if current tokenization cannot identify matched terms robustly enough for
the scoped status.
