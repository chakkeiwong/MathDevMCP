# Phase 02 Result: Assumption Branch Closure

Date: 2026-07-08

Status: `PASSED`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `6bbd8cc` plus dirty worktree; touched files are uncommitted. |
| Commands actually run | `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_derivation_search_tree.py -q`; `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py`; `git diff --check -- src/mathdevmcp/document_derivation_tree.py tests/test_document_derivation_tree.py docs/plans/mathdevmcp-substantive-document-derivation-visible-ledger-2026-07-08.md`; explanatory CLI smoke on `eq:panel-npv-functional`. |
| Environment | `Python 3.11.15`; backend env requested by workflow: `mathdevmcp-backends`. |
| Wall time | Focused pytest: `47.79s`; CLI smoke: about `9s`. |
| Artifacts | `src/mathdevmcp/document_derivation_tree.py`; `tests/test_document_derivation_tree.py`; `docs/reviews/credit-card-npv-assumption-branches-phase02-smoke-2026-07-08.md`; `.json`. |
| Pass/veto status | Passed; no Phase 02 veto active. |

## What Changed

- Added candidate assumption branches derived from semantic packets.
- Each branch records:
  - assumptions;
  - obligations it closes;
  - mathematical why;
  - derivation route under assumptions;
  - external-tool-first ledger;
  - evidence references;
  - non-minimality/non-proof boundary.
- Tree roots now receive patch candidates generated from branch evidence.
- Markdown reports now show candidate assumption branches and proposed patch
  candidates.

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Non-claims |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 03 | Passed: tests assert branch closure links, routes, external-tool ledgers, and proposed patch text. | No missing branch ledger, missing route, or missing patch-location veto in focused tests. | Patch text is still diagnostic and not backend-certified; formalization stubs are not yet generated. | Add formalization stub records and backend-specific blockers. | Branches are sufficient candidates, not proofs or globally minimal assumptions. |

## Checks

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_derivation_tree_report.py tests/test_derivation_search_tree.py -q`: `19 passed in 47.79s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py`: passed.
- `git diff --check -- src/mathdevmcp/document_derivation_tree.py tests/test_document_derivation_tree.py docs/plans/mathdevmcp-substantive-document-derivation-visible-ledger-2026-07-08.md`: passed.

## Handoff

Phase 03 should attach backend-specific formalization stubs or precise
formalization blockers to each branch.  It must not promote stubs to proof.
