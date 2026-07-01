# Phase 11 Subplan: RLHL-04 Repair Integration Addendum

Date: 2026-06-29

Status: `READY_FOR_EXECUTION`

## Phase Objective

Integrate the governed `RLHL-04-kalman-prediction-error-loglik` source-packet
extension repair into the visible source-adapter runbook as an addendum phase,
without rewriting the Phase 10 frozen-manifest partial result.

## Entry Conditions Inherited From Previous Phase

- Phase 10 completed with
  `PASSED_WITH_PARTIAL_SOURCE_ADAPTER_REPORT`.
- The frozen manifest remains
  `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json`.
- The frozen manifest source-adapter report is expected to remain `partial`
  with `adapter_required_residual: 1` for `RLHL-04`.
- The governed repair plan/result exist:
  `docs/plans/mathdevmcp-rlhl04-source-packet-extension-repair-plan-2026-06-29.md`
  and
  `docs/plans/mathdevmcp-rlhl04-source-packet-extension-repair-result-2026-06-29.md`.
- Claude R1 reviewed the repair plan and the patched repair was executed after
  tenant policy blocked further Claude review. This fallback must remain
  visible and cannot be re-labeled as Claude convergence.

## Required Artifacts

- This Phase 11 subplan.
- Phase 11 result:
  `docs/plans/mathdevmcp-real-local-source-adapters-phase-11-rlhl04-repair-integration-result-2026-06-29.md`.
- Updated execution ledger:
  `docs/plans/mathdevmcp-real-local-source-adapters-visible-execution-ledger-2026-06-29.md`.
- Updated stop handoff:
  `docs/plans/mathdevmcp-real-local-source-adapters-visible-stop-handoff-2026-06-29.md`.
- Repaired manifest:
  `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.rlhl04_spd_repair.json`.
- Phase 11 replay reports:
  `.mathdevmcp/real_local_source_adapter_report_2026-06-29-phase11-rlhl04-spd-repair.json`
  and
  `.mathdevmcp/real_local_source_adapter_report_2026-06-29-phase11-frozen.json`.

## Required Checks, Tests, And Reviews

- Recheck the BayesFilter source lines `32-39`.
- Recheck frozen-manifest SHA-256.
- Verify the repaired manifest differs from the frozen manifest only by the one
  planned appended `RLHL-04` source packet.
- Run:

  ```text
  python3 -m pytest tests/test_real_local_source_adapters.py tests/test_real_local_high_level_pilot.py
  ```

- Run and save the repaired-manifest source-adapter CLI report.
- Run and save the frozen-manifest source-adapter CLI report.
- Inspect JSON summaries and `RLHL-04` adapter checks rather than relying on
  CLI exit status.
- Claude review is not required for this addendum because the material repair
  plan already received Claude R1, was patched, and further Claude review is
  blocked by tenant policy. The result must record this boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the visible runbook continue past Phase 10 by integrating the governed `RLHL-04` repair as an addendum while preserving the frozen partial baseline? |
| Baseline/comparator | Phase 10 frozen-manifest report: `partial`, `adapter_required_residual: 1`, residual case `RLHL-04`. |
| Primary pass criterion | Phase 11 replay shows repaired manifest `passed` with `adapter_required_residual: 0`, `RLHL-04` `source_supported`, and `positive_definite_or_spd_present: true`; frozen manifest replay still shows `partial` with `adapter_required_residual: 1`; ledger and stop handoff name both states correctly. |
| Veto diagnostics | Frozen manifest hash changes; repaired manifest contains any unplanned change; repaired report clears through probes/tests/benchmark/confidence; frozen report stops being partial; aggregate accuracy is emitted; ledger or handoff claims frozen-manifest full clearance; any release/scientific/broad-proof claim appears. |
| Explanatory diagnostics | Source line excerpt, manifest invariance output, pytest status, repaired/frozen CLI summaries, RLHL-04 check values. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, production implementation correctness, full LaTeX proof checking, nonlinear-filter correctness, score/Hessian/sampler correctness, or broad theorem proving. |
| Preserved artifact | Phase 11 result note plus replay report JSON files. |

## Forbidden Claims And Actions

- Do not edit the frozen manifest.
- Do not replace or reinterpret the Phase 10 partial frozen-manifest result.
- Do not promote the repaired manifest/report to benchmark gate.
- Do not emit or rely on a single aggregate accuracy metric.
- Do not claim broad proof, scientific validity, release readiness, public
  benchmark validity, or production Kalman implementation correctness.
- Do not mutate sibling repositories or source LaTeX files.
- Do not use Claude as an execution authority.

## Exact Next-Phase Handoff Conditions

There is no automatic Phase 12. Phase 11 hands off to a final visible runbook
state when:

- required checks pass;
- Phase 11 replay reports are saved;
- the Phase 11 result states repaired-manifest completion and frozen-manifest
  preservation;
- the ledger includes the Phase 11 addendum entry;
- the stop handoff status is updated to distinguish the frozen partial result
  from the governed repaired-manifest closure.

## Stop Conditions

Stop and write a blocker result if:

- any required check fails in a way that affects this repair;
- the frozen manifest hash changes;
- the repaired manifest has changes beyond the planned `RLHL-04` source packet;
- the repaired replay remains partial or the frozen replay no longer has the
  expected residual;
- continuing would require package installation, network fetch, destructive
  git/filesystem action, neighboring-repo edits, model/API work beyond blocked
  read-only Claude review, release policy changes, or a scientific/product
  capability claim.
