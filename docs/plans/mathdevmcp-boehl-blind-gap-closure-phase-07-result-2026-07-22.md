# Phase 07 Result: Instruction-Compliant Tuned Replay

Status: passed with a recorded shared-workspace artifact integrity warning.

The fresh session used only the two PDFs and the public CLI, with matching
input digests. It reported 13 findings: 1 arithmetic `confirmed_defect` and 12
`supported_tension` records. The same six obligation classes remain
`not_checkable`. The fresh report independently states that no comparator,
answer key, prior review, or plan was accessed.

The CLI initially reported artifact digest
`44623c704f609eabdd82ddec1d621b971678f0523f0d38a2d61b432912946dbb`; a
concurrent shared-workspace rewrite left the same-size artifact at digest
`7263c1114de840e8a9316314ac5321efdd212212f2037e70ad1486f66d322163`.
Both are preserved in the replay manifest; the latter is the frozen on-disk
artifact used for post-hoc comparison. This is a reproducibility limitation,
not a scientific result.

After the independent repair loop, the valid final replay is Fresh R5:
`docs/reviews/boehl-qe-tuned-replay-2026-07-22/fresh-r5/`. It used the two PDFs
and exact public command only, reported 11 source-bound supported tensions,
zero confirmed defects, zero claim-IR validation errors, and self-reported no
access to prior material. Its artifact SHA-256 is
`7bff5934a88fd8cda0e0f3b4f48a3a1edf89c7397b500fb93ff73bebd812a244`.

Handoff: comparison is descriptive only and must not be called a blind
holdout.
