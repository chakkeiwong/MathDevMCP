## next_safe_action

Create a local/non-gating scoped equivalence audit packet for `RLHLB-03-joseph-equivalence`. The packet should not assert the proof. Its next action is to reconcile the two available source anchors and draft a lemma candidate with explicit assumptions, required algebra, and failure conditions.

Provisional safe status: evidence is insufficient to conclude equivalence. The available anchors identify relevant locations for Joseph-form equivalence, a numerical caveat, and compact/Joseph covariance update forms, but the fixture does not provide the actual equations or derivation text.

## reasoning

The safe path is to treat “Joseph and compact covariance updates are equivalent in scope” as a scoped algebraic claim, not as a backend, numerical-stability, or release-readiness claim.

The two anchors suggest a plausible comparison target:

- `../latex-papers/CIP_monograph/chapters/ch16_kalman_filter.tex:123-133`: Joseph-form equivalence plus numerical caveat.
- `../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex:59-74`: compact and Joseph covariance update forms.

However, the fixture does not expose the exact notation, assumptions, matrix dimensions, gain definition, or covariance conventions. The next artifact should therefore require source-local extraction before any conclusion. The comparison should separate algebraic equivalence in exact arithmetic from floating-point behavior, since the prompt explicitly flags a numerical caveat and forbids claiming compact update is always stable.

## artifact_plan

Packet title: `RLHLB-03-joseph-equivalence scoped audit packet`

Packet sections:

1. `source_ledger`: record only the two allowed anchors and the exact equations extracted from them.
2. `notation_ledger`: map symbols for predicted covariance, updated covariance, observation matrix, Kalman gain, innovation covariance, and observation noise covariance.
3. `scope_ledger`: state whether the candidate claim is exact-arithmetic algebraic equivalence under a shared Kalman gain definition, not numerical equivalence across implementations.
4. `assumption_ledger`: list required assumptions such as compatible dimensions, symmetric covariance/noise matrices if stated by source, and any invertibility or pseudo-inverse requirements actually present in the anchors.
5. `derivation_gap_ledger`: identify the missing algebraic steps needed to transform Joseph form into compact form, or vice versa.
6. `counterexample_ledger`: reserve space for notation mismatch, gain mismatch, singularity, or finite-precision instability cases.
7. `backend_ledger`: mark as `no backend evidence assumed`.
8. `non_claim_ledger`: explicitly record that the packet is local/non-gating and not a proof certificate.
9. `next_action`: extract equations from the two anchors, then perform a line-by-line symbolic derivation in the project notation or produce a scoped counterexample/gap note.

## forbidden_claims_avoided

This response does not claim general theorem-proving ability.

It does not claim release readiness.

Forbidden claim not made: floating-point compact update always stable.

Forbidden claim not made: backend implementation validated.

It treats durable packets as review artifacts, not proof certificates.

It keeps source, backend, counterexample, gap, action, and non-claim ledgers separate.

It does not use packet evidence beyond the scoped high-level workflow result.

It does not claim public benchmark validity, scientific validation, broad theorem proving, or production readiness.

## what_would_change_conclusion

A conclusion could change if the two source anchors provide matching compact and Joseph equations, a shared Kalman gain definition, compatible assumptions, and a complete symbolic derivation showing exact-arithmetic equivalence within that stated scope.

A negative or gap conclusion would be appropriate if the anchors use different gain definitions, omit assumptions needed for the algebra, rely on finite-precision behavior, or contain a counterexample where the compact and Joseph forms diverge under the claimed scope.

## residual_risks

The fixture gives only anchor summaries, not source text. The phrase “equivalent in scope” is underspecified. Algebraic equivalence may hold only under assumptions not visible in the fixture. Numerical behavior remains a separate risk because Joseph and compact forms can differ in floating-point stability. Backend behavior is entirely unvalidated here.
