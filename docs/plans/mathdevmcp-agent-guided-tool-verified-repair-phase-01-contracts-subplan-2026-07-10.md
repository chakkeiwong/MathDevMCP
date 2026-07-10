# Phase 01 Subplan: Strict Contracts And Regression Gates

Date: 2026-07-10

Status: `DRAFT_PENDING_PHASE_00`

## Phase Objective

Define strict machine-readable contracts and failing/passing regression gates
that prevent diagnostic-only or raw-agent branches from rendering as repair
proposals.

## Entry Conditions Inherited From Previous Phase

- Phase 00 plan and review gate passed.
- Baseline failure mode is recorded: blocked ranked branches can look like
  document-ready fixes.

## Required Artifacts

- New or updated Python contracts for:
  `AgentHypothesisExpansion`, `ToolGroundedSearchPath`,
  `BackendFormalizationTarget`, `ToolGroundedRepairProposal`, and
  `DocumentGapReport`.
- Focused tests covering proposal leakage and closure-status discipline.
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-01-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_derivation_branch_controller.py -q`
- New focused tests for strict contracts.
- `python3 -m py_compile` on modified modules.
- `git diff --check`.
- Read-only review of the contract boundary if material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can contracts prevent raw agent hypotheses and diagnostic-only branches from becoming repair proposals? |
| Baseline/comparator | Existing `context_aware_executable_repair_proposal` generation from top-ranked branch. |
| Primary criterion | Tests fail if a blocked or diagnostic-only branch renders as a repair proposal; blocked paths render as gap reports. |
| Veto diagnostics | Closure status missing; raw agent text emitted as fix; diagnostic evidence promoted; no evidence refs per repair step. |
| Explanatory diagnostics | Existing reports may get more conservative. |
| Not concluded | No recursive search or backend expansion yet. |
| Artifact | Contract code, tests, and Phase 01 result. |

## Forbidden Claims Or Actions

- Do not add recursive search yet.
- Do not weaken current promotion guards.
- Do not certify LeanDojo, retrieval, route plans, or proof-state traces.

## Exact Next-Phase Handoff Conditions

Advance to Phase 02 only if strict contracts are in place and focused tests
prove blocked paths cannot render as final repair proposals.

## Stop Conditions

Stop if the current report API cannot be changed without breaking public
contracts and no compatibility route is clear.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 01 result / close record.
3. Draft or refresh Phase 02 subplan.
4. Review Phase 02 for consistency and boundary safety.
