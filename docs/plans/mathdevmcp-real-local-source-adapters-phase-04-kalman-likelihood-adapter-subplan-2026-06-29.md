# Phase 04 Subplan: Kalman Likelihood Adapter

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Implement a bounded Kalman prediction-error likelihood adapter for `RLHL-04`
that checks chain-rule, Gaussian innovation, logdet/quadratic, positive
definiteness, and mask/dense-panel assumption coverage from source packets.

## Entry Conditions Inherited From Previous Phase

Phase 03 has completed the IFT adapter while preserving source/probe separation;
Phase 02 normalized `RLHL-04` with Kalman likelihood route hints.

## Required Artifacts

- Kalman likelihood adapter function.
- Tests for positive support, missing Gaussian/logdet/PD/mask terms, and source
  anchor preservation.
- Phase 04 result record.
- Refreshed Phase 05 subplan.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py`
- Focused Python smoke evaluating `RLHL-04`.
- Claude review if adapter wording implies exactness outside linear Gaussian
  assumptions.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the source packets provide bounded evidence for deriving the prediction-error log-likelihood under linear Gaussian and observed-component assumptions? |
| Baseline/comparator | Pilot `RLHL-04` adapter gap and assumption-only executable probe. |
| Primary pass criterion | Adapter returns `source_supported` with chain-rule, Gaussian, logdet/quadratic, positive-definite, and mask/dense assumptions explicitly recorded. |
| Veto diagnostics | Claiming nonlinear filters are exact; missing mask/no-observation boundary; missing source anchors; no negative term tests. |
| Explanatory diagnostics | Required-term coverage and assumption list. |
| Not concluded | Score/Hessian validity, nonlinear filter exactness, implementation correctness. |
| Artifact | Adapter result, tests, and Phase 04 record. |

## Forbidden Claims / Actions

- Do not claim nonlinear filters are exact.
- Do not validate score/Hessian or production code from this adapter.
- Do not treat local source support as public benchmark evidence.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 05 only when `RLHL-04` has source-linked positive derivation
support with explicit domain assumptions and caveats.

## Stop Conditions

Stop if linear Gaussian, positive-definite, or mask assumptions cannot be
localized in source packets.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 04 result; draft or
refresh Phase 05; review Phase 05 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
