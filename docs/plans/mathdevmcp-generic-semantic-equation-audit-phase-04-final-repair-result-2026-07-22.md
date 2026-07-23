# Phase 04 Final Repair Result

Date: 2026-07-22

Status: implemented; pending independent re-review.

## Trigger

The final independent re-review returned `REVISE` and reproduced two
high-severity fail-open cases. The Phase 4 stop condition therefore prevented
the same-paper replay from launching.

1. A specifically identified ownership endpoint could pair with an endpoint
   whose object identity was unresolved, producing a false ownership tension.
2. Return dates outside `t`, `t-1`, and `t+1` were partially matched, so
   `t-2` and `t+2` could be truncated to `t` and reported as no tension.

## Repairs

1. Object compatibility no longer treats missing identity as affirmative
   evidence when either endpoint has a specific identity. Specific endpoints
   pair only when both carry an intersecting specific identity. Ownership
   extraction also recognizes `another <object>` as a distinct candidate
   identity. An unmatched endpoint still emits bounded abstention diagnostics;
   it does not emit a semantic tension.
2. Return tokens now parse an exact arbitrary integer shift. The token boundary
   rejects trailing alphanumeric, sign, decimal, brace, underscore, or other
   date-continuation fragments, and both movement and normalization-time
   extraction preserve the complete signed integer shift. Thus matching `t-2`
   movements compare as `t-2`, not `t`; malformed OCR-like forms such as
   `t-2x`, `t-1.5`, `t--2`, and incomplete shifts abstain rather than matching
   a valid prefix.

## Regression Evidence

New adversarial tests establish that:

- a team-specific level endpoint does not pair with `another division` and
  emits no `ownership_scope_mismatch` finding;
- a matching `t-2` normalization and movement preserve `t-2` and nominate no
  timing tension;
- eight malformed date-suffix forms cannot backtrack to a shorter valid return
  token and instead emit a movement-unresolved abstention;
- prior unresolved-scope cases retain explicit abstention diagnostics.

Checks on the repaired state:

- focused semantic and audit suite: `84 passed`;
- full relevant suite: `162 passed`;
- `PYTHONPATH=src python -m compileall -q src tests`: passed;
- `git diff --check`: passed;
- production, semantic tests, and the frozen semantic corpus contain no Boehl
  name, target equation labels, or named answer-key issue phrases.

## Claim Boundary

These repairs establish only the tested parser-semantic engineering behavior.
They do not authenticate PDF transcription, prove a displayed relation, show
general recall, or establish that the same-paper score will improve. The
replay remains stopped until an independent reviewer probes this exact state
and finds no unresolved high-severity evidence-integrity issue.
