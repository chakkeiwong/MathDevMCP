# Boehl QE Tuned Replay: Post-Hoc Comparison

Date: 2026-07-22

## Protocol

The replay report and on-disk audit artifact existed before the prior
seven-item comparison was opened. This is an instruction-compliant tuned
same-paper replay, not a blind holdout, because the implementation program used
the prior issue classes. Input PDF digests match the baseline. Same-paper
differences are descriptive only.

## Committee-Inventory Comparison

| Issue | Tuned replay outcome | Classification |
| --- | --- | --- |
| I01: Appendix C is not self-executing | external-model-closure findings | exact topic |
| I02: C.52--C.68 timing/object separation, especially C.59/C.62 | generic level/linearization candidates | partial |
| I03: C.71 zero steady state requires absolute deviation | zero/log boundary findings | exact topic |
| I04: C.75 deposit-return sign/timing tension | no direct C.75 finding | missed |
| I05: C.77 uses bank-held, not total, assets | entrant asset-domain finding | partial |
| I06: C.79 sign/coefficient conflict with C.47 | level-return linearization tension | partial |
| I07: equations after C.96 are outside the PDF | external-model-closure findings | exact topic |

Score: **3 exact, 3 partial, 1 missed**, unchanged from the prior fresh run.
The replay therefore does not demonstrate improved issue-level recall on these
seven items.

## What Improved

The same finding surface now carries a stronger engineering substrate:

- page/source evidence packets and typed claim IR;
- explicit inferred-relation status and evidence chains;
- source-package discovery and typed DynareMCP routing;
- bounded symbolic formalization with fail-closed authentication;
- explicit `unauthenticated_transcription` diagnostics for parser-only PDF
  equation candidates;
- artifact-backed compact/detail paging and tested MCP exposure.

These improvements close evidence-integrity, routing, and false-promotion
gaps. They narrow the route to checking C.75/C.79 but do not themselves solve
those scientific obligations.

## Remaining Gaps

1. C.75 remains missed. Robust recovery of the SDF normalization, date indices,
   and deposit-return sign from PDF text is still absent.
2. C.79 remains only a supported tension. A source-authenticated or
   independently verified transcription and explicit level-to-linearized
   derivation are required for a stronger verdict.
3. C.77 remains partial: the ownership domain is surfaced, but no complete
   source-bound correction is derived.
4. C.59/C.62 timing and installed/effective-capital distinctions remain partial.
5. Six obligation families remain not checkable without structured source,
   model code/YAML, data, or a certifying backend.
6. PDF extraction still has one usable parser, low confidence, and no faithful
   structured equation recovery or authenticated crops.
7. Adjacent source discovery does not fetch or authenticate remote author
   packages or errata.
8. The replay artifact was concurrently rewritten in the shared workspace;
   both digests are recorded, but the first-run bytes were not retained.
9. The fixture corpus is visible and synthetic. Generalization, precision, and
   recall require a separately sealed cross-domain corpus.

## Verdict

The engineering repair succeeded at rigorous claim boundaries and reproducible
abstention, not at scientific recall. The exact/partial/missed score is
unchanged. The next root-cause program should focus on authenticated equation
transcription and explicit semantic derivation from structured author sources,
then validate on a new sealed cross-domain corpus rather than tuning these two
PDFs again.

This comparison does not certify the paper, code, posterior, likelihood, ZLB
solution, causal claims, or product-wide detection performance.
