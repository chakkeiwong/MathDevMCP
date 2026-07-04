# Phase 00 Subplan: Governance And Source Boundary

## Phase Objective

Establish the execution baseline, source/privacy boundary, skeptical audit,
and local-only evidence contract before any fixture or code changes.

## Entry Conditions Inherited From Previous Phase

- The pilot inventory exists at
  `docs/plans/mathdevmcp-real-local-high-level-workflow-pilot-cases-2026-06-29.md`.
- The current high-level workflow implementation and benchmark gate exist in
  the repo.
- The worktree is dirty from prior user-approved work; unrelated changes must
  be preserved.

## Required Artifacts

- Master program:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-master-program-2026-06-29.md`
- Visible runbook:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-visible-gated-execution-plan-2026-06-29.md`
- Review trail:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-claude-review-trail-2026-06-29.md`
- Execution ledger:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-visible-execution-ledger-2026-06-29.md`
- Phase result:
  `docs/plans/mathdevmcp-real-local-high-level-pilot-phase-00-governance-source-boundary-result-2026-06-29.md`
- Phase 01 subplan.

## Required Checks, Tests, And Reviews

- Local checks:
  - `rg -n "Status:|Case 1|Case 10|Immediate Recommendation" docs/plans/mathdevmcp-real-local-high-level-workflow-pilot-cases-2026-06-29.md`
  - `python3 -m pytest tests/test_high_level_workflows.py tests/test_derive_from.py tests/test_prove_or_counterexample.py tests/test_assumptions_for.py tests/test_debug_derivation.py tests/test_audit_math_to_code.py tests/test_prepare_review_packet.py`
- Review:
  - Codex skeptical audit required.
  - Claude read-only review required for the master program and phase ladder.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is the proposed pilot execution governed, source-bounded, and compatible with current high-level workflow capabilities? |
| Baseline/comparator | Prior pilot inventory plus current high-level seeded benchmark tests. |
| Primary pass criterion | Source/privacy boundaries and non-claims are explicit; current high-level workflow tests pass; Phase 01 handoff is well-scoped. |
| Veto diagnostics | Missing stop conditions, source exfiltration risk, treating local pilot as benchmark-gate evidence, failing baseline high-level workflow tests. |
| Explanatory diagnostics | Dirty-worktree summary, inventory grep, focused high-level tests. |
| Not concluded | Fixture validity, executable pilot quality, adapter readiness, release readiness. |
| Artifacts | Phase result, ledger entry, Claude review entry, refreshed Phase 01 subplan. |

## Forbidden Claims And Actions

- Do not copy substantial source excerpts from sibling repos.
- Do not send whole files or whole plans to Claude.
- Do not modify neighboring repos.
- Do not claim the pilot is public, CI-safe, release-ready, or benchmark-gate
  evidence.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 01 only if:

- Claude and Codex converge on the phase ladder or fixable issues are patched;
- focused high-level workflow tests pass;
- source-boundary and stop-condition rules are recorded;
- Phase 01 has a clear manifest/case contract and no implementation work is
  hidden inside Phase 00.

## Stop Conditions

- Stop if baseline high-level workflow tests fail for reasons unrelated to this
  program.
- Stop if source/privacy policy is ambiguous for selected cases.
- Stop if Claude review identifies an unresolved sequencing or boundary flaw.
- Stop if continuing would require copying private material or changing
  neighboring repos.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 01 subplan.
4. Review the Phase 01 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
