# MathDevMCP Phase 08D P08C1-Bound Compact Payload Repair Subplan

Date: 2026-07-14

Status: `COMPLETE_PASS_P08D_FROZEN_PAYLOAD`

## Objective

Implement a schema-versioned, artifact-backed compact document-derivation
response whose deterministic pages remain directly actionable and preserve the
complete claim boundary for the target-faithful P08C1 card and risky-debt
audits within:

- 25,600 canonical response bytes; and
- 30,720 bytes for each public CLI, facade, FastMCP `CallToolResult`, and full
  stdio JSON-RPC representation.

The repair must expose every full referenced record through a strict public
resolver, preserve no-artifact behavior without target loss, and never rerun
the document audit during continuation or resolution.

## Entry Conditions

1. Phases 00-07 remain complete.
2. P08A extraction/context evidence remains immutable under extraction file
   SHA-256
   `8a0386d360068ff3ee481ea88a170a41abeae6dce5716a55a7c75660859e4da0`.
3. P08B remains independently verified and scoped only to
   `eq:cashflow-rate-derivative`.
4. P08C remains immutable historical evidence but is not a mathematical
   comparator because its card audit used a continuation-only cash-flow target.
5. P08C1 is closed `PASS_P08C1_TARGET_FIDELITY`, decision digest
   `8c2ca339fc5a360be7abaa4264a6b33d773995a160437d11ffdcab5d54d86c7b`,
   with full primary Claude Opus review `VERDICT: AGREE`.
6. The payload compiler and Phase 06 action validator are byte-identical to the
   P08C snapshot and current tree:
   `127de9b1fcf313a8dbd7bd0e1bf24e531845e4b8a843d3a917d458fb160ede02`
   and
   `9a74755442db135694e0b4f7c2763299a372e2a2aaeb95d2ecdcb80d552435c0`.
7. Publication, effective promotion, applicable source edits, defaults,
   releases, commits, pushes, installs, network/model use, and mathematical
   backend execution remain outside scope.

## Exact Baseline

The same P08C request identities remain valid because focus labels and audit
controls did not change, but the audit/result/artifact bytes did:

| Input | Card | Risky debt |
| --- | --- | --- |
| Request SHA-256 | `32a7793e5f1674edb2e9690429d2a4998316bd780385bce8867355c61fda3a45` | `fee205368a9af4d2a399d43827352d14830a02ade2e0ba35b3ff7ec231a638be` |
| Audit SHA-256 | `e74d738f651657cbb68498ebf51faf50c9a2589381d6477fa6910c2070f548e8` | `c6370c05d12dae1c2bee8f2e321da487f26115545943b9ee1874e56028228047` |
| Audit result ID | `audit_992acef95bd8043ea229e6133b56f8bb1aa2b8b473bde9d6b72144767d126851` | `audit_61a39057532995be0ca8f0d225e03bbf3c5d64369075d933c9ddc333f9a76622` |
| V1 compact SHA-256 | `118aa556f743e2cefb6ee8e26de08bd19c161ab66a3226b0d28da54386f8f11d` | `e2a76b66a92e4ae77f03142b24e15fa89408b81a6f2112a0b8170e8472ba8427` |
| V1 compact bytes | 140,928 | 137,694 |
| Detailed artifact SHA-256 | `c5ac16312c9ec34dae87f8974ac5ccb800b13c198c6ffe28a320cfe46d35709f` | `cb7a39b8acce5c4a91dbbc52ad2a6309304dbca88974ea42ae2417c44de89082` |
| Detailed artifact bytes | 1,539,618 | 1,531,606 |

The authoritative replay source is:

```text
.local/mathdevmcp/evidence/p08-20260714/p08c1/20260714T121103Z-fc7811786801
```

P08D may construct fresh temporary or output-root artifacts from these audit
bytes. It must not use the stale P08C audit/artifact as a semantic comparator.

## Skeptical Plan Audit

### Wrong baselines and proxies

- Phase 07 synthetic payloads and P08C continuation-only card bytes are invalid
  baselines.
- Target count, first-page size, canonical size alone, or a resolver count are
  proxy metrics. Promotion requires every greedy page and every public wire
  surface, exact ordered union, full resolver unions, and target-fidelity
  bindings.
- One-target pages are not assumed. The feasibility program tries every
  source-order prefix up to `target_limit` and selects the longest prefix that
  fits both limits. The frozen inputs happen to yield one target per page.

### Hidden assumptions found and repaired

1. The old JSON cursor was 1,154 characters and made the risky pages exceed the
   canonical limit. The refreshed design uses a strict fixed-width binary
   capability, 315 unpadded base64url characters, while retaining full 256-bit
   audit, request, artifact, filter, page-boundary, collection-scope, and
   checksum bindings.
2. Four frozen actions match the registered unresolved-choice projection; the
   repaired cash-flow target has a different valid scope-bound Phase 06 action.
   The v2 response therefore uses a compact registered-policy form only on
   exact byte-equality and otherwise carries the complete action inline after
   `validate_discriminating_action` succeeds. No action is truncated or
   normalized speculatively.
3. P08C1 introduced the authoritative `label_scoped_obligation`. Content
   identity and the public resolver must bind and expose that record in
   addition to the semantic packet, typed repair obligation, nested math
   obligation, source span, and target text.
4. Global resolver collections repeat by page. This is deliberate capability
   scoping, not a claim that separate global copies exist in the artifact.

### Environment and commands

The feasibility program uses `mcp==1.27.0`, canonical UTF-8 JSON, the current
response/action modules only after exact byte-identity checks, fresh temporary
artifacts, and no source audit, doctor, CAS, proof assistant, model, network, or
GPU operation. Its commands answer product feasibility directly.

Local skeptical verdict: `PASS_TO_SUBSTANTIVE_PLAN_REVIEW`.

## Feasibility Evidence

The refreshed
`docs/plans/p08d_payload_feasibility_spike_20260714.py` binds P08C1, rebuilds
fresh v1 comparators and verified detailed artifacts, checks exact target and
action semantics, constructs the actual greedy partition, decodes every token,
reconstructs every page boundary and resolver scope, and traverses all public
record collections.

| Page | Targets | Canonical | CLI | Facade | CallToolResult | Full stdio |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Card 0 | `eq:panel-npv-functional` | 24,191 | 24,192 | 24,201 | 24,331 | 24,365 |
| Card 1 | `eq:incremental-cash-flow` | 20,246 | 20,247 | 20,256 | 20,386 | 20,420 |
| Card 2 | `eq:incremental-npv` | 23,799 | 23,800 | 23,809 | 23,939 | 23,973 |
| Risky 0 | `eq:foc-k` | 25,387 | 25,388 | 25,397 | 25,527 | 25,561 |
| Risky 1 | `eq:foc-b` | 25,390 | 25,391 | 25,400 | 25,530 | 25,564 |

These are the final 236-byte, 315-character token measurements reproduced
after the workstation restart. The smallest canonical page margin is 210 bytes
and the smallest full-stdio page margin is 5,156 bytes.

The program traversed 52 card and 38 risky resolver pages. The worst card
resolver full-wire size was 30,588 bytes; the worst risky size was 30,705,
leaving a 15-byte margin. Production must therefore use byte-aware record fill,
canonical serialization, the closed resolver schema, and no extra wire fields.
The narrow resolver margin is a hard implementation test, not a reason to
raise the limit.

This evidence establishes feasibility only. Production code, registered-tool
serialization, mutation tests, and the formal replay must repeat the checks.
It remains the reviewed pre-implementation comparator. The fresh production
replay is recorded separately in the P08D result and supersedes the spike for
the phase decision; its worst complete resolver is 30,719 bytes, leaving a
one-byte full-stdio margin.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| P08C1 audit bytes | Verified P08C1 replay and review | Only target-faithful frozen audit | Payload passes for wrong mathematics | Exact input SHA, target order, obligation digest checks | Hard binding |
| Response schema `p08_document_derivation_response@2` | Shape and pagination break v1 | Prevents silent v1 consumer acceptance | Old consumer treats indices as full records | Dispatch/migration tests | Required API boundary |
| Cursor schema `p08_document_derivation_cursor@2` | New binary capability | Exact closed continuation/resolver authority | Forged or noncanonical token accepted | Length, magic, base64, checksum, offsets, digest mutation matrix | Hard binding |
| Binary cursor fixed layout | Feasibility result | Preserves full digests without JSON key overhead | Decoder order/version drift | Round trip to named semantic record and every-byte mutation checks | Reviewed representation |
| Target limit versus resolver limit | R1 substantive review finding | Target partition and record pagination are separate controls | Surface silently substitutes one limit for the other | Omitted/equal/different continuation limits and independent resolver-limit tests | Repaired API boundary |
| Canonical resolver scope descriptor | R1 substantive review finding | Binds the exact global/null and target/collection capabilities plus ordered raw-record identities | Token minted for one pair resolves another pair | Descriptor reconstruction and cross-target/global/collection mutations | Repaired authority boundary |
| Greedy longest source-order prefix | Existing deterministic order and `target_limit` maximum | Avoids target shopping and maximizes page use | Skip/reorder/starvation | Recompute partition from offset zero; union exact once | Reviewed algorithm |
| At least one complete target | Agent actionability | Never return a global-only page | One target exceeds boundary | Preserve it, mark exceeded, fail product gate | Hard fail-safe |
| Registered action projection only on exact match | Phase 06 validator | Saves bytes without changing action | Nonstandard action forced into wrong policy | Exact compare, expansion, semantic ID validation | Hard boundary |
| Inline validated action fallback | P08C1 cash-flow action | Preserves valid heterogeneous actions | Oversize or invalid action hidden | Validate exact mapping and measure page | Reviewed fallback |
| Label-scoped obligation identity/resolution | P08C1 target contract | Prevents payload from aliasing row/display target | Content digest omits authoritative extraction record | Inline ID/digest/SHA; public resolver exact record | Hard target boundary |
| Literal global IDs on each page | Claim-boundary contract | Directly shows veto/assumption/action identities | Count/hash hides applicability | Exact parity and removal mutation | Hard boundary |
| Literal page identity tables with integer memberships | Feasibility result | Deduplicates repeated target strings | Wrong/out-of-range membership | Expansion equality and index mutations | Reviewed representation |
| Raw record resolver | Persisted audit is source of truth | Makes normalized page reconstructable | Derived catalog claimed as stored data | Rebuild collections directly from stored audit | Hard representation boundary |
| Artifact-backed bounded mode | Existing optional `artifact_root` | Stable continuation/resolver source | Dangling cursor without bytes | Require verified artifact and exact request/audit binding | Reviewed route |
| No-artifact inline-complete mode | Existing default | No implicit writes or dangling continuation | `target_limit` strands omitted targets | Include all targets, no token, honest overage | Compatibility boundary |
| Structured FastMCP result with fixed text | Wire budget | Avoids duplicating full JSON in text | Content-only client silently loses data | Migration docs and exact registered-tool tests | Intentional experimental break |
| Fixed limits | Master product contract | Controls agent context and wire use | Limit changed to force pass | Literal constants and measurement tests | Hard product criterion |

## External-Tool-First Audit

SymPy, SageMath, Lean, LeanSearch-v2, LeanExplore, jixia, Pantograph, and
LeanDojo were considered. None is relevant to a presentation, pagination,
artifact-resolution, or wire-serialization repair. The selected tools are the
deterministic response compiler, Phase 06 action validator, canonical JSON,
strict token codec, and pinned FastMCP serialization. P08D introduces no
mathematical search or derivation algorithm.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the exact target-faithful P08C1 audits be represented as deterministic, directly actionable compact pages and resolvable records within both product limits? |
| Comparator | Exact P08C1 audits/requests above, exact P08A obligation bindings, fresh verified v1 detailed artifacts, and v1 compact semantic projections. |
| Primary criterion | Every artifact-indexed greedy page and every resolver page validates; canonical response <=25,600 and every public surface <=30,720; page union is exact once and in source order; global and per-target veto/assumption/action/non-claim identity is exact; each target binds and resolves its label-scoped, typed, math, source-span, target-text, blocker, evidence, source, assumption, and action records; no-artifact mode is inline-complete; publication remains disabled. |
| Veto diagnostics | Input/code/MCP drift; v1/v2 schema confusion; target omission/duplication/reorder; non-boundary or forged token; checksum/digest/offset/policy mutation; partition mismatch; invalid action projection/expansion; missing obligation identity/record; wrong table membership; unresolved or dangling record; absolute path leak; any public envelope overage; backend/model/network execution; publication/promotion/applicable repair. |
| Explanatory only | Compression ratio, page count, resolver count, field attribution, and margins above zero. |
| Not concluded | Mathematical proof/refutation, whole-document correctness, complete assumptions, best repair, publication/default/release readiness, general compactness outside frozen fixtures, Phase 08 closure before result review, or mission completion. |
| Preserved artifact | Implementation/tests/docs; formal P08D create/verify bundle with exact inputs, artifacts, pages, decoded tokens, resolver unions, no-artifact fallback, all public measurements, mutations, decision, and substantive review. |

## Closed V2 Response Contract

### Representations

`artifact_indexed` is allowed only with a verified v1 detailed artifact. It
uses byte-aware target pages and the dual-purpose v2 capability token.

`inline_complete` is required when `artifact_root` is absent. It carries every
full current target record, never emits a token, may exceed `target_limit` to
avoid loss, and reports `exceeded_complete_boundary_preserved` honestly.

### Per-page fields

The page retains the complete global boundary: audit/request/status/source,
publication, promotion, coverage, failure classifications, veto IDs,
unresolved/candidate assumption IDs, action-decision IDs, non-claims,
execution summary, artifact identity, record inventory, completeness, and byte
guardrail.

`page_identity_tables` contains literal `blocker_ids`, `evidence_refs`, and
`source_ref_ids` once per page. Each target contains checked indices, exact
status/failure/veto/assumption memberships, and one validated selected action.

`content_identity` contains:

- semantic packet ID;
- label-scoped obligation ID, canonical obligation digest, and raw record SHA;
- typed repair obligation ID/SHA;
- nested math obligation ID/SHA;
- source-span SHA; and
- target-text SHA.

### Binary capability token

The token is unpadded canonical base64url over exactly 236 bytes:

```text
magic[4] = MDP2
byte_policy_code[1]
requested_target_limit[1]
page_index[2] big-endian unsigned
previous_offset[2] big-endian unsigned
next_offset[2] big-endian unsigned
audit_result_digest[32]
audit_request_digest[32]
artifact_sha256[32]
filter_digest[32]
page_boundary_digest[32]
resolver_scope_digest[32]
checksum_sha256_of_all_prior_bytes[32]
```

The encoded token is exactly 315 characters. The decoder rejects padding,
noncanonical base64url, wrong magic/length/policy, invalid limits/offsets,
checksum mismatch, and any semantic mismatch after reconstruction. It rejects
requested target limits outside 1-100 and page/offset values outside 0-65,535. A
future wider document target range requires a new token version.

The token does not reduce digest strength or omit a v1 JSON binding; it removes
only repeated schema/field-name bytes. Named semantic fields are reconstructed
by the versioned decoder and compared with the artifact/request/partition.

The `resolver_scope_digest` is SHA-256 over canonical JSON schema
`p08d_document_derivation_resolver_scope@1`. Its ordered `scopes` entries are
exactly:

```text
scope_kind: global | target
target_id: null for global, exact page target ID otherwise
collection: one exact closed collection name
record_count
record_bindings: ordered [{identity, raw_record_sha256}, ...]
```

Global entries appear once in the fixed order below. Target entries appear in
page/source order and then in the fixed target-collection order below. Token
acceptance reconstructs this descriptor from the verified artifact, requires
digest equality, and then permits only an exact `(target_id, collection)` pair
present in the descriptor. A global collection requires `target_id=null`; a
target collection requires the exact page target ID.

`requested_target_limit` governs only the greedy target-page partition. On an
initial request, omission uses 20 and an explicit value must be 1-100. On
continuation, the token value is authoritative: omission reuses it and an
explicit caller value must equal it or the request is rejected. It is included
in the recomputed page-boundary digest; it is never inferred as 20.

### Action representation

`registered_policy` contains the action ID/kind, branch IDs, launch-veto
indices, prerequisite, and expected-artifact kind only when expansion against
the registered fixed policy reconstructs the exact raw action and passes the
Phase 06 validator.

`inline_validated` contains the complete raw action after exact Phase 06
validation when no registered projection matches. It is not truncated. Both
forms must preserve the original semantic `action_id` byte-for-byte.

## Public Resolver Contract

Add `resolve_document_derivation_records` to library, CLI, facade, and FastMCP.
It accepts only:

```text
page_token
target_id: string or null
collection
offset >= 0
1 <= limit <= 100
artifact_root
```

Allowed global collections:

```text
global_blocker_records
global_evidence_ref_records
global_source_ref_records
```

Allowed target collections:

```text
blocker_records
evidence_ref_records
source_ref_records
unresolved_assumption_records
candidate_assumption_records
selected_action
label_scoped_obligation
typed_repair_obligation
math_obligation
source_span
target_text
```

Every returned entry is exactly `identity`, `raw_record_sha256`, and redacted
`record`. Resolver pages use longest-prefix byte-aware fill against the
30,720-byte public limit, return no partial record, and reject offsets outside
a nonempty collection. A valid empty collection queried at `offset=0` returns a
successful zero-record page with `next_offset=null`; any other offset is an
error. The repository absolute-path regex scans success and
error payloads. Resolver unions must equal records independently rebuilt from
the verified persisted audit.

Resolver `limit` is an independent requested record-count cap, not the target
partition limit. It must be 1-100 on every resolver call, is reported as the
resolver page's `limit`, and may vary across calls without changing token
authority or collection identity. It never overrides or needs to equal the
token's `requested_target_limit`; byte-aware fill may return fewer records.

## Required Implementation

1. Bump response/cursor schema to v2 and reject v1 cursors with actionable
   migration text.
2. Implement `artifact_indexed` and `inline_complete` exactly as above.
3. Implement strict binary token encode/decode and recompute the full greedy
   partition from offset zero for continuation acceptance.
4. Replace repeated target assumptions/blockers/references/actions with the
   closed literal tables, memberships, action forms, and content identity.
5. Persist no new semantic artifact schema; continue reading verified
   `p07_document_derivation_artifact@1` bytes.
6. Implement the public resolver and every named collection directly from the
   persisted audit.
7. Make page and resolver fill byte-aware across canonical, CLI, facade,
   registered FastMCP result, and full stdio wire.
8. Preserve detailed and artifact-only semantics except explicit shared v2
   metadata needed for dispatch.
9. Change compact CLI output to canonical one-line JSON plus LF. Register
   FastMCP structured output without `outputSchema`; return only fixed text
   `MathDevMCP structured result; read structuredContent.` in `content`.
10. Document the experimental v1-to-v2/content-only-client migration.
11. Add `scripts/run_p08d_frozen_payload_replay.py` with create/verify modes,
    exact P08C1 inputs, no raw audit calls, and fresh output root.

## Required Checks

1. Focused v2 compiler tests for both representations, exact global/target
   parity, heterogeneous action expansion, content identity, label-scoped
   obligation resolution, greedy partitions, and one-target fail-safe.
2. Token tests for exact 236-byte/315-character length; rejection of padding,
   whitespace, invalid/standard-alphabet alternates, alternate encodings of the
   same decoded bytes, truncated/extended/wrong decoded layouts, and v1 tokens;
   every field and byte mutation; invalid offsets/limits; forged non-boundary
   offset; target-limit omission/equality/mismatch; partition recomputation;
   artifact/request/filter mismatch; and no raw workflow call.
3. Page-table/index mutations including negative/out-of-range/duplicate
   indices, repeated assumption occurrences, literal table mutation, and
   missing action/obligation digest.
4. Resolver tests for all collections, byte-aware fill, exact union, raw digest
   before redaction, path scanning, artifact mutation, exact canonical scope
   reconstruction, cross-target/global/null/collection rejection, independent
   record limits 1 and 100, empty/invalid offset behavior, and no raw workflow
   call.
5. Zero/one/two/three-target page-union tests with requested limits 1, 2, 20,
   and 100; exact source order; no-artifact all-target fallback.
6. CLI/facade/FastMCP registered-tool tests, exact structured content/fixed
   text, absent `outputSchema`, stdio serialization, migration behavior, and
   surface synchronization.
7. Publication quarantine, Phase 06 action, P08C1 target-fidelity, and frozen
   replay adjacency.
8. Formal card/risky replay of all pages and 90 resolver pages with exact
   measurements, forged tokens, mutations, and no-artifact fallback.
9. Focused `py_compile`, `git diff --check`, inspected diff, and one substantive
   independent implementation/result review before Phase 08 closure.

## Required Artifacts

- response compiler/cursor/resolver and public surfaces;
- focused tests and migration docs;
- refreshed feasibility program;
- formal P08D create/verify replay runner;
- fresh P08D evidence bundle under
  `.local/mathdevmcp/evidence/p08-20260714/p08d/<run-id>/`;
- Phase 08D result and independent review record;
- refreshed Phase 09 plan only after all Phase 08 criteria pass.

## Forbidden Claims And Actions

- Do not modify P08A, P08B, P08C, or passing P08C1 evidence.
- Do not rerun document audit, doctor, SymPy, Sage, Lean, retrieval, proof
  search, a model, network, or GPU operation in P08D.
- Do not edit frozen source documents or comparator reports.
- Do not raise byte limits, reorder/shop targets, drop global IDs, substitute
  unexplained counts/digests, truncate actions, omit label-scoped obligations,
  or accept dangling/non-reconstructable tokens.
- Do not introduce an implicit artifact directory when `artifact_root=None`.
- Do not enable publication/promotion/applicable repairs, defaults, releases,
  installs, commits, or pushes.
- Do not claim proof, whole-document correctness, best repair, Phase 08 closure
  before review, or mission completion.

## Handoff And Stop Conditions

Implementation may launch after substantive plan review finds no material
baseline, token, action, resolver, byte, compatibility, or claim-boundary
defect. Formal replay may launch after focused and adjacent tests pass and the
implementation diff is inspected.

P08D and Phase 08 pass only if every production page/resolver/public envelope
meets its limit, exact union/parity and privacy pass, no-artifact mode is
complete, P08A/P08B/P08C1 remain unchanged, and substantive result review has
no material finding. Then draft/review/launch Phase 09 automatically.

If a complete one-target page or one complete resolver record exceeds its
limit, preserve it and close P08D product-incomplete. If any semantic field,
action, obligation, or resolver binding is omitted or unreconstructable,
classify the repair unsafe and do not advance.

Repair ordinary implementation, test, replay, serialization, or documentation
defects locally. Stop for user direction only if the remaining choice changes
the registered byte target, public default/API direction beyond this reviewed
v2 migration, scientific interpretation, frozen corpus, publication/release,
privacy, permissions, cost, destructive/irreversible state, or project
direction.
