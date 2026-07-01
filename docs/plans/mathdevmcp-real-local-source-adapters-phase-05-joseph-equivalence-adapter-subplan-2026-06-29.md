# Phase 05 Subplan: Joseph Equivalence Adapter

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Implement a bounded Joseph covariance equivalence adapter for `RLHL-06` that
checks exact-arithmetic algebra under the standard Kalman gain relation while
preserving numerical-stability caveats.

## Entry Conditions Inherited From Previous Phase

Phase 04 has completed the Kalman likelihood adapter and preserved linear
Gaussian/mask assumption boundaries; Phase 02 normalized `RLHL-06` with Joseph
equivalence route hints.

## Required Artifacts

- Joseph equivalence adapter function.
- Tests for source-supported equivalence, missing gain relation, missing
  numerical caveat, and source-anchor preservation.
- Phase 05 result record.
- Refreshed Phase 06 subplan.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py`
- Focused Python smoke evaluating `RLHL-06`.
- Claude review if adapter wording risks claiming floating-point PSD for compact
  form.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the source packets support exact-arithmetic Joseph/compact covariance equivalence under the Kalman gain relation while preserving numerical caveats? |
| Baseline/comparator | Pilot `RLHL-06` adapter gap and scalar algebra probe. |
| Primary pass criterion | Adapter returns `source_supported` with Joseph form, compact form, Kalman gain/innovation relation, exact-arithmetic boundary, and numerical caveat. |
| Veto diagnostics | Claiming compact form preserves PSD under rounding; missing exact-arithmetic caveat; missing gain relation; scalar probe treated as matrix proof. |
| Explanatory diagnostics | Term/caveat coverage and optional symbolic scalar sanity check. |
| Not concluded | Production backend correctness, PSD under all floating-point operations. |
| Artifact | Adapter result, tests, and Phase 05 record. |

## Forbidden Claims / Actions

- Do not claim compact covariance update is PSD-safe under rounding.
- Do not validate a particular implementation backend.
- Do not use the scalar executable probe as the matrix proof.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 06 only when `RLHL-06` has source-linked exact-equivalence
support with numerical caveat preserved.

## Stop Conditions

Stop if the standard gain relation or numerical caveat is absent or ambiguous.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 05 result; draft or
refresh Phase 06; review Phase 06 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
