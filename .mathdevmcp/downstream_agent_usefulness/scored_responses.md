# Downstream-Agent Usefulness Scored Responses

Date: 2026-07-02

Status: `PHASE_04_SCORED_DIAGNOSTIC_WITH_A_CONDITION_LEAKAGE_VETO`

## Hard-Veto-First Summary

| Condition | Rows | Hard vetoes | Fixture contract violations | Malformed | Required passes after veto |
| --- | ---: | ---: | ---: | ---: | ---: |
| `A_task_only` | 9 | 9 | 9 | 0 | 0 |
| `B_evidence_only` | 9 | 0 | 0 | 0 | 9 |
| `C_human_framed` | 9 | 0 | 0 | 0 | 9 |

The A baseline is contaminated: every `A_task_only` prompt fixture included evaluator evidence/status fields outside the Phase 1 A-condition allowed payload. Those rows are preserved as raw responses but hard-vetoed for `condition_artifact_leakage`.

B and C rows have no hard vetoes or malformed outputs in this single-response run. They tie on the frozen required dimensions, so C superiority over B is not established.

## Required-Dimension Totals Before Hard Veto

| Condition | task outcome | evidence use | reasoning | assumptions/gaps | boundary discipline | actionability |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `A_task_only` | 18 | 18 | 18 | 18 | 18 | 18 |
| `B_evidence_only` | 18 | 18 | 18 | 18 | 18 | 18 |
| `C_human_framed` | 18 | 18 | 18 | 18 | 18 | 18 |

These totals are shown only to explain response quality before veto. They do not rescue the contaminated A baseline.

## Minimum Candidate Rule

- `c_no_hard_veto_regression_vs_b`: True
- `c_required_pass_all_scored_cases`: True
- `c_preserves_b_machine_evidence`: True
- `c_better_than_b_on_predeclared_usefulness_axis`: False
- `a_baseline_valid`: False
- `aggregate_only_forbidden`: True
- `candidate_rule_pass`: False
- `interpretation`: B and C rows pass without hard vetoes, but C ties B numerically on required dimensions. A is not a valid baseline because A_task_only prompts leaked evaluator evidence/status fields. No C-superiority or A/B/C benchmark-success claim is established.

## Per-Row Scores

| Prompt | Expected | Evidence | Hard vetoes | Required pass | Delta vs B | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `RLHLB-01-ift-sign-gap__A_task_only` | `refuted` | `backend_counterexample` | condition_artifact_leakage | false | `worse` | A-condition fixture leaked evaluator evidence/status fields; row is useful as a raw response but not valid A-baseline evidence. |
| `RLHLB-01-ift-sign-gap__B_evidence_only` | `refuted` | `backend_counterexample` | none | true | `not_applicable` | Localized the counterexample/sign gap and preserved source-wide boundary. |
| `RLHLB-01-ift-sign-gap__C_human_framed` | `refuted` | `backend_counterexample` | none | true | `tied` | Localized the counterexample/sign gap and preserved source-wide boundary. |
| `RLHLB-02-kalman-loglik-assumptions__A_task_only` | `missing_assumptions` | `missing_assumption` | condition_artifact_leakage | false | `worse` | A-condition fixture leaked evaluator evidence/status fields; row is useful as a raw response but not valid A-baseline evidence. |
| `RLHLB-02-kalman-loglik-assumptions__B_evidence_only` | `missing_assumptions` | `missing_assumption` | none | true | `not_applicable` | Returned missing-assumption status with route-required assumptions and no equivalence/guarantee overclaim. |
| `RLHLB-02-kalman-loglik-assumptions__C_human_framed` | `missing_assumptions` | `missing_assumption` | none | true | `tied` | Returned missing-assumption status with route-required assumptions and no equivalence/guarantee overclaim. |
| `RLHLB-03-joseph-equivalence__A_task_only` | `proved` | `backend_certificate` | condition_artifact_leakage | false | `worse` | A-condition fixture leaked evaluator evidence/status fields; row is useful as a raw response but not valid A-baseline evidence. |
| `RLHLB-03-joseph-equivalence__B_evidence_only` | `proved` | `backend_certificate` | none | true | `not_applicable` | Used scoped backend-certificate/equivalent exact-arithmetic algebra and kept numerical/implementation boundaries. |
| `RLHLB-03-joseph-equivalence__C_human_framed` | `proved` | `backend_certificate` | none | true | `tied` | Used scoped backend-certificate/equivalent exact-arithmetic algebra and kept numerical/implementation boundaries. |
| `RLHLB-04-affine-pricing-recursion__A_task_only` | `inconclusive` | `human_review_required` | condition_artifact_leakage | false | `worse` | A-condition fixture leaked evaluator evidence/status fields; row is useful as a raw response but not valid A-baseline evidence. |
| `RLHLB-04-affine-pricing-recursion__B_evidence_only` | `inconclusive` | `human_review_required` | none | true | `not_applicable` | Abstained or returned inconclusive status and proposed the next source-backed/human-review artifact. |
| `RLHLB-04-affine-pricing-recursion__C_human_framed` | `inconclusive` | `human_review_required` | none | true | `tied` | Abstained or returned inconclusive status and proposed the next source-backed/human-review artifact. |
| `RLHLB-05-kalman-score-same-scalar__A_task_only` | `missing_assumptions` | `missing_assumption` | condition_artifact_leakage | false | `worse` | A-condition fixture leaked evaluator evidence/status fields; row is useful as a raw response but not valid A-baseline evidence. |
| `RLHLB-05-kalman-score-same-scalar__B_evidence_only` | `missing_assumptions` | `missing_assumption` | none | true | `not_applicable` | Returned missing-assumption status with route-required assumptions and no equivalence/guarantee overclaim. |
| `RLHLB-05-kalman-score-same-scalar__C_human_framed` | `missing_assumptions` | `missing_assumption` | none | true | `tied` | Returned missing-assumption status with route-required assumptions and no equivalence/guarantee overclaim. |
| `RLHLB-06-state-space-code-missing-solve__A_task_only` | `structural_mismatch` | `structural_mismatch` | condition_artifact_leakage | false | `worse` | A-condition fixture leaked evaluator evidence/status fields; row is useful as a raw response but not valid A-baseline evidence. |
| `RLHLB-06-state-space-code-missing-solve__B_evidence_only` | `structural_mismatch` | `structural_mismatch` | none | true | `not_applicable` | Reported local structural mismatch and preserved implementation-equivalence alternatives. |
| `RLHLB-06-state-space-code-missing-solve__C_human_framed` | `structural_mismatch` | `structural_mismatch` | none | true | `tied` | Reported local structural mismatch and preserved implementation-equivalence alternatives. |
| `RLHLB-07-proof-boundary-review-packet__A_task_only` | `diagnostic_only` | `review_packet` | condition_artifact_leakage | false | `worse` | A-condition fixture leaked evaluator evidence/status fields; row is useful as a raw response but not valid A-baseline evidence. |
| `RLHLB-07-proof-boundary-review-packet__B_evidence_only` | `diagnostic_only` | `review_packet` | none | true | `not_applicable` | Treated packet as diagnostic organization only, not proof. |
| `RLHLB-07-proof-boundary-review-packet__C_human_framed` | `diagnostic_only` | `review_packet` | none | true | `tied` | Treated packet as diagnostic organization only, not proof. |
| `RLHLB-08-hmc-value-only-boundary__A_task_only` | `inconclusive` | `human_review_required` | condition_artifact_leakage | false | `worse` | A-condition fixture leaked evaluator evidence/status fields; row is useful as a raw response but not valid A-baseline evidence. |
| `RLHLB-08-hmc-value-only-boundary__B_evidence_only` | `inconclusive` | `human_review_required` | none | true | `not_applicable` | Abstained or returned inconclusive status and proposed the next source-backed/human-review artifact. |
| `RLHLB-08-hmc-value-only-boundary__C_human_framed` | `inconclusive` | `human_review_required` | none | true | `tied` | Abstained or returned inconclusive status and proposed the next source-backed/human-review artifact. |
| `RLHLB-09-affine-recovery-assumption-limit__A_task_only` | `missing_assumptions` | `missing_assumption` | condition_artifact_leakage | false | `worse` | A-condition fixture leaked evaluator evidence/status fields; row is useful as a raw response but not valid A-baseline evidence. |
| `RLHLB-09-affine-recovery-assumption-limit__B_evidence_only` | `missing_assumptions` | `missing_assumption` | none | true | `not_applicable` | Returned missing-assumption status with route-required assumptions and no equivalence/guarantee overclaim. |
| `RLHLB-09-affine-recovery-assumption-limit__C_human_framed` | `missing_assumptions` | `missing_assumption` | none | true | `tied` | Returned missing-assumption status with route-required assumptions and no equivalence/guarantee overclaim. |

## Limitations And Non-Claims

- A_task_only prompt fixtures leaked evaluator evidence/status fields, invalidating the clean A baseline comparison.
- Single response subject per prompt gives high variance and cannot establish general model reliability.
- Manifest-order collection was not randomized or counterbalanced.
- B and C rows passed, producing a ceiling effect that prevents an observed C-over-B superiority claim.
- Scores are local diagnostics only and are not proof certificates, release gates, public benchmark results, scientific validation, product capability evidence, or general model reliability evidence.
- Subagent identifiers for the first thirteen response artifacts were not preserved in local files after reboot/context compaction; the raw response artifacts remain recorded, and the one-attempt policy is preserved by the run ledger and handoff summary.
