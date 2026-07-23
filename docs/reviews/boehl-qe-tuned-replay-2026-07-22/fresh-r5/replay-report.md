# Fresh R5 Replay Report

## Run identity

This was the specified tuned replay, not a blind holdout. The command was run
unchanged from `run-instructions.md` with `--mode reproduce`,
`--specialist-policy none`, and `--response-mode detailed`.

The replay completed with status `completed_with_limits` and process exit code
0. No source edits, backend execution, or specialist side effects were
requested.

## Artifact

- Path: `audit-fcd0847c98b84e3de119b2977abacf3e.json`
- Bytes: `2615520`
- SHA-256: `7bff5934a88fd8cda0e0f3b4f48a3a1edf89c7397b500fb93ff73bebd812a244`
- The digest above was reported by the CLI and independently matched with
  `sha256sum` after completion.

## Inputs

| Source | Bytes | SHA-256 | Extracted text |
|---|---:|---|---:|
| `/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf` | 848234 | `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29` | 93267 chars |
| `/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf` | 8718795 | `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052` | 110233 chars |

## Findings

All findings have disposition `supported_tension`; this is diagnostic evidence,
not a proof that the paper is mathematically wrong.

1. **High, algorithm/numerics (`finding:arithmetic-mismatch:1`)**: the printed
   arithmetic `500 x 200 = 10,000` is false; the computed product is 100,000.
   Parser-text source anchor line: 6809. Because equations are parser-derived
   and marked unreliable, the PDF rendering still requires manual inspection
   before promoting this to a claim about the source document.
2. **Medium, document completeness
   (`finding:document-completeness-external-dependency`)**: required equations
   or model objects are supplied externally, so the artifact is not
   self-contained (line 3353).
3. **Medium, probability/statistics
   (`finding:uncertainty-terminology-conflict`)**: one uncertainty display
   mixes confidence-interval and credible-set terminology without consistently
   stating the statistical target (line 3640).
4. **Medium, approximation/linearization
   (`finding:zero-steady-log-boundary`)**: a zero steady state is combined with
   log-deviation language; an explicit absolute-deviation convention is needed
   (line 3178).
5. **Medium, approximation/linearization
   (`finding:level-linearization-boundary`)**: the level and log-deviation
   statements require an explicit positive-level or absolute-deviation
   convention.
6. **Medium, document completeness
   (`finding:external-model-closure`)**: the model boundary depends on an
   external equation package; standalone reconstruction is incomplete until
   that package is inspected.
7. **Medium, approximation/linearization
   (`finding:level-linearization-pair-candidate:e067748d8b27a3df27af`)**: a
   candidate level/linearized equation pair requires explicit comparison of
   expansion point, order, signs, coefficients, timing, and domains.
8. **Medium, approximation/linearization
   (`finding:level-linearization-pair-candidate:9ba07e0d03849da1aba1`)**: the
   same comparison requirements apply to the candidate pair around equations
   (C.57)--(C.58).
9. **Medium, approximation/linearization
   (`finding:level-linearization-pair-candidate:bbeb6d7c0d901fd20385`)**: the
   bank first-order-condition pair around (C.69)--(C.70) needs the same
   explicit comparison before consistency can be claimed.
10. **Medium, approximation/linearization
    (`finding:level-linearization-pair-candidate:5b0bdad0d715ca807f5d`)**: the
    candidate linearized incentive-constraint equation (C.71) needs explicit
    domain, timing, coefficient, sign, and expansion checks.
11. **Medium, approximation/linearization
    (`finding:level-linearization-pair-candidate:913a9ad5de0681aa399e`)**: the
    impulse-response/model-description relationship is a candidate pair and
    cannot establish consistency without those checks.

The 11 records include overlapping diagnostics rather than 11 independent
problems: findings 2 and 6 describe the same external-dependency boundary from
source and relationship checks, findings 4 and 5 describe the same zero-level
deviation convention, and findings 7--11 are generic candidate-pair prompts
that still require manual equation comparison. Only finding 1 establishes a
specific checked mismatch within the parser-derived text; none is certified
against the rendered PDF.

## Parser and evidence limits

ResearchAssistant `0.1.0` was used through its local CLI at
`/home/chakwong/python/ResearchAssistant/scripts/ra-dev`, commit
`3e9315eb52cf23166e913dfa2566d1908d18f45b` (dirty checkout). Its MCP
`parse-pdf` route was unavailable, so local CLI parsing was used. For each PDF,
only `pdftotext` succeeded. It reported low parse confidence and
`requires_manual_review: true`; equations and citations were marked
unreliable, section headings partial, and reference count zero. The other
parsers (`marker`, `grobid`, `mineru`, `markitdown`) were unavailable. Fewer
than two usable parsers means no multi-parser text consensus is established.

No code or data paths were supplied (`code_count: 0`, `data_count: 0`), so
implementation alignment was not checked. Specialist policy was `none`, and
backend execution was `not_requested`.

## Self-reported access boundary

The agent directly read the run-instructions file and the generated fresh-r5
artifact. The exact audit command read the two absolute PDF inputs and loaded
the configured MathDevMCP and ResearchAssistant runtime code. For manifest
metadata only, the agent additionally queried the current MathDevMCP Git HEAD,
Python version, and local timestamp. It did not run repository searches or
directory listings and did not access plans, other review contents, committee
reports, answer keys, or prior comparison artifacts. This boundary is
self-reported by the agent and is not OS-enforced.

## Non-claims

The PDF extraction and normalized objects do not certify faithful mathematical
recovery. Accounting for an obligation does not solve it or prove the paper
wrong. These findings do not establish code/paper semantic equivalence, general
error-detection recall or precision, publication readiness, source correctness,
or authorization for source edits, release, or scientific claim promotion.
