# Phase 3 Subplan: Workflow And Benchmark Integration

Date: 2026-07-01

Status: `READY_WITH_PHASE_2_VALIDATOR`

## Phase Objective

Integrate the reusable packet standard into review-packet and durable benchmark
packet paths while preserving backward-compatible high-level results and
existing diagnostic boundaries.

## Entry Conditions Inherited From Previous Phase

- Phase 2 module and validator tests pass.
- Existing packet tests have not regressed, or regressions are recorded as
  blockers.
- Phase 3 integration scope is limited to packet paths identified by Phase 0.
- Claude review gates are waived for this execution window by explicit user
  direction; Codex-only integration review and local checks remain required.

## Required Artifacts

- Phase 3 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-03-workflow-benchmark-integration-result-2026-07-01.md`.
- Scoped implementation diffs, likely involving one or more of:
  `src/mathdevmcp/prepare_review_packet.py`,
  `src/mathdevmcp/real_local_high_level_benchmark.py`,
  `src/mathdevmcp/high_level_workflows.py`.
- Focused integration tests.
- Updated visible execution ledger.
- Claude read-only implementation-diff review is waived for this execution
  window by explicit user direction; Codex-only implementation review is
  required.

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_agent_handoff_packet.py tests/test_prepare_review_packet.py tests/test_real_local_high_level_benchmark.py -q`.
- Any additional focused tests for changed integration surfaces.
- Manual inspection that high-level workflow result validation still passes.
- Codex-only review of compact integration diff and result summary.

Preferred first integration:

- use `validate_agent_handoff_packet` inside
  `build_real_local_high_level_packet_report`;
- add packet findings if the reusable standard fails;
- keep current `prepare_review_packet` output shape unchanged unless a scoped,
  tested nested integration is clearly safe.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can existing packet-producing paths use or align with the reusable standard without breaking current behavior? |
| Baseline/comparator | Phase 2 module plus current `prepare_review_packet` and durable benchmark packet report behavior. |
| Primary criterion | Existing tests and new integration tests pass; packet outputs preserve required fields, reasoning, source anchors, backend evidence, actions, and non-claims. |
| Veto diagnostics | Backward-incompatible high-level envelope change; existing benchmark packet report loses reasoning or framing; diagnostic packet becomes certifying; nested evidence lost; non-claims weakened; broad refactor. |
| Explanatory diagnostics | Before/after field coverage, validator use points, regression outputs, Claude findings. |
| Not concluded | Public API stability beyond local repo, release readiness, downstream-agent improvement. |

## Forbidden Claims Or Actions

- Do not change unrelated high-level workflow behavior.
- Do not use broad schema migration unless Phase 1/2 artifacts explicitly
  require it and tests cover it.
- Do not remove existing benchmark packet fields to fit the new module.
- Do not run downstream model-response collection.

## Exact Next-Phase Handoff Conditions

Advance to Phase 4 only if:

- integration tests and existing packet tests pass;
- changed outputs are documented in Phase 3 result;
- any backward-compatibility risk is either eliminated or recorded as a stop
  condition;
- Codex-only integration review is documented for material diffs;
- Phase 4 exposure scope is refreshed against the integrated behavior.

## Stop Conditions

Stop and write a blocker if:

- integration requires breaking existing high-level result contracts;
- benchmark packet report behavior cannot be preserved;
- local tests identify a semantic boundary regression;
- resolving the issue would require a broader product/default-policy decision.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 3 result/close record;
3. draft or refresh the Phase 4 subplan;
4. review the Phase 4 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
