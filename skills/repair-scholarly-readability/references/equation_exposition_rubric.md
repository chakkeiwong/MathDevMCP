# Equation Exposition Rubric

Use this rubric for equations that carry a mechanism, derivation, empirical
estimand, or decision. Small definitions may need only a subset.

## Integrity Ledger

For each important display, check:

| Item | Question |
| --- | --- |
| Role | Is this a definition, identity, equilibrium condition, approximation, estimator, source-reported result, or local derivation? |
| Source | Is the source/version and exact equation or section anchor recorded where material? |
| Symbols | Are symbols, indices, sets, vectors/matrices, and units defined before or at first use? |
| Types and dimensions | Are scalar/vector/matrix roles and conformability clear? |
| Domain | Are positivity, interiority, differentiability, invertibility, convergence, or support restrictions stated when required? |
| Timing and conditioning | Are dates, information sets, expectations, lags, and predetermined variables unambiguous? |
| Equality status | Is the relation exact, approximate, log-linearized, calibrated, estimated, or conjectural? |
| Assumptions | Which assumptions make the equation valid or give it economic meaning? |
| Interpretation | Can the reader state the equation in plain language without changing the target? |
| Intuition | Is there a useful limiting case, sign, comparative static, path, or special case? |
| Transition | Does the text explain why the next equation, result, or empirical test follows? |
| Reuse | Is a numbered equation referenced later? If not, should it be unnumbered, explained more clearly, or removed? |
| Code alignment | When relevant, is there an executable block or a precise no-code/no-run boundary? |

## Mathematical Verdicts

Use direct classifications:

- `correct`: checked derivation, source, code, or backend supports the relation;
- `wrong relative to the stated target`: the displayed or computed object differs
  from the claim;
- `unsupported`: no inspected support establishes it;
- `not checked`: evidence has not been inspected far enough;
- `heuristic only`: explicitly useful without a correctness claim.

Do not hide a mismatch behind “proxy,” “stabilized,” or “approximately correct.”
Define the changed target and its relation to the original.

## MathDevMCP Role

MathDevMCP can localize labels, propose missing assumptions, inspect notation,
route bounded algebra to SymPy/Sage/Lean, and create review packets. Its output
must be classified before editing:

1. concrete source-supported defect;
2. question requiring source or human review;
3. duplicate/low-value diagnostic;
4. abstention;
5. false positive.

Backend success checks only the scoped formal object under the supplied
assumptions. It does not certify that the object is the right economic model,
matches the cited paper, or is explained well.

## Exposition Pattern

Use prose in this order when appropriate:

1. State why the object is needed.
2. Define notation and assumptions.
3. Display the equation.
4. Interpret its terms and direction.
5. Give one discriminating implication or limiting case.
6. Connect it to evidence or the next model object.

Avoid symbol-by-symbol paraphrase that adds no meaning. Avoid intuition that
does not follow from the displayed relation.
