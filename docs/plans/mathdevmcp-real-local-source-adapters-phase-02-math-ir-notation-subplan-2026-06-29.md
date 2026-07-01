# Phase 02 Subplan: Math IR And Notation Normalization

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Convert validated source packets into normalized obligation records containing
case id, question, source anchors, detected domain family, required terms,
assumptions, adapter route hints, and explicit source/probe/residual channel
separation.

## Entry Conditions Inherited From Previous Phase

Phase 01 has produced validated bounded source packets for all manifest source
ranges and has preserved the no-proof packet boundary.

## Required Artifacts

- Normalized obligation builder in `src/mathdevmcp/real_local_source_adapters.py`.
- IR schema/examples for all five obligations.
- Tests for all five obligation records, channel-separation invariants, and
  mutation/negative cases.
- Phase 02 result record.
- Refreshed Phase 03 subplan.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py`
- Python smoke that prints five obligation ids and adapter route ids.
- Claude review if routing/default assumptions change materially.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can source packets be normalized into adapter-routable obligation records without asserting the result? |
| Baseline/comparator | Packet records from Phase 01 and manifest `source_obligation` fields. |
| Primary pass criterion | Five obligations are produced with expected route ids, required terms, source anchors, assumptions, forbidden claims, explicit adapter-clearance requirements, and separate source/probe/residual channel fields before adapter execution. |
| Veto diagnostics | IR emits supported/refuted status; route chosen without source evidence; missing assumptions hidden; source/probe/residual channels blended; adapter phases can write results into probe fields; adapter-required clearance can be inferred from probe/test/benchmark success. |
| Explanatory diagnostics | Route ids, term coverage, assumption coverage, non-claim fields. |
| Not concluded | Adapter success, theorem proof, source correctness. |
| Artifact | Normalized obligation API/tests and Phase 02 result. |

## Forbidden Claims / Actions

- Do not report mathematical pass/fail from IR normalization alone.
- Do not remove source anchors.
- Do not infer broad domain validity from detected route ids.
- Do not allow adapter outputs to overwrite executable-probe fields.
- Do not allow `adapter_required` clearance unless the adapter result includes
  source anchors, required-term coverage, adapter route, deterministic check
  evidence, and non-claims.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 03 only when all five obligations have normalized records, the
IFT case routes to `ift_sign_consistency`, channel-separation negative tests
pass, explicit adapter-clearance requirements exist, and no IR record claims
proof or refutation.

## Stop Conditions

Stop if notation cannot be normalized enough to route the five cases, or if
normalization would require an unsupported scientific interpretation.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 02 result; draft or
refresh Phase 03; review Phase 03 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
