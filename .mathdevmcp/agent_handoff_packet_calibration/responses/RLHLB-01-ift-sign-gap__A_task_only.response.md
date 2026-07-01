**next_safe_action**

Create a scoped derivation-audit artifact for `RLHLB-01-ift-sign-gap` that compares the sign algebra in `../dsge_hmc/docs/gradient_accuracy_analysis.tex:536-589` against the repeated sign convention in `../dsge_hmc/docs/gradient_accuracy_analysis.tex:883-893`. The action should not attempt to prove or disprove the theorem. It should identify the first line or transition where the sign convention becomes unsupported, ambiguous, or inconsistent, and record the missing justification needed to resolve it.

**reasoning**

The safe next step is a local proof-audit pass because the prompt only provides source anchors, not the text itself, backend evidence, a counterexample, or a completed packet. Therefore the conclusion cannot be “the theorem is false” or “the derivation is correct.” The question asks where the sign derivation first fails, but the available evidence is insufficient to name a specific equation or line without inspecting the anchored source.

The audit should start at the theorem statement and proof algebra in lines 536-589, because this is where the original sign-bearing derivation presumably occurs. The repeat at lines 883-893 should be treated only as a consistency check, not as independent proof. If the summary repeats a convention that is not justified in the proof, the first failure remains in the earlier algebra, not in the later summary.

The likely failure mode to check is an implicit sign change around an implicit-function-theorem step: for example, whether differentiating a first-order condition yields a negative inverse-Hessian term, whether the residual/Jacobian convention flips that sign, and whether the notation consistently distinguishes gradients of objective, residual, score, or loss. But that is only a hypothesis for the audit, not a conclusion.

**artifact_plan**

1. Record the task metadata: case `RLHLB-01-ift-sign-gap`, workflow `debug_derivation`, condition `A_task_only`, and source anchors.

2. Extract the sign-relevant equations from lines 536-589:
   - theorem statement,
   - definitions of objective/residual/gradient terms,
   - implicit equation being differentiated,
   - IFT derivative expression,
   - any substitution into the claimed sign result.

3. Build a line-by-line sign ledger:
   - source line,
   - local expression,
   - sign-bearing operation,
   - required convention,
   - whether the convention is explicitly stated,
   - first unsupported or inconsistent transition.

4. Compare lines 883-893 against the ledger:
   - does the summary repeat the same convention,
   - does it silently repair the earlier sign,
   - or does it preserve the same ambiguity?

5. Output a narrow finding:
   - “first unsupported sign transition is at line X” if source inspection supports that,
   - otherwise “insufficient evidence from provided anchors without source text inspection.”

**forbidden_claims_avoided**

This artifact does not claim general theorem-proving ability.

It does not claim the whole DSGE note is false.

It does not claim any HMC conclusion is invalid.

It does not claim that a probe proves a theorem.

It treats durable packets as review artifacts, not proof certificates.

It keeps source, backend evidence, counterexample status, gap, action, and non-claim ledgers separate.

It does not use or assume hidden backend evidence or packet conclusions.

It does not establish release readiness, public benchmark validity, scientific validation, or broad theorem proving.

**what_would_change_conclusion**

The conclusion could change after direct inspection of `gradient_accuracy_analysis.tex:536-589` and `883-893`. A clear explicit convention in the theorem proof may show that the sign is justified. Conversely, a line-by-line derivation may reveal a definite first failure, such as a missing minus sign in the IFT derivative or an inconsistent residual definition.

A backend symbolic check, numerical counterexample, or reviewed packet could support the audit, but only if its scope, assumptions, and source mapping are preserved.

**residual_risks**

The prompt does not include the actual source text, so any specific line-level failure would be speculative here.

The repeated summary may obscure whether the issue is algebraic, notational, or merely editorial.

There may be hidden definitions before line 536 that control the sign convention. Those would need inspection before making a durable finding.
