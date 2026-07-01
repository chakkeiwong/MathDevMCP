# Phase 3 Subplan: Backend Grounding Evidence Layer

Date: 2026-06-30

Status: `DRAFT_READY_AFTER_PHASE_2`

## Phase Objective

Ensure high-level workflow answers can attach concrete evidence from existing
source adapters, symbolic checks, counterexample search, proof-gap localization,
code/equation comparison, or explicit abstention.

## Entry Conditions Inherited From Previous Phase

- Phase 2 schema/rubric exists and identifies required evidence classes.
- Phase 2 manifest freezes `expected_case_count: 9`; Phase 3 must not add,
  remove, or reclassify cases.
- Phase 2 workflow contracts include `result_artifact`, requiring each case to
  preserve a per-case packet plus route-availability ledger row in later
  phases.
- Current backend/tool availability is known from Phase 0.
- No real-local benchmark performance claim has been made.

## Required Artifacts

- Evidence routing notes or code changes for workflow/backend integration.
- Route-availability ledger per benchmark case:
  source adapter present/absent, symbolic backend present/absent,
  counterexample path attempted/skipped, proof/formal backend state,
  code/equation route present/absent, and residual unresolved.
- Per-case packet stubs satisfying the Phase 2 minimal review-packet schema;
  these stubs may contain empty lists for unavailable evidence but must not
  omit required fields.
- Focused tests for evidence routing and abstention behavior.
- Phase 3 result:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-03-backend-grounding-evidence-result-2026-06-30.md`.
- Updated ledger entry and refreshed Phase 4 subplan review note.

## Required Checks, Tests, And Reviews

- Run focused tests for existing workflow modules and backend helpers affected
  by the phase.
- Verify backend-unavailable remains distinct from refutation.
- Verify structural/numeric/generated-test/review-packet evidence is not
  promoted to proof.
- Verify every case can emit the minimal packet schema from Phase 2, even when
  the status is abstention, backend unavailable, or inconclusive.
- Review material evidence-router changes with Claude if permitted.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do high-level workflows have a safe path to concrete evidence or explicit abstention for the real-local benchmark schema? |
| Baseline/comparator | Existing workflow evidence classes and lower-level tools. |
| Primary criterion | Each benchmark case has a route-availability ledger, each workflow family has a declared source/backend/diagnostic/abstention evidence route, minimal packet output is possible, and tests preserve boundaries. |
| Veto diagnostics | Backend absence becomes refutation; structural match becomes proof; numeric check becomes theorem proof; source adapter used beyond its local schema; missing evidence hidden; route availability not operationalized per case; Phase 2 nine-case manifest or status semantics changed silently. |
| Explanatory diagnostics | Evidence-route table, focused test results, unavailable-backend diagnostics. |
| Not concluded | Actual benchmark pass rate or proof of real-local claims. |

## Forbidden Claims And Actions

- Do not add new heavyweight dependencies or network fetches.
- Do not edit sibling repos.
- Do not claim formal proof unless a formal backend actually certifies the
  scoped claim.
- Do not silently insert assumptions to make a derivation pass.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 when evidence routes are stable enough to run current
workflows on the benchmark without changing pass criteria after results, and
the route ledger plus packet stubs can explain pass/partial/abstain outcomes
for all nine frozen cases.

## Stop Conditions

Stop if required evidence needs unavailable packages, network, formalization
work beyond the phase, a scientific judgment boundary, or any change to the
Phase 2 frozen manifest/rubric that has not been written as a blocker/schema
repair result.

## End-Of-Phase Protocol

At phase end: run checks; write the Phase 3 result; refresh/review Phase 4
subplan; review boundary safety; then advance or stop.
