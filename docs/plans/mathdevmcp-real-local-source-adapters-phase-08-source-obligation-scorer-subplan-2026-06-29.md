# Phase 08 Subplan: Source Obligation Scorer

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Integrate source-adapter results into a local report that keeps
source-obligation, executable-probe, and residual-gap ledgers separate and
reports adapter coverage without a blended accuracy metric.

## Entry Conditions Inherited From Previous Phase

Phases 03-07 have produced source-linked adapter results for all five selected
cases, with non-claims and source anchors preserved.

## Required Artifacts

- Source-adapter runner/report API.
- Tests for five source results, zero residual adapter-required gaps, no
  aggregate accuracy, and known-bad boundary violations.
- Phase 08 result record.
- Refreshed Phase 09 subplan.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py tests/test_real_local_high_level_pilot.py`
- Python smoke for full source-adapter report.
- Claude review of report interpretation if report status is `passed`.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the report show five bounded source-adapter results without blending them with executable-probe evidence? |
| Baseline/comparator | Pilot report with five `adapter_required` source obligations. |
| Primary pass criterion | Full report has five source-adapter results, zero residual adapter-required cases under this local schema, separate probe ledger imported or referenced, and `aggregate_accuracy: None`; every cleared case has source anchors, required-term coverage, adapter route, deterministic check evidence, and non-claims. |
| Veto diagnostics | Single accuracy score; source result inserted into benchmark gate; adapter result lacks anchors/checks; residual gap hidden; adapter-required cleared from probe/test/benchmark success instead of source-anchored local-schema check. |
| Explanatory diagnostics | Source status counts, adapter route ids, probe summary, residual-gap ledger. |
| Not concluded | Release readiness, public benchmark validity, scientific proof. |
| Artifact | Runner/report API/tests and Phase 08 record. |

## Forbidden Claims / Actions

- Do not emit blended aggregate accuracy.
- Do not make this report gating for release or CI.
- Do not hide residual adapter gaps if any remain.
- Do not interpret residual `adapter_required: 0` as mathematical correctness,
  scientific validity, or release readiness.
- Do not clear `adapter_required` from executable-probe success, absence of
  blockers, adapter confidence, `pytest`, high-level quality, or benchmark-gate
  outcomes.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 09 only when report ledgers remain separate, all five source
obligations have adapter results, and known-bad tests catch blended claims.

## Stop Conditions

Stop if any source result lacks anchors/checks, or report integration requires a
release-policy change. Stop if any frozen manifest/case/source/packet
provenance drifts before report finalization.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 08 result; draft or
refresh Phase 09; review Phase 09 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
