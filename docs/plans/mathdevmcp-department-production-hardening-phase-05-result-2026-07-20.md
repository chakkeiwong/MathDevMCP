# Phase 05 Result: Core Architecture Refactor Slices

Date: 2026-07-20
Status: complete_with_scoped_residuals
Plan: `mathdevmcp-department-production-hardening-phase-05-core-refactor-subplan-2026-07-20.md`

## Completed Slices

- Added dependency-free `ExternalBackend` protocol, injected backend execution,
  P04 schema identifiers, and live-manifest verifier registration in
  `backend_protocol.py`; no Sage import direction or scientific result
  semantics changed.
- Added shared `write_bytes_no_replace` storage primitive and routed agent-report
  persistence through it; existing canonical bytes, digest, symlink, and
  collision behavior is preserved.
- Existing evidence-manifest and document-artifact tests remain the
  characterization suite for path safety, tamper detection, canonical
  serialization, and no-overwrite behavior.

## Verification

| Check | Result |
| --- | --- |
| Backend/storage plus existing evidence suites | `126 passed` in the settled focused rerun; an earlier narrower slice recorded `75 passed` |
| Governance subprocess scan | `consistent` |
| Compile and diff checks | Passed |

## Characterization Blockers

- `document_derivation_tree.py` renderer and `document_derivation_response.py`
  validators are large serialized-output boundaries. Splitting them requires a
  frozen whole-document byte/schema corpus and a dedicated owner.
- `promotion_policy.py` and `high_level_contracts.py` contain high-complexity
  claim-boundary logic. Refactoring them without a reviewed semantic fixture
  could change promotion or abstention status.
- The large document renderer and claim-boundary validators remain
  characterized blockers. The backend cycle itself is closed in Phase 04 and
  the import graph now reports zero cycles.

These blockers are recorded rather than hidden by changing thresholds or
moving imports wholesale.
