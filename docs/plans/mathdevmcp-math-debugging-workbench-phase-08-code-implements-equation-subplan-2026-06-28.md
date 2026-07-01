# Phase 8 Subplan: Code Implements Equation

## Phase Objective

Implement `code_implements_equation` to compare equation obligations against
Python code using AST operations, symbol aliases, required terms, and known
failure modes.

## Entry Conditions Inherited From Previous Phase

- Kernel evidence records exist.
- Gap/proof statuses are available for math-side obligations.

## Required Artifacts

- `src/mathdevmcp/equation_code_match.py`
- `tests/test_equation_code_match.py`
- CLI/MCP exposure.
- Phase 8 result record.
- Refreshed Phase 9 subplan.

## Required Checks, Tests, Reviews

- Tests for matched implementation, missing logdet/solve, extra regularizer,
  transpose mismatch, time-index mismatch.
- Existing implementation audit and AST operation tests.
- `git diff --check`.
- Claude review for code/math claim boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo answer whether code implements an equation at a bounded structural level? |
| Baseline/comparator | Existing `audit_implementation_label`, AST Kalman recursion, temporal contracts. |
| Primary pass criterion | Result separates matched, missing, extra, conflicting, and unchecked code/math elements. |
| Veto diagnostics | Name matching treated as semantic proof; unchecked code path marked implemented. |
| Explanatory diagnostics | AST operations, symbol matches, required/missing terms. |
| Not concluded | Full semantic equivalence of arbitrary code and math. |
| Artifact | Code/equation module/tests/result. |

## Forbidden Claims And Actions

- Do not claim implementation correctness from symbol presence alone.
- Do not execute arbitrary project code.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 9 if code/equation statuses can feed claim classification.

## Stop Conditions

Stop if structural evidence cannot be separated from proof/correctness.
