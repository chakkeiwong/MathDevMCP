# Phase 03 Result: Source-First And Specialist Routing

Date: 2026-07-22

Status: complete with limits

ResearchAssistant is used for PDF evidence transport. DynareMCP is represented
as an optional route only for supplied `.mod` files; non-Dynare code receives an
explicit `not_applicable` route. Route records state operations, evidence tier,
and non-claim boundaries.

No arbitrary subprocess execution or Dynare semantic equivalence claim was
added. Direct cross-repository model IR exchange remains future work.
