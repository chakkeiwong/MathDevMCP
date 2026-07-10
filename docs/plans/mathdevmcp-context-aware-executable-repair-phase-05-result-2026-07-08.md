# Phase 05 Result: Budgeted Repair Branch Search

Date: 2026-07-09

Status: `PASSED`

## Objective

Rank repair branches by recorded evidence instead of listing assumption
templates without an ordering or blocker-specific next step.

## Implementation Summary

- Added reusable branch-ranking helpers in
  `src/mathdevmcp/derivation_branch_controller.py`.
- Added the contract `repair_branch_ranking_result`.
- Added deterministic ranking fields:
  - backend certification status;
  - closure strength;
  - source support;
  - blocker specificity;
  - non-minimality penalty;
  - expansion-record count.
- Added branch expansion records for assumption addition, derivation splits,
  formalization/backend attempts, and blockers.
- Integrated branch ranking into document derivation tree output, compact JSON,
  coverage counters, tool-use ledger, and Markdown rendering.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the tool rank repair branches by evidence rather than listing templates? |
| Baseline/comparator | Previous branch list had no deterministic ranking or branch-level expansion explanation. |
| Primary criterion | Passed. Risky-debt FOC branches are ranked as blocked with specific next evidence; simple algebra is ranked as scoped proved from SymPy evidence. |
| Veto diagnostics | No veto triggered. Ranking is not based on raw branch count; unsupported branches are not promoted; exhausted or blocked actions remain visible. |
| Not concluded | The top-ranked branch is not claimed to be globally optimal, minimal, proved, or publication-ready. |

## Frozen Smoke Artifacts

- Risky debt Markdown:
  `docs/reviews/risky-debt-branch-ranking-phase05-smoke-2026-07-09.md`
- Risky debt JSON:
  `docs/reviews/risky-debt-branch-ranking-phase05-smoke-2026-07-09.json`
- Simple algebra Markdown:
  `docs/reviews/simple-algebra-branch-ranking-phase05-smoke-2026-07-09.md`
- Simple algebra JSON:
  `docs/reviews/simple-algebra-branch-ranking-phase05-smoke-2026-07-09.json`

Smoke summary:

- Risky-debt total ranked branches: `6`.
- Risky-debt `eq:foc-k` top branch:
  `branch_semantic_packet_eq_foc_k_0_kernel_integrability_condition`.
- Risky-debt `eq:foc-k` top outcome:
  `blocked_with_specific_next_evidence`.
- Risky-debt `eq:foc-b` top outcome:
  `blocked_with_specific_next_evidence`.
- Simple algebra total ranked branches: `1`.
- Simple algebra top outcome:
  `scoped_proved`.

## Checks

- `python3 -m pytest tests/test_derivation_branch_controller.py tests/test_derivation_search_tree.py tests/test_document_derivation_tree.py -q`
  - Passed: `32 passed in 101.68s`.
- `python3 -m py_compile src/mathdevmcp/derivation_branch_controller.py src/mathdevmcp/document_derivation_tree.py`
  - Passed.
- Frozen smoke commands:
  - `python3 -m mathdevmcp.cli audit-document-derivation-tree docs/risky-debt-maliar-deep-learning-lecture-note.tex --focus-label prop:interior-foc --focus-label eq:foc-k --focus-label eq:foc-b --max-attempts 1 --output-md docs/reviews/risky-debt-branch-ranking-phase05-smoke-2026-07-09.md --output-json docs/reviews/risky-debt-branch-ranking-phase05-smoke-2026-07-09.json`
  - `python3 -m mathdevmcp.cli audit-document-derivation-tree /tmp/simple_phase04.tex --focus-label eq:simple --max-attempts 2 --output-md docs/reviews/simple-algebra-branch-ranking-phase05-smoke-2026-07-09.md --output-json docs/reviews/simple-algebra-branch-ranking-phase05-smoke-2026-07-09.json`
  - Both completed and wrote artifacts.
- JSON smoke assertion:
  - Passed. The ranking schema exposes `rankings` and `top_branch_id`; it does
    not expose a `ranked_branches` field.
- `git diff --check`
  - Passed.

## Review

Claude review remains unavailable under the Phase 00 external-service rejection
boundary. Codex performed the Phase 05 skeptical review locally:

- Wrong baseline checked: compare against unranked branch lists, not against a
  complete MCTS/prover.
- Proxy metric checked: branch count is not the pass criterion; outcome,
  blocker specificity, promotion guard status, and expansion records are the
  relevant evidence.
- Stop conditions checked: no installation, network fetch, destructive action,
  detached execution, or proof-boundary weakening was required.
- Artifact coverage checked: tests and frozen smoke artifacts cover both
  blocked stochastic and scoped-proved algebraic paths.

Remaining risk:

- Ranking still orders existing deterministic branch evidence only. It does not
  expand a large search tree or prove that the best-ranked branch is globally
  sufficient.

## Phase 06 Handoff

Phase 06 may start.

Entry evidence available:

- Branches carry expansion records, backend attempts, translation blockers, and
  branch ranking.
- Document reports render branch ranking and branch-local evidence.
- Phase 06 should turn this into document-ready repair text and regression
  reports without hiding blockers or overclaiming proof.
