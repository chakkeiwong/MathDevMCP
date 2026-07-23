# Phase 04 Subplan: Single Public Orchestrator

## Objective

Expose one compact-by-default LLM-facing function through library, CLI, facade,
and all-profile MCP surfaces.

## Entry Conditions

Phases 01--03 pass their contracts and focused tests.

## Required Artifacts

Orchestrator module, CLI/facade/server wiring, documentation, interface tests,
and a phase result note.

## Required Checks

PDF and TeX smoke calls, mode/policy validation, compact/detailed behavior,
artifact persistence, MCP surface synchronization, and CLI help.

## Evidence Contract

Compact output contains status, coverage, routes, warnings, non-claims, and an
artifact handle; detailed output contains the full audit envelope.

## Forbidden Claims/Actions

No unbounded response, publication/release authority, source edit, or silent
model execution.

## Handoff Conditions

One call returns a valid `applied_math_audit` contract and its artifact resolves.

## Stop Conditions

Stop if library, CLI, facade, and server schemas diverge.
