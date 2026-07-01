# Phase 14 Subplan: Literature To Local Audit

## Phase Objective

Implement a structured `literature_local_audit` over explicitly supplied theorem
assumptions and local assumptions, reporting matches, missing assumptions,
conflicts, notation differences, and applicability status.

## Entry Conditions Inherited From Previous Phase

- Assumption discovery, notation reconciliation, claim classification, and
  change-impact records exist.

## Required Artifacts

- `src/mathdevmcp/literature_local_audit.py`
- `tests/test_literature_local_audit.py`
- Phase 14 result record.
- Refreshed Phase 15 subplan.

## Required Checks, Tests, Reviews

- Synthetic theorem/local setting tests for full match, missing compactness,
  missing full-rank, stationarity mismatch, notation conflict.
- `git diff --check`.
- Claude review for theorem applicability language.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo compare theorem assumptions to local assumptions without overclaiming applicability? |
| Baseline/comparator | Assumption manifest and notation reconciliation support. |
| Primary pass criterion | Audit separates matched, missing, conflicting, and unreviewed assumptions with applicability status. |
| Veto diagnostics | Claiming theorem applies despite missing/conflicting assumptions. |
| Explanatory diagnostics | Assumption comparison table and notation notes. |
| Not concluded | Paper theorem correctness or local scientific validity. |
| Artifact | Literature-local module/tests/result. |

## Forbidden Claims And Actions

- Do not browse/fetch papers in this phase.
- Do not claim theorem applicability without assumption match or explicit human
  waiver.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 15 if all high-level workflows have stable artifacts or
documented blockers.

## Stop Conditions

Stop if applicability status cannot distinguish match, gap, conflict, and
unreviewed.
