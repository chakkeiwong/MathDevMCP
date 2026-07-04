# Phase 10 Result: Final Regression And Handoff

Date: 2026-06-29

Status: `PASSED_WITH_PARTIAL_SOURCE_ADAPTER_REPORT`

## Objective

Run final focused regressions, write the final source-adapter report and visible
handoff, and state exactly what was and was not concluded.

## Final Checks

Focused regression:

```text
python3 -m pytest tests/test_real_local_source_adapters.py tests/test_real_local_high_level_pilot.py tests/test_high_level_workflows.py tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py tests/test_release_smoke.py
```

Result: `73 passed`.

Source-adapter CLI:

```text
python3 -m mathdevmcp.cli real-local-source-adapters --root "$PWD"
```

Report artifact:

```text
.mathdevmcp/real_local_source_adapter_report_2026-06-29.json
```

Result summary:

```text
status: partial
case_total: 5
source_supported: 3
inconsistency_candidate: 1
human_review_required: 1
adapter_required_residual: 1
aggregate_accuracy: None
```

Original pilot CLI:

```text
python3 -m mathdevmcp.cli real-local-high-level-pilot --root "$PWD"
```

Report artifact:

```text
.mathdevmcp/real_local_high_level_pilot_report_2026-06-29-final.json
```

Result summary:

```text
status: passed
case_total: 5
probe_passed: 5
probe_failed: 0
adapter_required: 5
aggregate_accuracy: None
```

This remains the executable-probe pilot report. It is intentionally separate
from the source-adapter report.

High-level workflow quality:

```text
python3 -m mathdevmcp.cli high-level-workflow-quality --root "$PWD"
```

Result:

```text
quality_thresholds_passed
total_cases: 14
total_results: 14
```

Existing-suite benchmark gate observation:

```text
python3 -m mathdevmcp.cli benchmark-gate --root "$PWD"
```

Result: `passed: True`.

This benchmark-gate run is an existing-suite regression observation only. It is
not source-adapter promotion evidence and not local source-obligation clearance.

## Final Source-Adapter Status

| Case | Adapter Result | Clearance |
| --- | --- | --- |
| `RLHL-01-ift-gradient-bias-sign` | `inconsistency_candidate` | cleared under local source schema as a sign inconsistency candidate |
| `RLHL-04-kalman-prediction-error-loglik` | `human_review_required` | not cleared; residual `adapter_required` remains |
| `RLHL-06-joseph-covariance-equivalence` | `source_supported` | cleared under local source schema |
| `RLHL-07-affine-pricing-master-recursion` | `source_supported` | cleared under local source schema |
| `RLHL-10-kalman-score-same-scalar-contract` | `source_supported` | cleared under local source schema |

`RLHL-04` remains uncleared because the frozen likelihood packet omits
source-anchored positive-definite selected innovation covariance evidence. A
synthetic governed-extension test shows that adding BayesFilter lines `32-39`
would clear the local schema, but that extension was not applied to the frozen
manifest during this run.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Partial. The implementation produced bounded packet extraction, IR, five adapter routes, a source-adapter report, CLI/docs integration, and final regressions. Four of five cases have local source-schema clearance; one remains residual under the frozen manifest. |
| Veto diagnostics | The no-forced-closure veto fired safely for `RLHL-04`. No aggregate source/probe accuracy was emitted, local source results were not added to benchmark-gate totals, and no release/scientific/broad proof claim was made. |
| Explanatory diagnostics | Focused tests and CLI reports pass; benchmark gate passed as an existing-suite regression observation only. |
| Not concluded | Full source-obligation completion under the frozen manifest, public benchmark validity, release readiness, scientific validation, production implementation correctness, full LaTeX proof checking, external reproducibility, or broad theorem proving. |

## Decision Table

| Decision | Status |
| --- | --- |
| Complete visible runbook execution | Passed with partial source-adapter report |
| Promote source-adapter report to benchmark gate | Not allowed |
| Claim all five source obligations cleared | Not allowed; `RLHL-04` remains residual |
| Next justified action | Create a small reviewed manifest-extension repair for `RLHL-04` or accept the partial report as the frozen-run result |

## Final Artifact Summary

- Master program and visible runbook under `docs/plans/`.
- Phase results for Phases 00-10.
- Claude review trail with plan R1-R6-long and material Phase 03/08 reviews.
- Source adapter implementation:
  `src/mathdevmcp/real_local_source_adapters.py`.
- Tests:
  `tests/test_real_local_source_adapters.py`.
- CLI command:
  `real-local-source-adapters`.
- Docs:
  `benchmarks/real_tasks/holdout_local/README.md`.
- Final local reports:
  `.mathdevmcp/real_local_source_adapter_report_2026-06-29.json`
  and `.mathdevmcp/real_local_high_level_pilot_report_2026-06-29-final.json`.

## Next Justified Program

The smallest next program is a reviewed `RLHL-04` manifest-extension repair:

- add the BayesFilter innovation-regularity assumption packet at lines `32-39`;
- rerun packet/IR/source-adapter checks;
- verify `adapter_required_residual` becomes zero without changing the frozen
  run's interpretation;
- keep local/non-gating and non-claim boundaries.
