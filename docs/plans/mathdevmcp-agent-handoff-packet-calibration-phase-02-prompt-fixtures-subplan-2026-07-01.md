# Phase 2 Subplan: Prompt Fixture Generation

Date: 2026-07-01

Status: `REVISED_AFTER_CLAUDE_R1_PENDING_PHASE_1`

## Phase Objective

Generate local prompt fixtures for the five selected cases under the three
predeclared prompt conditions without running downstream model subjects.

## Entry Conditions Inherited From Previous Phase

- Calibration contract and scoring rubric are frozen.
- Selected cases and condition definitions are recorded.
- No responses have been collected.

## Required Artifacts

- Phase 2 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-02-prompt-fixtures-result-2026-07-01.md`.
- Prompt fixture directory:
  `.mathdevmcp/agent_handoff_packet_calibration/prompts/`.
- Prompt manifest:
  `.mathdevmcp/agent_handoff_packet_calibration/prompt_manifest.json`.
- Optional generator script or CLI extension if needed, with focused tests.
- Refreshed Phase 3 subplan.
- Ledger entry.

## Required Checks, Tests, And Reviews

- Verify 15 prompts exist: five cases x three conditions.
- Verify condition A omits evidence ledgers and human framing.
- Verify condition B includes evidence/status ledgers but omits human framing.
- Verify condition C includes human framing and bounded machine ledger summary.
- Verify A/B/C share identical task skeleton, requested output sections,
  response length band, and retry/malformed-output policy.
- Verify B and C share the same machine-evidence payload except that C adds
  human framing.
- Validate manifest JSON.
- Run focused tests if a generator is added.
- Claude read-only review of prompt-condition fairness brief if material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can we generate fair prompt fixtures that isolate the effect of human framing? |
| Baseline/comparator | Phase 1 condition definitions and current packet artifact. |
| Primary criterion | Prompt corpus contains exactly the predeclared case/condition set and passes leakage/fairness/evidence-parity checks. |
| Veto diagnostics | Framing leaks into A or B; C receives extra non-framing information unavailable to B; unequal task/output/length/retry policy; source text is overcopied; prompt asks for proof or release claims. |
| Explanatory diagnostics | Prompt counts, per-condition field summary, fixture examples. |
| Not concluded | Agent performance, packet superiority, or model reliability. |

## Forbidden Claims And Actions

- Do not run model subjects in Phase 2.
- Do not alter rubric criteria after seeing generated prompts except to fix
  contract violations before any response collection.
- Do not include large raw source excerpts.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only if:

- prompt manifest validates;
- prompt count is exactly 15;
- leakage/fairness checks pass;
- B/C evidence parity passes;
- Phase 3 subplan states whether model-subject execution needs explicit human
  approval.

## Stop Conditions

Stop if:

- prompt conditions cannot be separated fairly;
- source context would require copying large external/local source text;
- prompt generation requires network/API/model usage.

## End-Of-Phase Protocol

Run checks, write result, refresh/review Phase 3, append ledger, then advance or
stop.
