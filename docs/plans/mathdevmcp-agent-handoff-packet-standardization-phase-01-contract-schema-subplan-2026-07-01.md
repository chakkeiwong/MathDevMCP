# Phase 1 Subplan: Contract And Schema Standard

Date: 2026-07-01

Status: `READY_WITH_HUMAN_CLAUDE_REVIEW_WAIVER`

## Phase Objective

Define the reusable local agent-handoff packet contract, required fields,
validator behavior, evidence boundary, scoring/rubric hooks, and forbidden
claims before implementation.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result has frozen the baseline repository state and existing packet
  surfaces.
- Existing behavior and baseline test status are known.
- Prior calibration is used only as local design input.
- Claude review gates are waived for this execution window by explicit user
  direction; Codex-only skeptical review and local checks remain required.

## Required Artifacts

- Phase 1 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-01-contract-schema-result-2026-07-01.md`.
- Contract/spec artifact, either as a docs section in the result or a separate
  spec if implementation needs it.
- Updated visible execution ledger.
- Optional Claude review trail entry for the contract brief.

## Required Checks, Tests, Reviews

- Local review against current constants:
  `REQUIRED_REVIEW_PACKET_FIELDS` and `REQUIRED_HUMAN_FRAMING_FIELDS` in
  `src/mathdevmcp/real_local_high_level_benchmark.py`.
- Local review against `validate_high_level_result` boundaries in
  `src/mathdevmcp/high_level_contracts.py`.
- Focused text check that the contract includes the required fields, evidence
  contract, forbidden claims/actions, handoff conditions, and stop conditions.
- Claude read-only review is waived for this execution window by explicit user
  direction. Codex-only skeptical review of the compact contract brief is
  required because this phase fixes the implementation contract.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact packet standard should Phase 2 implement? |
| Baseline/comparator | Existing durable benchmark packet fields and prior C-style calibration packet shape. |
| Primary criterion | Required fields, validator obligations, non-claims, evidence/framing separation, and integration boundaries are explicit enough to implement and test. |
| Veto diagnostics | Missing required fields; unclear validator behavior; packet treated as proof; hidden schema change to high-level envelope; source/backend evidence collapsed into prose only; C-over-B overclaim. |
| Explanatory diagnostics | Field table, validator checklist, allowed/forbidden integration paths, Claude findings. |
| Not concluded | No code correctness, runtime behavior, or downstream-agent improvement. |

## Forbidden Claims Or Actions

- Do not implement code in Phase 1 except tiny documentation-only fixes to the
  contract artifacts.
- Do not change pass/fail criteria after seeing Phase 2 test output.
- Do not assert the standard is globally optimal.
- Do not require downstream model/API response collection as a precondition for
  local standardization.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- the contract states required top-level packet fields;
- the contract states required `human_framing` fields;
- the validator pass/fail behavior is explicit;
- evidence/framing separation and non-claim rules are explicit;
- the human Claude-review waiver is recorded and Codex-only contract review is
  documented;
- the Phase 2 subplan has been refreshed against the final contract.

## Stop Conditions

Stop and write a blocker if:

- the contract cannot be made compatible with existing high-level workflow
  results without a broader project-direction decision;
- Codex-only review finds a material contract blocker that cannot be fixed
  within the phase boundary;
- implementing the contract would require changing release/default policy
  before evidence exists.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 1 result/close record;
3. draft or refresh the Phase 2 subplan;
4. review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
