# Claude Read-Only Review Bundle

Date: 2026-07-04
Review name: `mathdevmcp-mission-spine`
Supervisor/executor: Codex
Reviewer: Claude Sonnet max read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority. Claude is advisory only.

## Objective

Review whether the new MathDevMCP mission-spine documents correctly prevent
mission drift after the downstream-agent usefulness benchmark lane, without
turning benchmark construction into the product goal or weakening the
conservative proof/diagnostic boundary.

## Context Summary

The user clarified that building the benchmark was not the goal. The benchmark
was an instrument for a larger product mission: making MathDevMCP a
conservative agent-facing math-development tool, exposed through CLI/MCP, that
helps agents and colleagues audit mathematical code/documents, locate proof
gaps, missing assumptions, implementation mismatches, and backend limitations
without mistaking diagnostics for proof.

Codex added a mission spine and linked it from the benchmark-maintenance
handoff and v2 collection closeout.

## Artifacts To Inspect

Inspect only these bounded artifacts:

- `docs/plans/mathdevmcp-mission-charter.md`
- `docs/plans/mathdevmcp-anti-drift-gate.md`
- `docs/plans/mathdevmcp-evidence-to-implementation-ledger.md`
- `docs/plans/mathdevmcp-mission-reset-memo.md`
- `docs/plans/mathdevmcp-benchmark-maintenance-handoff-2026-07-02.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-visible-stop-handoff-2026-07-03.md`
- `docs/plans/mathdevmcp-downstream-agent-usefulness-v2-collection-phase-05-review-decision-result-2026-07-03.md`

Do not inspect the whole repository.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Do the new mission-spine docs correctly anchor future work to the product mission and route benchmark evidence into implementation without overclaiming? |
| Baseline/comparator | Existing release/interface product spine plus the closed v2 local diagnostic result. |
| Primary criterion | Agree only if the docs clearly state that the mission is conservative agent-facing math review through CLI/MCP, benchmarks are instruments, v2 evidence feeds review/handoff-packet implementation, and forbidden claims remain explicit. |
| Veto diagnostics | Benchmark described as the mission; review packets treated as proof; local v2 diagnostic promoted to product/release/public/scientific/general-reliability evidence; anti-drift gate blocks useful implementation without a real boundary; conflicting mission statements. |
| Explanatory diagnostics | Link coverage, closeout fields, evidence-to-implementation mapping, next-lane clarity, non-claims. |
| Not concluded | No implementation improvement yet, no release readiness, no product capability claim, no public benchmark validity, no scientific validation, no proof certificate, no general model reliability. |

## Review Questions

1. Is the canonical mission statement consistent with the existing
   release/interface product spine?
2. Does the anti-drift gate prevent benchmark/process drift without blocking
   mission-aligned implementation?
3. Does the evidence-to-implementation ledger correctly translate the v2
   result into review/handoff-packet implementation work?
4. Do the linked benchmark handoff/closeout docs clearly point future agents
   back to the mission spine?
5. Is there any fixable wording that should be patched before treating this
   mission spine as a canonical project guide?

## Required Output

Return concise findings first. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
