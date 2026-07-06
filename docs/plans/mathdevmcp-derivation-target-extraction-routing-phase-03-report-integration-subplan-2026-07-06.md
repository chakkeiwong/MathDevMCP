# Phase 3 Subplan: Report Integration

Date: 2026-07-06

Status: `DRAFT_NEXT`

## Phase Objective

Integrate target extraction and route planning into
`audit_and_propose_derivations` so label reports group extracted obligations
under parent labels and route each obligation through the existing derivation
gap/proposal workflow.

## Entry Conditions Inherited From Previous Phase

- Phase 1 target extraction passed.
- Phase 2 route planner passed.
- Existing report tests pass.

## Required Artifacts

- Updated `src/mathdevmcp/derivation_audit_report.py`.
- Updated `tests/test_derivation_audit_report.py`.
- Optional updates to MCP/CLI tests only if output schema changes public
  behavior.
- Phase 3 result:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-03-report-integration-result-2026-07-06.md`
- Refreshed Phase 4 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py -q`
- `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
- `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/backend_route_planner.py`
- `git diff --check -- src/mathdevmcp/derivation_audit_report.py tests/test_derivation_audit_report.py docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-03-report-integration-result-2026-07-06.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can reports use extracted obligations instead of full blocks while preserving existing report usefulness? |
| Baseline/comparator | Current risky-debt report with two full-block targets. |
| Primary criterion | Label report records extracted target count and target-level proposals with parent label, equation label, line, lhs/rhs, route plan, validation, and assumption repairs. |
| Veto diagnostics | Missing old report fields; target grouping confusing; route plan hidden; report less concrete; generic proposal text. |
| Explanatory diagnostics | Extracted target count, fallback count, validation status counts. |
| Not concluded | No proof of risky-debt note; no source edits. |
| Artifact | Updated report workflow/tests/result. |

## Forbidden Claims/Actions

- Do not remove direct-target support.
- Do not break existing CLI/MCP contract.
- Do not claim route planner evidence is proof.
- Do not edit source documents.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 only if:

- report tests verify extracted obligation grouping;
- direct target and label paths both work;
- Phase 4 subplan names exact risky-debt output path and inspection criteria.

## Stop Conditions

Stop if:

- extracted-target integration breaks high-level validation;
- Markdown loses required fields;
- public wrappers require broad contract redesign.
