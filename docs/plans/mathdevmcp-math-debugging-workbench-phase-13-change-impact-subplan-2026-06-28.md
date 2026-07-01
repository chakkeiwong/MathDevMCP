# Phase 13 Subplan: Mathematical Change Impact

## Phase Objective

Implement `math_change_impact`, tracing downstream labels, references,
assumptions, proof packets, code links, generated tests, and claims affected by
a changed equation or assumption.

## Entry Conditions Inherited From Previous Phase

- Review packets exist.
- Dependency graph and label index are available.

## Required Artifacts

- `src/mathdevmcp/math_change_impact.py`
- `tests/test_math_change_impact.py`
- Phase 13 result record.
- Refreshed Phase 14 subplan.

## Required Checks, Tests, Reviews

- Tests for affected downstream proposition, implementation test, assumption
  manifest entry, and claim packet.
- Existing dependency graph tests.
- `git diff --check`.
- Claude review for impact overclaim.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo identify likely downstream artifacts affected by a math change? |
| Baseline/comparator | Existing dependency graph, latex index, proof packet links. |
| Primary pass criterion | Impact result lists affected artifacts with provenance and confidence level. |
| Veto diagnostics | Auto-editing downstream files; claiming complete impact coverage. |
| Explanatory diagnostics | Dependency paths and missing-link warnings. |
| Not concluded | Exhaustive impact analysis. |
| Artifact | Change impact module/tests/result. |

## Forbidden Claims And Actions

- Do not auto-edit downstream math/code.
- Do not claim no impact merely because graph links are absent.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 14 if impact links can include external theorem/local setting
assumption comparisons.

## Stop Conditions

Stop if impact confidence levels cannot prevent completeness overclaims.
