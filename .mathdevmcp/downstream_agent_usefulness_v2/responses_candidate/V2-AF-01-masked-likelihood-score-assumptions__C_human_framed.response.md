## answer_or_abstention

Abstain from treating the score route as differentiating the same scalar likelihood as the value route on the given evidence alone. It can be linked only conditionally, after the route-link assumptions below are made explicit and verified.

## evidence_route

- The value route uses selected observed-component innovations with a logdet plus solve term.
- The score route is written as a derivative of a full covariance object.
- The mask aliases observed components, but the assumptions connecting the masked/selected value route to the full-covariance score route are unstated.
- Therefore the key issue is scalar-target identity: both routes must refer to the same masked likelihood, not merely related covariance objects.

## assumptions_gaps_or_domain_obligations

| Obligation | Required assumption |
|---|---|
| Same scalar target | The score expression must be the derivative of exactly the scalar likelihood computed by the value route, including the same observed components, constants convention, innovation vector, covariance, and parameter dependence. |
| Mask/selection consistency | The mask must define a fixed selection operator `S` such that selected innovations and covariance are `r_obs = S r` and `C_obs = S C S^T`, with identical ordering and dimensions in both routes. |
| No unobserved-component leakage | The score route must not include derivative contributions from unobserved covariance blocks unless the full expression algebraically reduces to the selected observed likelihood. |
| Covariance domain | The selected covariance `C_obs` must be symmetric positive definite, or otherwise both routes must use the same stated generalized inverse/logdet convention. |
| Differentiability | Innovations and covariance entries used by the selected likelihood must be differentiable in the relevant parameters on the domain being considered. |
| Mask independence | The observed-component mask must be parameter-independent, or any derivative through the mask/selection rule must be explicitly included in both routes. |
| Derivative commutation | The derivative of the selected covariance must satisfy `d(C_obs)/dtheta = S (dC/dtheta) S^T` under the stated mask. |
| Innovation consistency | If the score differentiates the quadratic solve term, it must include the same parameter dependence of selected innovations as the value route. |

## boundary_and_nonclaim_notes

This does not establish that the routes are equivalent. It only states the assumptions needed before such an equivalence claim could be audited.

No claim is made about release readiness, benchmark validity, scientific validation, product capability, or general model reliability.

Passing a local diagnostic would not by itself prove equivalence beyond the checked mask, parameter point, and covariance domain.

## next_artifact

Create an assumption ledger mapping:

1. value-route scalar likelihood,
2. score-route derivative expression,
3. mask/selection operator,
4. selected covariance domain,
5. differentiability conditions,
6. explicit proof or diagnostic that the score is the derivative of the same selected scalar likelihood.
