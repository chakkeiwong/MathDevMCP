# Phase 06 Final Department Gate And Close

## Objective

Run the settled artifact through the complete department gate, classify all
remaining residuals, and issue the strongest justified release verdict.

## Entry Conditions

Phases 01-05 have result records; no unresolved engineering veto remains for
the selected department claim.

## Required Artifacts

- One settled full-test result.
- Coverage, skip, scanner, SBOM, wheel, lock, corpus, and release-manifest
  artifacts.
- Department owner approval and rollback reference.
- `mathdevmcp-department-production-hardening-result-2026-07-20.md`.

## Checks

- Clean worktree/tag/release identity.
- Wheel install on Python 3.11 and 3.12.
- Required department corpus/full profile.
- Complete tests, coverage threshold, security/supply-chain checks.
- MCP stable-profile smoke and experimental opt-in smoke.
- Rollback rehearsal.

## Evidence Contract

The result must say `ready`, `ready_with_scoped_residuals`, or `not_ready`, and
list exact vetoes. It must not upgrade an internal-beta result to production
merely because the public surface check passes.

## Forbidden Claims/Actions

- Do not tag or distribute until the release artifact and owner approval bind
  the same commit/digest.
- Do not omit unavailable strict evidence from the result.

## Handoff Conditions

The close record is complete, the release claim matches profile evidence, and
the next maintenance owner can reproduce the gate.

## Stop Conditions

Stop with `not_ready` for any P0 veto, missing owner/corpus authority, dirty
release identity, failing settled full suite, or unmeasured critical coverage.
