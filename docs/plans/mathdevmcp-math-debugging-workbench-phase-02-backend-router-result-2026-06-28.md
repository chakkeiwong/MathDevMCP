# Phase 2 Result: Backend Router

## Status

`PASSED_LOCAL_CHECKS_CLAUDE_REVIEW_UNAVAILABLE`

## Phase Objective

Implement a conservative backend router that maps workbench obligations to safe
backend attempts or abstentions with explicit reasons.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can obligations be routed to safe backend attempts or abstentions with clear reasons? |
| Baseline/comparator | Existing `check_proof_obligation`, symbolic backend, Lean check, and backend availability boundaries. |
| Primary criterion | Met locally. Scalar algebra routes to SymPy; unsafe syntax abstains; matrix-like syntax routes to human review; Sage unavailable remains diagnostic; Lean requires explicit source. |
| Veto diagnostics | Passed locally. Unavailable Sage is not a refutation; unsafe syntax is not false; matrix-like expressions are not scalar-routed as proofs. |
| Explanatory diagnostics | Router tests and existing proof/symbolic tests. |
| Not concluded | Backend completeness, theorem proving, or matrix-proof support. |

## Artifacts

- `src/mathdevmcp/math_debugging_router.py`
- `tests/test_math_debugging_router.py`

## Commands Run

```bash
PYTHONPATH=src python -m pytest -q tests/test_math_debugging_router.py
PYTHONPATH=src python -m pytest -q tests/test_proof_obligations.py tests/test_symbolic_backend.py
python3 -m py_compile src/mathdevmcp/math_debugging_router.py
git diff --check
```

## Check Results

- Initial router test run found a Sage availability edge:
  `find_spec("sage.all")` can raise `ModuleNotFoundError` when parent `sage`
  is absent.
- Patched availability checking to fail closed through `_module_available`.
- Final `tests/test_math_debugging_router.py`: `6 passed`.
- Existing proof/symbolic tests: `16 passed`.
- Python compile check: passed.
- `git diff --check`: passed.

## Router Semantics

- `auto`/`sympy`: delegates scalar-safe obligations to
  `check_proof_obligation`.
- `lean`: requires explicit Lean source and preserves Lean unavailable/timeout
  as diagnostic unless direct Lean verifies or rejects.
- `sage`: reports `backend_unavailable` when Sage modules are absent.
- `z3`: reports `not_encodable` for this bounded slice.
- Unsafe syntax: `not_encodable`.
- Matrix-like syntax: `human_review`/`unknown`, not scalar proof.

## Claude Review

Phase 2 read-only review was attempted once with a verdict-only prompt. It
produced no substantive output before interruption and returned a generic
execution error after interrupt.

Master-program review had already converged with `VERDICT: AGREE`; no local
material blocker was found.

## Phase 3 Handoff

Proceed to Phase 3: Counterexample Search.

Handoff conditions met:

- Router tests pass.
- Counterexample phase has clear allowed domains from the Phase 3 subplan:
  scalar false identities and small explicit matrix/noncommutative examples.
- The router preserves proof/refutation/diagnostic boundaries for Phase 3 to
  consume.

## Non-Claims

- Router output is not proof unless nested deterministic backend evidence is
  certifying for the scoped obligation.
- Human-review routing is not a failure.
- Backend unavailable is not a mathematical refutation.
