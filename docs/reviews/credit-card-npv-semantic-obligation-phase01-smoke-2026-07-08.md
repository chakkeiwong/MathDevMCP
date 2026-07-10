# Document Derivation Tree Audit

Target: `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex`

## Executive Summary

- Selected source rows: `1`
- Semantic packets: `1`
- Promoted branches: `0`
- Blockers: `9`
- This report is generic and document-local; it is not tied to a card-NPV-specific plan.

## Tools Used

| Tool | Purpose | Status | Contract | Arguments |
| --- | --- | --- | --- | --- |
| `locate_equations_in_file` | Localize source rows in the exact target file. | `completed` | `equation_rows` | `{"root": "docs/credit-card-npv-component-proposal", "tex_path": "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex"}` |
| `build_semantic_work_packet` | Classify each target and generate full-display semantic packets, missing obligations, assumption sets, and derivation routes. | `completed` | `semantic_work_packet` | `{"selected_rows": 1}` |
| `assumptions_required` | Detect route-required assumptions before backend proof attempts. | `completed` | `assumption_discovery_result` | `{"selected_rows": 1}` |
| `doctor_report` | Record external backend capability provenance. | `available` | `doctor_report` | `{"backend_env": "mathdevmcp-backends"}` |
| `can_derive_with_budget` | Run the external-tool-first branch controller on semantic packet targets. | `completed` | `derivation_search_tree_result` | `{"budget_profile": "standard", "max_attempts": 1, "selected_rows": 1}` |
| `render_derivation_tree_report` | Render each derivation tree into structured evidence sections. | `completed` | `derivation_tree_report_result` | `{"rendered_trees": 1}` |

## Target Packets And Trees

### 1. `eq:panel-npv-functional`

- Location: `credit_card_npv_component_proposal_final_submission.tex > The Valuation Problem and Decision Semantics > Valuation Object, State Space, and Wallet Accounting > eq:panel-npv-functional > line 664`
- Claim type: `valuation_identity_or_definition`
- Tree status: `budget_exhausted`
- Promotion guard: `can_promote=False`
- Semantic domains: `['conditional_expectation', 'npv_accounting_identity']`
- Extraction uncertainty: `[]`
- Full display span: `{'file': 'credit_card_npv_component_proposal_final_submission.tex', 'line_start': 663, 'line_end': 674, 'labels': ['eq:panel-npv-functional'], 'environment': 'equation', 'section_path': ['The Valuation Problem and Decision Semantics', 'Valuation Object, State Space, and Wallet Accounting']}`
- Operators: `['equality', 'conditional_expectation', 'conditional_bar', 'summation']`
- Symbols: `{'macros': ['\\Delta', '\\E', '\\NPV', '\\delta', '\\pi'], 'identifiers': ['CF_', 'C_i', 'H', 'TV_', 'X_', 'a', 'acq', 'd', 'h', 'i', 'it', 's', 't']}`

Source row target:

```tex
\Delta \NPV_i(a;d,s,\pi)
  =
  -C_i^{\mathrm{acq}}(a)
  +
  \E\!\left[
    \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s)
    +\delta_H\Delta TV_{i,t+H}(a,\pi;s)
    \mid X_{it}^{d}
  \right].
```

Full display target:

```tex
\begin{equation}
  \Delta \NPV_i(a;d,s,\pi)
  =
  -C_i^{\mathrm{acq}}(a)
  +
  \E\!\left[
    \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s)
    +\delta_H\Delta TV_{i,t+H}(a,\pi;s)
    \mid X_{it}^{d}
  \right].
  \label{eq:panel-npv-functional}
\end{equation}
```

Mathematically missing obligations:
- `conditional_law_defined` (probability_condition): A conditional probability law for the random variables inside the expectation.
  Why: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
  Closes: Makes the expectation operator well defined.
- `measurable_integrable_payoff_terms` (integrability_condition): Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
  Why: Without measurability and integrability, the expectation may be undefined or infinite.
  Closes: Turns the displayed expression into a finite scalar equality.
- `conditioning_information_defined` (information_condition): A definition of the conditioning information set, state, or sigma-field.
  Why: The notation after the conditional bar determines what information the expectation conditions on.
  Closes: Fixes the scope of the conditional expectation used in the derivation.
- `baseline_and_action_paths_defined` (counterfactual_condition): Definitions of the baseline path and the action path used in the incremental NPV.
  Why: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
  Closes: Makes the counterfactual comparison well posed.
- `cash_flow_components_exhaustive` (accounting_identity_condition): A statement that the listed cash-flow components are exhaustive and share the same sign convention.
  Why: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
  Closes: Justifies replacing total incremental cash flow by the listed component sum.
- `discount_horizon_terminal_value_defined` (valuation_condition): Definitions of the horizon, discount factors, and terminal-value term.
  Why: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
  Closes: Makes the finite-horizon valuation expression well defined.

Possible sufficient assumption sets:
- `finite_state_conditional_expectation`: The expectation becomes a finite weighted sum.
  - The conditioned shock or path has finite support.
  - Every payoff/value term inside the expectation is finite at each support point.
  - The conditioning state or information set is explicitly defined.
- `kernel_integrability_condition`: The expectation is a well-defined finite conditional integral.
  - A conditional kernel or probability law is fixed for the random object.
  - All random terms inside the expectation are measurable under that law.
  - Those terms are dominated by an integrable envelope or have finite conditional first moments.
- `finite_horizon_incremental_npv`: The incremental NPV expression is a finite, aligned accounting/valuation identity.
  - The baseline and action paths are defined on the same horizon and information set.
  - All cash-flow components use the same currency, time index, and sign convention.
  - Discount factors and terminal value are finite and defined for the horizon.

How the derivation can work:
- `Define conditional law`: Specify the kernel or conditional distribution used by the expectation.
- `Check integrability`: Verify each random payoff, value, or derivative term has a finite conditional expectation.
- `Use expectation as scalar`: Only after those checks should the equality be treated as a scalar derivation step.
- `Define two paths`: Write the action path and baseline path under the same information set.
- `Decompose cash flow`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
- `Discount and aggregate`: Apply the stated discount factors and terminal-value convention over the finite horizon.

Backend attempts:
- `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`

Remaining blockers:
- `blocker_lean_source_required` (formalization_required)
  Problem: Lean certification was selected but no Lean source was supplied.
  Why: Direct Lean checking requires an explicit Lean statement/proof artifact.
  Required next evidence: Supply Lean source or a formalization branch before Lean certification.
- `blocker_sympy_algebra_attempt` (adapter_diagnostic)
  Problem: sympy did not certify or refute the target.
  Why: The target has missing route-required assumptions.
  Required next evidence: Provide a certifying backend result, concrete counterexample, formalization, or stronger assumption set.
- `blocker_budget_exhausted` (budget_exhausted)
  Problem: The controller exhausted its attempt budget before proof or refutation.
  Why: Some scheduled evidence actions were not attempted within the selected budget profile.
  Required next evidence: Increase budget, provide a stronger formalization, or inspect exhausted actions.
- `blocker_semantic_packet_eq_panel_npv_functional_0_conditional_law_defined` (probability_condition)
  Problem: A conditional probability law for the random variables inside the expectation.
  Why: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
  Required next evidence: Makes the expectation operator well defined.
- `blocker_semantic_packet_eq_panel_npv_functional_0_measurable_integrable_payoff_terms` (integrability_condition)
  Problem: Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
  Why: Without measurability and integrability, the expectation may be undefined or infinite.
  Required next evidence: Turns the displayed expression into a finite scalar equality.
- `blocker_semantic_packet_eq_panel_npv_functional_0_conditioning_information_defined` (information_condition)
  Problem: A definition of the conditioning information set, state, or sigma-field.
  Why: The notation after the conditional bar determines what information the expectation conditions on.
  Required next evidence: Fixes the scope of the conditional expectation used in the derivation.
- `blocker_semantic_packet_eq_panel_npv_functional_0_baseline_and_action_paths_defined` (counterfactual_condition)
  Problem: Definitions of the baseline path and the action path used in the incremental NPV.
  Why: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
  Required next evidence: Makes the counterfactual comparison well posed.
- `blocker_semantic_packet_eq_panel_npv_functional_0_cash_flow_components_exhaustive` (accounting_identity_condition)
  Problem: A statement that the listed cash-flow components are exhaustive and share the same sign convention.
  Why: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
  Required next evidence: Justifies replacing total incremental cash flow by the listed component sum.
- `blocker_semantic_packet_eq_panel_npv_functional_0_discount_horizon_terminal_value_defined` (valuation_condition)
  Problem: Definitions of the horizon, discount factors, and terminal-value term.
  Why: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
  Required next evidence: Makes the finite-horizon valuation expression well defined.

Smallest next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.

## Non-Claims

- `document_tree_audit_not_document_proof`: This workflow is a semantic gap and tree-evidence report; it does not prove the whole document.
- `semantic_packets_not_certificates`: Missing obligations, assumption sets, and derivation routes are deterministic guidance, not proof certificates.
- `proof_search_not_final_certificate`: LeanDojo, Pantograph, retrieval, route plans, and static extraction are diagnostic until direct Lean or another certifying backend checks the scoped target.
