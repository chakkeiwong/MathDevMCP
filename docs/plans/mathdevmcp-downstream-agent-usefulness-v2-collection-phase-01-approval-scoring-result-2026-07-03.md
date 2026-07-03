# Phase 1 Result: Approval Packet And Scoring Contract

Date: 2026-07-03

Status: `PASSED_COLLECTION_NOT_AUTHORIZED`

## Phase Objective

Create the explicit response-collection approval packet and freeze the scoring
contract that any future v2 response collection must use, without authorizing
or launching collection.

## Entry Conditions

- Phase 0 candidate freeze manifest exists and parses.
- V2 prompt manifest remains 18 prompts across 6 cases and A/B/C conditions.
- V2 prompt validation remains zero-error.
- V2 response artifact count remains zero.
- Repaired baseline primary hash check passed 11/11 in Phase 0.
- Phase 0 Claude Opus review did not run to material review because the Opus
  reviewer model was unavailable through the current gateway.
- Human approved Sonnet max as substitute read-only reviewer.
- No response-worker surface has been approved for collection.

## Artifacts Produced

- Collection approval packet:
  `.mathdevmcp/downstream_agent_usefulness_v2/collection_approval_packet.md`.
- Frozen scoring contract:
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`.
- Draft Phase 2 subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-02-preflight-gate-subplan-2026-07-03.md`.
- Phase 1 review bundle retained for audit but not sent because Opus remained
  unavailable and no substitute reviewer direction had been given:
  `docs/reviews/mathdevmcp-v2-collection-phase-01-review-bundle-2026-07-03.md`.

## Local Checks

| Check | Result |
| --- | --- |
| Parse v2 JSON artifacts including scoring contract | Passed: 10 JSON files parsed |
| Prompt count | Passed: 18 |
| Prompt validation | Passed: 0 errors |
| Approval packet field enumeration | Passed: all required fields enumerated |
| Scoring contract prompt-manifest hash | Passed: matches `340ec24f062dc614d6e03a7d279a74539c8e033fef499ef3fc127e2722736bfe` |
| Scoring contract collection flag | Passed: `collection_authorized_by_this_contract=false` |
| V2 response artifact count | Passed: 0 |
| Focused pytest | Passed: `python3 -m pytest tests/test_downstream_usefulness_prompts.py`, 3 tests |
| Diff whitespace | Passed: `git diff --check -- .mathdevmcp/downstream_agent_usefulness_v2 docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-*.md docs/reviews/mathdevmcp-v2-collection-phase-*.md` |

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Answered: approval/scoring artifacts are complete enough for Phase 2 preflight, but not collection. |
| Baseline/comparator | Phase 0 freeze manifest, v2 prompt manifest, v2 prompt validation, scoring applicability map, and repaired baseline rubric. |
| Primary criterion | Passed locally: approval packet and scoring contract exist, parse/check cleanly, preserve no-collection boundary, keep scoring frozen before responses, Phase 2 subplan exists, and local checks passed. External-review closure requires a converged bounded reviewer verdict or explicit human waiver for local-only planning. |
| Veto diagnostics | No collection launched; no response artifacts appeared; no Claude response-worker use; no scoring-after-response drift; hard-veto-first scoring preserved. |
| Explanatory diagnostics | Packet completeness, scoring contract fields, prompt count, validation status, response artifact count, pytest result. |
| Not concluded | No response quality, scored v2 result, C-over-B superiority, public benchmark validity, release readiness, product capability, scientific validation, or general model reliability. |

## Approval Completeness

The approval packet deliberately records collection as incomplete:

- prompt manifest/count: proposed, pending explicit approval;
- response-worker surface: missing required approval;
- retry policy: proposed, pending explicit approval;
- malformed-output policy: proposed, pending explicit approval;
- scoring contract: proposed, pending explicit approval;
- artifact paths: proposed, pending explicit approval.

Because the response-worker surface and other fields are not explicitly
approved, Phase 2 must stop before collection unless the missing approvals are
provided.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 2 preflight/collection gate | Passed for approval/scoring preparation | No veto fired | Whether human will approve the exact collection scope and response-worker surface | Run Phase 2 preflight and stop if approval remains incomplete | No response quality, C-over-B superiority, collection authorization, or public/release/scientific/product claim |

## Next-Phase Handoff

Phase 2 may run local preflight checks. It must stop with
`BLOCKED_PENDING_COLLECTION_APPROVAL` unless explicit human approval names:

- the 18-prompt manifest;
- a non-Claude response-worker surface;
- one-attempt/no-hidden-retry policy or another predeclared retry design;
- malformed-output preservation policy;
- the frozen scoring contract;
- response, response-manifest, and scored-output artifact paths.
