# Phase 4 Read-Only Review Bundle: V2 Regression Guard

Date: 2026-07-04

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

## Objective

Review Phase 4 of the MathDevMCP mission gap closure program for consistency,
correctness, feasibility, artifact coverage, and boundary safety.

Phase 4 is intentionally bounded: it turns an existing v2 downstream-agent
usefulness diagnostic into a regression guard. It does not collect new
model/API responses and does not claim a new product score.

## Artifacts To Inspect

- Result:
  `docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-result-2026-07-04.md`
- Subplan:
  `docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-subplan-2026-07-04.md`
- Next subplan:
  `docs/plans/mathdevmcp-mission-gap-closure-phase-05-compatibility-policy-subplan-2026-07-04.md`
- Test:
  `tests/test_downstream_usefulness_prompts.py`
- Frozen v2 artifacts guarded by the test:
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`
  `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`

## Local Check Summary

- `python3 -m pytest tests/test_downstream_usefulness_prompts.py`
  - `4 passed`
- `python3 -m json.tool` passed for the three frozen v2 JSON artifacts above.
- `git diff --check` passed for the Phase 4 test/result/subplan/handoff docs.

## Repair Since Review R1

Review r1 returned `REVISE` because the test did not assert the scoring
contract's explicit hard-veto-first `scoring_order` field. The test now asserts
the exact `scoring_order` sequence from
`.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`.

## Evidence Contract To Check

| Field | Contract |
| --- | --- |
| Question | Can the existing v2 diagnostic be guarded without benchmark-as-product drift? |
| Baseline | Prior final v2 bounded local diagnostic with hard vetoes 0/0/0 and required passes A/B/C = 6/5/6. |
| Primary criterion | Existing artifacts are parsed and guarded for hard-veto-first interpretation, no hidden retry, no Claude response worker, non-claims, and frozen comparison rule. |
| Veto diagnostics | New unapproved model/API collection, scoring changes after outputs, treating v2 as release/product proof, or weakening non-claims. |
| Not concluded | No new C-over-B score for Phase 1-3 product changes, release readiness, public benchmark validity, scientific validation, product-wide capability, proof, or model reliability. |

## Specific Review Questions

1. Does the Phase 4 result honestly state what was and was not established?
2. Does the added test guard the existing-artifact regression properties it
   claims to guard?
3. Is there any benchmark-as-mission drift or unsupported product/release claim?
4. Is the Phase 5 compatibility-policy handoff correct and safe?
5. Are there missing local checks or artifact mismatches that should block
   advancement?

Findings first. End with exactly:

VERDICT: AGREE

or

VERDICT: REVISE
