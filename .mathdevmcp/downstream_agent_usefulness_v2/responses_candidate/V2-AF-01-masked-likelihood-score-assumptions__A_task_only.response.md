Local conclusion: abstain from linking the derivative route to the same scalar objective as the value route on the given context alone. The prompt says both routes use masked observations and only partially stated domain assumptions, but gives no equations or executable/source evidence.

Assumptions needed before the link is valid:

- The value route's scalar objective is explicitly defined, including mask semantics, weighting, normalization, constants, and reduction order.
- The derivative route is taken with respect to the same parameters, parameterization, constraints, and domain as the value route.
- The mask is identical across routes and does not introduce omitted terms, shape-dependent behavior, or different treatment of missing observations.
- Differentiation is valid on the stated domain: no unhandled discontinuities, boundary cases, invalid masked entries, or parameter regions where the objective is undefined.
- Any dropped constants or masked terms are derivative-zero under the same assumptions, not merely convenient omissions.
- The derivative route computes the derivative of the stated scalar objective, not of a surrogate, diagnostic, partial likelihood, or locally equivalent expression.
- If transformations, batching, aggregation, or conditioning are used, they preserve equality between the routed value objective and the derivative expression.

Gaps/non-claims:

- No claim that the routes are equivalent.
- No claim that diagnostics would prove equivalence beyond the checked cases.
- No claim of scientific validation, benchmark validity, release readiness, or general reliability.

Next concrete artifact: a masked-route equivalence note containing the exact scalar objective, mask definition, domain assumptions, derivative derivation in the same notation, and a targeted finite-difference or symbolic check showing the derivative route matches the value route's gradient under those stated assumptions.
