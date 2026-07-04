# Phase 02 Result: Math IR And Notation Normalization

Date: 2026-06-29

Status: `PASSED`

## Objective

Convert validated source packets into normalized obligation records containing
case id, question, source anchors, detected domain family, required terms,
assumptions, adapter route hints, and explicit source/probe/residual channel
separation.

## Skeptical Audit

- Wrong baseline: IR is built only from the Phase 01 packet report and frozen
  pilot manifest.
- Proxy metrics: IR records do not clear `adapter_required`, and tests/CLI/probe
  outcomes cannot clear the residual adapter channel.
- Stop conditions: missing packet validation, missing route requirements, or
  channel blending would block adapter phases.
- Hidden assumptions: required-term coverage is diagnostic pre-adapter routing
  context only.
- Artifact fit: IR records include adapter route, source anchors, required
  terms, assumptions, probe channel, residual adapter channel, clearance
  requirements, and non-claims.

## Implemented Artifacts

Updated:

- `src/mathdevmcp/real_local_source_adapters.py`
- `tests/test_real_local_source_adapters.py`

New IR report contract:

- `real_local_source_obligation_ir_report`

Adapter routes:

- `RLHL-01-ift-gradient-bias-sign`: `ift_sign_consistency`
- `RLHL-04-kalman-prediction-error-loglik`: `kalman_prediction_error_loglik`
- `RLHL-06-joseph-covariance-equivalence`: `joseph_covariance_equivalence`
- `RLHL-07-affine-pricing-master-recursion`: `affine_pricing_master_recursion`
- `RLHL-10-kalman-score-same-scalar-contract`: `kalman_score_same_scalar`

## Checks

Focused tests:

```text
python3 -m pytest tests/test_real_local_source_adapters.py
```

Result: `7 passed`.

Pilot regression:

```text
python3 -m pytest tests/test_real_local_high_level_pilot.py
```

Result: `6 passed`.

IR smoke:

```text
python3 - <<'PY'
from mathdevmcp.real_local_source_adapters import build_source_obligation_ir
r=build_source_obligation_ir('.')
print(r['status'])
print(r['summary'])
for item in r['obligations']:
    print(item['case_id'], item['adapter_route'], item['pre_adapter_status'], item['probe_channel']['may_clear_adapter_required'], item['residual_adapter_channel']['may_clear_from_probe_or_tests'])
PY
```

Result:

```text
consistent
{'case_total': 5, 'obligation_total': 5, 'pre_adapter_required': 5, 'aggregate_accuracy': None}
RLHL-01-ift-gradient-bias-sign ift_sign_consistency adapter_required False False
RLHL-04-kalman-prediction-error-loglik kalman_prediction_error_loglik adapter_required False False
RLHL-06-joseph-covariance-equivalence joseph_covariance_equivalence adapter_required False False
RLHL-07-affine-pricing-master-recursion affine_pricing_master_recursion adapter_required False False
RLHL-10-kalman-score-same-scalar-contract kalman_score_same_scalar adapter_required False False
```

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. Five obligations are produced with expected route ids, source anchors, required terms, assumptions, forbidden claims, explicit clearance requirements, and separate source/probe/residual channels. |
| Veto diagnostics | No Phase 02 veto fired. IR emits no supported/refuted source status, does not hide assumptions, and cannot clear adapters from probes/tests. |
| Explanatory diagnostics | Missing required terms remain diagnostic-only pre-adapter context, confirmed by a focused negative test. |
| Not concluded | Adapter success, theorem proof, source correctness, release readiness, or public benchmark validity. |

## Next Subplan Review

Phase 03 is ready. It may evaluate only `RLHL-01` through the IFT sign adapter,
must preserve source anchors, and must report any inconsistency as a local
source-linked inconsistency candidate rather than a global source-note failure.
