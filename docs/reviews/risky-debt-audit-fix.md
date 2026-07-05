# MathDevMCP Audit And Fix Proposal

Question: Audit the risky-debt lecture note and propose repairs
Status: proposal_ready

## Certification Boundary

The audit-and-fix report is diagnostic guidance only; it does not apply edits, verify repaired text, or certify mathematical correctness.

## Tool Uses

| Tool | Purpose | Status | Output contract | Arguments |
| --- | --- | --- | --- | --- |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `prop:risky-pricing`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'prop:risky-pricing', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `prop:interior-foc`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'prop:interior-foc', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `propose_fix` | Translate audit evidence into conservative repair proposals. | diagnostic_only | high_level_workflow_result | `{'question': 'Audit the risky-debt lecture note and propose repairs', 'evidence_count': 2, 'source': {'root': '/home/chakwong/python/MathDevMCP/docs', 'labels': ['prop:risky-pricing', 'prop:interior-foc']}}` |

## Audited Evidence

- `prop:risky-pricing`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `prop:interior-foc`: inconclusive - No proof-audit v2 obligation could be certified or refuted.

## Proposed Changes

1. `split_derivation_step` for `obligation_3`
   Summary: Split the ambiguous derivation row into smaller labeled obligations.
   Rationale: The derivation row was not split into a safe proof obligation.
   Evidence refs: proof_audit_v2:prop:risky-pricing:obligation_3
2. `split_derivation_step` for `obligation_2`
   Summary: Split the ambiguous derivation row into smaller labeled obligations.
   Rationale: The derivation row was not split into a safe proof obligation.
   Evidence refs: proof_audit_v2:prop:interior-foc:obligation_2
3. `split_derivation_step` for `obligation_5`
   Summary: Split the ambiguous derivation row into smaller labeled obligations.
   Rationale: The derivation row was not split into a safe proof obligation.
   Evidence refs: proof_audit_v2:prop:interior-foc:obligation_5

### Proposed Fixes

1. `split_derivation_step` for `obligation_3`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Debt pricing > line 400`
   Problem: The derivation row is not split into a safe proof obligation.
   Why: The derivation row was not split into a safe proof obligation.
   Proposed fix: Replace the split row with `b'(1+r) = \E\left[   D(k',b',z')R(k',z')   +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))   \mid z   \right]`. Then prove: Justify the reconstructed equality `b'(1+r) = \E\left[   D(k',b',z')R(k',z')   +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))   \mid z   \right]` from the surrounding proposition/proof context.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     b'(1+r)
     =
     \E\left[
     D(k',b',z')R(k',z')
     +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))
     \mid z
     \right]
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `b'(1+r) = \E\left[   D(k',b',z')R(k',z')   +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))   \mid z   \right]` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Evidence refs: proof_audit_v2:prop:risky-pricing:obligation_3
2. `split_derivation_step` for `obligation_2`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > line 777`
   Problem: The derivation row is not split into a safe proof obligation.
   Why: The derivation row was not split into a safe proof obligation.
   Proposed fix: Replace the split row with `0 = m(\bar e)\frac{d\bar e}{dk'}   +\beta \E[V^\star_k(k',b',z')\mid z]`. Then prove: Differentiate the local objective with respect to the corresponding interior choice and show `0 = m(\bar e)\frac{d\bar e}{dk'}   +\beta \E[V^\star_k(k',b',z')\mid z]`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     0
     =
     m(\bar e)\frac{d\bar e}{dk'}
     +\beta \E[V^\star_k(k',b',z')\mid z]
   \end{equation}
   ```
   Derivation obligation: Differentiate the local objective with respect to the corresponding interior choice and show `0 = m(\bar e)\frac{d\bar e}{dk'}   +\beta \E[V^\star_k(k',b',z')\mid z]`.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Evidence refs: proof_audit_v2:prop:interior-foc:obligation_2
3. `split_derivation_step` for `obligation_5`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > line 782`
   Problem: The derivation row is not split into a safe proof obligation.
   Why: The derivation row was not split into a safe proof obligation.
   Proposed fix: Replace the split row with `0 = m(\bar e)\frac{d\bar e}{db'}   +\beta \E[V^\star_b(k',b',z')\mid z]`. Then prove: Differentiate the local objective with respect to the corresponding interior choice and show `0 = m(\bar e)\frac{d\bar e}{db'}   +\beta \E[V^\star_b(k',b',z')\mid z]`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     0
     =
     m(\bar e)\frac{d\bar e}{db'}
     +\beta \E[V^\star_b(k',b',z')\mid z]
   \end{equation}
   ```
   Derivation obligation: Differentiate the local objective with respect to the corresponding interior choice and show `0 = m(\bar e)\frac{d\bar e}{db'}   +\beta \E[V^\star_b(k',b',z')\mid z]`.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Evidence refs: proof_audit_v2:prop:interior-foc:obligation_5

## Evidence Gaps

1. `prove_reconstructed_obligation` for `obligation_3`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Debt pricing > line 400`
   Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
   Why: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
   Proposed fix: Add the derivation step described below, with the stated regularity/interiority assumptions, then rerun `audit_derivation_v2_label` for `prop:risky-pricing`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     b'(1+r)
     =
     \E\left[
     D(k',b',z')R(k',z')
     +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))
     \mid z
     \right]
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `b'(1+r) = \E\left[   D(k',b',z')R(k',z')   +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))   \mid z   \right]` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Proof target: `b'(1+r) = \E\left[   D(k',b',z')R(k',z')   +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))   \mid z   \right]`
   Derivation plan: Add a proof step defining the lender payoff as `D(k',b',z')R(k',z')+(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))`. Then impose the zero-profit condition `b'(1+r)=\E[payoff\mid z]` to obtain `b'(1+r) = \E\left[   D(k',b',z')R(k',z')   +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))   \mid z   \right]`.
   Evidence refs: proof_audit_v2:prop:risky-pricing:obligation_3
2. `prove_reconstructed_obligation` for `obligation_2`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > line 777`
   Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
   Why: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
   Proposed fix: Add the derivation step described below, with the stated regularity/interiority assumptions, then rerun `audit_derivation_v2_label` for `prop:interior-foc`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     0
     =
     m(\bar e)\frac{d\bar e}{dk'}
     +\beta \E[V^\star_k(k',b',z')\mid z]
   \end{equation}
   ```
   Derivation obligation: Differentiate the local objective with respect to the corresponding interior choice and show `0 = m(\bar e)\frac{d\bar e}{dk'}   +\beta \E[V^\star_k(k',b',z')\mid z]`.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Proof target: `0 = m(\bar e)\frac{d\bar e}{dk'}   +\beta \E[V^\star_k(k',b',z')\mid z]`
   Derivation plan: Add a local derivation with objective `J(k',b')=\bar e(k,k',b,b',z)+\eta(\bar e(k,k',b,b',z))+\beta \E[V^\star(k',b',z')\mid z]`. Use interiority to set `\partial J/\partial k'=0`, use `1+\eta'(\bar e)=m(\bar e)`, and justify differentiating the conditional expectation so the target becomes `0 = m(\bar e)\frac{d\bar e}{dk'}   +\beta \E[V^\star_k(k',b',z')\mid z]`.
   Evidence refs: proof_audit_v2:prop:interior-foc:obligation_2
3. `prove_reconstructed_obligation` for `obligation_5`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > line 782`
   Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
   Why: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
   Proposed fix: Add the derivation step described below, with the stated regularity/interiority assumptions, then rerun `audit_derivation_v2_label` for `prop:interior-foc`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     0
     =
     m(\bar e)\frac{d\bar e}{db'}
     +\beta \E[V^\star_b(k',b',z')\mid z]
   \end{equation}
   ```
   Derivation obligation: Differentiate the local objective with respect to the corresponding interior choice and show `0 = m(\bar e)\frac{d\bar e}{db'}   +\beta \E[V^\star_b(k',b',z')\mid z]`.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Proof target: `0 = m(\bar e)\frac{d\bar e}{db'}   +\beta \E[V^\star_b(k',b',z')\mid z]`
   Derivation plan: Add a local derivation with objective `J(k',b')=\bar e(k,k',b,b',z)+\eta(\bar e(k,k',b,b',z))+\beta \E[V^\star(k',b',z')\mid z]`. Use interiority to set `\partial J/\partial b'=0`, use `1+\eta'(\bar e)=m(\bar e)`, and justify differentiating the conditional expectation so the target becomes `0 = m(\bar e)\frac{d\bar e}{db'}   +\beta \E[V^\star_b(k',b',z')\mid z]`.
   Evidence refs: proof_audit_v2:prop:interior-foc:obligation_5

## Next Actions

- `human_review`: Review proposed changes before applying edits.
- `rerun_relevant_audit`: After any manual repair, rerun the audit evidence that produced the proposal.

## Non-Claims

- `diagnostic_evidence_not_proof`: Diagnostic evidence is not a proof certificate.
- `general_theorem_proving_not_claimed`: This scoped workflow result does not claim general theorem-proving ability.
- `release_readiness_not_claimed`: This scoped workflow result does not claim release readiness.
- `fix_proposal_not_applied_or_verified`: Proposed fixes are diagnostic guidance only; they are not applied edits, proof certificates, or semantic implementation verification.
- `audit_fix_report_not_applied_or_certified`: The audit-and-fix report is diagnostic guidance only; it does not apply edits, verify repaired text, or certify mathematical correctness.
