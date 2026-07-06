# MathDevMCP Derivation Audit/Proposal Gated Overnight Execution Plan

Date: 2026-07-06

Status: `DRAFT_APPROVAL_REQUIRED`

## Purpose

This is the detached/overnight execution plan requested for the derivation
audit/proposal master program. It is separate from the visible runbook because
the visible template explicitly forbids detached or nested supervisors.

## Role Contract

- Codex is supervisor and executor.
- Claude Opus/max-effort is a read-only reviewer only.
- Claude cannot authorize boundary crossings.
- Detached launch is not allowed until a concrete supervisor command and user
  approval exist.

## Master Program

- `docs/plans/mathdevmcp-derivation-audit-proposal-master-program-2026-07-06.md`

## Launch Preconditions

Detached launch is allowed only after:

1. master program exists;
2. visible runbook exists;
3. Phase 0 and Phase 1 subplans exist;
4. plan review returns `VERDICT: AGREE` or documented Codex fallback review
   finds no material blocker;
5. current visible Phase 0 result records baseline checks;
6. a concrete supervisor command is selected;
7. user approves detached execution and Claude model/API usage.

## Candidate Launcher

Use the claudecodex launcher only after approval:

```bash
bash /home/chakwong/python/claudecodex/scripts/overnight_gated_launch.sh \
  --root /home/chakwong/python/MathDevMCP \
  --run-id mathdevmcp-derivation-audit-proposal-20260706 \
  --log-dir /home/chakwong/python/MathDevMCP/docs/plans/logs \
  --supervisor-cmd '<CONCRETE_SUPERVISOR_COMMAND>'
```

`<CONCRETE_SUPERVISOR_COMMAND>` is intentionally not filled in during Phase 0.
Using a shell script that merely runs tests would not execute the master
program. Using a detached Codex executor requires explicit user approval and a
known safe command surface.

## Required Detached Supervisor Behavior

The detached supervisor command, if approved, must:

- read the master program and current phase subplan;
- execute one phase at a time;
- use Claude only through read-only review gates;
- write phase results and handoffs under `docs/plans`;
- preserve unrelated dirty work;
- stop on human-required boundaries;
- never change pass/fail criteria after seeing results;
- write a visible stop handoff if blocked.

## Repair Loop

For each material blocker:

1. write a blocker note under `docs/plans`;
2. get read-only review when material;
3. patch visibly in the copied workspace;
4. rerun focused checks;
5. record result;
6. stop after five review rounds for the same blocker.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the master program execute unattended without losing proof-boundary discipline or review accountability? |
| Baseline/comparator | Visible execution in current Codex conversation. |
| Primary criterion | Detached process writes phase results, review trail, tests, and a final handoff while preserving non-claims and stopping on boundaries. |
| Veto diagnostics | No concrete supervisor command, no approval, hidden reviewer authority transfer, destructive command, uncontrolled workspace writes, no handoff artifact. |
| Explanatory diagnostics | Runtime, log path, review status, test counts. |
| Not concluded | Detached success would not prove mathematical correctness or release readiness. |
| Artifacts | Launch log, dirty manifest, phase results, final handoff. |

## Approval Needed

Before detached launch, ask the user to approve:

- Claude Code/API usage through
  `/home/chakwong/python/claudecodex/scripts/claude_review_gate.sh`;
- any detached Codex or supervisor command chosen for
  `<CONCRETE_SUPERVISOR_COMMAND>`;
- long-running overnight process creation through
  `/home/chakwong/python/claudecodex/scripts/overnight_gated_launch.sh`.

## Current Decision

Do not launch detached overnight execution during Phase 0. Execute visibly in
the current Codex conversation until the user approves a concrete detached
supervisor command.
