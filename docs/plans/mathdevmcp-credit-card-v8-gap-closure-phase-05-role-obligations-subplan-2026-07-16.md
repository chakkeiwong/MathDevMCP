# Phase 05 Subplan: Role-Specific Obligations

## Phase Objective

Generate local obligations appropriate to each routing role and separate local
correctness from downstream integration requirements.

## Entry Conditions Inherited From Previous Phase

- Cross-surface relation/role parity passes.
- Generic NPV spillover and false Bellman conformability blockers reproduce.

## Required Artifacts

- Builders for accounting identity, terminal definition, conditional
  expectation, LATE, randomization assumption, and Bellman recursion.
- Separate local and downstream obligation ledgers.
- Negative-control fixtures and relevance tests.
- `mathdevmcp-credit-card-v8-gap-closure-phase-05-result-2026-07-16.md`.

## Required Checks

- No baseline/terminal obligation on local PD/LGD/EAD or balance identities.
- No matrix-conformability blocker from scalar `\\star` notation.
- Conditional expectation, LATE, randomization, and Bellman receive the scoped
  assumptions listed in the predecessor plan.
- Generic theorem/default behavior remains available for unsupported roles.

## Evidence Contract

- Pass: obligation relevance is source/role scoped and negative controls hold.
- Veto: downstream valuation assumptions are presented as local identity
  requirements or predictive equations imply causal identification.
- Non-claim: proposed assumptions are candidate sufficient conditions, not
  established facts or globally minimal sets.

## Forbidden Claims And Actions

- Do not mark a stated randomization assumption as empirically satisfied.
- Do not call a Bellman expression optimal without domain/kernel/boundary
  evidence.

## Exact Next-Phase Handoff Conditions

Phase 06 may start when relevance tests pass independently of backend results.

## Stop Conditions

Stop a builder when role, relation, types, or exact source context are
ambiguous; return an actionable typed abstention instead.
