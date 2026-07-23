# Boehl QE PDF Audit Source And Run Manifest

Date: 2026-07-21

Plan: `docs/plans/mathdevmcp-researchassistant-pdf-integration-and-boehl-audit-plan-2026-07-21.md`

## Research Question

Can a source-bound ResearchAssistant PDF intake support a reproducible
MathDevMCP audit of the Boehl--Goy--Strobel paper and appendix, and which issue
claims in the BGS committee report can be reproduced from those published
objects?

## Frozen Inputs

| Input | Bytes | SHA-256 | PDF pages |
| --- | ---: | --- | ---: |
| Main paper PDF | 848,234 | `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29` | 17 |
| Online appendix PDF | 8,718,795 | `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052` | 60 |
| Committee report TeX | 922,162 | `c5cfc66061ce90b053cf7e1df6eb770bababfcda85aa54c26546437037da0690` | N/A |

The appendix PDF metadata reports the title and authors Gregor Boehl, Gavin
Goy, and Felix Strobel. The main-paper PDF metadata contains no title or author,
so its rendered first page is the identity anchor.

## Provider And Environment

| Field | Value |
| --- | --- |
| MathDevMCP baseline commit | `c192dab6cc4b6d35e02f8f056f6ec3e47d3ba2c7` |
| ResearchAssistant commit | `3e9315eb52cf23166e913dfa2566d1908d18f45b` |
| ResearchAssistant package version | `0.1.0` |
| ResearchAssistant worktree | Dirty because of unrelated untracked LaTeX build files; commit does not fully identify provider bytes |
| Provider transport | `/home/chakwong/python/ResearchAssistant/scripts/ra-dev parse-pdf --pdf <path>` |
| Direct ResearchAssistant MCP parse tool | Unavailable; `parse-pdf` is CLI-only |
| Python | `3.11.15` |
| Poppler `pdftotext`/`pdfinfo` | `22.02.0` |
| CPU/GPU | CPU-only; `CUDA_VISIBLE_DEVICES=-1`; no GPU operation |
| Random seeds | N/A; deterministic extraction and document audit |

Parser readiness: only `pdftotext` was available. Marker, GROBID, MinerU, and
MarkItDown returned unavailable. Consequently this run has no multi-parser text
consensus.

## Commands

The provider command was invoked through the new MathDevMCP CLI:

```text
CUDA_VISIBLE_DEVICES=-1 PYTHONPATH=src python3 -m mathdevmcp.cli \
  extract-pdf-with-research-assistant <pdf> \
  --response-mode <compact|detailed> --timeout-seconds 1000 \
  --output-json <artifact>
```

The direct baseline used:

```text
pdftotext -layout <pdf> <artifact.txt>
```

The focused committee audit used seven exact labels and the SymPy validation
route. The result selected 7 of 566 labeled equations and is partial coverage.

## Extraction Results

| Source | Provider duration | Usable parser | Extracted body chars | Confidence | Manual review |
| --- | ---: | --- | ---: | --- | --- |
| Main paper | 0.536 s | `pdftotext` | 93,267 | low | required |
| Appendix | 0.615 s | `pdftotext` | 110,233 | low | required |

The paper consensus title and author list are wrong. The appendix consensus
title is correct but its author list is wrong. These fields are not used as
source identity. The adapter now warns that low-confidence consensus metadata
is not verified source identity and that the provider checkout is dirty.

## Artifact Index

| Artifact | SHA-256 | Role |
| --- | --- | --- |
| `paper-extraction-compact.json` | `9328b4ffab3b197fb42d9351e46b295b29891dc1376996502f1b70ec7a283987` | MCP-safe paper extraction summary |
| `paper-extraction-detailed.json` | `a8dd4a3466be658497d3e08e08450d24a4415d578d1ee49a7245dd47337b0393` | Full per-parser paper output |
| `appendix-extraction-compact.json` | `3683680aed085a99af2017f1df27cd4032a645787f4601dd3109a4ba34196469` | MCP-safe appendix extraction summary |
| `appendix-extraction-detailed.json` | `462f3f4efb40463b459f01453f9c8e55737c2be1bf2e64c81fbbdd8f0ee7c94c` | Full per-parser appendix output |
| `paper-pdftotext-layout.txt` | `b34197cd4cd59dc028ecb52f1d20f82fe9e36bbe6d5efe71926e927825bbd3d0` | Direct layout-preserving baseline |
| `appendix-pdftotext-layout.txt` | `cb44c20a583fd115b79667cc273c7ecd07c33929b26f6013b52c9ec06b6ea593` | Direct layout-preserving baseline |
| `committee-latex-index.json` | `fa4eda0f5565690192817b6e313c5198b1e5edeb7adf942abb3658ab3309ca13` | LaTeX-native structure/index evidence |
| `committee-focused-rigor-audit.json` | `54fcea3c7cc47b3b3f8706d0183f636e1b31efa54d43b65bd6b93a15c098bd17` | Detailed seven-label MathDevMCP audit |
| `committee-focused-rigor-audit.md` | `6d87b6cde78f79631e589205c3563a08e7bfcc2325dde711b7cb15b96d39a2a8` | Actionable compact rendering |

The detailed committee audit is 706 KB for seven labels. Its size is a payload
diagnostic, not evidence quality.

## Evidence Boundary

The main question concerns issue reproduction, not certification. Parser text,
rendered-page inspection, committee prose, and a scoped SymPy derivative are
different evidence classes. Exact equation verdicts below rely on rendered
appendix pages 13 and 15--17 plus the level equations, not on parser consensus.
No artifact proves the whole paper, appendix, committee report, model code,
posterior, counterfactual, or lower-bound solution correct.
