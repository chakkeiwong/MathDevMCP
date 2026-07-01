# Phase 03 Subplan: IFT Sign Adapter

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Implement a bounded IFT sign-consistency adapter for `RLHL-01` that checks the
source theorem/proof sign relation against the declared adjoint convention and
reports the first sign inconsistency candidate with source anchors.

## Entry Conditions Inherited From Previous Phase

Phase 02 has normalized five source obligations and routed `RLHL-01` to the IFT
sign adapter with source packets containing the theorem/proof block and summary
repeat.

## Required Artifacts

- IFT adapter function and evidence schema.
- Tests for expected sign inconsistency, source-anchor preservation, and a
  mutation where theorem/proof signs agree.
- Phase 03 result record.
- Refreshed Phase 04 subplan.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py`
- Focused Python smoke evaluating `RLHL-01`.
- Claude read-only review of the adapter result interpretation if the adapter
  reports an inconsistency.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the bounded source adapter find a theorem/proof sign inconsistency candidate in `RLHL-01` under the source adjoint convention? |
| Baseline/comparator | Pilot marked this source obligation `adapter_required`; executable sign-flip probe was diagnostic only. |
| Primary pass criterion | Adapter returns `inconsistency_candidate` with theorem sign, proof sign, adjoint convention evidence, source anchors, and non-claims. |
| Veto diagnostics | Claiming the whole DSGE note is false; using probe result as source proof; missing source anchors; no mutation test. |
| Explanatory diagnostics | Extracted sign tokens and source roles. |
| Not concluded | HMC practical invalidity, solver correctness, global theorem falsehood. |
| Artifact | Adapter result, tests, and Phase 03 record. |

## Forbidden Claims / Actions

- Do not claim the entire source note is false.
- Do not claim HMC conclusions are invalid.
- Do not edit the source document.
- Do not treat this local sign adapter as general theorem proving.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 04 only when `RLHL-01` has source-linked adapter evidence and
the result remains scoped to a sign inconsistency candidate.

## Stop Conditions

Stop if the sign convention cannot be located, the extracted signs are
ambiguous, or review finds the adapter is overclaiming beyond local algebra.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 03 result; draft or
refresh Phase 04; review Phase 04 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
