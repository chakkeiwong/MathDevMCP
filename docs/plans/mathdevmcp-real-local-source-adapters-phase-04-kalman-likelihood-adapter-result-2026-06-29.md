# Phase 04 Result: Kalman Likelihood Adapter

Date: 2026-06-29

Status: `PASSED_WITH_SOURCE_PACKET_SCOPE_BLOCKER`

## Objective

Implement a bounded Kalman prediction-error likelihood adapter for `RLHL-04`
that checks chain-rule, Gaussian innovation, logdet/quadratic,
positive-definiteness, and mask/dense-panel assumption coverage from source
packets.

## Skeptical Audit

- Wrong baseline: evaluated only the frozen `RLHL-04` packet ranges.
- Proxy metrics: tests and assumption probes do not clear the source
  obligation.
- Stop conditions: missing SPD/positive-definite assumption in the bounded
  packet must prevent clearance.
- Hidden assumptions: the innovation regularity assumption exists nearby in
  BayesFilter, but outside the frozen `RLHL-04` source packet.
- Artifact fit: the adapter records required coverage and explicitly leaves
  clearance false when a required assumption is not packet-anchored.

## Implemented Artifacts

Updated:

- `src/mathdevmcp/real_local_source_adapters.py`
- `tests/test_real_local_source_adapters.py`

New adapter function:

- `evaluate_kalman_likelihood_adapter`

## Checks

Focused source-adapter tests:

```text
python3 -m pytest tests/test_real_local_source_adapters.py
```

Result: `12 passed`.

Pilot regression:

```text
python3 -m pytest tests/test_real_local_high_level_pilot.py
```

Result: `6 passed`.

Current frozen-packet smoke:

```text
python3 - <<'PY'
from mathdevmcp.real_local_source_adapters import evaluate_kalman_likelihood_adapter
r=evaluate_kalman_likelihood_adapter('.')
print(r['status'])
print(r['checks'])
print(r['clearance'])
PY
```

Result summary:

```text
status: human_review_required
positive_definite_or_spd_present: False
adapter_required_cleared: False
```

Synthetic extended-packet test:

- adding BayesFilter lines `32-39` for the innovation regularity assumption
  lets the adapter return `source_supported`;
- this confirms the adapter can clear only when the required assumption is
  source-anchored in the bounded packet.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Partially passed. The adapter checks chain rule, Gaussian predictive distribution, logdet/quadratic terms, mask/no-observation boundaries, and SPD assumption coverage. The frozen packet lacks the SPD assumption, so clearance is correctly withheld. |
| Veto diagnostics | The key Phase 04 veto fired in a controlled way: missing positive-definite source evidence prevents `adapter_required` clearance. No nonlinear-filter, score/Hessian, or implementation-correctness claim was made. |
| Explanatory diagnostics | The innovation regularity assumption exists nearby in `../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex` lines `32-39`, outside the frozen `RLHL-04` packet. |
| Not concluded | Source obligation clearance for `RLHL-04`, nonlinear filter exactness, score/Hessian validity, production implementation correctness, release readiness, public benchmark validity, or scientific validation. |

## Next Subplan Review

Phase 05 may proceed because the program allows partial/blocker outcomes rather
than forced residual clearance. The source-obligation scorer in Phase 08 must
preserve this `RLHL-04` residual gap unless a reviewed manifest extension adds
the innovation-regularity assumption packet.

Exact handoff:

- `RLHL-04` adapter implemented;
- frozen-packet result remains `human_review_required`;
- do not count `RLHL-04` as cleared under the frozen manifest;
- future reviewed repair may add BayesFilter lines `32-39` as an explicit
  assumption packet.
