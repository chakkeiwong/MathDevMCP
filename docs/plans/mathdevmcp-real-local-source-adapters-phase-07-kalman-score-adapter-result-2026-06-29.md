# Phase 07 Result: Kalman Score Adapter

Date: 2026-06-29

Status: `PASSED`

## Objective

Implement a bounded Kalman solve-form score adapter for `RLHL-10` that checks
differentiation of logdet/quadratic terms, solve substitution `S_t w_t = v_t`,
and the same-scalar HMC gradient boundary.

## Skeptical Audit

- Wrong baseline: evaluated only the frozen `RLHL-10` source packets and Phase
  02 IR route.
- Proxy metrics: the assumptions-only executable probe, tests, and benchmark
  status do not clear the source obligation.
- Stop conditions: missing solve relation or missing same-scalar boundary would
  leave the case `human_review_required`.
- Hidden assumptions: same-scalar support is a necessary HMC-gradient boundary,
  not proof of posterior validity or sampler convergence.
- Artifact fit: result records derivative terms, solve-form score, source
  label, trace/factor-solve caveat, value-oracle boundary, same-scalar HMC
  boundary, source anchors, clearance source, and non-claims.

## Implemented Artifacts

Updated:

- `src/mathdevmcp/real_local_source_adapters.py`
- `tests/test_real_local_source_adapters.py`

New adapter function:

- `evaluate_kalman_score_adapter`

## Checks

Focused source-adapter tests:

```text
python3 -m pytest tests/test_real_local_source_adapters.py
```

Result: `18 passed`.

Pilot regression:

```text
python3 -m pytest tests/test_real_local_high_level_pilot.py
```

Result: `6 passed`.

Kalman score adapter smoke:

```text
python3 - <<'PY'
from mathdevmcp.real_local_source_adapters import evaluate_kalman_score_adapter
r=evaluate_kalman_score_adapter('.')
print(r['status'])
print(r['checks'])
print(r['clearance'])
PY
```

Result summary:

```text
status: source_supported
innovation_derivatives_present: True
inverse_derivative_rule_present: True
score_contribution_present: True
solve_relation_present: True
solve_score_present: True
source_label_present: True
value_oracle_present: True
same_scalar_boundary_present: True
prior_transform_boundary_present: True
adapter_required_cleared: True
cleared_by: source_anchored_local_schema_check
```

Negative test:

- removing the same-scalar packet returns `human_review_required` and does not
  clear `adapter_required`.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. Adapter returns `source_supported` with derivative terms, solve relation, solve-form score, source label, value-oracle/same-scalar boundary, source anchors, and non-claims. |
| Veto diagnostics | No Phase 07 veto fired. It does not claim HMC validity, posterior correctness, sampler convergence, Hessian readiness, or backend correctness. |
| Explanatory diagnostics | The score packet and same-scalar packet together provide the required source anchors. |
| Not concluded | HMC validity, posterior correctness, sampler convergence, Hessian readiness, backend correctness, release readiness, public benchmark validity, scientific validation, or broad theorem proving. |

## Next Subplan Review

Phase 08 is ready. It must integrate adapter results into separate ledgers and
must preserve the `RLHL-04` residual gap unless a reviewed manifest extension is
approved. It must not emit a blended accuracy metric or add local results to the
benchmark gate.
