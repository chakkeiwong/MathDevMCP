# Public release preflight gap-closure plan audit

## Audit stance

This audit treats
`docs/plans/public-release-preflight-gap-closure-execution-plan.md` as another
developer's plan. The review focuses on whether the plan closes real
pre-release ambiguity without hiding material evidence.

## Overall assessment

Approved. The plan is justified because the current product surface checks pass
cleanly, while the broader readiness report still mixes public-release
readiness with optional strict-profile environment state. That distinction is
important before publishing again.

The main risk is over-normalizing caveats away. The implementation must keep
raw doctor evidence in the report and must preserve strict-profile blockers.

## Required constraints

1. Do not remove `doctor_summary` evidence.
   A public/base profile may ignore an optional caveat for recommendation
   purposes, but the underlying capability state should remain inspectable.

2. Do not weaken strict profiles.
   `backend`, `latexml`, `private-corpus`, and `full` must continue to block
   when their declared required evidence is absent.

3. Do not mutate local tool state.
   Adding `.serena/` to `.gitignore` is acceptable. Editing or deleting the
   `.serena/` directory is not.

4. Do not claim mathematical verification.
   Release-readiness is operational/product evidence, not a proof certificate.

5. Do not make network-dependent fixes mandatory.
   Lean toolchain download failures should remain explicit evidence, but a
   network-restricted public/base environment should not block public release
   if no Lean profile is being claimed.

## Phase audit

### Phase 1

Proceed. Ignoring a local tool cache is release hygiene, provided the directory
is not staged and not modified.

### Phase 2

Proceed with tests. The plan should prefer a helper that decides whether a
caveat applies to the selected profile so future caveats do not become another
flat list.

### Phase 3

Proceed. Documentation should explain what remains for strict/full release,
not expand the release scope.

### Phase 4

Proceed. Final verification should include both public surface and strict
profile checks so regressions are visible.

## Audit conclusion

No missing blockers were found. The plan is safe to execute if it preserves raw
evidence, strict-profile blocking behavior, and the diagnostic-only boundary.
