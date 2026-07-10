# Phase 04 Result: Report Integration And Regression Gate

Date: 2026-07-08

Status: `PASSED_WITH_RECORDED_PROPOSITION_LABEL_LIMITATION`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `6bbd8cc` plus dirty worktree; touched files are uncommitted. |
| Commands actually run | Frozen risky-debt `audit-document-derivation-tree`; frozen credit-card `audit-document-derivation-tree`; `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`; `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_tree_report.py`; JSON contract assertion script; `git diff --check ...`. |
| Environment | `Python 3.11.15`; backend env requested by workflow: `mathdevmcp-backends`. |
| Wall time | Frozen report commands about `9s` each; focused pytest `43.84s`. |
| Artifacts | `docs/reviews/risky-debt-document-derivation-tree-phase04-frozen-2026-07-08.md`; `.json`; `docs/reviews/credit-card-npv-document-derivation-tree-phase04-frozen-2026-07-08.md`; `.json`. |
| Pass/veto status | Passed; no proof-overclaim, card-specific logic, or missing non-claim veto.  Proposition label support remains a recorded limitation. |

## Frozen Regression Summary

| Case | Selected rows | Missing focus labels | Branches | Patch candidates | Formalization stubs | Blockers |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| Risky debt | 3 | `prop:interior-foc` | 8 | 8 | 24 | 52 |
| Credit-card NPV | 4 | none | 12 | 12 | 36 | 77 |

## Interpretation

The reports now include source-local full display spans, semantic obligations,
branch-linked sufficient assumptions, derivation routes under assumptions,
external-tool-first ledgers, proposed patch candidates, formalization stubs,
and non-claims.  This is materially stronger than the previous generic report
shape that mostly stopped at broad blockers and generic evidence collection.

The risky-debt frozen set exposed a real limitation: `prop:interior-foc` is a
proposition label, not a display-equation label.  The current workflow reports
it in `missing_focus_labels` and audits the display labels `eq:foc-k` and
`eq:foc-b`.  Proposition-span targeting should be the next generic enhancement.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Non-claims |
| --- | --- | --- | --- | --- | --- |
| Close this master-program slice | Passed: frozen reports include branches, patches, stubs, exact tool evidence, and non-claims. | No card-specific logic, hand-wavy-only patch output, or proof overclaim observed in checks. | Proposition labels outside display math remain unsupported; stubs are manual and non-certifying. | Build proposition/paragraph target extraction and executable formalization stubs in the next lane. | No whole-document proof, release readiness, or global correctness claim. |

## Checks

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_tree_derivation_lane_integration.py -q`: `13 passed in 43.84s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_tree_report.py`: passed.
- Frozen report JSON contract assertion: passed.
- `git diff --check` on touched code, tests, plans, and frozen reports: passed.

## Handoff

The current generic document workflow is meaningfully better for display
equation targets.  The next high-value generic improvement is proposition/span
targeting so labels like `prop:interior-foc` can produce a proposition-level
obligation packet rather than only reporting a missing focus label.
