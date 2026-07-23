# Fresh R5 Run Manifest

## Execution

- Purpose: tuned replay of the Boehl quantitative-easing applied-math audit.
- Artifact completion time: `2026-07-22T06:24:02.046432411+08:00` (filesystem
  modification time).
- Manifest metadata-query time: `2026-07-22T06:25:26+08:00`.
- Repository: `/home/chakwong/python/MathDevMCP`.
- Git commit: `c192dab6cc4b6d35e02f8f056f6ec3e47d3ba2c7`.
- Python: `3.11.15`.
- Command (exact):

```sh
PYTHONPATH=/home/chakwong/python/MathDevMCP/src python -m mathdevmcp.cli audit-applied-math-document \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf" \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf" \
  --mode reproduce --specialist-policy none --response-mode detailed \
  --artifact-root /home/chakwong/python/MathDevMCP/docs/reviews/boehl-qe-tuned-replay-2026-07-22/fresh-r5
```

- Exit code: `0`.
- Reported status: `completed_with_limits`.
- Mode: `reproduce`.
- Specialist policy: `none`.
- Response mode: `detailed`.
- Backend execution: `not_requested`.
- Source edits: `false`.
- Specialist side effects: `false`.
- Wall time: approximately `0.98 s` (CLI process duration reported by the
  runner).
- Random seeds: `N/A` (deterministic document-audit replay; no stochastic
  sampler or training run).
- Data version: `N/A` (no data paths supplied).
- CPU/GPU status: `N/A` (the command is a CPU-oriented document parser; no GPU
  was initialized or benchmarked).

## Source digests

| Input | Bytes | SHA-256 |
|---|---:|---|
| `A Structural Investigation of Quantitative Easing RES Boehl(24).pdf` | 848234 | `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29` |
| `A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf` | 8718795 | `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052` |

## Output artifact

- Path: `audit-fcd0847c98b84e3de119b2977abacf3e.json`.
- Bytes: `2615520`.
- SHA-256: `7bff5934a88fd8cda0e0f3b4f48a3a1edf89c7397b500fb93ff73bebd812a244`.
- The digest was reported by the CLI and independently verified with
  `sha256sum`.
- Required companion notes: `replay-report.md` and `run-manifest.md`.

## Provider and parser record

- Provider: ResearchAssistant `0.1.0`, local executable
  `/home/chakwong/python/ResearchAssistant/scripts/ra-dev`.
- Provider commit: `3e9315eb52cf23166e913dfa2566d1908d18f45b`; checkout dirty.
- Transport: `local_cli`; MCP `parse-pdf` unavailable.
- Both PDFs: `pdftotext` usable; parse confidence `low`; manual review
  required; equations/citations unreliable; section headings partial.
- Both PDFs: unavailable parsers `marker`, `grobid`, `mineru`, `markitdown`.
- Extracted text: 93267 chars (main) and 110233 chars (appendix).

## Access boundary

Self-reported: the agent directly read the run instructions and generated
fresh-r5 artifact. The exact audit command read the two named PDF paths and
loaded its configured MathDevMCP and ResearchAssistant runtime code. For
manifest metadata only, the agent additionally queried the current MathDevMCP
Git HEAD, Python version, and local timestamp. No repository search or directory
listing was run, and no plans, other review contents, committee reports, answer
keys, or prior artifacts were accessed. This is self-reported and not
OS-enforced.

## Evidence boundary

There were 11 `supported_tension` findings: one high-severity arithmetic
mismatch and ten medium-severity document-completeness, probability/statistics,
and approximation/linearization tensions. The result is diagnostic evidence
only; it does not certify PDF equation recovery, solve obligations, establish
code alignment or semantic equivalence, support general recall/precision,
authorize source edits/publication, or promote scientific claims.
