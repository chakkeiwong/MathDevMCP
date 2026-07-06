# Phase 4 Subplan: Risky-Debt V2 Experiment

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Generate a v2 risky-debt derivation report using extracted obligations and
inspect whether it improves on the current full-block report.

## Entry Conditions Inherited From Previous Phase

- Phase 3 report integration passed.
- Extracted target report path is tested.
- Current report remains available for comparison:
  `docs/reviews/risky-debt-derivation-gap-proposals.md`

## Required Artifacts

- Generated report:
  `docs/reviews/risky-debt-derivation-gap-proposals-v2.md`
- Phase 4 result:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-04-risky-debt-v2-experiment-result-2026-07-06.md`
- Optional bounded log under `docs/reviews` if command output is large.

## Required Checks/Tests/Reviews

- Generate v2 report for labels `prop:risky-pricing` and `prop:interior-foc`.
- Inspect Markdown for extracted obligations `eq:risky-pricing`, `eq:foc-k`,
  and `eq:foc-b` or documented equivalent stable target ids.
- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py -q`
- `git diff --check -- docs/reviews/risky-debt-derivation-gap-proposals-v2.md docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-04-risky-debt-v2-experiment-result-2026-07-06.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does extracted-obligation reporting improve risky-debt derivation audit usefulness? |
| Baseline/comparator | `docs/reviews/risky-debt-derivation-gap-proposals.md` full-block report. |
| Primary criterion | V2 report separates pricing and FOC obligations with target-level provenance and no loss of assumption repair details. |
| Veto diagnostics | V2 report lacks locations, loses assumption repairs, hides backend plan, or regresses to generic wording. |
| Explanatory diagnostics | Extracted target count, route plan counts, validation status counts. |
| Not concluded | No proof of the note; no applied edits; no scientific validation. |
| Artifact | V2 report and result record. |

## Forbidden Claims/Actions

- Do not edit risky-debt LaTeX.
- Do not claim v2 fixes the document.
- Do not compare by report length alone.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 only if:

- v2 report preserves or improves required fields;
- focused tests pass;
- public-surface regression tests are named.

## Stop Conditions

Stop if:

- v2 extraction is less reliable than full-block fallback;
- report cannot identify equation-level obligations;
- findings require human mathematical decision beyond proposal generation.
