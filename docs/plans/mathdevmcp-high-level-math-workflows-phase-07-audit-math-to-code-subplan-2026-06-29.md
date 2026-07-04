# Phase 7 Subplan: Audit Math To Code Workflow

## Phase Objective

Implement `audit_math_to_code(math, code)` for "Does this code implement this
equation?" questions.

## Entry Conditions Inherited From Previous Phase

- Contract, kernel, and debug/proof workflows exist.
- Low-level code/equation comparison is available.

## Required Artifacts

- `audit_math_to_code` function.
- Tests for structural match, structural mismatch, alias support, numeric-only
  diagnostic evidence, no semantic-proof promotion, and phase-local
  false-confidence traps.
- Phase 7 result record.
- Refreshed Phase 8 subplan.

## Required Checks, Tests, Reviews

- Workflow tests.
- Contract/kernel tests.
- Low-level equation/code tests if impacted.
- `python3 -m py_compile`.
- `git diff --check`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the workflow report code/equation alignment while preserving structural-only proof boundaries? |
| Baseline/comparator | Direct `code_implements_equation` and doc/code comparison outputs. |
| Primary pass criterion | Structural matches/mismatches are reported correctly and never promoted to mathematical proof; local negative controls catch structural-match-to-proof promotion. |
| Veto diagnostics | Structural match becomes `proved`; numeric tests become semantic correctness; missing terms hidden. |
| Explanatory diagnostics | Missing terms, matched terms, aliases, audit-only extras. |
| Not concluded | Full semantic implementation correctness. |
| Artifact | Function/tests/result. |

## Forbidden Claims And Actions

- Do not call structural match proof.
- Do not hide extra audit-only code terms.
- Do not expose CLI/MCP yet.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 8 if structural-only evidence is preserved and negative
controls pass.

## Stop Conditions

Stop if code/equation evidence cannot be distinguished from proof evidence.
