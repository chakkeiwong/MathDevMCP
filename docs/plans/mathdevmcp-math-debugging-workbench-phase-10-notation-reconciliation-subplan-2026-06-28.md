# Phase 10 Subplan: Notation Reconciliation

## Phase Objective

Implement notation and convention reconciliation across sections, including
symbols, aliases, signs, time indices, row/column orientation, domains, and
units where explicit.

## Entry Conditions Inherited From Previous Phase

- Claim classification exists.
- Existing notation/convention helpers remain available.

## Required Artifacts

- `src/mathdevmcp/notation_reconciliation.py`
- `tests/test_notation_reconciliation.py`
- Phase 10 result record.
- Refreshed Phase 11 subplan.

## Required Checks, Tests, Reviews

- Tests for sign reversal, alias conflict, time-index mismatch, row/column
  mismatch, unresolved alias.
- Existing notation/conventions tests if present.
- `git diff --check`.
- Claude review if boundary-sensitive.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo detect likely notation/convention conflicts without silently merging symbols? |
| Baseline/comparator | Existing notation and convention modules plus document label context. |
| Primary pass criterion | Result reports matched aliases, conflicts, unresolved symbols, and required human decisions. |
| Veto diagnostics | Same name treated as same object without definition; conflict hidden. |
| Explanatory diagnostics | Convention table and provenance. |
| Not concluded | Full semantic identity of symbols. |
| Artifact | Reconciliation module/tests/result. |

## Forbidden Claims And Actions

- Do not silently merge symbols across sections.
- Do not auto-edit notation.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 11 if convention records can be attached to generated tests.

## Stop Conditions

Stop if conflict reports are too ambiguous to guide review.
