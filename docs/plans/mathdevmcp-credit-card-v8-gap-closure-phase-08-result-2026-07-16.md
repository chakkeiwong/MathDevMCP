# Phase 08 Result: Agent Payload And Resolver Repair

## Decision

`PASS`

Every decisive proof, negative-evidence, and derivation-tree compact view now
meets its stated transport budget while preserving literal source, relation,
role, specialist status, veto, action, evidence, and non-claim boundaries.
Detailed evidence remains exactly digest-resolvable.

## Implemented Artifacts

- `src/mathdevmcp/agent_report_artifacts.py`
  - adds `compact_evidence_packet@1` for proof and negative-evidence packets;
  - reuses the verified canonical `agent-reports` store;
  - exposes exact detail resolution through `resolve_agent_report`;
  - enforces the 30,720-byte compact packet budget.
- `src/mathdevmcp/document_derivation_response.py`
  - adds a literal compact source-evidence view containing exact source span,
    canonical target, normalized relation, routing role, specialist result,
    binding reference, and non-promotion boundary;
  - reversibly compacts opaque SHA-256 identities and common blocker prefixes;
  - factors the registered Phase 06 action outcome policy while validating
    exact reconstruction of the complete action contract;
  - preserves exact per-label target and obligation resolution through the
    existing page-token resolver.
- `src/mathdevmcp/proof_audit_v2.py`
  - excludes wall-clock parser runtime from durable proof-packet identity;
  - records that exclusion explicitly without changing parser selection.
- `src/mathdevmcp/mcp_facade.py`, `src/mathdevmcp/mcp_server.py`, and
  `src/mathdevmcp/cli.py`
  - add explicit compact/detailed packet response modes and compact artifact
    roots;
  - expose CLI detail resolution using the existing verified resolver.
- `scripts/run_credit_card_v8_mcp_audit.py`
  - requests the repaired compact packet surfaces for the Phase 09 comparator.
- `tests/test_credit_card_v8_packet_transport.py`
  - covers all nine proof/negative packet pairs, public-surface parity, every
    v8 tree continuation page, and exact resolver round trips.

## Checks And Evidence

All scientific/test commands ran with `CUDA_VISIBLE_DEVICES=-1`.

- Packet sizes before repair:
  - proof: 117,505 to 127,053 bytes;
  - negative evidence: 107,374 to 118,133 bytes.
- Compact proof and negative packets after repair:
  - all are at or below 30,720 bytes;
  - every detailed packet reconstructs exactly through its SHA-256 artifact.
- Compact v8 tree pages after repair:
  - panel NPV: 25,565 bytes;
  - incremental cash flow: 22,454 bytes;
  - PD/LGD/EAD: 21,329 bytes;
  - balance stock-flow: 21,351 bytes;
  - terminal value: 23,139 bytes;
  - Bellman: 24,875 bytes;
  - causal cash-flow object: 23,633 bytes;
  - LATE: 24,427 bytes;
  - randomization assumption: 23,523 bytes.
- Worst compact tree page is below 25,600 bytes.
- All CLI, facade, FastMCP, call-tool, and stdio envelopes remain below 30,720
  bytes.
- Phase 08 focused gate: `91 passed`.
- Document-response regression suite: `78 passed`.

## Evidence Contract Result

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass Phase 08 | All decisive compact views meet budgets and exact details remain resolvable | Status, source, relation, role, specialist, action, veto, evidence, and non-claim parity passed | Large detailed artifacts still require local resolver access by design | Run the exact Phase 09 v8 audit | Smaller output does not improve mathematical validity |

## Reversible Compaction Boundary

- Opaque IDs are encoded reversibly and expanded during semantic validation.
- Common blocker prefixes are stored once and reconstructed exactly.
- Registered action outcome text is stored as a policy identity and expanded
  through the validated action contract.
- The normalized relation omits only `display_text` because it is required to
  equal the adjacent literal canonical target; that invariant is validated.
- Full ledgers and records remain in digest-bound detailed artifacts.

## External-Tool Ledger

No new mathematical backend was needed.  This phase repaired evidence
transport only.  Existing SymPy/Sage/Lean and Lean-search routing decisions
remain part of the resolved detailed evidence and the literal compact
specialist view.

## Boundary And Non-Claims

- Compaction never authorizes proof, source editing, publication, or release.
- Resolver success restores evidence identity; it does not certify truth.
- No v8 source bytes were edited.

## Phase 09 Handoff

Phase 09 may proceed because all decisive compact views meet their budgets and
their full detailed evidence is exactly resolvable under digest-bound local
artifacts.
