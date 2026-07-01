# Phase 01 Result: Source Packet Extraction

Date: 2026-06-29

Status: `PASSED`

## Objective

Implement a local-only source packet schema and extractor that reads the pilot
manifest line ranges and produces bounded, line-linked packets for each source
obligation.

## Skeptical Audit

- Wrong baseline: packets are extracted only from the Phase 00 frozen
  `high_level_pilot_cases.json` manifest.
- Proxy metrics: packet extraction does not clear `adapter_required` and does
  not prove or refute any source obligation.
- Stop conditions: absolute paths, bad ranges, missing files, oversized context,
  and packet hash drift remain blockers.
- Hidden assumptions: packet context is capped at two lines and defaults to the
  manifest line range only.
- Artifact fit: the output is a source-packet report with line spans, excerpts,
  hashes, and policy boundaries.

## Implemented Artifacts

- `src/mathdevmcp/real_local_source_adapters.py`
- `tests/test_real_local_source_adapters.py`

The packet report contract is `real_local_source_packet_report`.

Packet fields include:

- case id and title;
- source role and relative source path;
- manifest line range and extracted line range;
- context line counts;
- excerpt line count;
- excerpt content SHA-256;
- source-obligation question;
- packet policy boundaries.

## Checks

Focused packet tests:

```text
python3 -m pytest tests/test_real_local_source_adapters.py
```

Result: `5 passed`.

Pilot regression:

```text
python3 -m pytest tests/test_real_local_high_level_pilot.py
```

Result: `6 passed`.

Packet extraction smoke:

```text
python3 - <<'PY'
from mathdevmcp.real_local_source_adapters import extract_source_packets
r=extract_source_packets('.')
print(r['status'])
print(r['summary'])
print(r['metadata'])
print(r['packets'][0]['case_id'], r['packets'][0]['source_path'], r['packets'][0]['line_range'], r['packets'][0]['content_sha256'][:12])
PY
```

Result:

```text
consistent
{'case_total': 5, 'packet_total': 9, 'aggregate_accuracy': None}
{'schema_version': '1.0', 'contract': 'real_local_source_packet_report'}
RLHL-01-ift-gradient-bias-sign ../dsge_hmc/docs/gradient_accuracy_analysis.tex 536-589 1392ea2971a8
```

Negative tests cover:

- absolute source paths;
- invalid line ranges;
- oversized context;
- allowed small context.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. Every manifest source range yields a bounded packet; invalid absolute/range/oversized inputs fail; packets do not claim proof. |
| Veto diagnostics | No Phase 01 veto fired. No whole source file was copied, no absolute path was accepted, and packet status does not clear source obligations. |
| Explanatory diagnostics | 9 packet records were generated for 5 cases with content hashes and explicit policy boundaries. |
| Not concluded | Mathematical validity, adapter support, public redistributability, source proof, or release readiness. |

## Next Subplan Review

Phase 02 is ready. It must build normalized obligation IR records from these
packets, enforce source/probe/residual channel separation before adapter phases,
and avoid emitting any supported/refuted source-obligation status.
