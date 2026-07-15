# MathDevMCP Phase 08C1 Target-Fidelity Review Bundle

Date: 2026-07-14

Review name: `mathdevmcp-p08c1-target-fidelity-r1`

Supervisor/executor: Codex

Reviewer: Claude Opus, read-only, max effort

## Role Boundary

Review only. Do not edit files, run mutating commands, launch agents, execute a
backend/model/network service, or authorize publication/default/release
boundaries. Codex remains supervisor and executor.

## Objective

Skeptically determine whether the P08C1 repair truly prevents physical label
rows or enclosing displays from replacing a validated label-scoped
mathematical obligation, and whether the passing replay is sufficient evidence
for refreshing P08D against the new audit baseline.

## Exact Artifacts

Inspect these bounded artifacts and scoped regions only:

- `docs/plans/mathdevmcp-real-document-remediation-phase-08c1-label-scoped-audit-integration-repair-subplan-2026-07-14.md`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-08c1-label-scoped-audit-integration-repair-result-2026-07-14.md`;
- `src/mathdevmcp/document_derivation_tree.py`, only functions
  `_requested_equation_labels`, `_select_label_scoped_targets`,
  `_semantic_packet_from_label_scoped_target`, `_target_result_for_row`,
  `_ordered_target_results`, and `audit_document_derivation_tree`;
- `tests/test_document_derivation_real_regressions.py`;
- `tests/test_document_derivation_tree.py`, only the semantic-packet and
  multiline Bellman assertions near the first 210 lines;
- `scripts/run_p08c1_target_fidelity_replay.py`;
- `tests/test_p08c1_target_fidelity_replay.py`;
- `.local/mathdevmcp/evidence/p08-20260714/p08c1/20260714T121103Z-fc7811786801/target-fidelity.json`;
- `.local/mathdevmcp/evidence/p08-20260714/p08c1/20260714T121103Z-fc7811786801/decision.json`;
- immutable comparator
  `.local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0/p08a/extraction.json`, only the five obligations named below.

Do not inspect the whole repository and do not rely on the stale P08C audit as
the mathematical comparator.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does every frozen document-audit target preserve the exact validated P08A label-scoped obligation through semantic packet and typed tree input? |
| Comparator | Exact P08A obligations for `eq:panel-npv-functional`, `eq:incremental-cash-flow`, `eq:incremental-npv`, `eq:foc-k`, and `eq:foc-b`. |
| Primary criterion | Exact obligation record/ID/digest, normalized target, lhs/rhs, source math, spans, inventories, request order, and typed-tree equality for all five targets. |
| Vetoes | Any legacy-row fallback, full-display sibling contamination, incomplete lhs/rhs, ambiguous extraction accepted, target omission/duplication/reorder, replay trust loop, mutation blind spot, backend attempt, publication/promotion escape, or code/evidence mismatch. |
| Explanatory only | Test counts, packet size, blocker count, and raw string formatting. |
| Not concluded | Mathematical truth, proof, complete assumptions, compact-product pass, publication/default/release readiness, Phase 08 closure, or mission completion. |

## Local Evidence

- Focused target/extractor suite: `19 passed`.
- Full document tree: `17 passed`.
- Response/publication adjacency: `52 passed` and `13 passed`.
- Surface/frozen-runner adjacency: `73 passed`.
- P08C/P08C1 runner checks: `35 passed` and `3 passed`.
- Replay decision:
  `8c2ca339fc5a360be7abaa4264a6b33d773995a160437d11ffdcab5d54d86c7b`.
- Independent verify: `verified: true`.
- All 14 registered fidelity mutations rejected.
- Raw audit invocations: one per document; mathematical backend attempts: 0.
- `py_compile` and `git diff --check`: pass.

## Review Questions

1. Can any focused equation label still reach `_semantic_packet` through a
   physical locator row rather than the validated obligation adapter?
2. Can a proposition label or duplicate focus list cause child omission,
   duplication, reorder, or context/target confusion?
3. Does `_semantic_packet_from_label_scoped_target` preserve exact obligation
   semantics, or does any compatibility/display field reintroduce sibling
   source or alter target/lhs/rhs/inventories?
4. Can incomplete, ambiguous, orphaned, or inconsistent extraction fall back
   or be counted as covered?
5. Does the tree/controller demonstrably consume the packet-derived typed
   target, or could the replay pass while downstream work uses another target?
6. Can the replay validator trust stored status, fail to bind current code,
   miss a material mutation, or accept an artifact created after a partial
   engineering failure?
7. Are the regression changes scientifically correct, especially rejecting
   the old Bellman sibling absorption?
8. Is any material finding unresolved that should block refreshing and
   executing P08D against the P08C1 audit bytes?

## Required Output

Lead with findings ordered by severity and cite local file/line references.
If no material finding remains, say so. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
