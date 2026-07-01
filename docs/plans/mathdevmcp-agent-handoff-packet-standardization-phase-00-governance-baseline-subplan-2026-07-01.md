# Phase 0 Subplan: Governance And Baseline Inventory

Date: 2026-07-01

Status: `DRAFT_PENDING_MASTER_REVIEW`

## Phase Objective

Freeze the current repository state, prior calibration decision, existing
packet-related code surfaces, and baseline checks before any contract or
implementation work.

## Entry Conditions Inherited From Previous Phase

- This is the first phase.
- The master program and visible runbook exist.
- The prior calibration result is treated as provisional local design input,
  not as scored C-over-B superiority.
- Codex is supervisor/executor; Claude is read-only reviewer only.

## Required Artifacts

- Phase 0 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-standardization-phase-00-governance-baseline-result-2026-07-01.md`.
- Updated visible execution ledger.
- Updated stop handoff if execution stops.
- Git commit and dirty-worktree summary.
- Hashes or existence records for prior calibration artifacts.
- Inventory of existing packet-related code/test surfaces.

## Required Checks, Tests, Reviews

- `git rev-parse HEAD`.
- `git status --short`.
- `sha256sum` or equivalent hash for prior calibration artifacts that exist.
- Targeted baseline tests:
  `python3 -m pytest tests/test_prepare_review_packet.py tests/test_real_local_high_level_benchmark.py -q`.
- Local skeptical audit recorded in the ledger.
- Claude review is optional for the Phase 0 result unless a material baseline
  ambiguity appears.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What is the exact baseline from which packet standardization starts? |
| Baseline/comparator | Current repository state and prior calibration artifacts. |
| Primary criterion | Current state, artifacts, packet surfaces, and baseline test status are recorded without changing code. |
| Veto diagnostics | Missing prior calibration decision; baseline tests unavailable without explanation; dirty worktree ignored; C-over-B overclaim; code edited during inventory. |
| Explanatory diagnostics | Dirty-file list, code-surface inventory, artifact hashes, baseline test output. |
| Not concluded | No implementation readiness, release readiness, proof correctness, or standard promotion. |

## Forbidden Claims Or Actions

- Do not edit code or docs other than Phase 0 ledger/result/stop-handoff
  artifacts.
- Do not claim C scored better than B.
- Do not treat passing baseline tests as proof of packet-standard readiness.
- Do not discard or revert unrelated dirty changes.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- Phase 0 result exists and records commit, dirty status, artifact hashes or
  missing-artifact explanations, packet surface inventory, and baseline checks;
- no baseline test failure blocks understanding of current behavior, or the
  failure is recorded as a Phase 1 constraint;
- the next Phase 1 subplan has been reviewed for sequencing, artifact coverage,
  feasibility, and boundary safety.

## Stop Conditions

Stop and write a blocker result if:

- prior calibration artifacts needed to define the baseline are missing and
  cannot be reconstructed from local files;
- baseline tests fail in a way that makes current packet behavior impossible to
  characterize;
- continuing would require destructive git/file actions, package installs,
  network fetches, or editing unrelated dirty work.

## Phase Close Protocol

At phase close:

1. run the required local checks;
2. write the Phase 0 result/close record;
3. refresh the Phase 1 subplan if the baseline inventory changes assumptions;
4. review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
