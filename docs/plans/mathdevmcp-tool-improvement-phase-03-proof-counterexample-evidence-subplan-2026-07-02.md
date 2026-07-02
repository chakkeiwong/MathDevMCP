# Phase 3 Subplan: Proof And Counterexample Evidence

Date: 2026-07-02

Status: `DRAFT_NEXT`

## Phase Objective

Strengthen `prove_or_counterexample` so proof and refutation statuses are tied
to concrete backend evidence, counterexample artifacts, or explicit proof
obligations.

## Entry Conditions

- Phase 2 assumption taxonomy is available.
- Existing proof/counterexample tests pass.
- Optional backend availability is treated diagnostically.
- Proof/refutation workflows may display assumption records with scoped
  route-category metadata, but those categories are oracle-scoped diagnostics,
  not semantic sufficiency or minimality claims.

## Required Artifacts

- Updated `src/mathdevmcp/prove_or_counterexample.py`,
  `src/mathdevmcp/prove_or_refute.py`, `src/mathdevmcp/symbolic_backend.py`,
  and/or `src/mathdevmcp/counterexample_search.py`.
- Focused tests in `tests/test_prove_or_counterexample.py`.
- Phase 3 result record.
- Refreshed Phase 4 subplan.

## Required Checks/Tests/Reviews

- `python3 -m pytest tests/test_prove_or_counterexample.py tests/test_derive_from.py`
- `python3 -m pytest tests/test_high_level_contracts.py tests/test_high_level_workflows.py`
- Backend-availability checks only through existing optional diagnostics; no
  package install.
- `git diff --check` over touched files.
- Claude read-only review for proof/refutation boundary changes.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can proof/refutation outputs expose concrete evidence without overclaiming? |
| Baseline/comparator | Existing `prove_or_counterexample` results, Phase 2 scoped assumption taxonomy, and benchmark cases RLHLB-01/RLHLB-03. |
| Primary criterion | Proof requires scoped certificate/equivalent obligation; refutation requires either concrete counterexample or contract-valid scoped contradiction; unavailable backends remain diagnostic. |
| Veto diagnostics | Finite probe promoted to theorem; missing counterexample object for backend-counterexample refutation; scoped contradiction lacking contract-valid contradiction evidence; Lean/SymPy/Sage failure treated as false claim; proof without certificate. |
| Explanatory diagnostics | Backend route attempts and proof obligation records. |
| Not concluded | No broad theorem-proving ability or proof correctness beyond scoped certified obligations. |

## Forbidden Claims/Actions

- Do not treat backend unavailability as refutation.
- Do not claim proof unless evidence source supports the exact scope.
- Do not treat route-category assumptions as proof of sufficiency or global
  minimality.
- Do not require network or package installation.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 4 only if `derive_from` can reuse the proof/refutation
evidence surface without duplicating proof policy, including the distinction
between backend counterexamples and scoped contradictions.

## Stop Conditions

Stop if backend outputs are ambiguous, if backend-counterexample refutations
lack concrete counterexample artifacts, if scoped contradictions lack
contract-valid contradiction evidence, or if optional backend setup is required.
