# Phase 0 Subplan: Governance And Baseline Audit

## Phase Objective

Establish the workbench execution boundary, audit existing derivation/proof
surfaces, and confirm the first implementation phase can proceed without
release, benchmark-gate, or scientific-claim overreach.

## Entry Conditions Inherited From Previous Phase

- Master program exists.
- Visible gated execution runbook exists.
- Claude review trail and execution ledger exist.
- No previous phase artifacts are required.

## Required Artifacts

- `docs/plans/mathdevmcp-math-debugging-workbench-master-program-2026-06-28.md`
- `docs/plans/mathdevmcp-math-debugging-workbench-visible-gated-execution-plan-2026-06-28.md`
- `docs/plans/mathdevmcp-math-debugging-workbench-visible-execution-ledger-2026-06-28.md`
- `docs/plans/mathdevmcp-math-debugging-workbench-claude-review-trail-2026-06-28.md`
- `docs/plans/mathdevmcp-math-debugging-workbench-phase-00-governance-baseline-result-2026-06-28.md`
- Refreshed Phase 1 subplan.

## Required Checks, Tests, Reviews

- `git status --short`
- `rg -n "derive|proof|assumption|counterexample|lean|sympy|sage|proof_packet" src tests docs/mathdevmcp-operator-guide.md README.md`
- `PYTHONPATH=src python -m pytest -q tests/test_proof_obligations.py tests/test_symbolic_backend.py tests/test_proof_audit_v2.py tests/test_proof_packet.py tests/test_mcp_facade.py tests/test_mcp_surface_sync.py`
- Claude read-only review of the master program and Phase 1 handoff brief.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the workbench program properly bounded and grounded in current repo surfaces before implementation begins? |
| Baseline/comparator | Existing derivation/proof/packet/MCP modules and tests. |
| Primary pass criterion | Existing proof-related tests pass or failures are documented as unrelated; Phase 1 has a complete, bounded subplan. |
| Veto diagnostics | Missing stop conditions, release/gate/science overclaim, plan depending on unavailable network/setup, or Claude material blocker after five rounds. |
| Explanatory diagnostics | Search inventory and test results. |
| Not concluded | Any new workbench capability, release readiness, or proof completeness. |
| Artifact | Phase 0 result record and reviewed/refreshed Phase 1 subplan. |

## Forbidden Claims And Actions

- Do not claim any workbench function is implemented in Phase 0.
- Do not alter release policy or benchmark gates.
- Do not install packages or fetch network dependencies.
- Do not treat Claude review as execution authority.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only if:

- Phase 0 result exists;
- baseline proof-related checks are run and recorded;
- Phase 1 subplan exists and passes Codex consistency review;
- Claude review is either `AGREE`/non-blocking or unavailable after probe and
  prompt redesign attempts are recorded.

## Stop Conditions

Stop and write a blocker result if:

- the master program has an unresolved material sequencing flaw;
- baseline tests fail in a way that makes Phase 1 unsafe to interpret;
- Claude and Codex do not converge after five review rounds for the same
  material blocker;
- continuing requires package installation, credentials, network, or a
  project-direction decision outside this program.
