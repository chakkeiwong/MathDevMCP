# Phase 00 Subplan: Baseline And Contract Freeze

## Objective

Freeze the prior orchestrator baseline and the issue-level comparison rules so
later implementation changes answer the same question.

## Entry Conditions

The prior orchestrator source, focused tests, Boehl blind artifacts, and
remaining-gap report are readable. The current worktree may remain dirty; all
pre-existing changes are preserved.

## Required Artifacts

`docs/plans/mathdevmcp-applied-math-audit-gap-closure-master-program-2026-07-22.md`,
this subplan, a baseline manifest, and a Phase 00 result record.

## Required Checks/Tests/Reviews

Inspect git status and prior artifact hashes; run the existing applied-math
focused tests; verify the 12-family disposition vocabulary; review this plan
for metric leakage and stale assumptions.

## Evidence Contract

The prior Boehl scores are descriptive corpus evidence. Obligation count is not
a promotion metric. The answer key is sealed until a blind output is written.

## Forbidden Claims/Actions

Do not edit prior blind artifacts, tune against the answer key, or make
DynareMCP a required dependency.

## Exact Handoff Conditions

Baseline manifest records paths, digests, commands, and known failures; focused
tests pass or failures are classified; Phase 01 subplan is reviewed and ready.

## Stop Conditions

Stop only if prior artifacts are unavailable or source drift makes a fair
comparison impossible.
