# Industry-DSGE Pilot Regression Measurement Plan Review

Date: 2026-07-18

Reviewed plan:
`docs/plans/mathdevmcp-industry-dsge-pilot-regression-measurement-plan-2026-07-18.md`

Verdict: `PASS_AFTER_REVISION`

## Review Findings

### Resolved material findings

1. The first concept depended on the external DynareMCP source. That would have
   made later source edits silently change the baseline. The reviewed plan now
   requires minimal repo-local derived fixtures.
2. A single repaired fixture could not distinguish context awareness from an
   unsafe rule that suppresses every inverse finding. A matched fixture without
   the spectral-radius condition is now mandatory.
3. Passing tests that assert only current defects would encode regressions as
   desired behavior. The reviewed design separates passing characterization
   tests from strict expected-failure acceptance tests.
4. Exact report byte counts are sensitive to backend provenance and fixture
   length. Exact external counts are retained as comparison evidence, while
   local tests use semantic assertions and a declared 200-line interface budget.
5. Helper-level tests alone would not reproduce the downstream workflow. The
   reviewed plan requires an actual high-level focused rigor audit and uses
   helper tests only for localization and wording root causes.
6. Closure without cited source spans would be difficult to audit, and status
   correction alone would not test the missing repair loop. The acceptance
   layer now requires exact context support and a non-certifying candidate
   exposition patch for the matched negative fixture.
7. Unrestricted XFAIL could hide parser crashes or test defects. Every
   acceptance marker is now strict and limited to `AssertionError`.

### Boundary review

- The plan does not edit production code or the downstream dossier.
- It does not classify general readability, motivation, or pedagogy.
- It preserves diagnostic-versus-proof boundaries.
- It does not require Claude or another external reviewer because this is a
  Tier-1 measurement harness and does not change a mathematical/product claim.
- It preserves the concurrently modified worktree by using new, uniquely named
  fixture, test, plan, review, and result paths.

### Feasibility review

The current public Python workflow exposes enough data to reproduce the main
symptoms. Some desired future fields, such as stable semantic issue IDs and
context-closure spans, do not exist. Strict-XFAIL tests may therefore assert
their absence or desired semantic projection without inventing production
implementations.

## Approval

The plan is ready to execute. A valid completion requires both a green
characterization run and an explicit XFAIL inventory. A wholly green run with
no XFAIL targets would not measure the planned improvement boundary.
