# Phase 5 Subplan: Derive Or Refute

## Phase Objective

Implement a high-level `derive_or_refute` workflow that accepts givens, target,
and optional assumptions, then returns a derivation chain, counterexample, or
missing-assumption/unknown result.

## Entry Conditions Inherited From Previous Phase

- Kernel, router, counterexample search, and assumption discovery exist.

## Required Artifacts

- `src/mathdevmcp/derive_or_refute.py`
- `tests/test_derive_or_refute.py`
- CLI/MCP exposure.
- Phase 5 result record.
- Refreshed Phase 6 subplan.

## Required Checks, Tests, Reviews

- Tests for direct equality, one-step algebraic simplification, false target,
  and missing-assumption result.
- CLI/MCP smoke tests if exposed.
- `git diff --check`.
- Claude review for user-facing claim boundary.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo answer "can I derive X from Y?" in a bounded, evidence-backed way? |
| Baseline/comparator | Existing `derive_step` and `check_proof_obligation`. |
| Primary pass criterion | Results include obligations, backend attempts, assumptions, and either verified chain/refutation/unknown. |
| Veto diagnostics | Prose-only derivation, unsupported transitive steps, missing assumptions hidden. |
| Explanatory diagnostics | Step list and backend evidence. |
| Not concluded | Complete derivability over arbitrary givens. |
| Artifact | Workflow module/tests/result. |

## Forbidden Claims And Actions

- Do not synthesize unchecked multi-step proofs.
- Do not use LLM reasoning as certifying evidence.
- Do not mark unknown as false.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 6 if derive/refute can be reused by prove/refute.

## Stop Conditions

Stop if the workflow cannot preserve per-step evidence boundaries.
