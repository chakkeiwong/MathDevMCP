# Claude Read-Only Review Bundle

Date: 2026-07-03
Review name: `mathdevmcp-v2-collection-phase-01`

Status: `NOT_SENT_OPUS_MODEL_UNAVAILABLE_PENDING_REVIEWER_DIRECTION`

## Review Availability Note

Claude Opus review did not reach material review for Phase 0. After explicit
informed human approval to send the bounded Phase 0 bundle to
Claude/Anthropic, the gate reached the gateway but the `opus` alias resolved
to unavailable `claude-opus-4-7`. No-bundle probes showed `sonnet` transport
works, while tested Opus aliases were unavailable or unsupported.

This bundle is retained as a compact review artifact for future audit. It was
not sent to Claude during Phase 1 because no substitute reviewer direction had
been given.

## Objective

Review whether the Phase 1 approval packet, frozen scoring contract, and Phase
2 preflight subplan preserve collection boundaries and avoid scoring drift.

## Artifacts To Inspect

- `.mathdevmcp/downstream_agent_usefulness_v2/collection_approval_packet.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/scoring_contract_v2_collection.json`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-02-preflight-gate-subplan-2026-07-03.md`
- `.mathdevmcp/downstream_agent_usefulness_v2/collection_candidate_freeze_manifest.json`
- `.mathdevmcp/downstream_agent_usefulness_v2/scoring_applicability_map.json`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Are approval and scoring artifacts complete enough for Phase 2 preflight without authorizing collection? |
| Baseline/comparator | Phase 0 freeze manifest, v2 prompt manifest, repaired rubric, and v2 scoring applicability map. |
| Primary criterion | Approval packet enumerates all required approval fields; scoring contract freezes primary dimensions and hard-veto-first scoring; Phase 2 stops if approval is incomplete. |
| Veto diagnostics | Collection launched; response-worker surface silently assumed; Claude as response worker; hidden retries; malformed outputs replaceable; candidate-only stressors promoted after responses; unsupported usefulness or public/release/scientific/product claims. |
| Not concluded | No response quality, scored v2 result, C-over-B superiority, model reliability, release readiness, public benchmark validity, scientific validation, or product capability. |

## Required Verdict Format

If sent later, end with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
