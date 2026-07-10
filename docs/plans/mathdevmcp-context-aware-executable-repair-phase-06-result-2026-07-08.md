# Phase 06 Result: Document-Ready Repair Report Regression

Date: 2026-07-09

Status: `PASSED`

## Objective

Render document-ready repair proposals from ranked branch evidence and run the
frozen risky-debt and credit-card NPV regression set.

## Implementation Summary

- Added the structured proposal contract
  `context_aware_executable_repair_proposal`.
- Each target now exposes `document_ready_repair_proposals` in the compact tree.
- Each proposal is derived from the top-ranked branch and includes:
  - location and source span;
  - problem and derivation-specific why;
  - already-stated assumptions;
  - missing or unresolved assumptions;
  - proposed assumption set;
  - proposed LaTeX repair text;
  - derivation route under the proposed assumptions;
  - backend evidence and translation attempts;
  - remaining blockers before certification;
  - explicit non-claims.
- Markdown now renders `Document-ready repair proposals` before the lower-level
  branch dump.
- Fixed LaTeX conditional-bar parsing so `\middle|` is not partially parsed as
  `\mid`.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the final high-level report produce good repair proposals for frozen targets? |
| Baseline/comparator | Phase 04/05 display-equation frozen reports. |
| Primary criterion | Passed. Frozen targets now show proposition/context packets where relevant, local context status, typed assumptions, backend attempts/blockers, ranked branches, and branch-derived document-ready repair text. |
| Veto diagnostics | No veto triggered. Reports are not template-only, frozen targets are present, backend evidence/blockers are visible, and non-claims remain explicit. |
| Not concluded | No whole-document proof, release readiness, global optimality, or global minimality is claimed. |

## Frozen Regression Artifacts

- Risky-debt Markdown:
  `docs/reviews/risky-debt-document-ready-repair-phase06-frozen-2026-07-09.md`
- Risky-debt JSON:
  `docs/reviews/risky-debt-document-ready-repair-phase06-frozen-2026-07-09.json`
- Credit-card NPV Markdown:
  `docs/reviews/credit-card-npv-document-ready-repair-phase06-frozen-2026-07-09.md`
- Credit-card NPV JSON:
  `docs/reviews/credit-card-npv-document-ready-repair-phase06-frozen-2026-07-09.json`

Frozen report summary:

- Risky-debt selected rows: `2`.
- Risky-debt proposition/context packets: `1`.
- Risky-debt typed repair obligations: `3`.
- Risky-debt ranked branches: `6`.
- Credit-card NPV selected rows: `4`.
- Credit-card NPV typed repair obligations: `4`.
- Credit-card NPV ranked branches: `12`.
- Both frozen reports include `Document-ready repair proposals`, proposed
  LaTeX, remaining blockers before certification, and non-claims.
- The previous `\middle|` parsing defect was checked absent from the generated
  credit-card report.

## Checks

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`
  - Passed: `21 passed in 116.57s`.
- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_document_derivation_tree.py -q`
  - Passed: `34 passed in 133.34s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_tree_report.py`
  - Passed.
- Frozen regression commands:
  - `python3 -m mathdevmcp.cli audit-document-derivation-tree docs/risky-debt-maliar-deep-learning-lecture-note.tex --focus-label prop:interior-foc --focus-label eq:foc-k --focus-label eq:foc-b --max-attempts 1 --output-md docs/reviews/risky-debt-document-ready-repair-phase06-frozen-2026-07-09.md --output-json docs/reviews/risky-debt-document-ready-repair-phase06-frozen-2026-07-09.json`
  - `python3 -m mathdevmcp.cli audit-document-derivation-tree docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex --focus-label eq:panel-npv-functional --focus-label eq:incremental-cash-flow --focus-label eq:incremental-npv --max-attempts 1 --output-md docs/reviews/credit-card-npv-document-ready-repair-phase06-frozen-2026-07-09.md --output-json docs/reviews/credit-card-npv-document-ready-repair-phase06-frozen-2026-07-09.json`
  - Both completed and wrote artifacts.
- Frozen report content assertions:
  - Passed. Proposals have the expected contract, top-branch linkage, problem,
    why, proposed assumptions, proposed LaTeX, blockers, and non-claims.
- `git diff --check`
  - Passed.

## Review

Claude review remains unavailable under the Phase 00 external-service rejection
boundary. Codex performed a local read-only skeptical review:

- Branch-derived proposal boundary: no proof or minimality overclaim found.
- Frozen target coverage: no missing focus labels in risky-debt or credit-card
  regression reports.
- External-tool evidence: backend attempts, translation attempts, and typed
  blockers remain visible.
- Report usefulness: the high-level proposal section now appears before the
  low-level branch dump and contains concrete proposed LaTeX.

Remaining risk:

- The proposed LaTeX text is a conservative assumptions-and-route insertion; it
  is not an automatically applied document edit and is not a formal proof.
- The branch search is deterministic evidence ordering, not full MCTS or
  global search.

## Lane Handoff

The visible runbook phases are complete for this lane.

Recommended next lane:

- Improve backend-native formalization generation for the top-ranked repair
  proposals, especially Lean/Sage encodings for conditional expectation,
  integrability, and finite-state expectation routes.
