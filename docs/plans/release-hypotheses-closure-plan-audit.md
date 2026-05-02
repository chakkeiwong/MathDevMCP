# Release hypotheses closure plan audit

## Audit Posture

I reviewed `docs/plans/release-hypotheses-closure-execution-plan.md` as a
second developer focused on preventing release overclaiming, secret leakage,
CI fragility, and hidden backend assumptions.

## Verdict

Approved with constraints. The plan correctly separates public/base publication
readiness from strict internal evidence and turns the remaining hypotheses into
commands. It should proceed if the constraints below are followed.

## Required Constraints

1. Do not push, merge, tag, or publish from this pass. Publication can be
   tested as a local invariant over a clean committed tree, but remote release
   mechanics remain a human/release-manager action.

2. Do not treat the absence of `mathdevmcp-backends` as a product failure if
   local provisioning is blocked by external environment or network limits.
   The canonical backend hypothesis is closed only when that env validates; a
   fallback env such as `mathdev-lean` may support strict local evidence but
   must not be described as canonical closure.

3. Public CI must not require private corpus secrets, backend conda envs, or
   cached Lean toolchains. The public hypothesis step should run without those
   inputs and strict checks should be opt-in.

4. Private manifest paths and private source paths must remain outside git.
   Reset memo summaries may mention external `/tmp` evidence and redacted
   output, but no generated manifest JSON or source corpus should be staged.

5. Evidence-boundary checks must be conservative. They should prevent docs from
   saying full release readiness proves arbitrary mathematics, while preserving
   the valid statement that deterministic backend evidence can certify a scoped
   claim.

6. Final readiness after commit must be checked on the amended final commit,
   because the reset memo addendum changes the hash.

## Additional Suggested Checks

- Run `git diff --check` after each editing phase.
- Run `git status --short --branch` after every private-corpus command.
- Include tests that prove public hypothesis checks pass without private
  secrets.
- Include tests that prove strict canonical checks fail when
  `MATHDEVMCP_BACKEND_CONDA_ENV` is not `mathdevmcp-backends`.
- Scan committed generated evidence for private path leaks before committing.

## Audit Conclusion

Proceed. If canonical backend provisioning requires external approval or fails
because of network/environment constraints, record the exact result and
continue only if the public/base and non-canonical strict full gates still pass.
