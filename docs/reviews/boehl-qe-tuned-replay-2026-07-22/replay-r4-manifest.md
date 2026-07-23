# Boehl QE tuned replay R4 manifest

Classification: instruction-compliant tuned replay, not a blind holdout.

R4 follows the red-team repairs and the R3 evidence-binding correction. It
uses only the two unchanged PDFs and public CLI in a fresh session; no
committee material, answer key, prior comparison, plan, or replay artifact may
be inspected. Non-access is self-reported and not OS-enforced.

Inputs:

- Main SHA-256: `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29`
- Appendix SHA-256: `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052`

Output directory: `docs/reviews/boehl-qe-tuned-replay-2026-07-22/r4`.

Implementation digests:

- `applied_math_ir.py`: `1582992dcec1453b765c85eb81ecae0bc7a9e26f6ff97bc29505afbcc688b9a1`
- `applied_math_audit.py`: `0d6c40ef7f53d31f48f87551f04604cf20f7b526604e0cba28bd40f034a943e9`
- `applied_math_formalization.py`: `320543b902e02f3203dbd525fc338862c9355b82fdbaf265f62fb78555576610`
- `applied_math_validators.py`: `048aa351cf0209d064375d23083f8dfd91e35c1093ef8e719d6b5671124e506d`
- `applied_math_sympy_worker.py`: `6fd33dab1d5b6e04fb25e3840c772d593517dbf4c32d9af9399a3206c5df8925`
- `applied_math_adapters.py`: `11f680165d8d97a3b09830008edcf49bada1e576afaf1e7b9e21f896c293c622`
