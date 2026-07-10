# Phase 06 Subplan: Document-Ready Repair Report Regression

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Render document-ready repair proposals from ranked branch evidence and run the
frozen regression set.

## Entry Conditions Inherited From Previous Phase

- Branch search can rank branches and preserve evidence/blockers.
- Executable/backend blockers are attached to typed obligations.

## Required Artifacts

- Markdown/JSON report contract for context-aware executable repair proposals.
- Frozen regression reports for risky-debt and credit-card NPV labels.
- Comparison note against Phase 04 display-equation reports.
- Phase result:
  `docs/plans/mathdevmcp-context-aware-executable-repair-phase-06-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_tree_report.py`
- Frozen regression commands with bounded logs.
- Read-only review of final report boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the final high-level report produce good repair proposals for frozen targets? |
| Baseline/comparator | Phase 04 display-equation frozen reports from the previous lane. |
| Primary criterion | Proposition targets are handled; local context is used; assumptions are stated/missing with evidence; executable attempts or typed blockers are shown; repair text is document-ready and branch-derived. |
| Veto diagnostics | Template-only proposal; proof overclaim; missing frozen target; no backend attempt/blocker; no non-claims. |
| Explanatory diagnostics | Remaining unsupported operators, backend absence, budget exhaustion. |
| Not concluded | No whole-document proof, release readiness, or global minimality. |
| Artifact | Final reports and Phase 06 result. |

## Forbidden Claims Or Actions

- Do not tune only to credit-card NPV.
- Do not claim proof from diagnostic branches.
- Do not hide missing proposition targets.

## Exact Next-Phase Handoff Conditions

Close the lane only if frozen reports pass the primary criterion or write a
blocker result explaining the remaining generic gap.

## Stop Conditions

Stop if final reports remain template-only after typed obligations and backend
attempts are available.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 06 result / close record.
3. Write final handoff.
4. Review final artifacts for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
