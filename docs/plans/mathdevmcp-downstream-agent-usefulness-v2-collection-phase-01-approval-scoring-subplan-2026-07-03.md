# Phase 1 Subplan: Approval Packet And Scoring Contract

Date: 2026-07-03

Status: `EXECUTED_LOCALLY_PENDING_EXTERNAL_REVIEW_CONVERGENCE_COLLECTION_NOT_AUTHORIZED`

## Phase Objective

Create the explicit response-collection approval packet and freeze the scoring
contract that any future v2 response collection must use. This phase may
prepare approval artifacts, but it does not authorize or launch response
collection.

## Entry Conditions Inherited From Previous Phase

- Phase 0 candidate freeze manifest exists and parses:
  `.mathdevmcp/downstream_agent_usefulness_v2/collection_candidate_freeze_manifest.json`.
- V2 prompt manifest remains 18 prompts across 6 cases and A/B/C conditions.
- V2 prompt validation remains zero-error.
- V2 response artifact count remains zero.
- Repaired baseline primary hash check passed 11/11.
- Phase 0 Claude Opus review gate did not run to material review because Opus
  was unavailable through the current gateway.
- Human approved Sonnet max as substitute read-only reviewer for the bounded
  planning gate.
- No response-worker surface has been approved for collection.

## Required Artifacts

- Collection approval packet:
  `.mathdevmcp/downstream_agent_usefulness_v2/collection_approval_packet.md`.
- Frozen scoring contract:
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`.
- Phase 1 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-01-approval-scoring-result-2026-07-03.md`.
- Draft Phase 2 subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-02-preflight-gate-subplan-2026-07-03.md`.
- Claude review bundle for Phase 1/Phase 2 readiness:
  `docs/reviews/mathdevmcp-v2-collection-phase-01-review-bundle-2026-07-03.md`.
- Updated execution ledger and Claude review trail.

## Required Checks, Tests, Reviews

- Parse all v2 JSON artifacts, including the new scoring contract.
- Verify the approval packet explicitly names or marks as missing each required
  approval field:
  prompt manifest and count, response-worker surface, retry policy,
  malformed-output policy, scoring contract, and artifact paths.
- Verify the approval packet says collection remains unauthorized unless all
  required approval fields are explicitly human-approved.
- Verify the scoring contract freezes primary required dimensions before any
  responses and keeps candidate-only stressors explanatory unless a human
  explicitly approves them as primary before collection.
- Verify the scoring contract requires hard-veto-first scoring and forbids
  prompt-polish scoring.
- Verify v2 response artifact count remains zero.
- Verify prompt count remains 18 and prompt validation errors remain zero.
- Run focused pytest:
  `python3 -m pytest tests/test_downstream_usefulness_prompts.py`.
- Run `git diff --check` over v2 artifacts, plans, and review bundles.
- Claude Opus review remains blocked by reviewer-model availability. Human
  approved Sonnet max as substitute read-only reviewer. Treat this phase as
  externally reviewed only after a bounded reviewer verdict converges or after
  an explicit human waiver says local-only planning may continue.
- Local skeptical audit for wrong baseline, proxy metrics promoted to primary
  criteria, hidden approval assumptions, scoring drift, and Claude role
  confusion.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are the approval packet and scoring contract complete enough to support a later preflight gate without authorizing collection? |
| Baseline/comparator | Phase 0 candidate freeze manifest, v2 prompt manifest, v2 prompt validation, existing scoring applicability map, and repaired baseline scoring rubric. |
| Primary criterion | Phase 1 passes locally if the approval packet and scoring contract exist, parse/check cleanly, preserve the no-collection boundary, keep scoring frozen before responses, Phase 2 subplan exists, and local checks pass. External-review closure requires either a converged bounded reviewer verdict or explicit human waiver to continue local-only planning. |
| Veto diagnostics | Collection launched; response artifacts appear; response-worker surface silently assumed; Claude used as response worker; scoring criteria depend on seen responses; candidate-only stressors silently promoted; hard-veto-first scoring omitted; approval packet omits required human approval fields. |
| Explanatory diagnostics | Packet completeness table, scoring-contract fields, prompt count, validation status, response-artifact count, pytest result, review status. |
| Not concluded | No response quality, no scored v2 result, no C-over-B superiority, no public benchmark validity, no release readiness, no product capability, no scientific validation, no general model reliability. |

## Forbidden Claims Or Actions

- Do not collect responses.
- Do not use Claude as response worker.
- Do not assume the response-worker surface.
- Do not create response manifests, response directories, or scored-response
  files.
- Do not change scoring criteria after any future responses exist.
- Do not claim benchmark usefulness, C-over-B superiority, release readiness,
  scientific validation, product capability, public benchmark validity, or
  general model reliability.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- collection approval packet exists and explicitly enumerates all required
  approval fields;
- scoring contract exists, parses, and is frozen before collection;
- response artifact count remains zero;
- prompt validation remains clean;
- Phase 2 subplan exists and includes objective, inherited entry conditions,
  artifacts, checks/reviews, evidence contract, forbidden claims/actions,
  next-phase handoff, and stop conditions;
- either the Phase 1/Phase 2 bounded reviewer gate has converged with an
  acceptable verdict, or explicit human waiver/direction says Phase 2
  preflight planning may continue without treating Phase 1 as externally
  reviewed;
- pending reviewer-model direction remains a stop state, not a handoff
  condition;
- no response collection is authorized.

## Stop Conditions

Stop if:

- response collection would be needed to complete the phase;
- approval packet cannot enumerate all required human approval fields;
- scoring contract would require inspecting responses before freezing;
- response artifacts appear unexpectedly;
- prompt validation fails and cannot be repaired;
- Claude review returns `REVISE` and the issue cannot be repaired after five
  rounds;
- proceeding would require a response-worker decision, network/API/funding
  boundary, model-file change, package installation, or product/release/science
  claim.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 1 result/close record;
3. draft or refresh the Phase 2 subplan;
4. review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. run Claude read-only review gate on the compact bundle if the Phase 2 gate
   is material.
