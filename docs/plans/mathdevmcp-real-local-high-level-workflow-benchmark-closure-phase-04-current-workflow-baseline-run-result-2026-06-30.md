# Phase 4 Result: Current Workflow Baseline Run

Date: 2026-06-30

Status: `PASSED`

## Objective

Run the current high-level workflows on the frozen real-local benchmark before
targeted repairs, preserving an honest failure table.

## Skeptical Audit

- Wrong baseline checked: this is the current workflow baseline, not a repaired
  run or seeded benchmark replay.
- Proxy metric checked: aggregate accuracy remains `null`; counts are
  diagnostic only.
- Stop conditions checked: invalid Phase 2 manifest or Phase 3 route ledger
  stops the baseline.
- Hidden assumptions checked: Lean availability is route availability only and
  not proof without explicit source.
- Artifact fit checked: every result includes a route reference, packet summary,
  boundary checks, expected-status family, and failure class.
- Environment mismatch checked: no package install, network fetch, GPU action,
  sibling-repo edit, source edit, release policy change, or benchmark promotion
  was used.

Audit result: `PASSED`.

## Artifacts Written Or Updated

```text
src/mathdevmcp/real_local_high_level_benchmark.py
tests/test_real_local_high_level_benchmark.py
docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-05-targeted-capability-repairs-subplan-2026-06-30.md
```

Saved reports:

```text
.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase04_baseline.json
.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase04_focused_pytest.txt
```

## Baseline Summary

```text
status: completed
case_total: 9
boundary_violations: 0
unexpected_status_family: 2
baseline_evaluable: 6
correct_abstention_or_route_gap: 1
aggregate_accuracy: null
```

Status distribution:

```text
diagnostic_only: 1
inconclusive: 1
missing_assumptions: 2
proved: 1
refuted: 3
structural_mismatch: 1
```

Failure-class distribution:

```text
baseline_evaluable: 6
correct_abstention_or_route_gap: 1
unexpected_status_family: 2
```

## Per-Case Baseline Table

| Case | Workflow | Observed | Evidence | Expected Family | Match | Failure Class |
| --- | --- | --- | --- | --- | --- | --- |
| `RLHLB-01-ift-sign-gap` | `debug_derivation` | `refuted` | `backend_counterexample` | `refuted` | yes | `baseline_evaluable` |
| `RLHLB-02-kalman-loglik-assumptions` | `assumptions_for` | `missing_assumptions` | `missing_assumption` | `positive_or_abstain` | yes | `baseline_evaluable` |
| `RLHLB-03-joseph-equivalence` | `prove_or_counterexample` | `proved` | `backend_certificate` | `positive_or_abstain` | yes | `baseline_evaluable` |
| `RLHLB-04-affine-pricing-recursion` | `derive_from` | `inconclusive` | `human_review_required` | `positive_or_abstain` | yes | `correct_abstention_or_route_gap` |
| `RLHLB-05-kalman-score-same-scalar` | `assumptions_for` | `missing_assumptions` | `missing_assumption` | `positive_or_abstain` | yes | `baseline_evaluable` |
| `RLHLB-06-state-space-code-missing-solve` | `audit_math_to_code` | `structural_mismatch` | `structural_mismatch` | `routing_only` | yes | `baseline_evaluable` |
| `RLHLB-07-proof-boundary-review-packet` | `prepare_review_packet` | `diagnostic_only` | `review_packet` | `insufficient_evidence` | yes | `baseline_evaluable` |
| `RLHLB-08-hmc-value-only-boundary` | `prove_or_counterexample` | `refuted` | `backend_counterexample` | `insufficient_evidence` | no | `unexpected_status_family` |
| `RLHLB-09-affine-recovery-assumption-limit` | `derive_from` | `refuted` | `backend_counterexample` | `missing_assumptions` | no | `unexpected_status_family` |

## Determinism And Checks

Deterministic rerun projection:

```text
case_id, observed_status, observed_evidence_classes, failure_class: stable
```

Focused pytest:

```text
python3 -m pytest tests/test_real_local_high_level_benchmark.py tests/test_high_level_contracts.py tests/test_high_level_workflows.py tests/test_derive_from.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_prove_or_counterexample.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py -q
```

Result:

```text
70 passed
```

## Interpretation

The baseline found no boundary violations under the current envelope checks.
The material failures are status-family mismatches:

- `RLHLB-08` asks whether value-only filtering likelihood proves HMC production
  readiness. Current `prove_or_counterexample` refutes a placeholder equality,
  but the benchmark expects insufficient evidence or justified abstention.
- `RLHLB-09` asks whether neural-solver approximation guarantees can be derived
  from affine recovery text alone. Current `derive_from` refutes a placeholder
  equality, but the benchmark expects missing assumptions or justified
  abstention.

These are repair targets for semantic/source-boundary routing, not evidence
that the benchmark labels should be changed.

`RLHLB-04` is a useful canary: it already returns an inconclusive route gap for
a difficult derivation rather than a false proof/refutation.

## Claude Review

Phase 4 Claude R1 verdict: `AGREE`.

Findings:

- material repair targets are `RLHLB-08` and `RLHLB-09`;
- Phase 5 should require explicit semantic/source-backed proof route before
  allowing refutation on placeholder equalities;
- `RLHLB-04` should be used as a regression canary;
- `aggregate_accuracy=null` is appropriate because promotion should be based on
  eliminating the two mismatches and preserving determinism/tests.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. Every frozen case has a current-workflow result, route reference, packet summary, failure taxonomy, and boundary checks. |
| Veto diagnostics | No rubric change after results; no hidden wrong cases; no aggregate accuracy promotion; no Lean availability treated as proof; no improvement claim before repairs. |
| Explanatory diagnostics | Per-case table, deterministic rerun, focused pytest, Claude review. |
| Not concluded | Final capability quality, repair success, public benchmark validity, release readiness, scientific validation, production correctness, full LaTeX proof checking, or broad theorem proving. |

## Next-Phase Review

Phase 5 subplan was refreshed to:

- target `RLHLB-08` and `RLHLB-09` explicitly;
- forbid label changes as the repair;
- require `RLHLB-04` as a route-gap canary;
- require that placeholder-symbol equality refutations need semantic/source
  backing or must abstain.

## Handoff

Proceed to Phase 5 targeted capability repairs.
