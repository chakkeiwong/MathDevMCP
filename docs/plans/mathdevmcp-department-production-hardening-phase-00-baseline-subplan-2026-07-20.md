# Phase 00 Baseline And Release-Claim Freeze

## Objective

Freeze the department-production question, preserve the dirty worktree, and
record exact baseline evidence before changing code.

## Entry Conditions

- Master program exists and is the current execution authority.
- Existing maintainer-handoff worktree changes are preserved.
- No active conflicting worker is writing the checkout.

## Required Artifacts

- Baseline command/result record.
- Release-claim ledger distinguishing local stdio, approved corpus, strict
  backend, and unsupported network deployment.
- Plan-audit record covering R01-R10, F01-F06, and T01-T10.

## Checks

- `git status --short --branch` and `git diff --check`.
- process/worker check and Git worktree lock check.
- `pytest --collect-only -q`.
- release-profile analysis for base, public, backend, latexml,
  private-corpus, and full.
- source/module/test inventory and tool availability check.

## Evidence Contract

The baseline must identify which claims are directly measured, which are
diagnostic, and which require department authority. It must not treat test
collection, file size, or a public-surface pass as production readiness.

## Forbidden Claims/Actions

- Do not reset, clean, stage, or revert unknown work.
- Do not call private-corpus/full readiness without a manifest.
- Do not install coverage/scanners into the active scientific environment.

## Handoff Conditions

Proceed when the baseline and plan audit are written and no unexpected worker
or overlapping edit is present.

## Stop Conditions

Stop if another active worker owns a target file, the deployment claim changes,
or the baseline cannot be reproduced.
