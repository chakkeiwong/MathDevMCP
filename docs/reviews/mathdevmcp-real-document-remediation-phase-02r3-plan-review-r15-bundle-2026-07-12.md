# Phase 02R3 Timeout-Policy Recovery Repair Review R15 Bundle

Date: 2026-07-12

Review mode: fresh independent Codex, read-only

## Scope

Review only the additive P02R3 recovery plan, compact overlay, and one-shot
entry bootstrap after the two material R14 findings were repaired. Do not edit
files, run specialist parsers, create the live P02R3 entry, or execute
governance.

## Review History

R14 returned `REVISE`. Its immutable result SHA-256 is
`604f0aae23065b2257a71eb7291770f69bb7cd9ed7486dccb97e8430fd7579d0`.
It found:

1. the shared `timeout_seconds` patch unintentionally raised the LaTeXML
   version-call ceiling as well as the source-call ceiling;
2. the bootstrap verified the P02R2 entry directory but did not require the
   complete P02R2 phase root to contain exactly `entry`.

The user authorized one additional repair-plan review round. R15 is that round.
Two later rounds remain reserved for independent result review and final-seal
audit.

## Reviewed Artifacts

- P02R3 plan:
  `docs/plans/mathdevmcp-real-document-remediation-phase-02r3-timeout-policy-recovery-subplan-2026-07-12.md`,
  SHA-256 `610567d9b21ace9e07588b08e65820d8afb857da850cf4c769ade5302989587c`.
- P02R3 oracle:
  `docs/plans/mathdevmcp-real-document-remediation-phase-02r3-timeout-policy-recovery-oracle-2026-07-12.json`,
  SHA-256 `eed11350e4c965f3346031683449df08352d8515c5dc8160e0d9014ad6ac5a9c`.
- P02R3 bootstrap:
  `docs/plans/p02r3_entry_bootstrap_20260712.py`,
  SHA-256 `8db6fe49d06891ad653c9ea55644b37a34548d735514791b408e932fb0c68790`.

## Bound Predecessors

- P02R2 plan SHA-256:
  `6ed09b8c1c177c6e76b9547ae350454907047c66c5f62b91c42800bd2c2d1a71`.
- P02R2 oracle SHA-256:
  `92d75deb5fc30311a46c4d4f077939c594e667269a96ca56de8bf3be928d5562`.
- P02R2 entry SHA-256:
  `8d74abcab7b3735252e8d0f58b0b583dcf7da6b7e9d8557891087f97d6217974`.
- Timeout blocker SHA-256:
  `d88e3e33eaaa92f980278478861ac31b5ce016f9367b800e45e7b322078beaa9`.
- Timeout adjudication SHA-256:
  `250537ea349798e45c8fed62e551f9cb2917f8531d1f3097b449705c5d1b1d41`.

## R14 Repair Summary

- The overlay replaces the complete inherited executable registry exactly once.
- Effective LaTeXML ceilings are version `60`, source `180` seconds.
- Effective Pandoc ceilings are version `30`, source `30` seconds.
- The ambiguous shared `timeout_seconds` key is absent from the effective
  executable registry.
- The bootstrap opens the P02R2 phase-root chain with `O_NOFOLLOW`, requires its
  child set to equal `{entry}`, opens `entry` with `O_NOFOLLOW`, and requires the
  exact four regular files.
- The review contract preserves R14 and its eight old bindings, permits exactly
  R15, binds R15 to the repaired bytes and R14 digest, and preserves two later
  review rounds for result/final gates.

## Local Pre-Review Evidence

- Strict JSON parse passed.
- Bootstrap compilation passed.
- Read-only effective-profile reconstruction produced LaTeXML `60/180` and
  Pandoc `30/30` version/source ceilings.
- All sealed P02R2 and R14 digests reopened exactly.
- Live P02R2 contains exactly `entry/` and its four sealed files.
- Live P02R3 evidence root is absent.
- Disposable full bootstrap succeeded and produced synthetic entry digest
  `0e70139bcede497dbd9d525de548477b2a882da5e17cbbd0c9a95dd0b68429fc`.
- A disposable unexpected P02R2 `result-rounds/` child was rejected at the
  parent-tree check before P02R3 allocation.
- Disposable timeout-blocker tamper and R15 binding tamper were rejected before
  P02R3 allocation.
- `git diff --check` passed.

Disposable artifacts are diagnostic only and are not formal evidence or pass
predecessors.

## Skeptical Review Questions

1. Do the repaired artifacts fully resolve both R14 findings without broadening
   any version-call timeout or weakening predecessor-tree closure?
2. Is whole-registry replacement an exact, implementable overlay with only the
   intended operational difference: LaTeXML source timeout `60` to `180`?
3. Does the plan still treat `180` as a target-specific hypothesis, keep
   timeout completion non-promotional, and fail the separate action gate for any
   timed-out version or source receipt?
4. Does the no-follow P02R2 parent/entry check reject every extra child,
   symlink, special file, missing file, or non-regular entry artifact before
   P02R3 allocation?
5. Is R14 history bound exactly, is R15 the sole agreeing repair review, and are
   the two remaining reviews protected for result and final-seal gates?
6. Does the veto partition still cover all nine capability states exactly once,
   preserve invocation/source/artifact integrity and independent contradiction
   vetoes, and keep limitation-only states non-promotional?
7. Are there stale shared-timeout consumers, schema validators, guard checks, or
   test assumptions that make the reviewed post-entry implementation infeasible
   within the inherited 23-path allowlist?
8. Identify any wrong baseline, proxy promotion, hidden default, unfair
   comparison, missing stop condition, stale context, environment mismatch, or
   artifact that would not answer the stated question.

## Required Output

Findings first, severity ordered, with file/line references. Distinguish plan
defects from anticipated post-entry implementation work. If a material plan,
oracle, or bootstrap defect remains, end `VERDICT: REVISE`; otherwise state no
material defect remains, list residual implementation risks, and end
`VERDICT: AGREE`.

Include each exact line once:

```text
Reviewed P02R3 plan SHA-256: `610567d9b21ace9e07588b08e65820d8afb857da850cf4c769ade5302989587c`
Reviewed P02R3 oracle SHA-256: `eed11350e4c965f3346031683449df08352d8515c5dc8160e0d9014ad6ac5a9c`
Reviewed P02R3 bootstrap SHA-256: `8db6fe49d06891ad653c9ea55644b37a34548d735514791b408e932fb0c68790`
Reviewed P02R3 R14 result SHA-256: `604f0aae23065b2257a71eb7291770f69bb7cd9ed7486dccb97e8430fd7579d0`
Reviewed P02R2 plan SHA-256: `6ed09b8c1c177c6e76b9547ae350454907047c66c5f62b91c42800bd2c2d1a71`
Reviewed P02R2 oracle SHA-256: `92d75deb5fc30311a46c4d4f077939c594e667269a96ca56de8bf3be928d5562`
Reviewed P02R2 entry SHA-256: `8d74abcab7b3735252e8d0f58b0b583dcf7da6b7e9d8557891087f97d6217974`
Reviewed timeout blocker SHA-256: `d88e3e33eaaa92f980278478861ac31b5ce016f9367b800e45e7b322078beaa9`
Reviewed timeout adjudication SHA-256: `250537ea349798e45c8fed62e551f9cb2917f8531d1f3097b449705c5d1b1d41`
```

End with exactly `VERDICT: AGREE` or `VERDICT: REVISE`.
