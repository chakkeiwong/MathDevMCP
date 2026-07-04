# Phase 06 Result: Affine Recursion Adapter

Date: 2026-06-29

Status: `PASSED`

## Objective

Implement a bounded affine-pricing recursion adapter for `RLHL-07` that checks
exponential-affine ansatz substitution, Gaussian MGF use, and coefficient
collection for `A_n` and `B_n` with vector/matrix caveats.

## Skeptical Audit

- Wrong baseline: evaluated only the frozen `RLHL-07` source packet and Phase
  02 IR route.
- Proxy metrics: the inconclusive executable probe, tests, and benchmark status
  do not clear the source obligation.
- Stop conditions: missing Gaussian MGF or coefficient equations would leave
  the case `human_review_required`.
- Hidden assumptions: source support is for the proposition's derivation
  structure, not empirical pricing validity or identification.
- Artifact fit: result records state transition, ansatz, expectation, Gaussian
  MGF, `A_n`/`B_n`, initial conditions, coefficient collection, source anchors,
  clearance source, and non-claims.

## Implemented Artifacts

Updated:

- `src/mathdevmcp/real_local_source_adapters.py`
- `tests/test_real_local_source_adapters.py`

New adapter function:

- `evaluate_affine_recursion_adapter`

## Checks

Focused source-adapter tests:

```text
python3 -m pytest tests/test_real_local_source_adapters.py
```

Result: `16 passed`.

Pilot regression:

```text
python3 -m pytest tests/test_real_local_high_level_pilot.py
```

Result: `6 passed`.

Affine adapter smoke:

```text
python3 - <<'PY'
from mathdevmcp.real_local_source_adapters import evaluate_affine_recursion_adapter
r=evaluate_affine_recursion_adapter('.')
print(r['status'])
print(r['checks'])
print(r['clearance'])
PY
```

Result summary:

```text
status: source_supported
state_transition_present: True
exponential_affine_ansatz_present: True
conditional_normality_present: True
gaussian_mgf_present: True
a_recursion_present: True
b_recursion_present: True
coefficient_collection_present: True
adapter_required_cleared: True
cleared_by: source_anchored_local_schema_check
```

Negative test:

- truncating the packet before the Gaussian MGF/coefficient collection returns
  `human_review_required` and does not clear `adapter_required`.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. Adapter returns `source_supported` with ansatz, Gaussian conditional normality/MGF, `A_n`, `B_n`, initial conditions, coefficient collection, source anchors, and non-claims. |
| Veto diagnostics | No Phase 06 veto fired. It does not claim empirical pricing validity, identification, or exactness of later non-affine approximations. |
| Explanatory diagnostics | The source packet contains the master recursion proposition and proof through coefficient collection. |
| Not concluded | Empirical validity, identification, later approximation correctness, release readiness, public benchmark validity, scientific validation, or broad theorem proving. |

## Next Subplan Review

Phase 07 is ready. It must evaluate only `RLHL-10`, require solve-form score
evidence and same-scalar boundary evidence, and must not claim HMC/posterior
validity, sampler convergence, Hessian readiness, or backend correctness.
