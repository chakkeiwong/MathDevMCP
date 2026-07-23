# Boehl QE tuned replay R2 manifest

Classification: instruction-compliant tuned replay, not a blind holdout.

This replay follows the red-team repair loop. It uses only the two unchanged
PDFs and the public CLI. It must not inspect committee material, answer keys,
prior comparisons, or plans. Filesystem non-access is self-reported and not
OS-enforced.

Input SHA-256:

- Main: `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29`
- Appendix: `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052`

Implementation file digests at freeze:

- `applied_math_ir.py`: `1582992dcec1453b765c85eb81ecae0bc7a9e26f6ff97bc29505afbcc688b9a1`
- `applied_math_audit.py`: `a5a59c8b8fea531f1ebe62022848bdf848e534c6862edaefd21c380d55dc32a3`
- `applied_math_formalization.py`: `320543b902e02f3203dbd525fc338862c9355b82fdbaf265f62fb78555576610`
- `applied_math_validators.py`: `048aa351cf0209d064375d23083f8dfd91e35c1093ef8e719d6b5671124e506d`
- `applied_math_sympy_worker.py`: `6fd33dab1d5b6e04fb25e3840c772d593517dbf4c32d9af9399a3206c5df8925`
- `applied_math_adapters.py`: `11f680165d8d97a3b09830008edcf49bada1e576afaf1e7b9e21f896c293c622`

Command:

```text
PYTHONPATH=/home/chakwong/python/MathDevMCP/src python -m mathdevmcp.cli audit-applied-math-document \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Boehl(24).pdf" \
  "/home/chakwong/python/DynareMCP/docs/A Structural Investigation of Quantitative Easing RES Appendix Boehl(24).pdf" \
  --response-mode detailed \
  --artifact-root /home/chakwong/python/MathDevMCP/docs/reviews/boehl-qe-tuned-replay-2026-07-22/r2
```

The output path is a dedicated R2 directory to prevent concurrent writers from
overwriting the prior replay artifact.
