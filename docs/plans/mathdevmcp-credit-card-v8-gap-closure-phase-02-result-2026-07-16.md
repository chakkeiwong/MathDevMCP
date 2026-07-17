# Phase 02 Result: Parser Status And Provenance

Date: 2026-07-16

Decision: `PASS`

## Objective Result

Proof-audit v2 now separates `source_binding_status` from
`specialist_parser_readiness`. Exact file/digest calls measure parser readiness
against the selected label instead of allowing unrelated historical corpus
labels to overwrite accepted exact-source extraction.

## Evidence

- Exact v8 `eq:incremental-cash-flow` reports
  `source_binding_status=accepted_exact_source` and
  `specialist_parser_readiness=selected_for_proof_audit`.
- Exact proof and negative-evidence packets propagate the same source status.
- A deliberately incomplete parser expectation retains accepted source binding
  but returns `unverified:parser_limit`.
- A genuinely absent label now fails closed as
  `inconclusive:source_label_missing` instead of raising `KeyError`.
- Legacy unqualified report calls retain their corpus-wide parser policy for
  compatibility; exact calls use selected-label readiness.
- Failure-focused and exact parity controls: `8 passed`.
- Earlier grouped adjacent run: 59 passed and 2 failures; both failures were
  diagnosed and repaired. One was the missing-label exception; the other was a
  legacy unqualified policy regression.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass Phase 02 | Truthful independent source/parser statuses | No exact accepted source called missing; no status promotion | Other report consumers still need Phase 04 parity | Build typed relation/role contract | Parser or mathematical certification |

## Residual Risks

- The parser benchmark still records directory-wide diagnostics, including
  duplicates, but they no longer define exact-source acceptance.
- Non-equality shapes still lack adapter targets and remain Phase 03 scope.
- Top-level proof status remains conservative and may be inconclusive for
  reasons unrelated to source binding.

## Non-Claims

- Correct status taxonomy is not proof or parser certification.
- No scientific claim, source edit, or publication state changed.

## Phase 03 Handoff

Exact source and parser substatuses now agree with provenance. Phase 03 may
version an additive canonical mathematical-object contract for relations and
routing roles while preserving the existing label-scoped obligation oracle and
rejecting stale source/obligation identities.
