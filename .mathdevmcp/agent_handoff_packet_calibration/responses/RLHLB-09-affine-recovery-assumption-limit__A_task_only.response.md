## next_safe_action

Create a local/non-gating derivation-scope note for `RLHLB-09-affine-recovery-assumption-limit` whose conclusion is: **neural-solver approximation guarantees cannot be derived from the affine recovery text alone without additional formal assumptions, definitions, and proof obligations**. The safe action is to mark the route as evidence-insufficient and prepare an assumption ledger for review, not to prove or promote the claim.

## reasoning

The only available source anchor is `../latex-papers/CIP_monograph/chapters/ch15_nonlinear_pricing.tex:267-302`, described as affine recovery and nonlinear-pricing approximation text. That anchor may provide motivating text, a recovery relation, or approximation language, but by itself it is not enough to establish a neural-solver approximation guarantee unless it contains, explicitly and formally, the needed mathematical hypotheses.

At minimum, such a guarantee would need clear objects: the function class being approximated, the domain, norm or metric, regularity assumptions, solver architecture, training or optimization assumptions, error decomposition, stability of the recovered affine component, and the relationship between approximation error and the nonlinear pricing target. If those items are only narrative givens, they should remain **givens, not formal assumptions**.

Therefore the next artifact should separate what the affine recovery text explicitly states from what would have to be added as route-required assumptions. The workflow should not infer hidden lemmas, backend results, or durable packet conclusions.

## artifact_plan

Prepare a short review artifact with four parts.

1. Source extraction: quote or paraphrase only the claims present in lines 267-302, with no expansion beyond the anchor.

2. Assumption ledger: list every condition required to move from affine recovery text to a neural-solver approximation statement. Mark each as one of: explicit in anchor, missing, ambiguous, or route-required.

3. Non-derivability finding: state that affine recovery text alone is insufficient for a rigorous neural-solver approximation guarantee unless the missing assumptions are supplied and checked.

4. Next evidence request: identify the specific material needed next, such as a formal theorem statement, approximation lemma, stability argument, neural architecture assumptions, training/optimization assumptions, and downstream pricing-error bound.

## forbidden_claims_avoided

This artifact does not claim general theorem-proving ability.

It does not claim release readiness.

It does not treat route-required assumptions as globally minimal.

It does not make a rigorous uniform approximation bound.

It does not claim neural solver correctness.

It does not claim pricing validity.

It does not treat durable packets as proof certificates by themselves.

It does not promote narrative affine-recovery text into formal assumptions without review.

## what_would_change_conclusion

The conclusion could change if the cited lines, or an allowed companion source, explicitly provide a theorem connecting affine recovery to neural-solver approximation under stated assumptions, including the relevant norm, domain, approximation class, stability conditions, and pricing-error transfer.

It could also change if a reviewed derivation supplies the missing assumptions and proves that the neural solver approximates the target object with a controlled error that is sufficient for the intended nonlinear-pricing use.

## residual_risks

The anchor may contain stronger formal content than the fixture reveals, but the frozen prompt does not provide that content. Conversely, the anchor may contain only informal motivation, in which case any guarantee would require substantial external derivation.

The main residual risk is accidental over-reading: treating affine recovery language as if it already implies neural approximation, solver correctness, or pricing validity. The safe posture is to preserve the gap explicitly and request the missing formal evidence next.
