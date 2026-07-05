# MathDevMCP Audit And Fix Proposal

Question: Audit the risky-debt lecture note broadly and propose repairs
Status: proposal_ready

## Certification Boundary

The audit-and-fix report is diagnostic guidance only; it does not apply edits, verify repaired text, or certify mathematical correctness.

## Audit Coverage

Mode: `whole_document`
Audited labels: 25 / 84
Skipped labels: 59
Complete for selected scope: False
Target file: `risky-debt-maliar-deep-learning-lecture-note.tex`
Label limit: 25
Audited label list: `eq:ar1-shock`, `eq:investment-law`, `eq:basic-cash-flow`, `prop:basic-bellman`, `eq:basic-bellman`, `eq:risky-cash-flow`, `eq:recovery`, `eq:policy-q-value`, `eq:policy-going-concern`, `eq:policy-bellman`, `eq:q-value`, `eq:best-going-concern`, `prop:risky-bellman`, `eq:risky-bellman`, `eq:default-set`, `prop:risky-pricing`, `eq:risky-pricing`, `eq:explicit-rate`, `prop:coupled-fixed-point`, `eq:fixed-point-equity`, ... (5 more)
Skipped preview: `eq:network-going-concern`, `eq:bellman-fb-residual`, `eq:default-indicator`, `eq:pricing-residual`, `eq:policy-residual`, `prop:direct-policy-loss`, `eq:cashflow-total-k`, `eq:cashflow-rate-derivative`, `prop:interior-foc`, `eq:foc-k`

## Tool Uses

| Tool | Purpose | Status | Output contract | Arguments |
| --- | --- | --- | --- | --- |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:ar1-shock`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:ar1-shock', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:investment-law`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:investment-law', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:basic-cash-flow`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:basic-cash-flow', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `prop:basic-bellman`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'prop:basic-bellman', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:basic-bellman`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:basic-bellman', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:risky-cash-flow`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:risky-cash-flow', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:recovery`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:recovery', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:policy-q-value`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:policy-q-value', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:policy-going-concern`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:policy-going-concern', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:policy-bellman`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:policy-bellman', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:q-value`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:q-value', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:best-going-concern`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:best-going-concern', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `prop:risky-bellman`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'prop:risky-bellman', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:risky-bellman`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:risky-bellman', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:default-set`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:default-set', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `prop:risky-pricing`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'prop:risky-pricing', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:risky-pricing`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:risky-pricing', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:explicit-rate`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:explicit-rate', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `prop:coupled-fixed-point`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'prop:coupled-fixed-point', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:fixed-point-equity`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:fixed-point-equity', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `prop:limited-liability-complementarity`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'prop:limited-liability-complementarity', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:complementarity`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:complementarity', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:fb`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:fb', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:v-network`. | inconclusive | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:v-network', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:network-policies`. | unverified | proof_audit_v2_result | `{'root': '/home/chakwong/python/MathDevMCP/docs', 'label': 'eq:network-policies', 'paragraph_context': True, 'summary_only': True, 'backend': 'sympy'}` |
| `propose_fix` | Translate audit evidence into conservative repair proposals. | diagnostic_only | high_level_workflow_result | `{'question': 'Audit the risky-debt lecture note broadly and propose repairs', 'evidence_count': 25, 'source': {'root': '/home/chakwong/python/MathDevMCP/docs', 'labels': ['eq:ar1-shock', 'eq:investment-law', 'eq:basic-cash-flow', 'prop:basic-bellman', 'eq:basic-bellman', 'eq:risky-cash-flow', 'eq:recovery', 'eq:policy-q-value', 'eq:policy-going-concern', 'eq:policy-bellman', 'eq:q-value', 'eq:best-going-concern', 'prop:risky-bellman', 'eq:risky-bellman', 'eq:default-set', 'prop:risky-pricing', 'eq:risky-pricing', 'eq:explicit-rate', 'prop:coupled-fixed-point', 'eq:fixed-point-equity', 'prop:limited-liability-complementarity', 'eq:complementarity', 'eq:fb', 'eq:v-network', 'eq:network-policies']}}` |

## Audited Evidence

- `eq:ar1-shock`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:investment-law`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:basic-cash-flow`: unverified - At least one obligation remains unverified or diagnostic-only.
- `prop:basic-bellman`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:basic-bellman`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:risky-cash-flow`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `eq:recovery`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `eq:policy-q-value`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:policy-going-concern`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:policy-bellman`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:q-value`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:best-going-concern`: unverified - At least one obligation remains unverified or diagnostic-only.
- `prop:risky-bellman`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `eq:risky-bellman`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `eq:default-set`: unverified - At least one obligation remains unverified or diagnostic-only.
- `prop:risky-pricing`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `eq:risky-pricing`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `eq:explicit-rate`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `prop:coupled-fixed-point`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `eq:fixed-point-equity`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `prop:limited-liability-complementarity`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:complementarity`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:fb`: unverified - At least one obligation remains unverified or diagnostic-only.
- `eq:v-network`: inconclusive - No proof-audit v2 obligation could be certified or refuted.
- `eq:network-policies`: unverified - At least one obligation remains unverified or diagnostic-only.

## Proposed Changes

1. `split_derivation_step` for `obligation_4`
   Summary: Split the ambiguous derivation row into smaller labeled obligations.
   Rationale: The derivation row was not split into a safe proof obligation.
   Evidence refs: proof_audit_v2:eq:investment-law:obligation_4
2. `split_derivation_step` for `obligation_1`
   Summary: Split the ambiguous derivation row into smaller labeled obligations.
   Rationale: The derivation row was not split into a safe proof obligation.
   Evidence refs: proof_audit_v2:prop:basic-bellman:obligation_1
3. `split_derivation_step` for `obligation_2`
   Summary: Split the ambiguous derivation row into smaller labeled obligations.
   Rationale: The derivation row was not split into a safe proof obligation.
   Evidence refs: proof_audit_v2:eq:risky-cash-flow:obligation_2
4. `split_derivation_step` for `obligation_3`
   Summary: Split the ambiguous derivation row into smaller labeled obligations.
   Rationale: The derivation row was not split into a safe proof obligation.
   Evidence refs: proof_audit_v2:eq:policy-q-value:obligation_3
5. `split_derivation_step` for `obligation_7`
   Summary: Split the ambiguous derivation row into smaller labeled obligations.
   Rationale: The derivation row was not split into a safe proof obligation.
   Evidence refs: proof_audit_v2:eq:policy-q-value:obligation_7

### Proposed Fixes

1. `split_derivation_step` for `obligation_4`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Warm-up: the basic investment Bellman equation > line 134`
   Problem: The derivation row is not split into a safe proof obligation.
   Why: The derivation row was not split into a safe proof obligation.
   Proposed fix: Replace the split row with `e(k,k',z) = \pi(k,z)-\psi(k'-(1-\delta)k,k)-\bigl(k'-(1-\delta)k\bigr)`. Then prove: Justify the reconstructed equality `e(k,k',z) = \pi(k,z)-\psi(k'-(1-\delta)k,k)-\bigl(k'-(1-\delta)k\bigr)` from the surrounding proposition/proof context.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     e(k,k',z)
     =
     \pi(k,z)-\psi(k'-(1-\delta)k,k)-\bigl(k'-(1-\delta)k\bigr)
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `e(k,k',z) = \pi(k,z)-\psi(k'-(1-\delta)k,k)-\bigl(k'-(1-\delta)k\bigr)` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Evidence refs: proof_audit_v2:eq:investment-law:obligation_4
2. `split_derivation_step` for `obligation_1`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Warm-up: the basic investment Bellman equation > line 153`
   Problem: The derivation row is not split into a safe proof obligation.
   Why: The derivation row was not split into a safe proof obligation.
   Proposed fix: Replace the split row with `V(k,z) = \max_{k'}   \left\{   e(k,k',z)   +\beta \E[V(k',z')\mid z]   \right\}`. Then prove: Justify the reconstructed equality `V(k,z) = \max_{k'}   \left\{   e(k,k',z)   +\beta \E[V(k',z')\mid z]   \right\}` from the surrounding proposition/proof context.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     V(k,z)
     =
     \max_{k'}
     \left\{
     e(k,k',z)
     +\beta \E[V(k',z')\mid z]
     \right\}
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `V(k,z) = \max_{k'}   \left\{   e(k,k',z)   +\beta \E[V(k',z')\mid z]   \right\}` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Evidence refs: proof_audit_v2:prop:basic-bellman:obligation_1
3. `split_derivation_step` for `obligation_2`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Cash flow with risky debt > line 194`
   Problem: The derivation row is not split into a safe proof obligation.
   Why: The derivation row was not split into a safe proof obligation.
   Proposed fix: Replace the split row with `e(k,k',b,b',z;\widetilde r) = (1-\tau)\pi(k,z)   -\psi(k'-(1-\delta)k,k)`. Then prove: Justify the reconstructed equality `e(k,k',b,b',z;\widetilde r) = (1-\tau)\pi(k,z)   -\psi(k'-(1-\delta)k,k)` from the surrounding proposition/proof context.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     e(k,k',b,b',z;\widetilde r)
     =
     (1-\tau)\pi(k,z)
     -\psi(k'-(1-\delta)k,k)
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `e(k,k',b,b',z;\widetilde r) = (1-\tau)\pi(k,z)   -\psi(k'-(1-\delta)k,k)` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Evidence refs: proof_audit_v2:eq:risky-cash-flow:obligation_2
4. `split_derivation_step` for `obligation_3`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Default and recovery > line 283`
   Problem: The derivation row is not split into a safe proof obligation.
   Why: The derivation row was not split into a safe proof obligation.
   Proposed fix: Replace the split row with `Q^h(k,b,z;k',b') = e(k,k',b,b',z;\widetilde r)   +\eta(e(k,k',b,b',z;\widetilde r))   +\beta \E[V^h(k',b',z')\mid z]`. Then prove: Justify the reconstructed equality `Q^h(k,b,z;k',b') = e(k,k',b,b',z;\widetilde r)   +\eta(e(k,k',b,b',z;\widetilde r))   +\beta \E[V^h(k',b',z')\mid z]` from the surrounding proposition/proof context.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     Q^h(k,b,z;k',b')
     =
     e(k,k',b,b',z;\widetilde r)
     +\eta(e(k,k',b,b',z;\widetilde r))
     +\beta \E[V^h(k',b',z')\mid z]
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `Q^h(k,b,z;k',b') = e(k,k',b,b',z;\widetilde r)   +\eta(e(k,k',b,b',z;\widetilde r))   +\beta \E[V^h(k',b',z')\mid z]` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Evidence refs: proof_audit_v2:eq:policy-q-value:obligation_3
5. `split_derivation_step` for `obligation_7`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Default and recovery > line 293`
   Problem: The derivation row is not split into a safe proof obligation.
   Why: The derivation row was not split into a safe proof obligation.
   Proposed fix: Replace the split row with `G^h(k,b,z) = Q^h(k,b,z;h^k(k,b,z),h^b(k,b,z))`. Then prove: Justify the reconstructed equality `G^h(k,b,z) = Q^h(k,b,z;h^k(k,b,z),h^b(k,b,z))` from the surrounding proposition/proof context.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     G^h(k,b,z)
     =
     Q^h(k,b,z;h^k(k,b,z),h^b(k,b,z))
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `G^h(k,b,z) = Q^h(k,b,z;h^k(k,b,z),h^b(k,b,z))` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Evidence refs: proof_audit_v2:eq:policy-q-value:obligation_7

## Evidence Gaps

1. `concretize_before_fix` for `conformable_product_required`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Expected values and the shock process > line 100`
   Problem: The audit reports a missing assumption or shape constraint, but the current tools have not derived the exact assumption statement to insert here.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Proof target: `\log z' = \rho \log z + \varepsilon',`
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: \log z' = \rho \log z + \varepsilon',
   Evidence refs: proof_audit_v2:eq:ar1-shock:obligation_2
2. `concretize_before_fix` for `obligation_2`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Expected values and the shock process > line 100`
   Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Proof target: `\log z' = \rho \log z + \varepsilon',`
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: \log z' = \rho \log z + \varepsilon',
   Evidence refs: proof_audit_v2:eq:ar1-shock:obligation_2
3. `concretize_before_fix` for `obligation_3`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Expected values and the shock process > line 103`
   Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: where \(\rho\) is a persistence parameter and \(\varepsilon'\) is a random
   Evidence refs: proof_audit_v2:eq:ar1-shock:obligation_3
4. `concretize_before_fix` for `obligation_3`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Expected values and the shock process > line 103`
   Problem: The audit reports a missing assumption or shape constraint, but the current tools have not derived the exact assumption statement to insert here.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: where \(\rho\) is a persistence parameter and \(\varepsilon'\) is a random
   Evidence refs: proof_audit_v2:eq:ar1-shock:obligation_3
5. `concretize_before_fix` for `obligation_8`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Default and recovery > line 299`
   Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:manual_formalization_required` on route `human_review` and matrix-IR status `parsed`. The obligation uses notation that requires human review or manual formalization.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Proof target: `V^h(k,b,z)=\max\{0,G^h(k,b,z)\}.`
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: V^h(k,b,z)=\max\{0,G^h(k,b,z)\}.
   Evidence refs: proof_audit_v2:eq:policy-q-value:obligation_8
6. `concretize_before_fix` for `obligation_10`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Default and recovery > line 320`
   Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Proof target: `G^\star(k,b,z) = \max_{k',b'} Q^\star(k,b,z;k',b').`
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: G^\star(k,b,z) = \max_{k',b'} Q^\star(k,b,z;k',b').
   Evidence refs: proof_audit_v2:eq:q-value:obligation_10
7. `concretize_before_fix` for `obligation_11`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Default and recovery > line 328`
   Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Proof target: `\argmax_{k',b'} Q^\star(k,b,z;k',b').`
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: \argmax_{k',b'} Q^\star(k,b,z;k',b').
   Evidence refs: proof_audit_v2:eq:q-value:obligation_11
8. `concretize_before_fix` for `obligation_10`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Default and recovery > line 320`
   Problem: The audit reports a missing assumption or shape constraint, but the current tools have not derived the exact assumption statement to insert here.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Proof target: `G^\star(k,b,z) = \max_{k',b'} Q^\star(k,b,z;k',b').`
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: G^\star(k,b,z) = \max_{k',b'} Q^\star(k,b,z;k',b').
   Evidence refs: proof_audit_v2:eq:q-value:obligation_10
9. `concretize_before_fix` for `obligation_11`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Default and recovery > line 328`
   Problem: The audit reports a missing assumption or shape constraint, but the current tools have not derived the exact assumption statement to insert here.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Proof target: `\argmax_{k',b'} Q^\star(k,b,z;k',b').`
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: \argmax_{k',b'} Q^\star(k,b,z;k',b').
   Evidence refs: proof_audit_v2:eq:q-value:obligation_11
10. `concretize_before_fix` for `obligation_1`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Writing default as equations > line 492`
   Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
   Why: Proof-audit v2 returned `unverified` with substatus `unverified:manual_formalization_required` on route `human_review` and matrix-IR status `parsed`. The obligation uses notation that requires human review or manual formalization.
   Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
   Proof target: `V=\max\{0,G\}`
   Derivation plan: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
   Source: V=\max\{0,G\}
   Evidence refs: proof_audit_v2:prop:limited-liability-complementarity:obligation_1
11. `prove_reconstructed_obligation` for `obligation_4`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Warm-up: the basic investment Bellman equation > line 134`
   Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
   Why: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
   Proposed fix: Add the derivation step described below, with the stated regularity/interiority assumptions, then rerun `audit_derivation_v2_label` for `eq:investment-law`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     e(k,k',z)
     =
     \pi(k,z)-\psi(k'-(1-\delta)k,k)-\bigl(k'-(1-\delta)k\bigr)
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `e(k,k',z) = \pi(k,z)-\psi(k'-(1-\delta)k,k)-\bigl(k'-(1-\delta)k\bigr)` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Proof target: `e(k,k',z) = \pi(k,z)-\psi(k'-(1-\delta)k,k)-\bigl(k'-(1-\delta)k\bigr)`
   Derivation plan: Justify the reconstructed equality `e(k,k',z) = \pi(k,z)-\psi(k'-(1-\delta)k,k)-\bigl(k'-(1-\delta)k\bigr)` from the surrounding proposition/proof context.
   Evidence refs: proof_audit_v2:eq:investment-law:obligation_4
12. `prove_reconstructed_obligation` for `obligation_1`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Warm-up: the basic investment Bellman equation > line 153`
   Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
   Why: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
   Proposed fix: Add the derivation step described below, with the stated regularity/interiority assumptions, then rerun `audit_derivation_v2_label` for `prop:basic-bellman`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     V(k,z)
     =
     \max_{k'}
     \left\{
     e(k,k',z)
     +\beta \E[V(k',z')\mid z]
     \right\}
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `V(k,z) = \max_{k'}   \left\{   e(k,k',z)   +\beta \E[V(k',z')\mid z]   \right\}` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Proof target: `V(k,z) = \max_{k'}   \left\{   e(k,k',z)   +\beta \E[V(k',z')\mid z]   \right\}`
   Derivation plan: Justify the reconstructed equality `V(k,z) = \max_{k'}   \left\{   e(k,k',z)   +\beta \E[V(k',z')\mid z]   \right\}` from the surrounding proposition/proof context.
   Evidence refs: proof_audit_v2:prop:basic-bellman:obligation_1
13. `prove_reconstructed_obligation` for `obligation_2`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Cash flow with risky debt > line 194`
   Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
   Why: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
   Proposed fix: Add the derivation step described below, with the stated regularity/interiority assumptions, then rerun `audit_derivation_v2_label` for `eq:risky-cash-flow`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     e(k,k',b,b',z;\widetilde r)
     =
     (1-\tau)\pi(k,z)
     -\psi(k'-(1-\delta)k,k)
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `e(k,k',b,b',z;\widetilde r) = (1-\tau)\pi(k,z)   -\psi(k'-(1-\delta)k,k)` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Proof target: `e(k,k',b,b',z;\widetilde r) = (1-\tau)\pi(k,z)   -\psi(k'-(1-\delta)k,k)`
   Derivation plan: Justify the reconstructed equality `e(k,k',b,b',z;\widetilde r) = (1-\tau)\pi(k,z)   -\psi(k'-(1-\delta)k,k)` from the surrounding proposition/proof context.
   Evidence refs: proof_audit_v2:eq:risky-cash-flow:obligation_2
14. `prove_reconstructed_obligation` for `obligation_3`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Default and recovery > line 283`
   Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
   Why: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
   Proposed fix: Add the derivation step described below, with the stated regularity/interiority assumptions, then rerun `audit_derivation_v2_label` for `eq:policy-q-value`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     Q^h(k,b,z;k',b')
     =
     e(k,k',b,b',z;\widetilde r)
     +\eta(e(k,k',b,b',z;\widetilde r))
     +\beta \E[V^h(k',b',z')\mid z]
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `Q^h(k,b,z;k',b') = e(k,k',b,b',z;\widetilde r)   +\eta(e(k,k',b,b',z;\widetilde r))   +\beta \E[V^h(k',b',z')\mid z]` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Proof target: `Q^h(k,b,z;k',b') = e(k,k',b,b',z;\widetilde r)   +\eta(e(k,k',b,b',z;\widetilde r))   +\beta \E[V^h(k',b',z')\mid z]`
   Derivation plan: Justify the reconstructed equality `Q^h(k,b,z;k',b') = e(k,k',b,b',z;\widetilde r)   +\eta(e(k,k',b,b',z;\widetilde r))   +\beta \E[V^h(k',b',z')\mid z]` from the surrounding proposition/proof context.
   Evidence refs: proof_audit_v2:eq:policy-q-value:obligation_3
15. `prove_reconstructed_obligation` for `obligation_7`
   Location: `risky-debt-maliar-deep-learning-lecture-note.tex > The risky-debt model > Default and recovery > line 293`
   Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
   Why: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
   Proposed fix: Add the derivation step described below, with the stated regularity/interiority assumptions, then rerun `audit_derivation_v2_label` for `eq:policy-q-value`.
   Replacement LaTeX:
   ```latex
   \begin{equation}
     G^h(k,b,z)
     =
     Q^h(k,b,z;h^k(k,b,z),h^b(k,b,z))
   \end{equation}
   ```
   Derivation obligation: Justify the reconstructed equality `G^h(k,b,z) = Q^h(k,b,z;h^k(k,b,z),h^b(k,b,z))` from the surrounding proposition/proof context.
   Boundary: This is a context reconstruction for review; the equality still needs a derivation or a stronger symbolic/formal backend.
   Proof target: `G^h(k,b,z) = Q^h(k,b,z;h^k(k,b,z),h^b(k,b,z))`
   Derivation plan: Justify the reconstructed equality `G^h(k,b,z) = Q^h(k,b,z;h^k(k,b,z),h^b(k,b,z))` from the surrounding proposition/proof context.
   Evidence refs: proof_audit_v2:eq:policy-q-value:obligation_7

## Next Actions

- `human_review`: Review proposed changes before applying edits.
- `rerun_relevant_audit`: After any manual repair, rerun the audit evidence that produced the proposal.

## Non-Claims

- `diagnostic_evidence_not_proof`: Diagnostic evidence is not a proof certificate.
- `general_theorem_proving_not_claimed`: This scoped workflow result does not claim general theorem-proving ability.
- `release_readiness_not_claimed`: This scoped workflow result does not claim release readiness.
- `fix_proposal_not_applied_or_verified`: Proposed fixes are diagnostic guidance only; they are not applied edits, proof certificates, or semantic implementation verification.
- `audit_fix_report_not_applied_or_certified`: The audit-and-fix report is diagnostic guidance only; it does not apply edits, verify repaired text, or certify mathematical correctness.
