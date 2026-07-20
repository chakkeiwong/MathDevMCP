# Phase 05 Core Architecture Refactor Slices

## Objective

Execute one characterized slice for each remaining core refactoring direction:
derivation stages, validator rules, evidence storage, and maintainability debt
accounting. The backend-protocol slice closed in Phase 04 and is a frozen entry
condition here.

## Entry Conditions

Phase 04 interface slice is stable, reports zero import cycles, and the
coverage baseline identifies the highest-risk executable boundaries.

## Required Artifacts

- Pure document-derivation stage module with parity tests.
- Rule-pipeline validator slice with ordered findings and parity tests.
- Preserve the dependency-free external-backend protocol and injected Sage
  adapter completed in Phase 04.
- Evidence storage helpers separated from schema/publication code.
- Maintainability report with complexity, fan-out, and debt-budget fields.

## Checks

- Characterization and mutation tests before/after each moved boundary.
- Sage unavailable/timeout/malformed/success paths.
- Evidence symlink/tamper/no-overwrite/concurrency paths.
- Import graph and package import smoke.
- Full affected test sets and coverage delta.

## Evidence Contract

The only accepted refactor evidence is behavior-preserving parity plus reduced
coupling or bounded complexity. A smaller file is not evidence of correctness.

## Skeptical Audit

`PASS_AFTER_REVISION`. The original plan risked repeating the completed backend
work and treating line movement as progress. This revision requires one named,
pure seam per remaining direction, freezes exact finding/output order, and
uses pre/post characterization plus mutation checks. If a seam cannot be moved
without semantic changes, record that direction as a characterized blocker
rather than broadening the edit.

## Forbidden Claims/Actions

- Do not change mathematical semantics or promotion policy while moving code.
- Do not eliminate a cycle by importing the entire facade elsewhere.
- Do not hide unresolved debt by changing thresholds upward.

## Handoff Conditions

At least one safe slice per direction is complete, or the direction has a
written characterization blocker, owner, and next smallest slice.

## Stop Conditions

Stop when a move changes serialized output, evidence identity, backend status,
or scientific contract.
