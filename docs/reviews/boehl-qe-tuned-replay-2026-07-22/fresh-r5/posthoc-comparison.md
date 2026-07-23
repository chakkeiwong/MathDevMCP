# Fresh R5 Post-Hoc Comparison

The R5 report, manifest, and audit artifact were frozen before this comparison
was written. R5 is an instruction-compliant tuned replay with self-reported,
non-OS-enforced non-access. It is not a blind holdout.

| Committee issue | R5 result |
| --- | --- |
| Appendix C not self-executing | exact topic |
| C.52--C.68 timing/object separation | partial |
| C.71 zero steady state | exact topic |
| C.75 deposit-return sign/timing | missed |
| C.77 bank-held ownership domain | missed |
| C.79 sign/coefficient conflict | missed |
| Equations after C.96 outside PDF | exact topic |

Result: **3 exact, 1 partial, 3 missed**.

The valid replay confirms the central conclusion from R4: source and claim
integrity improved, but generic semantic error detection remains weak. The
earlier `3 exact, 3 partial, 1 missed` result relied partly on Boehl-shaped
production rules and is not valid evidence of general capability.

No general recall, mathematical correctness, model/code equivalence,
posterior validity, causal validity, or release-readiness claim follows.
