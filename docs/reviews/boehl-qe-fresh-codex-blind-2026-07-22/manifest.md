# Fresh blind audit manifest

| Field | Value |
|---|---|
| Run status | `completed_with_limits` |
| Blind scope | Exactly the two supplied Boehl QE PDFs; no comparator, answer key, prior review/plan, or repository edits inspected |
| Command | `PYTHONPATH=/home/chakwong/python/MathDevMCP/src python -m mathdevmcp.cli audit-applied-math-document "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf" "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf" --response-mode detailed --artifact-root /tmp/mathdevmcp-fresh-blind-boehl` |
| Working directory | `/home/chakwong/python/MathDevMCP` |
| MathDevMCP source | `/home/chakwong/python/MathDevMCP/src` |
| Extraction provider | ResearchAssistant local `parse-pdf`; package `0.1.0`; git commit `3e9315eb52cf23166e913dfa2566d1908d18f45b`; dirty checkout recorded by artifact |
| Usable parser | `pdftotext` only; other configured parsers unavailable |
| Backend execution | `not_requested` |
| Source edits | `false` |
| Main PDF bytes/SHA-256 | `848234` / `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29` |
| Appendix PDF bytes/SHA-256 | `8718795` / `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052` |
| Audit artifact | `/tmp/mathdevmcp-fresh-blind-boehl/audit-bb3f727858d91340.json` |
| Audit artifact bytes/SHA-256 | `1851131` / `22edf0efc28a0ae512da44da2345e6f42977229e5036a3774babe4a76563c8c0` |
| Report | `/tmp/mathdevmcp-fresh-blind-boehl/blind-discovery.md` |
| Findings | 13 total: 1 `confirmed_defect`, 12 `supported_tension` |
| Abstentions | 6 selected obligation classes `not_checkable` |

The artifact's own warnings and non-claims are authoritative for the limits of
this run: PDF extraction is non-certifying; fewer than two parsers agreed; no
code paths were supplied; manual review is required; and one document case
cannot establish general error-detection recall or precision.
