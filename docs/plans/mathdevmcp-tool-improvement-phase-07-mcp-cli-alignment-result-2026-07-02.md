# Phase 7 Result: MCP And CLI Surface Alignment

Date: 2026-07-02

Status: `PASSED_AFTER_LOCAL_REPAIR`

## Phase Objective

Expose improved high-level workflow outputs through MCP, server, and CLI
surfaces so coding agents can call the tools reliably.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Improved workflow fields are reachable from MCP/server/CLI surfaces without losing evidence fields or weakening boundaries. |
| Baseline/comparator | Existing MCP facade, MCP server wrappers, and CLI commands. |
| Primary criterion | Passed locally: facade/server/CLI tests preserve Phase 6 packet fields and review-packet descriptions remain diagnostic-only. |
| Veto diagnostics | No evidence field was dropped; review packet remains non-certifying; optional backends were not made mandatory. |
| Explanatory diagnostics | Surface tests assert `backend_checks`, `nested_evidence_summary`, `route_plans`, `trace_maps`, `residual_gaps`, `decision_criteria`, `risk_register`, and `non_claims` survive. |
| Not concluded | No product readiness, release readiness, public benchmark validity, scientific validation, broad theorem proving, or general reliability. |

## Artifacts

- `tests/test_mcp_facade.py`
- `tests/test_mcp_server.py`
- `tests/test_mcp_surface_sync.py`
- `tests/test_release_smoke.py`
- `src/mathdevmcp/benchmarks.py`
- Refreshed Phase 8 subplan:
  `docs/plans/mathdevmcp-tool-improvement-phase-08-benchmark-regression-subplan-2026-07-02.md`

## Implementation Summary

- Added MCP facade test coverage for Phase 6 review-packet fields.
- Added MCP server test coverage for the same fields.
- Added registry/description checks to preserve the diagnostic-only,
  non-certificate boundary.
- Added CLI smoke coverage for `prepare-review-packet` preserving Phase 6
  fields through JSON-file evidence input.
- Repaired the seeded high-level benchmark oracle to match the already-approved
  Phase 4 `derive_from` route-plan behavior: diagnostic `review_packet`
  evidence may accompany derive proof/refutation/inconclusive evidence, while
  the required certifying or blocking class and proof boundary remain checked.

## Local Checks

| Check | Result |
| --- | --- |
| `python3 -m pytest tests/test_mcp_surface_sync.py tests/test_mcp_server.py tests/test_mcp_facade.py` | Passed after local repair: 50 tests. |
| `python3 -m pytest tests/test_release_smoke.py::test_cli_prepare_review_packet_preserves_phase6_packet_fields tests/test_release_smoke.py::test_cli_high_level_workflow_commands_return_contract_envelopes` | Passed: 2 tests. |
| `python3 -m pytest tests/test_prepare_review_packet.py tests/test_math_review_packet.py tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_audit_math_to_code.py` | Passed: 29 tests. |
| High-level benchmark diagnostic script using `build_benchmark_report` and `build_high_level_workflow_quality_report` | Passed after oracle repair: 70/70; high-level quality thresholds passed. |
| `git diff --check` over touched Phase 6/7 implementation/tests/docs | Passed. |

## Local Repair Note

The first broad MCP/server/facade run failed because the seeded high-level
benchmark still expected exact `derive_from` evidence classes from before Phase
4. Current `derive_from` deliberately emits a diagnostic `review_packet`
route-plan companion. The benchmark oracle was repaired to require the
certifying/blocking evidence class while allowing the diagnostic
`review_packet` companion. This is an oracle-alignment repair, not a proof
promotion.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 8 | Passed after local repair | No veto triggered | Final closeout must distinguish local benchmark diagnostics from public/promotion claims | Run regression closeout and write benchmark-to-improvement mapping | No release, product, scientific, public benchmark, or reliability claim |

## Phase 8 Handoff

Phase 8 should run focused regressions, record the 70/70 local seeded benchmark
diagnostic after the oracle alignment, and map the implementation changes to
the repaired downstream-agent benchmark gaps. It must not claim C-over-B
promotion, public benchmark validity, release readiness, broad theorem proving,
or general downstream-agent reliability.
