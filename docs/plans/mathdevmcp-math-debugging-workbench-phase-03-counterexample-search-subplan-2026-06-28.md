# Phase 3 Subplan: Counterexample Search

## Phase Objective

Implement bounded counterexample search for simple scalar identities and small
matrix/noncommutative failures, producing concrete assignments and evaluated
lhs/rhs evidence.

## Entry Conditions Inherited From Previous Phase

- Backend router exists.
- Workbench kernel can represent counterexamples.

## Required Artifacts

- `src/mathdevmcp/counterexample_search.py`
- `tests/test_counterexample_search.py`
- CLI/MCP exposure plan or minimal tool if stable.
- Phase 3 result record.
- Refreshed Phase 4 subplan.

## Required Checks, Tests, Reviews

- Counterexample tests for scalar false identities, no-counterexample-found
  abstention, and 2x2 matrix noncommutativity.
- Existing proof obligation tests.
- `git diff --check`.
- Claude review if search semantics or claims are material.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the workbench refute simple false claims with concrete reproducible examples? |
| Baseline/comparator | Existing SymPy numeric mismatch and numeric diagnostics. |
| Primary pass criterion | False seeded claims return concrete assignments and evaluated unequal sides; search failure remains inconclusive. |
| Veto diagnostics | Absence of counterexample claimed as proof; random probe without seed/artifact; unsafe expression evaluation. |
| Explanatory diagnostics | Search domain, seed, assignments, evaluated lhs/rhs. |
| Not concluded | Completeness of counterexample search. |
| Artifact | Counterexample module/tests/result. |

## Forbidden Claims And Actions

- Do not execute untrusted Python expressions.
- Do not call finite random search exhaustive unless domain is enumerated.
- Do not treat numeric equality over probes as proof.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 if counterexample records are stable enough for assumption
discovery to cite as blocking evidence.

## Stop Conditions

Stop if safe expression evaluation cannot be maintained or counterexample
records cannot preserve reproducible assignments.
