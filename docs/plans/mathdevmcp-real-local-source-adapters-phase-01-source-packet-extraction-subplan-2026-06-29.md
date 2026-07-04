# Phase 01 Subplan: Source Packet Extraction

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Implement a local-only source packet schema and extractor that reads the pilot
manifest line ranges and produces bounded, line-linked packets for each source
obligation.

## Entry Conditions Inherited From Previous Phase

Phase 00 has confirmed the five-case pilot baseline, source path existence,
line anchors, and local/non-gating boundary.

## Required Artifacts

- `src/mathdevmcp/real_local_source_adapters.py` with packet extraction and
  validation primitives.
- `tests/test_real_local_source_adapters.py` focused packet tests.
- Source packet records with case id, source role, relative path, line start,
  line end, excerpt, line count, and content hash.
- Phase 01 result record.
- Refreshed Phase 02 subplan.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_source_adapters.py`
- `python3 -m pytest tests/test_real_local_high_level_pilot.py`
- Source-packet extraction smoke via Python one-liner.
- Claude review only if packet schema or boundary rules materially change.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP produce bounded source packets for all five local obligations with path, line, role, and excerpt provenance? |
| Baseline/comparator | Pilot manifest source snapshots and line ranges. |
| Primary pass criterion | Every manifest source range yields a validated bounded packet with content hash; invalid absolute/missing/range-bad/oversized inputs fail; packets do not claim proof. |
| Veto diagnostics | Whole source document copied; absolute source path accepted; missing range accepted; packet exceeds manifest range plus allowed context; packet status treated as mathematical support; packet hash drifts after capture. |
| Explanatory diagnostics | Packet count, source-line spans, excerpt hashes/counts, validation findings. |
| Not concluded | Mathematical validity, adapter support, public redistributability. |
| Artifact | Packet API/tests and Phase 01 result. |

## Forbidden Claims / Actions

- Do not claim source packet extraction proves or refutes any obligation.
- Do not copy whole source files into repo artifacts.
- Do not accept absolute source paths from the manifest.
- Do not add packet results to benchmark gates.
- Do not exceed the manifest line range except at most two context lines when a
  later reviewed adapter explicitly needs that context.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 02 only when all manifest source ranges extract into bounded
packets, invalid packet inputs are rejected by tests, and packet outputs expose
provenance without source-proof claims.

## Stop Conditions

Stop if source extraction requires copying excessive source text, line anchors
are unstable, required context exceeds the packet cap, or the packet schema
cannot preserve local-only provenance. After packet hashes are captured, stop
and write a blocked/partial result if any packet hash changes before final
handoff.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 01 result; draft or
refresh Phase 02; review Phase 02 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
