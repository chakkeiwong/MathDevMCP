# Phase 01 Result: Exact Source Selection

Date: 2026-07-16

Decision: `PASS_WITH_TYPED_PHASE_03_HANDOFF`

## Objective Result

Assumption and derivation report APIs now accept exact `file` and
`source_digest` selectors through library, CLI, facade, and FastMCP surfaces.
The implementation reuses the validated label-scoped obligation extraction
path and records a normalized per-label selection ledger.

## Evidence

- Frozen v8 SHA-256 remained
  `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`.
- All nine v8 labels returned `selection_status=selected` with accepted exact
  file and digest binding.
- Seven current equality/definition targets were inspected by each high-level
  report.
- `eq:causal-cashflow-object` and `eq:randomization-assumption` were exact-bound
  but remained quarantined as unsupported relation shapes. They were not
  reported absent and are handed to Phase 03.
- Unqualified duplicate labels remain ambiguous.
- A stale digest returns `source_digest_mismatch` and inspects zero targets.
- Focused CPU-only suite: `94 passed`.
- Python compile checks and `git diff --check`: passed.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass Phase 01 | Exact source selector parity and nine-label binding | No silent sibling, false absence, or stale-digest acceptance observed | Two non-equality shapes await Phase 03 | Repair parser/source status in Phase 02 | Mathematical correctness or full target extraction |

## Changed Files

- `src/mathdevmcp/derivation_target_extraction.py`
- `src/mathdevmcp/assumptions_for.py`
- `src/mathdevmcp/derivation_audit_report.py`
- `src/mathdevmcp/mcp_facade.py`
- `src/mathdevmcp/cli.py`
- `src/mathdevmcp/mcp_server.py`
- `scripts/run_credit_card_v8_mcp_audit.py`
- focused tests for the affected surfaces

## Residual Risks

- Selector errors are represented in coverage/selection ledgers rather than a
  new top-level error contract; Phase 09 must verify agent usability.
- Exact source binding does not yet correct the nested false parser status.
- The label-scoped schema still supports equality-like targets only; Phase 03
  owns its versioned relation migration.

## Non-Claims

- Source selection is not proof, semantic validation, or document correctness.
- Seven inspected targets do not constitute nine-target mathematical coverage.
- No source document was edited and publication remains disabled.

## Phase 02 Handoff

Phase 02 entry conditions are met if the repaired master-program review returns
no remaining material blocker. It must preserve the exact selector ledger and
separate accepted source identity from specialist parser readiness.
