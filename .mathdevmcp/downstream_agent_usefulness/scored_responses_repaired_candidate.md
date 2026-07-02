# Repaired Candidate Scored Responses

Date: 2026-07-02

Status: `REPAIRED_CANDIDATE_SCORED_DIAGNOSTIC`

## Summary

The repaired collection recorded 27 Codex-subagent responses, one per repaired prompt, with no hidden retries and no Claude response worker. The repaired A/B/C comparison is now valid as a local diagnostic because the A-condition fixture leakage was removed and the repaired prompt manifest validates with zero prompt-contract errors.

Hard vetoes: A = 0, B = 0, C = 0. Required-pass counts: A = 8/9, B = 9/9, C = 9/9. C improves over A only on the Joseph backend-certificate case; C ties B under the frozen required dimensions, so no C-over-B superiority or promotion claim is established.

## Condition Summary

| Condition | Rows | Hard vetoes | Malformed | Prompt leaks | Required passes | Required total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `A_task_only` | 9 | 0 | 0 | 0 | 8 | 106/108 |
| `B_evidence_only` | 9 | 0 | 0 | 0 | 9 | 108/108 |
| `C_human_framed` | 9 | 0 | 0 | 0 | 9 | 108/108 |

## Minimum Candidate Rule

- `a_baseline_valid`: `True`
- `repaired_a_prompt_leakage_count`: `0`
- `aggregate_only_forbidden`: `True`
- `c_no_hard_veto_regression_vs_b`: `True`
- `c_required_pass_all_scored_cases`: `True`
- `c_preserves_b_machine_evidence`: `True`
- `c_better_than_b_on_predeclared_usefulness_axis`: `False`
- `c_better_than_a_on_local_required_pass_count`: `True`
- `candidate_rule_pass`: `False`
- `interpretation`: `The repaired A/B/C comparison is valid as a local diagnostic and removes the original A-condition leakage. C passes all rows and is better than A on the Joseph backend-certificate case, but C ties B on required rubric dimensions; no C-over-B superiority or promotion claim is established.`

## Per-Case Rows

| Case | A pass | B pass | C pass | A vs B | C vs B | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `RLHLB-01-ift-sign-gap` | True | True | True | tied | tied | Localized the sign gap and avoided source-wide overclaim. |
| `RLHLB-02-kalman-loglik-assumptions` | True | True | True | tied | tied | Returned route-required Gaussian and covariance-domain assumptions. |
| `RLHLB-03-joseph-equivalence` | False | True | True | worse | tied | A lacked decisive backend-certificate evidence; B/C passed with scoped proof evidence and boundaries. |
| `RLHLB-04-affine-pricing-recursion` | True | True | True | tied | tied | Abstained from proxy derivation and named matrix/domain route gaps. |
| `RLHLB-05-kalman-score-same-scalar` | True | True | True | tied | tied | Identified same-scalar, differentiability, covariance-domain, masking, and route-link assumptions. |
| `RLHLB-06-state-space-code-missing-solve` | True | True | True | tied | tied | Reported local structural mismatch while preserving equivalence alternatives. |
| `RLHLB-07-proof-boundary-review-packet` | True | True | True | tied | tied | Treated the packet as diagnostic organization, not proof. |
| `RLHLB-08-hmc-value-only-boundary` | True | True | True | tied | tied | Refused to promote value-only likelihood evidence to HMC readiness. |
| `RLHLB-09-affine-recovery-assumption-limit` | True | True | True | tied | tied | Returned missing-assumption status for neural-solver guarantees. |

## Non-Claims

- This is a local, non-gating diagnostic result.
- This is not a proof certificate, release gate, public benchmark result, scientific validation, product capability claim, broad theorem-proving claim, or general model reliability claim.
- The repaired result does not establish C-over-B superiority.
