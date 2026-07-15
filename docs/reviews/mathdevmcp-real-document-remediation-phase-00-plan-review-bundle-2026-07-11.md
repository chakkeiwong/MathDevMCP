# Independent Read-Only Review Bundle

Date: 2026-07-11

Review name: `mathdevmcp-real-document-remediation-p00-plan-r4`

Supervisor/executor: Codex

Reviewer: fresh independent Codex read-only reviewer; external Claude transport
is policy-denied for this run

## Role Boundary

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state. Do not
authorize execution, publication, product, release, or scientific boundaries.

## Objective

Determine whether the Phase 00 subplan is safe, internally consistent,
feasible, and sufficient to quarantine document repair publication without
prematurely implementing Phase 01 evidence manifests.

## Bounded Artifacts To Inspect

- `docs/plans/mathdevmcp-real-document-remediation-phase-00-publication-quarantine-subplan-2026-07-11.md`
- `docs/plans/mathdevmcp-real-document-remediation-visible-gated-execution-runbook-2026-07-11.md`
- Master-plan lines 1122-1218 and Phase 00 lines 1168 onward in
  `docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`
- Current publication/output implementation surfaces:
  `src/mathdevmcp/document_derivation_tree.py` functions
  `_branch_backend_attempts`, `_attach_branch_backend_evidence`,
  `_branch_closure_status`, `_document_ready_repair_proposals`,
  `_document_gap_reports`, `_patch_candidate_for_branch`,
  `_validate_ready_proposal`, `_validate_gap_report`, `_compiled_item`,
  `_compile_tool_grounded_proposal_report`, `_augment_tree`, `_compact_tree`,
  `_target_failure_result`, `_target_result_for_row`, coverage construction,
  document repair/gap/compiler renderers, and `audit_document_derivation_tree`.
- `src/mathdevmcp/assumption_discovery.py` square-root rule only.
- Public pass-through/registration functions for this tool only in
  `src/mathdevmcp/cli.py`, `src/mathdevmcp/mcp_facade.py`, and
  `src/mathdevmcp/mcp_server.py`. These are read-only in P00; inability to
  propagate through their existing delegation requires plan revision.
- The complete future Phase 00 diff within the four-file implementation/test
  allowlist named by the subplan.
- Entire `tests/test_document_publication_quarantine.py` after it is created.
- In `tests/test_document_derivation_tree.py`, the unsafe simple-algebra test
  plus every exact test selected by the subplan's `-k` expression. The reviewer
  may verify those test bodies are synthetic `tmp_path` fixtures.

Do not review the whole repository or the whole 1,813-line master plan.

## Baseline Evidence

- Git commit: `a85fbb676eb4d551a8d78a70a5043524f308b7b9`.
- Master-plan digest:
  `5166192908f2a370a88538c07fefe79df984999059d85671087ddcc06a5b4182`.
- Existing simple-algebra focused test passed in 11.12 seconds while asserting
  `publishable_as_repair is True` and one ready repair.
- Current document code copies root backend attempts to every branch and uses
  raw `branch_promotion_report` output in document repair compilation.

## Round 1 Repairs To Verify

1. All patch candidate text is now within the recursive no-applicable-edit veto;
   `proposed_edit` and `proposed_text` are forbidden.
2. Raw promotion is allowed only under explicitly diagnostic names; every
   generic document promotion alias/count is effective and fail-closed.
3. Sibling, colliding legacy ref, and edit-mismatch fixtures are required.
4. Commands select synthetic fixtures only and do not open the repository's
   real lecture-note document.
5. Canonical LaTeX `\sqrt{x}` recognition/preservation is required and narrowly
   scoped.
6. Every declared log has an exact redirecting command, plus an assignment
   audit and structured recursive test.
7. Both adapter and worker exceptions require engineering-veto regressions.

## Round 2 Repairs To Verify

1. An executable, surface-tested emergency kill switch disables the whole
   document tool before a publication/edit-veto blocker result is written.
2. The recursive promotion test uses the exact path-aware raw-history exception
   and fails every generic alias/count leak.
3. Protected pre-existing dirty paths have pre-implementation hashes and a
   post-implementation check; `src/`/`tests/` paths have a failing allowlist
   gate and retained logs.
4. This review boundary covers all planned publication surfaces, the exact
   selected tests, the new adversarial file, and the complete bounded Phase 00
   diff during result review.

## Round 3 Repair To Verify

The raw-history exception is now a closed normalized-path schema. Only
`targets[*].tree.assumption_branches[*].backend_evidence.raw_promotion` and
`coverage.raw_promoted_count` may exist. Raw keys elsewhere, nested
promotion/count aliases inside the raw dictionary, and any non-allowlisted
`can_promote=true` are vetoes. No target/controller raw duplicate is allowed.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Will the planned P00 changes force all document repair publication off while preserving actionable diagnostics and explicit failure classes? |
| Baseline | Simple algebra currently publishes from legacy/unbound backend evidence. |
| Primary criterion | Publication disabled, generic promotion effectively false, and zero true repair flags/applicable edit fields on all surfaces; apparent closure becomes partial evidence with evidence-binding veto; unresolved assumptions and engineering errors remain visible. |
| Vetoes | Nested true repair/promotion flag, applicable `proposed_edit`/`proposed_text` or unblocked patch candidate, generic raw-promotion alias, lost assumption, error collapsed into mathematics, surface mismatch, or P01/P06 scope leakage. |
| Explanatory only | Test counts, raw backend status, tool availability, report counts. |
| Not concluded | No evidence-manifest correctness, real-document capability, backend breadth, release readiness, or default re-enablement. |

## Review Questions

1. Does the raw-versus-effective promotion split fail closed without creating a
   misleading second source of mathematical truth?
2. Is a non-repair partial-evidence report the correct quarantine output for
   apparent legacy backend closure?
3. Are `engineering_error`, `evidence_binding_error`, and
   `mathematical_blocked` distinguishable enough for P00 without stealing P06?
4. Do the tests cover nested publication leaks and assumption preservation, not
   merely a top-level false flag?
5. Does any work item silently require P01 manifest identity, P02 extraction,
   P03 semantics, P05 backend execution, or P06 ranking/ledger redesign?
6. Are the entry, stop, rollback, artifacts, and exact P01 handoff conditions
   sufficient?
7. Identify wrong baselines, proxy criteria, hidden assumptions, environment
   mismatches, artifact gaps, unsupported claims, or infeasible commands.

## Required Output

Findings first, ordered by severity. Be direct about fixable defects. End with
exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
