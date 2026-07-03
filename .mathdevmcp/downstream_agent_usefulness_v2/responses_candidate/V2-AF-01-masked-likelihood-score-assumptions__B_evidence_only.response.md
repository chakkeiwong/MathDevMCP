local_answer:
The score route cannot yet be treated as differentiating the same scalar likelihood as the value route. That equivalence requires an explicit route-link assumption: the "full covariance" derivative in the score route must reduce exactly to the observed-component covariance used by the masked value route.

evidence_used:
- The value route uses only observed components: selected innovations with logdet plus solve term.
- The score route is written for a full covariance object.
- The mask note says the observed-component mask aliases the selected covariance, but does not state the assumptions connecting the two routes.

assumptions_or_gaps:
- The score covariance must be exactly the masked or selected covariance used by the value route, not the unmasked full covariance.
- The same observed innovation vector, ordering, and mask must be used in both routes.
- The mask or selection operator must be parameter-independent; otherwise its derivative would also affect the score.
- Contributions from unobserved covariance blocks must be absent, constant, or explicitly projected out.
- The derivative must include the same dependencies as the value likelihood, including covariance and any innovation/residual dependence on parameters if applicable.
- The selected covariance must be differentiable and nonsingular/valid for the logdet and solve terms.

boundary_notes:
From the provided evidence alone, the equivalence is an unstated assumption, not an established fact. The mask alias note is not sufficient by itself to prove that the full-covariance score differentiates the masked scalar likelihood.
