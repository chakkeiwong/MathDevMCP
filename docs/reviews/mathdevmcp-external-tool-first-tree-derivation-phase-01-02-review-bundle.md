# Claude Read-Only Review Bundle

Date: 2026-07-08
Review name: `mathdevmcp-external-tool-first-tree-derivation-phase-01-02`
Supervisor/executor: Codex
Reviewer: Claude read-only reviewer

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, approve
boundary crossings, or act as execution authority.

## Objective

Review Phase 1/2 of the external-tool-first tree derivation runbook. The phase
adds a serializable derivation-search tree ledger and tests. It must not claim
to implement a prover, search executor, backend adapter, or mathematical
certification.

## Artifacts To Inspect

- `docs/plans/mathdevmcp-external-tool-first-tree-derivation-phase-01-02-subplan-2026-07-08.md`
- `src/mathdevmcp/derivation_search_tree.py`
- `tests/test_derivation_search_tree.py`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the Phase 1/2 data model serialize derivation-search branches without overclaiming proof/refutation? |
| Baseline/comparator | Phase 0 external-tool-first route plan and current one-shot high-level workflows. |
| Primary criterion | A branch/tree records source, assumptions, external-tool-first evidence, backend attempts, blockers, patch candidates, and non-claims; promotion guards require certifying backend/counterexample evidence for proved/refuted statuses. |
| Veto diagnostics | Route/retrieval/static/proof-state evidence can mark a branch proved/refuted; backend unavailability can become refutation; initial in-house search proceeds without external-tool evidence or gap blocker; patch candidates can omit location or rationale. |
| Explanatory diagnostics | Naming/schema consistency, determinism, future adapter integration concerns. |
| Not concluded | No backend execution, no search expansion, no target-document proof, no public release readiness. |

## Review Questions

1. Is there a material correctness or boundary issue in the new tree contract?
2. Do the promotion guards prevent route/retrieval/static/proof-state evidence
   and backend unavailability from becoming proof/refutation claims?
3. Are the focused tests sufficient for this representation-only phase?
4. Are there unsupported claims or hidden authority transfers?

## Required Output

Return concise findings. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
