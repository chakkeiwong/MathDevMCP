# Phase 0 Subplan: Governance And Baseline Freeze

Date: 2026-07-01

Status: `REVISED_AFTER_CLAUDE_R1`

## Phase Objective

Freeze the current packet, manifest, and boundary state before designing the
agent-handoff calibration, so later improvements are measured against a known
baseline.

## Entry Conditions Inherited From Previous Phase

- The human-framed packet repair has passed local tests.
- The current packet artifact exists under `.mathdevmcp/`.
- The program remains local/non-gating and makes no release, product, public
  benchmark, scientific-validity, or broad theorem-proving claim.

## Required Artifacts

- Phase 0 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-00-governance-baseline-result-2026-07-01.md`.
- Baseline manifest summary from
  `benchmarks/real_tasks/holdout_local/real_local_high_level_workflow_benchmark_cases.json`.
- Git commit, dirty-worktree summary, and SHA256 hashes for the benchmark
  manifest, packet artifact, and final matrix.
- Packet generator command provenance and selected-case rationale.
- Packet artifact summary from
  `.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase08_packets.json`.
- Final-matrix artifact summary from
  `.mathdevmcp/real_local_high_level_workflow_benchmark_closure_phase08_final_matrix.json`.
- Ledger entry in
  `docs/plans/mathdevmcp-agent-handoff-packet-calibration-visible-execution-ledger-2026-07-01.md`.

## Required Checks, Tests, And Reviews

- Run the manifest/packet focused tests:
  `python3 -m pytest tests/test_real_local_high_level_benchmark.py -q`.
- Verify packet report status is `consistent`, case count is 9, and packet
  findings are 0.
- Verify selected five case IDs are present.
- Record `git rev-parse HEAD`, targeted dirty status, and `sha256sum` for the
  frozen artifacts.
- Claude review of this subplan and Phase 1 subplan if available.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact packet and case state will the agent-handoff calibration use as baseline? |
| Baseline/comparator | Current generated packet artifact and final matrix after human-framing repair. |
| Primary criterion | Baseline artifacts exist, parse, report the expected nine-case packet set with no packet findings, and have recorded hashes/provenance before prompt/rubric work. |
| Veto diagnostics | Missing packet artifact; manifest inconsistency; selected case absent; packet artifact not regenerated after schema changes; missing hash/provenance; local/non-gating boundary missing. |
| Explanatory diagnostics | Case count, selected case IDs, packet summary, focused pytest. |
| Not concluded | Agent-handoff improvement, model reliability, release readiness, public benchmark validity, or scientific validation. |

## Forbidden Claims And Actions

- Do not score agent responses in Phase 0.
- Do not run downstream model subjects in Phase 0.
- Do not change packet schema or benchmark cases in Phase 0.
- Do not treat existing packet quality as calibrated agent-handoff evidence.
- Do not proceed if artifact hashes/provenance cannot be recorded.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only if:

- focused tests pass;
- packet artifact parses and contains all five selected case IDs;
- artifact hashes and selected-case rationale are recorded;
- Phase 0 result records baseline artifact paths and non-claims;
- Phase 1 subplan exists and has been locally reviewed for consistency.

## Stop Conditions

Stop if:

- packet artifacts are missing or inconsistent;
- selected cases are absent;
- focused tests fail for reasons unrelated to this calibration and cannot be
  fixed without changing the packet baseline;
- continuing would require changing the already calibrated packet contract.

## End-Of-Phase Protocol

Run the required checks, write the Phase 0 result, refresh/review the Phase 1
subplan, append the ledger, then advance or stop.
