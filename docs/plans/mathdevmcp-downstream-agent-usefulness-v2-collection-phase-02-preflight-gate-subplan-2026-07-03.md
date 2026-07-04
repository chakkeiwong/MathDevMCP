# Phase 2 Subplan: Preflight And Collection Gate

Date: 2026-07-03

Status: `DRAFT_READY_FOR_PHASE_1_CLOSE_REVIEW`

## Phase Objective

Run final local preflight checks against the frozen v2 candidate, approval
packet, and scoring contract, then decide whether response collection is
explicitly authorized. If approval is incomplete, stop with an approval-needed
handoff and do not collect responses.

## Entry Conditions Inherited From Previous Phase

- Phase 1 approval packet exists:
  `.mathdevmcp/downstream_agent_usefulness_v2/collection_approval_packet.md`.
- Phase 1 scoring contract exists and parses:
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`.
- V2 prompt manifest remains 18 prompts across 6 cases and A/B/C conditions.
- V2 prompt validation remains zero-error.
- V2 response artifact count remains zero.
- Candidate-only stressors remain explanatory unless explicitly approved as
  primary before collection.
- Claude Opus review for the planning boundary remains blocked by reviewer
  model availability; no Claude-review waiver has been recorded.

## Required Artifacts

- Preflight report:
  `.mathdevmcp/downstream_agent_usefulness_v2/collection_preflight_report.json`.
- Phase 2 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-02-preflight-gate-result-2026-07-03.md`.
- Draft Phase 3 response-collection subplan if, and only if, collection
  approval is complete:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-03-response-collection-subplan-2026-07-03.md`.
- Updated execution ledger and stop handoff.

## Required Checks, Tests, Reviews

- Parse all v2 JSON artifacts, including freeze manifest and scoring contract.
- Verify prompt manifest hash still equals the scoring-contract hash.
- Verify prompt count remains 18 and validation errors remain zero.
- Verify response artifact count remains zero before collection.
- Verify approval packet fields:
  prompt manifest/count, response-worker surface, retry policy,
  malformed-output policy, scoring contract, and artifact paths.
- Verify response-worker surface is explicitly approved and is not Claude
  before any Phase 3 handoff.
- Verify retry and malformed-output policies are explicitly approved before
  any Phase 3 handoff.
- Run focused pytest:
  `python3 -m pytest tests/test_downstream_usefulness_prompts.py`.
- Run `git diff --check` over v2 artifacts, plans, and review bundles.
- Local skeptical audit for implied approval, hidden response-worker choice,
  scoring drift, prompt mutation, malformed-output replacement, and unsupported
  claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the v2 candidate ready to collect responses under a complete explicit approval, or must it stop before collection? |
| Baseline/comparator | Phase 1 approval packet, frozen scoring contract, v2 prompt manifest, prompt validation, and candidate freeze manifest. |
| Primary criterion | Phase 2 passes if local preflight checks pass and either collection approval is complete enough to draft Phase 3, or the phase writes an approval-needed stop result without collecting responses. |
| Veto diagnostics | Missing response-worker approval; Claude as response worker; missing retry/malformed-output/scoring/artifact-path approval; response artifacts already present; prompt hash drift; prompt validation error; scoring contract drift; unsupported claim. |
| Explanatory diagnostics | Preflight JSON, approval completeness table, prompt/hash checks, pytest result, response-artifact count, stop handoff. |
| Not concluded | No response quality, no scored v2 result, no C-over-B superiority, no public benchmark validity, no release readiness, no product capability, no scientific validation, no general model reliability. |

## Forbidden Claims Or Actions

- Do not collect responses unless all approval fields are complete.
- Do not use Claude as response worker.
- Do not infer response-worker approval from prior benchmark work.
- Do not create response directories, response manifests, or scored-response
  files unless collection is explicitly authorized.
- Do not change scoring criteria after responses exist.
- Do not claim usefulness, C-over-B superiority, public benchmark validity,
  release readiness, product capability, scientific validation, or general
  model reliability.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- collection approval explicitly names the 18-prompt manifest;
- response-worker surface is explicitly named and is not Claude;
- retry policy is explicitly approved;
- malformed-output policy is explicitly approved;
- scoring contract is explicitly approved;
- response/scoring artifact paths are explicitly approved;
- prompt validation remains clean;
- response artifact count is zero before collection;
- Phase 3 subplan exists and includes objective, inherited entry conditions,
  artifacts, checks/reviews, evidence contract, forbidden claims/actions,
  next-phase handoff, and stop conditions.

If any approval field is missing, stop with
`BLOCKED_PENDING_COLLECTION_APPROVAL`.

## Stop Conditions

Stop if:

- any required approval field is missing;
- Claude is proposed as response worker;
- prompt validation fails and cannot be repaired without changing approved
  prompts;
- prompt hashes drift after approval;
- response artifacts appear before authorized collection;
- scoring criteria would need to change after seeing responses;
- collection would require unapproved network/API/funding/runtime/model-file
  boundaries;
- any product/release/scientific/public-benchmark/general-reliability claim is
  needed to proceed.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 2 result/close record;
3. draft Phase 3 only if collection approval is complete;
4. otherwise update the stop handoff with the exact missing approval fields;
5. review any next subplan for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
