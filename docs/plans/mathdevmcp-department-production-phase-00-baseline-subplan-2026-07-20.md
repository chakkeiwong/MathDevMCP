# P00 Subplan: Baseline And Characterization

## Objective

Freeze the production question, current profile results, public contracts,
complexity/coupling debt, and test inventory before implementation.

## Entry Conditions

- Master program and skeptical audit exist.
- The maintainer-handoff change set is stable but uncommitted.
- No concurrent worker is modifying overlapping files.

## Required Artifacts

- Traceability tables in the master program.
- Baseline reports for profiles, MCP stability counts, test collection,
  complexity, import cycles, and direct-test mapping.
- Characterization tests for release profile vocabulary and public output
  contracts touched later.

## Checks And Evidence Contract

The baseline commands must answer what exists, not whether it is good. Record
exact counts and statuses; do not turn line count or test count into a pass
criterion.

## Forbidden Actions

- No refactoring before characterization.
- No claim that the dirty tree is a release artifact.
- No substitution of sanitized fixtures for approved department evidence.

## Handoff

P01 begins when the ten blockers and six refactors have explicit baseline
evidence and tests can detect release-profile/surface drift.

## Stop Conditions

Unexpected file changes or a baseline contradiction that changes program scope.
