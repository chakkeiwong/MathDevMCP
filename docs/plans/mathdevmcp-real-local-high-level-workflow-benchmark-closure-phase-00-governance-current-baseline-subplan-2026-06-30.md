# Phase 0 Subplan: Governance And Current Baseline

Date: 2026-06-30

Status: `READY_FOR_EXECUTION`

## Phase Objective

Freeze the current high-level workflow, source-adapter, benchmark, and worktree
baseline before constructing any new real-local workflow benchmark.

## Entry Conditions Inherited From Previous Phase

- No previous phase in this program.
- Predecessor high-level workflow runbook exists and completed seeded tests.
- Source-adapter Phase 11 addendum exists and preserves frozen/repaired
  distinction.
- The worktree is dirty; unrelated user/prior-agent changes must be preserved.

## Required Artifacts

- Phase 0 result:
  `docs/plans/mathdevmcp-real-local-high-level-workflow-benchmark-closure-phase-00-governance-current-baseline-result-2026-06-30.md`.
- Updated ledger entry.
- Baseline command summaries for seeded workflow quality, source-adapter
  repaired/frozen reports, and current worktree state.
- Baseline freeze manifest containing:
  - exact baseline manifests and report artifacts;
  - exact commands to reproduce baseline checks;
  - scorer/runner/module versions or commit identifiers available locally;
  - adapter/backend availability state;
  - expected verdict snapshots for seeded quality and source-adapter repaired
    versus frozen reports;
  - dirty-worktree boundary and unrelated-change preservation note.
- Refreshed Phase 1 subplan review note.

## Required Checks, Tests, And Reviews

- `git status --short`.
- `python3 -m mathdevmcp.cli high-level-workflow-quality --root "$PWD"`.
- `python3 -m pytest tests/test_high_level_contracts.py tests/test_high_level_workflows.py tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py`.
- Recheck repaired and frozen source-adapter CLI reports if the manifests exist.
- Codex skeptical audit.
- Claude review only if the Phase 1 launch boundary is materially revised.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the exact current baseline before real-local benchmark closure begins? |
| Baseline/comparator | Completed seeded high-level workflow program and source-adapter Phase 11 addendum. |
| Primary criterion | Current seeded workflow checks pass or failures are recorded; source-adapter repaired/frozen distinction is visible; dirty worktree is recorded without reverting unrelated changes. |
| Veto diagnostics | Treating seeded benchmark as real-local closure; hiding dirty worktree state; claiming release/scientific/public validity; failing to preserve source-adapter frozen/repaired distinction; baseline artifact omits commands, expected snapshots, or backend/adapter availability. |
| Explanatory diagnostics | Test counts, CLI summaries, git status, artifact existence. |
| Not concluded | Any improvement on real-local cases, benchmark validity of future cases, release readiness, scientific validity, or broad theorem proving. |

## Forbidden Claims And Actions

- Do not modify code or benchmark cases in Phase 0 except result/ledger docs.
- Do not revert unrelated dirty files.
- Do not claim real-local benchmark closure.
- Do not promote repaired source-adapter artifacts to benchmark gate.
- Do not run package installs, network fetches, GPU jobs, or neighboring-repo
  edits.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only when:

- baseline checks are run or failures are documented;
- baseline freeze manifest records exact artifacts, commands, expected
  snapshots, scorer/runner state, and backend/adapter availability;
- seeded-vs-real-local distinction is explicit;
- source-adapter frozen/repaired distinction is explicit;
- Phase 1 subplan still matches the baseline and has no material sequencing
  issue.

## Stop Conditions

Stop if:

- baseline commands fail in a way that prevents measuring current workflows;
- predecessor artifacts are missing and cannot be reconstructed locally;
- the plan would require changing release/benchmark policy before inventory;
- continuing would require package install, network, credentials, destructive
  action, or editing sibling repos.

## End-Of-Phase Protocol

At phase end: run required checks; write the Phase 0 result; refresh/review the
Phase 1 subplan for consistency, correctness, feasibility, artifact coverage,
and boundary safety; then advance or stop.
