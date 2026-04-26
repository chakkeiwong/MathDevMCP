# MathDevMCP Deployment Guide

MathDevMCP should be deployed as a small base package with optional external workers. The base package must import without LaTeXML, Pandoc, Lean, Sage, or LeanDojo.

## Local Smoke

Run:

```bash
scripts/release_smoke.sh /home/chakwong/MathDevMCP
```

The smoke path runs:

- `doctor`,
- current-parser benchmark,
- benchmark gate,
- release corpus validation,
- governance policy,
- release-readiness report.

## Optional Workers

Use separate environments or workers for:

- parser tools: LaTeXML and Pandoc,
- symbolic/numeric tools: SymPy and Sage,
- Lean direct checking,
- LeanDojo proof search.

LeanDojo should remain isolated from document/PDF/ML environments when dependency conflicts appear.

## Release Caveats

External commands must have timeouts and structured `inconclusive` failures. Private corpora should not be committed; only manifest stubs and expected labels belong in git.
