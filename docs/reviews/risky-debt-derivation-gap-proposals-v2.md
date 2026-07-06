# Derivation Gap/Proposal Report

Question: Audit risky-debt derivations with extracted obligations

Status: `proposal_ready`

## Coverage

- Targets inspected: 3
- Gaps: 3
- Proposals: 3
- Certifying proposals: 0

## Extracted Targets

- Extracted target count: 3
- Full-block fallback count: 0

### Parent Label: `prop:risky-pricing`

- Target: `eq:risky-pricing`
  - Location: `risky-debt-maliar-deep-learning-lecture-note.tex > line 399`
  - Extraction status: `extracted`
  - LHS: `b'(1+r)`
  - RHS: `\E\left[     D(k',b',z')R(k',z')     +(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))     \mid z   \right].`

### Parent Label: `prop:interior-foc`

- Target: `eq:foc-k`
  - Location: `risky-debt-maliar-deep-learning-lecture-note.tex > line 776`
  - Extraction status: `extracted`
  - LHS: `0`
  - RHS: `m(\bar e)\frac{d\bar e}{dk'}   +\beta \E[V^\star_k(k',b',z')\mid z],`

- Target: `eq:foc-b`
  - Location: `risky-debt-maliar-deep-learning-lecture-note.tex > line 781`
  - Extraction status: `extracted`
  - LHS: `0`
  - RHS: `m(\bar e)\frac{d\bar e}{db'}   +\beta \E[V^\star_b(k',b',z')\mid z].`

## Backend Route Plans

### prop:risky-pricing

- Target label: `eq:risky-pricing`
- Location: `risky-debt-maliar-deep-learning-lecture-note.tex > line 399`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### prop:interior-foc

- Target label: `eq:foc-k`
- Location: `risky-debt-maliar-deep-learning-lecture-note.tex > line 776`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

### prop:interior-foc

- Target label: `eq:foc-b`
- Location: `risky-debt-maliar-deep-learning-lecture-note.tex > line 781`
- Selected route: `bounded_counterexample:counterexample_search` with status `requires_formalization`
- Boundary: Route planning is diagnostic only. A route candidate is not a proof, refutation, or validated derivation unless a scoped backend certificate or concrete counterexample is recorded by a downstream tool.

| Backend | Route | Status | Tool | Evidence Contract | Reason |
| --- | --- | --- | --- | --- | --- |
| `sympy` | `symbolic_identity` | `not_applicable` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain hints require review before scalar symbolic routing. |
| `bounded_counterexample` | `counterexample_search` | `requires_formalization` | `find_counterexample` | `counterexample_search_result` | The equality has lhs/rhs, but the expression must be formalized before bounded counterexample search can encode it. |
| `sage` | `matrix_domain_symbolic` | `requires_formalization` | `derive_or_refute` | `derive_or_refute_result` | Matrix/domain notation suggests Sage could help after the LaTeX expression is formalized. |
| `lean` | `formal_proof` | `requires_formalization` | `lean_check` | `lean_check_result` | The target contains LaTeX/domain notation and needs explicit Lean source before Lean can certify anything. |

## Tool Uses

| Tool | Purpose | Status | Output | Arguments |
| --- | --- | --- | --- | --- |
| `build_index` | Extract LaTeX labels and source locations for derivation auditing. | `completed` | `latex_index` | `{'root': 'docs'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': 'docs', 'label': 'prop:risky-pricing'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'risky-debt-maliar-deep-learning-lecture-note.tex:395:proposition:prop:risky-pricing:target:eq:risky-pricing', 'label': 'eq:risky-pricing', 'parent_label': 'prop:risky-pricing'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': "b'(1+r) = \\E\\left[\n    D(k',b',z')R(k',z')\n    +(1-D(k',b',z'))b'(1+\\widetilde r(z,k',b'))\n    \\mid z\n  \\right].", 'givens': [], 'assumptions': [], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': "b'(1+r) = \\E\\left[\n    D(k',b',z')R(k',z')\n    +(1-D(k',b',z'))b'(1+\\widetilde r(z,k',b'))\n    \\mid z\n  \\right]."}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `extract_derivation_targets_for_label` | Extract source-local equation or align-row obligations from the label block. | `extracted` | `derivation_target_extraction_result` | `{'root': 'docs', 'label': 'prop:interior-foc'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'risky-debt-maliar-deep-learning-lecture-note.tex:770:proposition:prop:interior-foc:target:eq:foc-k', 'label': 'eq:foc-k', 'parent_label': 'prop:interior-foc'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': "0 = m(\\bar e)\\frac{d\\bar e}{dk'}\n  +\\beta \\E[V^\\star_k(k',b',z')\\mid z],", 'givens': [], 'assumptions': [], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': "0 = m(\\bar e)\\frac{d\\bar e}{dk'}\n  +\\beta \\E[V^\\star_k(k',b',z')\\mid z],"}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `plan_backend_routes` | Plan deterministic backend routes for the extracted obligation without claiming proof. | `planned` | `backend_route_plan_result` | `{'target_id': 'risky-debt-maliar-deep-learning-lecture-note.tex:770:proposition:prop:interior-foc:target:eq:foc-b', 'label': 'eq:foc-b', 'parent_label': 'prop:interior-foc'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': "0 = m(\\bar e)\\frac{d\\bar e}{db'}\n  +\\beta \\E[V^\\star_b(k',b',z')\\mid z].", 'givens': [], 'assumptions': [], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': "0 = m(\\bar e)\\frac{d\\bar e}{db'}\n  +\\beta \\E[V^\\star_b(k',b',z')\\mid z]."}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |

## Gaps And Proposals

### eq:risky-pricing

- Proposal: `derivation_proposal_derivation_gap_eq_risky_pricing_missing_assumptions_1`
  - Location: `risky-debt-maliar-deep-learning-lecture-note.tex > prop:risky-pricing > eq:risky-pricing > line 399`
  - Problem: The derivation route is blocked by missing route-required assumptions. Missing assumption gaps: 1.
  - Why: The route uses operations whose domain, shape, regularity, probability, or economic assumptions must be stated before the derivation is well posed.
  - Proposed fix: Add or verify the linked route-required assumptions, then rerun the deterministic derivation route.
  - Validation: `blocked_by_missing_assumptions`; The proposal names route-required assumptions but does not prove the target.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `assumption_rule:conditional_expectation_integrability`, `counterexample_search:not_encodable`

  - Derivation route:
    - State route assumptions: Apply the linked assumption proposals before treating the derivation as well posed.
    - Rerun deterministic route: Call derive_or_refute with the proposed assumptions as explicit assumptions, not free-form givens.
    - Accept only backend closure: Promote the derivation only if a backend certificate or concrete counterexample is returned.

  - Backend plan:
    - assumptions_required: Recover route-required assumptions before retrying deterministic derivation. Expected artifact: `assumption_gap_proposals`.
    - derive_or_refute: Rerun the scoped derivation after assumptions are explicitly supplied. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

  - Linked assumption repairs:
    - Proposal: `assumption_proposal_assumption_gap_eq_risky_pricing_1_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable`
      - Proposed assumption: Assume the conditional law of next-period shocks is defined given the current state and that every random payoff term inside the conditional expectation is integrable.
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - The displayed equation contains a conditional expectation, so the expression is not a real-valued equation until a conditional law for the next-period shock is fixed.
        - The random variables inside the expectation include recovery, default indicators, promised payoffs, or value derivatives; these must be measurable and integrable.
        - Without these conditions the expectation may be undefined or infinite, so the zero-profit or FOC equation cannot be used as an equality of finite quantities.
      - Possible sufficient assumption sets:
        - `minimal_probability_integrability` (minimal route condition): Makes the conditional expectation in the pricing or FOC expression well defined.
          - A conditional probability law for next-period shocks \(z'\) given current \(z\) is fixed.
          - The payoff terms inside the conditional expectation are measurable with respect to that law.
          - The recovery and promised-payoff terms have finite conditional first moments.
        - `finite_state_sufficient_condition` (strong sufficient condition): Turns the conditional expectation into a finite weighted sum, avoiding measure-theoretic integrability questions.
          - The shock process has finite support conditional on each current \(z\).
          - Recovery, default, value-derivative, and payoff terms are finite at every next-period shock node.
        - `dominated_continuous_sufficient_condition` (continuous-state sufficient condition): Supports existence of the conditional expectation, and when paired with smoothness can support differentiating expected continuation values.
          - The conditional transition kernel exists and is fixed at the current state.
          - The random payoff or value-derivative expression is dominated by an integrable envelope.
      - How the derivation works under the assumptions:
        - Define the conditional law: Fix the transition kernel or conditional distribution for \(z'\) given the current state \(z\).
        - Check payoff measurability and integrability: Verify the default indicator, recovery payoff, promised payoff, or value derivative terms are measurable and have finite conditional expectation.
        - Rewrite expectation as a well-defined operator: Treat \(\E[\cdot\mid z]\) as an integral or finite weighted sum over \(z'\).
        - Use the displayed equation: Only after the expectation is finite does the pricing or FOC residual define a valid scalar equality.

### eq:foc-k

- Proposal: `derivation_proposal_derivation_gap_eq_foc_k_missing_assumptions_1`
  - Location: `risky-debt-maliar-deep-learning-lecture-note.tex > prop:interior-foc > eq:foc-k > line 776`
  - Problem: The derivation route is blocked by missing route-required assumptions. Missing assumption gaps: 3.
  - Why: The route uses operations whose domain, shape, regularity, probability, or economic assumptions must be stated before the derivation is well posed.
  - Proposed fix: Add or verify the linked route-required assumptions, then rerun the deterministic derivation route.
  - Validation: `blocked_by_missing_assumptions`; The proposal names route-required assumptions but does not prove the target.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `assumption_rule:conditional_expectation_integrability`, `assumption_rule:foc_expectation_differentiation`, `assumption_rule:differentiability`, `counterexample_search:not_encodable`

  - Derivation route:
    - State route assumptions: Apply the linked assumption proposals before treating the derivation as well posed.
    - Rerun deterministic route: Call derive_or_refute with the proposed assumptions as explicit assumptions, not free-form givens.
    - Accept only backend closure: Promote the derivation only if a backend certificate or concrete counterexample is returned.

  - Backend plan:
    - assumptions_required: Recover route-required assumptions before retrying deterministic derivation. Expected artifact: `assumption_gap_proposals`.
    - derive_or_refute: Rerun the scoped derivation after assumptions are explicitly supplied. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

  - Linked assumption repairs:
    - Proposal: `assumption_proposal_assumption_gap_eq_foc_k_1_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable`
      - Proposed assumption: Assume the conditional law of \(z'\mid z\) is defined and independent of the choice being differentiated; assume \(V^\star(k',b',z')\) is differentiable in \(k'\) and \(b'\) on the interior continuation region; assume \(V^\star_k\) and \(V^\star_b\) are conditionally integrable or dominated so differentiation can pass through \(\E[\cdot\mid z]\).
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - Mathematically missing: a conditional law \(Q(dz'\mid z)\) for the continuation shock.
        - Mathematically missing: differentiability of \(V^\star(k',b',z')\) in \(k'\) and \(b'\) on the smooth interior continuation region.
        - Mathematically missing: conditional integrability or domination of \(V^\star_k(k',b',z')\) and \(V^\star_b(k',b',z')\).
        - Mathematically missing: choice-independence of \(Q(dz'\mid z)\), or else the derivative of the expectation includes transition-kernel derivative terms.
        - Why missing: the proof says the derivative of the continuation term is the expected derivative, but that is an interchange-of-derivative-and-expectation step, not a formal consequence of differentiability alone.
      - Possible sufficient assumption sets:
        - `finite_state_interior_foc` (simple sufficient condition): The derivative of the finite expected continuation value is the finite expected derivative.
          - The conditional law \(P(z'\mid z)\) has finite support and does not depend on \(k'\) or \(b'\).
          - For every support point, \(V^\star(\cdot,\cdot,z')\) is differentiable at \((k',b')\) in the continuation region.
          - The finite sums of \(V^\star_k(k',b',z')\) and \(V^\star_b(k',b',z')\) are well defined.
          - The action \((k',b')\) is interior and the cash-flow/risky-rate functions are differentiable along the stated route.
        - `dominated_interchange_interior_foc` (continuous-state sufficient condition): Dominated convergence or a Leibniz rule justifies moving the derivative through \(\E[\cdot\mid z]\).
          - A conditional kernel \(Q(dz'\mid z)\) is specified and is independent of \(k'\) and \(b'\).
          - There are integrable envelopes dominating local derivatives of \(V^\star(k',b',z')\) with respect to \(k'\) and \(b'\).
          - The current state is a smooth continuation state, the action is interior, and the proof is away from default/borrowing kinks.
          - The current cash-flow term \(e(k,k',b,b',z;\widetilde r)\) and \(\widetilde r(z,k',b')\) are differentiable in the choice variables.
      - How the derivation works under the assumptions:
        - Start from smooth interior objective: For fixed current state, define \(F(k',b')=e(k,k',b,b',z;\widetilde r)+\eta(e(k,k',b,b',z;\widetilde r))+\beta\E[V^\star(k',b',z')\mid z]\).
        - Differentiate current cash flow: By the chain rule, \(\partial(e+\eta(e))/\partial x=(1+\eta'(e))\,d\bar e/dx=m(\bar e)d\bar e/dx\) for \(x\in\{k',b'\}\).
        - Interchange derivative and expectation: Under a choice-independent transition law \(Q(dz'\mid z)\) and integrability/domination, \(\partial_x\E[V^\star(k',b',z')\mid z]=\E[V^\star_x(k',b',z')\mid z]\).
        - Exclude omitted kernel terms: If \(Q\) depended on \(x\), a term like \(\int V^\star(k',b',z')\,\partial_x Q(dz'\mid z)\) would appear; the assumption rules this out.
        - Apply interior optimality: Set \(\partial F/\partial k'=0\) and \(\partial F/\partial b'=0\), giving the two Euler FOC equations.
    - Proposal: `assumption_proposal_assumption_gap_eq_foc_k_2_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present`
      - Proposed assumption: Assume the transition law for \(z'\) conditional on \(z\) is independent of the choice being differentiated, the continuation value derivatives are integrable, and differentiation may be interchanged with the conditional expectation.
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - Mathematically missing: a conditional law \(Q(dz'\mid z)\) for the continuation shock.
        - Mathematically missing: differentiability of \(V^\star(k',b',z')\) in \(k'\) and \(b'\) on the smooth interior continuation region.
        - Mathematically missing: conditional integrability or domination of \(V^\star_k(k',b',z')\) and \(V^\star_b(k',b',z')\).
        - Mathematically missing: choice-independence of \(Q(dz'\mid z)\), or else the derivative of the expectation includes transition-kernel derivative terms.
        - Why missing: the proof says the derivative of the continuation term is the expected derivative, but that is an interchange-of-derivative-and-expectation step, not a formal consequence of differentiability alone.
      - Possible sufficient assumption sets:
        - `choice_independent_transition_kernel` (standard dynamic-programming route): Allows \(\partial/\partial k'\) and \(\partial/\partial b'\) to pass through the conditional expectation without transition-kernel derivative terms.
          - The conditional law of \(z'\) depends on current \(z\), not directly on the choice \(k'\) or \(b'\).
          - The continuation value \(V^\star(k',b',z')\) is differentiable in \(k'\) and \(b'\) on the interior continuation region.
          - The derivatives \(V^\star_k(k',b',z')\) and \(V^\star_b(k',b',z')\) are conditionally integrable.
        - `dominated_differentiation_route` (continuous-state sufficient condition): Justifies the Euler FOC step by a dominated-convergence or Leibniz-rule argument.
          - There is an integrable envelope dominating the local derivatives of the continuation value.
          - The current action is interior and away from default and borrowing kinks.
          - The risky-rate function and cash-flow function are differentiable along the chosen interior route.
      - How the derivation works under the assumptions:
        - Start from smooth interior objective: For fixed current state, define \(F(k',b')=e(k,k',b,b',z;\widetilde r)+\eta(e(k,k',b,b',z;\widetilde r))+\beta\E[V^\star(k',b',z')\mid z]\).
        - Differentiate current cash flow: By the chain rule, \(\partial(e+\eta(e))/\partial x=(1+\eta'(e))\,d\bar e/dx=m(\bar e)d\bar e/dx\) for \(x\in\{k',b'\}\).
        - Interchange derivative and expectation: Under a choice-independent transition law \(Q(dz'\mid z)\) and integrability/domination, \(\partial_x\E[V^\star(k',b',z')\mid z]=\E[V^\star_x(k',b',z')\mid z]\).
        - Exclude omitted kernel terms: If \(Q\) depended on \(x\), a term like \(\int V^\star(k',b',z')\,\partial_x Q(dz'\mid z)\) would appear; the assumption rules this out.
        - Apply interior optimality: Set \(\partial F/\partial k'=0\) and \(\partial F/\partial b'=0\), giving the two Euler FOC equations.
    - Proposal: `assumption_proposal_assumption_gap_eq_foc_k_3_target_function_is_differentiable_on_the_stated_domain`
      - Proposed assumption: Assume the target function is differentiable on the stated domain.
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - The target uses notation whose route rule requires this assumption before the expression is well posed.
      - Possible sufficient assumption sets:
        - `route_rule_assumption` (route condition): States the deterministic route condition detected by the assumption rule.
          - Assume the target function is differentiable on the stated domain.
      - How the derivation works under the assumptions:
        - State route assumption: Add or verify the detected assumption before applying the derivation step.

### eq:foc-b

- Proposal: `derivation_proposal_derivation_gap_eq_foc_b_missing_assumptions_1`
  - Location: `risky-debt-maliar-deep-learning-lecture-note.tex > prop:interior-foc > eq:foc-b > line 781`
  - Problem: The derivation route is blocked by missing route-required assumptions. Missing assumption gaps: 3.
  - Why: The route uses operations whose domain, shape, regularity, probability, or economic assumptions must be stated before the derivation is well posed.
  - Proposed fix: Add or verify the linked route-required assumptions, then rerun the deterministic derivation route.
  - Validation: `blocked_by_missing_assumptions`; The proposal names route-required assumptions but does not prove the target.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `assumption_rule:conditional_expectation_integrability`, `assumption_rule:foc_expectation_differentiation`, `assumption_rule:differentiability`, `counterexample_search:not_encodable`

  - Derivation route:
    - State route assumptions: Apply the linked assumption proposals before treating the derivation as well posed.
    - Rerun deterministic route: Call derive_or_refute with the proposed assumptions as explicit assumptions, not free-form givens.
    - Accept only backend closure: Promote the derivation only if a backend certificate or concrete counterexample is returned.

  - Backend plan:
    - assumptions_required: Recover route-required assumptions before retrying deterministic derivation. Expected artifact: `assumption_gap_proposals`.
    - derive_or_refute: Rerun the scoped derivation after assumptions are explicitly supplied. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

  - Linked assumption repairs:
    - Proposal: `assumption_proposal_assumption_gap_eq_foc_b_1_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable`
      - Proposed assumption: Assume the conditional law of \(z'\mid z\) is defined and independent of the choice being differentiated; assume \(V^\star(k',b',z')\) is differentiable in \(k'\) and \(b'\) on the interior continuation region; assume \(V^\star_k\) and \(V^\star_b\) are conditionally integrable or dominated so differentiation can pass through \(\E[\cdot\mid z]\).
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - Mathematically missing: a conditional law \(Q(dz'\mid z)\) for the continuation shock.
        - Mathematically missing: differentiability of \(V^\star(k',b',z')\) in \(k'\) and \(b'\) on the smooth interior continuation region.
        - Mathematically missing: conditional integrability or domination of \(V^\star_k(k',b',z')\) and \(V^\star_b(k',b',z')\).
        - Mathematically missing: choice-independence of \(Q(dz'\mid z)\), or else the derivative of the expectation includes transition-kernel derivative terms.
        - Why missing: the proof says the derivative of the continuation term is the expected derivative, but that is an interchange-of-derivative-and-expectation step, not a formal consequence of differentiability alone.
      - Possible sufficient assumption sets:
        - `finite_state_interior_foc` (simple sufficient condition): The derivative of the finite expected continuation value is the finite expected derivative.
          - The conditional law \(P(z'\mid z)\) has finite support and does not depend on \(k'\) or \(b'\).
          - For every support point, \(V^\star(\cdot,\cdot,z')\) is differentiable at \((k',b')\) in the continuation region.
          - The finite sums of \(V^\star_k(k',b',z')\) and \(V^\star_b(k',b',z')\) are well defined.
          - The action \((k',b')\) is interior and the cash-flow/risky-rate functions are differentiable along the stated route.
        - `dominated_interchange_interior_foc` (continuous-state sufficient condition): Dominated convergence or a Leibniz rule justifies moving the derivative through \(\E[\cdot\mid z]\).
          - A conditional kernel \(Q(dz'\mid z)\) is specified and is independent of \(k'\) and \(b'\).
          - There are integrable envelopes dominating local derivatives of \(V^\star(k',b',z')\) with respect to \(k'\) and \(b'\).
          - The current state is a smooth continuation state, the action is interior, and the proof is away from default/borrowing kinks.
          - The current cash-flow term \(e(k,k',b,b',z;\widetilde r)\) and \(\widetilde r(z,k',b')\) are differentiable in the choice variables.
      - How the derivation works under the assumptions:
        - Start from smooth interior objective: For fixed current state, define \(F(k',b')=e(k,k',b,b',z;\widetilde r)+\eta(e(k,k',b,b',z;\widetilde r))+\beta\E[V^\star(k',b',z')\mid z]\).
        - Differentiate current cash flow: By the chain rule, \(\partial(e+\eta(e))/\partial x=(1+\eta'(e))\,d\bar e/dx=m(\bar e)d\bar e/dx\) for \(x\in\{k',b'\}\).
        - Interchange derivative and expectation: Under a choice-independent transition law \(Q(dz'\mid z)\) and integrability/domination, \(\partial_x\E[V^\star(k',b',z')\mid z]=\E[V^\star_x(k',b',z')\mid z]\).
        - Exclude omitted kernel terms: If \(Q\) depended on \(x\), a term like \(\int V^\star(k',b',z')\,\partial_x Q(dz'\mid z)\) would appear; the assumption rules this out.
        - Apply interior optimality: Set \(\partial F/\partial k'=0\) and \(\partial F/\partial b'=0\), giving the two Euler FOC equations.
    - Proposal: `assumption_proposal_assumption_gap_eq_foc_b_2_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present`
      - Proposed assumption: Assume the transition law for \(z'\) conditional on \(z\) is independent of the choice being differentiated, the continuation value derivatives are integrable, and differentiation may be interchanged with the conditional expectation.
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - Mathematically missing: a conditional law \(Q(dz'\mid z)\) for the continuation shock.
        - Mathematically missing: differentiability of \(V^\star(k',b',z')\) in \(k'\) and \(b'\) on the smooth interior continuation region.
        - Mathematically missing: conditional integrability or domination of \(V^\star_k(k',b',z')\) and \(V^\star_b(k',b',z')\).
        - Mathematically missing: choice-independence of \(Q(dz'\mid z)\), or else the derivative of the expectation includes transition-kernel derivative terms.
        - Why missing: the proof says the derivative of the continuation term is the expected derivative, but that is an interchange-of-derivative-and-expectation step, not a formal consequence of differentiability alone.
      - Possible sufficient assumption sets:
        - `choice_independent_transition_kernel` (standard dynamic-programming route): Allows \(\partial/\partial k'\) and \(\partial/\partial b'\) to pass through the conditional expectation without transition-kernel derivative terms.
          - The conditional law of \(z'\) depends on current \(z\), not directly on the choice \(k'\) or \(b'\).
          - The continuation value \(V^\star(k',b',z')\) is differentiable in \(k'\) and \(b'\) on the interior continuation region.
          - The derivatives \(V^\star_k(k',b',z')\) and \(V^\star_b(k',b',z')\) are conditionally integrable.
        - `dominated_differentiation_route` (continuous-state sufficient condition): Justifies the Euler FOC step by a dominated-convergence or Leibniz-rule argument.
          - There is an integrable envelope dominating the local derivatives of the continuation value.
          - The current action is interior and away from default and borrowing kinks.
          - The risky-rate function and cash-flow function are differentiable along the chosen interior route.
      - How the derivation works under the assumptions:
        - Start from smooth interior objective: For fixed current state, define \(F(k',b')=e(k,k',b,b',z;\widetilde r)+\eta(e(k,k',b,b',z;\widetilde r))+\beta\E[V^\star(k',b',z')\mid z]\).
        - Differentiate current cash flow: By the chain rule, \(\partial(e+\eta(e))/\partial x=(1+\eta'(e))\,d\bar e/dx=m(\bar e)d\bar e/dx\) for \(x\in\{k',b'\}\).
        - Interchange derivative and expectation: Under a choice-independent transition law \(Q(dz'\mid z)\) and integrability/domination, \(\partial_x\E[V^\star(k',b',z')\mid z]=\E[V^\star_x(k',b',z')\mid z]\).
        - Exclude omitted kernel terms: If \(Q\) depended on \(x\), a term like \(\int V^\star(k',b',z')\,\partial_x Q(dz'\mid z)\) would appear; the assumption rules this out.
        - Apply interior optimality: Set \(\partial F/\partial k'=0\) and \(\partial F/\partial b'=0\), giving the two Euler FOC equations.
    - Proposal: `assumption_proposal_assumption_gap_eq_foc_b_3_target_function_is_differentiable_on_the_stated_domain`
      - Proposed assumption: Assume the target function is differentiable on the stated domain.
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - The target uses notation whose route rule requires this assumption before the expression is well posed.
      - Possible sufficient assumption sets:
        - `route_rule_assumption` (route condition): States the deterministic route condition detected by the assumption rule.
          - Assume the target function is differentiable on the stated domain.
      - How the derivation works under the assumptions:
        - State route assumption: Add or verify the detected assumption before applying the derivation step.

## Non-Claims

- `derivation_audit_report_not_applied_or_certified`: The derivation audit report is diagnostic guidance only; it does not apply edits, prove full-document correctness, or certify proposed repairs unless a scoped backend certificate or concrete counterexample is explicitly recorded.
- `general_theorem_proving_not_claimed`: This scoped workflow result does not claim general theorem-proving ability.
- `givens_not_formal_assumptions`: givens not formal assumptions
- `release_readiness_not_claimed`: This scoped workflow result does not claim release readiness.
- `route_assumptions_not_global_minimality`: Route-required assumptions are not claimed to be globally minimal.
