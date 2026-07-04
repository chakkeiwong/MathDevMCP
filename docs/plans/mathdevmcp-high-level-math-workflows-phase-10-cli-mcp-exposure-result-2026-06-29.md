# Phase 10 Result: CLI And MCP Exposure

Date: `2026-06-29`

## Result

`PASS_WITH_REVIEWER_UNAVAILABLE`

## Phase Objective

Expose the benchmarked high-level workflows through CLI and MCP surfaces.

## Entry Conditions Verified

- Phase 9 question-level benchmark passed.
- High-level quality report passed with `14` cases across `6` workflows,
  `12` negative controls, stable deterministic rerun, and all mutation probes.
- Benchmark gate passed `70/70`.
- High-level contract schema remained stable.

## Skeptical Plan Audit

- Baseline/comparator was the existing CLI/MCP low-level workbench surface.
- The public surface is limited to the six Phase 9 benchmarked high-level
  workflows plus the high-level workflow quality report.
- CLI/MCP wrappers are thin delegates and preserve the library envelope fields:
  `metadata`, `non_claims`, `evidence_classes`, `certification_source`,
  `veto_reasons`, `assumptions`, and `counterexamples`.
- Benchmark pass is treated as an exposure prerequisite, not release readiness
  or broad theorem-proving evidence.
- No package installation, network fetch, release-policy change, or destructive
  action was needed.

## Artifacts

- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/mcp_server.py`
- `tests/test_mcp_facade.py`
- `tests/test_mcp_server.py`
- `tests/test_release_smoke.py`

## Exposed CLI Commands

- `derive-from`
- `prove-or-counterexample`
- `assumptions-for`
- `debug-derivation`
- `audit-math-to-code`
- `prepare-review-packet`
- `high-level-workflow-quality`

## Exposed MCP Tools

- `derive_from`
- `prove_or_counterexample`
- `assumptions_for`
- `debug_derivation`
- `audit_math_to_code`
- `prepare_review_packet`
- `high_level_workflow_quality`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can users access benchmarked high-level workflows through stable command/API surfaces? |
| Primary criterion | Passed. CLI/MCP tools return high-level contract envelopes and expose no unbenchmarked high-level workflow. |
| Veto diagnostics | Passed. Tests verify non-claims, evidence classes, certification source, and diagnostic-only/structural boundaries survive wrappers. |
| Explanatory diagnostics | CLI smoke tests, MCP facade/server tests, benchmark gate, and high-level quality report. |
| Not concluded | Product readiness, release readiness, external benchmark validity, or broad theorem proving. |

## Checks Run

- `python -m pytest tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_release_smoke.py::test_cli_high_level_workflow_commands_return_contract_envelopes tests/test_release_smoke.py::test_cli_high_level_workflow_quality_module_command_passes`
  - Result: `39 passed`
- `python -m pytest tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py tests/test_context_and_fixtures.py::test_high_level_workflow_quality_report_uses_actual_seeded_results`
  - Result: `33 passed`
- `python -m py_compile src/mathdevmcp/cli.py src/mathdevmcp/mcp_facade.py src/mathdevmcp/mcp_server.py`
  - Result: passed
- `python -m mathdevmcp.cli benchmark-gate --root .`
  - Result: passed `70/70`
- `python -m mathdevmcp.cli high-level-workflow-quality --root .`
  - Result: `quality_thresholds_passed`
- `python -m pytest tests/test_release_smoke.py::test_cli_benchmark_gate_module_command_passes tests/test_release_smoke.py::test_cli_workbench_benchmark_quality_module_command_passes tests/test_release_smoke.py::test_cli_high_level_workflow_quality_module_command_passes`
  - Result: `3 passed`
- `git diff --check`
  - Result: passed

## Claude Review

Claude was used only as a read-only reviewer.

- Phase 10 compact review prompt did not return a verdict.
- Interrupt produced `Execution error`.
- Tiny probe returned `OK`.
- Smaller review prompt also did not return a verdict.
- Interrupt produced `Execution error`.

This is recorded as reviewer unavailable after successful liveness probe and
prompt redesign. It is not Claude approval. The phase proceeded because local
checks directly answered the Phase 10 evidence contract and no human/runtime/
funding/product/scientific boundary was crossed.

## Decision

Proceed to Phase 11 docs/operator UX.

## Refreshed Phase 11 Subplan Review

Phase 11 remains consistent with this result:

- Entry condition is satisfied by CLI/MCP exposure and passing tests.
- Docs must document all seven new commands/tools and benchmark interpretation.
- Docs must state non-claims: no general theorem proving, no proof by
  structural/diagnostic/review-packet evidence, no release readiness, and no
  external benchmark validity.
- Stop condition remains correct: stop if docs cannot describe workflows
  without overclaiming.
