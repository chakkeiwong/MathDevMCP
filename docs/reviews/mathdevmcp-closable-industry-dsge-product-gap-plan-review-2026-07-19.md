# Review of the Closable Industry-DSGE Product-Gap Program

Date: 2026-07-19
Verdict: `PASS_AFTER_REVISION`

## Review Method

The plan was reviewed against the Industry-DSGE pilot memo, the current rigor
library/CLI/facade/FastMCP surfaces, the academic-governance reset, the
external-tool-first policy, and the repository's scientific evidence rules. The
review explicitly checked baselines, proxy metrics, stop conditions, hidden
defaults, environment mismatch, source identity, claim boundaries, and whether
the proposed artifacts would answer the stated engineering question.

## Material Findings and Repairs

1. **The original exact-digest comparison rule was wrong.** A repaired TeX file
   necessarily has a new digest, so requiring equality would reject every real
   before/after comparison. The plan now requires the same canonical path and
   normalized selected-label scope, preserves both digests, and treats a digest
   change as expected lineage evidence rather than a mismatch.
2. **Profile equality was an invalid semantic requirement.** `actionable` and
   `forensic` are views over the same canonical issue ledger. The plan now
   compares canonical issues independently of presentation profile.
3. **Issue IDs must not contain the source digest.** Stable IDs remain
   `label/family`; report lineage carries digests separately. Otherwise every
   source edit would make all issues appear `new`.
4. **A new page-token protocol was disproportionate.** Exact persisted-report
   SHA-256 plus a closed collection allowlist is sufficient for local academic
   artifact retrieval. The plan now reuses that existing authorization model.
5. **Role precedence was under-specified.** A display may be both a definition
   and a conditional identity. The revision requires deterministic primary
   routing while preserving all detected roles/evidence, with ambiguity falling
   back to `unknown` rather than silently entering a proof route.
6. **Patch expansion could become generic prose generation.** The revision
   limits patches to a named allowlist, retains `human_review`, and forbids
   source-specific truth or automatic TeX application.

## Residual Risks Accepted for This Program

- Heuristic role cues can be wrong. Fixture tests establish deterministic
  behavior only, not precision or recall.
- Stable IDs will treat renamed labels or reclassified issue families as new.
  The comparison must report unmatched prior/current records visibly.
- User metadata can improve routing but cannot establish source truth or clear a
  document-context obligation.
- Byte count and issue count are descriptive. They cannot certify usefulness,
  readability, or mathematical correctness.

## Pre-Execution Decision

The revised plan has a correct baseline, explicit continuation vetoes, bounded
public behavior, negative tests, and artifacts capable of answering its stated
engineering question. No material unexamined default remains. Execution is
authorized within the plan's non-certifying scope.
