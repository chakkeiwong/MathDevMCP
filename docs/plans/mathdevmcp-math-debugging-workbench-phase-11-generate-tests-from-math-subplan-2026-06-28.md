# Phase 11 Subplan: Generate Tests From Math

## Phase Objective

Implement `generate_math_tests`, producing diagnostic pytest snippets or test
plans from equations, assumptions, code links, and expected failure modes.

## Entry Conditions Inherited From Previous Phase

- Assumption discovery, counterexample search, and code/equation matching exist.
- Notation records can supply aliases/conventions.

## Required Artifacts

- `src/mathdevmcp/math_to_tests.py`
- `tests/test_math_to_tests.py`
- Phase 11 result record.
- Refreshed Phase 12 subplan.

## Required Checks, Tests, Reviews

- Tests for generated symbolic identity check, numeric fixture, shape/property
  check, finite-difference check, and expected-failure diagnostic.
- Generated snippets must parse or be explicitly marked as plans only.
- `git diff --check`.
- Claude review for proof/test boundary language.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can math obligations be turned into executable diagnostics or test plans safely? |
| Baseline/comparator | Existing tests, numeric diagnostics, and code audit helpers. |
| Primary pass criterion | Generated artifacts state assumptions, target, expected failure mode, and diagnostic-only boundary. |
| Veto diagnostics | Generated test claimed as proof; unsafe code execution. |
| Explanatory diagnostics | Test snippet or plan metadata. |
| Not concluded | Correctness of implementation beyond tested cases. |
| Artifact | Test-generation module/tests/result. |

## Forbidden Claims And Actions

- Do not write generated tests into user code automatically.
- Do not execute generated tests against arbitrary code unless explicitly safe.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 12 if generated diagnostics can be included in review packets.

## Stop Conditions

Stop if generated snippets cannot preserve assumptions and diagnostic boundary.
