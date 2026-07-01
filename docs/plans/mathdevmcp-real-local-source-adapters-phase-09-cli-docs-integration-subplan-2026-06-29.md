# Phase 09 Subplan: CLI Docs And Non-Gating Integration

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Expose the source-adapter report through a local CLI command and update local
holdout docs with operator-safe wording and non-gating boundaries.

## Entry Conditions Inherited From Previous Phase

Phase 08 has produced a source-adapter report with separate ledgers, five source
results, zero residual adapter-required cases, and no aggregate accuracy.

## Required Artifacts

- CLI command for the real-local source-adapter report.
- README/operator wording for local-only use.
- Phase 09 result record.
- Refreshed Phase 10 subplan.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py`
- CLI smoke for the new command.
- `rg` grep for non-gating and forbidden-claim wording.
- Claude review only if public/release wording changes materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can operators run the source-adapter report locally without confusing it with benchmark-gate/release evidence? |
| Baseline/comparator | Existing `real-local-high-level-pilot` CLI and holdout-local README. |
| Primary pass criterion | CLI returns the report, docs state local/non-gating/source-adapter boundaries, and no release/public claims are introduced. |
| Veto diagnostics | CLI report included in benchmark gate; docs imply public benchmark validity or release readiness; aggregate accuracy shown. |
| Explanatory diagnostics | CLI output, docs grep. |
| Not concluded | Public redistributability, release readiness. |
| Artifact | CLI/docs changes and Phase 09 record. |

## Forbidden Claims / Actions

- Do not change benchmark-gate criteria.
- Do not advertise public redistributability.
- Do not claim broad proof capability.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 10 only when CLI/docs are local-only, non-gating, and pass
focused checks.

## Stop Conditions

Stop if exposing the CLI would require a policy decision about public release or
CI gating.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 09 result; draft or
refresh Phase 10; review Phase 10 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
