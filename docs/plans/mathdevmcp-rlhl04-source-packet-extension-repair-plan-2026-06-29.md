# RLHL-04 Source Packet Extension Repair Plan

Date: 2026-06-29

Status: `REVISED_AFTER_CLAUDE_R1`

## Objective

Close the remaining `RLHL-04-kalman-prediction-error-loglik` local
source-adapter residual with a governed repaired manifest, without mutating or
reinterpreting the frozen local manifest result.

## Five Repair Points

1. Preserve the frozen source-adapter baseline and its partial result.
2. Add the missing BayesFilter innovation-regularity source packet only in a
   separate repaired manifest artifact.
3. Verify that the repaired manifest clears `RLHL-04` through the existing
   source-anchored local-schema adapter, not through executable probes, tests,
   or confidence.
4. Verify that the frozen manifest still reports `partial` with the same
   `RLHL-04` residual, so historical evidence is not overwritten.
5. Write a close record that keeps source, probe, residual, and benchmark-gate
   ledgers separate and states non-claims.

## Entry Conditions

- The final source-adapter handoff exists at
  `docs/plans/mathdevmcp-real-local-source-adapters-phase-10-final-regression-handoff-result-2026-06-29.md`.
- The frozen manifest is
  `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json`.
- The frozen source-adapter report status is expected to remain `partial` with
  `adapter_required_residual: 1` for `RLHL-04`.
- Existing synthetic tests show that adding
  `../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex`
  lines `32-39` clears the local `RLHL-04` adapter.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does a separate governed manifest extension containing the BayesFilter innovation-regularity assumption packet clear the `RLHL-04` local source-adapter residual? |
| Baseline/comparator | Frozen manifest source-adapter CLI/report: `partial`, `adapter_required_residual: 1`, residual case `RLHL-04`. |
| Primary pass criterion | Repaired manifest source-adapter CLI/report returns `passed`, `adapter_required_residual: 0`, `RLHL-04` has `status: source_supported`, and `positive_definite_or_spd_present: true`. |
| Veto diagnostics | Frozen manifest changes; frozen manifest no longer reports the expected residual; repaired report clears from probe/test/benchmark evidence; aggregate accuracy emitted; source/probe/residual ledgers are collapsed; the new packet has wrong path/range/role or missing local source lines. |
| Explanatory diagnostics | Packet count increase, source anchors for `RLHL-04`, adapter missing-check list, CLI summaries, focused pytest status. |
| Not concluded | Public benchmark validity, release readiness, scientific validation, full LaTeX proof checking, nonlinear-filter correctness, score/Hessian/sampler correctness, broad theorem proving, or replacement of the frozen partial result. |
| Preserved artifact | Repaired manifest JSON, source-adapter CLI report JSON, close/result note, and this plan. |

## Skeptical Plan Audit

- Wrong baseline: the comparator is the completed partial source-adapter report,
  not the earlier aspirational zero-residual gate or benchmark-gate status.
- Proxy metric risk: pytest and executable-probe success are regression and
  safety diagnostics only; the only clearance signal is the source-adapter
  local schema on the repaired manifest.
- Hidden assumption: BayesFilter lines `32-39` must exist locally and contain
  positive-definite selected innovation covariance evidence.
- Stale context: the line range must be rechecked immediately before manifest
  creation.
- Environment mismatch: no package install, network fetch, GPU use, external
  source mutation, or benchmark promotion is required.
- Path-resolution risk: manifest source paths are resolved from the MathDevMCP
  repo root used as `--root "$PWD"`. The planned packet therefore resolves to
  `$PWD/../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex`,
  and that exact local file must be checked before execution.
- Artifact fit: a separate repaired manifest plus paired frozen/repaired CLI
  reports directly answer whether the residual is a manifest-scope gap.
- Stop conditions: any veto diagnostic stops execution and produces a blocker
  note rather than forcing closure.

Audit result before Claude review: `PASSED_FOR_REVIEW`.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure Mode | Early Diagnostic | Promotion Status |
| --- | --- | --- | --- | --- | --- |
| Separate repaired manifest | Final handoff next action | Preserves frozen-run interpretation while testing a governed source-packet extension | Accidentally treated as replacing the frozen manifest | Run frozen CLI after repair and document it remains `partial` | Reviewed repair artifact |
| BayesFilter line range `32-39` | Synthetic test and final handoff | Contains named innovation regularity assumption with selected covariance positive definiteness | Source drift or wrong file could make check meaningless | Print/check local lines before manifest creation | Hypothesis until line check passes |
| Existing adapter route | `evaluate_kalman_likelihood_adapter` tests | Adapter already requires linear Gaussian, chain rule, likelihood terms, SPD, and mask policy | Adapter could overfit phrase presence | Run existing positive/negative adapter tests | Baseline implementation |
| CLI success on `partial` | Existing CLI contract | A visible residual gap is a valid governed report state | Exit status alone could hide residual | Inspect JSON summary/status, not only exit code | Reviewed default |
| No README promotion claim | Current README boundary language | Avoids implying repaired manifest is public/gating evidence | Docs could imply completion of frozen result | Grep/review README/result note for non-claims | Boundary constraint |

## Required Artifacts

- `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.rlhl04_spd_repair.json`
- `.mathdevmcp/real_local_source_adapter_report_2026-06-29-rlhl04-spd-repair.json`
- `.mathdevmcp/real_local_source_adapter_report_2026-06-29-frozen-after-rlhl04-repair.json`
- `docs/plans/mathdevmcp-rlhl04-source-packet-extension-repair-result-2026-06-29.md`
- A run manifest embedded in the result note with git commit, commands,
  environment, CPU/GPU status (`N/A` for GPU), source paths, random seeds
  (`N/A`), wall time if known, and output artifact paths.
- Optional focused README note if needed to expose the repaired-manifest command
  without promoting it.

## Required Checks

Run these local checks after implementation:

```text
python3 -m pytest tests/test_real_local_source_adapters.py tests/test_real_local_high_level_pilot.py
python3 -m mathdevmcp.cli real-local-source-adapters --root "$PWD" --manifest benchmarks/real_tasks/holdout_local/high_level_pilot_cases.rlhl04_spd_repair.json
python3 -m mathdevmcp.cli real-local-source-adapters --root "$PWD" --manifest benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json
```

The CLI JSON outputs must be saved to the `.mathdevmcp` artifacts listed
above.

Also run invariance checks that:

- the frozen manifest SHA-256 before and after implementation is identical;
- the repaired manifest differs from the frozen manifest only by one appended
  `RLHL-04` `source_files` entry with exactly the planned `path`,
  `line_range`, and `role`;
- the repaired manifest contains no other case, probe, obligation, or forbidden
  claim changes.

## Forbidden Claims And Actions

- Do not edit the frozen manifest in place.
- Do not treat the repaired manifest as a public benchmark fixture or
  benchmark-gate input.
- Do not use executable probes, pytest, Claude review, or CLI exit status to
  clear `adapter_required`.
- Do not emit a single aggregate accuracy metric for source/probe results.
- Do not claim broad proof, scientific validity, release readiness, or
  production Kalman implementation correctness.
- Do not mutate sibling repositories or source LaTeX files.
- Do not install packages, fetch network resources, or run long experiments.
- Do not accept a repaired pass if `RLHL-04` clears because of unrelated adapter
  code changes rather than the targeted added source packet.

## Execution Steps

1. Recheck the local BayesFilter source lines `32-39`.
2. Create the separate repaired manifest by copying the frozen manifest content
   and appending one `RLHL-04` `source_files` entry:

   ```json
   {
     "path": "../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex",
     "line_range": "32-39",
     "role": "innovation regularity assumption"
   }
   ```

3. Run the focused pytest checks.
4. Run the repaired-manifest source-adapter CLI and save the JSON report.
5. Run the frozen-manifest source-adapter CLI and save the JSON report.
6. Run the manifest invariance checks.
7. Inspect the JSON summaries for the primary criterion and veto diagnostics.
8. Write the repair result / close record, including the run manifest and a
   short replay note naming the exact commands and output paths.

## Exact Handoff Conditions

The repair is complete only if:

- the repaired manifest exists and differs from the frozen manifest only by the
  governed `RLHL-04` source-packet extension;
- the frozen manifest file hash is unchanged before and after implementation;
- focused tests pass;
- repaired CLI report is `passed` with `adapter_required_residual: 0`;
- repaired `RLHL-04` adapter result is `source_supported` with
  `positive_definite_or_spd_present: true`;
- frozen CLI report remains `partial` with `adapter_required_residual: 1` for
  `RLHL-04`;
- the result note records commands, summaries, decision table, non-claims, and
  next justified action.

## Stop Conditions

Stop and write a blocker note if:

- Claude review returns a material `REVISE` that cannot be patched within five
  focused review rounds;
- the BayesFilter line range is absent or does not contain the required
  positive-definite selected innovation covariance assumption;
- the repaired manifest changes any frozen case content other than the single
  planned source-packet extension;
- the frozen manifest hash changes;
- focused tests fail for reasons not clearly unrelated to this repair;
- the repaired CLI remains `partial` or the frozen CLI no longer shows the
  expected residual;
- the repaired pass cannot be tied to exactly the added source packet;
- any action would require human, runtime, model-file, funding,
  product-capability, privacy, source-repository, or scientific-claim boundary
  approval.

## Claude Review Trail

- R1 verdict: `REVISE`.
- R1 issues patched: exact report artifact paths and run-manifest requirement;
  repaired-vs-frozen invariance check; root-relative source path-resolution
  rule; explicit veto against unrelated-code clearance.
- R2 attempt: blocked by the approval reviewer even after user repo-level
  approval because tenant policy forbids sending further private
  workspace-derived repo artifacts and internal paths to an untrusted external
  service.
- Fallback: execute only after a Codex-only post-patch review verifies that R1
  findings are patched and no material evidence-contract, sequencing,
  feasibility, artifact-coverage, or boundary-safety issue remains. This
  fallback is narrower than Claude convergence and must be recorded in the
  close result.
