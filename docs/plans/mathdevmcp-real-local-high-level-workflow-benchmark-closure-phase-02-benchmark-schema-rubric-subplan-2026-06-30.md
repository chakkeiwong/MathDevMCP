# Phase 2 Subplan: Benchmark Schema And Rubric

Date: 2026-06-30

Status: `DRAFT_READY_AFTER_PHASE_1`

## Phase Objective

Convert the Phase 1 inventory into a durable benchmark schema and quality
rubric for real-local high-level workflow cases.

## Entry Conditions Inherited From Previous Phase

- Phase 1 candidate inventory exists with 5-10 bounded cases.
- Candidate cases have source anchors, workflow labels, expected evidence, and
  forbidden claims.
- The benchmark is still local/non-gating.

## Required Artifacts

- Real-local high-level workflow benchmark manifest or draft manifest under
  `benchmarks/real_tasks/holdout_local/`.
- Rubric/quality note under `docs/plans/`.
- Minimal derivation/proof review-packet schema with fields required for
  pre-repair and post-repair comparability: question, source anchors,
  assumptions, route availability, derivation/proof steps, backend checks,
  counterexamples, gaps, actions, evidence classes, and non-claims.
- Phase 2 result:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-02-benchmark-schema-rubric-result-2026-06-30.md`.
- Focused schema/tests if implementation is needed.
- Updated ledger entry and refreshed Phase 3 subplan review note.

## Required Checks, Tests, And Reviews

- Validate that every case records workflow type, question, source anchors,
  expected evidence classes, scoring rubric, negative-control status, and
  forbidden claims.
- Add or run focused schema tests if a loader/schema is implemented.
- Check that quality metrics cover source grounding, assumption correctness,
  derivation/proof validity, counterexample quality, backend evidence,
  abstention quality, and boundary discipline.
- Predeclare negative-control expected statuses and scoring semantics:
  `refuted`, `missing_assumptions`, `backend_unavailable`,
  `not_encodable`, `insufficient_evidence`, or routing-only.
- Define per-workflow evidence contracts to be used unchanged in Phase 4.
- Review with Claude if schema/rubric choices materially affect benchmark
  interpretation and review is allowed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the candidate cases be represented in a benchmark schema that measures real workflow quality instead of only pass count? |
| Baseline/comparator | Phase 1 inventory and existing seeded high-level benchmark conventions. |
| Primary criterion | Schema/rubric covers all candidate cases, negative controls with predeclared statuses, evidence classes, per-workflow scoring, good-abstention semantics, minimal packet schema, and non-claim boundaries. |
| Veto diagnostics | Single aggregate score as promotion criterion; missing negative controls; no abstention scoring; no source/backend evidence distinction; no minimal packet schema before baseline run; cases require unbounded source text. |
| Explanatory diagnostics | Schema validation, coverage table, rubric dimension table. |
| Not concluded | Current workflow performance or improved capability. |

## Forbidden Claims And Actions

- Do not claim benchmark quality from case count alone.
- Do not make local cases public or gating by default.
- Do not weaken non-claims to improve apparent pass rate.
- Do not encode gold answers that require unsupported scientific claims.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 when schema/rubric artifacts validate locally and make clear
what evidence can prove, refute, abstain, remain diagnostic, or count as a good
abstention.

## Stop Conditions

Stop if schema cannot represent assumptions, counterexamples, abstentions, and
boundary violations separately; if required source context exceeds safe bounds;
or if scoring requires human scientific judgment not encoded in the plan.

## End-Of-Phase Protocol

At phase end: run required checks; write the Phase 2 result; refresh/review the
Phase 3 subplan; review artifact coverage and boundary safety; then advance or
stop.
