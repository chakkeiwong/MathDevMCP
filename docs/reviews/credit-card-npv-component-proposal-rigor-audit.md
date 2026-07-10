# Math Document Rigor Audit

Target: `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex`

## Executive Summary

- Coverage status: `partial_coverage`
- Selected targets: 6 / 214 labeled equation rows
- Gaps: 21
- Proposals: 21
- Concrete repairs: 4
- Diagnostic abstentions: 17
- This report is diagnostic and proposal-oriented; it is not a proof of the document.

## Backend Provenance

- Active Python: `/home/chakwong/miniconda3/envs/tfgpu/bin/python3`
- LeanDojo status: `available`
- LeanDojo environment scope: `backend_python`
- LeanDojo backend env: `mathdevmcp-backends`
- Certification boundary: LeanDojo availability is proof-search evidence only. A proof is certified only by direct Lean checking with no placeholders, or by another certifying backend under the scoped contract.

## Document Inventory

- Lines: 8944
- Sections: 199
- Equation rows: 224
- Labeled equation rows: 214
- Duplicate labels: 0
- Missing refs: 0

## Tool Uses

| Tool | Purpose | Status | Output contract | Arguments |
| --- | --- | --- | --- | --- |
| `locate_equations_in_file` | Localize display equations in the exact target file. | `completed` | `equation_rows` | `{"root": "docs/credit-card-npv-component-proposal", "tex_path": "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex"}` |
| `summarize_equation_localization` | Summarize equation localization uncertainty. | `completed` | `equation_localization_summary` | `{"row_count": 224}` |
| `doctor_report` | Record active/backend Python and external backend capability provenance. | `available` | `doctor_report` | `{}` |
| `lean_readiness` | Record direct Lean, Lake, and LeanDojo readiness without promoting readiness to proof. | `ready_with_caveats` | `lean_readiness` | `{"root": "docs/credit-card-npv-component-proposal"}` |
| `audit_and_propose_fix` | Audit selected labels and propose concrete derivation/evidence repairs. | `proposal_ready` | `high_level_workflow_result` | `{"exact_file_root": "temporary_single_file_copy", "labels": ["eq:proposal-objective", "eq:panel-npv-functional", "eq:incremental-npv", "eq:ss-bellman", "eq:experiment-npv-estimand", "eq:policy-value-estimator"], "root": "docs/credit-card-npv-component-proposal", "target_file": "credit_card_npv_component_proposal_final_submission.tex", "validate_proposed_fixes": true}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:proposal-objective`. | `inconclusive` | `proof_audit_v2_result` | `{"backend": "sympy", "label": "eq:proposal-objective", "paragraph_context": true, "root": "/tmp/mathdevmcp-rigor-audit-hgl6xe9v", "summary_only": true}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:panel-npv-functional`. | `inconclusive` | `proof_audit_v2_result` | `{"backend": "sympy", "label": "eq:panel-npv-functional", "paragraph_context": true, "root": "/tmp/mathdevmcp-rigor-audit-hgl6xe9v", "summary_only": true}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:incremental-npv`. | `unverified` | `proof_audit_v2_result` | `{"backend": "sympy", "label": "eq:incremental-npv", "paragraph_context": true, "root": "/tmp/mathdevmcp-rigor-audit-hgl6xe9v", "summary_only": true}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:ss-bellman`. | `unverified` | `proof_audit_v2_result` | `{"backend": "sympy", "label": "eq:ss-bellman", "paragraph_context": true, "root": "/tmp/mathdevmcp-rigor-audit-hgl6xe9v", "summary_only": true}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:experiment-npv-estimand`. | `inconclusive` | `proof_audit_v2_result` | `{"backend": "sympy", "label": "eq:experiment-npv-estimand", "paragraph_context": true, "root": "/tmp/mathdevmcp-rigor-audit-hgl6xe9v", "summary_only": true}` |
| `audit_derivation_v2_label` | Generate local derivation audit evidence for `eq:policy-value-estimator`. | `unverified` | `proof_audit_v2_result` | `{"backend": "sympy", "label": "eq:policy-value-estimator", "paragraph_context": true, "root": "/tmp/mathdevmcp-rigor-audit-hgl6xe9v", "summary_only": true}` |
| `propose_fix` | Translate audit evidence into conservative repair proposals. | `diagnostic_only` | `high_level_workflow_result` | `{"evidence_count": 6, "question": "Audit selected document labels for mathematical rigor gaps and proposed repairs", "source": {"labels": ["eq:proposal-objective", "eq:panel-npv-functional", "eq:incremental-npv", "eq:ss-bellman", "eq:experiment-npv-estimand", "eq:policy-value-estimator"], "root": "/tmp/mathdevmcp-rigor-audit-hgl6xe9v"}}` |
| `validate_proposed_fixes` | Attach deterministic backend-attempt accountability to concrete proposed fixes. | `completed` | `proposal_fix_validation_summary` | `{"backend_order": ["lean", "sage", "sympy"], "detail_count": 15, "policy": "require_attempt_when_encodable"}` |

## Concrete Repair Ledger

### 1. `obligation_1`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Executive Proposal and Decision Request > line 252`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Proposed fix: Replace the affected displayed math with the replacement LaTeX below, then rerun the referenced audit before treating the edit as certified.
- Replacement LaTeX:

```latex
\begin{equation}
  \Delta \NPV_i(a;d,s,\pi)
  =
  \E\left[
  \NPV_i(a;d,s,\pi)-\NPV_i(a_0;d,s,\pi)
  \mid \mathcal{I}_{id}
  \right]
\end{equation}
```
- Proof target: `\Delta \NPV_i(a;d,s,\pi) = \E\left[   \NPV_i(a;d,s,\pi)-\NPV_i(a_0;d,s,\pi)   \mid \mathcal{I}_{id}   \right]`
- Derivation route: Justify the reconstructed equality `\Delta \NPV_i(a;d,s,\pi) = \E\left[   \NPV_i(a;d,s,\pi)-\NPV_i(a_0;d,s,\pi)   \mid \mathcal{I}_{id}   \right]` from the surrounding proposition/proof context.
- Smallest next audit: `audit_derivation_v2_label` on `eq:proposal-objective` - Rerun the local derivation audit after applying or formalizing the proposed repair.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:proposal-objective:obligation_1`

### 2. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > The Valuation Problem and Decision Semantics > Valuation Object, State Space, and Wallet Accounting > line 665`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Proposed fix: Replace the affected displayed math with the replacement LaTeX below, then rerun the referenced audit before treating the edit as certified.
- Replacement LaTeX:

```latex
\begin{equation}
  \Delta \NPV_i(a;d,s,\pi)
  =
  -C_i^{\mathrm{acq}}(a)
  +
  \E\!\left[
  \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s)
  +\delta_H\Delta TV_{i,t+H}(a,\pi;s)
  \mid X_{it}^{d}
  \right]
\end{equation}
```
- Proof target: `\Delta \NPV_i(a;d,s,\pi) = -C_i^{\mathrm{acq}}(a)   +   \E\!\left[   \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s)   +\delta_H\Delta TV_{i,t+H}(a,\pi;s)   \mid X_{it}^{d}   \right]`
- Derivation route: Justify the reconstructed equality `\Delta \NPV_i(a;d,s,\pi) = -C_i^{\mathrm{acq}}(a)   +   \E\!\left[   \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s)   +\delta_H\Delta TV_{i,t+H}(a,\pi;s)   \mid X_{it}^{d}   \right]` from the surrounding proposition/proof context.
- Smallest next audit: `audit_derivation_v2_label` on `eq:panel-npv-functional` - Rerun the local derivation audit after applying or formalizing the proposed repair.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:panel-npv-functional:obligation_2`

### 3. `obligation_4`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 842`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Proposed fix: Replace the affected displayed math with the replacement LaTeX below, then rerun the referenced audit before treating the edit as certified.
- Replacement LaTeX:

```latex
\begin{equation}
  \Delta CF_{i,t+h}(a,\pi;s)
  =
  \Delta PPNR_{i,t+h}(a,\pi;s)
  - \Delta EL_{i,t+h}(a,\pi;s)
  - \Delta Kchg_{i,t+h}(a,\pi;s)
\end{equation}
```
- Proof target: `\Delta CF_{i,t+h}(a,\pi;s) = \Delta PPNR_{i,t+h}(a,\pi;s)   - \Delta EL_{i,t+h}(a,\pi;s)   - \Delta Kchg_{i,t+h}(a,\pi;s)`
- Derivation route: Justify the reconstructed equality `\Delta CF_{i,t+h}(a,\pi;s) = \Delta PPNR_{i,t+h}(a,\pi;s)   - \Delta EL_{i,t+h}(a,\pi;s)   - \Delta Kchg_{i,t+h}(a,\pi;s)` from the surrounding proposition/proof context.
- Smallest next audit: `audit_derivation_v2_label` on `eq:incremental-npv` - Rerun the local derivation audit after applying or formalizing the proposed repair.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_4`

### 4. `obligation_3`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4089`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Proposed fix: Replace the affected displayed math with the replacement LaTeX below, then rerun the referenced audit before treating the edit as certified.
- Replacement LaTeX:

```latex
\begin{equation}
  J^{\varphi}_{c,k}(b,O;s)
  =
  \E^{\varphi,\pi^{down}}\!\left[
  \sum_{h=t}^{H-1}\delta^{h-t}
  c_{k,h}(b_{ih},O_{ih},a_{ih};s)
  \mid b_{it}=b,O_{it}=O
  \right]
\end{equation}
```
- Proof target: `J^{\varphi}_{c,k}(b,O;s) = \E^{\varphi,\pi^{down}}\!\left[   \sum_{h=t}^{H-1}\delta^{h-t}   c_{k,h}(b_{ih},O_{ih},a_{ih};s)   \mid b_{it}=b,O_{it}=O   \right]`
- Derivation route: Justify the reconstructed equality `J^{\varphi}_{c,k}(b,O;s) = \E^{\varphi,\pi^{down}}\!\left[   \sum_{h=t}^{H-1}\delta^{h-t}   c_{k,h}(b_{ih},O_{ih},a_{ih};s)   \mid b_{it}=b,O_{it}=O   \right]` from the surrounding proposition/proof context.
- Smallest next audit: `audit_derivation_v2_label` on `eq:ss-bellman` - Rerun the local derivation audit after applying or formalizing the proposed repair.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_3`


## Diagnostic Abstention Ledger

### 1. `obligation_3`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 834`
- Problem: The claim still needs human review before certification.
- Why mathematically problematic: Typed obligation requires human review or additional formalization.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: `add_review_boundary` is a certification or evidence gap unless it includes exact replacement text or an assumption statement.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
- Blocker kind: `generic_formalization`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `formalized_local_obligation` (formalization_condition): A typed local obligation with defined symbols, domains, and operator meanings.
    Why missing: The diagnostic source does not yet expose enough structure for a mathematical repair.
    Closes: Creates the next deterministic target for assumption discovery or proof audit.
- Possible sufficient assumption sets:
  - `typed_obligation_first` (next deterministic artifact): Makes the abstention inspectable by deterministic tooling.
    - Define every symbol, domain, and operator in the cited source line.
    - Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic.
    - Rerun the relevant assumption/proof audit after the typed obligation exists.
- How the derivation can work under the assumptions:
  - Formalize local obligation: Convert the cited line into a typed obligation before proposing a document edit.
- Actionable abstention next audit: `audit_and_propose_fix` - Regenerate concrete proposals after adding the listed obligations.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Smallest next audit: `audit_and_propose_fix` on `eq:incremental-npv` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `not_certified` - No structured backend validation evidence was attached to this proposal detail.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_3`

### 2. `obligation_5`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 852`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: The reconstructed replacement LaTeX failed conservative structure checks.
- Required evidence before repair:
  - A concrete repair payload that can be checked by the next audit.
- Blocker kind: `malformed_replacement_latex+conditional_expectation+npv_accounting_identity`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `balanced_replacement_latex` (parser_provenance_condition): Balanced LaTeX delimiters and a complete displayed-math environment for the proposed replacement.
    Why missing: A malformed replacement cannot be safely applied or checked by symbolic/formal tools.
    Closes: Makes the replacement text parseable before mathematical validation.
  - `source_span_reconstruction` (provenance_condition): A source span that contains the full equality, not only a fragment of a multiline expression.
    Why missing: Partial source reconstruction can drop closing delimiters or terms and create a false repair.
    Closes: Lets the audit reconstruct the intended proof target from complete evidence.
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `baseline_and_action_paths_defined` (counterfactual_condition): Definitions of the baseline path and the action path used in the incremental NPV.
    Why missing: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
    Closes: Makes the counterfactual comparison well posed.
  - `cash_flow_components_exhaustive` (accounting_identity_condition): A statement that the listed cash-flow components are exhaustive and share the same sign convention.
    Why missing: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
    Closes: Justifies replacing total incremental cash flow by the listed component sum.
  - `discount_horizon_terminal_value_defined` (valuation_condition): Definitions of the horizon, discount factors, and terminal-value term.
    Why missing: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
    Closes: Makes the finite-horizon valuation expression well defined.
- Possible sufficient assumption sets:
  - `complete_source_span_first` (repair precondition): Prevents a partial parser reconstruction from being treated as a mathematical edit.
    - The cited source span contains the complete displayed expression.
    - The proposed replacement compiles as standalone LaTeX display math.
    - The proof target is extracted from the same complete replacement.
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_horizon_incremental_npv` (simple sufficient condition): The incremental NPV expression is a finite, aligned accounting/valuation identity.
    - The baseline and action paths are defined on the same horizon and information set.
    - All cash-flow components use the same currency, time index, and sign convention.
    - Discount factors and terminal value are finite and defined for the horizon.
- How the derivation can work under the assumptions:
  - Recover full source span: Extract the entire displayed equation or align environment around the cited line.
  - Check LaTeX structure: Verify delimiters and begin/end environments are balanced before presenting replacement text.
  - Rerun derivation audit: Only after parseable replacement text exists should proof-audit run on the reconstructed target.
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Define two paths: Write the action path and baseline path under the same information set.
  - Decompose cash flow: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
  - Discount and aggregate: Apply the stated discount factors and terminal-value convention over the finite horizon.
- Actionable abstention next audit: `audit_derivation_v2_label` - Recover a complete parseable source span, then rerun the derivation audit.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Replacement LaTeX:

```latex
\begin{equation}
  \Delta \NPV_i(a;d,s,\pi)
  =
  - C_i^{\mathrm{acq}}(a)
  +
  \E\left[
  \sum_{h=0}^{H}
  \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)
  + \delta_H\Delta TV_{i,t+H}(a,\pi;s)
  \,\middle|\, \mathcal{I}_{id}
\end{equation}
```
- Proof target: `\Delta \NPV_i(a;d,s,\pi) = - C_i^{\mathrm{acq}}(a)   +   \E\left[   \sum_{h=0}^{H}   \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)   + \delta_H\Delta TV_{i,t+H}(a,\pi;s)   \,\middle\|\, \mathcal{I}_{id}`
- Derivation route: Justify the reconstructed equality `\Delta \NPV_i(a;d,s,\pi) = - C_i^{\mathrm{acq}}(a)   +   \E\left[   \sum_{h=0}^{H}   \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)   + \delta_H\Delta TV_{i,t+H}(a,\pi;s)   \,\middle\|\, \mathcal{I}_{id}` from the surrounding proposition/proof context.
- Smallest next audit: `audit_and_propose_fix` on `eq:incremental-npv` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_5`

### 3. `obligation_6`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 856`
- Problem: The claim still needs human review before certification.
- Why mathematically problematic: Typed obligation requires human review or additional formalization.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: `add_review_boundary` is a certification or evidence gap unless it includes exact replacement text or an assumption statement.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
- Blocker kind: `generic_formalization`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `formalized_local_obligation` (formalization_condition): A typed local obligation with defined symbols, domains, and operator meanings.
    Why missing: The diagnostic source does not yet expose enough structure for a mathematical repair.
    Closes: Creates the next deterministic target for assumption discovery or proof audit.
- Possible sufficient assumption sets:
  - `typed_obligation_first` (next deterministic artifact): Makes the abstention inspectable by deterministic tooling.
    - Define every symbol, domain, and operator in the cited source line.
    - Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic.
    - Rerun the relevant assumption/proof audit after the typed obligation exists.
- How the derivation can work under the assumptions:
  - Formalize local obligation: Convert the cited line into a typed obligation before proposing a document edit.
- Actionable abstention next audit: `audit_and_propose_fix` - Regenerate concrete proposals after adding the listed obligations.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Smallest next audit: `audit_and_propose_fix` on `eq:incremental-npv` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `not_certified` - No structured backend validation evidence was attached to this proposal detail.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_6`

### 4. `conformable_product_required`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Problem: Missing constraint `conformable_product_required`.
- Why mathematically problematic: Transpose and matrix product notation require conformable dimensions.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: No exact replacement text, assumption statement, safe wording, or derivation route was attached.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
  - An explicit assumption statement, not only an assumption category or target name.
- Blocker kind: `conditional_expectation+bellman_value_recursion+shape_conformability`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `state_action_spaces_defined` (dynamic_programming_condition): Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
    Why missing: A Bellman maximization is not well posed until its domain and feasible controls are defined.
    Closes: Makes the optimization domain explicit.
  - `transition_kernel_defined` (probability_condition): A transition law for next-period states conditional on current state and action.
    Why missing: The continuation value is an expectation over next states; that expectation needs a transition kernel.
    Closes: Defines the stochastic continuation operator.
  - `reward_and_value_integrable` (integrability_condition): Finite reward and integrable continuation value under each admissible action.
    Why missing: The objective may be undefined or infinite without boundedness or integrability conditions.
    Closes: Makes the Bellman objective finite for comparison across actions.
  - `terminal_boundary_condition_defined` (recursion_boundary_condition): A terminal, transversality, or boundary condition for the recursive value.
    Why missing: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
    Closes: Closes the recursive definition.
  - `dimension_declarations` (shape_condition): Dimensions for every vector, matrix, and transposed object in the expression.
    Why missing: Matrix products and transposes are undefined unless the operands have conformable dimensions.
    Closes: Makes the matrix expression syntactically and semantically well formed.
  - `scalar_vector_matrix_roles` (type_condition): A scalar/vector/matrix role for each ambiguous symbol.
    Why missing: The same notation can denote scalars, vectors, or matrices; the product type changes with that role.
    Closes: Prevents a shape-compatible expression from being misread as a different object.
- Possible sufficient assumption sets:
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_state_finite_action_bellman` (simple sufficient condition): The Bellman operator is well defined and can be audited as a dynamic-programming recursion.
    - The state and action sets are finite or compact with a nonempty feasible set.
    - Rewards are finite and measurable.
    - A transition matrix or kernel is specified for each admissible action.
    - A terminal value or contraction condition is stated.
  - `explicit_dimension_contract` (minimal shape contract): Makes the expression well typed before any algebraic or proof audit.
    - Declare the dimension of every matrix and vector appearing in the product.
    - State that adjacent matrix products are conformable.
    - State whether transpose notation denotes an inner product, outer product, or matrix transpose.
- How the derivation can work under the assumptions:
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Declare state and actions: Specify the domain over which the maximum is taken.
  - Define transition and reward: State the reward map and transition law used to form expected continuation value.
  - Apply Bellman operator: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value.
  - Assign dimensions: Map each symbol to a scalar, vector, or matrix with explicit dimensions.
  - Check products: Verify adjacent dimensions match and the final expression has the claimed scalar/vector/matrix type.
- Actionable abstention next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Smallest next audit: `audit_and_propose_fix` on `eq:ss-bellman` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `not_certified` - No structured backend validation evidence was attached to this proposal detail.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

### 5. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Problem: The claim still needs human review before certification.
- Why mathematically problematic: Typed obligation has missing assumptions or dimension constraints.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: `add_review_boundary` is a certification or evidence gap unless it includes exact replacement text or an assumption statement.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
- Blocker kind: `conditional_expectation+bellman_value_recursion+shape_conformability`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `state_action_spaces_defined` (dynamic_programming_condition): Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
    Why missing: A Bellman maximization is not well posed until its domain and feasible controls are defined.
    Closes: Makes the optimization domain explicit.
  - `transition_kernel_defined` (probability_condition): A transition law for next-period states conditional on current state and action.
    Why missing: The continuation value is an expectation over next states; that expectation needs a transition kernel.
    Closes: Defines the stochastic continuation operator.
  - `reward_and_value_integrable` (integrability_condition): Finite reward and integrable continuation value under each admissible action.
    Why missing: The objective may be undefined or infinite without boundedness or integrability conditions.
    Closes: Makes the Bellman objective finite for comparison across actions.
  - `terminal_boundary_condition_defined` (recursion_boundary_condition): A terminal, transversality, or boundary condition for the recursive value.
    Why missing: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
    Closes: Closes the recursive definition.
  - `dimension_declarations` (shape_condition): Dimensions for every vector, matrix, and transposed object in the expression.
    Why missing: Matrix products and transposes are undefined unless the operands have conformable dimensions.
    Closes: Makes the matrix expression syntactically and semantically well formed.
  - `scalar_vector_matrix_roles` (type_condition): A scalar/vector/matrix role for each ambiguous symbol.
    Why missing: The same notation can denote scalars, vectors, or matrices; the product type changes with that role.
    Closes: Prevents a shape-compatible expression from being misread as a different object.
- Possible sufficient assumption sets:
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_state_finite_action_bellman` (simple sufficient condition): The Bellman operator is well defined and can be audited as a dynamic-programming recursion.
    - The state and action sets are finite or compact with a nonempty feasible set.
    - Rewards are finite and measurable.
    - A transition matrix or kernel is specified for each admissible action.
    - A terminal value or contraction condition is stated.
  - `explicit_dimension_contract` (minimal shape contract): Makes the expression well typed before any algebraic or proof audit.
    - Declare the dimension of every matrix and vector appearing in the product.
    - State that adjacent matrix products are conformable.
    - State whether transpose notation denotes an inner product, outer product, or matrix transpose.
- How the derivation can work under the assumptions:
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Declare state and actions: Specify the domain over which the maximum is taken.
  - Define transition and reward: State the reward map and transition law used to form expected continuation value.
  - Apply Bellman operator: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value.
  - Assign dimensions: Map each symbol to a scalar, vector, or matrix with explicit dimensions.
  - Check products: Verify adjacent dimensions match and the final expression has the claimed scalar/vector/matrix type.
- Actionable abstention next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Smallest next audit: `audit_and_propose_fix` on `eq:ss-bellman` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `not_certified` - No structured backend validation evidence was attached to this proposal detail.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

### 6. `obligation_4`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4091`
- Problem: The claim still needs human review before certification.
- Why mathematically problematic: Typed obligation requires human review or additional formalization.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: `add_review_boundary` is a certification or evidence gap unless it includes exact replacement text or an assumption statement.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
- Blocker kind: `generic_formalization`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `formalized_local_obligation` (formalization_condition): A typed local obligation with defined symbols, domains, and operator meanings.
    Why missing: The diagnostic source does not yet expose enough structure for a mathematical repair.
    Closes: Creates the next deterministic target for assumption discovery or proof audit.
- Possible sufficient assumption sets:
  - `typed_obligation_first` (next deterministic artifact): Makes the abstention inspectable by deterministic tooling.
    - Define every symbol, domain, and operator in the cited source line.
    - Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic.
    - Rerun the relevant assumption/proof audit after the typed obligation exists.
- How the derivation can work under the assumptions:
  - Formalize local obligation: Convert the cited line into a typed obligation before proposing a document edit.
- Actionable abstention next audit: `audit_and_propose_fix` - Regenerate concrete proposals after adding the listed obligations.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Smallest next audit: `audit_and_propose_fix` on `eq:ss-bellman` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `not_certified` - No structured backend validation evidence was attached to this proposal detail.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_4`

### 7. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Problem: Missing constraint `obligation_2`.
- Why mathematically problematic: Transpose and matrix product notation require conformable dimensions.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: No exact replacement text, assumption statement, safe wording, or derivation route was attached.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
  - An explicit assumption statement, not only an assumption category or target name.
- Blocker kind: `conditional_expectation+bellman_value_recursion+shape_conformability`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `state_action_spaces_defined` (dynamic_programming_condition): Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
    Why missing: A Bellman maximization is not well posed until its domain and feasible controls are defined.
    Closes: Makes the optimization domain explicit.
  - `transition_kernel_defined` (probability_condition): A transition law for next-period states conditional on current state and action.
    Why missing: The continuation value is an expectation over next states; that expectation needs a transition kernel.
    Closes: Defines the stochastic continuation operator.
  - `reward_and_value_integrable` (integrability_condition): Finite reward and integrable continuation value under each admissible action.
    Why missing: The objective may be undefined or infinite without boundedness or integrability conditions.
    Closes: Makes the Bellman objective finite for comparison across actions.
  - `terminal_boundary_condition_defined` (recursion_boundary_condition): A terminal, transversality, or boundary condition for the recursive value.
    Why missing: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
    Closes: Closes the recursive definition.
  - `dimension_declarations` (shape_condition): Dimensions for every vector, matrix, and transposed object in the expression.
    Why missing: Matrix products and transposes are undefined unless the operands have conformable dimensions.
    Closes: Makes the matrix expression syntactically and semantically well formed.
  - `scalar_vector_matrix_roles` (type_condition): A scalar/vector/matrix role for each ambiguous symbol.
    Why missing: The same notation can denote scalars, vectors, or matrices; the product type changes with that role.
    Closes: Prevents a shape-compatible expression from being misread as a different object.
- Possible sufficient assumption sets:
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_state_finite_action_bellman` (simple sufficient condition): The Bellman operator is well defined and can be audited as a dynamic-programming recursion.
    - The state and action sets are finite or compact with a nonempty feasible set.
    - Rewards are finite and measurable.
    - A transition matrix or kernel is specified for each admissible action.
    - A terminal value or contraction condition is stated.
  - `explicit_dimension_contract` (minimal shape contract): Makes the expression well typed before any algebraic or proof audit.
    - Declare the dimension of every matrix and vector appearing in the product.
    - State that adjacent matrix products are conformable.
    - State whether transpose notation denotes an inner product, outer product, or matrix transpose.
- How the derivation can work under the assumptions:
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Declare state and actions: Specify the domain over which the maximum is taken.
  - Define transition and reward: State the reward map and transition law used to form expected continuation value.
  - Apply Bellman operator: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value.
  - Assign dimensions: Map each symbol to a scalar, vector, or matrix with explicit dimensions.
  - Check products: Verify adjacent dimensions match and the final expression has the claimed scalar/vector/matrix type.
- Actionable abstention next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Smallest next audit: `audit_and_propose_fix` on `eq:ss-bellman` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `not_certified` - No structured backend validation evidence was attached to this proposal detail.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

### 8. `obligation_3`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 834`
- Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:manual_formalization_required` on route `human_review` and matrix-IR status `parsed_with_unresolved`. The obligation uses notation that requires human review or manual formalization.
- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Why not concrete: The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
- Blocker kind: `generic_formalization`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `formalized_local_obligation` (formalization_condition): A typed local obligation with defined symbols, domains, and operator meanings.
    Why missing: The diagnostic source does not yet expose enough structure for a mathematical repair.
    Closes: Creates the next deterministic target for assumption discovery or proof audit.
- Possible sufficient assumption sets:
  - `typed_obligation_first` (next deterministic artifact): Makes the abstention inspectable by deterministic tooling.
    - Define every symbol, domain, and operator in the cited source line.
    - Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic.
    - Rerun the relevant assumption/proof audit after the typed obligation exists.
- How the derivation can work under the assumptions:
  - Formalize local obligation: Convert the cited line into a typed obligation before proposing a document edit.
- Actionable abstention next audit: `audit_and_propose_fix` - Regenerate concrete proposals after adding the listed obligations.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Proof target: `\sum_{t=0}^{T} \delta_t \{R_{it}-C_{it}\}`
- Derivation route: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
- Smallest next audit: `audit_and_propose_fix` on `eq:incremental-npv` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_3`

### 9. `obligation_6`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 856`
- Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:manual_formalization_required` on route `human_review` and matrix-IR status `parsed_with_unresolved`. The obligation uses notation that requires human review or manual formalization.
- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Why not concrete: The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
- Blocker kind: `generic_formalization`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `formalized_local_obligation` (formalization_condition): A typed local obligation with defined symbols, domains, and operator meanings.
    Why missing: The diagnostic source does not yet expose enough structure for a mathematical repair.
    Closes: Creates the next deterministic target for assumption discovery or proof audit.
- Possible sufficient assumption sets:
  - `typed_obligation_first` (next deterministic artifact): Makes the abstention inspectable by deterministic tooling.
    - Define every symbol, domain, and operator in the cited source line.
    - Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic.
    - Rerun the relevant assumption/proof audit after the typed obligation exists.
- How the derivation can work under the assumptions:
  - Formalize local obligation: Convert the cited line into a typed obligation before proposing a document edit.
- Actionable abstention next audit: `audit_and_propose_fix` - Regenerate concrete proposals after adding the listed obligations.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Proof target: `\sum_{h=0}^{H}`
- Derivation route: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
- Smallest next audit: `audit_and_propose_fix` on `eq:incremental-npv` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_6`

### 10. `conformable_product_required`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Problem: The audit reports a missing assumption or shape constraint, but the current tools have not derived the exact assumption statement to insert here.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Why not concrete: The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
- Blocker kind: `conditional_expectation+bellman_value_recursion+shape_conformability`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `state_action_spaces_defined` (dynamic_programming_condition): Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
    Why missing: A Bellman maximization is not well posed until its domain and feasible controls are defined.
    Closes: Makes the optimization domain explicit.
  - `transition_kernel_defined` (probability_condition): A transition law for next-period states conditional on current state and action.
    Why missing: The continuation value is an expectation over next states; that expectation needs a transition kernel.
    Closes: Defines the stochastic continuation operator.
  - `reward_and_value_integrable` (integrability_condition): Finite reward and integrable continuation value under each admissible action.
    Why missing: The objective may be undefined or infinite without boundedness or integrability conditions.
    Closes: Makes the Bellman objective finite for comparison across actions.
  - `terminal_boundary_condition_defined` (recursion_boundary_condition): A terminal, transversality, or boundary condition for the recursive value.
    Why missing: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
    Closes: Closes the recursive definition.
  - `dimension_declarations` (shape_condition): Dimensions for every vector, matrix, and transposed object in the expression.
    Why missing: Matrix products and transposes are undefined unless the operands have conformable dimensions.
    Closes: Makes the matrix expression syntactically and semantically well formed.
  - `scalar_vector_matrix_roles` (type_condition): A scalar/vector/matrix role for each ambiguous symbol.
    Why missing: The same notation can denote scalars, vectors, or matrices; the product type changes with that role.
    Closes: Prevents a shape-compatible expression from being misread as a different object.
- Possible sufficient assumption sets:
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_state_finite_action_bellman` (simple sufficient condition): The Bellman operator is well defined and can be audited as a dynamic-programming recursion.
    - The state and action sets are finite or compact with a nonempty feasible set.
    - Rewards are finite and measurable.
    - A transition matrix or kernel is specified for each admissible action.
    - A terminal value or contraction condition is stated.
  - `explicit_dimension_contract` (minimal shape contract): Makes the expression well typed before any algebraic or proof audit.
    - Declare the dimension of every matrix and vector appearing in the product.
    - State that adjacent matrix products are conformable.
    - State whether transpose notation denotes an inner product, outer product, or matrix transpose.
- How the derivation can work under the assumptions:
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Declare state and actions: Specify the domain over which the maximum is taken.
  - Define transition and reward: State the reward map and transition law used to form expected continuation value.
  - Apply Bellman operator: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value.
  - Assign dimensions: Map each symbol to a scalar, vector, or matrix with explicit dimensions.
  - Check products: Verify adjacent dimensions match and the final expression has the claimed scalar/vector/matrix type.
- Actionable abstention next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Proof target: `+ \delta\,\E\left[V_{t+1}^{\star}(b',O';s)\mid b,O,a,s,\pi^{down}\right]`
- Derivation route: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
- Smallest next audit: `audit_and_propose_fix` on `eq:ss-bellman` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `not_encodable` - No configured backend could encode this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

### 11. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Why not concrete: The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
- Blocker kind: `conditional_expectation+bellman_value_recursion+shape_conformability`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `state_action_spaces_defined` (dynamic_programming_condition): Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
    Why missing: A Bellman maximization is not well posed until its domain and feasible controls are defined.
    Closes: Makes the optimization domain explicit.
  - `transition_kernel_defined` (probability_condition): A transition law for next-period states conditional on current state and action.
    Why missing: The continuation value is an expectation over next states; that expectation needs a transition kernel.
    Closes: Defines the stochastic continuation operator.
  - `reward_and_value_integrable` (integrability_condition): Finite reward and integrable continuation value under each admissible action.
    Why missing: The objective may be undefined or infinite without boundedness or integrability conditions.
    Closes: Makes the Bellman objective finite for comparison across actions.
  - `terminal_boundary_condition_defined` (recursion_boundary_condition): A terminal, transversality, or boundary condition for the recursive value.
    Why missing: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
    Closes: Closes the recursive definition.
  - `dimension_declarations` (shape_condition): Dimensions for every vector, matrix, and transposed object in the expression.
    Why missing: Matrix products and transposes are undefined unless the operands have conformable dimensions.
    Closes: Makes the matrix expression syntactically and semantically well formed.
  - `scalar_vector_matrix_roles` (type_condition): A scalar/vector/matrix role for each ambiguous symbol.
    Why missing: The same notation can denote scalars, vectors, or matrices; the product type changes with that role.
    Closes: Prevents a shape-compatible expression from being misread as a different object.
- Possible sufficient assumption sets:
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_state_finite_action_bellman` (simple sufficient condition): The Bellman operator is well defined and can be audited as a dynamic-programming recursion.
    - The state and action sets are finite or compact with a nonempty feasible set.
    - Rewards are finite and measurable.
    - A transition matrix or kernel is specified for each admissible action.
    - A terminal value or contraction condition is stated.
  - `explicit_dimension_contract` (minimal shape contract): Makes the expression well typed before any algebraic or proof audit.
    - Declare the dimension of every matrix and vector appearing in the product.
    - State that adjacent matrix products are conformable.
    - State whether transpose notation denotes an inner product, outer product, or matrix transpose.
- How the derivation can work under the assumptions:
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Declare state and actions: Specify the domain over which the maximum is taken.
  - Define transition and reward: State the reward map and transition law used to form expected continuation value.
  - Apply Bellman operator: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value.
  - Assign dimensions: Map each symbol to a scalar, vector, or matrix with explicit dimensions.
  - Check products: Verify adjacent dimensions match and the final expression has the claimed scalar/vector/matrix type.
- Actionable abstention next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Proof target: `+ \delta\,\E\left[V_{t+1}^{\star}(b',O';s)\mid b,O,a,s,\pi^{down}\right]`
- Derivation route: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
- Smallest next audit: `audit_and_propose_fix` on `eq:ss-bellman` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `not_encodable` - No configured backend could encode this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

### 12. `obligation_4`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4091`
- Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:manual_formalization_required` on route `human_review` and matrix-IR status `parsed_with_unresolved`. The obligation uses notation that requires human review or manual formalization.
- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Why not concrete: The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit.
- Required evidence before repair:
  - Exact replacement LaTeX or exact safe wording tied to the cited source line.
- Blocker kind: `generic_formalization`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `formalized_local_obligation` (formalization_condition): A typed local obligation with defined symbols, domains, and operator meanings.
    Why missing: The diagnostic source does not yet expose enough structure for a mathematical repair.
    Closes: Creates the next deterministic target for assumption discovery or proof audit.
- Possible sufficient assumption sets:
  - `typed_obligation_first` (next deterministic artifact): Makes the abstention inspectable by deterministic tooling.
    - Define every symbol, domain, and operator in the cited source line.
    - Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic.
    - Rerun the relevant assumption/proof audit after the typed obligation exists.
- How the derivation can work under the assumptions:
  - Formalize local obligation: Convert the cited line into a typed obligation before proposing a document edit.
- Actionable abstention next audit: `audit_and_propose_fix` - Regenerate concrete proposals after adding the listed obligations.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Proof target: `\sum_{h=t}^{H-1}\delta^{h-t}`
- Derivation route: Use the referenced proof-audit obligation to derive a concrete local obligation; if the source is prose, refine the parser/provenance before proposing an edit.
- Smallest next audit: `audit_and_propose_fix` on `eq:ss-bellman` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_4`

### 13. `obligation_1`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Executive Proposal and Decision Request > line 252`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit.
- Required evidence before repair:
  - A concrete repair payload that can be checked by the next audit.
- Blocker kind: `conditional_expectation+npv_accounting_identity`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `baseline_and_action_paths_defined` (counterfactual_condition): Definitions of the baseline path and the action path used in the incremental NPV.
    Why missing: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
    Closes: Makes the counterfactual comparison well posed.
  - `cash_flow_components_exhaustive` (accounting_identity_condition): A statement that the listed cash-flow components are exhaustive and share the same sign convention.
    Why missing: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
    Closes: Justifies replacing total incremental cash flow by the listed component sum.
  - `discount_horizon_terminal_value_defined` (valuation_condition): Definitions of the horizon, discount factors, and terminal-value term.
    Why missing: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
    Closes: Makes the finite-horizon valuation expression well defined.
- Possible sufficient assumption sets:
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_horizon_incremental_npv` (simple sufficient condition): The incremental NPV expression is a finite, aligned accounting/valuation identity.
    - The baseline and action paths are defined on the same horizon and information set.
    - All cash-flow components use the same currency, time index, and sign convention.
    - Discount factors and terminal value are finite and defined for the horizon.
- How the derivation can work under the assumptions:
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Define two paths: Write the action path and baseline path under the same information set.
  - Decompose cash flow: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
  - Discount and aggregate: Apply the stated discount factors and terminal-value convention over the finite horizon.
- Actionable abstention next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Replacement LaTeX:

```latex
\begin{equation}
  \Delta \NPV_i(a;d,s,\pi)
  =
  \E\left[
  \NPV_i(a;d,s,\pi)-\NPV_i(a_0;d,s,\pi)
  \mid \mathcal{I}_{id}
  \right]
\end{equation}
```
- Proof target: `\Delta \NPV_i(a;d,s,\pi) = \E\left[   \NPV_i(a;d,s,\pi)-\NPV_i(a_0;d,s,\pi)   \mid \mathcal{I}_{id}   \right]`
- Derivation route: Justify the reconstructed equality `\Delta \NPV_i(a;d,s,\pi) = \E\left[   \NPV_i(a;d,s,\pi)-\NPV_i(a_0;d,s,\pi)   \mid \mathcal{I}_{id}   \right]` from the surrounding proposition/proof context.
- Smallest next audit: `audit_and_propose_fix` on `eq:proposal-objective` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:proposal-objective:obligation_1`

### 14. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > The Valuation Problem and Decision Semantics > Valuation Object, State Space, and Wallet Accounting > line 665`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit.
- Required evidence before repair:
  - A concrete repair payload that can be checked by the next audit.
- Blocker kind: `conditional_expectation+npv_accounting_identity`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `baseline_and_action_paths_defined` (counterfactual_condition): Definitions of the baseline path and the action path used in the incremental NPV.
    Why missing: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
    Closes: Makes the counterfactual comparison well posed.
  - `cash_flow_components_exhaustive` (accounting_identity_condition): A statement that the listed cash-flow components are exhaustive and share the same sign convention.
    Why missing: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
    Closes: Justifies replacing total incremental cash flow by the listed component sum.
  - `discount_horizon_terminal_value_defined` (valuation_condition): Definitions of the horizon, discount factors, and terminal-value term.
    Why missing: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
    Closes: Makes the finite-horizon valuation expression well defined.
- Possible sufficient assumption sets:
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_horizon_incremental_npv` (simple sufficient condition): The incremental NPV expression is a finite, aligned accounting/valuation identity.
    - The baseline and action paths are defined on the same horizon and information set.
    - All cash-flow components use the same currency, time index, and sign convention.
    - Discount factors and terminal value are finite and defined for the horizon.
- How the derivation can work under the assumptions:
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Define two paths: Write the action path and baseline path under the same information set.
  - Decompose cash flow: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
  - Discount and aggregate: Apply the stated discount factors and terminal-value convention over the finite horizon.
- Actionable abstention next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Replacement LaTeX:

```latex
\begin{equation}
  \Delta \NPV_i(a;d,s,\pi)
  =
  -C_i^{\mathrm{acq}}(a)
  +
  \E\!\left[
  \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s)
  +\delta_H\Delta TV_{i,t+H}(a,\pi;s)
  \mid X_{it}^{d}
  \right]
\end{equation}
```
- Proof target: `\Delta \NPV_i(a;d,s,\pi) = -C_i^{\mathrm{acq}}(a)   +   \E\!\left[   \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s)   +\delta_H\Delta TV_{i,t+H}(a,\pi;s)   \mid X_{it}^{d}   \right]`
- Derivation route: Justify the reconstructed equality `\Delta \NPV_i(a;d,s,\pi) = -C_i^{\mathrm{acq}}(a)   +   \E\!\left[   \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s)   +\delta_H\Delta TV_{i,t+H}(a,\pi;s)   \mid X_{it}^{d}   \right]` from the surrounding proposition/proof context.
- Smallest next audit: `audit_and_propose_fix` on `eq:panel-npv-functional` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:panel-npv-functional:obligation_2`

### 15. `obligation_4`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 842`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit.
- Required evidence before repair:
  - A concrete repair payload that can be checked by the next audit.
- Blocker kind: `npv_accounting_identity`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `baseline_and_action_paths_defined` (counterfactual_condition): Definitions of the baseline path and the action path used in the incremental NPV.
    Why missing: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
    Closes: Makes the counterfactual comparison well posed.
  - `cash_flow_components_exhaustive` (accounting_identity_condition): A statement that the listed cash-flow components are exhaustive and share the same sign convention.
    Why missing: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
    Closes: Justifies replacing total incremental cash flow by the listed component sum.
  - `discount_horizon_terminal_value_defined` (valuation_condition): Definitions of the horizon, discount factors, and terminal-value term.
    Why missing: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
    Closes: Makes the finite-horizon valuation expression well defined.
- Possible sufficient assumption sets:
  - `finite_horizon_incremental_npv` (simple sufficient condition): The incremental NPV expression is a finite, aligned accounting/valuation identity.
    - The baseline and action paths are defined on the same horizon and information set.
    - All cash-flow components use the same currency, time index, and sign convention.
    - Discount factors and terminal value are finite and defined for the horizon.
- How the derivation can work under the assumptions:
  - Define two paths: Write the action path and baseline path under the same information set.
  - Decompose cash flow: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
  - Discount and aggregate: Apply the stated discount factors and terminal-value convention over the finite horizon.
- Actionable abstention next audit: `audit_and_propose_fix` - Regenerate concrete proposals after adding the listed obligations.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Replacement LaTeX:

```latex
\begin{equation}
  \Delta CF_{i,t+h}(a,\pi;s)
  =
  \Delta PPNR_{i,t+h}(a,\pi;s)
  - \Delta EL_{i,t+h}(a,\pi;s)
  - \Delta Kchg_{i,t+h}(a,\pi;s)
\end{equation}
```
- Proof target: `\Delta CF_{i,t+h}(a,\pi;s) = \Delta PPNR_{i,t+h}(a,\pi;s)   - \Delta EL_{i,t+h}(a,\pi;s)   - \Delta Kchg_{i,t+h}(a,\pi;s)`
- Derivation route: Justify the reconstructed equality `\Delta CF_{i,t+h}(a,\pi;s) = \Delta PPNR_{i,t+h}(a,\pi;s)   - \Delta EL_{i,t+h}(a,\pi;s)   - \Delta Kchg_{i,t+h}(a,\pi;s)` from the surrounding proposition/proof context.
- Smallest next audit: `audit_and_propose_fix` on `eq:incremental-npv` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_4`

### 16. `obligation_5`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 852`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: The source detail is evidence-only and its reconstructed replacement LaTeX failed conservative structure checks.
- Required evidence before repair:
  - A concrete repair payload that can be checked by the next audit.
- Blocker kind: `malformed_replacement_latex+conditional_expectation+npv_accounting_identity`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `balanced_replacement_latex` (parser_provenance_condition): Balanced LaTeX delimiters and a complete displayed-math environment for the proposed replacement.
    Why missing: A malformed replacement cannot be safely applied or checked by symbolic/formal tools.
    Closes: Makes the replacement text parseable before mathematical validation.
  - `source_span_reconstruction` (provenance_condition): A source span that contains the full equality, not only a fragment of a multiline expression.
    Why missing: Partial source reconstruction can drop closing delimiters or terms and create a false repair.
    Closes: Lets the audit reconstruct the intended proof target from complete evidence.
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `baseline_and_action_paths_defined` (counterfactual_condition): Definitions of the baseline path and the action path used in the incremental NPV.
    Why missing: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
    Closes: Makes the counterfactual comparison well posed.
  - `cash_flow_components_exhaustive` (accounting_identity_condition): A statement that the listed cash-flow components are exhaustive and share the same sign convention.
    Why missing: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
    Closes: Justifies replacing total incremental cash flow by the listed component sum.
  - `discount_horizon_terminal_value_defined` (valuation_condition): Definitions of the horizon, discount factors, and terminal-value term.
    Why missing: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
    Closes: Makes the finite-horizon valuation expression well defined.
- Possible sufficient assumption sets:
  - `complete_source_span_first` (repair precondition): Prevents a partial parser reconstruction from being treated as a mathematical edit.
    - The cited source span contains the complete displayed expression.
    - The proposed replacement compiles as standalone LaTeX display math.
    - The proof target is extracted from the same complete replacement.
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_horizon_incremental_npv` (simple sufficient condition): The incremental NPV expression is a finite, aligned accounting/valuation identity.
    - The baseline and action paths are defined on the same horizon and information set.
    - All cash-flow components use the same currency, time index, and sign convention.
    - Discount factors and terminal value are finite and defined for the horizon.
- How the derivation can work under the assumptions:
  - Recover full source span: Extract the entire displayed equation or align environment around the cited line.
  - Check LaTeX structure: Verify delimiters and begin/end environments are balanced before presenting replacement text.
  - Rerun derivation audit: Only after parseable replacement text exists should proof-audit run on the reconstructed target.
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Define two paths: Write the action path and baseline path under the same information set.
  - Decompose cash flow: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
  - Discount and aggregate: Apply the stated discount factors and terminal-value convention over the finite horizon.
- Actionable abstention next audit: `audit_derivation_v2_label` - Recover a complete parseable source span, then rerun the derivation audit.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Replacement LaTeX:

```latex
\begin{equation}
  \Delta \NPV_i(a;d,s,\pi)
  =
  - C_i^{\mathrm{acq}}(a)
  +
  \E\left[
  \sum_{h=0}^{H}
  \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)
  + \delta_H\Delta TV_{i,t+H}(a,\pi;s)
  \,\middle|\, \mathcal{I}_{id}
\end{equation}
```
- Proof target: `\Delta \NPV_i(a;d,s,\pi) = - C_i^{\mathrm{acq}}(a)   +   \E\left[   \sum_{h=0}^{H}   \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)   + \delta_H\Delta TV_{i,t+H}(a,\pi;s)   \,\middle\|\, \mathcal{I}_{id}`
- Derivation route: Justify the reconstructed equality `\Delta \NPV_i(a;d,s,\pi) = - C_i^{\mathrm{acq}}(a)   +   \E\left[   \sum_{h=0}^{H}   \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)   + \delta_H\Delta TV_{i,t+H}(a,\pi;s)   \,\middle\|\, \mathcal{I}_{id}` from the surrounding proposition/proof context.
- Smallest next audit: `audit_and_propose_fix` on `eq:incremental-npv` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_5`

### 17. `obligation_3`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4089`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Why not concrete: The source detail is marked evidence-only; it is useful audit evidence, not a proposed document edit.
- Required evidence before repair:
  - A concrete repair payload that can be checked by the next audit.
- Blocker kind: `conditional_expectation+bellman_value_recursion`
- Safe wording: Do not treat this item as a document edit yet. State the missing obligations below, choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair.
- Mathematically missing obligations:
  - `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
    Why missing: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
    Closes: Makes the expectation operator well defined.
  - `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
    Why missing: Without measurability and integrability, the expectation may be undefined or infinite.
    Closes: Turns the displayed expression into a finite scalar equality.
  - `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
    Why missing: The notation after the conditional bar determines what information the expectation conditions on.
    Closes: Fixes the scope of the conditional expectation used in the derivation.
  - `state_action_spaces_defined` (dynamic_programming_condition): Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
    Why missing: A Bellman maximization is not well posed until its domain and feasible controls are defined.
    Closes: Makes the optimization domain explicit.
  - `transition_kernel_defined` (probability_condition): A transition law for next-period states conditional on current state and action.
    Why missing: The continuation value is an expectation over next states; that expectation needs a transition kernel.
    Closes: Defines the stochastic continuation operator.
  - `reward_and_value_integrable` (integrability_condition): Finite reward and integrable continuation value under each admissible action.
    Why missing: The objective may be undefined or infinite without boundedness or integrability conditions.
    Closes: Makes the Bellman objective finite for comparison across actions.
  - `terminal_boundary_condition_defined` (recursion_boundary_condition): A terminal, transversality, or boundary condition for the recursive value.
    Why missing: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
    Closes: Closes the recursive definition.
- Possible sufficient assumption sets:
  - `finite_state_conditional_expectation` (simple sufficient condition): The expectation becomes a finite weighted sum.
    - The conditioned shock or path has finite support.
    - Every payoff/value term inside the expectation is finite at each support point.
    - The conditioning state or information set is explicitly defined.
  - `kernel_integrability_condition` (general sufficient condition): The expectation is a well-defined finite conditional integral.
    - A conditional kernel or probability law is fixed for the random object.
    - All random terms inside the expectation are measurable under that law.
    - Those terms are dominated by an integrable envelope or have finite conditional first moments.
  - `finite_state_finite_action_bellman` (simple sufficient condition): The Bellman operator is well defined and can be audited as a dynamic-programming recursion.
    - The state and action sets are finite or compact with a nonempty feasible set.
    - Rewards are finite and measurable.
    - A transition matrix or kernel is specified for each admissible action.
    - A terminal value or contraction condition is stated.
- How the derivation can work under the assumptions:
  - Define conditional law: Specify the kernel or conditional distribution used by the expectation.
  - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation.
  - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - Declare state and actions: Specify the domain over which the maximum is taken.
  - Define transition and reward: State the reward map and transition law used to form expected continuation value.
  - Apply Bellman operator: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value.
- Actionable abstention next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.
- Abstention non-claim: These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.
- Replacement LaTeX:

```latex
\begin{equation}
  J^{\varphi}_{c,k}(b,O;s)
  =
  \E^{\varphi,\pi^{down}}\!\left[
  \sum_{h=t}^{H-1}\delta^{h-t}
  c_{k,h}(b_{ih},O_{ih},a_{ih};s)
  \mid b_{it}=b,O_{it}=O
  \right]
\end{equation}
```
- Proof target: `J^{\varphi}_{c,k}(b,O;s) = \E^{\varphi,\pi^{down}}\!\left[   \sum_{h=t}^{H-1}\delta^{h-t}   c_{k,h}(b_{ih},O_{ih},a_{ih};s)   \mid b_{it}=b,O_{it}=O   \right]`
- Derivation route: Justify the reconstructed equality `J^{\varphi}_{c,k}(b,O;s) = \E^{\varphi,\pi^{down}}\!\left[   \sum_{h=t}^{H-1}\delta^{h-t}   c_{k,h}(b_{ih},O_{ih},a_{ih};s)   \mid b_{it}=b,O_{it}=O   \right]` from the surrounding proposition/proof context.
- Smallest next audit: `audit_and_propose_fix` on `eq:ss-bellman` - Regenerate the proposal after adding the required concrete payload.
- Backend evidence: `attempted_not_certified` - Configured backends were attempted, but none certified or refuted this proposed fix target.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_3`


## Gap And Proposal Ledger

### 1. `obligation_1`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Executive Proposal and Decision Request > line 252`
- Classification: `concrete_repair`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:proposal-objective:obligation_1`

- Proposed fix: Replace the affected displayed math with the replacement LaTeX below, then rerun the referenced audit before treating the edit as certified.
- Backend evidence: `attempted_not_certified`

### 2. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > The Valuation Problem and Decision Semantics > Valuation Object, State Space, and Wallet Accounting > line 665`
- Classification: `concrete_repair`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:panel-npv-functional:obligation_2`

- Proposed fix: Replace the affected displayed math with the replacement LaTeX below, then rerun the referenced audit before treating the edit as certified.
- Backend evidence: `attempted_not_certified`

### 3. `obligation_3`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 834`
- Classification: `diagnostic_abstention`
- Problem: The claim still needs human review before certification.
- Why mathematically problematic: Typed obligation requires human review or additional formalization.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_3`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `not_certified`

### 4. `obligation_4`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 842`
- Classification: `concrete_repair`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_4`

- Proposed fix: Replace the affected displayed math with the replacement LaTeX below, then rerun the referenced audit before treating the edit as certified.
- Backend evidence: `attempted_not_certified`

### 5. `obligation_5`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 852`
- Classification: `diagnostic_abstention`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_5`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `attempted_not_certified`

### 6. `obligation_6`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 856`
- Classification: `diagnostic_abstention`
- Problem: The claim still needs human review before certification.
- Why mathematically problematic: Typed obligation requires human review or additional formalization.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_6`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `not_certified`

### 7. `conformable_product_required`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Classification: `diagnostic_abstention`
- Problem: Missing constraint `conformable_product_required`.
- Why mathematically problematic: Transpose and matrix product notation require conformable dimensions.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `not_certified`

### 8. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Classification: `diagnostic_abstention`
- Problem: The claim still needs human review before certification.
- Why mathematically problematic: Typed obligation has missing assumptions or dimension constraints.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `not_certified`

### 9. `obligation_3`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4089`
- Classification: `concrete_repair`
- Problem: The derivation row is not split into a safe proof obligation.
- Why mathematically problematic: The derivation row was not split into a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_3`

- Proposed fix: Replace the affected displayed math with the replacement LaTeX below, then rerun the referenced audit before treating the edit as certified.
- Backend evidence: `attempted_not_certified`

### 10. `obligation_4`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4091`
- Classification: `diagnostic_abstention`
- Problem: The claim still needs human review before certification.
- Why mathematically problematic: Typed obligation requires human review or additional formalization.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_4`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `not_certified`

### 11. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Classification: `diagnostic_abstention`
- Problem: Missing constraint `obligation_2`.
- Why mathematically problematic: Transpose and matrix product notation require conformable dimensions.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `not_certified`

### 12. `obligation_3`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 834`
- Classification: `diagnostic_abstention`
- Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:manual_formalization_required` on route `human_review` and matrix-IR status `parsed_with_unresolved`. The obligation uses notation that requires human review or manual formalization.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_3`

- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Backend evidence: `attempted_not_certified`

### 13. `obligation_6`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 856`
- Classification: `diagnostic_abstention`
- Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:manual_formalization_required` on route `human_review` and matrix-IR status `parsed_with_unresolved`. The obligation uses notation that requires human review or manual formalization.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_6`

- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Backend evidence: `attempted_not_certified`

### 14. `conformable_product_required`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Classification: `diagnostic_abstention`
- Problem: The audit reports a missing assumption or shape constraint, but the current tools have not derived the exact assumption statement to insert here.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Backend evidence: `not_encodable`

### 15. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4074`
- Classification: `diagnostic_abstention`
- Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:missing_assumption` on route `human_review` and matrix-IR status `parsed`. The obligation has missing shape, dimension, or regularity constraints.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_2`

- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Backend evidence: `not_encodable`

### 16. `obligation_4`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4091`
- Classification: `diagnostic_abstention`
- Problem: The audit reports that this claim needs formalization or human review; that is a certification gap, not a document edit by itself.
- Why mathematically problematic: Proof-audit v2 returned `unverified` with substatus `unverified:manual_formalization_required` on route `human_review` and matrix-IR status `parsed_with_unresolved`. The obligation uses notation that requires human review or manual formalization.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_4`

- Proposed fix: Do not edit the document from this item alone. First produce a concrete assumption statement, replacement LaTeX, or proof obligation tied to the source line.
- Backend evidence: `attempted_not_certified`

### 17. `obligation_1`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Executive Proposal and Decision Request > line 252`
- Classification: `diagnostic_abstention`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:proposal-objective:obligation_1`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `attempted_not_certified`

### 18. `obligation_2`

- Location: `credit_card_npv_component_proposal_final_submission.tex > The Valuation Problem and Decision Semantics > Valuation Object, State Space, and Wallet Accounting > line 665`
- Classification: `diagnostic_abstention`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:panel-npv-functional:obligation_2`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `attempted_not_certified`

### 19. `obligation_4`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 842`
- Classification: `diagnostic_abstention`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_4`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `attempted_not_certified`

### 20. `obligation_5`

- Location: `credit_card_npv_component_proposal_final_submission.tex > line 852`
- Classification: `diagnostic_abstention`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:incremental-npv:obligation_5`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `attempted_not_certified`

### 21. `obligation_3`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Dynamic State-Space Model and Policy Simulation > Observation, Filtering, and Policy Value > Reward mapping and constrained belief-state policy value > line 4089`
- Classification: `diagnostic_abstention`
- Problem: The report has a concrete proof target, but proof-audit v2 has not certified the derivation for that target.
- Why mathematically problematic: Proof-audit v2 returned `inconclusive` with substatus `inconclusive:source_label_missing` on route `symbolic` and matrix-IR status `parsed`. The row could not be extracted as a safe proof obligation.
- Evidence refs: `proof_audit_v2:eq:ss-bellman:obligation_3`

- Proposed fix: Do not edit the document from this item alone; first satisfy the required evidence before repair.
- Backend evidence: `attempted_not_certified`

## Non-Claims

- `document_rigor_audit_not_document_proof`: The report is a rigor gap/proposal ledger, not a proof of the document.
- `partial_coverage_not_exhaustive`: Limited target selection is not an exhaustive full-document audit.
- `leandojo_not_certificate`: LeanDojo proof search is not a certificate unless the reconstructed Lean source passes direct Lean checking without placeholders.
