# Boehl QE tuned replay R3 manifest

Classification: instruction-compliant tuned replay, not a blind holdout.

R3 supersedes the earlier replay artifacts because it follows the independent
red-team repair and the PDF fail-closed correction. It uses only the two
unchanged PDFs and public CLI in a fresh session. It must not inspect committee
material, answer keys, prior comparisons, plans, or prior replay reports.
Non-access is self-reported and not OS-enforced.

Inputs:

- Main SHA-256: `bb3f727858d9134064235753a783947756e32f7dbc65a7a177886cab5dc5fd29`
- Appendix SHA-256: `c02de9858a64ddc39d7499ed8a83bae28442941041894082f16bca44cabe4052`

Output directory:

`docs/reviews/boehl-qe-tuned-replay-2026-07-22/r3`

The directory is dedicated to R3 so no other replay shares its artifact path.
