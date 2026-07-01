# Phase 1 Subplan: Common Workbench Kernel

## Phase Objective

Create the shared schema layer for question-centered mathematical debugging:
`MathQuestion`, `WorkbenchObligation`, `AssumptionRecord`,
`BackendAttemptRecord`, `CounterexampleRecord`, and `WorkbenchResult`.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result exists and does not block implementation.
- Baseline proof-related tests have been recorded.
- The master program and visible runbook remain non-gating and non-release.

## Required Artifacts

- `src/mathdevmcp/math_debugging.py`
- `tests/test_math_debugging_kernel.py`
- CLI/MCP exposure is optional in Phase 1 and should be deferred unless needed
  for tests.
- `docs/plans/mathdevmcp-math-debugging-workbench-phase-01-common-kernel-result-2026-06-28.md`
- Refreshed Phase 2 subplan.

## Required Checks, Tests, Reviews

- `PYTHONPATH=src python -m pytest -q tests/test_math_debugging_kernel.py`
- `PYTHONPATH=src python -m pytest -q tests/test_contracts.py tests/test_schema_contracts.py`
- `git diff --check`
- Claude read-only review of the Phase 1 result and Phase 2 subplan if schemas
  are material or boundary-sensitive.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo represent high-level math-debugging questions and evidence without making proof claims? |
| Baseline/comparator | Existing contract style in `contracts.py`, proof obligation result shape, and proof packet evidence boundaries. |
| Primary pass criterion | New schema constructors return stable contract metadata, preserve assumptions/backend attempts/counterexamples, and classify statuses conservatively. |
| Veto diagnostics | Any schema field implying proof without backend evidence, missing certification boundary, or ambiguous status names. |
| Explanatory diagnostics | Unit tests over true, false, unknown, missing-assumption, and not-encodable records. |
| Not concluded | Any actual derivation/proof workflow implementation. |
| Artifact | Kernel module, tests, and Phase 1 result. |

## Forbidden Claims And Actions

- Do not implement broad proof search in Phase 1.
- Do not expose new user-facing tools until schemas are stable enough.
- Do not call diagnostic evidence a certificate.
- Do not change existing public MCP aliases or release gates.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if:

- kernel tests pass;
- schema names and statuses are documented in the Phase 1 result;
- Phase 2 router subplan exists and names exact backend routes and abstentions.

## Stop Conditions

Stop if:

- the common schema cannot express proof, refutation, missing assumptions,
  counterexamples, and abstention without ambiguity;
- tests reveal incompatibility with existing contract validation;
- implementation would require broad refactors of existing proof-audit modules.
