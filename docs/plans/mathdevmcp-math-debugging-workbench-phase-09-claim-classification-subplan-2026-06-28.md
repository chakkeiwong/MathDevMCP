# Phase 9 Subplan: Claim Classification

## Phase Objective

Implement `classify_math_claim`, classifying claims as definition, assumption,
derived identity, backend-proved, refuted, numerically supported, empirical,
unsupported, or not encodable.

## Entry Conditions Inherited From Previous Phase

- Proof/refutation, assumption, counterexample, and code/equation evidence
  records exist.

## Required Artifacts

- `src/mathdevmcp/math_claim_classifier.py`
- `tests/test_math_claim_classifier.py`
- CLI/MCP exposure.
- Phase 9 result record.
- Refreshed Phase 10 subplan.

## Required Checks, Tests, Reviews

- Tests across seeded claim classes.
- Existing claim support tests.
- `git diff --check`.
- Claude review for false promotion risk.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can claims be classified by evidence type without promotion? |
| Baseline/comparator | Existing `claim_support` and proof packet boundaries. |
| Primary pass criterion | Classifier assigns conservative class and next action for each seeded evidence shape. |
| Veto diagnostics | Numeric/empirical/unsupported claim upgraded to proof. |
| Explanatory diagnostics | Evidence class and support source. |
| Not concluded | Semantic truth of unsupported claims. |
| Artifact | Classifier module/tests/result. |

## Forbidden Claims And Actions

- Do not infer truth from fluent prose.
- Do not classify missing evidence as support.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 10 if claim classes can be used by notation reconciliation and
review packets.

## Stop Conditions

Stop if claim categories cannot preserve proof boundary distinctions.
