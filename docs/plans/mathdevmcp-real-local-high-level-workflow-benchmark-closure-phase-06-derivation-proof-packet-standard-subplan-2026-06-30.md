# Phase 6 Subplan: Derivation And Proof Packet Standard

Date: 2026-06-30

Status: `DRAFT_READY_AFTER_PHASE_5`

## Phase Objective

Harden the minimal Phase 2 packet schema into durable review packets for
high-level workflow answers, bundling question, source anchors, assumptions,
derivation/proof steps, backend checks, counterexamples, gaps, and non-claims.

## Entry Conditions Inherited From Previous Phase

- Phase 5 repaired or residual benchmark behavior is known.
- Per-case outputs expose source/backend/evidence/gap information.
- No unsupported proof/release/scientific claim is pending.

## Required Artifacts

- Packet schema or contract update extending the Phase 2 minimal schema.
- Tests for packet completeness and boundary preservation.
- Example packets for representative benchmark cases.
- Phase 6 result:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-06-derivation-proof-packet-standard-result-2026-06-30.md`.
- Updated ledger entry and refreshed Phase 7 subplan review note.

## Required Checks, Tests, And Reviews

- Run review-packet tests and affected workflow tests.
- Verify packets preserve source/backend/probe/residual separation.
- Verify unresolved gaps and non-claims are present.
- Claude review if packet semantics materially affect user-facing claims and
  review is allowed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can benchmarked high-level answers produce reviewable packets without turning diagnostics into proof? |
| Baseline/comparator | Phase 2 minimal packet schema, existing `prepare_review_packet` output, and Phase 5 benchmark results. |
| Primary criterion | Packets include question, sources, assumptions, steps, tool checks, counterexamples/gaps, actions, non-claims, and evidence classes for representative cases. |
| Veto diagnostics | Packet omits residual gaps; packet claims certificate status without backend; source text overcopied; review aid treated as proof. |
| Explanatory diagnostics | Packet completeness table, focused tests, example packet summaries. |
| Not concluded | Human acceptance, formal proof, release readiness, or scientific validity. |

## Forbidden Claims And Actions

- Do not call review packets certificates unless a certifying backend is
  actually present and scoped.
- Do not include large source excerpts.
- Do not hide uncertainty or human-review requirements.
- Do not change benchmark pass criteria in packet work.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 7 when packets are stable and documentation/promotion policy
can describe exactly what benchmarked workflow outputs mean.

## Stop Conditions

Stop if packet generation cannot represent residual gaps/non-claims or if
source context would need to be copied beyond bounded anchors.

## End-Of-Phase Protocol

At phase end: run checks; write Phase 6 result; refresh/review Phase 7
subplan; then advance or stop.
