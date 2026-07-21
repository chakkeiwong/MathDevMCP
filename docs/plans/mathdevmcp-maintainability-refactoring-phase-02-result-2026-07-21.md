# Phase 02 Result: Immutable Backend Configuration

Date: 2026-07-21
Status: closed

## Objective

Resolve backend selection once per request without mutating process-global
environment state, while preserving no-argument helper behavior and diagnostic
contracts.

## Evidence

- Added frozen `BackendConfig` and propagated it through backend executable,
  Python, doctor, Lean readiness, and document workflow checks.
- Added request-local configuration tests, including concurrent distinct
  toolchain environments and process-environment non-mutation.
- Replaced release-policy environment mutation with an explicit config.
- Preserved the historical document-tree Lean toolchain default only inside its
  compatibility scope; generic backend config does not invent a default.

## Checks

| Check | Result |
|---|---|
| Focused doctor/document/readiness tests | 51 passed, 1 skipped |
| Backend lane | 120 passed, 1 skipped |
| Release caveat closure tests | passed in focused combined run |
| Compile and diff checks | passed |

## Decision

Closed. The evidence establishes engineering isolation only. It does not
establish backend availability, Lean certification, or mathematical validity.

## Handoff

Phase 03 may proceed with compatibility-preserving document-audit seams.
