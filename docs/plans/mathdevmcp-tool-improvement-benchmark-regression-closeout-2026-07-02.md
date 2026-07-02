# Tool Improvement Benchmark Regression Closeout

Date: 2026-07-02

Status: `LOCAL_REGRESSION_PASSED`

## Scope

This note maps the implemented tool improvements to the local diagnostic
benchmark signals that motivated the program. It is not a public benchmark,
release-readiness, scientific-validity, product-capability, broad
theorem-proving, or downstream-agent reliability claim.

## Local Seeded Benchmark Result

| Diagnostic | Result |
| --- | --- |
| Seeded benchmark total | 70/70 passed |
| High-level workflow quality | `quality_thresholds_passed` |
| Workbench quality | `quality_thresholds_passed` |
| High-level mutation family | all simulated boundary mutations detected |
| Workbench mutation family | all simulated boundary mutations detected |

The seeded benchmark was repaired in Phase 7 to align the high-level oracle
with the Phase 4 `derive_from` route-plan design. The repair allows diagnostic
`review_packet` route-plan evidence to accompany `derive_from` results while
still requiring the certifying or blocking evidence class and preserving the
proof boundary.

## Downstream-Agent Benchmark Context

The repaired downstream-agent benchmark remains a local diagnostic:

- A required passes: 8/9;
- B required passes: 9/9;
- C required passes: 9/9;
- hard vetoes: A = 0, B = 0, C = 0;
- C improves over A on the Joseph backend-certificate case;
- C ties B under the frozen rubric;
- no C-over-B promotion is supported.

## Gap-To-Improvement Mapping

| Observed gap | Implemented improvement | Regression evidence | Boundary |
| --- | --- | --- | --- |
| Packets and workflow outputs were too terse for downstream reasoning. | Phase 1 evidence ledger plus Phase 6 nested packet summaries, decision criteria, risks, and non-claims. | `tests/test_prepare_review_packet.py`, `tests/test_math_review_packet.py`, MCP/CLI preservation tests. | Richer packet context is not proof or reliability evidence. |
| Assumption requests needed route-specific framing. | Phase 2 route-category taxonomy and scoped assumption records. | Assumption/high-level workflow tests from earlier phases and final 79-test regression. | Route-required assumptions are not claimed globally minimal. |
| Proof/counterexample workflows needed concrete backend evidence boundaries. | Phase 3 backend-attempt, obligation, and concrete-counterexample evidence gates. | `tests/test_prove_or_counterexample.py`, final regression. | Proof promotion remains scoped to certifying backend attempts and proved obligations. |
| `derive_from` needed to show how a route was attempted. | Phase 4 diagnostic route plans preserving givens vs explicit assumptions. | `tests/test_derive_from.py`, Phase 7 benchmark oracle alignment, final 70/70 seeded benchmark. | Route plans are diagnostic companions, not proof chains. |
| Math-to-code audits needed traceable context. | Phase 5 trace maps with term traces and alias collisions. | `tests/test_audit_math_to_code.py`, `tests/test_prepare_review_packet.py`, MCP/CLI preservation tests. | Trace maps are structural visibility, not semantic code proof. |
| Agent-callable surfaces could drop rich evidence. | Phase 7 facade/server/CLI tests preserving Phase 6 packet fields and diagnostic descriptions. | `tests/test_mcp_surface_sync.py`, `tests/test_mcp_server.py`, `tests/test_mcp_facade.py`, targeted CLI smoke. | Surface availability is not evidence of downstream-agent correctness. |

## Residual Gaps

- The repaired downstream-agent benchmark has a ceiling/tie problem for B vs C;
  the current implementation does not establish C-over-B improvement.
- No new downstream-agent response collection was run in this program.
- The local seeded benchmark checks deterministic fixtures and simulated
  boundary mutations; it does not establish external benchmark validity.
- Review packets are more self-contained, but human/domain understanding and
  formal proof obligations remain outside the packet unless supplied by
  certifying backends or reviewed sources.
- Claude Phase 6 review only converged through a minimal no-file-inspection
  fallback prompt after broader review prompts stalled, so local tests carry
  the main evidentiary weight for Phase 6/7.
- Future material Claude review gates should use the hardened claudecodex
  `claude_review_gate.sh` transport. That improves review-gate reliability and
  logging discipline, but it does not retroactively strengthen the Phase 6
  review evidence.

## Decision

The implementation program has enough local regression evidence to close this
runbook as complete for the scoped objective: high-level mathematical workflow
tools now expose richer structured evidence, route plans, proof/counterexample
metadata, assumption taxonomy, trace maps, and review packets through local
agent-callable surfaces while preserving stated boundaries.

The next safe work lane is benchmark maintenance or a new downstream-agent
collection designed to test whether the richer packets measurably improve
agent work quality. That would require a separate plan and evidence contract.
