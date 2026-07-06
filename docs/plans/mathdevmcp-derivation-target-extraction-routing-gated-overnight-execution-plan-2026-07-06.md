# Gated Overnight Execution Plan: Derivation Target Extraction And Routing

Date: 2026-07-06

Status: `DRAFT_NEEDS_APPROVAL_BEFORE_DETACHED_LAUNCH`

## Objective

Provide a detached-capable execution plan for the derivation target extraction
and backend routing master program. Codex remains supervisor/executor; Claude is
read-only reviewer only.

## Boundary

This plan does not itself authorize detached launch. Detached launch requires a
concrete command and explicit approval.

## Supervisor And Reviewer Roles

- Supervisor/executor: Codex.
- Reviewer: Claude Opus, read-only, max/high effort.
- Claude may not edit files, run experiments, launch agents, authorize product
  or scientific claims, or cross human/runtime/model/funding boundaries.

## Repair Loop

For each phase:

1. run required local checks;
2. write phase result;
3. draft/refresh next subplan;
4. review next subplan/result;
5. if review finds a fixable issue, patch visibly and rerun focused checks;
6. retry Claude review at max effort for material issues, max five rounds;
7. if not converged, write blocker result and stop.

## Required Approval Before Detached Launch

Ask before running any detached launch command such as:

```bash
bash /home/chakwong/python/claudecodex/scripts/overnight_gated_launch.sh ...
```

Expected approval needs:

- Claude review gate model/API usage;
- detached launch script if user wants unattended execution;
- no package install, network fetch, destructive git command, or source document
  edit is planned.

## Proposed Visible First Step

Before detached execution, run Phase 0 visibly:

- baseline tests;
- compact Claude review gate or fallback review;
- Phase 0 result.

Detached execution may start only after Phase 0 passes and user approves a
concrete launch command.

## Stop Conditions

Stop if:

- Claude review/export is rejected and Codex fallback finds a material blocker;
- any phase changes scientific/product boundaries;
- tests fail in a way that cannot be repaired within scoped changes;
- continuing requires unapproved external state changes.
