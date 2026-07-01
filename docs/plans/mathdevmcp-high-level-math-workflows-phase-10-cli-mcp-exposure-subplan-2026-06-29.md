# Phase 10 Subplan: CLI And MCP Exposure

## Phase Objective

Expose the benchmarked high-level workflows through CLI and MCP surfaces.

## Entry Conditions Inherited From Previous Phase

- Question-level benchmark and quality thresholds pass.
- High-level workflow contracts are stable.

## Required Artifacts

- CLI commands for high-level workflows.
- MCP facade/server tools for high-level workflows.
- CLI/MCP tests.
- Phase 10 result record.
- Refreshed Phase 11 subplan.

## Required Checks, Tests, Reviews

- CLI command tests.
- MCP facade/server tests.
- Benchmark gate/quality report.
- Tool matrix or docs surface checks if needed.
- `python3 -m py_compile`.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can users access benchmarked high-level workflows through stable command/API surfaces? |
| Baseline/comparator | Existing CLI/MCP low-level workbench surfaces. |
| Primary pass criterion | CLI/MCP tools return the same high-level contract envelopes and do not expose unbenchmarked behavior. |
| Veto diagnostics | CLI/MCP drops non-claims; outputs differ from library function; tools claim certifying capability beyond evidence. |
| Explanatory diagnostics | CLI/MCP output snapshots and tool metadata. |
| Not concluded | Product/release readiness. |
| Artifact | CLI/MCP code/tests/result. |

## Forbidden Claims And Actions

- Do not expose a workflow that lacks Phase 9 benchmark coverage.
- Do not mark diagnostic-only tools as certifying-capable.
- Do not change public release policy.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 11 if CLI/MCP outputs match library contracts and benchmark
checks remain green.

## Stop Conditions

Stop if public surfaces cannot preserve non-claims or evidence classes.
