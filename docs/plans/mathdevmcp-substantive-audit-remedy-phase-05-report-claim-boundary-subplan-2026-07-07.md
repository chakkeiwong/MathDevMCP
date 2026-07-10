# Phase 5 Subplan: Report Claim Boundary Workflow

Date: 2026-07-07

Status: `DRAFT_PENDING_PHASE_4`

## Phase Objective

Add `audit_report_claim_boundary` to classify report-status and nonclaim
language separately from mathematical theorem claims.

## Entry Conditions

- Phase 4 passed.
- Scope and nonclaim vocabulary is available.

## Required Artifacts

- New library workflow.
- CLI/MCP/FastMCP exposure.
- Tests for D447 nonclaim/report-status classification.
- Phase 5 result record.

## Required Checks/Tests/Reviews

- New workflow tests.
- Interface tests.
- Existing `classify_math_claim` tests if reused/updated.
- `git diff --check`.
- Review next Phase 6 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the tool classify nonclaim/report-status assertions without treating them as theorems? |
| Baseline/comparator | Current `classify_math_claim` returning unsupported for mixed nonclaim/status text. |
| Primary criterion | Output identifies mathematical_claim=false, document evidence needed, overclaim risks, missing evidence, and safe wording. |
| Veto diagnostics | Requires proof certificate for nonclaim text; ignores document evidence; unsupported-only answer; suggests overclaiming wording. |
| Explanatory diagnostics | Matched boundary phrases, evidence snippets, missing support categories. |
| Not concluded | Truth of the underlying scientific report. |

## Forbidden Claims/Actions

- Do not validate report scientific truth.
- Do not edit source reports.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 only if report-boundary claims produce actionable document
evidence requirements and safe wording.

## Stop Conditions

Stop if the workflow cannot classify report-status language without a larger
document-evidence index. The stop handoff must include the minimal unsupported
claim text, the unavailable document-evidence dependency, and the next design
question for human review.
