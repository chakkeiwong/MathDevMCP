# Boehl QE Tuned Replay R4: Post-Hoc Comparison

The R4 artifact was frozen before this comparison was written. This is a
descriptive same-paper comparison, not a population recall estimate.

| Committee issue | R4 classification | Reason |
| --- | --- | --- |
| I01: Appendix C not self-executing | exact topic | external package dependency surfaced |
| I02: C.52--C.68 timing/object separation | partial | generic level/linearization candidates only |
| I03: C.71 zero steady state | exact topic | zero/log boundary surfaced |
| I04: C.75 deposit-return sign/timing | missed | no authenticated or generic SDF relation |
| I05: C.77 bank-held ownership domain | missed | paper-specific ownership rule removed; generic matcher did not recover it |
| I06: C.79 sign/coefficient conflict | missed | paper-specific return rule removed; generic matcher did not recover it |
| I07: equations after C.96 outside PDF | exact topic | external closure surfaced |

R4 score: **3 exact, 1 partial, 3 missed**. This is worse than the earlier
`3 exact, 3 partial, 1 missed`, but the earlier partial hits depended on
source-specific production tokens and were invalid promotion evidence.

The correct interpretation is that evidence integrity improved while generic
scientific recall remains weak. The next work should build typed symbol,
timing, domain, and relation extraction from authenticated structured sources,
then evaluate it on a sealed cross-domain corpus.
