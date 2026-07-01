# Phase 1 Subplan: Real Local Case Inventory

Date: 2026-06-30

Status: `DRAFT_READY_AFTER_PHASE_0`

## Phase Objective

Inventory 5-10 realistic high-level workflow benchmark candidate cases from
local repos, especially `latex-papers` docs and each repo's `docs` materials,
without copying large source text or making public benchmark claims.

## Entry Conditions Inherited From Previous Phase

- Phase 0 baseline result exists.
- Local source paths are readable.
- The benchmark remains local/non-gating.
- Dirty worktree state is recorded and unrelated changes are preserved.

## Required Artifacts

- Candidate inventory:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-01-case-inventory-2026-06-30.md`.
- Candidate coverage matrix with workflow type, route type, outcome type,
  source family, expected evidence, negative-control status, and local-only
  provenance boundary.
- Phase 1 result:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-01-real-local-case-inventory-result-2026-06-30.md`.
- Updated ledger entry.
- Refreshed Phase 2 subplan review note.

## Required Checks, Tests, And Reviews

- Verify readable local source roots before inventory.
- Use `rg`/`find` to identify candidate docs under `../latex-papers` and other
  local repo `docs` directories.
- Record only bounded anchors: repo, path, line/range candidate, task type,
  expected evidence class, and forbidden claims.
- Local check that inventory has 5-10 candidates and covers at least four
  workflow families.
- Local check that the coverage matrix includes success, justified abstention,
  negative control, backend-unavailable or not-encodable, and source-mismatch
  or evidence-gap outcomes where feasible.
- Claude read-only review is material if the inventory makes non-obvious case
  inclusion/exclusion decisions and tenant policy permits a compact sanitized
  brief.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Which local repo-derived cases should seed the real-local high-level workflow benchmark? |
| Baseline/comparator | Phase 0 current workflow baseline and prior five-case source-adapter pilot. |
| Primary criterion | 5-10 candidates with bounded source anchors, workflow labels, expected evidence, negative-control opportunities, forbidden claims, and a workflow-type x route-type x outcome-type coverage matrix. |
| Veto diagnostics | Wholesale source copying; cases chosen only because current workflows pass; no negative controls; fewer than four workflow families; missing route/outcome coverage matrix; source paths unavailable; public/release/scientific claims. |
| Explanatory diagnostics | Source-family coverage, workflow-family coverage, line-anchor availability, expected backend/source evidence. |
| Not concluded | Final benchmark schema, pass/fail scoring, capability improvement, or public benchmark validity. |

## Forbidden Claims And Actions

- Do not copy large source excerpts into the inventory.
- Do not edit sibling repos.
- Do not select cases based on current workflow output.
- Do not claim case inclusion means the source theorem is true or false.
- Do not promote local cases to public fixtures.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 when the inventory has 5-10 bounded candidate cases, enough
workflow diversity, explicit negative-control opportunities, route/outcome
coverage, and no source access or boundary blocker.

## Stop Conditions

Stop if local source roots are missing, fewer than five candidate cases can be
anchored without broad copying, source licensing/privacy boundary is unclear,
or case choice requires a project-direction decision.

## End-Of-Phase Protocol

At phase end: run required checks; write the Phase 1 result; refresh/review the
Phase 2 subplan; review boundary safety; then advance or stop.
