# MathDevMCP Real Local High-Level Workflow Pilot Cases

Date: 2026-06-29

Status: draft local pilot inventory, not benchmark-gate evidence.

## Purpose

Construct 5-10 real mathematical workflow cases from neighboring repositories
under `/home/chakwong/python`, especially `latex-papers` and repo-local
`docs/` trees. These cases are intended to seed a future benchmark for the
new high-level MathDevMCP workflows:

- `derive_from`;
- `prove_or_counterexample`;
- `assumptions_for`;
- `debug_derivation`;
- `audit_math_to_code`;
- `prepare_review_packet`.

The cases below are deliberately framed as pilot candidates. They are not yet
committed benchmark fixtures, CI inputs, release evidence, or claims about
external benchmark validity.

## Source And Evidence Policy

- Keep source provenance explicit: every candidate records repo, path, and line
  anchors from the inspected local copy.
- Do not exfiltrate private or unpublished source material to external review
  tools. If Claude is later used, prompts should use short bounded summaries or
  sanitized excerpts only.
- Formal benchmark fixtures should copy or sanitize minimal excerpts into a
  controlled fixture tier, rather than making CI depend directly on sibling repo
  paths.
- A structural match, text match, review packet, or local symbolic diagnostic is
  diagnostic evidence only unless a deterministic backend certificate or
  checked derivation explicitly supports a stronger status.
- Backend unavailable, parser failure, or not-encodable status is not a
  refutation.

## Candidate Cases

### Case 1: IFT Gradient Bias Sign Consistency

- Source: `/home/chakwong/python/dsge_hmc/docs/gradient_accuracy_analysis.tex`
  lines 536-589, with summary repeat at lines 883-893.
- User question: "Can we prove the stated IFT gradient-bias formula from the
  theorem definitions, or is there a sign inconsistency?"
- Primary workflow: `debug_derivation`.
- Secondary workflow: `prove_or_counterexample`.
- Expected result type: negative-control diagnostic. The statement boxed at
  lines 553-559 says
  `G^IFT - G^FD = - lambda^T dr/dtheta`, while the displayed proof reaches
  `+ lambda^T dr/dtheta` at line 575 under the stated adjoint convention
  `lambda^T = - zbar^T J_z^{-1}`.
- Evidence contract: derive the algebra from the definitions of `G^IFT`,
  `G^FD`, and `lambda`; report the first inconsistent sign boundary. A SymPy
  scalarization or symbolic sign check can support the diagnosis.
- Forbidden claims: do not claim the whole DSGE note is false; do not claim the
  practical HMC conclusion is invalid; do not fix the paper from the benchmark
  runner.
- Adjudication note: this is a strong negative control because the source itself
  contains both the target statement and the proof algebra.

### Case 2: IFT Adjoint Gradient Derivation

- Source: `/home/chakwong/python/dsge_hmc/docs/gradient_accuracy_analysis.tex`
  lines 336-433.
- User question: "Can I derive the adjoint formula
  `grad_theta L = lambda^T J_theta` from the implicit-function derivative and
  the adjoint equation?"
- Primary workflow: `derive_from`.
- Expected result type: positive derivation with explicit assumptions.
- Required assumptions: differentiability of `f` and `L`, local invertibility
  of `J_z`, compatible row/column conventions, and the adjoint convention
  `J_z^T lambda = - zbar`.
- Evidence contract: show the chain rule, substitute the IFT sensitivity, solve
  the adjoint equation, and check dimensions.
- Forbidden claims: do not claim global uniqueness, convergence of a numerical
  solver, or correctness of the TensorFlow custom-gradient implementation.
- Adjudication note: useful as a positive companion to Case 1; it tests whether
  the workflow can derive a standard result while preserving convention
  dependencies.

### Case 3: DSGE Residual Jacobian Vectorization

- Source: `/home/chakwong/python/dsge_hmc/docs/gradient_accuracy_analysis.tex`
  lines 912-943.
- User question: "Can I derive the vectorized residual Jacobian blocks for
  `F_1 = H_y' gx hx + H_y gx + H_x' hx + H_x`?"
- Primary workflow: `derive_from`.
- Secondary workflow: `assumptions_for`.
- Expected result type: derivation/check of Kronecker-form Jacobian blocks.
- Required assumptions: column-major vectorization convention, fixed coefficient
  matrices during differentiation with respect to `gx` and `hx`, compatible
  dimensions, and the identity `vec(ABC) = (C^T kron A) vec(B)`.
- Evidence contract: recover the two displayed Jacobian blocks and identify any
  dimension conditions needed for `J_z`.
- Forbidden claims: do not claim the matrix-sign solver residual is small,
  convergence-safe, or HMC-safe from this algebra alone.
- Adjudication note: good for testing dimension-aware derivation, not just
  scalar symbolic simplification.

### Case 4: Kalman Prediction-Error Log-Likelihood

- Source:
  `/home/chakwong/python/latex-papers/CIP_monograph/chapters/ch16_kalman_filter.tex`
  lines 197-223 and
  `/home/chakwong/python/BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex`
  lines 76-105.
- User question: "Can we derive the prediction-error log-likelihood from the
  Kalman innovations?"
- Primary workflow: `derive_from`.
- Secondary workflow: `assumptions_for`.
- Expected result type: positive derivation with domain assumptions.
- Required assumptions: linear Gaussian state-space model, positive definite
  selected innovation covariance `S_t`, valid observation mask policy, and
  Kalman predictive distribution `Y_t | Y_{1:t-1}` being Gaussian with mean
  `Yhat_t|t-1` and covariance `S_t`.
- Evidence contract: use the probability chain rule and Gaussian log-density;
  preserve the distinction between dense and masked panels.
- Forbidden claims: do not claim nonlinear filters are exact; do not claim the
  score or Hessian is validated unless derivative recursions are separately
  checked.
- Adjudication note: useful because two independent local documents encode the
  same likelihood spine.

### Case 5: Kalman Optimality Assumptions

- Source:
  `/home/chakwong/python/latex-papers/CIP_monograph/chapters/ch16_kalman_filter.tex`
  lines 112-120 and
  `/home/chakwong/python/BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex`
  lines 13-39.
- User question: "If we want the Kalman recursion to deliver the exact
  conditional mean/covariance and MMSE estimator, what assumptions are required?"
- Primary workflow: `assumptions_for`.
- Expected result type: assumption set, not proof of a particular
  implementation.
- Required assumptions: linear state and observation equations, Gaussian
  innovations for nonlinear-MMSE optimality, zero-mean noise, covariance domain
  conditions, independence or declared correlation treatment, valid initial
  moments, and positive definite selected innovation covariance.
- Evidence contract: separate assumptions needed for linear-MMSE filtering from
  assumptions needed for full MMSE optimality under Gaussianity.
- Forbidden claims: do not claim numerical stability, square-root equivalence,
  or code correctness from the mathematical assumptions alone.
- Adjudication note: important for the "what assumptions are required for X?"
  workflow.

### Case 6: Joseph Covariance Update Equivalence

- Source:
  `/home/chakwong/python/latex-papers/CIP_monograph/chapters/ch16_kalman_filter.tex`
  lines 123-133 and
  `/home/chakwong/python/BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex`
  lines 59-74.
- User question: "Can we prove that the Joseph covariance update is
  algebraically equivalent to the compact Kalman covariance update under the
  standard gain definition?"
- Primary workflow: `prove_or_counterexample`.
- Secondary workflow: `derive_from`.
- Expected result type: positive proof under explicit assumptions, with a
  boundary around floating-point behavior.
- Required assumptions: `K = P H^T (H P H^T + R)^{-1}`, symmetric prior
  covariance `P`, measurement covariance `R`, and exact arithmetic for algebraic
  equivalence.
- Evidence contract: expand
  `(I-KH)P(I-KH)^T + K R K^T` and use `S = HPH^T + R` to reduce to
  `(I-KH)P`; separately state why Joseph form is preferred numerically.
- Forbidden claims: do not claim compact form preserves positive
  semidefiniteness under rounding; do not claim a particular backend implements
  either form correctly without code audit.
- Adjudication note: a good proof/counterexample case because it has a clean
  theorem and a clear numerical caveat.

### Case 7: Affine Pricing Master Recursion

- Source:
  `/home/chakwong/python/latex-papers/CIP_monograph/chapters/ch11_state_space_recursions.tex`
  lines 242-322.
- User question: "Can I derive the affine recursion coefficients `A_n` and
  `B_n` from the exponential-affine ansatz and Gaussian transition law?"
- Primary workflow: `derive_from`.
- Expected result type: positive derivation.
- Required assumptions: risk-neutral Gaussian affine transition,
  exponential-affine payoff/continuation form, affine adjusted short rate,
  finite covariance, and initial conditions `A_0 = 0`, `B_0 = 0`.
- Evidence contract: substitute the ansatz, apply the Gaussian moment
  generating function, then collect state-dependent and constant terms.
- Forbidden claims: do not claim every later non-affine asset approximation is
  exact; do not claim empirical pricing validity or identification.
- Adjudication note: this is a high-value latex-papers case because it resembles
  a real professor query about deriving a model object from stated assumptions.

### Case 8: BGS Excess-Return FOC Relation

- Source:
  `/home/chakwong/python/DynareMCP/docs/AIpostdoc/literature/bgs_foundation_corpus_2026_05_28/08_foundation_model/foundation_derivation_notes.md`
  lines 86-110.
- User question: "Can I derive the BGS relation equating government-bond excess
  returns to `Delta` times private-security excess returns from the two FOCs?"
- Primary workflow: `derive_from`.
- Expected result type: positive algebraic derivation.
- Required assumptions: both FOCs hold with the same multiplier expression,
  same conditional expectation operator, and same augmented discount factor.
- Evidence contract: divide or substitute the two FOC right-hand sides and
  preserve the interpretation boundary around `Delta`.
- Forbidden claims: do not claim the full BGS model is validated; do not infer
  empirical QE effectiveness; do not treat literature notes as a formal proof
  beyond the local algebra.
- Adjudication note: compact, real, and easy to certify with symbolic
  substitution.

### Case 9: BGS QE Constraint Aggregation

- Source:
  `/home/chakwong/python/DynareMCP/docs/AIpostdoc/literature/bgs_foundation_corpus_2026_05_28/08_foundation_model/foundation_derivation_notes.md`
  lines 112-166.
- User question: "Can we derive the aggregate QE constraint from bank portfolio
  restriction and market clearing?"
- Primary workflow: `derive_from`.
- Secondary workflow: `assumptions_for`.
- Expected result type: positive derivation with inequality and notation
  tracking.
- Required assumptions: binding or weak portfolio restriction as stated,
  market-clearing identities for private and government holdings, consistent
  distinction between private-bank holdings and central-bank holdings, and
  nonnegative scaling where inequalities are preserved.
- Evidence contract: substitute `S^p = S - S^g` and `B^p = B - B^g` into the
  aggregate portfolio restriction and collect terms.
- Forbidden claims: do not claim purchases are always effective; the source
  distinguishes slack versus binding constraints and inefficiency costs.
- Adjudication note: useful for testing whether the workflow handles economic
  notation and inequalities without hallucinating policy claims.

### Case 10: Kalman Score Same-Scalar Derivative Contract

- Source:
  `/home/chakwong/python/BayesFilter/docs/chapters/ch09_kalman_score.tex`
  lines 20-103 and
  `/home/chakwong/python/BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex`
  lines 120-130.
- User question: "Can I derive the solve-form Kalman score contribution from
  the prediction-error log-likelihood, and what must be true for it to be a
  valid HMC gradient?"
- Primary workflow: `derive_from`.
- Secondary workflow: `assumptions_for`.
- Expected result type: derivation plus evidence-boundary report.
- Required assumptions: same scalar likelihood as the value path, differentiable
  state-space objects, valid derivatives of `v_t` and `S_t`, positive definite
  innovation covariance, and solve equation `S_t w_t = v_t`.
- Evidence contract: differentiate the log determinant and quadratic form,
  substitute the solve variable, and state the same-scalar condition for HMC.
- Forbidden claims: do not claim Hessian readiness, posterior validity, sampler
  convergence, or backend correctness without downstream checks.
- Adjudication note: good bridge from derivation to `audit_math_to_code`,
  because a future case can compare these formulas to an implementation.

## Coverage Summary

The ten candidates cover:

- `derive_from`: Cases 2, 3, 4, 7, 8, 9, 10.
- `prove_or_counterexample`: Cases 1 and 6.
- `assumptions_for`: Cases 3, 4, 5, 9, 10.
- `debug_derivation`: Case 1.
- `audit_math_to_code`: Case 10 can be extended into a code audit once a local
  implementation path is selected; Cases 3 and 4 also have natural code-audit
  extensions.
- `prepare_review_packet`: every case can generate a review packet, with Cases
  1, 4, 7, and 10 being the best first targets.

Suggested first formalization set:

1. Case 1, because it is a high-signal negative control.
2. Case 4, because Kalman likelihood is central and source-backed in two docs.
3. Case 6, because it is a compact proof with a numerical boundary.
4. Case 7, because it exercises long-form affine derivation.
5. Case 10, because it tests same-scalar gradient discipline for HMC.

## Conversion Plan To Benchmark Fixtures

1. Extract minimal sanitized excerpts for the selected cases into a local
   fixture tier, preserving path provenance and line anchors in metadata.
2. Add a manifest schema for high-level real-local cases with fields for
   source paths, workflow, question, expected status, required assumptions,
   required evidence classes, forbidden claims, and adjudication notes.
3. Write expected-answer rubrics that score boundary preservation and evidence
   use before prose quality.
4. Run each case through the current high-level workflow layer. Mark cases that
   require future LaTeX/domain adapters as `candidate_only` rather than failed.
5. Promote only cases with stable extraction, clear oracle status, and
   non-ambiguous forbidden-claim boundaries into the formal local benchmark.

## Stop Conditions For Formalization

- Source ownership or publication status is unclear and a sanitized excerpt
  cannot be safely committed.
- The expected result depends on unresolved scientific judgment rather than a
  local derivation, source-backed assumption boundary, or deterministic check.
- A case cannot be adjudicated without sending substantial private source text
  to an external model.
- The current workflow cannot parse or encode the mathematical structure and no
  honest `candidate_only` status is available.

## Immediate Recommendation

Use this inventory to create a reviewed subplan for a five-case pilot fixture
pack. The pilot should prefer Cases 1, 4, 6, 7, and 10, because together they
exercise negative-control derivation debugging, Kalman likelihood derivation,
proof with numerical caveat, affine recursion derivation, and same-scalar
gradient assumptions.
