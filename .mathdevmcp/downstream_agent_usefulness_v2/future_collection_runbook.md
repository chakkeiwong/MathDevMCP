# Future V2 Response Collection Runbook

Date: 2026-07-02

Status: `COLLECTION_NOT_AUTHORIZED`

## Purpose

This runbook describes how to collect responses for the v2 candidate prompts
after explicit human approval. It does not authorize collection.

## Approval Required Before Launch

Collection must not begin until a human explicitly approves all of:

- prompt manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json`;
- prompt count: 18 prompts;
- response-worker surface: to be named explicitly; Claude is forbidden as a
  response worker;
- retry policy: one attempt per prompt, no hidden retries, unless a different
  replicated design is approved before launch;
- artifact paths:
  `.mathdevmcp/downstream_agent_usefulness_v2/responses_candidate/`,
  `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`,
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`,
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.md`;
- scoring rubric/applicability contract: frozen before collection;
- malformed-output policy: preserve malformed or incomplete outputs as
  artifacts and score them as malformed; do not replace them with hidden
  retries.

## Pre-Collection Checks

Run these checks immediately before collection:

```bash
python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json
python3 -m json.tool .mathdevmcp/downstream_agent_usefulness_v2/prompt_contract_validation.json
python3 -m pytest tests/test_downstream_usefulness_prompts.py
```

Also rerun the v2 prompt leakage/hash validation recorded in Phase 3 or an
equivalent script. The validation report must contain zero errors.

## Collection Rules

- Use the approved response-worker surface only.
- Claude is forbidden as a response worker.
- Claude may be used only as a read-only reviewer, never as response worker.
- Use one visible attempt per prompt unless an approved replicated design says
  otherwise.
- Record every prompt id, worker identity/surface, command or invocation
  method, start/end timestamp, exit status, and response artifact path.
- Preserve malformed, empty, partial, or off-schema outputs.
- Do not edit prompt fixtures during collection.
- Do not change scoring criteria after seeing responses.
- Do not hide failed attempts.

## Scoring Rules

- Score hard-veto-first.
- Use the frozen repaired baseline required dimensions unless a separate v2
  rubric is explicitly approved before collection.
- Treat candidate-only stressors in
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_applicability_map.json`
  as explanatory unless preapproved as required dimensions.
- Do not score prompt polish as task success.
- Do not declare C better than B if C has any hard-veto regression or if B and
  C tie under the predeclared primary dimensions.

## Result Note Requirements

Any collection result must include:

- run manifest: git commit, command/surface, environment, worker identity,
  prompt manifest hash, scoring contract, timestamps, artifact paths;
- response manifest;
- hard-veto counts before pass counts;
- required-pass counts by condition;
- per-case B/C comparison;
- malformed-output summary;
- decision table;
- limitations and non-claims.

## Forbidden Claims

Even if future collection passes, do not claim:

- public benchmark validity;
- release readiness;
- scientific validation;
- product capability;
- broad theorem proving;
- general model reliability;
- proof correctness beyond scoped certified obligations.

## Stop Conditions

Stop collection if:

- approval does not name prompt count, response-worker surface, retry policy,
  and artifact paths;
- prompt validation fails;
- prompt fixtures are modified after approval;
- Claude is proposed as response worker;
- scoring criteria would need to change after seeing responses;
- malformed outputs would be replaced rather than preserved;
- any release, product, public benchmark, scientific, funding, runtime, or
  model-file boundary is crossed.
