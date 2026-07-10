# Phase 09 Real-Document Comparison

Date: 2026-07-10

## Question

Do the strict agent-guided, tool-verified reports avoid the previous regression
where blocked ranked branches looked like proposed mathematical fixes?

## Artifacts

- Card NPV Markdown:
  `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.md`
- Card NPV JSON:
  `docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json`
- Risky debt Markdown:
  `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.md`
- Risky debt JSON:
  `docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json`

## Result Summary

| Document | Targets | Ready repairs | Gap reports | Compiler errors | Worker failures |
| --- | ---: | ---: | ---: | ---: | ---: |
| Card NPV | 4 | 0 | 4 | 0 | 0 |
| Risky debt | 2 | 0 | 2 | 0 | 0 |

All six target outputs are `document_gap_report` items under the strict
compiler.  No target is published as a document-ready repair proposal because
no target has backend-closed or partially backend-closed evidence.

## Improvement Over Baseline Weakness

The previous weakness was not that the tool failed to solve all hard
mathematics.  The damaging weakness was that blocked branches could still look
like repair proposals.  The Phase 09 reports avoid that:

- Each target records `tool_grounded_proposal_compiler_result`.
- Each compiled item has `publishable_as_repair=false`.
- Each compiled item has `publishable_as_gap_report=true`.
- Each gap report lists remaining blocker ids and evidence refs.
- Candidate LaTeX appears only as blocked candidate edit text with the
  non-claim "This is a gap report, not a repair proposal."

## Main Remaining Scientific Gaps

Card NPV:

- Conditional expectation law and conditioning scope are not encoded.
- Integrability/measurability of random cash-flow and terminal-value terms is
  not closed.
- Macro-to-backend symbol mapping is still needed before SymPy/Sage/Lean can
  certify the finite-horizon identities.
- Some labels have multiple localized rows, so grouped/split obligations still
  need explicit formal targets.

Risky debt:

- The proposition states interiority and differentiability, but conditional
  law, integrability, derivative-under-expectation interchange, and
  choice-independent transition-law conditions remain unresolved.
- The FOC rows still need grouped/split obligations for the multiline display.
- Backend attempts remain diagnostic because stochastic and derivative
  constructs are not yet encoded as certifying backend targets.

## Non-Claims

- These reports do not prove either document.
- These reports do not claim the proposed assumptions are minimal or
  sufficient for publication.
- These reports do not claim speedup from parallel execution.
- These reports do not claim public release readiness.
