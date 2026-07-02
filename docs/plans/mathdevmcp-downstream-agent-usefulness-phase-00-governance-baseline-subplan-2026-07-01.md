# Phase 0 Subplan: Governance And Baseline Freeze

Date: 2026-07-01

Status: `LAUNCHED_PENDING_PHASE_0_EXECUTION`

## Phase Objective

Freeze the current repository state, prior packet-standard decision, existing
high-level workflow benchmark artifacts, approval boundaries, and baseline
checks before any new contract, case, prompt, response, or repair work.

## Entry Conditions Inherited From Previous Phase

- This is the first execution phase.
- The master program and visible runbook exist.
- The prior packet standard is only a local candidate.
- Codex is supervisor/executor.
- Claude is read-only reviewer only.

## Required Artifacts

- Phase 0 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-00-governance-baseline-result-2026-07-01.md`.
- Updated visible execution ledger.
- Updated stop handoff if execution stops.
- Git commit and dirty-worktree summary.
- Inventory of existing high-level workflow, packet, benchmark, and calibration
  artifacts.
- Baseline local-check outputs or summaries.

## Required Checks, Tests, Reviews

- `git rev-parse HEAD`.
- `git status --short`.
- `python3 -m pytest tests/test_agent_handoff_packet.py tests/test_high_level_workflows.py tests/test_real_local_high_level_benchmark.py -q`.
- `python3 -m mathdevmcp.cli high-level-workflow-quality --root .`.
- Local skeptical audit recorded in the ledger.
- Claude read-only review of the Phase 0 result if a material baseline
  ambiguity appears; otherwise Claude review of the master/runbook before
  launch is sufficient.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What exact baseline and approval boundary does the downstream-agent usefulness program start from? |
| Baseline/comparator | Current commit, clean/dirty state, prior high-level workflow benchmark, packet-standardization result, and A/B/C calibration non-claims. |
| Primary criterion | Baseline state, artifacts, tests, and human-approval boundaries are recorded without changing implementation behavior. |
| Veto diagnostics | Dirty state ignored; prior B/C tie misrepresented; missing baseline artifacts hidden; tests fail in a way that makes current behavior uninterpretable; code or benchmark behavior edited during inventory. |
| Explanatory diagnostics | Git state, artifact inventory, focused pytest result, quality command output, approval-boundary table. |
| Not concluded | No downstream-agent usefulness, promotion, release readiness, scientific validation, product capability, or public benchmark validity. |

## Forbidden Claims Or Actions

- Do not edit code or benchmark behavior.
- Do not collect new downstream responses.
- Do not claim the packet standard is superior to B under the prior frozen
  rubric.
- Do not treat passing baseline checks as downstream-agent usefulness.
- Do not modify unrelated dirty user work.

## Exact Next-Phase Handoff Conditions

Advance to Phase 1 only if:

- Phase 0 result exists and records commit, dirty state, artifact inventory,
  baseline checks, and approval boundaries;
- no baseline failure prevents interpreting the current system, or the failure
  is recorded as a Phase 1 constraint;
- the Phase 1 subplan has been reviewed for sequencing, correctness,
  feasibility, artifact coverage, and boundary safety.

## Stop Conditions

Stop and write a blocker result if:

- baseline artifacts needed to define the comparator are missing and cannot be
  reconstructed locally;
- baseline tests fail in a way that makes current behavior uninterpretable;
- continuing would require package installs, network fetches, credentials,
  destructive git/file actions, or response collection without approval.

## Phase Close Protocol

At phase close:

1. run the required local checks;
2. write the Phase 0 result/close record;
3. draft or refresh the Phase 1 subplan;
4. review the Phase 1 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
