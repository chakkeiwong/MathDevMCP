# Phase 0 Subplan: Governance Baseline And Launch

Date: 2026-07-02

Status: `READY`

## Phase Objective

Record the baseline, validate the new master program/runbook artifacts, confirm
current benchmark state, and launch visible gated execution without changing
implementation behavior.

## Entry Conditions

- Repaired downstream-agent benchmark result exists.
- Tool improvement plan and benchmark-maintenance handoff exist.
- No implementation phase has started.
- Dirty/untracked worktree state is expected and must be preserved.

## Required Artifacts

- Master program.
- All phase subplans.
- Visible gated execution runbook.
- Claude review trail.
- Visible execution ledger.
- Stop handoff.
- Phase 0 result record.

## Required Checks/Tests/Reviews

- `git status --short`
- `python3 -m pytest tests/test_downstream_usefulness_prompts.py tests/test_agent_handoff_packet.py`
- JSON parse for `.mathdevmcp/downstream_agent_usefulness/*.json`
- prompt contract validation for original and repaired downstream manifests
- implementation-boundary status audit: compare current `git status --short`
  against the Phase 0 prelaunch status and confirm Phase 0 made no
  implementation/test edits
- `git diff --check` over new tool-improvement plan artifacts
- Claude read-only review of master program/runbook/subplan summary when
  available

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the implementation master program ready to launch under visible gated execution? |
| Baseline/comparator | Current repo state, repaired benchmark result, and existing high-level workflow modules. |
| Primary criterion | Required plan/runbook/subplan artifacts exist, local checks pass or known limitations are recorded, Phase 0 made no implementation/test edits, and Phase 1 handoff is safe. |
| Veto diagnostics | Missing subplan; wrong benchmark baseline; hidden approval boundary; Claude treated as execution authority; implementation edits during Phase 0; failed JSON/prompt validation not recorded. |
| Explanatory diagnostics | Worktree status, artifact inventory, repaired benchmark summary, Claude review trail. |
| Not concluded | No tool improvement, benchmark improvement, release readiness, product capability, scientific validation, public benchmark validity, or general reliability. |

## Forbidden Claims/Actions

- Do not edit implementation code in Phase 0.
- Do not collect new benchmark responses.
- Do not claim tool improvement from planning artifacts.
- Do not use Claude as executor.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only if:

- Phase 0 result is written;
- plan/runbook/subplan checks pass or limitations are explicitly bounded;
- Phase 0 implementation-boundary audit confirms no Phase 0 implementation or
  test edits beyond pre-existing dirty/untracked state;
- Claude review either returns `AGREE`, or true bounded Claude unavailability
  is recorded with no unresolved material findings from any completed fallback
  critique and local checks passing;
- Phase 1 subplan is reviewed and still feasible.

## Stop Conditions

Stop if plan artifacts are missing, the repaired benchmark baseline cannot be
validated, local checks fail in a way that invalidates the launch, or Claude
review identifies an unfixable sequencing/boundary problem.
