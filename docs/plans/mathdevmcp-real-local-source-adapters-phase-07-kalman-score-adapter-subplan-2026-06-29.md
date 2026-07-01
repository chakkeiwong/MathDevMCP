# Phase 07 Subplan: Kalman Score Adapter

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Implement a bounded Kalman solve-form score adapter for `RLHL-10` that checks
differentiation of logdet/quadratic terms, solve substitution `S_t w_t = v_t`,
and the same-scalar HMC gradient boundary.

## Entry Conditions Inherited From Previous Phase

Phase 06 has completed the affine adapter; Phase 02 normalized `RLHL-10` with
Kalman score route hints and source packets from BayesFilter.

## Required Artifacts

- Kalman score adapter function.
- Tests for source support, missing solve relation, missing same-scalar
  contract, and source-anchor preservation.
- Phase 07 result record.
- Refreshed Phase 08 subplan.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py`
- Focused Python smoke evaluating `RLHL-10`.
- Claude review if adapter wording risks claiming HMC/posterior validity.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the source packets support the solve-form Kalman score contribution and same-scalar validity boundary? |
| Baseline/comparator | Pilot `RLHL-10` adapter gap and assumptions-only executable probe. |
| Primary pass criterion | Adapter returns `source_supported` with derivative terms, solve relation, invertible/PD/domain assumptions, and same-scalar boundary recorded. |
| Veto diagnostics | Claiming HMC validity, posterior validity, Hessian readiness, or sampler convergence; missing same-scalar boundary; missing source anchors. |
| Explanatory diagnostics | Required-term coverage and assumption list. |
| Not concluded | HMC validity, posterior correctness, sampler convergence, Hessian readiness. |
| Artifact | Adapter result, tests, and Phase 07 record. |

## Forbidden Claims / Actions

- Do not claim HMC/posterior/sampler validity.
- Do not claim Hessian readiness.
- Do not validate production backend correctness.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 08 only when all five case adapters have source-linked results
and every result preserves forbidden-claim boundaries.

## Stop Conditions

Stop if solve-form equivalence or same-scalar boundary cannot be localized.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 07 result; draft or
refresh Phase 08; review Phase 08 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
