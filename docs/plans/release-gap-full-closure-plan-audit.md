# Release gap full-closure plan audit

## Audit Posture

I reviewed `docs/plans/release-gap-full-closure-execution-plan.md` as a second
developer whose job is to prevent release overclaiming, accidental private-data
exposure, hidden dependency mutation, and profile-policy drift.

## Verdict

Approved with constraints. The plan targets the real live gaps shown by
`release-profile-analysis` and keeps public/base readiness separate from strict
full/internal readiness. It should proceed if the constraints below are
followed.

## Findings and Required Constraints

1. The plan must not equate full-profile readiness with mathematical proof.
   `release-readiness --profile full` can certify that release evidence exists
   for configured backends, corpus gates, and public checks. It does not certify
   arbitrary mathematics unless a deterministic backend certificate is present
   in a separate proof-audit contract.

2. Backend dependency-conflict handling must be narrow.
   It is valid to stop active application-env `magic-pdf`/`pydantic` conflicts
   from affecting backend/full readiness when a configured backend Python
   successfully imports LeanDojo. It is not valid to remove those conflicts from
   `doctor_summary`, public diagnostics, or cases where backend Python is
   missing.

3. Lean toolchain caveats must stay strict.
   Selecting the cached `leanprover/lean4:v4.30.0-rc2` toolchain is acceptable
   for local evidence, but if Lean is unavailable under the selected backend
   subprocess environment, backend/full must still show that caveat.

4. Private-corpus evidence must remain outside git.
   The generated `/tmp` corpus and populated manifest must never be staged. The
   reset memo may record the external path and redacted summary, but no private
   source contents or generated manifest JSON should be committed.

5. `validate_backend_install.sh` should not be loosened silently.
   If the script changes, it must continue to require the release-critical
   backend evidence. It may classify symbolic extras such as backend-env `sympy`
   as optional only if `release-readiness --profile backend` does not require
   them.

6. The full-profile command should be run with all strict environment variables
   in one shell:
   `MATHDEVMCP_BACKEND_CONDA_ENV`, `MATHDEVMCP_LEAN_TOOLCHAIN`,
   `MATHDEVMCP_REQUIRE_LATEXML`, and `MATHDEVMCP_PRIVATE_CORPUS_MANIFEST`.
   Passing individual profiles separately is not enough to claim full readiness.

7. The final memo must distinguish release blockers from publication actions.
   If profiles become ready, remaining work is push/merge/tag/publish and
   revalidation after publication, not another hidden implementation blocker.

## Additional Suggested Checks

- Run `git diff --check` after every editing phase.
- Run `git status --short --branch` after private-corpus generation to confirm
  external artifacts did not appear in git.
- Include one test that stubs a configured backend import as successful while
  active doctor conflicts exist, proving the intended caveat separation.
- Include one final post-commit cross-profile report so the committed hash is
  visible in release evidence.

## Audit Conclusion

Proceed. If the full profile remains `not_ready` after Phase 3 with all strict
evidence configured, stop and ask for direction unless the remaining issue is a
small code/reporting bug already covered by the plan.
