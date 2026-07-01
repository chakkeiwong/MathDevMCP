# Phase 5 Subplan: Regression And Agent-Usefulness Benchmark Hook

Date: 2026-07-01

Status: `READY_WITH_PHASE_4_DOCS_EXPOSURE`

## Phase Objective

Verify the standardized packet across local regression tests and align it with
the existing agent-handoff calibration artifacts, while defining future
downstream-agent usefulness measurement hooks without collecting new responses
unless separately approved.

## Entry Conditions Inherited From Previous Phase

- Phases 2-4 have implemented and exposed the local standard, or recorded a
  bounded implementation subset.
- Existing packet/report behavior remains testable.
- Prior calibration artifacts remain local/non-gating evidence.
- Claude review gates are waived for this execution window by explicit user
  direction; Codex-only regression/claim review and local checks remain
  required.

## Required Artifacts

- Phase 5 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-05-regression-agent-usefulness-benchmark-result-2026-07-01.md`.
- Regression command outputs or summarized manifests.
- Optional alignment note linking the new standard to prior calibration
  fixtures.
- Updated visible execution ledger.
- Claude read-only review is waived for this execution window by explicit user
  direction. Codex-only review of benchmark/claim wording is required if the
  result makes a standardization decision recommendation.

## Required Checks, Tests, Reviews

- Focused packet standard tests from Phases 2-4.
- Existing high-level workflow packet/report tests.
- If feasible in the local environment, broader high-level tests touched by
  implementation diffs.
- Local check that prior calibration tie/non-claim is still stated if referenced.
- No new downstream-agent response collection unless separately approved.

Required Phase 5 local checks:

- focused packet standard tests;
- durable packet report tests;
- adjacent high-level packet tests;
- packet report diagnostic confirming `status: consistent` and
  `packet_findings: 0`;
- text check that prior calibration B/C tie is preserved if referenced.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the operational standard preserve current packet behavior and provide a clean hook for future downstream-agent usefulness measurement? |
| Baseline/comparator | Existing local packet regression tests and prior calibration artifacts. |
| Primary criterion | Tests pass; artifacts state the standard's local scope; future benchmark hook is specified without retrofitting prior scores or collecting unapproved responses. |
| Veto diagnostics | Prior calibration tie misrepresented; benchmark hook treated as evidence; new model responses collected without approval; hard-veto discipline dropped; regression failures hidden by docs-only claims. |
| Explanatory diagnostics | Test matrix, packet field coverage, calibration-artifact alignment notes, Claude findings. |
| Not concluded | General downstream-agent improvement, public benchmark validity, release readiness, scientific validation. |

## Forbidden Claims Or Actions

- Do not run model/API response collection without explicit approval.
- Do not retrofit prior calibration scoring criteria.
- Do not claim the benchmark hook proves usefulness.
- Do not hide any hard-veto or regression failure behind aggregate summaries.

## Exact Next-Phase Handoff Conditions

Advance to Phase 6 only if:

- regression tests are run and recorded;
- any skipped or unavailable tests are justified;
- standardization decision evidence is separated from future benchmark design;
- final handoff subplan is refreshed against actual artifacts and limitations.

## Stop Conditions

Stop and write a blocker if:

- regression tests expose a boundary or compatibility failure;
- benchmark alignment would require changing prior calibration results;
- meaningful evaluation would require new model responses without approval;
- the evidence is insufficient to make even a bounded local-standard decision.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 5 result/close record;
3. draft or refresh the Phase 6 subplan;
4. review the Phase 6 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
