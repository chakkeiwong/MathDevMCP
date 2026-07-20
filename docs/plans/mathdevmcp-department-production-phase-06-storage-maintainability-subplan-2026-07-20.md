# P06 Subplan: Storage And Maintainability Ratchet

## Objective

Separate security-sensitive artifact storage from scientific manifest schemas
and replace the coarse size ceiling with actionable debt budgets.

## Entry Conditions

P05 workflow contracts pass and coverage can measure extracted modules.

## Required Artifacts

- Artifact-store module owning safe-root resolution, canonical/no-follow reads,
  atomic no-replace writes, permissions, and directory durability.
- Evidence manifest imports/re-exports preserving compatibility.
- Maintainability report with per-hotspot baselines, counts over size/complexity
  thresholds, fan-out, cycle budget, and touched-hotspot improvement rule.
- Architecture/debt documentation for the junior maintainer.

## Required Checks

- All evidence manifest, artifact, resumability, tamper, symlink, traversal,
  short-write, permission, and concurrency tests.
- Maintainability negative fixtures for each budget.
- Static, coverage, and import-cycle gates.

## Evidence Contract

The storage extraction passes only if security behavior is unchanged or
strictly stronger. A new report with the same maximum file size but more large
files must fail.

## Forbidden Actions

- No overwrite fallback, symlink following, permission weakening, or mutable
  manifest publication.
- No debt-baseline increase to make a regression pass.

## Handoff

P07 begins when storage security tests pass and maintainability debt cannot grow
silently.

## Stop Conditions

Platform filesystem semantics cannot preserve a tested invariant, or the move
changes persisted bytes.
