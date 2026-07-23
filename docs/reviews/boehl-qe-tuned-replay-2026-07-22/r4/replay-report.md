# Boehl QE Tuned Replay R4 Report

## Scope

R4 is the valid post-red-team instruction-compliant tuned replay. It is not a
blind holdout. The two input digests match the baseline and no code or data was
supplied. ResearchAssistant again provided only low-confidence `pdftotext`
output requiring manual review.

## Result

The public CLI emitted 11 findings, all `supported_tension`:

- the extracted arithmetic `500 x 200 = 10,000`, now correctly vetoed from
  `confirmed_defect` by `unauthenticated_transcription`;
- external equation/model closure;
- confidence-interval versus credible-set terminology;
- the zero-steady-state/log-deviation boundary;
- five inferred level/linearization candidates.

Every finding has at least one bound source packet and the claim IR has no
validation errors. No parser-only equation or arithmetic statement was
promoted to a confirmed mathematical defect.

Two generic relation findings from the earlier tuned replay disappeared after
removal of paper-specific production tokens: the return/sign candidate and
entrant ownership-domain candidate. This is a recall regression relative to
the same-paper inventory but a necessary removal of answer-shaped rules.

## Artifact

- JSON: `audit-bcec3e67225a0fe9d8e24c2fcaa671a2.json`
- SHA-256: `68bceb514b8942ae3e19479c7d75371891ac9da91fc1956866c567aa39635ca7`
- Bytes: `2615518`

## Non-Claims

R4 does not establish general recall, source-faithful equation transcription,
mathematical correctness, code equivalence, posterior validity, causal
validity, publication readiness, or production readiness.
