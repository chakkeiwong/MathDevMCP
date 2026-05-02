# Release profile analysis completion plan audit

## Audit stance

This audit reviews
`docs/plans/release-profile-analysis-completion-execution-plan.md` as another
developer's plan. The focus is whether the proposed profile-analysis pass gives
maintainers a complete release interpretation without weakening the existing
profile gates.

## Overall assessment

Approved. A cross-profile analysis report is the right missing artifact. The
previous pass made individual profile results correct; this pass should make
the collection of profile results easy to interpret and repeat.

The main risk is accidentally creating a second release policy engine. The new
analysis must summarize `release_readiness_report(...)` outputs, not duplicate
or override their blocker logic.

## Required constraints

1. Preserve strict profile semantics.
   A blocked `backend`, `latexml`, `private-corpus`, or `full` profile must
   remain blocked in the analysis.

2. Preserve raw evidence.
   The analysis can include highlights, but individual readiness reports must
   keep full `doctor_summary`, parser, governance, and corpus evidence.

3. Avoid private path leakage.
   Analysis highlights and next actions should not echo absolute private
   manifest paths. If paths are needed, use placeholders or rely on the
   redacted release-corpus validation.

4. Keep overall status conservative.
   If public/base are ready and strict profiles are blocked, the analysis can
   be `ready_with_caveats`; it should not say `ready` for the whole release
   universe unless strict profiles also pass or are explicitly out of scope.

5. Keep tests environment-aware.
   Backend env and private corpus availability vary by machine. Tests should
   assert classification shape and blockers when absent, not require optional
   external setup to exist.

## Phase audit

### Phase 1

Proceed. The library contract should be compact and stable. Prefer helper
functions for interpretation and next actions so docs and tests can reason
about strings.

### Phase 2

Proceed. CLI/MCP access is useful because release review often happens through
agents. The MCP handler should be a thin facade only.

### Phase 3

Proceed. Documentation should make `release-profile-analysis` the recommended
first command for release gap discussions.

### Phase 4

Proceed. Final checks must include both profile analysis and the existing
profile-specific readiness gates.

## Audit conclusion

No missing blockers were found. Execute all phases, but keep the analysis as a
summary layer over existing readiness reports rather than a new authority.
