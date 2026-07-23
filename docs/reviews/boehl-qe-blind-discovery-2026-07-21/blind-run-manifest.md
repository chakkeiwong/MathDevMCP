# Blind run manifest

Date completed: 2026-07-21

## Source identity

| Source | SHA-256 | Bytes | PDF pages |
| --- | --- | ---: | ---: |
| Main paper: `/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf` | `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29` | 848,234 | 17 |
| Online appendix: `/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf` | `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052` | 8,718,795 | 60 |

Hashes were computed before extraction and independently reproduced inside the
public source-bound extraction envelope. The bridge reread each PDF after
provider execution and did not report a source-change veto.

## Repository and environment identity

- MathDevMCP commit: `c192dab6cc4b6d35e02f8f056f6ec3e47d3ba2c7`
- Branch: `main`
- MathDevMCP worktree: dirty before this run; unrelated user changes and
  untracked files were preserved.
- MathDevMCP package version: `0.1.0`
- ResearchAssistant package version: `0.1.0`
- ResearchAssistant commit: `3e9315eb52cf23166e913dfa2566d1908d18f45b`
- ResearchAssistant worktree: dirty; the commit does not fully identify the
  provider bytes.
- Provider transport: local CLI, because the provider MCP surface does not
  expose `parse-pdf`.
- Host: `Linux DESKTOP-O4SCJCJ 6.6.87.2-microsoft-standard-WSL2 x86_64`
- Python: `3.11.15`, executable reported by `doctor` as
  `/home/chakwong/miniconda3/envs/tfgpu/bin/python`
- SymPy: `1.14.0` (supported-version match)
- MCP: `1.27.0` (supported-version match)
- Poppler `pdftotext`/`pdfinfo`: `22.02.0`
- Timezone: `Asia/Hong_Kong`
- GPU/CUDA: not used or initialized.

## Public functions used

The following public MathDevMCP functions/surfaces were used:

| Public function or command | Role | Result boundary |
| --- | --- | --- |
| `doctor` | backend/environment availability | operational evidence only |
| `tool-matrix` | advertised problem/tool map | informational only |
| `extract_pdf_with_research_assistant` / CLI `extract-pdf-with-research-assistant` | byte-bound detailed PDF extraction | non-certifying evidence transport |
| `external_tool_first_plan` / CLI `external-tool-first-plan` | record considered external routes | routing artifact, not proof |
| `check_equality` compatibility surface / CLI `check-proof-obligation` | bounded SymPy equality checks | certifying only for the exact encoded scalar expressions |
| `derive_or_refute` / CLI `derive-or-refute` | attempted bounded equality/refutation | outputs rejected where assumptions were not enforced |
| `assumptions_for` / CLI `assumptions-for` | attempted domain-assumption discovery | inconclusive; not promoted |

No public MathDevMCP PDF audit function beyond extraction accepted a PDF as its
document input. LaTeX-focused document-rigor workflows were not applied to the
PDFs because doing so would require inventing a structured LaTeX source.

## Exact material commands

### Public interface discovery and environment

```bash
PYTHONPATH=src python -m mathdevmcp.cli --help
PYTHONPATH=src python -m mathdevmcp.cli extract-pdf-with-research-assistant --help
PYTHONPATH=src python -m mathdevmcp.cli doctor
PYTHONPATH=src python -m mathdevmcp.cli tool-matrix
PYTHONPATH=src python -m mathdevmcp.cli external-tool-first-plan --help
PYTHONPATH=src python -m mathdevmcp.cli derive-or-refute --help
PYTHONPATH=src python -m mathdevmcp.cli assumptions-for --help
PYTHONPATH=src python -m mathdevmcp.cli check-proof-obligation --help
```

Public documentation/code inspection was restricted to `README.md`,
`mcp/README.md`, `src/mathdevmcp/{cli.py,mcp_facade.py,mcp_server.py,
research_assistant_pdf.py}`, and directly relevant tests. No broad repository
paper-name search was run.

### Source identity and PDF information

```bash
sha256sum '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf' '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf'
stat -c '%n|%s|%y' '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf' '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf'
pdfinfo '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf'
pdfinfo '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf'
```

### Public ResearchAssistant-backed extraction

The following was first run in the normal sandbox and then repeated with trusted
permissions because the sandboxed GROBID health probe returned `Operation not
permitted`, which cannot establish service unavailability:

```bash
/usr/bin/time -v env PYTHONPATH=src python -m mathdevmcp.cli extract-pdf-with-research-assistant '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf' --response-mode detailed --output-json /tmp/boehl-main-ra-detailed.json
/usr/bin/time -v env PYTHONPATH=src python -m mathdevmcp.cli extract-pdf-with-research-assistant '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf' --response-mode detailed --output-json /tmp/boehl-appendix-ra-detailed.json
/usr/bin/time -v env PYTHONPATH=src python -m mathdevmcp.cli extract-pdf-with-research-assistant '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf' --response-mode detailed --output-json /tmp/boehl-main-ra-trusted-detailed.json
/usr/bin/time -v env PYTHONPATH=src python -m mathdevmcp.cli extract-pdf-with-research-assistant '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf' --response-mode detailed --output-json /tmp/boehl-appendix-ra-trusted-detailed.json
```

The bridge invoked these provider commands:

```bash
/home/chakwong/python/ResearchAssistant/scripts/ra-dev parse-pdf --pdf '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf'
/home/chakwong/python/ResearchAssistant/scripts/ra-dev parse-pdf --pdf '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf'
```

Both used `--timeout-seconds 1000` and the 67,108,864-byte provider-output cap.
All detailed bodies stayed under `/tmp` and were not copied into the repository.

### External-tool-first routes and bounded checks

```bash
PYTHONPATH=src python -m mathdevmcp.cli external-tool-first-plan 'Audit whether the printed DSGE equations and prose roles in a PDF are mutually consistent' --goal-kind document-rigor-audit
PYTHONPATH=src python -m mathdevmcp.cli external-tool-first-plan 'Check whether an adjustment-cost first-order condition follows from the printed budget constraint' --goal-kind derivation
PYTHONPATH=src python -m mathdevmcp.cli check-proof-obligation '500*200' '10000' --backend sympy
PYTHONPATH=src python -m mathdevmcp.cli check-proof-obligation '0.9**(log(log(0.9)/log(0.8))/(log(0.9)-log(0.8)))*log(0.9)-0.8**(log(log(0.9)/log(0.8))/(log(0.9)-log(0.8)))*log(0.8)' '0' --backend sympy
PYTHONPATH=src python -m mathdevmcp.cli check-proof-obligation 'log(log(0.9)/log(0.8))/(log(0.9)-log(0.8))' 'log(log(0.8)/log(0.9))/(log(0.9)-log(0.8))' --backend sympy
PYTHONPATH=src python -m mathdevmcp.cli check-proof-obligation '0.9**(log(log(0.8)/log(0.9))/(log(0.9)-log(0.8)))*log(0.9)-0.8**(log(log(0.8)/log(0.9))/(log(0.9)-log(0.8)))*log(0.8)' '0' --backend sympy
PYTHONPATH=src python -m mathdevmcp.cli check-proof-obligation 'D*G' 'D+G' --backend sympy
PYTHONPATH=src python -m mathdevmcp.cli check-proof-obligation 'h/gamma' 'h*gamma' --backend sympy
PYTHONPATH=src python -m mathdevmcp.cli derive-or-refute 'beta*R = 1' --lhs 'R' --rhs '1' --assumption 'beta*R = 1' --backend sympy
PYTHONPATH=src python -m mathdevmcp.cli derive-or-refute 'Rb*(r+qprev) = kb*qcur' --lhs 'Rb*(r+qprev)' --rhs 'kb*qcur' --assumption 'Rb>0' --backend sympy
PYTHONPATH=src python -m mathdevmcp.cli assumptions-for 'log(L)' --provided-assumption 'steady-state L = 0'
```

Only the first two numeric `check-proof-obligation` mismatches were promoted as
raw findings. Generic symbolic `unverified` outputs and `derive-or-refute`
counterexamples that did not enforce supplied assumptions were explicitly
abstained from. The corrected-formula positive control was also abstained from:
MathDevMCP labeled a floating residual of `-6.93889390390723e-18` as a mismatch,
which is a numeric-tolerance false positive rather than a mathematical defect.

### Direct PDF rendering

```bash
mkdir -p /tmp/boehl-main-render
pdftoppm -f 4 -l 14 -png -r 150 '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf' /tmp/boehl-main-render/page
mkdir -p /tmp/boehl-app-render
pdftoppm -f 4 -l 17 -png -r 150 '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf' /tmp/boehl-app-render/page
pdftoppm -f 1 -l 1 -png -r 180 '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf' /tmp/boehl-app-render/detail
pdftoppm -f 21 -l 21 -png -r 180 '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf' /tmp/boehl-app-render/detail
pdftoppm -f 54 -l 54 -png -r 180 '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf' /tmp/boehl-app-render/detail
```

Rendered images stayed under `/tmp` and were not copied into the repository.

## Parser availability and provider observations

Trusted-context results were the same for both PDFs:

| Parser | Status | Evidence |
| --- | --- | --- |
| `pdftotext` | available, `ok` | `/usr/bin/pdftotext`; one usable body |
| Marker | unavailable | `marker_single not found in PATH` |
| GROBID | unavailable | trusted health probe to `localhost:8070` returned connection refused |
| MinerU | unavailable/misconfigured | `magic-pdf` absent and user config absent |
| MarkItDown | unavailable | `markitdown` absent |

ResearchAssistant reported low parse confidence, manual review required, no
parser disagreements, only one usable parser, and no multi-parser consensus.
The absence of disagreements is not agreement evidence when four parsers failed.

MathDevMCP `doctor` also reported LaTeXML 0.8.6, Pandoc 2.9.2.1, Lean 4.29.1,
SageMath 9.5, and SymPy 1.14.0 available. LeanDojo, LeanExplore, Pantograph,
and LeanSearch-v2 were unavailable or not configured. SymPy was selected for
the two closed scalar checks. Sage/Lean were not used because they add no
authority for document-role or economic-interpretation questions, and the
selected scalar counterexamples required no formal theorem library.

## Runtime and output-size observations

| Run | Provider duration in envelope | Wall time from `/usr/bin/time` | Max RSS | Provider stdout | Detailed JSON |
| --- | ---: | ---: | ---: | ---: | ---: |
| Main, sandbox | 0.529221 s | 0.79 s | 44,032 KiB | 106,659 B | 114,839 B |
| Appendix, sandbox | 0.617654 s | 0.83 s | 51,712 KiB | 131,424 B | 139,580 B |
| Main, trusted | 0.555532 s | 0.90 s | 44,032 KiB | 106,656 B | 114,836 B |
| Appendix, trusted | 1.007401 s | 1.37 s | 51,712 KiB | 131,421 B | 139,577 B |

The three-byte trusted/sandbox output differences came from the different
GROBID preflight error strings; the usable `pdftotext` body sizes were identical
across contexts. Main body: 93,267 characters and 1,762 lines. Appendix body:
110,233 characters and 4,291 lines. Compact mode was not used because it omits
the parser bodies needed for discovery.

Temporary JSON SHA-256 values, recorded only to identify the ephemeral runs:

- sandbox main: `652cb73845727a9d308c9e756ca5af680a8bc3bba4d51e4295d3567d12ed7262`
- sandbox appendix: `d623ed398399238eb0a6f2c1a8a268f39cade787f39dc91c40ec86256e954d95`
- trusted main: `b9eeb06e467e9fc5117ddbce2c9b10796f1e053458473d1cb618a833b926e473`
- trusted appendix: `5a1d50904bbaed20ad6ecfab4bb0038ce0560f834ef4b4003cf24cc4e4933d72`

## Isolation declaration

No forbidden file content was accessed. No file under any `docs/plans`
directory, any pre-existing `docs/reviews` directory, any DynareMCP
AIpostdoc/finalBGS path, or any paper-specific git history/diff was opened,
read, searched, quoted, or used. No repository search for the paper name,
equation labels, or known findings was performed. No other agent or external
model was asked for answers. No answer key was inspected before or after
writing these artifacts.

However, the answer to the literal question `was any forbidden path accessed?`
is **yes, at path-name/listing level only**: an initial `git status --short`
command listed names of forbidden plan/review paths. This violated the strict
instruction not to list such paths. The command did not read their contents,
and the displayed names were not used for discovery. All subsequent git checks
were non-listing. This deviation is material to protocol compliance and is not
being hidden.

The only writes under the repository are the two user-authorized files in this
discovery directory. Application code was not modified. Temporary extraction
and render artifacts remained under `/tmp`.
