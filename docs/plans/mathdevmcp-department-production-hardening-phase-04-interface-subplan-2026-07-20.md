# Phase 04 Interface And Maintainability Refactor Slice

## Objective

Reduce CLI/MCP interface-hub coupling while preserving command behavior,
FastMCP schemas, aliases, and output contracts.

## Entry Conditions

Phases 01-03 have characterization tests and a measurable coverage baseline.

## Required Artifacts

- Declarative CLI command metadata/adapters with thin dispatchers.
- MCP wrapper groups split by domain while retaining explicit typed signatures.
- Stable-profile catalog and experimental opt-in policy.
- Updated architecture notes and migration tests.

## Checks

- CLI help/snapshot/command contract tests.
- MCP schema, alias, stable-profile, and stdio tests.
- Import-cycle/fan-out/debt report.
- Full affected subsystem tests and coverage comparison.

## Evidence Contract

The refactor is accepted only if outputs and schemas are byte/field compatible
for stable paths. Line-count reduction is explanatory, not a promotion metric.

## Forbidden Claims/Actions

- Do not dynamically generate wrappers that erase inspectable signatures.
- Do not change stable arguments or output semantics silently.
- Do not refactor all large modules in one batch.

## Handoff Conditions

One interface boundary is extracted, characterized, and documented; debt does
not increase and stable-tool tests pass.

## Stop Conditions

Stop on schema drift, import-cycle growth, or a required scientific behavior
change.
