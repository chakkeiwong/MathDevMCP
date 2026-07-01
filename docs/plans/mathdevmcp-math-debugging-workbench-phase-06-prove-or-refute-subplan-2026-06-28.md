# Phase 6 Subplan: Prove Or Refute

## Phase Objective

Implement `prove_or_refute` for theorem/identity-like claims, routing to exact
normalization, SymPy, Lean when explicitly supplied, counterexample search, and
safe abstention.

## Entry Conditions Inherited From Previous Phase

- `derive_or_refute` and backend router exist.
- Counterexample search is available.

## Required Artifacts

- `src/mathdevmcp/prove_or_refute.py`
- `tests/test_prove_or_refute.py`
- CLI/MCP exposure.
- Phase 6 result record.
- Refreshed Phase 7 subplan.

## Required Checks, Tests, Reviews

- Tests for proved identity, refuted identity, Lean unavailable/inconclusive,
  unsafe expression not encodable.
- Existing Lean check and proof obligation tests.
- `git diff --check`.
- Claude review for proof claim language.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the repo answer "can we prove X?" with proof/refutation/unknown boundaries? |
| Baseline/comparator | Existing `check_proof_obligation`, `lean_check`, and counterexample search. |
| Primary pass criterion | Tool returns `proved`, `refuted`, `unknown`, `not_encodable`, or `backend_unavailable` with evidence. |
| Veto diagnostics | Lean timeout as refutation; numeric as proof; unsupported syntax as false. |
| Explanatory diagnostics | Backend attempts, counterexample if found, assumptions. |
| Not concluded | Complete theorem proving. |
| Artifact | Workflow module/tests/result. |

## Forbidden Claims And Actions

- Do not allow Lean `sorry` as proof.
- Do not fetch Lean dependencies.
- Do not call diagnostic evidence a certificate.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 7 if proof/refutation statuses can be consumed per derivation
step.

## Stop Conditions

Stop if statuses cannot clearly separate proof, refutation, unknown, and backend
unavailable.
