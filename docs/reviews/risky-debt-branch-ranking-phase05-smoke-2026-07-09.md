# Document Derivation Tree Audit

Target: `docs/risky-debt-maliar-deep-learning-lecture-note.tex`

## Executive Summary

- Selected source rows: `2`
- Semantic packets: `2`
- Proposition/context packets: `1`
- Context graphs: `3`
- Context graph statuses: `{'stated': 6, 'nearby_stated': 17, 'inferred_candidate': 15, 'unresolved': 12, 'missing': 4}`
- Typed repair obligations: `3`
- Typed repair obligation statuses: `{'blocked_on_missing_typed_assumptions': 3}`
- Ranked branches: `6`
- Promoted branches: `0`
- Blockers: `82`
- Missing focus labels: `[]`
- This report is generic and document-local; it is not tied to a card-NPV-specific plan.

## Tools Used

| Tool | Purpose | Status | Contract | Arguments |
| --- | --- | --- | --- | --- |
| `locate_equations_in_file` | Localize source rows in the exact target file. | `completed` | `equation_rows` | `{"root": "docs", "tex_path": "docs/risky-debt-maliar-deep-learning-lecture-note.tex"}` |
| `build_proposition_context_packet` | Localize proposition labels that are not display-equation rows and attach equation targets/context. | `completed` | `proposition_context_packet_result` | `{"context_target_count": 1, "focus_labels": ["prop:interior-foc", "eq:foc-k", "eq:foc-b"]}` |
| `build_semantic_work_packet` | Classify each target and generate full-display semantic packets, missing obligations, assumption sets, and derivation routes. | `completed` | `semantic_work_packet` | `{"selected_rows": 2}` |
| `assumptions_required` | Detect route-required assumptions before backend proof attempts. | `completed` | `assumption_discovery_result` | `{"selected_rows": 2}` |
| `build_local_context_graph` | Classify local source evidence as stated, nearby stated, inferred, missing, or unresolved before proposing repairs. | `completed` | `local_context_graph` | `{"context_graph_count": 3, "status_counts": {"inferred_candidate": 15, "missing": 4, "nearby_stated": 17, "stated": 6, "unresolved": 12}}` |
| `typed_repair_obligation_from_packet` | Convert context graph and semantic packet evidence into typed repair obligations before branch/report generation. | `completed` | `typed_repair_obligation` | `{"status_counts": {"blocked_on_missing_typed_assumptions": 3}, "typed_repair_obligation_count": 3}` |
| `doctor_report` | Record external backend capability provenance. | `available` | `doctor_report` | `{"backend_env": "mathdevmcp-backends"}` |
| `can_derive_with_budget` | Run the external-tool-first branch controller on semantic packet targets. | `completed` | `derivation_search_tree_result` | `{"budget_profile": "standard", "max_attempts": 1, "selected_rows": 2}` |
| `rank_repair_branches` | Rank assumption branches by recorded backend evidence, blocker specificity, source support, closure strength, and non-minimality. | `completed` | `repair_branch_ranking_result` | `{"ranked_branch_count": 6}` |
| `render_derivation_tree_report` | Render each derivation tree into structured evidence sections. | `completed` | `derivation_tree_report_result` | `{"rendered_trees": 2}` |

## Proposition/Context Packets

### `prop:interior-foc`

- Kind: `proposition`
- Location: `risky-debt-maliar-deep-learning-lecture-note.tex:770-787`
- Section path: `['Residuals for the risky-debt model', 'Euler residuals from first-order conditions']`
- Equation targets: `['eq:foc-k', 'eq:foc-b']`
- Hypotheses: `["Suppose the current state is a continuation state, the optimal action \\((k',b')\\) is interior, and the relevant functions are differentiable."]`
- Non-claim: This proposition context packet localizes source evidence; it is not a proof certificate or repair.

Source proposition:

```tex
\begin{proposition}[Interior first-order conditions]
\label{prop:interior-foc}
Suppose the current state is a continuation state, the optimal action
\((k',b')\) is interior, and the relevant functions are differentiable. Then the
optimal policy satisfies
\begin{align}
  0
  &=
  m(\bar e)\frac{d\bar e}{dk'}
  +\beta \E[V^\star_k(k',b',z')\mid z],
  \label{eq:foc-k}\\
  0
  &=
  m(\bar e)\frac{d\bar e}{db'}
  +\beta \E[V^\star_b(k',b',z')\mid z].
  \label{eq:foc-b}
\end{align}
\end{proposition}
```

Local context graph:

- Status counts: `{'stated': 6, 'nearby_stated': 3, 'inferred_candidate': 5, 'unresolved': 4}`
- `assumption_continuation_state` status `stated`
  - Role: rules out default/terminal regimes for the local FOC route
  - What: The current state is a continuation state.
  - Why status: The condition is stated in the target source span.
  - Required next evidence: Carry this stated condition into the typed FOC obligation.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:770-787']`
- `assumption_interior_action` status `stated`
  - Role: permits first-order conditions instead of inequality/KKT boundary conditions
  - What: The optimal action is interior.
  - Why status: The condition is stated in the target source span.
  - Required next evidence: Carry this stated condition into the typed FOC obligation.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:770-787']`
- `assumption_relevant_functions_differentiable` status `stated`
  - Role: supports local derivative notation in the FOC route
  - What: The relevant functions are differentiable.
  - Why status: The condition is stated in the target source span.
  - Required next evidence: Use this as differentiability evidence, but do not treat it as integrability or derivative-expectation interchange evidence.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:770-787']`
- `definition_bar_e_current_cash_flow` status `nearby_stated`
  - Role: definition of the cash-flow term used in the FOC rows
  - What: The nearby text defines the interior current-cash-flow object `\bar e`.
  - Why status: The definition appears in the local paragraph preceding the proposition.
  - Required next evidence: Carry this definition into typed FOC obligations.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:731-768']`
- `definition_marginal_cash_value_m` status `nearby_stated`
  - Role: definition of the multiplier in the FOC rows
  - What: The nearby text defines `m(e)` as the marginal value of current cash flow.
  - Why status: The definition appears in the local paragraph preceding the proposition.
  - Required next evidence: Carry this definition into typed FOC obligations.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:731-768']`
- `notation_evaluation_point` status `nearby_stated`
  - Role: notation declaration for derivative terms appearing in FOC rows
  - What: The nearby text states the evaluation point for the cash-flow derivative terms.
  - Why status: The declaration appears immediately before the proposition.
  - Required next evidence: Carry the evaluation point into typed obligations to avoid free-symbol drift.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:731-768']`
- `requirement_conditional_law_defined` status `unresolved`
  - Role: well-definedness condition for conditional expectation
  - What: A conditional law for the expectation is defined.
  - Why status: The local source contains related notation or a proof step, but not the required condition itself.
  - Required next evidence: Cite or add the transition kernel/probability law used by the conditional expectation.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780', 'risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`
- `requirement_conditional_integrability` status `unresolved`
  - Role: finite-scalar condition for expectation-valued equations
  - What: Random terms inside the conditional expectation are measurable and integrable.
  - Why status: The local source contains related notation or a proof step, but not the required condition itself.
  - Required next evidence: Cite or add measurability and finite conditional first-moment/dominated-envelope conditions.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780', 'risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`
- `requirement_expectation_derivative_interchange` status `unresolved`
  - Role: justifies replacing the derivative of expected continuation value with expected value derivatives
  - What: Differentiation may pass through the conditional expectation.
  - Why status: The local source contains related notation or a proof step, but not the required condition itself.
  - Required next evidence: State a finite-state sum route or a dominated/Leibniz interchange condition for the continuation-value derivatives.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780', 'risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`
- `requirement_choice_independent_transition_law` status `unresolved`
  - Role: rules out omitted transition-kernel derivative terms in the FOC
  - What: The conditional law does not add choice-derivative terms.
  - Why status: The local source contains related notation or a proof step, but not the required condition itself.
  - Required next evidence: State that the conditional law of `z'` given `z` is independent of `k'` and `b'`, or include the missing kernel derivative terms.
  - Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780', 'risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`

Typed repair obligation:

- ID: `typed_repair_obligation_proposition_context_packet:prop:interior-foc`
- Diagnostic status: `blocked_on_missing_typed_assumptions`
- Unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange']`
- Encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
- Route hints: `[{'backend': 'lean', 'suitability': 'formalization_candidate', 'reason': 'Typed notation may be formalized manually and checked by Lean.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing assumptions or unsupported notation prevent verified backend routing.'}, {'backend': 'manual_formalization', 'suitability': 'required_before_cas', 'reason': 'Conditional expectation requires a typed probability kernel and integrability assumptions before CAS or Lean encoding.'}, {'backend': 'lean', 'suitability': 'formalization_candidate_after_assumptions', 'reason': 'Derivative-under-expectation can only be checked after the interchange theorem assumptions are stated.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing or unresolved typed assumptions block certifying backend attempts.'}]`
- Boundary: Typed repair obligations are diagnostic routing artifacts; they are not proof certificates or backend encodings.


## Target Packets And Trees

### 1. `eq:foc-k`

- Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-k > line 776`
- Claim type: `stochastic_expectation`
- Tree status: `budget_exhausted`
- Promotion guard: `can_promote=False`
- Semantic domains: `['conditional_expectation', 'bellman_value_recursion']`
- Extraction uncertainty: `['alignment_markers_preserved']`
- Full display span: `{'file': 'risky-debt-maliar-deep-learning-lecture-note.tex', 'line_start': 775, 'line_end': 786, 'labels': ['eq:foc-k', 'eq:foc-b'], 'environment': 'align', 'section_path': ['Residuals for the risky-debt model', 'Euler residuals from first-order conditions']}`
- Operators: `['equality', 'conditional_expectation', 'conditional_bar', 'derivative']`
- Symbols: `{'macros': ['\\E', '\\bar', '\\beta', '\\star'], 'identifiers': ['V', 'b', 'd', 'db', 'dk', 'e', 'k', 'm', 'z']}`
- Context graph statuses: `{'nearby_stated': 7, 'inferred_candidate': 5, 'unresolved': 4, 'missing': 2}`
- Typed repair obligation: `typed_repair_obligation_semantic_packet_eq_foc_k_0`
- Typed obligation status: `blocked_on_missing_typed_assumptions`
- Typed unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`

Source row target:

```tex
0
  &=
  m(\bar e)\frac{d\bar e}{dk'}
  +\beta \E[V^\star_k(k',b',z')\mid z],
```

Full display target:

```tex
\begin{align}
  0
  &=
  m(\bar e)\frac{d\bar e}{dk'}
  +\beta \E[V^\star_k(k',b',z')\mid z],
  \label{eq:foc-k}\\
  0
  &=
  m(\bar e)\frac{d\bar e}{db'}
  +\beta \E[V^\star_b(k',b',z')\mid z].
  \label{eq:foc-b}
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
- `state_action_spaces_defined` (dynamic_programming_condition): Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
  Why: A Bellman maximization is not well posed until its domain and feasible controls are defined.
  Closes: Makes the optimization domain explicit.
- `transition_kernel_defined` (probability_condition): A transition law for next-period states conditional on current state and action.
  Why: The continuation value is an expectation over next states; that expectation needs a transition kernel.
  Closes: Defines the stochastic continuation operator.
- `reward_and_value_integrable` (integrability_condition): Finite reward and integrable continuation value under each admissible action.
  Why: The objective may be undefined or infinite without boundedness or integrability conditions.
  Closes: Makes the Bellman objective finite for comparison across actions.
- `terminal_boundary_condition_defined` (recursion_boundary_condition): A terminal, transversality, or boundary condition for the recursive value.
  Why: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
  Closes: Closes the recursive definition.

Local context graph:
- `assumption_continuation_state` status `nearby_stated`
  Role: rules out default/terminal regimes for the local FOC route
  What: The current state is a continuation state.
  Why status: The condition is stated in the local paragraph/proposition context.
  Required next evidence: Carry this stated condition into the typed FOC obligation.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:731-768', 'risky-debt-maliar-deep-learning-lecture-note.tex:770-787', 'risky-debt-maliar-deep-learning-lecture-note.tex:789-799']`
- `assumption_interior_action` status `nearby_stated`
  Role: permits first-order conditions instead of inequality/KKT boundary conditions
  What: The optimal action is interior.
  Why status: The condition is stated in the local paragraph/proposition context.
  Required next evidence: Carry this stated condition into the typed FOC obligation.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:731-768', 'risky-debt-maliar-deep-learning-lecture-note.tex:770-787', 'risky-debt-maliar-deep-learning-lecture-note.tex:789-799']`
- `assumption_relevant_functions_differentiable` status `nearby_stated`
  Role: supports local derivative notation in the FOC route
  What: The relevant functions are differentiable.
  Why status: The condition is stated in the local paragraph/proposition context.
  Required next evidence: Use this as differentiability evidence, but do not treat it as integrability or derivative-expectation interchange evidence.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:770-787', 'risky-debt-maliar-deep-learning-lecture-note.tex:789-799']`
- `definition_bar_e_current_cash_flow` status `nearby_stated`
  Role: definition of the cash-flow term used in the FOC rows
  What: The nearby text defines the interior current-cash-flow object `\bar e`.
  Why status: The definition appears in the local paragraph preceding the proposition.
  Required next evidence: Carry this definition into typed FOC obligations.
  Source refs: `['None:731-768']`
- `definition_marginal_cash_value_m` status `nearby_stated`
  Role: definition of the multiplier in the FOC rows
  What: The nearby text defines `m(e)` as the marginal value of current cash flow.
  Why status: The definition appears in the local paragraph preceding the proposition.
  Required next evidence: Carry this definition into typed FOC obligations.
  Source refs: `['None:731-768']`
- `notation_evaluation_point` status `nearby_stated`
  Role: notation declaration for derivative terms appearing in FOC rows
  What: The nearby text states the evaluation point for the cash-flow derivative terms.
  Why status: The declaration appears immediately before the proposition.
  Required next evidence: Carry the evaluation point into typed obligations to avoid free-symbol drift.
  Source refs: `['None:731-768']`
- `requirement_conditional_law_defined` status `unresolved`
  Role: well-definedness condition for conditional expectation
  What: A conditional law for the expectation is defined.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: Cite or add the transition kernel/probability law used by the conditional expectation.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780']`
- `requirement_conditional_integrability` status `unresolved`
  Role: finite-scalar condition for expectation-valued equations
  What: Random terms inside the conditional expectation are measurable and integrable.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: Cite or add measurability and finite conditional first-moment/dominated-envelope conditions.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780']`
- `requirement_expectation_derivative_interchange` status `unresolved`
  Role: justifies replacing the derivative of expected continuation value with expected value derivatives
  What: Differentiation may pass through the conditional expectation.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: State a finite-state sum route or a dominated/Leibniz interchange condition for the continuation-value derivatives.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780']`
- `requirement_choice_independent_transition_law` status `unresolved`
  Role: rules out omitted transition-kernel derivative terms in the FOC
  What: The conditional law does not add choice-derivative terms.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: State that the conditional law of `z'` given `z` is independent of `k'` and `b'`, or include the missing kernel derivative terms.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780']`
- `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`
  Role: route-required assumption from assumption_discovery
  What: conditional expectation law is defined and the random payoff terms are integrable
  Why status: The low-level route detector marked this assumption as missing.
  Required next evidence: Resolve this assumption in typed IR before backend proof attempts.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780']`
- `route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present` status `missing`
  Role: route-required assumption from assumption_discovery
  What: differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present
  Why status: The low-level route detector marked this assumption as missing.
  Required next evidence: Resolve this assumption in typed IR before backend proof attempts.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:776-780']`
- `route_assumption_target_function_is_differentiable_on_the_stated_domain` status `nearby_stated`
  Role: route-required assumption from assumption_discovery
  What: target function is differentiable on the stated domain
  Why status: The condition is stated in the local paragraph/proposition context. This reconciles the low-level route requirement with local source evidence.
  Required next evidence: Resolve this assumption in typed IR before backend proof attempts.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:770-787', 'risky-debt-maliar-deep-learning-lecture-note.tex:789-799']`

Typed repair obligation:
- ID: `typed_repair_obligation_semantic_packet_eq_foc_k_0`
  Diagnostic status: `blocked_on_missing_typed_assumptions`
  Encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  Unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`
  Route hints: `[{'backend': 'lean', 'suitability': 'formalization_candidate', 'reason': 'Typed notation may be formalized manually and checked by Lean.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing assumptions or unsupported notation prevent verified backend routing.'}, {'backend': 'manual_formalization', 'suitability': 'required_before_cas', 'reason': 'Conditional expectation requires a typed probability kernel and integrability assumptions before CAS or Lean encoding.'}, {'backend': 'lean', 'suitability': 'formalization_candidate_after_assumptions', 'reason': 'Derivative-under-expectation can only be checked after the interchange theorem assumptions are stated.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing or unresolved typed assumptions block certifying backend attempts.'}]`
  Assumption statuses:
  - `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`: conditional expectation law is defined and the random payoff terms are integrable
  - `route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present` status `missing`: differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present
  - `requirement_choice_independent_transition_law` status `unresolved`: The conditional law does not add choice-derivative terms.
  - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  - `requirement_conditional_law_defined` status `unresolved`: A conditional law for the expectation is defined.
  - `requirement_expectation_derivative_interchange` status `unresolved`: Differentiation may pass through the conditional expectation.
  - `assumption_continuation_state` status `nearby_stated`: The current state is a continuation state.
  - `assumption_interior_action` status `nearby_stated`: The optimal action is interior.
  - `assumption_relevant_functions_differentiable` status `nearby_stated`: The relevant functions are differentiable.
  - `route_assumption_target_function_is_differentiable_on_the_stated_domain` status `nearby_stated`: target function is differentiable on the stated domain
  Boundary: Typed repair obligations are diagnostic routing artifacts; they are not proof certificates or backend encodings.

Possible sufficient assumption sets:
- `finite_state_conditional_expectation`: The expectation becomes a finite weighted sum.
  - The conditioned shock or path has finite support.
  - Every payoff/value term inside the expectation is finite at each support point.
  - The conditioning state or information set is explicitly defined.
- `kernel_integrability_condition`: The expectation is a well-defined finite conditional integral.
  - A conditional kernel or probability law is fixed for the random object.
  - All random terms inside the expectation are measurable under that law.
  - Those terms are dominated by an integrable envelope or have finite conditional first moments.
- `finite_state_finite_action_bellman`: The Bellman operator is well defined and can be audited as a dynamic-programming recursion.
  - The state and action sets are finite or compact with a nonempty feasible set.
  - Rewards are finite and measurable.
  - A transition matrix or kernel is specified for each admissible action.
  - A terminal value or contraction condition is stated.

Branch ranking:
- Contract: `repair_branch_ranking_result`
- Top branch: `branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition`
- Rank `1`: `branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 7, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `2`: `branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation` outcome `blocked_with_specific_next_evidence`, score `81`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 4, 'score': 81, 'specific_blocker_count': 7, 'backend_attempt_count': 1, 'assumption_count': 4}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=4.
- Rank `3`: `branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman` outcome `blocked_with_specific_next_evidence`, score `81`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 4, 'score': 81, 'specific_blocker_count': 7, 'backend_attempt_count': 1, 'assumption_count': 4}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=4.

Candidate assumption branches:
- `branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'transition_kernel_defined', 'reward_and_value_integrable']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_foc_k_0']`
  - Typed unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The conditioned shock or path has finite support.', 'Every payoff/value term inside the expectation is finite at each support point.', 'The conditioning state or information set is explicitly defined.', 'The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 4 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Specify the domain over which the maximum is taken.
    - `derivation_split` status `diagnostic_route`: State the reward map and transition law used to form expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_derivative_expectation_interchange_required` (derivative_expectation_interchange_required): The derivative-under-expectation step is not justified as an encodable theorem instance.
      Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'transition_kernel_defined', 'reward_and_value_integrable']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_foc_k_0']`
  - Typed unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['A conditional kernel or probability law is fixed for the random object.', 'All random terms inside the expectation are measurable under that law.', 'Those terms are dominated by an integrable envelope or have finite conditional first moments.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Specify the domain over which the maximum is taken.
    - `derivation_split` status `diagnostic_route`: State the reward map and transition law used to form expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_derivative_expectation_interchange_required` (derivative_expectation_interchange_required): The derivative-under-expectation step is not justified as an encodable theorem instance.
      Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'state_action_spaces_defined', 'transition_kernel_defined', 'reward_and_value_integrable', 'terminal_boundary_condition_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_foc_k_0']`
  - Typed unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The Bellman operator is well defined and can be audited as a dynamic-programming recursion.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The state and action sets are finite or compact with a nonempty feasible set.', 'Rewards are finite and measurable.', 'A transition matrix or kernel is specified for each admissible action.', 'A terminal value or contraction condition is stated.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 4 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Specify the domain over which the maximum is taken.
    - `derivation_split` status `diagnostic_route`: State the reward map and transition law used to form expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_derivative_expectation_interchange_required` (derivative_expectation_interchange_required): The derivative-under-expectation step is not justified as an encodable theorem instance.
      Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`

How the derivation can work:
- `Define conditional law`: Specify the kernel or conditional distribution used by the expectation.
- `Check integrability`: Verify each random payoff, value, or derivative term has a finite conditional expectation.
- `Use expectation as scalar`: Only after those checks should the equality be treated as a scalar derivation step.
- `Declare state and actions`: Specify the domain over which the maximum is taken.
- `Define transition and reward`: State the reward map and transition law used to form expected continuation value.
- `Apply Bellman operator`: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value.

Backend attempts:
- `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`

Proposed patch candidates:
- `patch_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation` status `typed_translation_blocked`
  Proposed fix: Near `eq:foc-k` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-k > line 776, add an assumptions paragraph: "For this displayed equality, assume: The conditioned shock or path has finite support. Every payoff/value term inside the expectation is finite at each support point. The conditioning state or information set is explicitly defined. The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition` status `typed_translation_blocked`
  Proposed fix: Near `eq:foc-k` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-k > line 776, add an assumptions paragraph: "For this displayed equality, assume: A conditional kernel or probability law is fixed for the random object. All random terms inside the expectation are measurable under that law. Those terms are dominated by an integrable envelope or have finite conditional first moments. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman` status `typed_translation_blocked`
  Proposed fix: Near `eq:foc-k` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-k > line 776, add an assumptions paragraph: "For this displayed equality, assume: The state and action sets are finite or compact with a nonempty feasible set. Rewards are finite and measurable. A transition matrix or kernel is specified for each admissible action. A terminal value or contraction condition is stated. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The Bellman operator is well defined and can be audited as a dynamic-programming recursion.` by making the operators and objects in the displayed equality well-defined before backend certification.

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
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_derivative_expectation_interchange_required` (derivative_expectation_interchange_required)
  Problem: The derivative-under-expectation step is not justified as an encodable theorem instance.
  Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_derivative_expectation_interchange_required` (derivative_expectation_interchange_required)
  Problem: The derivative-under-expectation step is not justified as an encodable theorem instance.
  Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_derivative_expectation_interchange_required` (derivative_expectation_interchange_required)
  Problem: The derivative-under-expectation step is not justified as an encodable theorem instance.
  Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_semantic_packet_eq_foc_k_0_conditional_law_defined` (probability_condition)
  Problem: A conditional probability law for the random variables inside the expectation.
  Why: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
  Required next evidence: Makes the expectation operator well defined.
- `blocker_semantic_packet_eq_foc_k_0_measurable_integrable_payoff_terms` (integrability_condition)
  Problem: Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
  Why: Without measurability and integrability, the expectation may be undefined or infinite.
  Required next evidence: Turns the displayed expression into a finite scalar equality.
- `blocker_semantic_packet_eq_foc_k_0_conditioning_information_defined` (information_condition)
  Problem: A definition of the conditioning information set, state, or sigma-field.
  Why: The notation after the conditional bar determines what information the expectation conditions on.
  Required next evidence: Fixes the scope of the conditional expectation used in the derivation.
- `blocker_semantic_packet_eq_foc_k_0_state_action_spaces_defined` (dynamic_programming_condition)
  Problem: Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
  Why: A Bellman maximization is not well posed until its domain and feasible controls are defined.
  Required next evidence: Makes the optimization domain explicit.
- `blocker_semantic_packet_eq_foc_k_0_transition_kernel_defined` (probability_condition)
  Problem: A transition law for next-period states conditional on current state and action.
  Why: The continuation value is an expectation over next states; that expectation needs a transition kernel.
  Required next evidence: Defines the stochastic continuation operator.
- `blocker_semantic_packet_eq_foc_k_0_reward_and_value_integrable` (integrability_condition)
  Problem: Finite reward and integrable continuation value under each admissible action.
  Why: The objective may be undefined or infinite without boundedness or integrability conditions.
  Required next evidence: Makes the Bellman objective finite for comparison across actions.
- `blocker_semantic_packet_eq_foc_k_0_terminal_boundary_condition_defined` (recursion_boundary_condition)
  Problem: A terminal, transversality, or boundary condition for the recursive value.
  Why: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
  Required next evidence: Closes the recursive definition.
- `blocker_semantic_packet_eq_foc_k_0_source_extraction_uncertainty` (source_extraction_uncertainty)
  Problem: The localized source row has extraction uncertainty.
  Why: Equation locator reported: alignment_markers_preserved.
  Required next evidence: Recover a complete source-local obligation before promoting a derivation.

Smallest next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.

### 2. `eq:foc-b`

- Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-b > line 781`
- Claim type: `stochastic_expectation`
- Tree status: `budget_exhausted`
- Promotion guard: `can_promote=False`
- Semantic domains: `['conditional_expectation', 'bellman_value_recursion']`
- Extraction uncertainty: `['alignment_markers_preserved']`
- Full display span: `{'file': 'risky-debt-maliar-deep-learning-lecture-note.tex', 'line_start': 775, 'line_end': 786, 'labels': ['eq:foc-k', 'eq:foc-b'], 'environment': 'align', 'section_path': ['Residuals for the risky-debt model', 'Euler residuals from first-order conditions']}`
- Operators: `['equality', 'conditional_expectation', 'conditional_bar', 'derivative']`
- Symbols: `{'macros': ['\\E', '\\bar', '\\beta', '\\star'], 'identifiers': ['V', 'b', 'd', 'db', 'dk', 'e', 'k', 'm', 'z']}`
- Context graph statuses: `{'nearby_stated': 7, 'inferred_candidate': 5, 'unresolved': 4, 'missing': 2}`
- Typed repair obligation: `typed_repair_obligation_semantic_packet_eq_foc_b_1`
- Typed obligation status: `blocked_on_missing_typed_assumptions`
- Typed unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`

Source row target:

```tex
0
  &=
  m(\bar e)\frac{d\bar e}{db'}
  +\beta \E[V^\star_b(k',b',z')\mid z].
```

Full display target:

```tex
\begin{align}
  0
  &=
  m(\bar e)\frac{d\bar e}{dk'}
  +\beta \E[V^\star_k(k',b',z')\mid z],
  \label{eq:foc-k}\\
  0
  &=
  m(\bar e)\frac{d\bar e}{db'}
  +\beta \E[V^\star_b(k',b',z')\mid z].
  \label{eq:foc-b}
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
- `state_action_spaces_defined` (dynamic_programming_condition): Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
  Why: A Bellman maximization is not well posed until its domain and feasible controls are defined.
  Closes: Makes the optimization domain explicit.
- `transition_kernel_defined` (probability_condition): A transition law for next-period states conditional on current state and action.
  Why: The continuation value is an expectation over next states; that expectation needs a transition kernel.
  Closes: Defines the stochastic continuation operator.
- `reward_and_value_integrable` (integrability_condition): Finite reward and integrable continuation value under each admissible action.
  Why: The objective may be undefined or infinite without boundedness or integrability conditions.
  Closes: Makes the Bellman objective finite for comparison across actions.
- `terminal_boundary_condition_defined` (recursion_boundary_condition): A terminal, transversality, or boundary condition for the recursive value.
  Why: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
  Closes: Closes the recursive definition.

Local context graph:
- `assumption_continuation_state` status `nearby_stated`
  Role: rules out default/terminal regimes for the local FOC route
  What: The current state is a continuation state.
  Why status: The condition is stated in the local paragraph/proposition context.
  Required next evidence: Carry this stated condition into the typed FOC obligation.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:731-768', 'risky-debt-maliar-deep-learning-lecture-note.tex:770-787', 'risky-debt-maliar-deep-learning-lecture-note.tex:789-799']`
- `assumption_interior_action` status `nearby_stated`
  Role: permits first-order conditions instead of inequality/KKT boundary conditions
  What: The optimal action is interior.
  Why status: The condition is stated in the local paragraph/proposition context.
  Required next evidence: Carry this stated condition into the typed FOC obligation.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:731-768', 'risky-debt-maliar-deep-learning-lecture-note.tex:770-787', 'risky-debt-maliar-deep-learning-lecture-note.tex:789-799']`
- `assumption_relevant_functions_differentiable` status `nearby_stated`
  Role: supports local derivative notation in the FOC route
  What: The relevant functions are differentiable.
  Why status: The condition is stated in the local paragraph/proposition context.
  Required next evidence: Use this as differentiability evidence, but do not treat it as integrability or derivative-expectation interchange evidence.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:770-787', 'risky-debt-maliar-deep-learning-lecture-note.tex:789-799']`
- `definition_bar_e_current_cash_flow` status `nearby_stated`
  Role: definition of the cash-flow term used in the FOC rows
  What: The nearby text defines the interior current-cash-flow object `\bar e`.
  Why status: The definition appears in the local paragraph preceding the proposition.
  Required next evidence: Carry this definition into typed FOC obligations.
  Source refs: `['None:731-768']`
- `definition_marginal_cash_value_m` status `nearby_stated`
  Role: definition of the multiplier in the FOC rows
  What: The nearby text defines `m(e)` as the marginal value of current cash flow.
  Why status: The definition appears in the local paragraph preceding the proposition.
  Required next evidence: Carry this definition into typed FOC obligations.
  Source refs: `['None:731-768']`
- `notation_evaluation_point` status `nearby_stated`
  Role: notation declaration for derivative terms appearing in FOC rows
  What: The nearby text states the evaluation point for the cash-flow derivative terms.
  Why status: The declaration appears immediately before the proposition.
  Required next evidence: Carry the evaluation point into typed obligations to avoid free-symbol drift.
  Source refs: `['None:731-768']`
- `requirement_conditional_law_defined` status `unresolved`
  Role: well-definedness condition for conditional expectation
  What: A conditional law for the expectation is defined.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: Cite or add the transition kernel/probability law used by the conditional expectation.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`
- `requirement_conditional_integrability` status `unresolved`
  Role: finite-scalar condition for expectation-valued equations
  What: Random terms inside the conditional expectation are measurable and integrable.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: Cite or add measurability and finite conditional first-moment/dominated-envelope conditions.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`
- `requirement_expectation_derivative_interchange` status `unresolved`
  Role: justifies replacing the derivative of expected continuation value with expected value derivatives
  What: Differentiation may pass through the conditional expectation.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: State a finite-state sum route or a dominated/Leibniz interchange condition for the continuation-value derivatives.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`
- `requirement_choice_independent_transition_law` status `unresolved`
  Role: rules out omitted transition-kernel derivative terms in the FOC
  What: The conditional law does not add choice-derivative terms.
  Why status: The local source contains related notation or a proof step, but not the required condition itself.
  Required next evidence: State that the conditional law of `z'` given `z` is independent of `k'` and `b'`, or include the missing kernel derivative terms.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`
- `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`
  Role: route-required assumption from assumption_discovery
  What: conditional expectation law is defined and the random payoff terms are integrable
  Why status: The low-level route detector marked this assumption as missing.
  Required next evidence: Resolve this assumption in typed IR before backend proof attempts.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`
- `route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present` status `missing`
  Role: route-required assumption from assumption_discovery
  What: differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present
  Why status: The low-level route detector marked this assumption as missing.
  Required next evidence: Resolve this assumption in typed IR before backend proof attempts.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:781-785']`
- `route_assumption_target_function_is_differentiable_on_the_stated_domain` status `nearby_stated`
  Role: route-required assumption from assumption_discovery
  What: target function is differentiable on the stated domain
  Why status: The condition is stated in the local paragraph/proposition context. This reconciles the low-level route requirement with local source evidence.
  Required next evidence: Resolve this assumption in typed IR before backend proof attempts.
  Source refs: `['risky-debt-maliar-deep-learning-lecture-note.tex:770-787', 'risky-debt-maliar-deep-learning-lecture-note.tex:789-799']`

Typed repair obligation:
- ID: `typed_repair_obligation_semantic_packet_eq_foc_b_1`
  Diagnostic status: `blocked_on_missing_typed_assumptions`
  Encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  Unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`
  Route hints: `[{'backend': 'lean', 'suitability': 'formalization_candidate', 'reason': 'Typed notation may be formalized manually and checked by Lean.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing assumptions or unsupported notation prevent verified backend routing.'}, {'backend': 'manual_formalization', 'suitability': 'required_before_cas', 'reason': 'Conditional expectation requires a typed probability kernel and integrability assumptions before CAS or Lean encoding.'}, {'backend': 'lean', 'suitability': 'formalization_candidate_after_assumptions', 'reason': 'Derivative-under-expectation can only be checked after the interchange theorem assumptions are stated.'}, {'backend': 'human_review', 'suitability': 'required', 'reason': 'Missing or unresolved typed assumptions block certifying backend attempts.'}]`
  Assumption statuses:
  - `route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable` status `missing`: conditional expectation law is defined and the random payoff terms are integrable
  - `route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present` status `missing`: differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present
  - `requirement_choice_independent_transition_law` status `unresolved`: The conditional law does not add choice-derivative terms.
  - `requirement_conditional_integrability` status `unresolved`: Random terms inside the conditional expectation are measurable and integrable.
  - `requirement_conditional_law_defined` status `unresolved`: A conditional law for the expectation is defined.
  - `requirement_expectation_derivative_interchange` status `unresolved`: Differentiation may pass through the conditional expectation.
  - `assumption_continuation_state` status `nearby_stated`: The current state is a continuation state.
  - `assumption_interior_action` status `nearby_stated`: The optimal action is interior.
  - `assumption_relevant_functions_differentiable` status `nearby_stated`: The relevant functions are differentiable.
  - `route_assumption_target_function_is_differentiable_on_the_stated_domain` status `nearby_stated`: target function is differentiable on the stated domain
  Boundary: Typed repair obligations are diagnostic routing artifacts; they are not proof certificates or backend encodings.

Possible sufficient assumption sets:
- `finite_state_conditional_expectation`: The expectation becomes a finite weighted sum.
  - The conditioned shock or path has finite support.
  - Every payoff/value term inside the expectation is finite at each support point.
  - The conditioning state or information set is explicitly defined.
- `kernel_integrability_condition`: The expectation is a well-defined finite conditional integral.
  - A conditional kernel or probability law is fixed for the random object.
  - All random terms inside the expectation are measurable under that law.
  - Those terms are dominated by an integrable envelope or have finite conditional first moments.
- `finite_state_finite_action_bellman`: The Bellman operator is well defined and can be audited as a dynamic-programming recursion.
  - The state and action sets are finite or compact with a nonempty feasible set.
  - Rewards are finite and measurable.
  - A transition matrix or kernel is specified for each admissible action.
  - A terminal value or contraction condition is stated.

Branch ranking:
- Contract: `repair_branch_ranking_result`
- Top branch: `branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition`
- Rank `1`: `branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition` outcome `blocked_with_specific_next_evidence`, score `83`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 2, 'score': 83, 'specific_blocker_count': 7, 'backend_attempt_count': 1, 'assumption_count': 3}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=2.
- Rank `2`: `branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation` outcome `blocked_with_specific_next_evidence`, score `81`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 4, 'score': 81, 'specific_blocker_count': 7, 'backend_attempt_count': 1, 'assumption_count': 4}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=4.
- Rank `3`: `branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman` outcome `blocked_with_specific_next_evidence`, score `81`
  - Components: `{'backend_certification': 25, 'closure_strength': 20, 'source_support': 15, 'blocker_specificity': 25, 'non_minimality_penalty': 4, 'score': 81, 'specific_blocker_count': 7, 'backend_attempt_count': 1, 'assumption_count': 4}`
  - Explanation: Ranked as blocked_with_specific_next_evidence: backend=25, closure=20, source=15, blocker_specificity=25, non_minimality_penalty=4.

Candidate assumption branches:
- `branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'transition_kernel_defined', 'reward_and_value_integrable']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_foc_b_1']`
  - Typed unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The conditioned shock or path has finite support.', 'Every payoff/value term inside the expectation is finite at each support point.', 'The conditioning state or information set is explicitly defined.', 'The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 4 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Specify the domain over which the maximum is taken.
    - `derivation_split` status `diagnostic_route`: State the reward map and transition law used to form expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_derivative_expectation_interchange_required` (derivative_expectation_interchange_required): The derivative-under-expectation step is not justified as an encodable theorem instance.
      Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'transition_kernel_defined', 'reward_and_value_integrable']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_foc_b_1']`
  - Typed unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['A conditional kernel or probability law is fixed for the random object.', 'All random terms inside the expectation are measurable under that law.', 'Those terms are dominated by an integrable envelope or have finite conditional first moments.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 3 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Specify the domain over which the maximum is taken.
    - `derivation_split` status `diagnostic_route`: State the reward map and transition law used to form expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_derivative_expectation_interchange_required` (derivative_expectation_interchange_required): The derivative-under-expectation step is not justified as an encodable theorem instance.
      Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman` status `blocked_before_backend_certification`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'state_action_spaces_defined', 'transition_kernel_defined', 'reward_and_value_integrable', 'terminal_boundary_condition_defined']`
  - Typed obligation ids: `['typed_repair_obligation_semantic_packet_eq_foc_b_1']`
  - Typed unresolved constructs: `['latex_derivative', 'expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present']`
  - Typed encodability: `{'status': 'blocked_pending_typed_assumptions', 'candidate_backends': ['lean', 'human_review', 'manual_formalization'], 'blocked_by_assumption_ids': ['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange'], 'unsupported_constructs': ['expectation', 'conditional', 'conditional_law', 'integrability', 'derivative_expectation_interchange'], 'why': 'Missing/unresolved assumptions or stochastic/interchange constructs must be resolved before certifying backend routing.'}`
  - Backend evidence status: `typed_translation_blocked`
  - Backend promotion guard: `{'can_promote': False, 'supported_status': None, 'reason': 'No certifying proof/refutation evidence supports promotion.', 'errors': [], 'evidence_refs': [], 'boundary': 'A branch can be promoted to proved or refuted only from scoped certifying backend evidence or a concrete counterexample. Route plans, retrieval hits, static extraction, proof-state traces, and backend unavailability are diagnostic evidence only.'}`
  - Why: This branch closes `The Bellman operator is well defined and can be audited as a dynamic-programming recursion.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The state and action sets are finite or compact with a nonempty feasible set.', 'Rewards are finite and measurable.', 'A transition matrix or kernel is specified for each admissible action.', 'A terminal value or contraction condition is stated.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - Expansion records:
    - `assumption_addition` status `proposed`: Propose 4 assumption(s) for this branch.
    - `derivation_split` status `diagnostic_route`: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - `derivation_split` status `diagnostic_route`: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Only after those checks should the equality be treated as a scalar derivation step.
    - `derivation_split` status `diagnostic_route`: Specify the domain over which the maximum is taken.
    - `derivation_split` status `diagnostic_route`: State the reward map and transition law used to form expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `derivation_split` status `diagnostic_route`: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - `formalization_route` status `executed`: sympy has bounded attempt evidence attached to this branch.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Branch backend attempts:
    - `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`
  - Translation attempts:
    - `sympy` status `executed`; attempt ids `['sympy_algebra_attempt']`; blockers `[]`
    - `sage` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_latex_macro_translation_required']`
    - `lean` status `blocked_before_execution`; attempt ids `[]`; blockers `['blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditional_expectation_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditioning_scope_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditional_law_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_integrability_translation_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_derivative_expectation_interchange_required', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_missing_typed_assumptions', 'blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_latex_macro_translation_required']`
  - Translation blockers:
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditional_expectation_translation_required` (conditional_expectation_translation_required): The expectation operator cannot be translated as a scalar algebraic expression yet.
      Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditioning_scope_translation_required` (conditioning_scope_translation_required): The conditional bar has no backend-level conditioning object yet.
      Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditional_law_translation_required` (conditional_law_translation_required): The conditional law required by the expectation is not stated as an encodable object.
      Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_integrability_translation_required` (integrability_translation_required): Integrability of the random payoff/value terms is not established.
      Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_derivative_expectation_interchange_required` (derivative_expectation_interchange_required): The derivative-under-expectation step is not justified as an encodable theorem instance.
      Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
      Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_missing_typed_assumptions` (missing_domain_or_assumption_required): The branch still has missing or unresolved typed assumptions.
      Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
      Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
    - `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_latex_macro_translation_required` (macro_translation_required): LaTeX macros must be translated into backend symbols before execution.
      Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
      Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`

How the derivation can work:
- `Define conditional law`: Specify the kernel or conditional distribution used by the expectation.
- `Check integrability`: Verify each random payoff, value, or derivative term has a finite conditional expectation.
- `Use expectation as scalar`: Only after those checks should the equality be treated as a scalar derivation step.
- `Declare state and actions`: Specify the domain over which the maximum is taken.
- `Define transition and reward`: State the reward map and transition law used to form expected continuation value.
- `Apply Bellman operator`: Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value.

Backend attempts:
- `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`

Proposed patch candidates:
- `patch_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation` status `typed_translation_blocked`
  Proposed fix: Near `eq:foc-b` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-b > line 781, add an assumptions paragraph: "For this displayed equality, assume: The conditioned shock or path has finite support. Every payoff/value term inside the expectation is finite at each support point. The conditioning state or information set is explicitly defined. The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition` status `typed_translation_blocked`
  Proposed fix: Near `eq:foc-b` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-b > line 781, add an assumptions paragraph: "For this displayed equality, assume: A conditional kernel or probability law is fixed for the random object. All random terms inside the expectation are measurable under that law. Those terms are dominated by an integrable envelope or have finite conditional first moments. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman` status `typed_translation_blocked`
  Proposed fix: Near `eq:foc-b` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-b > line 781, add an assumptions paragraph: "For this displayed equality, assume: The state and action sets are finite or compact with a nonempty feasible set. Rewards are finite and measurable. A transition matrix or kernel is specified for each admissible action. A terminal value or contraction condition is stated. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The Bellman operator is well defined and can be audited as a dynamic-programming recursion.` by making the operators and objects in the displayed equality well-defined before backend certification.

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
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_derivative_expectation_interchange_required` (derivative_expectation_interchange_required)
  Problem: The derivative-under-expectation step is not justified as an encodable theorem instance.
  Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_derivative_expectation_interchange_required` (derivative_expectation_interchange_required)
  Problem: The derivative-under-expectation step is not justified as an encodable theorem instance.
  Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditional_expectation_translation_required` (conditional_expectation_translation_required)
  Problem: The expectation operator cannot be translated as a scalar algebraic expression yet.
  Why: A backend needs the probability law, measurable random terms, and finite expectation before it can encode the target.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditioning_scope_translation_required` (conditioning_scope_translation_required)
  Problem: The conditional bar has no backend-level conditioning object yet.
  Why: The expression must identify whether the conditioning object is a state, sigma-field, information set, or kernel argument.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_conditional_law_translation_required` (conditional_law_translation_required)
  Problem: The conditional law required by the expectation is not stated as an encodable object.
  Why: Conditional expectation notation is only meaningful after the transition kernel or conditional distribution is fixed.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_integrability_translation_required` (integrability_translation_required)
  Problem: Integrability of the random payoff/value terms is not established.
  Why: Without finite conditional first moments or a dominated envelope, the backend cannot treat the expectation as finite.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_derivative_expectation_interchange_required` (derivative_expectation_interchange_required)
  Problem: The derivative-under-expectation step is not justified as an encodable theorem instance.
  Why: The backend needs a finite-state sum route or a dominated/Leibniz interchange condition before this derivation step can be checked.
  Required next evidence: State or verify the required typed assumption, update the branch assumptions, and rerun the backend translator.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_missing_typed_assumptions` (missing_domain_or_assumption_required)
  Problem: The branch still has missing or unresolved typed assumptions.
  Why: Typed encodability is blocked by `['route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable', 'route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present', 'requirement_choice_independent_transition_law', 'requirement_conditional_integrability', 'requirement_conditional_law_defined', 'requirement_expectation_derivative_interchange']`.
  Required next evidence: Close each listed typed assumption with a source citation or an explicit proposed assumption before certifying backend translation.
- `blocker_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_latex_macro_translation_required` (macro_translation_required)
  Problem: LaTeX macros must be translated into backend symbols before execution.
  Why: The source span contains macros `['\\E', '\\bar', '\\beta', '\\star']` whose mathematical types and backend names are not fixed.
  Required next evidence: Map each macro used by the target to a typed backend symbol or definition and rerun the translator.
- `blocker_formalization_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; derivative/interchange step requires differentiability and domain formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_semantic_packet_eq_foc_b_1_conditional_law_defined` (probability_condition)
  Problem: A conditional probability law for the random variables inside the expectation.
  Why: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
  Required next evidence: Makes the expectation operator well defined.
- `blocker_semantic_packet_eq_foc_b_1_measurable_integrable_payoff_terms` (integrability_condition)
  Problem: Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
  Why: Without measurability and integrability, the expectation may be undefined or infinite.
  Required next evidence: Turns the displayed expression into a finite scalar equality.
- `blocker_semantic_packet_eq_foc_b_1_conditioning_information_defined` (information_condition)
  Problem: A definition of the conditioning information set, state, or sigma-field.
  Why: The notation after the conditional bar determines what information the expectation conditions on.
  Required next evidence: Fixes the scope of the conditional expectation used in the derivation.
- `blocker_semantic_packet_eq_foc_b_1_state_action_spaces_defined` (dynamic_programming_condition)
  Problem: Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.
  Why: A Bellman maximization is not well posed until its domain and feasible controls are defined.
  Required next evidence: Makes the optimization domain explicit.
- `blocker_semantic_packet_eq_foc_b_1_transition_kernel_defined` (probability_condition)
  Problem: A transition law for next-period states conditional on current state and action.
  Why: The continuation value is an expectation over next states; that expectation needs a transition kernel.
  Required next evidence: Defines the stochastic continuation operator.
- `blocker_semantic_packet_eq_foc_b_1_reward_and_value_integrable` (integrability_condition)
  Problem: Finite reward and integrable continuation value under each admissible action.
  Why: The objective may be undefined or infinite without boundedness or integrability conditions.
  Required next evidence: Makes the Bellman objective finite for comparison across actions.
- `blocker_semantic_packet_eq_foc_b_1_terminal_boundary_condition_defined` (recursion_boundary_condition)
  Problem: A terminal, transversality, or boundary condition for the recursive value.
  Why: A recursion cannot be checked as a dynamic-programming equation without a boundary condition.
  Required next evidence: Closes the recursive definition.
- `blocker_semantic_packet_eq_foc_b_1_source_extraction_uncertainty` (source_extraction_uncertainty)
  Problem: The localized source row has extraction uncertainty.
  Why: Equation locator reported: alignment_markers_preserved.
  Required next evidence: Recover a complete source-local obligation before promoting a derivation.

Smallest next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.

## Non-Claims

- `document_tree_audit_not_document_proof`: This workflow is a semantic gap and tree-evidence report; it does not prove the whole document.
- `semantic_packets_not_certificates`: Missing obligations, assumption sets, and derivation routes are deterministic guidance, not proof certificates.
- `proof_search_not_final_certificate`: LeanDojo, Pantograph, retrieval, route plans, and static extraction are diagnostic until direct Lean or another certifying backend checks the scoped target.
