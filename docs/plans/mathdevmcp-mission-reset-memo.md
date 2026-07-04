# MathDevMCP Mission Reset Memo

Date: 2026-07-04

Status: `READ_THIS_FIRST_FOR_MISSION_ALIGNMENT_REVIEW_AGREED`

## Read This First

The benchmark is an instrument, not the mission.

The mission is to build a conservative agent-facing math-development tool,
exposed through CLI/MCP, that helps agents and colleagues audit mathematical
code and documents, locate proof gaps, missing assumptions, implementation
mismatches, and backend limitations, while never mistaking diagnostics for
proof.

Before starting any substantial lane, read:

- `docs/plans/mathdevmcp-mission-charter.md`
- `docs/plans/mathdevmcp-anti-drift-gate.md`
- `docs/plans/mathdevmcp-evidence-to-implementation-ledger.md`

Sonnet max read-only review agreed with this mission spine:
`REVIEW_STATUS=agreed`, `VERDICT=AGREE`,
`RUN_DIR=.claude_reviews/20260704-021100-mathdevmcp-mission-spine-sonnet-r1`.

## Current Direction

The v2 downstream-agent usefulness collection is closed as a bounded local
diagnostic with final Sonnet review agreement.

Do not default to building another benchmark. The current evidence points to
implementation work:

- improve review-packet/handoff-packet generation;
- make generated packets compact, actionable, provenance-aware, and explicit
  about assumptions, route gaps, veto risks, non-claims, and next artifacts;
- expose the improved workflow through stable CLI/MCP or library surfaces;
- use the v2 benchmark as a regression/evaluation harness after the product
  workflow changes.

## Product Spine To Preserve

```text
source label or code path
-> parser/provenance evidence
-> typed MathObligation diagnostics
-> route decision
-> shape/dimension diagnostics
-> backend evidence or explicit abstention
-> compact colleague/agent-facing report
-> benchmark or release artifact
```

## What To Ask At Lane Start

1. Which part of the product spine is being improved or protected?
2. Which user workflow becomes easier, safer, or more reproducible?
3. What evidence instrument will measure the change?
4. How will the result feed implementation, release readiness, or a regression
   guard?
5. What claim remains forbidden?

## What To Avoid

- Do not optimize benchmark totals for their own sake.
- Do not treat review/handoff packets as proof certificates.
- Do not add governance artifacts when a concrete CLI/MCP workflow repair is
  the justified next step.
- Do not weaken abstention, backend-evidence, provenance, or non-claim
  boundaries to make outputs look more successful.
- Do not design benchmark cases around unmerged implementation details.

## Current Best Next Plan

Draft and execute a mission-aligned implementation plan:

```text
Review/Handoff Packet Product Improvement
```

Likely scope:

- inspect current review-packet and handoff-packet builders;
- map the v2 winning case to missing product behavior;
- add or refine a compact packet schema if needed;
- implement focused improvements in the existing workflow surfaces;
- add tests for packet actionability, non-claim discipline, provenance,
  route-gap clarity, and CLI/MCP output shape;
- run targeted tests and the relevant benchmark/regression guard.

Stop if the plan turns back into "make v3 benchmark" without a concrete
product workflow change.
