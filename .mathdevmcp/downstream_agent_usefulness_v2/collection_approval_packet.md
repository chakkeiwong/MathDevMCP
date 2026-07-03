# V2 Collection Approval Packet

Date: 2026-07-03

Status: `COLLECTION_APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03`

## Purpose

This packet enumerates the exact human approvals required before collecting
responses for the v2 downstream-agent usefulness benchmark candidate. The
current resumed run records explicit approval for the exact scope below.

## Candidate Scope

| Field | Value |
| --- | --- |
| Prompt manifest | `.mathdevmcp/downstream_agent_usefulness_v2/prompt_manifest_candidate.json` |
| Prompt manifest sha256 | `340ec24f062dc614d6e03a7d279a74539c8e033fef499ef3fc127e2722736bfe` |
| Prompt count | 18 |
| Case count | 6 |
| Conditions | `A_task_only`, `B_evidence_only`, `C_human_framed` |
| Prompt validation | 0 errors |
| Candidate freeze manifest | `.mathdevmcp/downstream_agent_usefulness_v2/collection_candidate_freeze_manifest.json` |

## Required Approval Fields

| Required field | Proposed value | Approval status |
| --- | --- | --- |
| Prompt manifest and count | Manifest and 18 prompts listed above | `APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03` |
| Response-worker surface | Codex subagents via `multi_agent_v1.spawn_agent`; Claude forbidden | `APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03` |
| Retry policy | One visible attempt per prompt; no hidden retries | `APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03` |
| Malformed-output policy | Preserve malformed, empty, partial, or off-schema output as the response artifact and score it as malformed; do not replace it | `APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03` |
| Scoring contract | `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json` | `APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03` |
| Response artifact directory | `.mathdevmcp/downstream_agent_usefulness_v2/responses_candidate/` | `APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03` |
| Response manifest | `.mathdevmcp/downstream_agent_usefulness_v2/response_manifest_candidate.json` | `APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03` |
| Scored JSON | `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.json` | `APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03` |
| Scored Markdown | `.mathdevmcp/downstream_agent_usefulness_v2/scored_responses_candidate.md` | `APPROVED_BY_CURRENT_HUMAN_APPROVAL_2026_07_03` |

## Collection Boundary

Collection is authorized for exactly the approved scope above. A prior
invalidation note remains historical audit context for an earlier ambiguous
approval, but the current resumed run records explicit approval for the Phase 3
collection scope.

Claude is forbidden as a response worker. Claude may be a read-only reviewer
only, subject to current review-gate availability and explicit human approval
for any external-review or reviewer-model substitution boundary.

## Collection Rules If Later Approved

- Do not edit prompt fixtures after approval.
- Use the approved response-worker surface only.
- Record one response or malformed-output record for every prompt.
- Record worker identity/surface, prompt id, timestamps, exit status, command
  or invocation method, and response artifact path.
- Do not run hidden retries.
- Do not replace malformed outputs.
- Do not change scoring criteria after seeing responses.
- Report hard vetoes before required-pass counts.

## Non-Claims

This packet does not claim downstream-agent usefulness, C-over-B superiority,
public benchmark validity, release readiness, scientific validation, product
capability, broad theorem proving, or general model reliability.
