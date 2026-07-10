# Phase 0 Subplan: Governance, Plan Review, And Launch

Date: 2026-07-07

Status: `EXECUTED`

## Phase Objective

Validate the master program, visible gated execution runbook, review process,
and first implementation subplan before changing the new Python workflow code.

## Entry Conditions

- User requested a concrete Python path and gated execution.
- Claude review-gate guide has been read.
- Existing dirty worktree changes must be preserved.
- No implementation for `math_document_rigor.py` has started.

## Required Artifacts

- Master program.
- Phase 0-4 subplans.
- Visible gated execution runbook.
- Visible execution ledger.
- Claude review trail.
- Stop handoff.
- Claude review bundle for Phase 0 plan artifacts.
- Phase 0 result record.

## Required Checks/Tests/Reviews

- `git status --short`
- `git diff --check` over new plan/review artifacts.
- Claude read-only review gate over the bounded Phase 0 review bundle.
- If Claude gate is unavailable, record probe/fallback status and run a fresh
  Codex skeptical review before continuing.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the document-rigor audit program safe and concrete enough to launch? |
| Baseline/comparator | Current manual audit plan and existing MathDevMCP workflow tools. |
| Primary criterion | Plan/runbook/subplans exist, define evidence contracts and stop conditions, and receive Claude `AGREE` or documented bounded reviewer unavailability with Codex skeptical review. |
| Veto diagnostics | Missing stop conditions; Claude as executor; target LaTeX source edit during planning; no partial-coverage boundary; LeanDojo certification confusion; unbounded prompt. |
| Explanatory diagnostics | Review-gate status, git status, diff check, Codex skeptical audit. |
| Not concluded | No implementation quality, no document rigor result, no proof/document/scientific/product claim. |

## Forbidden Claims/Actions

- Do not edit implementation files in Phase 0.
- Do not run the document audit in Phase 0.
- Do not send whole repository or target document contents to Claude.
- Do not treat Claude as an execution authority.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 1 only if:

- Phase 0 result is written;
- plan artifacts pass `git diff --check`;
- Claude review returns `AGREE`, or true bounded reviewer unavailability is
  recorded with no unresolved material Codex findings;
- Phase 1 subplan is still feasible and bounded.

## Stop Conditions

Stop if the review finds an unfixable program-boundary issue, if local checks
invalidate the plan artifacts, or if continuing would require installing
packages, fetching network resources, or changing target document content.
