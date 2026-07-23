# Phase 01 Result: Label-Centered Equation Blocks

Status: superseded by
`mathdevmcp-generic-semantic-equation-audit-phase-04-repair-result-2026-07-22.md`.
The first independent code review reopened this phase for page-boundary
provenance repair.

Implemented deterministic, source-bound equation blocks in
`src/mathdevmcp/applied_math_semantics.py`. Standalone and inline labels retain
the exact source packet, source digest, page, line range, raw text, formula
candidate, role context, extraction digests, and parser-only non-claim.

The repair also handles PDF column-order fragments conservatively. A label may
bind to a following equality only before the next label and only after an
explicit continuation connective. A later labeled display cannot be borrowed
as the current block's formula.

Evidence:

- frozen corpus SHA-256:
  `2476a2066873cbd22fd42cc83b4828b00b156f26160dcc2ccc8cd51d258f961c`;
- semantic fixture suite after all Phase 1 repairs: `16 passed`;
- whole focused integration suite at the Phase 4 handoff: `93 passed`;
- source-specific label/token scan found no Boehl labels or target phrases in
  the semantic production module.

Handoff: every candidate block is tied to an exact parser packet and bounded
source location. Blocks remain candidate extraction records, not authenticated
equations.
