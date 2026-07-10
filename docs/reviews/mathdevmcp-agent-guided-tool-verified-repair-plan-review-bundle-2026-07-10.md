# Claude Read-Only Review Bundle

Date: 2026-07-10
Review name: `mathdevmcp-agent-guided-tool-verified-repair-plan-review`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

READ-ONLY REVIEW ONLY.

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review the new master program and visible runbook for the MathDevMCP
agent-guided, tool-verified derivation repair lane.

The key design is:

- the agent proposes mathematical hypotheses only as candidate branches;
- the derivation tree verifies, refutes, partially closes, rejects, or blocks
  those branches;
- deterministic tools/backends carry certification where possible;
- reports publish only tool/tree-grounded repairs or exact gap reports.

## Artifacts To Inspect

- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-master-program-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-visible-runbook-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-00-governance-baseline-subplan-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-01-contracts-subplan-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-02-agent-hypotheses-subplan-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-03-recursive-tree-subplan-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-04-backend-formalization-subplan-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-05-expansion-rules-subplan-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-06-proposal-compiler-subplan-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-07-cli-mcp-subplan-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-08-parallel-search-subplan-2026-07-10.md`
- `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-09-real-doc-mission-control-subplan-2026-07-10.md`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the plan internally consistent, correctly sequenced, and safe for implementing agent-guided, tool-verified repair? |
| Baseline/comparator | Current Phase 06 reports that can still render blocked ranked branches as repair-like prose. |
| Primary criterion | The plan must enforce that agent hypotheses enter only as candidate branches, deterministic tools/backends verify or block branches, and reports publish only evidence-grounded repairs or exact gap reports. |
| Veto diagnostics | Raw agent text allowed as repair; diagnostic evidence promoted to proof; blocked branch can render as repair; missing stop conditions; detached execution despite visible template; Claude treated as executor; implementation sequence violates dependencies. |
| Explanatory diagnostics | Optional backend absence, conservative reports, Claude unavailable, dirty worktree. |
| Not concluded | No implementation correctness, no backend proof, no release readiness, no publication readiness. |

## Review Questions

1. Is there a material correctness or boundary issue in the master program or
   runbook?
2. Is the phase order logically dependency-safe?
3. Does every phase have objective, entry conditions, artifacts, checks/reviews,
   evidence contract, forbidden claims/actions, next-phase handoff, and stop
   conditions?
4. Does the plan prevent the current regression where blocked diagnostic
   branches become repair-like prose?
5. Are there unsupported claims, hidden authority transfers, or missing stop
   conditions?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
