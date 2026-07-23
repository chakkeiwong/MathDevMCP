# Boehl QE Tuned Replay Manifest

## Run identity

- Classification: instruction-compliant tuned replay; not a blind holdout.
- Run date: 2026-07-22 (Asia/Hong_Kong).
- Public implementation: `mathdevmcp.cli audit-applied-math-document`.
- MathDevMCP checkout: `/home/chakwong/python/MathDevMCP`.
- MathDevMCP git commit: `c192dab6cc4b6d35e02f8f056f6ec3e47d3ba2c7`.
- MathDevMCP checkout was dirty, so the commit alone does not identify the executed implementation. Selected implementation SHA256 digests were: `src/mathdevmcp/cli.py` = `7073a4ea83334e3d89263787202d31445548d88ae21ad7b2f94315d41d548d43`; `src/mathdevmcp/applied_math_audit.py` = `48840e7c5bde8862ace2b2789ff4a1e55470084a92d6b981118f1161bbd610af`; `src/mathdevmcp/research_assistant_pdf.py` = `9a046dd557b9315cad5ddc663b7596fed9f6c59cc74db95111100831a2752c58`. These selected digests are not a full-worktree content identity.
- Python: `3.11.15`.
- Package version: unversioned local checkout (imported from `PYTHONPATH=/home/chakwong/python/MathDevMCP/src`).
- Provider: ResearchAssistant local CLI, package `0.1.0`, provider checkout `/home/chakwong/python/ResearchAssistant`, git commit `3e9315eb52cf23166e913dfa2566d1908d18f45b`, dirty checkout reported by provider, executable `/home/chakwong/python/ResearchAssistant/scripts/ra-dev`.
- Provider transport: `local_cli`; the generated artifact reports that ResearchAssistant MCP does not expose `parse-pdf`.

## Exact command

```text
PYTHONPATH=/home/chakwong/python/MathDevMCP/src python -m mathdevmcp.cli audit-applied-math-document \
  '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf' \
  '/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf' \
  --response-mode detailed \
  --artifact-root /home/chakwong/python/MathDevMCP/docs/reviews/boehl-qe-tuned-replay-2026-07-22
```

## Inputs

| Input | Bytes | SHA256 |
|---|---:|---|
| `A Structural Investigation of Quantitative Easing RES Boehl(24).pdf` | 848234 | `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29` |
| `A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf` | 8718795 | `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052` |

## Output

- JSON artifact: `audit-bb3f727858d91340.json`.
- JSON bytes: `1951971`.
- JSON SHA256 reported by the CLI at completion: `44623c704f609eabdd82ddec1d621b971678f0523f0d38a2d61b432912946dbb`.
- Final on-disk SHA256 observed during handoff: `7263c1114de840e8a9316314ac5321efdd212212f2037e70ad1486f66d322163` (same path and byte size, but a shared-workspace concurrent rewrite changed the digest after the CLI returned; this discrepancy is retained rather than hidden).
- CLI status: `completed_with_limits`.
- Mode: `screen`; response mode: `detailed`; specialist policy: `auto`.
- No code or data paths were supplied; backend execution was `not_requested`; source edits were `false`.

## Access boundary

To the best of the operator's knowledge, comparator materials, answer keys, committee reports, prior reports, plans, and other review artifacts were not accessed for this replay. The only substantive inputs were the two PDFs named above and the public CLI invocation. This boundary is instructional and self-reported, not OS-enforced sandbox isolation.
