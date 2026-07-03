# V2 Candidate Scored Responses

Date: 2026-07-03

Status: `V2_CANDIDATE_SCORED_LOCAL_DIAGNOSTIC`

## Summary

The v2 collection recorded 18 Codex-subagent responses, one per approved
prompt, with no hidden retries and no Claude response worker. Scoring was
applied hard-veto-first under the frozen collection scoring contract.

Hard vetoes: A = 0, B = 0, C = 0. Required-pass counts: A = 6/6, B = 5/6,
C = 6/6. C ties B on five cases and improves on the Gaussian-score review
packet case, where the B response is a sparse diagnostic status while the C
response gives a self-contained review question, risks, gaps, and next
artifact.

This supports only a bounded local C-over-B diagnostic for this single-response
run. It is not a public benchmark result, release gate, scientific validation,
product capability claim, broad theorem-proving claim, proof-correctness claim
beyond scoped obligations, or general model-reliability claim.

## Hard-Veto-First Summary

| Condition | Rows | Hard vetoes | Malformed | Required passes | Required total |
| --- | ---: | ---: | ---: | ---: | ---: |
| `A_task_only` | 6 | 0 | 0 | 6 | 72/72 |
| `B_evidence_only` | 6 | 0 | 0 | 5 | 69/72 |
| `C_human_framed` | 6 | 0 | 0 | 6 | 72/72 |

## Minimum Candidate Rule

- `aggregate_only_forbidden`: `True`
- `c_no_hard_veto_regression_vs_b`: `True`
- `c_no_malformed_regression_vs_b`: `True`
- `c_required_pass_at_least_b`: `True`
- `c_no_primary_dimension_regression_vs_b`: `True`
- `c_better_than_b_on_predeclared_usefulness_axis`: `True`
- `improved_cases`: `V2-PRP-01-gaussian-score-review-packet`
- `improved_axes`: `task_outcome_correctness`, `self_contained_reasoning`,
  `actionability_for_next_agent`
- `candidate_rule_pass`: `True`

Interpretation: under the frozen local diagnostic contract, C passes the
minimum C-over-B rule in this run because it ties B on five cases and improves
on one case without hard-veto, malformed-output, or primary-dimension
regression.

## Per-Case Rows

| Case | A pass | B pass | C pass | A vs B | C vs B | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `V2-DF-01-affine-matrix-domain-obligation` | True | True | True | tied | tied | All conditions avoid deriving the matrix recursion from scalar sanity evidence alone; C is more detailed but not primary-better than B. |
| `V2-PC-01-domain-restricted-counterexample` | True | True | True | tied | tied | B and C both preserve the unrestricted/restricted scope split; C gives a clearer certificate map. |
| `V2-AF-01-masked-likelihood-score-assumptions` | True | True | True | tied | tied | B and C both identify same-scalar, mask, covariance-domain, and differentiability obligations. |
| `V2-AMC-01-logdet-quadratic-code-trace` | True | True | True | tied | tied | B and C both flag the missing or unresolved quadratic solve term without making a global code claim. |
| `V2-DD-01-first-gap-product-rule` | True | True | True | tied | tied | B and C both identify Step 2 as the first product-rule failure; C adds an explanatory counterexample check. |
| `V2-PRP-01-gaussian-score-review-packet` | True | False | True | better | better | B is diagnostic-only but too sparse as a review packet; C gives the review question, gaps, veto risks, and next artifact. |

## Non-Claims

- Scores are local downstream-usefulness diagnostics only.
- Scores are not proof certificates.
- Scores are not release gates.
- Scores are not public benchmark results.
- Scores are not scientific validation.
- Scores are not product capability evidence.
- Scores are not proof of broad theorem-proving ability.
- Scores are not proof of general model reliability.
