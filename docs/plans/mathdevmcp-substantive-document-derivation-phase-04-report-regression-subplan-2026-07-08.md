# Phase 04 Subplan: Report Integration And Regression Gate

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Integrate richer semantic packets, assumption branches, and formalization
evidence into `audit_document_derivation_tree`, then run generic and hard
document regression reports.

## Entry Conditions Inherited From Previous Phase

- Semantic packets reconstruct full display targets.
- Assumption branches show closure routes.
- Formalization stubs and blockers are recorded without proof overclaiming.

## Required Artifacts

- Updated markdown/JSON report contract.
- Generic fixtures for NPV, conditional expectation, Bellman, shape, and FOC
  style targets.
- Hard-document smoke reports for:
  - risky-debt lecture note;
  - credit-card NPV component proposal;
  using them only as regression targets.
- Frozen regression commands must include:
  - risky debt file
    `docs/risky-debt-maliar-deep-learning-lecture-note.tex` with labels
    `eq:risky-pricing`, `prop:interior-foc`, `eq:foc-k`, `eq:foc-b`;
  - credit-card file
    `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex`
    with labels `eq:panel-npv-functional`, `eq:incremental-cash-flow`,
    `eq:incremental-npv`.
- Baseline artifacts for qualitative comparison:
  - `docs/reviews/risky-debt-derivation-gap-proposals-v2.md`;
  - `docs/reviews/credit-card-npv-generic-document-derivation-tree-smoke-2026-07-08.md`.
- Phase result:
  `docs/plans/mathdevmcp-substantive-document-derivation-phase-04-result-2026-07-08.md`
- Phase result must include a run manifest and decision table as specified in
  the master program.

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_tree_report.py`
- `git diff --check`
- Generate bounded smoke reports with the frozen focus labels above.  Extra
  `--max-labels` exploratory runs may be explanatory only and cannot replace
  the frozen regression set.
- Read-only review of final result and report claim boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the high-level report materially improve without becoming document-specific or overclaiming? |
| Baseline/comparator | Frozen baseline artifacts: `docs/reviews/risky-debt-derivation-gap-proposals-v2.md` and `docs/reviews/credit-card-npv-generic-document-derivation-tree-smoke-2026-07-08.md`. |
| Primary criterion | Reports include concrete source-local assumption branches, derivation routes, patch candidates or specific formalization blockers, and exact tool evidence. |
| Veto diagnostics | Card-specific logic; hand-wavy patch text; no proposed fix when branch supports one; proof overclaim; missing non-claims. |
| Explanatory diagnostics | Backend absence, branch budget exhaustion, hard document domain mismatch. |
| Not concluded | No whole-document proof, release readiness, or global correctness claim. |
| Artifact | Markdown/JSON smoke reports and Phase 04 result note. |

## Forbidden Claims Or Actions

- Do not tune the tool only to the credit-card NPV document.
- Do not treat report readability as mathematical certification.
- Do not use long backend searches without a separate experiment plan.

## Exact Next-Phase Handoff Conditions

Close the master-program slice only if:

- regression tests pass;
- smoke reports demonstrate the richer contract;
- any remaining weakness is recorded as a blocker or next program.

## Stop Conditions

Stop if:

- smoke reports remain materially hand-wavy after Phase 01-03 artifacts exist;
- hard-document runs require unapproved long searches or installs;
- reviewer identifies a boundary violation that cannot be repaired locally.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write the Phase 04 result / close record.
3. Write or refresh a final handoff / next-lane plan.
4. Review final artifacts for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
