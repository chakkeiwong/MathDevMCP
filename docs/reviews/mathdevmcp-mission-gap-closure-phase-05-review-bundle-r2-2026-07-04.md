# Phase 5 Compact Read-Only Review Bundle: Compatibility Policy R2

Date: 2026-07-04

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. Review this
compact bundle first. Inspect named repo files only if this summary is
insufficient.

## Why R2 Exists

The first Phase 5 review gate timed out after the probe returned `OK`, so the
prompt/bundle was treated as too broad. This R2 bundle narrows the review to
the exact compatibility boundary and test claims.

## Phase 5 Claim To Review

Phase 5 defines a repo-local additive packet compatibility policy for
MathDevMCP review packets.

Allowed claim:

- documented repo-local additive fields such as top-level `agent_handoff` are
  compatible with local consumers when existing required fields, status,
  evidence, provenance, and non-claims remain intact.

Forbidden claim:

- exact compatibility with unknown external closed-schema consumers.

## Policy Excerpt

Policy path:

- `docs/mathdevmcp-packet-compatibility-policy.md`

Decisive policy points:

- existing required fields should remain present with conservative meanings;
- documented additive fields may be added only when they preserve existing
  status, evidence, and non-claim semantics;
- top-level `agent_handoff` is documented as an additive repo-local field for
  `prepare_review_packet`;
- compact handoff is the preferred compatibility view for agents that do not
  need the full envelope;
- exact compatibility with unknown external closed-schema consumers is not
  claimed;
- strict-schema export remains future work if a real consumer requires it.

## Test Assertions Added

Test paths:

- `tests/test_prepare_review_packet.py`
- `tests/test_mcp_facade.py`

Library-level compatibility test asserts:

- required high-level fields remain present;
- `agent_handoff` is in the local high-level allow-list;
- top-level `result["agent_handoff"]` equals low-level
  `low_level["agent_handoff"]`;
- compact handoff contains `scoped_question`, `status`, `reason`,
  `evidence_ledger`, `assumption_gap_ledger`, `veto_risks`,
  `non_claim_boundary`, `next_actions`, `next_artifact`, and
  `certification_boundary`;
- certification boundary contains "not a proof certificate";
- `validate_high_level_result(result) == []`;
- an arbitrary top-level `external_closed_schema_probe` field is rejected as an
  unknown top-level field.

MCP compact handoff test asserts:

- compact MCP handoff contains the required compact fields above;
- `metadata` is absent from compact handoff;
- `workflow` is absent from compact handoff;
- certification boundary contains "not a proof certificate".

## Local Checks

- `python3 -m pytest tests/test_math_review_packet.py tests/test_prepare_review_packet.py tests/test_mcp_facade.py tests/test_mcp_server.py`
  - `56 passed`
- `python3 -m py_compile src/mathdevmcp/high_level_contracts.py src/mathdevmcp/prepare_review_packet.py src/mathdevmcp/math_review_packet.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`
  - passed
- focused exact-artifact check:
  `python3 -m pytest tests/test_prepare_review_packet.py::test_prepare_review_packet_additive_compatibility_contract_is_bounded tests/test_mcp_facade.py::test_call_mcp_tool_prepare_review_packet_can_return_compact_handoff`
  - `2 passed`
- `git diff --check` passed for the Phase 5 doc/test/plan artifacts.

## Review Questions

1. Is the allowed claim supported by the described policy and tests?
2. Is the forbidden exact-schema external compatibility claim avoided?
3. Is the local test coverage sufficient for this bounded Phase 5 gate?
4. Is it safe to advance to Phase 6 release-readiness boundary with the
   remaining exact-schema risk recorded as a non-claim/blocker?

End with exactly:

VERDICT: AGREE

or

VERDICT: REVISE
