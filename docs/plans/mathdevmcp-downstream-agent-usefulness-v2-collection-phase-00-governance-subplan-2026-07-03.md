# Phase 0 Subplan: Governance And Candidate Freeze

Date: 2026-07-03

Status: `READY_FOR_PHASE_0_EXECUTION`

## Phase Objective

Freeze the v2 candidate state, approval boundaries, role contract, and Claude
review-gate process before writing approval/scoring artifacts or considering
response collection.

## Entry Conditions Inherited From Previous Phase

- V2 candidate construction program completed.
- V2 candidate artifacts exist under
  `.mathdevmcp/downstream_agent_usefulness_v2/`.
- Claude review gate for v2 candidate returned `REVIEW_STATUS=agreed` and
  `VERDICT=AGREE`.
- V2 response collection has not been authorized.
- V2 response artifact count is expected to be zero.

## Required Artifacts

- Phase 0 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-00-governance-result-2026-07-03.md`.
- Candidate freeze manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/collection_candidate_freeze_manifest.json`.
- Draft Phase 1 subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-01-approval-scoring-subplan-2026-07-03.md`.
- Claude review bundle for Phase 0/Phase 1 readiness:
  `docs/reviews/mathdevmcp-v2-collection-phase-00-review-bundle-2026-07-03.md`.
- Updated execution ledger, review trail, and stop handoff if needed.

## Required Checks, Tests, Reviews

- Parse all v2 JSON artifacts.
- Verify prompt count is 18 and prompt validation errors are zero.
- Verify v2 response artifact count is zero.
- Verify primary repaired baseline hashes still match the v2 baseline hash
  manifest.
- Run focused pytest: `python3 -m pytest tests/test_downstream_usefulness_prompts.py`.
- Run `git diff --check` over new collection/scoring plans and v2 artifacts.
- Run Claude read-only review gate on a compact Phase 0/Phase 1 readiness
  bundle.
- Local skeptical audit for wrong baseline, implied collection approval,
  Claude role confusion, missing stop conditions, and unsupported claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the v2 candidate frozen and is the collection/scoring program safely gated before approval/scoring artifacts are created? |
| Baseline/comparator | V2 candidate artifacts and repaired baseline hash manifest. |
| Primary criterion | Phase 0 passes if candidate freeze manifest exists, all local checks pass, response artifact count is zero, Phase 1 subplan exists, and Claude review gate agrees or records a handled non-blocking status. |
| Veto diagnostics | Response artifacts already present; prompt validation errors; baseline hash mismatch; implied collection approval; Claude as response worker; unsupported claims. |
| Explanatory diagnostics | Artifact list, hashes, prompt count, validation status, pytest result, Claude review status. |
| Not concluded | No response quality, scored v2 result, C-over-B superiority, model reliability, release/public/scientific/product claim. |

## Forbidden Claims Or Actions

- Do not collect responses.
- Do not use Claude as response worker.
- Do not create response manifests or scored-response files.
- Do not treat candidate freeze as usefulness evidence.
- Do not change scoring criteria after any future responses.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- candidate freeze manifest exists and parses;
- response artifact count is zero;
- prompt validation remains clean;
- Phase 1 subplan exists and includes the required fields;
- Claude review gate returns `AGREE` or any non-primary/fallback status is
  explicitly recorded and judged non-blocking for planning-only work.

## Stop Conditions

Stop if:

- v2 response artifacts already exist unexpectedly;
- prompt validation fails and cannot be repaired;
- baseline hashes mismatch unexpectedly;
- Claude review returns `REVISE` and the issue cannot be repaired after five
  rounds;
- proceeding would require response collection or a response-worker decision.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 0 result/close record;
3. draft or refresh the Phase 1 subplan;
4. review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. run Claude read-only review gate on the compact bundle.
