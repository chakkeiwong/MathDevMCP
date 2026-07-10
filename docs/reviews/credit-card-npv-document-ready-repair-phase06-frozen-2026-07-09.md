# Document Derivation Tree Audit

Target: `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex`

## Executive Summary

- Selected source rows: `4`
- Semantic packets: `4`
- Proposition/context packets: `0`
- Context graphs: `4`
- Context graph statuses: `{'inferred_candidate': 20, 'missing': 6, 'unresolved': 4}`
- Typed repair obligations: `4`
- Typed repair obligation statuses: `{'blocked_on_missing_typed_assumptions': 4}`
- Ranked branches: `12`
- Promoted branches: `0`
- Blockers: `149`
- Missing focus labels: `[]`
- This report is generic and document-local; it is not tied to a card-NPV-specific plan.

## Tools Used

| Tool | Purpose | Status | Contract | Arguments |
| --- | --- | --- | --- | --- |
| `locate_equations_in_file` | Localize source rows in the exact target file. | `completed` | `equation_rows` | `{"root": "docs/credit-card-npv-component-proposal", "tex_path": "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex"}` |
| `build_proposition_context_packet` | Localize proposition labels that are not display-equation rows and attach equation targets/context. | `not_needed` | `proposition_context_packet_result` | `{"context_target_count": 0, "focus_labels": ["eq:panel-npv-functional", "eq:incremental-cash-flow", "eq:incremental-npv"]}` |
| `build_semantic_work_packet` | Classify each target and generate full-display semantic packets, missing obligations, assumption sets, and derivation routes. | `completed` | `semantic_work_packet` | `{"selected_rows": 4}` |
| `assumptions_required` | Detect route-required assumptions before backend proof attempts. | `completed` | `assumption_discovery_result` | `{"selected_rows": 4}` |
| `build_local_context_graph` | Classify local source evidence as stated, nearby stated, inferred, missing, or unresolved before proposing repairs. | `completed` | `local_context_graph` | `{"context_graph_count": 4, "status_counts": {"inferred_candidate": 20, "missing": 6, "unresolved": 4}}` |
| `typed_repair_obligation_from_packet` | Convert context graph and semantic packet evidence into typed repair obligations before branch/report generation. | `completed` | `typed_repair_obligation` | `{"status_counts": {"blocked_on_missing_typed_assumptions": 4}, "typed_repair_obligation_count": 4}` |
| `doctor_report` | Record external backend capability provenance. | `available` | `doctor_report` | `{"backend_env": "mathdevmcp-backends"}` |
| `can_derive_with_budget` | Run the external-tool-first branch controller on semantic packet targets. | `completed` | `derivation_search_tree_result` | `{"budget_profile": "standard", "max_attempts": 1, "selected_rows": 4}` |
| `rank_repair_branches` | Rank assumption branches by recorded backend evidence, blocker specificity, source support, closure strength, and non-minimality. | `completed` | `repair_branch_ranking_result` | `{"ranked_branch_count": 12}` |
| `render_derivation_tree_report` | Render each derivation tree into structured evidence sections. | `completed` | `derivation_tree_report_result` | `{"rendered_trees": 4}` |

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
- Context graph statuses: `{'inferred_candidate': 5, 'missing': 2, 'unresolved': 1}`
- Typed repair obligation: `typed_repair_obligation_semantic_packet_eq_panel_npv_functional_0`
- Typed obligation status: `blocked_on_missing_typed_assumptions`
- Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`

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

Local context graph:
- `requirement_conditional_law_defined` status `missing`
  Role: well-definedness condition for conditional expectation
  What: A conditional law for the expectation is defined.
  Why status: No matching local source evidence states the required condition.
  Required next evidence: Cite or add the transition kernel/probability law used by the conditional expectation.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:664-673']`
- `requirement_conditional_integrability` status `unresolved`
  Role: finite-scalar condition for expectation-valued equations
  What: Random terms inside the conditional expectation are measurable and integrable.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: Cite or add measurability and finite conditional first-moment/dominated-envelope conditions.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:664-673']`
- `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`
  Role: route-required assumption from assumption_discovery
  What: conditional expectation law is defined and the random payoff terms are integrable
  Why status: The low-level route detector marked this assumption as missing.
  Required next evidence: Resolve this assumption in typed IR before backend proof attempts.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:664-673']`

Typed repair obligation:
- ID: `typed_repair_obligation_semantic_packet_eq_panel_npv_functional_0`
  Diagnostic status: `blocked_on_missing_typed_assumptions`
  Encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  Unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  Route hints: `[{'backend': 'lean', 'suitability': 'formalization_candidate', 'reason': 'Typed notation may be formalized manually and checked by Lean.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing assumptions or unsupported notation prevent verified backend routing.'}, {'backend': 'manual_formalization', 'suitability': 'required_before_cas', 'reason': 'Conditional expectation requires a typed probability kernel and integrability assumptions before CAS or Lean encoding.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing or unresolved typed assumptions block certifying backend attempts.'}]`
  Assumption statuses:
  - `requirement_conditional_law_defined` status `missing`: A conditional law for the expectation is defined.
  - `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`: conditional expectation law is defined and the random payoff terms are integrable
  - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  Boundary: Typed repair obligations are diagnostic routing artifacts; they are not proof certificates or backend encodings.

Document-ready repair proposals:
- `document_ready_repair_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv`
  - Contract: `context_aware_executable_repair_proposal`
  - Location: `credit_card_npv_component_proposal_final_submission.tex > The Valuation Problem and Decision Semantics > Valuation Object, State Space, and Wallet Accounting > eq:panel-npv-functional > line 664`
  - Top ranked branch: `branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv`
  - Ranking outcome: `blocked_with_specific_next_evidence`, score `83`
  - Problem: The target is not yet a certifiable derivation because missing or unresolved assumptions ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'] block constructs ['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability'].
  - Why this is a derivation problem: Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing. This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification. A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target. The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument. Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  - Missing or unresolved assumptions:
    - `requirement_conditional_law_defined` status `missing`: A conditional law for the expectation is defined.
    - `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`: conditional expectation law is defined and the random payoff terms are integrable
    - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  - Proposed assumption set:
    - The baseline and action paths are defined on the same horizon and information set.
    - All cash-flow components use the same currency, time index, and sign convention.
    - Discount factors and terminal value are finite and defined for the horizon.
  - Derivation route after adding assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
    - Decompose cash flow: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - Discount and aggregate: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
  - Proposed edit placement: Insert near `eq:panel-npv-functional` before citing the display as justified.
  - Proposed LaTeX:

```tex
\paragraph{Repair assumptions for \texttt{eq:panel-npv-functional}.}
Use the following local assumptions for this displayed equality:
\begin{itemize}
  \item The baseline and action paths are defined on the same horizon and information set.
  \item All cash-flow components use the same currency, time index, and sign convention.
  \item Discount factors and terminal value are finite and defined for the horizon.
\end{itemize}

Under these assumptions, the derivation should be checked by the following route:
\begin{enumerate}
  \item \textbf{Define conditional law.} Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is \(X_{it}^{d}\).
  \item \textbf{Check integrability.} Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is \(X_{it}^{d}\). Candidate source-local random terms include \(\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)\).
  \item \textbf{Use expectation as scalar.} Only after those checks should the equality be treated as a scalar derivation step.
  \item \textbf{Define two paths.} Write the action path and baseline path under the same information set.
  \item \textbf{Decompose cash flow.} Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include \(\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)\).
  \item \textbf{Discount and aggregate.} Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include \(\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)\).
\end{enumerate}

This paragraph is a repair proposal only: rerun the listed backend or formalization checks before treating the displayed equality as certified.
```
  - Remaining blockers before certification:
    - `conditional_expectation_translation_required`: The expectation operator cannot be translated as a scalar algebraic expression yet. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `conditioning_scope_translation_required`: The conditional bar has no backend-level conditioning object yet. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `conditional_law_translation_required`: The conditional law required by the expectation is not stated as an encodable object. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `integrability_translation_required`: Integrability of the random payoff/value terms is not established. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `missing_domain_or_assumption_required`: The branch still has missing or unresolved typed assumptions. Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `macro_translation_required`: LaTeX macros must be translated into backend symbols before execution. Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Source refs for missing/unresolved evidence: `['credit_card_npv_component_proposal_final_submission.tex > eq:panel-npv-functional > line 664-673']`
  - Backend evidence status: `typed_translation_blocked`
  - Validation: `typed_translation_blocked` from `rank_repair_branches_top_branch`
  - Non-claims: `['This proposal is branch-derived diagnostic repair text, not an applied edit.', 'This proposal does not certify the document claim.', 'The selected branch is evidence-ranked, not globally optimal or minimal.']`

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

Branch ranking:
- Contract: `repair_branch_ranking_result`
- Top branch: `branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv`
- Rank `1`: `branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `2`: `branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `3`: `branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation` outcome `blocked_with_specific_next_evidence`, score `81`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 4, 'score': 81, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 4}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=4.

Candidate assumption branches:
- `branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_panel_npv_functional_0']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The conditioned shock or path has finite support.', 'Every payoff/value term inside the expectation is finite at each support point.', 'The conditioning state or information set is explicitly defined.', 'The conditioning object `X_{it}^{d}` is defined as a sigma-field, information set, state, or conditioning variable for this equality.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 4 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_panel_npv_functional_0']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['A conditional kernel or probability law is fixed for the random object.', 'All random terms inside the expectation are measurable under that law.', 'Those terms are dominated by an integrable envelope or have finite conditional first moments.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv` status `blocked_before_backend_certification`
  - Closes obligations: `['measurable_integrable_payoff_terms', 'baseline_and_action_paths_defined', 'cash_flow_components_exhaustive', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_panel_npv_functional_0']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The baseline and action paths are defined on the same horizon and information set.', 'All cash-flow components use the same currency, time index, and sign convention.', 'Discount factors and terminal value are finite and defined for the horizon.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_integrability_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_integrability_translation_required', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`

How the derivation can work:
- `Define conditional law`: Specify the kernel or conditional distribution used by the expectation.
- `Check integrability`: Verify each random payoff, value, or derivative term has a finite conditional expectation.
- `Use expectation as scalar`: Only after those checks should the equality be treated as a scalar derivation step.
- `Define two paths`: Write the action path and baseline path under the same information set.
- `Decompose cash flow`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
- `Discount and aggregate`: Apply the stated discount factors and terminal-value convention over the finite horizon.

Backend attempts:
- `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`

Proposed patch candidates:
- `patch_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation` status `typed_translation_blocked`
  Proposed fix: Near `eq:panel-npv-functional` at credit_card_npv_component_proposal_final_submission.tex > The Valuation Problem and Decision Semantics > Valuation Object, State Space, and Wallet Accounting > eq:panel-npv-functional > line 664, add an assumptions paragraph: "For this displayed equality, assume: The conditioned shock or path has finite support. Every payoff/value term inside the expectation is finite at each support point. The conditioning state or information set is explicitly defined. The conditioning object `X_{it}^{d}` is defined as a sigma-field, information set, state, or conditioning variable for this equality. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition` status `typed_translation_blocked`
  Proposed fix: Near `eq:panel-npv-functional` at credit_card_npv_component_proposal_final_submission.tex > The Valuation Problem and Decision Semantics > Valuation Object, State Space, and Wallet Accounting > eq:panel-npv-functional > line 664, add an assumptions paragraph: "For this displayed equality, assume: A conditional kernel or probability law is fixed for the random object. All random terms inside the expectation are measurable under that law. Those terms are dominated by an integrable envelope or have finite conditional first moments. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv` status `typed_translation_blocked`
  Proposed fix: Near `eq:panel-npv-functional` at credit_card_npv_component_proposal_final_submission.tex > The Valuation Problem and Decision Semantics > Valuation Object, State Space, and Wallet Accounting > eq:panel-npv-functional > line 664, add an assumptions paragraph: "For this displayed equality, assume: The baseline and action paths are defined on the same horizon and information set. All cash-flow components use the same currency, time index, and sign convention. Discount factors and terminal value are finite and defined for the horizon. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `X_{it}^{d}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `X_{it}^{d}`. Candidate source-local random terms include `\Delta CF_, \Delta TV_, \Delta CF_{i,t+h}(a,\pi;s), \Delta TV_{i,t+H}(a,\pi;s)`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification.

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
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_panel_npv_functional_0_finite_state_conditional_expectation_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_panel_npv_functional_0_kernel_integrability_condition_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_panel_npv_functional_0_finite_horizon_incremental_npv_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
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

### 2. `eq:incremental-cash-flow`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 841`
- Claim type: `valuation_identity_or_definition`
- Tree status: `budget_exhausted`
- Promotion guard: `can_promote=False`
- Semantic domains: `['conditional_expectation', 'npv_accounting_identity']`
- Extraction uncertainty: `['macros_not_expanded', 'alignment_markers_preserved']`
- Full display span: `{'file': 'credit_card_npv_component_proposal_final_submission.tex', 'line_start': 840, 'line_end': 862, 'labels': ['eq:incremental-cash-flow', 'eq:incremental-npv'], 'environment': 'align', 'section_path': ['Literature-Grounded Economic Mechanisms', 'Literature Review Introduction']}`
- Operators: `['equality', 'conditional_expectation', 'conditional_bar', 'summation']`
- Symbols: `{'macros': ['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi'], 'identifiers': ['CF_', 'C_i', 'EL_', 'H', 'I', 'Kchg_', 'PPNR_', 'RelValue_', 'TV_', 'Tax_', 'a', 'acq', 'd', 'h', 'i', 'id', 's', 't']}`
- Context graph statuses: `{'inferred_candidate': 5, 'missing': 1, 'unresolved': 1}`
- Typed repair obligation: `typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_0`
- Typed obligation status: `blocked_on_missing_typed_assumptions`
- Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`

Source row target:

```tex
\Delta CF_{i,t+h}(a,\pi;s)
  &=
  \Delta PPNR_{i,t+h}(a,\pi;s)
  - \Delta EL_{i,t+h}(a,\pi;s)
  - \Delta Kchg_{i,t+h}(a,\pi;s)
  \nonumber
```

Full display target:

```tex
\begin{align}
  \Delta CF_{i,t+h}(a,\pi;s)
  &=
  \Delta PPNR_{i,t+h}(a,\pi;s)
  - \Delta EL_{i,t+h}(a,\pi;s)
  - \Delta Kchg_{i,t+h}(a,\pi;s)
  \nonumber\\
  &\quad
  - \Delta Tax_{i,t+h}(a,\pi;s)
  + \Delta RelValue_{i,t+h}(a,\pi;s),
  \label{eq:incremental-cash-flow}\\
  \Delta \NPV_i(a;d,s,\pi)
  &=
  - C_i^{\mathrm{acq}}(a)
  +
  \E\left[
    \sum_{h=0}^{H}
      \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)
    + \delta_H\Delta TV_{i,t+H}(a,\pi;s)
    \,\middle|\, \mathcal{I}_{id}
  \right].
  \label{eq:incremental-npv}
\end{align}
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

Local context graph:
- `requirement_conditional_law_defined` status `missing`
  Role: well-definedness condition for conditional expectation
  What: A conditional law for the expectation is defined.
  Why status: No matching local source evidence states the required condition.
  Required next evidence: Cite or add the transition kernel/probability law used by the conditional expectation.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:841-846']`
- `requirement_conditional_integrability` status `unresolved`
  Role: finite-scalar condition for expectation-valued equations
  What: Random terms inside the conditional expectation are measurable and integrable.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: Cite or add measurability and finite conditional first-moment/dominated-envelope conditions.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:841-846']`

Typed repair obligation:
- ID: `typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_0`
  Diagnostic status: `blocked_on_missing_typed_assumptions`
  Encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  Unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  Route hints: `[{'backend': 'lean', 'suitability': 'formalization_candidate', 'reason': 'Typed notation may be formalized manually and checked by Lean.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing assumptions or unsupported notation prevent verified backend routing.'}, {'backend': 'manual_formalization', 'suitability': 'required_before_cas', 'reason': 'Conditional expectation requires a typed probability kernel and integrability assumptions before CAS or Lean encoding.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing or unresolved typed assumptions block certifying backend attempts.'}]`
  Assumption statuses:
  - `requirement_conditional_law_defined` status `missing`: A conditional law for the expectation is defined.
  - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  Boundary: Typed repair obligations are diagnostic routing artifacts; they are not proof certificates or backend encodings.

Document-ready repair proposals:
- `document_ready_repair_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv`
  - Contract: `context_aware_executable_repair_proposal`
  - Location: `credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 841`
  - Top ranked branch: `branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv`
  - Ranking outcome: `blocked_with_specific_next_evidence`, score `83`
  - Problem: The target is not yet a certifiable derivation because missing or unresolved assumptions ['requirement_conditional_law_defined', 'requirement_conditional_integrability'] block constructs ['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability'].
  - Why this is a derivation problem: Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing. This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification. A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target. The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument. Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  - Missing or unresolved assumptions:
    - `requirement_conditional_law_defined` status `missing`: A conditional law for the expectation is defined.
    - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  - Proposed assumption set:
    - The baseline and action paths are defined on the same horizon and information set.
    - All cash-flow components use the same currency, time index, and sign convention.
    - Discount factors and terminal value are finite and defined for the horizon.
  - Derivation route after adding assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
    - Decompose cash flow: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Discount and aggregate: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
  - Proposed edit placement: Insert near `eq:incremental-cash-flow` before citing the display as justified.
  - Proposed LaTeX:

```tex
\paragraph{Repair assumptions for \texttt{eq:incremental-cash-flow}.}
Use the following local assumptions for this displayed equality:
\begin{itemize}
  \item The baseline and action paths are defined on the same horizon and information set.
  \item All cash-flow components use the same currency, time index, and sign convention.
  \item Discount factors and terminal value are finite and defined for the horizon.
\end{itemize}

Under these assumptions, the derivation should be checked by the following route:
\begin{enumerate}
  \item \textbf{Define conditional law.} Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is \(\mathcal{I}_{id}\).
  \item \textbf{Check integrability.} Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is \(\mathcal{I}_{id}\). Candidate source-local random terms include \(\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_\).
  \item \textbf{Use expectation as scalar.} Only after those checks should the equality be treated as a scalar derivation step.
  \item \textbf{Define two paths.} Write the action path and baseline path under the same information set.
  \item \textbf{Decompose cash flow.} Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include \(\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_\).
  \item \textbf{Discount and aggregate.} Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include \(\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_\).
\end{enumerate}

This paragraph is a repair proposal only: rerun the listed backend or formalization checks before treating the displayed equality as certified.
```
  - Remaining blockers before certification:
    - `conditional_expectation_translation_required`: The expectation operator cannot be translated as a scalar algebraic expression yet. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `conditioning_scope_translation_required`: The conditional bar has no backend-level conditioning object yet. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `conditional_law_translation_required`: The conditional law required by the expectation is not stated as an encodable object. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `integrability_translation_required`: Integrability of the random payoff/value terms is not established. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `missing_domain_or_assumption_required`: The branch still has missing or unresolved typed assumptions. Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `macro_translation_required`: LaTeX macros must be translated into backend symbols before execution. Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Source refs for missing/unresolved evidence: `['credit_card_npv_component_proposal_final_submission.tex > eq:incremental-cash-flow > line 841-846']`
  - Backend evidence status: `typed_translation_blocked`
  - Validation: `typed_translation_blocked` from `rank_repair_branches_top_branch`
  - Non-claims: `['This proposal is branch-derived diagnostic repair text, not an applied edit.', 'This proposal does not certify the document claim.', 'The selected branch is evidence-ranked, not globally optimal or minimal.']`

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

Branch ranking:
- Contract: `repair_branch_ranking_result`
- Top branch: `branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv`
- Rank `1`: `branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `2`: `branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `3`: `branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation` outcome `blocked_with_specific_next_evidence`, score `81`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 4, 'score': 81, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 4}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=4.

Candidate assumption branches:
- `branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_0']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The conditioned shock or path has finite support.', 'Every payoff/value term inside the expectation is finite at each support point.', 'The conditioning state or information set is explicitly defined.', 'The conditioning object `\\mathcal{I}_{id}` is defined as a sigma-field, information set, state, or conditioning variable for this equality.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 4 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:available', 'sage:available', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `not_encodable`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_0']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['A conditional kernel or probability law is fixed for the random object.', 'All random terms inside the expectation are measurable under that law.', 'Those terms are dominated by an integrable envelope or have finite conditional first moments.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:available', 'sage:available', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `not_encodable`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv` status `blocked_before_backend_certification`
  - Closes obligations: `['measurable_integrable_payoff_terms', 'baseline_and_action_paths_defined', 'cash_flow_components_exhaustive', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_0']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The baseline and action paths are defined on the same horizon and information set.', 'All cash-flow components use the same currency, time index, and sign convention.', 'Discount factors and terminal value are finite and defined for the horizon.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:available', 'sage:available', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `not_encodable`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`

How the derivation can work:
- `Define conditional law`: Specify the kernel or conditional distribution used by the expectation.
- `Check integrability`: Verify each random payoff, value, or derivative term has a finite conditional expectation.
- `Use expectation as scalar`: Only after those checks should the equality be treated as a scalar derivation step.
- `Define two paths`: Write the action path and baseline path under the same information set.
- `Decompose cash flow`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
- `Discount and aggregate`: Apply the stated discount factors and terminal-value convention over the finite horizon.

Backend attempts:
- `sympy_algebra_attempt` with `sympy`: status `not_encodable`, evidence `diagnostic`, certification `diagnostic`

Proposed patch candidates:
- `patch_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation` status `typed_translation_blocked`
  Proposed fix: Near `eq:incremental-cash-flow` at credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 841, add an assumptions paragraph: "For this displayed equality, assume: The conditioned shock or path has finite support. Every payoff/value term inside the expectation is finite at each support point. The conditioning state or information set is explicitly defined. The conditioning object `\mathcal{I}_{id}` is defined as a sigma-field, information set, state, or conditioning variable for this equality. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition` status `typed_translation_blocked`
  Proposed fix: Near `eq:incremental-cash-flow` at credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 841, add an assumptions paragraph: "For this displayed equality, assume: A conditional kernel or probability law is fixed for the random object. All random terms inside the expectation are measurable under that law. Those terms are dominated by an integrable envelope or have finite conditional first moments. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv` status `typed_translation_blocked`
  Proposed fix: Near `eq:incremental-cash-flow` at credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 841, add an assumptions paragraph: "For this displayed equality, assume: The baseline and action paths are defined on the same horizon and information set. All cash-flow components use the same currency, time index, and sign convention. Discount factors and terminal value are finite and defined for the horizon. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification.

Remaining blockers:
- `blocker_lean_source_required` (formalization_required)
  Problem: Lean certification was selected but no Lean source was supplied.
  Why: Direct Lean checking requires an explicit Lean statement/proof artifact.
  Required next evidence: Supply Lean source or a formalization branch before Lean certification.
- `blocker_sympy_algebra_attempt` (adapter_diagnostic)
  Problem: sympy did not certify or refute the target.
  Why: Expression contains syntax outside the conservative router grammar.
  Required next evidence: Provide a certifying backend result, concrete counterexample, formalization, or stronger assumption set.
- `blocker_budget_exhausted` (budget_exhausted)
  Problem: The controller exhausted its attempt budget before proof or refutation.
  Why: Some scheduled evidence actions were not attempted within the selected budget profile.
  Required next evidence: Increase budget, provide a stronger formalization, or inspect exhausted actions.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_0_finite_state_conditional_expectation_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_0_kernel_integrability_condition_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_0_finite_horizon_incremental_npv_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_semantic_packet_eq_incremental_cash_flow_0_conditional_law_defined` (probability_condition)
  Problem: A conditional probability law for the random variables inside the expectation.
  Why: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
  Required next evidence: Makes the expectation operator well defined.
- `blocker_semantic_packet_eq_incremental_cash_flow_0_measurable_integrable_payoff_terms` (integrability_condition)
  Problem: Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
  Why: Without measurability and integrability, the expectation may be undefined or infinite.
  Required next evidence: Turns the displayed expression into a finite scalar equality.
- `blocker_semantic_packet_eq_incremental_cash_flow_0_conditioning_information_defined` (information_condition)
  Problem: A definition of the conditioning information set, state, or sigma-field.
  Why: The notation after the conditional bar determines what information the expectation conditions on.
  Required next evidence: Fixes the scope of the conditional expectation used in the derivation.
- `blocker_semantic_packet_eq_incremental_cash_flow_0_baseline_and_action_paths_defined` (counterfactual_condition)
  Problem: Definitions of the baseline path and the action path used in the incremental NPV.
  Why: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
  Required next evidence: Makes the counterfactual comparison well posed.
- `blocker_semantic_packet_eq_incremental_cash_flow_0_cash_flow_components_exhaustive` (accounting_identity_condition)
  Problem: A statement that the listed cash-flow components are exhaustive and share the same sign convention.
  Why: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
  Required next evidence: Justifies replacing total incremental cash flow by the listed component sum.
- `blocker_semantic_packet_eq_incremental_cash_flow_0_discount_horizon_terminal_value_defined` (valuation_condition)
  Problem: Definitions of the horizon, discount factors, and terminal-value term.
  Why: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
  Required next evidence: Makes the finite-horizon valuation expression well defined.
- `blocker_semantic_packet_eq_incremental_cash_flow_0_source_extraction_uncertainty` (source_extraction_uncertainty)
  Problem: The localized source row has extraction uncertainty.
  Why: Equation locator reported: macros_not_expanded, alignment_markers_preserved.
  Required next evidence: Recover a complete source-local obligation before promoting a derivation.
- `blocker_semantic_packet_eq_incremental_cash_flow_0_grouped_multiline_obligation_required` (grouped_multiline_obligation_required)
  Problem: The label spans multiple localized equation rows.
  Why: A single-row tree attempt cannot certify a full multiline align environment.
  Required next evidence: Group all rows for the label into one formal obligation or split them into separately labeled obligations.

Smallest next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.

### 3. `eq:incremental-cash-flow`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 847`
- Claim type: `valuation_identity_or_definition`
- Tree status: `partial`
- Promotion guard: `can_promote=False`
- Semantic domains: `['conditional_expectation', 'npv_accounting_identity']`
- Extraction uncertainty: `['alignment_markers_preserved']`
- Full display span: `{'file': 'credit_card_npv_component_proposal_final_submission.tex', 'line_start': 840, 'line_end': 862, 'labels': ['eq:incremental-cash-flow', 'eq:incremental-npv'], 'environment': 'align', 'section_path': ['Literature-Grounded Economic Mechanisms', 'Literature Review Introduction']}`
- Operators: `['equality', 'conditional_expectation', 'conditional_bar', 'summation']`
- Symbols: `{'macros': ['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi'], 'identifiers': ['CF_', 'C_i', 'EL_', 'H', 'I', 'Kchg_', 'PPNR_', 'RelValue_', 'TV_', 'Tax_', 'a', 'acq', 'd', 'h', 'i', 'id', 's', 't']}`
- Context graph statuses: `{'inferred_candidate': 5, 'missing': 1, 'unresolved': 1}`
- Typed repair obligation: `typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_1`
- Typed obligation status: `blocked_on_missing_typed_assumptions`
- Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`

Source row target:

```tex
&\quad
  - \Delta Tax_{i,t+h}(a,\pi;s)
  + \Delta RelValue_{i,t+h}(a,\pi;s),
```

Full display target:

```tex
\begin{align}
  \Delta CF_{i,t+h}(a,\pi;s)
  &=
  \Delta PPNR_{i,t+h}(a,\pi;s)
  - \Delta EL_{i,t+h}(a,\pi;s)
  - \Delta Kchg_{i,t+h}(a,\pi;s)
  \nonumber\\
  &\quad
  - \Delta Tax_{i,t+h}(a,\pi;s)
  + \Delta RelValue_{i,t+h}(a,\pi;s),
  \label{eq:incremental-cash-flow}\\
  \Delta \NPV_i(a;d,s,\pi)
  &=
  - C_i^{\mathrm{acq}}(a)
  +
  \E\left[
    \sum_{h=0}^{H}
      \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)
    + \delta_H\Delta TV_{i,t+H}(a,\pi;s)
    \,\middle|\, \mathcal{I}_{id}
  \right].
  \label{eq:incremental-npv}
\end{align}
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

Local context graph:
- `requirement_conditional_law_defined` status `missing`
  Role: well-definedness condition for conditional expectation
  What: A conditional law for the expectation is defined.
  Why status: No matching local source evidence states the required condition.
  Required next evidence: Cite or add the transition kernel/probability law used by the conditional expectation.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:847-850']`
- `requirement_conditional_integrability` status `unresolved`
  Role: finite-scalar condition for expectation-valued equations
  What: Random terms inside the conditional expectation are measurable and integrable.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: Cite or add measurability and finite conditional first-moment/dominated-envelope conditions.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:847-850']`

Typed repair obligation:
- ID: `typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_1`
  Diagnostic status: `blocked_on_missing_typed_assumptions`
  Encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  Unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  Route hints: `[{'backend': 'lean', 'suitability': 'formalization_candidate', 'reason': 'Typed notation may be formalized manually and checked by Lean.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing assumptions or unsupported notation prevent verified backend routing.'}, {'backend': 'manual_formalization', 'suitability': 'required_before_cas', 'reason': 'Conditional expectation requires a typed probability kernel and integrability assumptions before CAS or Lean encoding.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing or unresolved typed assumptions block certifying backend attempts.'}]`
  Assumption statuses:
  - `requirement_conditional_law_defined` status `missing`: A conditional law for the expectation is defined.
  - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  Boundary: Typed repair obligations are diagnostic routing artifacts; they are not proof certificates or backend encodings.

Document-ready repair proposals:
- `document_ready_repair_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv`
  - Contract: `context_aware_executable_repair_proposal`
  - Location: `credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 847`
  - Top ranked branch: `branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv`
  - Ranking outcome: `blocked_with_specific_next_evidence`, score `83`
  - Problem: The target is not yet a certifiable derivation because missing or unresolved assumptions ['requirement_conditional_law_defined', 'requirement_conditional_integrability'] block constructs ['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability'].
  - Why this is a derivation problem: Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing. This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification. A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target. The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument. Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  - Missing or unresolved assumptions:
    - `requirement_conditional_law_defined` status `missing`: A conditional law for the expectation is defined.
    - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  - Proposed assumption set:
    - The baseline and action paths are defined on the same horizon and information set.
    - All cash-flow components use the same currency, time index, and sign convention.
    - Discount factors and terminal value are finite and defined for the horizon.
  - Derivation route after adding assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
    - Decompose cash flow: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Discount and aggregate: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
  - Proposed edit placement: Insert near `eq:incremental-cash-flow` before citing the display as justified.
  - Proposed LaTeX:

```tex
\paragraph{Repair assumptions for \texttt{eq:incremental-cash-flow}.}
Use the following local assumptions for this displayed equality:
\begin{itemize}
  \item The baseline and action paths are defined on the same horizon and information set.
  \item All cash-flow components use the same currency, time index, and sign convention.
  \item Discount factors and terminal value are finite and defined for the horizon.
\end{itemize}

Under these assumptions, the derivation should be checked by the following route:
\begin{enumerate}
  \item \textbf{Define conditional law.} Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is \(\mathcal{I}_{id}\).
  \item \textbf{Check integrability.} Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is \(\mathcal{I}_{id}\). Candidate source-local random terms include \(\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_\).
  \item \textbf{Use expectation as scalar.} Only after those checks should the equality be treated as a scalar derivation step.
  \item \textbf{Define two paths.} Write the action path and baseline path under the same information set.
  \item \textbf{Decompose cash flow.} Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include \(\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_\).
  \item \textbf{Discount and aggregate.} Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include \(\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_\).
\end{enumerate}

This paragraph is a repair proposal only: rerun the listed backend or formalization checks before treating the displayed equality as certified.
```
  - Remaining blockers before certification:
    - `conditional_expectation_translation_required`: The expectation operator cannot be translated as a scalar algebraic expression yet. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `conditioning_scope_translation_required`: The conditional bar has no backend-level conditioning object yet. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `conditional_law_translation_required`: The conditional law required by the expectation is not stated as an encodable object. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `integrability_translation_required`: Integrability of the random payoff/value terms is not established. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `missing_domain_or_assumption_required`: The branch still has missing or unresolved typed assumptions. Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `macro_translation_required`: LaTeX macros must be translated into backend symbols before execution. Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Source refs for missing/unresolved evidence: `['credit_card_npv_component_proposal_final_submission.tex > eq:incremental-cash-flow > line 847-850']`
  - Backend evidence status: `typed_translation_blocked`
  - Validation: `typed_translation_blocked` from `rank_repair_branches_top_branch`
  - Non-claims: `['This proposal is branch-derived diagnostic repair text, not an applied edit.', 'This proposal does not certify the document claim.', 'The selected branch is evidence-ranked, not globally optimal or minimal.']`

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

Branch ranking:
- Contract: `repair_branch_ranking_result`
- Top branch: `branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv`
- Rank `1`: `branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `2`: `branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `3`: `branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation` outcome `blocked_with_specific_next_evidence`, score `81`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 4, 'score': 81, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 4}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=4.

Candidate assumption branches:
- `branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_1']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The conditioned shock or path has finite support.', 'Every payoff/value term inside the expectation is finite at each support point.', 'The conditioning state or information set is explicitly defined.', 'The conditioning object `\\mathcal{I}_{id}` is defined as a sigma-field, information set, state, or conditioning variable for this equality.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 4 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:available', 'sage:available', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `adapter_error`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_1']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['A conditional kernel or probability law is fixed for the random object.', 'All random terms inside the expectation are measurable under that law.', 'Those terms are dominated by an integrable envelope or have finite conditional first moments.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:available', 'sage:available', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `adapter_error`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv` status `blocked_before_backend_certification`
  - Closes obligations: `['measurable_integrable_payoff_terms', 'baseline_and_action_paths_defined', 'cash_flow_components_exhaustive', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_incremental_cash_flow_1']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The baseline and action paths are defined on the same horizon and information set.', 'All cash-flow components use the same currency, time index, and sign convention.', 'Discount factors and terminal value are finite and defined for the horizon.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:available', 'sage:available', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `adapter_error`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`

How the derivation can work:
- `Define conditional law`: Specify the kernel or conditional distribution used by the expectation.
- `Check integrability`: Verify each random payoff, value, or derivative term has a finite conditional expectation.
- `Use expectation as scalar`: Only after those checks should the equality be treated as a scalar derivation step.
- `Define two paths`: Write the action path and baseline path under the same information set.
- `Decompose cash flow`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
- `Discount and aggregate`: Apply the stated discount factors and terminal-value convention over the finite horizon.

Backend attempts:
- `sympy_algebra_attempt` with `sympy`: status `adapter_error`, evidence `diagnostic`, certification `diagnostic`

Proposed patch candidates:
- `patch_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation` status `typed_translation_blocked`
  Proposed fix: Near `eq:incremental-cash-flow` at credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 847, add an assumptions paragraph: "For this displayed equality, assume: The conditioned shock or path has finite support. Every payoff/value term inside the expectation is finite at each support point. The conditioning state or information set is explicitly defined. The conditioning object `\mathcal{I}_{id}` is defined as a sigma-field, information set, state, or conditioning variable for this equality. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition` status `typed_translation_blocked`
  Proposed fix: Near `eq:incremental-cash-flow` at credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 847, add an assumptions paragraph: "For this displayed equality, assume: A conditional kernel or probability law is fixed for the random object. All random terms inside the expectation are measurable under that law. Those terms are dominated by an integrable envelope or have finite conditional first moments. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv` status `typed_translation_blocked`
  Proposed fix: Near `eq:incremental-cash-flow` at credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-cash-flow > line 847, add an assumptions paragraph: "For this displayed equality, assume: The baseline and action paths are defined on the same horizon and information set. All cash-flow components use the same currency, time index, and sign convention. Discount factors and terminal value are finite and defined for the horizon. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification.

Remaining blockers:
- `blocker_lean_source_required` (formalization_required)
  Problem: Lean certification was selected but no Lean source was supplied.
  Why: Direct Lean checking requires an explicit Lean statement/proof artifact.
  Required next evidence: Supply Lean source or a formalization branch before Lean certification.
- `blocker_counterexample_requires_lhs_rhs` (formalization_required)
  Problem: Counterexample search requires a target equality with lhs and rhs.
  Why: The controller could not split the target into non-empty lhs/rhs expressions.
  Required next evidence: Provide lhs/rhs or formalize the target as an equality.
- `blocker_sympy_algebra_attempt` (adapter_diagnostic)
  Problem: sympy did not certify or refute the target.
  Why: sympy adapter call failed: ValueError: derive_or_refute requires lhs/rhs or a target containing '='
  Required next evidence: Provide a certifying backend result, concrete counterexample, formalization, or stronger assumption set.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_1_finite_state_conditional_expectation_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_1_kernel_integrability_condition_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_cash_flow_1_finite_horizon_incremental_npv_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_semantic_packet_eq_incremental_cash_flow_1_conditional_law_defined` (probability_condition)
  Problem: A conditional probability law for the random variables inside the expectation.
  Why: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
  Required next evidence: Makes the expectation operator well defined.
- `blocker_semantic_packet_eq_incremental_cash_flow_1_measurable_integrable_payoff_terms` (integrability_condition)
  Problem: Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
  Why: Without measurability and integrability, the expectation may be undefined or infinite.
  Required next evidence: Turns the displayed expression into a finite scalar equality.
- `blocker_semantic_packet_eq_incremental_cash_flow_1_conditioning_information_defined` (information_condition)
  Problem: A definition of the conditioning information set, state, or sigma-field.
  Why: The notation after the conditional bar determines what information the expectation conditions on.
  Required next evidence: Fixes the scope of the conditional expectation used in the derivation.
- `blocker_semantic_packet_eq_incremental_cash_flow_1_baseline_and_action_paths_defined` (counterfactual_condition)
  Problem: Definitions of the baseline path and the action path used in the incremental NPV.
  Why: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
  Required next evidence: Makes the counterfactual comparison well posed.
- `blocker_semantic_packet_eq_incremental_cash_flow_1_cash_flow_components_exhaustive` (accounting_identity_condition)
  Problem: A statement that the listed cash-flow components are exhaustive and share the same sign convention.
  Why: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
  Required next evidence: Justifies replacing total incremental cash flow by the listed component sum.
- `blocker_semantic_packet_eq_incremental_cash_flow_1_discount_horizon_terminal_value_defined` (valuation_condition)
  Problem: Definitions of the horizon, discount factors, and terminal-value term.
  Why: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
  Required next evidence: Makes the finite-horizon valuation expression well defined.
- `blocker_semantic_packet_eq_incremental_cash_flow_1_source_extraction_uncertainty` (source_extraction_uncertainty)
  Problem: The localized source row has extraction uncertainty.
  Why: Equation locator reported: alignment_markers_preserved.
  Required next evidence: Recover a complete source-local obligation before promoting a derivation.
- `blocker_semantic_packet_eq_incremental_cash_flow_1_grouped_multiline_obligation_required` (grouped_multiline_obligation_required)
  Problem: The label spans multiple localized equation rows.
  Why: A single-row tree attempt cannot certify a full multiline align environment.
  Required next evidence: Group all rows for the label into one formal obligation or split them into separately labeled obligations.

Smallest next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.

### 4. `eq:incremental-npv`

- Location: `credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-npv > line 851`
- Claim type: `valuation_identity_or_definition`
- Tree status: `budget_exhausted`
- Promotion guard: `can_promote=False`
- Semantic domains: `['conditional_expectation', 'npv_accounting_identity']`
- Extraction uncertainty: `['alignment_markers_preserved']`
- Full display span: `{'file': 'credit_card_npv_component_proposal_final_submission.tex', 'line_start': 840, 'line_end': 862, 'labels': ['eq:incremental-cash-flow', 'eq:incremental-npv'], 'environment': 'align', 'section_path': ['Literature-Grounded Economic Mechanisms', 'Literature Review Introduction']}`
- Operators: `['equality', 'conditional_expectation', 'conditional_bar', 'summation']`
- Symbols: `{'macros': ['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi'], 'identifiers': ['CF_', 'C_i', 'EL_', 'H', 'I', 'Kchg_', 'PPNR_', 'RelValue_', 'TV_', 'Tax_', 'a', 'acq', 'd', 'h', 'i', 'id', 's', 't']}`
- Context graph statuses: `{'inferred_candidate': 5, 'missing': 2, 'unresolved': 1}`
- Typed repair obligation: `typed_repair_obligation_semantic_packet_eq_incremental_npv_2`
- Typed obligation status: `blocked_on_missing_typed_assumptions`
- Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`

Source row target:

```tex
\Delta \NPV_i(a;d,s,\pi)
  &=
  - C_i^{\mathrm{acq}}(a)
  +
  \E\left[
    \sum_{h=0}^{H}
      \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)
    + \delta_H\Delta TV_{i,t+H}(a,\pi;s)
    \,\middle|\, \mathcal{I}_{id}
  \right].
```

Full display target:

```tex
\begin{align}
  \Delta CF_{i,t+h}(a,\pi;s)
  &=
  \Delta PPNR_{i,t+h}(a,\pi;s)
  - \Delta EL_{i,t+h}(a,\pi;s)
  - \Delta Kchg_{i,t+h}(a,\pi;s)
  \nonumber\\
  &\quad
  - \Delta Tax_{i,t+h}(a,\pi;s)
  + \Delta RelValue_{i,t+h}(a,\pi;s),
  \label{eq:incremental-cash-flow}\\
  \Delta \NPV_i(a;d,s,\pi)
  &=
  - C_i^{\mathrm{acq}}(a)
  +
  \E\left[
    \sum_{h=0}^{H}
      \delta_h\,\Delta CF_{i,t+h}(a,\pi;s)
    + \delta_H\Delta TV_{i,t+H}(a,\pi;s)
    \,\middle|\, \mathcal{I}_{id}
  \right].
  \label{eq:incremental-npv}
\end{align}
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

Local context graph:
- `requirement_conditional_law_defined` status `missing`
  Role: well-definedness condition for conditional expectation
  What: A conditional law for the expectation is defined.
  Why status: No matching local source evidence states the required condition.
  Required next evidence: Cite or add the transition kernel/probability law used by the conditional expectation.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:851-861']`
- `requirement_conditional_integrability` status `unresolved`
  Role: finite-scalar condition for expectation-valued equations
  What: Random terms inside the conditional expectation are measurable and integrable.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: Cite or add measurability and finite conditional first-moment/dominated-envelope conditions.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:851-861']`
- `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`
  Role: route-required assumption from assumption_discovery
  What: conditional expectation law is defined and the random payoff terms are integrable
  Why status: The low-level route detector marked this assumption as missing.
  Required next evidence: Resolve this assumption in typed IR before backend proof attempts.
  Source refs: `['credit_card_npv_component_proposal_final_submission.tex:851-861']`

Typed repair obligation:
- ID: `typed_repair_obligation_semantic_packet_eq_incremental_npv_2`
  Diagnostic status: `blocked_on_missing_typed_assumptions`
  Encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  Unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  Route hints: `[{'backend': 'lean', 'suitability': 'formalization_candidate', 'reason': 'Typed notation may be formalized manually and checked by Lean.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing assumptions or unsupported notation prevent verified backend routing.'}, {'backend': 'manual_formalization', 'suitability': 'required_before_cas', 'reason': 'Conditional expectation requires a typed probability kernel and integrability assumptions before CAS or Lean encoding.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing or unresolved typed assumptions block certifying backend attempts.'}]`
  Assumption statuses:
  - `requirement_conditional_law_defined` status `missing`: A conditional law for the expectation is defined.
  - `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`: conditional expectation law is defined and the random payoff terms are integrable
  - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  Boundary: Typed repair obligations are diagnostic routing artifacts; they are not proof certificates or backend encodings.

Document-ready repair proposals:
- `document_ready_repair_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv`
  - Contract: `context_aware_executable_repair_proposal`
  - Location: `credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-npv > line 851`
  - Top ranked branch: `branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv`
  - Ranking outcome: `blocked_with_specific_next_evidence`, score `83`
  - Problem: The target is not yet a certifiable derivation because missing or unresolved assumptions ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'] block constructs ['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability'].
  - Why this is a derivation problem: Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing. This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification. A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target. The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument. Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  - Missing or unresolved assumptions:
    - `requirement_conditional_law_defined` status `missing`: A conditional law for the expectation is defined.
    - `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`: conditional expectation law is defined and the random payoff terms are integrable
    - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  - Proposed assumption set:
    - The baseline and action paths are defined on the same horizon and information set.
    - All cash-flow components use the same currency, time index, and sign convention.
    - Discount factors and terminal value are finite and defined for the horizon.
  - Derivation route after adding assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
    - Decompose cash flow: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Discount and aggregate: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
  - Proposed edit placement: Insert near `eq:incremental-npv` before citing the display as justified.
  - Proposed LaTeX:

```tex
\paragraph{Repair assumptions for \texttt{eq:incremental-npv}.}
Use the following local assumptions for this displayed equality:
\begin{itemize}
  \item The baseline and action paths are defined on the same horizon and information set.
  \item All cash-flow components use the same currency, time index, and sign convention.
  \item Discount factors and terminal value are finite and defined for the horizon.
\end{itemize}

Under these assumptions, the derivation should be checked by the following route:
\begin{enumerate}
  \item \textbf{Define conditional law.} Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is \(\mathcal{I}_{id}\).
  \item \textbf{Check integrability.} Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is \(\mathcal{I}_{id}\). Candidate source-local random terms include \(\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_\).
  \item \textbf{Use expectation as scalar.} Only after those checks should the equality be treated as a scalar derivation step.
  \item \textbf{Define two paths.} Write the action path and baseline path under the same information set.
  \item \textbf{Decompose cash flow.} Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include \(\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_\).
  \item \textbf{Discount and aggregate.} Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include \(\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_\).
\end{enumerate}

This paragraph is a repair proposal only: rerun the listed backend or formalization checks before treating the displayed equality as certified.
```
  - Remaining blockers before certification:
    - `conditional_expectation_translation_required`: The expectation operator cannot be translated as a scalar algebraic expression yet. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `conditioning_scope_translation_required`: The conditional bar has no backend-level conditioning object yet. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `conditional_law_translation_required`: The conditional law required by the expectation is not stated as an encodable object. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `integrability_translation_required`: Integrability of the random payoff/value terms is not established. Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `missing_domain_or_assumption_required`: The branch still has missing or unresolved typed assumptions. Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `macro_translation_required`: LaTeX macros must be translated into backend symbols before execution. Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Source refs for missing/unresolved evidence: `['credit_card_npv_component_proposal_final_submission.tex > eq:incremental-npv > line 851-861']`
  - Backend evidence status: `typed_translation_blocked`
  - Validation: `typed_translation_blocked` from `rank_repair_branches_top_branch`
  - Non-claims: `['This proposal is branch-derived diagnostic repair text, not an applied edit.', 'This proposal does not certify the document claim.', 'The selected branch is evidence-ranked, not globally optimal or minimal.']`

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

Branch ranking:
- Contract: `repair_branch_ranking_result`
- Top branch: `branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv`
- Rank `1`: `branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `2`: `branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `3`: `branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation` outcome `blocked_with_specific_next_evidence`, score `81`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 4, 'score': 81, 'specific_blocker_count': 6, 'backend_attempt_count': 1, 'assumption_count': 4}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=4.

Candidate assumption branches:
- `branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_incremental_npv_2']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The conditioned shock or path has finite support.', 'Every payoff/value term inside the expectation is finite at each support point.', 'The conditioning state or information set is explicitly defined.', 'The conditioning object `\\mathcal{I}_{id}` is defined as a sigma-field, information set, state, or conditioning variable for this equality.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 4 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_incremental_npv_2']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['A conditional kernel or probability law is fixed for the random object.', 'All random terms inside the expectation are measurable under that law.', 'Those terms are dominated by an integrable envelope or have finite conditional first moments.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv` status `blocked_before_backend_certification`
  - Closes obligations: `['measurable_integrable_payoff_terms', 'baseline_and_action_paths_defined', 'cash_flow_components_exhaustive', 'discount_horizon_terminal_value_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_incremental_npv_2']`
  - Typed unresolved constructs: `['expectation', 'posterior', 'conditional', 'conditional_law', 'integrability']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The baseline and action paths are defined on the same horizon and information set.', 'All cash-flow components use the same currency, time index, and sign convention.', 'Discount factors and terminal value are finite and defined for the horizon.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Define two paths: Write the action path and baseline path under the same information set.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Write the action path and baseline path under the same information set.
    - `derivation_split` status `diagnostic_route`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `derivation_split` status `diagnostic_route`: Apply the stated discount factors and terminal-value convention over the finite horizon. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_integrability_translation_required', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`

How the derivation can work:
- `Define conditional law`: Specify the kernel or conditional distribution used by the expectation.
- `Check integrability`: Verify each random payoff, value, or derivative term has a finite conditional expectation.
- `Use expectation as scalar`: Only after those checks should the equality be treated as a scalar derivation step.
- `Define two paths`: Write the action path and baseline path under the same information set.
- `Decompose cash flow`: Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.
- `Discount and aggregate`: Apply the stated discount factors and terminal-value convention over the finite horizon.

Backend attempts:
- `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`

Proposed patch candidates:
- `patch_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation` status `typed_translation_blocked`
  Proposed fix: Near `eq:incremental-npv` at credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-npv > line 851, add an assumptions paragraph: "For this displayed equality, assume: The conditioned shock or path has finite support. Every payoff/value term inside the expectation is finite at each support point. The conditioning state or information set is explicitly defined. The conditioning object `\mathcal{I}_{id}` is defined as a sigma-field, information set, state, or conditioning variable for this equality. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition` status `typed_translation_blocked`
  Proposed fix: Near `eq:incremental-npv` at credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-npv > line 851, add an assumptions paragraph: "For this displayed equality, assume: A conditional kernel or probability law is fixed for the random object. All random terms inside the expectation are measurable under that law. Those terms are dominated by an integrable envelope or have finite conditional first moments. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv` status `typed_translation_blocked`
  Proposed fix: Near `eq:incremental-npv` at credit_card_npv_component_proposal_final_submission.tex > Literature-Grounded Economic Mechanisms > Literature Review Introduction > eq:incremental-npv > line 851, add an assumptions paragraph: "For this displayed equality, assume: The baseline and action paths are defined on the same horizon and information set. All cash-flow components use the same currency, time index, and sign convention. Discount factors and terminal value are finite and defined for the horizon. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `\mathcal{I}_{id}`. Candidate source-local random terms include `\Delta CF_, \Delta PPNR_, \Delta EL_, \Delta Kchg_`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The incremental NPV expression is a finite, aligned accounting/valuation identity.` by making the operators and objects in the displayed equality well-defined before backend certification.

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
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_npv_2_finite_state_conditional_expectation_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_npv_2_kernel_integrability_condition_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['requirement_conditional_law_defined', 'route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'requirement_conditional_integrability']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\Delta', '\\E', '\\NPV', '\\delta', '\\mathcal', '\\pi']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_incremental_npv_2_finite_horizon_incremental_npv_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_semantic_packet_eq_incremental_npv_2_conditional_law_defined` (probability_condition)
  Problem: A conditional probability law for the random variables inside the expectation.
  Why: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
  Required next evidence: Makes the expectation operator well defined.
- `blocker_semantic_packet_eq_incremental_npv_2_measurable_integrable_payoff_terms` (integrability_condition)
  Problem: Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
  Why: Without measurability and integrability, the expectation may be undefined or infinite.
  Required next evidence: Turns the displayed expression into a finite scalar equality.
- `blocker_semantic_packet_eq_incremental_npv_2_conditioning_information_defined` (information_condition)
  Problem: A definition of the conditioning information set, state, or sigma-field.
  Why: The notation after the conditional bar determines what information the expectation conditions on.
  Required next evidence: Fixes the scope of the conditional expectation used in the derivation.
- `blocker_semantic_packet_eq_incremental_npv_2_baseline_and_action_paths_defined` (counterfactual_condition)
  Problem: Definitions of the baseline path and the action path used in the incremental NPV.
  Why: An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.
  Required next evidence: Makes the counterfactual comparison well posed.
- `blocker_semantic_packet_eq_incremental_npv_2_cash_flow_components_exhaustive` (accounting_identity_condition)
  Problem: A statement that the listed cash-flow components are exhaustive and share the same sign convention.
  Why: A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.
  Required next evidence: Justifies replacing total incremental cash flow by the listed component sum.
- `blocker_semantic_packet_eq_incremental_npv_2_discount_horizon_terminal_value_defined` (valuation_condition)
  Problem: Definitions of the horizon, discount factors, and terminal-value term.
  Why: The NPV sum depends on time indexing, discounting, and the terminal payoff convention.
  Required next evidence: Makes the finite-horizon valuation expression well defined.
- `blocker_semantic_packet_eq_incremental_npv_2_source_extraction_uncertainty` (source_extraction_uncertainty)
  Problem: The localized source row has extraction uncertainty.
  Why: Equation locator reported: alignment_markers_preserved.
  Required next evidence: Recover a complete source-local obligation before promoting a derivation.

Smallest next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.

## Non-Claims

- `document_tree_audit_not_document_proof`: This workflow is a semantic gap and tree-evidence report; it does not prove the whole document.
- `semantic_packets_not_certificates`: Missing obligations, assumption sets, and derivation routes are deterministic guidance, not proof certificates.
- `proof_search_not_final_certificate`: LeanDojo, Pantograph, retrieval, route plans, and static extraction are diagnostic until direct Lean or another certifying backend checks the scoped target.
