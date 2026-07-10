# Phase 01 Result: Proposition And Context Packet Extraction

Date: 2026-07-08

Status: `PASSED`

## Run Manifest

| Field | Value |
| --- | --- |
| Git commit | `6bbd8cc` plus dirty worktree; touched files are uncommitted. |
| Commands actually run | `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_document_derivation_tree.py -q`; `python3 -m py_compile src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/document_derivation_tree.py`; `git diff --check -- src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/document_derivation_tree.py tests/test_derivation_target_extraction.py tests/test_document_derivation_tree.py docs/plans/mathdevmcp-context-aware-executable-repair-visible-ledger-2026-07-08.md`; bounded CLI smoke on `prop:interior-foc`, `eq:foc-k`, `eq:foc-b`. |
| Environment | `Python 3.11.15`; backend env requested by workflow: `mathdevmcp-backends`. |
| Wall time | Focused pytest: `55.11s`; CLI smoke: about `9s`. |
| Artifacts | `src/mathdevmcp/derivation_target_extraction.py`; `src/mathdevmcp/document_derivation_tree.py`; `tests/test_derivation_target_extraction.py`; `tests/test_document_derivation_tree.py`; `docs/reviews/risky-debt-context-packet-phase01-smoke-2026-07-08.md`; `.json`. |
| Pass/veto status | Passed; proposition label no longer remains only a missing focus label. |

## What Changed

- Added `build_proposition_context_packet` to
  `src/mathdevmcp/derivation_target_extraction.py`.
- Proposition context packets include source span, proposition source text,
  hypotheses, referenced labels, equation targets, uncertainty, evidence
  references, and a non-proof boundary.
- `audit_document_derivation_tree` now builds proposition/context packets for
  focus labels that are not display-equation rows.
- The markdown report now includes a `Proposition/Context Packets` section.

## Smoke Result

For `docs/risky-debt-maliar-deep-learning-lecture-note.tex` with focus labels
`prop:interior-foc`, `eq:foc-k`, and `eq:foc-b`:

- `missing_focus_labels`: `[]`
- `context_target_labels`: `['prop:interior-foc']`
- proposition packet equation targets: `['eq:foc-k', 'eq:foc-b']`

## Decision Table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | Non-claims |
| --- | --- | --- | --- | --- | --- |
| Advance to Phase 02 | Passed: `prop:interior-foc` yields a context packet with proposition source and equation targets. | No missing-proposition-label or detached-row veto in focused tests. | Proof text after the proposition is not yet robustly attached as a separate proof block. | Build local context graph to distinguish stated, inferred, missing, and unresolved assumptions. | Context packets are not proofs and not repairs. |

## Checks

- `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_document_derivation_tree.py -q`: `11 passed in 55.11s`.
- `python3 -m py_compile src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/document_derivation_tree.py`: passed.
- `git diff --check` on touched Phase 01 files and ledger: passed.

## Handoff To Phase 02

Phase 02 should build a context graph over proposition packets and equation
targets.  It should classify assumptions as stated, nearby-stated,
inferred-candidate, missing, or unresolved using source evidence.
