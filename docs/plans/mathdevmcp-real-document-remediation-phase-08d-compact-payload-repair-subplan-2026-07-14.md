# MathDevMCP Phase 08D Compact Payload Repair Subplan

Date: 2026-07-14

Status: `SUPERSEDED_PENDING_P08C1_TARGET_FIDELITY_REPAIR`

> Supersession note (2026-07-14): the skeptical pre-implementation audit
> found that the immutable P08C card audit represents
> `eq:incremental-cash-flow` with only its final continuation row and with
> `lhs=None`, `rhs=None`. P08A binds the same label to the complete equality
> under obligation digest
> `7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0`.
> The payload baseline is therefore mathematically unfaithful. This plan and
> its feasibility measurements remain diagnostic history only and must be
> refreshed after the P08C1 target-fidelity repair and a fresh frozen replay.

## Phase Objective

Repair the compact document-derivation response so every frozen target can be
consumed through deterministic pages within the 25,600-byte canonical limit
and 30,720-byte CLI/MCP transport limit, while preserving the complete global
claim boundary, exact target associations, one directly usable action on each
current target, and a content-addressed route to every full record.

P08D is a presentation/product repair. It replays the exact independently
verified P08C request and raw-audit mappings. It does not rerun document audit,
doctor, a mathematical backend, retrieval, proof search, or a model.

## Entry Conditions

1. P08A remains `PASS_P08A_FROZEN_EXTRACTION_CONTEXT` in parent run
   `.local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0`.
2. P08B remains independently verified `backend_checked` for only
   `eq:cashflow-rate-derivative`, decision digest
   `8548c8d8e26bf404392fb4a51e7ea483ac7773961bd8897251bf5ec7240ab08c`.
3. P08C continuation
   `.local/mathdevmcp/evidence/p08-20260714/continuations/20260714T080342Z-3a1e3445eeab`
   independently verified with decision digest
   `0c23863c391ef07d7b3f1911bdcee912e640e368343650f168c0bba7e888bbd3`.
4. P08C passed identity, parity, actionability, private-path, engineering,
   zero-backend, and publication-quarantine checks, but failed only
   `compact_product_criterion_not_met`.
5. The replay inputs are immutable and literal:

   | Input | SHA-256 |
   | --- | --- |
   | Card request | `32a7793e5f1674edb2e9690429d2a4998316bd780385bce8867355c61fda3a45` |
   | Card raw audit | `25360385c7fab0012965ac14cf9bdb11eef0687296e9f1ff46c616c882f6fcfd` |
   | Risky request | `fee205368a9af4d2a399d43827352d14830a02ade2e0ba35b3ff7ec231a638be` |
   | Risky raw audit | `010247eb5c1f2532e1ba13d4934fe0dd79106485d69400d1c6031c404cb1c443` |
   | Card persisted artifact | `34605aeab7ee6319f703be806b7a5b9843f155741a92c1efcd25f9ce4ffab082` |
   | Risky persisted artifact | `1661a97b9f62ea0c33dc0441b5f7bac7329c5b3399c31cc9682abdd6d307005f` |

6. Publication, applicable edits, promotion, proof claims, default/release
   changes, network/model use, installs, commits, and pushes remain outside
   scope.

## Skeptical Plan Audit

The P08C failure cannot be fixed by raising the limit, truncating the action,
dropping repeated-but-semantic IDs, or treating a set digest alone as an
explicit veto/assumption list. The wrong baseline would be the 12,970-byte
synthetic Phase 07 payload; the exact P08C audits are the required baseline.
The wrong success proxy would be one small first page; the gate requires every
page, deterministic union reconstruction, and public CLI/facade behavior.

The dominant real-payload costs are repeated full target records, the duplicated
global reference inventory and blocker catalog, and a Phase 06 action whose
byte-identical outcome policy and global-veto memberships repeat on every
target. The exact read-only feasibility program
`docs/plans/p08d_payload_feasibility_spike_20260714.py` uses the closed v2 page
token and registered action-policy projection below. It validates every
expanded action with `validate_discriminating_action` and serializes the actual
`mcp==1.27.0` `CallToolResult` plus a complete stdio JSON-RPC response line.

| Frozen page | Canonical response | CLI + LF | Facade | `CallToolResult` + LF | Full stdio line + LF |
| --- | ---: | ---: | ---: | ---: | ---: |
| Card 0 | 25,151 | 25,152 | 25,161 | 25,291 | 25,325 |
| Card 1 | 25,349 | 25,350 | 25,359 | 25,489 | 25,523 |
| Card 2 | 24,907 | 24,908 | 24,917 | 25,047 | 25,081 |
| Risky 0 | 24,892 | 24,893 | 24,902 | 25,032 | 25,066 |
| Risky 1 | 24,895 | 24,896 | 24,905 | 25,035 | 25,069 |

The worst projected canonical margin is 251 bytes and the worst projected
full-wire margin is 5,197 bytes. This establishes implementation feasibility,
not product promotion: production output must be measured again, and any page
that fits only because a global ID, current-target association, action field,
engineering status, source identity, non-claim, or artifact binding vanished
is invalid. A page token that skips, duplicates, reorders, or reruns a target
is also invalid.

The same program traverses every public record collection with exact
byte-aware resolver batching: 57 card resolver pages and 36 risky resolver
pages when every page-token scope is traversed. After applying the existing
transport redaction, the largest card resolver page is 30,503 canonical bytes
and 30,677 bytes as a full stdio line; the largest risky page is 30,351
canonical and 30,525 full-wire bytes. The smallest resolver wire margin is
therefore only 43 bytes. Production must use
the exact closed resolver schema and byte-aware fill; additional metadata,
pretty JSON, or a partial-record truncation is not permitted.

Before projection, the feasibility program opens the exact `detailed.json`
named by each comparator, verifies canonical bytes, schema, SHA-256, byte
count, request equality, audit/request identities, and equality of its stored
audit to the frozen raw audit after the compiler's exact removal of the sole
top-level `markdown` presentation field. It independently rebuilds the frozen
v1 targets and derived grouped blocker catalog from `record["audit"]`; only
then does it build v2 pages from that stored audit. The grouped catalog is a v1
comparator only, not a record claimed to be stored in the artifact.

Wrong baselines, proxy promotion, hidden defaults, stale P08C bytes,
environment mismatch, unfair all-target-versus-one-target comparison, missing
stop conditions, and commands that would not answer the product question were
checked. Local skeptical verdict: `PASS_WITH_REQUIRED_SCHEMA_AND_REPLAY_TESTS`.

## External-Tool-First Audit

No mathematical external tool is applicable to this presentation repair.
SymPy, Sage, Lean, LeanSearch-v2, LeanExplore, jixia, Pantograph, and LeanDojo
were considered and rejected because P08D neither derives nor certifies a
mathematical claim. The selected route is the existing deterministic Python
response compiler plus canonical JSON measurement and exact replay of verified
P08C mappings. No new search, compression service, or agent-written
mathematical derivation is introduced.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Exact P08C request/audit bytes | Independently verified P08C continuation | Isolates presentation changes from document-audit nondeterminism | New raw result makes size comparison unfair | Verify literal file SHA-256 before import/replay | Hard binding |
| Persisted artifact is the reconstruction source | Existing `p07_document_derivation_artifact@1` records and continuation loader | A page token can resolve only bytes that are actually stored | Feasibility silently depends on a derived compact file rather than the resolver source | Verify canonical bytes/schema/SHA/size/request/IDs and exact stored-audit equality after the documented presentation-field projection before page compilation | Hard binding |
| Response schema major bump | Compact target record shape changes | Prevents old consumers from accepting normalized references as old full records | Silent breaking change under v1 schema | Old-schema fixture rejected with an actionable migration error; v2 public surface asserted | Required compatibility boundary |
| `target_limit` is a maximum | Existing pagination argument | Allows deterministic byte-aware reduction while respecting caller upper bound | Silent target loss or surprising permanent one-target cap | Record requested/effective limits and page union | Reviewed product interpretation |
| Greedy source-order page fill | Deterministic existing target order | Maximizes current-page targets without target shopping | Later target starvation or order drift | Replay all cursors; exact once-only ordered union | Reviewed algorithm |
| At least one target per nonempty page | Agent actionability requirement | Prevents a global-only loop | One target itself exceeds the guardrail | Emit the complete target, mark size exceeded, and fail the gate rather than omit | Hard fail-safe |
| Global veto and unresolved-assumption IDs remain explicit on every page | Master compact contract | These IDs govern interpretation and publication | Digest/count hides which veto applies | Exact list parity against raw audit and detailed view | Hard boundary |
| Candidate-assumption and action-decision IDs remain explicit | P07/P08C parity contract | Preserves branch/action identity | Consumer sees an action without its decision boundary | Exact list parity and removal mutation | Hard boundary |
| Selected action is losslessly expandable from the current target | Phase 06 validated action contract | The frozen actions share one exact registered policy; variable branch and veto memberships remain inline | A convenient action is projected despite differing from the registered policy, or expansion changes its semantic ID | Require exact fixed-field equality before projection, reconstruct the full mapping, and run `validate_discriminating_action`; otherwise transport the full action | Hard boundary |
| Full repeated assumption/blocker/reference records live in verified detailed artifact in artifact-backed compact mode | P07 artifact architecture and P08C diagnosis | Avoids duplicating multi-kilobyte records in every page | Page token is dangling, ambiguous, or digest-only without resolution | Reopen artifact by SHA-256 through the public resolver and reconstruct exact target set from the page token | Reviewed normalization |
| Global veto and assumption IDs remain literal; targets use checked integer memberships | Exact global lists already appear on every page | Preserves target association without repeating multi-kilobyte strings | Index is out of range or expands to another target's ordered ID list; repeated semantic IDs hide distinct records | Expand the ordered membership including repetitions; separately bind every raw record by `(identity, raw_record_sha256)` in the page token and resolver | Reviewed compact representation |
| Target blocker/reference sets use literal page-table entries plus checked integer memberships | Full blocker/ref strings dominate the budget when repeated, but the active contract requires literal identifiers | Preserves exact membership and direct agent resolution without hash substitution | Table entry or index is changed, duplicated, or points to another target | Expand every index and compare literal sets to the raw target; mutate one table row and one index | Reviewed compact representation |
| One `page_token` serves continuation and record resolution | Cursor and selector otherwise repeat the same artifact/page bindings | Saves about one opaque token while retaining closed independent reconstruction | Resolver authority becomes broader than the current page or a forged offset is accepted | Token binds the complete page partition and all current-page/global collection identities; resolver accepts only named collections reconstructed from the artifact | Reviewed closed capability |
| Global blocker/reference records are paginated through the page token | Master permits evidence-record pagination; exact frozen global inventories cost 16-19 KB before targets | Keeps current-target literals inline and every global record publicly resolvable | Counts/digests are mistaken for the identities or resolver cannot enumerate them | Resolver must return the complete ordered identity list page-by-page; union equals the detailed artifact | Reviewed v2 API supersession |
| Global blocker collection contains exact pre-redaction blocker records | The artifact stores audit records; the v1 `blocker_catalog` is a grouped presentation projection | Makes resolver parity independently reconstructable without claiming derived groups are stored | A grouped catalog or normalized substitute is falsely treated as raw artifact content | Walk `record["audit"]`, derive an ID only when absent, deduplicate only exact identity/digest pairs, and order by canonical binding; retain the grouped catalog only as a v1 comparator | Hard representation boundary |
| Target content identity binds existing nested records | Frozen targets contain a semantic-work-packet ID, typed-repair and math-obligation ID/records, source span, and target text | Meets P08C source/obligation identity without inventing IDs or transporting a 42-61 KB packet | Label/row alone aliases changed mathematics; digest-only content cannot be inspected | Inline existing IDs and canonical typed/math-obligation, span, and target digests; resolve every bound record except the oversized packet container itself | Reviewed compact representation |
| No-artifact compact mode remains inline-complete | Current CLI/MCP `artifact_root=None` default | Avoids silently introducing a write location or returning a dangling page token | Target pagination strands omitted targets or normalized refs cannot resolve | With no artifact, include all targets inline, expose no continuation/resolver token, and report any honest size overage | Compatibility-safe fallback, not the frozen size-promotion route |
| Artifact-backed compact mode is the bounded route | Existing optional `artifact_root` and master frozen commands | Supplies stable bytes for continuation and record resolution | Users assume omitted `artifact_root` still permits bounded continuation | CLI/MCP docs and response state say bounded pagination requires a verified artifact | Reviewed migration |
| FastMCP v2 data is structured-content-only | Duplicating full JSON in text defeats the transport budget | Keeps one authoritative machine-readable payload | Content-only clients receive only a pointer and silently lose the result | Remove `outputSchema`, assert exact fixed text and `structuredContent`, document this breaking migration, and test CLI/facade alternatives | Intentional experimental API break |
| Canonical limit 25,600; public transport limit 30,720 | Master plan | Preserves intended agent-context product | Pretty/envelope output passes canonical only or vice versa | Measure canonical JSON, compact CLI JSON plus newline, facade `ok` envelope, and pinned FastMCP `CallToolResult` wire JSON; largest representation drives page fill | Hard product criterion |
| No general compression codec | Agent-facing usability | Opaque zlib/base64 would fit but make direct consumption worse | Payload passes while becoming unusable | Schema remains ordinary JSON with named fields | Reviewed exclusion |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the exact P08C card and risky audits be represented as deterministic compact pages that remain evidence-complete and directly actionable within both registered byte limits? |
| Baseline/comparator | Exact P08C request/audit bytes above; P08C compact sizes 159,837/131,379; P08C detailed mappings and artifacts as semantic comparators. |
| Primary criterion | Every artifact-backed page validates; canonical JSON, compact CLI JSON plus one LF newline, facade `ok` envelope, actual pinned FastMCP `CallToolResult`, and the complete stdio JSON-RPC response line are within their registered limits (25,600 canonical; 30,720 transport); ordered union contains every target exactly once; exact global status/promotion/coverage/failure/veto/assumption/action/non-claim identities repeat unchanged; every current target has exact veto and assumption memberships, source/obligation identity, one losslessly expandable and validated action, literal blocker/evidence/source identities represented once in page tables with checked integer memberships, and a publicly resolvable page token; global blocker/reference resolution unions equal the detailed artifact; publication remains disabled. No-artifact mode must remain inline-complete and fail size honestly rather than omit. |
| Veto diagnostics | P08C input drift; schema not bumped; undocumented no-artifact behavior; raw audit/backend/doctor/model/network execution; target omission/duplication/reorder; page loop; forged canonically valid non-boundary page token; token/request/artifact mismatch; global or target veto/assumption/action ID omission; missing literal blocker/evidence/source table entry or membership; action expansion/ID mismatch; absent public resolver; page-token grammar or reconstruction mismatch; unredacted resolver path; MCP version mismatch; canonical or transport overage in artifact-backed replay; publication/promotion/applicable repair. |
| Explanatory only | Savings ratio, pages per document, pretty bytes below the transport limit, catalog cardinality, and field-level byte attribution. |
| What will not be concluded | No new mathematical evidence, proof, whole-document correctness, best repair, complete assumptions, publication/default/release readiness, or general size guarantee outside the frozen audits and tested fixtures. |
| Preserved artifact | Schema/compiler/resolver diff and tests; a P08D replay bundle containing input bindings, every compact page, page-token resolution results, detailed comparator, page-union/parity record, byte measurements, public-envelope measurements, and decision; result and independent substantive review. |

## Closed V2 Representation And Resolver Contract

The v2 response has two explicit compact representations:

1. `artifact_indexed`: allowed only when `artifact.state == verified`; supports
   byte-aware target pages and one dual-purpose continuation/resolution token.
2. `inline_complete`: used when `artifact_root` is absent; returns every target
   with the existing full current records, never issues a page token,
   and reports `exceeded_complete_boundary_preserved` if the complete response
   is too large. It may exceed the caller's `target_limit` to avoid stranding
   targets without a continuation. The response records requested and
   effective limits and the reason.

No implicit artifact directory is introduced. CLI and MCP keep
`artifact_root=None` as a valid default, but documentation must state that a
verified artifact root is required for bounded multi-page compact transport.
This is a representation/schema migration, not a change to audit execution or
publication defaults.

Artifact-indexed targets replace repeated full records with these closed
fields. Literal identifiers remain in the response exactly once in named page
tables; targets use integer memberships into those tables, so v2 does not
substitute hashes for identifiers:

| Field | Meaning |
| --- | --- |
| `page_identity_tables.blocker_ids` | Literal blocker IDs for the current page, deduplicated in canonical order. |
| `page_identity_tables.evidence_refs` | Literal evidence refs for the current page, deduplicated in canonical order. |
| `page_identity_tables.source_ref_ids` | Literal source-ref IDs for the current page, deduplicated in canonical order. |
| `target.*_indices` | Checked integer membership into the corresponding page table; expansion must equal the raw target set exactly. |
| `target.veto_indices` | Checked membership into the literal global `veto_ids` list. |
| `target.*_assumption_indices` | Checked membership into the literal global unresolved/candidate assumption lists. |
| `target.content_identity` | Exact semantic-work-packet, typed-repair-obligation, and nested math-obligation IDs plus raw canonical SHA-256 values for the two obligations, source span, and target text. |
| `page.page_token` | Strict artifact/page/collection-bound token accepted by continuation and the public resolver. |

The compact response retains literal global veto, unresolved-assumption,
candidate-assumption, and action-decision ID lists. Per-target veto and
assumption indices expand into the exact ordered target ID list, including
repeated indices when distinct records share a semantic ID. Literal
current-page blocker/evidence/source identifiers appear once in the page
tables. Semantic IDs are not assumed unique record keys: the frozen candidate
assumptions contain 19/21 records but only 10/11 unique IDs, and blocker records
also reuse IDs. Therefore every record-bearing collection in the page token is
an ordered list of closed bindings with exactly `identity` and
`raw_record_sha256`, where the digest is over the raw canonical record.
The resolver reconstructs that list from the persisted audit before returning
redacted records; duplicate bindings are invalid, while repeated identities
with distinct record digests are valid. The v2 schema supersedes the v1
requirement that every target and global reference inventory repeat every
record: target memberships are checked indices and all records are enumerated
through the public resolver. This is permitted evidence-record pagination, not
a digest-only substitute.
For blocker collections, the raw record SHA-256 is computed before adding any
presentation identity: an existing nonempty `id` is used, otherwise the
identity is `blocker_` plus the raw record digest. Exact identity/digest pairs
are deduplicated and canonically ordered; records sharing an ID but differing
in bytes remain distinct. Selected actions likewise come from the persisted
audit, never from the compact comparator.

Each artifact-indexed target has exactly these keys:

```text
target_id label row_id row_index location content_identity status
publication_mode promotion_ref failure_classification_indices veto_indices
unresolved_assumption_indices candidate_assumption_indices
unresolved_assumption_record_count candidate_assumption_record_count
blocker_record_count blocker_indices evidence_ref_indices source_ref_indices
selected_action
```

`content_identity` has exactly `semantic_work_packet_id`,
`typed_repair_obligation_id`, `typed_repair_obligation_sha256`,
`math_obligation_id`, `math_obligation_sha256`, `source_span_sha256`, and
`target_text_sha256`. The semantic packet ID preserves
the existing artifact identity; the four digests bind independently
resolvable complete records. These are exact P08C artifact-record identities,
not a retroactive claim that they equal the earlier Phase 02
`LabelScopedObligation.obligation_digest`, which is not propagated into P08C.
The full semantic packet is 42-61 KB in the
frozen inputs and is not falsely advertised as one bounded resolver record.

The frozen Phase 06 actions may use
`p08d_unresolved_choice_action_policy@1` only when every fixed field is
byte-equal to the registered mapping: schema, action kind, ledger binding,
prerequisite, tool route, budget, expected artifact, all eight outcome records,
and both non-claims. The only projected values are the original `action_id`,
the checked equality `target_ids == branch_ids`, the literal branch IDs, and
`launch_veto_indices` into global `veto_ids`. The compact view also exposes the
action kind, prerequisite, and expected-artifact kind directly. Expansion must
reconstruct the exact original mapping and pass `validate_discriminating_action`
with the original `action_id`; any fixed-field mismatch forces full-action
transport. Fallback actions are transported in full.

The page token is canonical unpadded URL-safe base64 over canonical JSON plus a
checksum. After checksum removal its keys are exactly:

```text
schema_version                 p08_document_derivation_cursor@2
selector_schema_version        p08d_document_derivation_selector@1
audit_result_id                audit_<64 lowercase hex>
audit_request_id               request_<64 lowercase hex>
artifact_sha256                64 lowercase hex
filter_id                      filter_<64 lowercase hex>
byte_policy_version            p08d_compact_byte_policy@1
requested_target_limit         integer 1..100
page_boundary_digest           digest of the canonical page-boundary record recomputed from offset zero
page_index                     zero-based page number
previous_offset                exact predecessor offset (zero for the first page)
next_offset                    exact byte-policy boundary after this page
scope_collections_digest       digest of the complete closed global/current-page collection map
```

The artifact-indexed response has exactly these top-level keys:

```text
metadata response_schema_version response_mode compact_representation
response_status authority audit_result_id audit_request_id audit_status status
audit_status_source source_ref publication_mode promotion coverage
failure_classifications veto_ids unresolved_assumption_ids
candidate_assumption_ids action_decision_ids non_claims execution_summary
output_references artifact record_inventory page_identity_tables targets page
completeness payload_guardrail canonical_byte_count
```

The v1 `reference_inventory` and derived `blocker_catalog` fields are replaced
only in `artifact_indexed` compact responses by `record_inventory`, literal
page identity tables, and public resolver collections. The v1 status aliases
and `output_references` remain because they are small compatibility and
boundary fields.

`inline_complete` has exactly the v1 compact top-level key set plus
`compact_representation`, with the exact v1 `reference_inventory`, derived
`blocker_catalog`, and complete v1 target records. Its `page` has exactly
`offset`, `limit`, `requested_limit`, `effective_limit`,
`limit_override_reason`, `included_target_count`, `total_target_count`,
`target_ids`, `next_cursor`, `continuation_available`, and `filter_id`.
`offset=0`; `requested_limit` is the validated caller value; `effective_limit`,
`limit`, and both target counts equal the complete target count;
`limit_override_reason` is `inline_complete_without_resolver` when the complete
count exceeds the request and `not_required` otherwise; `next_cursor` is null;
and `continuation_available` is false. Its exact v1 `payload_guardrail` gains
only `transport_target_byte_count` and `transport_status`; canonical `status`
and transport status are independently `met` or
`exceeded_complete_boundary_preserved`. It emits no page token and validates
against the same raw audit. Detailed and artifact-only modes retain their
current complete field sets and semantics under response schema v2; they do
not acquire `compact_representation`, compact normalization, target paging, or
resolver tokens.

Its nested objects are also closed. `artifact` has exactly `state`,
`schema_version`, `sha256`, `byte_count`, and `authority`; `record_inventory`
has exactly `global_blocker_record_count`, `global_evidence_ref_count`,
`global_source_ref_count`, and `resolution`; `page_identity_tables` has exactly
`blocker_ids`, `evidence_refs`, and `source_ref_ids`; `page` has exactly
`page_index`, `previous_offset`, `next_offset`, `requested_limit`,
`effective_limit`, `included_target_count`, `total_target_count`, `target_ids`,
`continuation_available`, `filter_id`, `byte_policy_version`,
`page_boundary_digest`, and `page_token`; `completeness` has exactly
`global_boundary`, `current_target_identities`, and
`global_and_full_records`; `payload_guardrail` has exactly
`canonical_target_bytes`, `transport_target_bytes`, `status`, and `authority`.
Production may not add optional keys to these measured objects without a fresh
feasibility measurement and plan review.

The page-boundary record has exactly `response_schema_version`,
`artifact_schema_version`, `compact_representation`, `byte_policy_version`,
`canonical_limit`, `transport_limit`, `requested_target_limit`, `page_index`,
`previous_offset`, `next_offset`, `target_ids`, and `filter_id`. The closed
collection map has `global` keys `global_blocker_records`,
`global_evidence_ref_records`, and `global_source_ref_records`; `targets` maps
each current target ID to exactly `blocker_records`, `evidence_ref_records`,
`source_ref_records`, `unresolved_assumption_records`,
`candidate_assumption_records`, `selected_action`, `typed_repair_obligation`,
`math_obligation`, `source_span`, `target_text`, and the exact non-record
`content_identity` map.
Each record collection
is an ordered list of the two-key identity/digest binding above. The selected
action collection is a one-item binding for the exact raw Phase 06 action.

The decoder rejects alternate base64 spellings, extra/missing keys, unknown
schema versions, malformed identities, and a noncanonical checksum.
Continuation receives the current page token through the existing
`target_cursor` input, requires the caller's `target_limit` to equal the bound
`requested_target_limit`, recomputes the complete greedy partition from offset
zero, and compiles the page beginning at the token's `next_offset`. The final
page token remains valid for record resolution but is rejected as a
continuation because `next_offset == total_target_count`. The public library,
CLI, facade, and FastMCP operation `resolve_document_derivation_records`
accepts:

```text
artifact_root   required existing safe local root
page_token      required strict token
target_id       current-page target ID, or null for a global collection
collection      unresolved_assumption_records |
                candidate_assumption_records |
                selected_action | typed_repair_obligation | math_obligation |
                source_span |
                target_text | blocker_records | evidence_ref_records |
                source_ref_records | global_blocker_records |
                global_evidence_ref_records | global_source_ref_records
offset          nonnegative integer
limit           1..100
```

It opens only the exact artifact named by the token, validates its canonical
bytes, schema, SHA-256, byte count, request equality, result/request identities,
and stored audit identity, then reconstructs the selected target/scope from the stored raw
audit, and returns a deterministic page containing redacted transport
projections of the exact identities and records, total/returned counts, next
offset, and the independently recomputed collection identity list and
`scope_collections_digest`. Every returned record carries its raw canonical
record SHA-256 and artifact binding; raw absolute paths never cross the public
resolver. It never reads the source document or calls the raw workflow, doctor,
a backend, network, or model. Frozen resolver results must also remain under
the 30,720-byte public-envelope limit; if one complete redacted record cannot
fit, the operation returns an explicit product overage without truncating it.

The resolver response schema is `p08d_document_derivation_record_page@1` and
has exactly these keys before the facade adds `ok: true`:

```text
schema_version
authority                       diagnostic_presentation_only
audit_result_id
audit_request_id
artifact                        exact verified schema/SHA-256/byte-count binding
page_index
target_id                       requested current-page target ID or null
collection
offset
limit
total_record_count
returned_record_count
records                         ordered redacted record projections
next_offset                     integer or null
scope_collections_digest
payload_guardrail               30,720-byte resolver-envelope status
non_claim                       resolver records are evidence navigation, not proof or publication authority
```

Each `records` entry has exactly `identity`, `raw_record_sha256`, and
`record`; `record` is the redacted transport projection of the complete raw
record, while the SHA-256 is computed before redaction. For literal string
collections, the raw record is that JSON string. The page refuses duplicate
identity/digest pairs, preserves distinct records sharing an identity, checks
`returned_record_count == len(records)`, and returns `next_offset` only when
more records remain. If the exact requested `offset` is beyond the collection,
it returns a structured invalid-arguments error rather than an empty success.
The same repository `_ABSOLUTE_PATH_FRAGMENT` regex used by the response
transport scans the entire serialized resolver success and error surfaces, not
only known workspace or artifact-root substrings.

## Compatibility And Wire-Byte Matrix

| Surface | Exact v2 contract | Serialization measured | v1 behavior |
| --- | --- | --- | --- |
| Library/compiler | `p08_document_derivation_response@2`; cursor `p08_document_derivation_cursor@2` | Existing canonical UTF-8 JSON helper, no newline | v2 compiler never emits v1; legacy v1 cursor is rejected with an actionable migration error |
| CLI compact | Same v2 response | Canonical UTF-8 JSON plus exactly one LF; compact command no longer indents | Clients dispatch on `response_schema_version`; v1 artifacts remain readable for migration |
| Facade | Existing output contract name `document_derivation_response`, value is v2 response plus `ok: true` | Canonical UTF-8 JSON of exact facade object, no newline | Same dispatch field; no silent relabeling of v1 |
| FastMCP | Registered tool returns `CallToolResult`; `outputSchema` absent; `structuredContent` is exact facade v2 object; one fixed `TextContent` message is `MathDevMCP structured result; read structuredContent.` | Under pinned `mcp==1.27.0`, measure both `CallToolResult.model_dump_json(by_alias=True, exclude_none=True)` plus LF and the actual `JSONRPCMessage(JSONRPCResponse(...)).model_dump_json(by_alias=True, exclude_none=True)` stdio serialization plus LF | Intentional breaking change for content-only MCP clients: they receive only the fixed pointer and must migrate to `structuredContent`, the CLI, or the facade; v1 cursors are rejected; schema/migration tests assert absent `outputSchema` and exact text |
| Persisted artifact | `p07_document_derivation_artifact@1` remains page-token-readable | Existing canonical artifact bytes, exact SHA-256 | No rewrite or mutation of P08C/v1 artifacts |
| Page token | Cursor `p08_document_derivation_cursor@2` with resolver capability `p08d_document_derivation_selector@1` | Strict canonical unpadded base64 token | No v1 resolver token exists; reject v1 cursors with an actionable migration error |

Canonical serialization for the response, facade, and JSON-RPC envelope is:

```python
json.dumps(
    value,
    ensure_ascii=False,
    allow_nan=False,
    sort_keys=True,
    separators=(",", ":"),
).encode("utf-8")
```

The page-fill algorithm computes all five response/envelope sizes above for
each candidate page and applies 25,600 bytes to the canonical response and
30,720 bytes independently to CLI, facade, `CallToolResult`, and full stdio
wire. The P08D
manifest records MCP version. Anything other than the repository-pinned
`mcp==1.27.0` is a setup veto, not an implicit comparator.
Production tests must call the actually registered FastMCP tool through its
manager/low-level conversion and serialize the resulting `JSONRPCMessage`;
constructing an equivalent `CallToolResult` by hand is feasibility evidence
only and cannot close the wire contract.

## Required Implementation

1. Bump the response and cursor schema major versions, define the
   `artifact_indexed` and `inline_complete` variants, and document rejection of
   legacy cursors plus the artifact-backed migration route.
2. Keep detailed and artifact-only semantics intact except for the explicit
   response-schema version and any shared metadata needed for parity.
3. In artifact-indexed mode, replace full compact assumption records with
   checked per-target memberships into exact literal global ID lists. Preserve
   repeated memberships and bind every distinct raw record by identity/digest
   through the page token; never infer record uniqueness from an assumption ID.
   Bind each target to its exact semantic-packet/typed-obligation IDs and raw
   canonical obligation/source-span/target-text digests, and expose the latter
   three complete records through the resolver.
4. Keep exact per-target veto membership and a lossless selected-action
   projection. Indices may reference literal global/page tables, but expansion
   must reproduce the exact Phase 06 action, pass its validator, and preserve
   its semantic `action_id`. Fallback actions remain fully usable and
   explicitly presentation-only.
5. Replace repeated blocker/evidence/source record arrays with literal
   page-table entries, checked target memberships, and the strict page token
   above. A bare count/hash/set digest is invalid.
6. Remove the duplicated derived blocker catalog and global reference strings from
   artifact-indexed transport. Preserve their full records in detailed/artifact
   and inline-complete modes; expose raw blocker/reference counts plus the
   page-token resolver, whose paginated identity/digest union must equal records
   independently reconstructed from the persisted audit. Do not claim the
   grouped v1 blocker catalog is directly stored in the artifact.
7. Make compact pagination byte-aware: include the longest source-order prefix
   not exceeding the caller's `target_limit` and both product limits. If no
   target fits with the global boundary, include one complete target, mark the
   size failure, and stop advancement.
8. Bind the page token directly to audit result, request, artifact bytes,
   filter, byte-policy version, requested limit, page index, previous/next
   offsets, and both recomputed page-boundary and collection-map digests. The
   boundary digest binds response/artifact schemas, representation, limits, and
   exact target IDs. Continuation
   verification must reconstruct the complete byte-aware partition from offset
   zero and reject a canonically checksummed token for any non-boundary,
   skipped, duplicated, or reordered page. It must not call the raw workflow.
9. Add the closed public page-token decoder and
   `resolve_document_derivation_records` operation to the library, CLI, facade,
   FastMCP surface, and documentation. Resolver calls must be read-only and
   independently reconstruct every returned collection from artifact bytes and
   return only redacted public records bound to raw-record digests.
   The decoder must validate canonical artifact bytes, schema, SHA-256, byte
   count, request equality, and audit/request identities before record use.
10. Preserve no-artifact mode as inline-complete: no page token, no cursor, no
   stranded target, and honest overage classification.
11. Add a bounded replay script that verifies the exact P08C inputs, compiles
   and traverses every page, measures canonical and public envelopes, verifies
   every page-token collection through the public resolver, exercises no-artifact fallback,
   and writes a new P08D result bundle outside the immutable P08C continuation.

## Required Checks

1. Focused response tests for both v2 representations, exact global parity,
   target membership, complete Phase 06 actions, individual content identities,
   page-token reconstruction, adaptive pagination, one-target oversize fail-safe,
   cursor strictness, forged-valid-offset rejection, partition recomputation,
   and path quarantine.
2. Mutation tests removing or changing each global ID class, target veto or
   assumption membership or record digest, action field, one individual
   blocker/evidence/source literal table entry/index/record digest, page-token
   checksum/schema/artifact/target/
   collection digest, cursor offset/page index/predecessor/page-boundary/
   schema/representation/byte policy, and publication/promotion field. Include
   negative, out-of-range, and duplicate indices for page tables and action
   launch vetoes; repeated assumption indices remain valid only when their
   ordered identity/digest occurrence list matches the artifact.
3. Page-union tests for zero, one, two, and three targets; requested limits 1,
   2, 20, and 100; exact once-only order; no raw-audit call on continuation;
   no-artifact mode includes all targets and returns no dangling cursor.
4. Public resolver tests across library, CLI, facade, and FastMCP, including
   exact closed input schema, pagination, output byte guardrail, artifact
   mutation, target mismatch, redacted-path/raw-record-digest binding, and
   proof that no raw workflow is called; exact obligation/source-span/target-text
   resolution; and absolute-path-regex scanning of success and error surfaces.
5. CLI, facade, FastMCP schema, MCP-surface, publication-quarantine, Phase 06
   action, and P08C/P08D frozen adjacency. FastMCP tests must assert absent
   `outputSchema`, exact fixed text, exact `structuredContent`, the deliberate
   content-only-client migration, and actual registered-tool/stdio conversion.
6. Exact P08C frozen replay for all card and risky pages, canonical/CLI/facade/
   pinned-FastMCP wire measurements, every public page-token collection, forged
   cursor replay, and the no-artifact inline-complete fallback.
7. `py_compile`, `git diff --check`, and inspected focused diff.
8. One substantive independent review before treating the repaired compact
   product as passed or opening Phase 09.

## Required Artifacts

- updated response compiler plus CLI/facade/FastMCP resolver surfaces;
- focused response/resolver/public-surface tests and migration documentation;
- the reproducible pre-implementation feasibility program
  `docs/plans/p08d_payload_feasibility_spike_20260714.py`;
- `scripts/run_p08d_frozen_payload_replay.py` with read-only P08C input binding
  and create/verify or equivalently independent replay verification;
- P08D replay bundle under
  `.local/mathdevmcp/evidence/p08-20260714/p08d/<run-id>/`;
- Phase 08D result and substantive review record;
- refreshed Phase 09 plan only after every Phase 08 criterion passes.

## Forbidden Claims And Actions

- Do not modify the P08B parent run or P08C continuation.
- Do not edit either frozen document or comparator report.
- Do not rerun raw document audit, doctor, SymPy, Sage, Lean, retrieval, proof
  search, a model, or a network service in P08D.
- Do not raise the byte limits, change the frozen focus targets, or choose an
  easier page after seeing results.
- Do not replace explicit global/target veto or assumption IDs with only counts
  or digests.
- Do not truncate or weaken the validated Phase 06 action to pass size.
- Do not accept an unresolved or non-reconstructable page token.
- Do not issue a page token or continuation when no verified artifact exists.
- Do not enable publication, promotion, applicable repairs, default/release
  changes, source edits, install, commit, or push.
- Do not claim proof, whole-document correctness, best repair, mission
  completion, or general compactness beyond the evidence contract.

## Exact Handoff Conditions

Phase 08D implementation may begin after skeptical plan review finds no
material baseline, feasibility, schema, artifact, or claim-boundary defect.
The frozen replay may launch after focused and adjacent tests pass and the
implementation diff is inspected.

Phase 08 may close and Phase 09 planning may open only when:

1. every artifact-indexed card and risky compact page is within 25,600 canonical
   bytes and the actual CLI, facade, `CallToolResult`, and complete stdio
   JSON-RPC line are each within 30,720 bytes;
2. all pages independently validate and their union reconstructs the exact
   P08C target order without rerunning the audit;
3. global and per-target parity, every individual blocker/evidence/source
   identity, complete action, public page-token reconstruction, no-artifact
   inline completeness, privacy, engineering, and publication boundaries pass;
4. P08A and P08B retained evidence remains unchanged;
5. substantive independent result review returns no material finding.

If safety/parity passes but any complete one-target page still exceeds the
limit, preserve it and close P08D as product-incomplete. If a claim-boundary
field is omitted or a page token cannot reconstruct, classify the repair as
unsafe and do not advance.

## Stop Conditions

Repair ordinary schema, cursor, test, replay, or measurement defects locally
and repeat focused checks. Stop for user direction only if the remaining
choice changes the registered byte target, public default/API direction,
scientific interpretation, frozen corpus, publication/release authority,
privacy, permissions, cost, irreversible state, or project direction. Stop
immediately on immutable-artifact mutation, source-document edit,
mathematical/model/network execution, or publication enablement.
