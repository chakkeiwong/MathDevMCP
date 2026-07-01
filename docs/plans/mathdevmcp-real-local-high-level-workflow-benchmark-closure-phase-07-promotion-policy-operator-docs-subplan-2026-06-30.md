# Phase 7 Subplan: Promotion Policy And Operator Docs

Date: 2026-06-30

Status: `DRAFT_READY_AFTER_PHASE_6`

## Phase Objective

Document how real-local benchmark results, repaired manifests, and review
packets may be used, and decide whether any artifact remains local/non-gating
or becomes a candidate for a later formal gate.

## Entry Conditions Inherited From Previous Phase

- Phase 6 packet standard exists.
- Benchmark results and residuals are explicit.
- No default release or benchmark policy has been changed.

## Required Artifacts

- Operator docs updates.
- Promotion/non-promotion policy note.
- Explicit default-policy non-promotion decision artifact unless a separate
  governed promotion decision is created.
- Docs grep evidence.
- Phase 7 result:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-07-promotion-policy-operator-docs-result-2026-06-30.md`.
- Updated ledger entry and refreshed Phase 8 subplan review note.

## Required Checks, Tests, And Reviews

- Grep docs for forbidden affirmative claims.
- Run docs/support-matrix tests if touched.
- Verify benchmark gate does not silently include local artifacts unless a
  separate reviewed promotion decision exists.
- Claude review for policy wording if permitted.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do docs and policy describe the benchmarked high-level workflows without overclaiming or accidental promotion? |
| Baseline/comparator | Existing high-level workflow docs and source-adapter local/non-gating policy. |
| Primary criterion | Docs explain capabilities, artifacts, limitations, local/non-gating status, abstention calibration limits, and promotion requirements; forbidden-claim checks pass. |
| Veto diagnostics | Release-readiness/public-validity/scientific/broad-proof claims; claim that abstention quality is calibrated outside these cases; local cases inserted into formal gate without policy; repaired manifest treated as frozen result. |
| Explanatory diagnostics | Grep output, docs tests, policy table. |
| Not concluded | Actual promotion to public benchmark or release readiness. |

## Forbidden Claims And Actions

- Do not promote local benchmark cases to public/gating fixtures in this phase
  unless a separate reviewed decision is made.
- Do not claim external reproducibility from local-only sources.
- Do not claim abstention quality is calibrated outside the benchmarked local
  cases.
- Do not erase residual risks.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 8 when docs/policy are coherent and final regression can test
code, benchmark, docs, and non-claim boundaries together.

## Stop Conditions

Stop if docs need a project-direction decision about public release, private
source disclosure, or default benchmark policy.

## End-Of-Phase Protocol

At phase end: run checks; write Phase 7 result; refresh/review Phase 8
subplan; then advance or stop.
