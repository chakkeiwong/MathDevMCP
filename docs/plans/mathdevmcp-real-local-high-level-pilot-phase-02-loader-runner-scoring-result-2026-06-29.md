# Phase 02 Result: Loader, Runner, And Scoring

Date: 2026-06-29

Status: `PASSED`

## Objective

Implement local pilot loading, validation, executable probe dispatch, and
boundary-preserving scoring.

## Artifacts Created

- `src/mathdevmcp/real_local_high_level_pilot.py`
- `tests/test_real_local_high_level_pilot.py`

## Implementation Summary

The new module provides:

- `load_high_level_pilot_manifest(...)` for local manifest loading and
  validation;
- `score_probe_result(...)` for executable-probe scoring;
- `run_high_level_pilot(...)` for report generation with separate ledgers.

The report preserves three distinct channels:

- `source_obligation_ledger`;
- `probe_ledger`;
- `adapter_gap_ledger`.

It deliberately emits `aggregate_accuracy: None`.

## Local Checks

```text
python3 -m pytest tests/test_real_local_high_level_pilot.py
```

Result: `6 passed`.

```text
python3 -m pytest tests/test_high_level_workflows.py tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py
```

Result: `40 passed`.

Manual report invocation:

```text
status: passed
summary: {'case_total': 5, 'probe_passed': 5, 'probe_failed': 0, 'adapter_required': 5, 'aggregate_accuracy': None}
```

## Known-Bad Scorer Coverage

Tests cover:

- absolute source path rejection;
- blended `case_status` rejection;
- failure when a required non-claim is missing;
- failure when an adapter gap is hidden.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. Loader validates manifest fields/path/snapshot policy; runner dispatches declared probes; scoring checks probe status/evidence/non-claims separately from source and adapter channels; known-bad scorer tests fail as intended. |
| Veto diagnostics | No Phase 2 veto fired. The runner does not mutate source files, does not add pilot results to benchmark-gate totals, and does not emit a single blended accuracy metric. |
| Explanatory diagnostics | All five executable probes pass their declared boundary checks, and all five source obligations remain adapter-required. |
| Not concluded | Full semantic correctness of source derivations, release readiness, and benchmark-gate evidence are not concluded. |

## Phase 03 Handoff

Proceed to Phase 03. The calibration/report phase must:

- generate a persistent pilot report artifact;
- preserve separate source/probe/adapter ledgers;
- avoid post-hoc expectation changes;
- avoid single aggregate pilot accuracy;
- report adapter-required gaps as non-claims, not failures.

## Next Subplan Review

Phase 03 subplan remains consistent and feasible. It consumes the Phase 02
runner/scorer and requires a report artifact plus focused tests.
