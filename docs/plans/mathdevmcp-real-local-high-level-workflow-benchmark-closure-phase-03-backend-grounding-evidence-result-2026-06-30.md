# Phase 3 Result: Backend Grounding Evidence Layer

Date: 2026-06-30

Status: `PASSED`

## Objective

Ensure every frozen real-local high-level benchmark case has an explicit route
to source adapters, symbolic checks, counterexample search, code/equation
comparison, review packets, or justified abstention before the Phase 4 baseline
run.

## Skeptical Audit

- Wrong baseline checked: Phase 3 uses the Phase 2 frozen manifest and does not
  run workflows as performance evidence.
- Proxy metric checked: route counts and packet-stub counts are feasibility
  diagnostics, not benchmark quality or pass rate.
- Stop conditions checked: route building must stop on invalid manifest,
  missing packet fields, or silent Phase 2 rubric drift.
- Hidden assumptions checked: Lean availability is route availability only and
  not proof without explicit proof source.
- Artifact fit checked: route ledger plus packet stubs answer Phase 3; a
  benchmark result would be premature.
- Environment mismatch checked: no package install, network fetch, GPU action,
  sibling-repo edit, source edit, release policy change, or benchmark promotion
  was used.

Audit result: `PASSED`.

## Artifacts Written Or Updated

```text
src/mathdevmcp/real_local_high_level_benchmark.py
tests/test_real_local_high_level_benchmark.py
docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-04-current-workflow-baseline-run-subplan-2026-06-30.md
```

Saved reports:

```text
.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase03_route_availability.json
.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase03_focused_pytest.txt
```

## Route Ledger Summary

```text
status: consistent
case_total: 9
packet_stub_total: 9
source_adapter_present: 5
source_adapter_absent: 0
source_adapter_not_applicable: 4
symbolic_backend_available: true
aggregate_accuracy: null
```

Per-case route states:

| Case | Source Adapter | Symbolic Route | Formal Route | Code Route | Residuals |
| --- | --- | --- | --- | --- | --- |
| `RLHLB-01-ift-sign-gap` | present: `ift_sign_consistency` | available | not applicable | not applicable | negative-control boundary |
| `RLHLB-02-kalman-loglik-assumptions` | present: `kalman_prediction_error_loglik` | not applicable | not applicable | not applicable | none |
| `RLHLB-03-joseph-equivalence` | present: `joseph_covariance_equivalence` | available | Lean available, explicit source required | not applicable | none |
| `RLHLB-04-affine-pricing-recursion` | present: `affine_pricing_master_recursion` | available | not applicable | not applicable | none |
| `RLHLB-05-kalman-score-same-scalar` | present: `kalman_score_same_scalar` | not applicable | not applicable | not applicable | none |
| `RLHLB-06-state-space-code-missing-solve` | not applicable | not applicable | not applicable | available | negative-control boundary |
| `RLHLB-07-proof-boundary-review-packet` | not applicable | not applicable | not applicable | not applicable | negative-control boundary; packet not certificate |
| `RLHLB-08-hmc-value-only-boundary` | not applicable | available | Lean available, explicit source required | not applicable | negative-control boundary |
| `RLHLB-09-affine-recovery-assumption-limit` | not applicable | available | not applicable | not applicable | negative-control boundary |

## Packet-Stub Assessment

All nine packet stubs include the Phase 2 required fields:

```text
question
source_anchors
assumptions
route_availability
derivation_proof_steps
backend_checks
counterexamples
gaps
actions
evidence_classes
non_claims
```

Packet stubs explicitly state that Phase 3 route availability is not proof,
refutation, benchmark pass, release-readiness evidence, or scientific
validation. Forbidden claims are represented as `Forbidden claim not made: ...`
statements rather than bare claim text.

## Required Checks

Route report:

```text
python3 -m mathdevmcp.cli real-local-high-level-routes --root .
```

Result:

```text
consistent
case_total: 9
packet_stub_total: 9
source_adapter_present: 5
source_adapter_not_applicable: 4
source_adapter_absent: 0
aggregate_accuracy: null
```

Focused pytest:

```text
python3 -m pytest tests/test_real_local_high_level_benchmark.py tests/test_high_level_contracts.py tests/test_high_level_workflows.py tests/test_prove_or_counterexample.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py -q
```

Result:

```text
49 passed
```

## Claude Review

Phase 3 Claude R1 verdict: `AGREE`.

Findings:

- no sequencing blocker because Phase 3 remains pre-baseline;
- boundary is intact because workflows are not run as correctness evidence;
- carry-forward caution: Phase 4 must keep the manifest/rubric frozen and
  preserve Lean as route availability only unless explicit proof/source
  artifacts are supplied.

Patch applied:

- Phase 4 subplan now explicitly validates manifest/rubric and route ledger
  stability before baseline and treats Lean availability without explicit proof
  source as a veto.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. All nine cases have route ledger rows, all packet stubs satisfy the Phase 2 schema, and route states preserve evidence boundaries. |
| Veto diagnostics | Backend absence is not refutation; structural and review-packet evidence remain diagnostic; Lean availability is not proof; no Phase 2 manifest/rubric drift occurred. |
| Explanatory diagnostics | Route-count summary, per-case route table, packet-stub schema check, focused tests, Claude review. |
| Not concluded | Actual benchmark pass rate, proof of real-local claims, repair success, public benchmark validity, release readiness, scientific validation, production correctness, full LaTeX proof checking, or broad theorem proving. |

## Next-Phase Review

Phase 4 subplan remains consistent and feasible after Phase 3:

- it is the first phase that runs current workflows on the frozen benchmark;
- it must verify Phase 2/3 artifacts remain unchanged before and after rerun;
- it must preserve predeclared negative-control semantics;
- it must keep aggregate metrics diagnostic only;
- it must not treat Lean availability as proof without explicit proof source.

## Handoff

Proceed to Phase 4 current workflow baseline run.
