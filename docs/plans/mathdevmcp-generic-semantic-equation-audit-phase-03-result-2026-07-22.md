# Phase 03 Result: Relation Hypotheses And Checks

Status: superseded and not current. The first independent code review proved
that the ownership-by-shared-symbol result below was unsupported and that
unbounded relations could be false pairs. The current behavior and evidence
are recorded in
`mathdevmcp-generic-semantic-equation-audit-phase-04-repair-result-2026-07-22.md`.

Implemented versioned normalization-to-movement, ownership-preservation, and
level-to-linearized hypotheses plus diagnostic semantic checks. Ownership
relations require a unique shared nontrivial left-hand object; ubiquitous time
indices are excluded from identity. A level row's explicit ownership scope may
be preserved by a paired linearized row only when at least two material symbol
families remain shared.

The exact Fresh R5 parser packets were used as a diagnostic, not as the frozen
engineering oracle. They now produce these bounded records:

| Relation | Check | Outcome |
| --- | --- | --- |
| normalization movement at C.75 | `normalization_sign_tension` | diagnostic tension |
| level C.25 to linearized C.77 | `ownership_scope_preserved_by_bound_symbols` | no tension nominated; entity-specific scope retained through `bb`, `kb`, `q`, `qb`, `qt` |
| level C.47 to linearized C.79 | `sign_or_coefficient_mismatch` | diagnostic tension |

No unrelated semantic tension was emitted in that diagnostic, and semantic
artifact validation returned no errors.

Non-claims: C.75 remains convention/timing dependent; C.77 is source-bound
scope preservation, not proof of model-wide correctness; C.79 remains a
parser-supported tension until authenticated transcription or source code is
available.
