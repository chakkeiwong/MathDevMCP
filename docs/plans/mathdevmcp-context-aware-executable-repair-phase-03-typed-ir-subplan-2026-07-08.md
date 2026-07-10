# Phase 03 Subplan: Typed Repair Obligation IR

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Convert context packets and context graph records into typed repair
obligations before backend calls or repair text generation.

## Entry Conditions Inherited From Previous Phase

- Context graph distinguishes stated/missing/unresolved assumptions with
  source references.
- Proposition and display targets preserve source spans and equation targets.

## Required Artifacts

- Typed repair obligation records containing target, assumptions, operators,
  variables, domains, unresolved constructs, route hints, and encodability.
- Integration with existing `math_ir.py` diagnostics rather than a duplicate IR.
- Tests on conditional expectation plus derivative/FOC targets.
- Phase result:
  `docs/plans/mathdevmcp-context-aware-executable-repair-phase-03-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_math_ir.py tests/test_document_derivation_tree.py -q`
- `python3 -m py_compile src/mathdevmcp/math_ir.py src/mathdevmcp/document_derivation_tree.py`
- `git diff --check`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can each branch be generated from a typed obligation rather than raw LaTeX templates? |
| Baseline/comparator | Current branch records derive from semantic packet templates and stub blockers. |
| Primary criterion | Branches cite typed obligation ids with unresolved constructs and backend route hints. |
| Veto diagnostics | Branch without typed obligation; missing unresolved construct; unsupported operator hidden. |
| Explanatory diagnostics | Ambiguous shape, stochastic operator, derivative under expectation. |
| Not concluded | Typed IR is diagnostic until backend-certified. |
| Artifact | Tests and Phase 03 result. |

## Forbidden Claims Or Actions

- Do not treat typed IR as proof.
- Do not drop source provenance when translating to IR.

## Exact Next-Phase Handoff Conditions

Advance to Phase 04 only if typed obligations specify which backend routes are
candidate, blocked, or require manual translation.

## Stop Conditions

Stop if typed IR cannot represent the frozen FOC targets without hiding
expectation/derivative blockers.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 03 result / close record.
3. Draft or refresh Phase 04 subplan.
4. Review Phase 04 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
