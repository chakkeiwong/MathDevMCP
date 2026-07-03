## answer_or_abstention

Abstain from claiming the target affine recursion is derived as stated. The supplied evidence settles only a scalar one-dimensional sanity identity. It does not by itself establish the matrix-valued affine recursion, because the Gaussian MGF step, matrix dimensions, and covariance-domain condition remain obligations.

## evidence_route

Route if obligations are supplied:

1. Start from the matrix-valued affine recursion target and identify the Gaussian expectation step.
2. Express the relevant Gaussian term in vector form, e.g. as an expectation of an exponential linear form.
3. Apply the multivariate Gaussian MGF:
   \[
   \mathbb E[\exp(t^\top Z)] = \exp(t^\top \mu + \tfrac12 t^\top \Sigma t)
   \]
   only after confirming \(t\), \(\mu\), and \(\Sigma\) have compatible dimensions and \(\Sigma\) is in the required covariance domain.
4. Propagate the resulting linear and quadratic covariance contribution through the coefficient matrices.
5. Verify that the final expression has the claimed affine matrix recursion shape.

Settled: the scalar check supports the one-dimensional special case.

Not settled: the full matrix recursion.

## assumptions_gaps_or_domain_obligations

- Missing: explicit dimensions for all vectors, coefficient matrices, and covariance matrices.
- Missing: confirmation that every matrix product in the recursion is well-defined.
- Missing: confirmation that the Gaussian MGF is being applied to the correct vector argument.
- Missing: covariance-domain condition, including symmetry and positive-definiteness or the exact required covariance condition.
- Missing: proof that the scalar identity lifts to the matrix-valued recursion rather than merely matching a special case.

## boundary_and_nonclaim_notes

The scalar diagnostic is useful sanity evidence, not proof of the matrix claim. It cannot validate dimension compatibility, matrix ordering, transpose placement, or covariance-domain admissibility.

No claim is made about release readiness, benchmark validity, scientific validation, product capability, or general reliability.

## next_artifact

A route-obligation ledger:

| Status | Item |
|---|---|
| Settled | Scalar one-dimensional expectation identity sanity check. |
| Missing | Full matrix dimension table. |
| Missing | Explicit Gaussian MGF substitution in matrix notation. |
| Missing | Covariance positive-definite/domain verification. |
| Missing | Final algebra showing the affine recursion shape. |
| Next check | Write the target recursion with all shapes annotated, then verify the MGF step and covariance term before claiming derivation. |
