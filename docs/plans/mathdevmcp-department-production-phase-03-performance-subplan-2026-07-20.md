# P03 Subplan: Performance And Resource Budgets

## Objective

Replace non-negative timing assertions with bounded production diagnostics for
indexing, querying, MCP startup, and representative document workloads.

## Entry Conditions

Production surface and test lanes are stable.

## Required Artifacts

- Versioned performance-budget policy.
- Deterministic synthetic small/medium/large LaTeX generator outside the repo.
- Cold/warm index build, query, MCP initialize/list/doctor, wall time, and peak
  RSS measurements.
- Generous functional veto thresholds and descriptive timing artifacts.
- Hook for approved-corpus measurements without recording private paths.

## Required Checks

- Focused deterministic tests of budget classification.
- Local CPU performance smoke.
- Timeout and oversized-input negative cases.

## Evidence Contract

Budget passes mean viable under stated hardware/environment, not performance
superiority. Tail timings from one machine are descriptive only.

## Forbidden Actions

- No tight CI microbenchmark ranking.
- No private path or document content in artifacts.
- No claim that synthetic scale represents all department documents.

## Handoff

P04 begins when catastrophic regressions are vetoed and descriptive performance
data is retained.

## Stop Conditions

The harness is unstable enough that it cannot distinguish implementation
regression from host noise.
