# Phase 5 Subplan: Targeted Capability Repairs

Date: 2026-06-30

Status: `DRAFT_READY_AFTER_PHASE_4`

## Phase Objective

Repair high-level workflows only against observed Phase 4 failures, preserving
evidence boundaries and abstention quality.

## Entry Conditions Inherited From Previous Phase

- Phase 4 baseline failure table exists.
- Repair targets are categorized by workflow and failure class.
- Benchmark/rubric criteria are fixed unless a blocker result explicitly
  justifies schema repair.
- Phase 4 identified two material mismatches: `RLHLB-08` and `RLHLB-09`
  currently refute placeholder/semantic equality questions where the benchmark
  expects insufficiency or missing-assumption handling.
- `RLHLB-04` is a regression canary for the desired route-gap abstention path.

## Required Artifacts

- Focused code/test changes for affected workflow modules.
- Per-workflow repair notes.
- Updated benchmark result report.
- Anti-overfitting guard report covering unchanged seeded regression and a
  preregistered cross-case rerun set that was not directly targeted by each
  repair.
- Phase 5 result:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-05-targeted-capability-repairs-result-2026-06-30.md`.
- Updated ledger entry and refreshed Phase 6 subplan review note.

## Required Checks, Tests, And Reviews

- Run affected unit tests and benchmark replay after each material repair.
- Verify failures shrink or convert to correct abstentions without weakening
  boundary checks.
- Verify each material repair against both its target case and the
  preregistered untouched rerun set, including `RLHLB-04` as a route-gap
  canary.
- Mutation/negative-control checks for false proof/refutation confidence.
- Claude review for material semantic repairs if permitted.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can targeted repairs improve real-local workflow behavior without weakening evidence boundaries? |
| Baseline/comparator | Phase 4 current-workflow baseline report. |
| Primary criterion | Observed failures are repaired, correctly abstained, or documented as residual; no negative-control, untouched-rerun, seeded-regression, or boundary-discipline regression. |
| Veto diagnostics | Benchmark overfitting by changing gold labels; weakening non-claims; hiding residuals; treating source/diagnostic evidence as proof; placeholder-symbol equality refuted without semantic/source route; losing seeded benchmark behavior; repair improves target case but breaks untouched rerun set. |
| Explanatory diagnostics | Before/after failure table, per-workflow tests, mutation probes, seeded benchmark regression. |
| Not concluded | General theorem proving, correctness outside benchmark scope, or release readiness. |

## Forbidden Claims And Actions

- Do not repair by changing benchmark expectations after seeing failures unless
  a blocker result proves the benchmark was wrong.
- Do not remove negative controls to improve scores.
- Do not add unsupported assumptions silently.
- Do not claim proof without certifying evidence.
- Do not install new packages without explicit approval.
- Do not globally weaken all symbolic refutations; restrict the repair to
  semantic placeholder/source-boundary questions that lack a certifying route.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 when repaired workflow outputs are stable enough to package
as durable derivation/proof review packets, and all remaining residuals are
explicit.

## Stop Conditions

Stop if repairs require new dependencies, extensive formalization, scientific
judgment outside local evidence, or a change to program direction.

## End-Of-Phase Protocol

At phase end: run checks; write the Phase 5 result; refresh/review Phase 6
subplan; review residual boundaries; then advance or stop.
