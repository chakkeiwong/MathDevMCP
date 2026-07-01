# RLHL-04 Source Packet Extension Repair Result

Date: 2026-06-29

Status: `PASSED_WITH_GOVERNED_REPAIR_MANIFEST`

## Objective

Close the remaining `RLHL-04-kalman-prediction-error-loglik` local
source-adapter residual using a separate repaired manifest while preserving the
frozen-manifest partial result.

## Plan And Review

Plan:

```text
docs/plans/mathdevmcp-rlhl04-source-packet-extension-repair-plan-2026-06-29.md
```

Claude review:

- R1 returned `VERDICT: REVISE`.
- R1 findings were patched visibly: exact output artifacts, run manifest,
  repaired-vs-frozen invariance check, root-relative path-resolution rule, and
  unrelated-code-clearance veto.
- R2 was blocked by the approval reviewer even after user repo-level approval
  because tenant policy forbids sending further private workspace-derived repo
  artifacts and internal paths to an untrusted external service.
- A Codex-only post-patch gate checked the R1 repairs, evidence contract,
  sequencing, feasibility, artifact coverage, and boundary safety before
  execution.

## Source Packet Added

The repaired manifest appends this packet only to
`RLHL-04-kalman-prediction-error-loglik`:

```json
{
  "path": "../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex",
  "line_range": "32-39",
  "role": "innovation regularity assumption"
}
```

Local source check:

```text
32 \begin{assumption}[Innovation regularity]
35 covariance $S_t$ defined below is positive definite on the observed
36 coordinates.
39 \end{assumption}
```

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `44a7e96` |
| Working directory | `/home/chakwong/python/MathDevMCP` |
| Python | `Python 3.11.15` |
| Timestamp | `2026-06-29T22:23:13+08:00` |
| GPU/CPU status | GPU `N/A`; no GPU/CUDA action used. CPU-only local JSON/test/CLI checks. |
| Random seeds | `N/A`; deterministic JSON/test/CLI checks. |
| Data/source version | Frozen manifest SHA-256 `777aeacde3fcdb8b2c41e665588074e4eb97d3439ca438a03beefdece47fbcc0`; BayesFilter source path resolved from MathDevMCP root to `$PWD/../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex`. |
| Repaired manifest | `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.rlhl04_spd_repair.json`, SHA-256 `52dacfc35c9a18334d3a43d574805f3bee3bed6f351296f1d687f81317f887a7` |
| Repaired report | `.mathdevmcp/real_local_source_adapter_report_2026-06-29-rlhl04-spd-repair.json`, SHA-256 `50cdb175e8aa91b018103d16c1122e537573f96179decdf63f1c95f5f5de082e` |
| Frozen-after-repair report | `.mathdevmcp/real_local_source_adapter_report_2026-06-29-frozen-after-rlhl04-repair.json`, SHA-256 `74ee1dcb8ebfc3020650419057b6bc31eaebdb81a1853e1b6edc230b1bff022d` |
| Wall time | Focused pytest: `1.10s`; CLI checks were short local runs. |

## Commands And Results

Source line check:

```text
nl -ba ../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex | sed -n '32,39p'
```

Result: lines exist and contain the named innovation-regularity assumption with
selected covariance positive-definiteness on observed coordinates.

Focused regression:

```text
python3 -m pytest tests/test_real_local_source_adapters.py tests/test_real_local_high_level_pilot.py
```

Result:

```text
26 passed in 1.10s
```

Repaired manifest report:

```text
python3 -m mathdevmcp.cli real-local-source-adapters --root "$PWD" --manifest benchmarks/real_tasks/holdout_local/high_level_pilot_cases.rlhl04_spd_repair.json
```

Saved to:

```text
.mathdevmcp/real_local_source_adapter_report_2026-06-29-rlhl04-spd-repair.json
```

Result summary:

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

Frozen manifest report:

```text
python3 -m mathdevmcp.cli real-local-source-adapters --root "$PWD" --manifest benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json
```

Saved to:

```text
.mathdevmcp/real_local_source_adapter_report_2026-06-29-frozen-after-rlhl04-repair.json
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
RLHL-04 status: human_review_required
RLHL-04 positive_definite_or_spd_present: False
RLHL-04 residual missing_checks: ["positive_definite_or_spd_present"]
```

Manifest invariance:

```text
PASS repaired manifest differs only by planned RLHL-04 source packet
PASS invariance retained after CLI runs
frozen manifest SHA-256 after execution:
777aeacde3fcdb8b2c41e665588074e4eb97d3439ca438a03beefdece47fbcc0
```

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. The repaired manifest report is `passed`, has `adapter_required_residual: 0`, and `RLHL-04` is `source_supported` with `positive_definite_or_spd_present: True`. |
| Baseline preservation | Passed. The frozen manifest hash stayed `777aeacde3fcdb8b2c41e665588074e4eb97d3439ca438a03beefdece47fbcc0`, and the frozen report remains `partial` with the same `RLHL-04` SPD residual. |
| Veto diagnostics | No frozen in-place edit, no aggregate accuracy, no source/probe/residual ledger collapse, no benchmark-gate promotion, no release/scientific/broad-proof claim, and no unrelated-code clearance observed. |
| Explanatory diagnostics | Packet count for `RLHL-04` increases to three in the repaired manifest; source-supported count increases from three to four; human-review-required count drops from one to zero only in the repaired report. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, full LaTeX proof checking, nonlinear-filter correctness, score/Hessian/sampler correctness, broad theorem proving, or replacement of the frozen partial result. |

## Decision Table

| Decision | Status |
| --- | --- |
| Accept the repaired manifest as a governed local source-packet extension | Accepted for local/non-gating use. |
| Claim the frozen manifest now fully clears all source obligations | Rejected; frozen report remains intentionally partial. |
| Promote source-adapter report to benchmark gate | Rejected; out of scope and explicitly forbidden. |
| Treat repaired pass as proof of Kalman implementation/scientific validity | Rejected; local source-schema clearance only. |
| Next justified action | Keep both reports: frozen partial as historical baseline and repaired manifest/report as the governed closure artifact for the `RLHL-04` source-packet-scope gap. |

## Close Record

The repair target is complete under the plan's local evidence contract. The
remaining distinction is interpretive, not technical: the frozen manifest still
records the original partial source-adapter result, while the repaired manifest
demonstrates that the residual was a source-packet-scope gap closed by the
BayesFilter innovation-regularity assumption packet.
