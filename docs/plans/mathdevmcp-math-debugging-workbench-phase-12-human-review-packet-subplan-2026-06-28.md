# Phase 12 Subplan: Human Review Packet

## Phase Objective

Extend or wrap proof packets into `math_review_packet`, a compact artifact that
aggregates source, obligations, assumptions, backend attempts, counterexamples,
code links, notation conflicts, generated diagnostics, and next actions.

## Entry Conditions Inherited From Previous Phase

- Core workflows produce stable evidence records.
- Existing `proof_packet` remains available.

## Required Artifacts

- `src/mathdevmcp/math_review_packet.py`
- `tests/test_math_review_packet.py`
- CLI/MCP exposure.
- Phase 12 result record.
- Refreshed Phase 13 subplan.

## Required Checks, Tests, Reviews

- Packet tests for true identity, false identity, missing-assumption derivation,
  code mismatch, and notation conflict.
- Existing proof packet tests.
- `git diff --check`.
- Claude review of packet boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a reviewer get a compact, evidence-preserving packet for a math debugging question? |
| Baseline/comparator | Existing `proof_packet_label`. |
| Primary pass criterion | Packet aggregates evidence without changing nested statuses or certification boundaries. |
| Veto diagnostics | Packet status overclaims beyond nested evidence. |
| Explanatory diagnostics | Summary, actions, linked artifacts. |
| Not concluded | Packet itself is not a proof certificate. |
| Artifact | Review packet module/tests/result. |

## Forbidden Claims And Actions

- Do not flatten diagnostic evidence into proof.
- Do not hide unresolved blockers.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 13 if packets can be referenced by dependency/impact analysis.

## Stop Conditions

Stop if aggregation changes evidence meanings.
