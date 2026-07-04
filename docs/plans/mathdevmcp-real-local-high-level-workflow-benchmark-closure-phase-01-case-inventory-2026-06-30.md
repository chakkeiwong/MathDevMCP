# Phase 1 Case Inventory: Real-Local High-Level Workflow Benchmark Closure

Date: 2026-06-30

Status: `CANDIDATE_INVENTORY`

This inventory contains bounded local candidate cases for the real-local
high-level workflow benchmark. It records source anchors and expected evidence
routes only; it does not copy large source text, assert source claims are true,
or promote local cases to benchmark-gate evidence.

## Candidate Cases

| ID | Workflow | User Question Shape | Source Anchors | Expected Route | Expected Outcome Type | Negative Control | Forbidden Claims |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `RLHLB-01-ift-sign-gap` | `debug_derivation` | Where does this sign derivation first fail? | `../dsge_hmc/docs/gradient_accuracy_analysis.tex:536-589`; `../dsge_hmc/docs/gradient_accuracy_analysis.tex:883-893` | Source-adapter plus proof-gap localization | source-mismatch / gap-found | yes | Whole DSGE note false; HMC conclusion invalid; probe proves theorem |
| `RLHLB-02-kalman-loglik-assumptions` | `assumptions_for` | What assumptions are required to derive Kalman prediction-error log-likelihood? | `../latex-papers/CIP_monograph/chapters/ch16_kalman_filter.tex:197-223`; `../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex:32-39`; `../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex:76-105` | Source-adapter plus assumption extraction | success with source-stated assumptions | no | Nonlinear filters exact; score/Hessian validated; source likelihood is implementation proof |
| `RLHLB-03-joseph-equivalence` | `prove_or_counterexample` | Can we prove Joseph and compact covariance updates are equivalent in scope? | `../latex-papers/CIP_monograph/chapters/ch16_kalman_filter.tex:123-133`; `../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex:59-74` | Source-adapter local schema; exact-arithmetic boundary | source-supported scoped proof | no | Floating-point compact update always stable; backend implementation validated |
| `RLHLB-04-affine-pricing-recursion` | `derive_from` | Can we derive affine pricing recursion from Gaussian affine assumptions? | `../latex-papers/CIP_monograph/chapters/ch11_state_space_recursions.tex:242-322` | Source-adapter plus symbolic derivation-route diagnostics | success with assumptions | no | Empirical pricing validity; nonlinear approximation exact |
| `RLHLB-05-kalman-score-same-scalar` | `assumptions_for` | What assumptions are needed for the Kalman score to match the same scalar likelihood? | `../BayesFilter/docs/chapters/ch09_kalman_score.tex:20-103`; `../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex:120-130` | Source-adapter plus assumption extraction | success with source-stated assumptions | no | HMC validity; posterior correctness; Hessian readiness |
| `RLHLB-06-state-space-code-missing-solve` | `audit_math_to_code` | Does code implement the documented Kalman likelihood solve/quadratic form? | `benchmarks/fixtures/doc_department_state_space.tex:7-23`; `benchmarks/fixtures/doc_department_state_space_missing_solve.py:1-17`; `docs/mathdevmcp-release-report.tex:1099-1123` | Structural code/equation audit | structural_mismatch / source-mismatch | yes | Code is mathematically wrong; absence of literal solve proves implementation invalid |
| `RLHLB-07-proof-boundary-review-packet` | `prepare_review_packet` | Can we produce a packet for a difficult Gaussian score derivation without overclaiming proof? | `docs/mathdevmcp-release-report.tex:1255-1361` | Review-packet route with backend-attempt summary | diagnostic_only / justified abstention | yes | Review packet is a certificate; full score derivation proved |
| `RLHLB-08-hmc-value-only-boundary` | `prove_or_counterexample` | Does a value-only filtering likelihood route prove HMC production readiness? | `../BayesFilter/docs/chapters/ch21_hmc_for_state_space.tex:6-52` | Source boundary plus backend-unavailable/value-only route | insufficient_evidence / justified abstention | yes | HMC production readiness; TFP/NUTS mathematical criticism; sampler correctness |
| `RLHLB-09-affine-recovery-assumption-limit` | `derive_from` | Can neural-solver approximation guarantees be derived from affine recovery text alone? | `../latex-papers/CIP_monograph/chapters/ch15_nonlinear_pricing.tex:267-302` | Source assumptions plus negative overclaim check | missing_assumptions / justified abstention for uniform bound | yes | Rigorous uniform approximation bound; neural solver correctness; pricing validity |

## Coverage Matrix

| Dimension | Covered Values | Cases |
| --- | --- | --- |
| Workflow type | `debug_derivation`, `assumptions_for`, `prove_or_counterexample`, `derive_from`, `audit_math_to_code`, `prepare_review_packet` | all six workflow families covered |
| Route type | source adapter, source-assumption extraction, symbolic/derivation diagnostics, structural code/equation audit, review-packet route, backend-unavailable/value-only route | `RLHLB-01` through `RLHLB-09` |
| Outcome type | success, source-supported scoped proof, source-mismatch, structural mismatch, missing assumptions, insufficient evidence, diagnostic-only, justified abstention | all represented |
| Negative-control type | sign inconsistency, missing solve/quadratic form, review packet not certificate, value-only not HMC readiness, heuristic approximation not uniform theorem | `RLHLB-01`, `RLHLB-06`, `RLHLB-07`, `RLHLB-08`, `RLHLB-09` |
| Source family | `dsge_hmc`, `latex-papers/CIP_monograph`, `BayesFilter`, MathDevMCP docs/fixtures | four source families |

## Quality Notes

- Case selection was based on existing local source anchors and workflow
  coverage needs, not current workflow pass/fail output.
- The five `RLHLB-01` through `RLHLB-05` cases reuse governed real-local
  pilot/source-adapter anchors.
- The four additional cases add explicit coverage for code-audit mismatch,
  review-packet abstention, backend-unavailable/value-only boundary, and
  assumption-limit overclaim prevention.
- Every case is local/non-gating until a later promotion-policy phase says
  otherwise.

## Non-Claims

This inventory does not establish benchmark validity, release readiness,
scientific validation, production implementation correctness, external
reproducibility, full LaTeX proof checking, or broad theorem proving.
