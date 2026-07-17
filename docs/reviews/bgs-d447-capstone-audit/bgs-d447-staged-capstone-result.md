# BGS D447 Staged Capstone Result

Decision: `PARTIAL_CAPSTONE_SCALE_OR_TOOL_GAPS`

## Phase Results

| Phase | Status |
| --- | --- |
| readiness | `passed` |
| ingestion | `passed_with_predeclared_ownership_gaps` |
| paired regression | `passed` |
| scientific slice | `passed` |
| full capstone | `partial_scale_or_tool_gaps` |
| independent generalization | `not_tested_no_verified_clean_holdout` |

## Decision Table

| Field | Result |
| --- | --- |
| Decision | `PARTIAL_CAPSTONE_SCALE_OR_TOOL_GAPS` |
| Primary criterion | Not fully met: exact identity, paired boundary behavior, and the 18-label slice passed, but the bounded 566-label deep capstone did not complete. |
| Veto status | No source-integrity, cross-version, branch-erasure, or claim-promotion veto fired. |
| Main uncertainty | Independent generalization is untested; source-dependent BGS branches and seven nested-alignment ownership labels remain unresolved. |
| Next justified action | Implement resumable/batched deep workflows and first-class scope diagnostics, then acquire a provenance-clean holdout before any broad-generalization claim. |
| Not concluded | BGS correctness, exact replication, implementation equivalence, author error, theorem proof, publication readiness, or independent generalization. |

## Separate Ledgers

### Engineering correctness

- D447 physical/mathematical/extractable accounting: 593 / 573 / 566.
- Exact D447 mathematical-label resolutions: 573.
- Full-capstone status: partial_scale_or_tool_gaps.
- Frozen DynareMCP source digests were unchanged.

### Mathematical/backend validity

- C.71--C.77 workflow status: passed.
- C.75 sign/timing and C.77 asset-base alternatives remained visible and uncertified.
- Backend/CAS outcomes are diagnostic within their encoded scope only; absence or abstention is not a refutation.

### Scientific interpretation

- D447 boundary prose improves claim discipline but does not prove unchanged mathematics.
- D446/D447 are contaminated regression sources, not a holdout.
- No statistically or mathematically supported system-level superiority ranking is made.

## Post-Run Red Team

- The strongest alternative explanation for the slice pass is overfit to known D447 repairs and source language.
- A clean holdout failure would overturn any future broad-generalization inference from this capstone.
- The weakest evidence is scientific certification: the report remains source-dependent and many obligations are outside deterministic backend scope.

## Remaining Gaps

- Seven equation labels after nested aligned structures are lookup-only until mathematical row ownership is formalized.
- The fixed-point math/code audit localizes the missing theta dependency, but its first-class scope diagnostic remains `not_triggered`.
- No provenance-clean independent holdout was identified or run.
- D447 cannot by itself establish whole-system mathematical or scientific correctness.
- Full-document deep workflows require resumable batching or shared evidence state; bounded timeouts were: audit_and_propose_fix after 1200.1 seconds; audit_math_document_rigor after 1200.1 seconds; audit_document_derivation_tree after 1200.0 seconds.
- Representative compact packet calls remained slow (45.7--165.2 seconds each).

## Run Manifest

Raw manifest: `.local/mathdevmcp/evidence/bgs-d447-capstone-20260717/run-manifest.json`
