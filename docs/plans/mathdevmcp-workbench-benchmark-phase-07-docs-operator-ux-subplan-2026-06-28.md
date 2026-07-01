# Phase 7 Subplan: Docs And Operator UX

## Phase Objective

Document how to run and interpret the new benchmark program, including seeded
gate behavior, benchmark-quality metrics, and external adapted pack boundaries.

## Entry Conditions Inherited From Previous Phase

- Gate/report integration is stable.
- Diagnostic external pack status is either implemented or blocked with a clear
  local-source requirement.

## Required Artifacts

- README/operator/benchmark docs updates.
- Example commands for seeded benchmark, quality report, and external diagnostic
  manifest validation.
- Phase 7 result record.
- Refreshed Phase 8 subplan.

## Required Checks, Tests, Reviews

- Docs grep for forbidden claims.
- CLI help or command smoke for documented commands.
- `git diff --check`.
- Claude review for docs overclaim risk.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can operators understand benchmark purpose, quality limits, and external pack status? |
| Baseline/comparator | Current README/operator guide/benchmark docs. |
| Primary pass criterion | Docs distinguish seeded gated evidence, diagnostic external packs by source family/oracle class, quality metrics, run manifests, and non-claims. |
| Veto diagnostics | Docs imply leaderboard/release/scientific validity or broad theorem-proving capability. |
| Explanatory diagnostics | Grep hits and command smoke output. |
| Not concluded | External pack promotion or release readiness. |
| Artifact | Docs/result. |

## Forbidden Claims And Actions

- Do not claim benchmark validity beyond stated quality metrics.
- Do not imply academic license equals public redistribution.
- Do not hide diagnostic/non-gating status.
- Do not show external scores beside seeded CI totals unless source-specific
  provenance/oracle review is explicit.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 8 if docs pass forbidden-claim review and commands are
discoverable.

## Stop Conditions

Stop if docs cannot describe benchmark status without overclaiming.
