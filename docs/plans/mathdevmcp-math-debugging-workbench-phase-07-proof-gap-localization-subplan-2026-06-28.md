# Phase 7 Subplan: Proof Gap Localization

## Phase Objective

Implement `localize_proof_gap`, which splits a derivation into adjacent
obligations and reports the first unjustified, refuted, missing-assumption, or
not-encodable step.

## Entry Conditions Inherited From Previous Phase

- `prove_or_refute` exists.
- Assumption discovery exists.

## Required Artifacts

- `src/mathdevmcp/proof_gap.py`
- `tests/test_proof_gap.py`
- CLI/MCP exposure.
- Phase 7 result record.
- Refreshed Phase 8 subplan.

## Required Checks, Tests, Reviews

- Tests for all-verified chain, one false step, missing invertibility, matrix
  commutation gap.
- `git diff --check`.
- Claude review for gap and repair language.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo identify where a derivation stops being justified? |
| Baseline/comparator | Existing label derivation audit and proof-audit v2. |
| Primary pass criterion | First failing step and repair suggestion are reported without validating later steps as proof. |
| Veto diagnostics | Whole-derivation valid if any step fails; repair suggestion stated as proof. |
| Explanatory diagnostics | Step statuses and first gap. |
| Not concluded | Automatic repair of derivation. |
| Artifact | Gap module/tests/result. |

## Forbidden Claims And Actions

- Do not continue proof validity claim past the first blocking gap.
- Do not rewrite source documents automatically.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 8 if gap statuses can inform code/equation mismatch reports.

## Stop Conditions

Stop if per-step evidence cannot be preserved.
