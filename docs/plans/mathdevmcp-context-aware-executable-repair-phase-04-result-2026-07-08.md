# Phase 04 Result: Executable Backend Translators

Date: 2026-07-09

Status: `PASSED`

## Objective

Replace branch-level formalization-only stubs with explicit backend evidence:
bounded executable attempts when the typed target is encodable, and precise
typed translation blockers when it is not.

## Implementation Summary

- Added branch-level backend evidence in
  `src/mathdevmcp/document_derivation_tree.py`.
- Each assumption branch now carries:
  - `backend_attempts`
  - `translation_attempts`
  - `translation_blockers`
  - `backend_evidence`
  - branch-local `blockers`
- Encodable algebraic targets expose scoped executable SymPy evidence on the
  branch.
- Stochastic FOC branches expose exact typed blockers for conditional
  expectation, conditional law, integrability, derivative-expectation
  interchange, macro translation, and missing typed assumptions.
- Markdown now renders branch backend attempts, translation attempts, and
  translation blockers under each candidate branch.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can branches show actual executable attempts or exact typed translation blockers? |
| Baseline/comparator | Previous branch records had typed obligations and stubs, while executable attempts were root-only. |
| Primary criterion | Passed. Simple algebra has branch-visible scoped SymPy proof evidence; risky-debt FOC branches have branch-visible typed translation blockers. |
| Veto diagnostics | No veto triggered. Stubs are not described as proofs, backend absence is not a refutation, and branch evidence is no longer hidden at the root. |
| Not concluded | No whole-document proof, global minimality, or Lean/Sage certification is claimed for the risky-debt FOC targets. |

## Frozen Smoke Artifacts

- Risky debt Markdown:
  `docs/reviews/risky-debt-executable-backends-phase04-smoke-2026-07-09.md`
- Risky debt JSON:
  `docs/reviews/risky-debt-executable-backends-phase04-smoke-2026-07-09.json`
- Simple algebra Markdown:
  `docs/reviews/simple-algebra-executable-backends-phase04-smoke-2026-07-09.md`
- Simple algebra JSON:
  `docs/reviews/simple-algebra-executable-backends-phase04-smoke-2026-07-09.json`

Smoke summary:

- Risky-debt first branch status:
  `blocked_before_backend_certification`.
- Risky-debt first branch attempt count: `1`, diagnostic only.
- Risky-debt first branch translation blocker kinds include:
  - `conditional_expectation_translation_required`
  - `conditional_law_translation_required`
  - `conditioning_scope_translation_required`
  - `integrability_translation_required`
  - `derivative_expectation_interchange_required`
  - `macro_translation_required`
  - `missing_domain_or_assumption_required`
- Simple algebra branch status:
  `scoped_target_proved_not_document_proof`.
- Simple algebra SymPy translation status:
  `executed`.
- Simple algebra branch promotion guard:
  `can_promote=True`.

## Checks

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_external_tool_adapters.py tests/test_derive_or_refute.py -q`
  - Passed: `31 passed in 107.62s`.
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/external_tool_adapters.py`
  - Passed.
- Frozen smoke commands:
  - `python3 -m mathdevmcp.cli audit-document-derivation-tree docs/risky-debt-maliar-deep-learning-lecture-note.tex --focus-label prop:interior-foc --focus-label eq:foc-k --focus-label eq:foc-b --max-attempts 1 --output-md docs/reviews/risky-debt-executable-backends-phase04-smoke-2026-07-09.md --output-json docs/reviews/risky-debt-executable-backends-phase04-smoke-2026-07-09.json`
  - `python3 -m mathdevmcp.cli audit-document-derivation-tree /tmp/simple_phase04.tex --focus-label eq:simple --max-attempts 2 --output-md docs/reviews/simple-algebra-executable-backends-phase04-smoke-2026-07-09.md --output-json docs/reviews/simple-algebra-executable-backends-phase04-smoke-2026-07-09.json`
  - Both completed and wrote artifacts.
- JSON smoke assertion:
  - Passed: risky-debt branch has exact typed blockers and no promotion; simple algebra branch has scoped SymPy proof promotion.
- `git diff --check`
  - Passed.

## Review

Claude review remains unavailable under the Phase 00 external-service rejection
boundary. Codex performed the Phase 04 skeptical review locally:

- Branch-level evidence visibility: no remaining issue for the focused tests.
- Proof overclaim: no remaining issue; simple algebra is explicitly
  `scoped_target_proved_not_document_proof`, and risky-debt remains blocked.
- Backend/blocker specificity: no remaining issue for the frozen FOC targets.
- Artifact coverage: no remaining issue; tests and frozen smoke artifacts cover
  both executable and blocked paths.

Remaining risk:

- The risky-debt backend attempt itself still comes from the root controller and
  is diagnostic because the target is not yet translated into a backend-native
  expression. Phase 05 should rank branches using blocker specificity and
  scoped backend evidence, not by raw branch count.

## Phase 05 Handoff

Phase 05 may start.

Entry evidence available:

- Branches carry backend attempts and typed translation blockers directly.
- Promotion guards are branch-visible.
- Encodable and blocked examples both have frozen smoke artifacts.

Phase 05 should add deterministic ranking fields over branch outcomes without
claiming MCTS, global optimality, or minimality.
