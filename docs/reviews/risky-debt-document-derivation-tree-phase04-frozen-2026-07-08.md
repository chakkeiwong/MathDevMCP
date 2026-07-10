# Document Derivation Tree Audit

Target: `docs/risky-debt-maliar-deep-learning-lecture-note.tex`

## Executive Summary

- Selected source rows: `3`
- Semantic packets: `3`
- Promoted branches: `0`
- Blockers: `52`
- Missing focus labels: `['prop:interior-foc']`
- This report is generic and document-local; it is not tied to a card-NPV-specific plan.

## Tools Used

| Tool | Purpose | Status | Contract | Arguments |
| --- | --- | --- | --- | --- |
| `locate_equations_in_file` | Localize source rows in the exact target file. | `completed` | `equation_rows` | `{"root": "docs", "tex_path": "docs/risky-debt-maliar-deep-learning-lecture-note.tex"}` |
| `build_semantic_work_packet` | Classify each target and generate full-display semantic packets, missing obligations, assumption sets, and derivation routes. | `completed` | `semantic_work_packet` | `{"selected_rows": 3}` |
| `assumptions_required` | Detect route-required assumptions before backend proof attempts. | `completed` | `assumption_discovery_result` | `{"selected_rows": 3}` |
| `doctor_report` | Record external backend capability provenance. | `available` | `doctor_report` | `{"backend_env": "mathdevmcp-backends"}` |
| `can_derive_with_budget` | Run the external-tool-first branch controller on semantic packet targets. | `completed` | `derivation_search_tree_result` | `{"budget_profile": "standard", "max_attempts": 1, "selected_rows": 3}` |
| `render_derivation_tree_report` | Render each derivation tree into structured evidence sections. | `completed` | `derivation_tree_report_result` | `{"rendered_trees": 3}` |

## Target Packets And Trees

### 1. `eq:risky-pricing`

- Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Debt pricing > eq:risky-pricing > line 399`
- Claim type: `identity_or_definition`
- Tree status: `budget_exhausted`
- Promotion guard: `can_promote=False`
- Semantic domains: `['conditional_expectation']`
- Extraction uncertainty: `[]`
- Full display span: `{'file': 'risky-debt-maliar-deep-learning-lecture-note.tex', 'line_start': 398, 'line_end': 407, 'labels': ['eq:risky-pricing'], 'environment': 'equation', 'section_path': ['Debt pricing']}`
- Operators: `['equality', 'conditional_expectation', 'conditional_bar']`
- Symbols: `{'macros': ['\\E', '\\widetilde'], 'identifiers': ['D', 'R', 'b', 'k', 'r', 'z']}`

Source row target:

```tex
b'(1+r)
  =
  \E\left[
    D(k',b',z')R(k',z')
    +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))
    \mid z
  \right].
```

Full display target:

```tex
\begin{equation}
  b'(1+r)
  =
  \E\left[
    D(k',b',z')R(k',z')
    +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))
    \mid z
  \right].
  \label{eq:risky-pricing}
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

Possible sufficient assumption sets:
- `finite_state_conditional_expectation`: The expectation becomes a finite weighted sum.
  - The conditioned shock or path has finite support.
  - Every payoff/value term inside the expectation is finite at each support point.
  - The conditioning state or information set is explicitly defined.
- `kernel_integrability_condition`: The expectation is a well-defined finite conditional integral.
  - A conditional kernel or probability law is fixed for the random object.
  - All random terms inside the expectation are measurable under that law.
  - Those terms are dominated by an integrable envelope or have finite conditional first moments.

Candidate assumption branches:
- `branch_semantic_packet_eq_risky_pricing_0_finite_state_conditional_expectation` status `proposed_sufficient_not_minimal`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined']`
  - Why: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The conditioned shock or path has finite support.', 'Every payoff/value term inside the expectation is finite at each support point.', 'The conditioning state or information set is explicitly defined.', 'The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `D(k',b',z'), R(k',z'), r(z,k',b')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_risky_pricing_0_kernel_integrability_condition` status `proposed_sufficient_not_minimal`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined']`
  - Why: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['A conditional kernel or probability law is fixed for the random object.', 'All random terms inside the expectation are measurable under that law.', 'Those terms are dominated by an integrable envelope or have finite conditional first moments.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `D(k',b',z'), R(k',z'), r(z,k',b')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`

How the derivation can work:
- `Define conditional law`: Specify the kernel or conditional distribution used by the expectation.
- `Check integrability`: Verify each random payoff, value, or derivative term has a finite conditional expectation.
- `Use expectation as scalar`: Only after those checks should the equality be treated as a scalar derivation step.

Backend attempts:
- `sympy_algebra_attempt` with `sympy`: status `missing_assumptions`, evidence `diagnostic`, certification `diagnostic`

Proposed patch candidates:
- `patch_branch_semantic_packet_eq_risky_pricing_0_finite_state_conditional_expectation` status `diagnostic_pending_backend_or_formalization`
  Proposed fix: Near `eq:risky-pricing` at risky-debt-maliar-deep-learning-lecture-note.tex > Debt pricing > eq:risky-pricing > line 399, add an assumptions paragraph: "For this displayed equality, assume: The conditioned shock or path has finite support. Every payoff/value term inside the expectation is finite at each support point. The conditioning state or information set is explicitly defined. The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `D(k',b',z'), R(k',z'), r(z,k',b')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_risky_pricing_0_kernel_integrability_condition` status `diagnostic_pending_backend_or_formalization`
  Proposed fix: Near `eq:risky-pricing` at risky-debt-maliar-deep-learning-lecture-note.tex > Debt pricing > eq:risky-pricing > line 399, add an assumptions paragraph: "For this displayed equality, assume: A conditional kernel or probability law is fixed for the random object. All random terms inside the expectation are measurable under that law. Those terms are dominated by an integrable envelope or have finite conditional first moments. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `D(k',b',z'), R(k',z'), r(z,k',b')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.

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
- `blocker_formalization_branch_semantic_packet_eq_risky_pricing_0_finite_state_conditional_expectation_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_risky_pricing_0_finite_state_conditional_expectation_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_risky_pricing_0_finite_state_conditional_expectation_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_risky_pricing_0_kernel_integrability_condition_sympy` (formalization_required)
  Problem: sympy stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_risky_pricing_0_kernel_integrability_condition_sage` (formalization_required)
  Problem: sage stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_formalization_branch_semantic_packet_eq_risky_pricing_0_kernel_integrability_condition_lean` (formalization_required)
  Problem: lean stub is not yet a certifying formalization.
  Why: conditional expectation requires a probability kernel/integrability formalization; LaTeX macros require translation to backend symbols; Lean theorem statement for the LaTeX equality has not been generated
  Required next evidence: Translate the source-local equality and branch assumptions into the backend language, then run the backend check.
- `blocker_semantic_packet_eq_risky_pricing_0_conditional_law_defined` (probability_condition)
  Problem: A conditional probability law for the random variables inside the expectation.
  Why: A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.
  Required next evidence: Makes the expectation operator well defined.
- `blocker_semantic_packet_eq_risky_pricing_0_measurable_integrable_payoff_terms` (integrability_condition)
  Problem: Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.
  Why: Without measurability and integrability, the expectation may be undefined or infinite.
  Required next evidence: Turns the displayed expression into a finite scalar equality.
- `blocker_semantic_packet_eq_risky_pricing_0_conditioning_information_defined` (information_condition)
  Problem: A definition of the conditioning information set, state, or sigma-field.
  Why: The notation after the conditional bar determines what information the expectation conditions on.
  Required next evidence: Fixes the scope of the conditional expectation used in the derivation.

Smallest next audit: `audit_and_propose_assumptions` - Generate explicit assumption proposals for the missing route conditions.

### 2. `eq:foc-k`

- Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-k > line 776`
- Claim type: `stochastic_expectation`
- Tree status: `budget_exhausted`
- Promotion guard: `can_promote=False`
- Semantic domains: `['conditional_expectation', 'bellman_value_recursion']`
- Extraction uncertainty: `['alignment_markers_preserved']`
- Full display span: `{'file': 'risky-debt-maliar-deep-learning-lecture-note.tex', 'line_start': 775, 'line_end': 786, 'labels': ['eq:foc-k', 'eq:foc-b'], 'environment': 'align', 'section_path': ['Residuals for the risky-debt model', 'Euler residuals from first-order conditions']}`
- Operators: `['equality', 'conditional_expectation', 'conditional_bar', 'derivative']`
- Symbols: `{'macros': ['\\E', '\\bar', '\\beta', '\\star'], 'identifiers': ['V', 'b', 'd', 'db', 'dk', 'e', 'k', 'm', 'z']}`

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

Candidate assumption branches:
- `branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation` status `proposed_sufficient_not_minimal`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'transition_kernel_defined', 'reward_and_value_integrable']`
  - Why: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The conditioned shock or path has finite support.', 'Every payoff/value term inside the expectation is finite at each support point.', 'The conditioning state or information set is explicitly defined.', 'The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition` status `proposed_sufficient_not_minimal`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'transition_kernel_defined', 'reward_and_value_integrable']`
  - Why: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['A conditional kernel or probability law is fixed for the random object.', 'All random terms inside the expectation are measurable under that law.', 'Those terms are dominated by an integrable envelope or have finite conditional first moments.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman` status `proposed_sufficient_not_minimal`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'state_action_spaces_defined', 'transition_kernel_defined', 'reward_and_value_integrable', 'terminal_boundary_condition_defined']`
  - Why: This branch closes `The Bellman operator is well defined and can be audited as a dynamic-programming recursion.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The state and action sets are finite or compact with a nonempty feasible set.', 'Rewards are finite and measurable.', 'A transition matrix or kernel is specified for each admissible action.', 'A terminal value or contraction condition is stated.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
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
- `patch_branch_semantic_packet_eq_foc_k_0_finite_state_conditional_expectation` status `diagnostic_pending_backend_or_formalization`
  Proposed fix: Near `eq:foc-k` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-k > line 776, add an assumptions paragraph: "For this displayed equality, assume: The conditioned shock or path has finite support. Every payoff/value term inside the expectation is finite at each support point. The conditioning state or information set is explicitly defined. The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition` status `diagnostic_pending_backend_or_formalization`
  Proposed fix: Near `eq:foc-k` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-k > line 776, add an assumptions paragraph: "For this displayed equality, assume: A conditional kernel or probability law is fixed for the random object. All random terms inside the expectation are measurable under that law. Those terms are dominated by an integrable envelope or have finite conditional first moments. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_foc_k_0_finite_state_finite_action_bellman` status `diagnostic_pending_backend_or_formalization`
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

### 3. `eq:foc-b`

- Location: `risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-b > line 781`
- Claim type: `stochastic_expectation`
- Tree status: `budget_exhausted`
- Promotion guard: `can_promote=False`
- Semantic domains: `['conditional_expectation', 'bellman_value_recursion']`
- Extraction uncertainty: `['alignment_markers_preserved']`
- Full display span: `{'file': 'risky-debt-maliar-deep-learning-lecture-note.tex', 'line_start': 775, 'line_end': 786, 'labels': ['eq:foc-k', 'eq:foc-b'], 'environment': 'align', 'section_path': ['Residuals for the risky-debt model', 'Euler residuals from first-order conditions']}`
- Operators: `['equality', 'conditional_expectation', 'conditional_bar', 'derivative']`
- Symbols: `{'macros': ['\\E', '\\bar', '\\beta', '\\star'], 'identifiers': ['V', 'b', 'd', 'db', 'dk', 'e', 'k', 'm', 'z']}`

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

Candidate assumption branches:
- `branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation` status `proposed_sufficient_not_minimal`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'transition_kernel_defined', 'reward_and_value_integrable']`
  - Why: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The conditioned shock or path has finite support.', 'Every payoff/value term inside the expectation is finite at each support point.', 'The conditioning state or information set is explicitly defined.', 'The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition` status `proposed_sufficient_not_minimal`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'transition_kernel_defined', 'reward_and_value_integrable']`
  - Why: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['A conditional kernel or probability law is fixed for the random object.', 'All random terms inside the expectation are measurable under that law.', 'Those terms are dominated by an integrable envelope or have finite conditional first moments.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
  - Formalization stubs:
    - `sympy` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `sage` status `requires_manual_translation`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols']`
    - `lean` status `skeleton_contains_sorry_not_certifying`; unsupported: `['conditional expectation requires a probability kernel/integrability formalization', 'derivative/interchange step requires differentiability and domain formalization', 'LaTeX macros require translation to backend symbols', 'Lean theorem statement for the LaTeX equality has not been generated']`
- `branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman` status `proposed_sufficient_not_minimal`
  - Closes obligations: `['conditional_law_defined', 'measurable_integrable_payoff_terms', 'conditioning_information_defined', 'state_action_spaces_defined', 'transition_kernel_defined', 'reward_and_value_integrable', 'terminal_boundary_condition_defined']`
  - Why: This branch closes `The Bellman operator is well defined and can be audited as a dynamic-programming recursion.` by making the operators and objects in the displayed equality well-defined before backend certification.
  - Proposed assumptions: ['The state and action sets are finite or compact with a nonempty feasible set.', 'Rewards are finite and measurable.', 'A transition matrix or kernel is specified for each admissible action.', 'A terminal value or contraction condition is stated.']
  - Route under assumptions:
    - Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`.
    - Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`.
    - Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step.
    - Declare state and actions: Specify the domain over which the maximum is taken.
  - External-tool ledger: `['sympy:requires_formalization', 'sage:requires_formalization', 'lean:requires_formalization', 'leansearchv2:available', 'lean_explore:available', 'jixia:requires_formalization', 'pantograph:requires_formalization', 'lean_dojo:requires_formalization']`
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
- `patch_branch_semantic_packet_eq_foc_b_1_finite_state_conditional_expectation` status `diagnostic_pending_backend_or_formalization`
  Proposed fix: Near `eq:foc-b` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-b > line 781, add an assumptions paragraph: "For this displayed equality, assume: The conditioned shock or path has finite support. Every payoff/value term inside the expectation is finite at each support point. The conditioning state or information set is explicitly defined. The conditioning object `z` is defined as a sigma-field, information set, state, or conditioning variable for this equality. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation becomes a finite weighted sum.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_foc_b_1_kernel_integrability_condition` status `diagnostic_pending_backend_or_formalization`
  Proposed fix: Near `eq:foc-b` at risky-debt-maliar-deep-learning-lecture-note.tex > Residuals for the risky-debt model > Euler residuals from first-order conditions > eq:foc-b > line 781, add an assumptions paragraph: "For this displayed equality, assume: A conditional kernel or probability law is fixed for the random object. All random terms inside the expectation are measurable under that law. Those terms are dominated by an integrable envelope or have finite conditional first moments. Under these assumptions, the derivation route is: Define conditional law: Specify the kernel or conditional distribution used by the expectation. In this source span, the conditioning object is `z`. Check integrability: Verify each random payoff, value, or derivative term has a finite conditional expectation. In this source span, the conditioning object is `z`. Candidate source-local random terms include `star_k(k',b',z'), star_b(k',b',z')`. Use expectation as scalar: Only after those checks should the equality be treated as a scalar derivation step."
  Rationale: This branch closes `The expectation is a well-defined finite conditional integral.` by making the operators and objects in the displayed equality well-defined before backend certification.
- `patch_branch_semantic_packet_eq_foc_b_1_finite_state_finite_action_bellman` status `diagnostic_pending_backend_or_formalization`
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
