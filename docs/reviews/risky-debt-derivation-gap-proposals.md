# Derivation Gap/Proposal Report

Question: Audit risky-debt derivations

Status: `proposal_ready`

## Coverage

- Targets inspected: 2
- Gaps: 2
- Proposals: 2
- Certifying proposals: 0

## Tool Uses

| Tool | Purpose | Status | Output | Arguments |
| --- | --- | --- | --- | --- |
| `build_index` | Extract LaTeX labels and source locations for derivation auditing. | `completed` | `latex_index` | `{'root': 'docs'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': "\\begin{proposition}[Zero-profit risky debt pricing]\n\\label{prop:risky-pricing}\nFor \\(b'>0\\), the zero-profit condition for the risky debt rate is\n\\begin{equation}\n  b'(1+r)\n  =\n  \\E\\left[\n    D(k',b',z')R(k',z')\n    +(1-D(k',b',z'))b'(1+\\widetilde r(z,k',b'))\n    \\mid z\n  \\right].\n  \\label{eq:risky-pricing}\n\\end{equation}\n\\end{proposition}", 'givens': [], 'assumptions': [], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': "\\begin{proposition}[Zero-profit risky debt pricing]\n\\label{prop:risky-pricing}\nFor \\(b'>0\\), the zero-profit condition for the risky debt rate is\n\\begin{equation}\n  b'(1+r)\n  =\n  \\E\\left[\n    D(k',b',z')R(k',z')\n    +(1-D(k',b',z'))b'(1+\\widetilde r(z,k',b'))\n    \\mid z\n  \\right].\n  \\label{eq:risky-pricing}\n\\end{equation}\n\\end{proposition}"}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |
| `derive_or_refute` | Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target. | `completed` | `derive_or_refute_result` | `{'target': "\\begin{proposition}[Interior first-order conditions]\n\\label{prop:interior-foc}\nSuppose the current state is a continuation state, the optimal action\n\\((k',b')\\) is interior, and the relevant functions are differentiable. Then the\noptimal policy satisfies\n\\begin{align}\n  0\n  &=\n  m(\\bar e)\\frac{d\\bar e}{dk'}\n  +\\beta \\E[V^\\star_k(k',b',z')\\mid z],\n  \\label{eq:foc-k}\\\\\n  0\n  &=\n  m(\\bar e)\\frac{d\\bar e}{db'}\n  +\\beta \\E[V^\\star_b(k',b',z')\\mid z].\n  \\label{eq:foc-b}\n\\end{align}\n\\end{proposition}", 'givens': [], 'assumptions': [], 'backend': 'auto'}` |
| `build_derivation_gaps` | Convert low-level derivation evidence into named gap records with proof/refutation boundaries. | `completed` | `derivation_gap_list` | `{'target': "\\begin{proposition}[Interior first-order conditions]\n\\label{prop:interior-foc}\nSuppose the current state is a continuation state, the optimal action\n\\((k',b')\\) is interior, and the relevant functions are differentiable. Then the\noptimal policy satisfies\n\\begin{align}\n  0\n  &=\n  m(\\bar e)\\frac{d\\bar e}{dk'}\n  +\\beta \\E[V^\\star_k(k',b',z')\\mid z],\n  \\label{eq:foc-k}\\\\\n  0\n  &=\n  m(\\bar e)\\frac{d\\bar e}{db'}\n  +\\beta \\E[V^\\star_b(k',b',z')\\mid z].\n  \\label{eq:foc-b}\n\\end{align}\n\\end{proposition}"}` |
| `build_derivation_proposals` | Create concrete derivation proposals linked to each gap. | `completed` | `derivation_proposal_list` | `{'gap_count': 'derived'}` |

## Gaps And Proposals

### prop:risky-pricing

- Proposal: `derivation_proposal_derivation_gap_prop_risky_pricing_missing_assumptions_1`
  - Location: `risky-debt-maliar-deep-learning-lecture-note.tex > prop:risky-pricing > line 395`
  - Problem: The derivation route is blocked by missing route-required assumptions. Missing assumption gaps: 2.
  - Why: The route uses operations whose domain, shape, regularity, probability, or economic assumptions must be stated before the derivation is well posed.
  - Proposed fix: Add or verify the linked route-required assumptions, then rerun the deterministic derivation route.
  - Validation: `blocked_by_missing_assumptions`; The proposal names route-required assumptions but does not prove the target.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `assumption_rule:conditional_expectation_integrability`, `assumption_rule:zero_profit_pricing_convention`, `counterexample_search:not_encodable`

  - Derivation route:
    - State route assumptions: Apply the linked assumption proposals before treating the derivation as well posed.
    - Rerun deterministic route: Call derive_or_refute with the proposed assumptions as explicit assumptions, not free-form givens.
    - Accept only backend closure: Promote the derivation only if a backend certificate or concrete counterexample is returned.

  - Backend plan:
    - assumptions_required: Recover route-required assumptions before retrying deterministic derivation. Expected artifact: `assumption_gap_proposals`.
    - derive_or_refute: Rerun the scoped derivation after assumptions are explicitly supplied. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

  - Linked assumption repairs:
    - Proposal: `assumption_proposal_assumption_gap_prop_risky_pricing_1_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable`
      - Proposed assumption: Assume a conditional transition law for \(z'\mid z\); assume \(D(k',b',z')R(k',z')\) and \((1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))\) are measurable and conditionally integrable; and assume the zero-profit pricing equation is evaluated for \(b'>0\).
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - Mathematically missing: a conditional probability law \(Q(dz'\mid z)\) or finite transition probabilities for \(z'\mid z\).
        - Mathematically missing: measurability and conditional integrability of \(D(k',b',z')R(k',z')\) and \((1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))\).
        - Mathematically missing: the economic valuation convention that the conditional expected risky payoff is set equal to \(b'(1+r)\) for \(b'>0\).
        - Why missing: the proof partitions default and solvent payoffs, but a payoff partition alone does not define the expectation operator or the zero-profit pricing measure.
      - Possible sufficient assumption sets:
        - `finite_state_risky_pricing` (simple sufficient condition): The right side becomes a finite weighted sum equal to the lender's required risk-free payoff.
          - The transition law \(P(z'\mid z)\) has finite support.
          - For every support point, \(D(k',b',z')\), \(R(k',z')\), and \(\widetilde r(z,k',b')\) are finite and measurable.
          - The payoff partition is exhaustive: default payoff is \(D R\), solvent payoff is \((1-D)b'(1+\widetilde r)\).
          - The pricing convention is risk-neutral zero profit with gross risk-free return \(1+r\) and \(b'>0\).
        - `kernel_integrability_risky_pricing` (general sufficient condition): The expected risky payoff is a finite scalar, so the zero-profit equality is well posed.
          - A conditional kernel \(Q(dz'\mid z)\) is specified.
          - The maps \(z'\mapsto D(k',b',z')R(k',z')\) and \(z'\mapsto (1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))\) are \(Q(\cdot\mid z)\)-measurable.
          - Both payoff terms have finite conditional first moments under \(Q(\cdot\mid z)\).
          - Debt is priced under the stated risk-neutral or pricing-measure convention.
      - How the derivation works under the assumptions:
        - Define payoff random variable: Let \(Y(z')=D(k',b',z')R(k',z')+(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))\).
        - Make conditional expectation well defined: Under \(Q(dz'\mid z)\) and integrability, \(\E[Y(z')\mid z]=\int Y(z')Q(dz'\mid z)\), or \(\sum_{z'}P(z'\mid z)Y(z')\) in finite state.
        - Apply zero-profit convention: Risk-neutral zero profit requires \(\E[Y(z')\mid z]=b'(1+r)\) for the positive promised debt position \(b'>0\).
        - Recover displayed pricing equation: Substitute \(Y(z')\) back into the equality to obtain the displayed risky-debt pricing condition.
    - Proposal: `assumption_proposal_assumption_gap_prop_risky_pricing_2_lender_pricing_uses_the_stated_zero_profit_risk_free_discounting_convention`
      - Proposed assumption: Assume lenders are risk-neutral or price under the stated pricing measure, the risk-free gross return is \(1+r\), and the promised debt payoff is priced by the zero-profit conditional expected payoff equation for positive debt.
      - Validation: `validated_by_rule`; Rule validation only checks that the proposed assumption matches a deterministic route requirement; it is not a proof certificate and does not prove global minimality.
      - Mathematical missing-assumption reasoning:
        - The pricing equation equates the lender's required risk-free payoff with an expected risky payoff.
        - That step is an economic pricing assumption: it requires risk-neutral valuation or an explicitly chosen pricing measure and payoff timing convention.
        - Without the convention, the same payoff expression could require risk premia, stochastic discount factors, or a different discounting normalization.
      - Possible sufficient assumption sets:
        - `risk_neutral_lender_measure` (economic pricing assumption): Justifies equating the required risk-free payoff \(b'(1+r)\) with the conditional expected lender payoff.
          - Lenders are risk-neutral or the expectation is taken under the pricing measure used for debt valuation.
          - The risk-free gross return over the period is \(1+r\).
          - Positive promised debt \(b'>0\) is the instrument being priced.
        - `discounted_zero_profit_equivalent` (equivalent convention): Justifies the zero-profit equation after moving the risk-free discount factor to the left side.
          - Debt price is normalized so that the date-\(t\) loan amount and date-\(t+1\) payoff are compared using the risk-free return.
          - Recovery and solvent promised payoff are the exhaustive lender payoff states.
      - How the derivation works under the assumptions:
        - State the lender valuation convention: Assume risk-neutral zero-profit pricing or specify the pricing measure.
        - Partition lender payoffs: Default payoff is recovery; solvent payoff is promised debt repayment.
        - Take conditional expected payoff: Compute the conditional expectation of those state-contingent payoffs under the stated pricing law.
        - Equate to risk-free required payoff: Set the expected risky payoff equal to \(b'(1+r)\) for positive promised debt.

### prop:interior-foc

- Proposal: `derivation_proposal_derivation_gap_prop_interior_foc_missing_assumptions_1`
  - Location: `risky-debt-maliar-deep-learning-lecture-note.tex > prop:interior-foc > line 770`
  - Problem: The derivation route is blocked by missing route-required assumptions. Missing assumption gaps: 2.
  - Why: The route uses operations whose domain, shape, regularity, probability, or economic assumptions must be stated before the derivation is well posed.
  - Proposed fix: Add or verify the linked route-required assumptions, then rerun the deterministic derivation route.
  - Validation: `blocked_by_missing_assumptions`; The proposal names route-required assumptions but does not prove the target.; Only certifying backend attempts or concrete counterexample artifacts can close a scoped derivation obligation. Diagnostic routes, missing assumption proposals, and formalization plans are not proof certificates.
  - Evidence refs: `derive_or_refute_result`, `route:human_review`, `backend_attempt:router:not_encodable`, `backend_attempt:sympy_finite_domain:not_encodable`, `assumption_rule:conditional_expectation_integrability`, `assumption_rule:foc_expectation_differentiation`, `counterexample_search:not_encodable`

  - Derivation route:
    - State route assumptions: Apply the linked assumption proposals before treating the derivation as well posed.
    - Rerun deterministic route: Call derive_or_refute with the proposed assumptions as explicit assumptions, not free-form givens.
    - Accept only backend closure: Promote the derivation only if a backend certificate or concrete counterexample is returned.

  - Backend plan:
    - assumptions_required: Recover route-required assumptions before retrying deterministic derivation. Expected artifact: `assumption_gap_proposals`.
    - derive_or_refute: Rerun the scoped derivation after assumptions are explicitly supplied. Expected artifact: `proof_certificate_or_counterexample_or_named_gap`.

  - Formalization target: `typed lhs/rhs`, `domains of each symbol`, `operator semantics`, `explicit assumptions used by backend route`

  - Linked assumption repairs:
    - Proposal: `assumption_proposal_assumption_gap_prop_interior_foc_1_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable`
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
    - Proposal: `assumption_proposal_assumption_gap_prop_interior_foc_2_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present`
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

## Non-Claims

- `derivation_audit_report_not_applied_or_certified`: The derivation audit report is diagnostic guidance only; it does not apply edits, prove full-document correctness, or certify proposed repairs unless a scoped backend certificate or concrete counterexample is explicitly recorded.
- `general_theorem_proving_not_claimed`: This scoped workflow result does not claim general theorem-proving ability.
- `givens_not_formal_assumptions`: givens not formal assumptions
- `release_readiness_not_claimed`: This scoped workflow result does not claim release readiness.
- `route_assumptions_not_global_minimality`: Route-required assumptions are not claimed to be globally minimal.
