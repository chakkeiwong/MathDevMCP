# Audit of final release productization execution plan

Date: 2026-04-29

Audited plan:

```text
docs/plans/final-release-productization-execution-plan.md
```

## Review stance

This audit treats the plan as if it was submitted by another developer for a
release-critical change. The focus is whether the plan can be executed without
human intervention, whether it preserves privacy and release honesty, and
whether it leaves enough verification evidence for an industrial internal
release.

## Strengths

- The plan starts from the actual current blocker:
  `private_corpus_manifest_required`.
- It correctly refuses to close the private corpus gate by weakening the release
  policy.
- It separates base, backend, LaTeXML, private-corpus, and full release profiles.
- It keeps LeanDojo isolated from the active Python environment.
- It requires actual program output in the final report instead of invented
  examples.
- It identifies the high-risk implementation modules by current size and
  release impact.
- It includes phase-level audit, tidy-up, and reset-memo updates.
- It explicitly says private paths and private documents must not be committed.

## Issues found before execution

1. **Real private data may be unavailable to the executing agent.**

   The plan says the correct final release gate should use real private,
   externally sanitized, or approved internal sample documents. In this
   workspace, no such private corpus is discoverable. To keep execution
   autonomous, the implementation must create an external sanitized corpus
   outside git, validate the gate against that corpus, and label the evidence
   honestly as sanitized external release evidence. The release report must not
   imply that unredacted department data was reviewed unless a real manifest is
   supplied later.

2. **The requested 80 to 100 page report is large enough to create quality risk.**

   The plan has a good structure, but executing it mechanically could produce
   padding. The implementation must prioritize dense, useful documentation:
   system behavior, commands, outputs, case studies, contracts, and limitations.
   Page count should be a constraint, not a license for filler.

3. **Refactor scope could become too broad.**

   Splitting every large module in one pass risks regressions. The implementation
   should perform conservative, behavior-preserving refactors focused on release
   corpus validation, release evidence generation, and documentation support.
   Larger benchmark/CLI decomposition should be done only when tests remain
   stable and the change materially improves maintainability.

4. **Commenting requirement could be over-applied.**

   "Detailed comments" should mean policy, invariants, and public contracts.
   The implementation should avoid line-by-line comments that make maintenance
   harder.

5. **Generated evidence could accidentally leak local paths.**

   Evidence snippets for private-corpus validation must be redacted and scanned
   before commit. Generated report snippets should avoid absolute private paths.

6. **`docs/proposal.tex` compatibility must be handled carefully.**

   Removing it outright may break build habits. Keeping a small compatibility
   wrapper that delegates to the release report is safer unless every reference
   is updated.

## Required execution adjustments

- Create a sanitized external corpus under `/tmp/mathdevmcp-private-corpus-*`
  for autonomous validation.
- Store the populated manifest outside git.
- Add tests that use `tmp_path` to prove full-profile success with a private
  manifest without committing private data.
- Add a release-evidence generator that writes only safe snippets under
  `docs/generated/release_report/`.
- Keep `.release-evidence/` and private manifests ignored.
- Convert `docs/proposal.tex` to a compatibility wrapper and create
  `docs/mathdevmcp-release-report.tex` as the primary document.
- Add or expand maintainer documentation and comments around policy boundaries,
  not every line of code.
- Audit with `rg` for stale proposal/scaffold language and private path leaks.

## Audit conclusion

The plan is executable and release-appropriate if the implementation treats the
private-corpus closure as sanitized external evidence when real private data is
not available, keeps refactors conservative, and verifies the final report with
actual commands and page count. No release gate should be weakened.
