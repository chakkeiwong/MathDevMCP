# Phase 3 Subplan: Response Collection Protocol

Date: 2026-07-01

Status: `REVISED_AFTER_CLAUDE_R1_PENDING_PHASE_2`

## Phase Objective

Collect downstream-agent responses for the 15 prompt fixtures only if the
model-use path is explicitly approved and bounded; otherwise write a blocker
result with exact approval needed.

## Entry Conditions Inherited From Previous Phase

- Prompt fixtures and manifest exist.
- Rubric and hard vetoes are frozen.
- No response scoring has begun.

## Required Artifacts

- Phase 3 result or blocker:
  `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-03-response-collection-result-2026-07-01.md`.
- Response directory:
  `.mathdevmcp/agent_handoff_packet_calibration/responses/`.
- Response manifest:
  `.mathdevmcp/agent_handoff_packet_calibration/response_manifest.json`.
- Exact command/model provenance for each response, if collected.
- Explicit model identity, settings, execution context, retry policy, malformed
  output policy, and approval record.
- Refreshed Phase 4 subplan.
- Ledger entry.

## Required Checks, Tests, And Reviews

- Pre-run approval check for any model/API/subagent usage.
- Verify response count matches approved scope.
- Verify no response is treated as proof or scorer authority.
- Verify no hidden retries or cherry-picking occurred.
- Validate response manifest JSON.
- Claude read-only review of collection protocol, not response generation
  authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can bounded downstream-agent responses be collected without crossing model-use or authority boundaries? |
| Baseline/comparator | Phase 2 prompt manifest and Phase 1 rubric. |
| Primary criterion | Responses are collected only under approved conditions with exact provenance, or a blocker result precisely names the missing approval and stops the program before scoring. |
| Veto diagnostics | Model runs without approval; Claude used as worker; responses alter scoring criteria; response content treated as mathematical proof; hidden retries or cherry-picking; partial scoring after approval blocker. |
| Explanatory diagnostics | Response counts, model/provenance manifest, runtime notes. |
| Not concluded | Packet effectiveness, model reliability, proof validity, or release/public/scientific claims. |

## Forbidden Claims And Actions

- Do not use Claude as a response-generation worker.
- Do not run model-subject collection without explicit approval if approval is
  required.
- Do not discard bad responses unless the predeclared protocol says how to
  handle malformed outputs.
- Do not change prompts after seeing responses.
- If approval is missing, do not proceed to partial scoring, surrogate
  interpretation, or fixture tweaking based on imagined responses.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 only if:

- responses exist for the approved condition/case set;
- response manifest records provenance and malformed-output handling;
- no scorer criteria changed after response collection.

If approval is missing, write a blocker result and stop. Phase 4 must not run.

## Stop Conditions

Stop if:

- model-use approval is required and absent;
- collection path would use Claude as worker;
- hidden retries/cherry-picking cannot be prevented;
- prompt or rubric flaws are discovered after response collection would begin.

## End-Of-Phase Protocol

Run checks, write result or blocker, refresh/review Phase 4 if applicable,
append ledger, then advance or stop.
