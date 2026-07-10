# Phase 04 Subplan: Executable Backend Translators

Date: 2026-07-08

Status: `DRAFT_UNDER_REVIEW`

## Phase Objective

Replace placeholder stubs with executable backend attempts for encodable
subgoals and precise typed translation blockers for non-encodable subgoals.

## Entry Conditions Inherited From Previous Phase

- Typed obligations contain route hints and unresolved constructs.
- External-tool-first policy remains active.

## Required Artifacts

- Translation attempt records for SymPy, Sage, and Lean.
- Executable attempt for simple algebraic subgoals when encodable.
- Precise translation blockers for conditional expectation, derivative under
  expectation, macro translation, and missing domains.
- Tests with mocked or bounded backend calls.
- Phase result:
  `docs/plans/mathdevmcp-context-aware-executable-repair-phase-04-result-2026-07-08.md`

## Required Checks, Tests, Reviews

- `python3 -m pytest tests/test_document_derivation_tree.py tests/test_external_tool_adapters.py tests/test_derive_or_refute.py -q`
- `python3 -m py_compile src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/external_tool_adapters.py`
- `git diff --check`
- Optional real backend smoke only when already available and bounded.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can branches show actual executable attempts or exact typed translation blockers? |
| Baseline/comparator | Current non-executable formalization stubs. |
| Primary criterion | Encodable algebraic fixture executes; hard stochastic target names exact blockers and next translation step. |
| Veto diagnostics | Stub described as proof; backend absence treated as refutation; unbounded backend command; missing input/output artifact. |
| Explanatory diagnostics | Unsupported macro, conditional expectation, derivative/interchange, missing domain. |
| Not concluded | Backend attempt certifies only scoped encoded subgoals. |
| Artifact | Tests, backend evidence records, Phase 04 result. |

## Forbidden Claims Or Actions

- Do not run long proof search.
- Do not install backends.
- Do not treat LeanDojo/Pantograph/LeanSearch as final certification.

## Exact Next-Phase Handoff Conditions

Advance to Phase 05 only if executable/blocker outcomes are branch records
that the branch search can rank.

## Stop Conditions

Stop if backend calls cannot be bounded or captured as artifacts.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 04 result / close record.
3. Draft or refresh Phase 05 subplan.
4. Review Phase 05 for consistency, correctness, feasibility, artifact
   coverage, and boundary safety.
