# Phase 4 Result: V2 Regression Guard

Date: 2026-07-04

Status: `COMPLETE_LOCAL_CHECKS_AND_READ_ONLY_REVIEW_AGREED`

Subplan:

- `docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-subplan-2026-07-04.md`

## Phase Objective Result

Phase 4 converted the existing v2 downstream-agent usefulness diagnostic into a
tracked regression guard. No new model/API responses were collected, no scoring
contract was changed, and no new product-score claim was made.

The guard now checks that the frozen v2 artifacts keep their hard-veto-first
shape, no-hidden-retry collection record, no-Claude-response-worker boundary,
candidate comparison rule, and explicit non-claims.

## Skeptical Audit

- Wrong baseline avoided: Phase 4 used the prior final v2 bounded local
  diagnostic as the baseline, not a new unapproved collection.
- Proxy metric risk contained: the v2 C-over-B result is treated as a local
  diagnostic and regression guard, not product success, release readiness, or
  proof.
- Missing stop conditions avoided: the subplan forbids new model/API response
  collection without explicit approval.
- Unfair comparison avoided: scoring criteria were not changed after seeing
  outputs.
- Hidden assumption recorded: without new collection, Phase 4 cannot measure
  whether the Phase 1-3 product surface changes improve model responses.
- Artifact fit: the added test directly guards the existing scored artifact,
  response manifest, scoring contract, and non-claim boundaries.

Audit result: `PASS_FOR_BOUNDED_EXISTING_ARTIFACT_REGRESSION_GUARD`.

## Evidence Changed

Added test:

- `tests/test_downstream_usefulness_prompts.py::test_v2_scored_artifacts_remain_bounded_regression_guard`

The test parses:

- `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`

Guarded properties:

- 18 scored rows and 18 response-manifest rows remain present.
- Response artifacts in the scored rows match response-manifest paths.
- Hard vetoes remain A/B/C/total = 0/0/0/0.
- Required passes remain A/B/C = 6/5/6.
- No response row records Claude as response worker.
- All response rows record no hidden retry.
- No response row is marked malformed.
- The minimum candidate rule remains B comparator vs C candidate,
  aggregate-only comparison remains forbidden, and the improved case remains
  `V2-PRP-01-gaussian-score-review-packet`.
- The scoring order preserves malformed-output recording, hard-veto
  application, primary scoring, explanatory scoring, per-case B-vs-C delta, and
  hard-veto-before-pass-count summary.
- The scoring contract remains non-authorizing for collection.
- Public-benchmark, release, scientific, and product-capability non-claims stay
  visible.

## Repair Record

First read-only review returned `REVISE` because the result claimed the guard
preserved hard-veto-first interpretation, but the test did not assert the
contract's explicit `scoring_order` field. The repair added an exact
`scoring_order` assertion to
`tests/test_downstream_usefulness_prompts.py::test_v2_scored_artifacts_remain_bounded_regression_guard`.

## Local Checks Run

Commands and results:

- `python3 -m pytest tests/test_downstream_usefulness_prompts.py`
  - initial result: `4 passed in 0.03s`
  - result after scoring-order repair: `4 passed in 0.04s`
- `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`
  - result: passed
- `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`
  - result: passed
- `python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`
  - result: passed
- `git diff --check -- tests/test_downstream_usefulness_prompts.py docs/plans/mathdevmcp-mission-gap-closure-phase-04-v2-regression-guard-subplan-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-phase-05-compatibility-policy-subplan-2026-07-04.md docs/plans/mathdevmcp-mission-gap-closure-visible-execution-ledger-2026-07-04.md`
  - result: passed

## Decision Table

| Field | Result |
| --- | --- |
| Decision | Phase 4 complete: local checks passed after focused repair and bounded read-only review r2 agreed. |
| Primary criterion status | Partially passed: guard readiness is implemented and checked; no new replay/collection result exists. |
| Veto diagnostic status | No veto triggered: no scoring change, no new collection, no benchmark-as-product claim, and hard-veto-first interpretation remains guarded. |
| Main uncertainty | The Phase 1-3 product changes have not been rescored through a new response collection, so no new downstream-usefulness delta is known. |
| Next justified action | Advance to Phase 5 compatibility policy if read-only review agrees with the bounded interpretation. |
| Not concluded | No new C-over-B score, no public benchmark validity, no downstream-agent reliability, no release readiness, no scientific validation, and no product-wide capability claim. |

## Phase 5 Subplan Refresh

Phase 5 should inherit:

- the v2 diagnostic is now guarded as existing local evidence;
- compatibility policy must not claim unknown exact-schema external consumer
  compatibility;
- additive `agent_handoff` remains a repo-local product surface unless a
  strict external schema mode is separately designed and tested.

## Forbidden Claims Retained

This result does not claim:

- a new model/API response collection;
- a new C-over-B score for the Phase 1-3 product changes;
- release readiness;
- product-wide readiness;
- public benchmark validity;
- downstream-agent reliability;
- scientific validation;
- proof or semantic implementation correctness.

## Read-Only Review Trail

First Phase 4 review:

- `REVIEW_STATUS=revise`
- `VERDICT=REVISE`
- `RUN_DIR=/home/chakwong/python/MathDevMCP/.claude_reviews/20260704-045411-mathdevmcp-mission-gap-closure-phase-04`
- Material finding: the test did not assert the scoring contract's explicit
  hard-veto-first `scoring_order`.

Repair:

- Added exact `scoring_order` coverage to the v2 regression guard test.

Second Phase 4 review:

- `REVIEW_STATUS=agreed`
- `VERDICT=AGREE`
- `RUN_DIR=/home/chakwong/python/MathDevMCP/.claude_reviews/20260704-045743-mathdevmcp-mission-gap-closure-phase-04-r2`
- `SUMMARY_JSON=/home/chakwong/python/MathDevMCP/.claude_reviews/20260704-045743-mathdevmcp-mission-gap-closure-phase-04-r2/status.json`
- Reviewer confirmed the scoring-order repair closes the r1 hard-veto-first
  coverage gap for this bounded regression-guard phase.
