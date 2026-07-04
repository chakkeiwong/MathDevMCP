# Phase 6 Subplan: Review Packet Compiler

Date: 2026-07-02

Status: `DRAFT_NEXT`

## Phase Objective

Make `prepare_review_packet` compile nested workflow outputs into
self-contained packets with assumptions, route attempts, backend checks,
obligations, gaps, decision criteria, risks, and non-claims.

## Entry Conditions

- Phases 1 through 5 have produced structured workflow outputs.
- Existing review packet tests pass.
- Phase 5 trace maps are structural diagnostics only and must be embedded as
  trace context, not as proof of code correctness.

## Required Artifacts

- Updated `src/mathdevmcp/prepare_review_packet.py` and/or
  `src/mathdevmcp/agent_handoff_packet.py`.
- Focused tests in `tests/test_prepare_review_packet.py` and
  `tests/test_agent_handoff_packet.py`.
- Phase 6 result record.
- Refreshed Phase 7 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_prepare_review_packet.py tests/test_agent_handoff_packet.py`
- `python3 -m pytest tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_audit_math_to_code.py`
- `git diff --check` over touched files.
- Claude read-only review for packet proof-boundary changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can review packets become self-contained enough for downstream agents while preserving proof boundaries? |
| Baseline/comparator | Existing `prepare_review_packet` and `agent_handoff_packet` behavior, Phase 5 trace maps, and benchmark case RLHLB-07. |
| Primary criterion | Packet validates, includes nested evidence and gaps, and never promotes packet completeness to proof. |
| Veto diagnostics | Proof-like overclaim; missing source/framing; hidden residual risks; nested diagnostic evidence or trace maps promoted to proof. |
| Explanatory diagnostics | Packet validation errors and nested evidence summaries. |
| Not concluded | No proof certificate, release readiness, scientific validation, or product capability. |

## Skeptical Plan Audit

- Wrong baseline risk: compare against the existing `math_review_packet` and
  high-level `prepare_review_packet` contracts, not against an imagined richer
  packet schema.
- Proxy metric risk: packet richness, downstream readability, and validation
  success are only review-usability diagnostics; they are not proof,
  scientific validation, public benchmark validity, or release readiness.
- Hidden assumption risk: route plans, trace maps, and nested backend attempts
  may carry useful context, but their existing boundary labels must remain
  visible and must not become certifying evidence merely by inclusion.
- Environment mismatch risk: local tests are sufficient for this additive
  packet compiler change; no optional backends, network access, or external
  benchmark refresh is required in this phase.
- Artifact-answer fit: additive low-level packet fields answer the Phase 6
  question while keeping the top-level high-level envelope stable for existing
  MCP/CLI consumers.

Audit result: `PASS_WITH_CONSTRAINTS`. Proceed only with additive diagnostic
packet fields and tests that assert the proof boundary is preserved.

## Forbidden Claims/Actions

- Do not treat a review packet as proof.
- Do not erase residual gaps.
- Do not use Claude or Codex as mathematical authority.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 7 only if packet output fields are stable enough to expose
through MCP/server surfaces.

## Stop Conditions

Stop if packet schema changes would break existing downstream consumers, or if
proof-boundary validation becomes weaker.
