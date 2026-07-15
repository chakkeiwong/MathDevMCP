# MathDevMCP Real-Document Remediation Phase 08 Plan Review Record

Date: 2026-07-14

Scope: independent read-only review of the Phase 08 frozen real-document
validation subplan. Codex remains the supervisor and executor. The reviewer did
not edit files, launch real-document workflows, execute a mathematical backend,
or authorize publication, source edits, defaults, release, or scientific
claims.

## Findings And Repairs

The review identified and the plan visibly repaired these material issues:

1. Context requirements were not fully pre-registered, and the risky-debt
   proposition container was not separated cleanly from its two equation
   targets. The plan now fixes every context request and explicitly partitions
   context-only `prop:interior-foc` from paginated `eq:foc-k` and `eq:foc-b`.
2. CAS-success terminology could be read as proof certification. The plan now
   reserves `formal_proof_certified` for a proof-checking kernel and calls a
   successful scoped CAS construction/check only `backend_checked`.
3. A target equation could tautologically support its own context requirement.
   Equation nodes, own labels, and target-span matches are excluded; exact
   required-file equality and a self-label-only regression are mandatory.
4. HEAD and dirty paths did not bind the uncommitted implementation that would
   construct and verify scientific artifacts. The plan now requires a
   pre-import code snapshot, SHA-256 identity, loaded-module accounting, and
   drift vetoes through production, verification, and interpretation. An
   adapter repair starts a fresh P08A run.
5. Later commands accepted only a shared artifact parent, which could mix
   attempts. Fresh-run creation now returns one immutable run-id/root binding;
   every later command requires the literal run root and rejects parent-only,
   latest, implicit, symlink, and cross-run selection.

## Final Review

The reviewer confirmed that the repaired plan binds frozen inputs, context
requests, CAS-versus-proof claims, dirty implementation bytes, immutable run
identity, and compact/detailed target partitions. Publication remains disabled,
stale publication arguments are absent, the four frozen digests match, and
`git diff --check` passes.

Residual risk is implementation of the new runner and any derivative adapter.
The plan gates and reviews those before real backend execution.

```text
VERDICT: AGREE
```
