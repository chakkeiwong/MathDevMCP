# Phase 03 Result: IFT Sign Adapter

Date: 2026-06-29

Status: `PASSED`

## Objective

Implement a bounded IFT sign-consistency adapter for `RLHL-01` that checks the
source theorem/proof sign relation against the declared adjoint convention and
reports the first sign inconsistency candidate with source anchors.

## Skeptical Audit

- Wrong baseline: the adapter evaluates only the `RLHL-01` source packets and
  Phase 02 IR route.
- Proxy metrics: the executable scalar probe, `pytest`, and benchmark status do
  not clear the source obligation.
- Stop conditions: missing source anchors, missing adjoint convention, or
  missing theorem/proof sign evidence would leave the case
  `human_review_required`.
- Hidden assumptions: the result is a local sign inconsistency candidate, not a
  resolved global contradiction or source-note invalidation.
- Artifact fit: the adapter result records source anchors, required terms,
  deterministic sign checks, clearance source, forbidden claims, and non-claims.

## Implemented Artifacts

Updated:

- `src/mathdevmcp/real_local_source_adapters.py`
- `tests/test_real_local_source_adapters.py`

New adapter function:

- `evaluate_ift_sign_adapter`

## Checks

Focused source-adapter tests:

```text
python3 -m pytest tests/test_real_local_source_adapters.py
```

Result: `9 passed`.

Pilot regression:

```text
python3 -m pytest tests/test_real_local_high_level_pilot.py
```

Result: `6 passed`.

IFT adapter smoke:

```text
python3 - <<'PY'
from mathdevmcp.real_local_source_adapters import evaluate_ift_sign_adapter
r=evaluate_ift_sign_adapter('.')
print(r['status'])
print(r['reason'])
print(r['checks'])
print(r['clearance'])
PY
```

Result summary:

```text
status: inconsistency_candidate
checks:
  theorem_negative_sign_present: True
  proof_positive_sign_present: True
  adjoint_negative_convention_present: True
  probe_not_used_for_clearance: True
clearance:
  adapter_required_cleared: True
  cleared_by: source_anchored_local_schema_check
```

Negative test:

- a reduced source range with the proof-final sign absent returns
  `human_review_required` and does not clear `adapter_required`.

## Claude Review

Claude read-only review:

```text
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name source-adapters-phase3-ift-review --model opus --effort high '...compact Phase 03 interpretation review...'
```

Verdict: `AGREE`.

Reviewer caution:

- keep the close-out wording as a local sign inconsistency candidate;
- do not claim the whole DSGE note is false, the HMC conclusion is invalid, or
  there is a broad resolved contradiction beyond the source-anchored local
  check.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. Adapter returns `inconsistency_candidate` with theorem sign, proof-final sign, adjoint convention evidence, source anchors, deterministic checks, clearance source, and non-claims. |
| Veto diagnostics | No Phase 03 veto fired. The result does not claim the whole source note is false, does not use the executable probe for clearance, and preserves source anchors. |
| Explanatory diagnostics | The bounded source packets contain a negative boxed theorem sign, a positive proof-final sign, and the negative adjoint convention. |
| Not concluded | HMC practical invalidity, solver correctness, global theorem falsehood, release readiness, scientific validation, public benchmark validity, or broad theorem proving. |

## Next Subplan Review

Phase 04 is ready. It must evaluate only `RLHL-04`, record linear Gaussian,
positive-definite, and mask/dense-panel assumptions, and must not claim
nonlinear filter exactness, score/Hessian validity, or implementation
correctness.
