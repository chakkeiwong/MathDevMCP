# MathDevMCP Packet Compatibility Policy

Date: 2026-07-04

Status: `repo_local_policy`

## Scope

This policy covers MathDevMCP JSON packets returned by local library, CLI, and
MCP surfaces. It is a repo-local compatibility policy for coding agents and
maintainers. It is not a guarantee that unknown external closed-schema
consumers will accept every packet.

## Compatibility Contract

MathDevMCP uses additive compatibility for documented repo-local packet
contracts:

- existing required fields should remain present with their conservative
  meanings;
- documented additive fields may be added when they preserve existing status,
  evidence, and non-claim semantics;
- additive fields must not turn diagnostic evidence into proof, release
  readiness, public benchmark validity, scientific validation, product-wide
  readiness, or downstream-agent reliability;
- machine consumers should ignore documented fields they do not need, but must
  preserve fields carrying `status`, `certification_source`, `veto_reasons`,
  `assumptions`, `counterexamples`, `actions`, `non_claims`, and evidence
  provenance.

The current `prepare_review_packet` high-level result adds top-level
`agent_handoff` as a documented additive field. It mirrors the low-level
`math_review_packet.agent_handoff` and is safe for repo-local consumers that
already process `high_level_workflow_result` envelopes by named fields.

## Stable Minimal Handoff

Consumers that need a compact, stable review surface should request the compact
handoff:

- CLI: `prepare-review-packet --handoff`
- MCP facade/server: `prepare_review_packet` with `handoff=True`
- library: `review_packet_agent_handoff(result)`

The compact handoff is the preferred compatibility view for coding agents that
do not need the full high-level envelope. It should preserve at least:

- `scoped_question`
- `status`
- `reason`
- `evidence_ledger`
- `assumption_gap_ledger`
- `veto_risks`
- `non_claim_boundary`
- `next_actions`
- `next_artifact`
- `certification_boundary`

MCP may also include its normal `ok` wrapper. Consumers should compare semantic
fields, not byte-identical CLI/MCP/library output.

## External Strict-Schema Boundary

Exact compatibility with unknown external closed-schema consumers is not
claimed. If a consumer rejects additive fields, use the compact handoff surface
or design a separate strict-schema export mode with tests. Do not remove
diagnostic fields or boundary fields from the full packet merely to satisfy a
hypothetical strict external schema.

Arbitrary new top-level fields are not automatically part of the local
contract. They should be added only through a reviewed compatibility change and
covered by tests.

## Non-Claims

This policy does not claim:

- proof or semantic implementation correctness;
- release readiness;
- public benchmark validity;
- scientific validation;
- product-wide readiness;
- downstream-agent reliability;
- exact compatibility with unknown external closed-schema consumers.
