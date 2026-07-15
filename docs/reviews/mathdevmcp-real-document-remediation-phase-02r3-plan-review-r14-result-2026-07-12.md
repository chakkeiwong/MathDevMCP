# Phase 02R3 Timeout-Policy Recovery Plan Review R14 Result

Date: 2026-07-12

Reviewer: fresh independent Codex read-only reviewer

## Findings

### 1. Material: the timeout patch broadens the reviewed hypothesis from source calls to version calls

The plan defines the change as a LaTeXML source-call timeout hypothesis and
evaluates timeout failure over source receipts. However, the sole patch replaces
`/parser_fidelity_profile/executables/latexml/timeout_seconds`. The inherited
runner consumes that same field for both version and source invocations. The
effective profile therefore silently raises the LaTeXML version-call ceiling
from 60 to 180 seconds too.

The overlay must either introduce distinct version/source timeout fields while
preserving the reviewed version timeout or explicitly audit and authorize 180
seconds for both call classes and update all evidence-contract language.

### 2. Material: the bootstrap does not enforce the entry-only P02R2 predecessor namespace

The plan requires the P02R2 entry manifests and exact entry-only namespace, with
live P02R2 `rr01` absent. The bootstrap checks the contents of the P02R2 entry
directory but never requires the parent P02R2 phase root to contain exactly
`entry`. Its protected-tree scan would preserve an unexpected result-round tree
rather than reject it. The bootstrap must no-follow validate the complete P02R2
phase-root shape as exactly one `entry` directory before allocation.

## Residual Implementation Risks

After repairing the plan/bootstrap, implementation must still replace
operational P02R2 constants inside the reviewed allowlist, reconstruct P02R3
over the sealed P02R2 profile, remove limitation-only states from the
`parser_veto` reducer while retaining action failure for any source timeout,
and prove the distinction with focused mutations.

The nine-state partition itself is closed and preserves integrity failures and
independently reconstructed contradictions as vetoes. Correctly classified
limitation-only states remain non-promotional. The eleven listed overlay paths
are unique and exact, but they do not cure the two scope defects above.

Reviewed P02R3 plan SHA-256: `3867c8f93ee4c9f62009944c2c5f9147af99972bf5f6bdfa08f2ad1c70ed4b79`
Reviewed P02R3 oracle SHA-256: `8ac9e7b2a0f561545f5ab3b7aeacdd66faae3bf07f4024e7d2358e6e891ef3de`
Reviewed P02R3 bootstrap SHA-256: `8e1f9d126a758601027af69f64d7568f68f09572930514063cb47e15b926bee4`
Reviewed P02R2 plan SHA-256: `6ed09b8c1c177c6e76b9547ae350454907047c66c5f62b91c42800bd2c2d1a71`
Reviewed P02R2 oracle SHA-256: `92d75deb5fc30311a46c4d4f077939c594e667269a96ca56de8bf3be928d5562`
Reviewed P02R2 entry SHA-256: `8d74abcab7b3735252e8d0f58b0b583dcf7da6b7e9d8557891087f97d6217974`
Reviewed timeout blocker SHA-256: `d88e3e33eaaa92f980278478861ac31b5ce016f9367b800e45e7b322078beaa9`
Reviewed timeout adjudication SHA-256: `250537ea349798e45c8fed62e551f9cb2917f8531d1f3097b449705c5d1b1d41`

VERDICT: REVISE
