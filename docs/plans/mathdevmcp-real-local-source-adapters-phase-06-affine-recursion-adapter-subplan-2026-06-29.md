# Phase 06 Subplan: Affine Recursion Adapter

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Implement a bounded affine-pricing recursion adapter for `RLHL-07` that checks
exponential-affine ansatz substitution, Gaussian MGF use, and coefficient
collection for `A_n` and `B_n` with vector/matrix caveats.

## Entry Conditions Inherited From Previous Phase

Phase 05 has completed the Joseph adapter; Phase 02 normalized `RLHL-07` with
affine recursion route hints and source packets from the master recursion.

## Required Artifacts

- Affine recursion adapter function.
- Tests for positive source support, missing Gaussian MGF, missing coefficient
  equations, and source-anchor preservation.
- Phase 06 result record.
- Refreshed Phase 07 subplan.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py`
- Focused Python smoke evaluating `RLHL-07`.
- Claude read-only review of adapter interpretation if recursion support is
  reported.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the source packets support the affine recursion via ansatz substitution, Gaussian MGF, and coefficient collection? |
| Baseline/comparator | Pilot `RLHL-07` adapter gap and inconclusive affine collection probe. |
| Primary pass criterion | Adapter returns `source_supported` with ansatz, Gaussian conditional normality/MGF, `A_n`, `B_n`, and initial-condition evidence. |
| Veto diagnostics | Claiming empirical pricing validity; claiming non-affine approximations are exact; missing MGF or coefficient collection evidence. |
| Explanatory diagnostics | Required-term coverage and coefficient names. |
| Not concluded | Empirical validity, identification, later approximation correctness. |
| Artifact | Adapter result, tests, and Phase 06 record. |

## Forbidden Claims / Actions

- Do not claim empirical pricing validity.
- Do not claim non-affine approximations are exact.
- Do not promote an inconclusive executable probe into failure of the source
  derivation.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 07 only when `RLHL-07` has source-linked derivation support
with MGF/coefficient evidence and non-claims.

## Stop Conditions

Stop if the Gaussian MGF or coefficient equations cannot be localized.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 06 result; draft or
refresh Phase 07; review Phase 07 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
