# P04 Subplan: Interface And Backend Boundaries

## Objective

Reduce CLI/facade hub coupling and eliminate the Sage/orchestrator/external
contract cycle without changing public schemas or mathematical semantics.

## Entry Conditions

P01-P03 production contracts, coverage, and performance baselines pass.

## Required Artifacts

- Dependency-free external adapter schemas and verifier protocol.
- Injected verifier composition route; no allowlisted three-module cycle.
- Declarative command/tool catalog boundary shared by release inspection and
  interface registration where safe.
- Domain registration helpers that reduce the central CLI parser and facade
  fan-out while preserving explicit typed FastMCP wrappers.

## Required Checks

- Exact adapter manifest and branch-orchestrator characterization tests.
- MCP registry, wrapper schema, CLI help/dispatch, release-cycle and import-cycle
  tests.
- Coverage and complexity deltas versus P00.

## Evidence Contract

Moving imports or lines is insufficient. Dependency direction must be explicit,
cycle count must decrease, and behavior/schema snapshots must remain equal.

## Forbidden Actions

- No dynamic untyped FastMCP wrapper generation.
- No hidden cycle through arbitrary lazy imports without a protocol boundary.
- No command removals or renames.

## Handoff

P05 begins when interface schemas are stable and the backend cycle is absent.

## Stop Conditions

An extraction changes a stable schema, output ordering, or certifying boundary.
