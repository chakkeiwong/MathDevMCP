# Phase 3 Result: Counterexample Search

## Status

`PASSED_LOCAL_CHECKS_CLAUDE_REVIEW_UNAVAILABLE`

## Phase Objective

Implement bounded counterexample search for simple scalar identities and small
matrix/noncommutative failures.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can the workbench refute simple false claims with concrete reproducible examples? |
| Baseline/comparator | Existing SymPy mismatch behavior, router records, and workbench counterexample schema. |
| Primary criterion | Met locally. False scalar and matrix-commutativity claims return concrete assignments and unequal evaluated sides; no-hit remains `unknown`; unsafe syntax is `not_encodable`. |
| Veto diagnostics | Passed locally. Absence of counterexample is not proof; unsafe expressions are not executed; matrix example is fixed/reproducible. |
| Explanatory diagnostics | Search domain, assignments, lhs/rhs values, backend label. |
| Not concluded | Completeness of counterexample search or truth when no counterexample is found. |

## Artifacts

- `src/mathdevmcp/counterexample_search.py`
- `tests/test_counterexample_search.py`

## Commands Run

```bash
PYTHONPATH=src python -m pytest -q tests/test_counterexample_search.py tests/test_math_debugging_kernel.py tests/test_math_debugging_router.py
python3 -m py_compile src/mathdevmcp/counterexample_search.py
git diff --check
```

## Check Results

- Counterexample/kernel/router focused tests: `16 passed`.
- Python compile check: passed.
- `git diff --check`: passed.

## Claude Review

Phase 3 read-only review was attempted once with a verdict-only prompt. It
produced no substantive output before interruption and returned a generic
execution error after interrupt.

## Phase 4 Handoff

Proceed to Phase 4: Assumption Discovery.

Handoff conditions met:

- Counterexample records are stable enough to cite as blocking evidence.
- No-hit search results preserve `unknown`, not proof.
- Phase 4 subplan exists.

## Non-Claims

- Counterexample search is bounded and incomplete.
- Numeric or finite-domain no-hit evidence is not proof.
- The matrix counterexample only refutes the scoped commutativity claim.
