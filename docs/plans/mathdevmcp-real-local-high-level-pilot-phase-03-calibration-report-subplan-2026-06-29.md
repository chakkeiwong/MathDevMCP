# Phase 03 Subplan: Pilot Calibration And Reports

## Phase Objective

Run the five-case pilot, preserve per-case evidence, and classify the current
workflow capabilities and adapter gaps without post-hoc changing expected
statuses or rubrics.

## Entry Conditions Inherited From Previous Phase

- Phase 02 loader, runner, scoring, and tests pass.
- Expected probe statuses and evidence classes were fixed in Phase 01.
- Source-obligation, executable-probe, and adapter-gap channels are distinct in
  the runner/scorer.
- The pilot remains local/non-gating.

## Required Artifacts

- Pilot report output under `.mathdevmcp/` or a phase result summary.
- Phase result:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-03-calibration-report-result-2026-06-29.md`
- Phase 04 subplan.

## Required Checks, Tests, And Reviews

- Local checks:
  - Python invocation of the pilot runner/report.
  - `python3 -m pytest tests/test_real_local_high_level_pilot.py`
- Review:
  - Codex self-review required.
  - Claude read-only review required for material interpretation of pilot
    pass/fail and adapter-gap classifications.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What does the current high-level workflow layer do on the five real-local pilot probes, and which full source obligations remain adapter-required? |
| Baseline/comparator | Phase 01 expected probe outcomes and Phase 02 scoring. |
| Primary pass criterion | Pilot report is deterministic, all executable probes pass their declared boundary checks, source obligations and adapter-required/full-source gaps are reported in separate ledgers, and no single aggregate accuracy number is emitted. |
| Veto diagnostics | Changing expected statuses after seeing outputs, treating probe pass as source proof, suppressing failed boundary checks, blending source/probe results, or ranking scientific correctness by pilot pass rate. |
| Explanatory diagnostics | Per-case observed status, evidence classes, missing terms, non-claims, adapter notes. |
| Not concluded | Full derivation/proof capability, external benchmark validity, release readiness. |
| Artifacts | Pilot report, phase result, refreshed Phase 04 subplan. |

## Forbidden Claims And Actions

- Do not call the report benchmark-gate evidence.
- Do not call adapter-required cases failures if the executable probe passed
  but the full source derivation remains unsupported.
- Do not change case expectations after execution.
- Do not infer scientific validity of DSGE, Kalman, affine-pricing, or BGS
  source material.
- Do not emit a single aggregate pilot accuracy metric.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 04 only if:

- the pilot report is generated and interpretable;
- all failures are either fixed with focused checks or recorded as blockers;
- non-claims are present in the report/result;
- report channels remain separate for source obligations, executable probes,
  and adapter gaps;
- Phase 04 can expose/report the pilot without gating release.

## Stop Conditions

- Stop if a pilot result violates a boundary check and cannot be fixed locally.
- Stop if the report encourages forbidden claims.
- Stop if source access disappears or path validation becomes unreliable.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 04 subplan.
4. Review the Phase 04 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
