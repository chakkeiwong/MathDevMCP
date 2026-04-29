# Audit: industrial release caveat-closure execution plan

## Audit stance

This audit is written as a second developer reviewing `docs/plans/industrial-release-caveat-closure-execution-plan.md` before implementation. The plan is approved for execution, but only if the implementation preserves profile-specific claims and does not silently promote optional evidence into base release requirements.

## Strengths

- The plan starts from the actual current release state: `ready_with_caveats`, no blockers, LaTeXML unavailable, backend LeanDojo isolated, private manifest not configured.
- The profile split is the right abstraction. `base`, `backend`, `latexml`, `private-corpus`, and `full` are concrete enough for colleagues and CI to understand.
- The safety invariant is explicit and correctly protects against treating parser, AST, numeric, or LeanDojo traces as mathematical proof.
- The private-corpus phase correctly treats privacy as a release requirement, not an afterthought.
- The evidence-matrix phase addresses a real operational problem: skipped optional checks must be visible rather than confused with passes.

## Required clarifications before/during implementation

1. **Backward compatibility of `release-readiness`.**
   Existing callers and tests expect `release_readiness_report(root)` and `python -m mathdevmcp.cli release-readiness --root ...` to work without a profile. The implementation should default to `base` and preserve the existing contract name unless there is a deliberate schema version bump.

2. **Backend profile must not depend on shell parsing.**
   Any helper for `conda run` must avoid constructing a single command string. Use argv arrays in Python and shell `"$@"` in scripts.

3. **LaTeXML installation cannot be assumed.**
   The plan allows installing LaTeXML, but the implementation should not block if OS package installation requires privileges or network. In that case, strict profiles should fail with exact instructions and base profile should remain releasable with a caveat.

4. **Private corpus validation needs two levels.**
   Manifest-shape validation and parser/content validation should be distinguishable. A missing private manifest is a blocker only for `private-corpus` and `full`, not for `base`.

5. **Public fixture expansion should be meaningful but bounded.**
   Adding too many fixtures can cause noisy benchmark churn. Each new release-gated fixture needs an expected label and an abstention/negative case.

6. **Parser robustness metrics must remain evidence metrics.**
   Per-file counts, duplicate labels, include status, and macro summaries are useful for routing. They must not be consumed as proof certificates.

7. **Generated artifacts must stay out of git.**
   Evidence bundles, LaTeXML scratch files, conda envs, Lean build outputs, and private manifests with real paths must remain ignored or outside the repository.

8. **Final status should be profile-specific.**
   It is acceptable for `base` and `backend` to pass while `latexml`, `private-corpus`, and `full` fail because optional tools/data are not configured. The reset memo must record that as a truthful release outcome rather than an implementation defect.

## Phase-by-phase audit notes

### Phase 1

Approved. Add profile fields without breaking existing report consumers. Tests should assert default profile behavior and profile-specific blocker/caveat differences.

### Phase 2

Approved with constraint: do not make LaTeXML mandatory in Python packaging or base release. Strict validation should fail when unavailable; optional validation should exit 0.

### Phase 3

Approved. The helper should preserve `MATHDEVMCP_LEAN_TOOLCHAIN` and `MATHDEVMCP_LEAN_PATH`. LeanDojo remains optional and cannot verify anything without final direct Lean checking.

### Phase 4

Approved. Strong privacy tests are required. Redaction should be tested on both manifest output and validation/evidence summaries.

### Phase 5

Approved if kept small and synthetic. Prefer a few compact fixtures that cover missing release domains over large document simulations.

### Phase 6

Approved. Parser report extensions should be additive and preserve existing fields.

### Phase 7

Approved. Documentation should include a profile matrix and "first 30 minutes" workflow. It must avoid claiming arbitrary theorem proving.

### Phase 8

Approved. Evidence collection should support profiles and report skipped optional gates explicitly.

### Phase 9

Approved. Final verification should include full pytest, release smoke, backend doctor, backend validation, LaTeXML optional validation, evidence collection, clean-install smoke when feasible, diff hygiene, commit, and post-commit readiness.

## Release decision expectation

The likely honest end state on this machine is:

```text
base: ready_with_caveats or ready depending on whether dirty worktree/LaTeXML caveat remains in base policy
backend: ready_with_caveats or ready if mathdevmcp-backends validates and LaTeXML remains optional
latexml: not_ready because LaTeXML is unavailable
private-corpus: not_ready because no private manifest is configured
full: not_ready because LaTeXML and private corpus are unavailable
```

That outcome is acceptable for this execution pass if the reports are explicit, tested, and documented.
