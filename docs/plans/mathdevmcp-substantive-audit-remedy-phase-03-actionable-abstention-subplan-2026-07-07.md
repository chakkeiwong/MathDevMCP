# Phase 3 Subplan: Actionable Abstention And Domain Obligations

Date: 2026-07-07

Status: `DRAFT_PENDING_PHASE_2`

## Phase Objective

Make abstention useful by adding deterministic obligation extractors for common
document-audit patterns: expectations, NPV/accounting identities, Bellman/value
recursions, OBC complementarity, fixed-point scope, and notation/unit hazards.

## Entry Conditions

- Phase 2 passed, so richer payloads will be preserved and rendered correctly.

## Required Artifacts

- Domain/actionable-abstention helper module.
- Integration into `audit_and_propose_fix` and/or `math_document_rigor`.
- Tests for NPV, Bellman, OBC, fixed-point, and notation hazard payloads.
- Phase 3 result record.

## Required Checks/Tests/Reviews

- Focused tests for abstention payloads and suggested safe wording.
- Existing `audit_and_propose_fix` tests.
- `tests/test_math_document_rigor.py`.
- `git diff --check`.
- Review next Phase 4 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do inconclusive/not-encodable results identify missing obligations and smallest next audit? |
| Baseline/comparator | Generic "backend_not_encodable" or "manual formalization required" diagnostics. |
| Primary criterion | Abstention entries include blocker kind, missing obligations, next audit, safe wording, and nonclaim boundary. |
| Veto diagnostics | Backend abstention without missing obligations; OBC max relation treated as full mask validation; expectation equation without integrability/measurability obligations; Bellman recursion without state/action/transition/reward obligations. |
| Explanatory diagnostics | Parsed terms, obligation classes, suggested wording, route limits. |
| Not concluded | Full solution of macro-finance, NPV, OBC, or Bellman systems. |

## Forbidden Claims/Actions

- Do not claim domain routers solve the model.
- Do not claim exact official mask validation from algebra alone.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 only if actionable abstention payloads appear in report
entries that cannot be concretely repaired.

## Stop Conditions

Stop if domain router output would be misleading without a larger ontology. The
stop handoff must include the minimal misleading example, the missing ontology
concept, and the next design question for human review.
