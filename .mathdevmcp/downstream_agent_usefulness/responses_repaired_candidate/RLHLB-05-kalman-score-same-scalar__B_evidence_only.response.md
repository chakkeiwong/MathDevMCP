answer_or_decision

Evidence is insufficient to claim that the Kalman score matches the derivative of the same scalar likelihood used by the value route. The needed assumptions must be stated first.

reasoning_chain

For the score expression to be treated as differentiating the same scalar likelihood, the value route and score route must be linked to one fixed scalar objective. The score must be the derivative of that objective under valid differentiability and covariance-domain conditions, with the same masking and data-selection semantics. Without those assumptions, a local Kalman score expression may be structurally plausible but still not established as the gradient of the same scalar likelihood.

evidence_used

- Case status: `missing_assumptions`
- Evidence class: `missing_assumption`
- Bounded context: asks what assumptions are missing before treating the Kalman score as differentiating the same scalar likelihood used by the value route
- Expected work: identify same-scalar likelihood, differentiability, covariance-domain, masking, and route-linking assumptions
- Source family provenance: `BayesFilter`

assumptions_or_gaps

Needed assumptions:

1. Same-scalar likelihood assumption: the scalar likelihood used by the value route is explicitly identified, including sign convention, constants, normalization, observation sequence, parameters, and initial-state treatment.

2. Route-linking assumption: the Kalman score route is explicitly shown to differentiate that exact scalar, not merely a similar innovation likelihood or a locally equivalent-looking expression.

3. Differentiability assumption: all matrices and recursions used in the likelihood are differentiable with respect to the target parameters on the domain being considered.

4. Covariance-domain assumption: predicted and innovation covariance matrices remain in the valid domain needed for inverses, log determinants, and derivative interchange, typically requiring positive definiteness or an explicitly handled semidefinite case.

5. Masking assumption: missing-data masks, observation selection, time indexing, and any skipped observations are identical between value and score routes.

6. Parameter-sharing assumption: both routes use the same parameterization and transformation rules, including constrained-parameter maps if present.

7. Initialization assumption: initial mean, covariance, diffuse treatment, and any burn-in or conditioning conventions are identical between routes.

8. Numerical route assumption: any stabilizing implementation choices, such as Joseph-form covariance updates, square-root filters, jitter, symmetrization, or fallback branches, do not change the scalar being differentiated unless explicitly accounted for.

next_artifact_or_action

The next safe artifact is a route-linking derivation or contract showing the value likelihood expression and the Kalman score expression side by side, with masking, covariance-domain conditions, initialization, and parameterization stated explicitly.

what_would_change_conclusion

The conclusion would change if an artifact established that the score route is the derivative of the exact scalar likelihood computed by the value route, under stated differentiability, covariance, masking, and initialization assumptions.

forbidden_claims_avoided

Avoided: treating diagnostic or structural evidence as proof; making source-wide or codebase-wide claims; using reviewer or agent output as authority; making release, public benchmark, scientific validation, product capability, broad theorem-proving, or general reliability claims.

residual_risks

Even with the assumptions stated, implementation details such as numerical stabilization, masked observations, covariance regularization, or parameter transforms could still make the computed score differ from the derivative of the computed scalar unless checked by a focused route-equivalence artifact.
