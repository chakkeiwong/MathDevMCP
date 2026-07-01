# Phase 00 Subplan: Governance And Source Freeze

Date: 2026-06-29

Status: `DRAFT`

## Phase Objective

Freeze the source-adapter baseline, source paths, line anchors, evidence
contract, stop conditions, and execution governance for the five local source
obligations.

## Entry Conditions Inherited From Previous Phase

This is the entry phase. It inherits the completed real-local high-level pilot
handoff where five executable probes pass and five source obligations remain
`adapter_required`.

## Required Artifacts

- Current baseline command outputs.
- Source path existence and line-anchor audit.
- Pilot manifest content hash and selected case-id list.
- Local repo/sibling repo commit/dirty provenance where available.
- Drift guard record naming the exact fields that must remain stable during the
  run: manifest hash, selected case ids, source line anchors, packet content
  hashes after Phase 01, and repo commit/dirty provenance.
- Initial execution ledger entry.
- Phase 00 result record.
- Refreshed Phase 01 subplan if needed.

## Required Checks / Tests / Reviews

- `python3 -m pytest tests/test_real_local_high_level_pilot.py`
- `python3 -m mathdevmcp.cli real-local-high-level-pilot --root "$PWD"`
- `rg -n "adapter_required|aggregate_accuracy|source_obligation_ledger" docs/plans/mathdevmcp-real-local-high-level-pilot-phase-05-final-regression-handoff-result-2026-06-29.md benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json`
- Local `test -f` checks for each referenced source file.
- Local hash command for the pilot manifest.
- Pre-launch blocking checklist from the visible runbook.
- Claude read-only review of the master program and Phase 00/01 boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the source-adapter program starting from the correct pilot baseline and valid local source anchors? |
| Baseline/comparator | Completed five-case pilot: five probes pass, five source obligations remain adapter-required. |
| Primary pass criterion | Baseline commands pass, source files exist, line anchors remain available, manifest hash and five selected case ids are recorded, and no source/probe/adapter channel is blended. |
| Veto diagnostics | Missing source file; wrong baseline; local pilot treated as public/gating; adapter-required count hidden; Claude treated as authority; frozen provenance drifts before handoff. |
| Explanatory diagnostics | Git status, path audit, pilot report, source manifest grep. |
| Not concluded | Adapter readiness, source proof, public benchmark validity, release readiness. |
| Artifact | Phase 00 result record and execution ledger entry. |

## Forbidden Claims / Actions

- Do not claim any source obligation is solved in this phase.
- Do not change code except plan/result docs if a governance fix is needed.
- Do not modify sibling repositories.
- Do not copy full source documents.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 01 only when the baseline remains the five-case pilot with
five adapter-required source obligations, all source paths exist, and the source
packet extraction scope is still local/non-gating and bounded to manifest line
ranges.

## Stop Conditions

Stop if any source file is missing, the manifest no longer validates, source
scope cannot remain local-only, or Claude/Codex review finds a material
unresolved sequencing or boundary issue. After Phase 00 capture, stop and write
a blocked/partial result if manifest hash, selected case ids, source line
anchors, packet content hashes, or repo commit/dirty provenance drift before
final handoff.

## Phase-End Protocol

At phase end: run required local checks; write the Phase 00 result; draft or
refresh Phase 01; review Phase 01 for consistency, correctness, feasibility,
artifact coverage, and boundary safety.
