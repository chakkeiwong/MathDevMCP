# Phase 3 Subplan: Apply To Credit-Card NPV Document

Date: 2026-07-07

Status: `EXECUTED`

## Phase Objective

Run the new workflow on the credit-card NPV final submission and generate
agent-consumable JSON and Markdown rigor reports.

## Entry Conditions

- Phase 2 CLI/MCP gates passed.
- Target document exists.
- Backend provenance check is available.

## Required Artifacts

- `docs/reviews/credit-card-npv-component-proposal-rigor-audit.md`
- `docs/reviews/credit-card-npv-component-proposal-rigor-audit.json`
- Phase 3 result record.

## Required Checks/Tests/Reviews

- Run the workflow against the exact final submission file, not the whole folder.
- Confirm generated report includes backend provenance, partial coverage,
  tool-use ledger, and at least one concrete gap/proposal entry.
- Confirm `git diff -- docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex`
  is empty.
- Claude read-only review of a bounded excerpt or summary of generated report,
  not the whole document.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the new workflow produce a useful rigor gap/proposal report for the substantial target document? |
| Baseline/comparator | Manual proposed plan and existing individual tool behavior. |
| Primary criterion | JSON/Markdown reports exist and contain concrete locations, problems, mathematical rationale, proposed fixes, backend provenance, and explicit partial coverage. |
| Veto diagnostics | Report is handwavy; report omits locations; no why/fix fields; target source modified; LeanDojo proof-search promoted to certificate; folder duplicate versions included by mistake. |
| Explanatory diagnostics | Equation counts, selected labels, backend availability, per-gap tool uses. |
| Not concluded | No full-document proof, no product capability, no scientific validation, no source edits. |

## Forbidden Claims/Actions

- Do not audit the entire folder as if it were one source file.
- Do not edit the target `.tex` file.
- Do not claim the generated report is exhaustive unless coverage confirms it.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 only if generated artifacts are present, bounded, and pass
the primary report-shape checks.

## Stop Conditions

Stop if the target report cannot be generated without hand-editing the target
document, or if the output regresses to generic recommendations.
