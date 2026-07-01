# Phase 0 Subplan: Governance And Baseline

## Phase Objective

Confirm the current repository baseline, workbench benchmark status, dirty
worktree boundaries, and no-download/no-release-claim launch conditions for the
high-level workflow program.

## Entry Conditions Inherited From Previous Phase

- Master program and visible runbook exist.
- Existing low-level workbench and workbench benchmark artifacts are present.

## Required Artifacts

- Phase 0 result record.
- Baseline command outputs summarized in the result.
- Refreshed Phase 1 subplan if baseline reveals a sequencing issue.

## Required Checks, Tests, Reviews

- `git status --short`.
- `PYTHONPATH=src python -m mathdevmcp.cli benchmark-gate --root .`.
- `PYTHONPATH=src python -m mathdevmcp.cli workbench-benchmark-quality --root .`.
- Focused low-level workbench tests needed to establish baseline:
  `tests/test_math_debugging_kernel.py`,
  `tests/test_math_debugging_router.py`,
  `tests/test_derive_or_refute.py`,
  `tests/test_prove_or_refute.py`,
  `tests/test_assumption_discovery.py`,
  `tests/test_counterexample_search.py`,
  `tests/test_proof_gap.py`,
  `tests/test_equation_code_match.py`,
  `tests/test_math_review_packet.py`,
  `tests/test_math_claim_classifier.py`,
  `tests/test_math_to_tests.py`,
  `tests/test_literature_local_audit.py`,
  `tests/test_notation_reconciliation.py`,
  `tests/test_math_change_impact.py`,
  `tests/test_workbench_benchmark_schema.py`,
  `tests/test_context_and_fixtures.py`,
  `tests/test_mcp_facade.py`,
  `tests/test_mcp_server.py`,
  `tests/test_release_smoke.py`.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the repo ready to start high-level workflow implementation without confusing baseline failures or dirty-worktree ownership? |
| Baseline/comparator | Existing benchmark gate and workbench quality report. |
| Primary pass criterion | Baseline checks either pass or failures are clearly unrelated/recorded before implementation. |
| Veto diagnostics | Hidden benchmark failure; release-publication dirty-worktree caveat treated as workflow blocker; unapproved network or external data dependency. |
| Explanatory diagnostics | Dirty worktree summary and focused baseline outputs. |
| Not concluded | High-level workflow correctness or release readiness. |
| Artifact | Phase 0 result. |

## Forbidden Claims And Actions

- Do not edit unrelated dirty files.
- Do not fetch external benchmark data.
- Do not claim release readiness.
- Do not treat dirty-worktree public-release caveats as high-level workflow
  failures.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 if the existing benchmark/workbench baseline is usable or
any unrelated caveat is documented with a safe implementation boundary.

## Stop Conditions

Stop if the existing low-level workbench or benchmark gate is broken in a way
that would make high-level workflow tests meaningless and cannot be repaired
locally within this program.
