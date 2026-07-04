# Review/Handoff Packet Product Improvement Plan

Date: 2026-07-04

Status: `READY_FOR_EXECUTION`

## Mission Link

This lane serves the canonical MathDevMCP mission:

- conservative agent-facing mathematical review through CLI/MCP;
- structured evidence and explicit abstention;
- compact reports that help agents and colleagues locate proof gaps, missing
  assumptions, implementation mismatches, and backend limitations without
  mistaking diagnostics for proof.

Mission spine:

- `docs/plans/mathdevmcp-mission-charter.md`
- `docs/plans/mathdevmcp-anti-drift-gate.md`
- `docs/plans/mathdevmcp-evidence-to-implementation-ledger.md`

## Product Capability

Improve the review/handoff packet product surface so downstream agents receive
one compact, actionable guide in addition to nested evidence.

Primary surfaces:

- library: `src/mathdevmcp/math_review_packet.py`;
- high-level wrapper: `src/mathdevmcp/prepare_review_packet.py`;
- CLI: `mathdevmcp prepare-review-packet`;
- MCP: `prepare_review_packet`.

## Evidence Input

The v2 downstream-agent usefulness diagnostic found that
`C_human_framed` improved on the Gaussian-score review-packet case because it
gave a self-contained review question, assumptions/gaps, veto risks, non-claim
boundary, and next artifact. This plan turns that evidence into product
behavior.

## Anti-Drift Gate

| Field | Answer |
| --- | --- |
| Mission link | Improve compact agent-facing mathematical review packets. |
| User served | Coding agents, maintainers, and colleagues reading CLI/MCP packet outputs. |
| Product artifact | Library packet output exposed through CLI/MCP. |
| Evidence instrument | v2 downstream-agent usefulness diagnostic plus focused unit/CLI/MCP tests. |
| Evidence-to-implementation path | Add a compact actionability guide to generated packets and test it through library, CLI, and MCP paths. |
| Non-goal | Do not build a new benchmark, change scoring criteria, or claim product/release/scientific validity. |
| Stop-for-drift condition | Stop if work becomes another benchmark iteration or docs-only artifact without product output changes. |

## Skeptical Audit

- Wrong baseline: the target is current `prepare_review_packet` behavior, not
  the benchmark prompt itself.
- Proxy metric risk: field presence is not downstream usefulness by itself;
  tests only verify that the product emits the intended actionable structure.
- Hidden assumption: adding prose fields must not turn packets into proof
  certificates.
- Environment mismatch: no external backend or network is needed.
- Command/artifact fit: focused packet tests and CLI/MCP tests directly check
  the product surface.

Audit result: pass. The plan is scoped to a concrete product-output change and
does not require new collection, scoring, package installs, or model/funding
boundaries.

## Implementation Scope

Add a backward-compatible low-level packet field, tentatively
`agent_handoff`, containing:

- scoped question;
- status and reason;
- source context summary if available;
- evidence ledger summary;
- assumption/gap ledger;
- veto and false-confidence risks;
- non-claim boundary;
- next actions or next artifacts/checks.

The field should be derived from existing packet evidence. It must not change
existing statuses, nested evidence, scoring, or certification behavior.

## Required Checks

- `python3 -m pytest tests/test_prepare_review_packet.py`
- `python3 -m pytest tests/test_math_review_packet.py`
- `python3 -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_release_smoke.py`
- `python3 -m py_compile src/mathdevmcp/math_review_packet.py src/mathdevmcp/prepare_review_packet.py src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`
- `git diff --check -- src/mathdevmcp tests docs/plans/mathdevmcp-review-handoff-packet-product-improvement-plan-2026-07-04.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP emit a compact, actionable review/handoff guide inside generated packets without weakening proof boundaries? |
| Baseline/comparator | Current `prepare_review_packet` and `math_review_packet` outputs. |
| Primary criterion | Packet outputs include a structured actionability guide with question, evidence summary, gaps/risks, non-claims, and next actions; existing packet contracts/tests still pass. |
| Veto diagnostics | Packet becomes certifying authority; existing statuses change unexpectedly; CLI/MCP wrappers break; non-claims disappear; tests require external backends or new collection. |
| Explanatory diagnostics | Field coverage, CLI/MCP preservation, focused pytest, py_compile, diff whitespace. |
| Not concluded | No downstream-agent usefulness promotion, release readiness, product capability claim, proof certificate, public benchmark validity, scientific validation, or general model reliability. |

## Closeout Rule

The result must state:

- product capability changed;
- evidence changed;
- implementation next step;
- regression guard;
- forbidden claims retained.
