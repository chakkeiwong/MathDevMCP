# Boehl QE Fresh R4 Tuned Replay

Date: 2026-07-22 06:08:19 +08:00
Classification: **tuned replay** (not a blind holdout)
Status: CLI replay completed; access-boundary noncompliance disclosed

## Scope and command

The public MathDevMCP CLI was run once with exactly the two user-supplied PDF
paths below. No code or data paths were supplied. The replay configuration was
selected before execution: `mode=reproduce`, `specialist-policy=none`, and
`response-mode=detailed`. The detailed response was persisted by the CLI under
this directory.

```text
PYTHONPATH=src python -m mathdevmcp.cli audit-applied-math-document \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf" \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf" \
  --mode reproduce --specialist-policy none --response-mode detailed \
  --artifact-root docs/reviews/boehl-qe-tuned-replay-2026-07-22/fresh-r4 \
  > docs/reviews/boehl-qe-tuned-replay-2026-07-22/fresh-r4/cli-output.json
```

The CLI exited with status `0`. Repository revision at execution was
`c192dab6cc4b6d35e02f8f056f6ec3e47d3ba2c7`; the worktree had unrelated
pre-existing modifications. Python was `/home/chakwong/miniconda3/envs/tfgpu/bin/python`
(`Python 3.11.15`). GPU execution was not requested or used.

## Input and artifact digests

| object | bytes | SHA-256 |
| --- | ---: | --- |
| paper PDF | 848,234 | `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29` |
| appendix PDF | 8,718,795 | `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052` |
| detailed audit artifact, `audit-fcd0847c98b84e3de119b2977abacf3e.json` | 2,615,521 | `6a8955037b86f120354b2438d39cc9da2de7635c220e98601522bb0e90afa86d` |
| captured CLI envelope, `cli-output.json` | 2,615,792 | `60691b3e7040d583684de19a8efc8cfbd98571398b5af84eff246e333c0d1e1d` |

The audit artifact records both input paths and the two input digests. Its
claim-IR validation error list is empty. The artifact remains the authoritative
detailed output; `cli-output.json` is the exact stdout capture.

## Access self-report

- Before execution, while locating the public command, the operator inspected
  `docs/plans/mathdevmcp-researchassistant-pdf-integration-and-boehl-audit-plan-2026-07-21.md`,
  `docs/plans/mathdevmcp-researchassistant-pdf-integration-and-boehl-audit-result-2026-07-21.md`,
  and filenames under the existing tuned-replay review directory. This violated
  the requested no-prior-plans/reports/comparisons access boundary. Those files
  were not CLI inputs and were not modified, but the interpretive report cannot
  be represented as a fully fresh, instruction-compliant review.
- Both requested PDFs were readable and remained digest-stable during the run.
- The public CLI routed PDF extraction through the local ResearchAssistant
  `ra-dev parse-pdf` command (provider commit
  `3e9315eb52cf23166e913dfa2566d1908d18f45b`, package `0.1.0`).
- `pdftotext` was available at `/usr/bin/pdftotext` (Poppler 22.02.0) and was
  the only usable parser for each PDF. The provider reported `marker`,
  `grobid`, `mineru`, and `markitdown` unavailable or misconfigured.
- ResearchAssistant reported low parse confidence, required manual review,
  unreliable equations/citations, and no multi-parser consensus. Its checkout
  was dirty, so the provider commit does not identify an immutable provider
  worktree.
- The ResearchAssistant MCP surface does not expose `parse-pdf`; the public
  CLI transport was therefore used and this transport limitation is retained
  as evidence, not hidden.
- No specialist route was run (`specialist-policy=none`); no code/data inputs
  were accessed by the audit.

## Findings

All findings below are the fresh CLI output's findings. Every one has disposition
`supported_tension` and an evidence chain, so none is promoted to a certified
mathematical defect. The arithmetic row additionally has formalization status
`backend_abstention` because it comes from parser-only PDF text.

| ID | family | severity | fresh finding |
| --- | --- | --- | --- |
| `finding:arithmetic-mismatch:1` | algorithm_numerics | high | Appendix text prints `500 x 200 = 10, 000`; literal arithmetic gives `100,000`. |
| `finding:document-completeness-external-dependency` | document_completeness | medium | The paper says the full equilibrium equations and steady-state derivation are downloaded from an external GitHub/YAML package. |
| `finding:uncertainty-terminology-conflict` | probability_statistics | medium | One uncertainty display uses both "confidence intervals" and "95% credible sets"; the target is not stated consistently. |
| `finding:zero-steady-log-boundary` | approximation_linearization | medium | The appendix describes a zero steady state and says `Lqt` is an absolute rather than log deviation; the convention needs to be explicit. |
| `finding:level-linearization-boundary` | approximation_linearization | medium | A level/log-deviation boundary requires an explicit positive-level or absolute-deviation convention. |
| `finding:external-model-closure` | document_completeness | medium | Standalone model reconstruction depends on an external equation package. |
| `finding:level-linearization-pair-candidate:e067748d8b27a3df27af` | approximation_linearization | medium | A candidate level/linearized pair around (C.59) requires comparison of expansion point, order, signs, coefficients, timing, and domains. |
| `finding:level-linearization-pair-candidate:9ba07e0d03849da1aba1` | approximation_linearization | medium | A candidate pair around (C.57)-(C.58) requires the same explicit consistency checks. |
| `finding:level-linearization-pair-candidate:bbeb6d7c0d901fd20385` | approximation_linearization | medium | The (C.69)-(C.70) candidate pair is a diagnostic target, not a verified inconsistency. |
| `finding:level-linearization-pair-candidate:5b0bdad0d715ca807f5d` | approximation_linearization | medium | The (C.71) expression and zero-liquidity note require explicit domain and linearization checks. |
| `finding:level-linearization-pair-candidate:913a9ad5de0681aa399e` | approximation_linearization | medium | The appendix's impulse-response description is a candidate semantic pair requiring manual source/formula inspection. |

The run therefore reports 11 diagnostic findings, 11 `supported_tension`, zero
`confirmed_defect`, and eight unresolved `not_checkable` obligations. These are
descriptive outputs of this tuned configuration, not a ranking, recall estimate,
or independent validation against an answer key.

## Non-claims

- PDF extraction does not certify faithful equation, citation, or symbol recovery.
- A `supported_tension` is not proof that the paper or appendix is wrong.
- The arithmetic mismatch was not promoted because the formalization route
  abstained on unauthenticated parser transcription.
- This run does not establish paper correctness, appendix correctness,
  committee-report correctness, model/code equivalence, exact likelihood or
  posterior validity, or any publication/release decision.
- This single tuned replay does not establish general PDF-audit precision,
  recall, convergence, or superiority, and it is not a blind-holdout result.
- Because prohibited prior artifacts were inspected before execution, this
  report is not claimed to be an instruction-compliant fresh interpretive
  replay. The exact CLI artifact is fresh and has only the two PDFs as sources.
- No source files, plans, reports, answer keys, or comparison artifacts were
  modified by this run.
