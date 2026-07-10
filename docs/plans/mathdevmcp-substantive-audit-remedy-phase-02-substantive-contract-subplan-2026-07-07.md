# Phase 2 Subplan: Substantive Proposal Contract

Date: 2026-07-07

Status: `DRAFT_PENDING_PHASE_1`

## Phase Objective

Introduce and enforce a substantive proposal contract so high-level audit
reports separate concrete mathematical repairs from non-actionable diagnostics.

## Entry Conditions

- Phase 1 passed, so evidence selection can be scoped to exact files.

## Required Artifacts

- Contract helper or schema for substantive proposals.
- Updated `audit_math_document_rigor` normalization and Markdown rendering.
- Focused tests that reject generic concrete fixes.
- Phase 2 result record.

## Required Checks/Tests/Reviews

- `tests/test_math_document_rigor.py`.
- New tests for concrete-fix ledger vs diagnostic ledger.
- `git diff --check`.
- Review next Phase 3 subplan.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the report prevent weak slogans from appearing as concrete fixes? |
| Baseline/comparator | Current report where "Then prove" and "Add review boundary" appear as fixes. |
| Primary criterion | Concrete ledger entries carry an actionable replacement, derivation route, safe report wording, or smallest next audit. Bare proof targets or assumption lists are diagnostic unless paired with one of those payloads. |
| Veto diagnostics | Generic "then prove" in concrete ledger; proof-target-only or assumption-list-only concrete entries; lost `math_fix`; lost replacement LaTeX; no backend/certification boundary; field-presence-only tests. |
| Explanatory diagnostics | Substance classification, missing-payload reasons, source low-level detail refs. |
| Not concluded | That a proposed fix is mathematically correct unless certified. |

## Forbidden Claims/Actions

- Do not certify unverified derivations.
- Do not hide diagnostics; demote them clearly.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 3 only if report rendering exposes rich math payloads,
non-actionable items are visibly separated, and tests reject bare proof-target
or assumption-list-only concrete fixes.

## Stop Conditions

Stop if the lower-level reports lack enough payload to classify substance and
need redesign before rendering.
