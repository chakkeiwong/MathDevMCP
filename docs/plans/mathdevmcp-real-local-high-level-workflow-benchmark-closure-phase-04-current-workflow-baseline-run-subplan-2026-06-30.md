# Phase 4 Subplan: Current Workflow Baseline Run

Date: 2026-06-30

Status: `DRAFT_READY_AFTER_PHASE_3`

## Phase Objective

Run the current high-level workflows on the real-local benchmark before
targeted repairs, preserving an honest failure table.

## Entry Conditions Inherited From Previous Phase

- Benchmark schema/rubric exists.
- Evidence routes are stable enough to run without changing criteria.
- Pass/fail/partial/abstain/wrong/boundary-violation taxonomy is fixed before
  the run.
- Phase 3 route ledger exists for all nine frozen cases and records Lean as
  route availability only unless an explicit proof/source artifact is supplied.

## Required Artifacts

- Baseline report JSON/Markdown under `.mathdevmcp/` and `docs/plans/`.
- Per-case result table with workflow, status, evidence classes, failure class,
  and non-claims.
- Workflow-family evidence contract table with comparator, primary criterion,
  veto diagnostics, explanatory-only diagnostics, and good-abstention semantics.
- Pre-repair packet artifacts or summaries using the Phase 2 minimal packet
  schema.
- Phase 4 result:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-04-current-workflow-baseline-run-result-2026-06-30.md`.
- Updated ledger entry and refreshed Phase 5 subplan review note.

## Required Checks, Tests, And Reviews

- Run the benchmark runner or focused workflow calls over all cases.
- Validate deterministic rerun for statuses and evidence classes.
- Validate the Phase 2 manifest/rubric and Phase 3 route ledger are unchanged
  before running and rerunning the baseline.
- Validate that each negative control lands in its predeclared expected status
  family or is marked benchmark/schema issue rather than silently rescored.
- Inspect per-case failures; do not rely only on aggregate score.
- Review baseline interpretation with Claude if results are materially
  ambiguous and review is allowed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | How do current high-level workflows perform on the real-local benchmark before repairs? |
| Baseline/comparator | Phase 0 current seeded baseline and Phase 2 real-local benchmark. |
| Primary criterion | Every case has a recorded current-workflow result, route ledger reference, packet summary, and failure taxonomy; no result overclaims evidence; aggregate metrics are diagnostic only. |
| Veto diagnostics | Changing rubric after seeing results; hiding wrong or boundary-violating cases; collapsing partial/abstain/wrong; accepting prose-only pass; Lean availability treated as proof without explicit proof source; artifact does not answer the case question; claiming improvement before repairs. |
| Explanatory diagnostics | Per-case statuses, failure classes, evidence classes, deterministic rerun stability. |
| Not concluded | Final capability quality or repair success. |

## Forbidden Claims And Actions

- Do not modify workflows to improve the baseline run.
- Do not discard hard cases after seeing failures.
- Do not turn diagnostic aggregate rates into promotion criteria.
- Do not claim failure of a workflow idea when the failure may be routing,
  encoding, or missing-backend related.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 when the baseline failure table clearly identifies repair
targets and separates implementation gaps, benchmark/schema gaps, evidence
gaps, and legitimate abstentions.

## Stop Conditions

Stop if the benchmark runner cannot produce reproducible per-case reports, if
the rubric is discovered to be invalid, or if results require a human
scientific judgment not encoded in the benchmark. Mark cases non-evaluable if
they pass only via prose without routed evidence or via adapter mismatch.

## End-Of-Phase Protocol

At phase end: run checks; write the Phase 4 result; refresh/review Phase 5
subplan against the observed failure table; then advance or stop.
