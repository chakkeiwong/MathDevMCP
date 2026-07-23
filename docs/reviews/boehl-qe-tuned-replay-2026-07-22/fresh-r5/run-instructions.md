# Fresh R5 run instructions

This file is the complete operational input for the fresh agent. Do not search
the repository, plans, review directories, committee reports, answer keys, or
prior comparisons. Do not list directories. Run exactly the command below,
using only the two absolute PDF paths and this output directory.

```text
PYTHONPATH=/home/chakwong/python/MathDevMCP/src python -m mathdevmcp.cli audit-applied-math-document \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf" \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf" \
  --mode reproduce --specialist-policy none --response-mode detailed \
  --artifact-root /home/chakwong/python/MathDevMCP/docs/reviews/boehl-qe-tuned-replay-2026-07-22/fresh-r5
```

This is an instruction-compliant tuned replay, not a blind holdout. State
non-access explicitly. Non-access is self-reported and not OS-enforced.
