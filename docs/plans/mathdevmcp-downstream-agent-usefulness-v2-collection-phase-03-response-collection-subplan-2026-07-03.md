# Phase 3 Subplan: Response Collection

Date: 2026-07-03

Status: `EXECUTED_COLLECTION_APPROVED_BY_CURRENT_HUMAN_APPROVAL`

## Phase Objective

Collect exactly one downstream-agent response or malformed-output record for
each frozen v2 prompt fixture under the explicitly approved collection scope.
Preserve the no-hidden-retry rule, keep Claude out of the response-worker
role, and write a response manifest suitable for hard-veto-first scoring.

## Entry Conditions Inherited From Previous Phase

- Phase 2 preflight local checks passed and stopped before unauthorized
  collection.
- Current resumed human approval was recorded in chat as `I approve` for the
  Phase 3 collection scope summarized from the Phase 2 handoff.
- Collection authorization record exists and parses:
  `.mathdevmcp/downstream_agent_usefulness_v2/collection_authorization_record.json`.
- Approved prompt manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json`.
- Approved prompt manifest sha256:
  `340ec24f062dc614d6e03a7d279a74539c8e033fef499ef3fc127e2722736bfe`.
- Approved prompt count: 18.
- Approved response-worker surface:
  Codex subagents via `multi_agent_v1.spawn_agent`.
- Forbidden response-worker surface: Claude.
- Approved retry policy: one visible attempt per prompt; no hidden retries.
- Approved malformed-output policy: preserve malformed, empty, partial, or
  off-schema outputs as response artifacts and score them as malformed; do not
  replace them.
- Approved scoring contract:
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`.
- Approved artifact paths:
  `.mathdevmcp/downstream_agent_usefulness_v2/responses_candidate/`,
  `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`,
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`,
  and `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.md`.
- Claude Opus review for earlier planning gates remained unavailable; this
  phase proceeds under explicit human collection approval and local gates only.

## Required Artifacts

- Response directory with one raw response artifact per prompt:
  `.mathdevmcp/downstream_agent_usefulness_v2/responses_candidate/`.
- Response manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`.
- Phase 3 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-03-response-collection-result-2026-07-03.md`.
- Draft Phase 4 scoring subplan:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-04-scoring-subplan-2026-07-03.md`.
- Updated visible execution ledger.

## Required Checks, Tests, Reviews

- Before collection:
  - parse prompt manifest, prompt-contract validation, scoring contract, and
    collection authorization record;
  - verify prompt manifest sha256 equals the approved hash;
  - verify prompt count remains 18;
  - verify prompt validation has zero errors;
  - verify response directory, response manifest, and scored-response files do
    not already exist;
  - run focused pytest:
    `python3 -m pytest tests/test_downstream_usefulness_prompts.py`;
  - run `git diff --check` over v2 artifacts, collection plans, and review
    bundles.
- During collection:
  - spawn one Codex subagent per prompt fixture;
  - give each subagent the exact fixture text and a single-attempt benchmark
    instruction;
  - do not use Claude as a response worker;
  - do not retry, replace, or repair any malformed, empty, partial, or
    off-schema output.
- After collection:
  - write one response artifact for every prompt id;
  - write a response manifest with prompt id, case id, condition, workflow,
    prompt path/hash, response path/hash, subagent identity, status, no-retry
    marker, and malformed-output marker;
  - parse the response manifest as JSON;
  - verify response count equals 18;
  - verify each manifest response path exists;
  - verify no scored-response files were created in Phase 3;
  - run `git diff --check` over new artifacts and plans.
- Phase 3 uses local review only. Claude is not a response worker and is not
  required to authorize crossing into Phase 4.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the approved 18-prompt v2 candidate collect one visible downstream-agent response per prompt without hidden retries, prompt mutation, Claude response-worker use, or malformed-output replacement? |
| Baseline/comparator | Approved prompt manifest, collection authorization record, Phase 2 preflight result, and frozen scoring contract. |
| Primary criterion | Phase 3 passes if exactly 18 response artifacts and a parsing response manifest exist, each approved prompt has exactly one recorded attempt or malformed-output record, no hidden retries occur, Claude is not used as response worker, and local checks pass. |
| Veto diagnostics | Prompt hash drift; prompt count drift; response artifacts already present before launch; Claude response-worker use; hidden retries; malformed-output replacement; missing response artifact; response count not equal to 18; scoring files created before Phase 4; unsupported usefulness or C-over-B claim. |
| Explanatory diagnostics | Subagent ids/nicknames, collection timestamps, response hashes, malformed-output flags, prompt validation status, pytest result, diff whitespace status. |
| Not concluded | No scored v2 result, no C-over-B superiority, no downstream-agent usefulness claim, no public benchmark validity, no release readiness, no scientific validation, no product capability, no broad theorem proving, and no general model reliability. |

## Forbidden Claims Or Actions

- Do not mutate approved prompt fixtures.
- Do not use Claude as response worker.
- Do not run hidden retries.
- Do not replace malformed, empty, partial, or off-schema outputs.
- Do not change scoring criteria after seeing responses.
- Do not score responses in Phase 3.
- Do not claim usefulness, C-over-B superiority, public benchmark validity,
  release readiness, scientific validation, product capability, broad theorem
  proving, proof correctness beyond scoped obligations, or general model
  reliability.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- response directory exists with one artifact per approved prompt id;
- response manifest exists and parses;
- response manifest records exactly 18 one-attempt entries;
- every approved prompt id is represented exactly once;
- malformed/empty/partial/off-schema outputs, if any, are preserved rather
  than replaced;
- Claude was not used as response worker;
- scored-response files do not yet exist;
- Phase 3 result exists and records local checks;
- Phase 4 scoring subplan exists and includes objective, inherited entry
  conditions, artifacts, checks/reviews, evidence contract, forbidden
  claims/actions, next-phase handoff, and stop conditions.

## Stop Conditions

Stop if:

- pre-collection checks fail;
- prompt hashes or prompt count drift from approved values;
- response artifacts already exist before launch;
- subagent spawning requires an unapproved response-worker surface;
- Claude would be used as response worker;
- any attempted workflow would require hidden retries or malformed-output
  replacement;
- collection produces fewer or more than 18 recorded attempts;
- response artifacts cannot be written without changing the approved artifact
  paths;
- scoring criteria would need to change after seeing responses;
- any public/scientific/product/release/general-reliability claim would be
  required to proceed.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 3 result/close record;
3. draft or refresh the Phase 4 scoring subplan;
4. review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety;
5. stop before scoring if the Phase 4 handoff conditions are not met.
