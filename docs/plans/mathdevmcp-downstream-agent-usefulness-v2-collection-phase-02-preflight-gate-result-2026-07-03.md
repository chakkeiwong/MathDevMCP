# Phase 2 Result: Preflight And Collection Gate

Date: 2026-07-03

Status: `BLOCKED_PENDING_COLLECTION_APPROVAL`

## Phase Objective

Run final local preflight checks against the frozen v2 candidate, approval
packet, and scoring contract, then decide whether response collection is
explicitly authorized.

## Result Summary

Preflight checks passed, but collection approval is incomplete. The program
must stop before response collection.

No response collection was run. No response directories, response manifests,
or scored-response artifacts were created.

## Artifacts Produced

- Preflight report:
  `.mathdevmcp/downstream_agent_usefulness_v2/collection_preflight_report.json`.
- Phase 2 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-02-preflight-gate-result-2026-07-03.md`.
- Updated execution ledger and stop handoff.

## Local Checks

| Check | Result |
| --- | --- |
| Parse v2 JSON artifacts | Passed |
| Prompt manifest hash matches scoring contract | Passed |
| Prompt count | Passed: 18 |
| Prompt validation | Passed: 0 errors |
| Response artifact count | Passed: 0 |
| Collection authorization flag | Passed: scoring contract says `false` |
| Approval completeness | Blocked: required fields remain pending/missing |
| Focused pytest | Passed: `python3 -m pytest tests/test_downstream_usefulness_prompts.py`, 3 tests |
| Diff whitespace | Passed: `git diff --check -- .mathdevmcp/downstream_agent_usefulness_v2 docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-*.md docs/reviews/mathdevmcp-v2-collection-phase-*.md` |

## Approval Completeness

From `.mathdevmcp/downstream_agent_usefulness_v2/collection_preflight_report.json`:

| Approval field | Status |
| --- | --- |
| Prompt manifest and count | `PENDING_EXPLICIT_HUMAN_APPROVAL` |
| Response-worker surface | `MISSING_REQUIRED_APPROVAL` |
| Retry policy | `PENDING_EXPLICIT_HUMAN_APPROVAL` |
| Malformed-output policy | `PENDING_EXPLICIT_HUMAN_APPROVAL` |
| Scoring contract | `PENDING_EXPLICIT_HUMAN_APPROVAL` |
| Response artifact directory | `PENDING_EXPLICIT_HUMAN_APPROVAL` |
| Response manifest | `PENDING_EXPLICIT_HUMAN_APPROVAL` |
| Scored JSON | `PENDING_EXPLICIT_HUMAN_APPROVAL` |
| Scored Markdown | `PENDING_EXPLICIT_HUMAN_APPROVAL` |

## Evidence Contract Status

| Field | Status |
| --- | --- |
| Question | Answered: v2 is not authorized for response collection yet. |
| Baseline/comparator | Phase 1 approval packet, frozen scoring contract, v2 prompt manifest, prompt validation, and candidate freeze manifest. |
| Primary criterion | Passed as a stop gate: local checks passed and the phase wrote an approval-needed stop result without collecting responses. |
| Veto diagnostics | Missing response-worker approval and pending approval fields require stop before collection. No response artifacts appeared, no Claude worker role was used, and no prompt/scoring drift was detected. |
| Explanatory diagnostics | Preflight JSON, approval completeness table, prompt/hash checks, pytest result, response-artifact count. |
| Not concluded | No response quality, scored v2 result, C-over-B superiority, public benchmark validity, release readiness, product capability, scientific validation, or general model reliability. |

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
| --- | --- | --- | --- | --- | --- |
| Stop before Phase 3 response collection | Passed as a stop gate | Approval incomplete; no unauthorized collection occurred | Whether the human will approve the exact collection scope and response-worker surface | Ask for explicit collection approval or end this runbook here | No response quality, scored v2 result, C-over-B superiority, collection authorization, or public/release/scientific/product claim |

## Exact Approval Needed To Continue

To launch Phase 3 response collection, the human must explicitly approve all of:

- prompt manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json`;
- prompt count: 18;
- response-worker surface: an explicitly named non-Claude model/agent surface;
- retry policy: one visible attempt per prompt, no hidden retries, unless a
  different replicated design is approved before launch;
- malformed-output policy: preserve malformed, empty, partial, or off-schema
  outputs and score them as malformed; do not replace them;
- scoring contract:
  `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`;
- response artifact directory:
  `.mathdevmcp/downstream_agent_usefulness_v2/responses_candidate/`;
- response manifest:
  `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json`;
- scored outputs:
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json`
  and
  `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.md`.

Claude remains forbidden as a response worker.
