local_answer:
  packet_type: diagnostic_only
  derivation_status: incomplete
  resolved_scope: small_scalar_observation_value_route_smoke_check
  partial_scope: scalar_derivative_route_local_expression
  unresolved_scope: full_covariance_matrix_calculus_step

evidence_used:
  - known_check: value-route smoke check passed for a small scalar observation case
  - partial_symbolic_fact: scalar derivative route has a local expression
  - open_obligation: full covariance matrix calculus step remains unresolved

assumptions_or_gaps:
  - scalar smoke check does not establish full derivation
  - scalar derivative expression is only local
  - covariance matrix calculus obligation remains open
  - no proof is authorized from the available checks

boundary_notes:
  - diagnostic packet only
  - not presented as proof
  - no claim of release readiness, benchmark validity, scientific validation, product capability, or general model reliability
