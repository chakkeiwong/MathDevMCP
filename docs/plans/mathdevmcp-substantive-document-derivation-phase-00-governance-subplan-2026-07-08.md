# Phase 00 Subplan: Governance And Baseline Gate

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Record the exact regression being fixed, lock the evidence contract, and create
a launch gate for implementation phases.

## Entry Conditions Inherited From Previous Phase

- User has rejected generic document reports that contain weak mathematical
  repair text.
- Existing `audit_document_derivation_tree` and tree renderer preserve claim
  boundaries but lack enough upstream evidence for concrete fixes.
- Repo policy already requires external-tool-first mathematical search.

## Required Artifacts

- Master program:
  `docs/plans/mathdevmcp-substantive-document-derivation-master-program-2026-07-08.md`
- Visible runbook:
  `docs/plans/mathdevmcp-substantive-document-derivation-visible-runbook-2026-07-08.md`
- Execution ledger:
  `docs/plans/mathdevmcp-substantive-document-derivation-visible-ledger-2026-07-08.md`
- Compact review bundle:
  `docs/reviews/mathdevmcp-substantive-document-derivation-plan-review-bundle-2026-07-08.md`
- Phase result:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-00-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- Local artifact check: plan files exist and mention all required evidence
  contract fields.
- Read-only Claude review gate when available.
- If Claude is unavailable, record the probe/gate failure and use a fresh Codex
  read-only review instead.
- Phase result must include the master-program manifest and decision-table
  fields.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the proposed program aimed at the real generic-tool regression rather than a one-off document repair? |
| Baseline/comparator | Current `audit_document_derivation_tree` output and existing external-tool-first lane. |
| Primary criterion | The master program and subplans require semantic source reconstruction, branch-linked assumptions, formalization stubs, external-tool evidence, concrete patch text, and non-claims. |
| Veto diagnostics | Missing stop conditions; card-specific implementation; renderer-only workaround; no local tests; Claude treated as execution authority. |
| Explanatory diagnostics | Claude unavailable, stale dirty worktree, optional backend absence. |
| Not concluded | No implementation correctness or report quality claim yet. |
| Artifact | Phase 00 result note and review trail. |

## Forbidden Claims Or Actions

- Do not claim the report quality is fixed in Phase 00.
- Do not modify runtime code in Phase 00 except plan/runbook artifacts.
- Do not let Claude edit files, run commands, or authorize scientific claims.
- Do not launch detached supervisors from this visible runbook.

## Exact Next-Phase Handoff Conditions

Advance to Phase 01 only if:

- local artifact checks pass;
- the review gate returns `AGREE` or a documented bounded fallback agrees with
  explicit non-claims;
- Phase 00 result records the skeptical audit and remaining risks.

## Stop Conditions

Stop if:

- review identifies a material plan flaw that cannot be patched without a
  project-direction decision;
- the runbook would require detached execution despite the visible-template
  boundary;
- implementation would need external installs or network access before Phase
  01 can even start.

## End-Of-Subplan Actions

1. Run local artifact checks.
2. Write the Phase 00 result / close record.
3. Draft or refresh Phase 01 subplan.
4. Review Phase 01 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
5. If review returns `REVISE`, visibly patch the plan and rerun focused
   artifact checks before implementation.
