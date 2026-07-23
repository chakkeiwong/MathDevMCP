# Phase 00 Result: Frozen Semantic Corpus And Baseline

Status: passed.

The independently reviewed plan was revised before implementation. The exact
12-case parser corpus and machine oracle are frozen at SHA-256
`2476a2066873cbd22fd42cc83b4828b00b156f26160dcc2ccc8cd51d258f961c`.
It includes 4 positive tensions, 4 no-tension cases, and 4 ambiguous cases
across finance, economics, management, and marketing.

The unchanged current orchestrator was run on the identical bytes and emitted
zero semantic findings for all cases. Baseline artifact SHA-256 is
`301433c117a283f08cfe05bad7a2e222c9d3a60e0194ae57f7d761834819feab`.
Focused pre-implementation tests passed (`31 passed`).

Handoff: production implementation may begin. The corpus/oracle may not be
changed during this implementation program. Any necessary oracle change is a
new program and invalidates the before/after comparison.

Non-claims: the visible corpus is an engineering contract, not a sealed
holdout, real-PDF recall estimate, or evidence of discipline-neutral
generalization.
