# MathDevMCP Clean Restart Memo

Date: 2026-07-23
Branch: `main`

## Mission

MathDevMCP is an exploratory, high-standard, rigorous, agent-facing
mathematical development system. It searches broadly across candidate
assumptions, derivations, counterexamples, formalizations, and external-tool
routes while remaining rigorous at the evidence and claim boundary.

## State Frozen For Restart

The applied-mathematics semantic audit work is implemented in the current
working tree and has passed the latest relevant checks:

- focused semantic and audit suite: `84 passed`;
- selected public/integration suite: `162 passed`;
- `PYTHONPATH=src python -m compileall -q src tests`: passed;
- `git diff --check`: passed;
- source-specific leakage scan: no Boehl labels, names, or answer-key phrases
  in production code, semantic tests, or the frozen fixture corpus.

The unfiltered repository command `PYTHONPATH=src pytest -q` did not produce a
pytest summary in this environment: it exited during collection/execution at
roughly 7-8% after reporting passing tests. This is recorded as an incomplete
full-suite diagnostic, not as a pass or a failure classification.

The latest repair addresses two previously reproduced fail-open paths:

1. specifically identified and unresolved ownership objects no longer pair;
2. valid integer timing shifts are preserved, while malformed or truncated
   OCR-like date suffixes abstain instead of matching a shorter prefix.

The latest implementation digests are recorded in the phase repair result and
must be recomputed before a future replay.

At this reset point they are:

```text
6dc502eec8ea3e2e729658c8449b0fc7739b5869daa297877e8f502f97ac3fee  src/mathdevmcp/applied_math_semantics.py
021dde77caec00e21c2626be549521efccdf130046a39adc3e9dce0e73b8d2bd  src/mathdevmcp/applied_math_audit.py
af941c83ca73ad07d8b5a4855b38c654ee37fe866b66c778eb12521ad7a3b93c  tests/test_applied_math_semantics.py
06557e5118b9570881e216ce0251310da2c186d75da1dade98b0e0c704897f63  tests/test_applied_math_audit.py
```

The final independent review has not yet passed. Its last result was
`REVISE`; the malformed-date prefix-matching repair above was made afterward.
The same-paper two-PDF replay therefore remains blocked pending a new
independent review of the exact current digests.

## Evidence And Claim Boundary

Tracked durable records include authored phase plans and close records,
independent review conclusions, fixture corpora and scorecards, run manifests,
replay reports, post-hoc comparisons, and final gap reports. These are retained
because they support promotion, reproducibility, or an explicit scientific or
engineering claim.

Non-authoritative generated bulk payloads are intentionally not tracked. They
include local runtime workspaces, caches, build/package products,
document-generation trees, redundant raw parser extraction payloads, detailed
intermediate audit JSON, and replay CLI output. Their paths are ignored in
`.gitignore`; a narrow allowlist retains authoritative machine evidence that is
directly bound by durable manifests, scorecards, or promoted claims.

No generated artifact is treated as a mathematical proof. Parser-derived PDF
equations remain non-certifying, semantic findings remain diagnostic tensions,
and the replay must not be described as a blind holdout or as evidence of
general recall.

## Restart Entry Procedure

1. Verify `git status --short` is empty and `git status --ignored --short`
   shows only expected generated paths.
2. Recompute source/test digests and rerun the focused and selected integration
   suites before changing code.
3. Obtain a fresh independent review of the latest semantic implementation,
   explicitly probing malformed date suffixes, object identity ambiguity,
   canonical artifact tampering, and parser-only promotion boundaries.
4. If that review passes or leaves only documented low/medium residuals,
   provision a new content-bounded replay workspace, freeze its allowlist and
   digests, and run exactly one fresh-agent two-PDF replay.
5. Freeze the replay report, manifest, and post-hoc comparison before opening
   any answer inventory. Record remaining gaps without upgrading descriptive
   replay results into scientific correctness or general recall claims.

## Hygiene Rule

Every repository path must be either tracked or intentionally ignored. New
generated outputs must be placed under an already ignored runtime/output path;
new durable evidence must be a concise authored record under the tracked
plans/reviews/tests/docs surfaces.
