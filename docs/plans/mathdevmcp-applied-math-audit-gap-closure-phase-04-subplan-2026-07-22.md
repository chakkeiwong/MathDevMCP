# Phase 04 Subplan: Source-First Discovery And Specialists

## Objective

Discover adjacent source/code/data artifacts and invoke compatible specialists
through typed, bounded adapters.

## Entry Conditions

Phase 03 traces are stable and source identity is enforced.

## Required Artifacts

Discovery manifest, specialist registry/adapter, Dynare invocation record,
injected-runner tests, and a Phase 04 result.

## Required Checks/Tests/Reviews

Test deterministic local discovery, provider identity, typed Dynare operations,
timeout/nonzero output, input/output digests, and path confinement.

## Evidence Contract

Record provider root/commit/dirty state, exact operation, input digest, output
digest, status, and non-claim. Backend evidence is separate from inference.

## Forbidden Claims/Actions

No arbitrary shell execution, unknown code execution, or claim of paper/code
semantic equivalence from a specialist result.

## Exact Handoff Conditions

Every route is reproducible or visibly abstains; non-Dynare documents remain
unaffected by the optional adapter.

## Stop Conditions

Stop if a route lacks input identity or hides backend/provider failure.
