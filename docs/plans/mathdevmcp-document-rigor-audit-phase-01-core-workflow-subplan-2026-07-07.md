# Phase 1 Subplan: Core Python Workflow MVP

Date: 2026-07-07

Status: `EXECUTED`

## Phase Objective

Add a reusable Python module that plans and runs a focused mathematical
document-rigor audit, producing structured JSON and Markdown without source
document edits.

## Entry Conditions

- Phase 0 gate passed.
- Master program and runbook are reviewed.
- Existing dirty worktree changes are preserved.

## Required Artifacts

- `src/mathdevmcp/math_document_rigor.py`
- `tests/test_math_document_rigor.py`
- Optional focused fixture or use existing fixture documents.
- Phase 1 result record.
- Refreshed Phase 2 subplan if implementation shape changes.

## Required Checks/Tests/Reviews

- `python3 -m pytest -q tests/test_math_document_rigor.py`
- Focused import smoke for `mathdevmcp.math_document_rigor`.
- `git diff --check` over edited source/tests/plans.
- Claude read-only review of implementation diff if material boundary questions remain.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can a reusable Python workflow produce a valid rigor audit packet from a LaTeX document using existing tools? |
| Baseline/comparator | Existing individual tools plus manual plan. |
| Primary criterion | Library functions return valid contract payloads with backend provenance, equation inventory, target selection, tool-use ledger, coverage, gaps/proposals, and Markdown rendering. |
| Veto diagnostics | Yes/no-only result; missing location/problem/why/fix; LeanDojo as certificate; missing partial coverage; exceptions on ordinary LaTeX fixture; target source edits. |
| Explanatory diagnostics | Unit tests, sample fixture report, backend capability fields. |
| Not concluded | No proof of target document; no full-document coverage; no scientific/product validation. |

## Forbidden Claims/Actions

- Do not claim the workflow proves a document.
- Do not require LeanDojo for base tests.
- Do not edit the credit-card NPV document in Phase 1.
- Do not add a large new parser when existing localization tools suffice.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if:

- tests pass;
- library output has contract metadata;
- Markdown renderer includes location/problem/why/fix/tool-use sections;
- backend provenance distinguishes active/backend Python and LeanDojo boundary.

## Stop Conditions

Stop if existing tools cannot provide enough evidence for non-handwavy entries
without redesigning the workflow contract, or if implementation requires
package installation/network fetch.
