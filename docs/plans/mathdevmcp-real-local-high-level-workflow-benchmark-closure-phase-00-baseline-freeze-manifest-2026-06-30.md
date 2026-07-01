# Phase 0 Baseline Freeze Manifest

Date: 2026-06-30

Program:
`mathdevmcp-real-local-high-level-workflow-benchmark-closure`

## Repository State

| Field | Value |
| --- | --- |
| Git commit | `44a7e96` |
| Python | `Python 3.11.15` |
| `mathdevmcp` package version | `0.1.0` |
| `pytest` version | `9.0.2` |
| Timestamp | `2026-06-30T01:42:21+08:00` |
| Worktree | Dirty; recorded in Phase 0 result. Unrelated changes are preserved. |

## Baseline Artifacts

| Artifact | Path | SHA-256 |
| --- | --- | --- |
| Seeded high-level quality report | `.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase00_high_level_quality.json` | `2920bed53d28a1c88fdd90bd2941adf436d15e6fa3688b16fb8aa9fe3bb4b3d9` |
| Frozen high-level pilot manifest | `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json` | `777aeacde3fcdb8b2c41e665588074e4eb97d3439ca438a03beefdece47fbcc0` |
| Repaired high-level pilot manifest | `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.rlhl04_spd_repair.json` | `52dacfc35c9a18334d3a43d574805f3bee3bed6f351296f1d687f81317f887a7` |
| Phase 0 repaired source-adapter report | `.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase00_source_adapter_repaired.json` | `50cdb175e8aa91b018103d16c1122e537573f96179decdf63f1c95f5f5de082e` |
| Phase 0 frozen source-adapter report | `.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase00_source_adapter_frozen.json` | `74ee1dcb8ebfc3020650419057b6bc31eaebdb81a1853e1b6edc230b1bff022d` |

## Commands

Seeded high-level quality:

```text
python3 -m mathdevmcp.cli high-level-workflow-quality --root "$PWD"
```

Focused high-level regression:

```text
python3 -m pytest tests/test_high_level_contracts.py tests/test_high_level_workflows.py tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py
```

Repaired source-adapter snapshot:

```text
python3 -m mathdevmcp.cli real-local-source-adapters --root "$PWD" --manifest benchmarks/real_tasks/holdout_local/high_level_pilot_cases.rlhl04_spd_repair.json
```

Frozen source-adapter snapshot:

```text
python3 -m mathdevmcp.cli real-local-source-adapters --root "$PWD" --manifest benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json
```

## Expected Verdict Snapshots

Seeded high-level workflow quality:

```text
status: quality_thresholds_passed
total_cases: 14
total_results: 14
workflow_count: 6
negative_control_count: 12
determinism_stable: True
mutation_results:
  not_encodable_to_refuted: True
  structural_match_to_proved: True
  review_packet_to_proved: True
  missing_assumptions_to_proved: True
  no_counterexample_to_refuted: True
```

Focused high-level regression:

```text
53 passed
```

Repaired source-adapter snapshot:

```text
status: passed
case_total: 5
source_supported: 4
inconsistency_candidate: 1
human_review_required: 0
adapter_required_residual: 0
aggregate_accuracy: None
RLHL-04 status: source_supported
RLHL-04 positive_definite_or_spd_present: True
```

Frozen source-adapter snapshot:

```text
status: partial
case_total: 5
source_supported: 3
inconsistency_candidate: 1
human_review_required: 1
adapter_required_residual: 1
aggregate_accuracy: None
RLHL-04 status: human_review_required
RLHL-04 positive_definite_or_spd_present: False
```

## Backend And Adapter Availability

| Route | Phase 0 State | Boundary |
| --- | --- | --- |
| High-level workflow seeded runner | Available; quality thresholds passed | Seeded sentinel only, not real-local closure. |
| Source adapters | Available; repaired/frozen distinction reproduced | Local/non-gating only. |
| Lean readiness | `ready_with_caveats` | Formal backend availability is not a proof of any benchmark case. |
| Symbolic/counterexample helpers | Existing tests passed through focused workflow regression | Availability must be rechecked per benchmark route. |
| GPU/CUDA | `N/A` | No GPU action used. |

## Non-Claims

This freeze manifest does not conclude real-local benchmark closure, release
readiness, public benchmark validity, scientific validation, production
implementation correctness, external reproducibility, full LaTeX proof
checking, or broad theorem proving.
