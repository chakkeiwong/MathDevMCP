# Phase 2 Subplan: Reusable Builder And Validator

Date: 2026-07-01

Status: `READY_WITH_PHASE_1_CONTRACT`

## Phase Objective

Implement a small reusable agent-handoff packet builder and validator that
encodes the Phase 1 contract without changing existing workflow behavior by
default.

## Entry Conditions Inherited From Previous Phase

- Phase 1 has frozen required fields, validator semantics, and non-claims.
- The implementation target is scoped to a reusable module and tests.
- Existing high-level result envelope behavior is preserved unless Phase 3
  later gates integration.
- Claude review gates are waived for this execution window by explicit user
  direction; Codex-only implementation review and local checks remain required.

## Required Artifacts

- Phase 2 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-02-reusable-builder-validator-result-2026-07-01.md`.
- Implementation module, expected candidate path:
  `src/mathdevmcp/agent_handoff_packet.py`.
- Focused tests, expected candidate path:
  `tests/test_agent_handoff_packet.py`.
- Updated visible execution ledger.
- Claude read-only implementation-diff review is waived for this execution
  window by explicit user direction; Codex-only implementation review is
  required.

## Required Checks, Tests, Reviews

- Focused new tests:
  `python3 -m pytest tests/test_agent_handoff_packet.py -q`.
- Existing packet tests:
  `python3 -m pytest tests/test_prepare_review_packet.py tests/test_real_local_high_level_benchmark.py -q`.
- Contract regression text already passed in Phase 1; Phase 2 must implement
  that exact contract rather than inventing a new packet shape.
- Static import check through pytest, no package installation.
- Codex-only review of compact contract-to-diff summary before advancing if the
  module is implemented.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the reusable module build and validate local handoff packets according to the Phase 1 contract? |
| Baseline/comparator | Phase 1 contract and existing benchmark packet behavior. |
| Primary criterion | Focused tests pass for valid packet creation, missing-field failures, human-framing failures, non-claim enforcement, and evidence/framing separation. |
| Veto diagnostics | Existing packet tests regress; validator accepts missing required fields; builder drops machine evidence; builder implies proof certification; implementation rewrites unrelated workflows; tests only check formatting. |
| Explanatory diagnostics | Field coverage tests, failure messages, compact diff review, regression test output. |
| Not concluded | Integration readiness, CLI/MCP readiness, downstream-agent improvement, mathematical proof correctness. |

## Forbidden Claims Or Actions

- Do not modify CLI/MCP/operator docs in this phase.
- Do not change `prepare_review_packet` behavior by default.
- Do not change `HIGH_LEVEL_CONTRACT` unless Phase 1 explicitly required it
  and this phase tests it.
- Do not import heavy optional dependencies or fetch packages.

## Implementation Requirements

- Attach contract metadata `agent_handoff_packet`.
- Preserve required top-level fields from Phase 1, including promoted
  `reasoning`.
- Preserve required `human_framing` fields.
- Preserve required `reasoning` fields.
- Return deterministic validator error strings.
- Fail closed for proof-like certification overclaims without boundary text.
- Do not mutate caller-provided input structures.

## Exact Next-Phase Handoff Conditions

Advance to Phase 3 only if:

- builder and validator tests pass;
- existing packet and benchmark tests pass or any failure is documented as an
  unrelated pre-existing blocker;
- the Phase 2 result records exact files changed and non-claims;
- Codex-only implementation review is documented for material code changes;
- Phase 3 integration scope is refreshed to use the implemented API.

## Stop Conditions

Stop and write a blocker if:

- the module cannot satisfy required fields without large workflow rewrites;
- existing tests fail because of Phase 2 changes and no scoped repair is clear;
- validator semantics remain ambiguous after contract review;
- implementation would require package installation, network, model files, or
  unrelated refactors.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 2 result/close record;
3. draft or refresh the Phase 3 subplan;
4. review the Phase 3 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
