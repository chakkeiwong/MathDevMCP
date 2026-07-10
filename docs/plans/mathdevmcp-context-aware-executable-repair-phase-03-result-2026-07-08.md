# Phase 03 Result: Typed Repair Obligation IR

Date: 2026-07-09

Status: `PASSED`

## Objective

Convert semantic packets and context graph records into typed repair
obligations before backend calls or repair text generation.

## Implementation Summary

- Added `typed_repair_obligation_from_packet` in `src/mathdevmcp/math_ir.py`.
- Reused existing `diagnose_typed_obligation`/`math_obligation` diagnostics
  instead of creating an unrelated IR.
- Attached typed repair obligations to proposition/context packets and semantic
  work packets in `src/mathdevmcp/document_derivation_tree.py`.
- Added branch fields:
  - `typed_obligation_ids`
  - `typed_unresolved_constructs`
  - `typed_backend_route_hints`
  - `typed_encodability`
- Added Markdown and coverage reporting for typed repair obligations.
- Added tests for direct typed repair obligation construction and document-tree
  branch citation.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can each branch be generated from a typed obligation rather than raw LaTeX templates? |
| Baseline/comparator | Previous branches cited semantic packets and stubs but not a typed obligation id. |
| Primary criterion | Passed. Branches for frozen FOC targets cite typed obligation ids, unresolved constructs, and backend route hints. |
| Veto diagnostics | No veto triggered. Typed records preserve expectation/conditional/interchange blockers, source context, and non-proof boundaries. |
| Not concluded | Typed IR is diagnostic only; no backend proof, full formalization, or document repair is certified. |

## Frozen Smoke Artifact

- Markdown: `docs/reviews/risky-debt-typed-ir-phase03-smoke-2026-07-09.md`
- JSON: `docs/reviews/risky-debt-typed-ir-phase03-smoke-2026-07-09.json`

Smoke summary:

- Typed repair obligations: `3`
- Typed statuses: `{'blocked_on_missing_typed_assumptions': 3}`
- `eq:foc-k` typed unresolved constructs include:
  - `expectation`
  - `conditional`
  - `conditional_law`
  - `integrability`
  - `derivative_expectation_interchange`
- `eq:foc-k` encodability:
  - `status`: `blocked_pending_typed_assumptions`
  - candidate backends/routes: `lean`, `human_review`, `manual_formalization`
- Branches for `eq:foc-k` and `eq:foc-b` cite their typed obligation ids.

## Checks

- `python3 -m pytest tests/test_math_ir.py tests/test_document_derivation_tree.py -q`
  - Passed: `18 passed in 79.06s`
- `python3 -m py_compile src/mathdevmcp/math_ir.py src/mathdevmcp/document_derivation_tree.py`
  - Passed.
- `git diff --check`
  - Passed.
- Targeted trailing-whitespace/final-newline check on touched Phase 03 files
  and smoke Markdown:
  - Passed.

## Review

Claude review was not retried because Phase 00 recorded external-service review
rejection in this environment.  No fresh subagent review was available earlier
because the local agent thread limit was reached.

Codex performed the Phase 03 skeptical review locally:

- Branch without typed obligation: no remaining issue in the frozen FOC tests.
- Unsupported operator hiding: no remaining issue; expectation, conditional law,
  integrability, and derivative-expectation interchange remain explicit.
- Proof overclaim: no remaining issue; typed repair obligations carry a
  non-proof, non-backend-encoding boundary.
- Source provenance: no remaining issue for frozen FOC targets; typed
  obligations preserve packet/source spans and context-derived assumption
  statuses.

Remaining risk:

- The typed symbol extraction is still heuristic and can include prose tokens
  from proposition-level raw text.  Phase 04 should use typed obligations as
  routing/blocking artifacts, not as final formal syntax.

## Phase 04 Handoff

Phase 04 may start.

Entry evidence available:

- Context graphs feed typed repair obligations.
- Branch records cite typed obligation ids.
- Typed obligations expose unresolved constructs and backend route hints.
- Frozen FOC targets are blocked before backend proof attempts until typed
  expectation/interchange assumptions are supplied.

Phase 04 should translate only obligations whose `encodability.status` and
route hints permit a backend attempt, and must record precise blockers for
stochastic or derivative-under-expectation obligations that still need manual
formalization.
