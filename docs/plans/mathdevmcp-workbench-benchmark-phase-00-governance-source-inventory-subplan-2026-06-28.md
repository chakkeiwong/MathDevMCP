# Phase 0 Subplan: Governance And Source Inventory

## Phase Objective

Establish the execution baseline for the workbench benchmark program: current
benchmark totals, workbench regression status, dirty-worktree boundary, licensed
external-source assumptions, and launch constraints.

## Entry Conditions Inherited From Previous Phase

- No prior phase in this benchmark program.
- Workbench implementation runbook is complete locally.
- User stated academic license coverage for discussed external benchmark
  families.

## Required Artifacts

- Phase 0 result record.
- Updated visible execution ledger entries.
- Refreshed Phase 1 subplan if the baseline reveals schema/quality issues.

## Required Checks, Tests, Reviews

- `git status --short`
- Current `benchmark-gate --root .`
- Focused workbench regression command, or reference most recent result if
  still fresh and no relevant code changed.
- `git diff --check`
- Codex skeptical plan audit.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is it safe and well-scoped to launch the benchmark program from the current repo state? |
| Baseline/comparator | Current benchmark gate total and current workbench regression evidence. |
| Primary pass criterion | Baseline is recorded; unrelated dirty files are identified; launch mode avoids network/downloads and destructive actions. |
| Veto diagnostics | Wrong benchmark total, hidden dirty-worktree dependency, external download required before governance, or release/gate claim from planning. |
| Explanatory diagnostics | `git status`, benchmark gate output, focused regression output. |
| Not concluded | Benchmark quality, external pack readiness, or release readiness. |
| Artifact | Phase 0 result and ledger entry. |

## Forbidden Claims And Actions

- Do not fetch external benchmark data.
- Do not edit unrelated dirty files.
- Do not claim new benchmark validity from baseline checks.
- Do not change benchmark pass/fail policy.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 if the current benchmark and workbench baselines are recorded
and no launch blocker requires user approval.

## Stop Conditions

Stop if current repo state makes benchmark totals uninterpretable, if required
baseline checks fail for unrelated reasons, or if execution requires external
downloads before schema design.
