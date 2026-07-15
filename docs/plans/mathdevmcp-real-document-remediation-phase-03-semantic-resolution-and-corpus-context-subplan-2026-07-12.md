# MathDevMCP Real-Document Remediation Phase 03 Semantic Resolution And Corpus Context Subplan

Date: 2026-07-12

Status: `REPAIRED_PENDING_INDEPENDENT_PLAN_REVIEW_R2`

Master program:
`docs/plans/mathdevmcp-real-document-mission-remediation-master-plan-2026-07-10.md`

Master-plan SHA-256:
`5166192908f2a370a88538c07fefe79df984999059d85671087ddcc06a5b4182`

## Phase Objective

Replace the current source-local keyword/role heuristics with a bounded,
provenance-complete corpus-context system that distinguishes source support,
candidate assumptions, ambiguity, incomplete search, completed absence, and
engineering failure without making mathematical claims.

Phase 03 passes only if the 14 eligible inherited P02 obligations receive
deterministic context-search manifests, the two ambiguous and one orphaned
obligations receive deterministic extraction-veto manifests with zero semantic
traversal, every source-supported context claim is connected to the entry
document by a valid dependency path and exact source span/digest, and symbol,
assumption, and report states preserve uncertainty rather than turning
retrieval or lexical similarity into semantics or proof.

## Entry Conditions Inherited From Phase 02

All entry bindings are immutable inputs to Phase 03 planning and execution:

```text
P02_STABLE_DECISION_REF=.local/mathdevmcp/evidence/p02r3-20260712/phase-results/P02-decision.json
P02_STABLE_DECISION_SHA256=f97b1a3a2faa02a661d69ee7b44620e1a8babb2669c7cafada89bf39c1c3db3d
P02_TERMINAL_RECEIPT_INDEX_REF=.local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/receipts/receipt-index-24.json
P02_TERMINAL_RECEIPT_INDEX_SHA256=8f56a72b4575ee3c87122c8656931d7bbb5040a5a3c024edb5f2909b81a78fd0
P02_EXTRACTION_BUNDLE_INDEX_REF=.local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/extraction-bundle/bundle-index.json
P02_EXTRACTION_BUNDLE_INDEX_SHA256=19776da1c8c9a548b19dcf6123a10af8755ab56355801b337847e1563995dc0d
P02_OBLIGATIONS_REF=.local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/extraction-bundle/obligations.json
P02_OBLIGATIONS_SHA256=5aa6681e215d12f382e96f46f9f695cf80e1632affa0dd8bc39069eae78d85a0
P02_EXTRACTION_BUNDLE_SEMANTIC_DIGEST=98dfaf84155723500dd2065cad4837ddea93a688273bb427b946a68172498395
P02_CLOSE_REF=docs/plans/mathdevmcp-real-document-remediation-phase-02-label-scoped-extraction-close-2026-07-12.md
P02_CLOSE_SHA256=cdd9b708c18f3f5ea99d1a6e026d3c20f1b9cfa2fca2d7dbe21e329033c4a01b
```

Entry validation must independently reopen the stable hard link and final
candidate, verify inode/byte equality, reconstruct the 24-receipt terminal
chain, require `decision: pass`, `publication_mode: disabled`, all 13 P02
criteria true, all 18 vetoes false, all eight P02 non-claims present, exactly 17
unique inherited obligations, and zero P02 backend/source-edit counts.

The repaired entry validation must also reopen and digest-bind the immutable R1
`REVISE` review and blocker. It measures the exact running CPython version from
`sys.version_info`; requires the reviewed executable and prefix; resolves the
interpreter's exact `purelib` through `sysconfig`; requires exactly one
case-normalized pytest distribution through standard-library
`importlib.metadata`; and opens its expected `dist-info/METADATA` path using
`O_NOFOLLOW`, requiring regular bytes and the reviewed digest. The entry record
requires the discovered distribution root to equal that exact dist-info
directory and parses `Name`/`Version` again from the exact hashed bytes. It
binds the measurement method, executable, prefix, Python and pytest versions,
purelib, distribution path, metadata path, byte count, and metadata SHA-256. A
declared or hard-coded version without this observation is forbidden evidence
provenance.

The 17 inherited obligation digests are the exact ordered list in the P02
bundle. The four frozen-document obligations are:

| File | Label | Obligation digest |
| --- | --- | --- |
| `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex` | `eq:incremental-cash-flow` | `7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0` |
| same file | `eq:incremental-npv` | `d9f072ac09016b17d5630556329bc871e79386a442c8c26587ef39a0134eeaac` |
| `docs/risky-debt-maliar-deep-learning-lecture-note.tex` | `eq:foc-k` | `d987e605da2d4e509d0d65289a56e9b7f5d121273543bdf74276b9fb4c23bba5` |
| same file | `eq:foc-b` | `8d04797cf7e394624890ab2e0b0688f22d86d9194de94af3aa1407fb1a45edca` |

The remaining 13 fixture obligations remain extraction/context adversarial
inputs. Across all 17 records, exactly 14 are `valid_complete` and
adapter-eligible, two are `ambiguous` and ineligible, and one is `orphaned` and
ineligible. The three ineligible records enter Phase 03 only as explicit
extraction-veto manifests: they bind the P02 bytes/state and record zero
semantic traversal or support claims. The 14 validated records receive bounded
context searches. No Phase 03 result may omit an inherited digest, treat an
extraction veto as a semantic gap, or replace a P02 record with a newly
re-extracted broader target.

## Current-Code Gap Audit

The pre-plan audit found these concrete gaps in current code:

1. `latex_index._discover_input_order` starts from every sibling `.tex` file,
   silently ignores missing/out-of-root includes and cycles, and returns only a
   flattened order. `build_index(path.parent)` therefore indexes 11 `.tex`
   files for the frozen card entry and 34 for the risky-debt entry even though
   neither entry document contains `\input` or `\include`. Unrelated drafts can
   become context merely because they share a directory.
2. `document_derivation_tree._local_statement_status` and
   `_requirement_status` use regex/keyword matches in a local paragraph window.
   They promote nearby lexical matches to `nearby_stated` and turn local
   non-matches into `missing` without a bounded corpus search or dependency
   relevance check.
3. `_source_ref` permits missing file/line/label fields and synthesizes an
   evidence ref from whatever is available. A `source_supported` claim needs
   exact file, byte/line span, label or enclosing node, source digest, and
   dependency path; `None:<line>`-style provenance must be rejected.
4. `math_ir._typed_role` assigns roles from spelling and whole-text keywords,
   while `_UNRESOLVED_PATTERNS` treats every `\pi` as posterior syntax. In the
   frozen card document, the source explicitly defines `\pi` as the assumed
   downstream policy, so the current heuristic can misclassify a real symbol.
5. `RepairAssumptionStatus` has one legacy `status` field. It cannot express
   the master schema's orthogonal support and encoding states, stable
   assumption identity, subjects, formal predicate, and blocker links.
6. `_top_ranked_branch_context`, gap reports, and Markdown renderers group
   `missing`/`unresolved` and `stated`/`nearby_stated`, allowing parser,
   retrieval, notation, candidate-assumption, mathematical, and engineering
   states to collapse into one narrative.
7. Existing tests assert legacy states such as `nearby_stated`, `missing`, and
   `posterior_candidate`. A safe migration needs explicit compatibility output;
   changing production semantics while leaving these consumers implicit would
   create schema drift.

Baseline evidence is green but does not answer the Phase 03 question:
`tests/test_latex_index.py`, `tests/test_math_ir.py`, and
`tests/test_notation_reconciliation.py` pass 31 tests. Test count is explanatory
only.

## Skeptical Plan Audit

- Wrong baseline avoided: the baseline is the current local-window and
  directory-wide heuristic behavior, not the P02 stable pass or green unit
  tests. P02 established source ownership, not context correctness.
- Proxy metrics rejected: fewer missing assumptions, more retrieved nodes,
  higher symbol confidence, test counts, report size, and reviewer agreement
  cannot promote Phase 03. Exact state/provenance fidelity is primary.
- Stop conditions are explicit below. Missing includes, incomplete search,
  ambiguous notation, and budget exhaustion remain typed diagnostics; invented
  provenance, source drift, context leakage, and engineering errors treated as
  mathematics are vetoes.
- Fair comparison: local-window baseline and dependency resolver consume the
  same inherited P02 obligation and frozen source bytes. The plan does not
  compare different targets or call fewer reported gaps an improvement.
- Hidden assumptions exposed: sibling files are not corpus dependencies;
  lexical matches are candidates, not support; a search can be incomplete; and
  source support is not mathematical sufficiency or proof.
- Stale context controlled: Phase 03 entry records exact P02 artifacts, code
  baseline digests, frozen source digests, and a new implementation manifest.
- Environment matched: CPython 3.11.15 with `PYTHONPATH=src`, CPU-only local
  parsing. No GPU, network, installer, model call, or mathematical backend is
  required.
- Artifact fitness: per-obligation search manifests preserve searched and
  unsearched boundaries, dependency paths, exact source refs, symbol candidates,
  typed assumptions, vetoes, and non-claims. A summary count cannot substitute.

Audit decision: `PASS_TO_DRAFT_AND_REVIEW_PHASE_03_ONLY`. Execution remains
closed pending independent plan agreement and sufficient later review budget.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Entry-file reachability defines the corpus | Master P03 dependency requirement plus current sibling-leak audit | Context must be causally connected to the requested document | Relevant externally supplied root is omitted, or unrelated drafts leak in | sibling-decoy, nested-include, missing-include, cycle, and out-of-root fixtures | Reviewed engineering default |
| Exact `\input`/`\include` edges only in this phase | Master work package P03-W1 | Deterministic, source-visible dependency relation | Macro-generated includes are missed | record `unsupported_include_form` and `not_searched`; do not claim absence | Scoped reviewed baseline |
| Frozen entries search one reachable file | Both frozen entries contain zero include commands | Whole reachable closure is one file and avoids sibling leakage | A hidden dependency exists only by prose or build tooling | manifest records zero include edges and all unsearched siblings | Target-specific reviewed default |
| Card byte ceiling `469323`, risky byte ceiling `117506` | Sealed source byte counts | Exactly covers each one-file reachable closure | Source changes or accidental second-file search | source digest/byte-count check before search | Target-specific reviewed default |
| Fixture default: at most 8 files, 256 nodes, 1 MiB, 64 dependency expansions | Smallest bounded adversarial ladder, not empirical promotion evidence | Covers nested/cyclic/missing include fixtures without unbounded traversal | Complex corpus exhausts budget and appears absent | explicit `budget_exhausted`, unsearched files/nodes, no `not_found_after_search` | Baseline hypothesis |
| Dependency relevance precedes lexical score | Master P03 contract | Prevents irrelevant prose from closing a context node | True support has weak lexical overlap | source-supported requires typed edge plus applicability reason; ambiguous otherwise | Reviewed default |
| No scalar confidence threshold promotes a role | Current heuristic failure and master ambiguity requirement | A score cannot establish symbol meaning | Arbitrary threshold silently converts candidate to fact | all candidates retain evidence; conflicts/ties remain ambiguous | Reviewed default |
| Explicit scoped override has highest candidate priority but remains provenance-bound | Master P03-W3 | Users need a controlled discriminator | Global override contaminates other files/labels | scope mismatch and mutate-one-scope tests | Reviewed default |
| Support and encoding are orthogonal | Normative `TypedAssumption` schema | Source support does not imply backend encoding or mathematical sufficiency | `source_supported` silently becomes executable/proved | one mutation test per support/encoding transition | Reviewed default |
| Publication/backend/source edits stay disabled | P00-P02 handoff | P03 is classification only | Semantic result crosses into proof or repair | guard ledger, zero counts, P00 quarantine tests | Inherited hard boundary |

## External-Tool-First Consideration Ledger

| Tool | Possible role | Availability/version evidence | Selected in P03 | Reason |
| --- | --- | --- | --- | --- |
| Current byte-preserving locator/P02 obligations | Exact target/source boundary | P02 stable evidence and parser version `p02_lightweight_locator@1` | Yes | Required substrate; P03 must not re-expand target ownership |
| Repository-native source scanner | Includes, labels, references, definition/assumption/notation candidates | Existing `latex_index` and exact source bytes | Yes, repaired | Phase question is source/corpus dependency accounting |
| LaTeXML `0.8.6` and Pandoc `2.9.2.1` | Diagnostic structural hints | Exact P02 raw version/source receipts | No live invocation | P02 found only malformed or non-source-mappable outcomes; they cannot provide exact P03 provenance |
| SymPy/SageMath | Algebra/domain checks | Considered by project policy | No | Context classification precedes mathematical checking |
| Lean | Certification of a formal scoped claim | Considered by project policy | No | P03 produces no Lean statement or certifying claim |
| LeanSearch-v2/LeanExplore | Premise retrieval | Considered by project policy | No | Source-corpus context is not yet a Lean goal or library premise query |
| jixia | Lean static extraction | Considered by project policy | No | No Lean source exists in scope |
| Pantograph/LeanDojo | Lean proof-state/search interaction | Considered by project policy | No | P03 forbids proof search and backend execution |

No new in-house mathematical search algorithm is introduced. The native work
is bounded source dependency/provenance orchestration. External mathematical
tools become relevant only after later formalization and cannot certify P03
context classifications.

## Work Packages

### P03-W1: Entry-Rooted Corpus Dependency Graph

Add `src/mathdevmcp/document_context_graph.py`. Extend `latex_index` with an
entry-rooted discovery API without changing P02 obligation bytes.

The new API accepts an explicit normalized workspace/corpus root and exact
entry-file ref. A relative `../shared.tex` include may be followed only when its
no-follow resolved target remains within that declared root. Merely sharing a
directory never creates an edge. Preserve the existing directory-wide
`build_index(root)` behavior for legacy diagnostic consumers; add an explicit
entry-rooted route and require it in all P03 code. A P03 context request without
an exact entry ref fails closed rather than falling back to the legacy sibling
scan.

Source scanning inherits P02 byte discipline: strict UTF-8, exact raw byte
spans, escaped-percent-aware LaTeX comment handling, no macro expansion, and no
normalization of mathematical source merely to create an identity. Unsupported
macro-generated or unbraced include forms are recorded as unsearched
engineering diagnostics.

Required graph contract:

- entry file logical ref and SHA-256;
- one file node per reachable regular non-symlink `.tex` file, with logical ref,
  SHA-256, byte count, exact full-file line/byte span, parse state, and entry
  reachability;
- typed nodes for labels/references, propositions, definitions, assumptions,
  notation declarations, and sections, each with exact file/source digest and
  non-null byte/line span;
- typed edges for `input`, `include`, `contains`, `labels`, `references`,
  proposition-to-equation, and explicit declaration/alias relations;
- diagnostics for missing include, cycle, duplicate label, unsupported include
  form, symlink, path traversal/out-of-root edge, decode failure, and source
  drift;
- `considered_files`, `reachable_files`, and `excluded_sibling_files` kept
  separate.

Missing/cyclic/unsupported include edges are engineering diagnostics. They block
claims that require the affected path but do not refute any mathematical
statement and do not automatically fail unrelated reachable nodes. Symlink and
out-of-root traversal are integrity vetoes.

Required tests:

- `test_cross_file_definition_is_retrieved_by_dependency`;
- `test_duplicate_labels_remain_file_scoped`;
- `test_missing_include_is_engineering_diagnostic`;
- `test_unrelated_sibling_tex_is_excluded_from_entry_corpus`;
- `test_include_cycle_is_bounded_and_recorded`;
- `test_out_of_root_and_symlink_include_are_integrity_vetoes`;
- `test_every_context_node_has_digest_and_exact_span`.

### Canonical P03 Identities

All P03 identity payloads use the Phase 01 canonical JSON rules. Derived ids
and runtime/artifact paths are excluded from their own identity payloads:

```text
context_node_id = "ctx_" + sha256(canonical(entry_source_digest, node_kind,
                                             source_file, byte_span,
                                             declaration_key))
context_edge_id = "edge_" + sha256(canonical(edge_kind, from_node_id,
                                               to_node_id, source_span))
corpus_graph_digest = sha256(canonical(entry_ref, entry_source_digest,
                                        ordered_nodes, ordered_edges,
                                        ordered_diagnostics))
context_request_digest = sha256(canonical(obligation_digest, corpus_graph_digest,
                                           requirement_predicate,
                                           required_edge_kinds, budget))
context_search_manifest_digest = sha256(canonical(sealed search manifest
                                                    excluding only this digest))
symbol_candidate_id = "sym_" + sha256(canonical(symbol, proposed_role, scope,
                                                  evidence_kind, evidence_refs))
```

Node/edge arrays are ordered by UTF-8 logical ref, byte start, kind, and id.
Search order and ranked candidates are ordered evidence, not set-like data.
Typed-assumption predicate/binding identities follow the master schema exactly.
Mutating one source digest/span, dependency edge, budget, state, role, support,
or encoding field must change the corresponding downstream digest.

### P03-W2: Bounded Context Resolver

Implement `build_context_dependency_graph` and
`resolve_context_requirement` in the new module. Replace production calls to
`build_local_context_graph` with the new resolver; keep an explicitly named
legacy adapter only where old diagnostic consumers still require it.

Each request binds an inherited obligation digest, entry source digest,
requirement id/predicate, required node/edge kinds, and a predeclared budget.
Each result records:

- files/nodes/bytes/edges considered and searched;
- exact dependency path for every candidate/supporting source ref;
- unsearched files/nodes and why;
- budget exhausted state;
- ranked candidates with relevance reason and lexical evidence kept separate;
- terminal context state: `stated`, `source_supported`, `ambiguous`,
  `not_found_after_search`, `not_searched`, or `candidate_assumption`;
- engineering diagnostics, vetoes, and non-claims.

For an inherited `ambiguous` or `orphaned` extraction record, the manifest has
`entry_state: extraction_veto`, repeats the exact P02 state/ambiguity refs,
records zero searched nodes and zero semantic candidates, and is ineligible for
symbol, assumption, or context-support resolution.

`not_found_after_search` is legal only when the complete predeclared reachable
closure for that requirement was searched with no relevant engineering
diagnostic. Budget exhaustion or unsupported/unopened dependency paths force
`not_searched`. A keyword match without a valid dependency/applicability path
is at most a candidate and can never become `source_supported`.

Required tests:

- `test_not_searched_never_becomes_missing`;
- `test_not_found_requires_completed_search`;
- `test_context_budget_records_unsearched_files`;
- `test_keyword_match_without_dependency_does_not_source_support`;
- `test_irrelevant_same_section_text_does_not_close_requirement`;
- `test_missing_include_blocks_only_dependent_context_claims`;
- `test_resolver_is_deterministic_under_file_creation_order`.

### P03-W3: Confidence-Bearing Symbol And Notation Resolution

Replace `_typed_role`'s single unconditional result with candidate records that
contain symbol spelling, role, scope, evidence kind, exact source refs,
applicability reason, priority class, and resolution state. Integrate
`reconcile_notation` as an ambiguity-preserving comparator; do not overwrite
duplicate symbol records or choose the first alias candidate.

Evidence precedence is explicit scoped override, exact declaration/definition,
explicit alias, dependency-linked use-site/prose, then lexical heuristic.
Lexical evidence alone never resolves a role. Conflicting candidates remain
`ambiguous`; absent evidence remains `unknown`/`not_searched` according to the
search manifest.

Remove `\pi` from the unconditional posterior unresolved-pattern rule. In the
frozen card entry, `\pi` must resolve as an assumed downstream policy from the
exact definition at lines 249-264 or remain ambiguous if the supporting path is
withheld. It must never become posterior solely from spelling. Existing HMC
posterior tests must use explicit posterior evidence rather than `\pi` alone.

Required tests:

- `test_pi_is_not_unconditionally_posterior`;
- `test_card_pi_resolves_policy_or_ambiguous`;
- `test_explicit_override_has_provenance_and_scope`;
- `test_override_cannot_leak_to_another_file_or_label`;
- `test_conflicting_roles_remain_ambiguous`;
- `test_duplicate_alias_candidates_are_not_first_match_resolved`;
- `test_lexical_role_is_candidate_not_fact`.

### P03-W4: Normative Typed Assumption States

Replace `RepairAssumptionStatus` output in the P03 route with the master
`TypedAssumption` schema:

- `assumption_id`, derived only from kind, subjects, human predicate, and formal
  predicate;
- `predicate`, `formal_predicate`, `kind`, and `subjects`;
- `support_state` in exactly `stated`, `source_supported`,
  `candidate_assumption`, `ambiguous`, `not_found_after_search`, or
  `not_searched`;
- exact `source_refs`, empty for candidates/unsearched records;
- `encoding_state` in exactly `encoded`, `not_encodable`, `not_yet_encoded`, or
  `not_applicable`;
- `closes_blocker_ids`.

Support and encoding changes must alter the binding payload without changing
the predicate-derived assumption id. Candidate assumptions cannot become
stated through repetition, lexical match, backend availability, or later branch
success. P03 performs no actual backend encoding, so `encoded` is accepted only
for an explicitly supplied, validated existing formal predicate; otherwise use
`not_yet_encoded` or `not_applicable`.

Required tests:

- `test_candidate_assumption_does_not_become_stated`;
- `test_source_supported_requires_exact_ref`;
- `test_not_found_requires_completed_search`;
- `test_none_line_provenance_is_rejected`;
- `test_assumption_id_stable_across_support_state_change`;
- `test_binding_digest_changes_with_support_or_encoding_state`;
- `test_source_support_does_not_imply_encoded_or_mathematically_sufficient`.

### P03-W5: Semantic Packet And Report Boundary

Update document semantic packets, branch inputs, gap/partial-evidence records,
coverage summaries, compact views, and Markdown rendering to keep separate:

- extraction/parser ambiguity;
- context search state and engineering diagnostics;
- notation/symbol ambiguity;
- source-supported and source-stated assumptions;
- candidate assumptions;
- mathematical route requirements/gaps;
- encoding/formalization blockers;
- backend evidence (empty in P03);
- interpretation/non-claims.

Do not expose legacy `nearby_stated` or bare `missing` as normative P03 states.
If a compatibility view is retained, name it `legacy_context_status`, derive it
from normative fields, label it diagnostic/deprecated, and forbid downstream
promotion or mathematical classification from consuming it.

Affected context engineering errors veto the target before any backend route.
They do not become mathematical blockers, refutations, or candidate
assumptions. Reports must say what was searched and what was not searched.

Required tests:

- `test_compiler_preserves_context_state_distinctions`;
- `test_engineering_context_error_vetoes_target`;
- `test_not_searched_is_rendered_as_unsearched_not_missing`;
- `test_parser_ambiguity_is_not_rendered_as_math_gap`;
- `test_candidate_assumption_is_not_rendered_as_source_fact`;
- frozen card/risky context snapshots by ids/states/digests, not prose;
- P00 publication quarantine remains exact.

### P03-W6: Context-Only Evidence And Governance Boundary

Do not use `audit_document_derivation_tree` to generate formal P03 evidence.
That legacy route initializes doctor/backend capability state and enters branch
orchestration, even when a focused test name mentions only context. Add a
context-only API that consumes the exact sealed P02 obligation records plus an
entry file and returns only corpus graph, search manifests, symbol candidates,
typed assumptions, report-state ledgers, and non-claims. It must have no import
or call path to doctor, backend adapters/controllers, hypothesis expansion,
formalization, promotion, or repair compilation.

Add `src/mathdevmcp/context_evidence.py` for strict canonical schemas and
independent artifact reconstruction, `scripts/generate_p03_context_evidence.py`
for no-replace formal generation, `tests/p03_no_backend_guard.py` for formal
process/import/source-write interception, and `scripts/p03_governance.py` for
the append-only state machine. The generator no-follow loads the exact guard
bytes bound by the round implementation manifest before importing any P03
production module.

Move the P03 semantic-packet/context/report adapter used by
`document_derivation_tree` into the backend-free `context_evidence` module and
make backend-capable `document_derivation_tree` imports lazy. Formal tests may
import and call only that context adapter; they never call
`audit_document_derivation_tree`, doctor, branch controllers, formalizers, or
compilers. The legacy full-audit route remains publication-disabled and outside
P03 formal evidence. Its later branch/backend behavior is owned by Phase 04 and
beyond.

The formal pass action order is exactly:

```text
init_round
context_graph_tests
resolver_tests
symbol_assumption_tests
report_boundary_tests
frozen_context_regressions
p00_quarantine
generate_context_bundle
mutation_gate
zero_backend_source_edit_gate
compile
protected_check
implementation_exit
allowlist
diff
bind_result
build_run_manifest
build_candidate
candidate_gate
result_review_binding
build_final_candidate
final_candidate_gate
final_seal_audit_binding
stable_publication
```

Failure-only suffix actions are `bind_scoped_repair` then `close_round`.
Every invoked action appends exactly one no-overwrite receipt and receipt index,
including a nonzero child result. After the first failed local action, only the
reviewed evidence/repair/close suffix is legal. `REVISE` review/audit verdicts
enter the same append-only close route. A stable link with failed terminal
sealing is human recovery and is never retried.

All test subprocesses run with exact clean environment, plugin autoload
disabled, and `-p tests.p03_no_backend_guard`. The guard rejects imports of
backend/doctor/controller modules from the context-only import closure,
mathematical backend invocations, subprocess/network/GPU/install paths, and
writes to the two frozen sources. The context generator runs under the same
guard and must record zero forbidden attempts. Test selection is by exact
context-only file registry, not an open-ended `-k` expression that could
accidentally enter backend orchestration.

The governance CLI accepts only these normalized operations:

```text
p03_governance.py init-round --round-root <fixed rr0[1-5] ref>
p03_governance.py run --round-root <same ref> --action <registered action>
p03_governance.py run --round-root <same ref> --action result_review_binding --artifact-ref <exact round review ref>
p03_governance.py run --round-root <same ref> --action final_seal_audit_binding --artifact-ref <exact round audit ref>
```

Equal-sign arguments, abbreviations, extra/repeated arguments, caller-supplied
dispatch variables, shell execution, and unregistered actions are rejected
before mutation. Subprocess actions receive only `HOME`, `LANG`, `LC_ALL`,
`PATH`, `PYTHONHASHSEED=0`, `PYTHONPATH=src`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, fixed P03 action/round/depth variables, and
round-local `TMPDIR`. Receipts bind schema/phase/round/sequence/action, fixed
external argv, exact child argv/environment digest or native handler id,
start/end/wall time, exit code, prior receipt digest, stdout/stderr refs,
digests/counts, artifact ref for review actions, and action-specific bindings.
Receipt indexes are immutable contiguous prefixes; action ids cannot repeat in
a round.

Fixed formal refs use
`.local/mathdevmcp/evidence/p03-20260712/result-rounds/RESULT_ROUND/` for
round-local artifacts,
`docs/plans/mathdevmcp-real-document-remediation-phase-03-semantic-resolution-and-corpus-context-result-RESULT_ROUND-2026-07-12.md`
for human results,
`docs/reviews/mathdevmcp-real-document-remediation-phase-03-result-review-RESULT_ROUND-result-2026-07-12.md`
and the corresponding `final-seal-audit` ref for reviews, and
`.local/mathdevmcp/evidence/p03-20260712/phase-results/P03-decision.json` for
the disabled no-overwrite stable link.

Required tests:

- `test_context_only_api_has_no_backend_or_doctor_import_path`;
- `test_formal_guard_rejects_backend_import_and_source_write`;
- `test_generator_reopens_manifest_bound_guard_before_production_import`;
- `test_inherited_obligations_partition_into_14_search_and_3_extraction_veto_manifests`;
- `test_candidate_reconstructs_without_trusting_summary_counts`;
- one-field receipt/artifact/ledger mutation per primary criterion and veto.

## Implementation Delta Allowlist

Only these code/test paths may be added or modified during Phase 03
implementation:

```text
src/mathdevmcp/document_context_graph.py
src/mathdevmcp/context_evidence.py
src/mathdevmcp/latex_index.py
src/mathdevmcp/document_derivation_tree.py
src/mathdevmcp/math_ir.py
src/mathdevmcp/notation_reconciliation.py
scripts/generate_p03_context_evidence.py
scripts/p03_governance.py
tests/p03_no_backend_guard.py
tests/fixtures/document_context_graph/**
tests/test_context_evidence.py
tests/test_document_context_graph.py
tests/test_document_context_resolver.py
tests/test_context_real_regressions.py
tests/test_latex_index.py
tests/test_document_derivation_tree.py
tests/test_document_derivation_real_regressions.py
tests/test_math_ir.py
tests/test_notation_reconciliation.py
```

Changes outside this list require a visible reviewed plan amendment before
editing. In particular, do not modify P02 sealed plans/oracles/bootstrap,
P02 stable evidence, frozen source documents, backend adapters/controllers,
promotion policy, MCP/CLI interfaces, package environments, or release policy.

The reviewed plan, entry bootstrap, agreeing plan review, and later review
artifacts are immutable after binding and are never implementation paths.
Governance may create, never overwrite, only the fixed budget-authorization,
round result/review/close, P03 evidence-root, terminal close, execution-ledger,
and stop-handoff artifacts named by this plan. Those are supervisor/governance
outputs, not an authorization to edit arbitrary `docs/plans`, `docs/reviews`,
or `.local` paths.

## Required Artifacts

Before implementation:

- this reviewed subplan and one exact-digest agreeing plan review;
- `docs/plans/p03_entry_bootstrap_20260712.py`, reviewed at the same exact
  digest as this plan;
- a P03 entry record binding every P02 entry value, plan/review bytes, dirty
  implementation baseline, frozen source digests, allowlist, Python/pytest
  runtime measurement provenance, CPU-only declaration, and review budget;
- no-write entry preflight followed by one no-replace entry allocation;
- a protected/immutable manifest covering P00-P02 decisions/evidence, frozen
  sources, reviewed plan/review, and all out-of-scope dirty paths.

The fixed Phase 03 evidence root is
`.local/mathdevmcp/evidence/p03-20260712`. Before review, the bootstrap must pass
its no-write `--mode preflight` branch while that root is absent. After plan
agreement, it still must not allocate the entry until the fixed
`docs/plans/mathdevmcp-real-document-remediation-phase-03-review-budget-authorization-2026-07-12.json`
exists and strictly records one reserved result-review round and one separately
reserved final-seal-audit round. That authorization record documents user
authority; it is not a cryptographic signature or review verdict. The one-shot
`--mode create` branch binds its exact bytes/digest into the entry and refuses
any pre-existing P03 root or partial output.

The authorization file is strict canonical JSON with no extra keys. Its exact
schema and fixed values are:

```json
{
  "authority": "human_user",
  "date": "2026-07-12",
  "final_seal_audit_rounds_reserved": 1,
  "non_claim": "Review budget is execution authority only, not a technical verdict or signature.",
  "phase": "P03",
  "plan_review_sha256": "<SHA-256 of the fixed agreeing Phase 03 plan-review bytes>",
  "plan_sha256": "<SHA-256 of this exact reviewed Phase 03 plan>",
  "result_review_rounds_reserved": 1,
  "schema_version": "p03_review_budget_authorization@1"
}
```

Both digest fields must be lowercase 64-hex values equal to the reopened fixed
artifacts. The file is written only after an agreeing plan review and before
entry creation; it is then immutable and cannot be replenished or reinterpreted
inside a result round.

For each formal result round:

- append-only command receipts and indexes;
- exact implementation manifest and allowlist/diff/protected checks;
- corpus graph plus integrity/diagnostic ledger;
- exactly 14 context-search manifests for `valid_complete`/adapter-eligible P02
  records and exactly three extraction-veto manifests for the two `ambiguous`
  and one `orphaned`/adapter-ineligible records, covering all 17 inherited
  obligation digests exactly once;
- symbol-resolution ledger and notation-conflict ledger;
- typed-assumption bundle with canonical ids/binding digests;
- parser/context/mathematical/engineering/interpretation ledgers;
- zero-backend and zero-source-edit guard attestations;
- focused/mutation/frozen-result artifacts;
- twelve-section human result, machine result, run manifest, candidate,
  independent result review, final candidate, separate final-seal audit, and
  disabled-mode stable decision.

The result artifact must include a run manifest with git commit, exact command,
CPython environment, CPU/GPU state, P02 data/artifact versions, seed policy
(`N/A`, deterministic parsing), wall time, all output refs, plan/result refs,
and exact implementation delta digest.

The entry runtime measurement is engineering provenance, not environment
fitness or scientific evidence. The reviewed expected values are CPython
`3.11.15`, prefix `/home/chakwong/miniconda3/envs/tfgpu`, purelib
`/home/chakwong/miniconda3/envs/tfgpu/lib/python3.11/site-packages`, pytest
`9.0.2`, metadata path `pytest-9.0.2.dist-info/METADATA`, and metadata SHA-256
`14131718cc1f40cfecb5eac338037029a519b6392876100afec1e949f023d1ed`.
Changing any value or finding duplicate/missing pytest distributions is a
pre-entry provenance failure, not permission to select another installation.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can the exact 17 P02 obligations be enriched with bounded corpus context and typed semantic uncertainty without inventing support or collapsing search/notation/engineering states into mathematical claims? |
| Exact baseline | P02 stable obligations plus current directory-wide `build_index(path.parent)`, local paragraph regex statuses, spelling-based `_typed_role`, first-match notation aliases, legacy `RepairAssumptionStatus`, and merged gap rendering. |
| Primary pass criterion | The 14 `valid_complete`/adapter-eligible inherited obligations receive deterministic context-search manifests and the two `ambiguous` plus one `orphaned`/adapter-ineligible obligations receive deterministic extraction-veto manifests with zero semantic traversal; all 17 inherited digests are covered exactly once; every `source_supported`/`stated` record has valid exact provenance and dependency applicability; all search/support/encoding/symbol/report states obey their closed schemas; frozen card `\pi` is policy or ambiguous, never posterior-by-spelling; affected engineering errors veto before math/backend routing. |
| Veto diagnostics | P02 binding/source drift; sibling-context leakage; invented or incomplete provenance; `None:<line>`; out-of-root/symlink acceptance; local absence as corpus absence; `not_searched` rendered missing; irrelevant keyword support; unconditional role resolution; candidate assumption rendered stated; context error rendered mathematical; any backend/source edit/publication leak; allowlist or receipt failure. |
| Explanatory only | Number of retrieved nodes, fewer gap counts, lexical scores, role-candidate counts, wall time, test counts, and review agreement. |
| Not concluded | No context-search completeness beyond recorded budgets; no semantic equivalence, sufficient/minimal assumptions, mathematical closure, proof/refutation, backend fitness, general LaTeX support, repair publication, Phase 04 readiness, or release readiness. |
| Preserved artifact | P03 entry, per-obligation search manifests, corpus/symbol/assumption/ledger bundles, append-only receipts, human/machine result, reviews, disabled stable decision, and exact P04 handoff if passed. |

## Required Checks And Tests

Pre-entry local checks:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest tests/test_latex_index.py tests/test_math_ir.py tests/test_notation_reconciliation.py -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest tests/test_document_derivation_real_regressions.py -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m py_compile src/mathdevmcp/latex_index.py src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/math_ir.py src/mathdevmcp/notation_reconciliation.py
/usr/bin/env -i HOME=/tmp/mathdevmcp-p03-entry-home LANG=C.UTF-8 LC_ALL=C.UTF-8 PATH=/usr/bin:/bin PYTHONHASHSEED=0 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -B -S docs/plans/p03_entry_bootstrap_20260712.py --mode preflight
git diff --check
```

Post-implementation focused ladder, smallest first:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest tests/test_document_context_graph.py -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest tests/test_latex_index.py tests/test_math_ir.py tests/test_notation_reconciliation.py -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q -p tests.p03_no_backend_guard tests/test_context_evidence.py tests/test_context_real_regressions.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest tests/test_document_publication_quarantine.py tests/test_label_scoped_obligation.py tests/test_extraction_evidence.py -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m py_compile src/mathdevmcp/document_context_graph.py src/mathdevmcp/latex_index.py src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/math_ir.py src/mathdevmcp/notation_reconciliation.py
git diff --check
```

Mutation checks must alter one fact at a time and prove rejection or state
downgrade for: removed source digest, null file/line, broken dependency edge,
unsearched file omitted from manifest, keyword-only candidate promoted,
candidate assumption relabeled stated, `\pi` relabeled posterior without
evidence, scoped override widened, support state changed without binding digest
change, engineering diagnostic moved to math ledger, and publication/backend
count made nonzero.

Any broader suite failure must be classified before use. The two known
unrelated P02-era broad regressions are not silently accepted as P03 passes;
only a failure proven outside the P03 allowlist and behavior contract may be
quarantined with exact evidence.

## Pre-Mortem

How the phase could pass while misleading us:

- it searches all sibling files, finds plausible words, and reports improved
  support; the sibling-decoy fixture and entry-reachability manifest expose it;
- it searches only a local window, exhausts budget, and calls absence missing;
  the unsearched-boundary mutation exposes it;
- it attaches a real source span that is irrelevant to the requirement; typed
  dependency/applicability paths and irrelevant-keyword fixtures expose it;
- it replaces one hard-coded symbol role with a hidden confidence threshold;
  candidate/conflict tests require no score-only promotion;
- it emits normative fields but reports merged legacy prose; compact/Markdown
  parity tests inspect every state/veto by id;
- it preserves P02 obligation count while substituting new targets; exact
  ordered obligation-digest binding exposes it.

How the phase could fail for engineering rather than scientific reasons:

- unsupported macro-generated includes, missing files, decode errors, source
  drift, budget exhaustion, or bad provenance. These remain explicit
  engineering/context diagnostics; they do not refute a source or mathematical
  claim.

Cheapest discriminating diagnostics are the isolated graph fixtures, canonical
round trips, one-field mutations, and one frozen target per document before the
full 17-obligation evidence build.

## Review And Repair Loop

Phase 03 plan review R1, bound at SHA-256
`4e4c2c235f53b035ec4a5780f02165a4662630782e3f5862a524edbd4ab9cd03`,
returned `REVISE` because pytest `9.0.2` was represented as measured entry
provenance without bootstrap measurement. Its blocker SHA-256 is
`0b76111e955eb6e555b9bb711ad4c876ed487ad878cbe53f62a63021d7eedf90`.
The user authorized one additional fresh, bounded, read-only Codex repaired-plan
review on 2026-07-12. That R2 review must bind both R1 artifacts and the repaired
plan/bootstrap bytes. One later result-review round and one different
final-seal-audit round remain separately reserved because the Claude route
remains policy-unavailable. The two later reservations are materialized only
through the strict authorization record above after R2 agreement.
The review must bind the exact plan and entry-bootstrap SHA-256 values, P02
stable digest, terminal-index digest, bundle semantic digest, P02 close digest,
and master-plan digest, and end with `VERDICT: AGREE` or `VERDICT: REVISE`.

If the R2 plan review says `REVISE`, write the review artifact and a visible
blocker result. Do not edit the reviewed plan under the same digest, do not
execute Phase 03, and ask the user for another review round before a repaired
plan is reviewed. If it says `AGREE`, preserve the reviewed bytes, write the fixed
strict budget-authorization record using the already granted separate result
review and final-seal-audit reservations, and invoke the reviewed one-shot entry
bootstrap. Agreement is not itself implementation or publication authority.

During later execution, every fixable implementation/result finding uses a new
append-only `rrNN` round. Never overwrite or retry a recorded action. A
`REVISE` review is bound, scoped repair is written, the round is closed, focused
checks rerun, and the next round binds the predecessor close/index. Stop after
five non-convergent substantive review rounds for the same blocker or earlier
at any authority/scientific/runtime boundary.

## Forbidden Claims And Actions

- Do not modify any sealed P00-P02 plan, oracle, bootstrap, review, stable
  decision, receipt, parser evidence, or extraction bundle.
- Do not edit either frozen source document or any unrelated dirty path.
- Do not index arbitrary sibling `.tex` files as entry-document context.
- Do not claim corpus absence unless the predeclared reachable closure was
  completely searched without a relevant engineering diagnostic.
- Do not call lexical similarity, nearby prose, a source ref, or a user/agent
  hypothesis semantic proof or mathematical support.
- Do not turn `candidate_assumption`, `ambiguous`, or `not_searched` into
  `stated`, `source_supported`, or `not_found_after_search` without the required
  evidence transition.
- Do not assign `\pi` or any symbol a role from spelling alone.
- Do not treat a context error as mathematical evidence against a claim.
- Do not run SymPy, Sage, Lean, LeanSearch-v2, LeanExplore, jixia, Pantograph,
  LeanDojo, a model/agent generation route, network, installer, GPU, or source
  edit path.
- Do not enable publication, change a default public interface, execute Phase
  04, commit, or push.
- Do not start Phase 03 implementation merely because the plan review agrees;
  the result/final review reserve is a separate human budget boundary.

## Exact Next-Phase Handoff Conditions

Phase 04 planning may begin only after a P03 disabled stable decision
independently reconstructs with:

- exact P02 stable, terminal-index, close, bundle-index, obligations, and
  semantic-digest bindings;
- all 17 inherited obligation digests present exactly once as exactly 14
  context-search manifests plus exactly three extraction-veto manifests;
- all P03 primary criteria true and every veto false;
- each eligible obligation has one valid context-search manifest and each
  ineligible obligation has one zero-traversal extraction-veto manifest;
- every source-supported/stated ref exact and dependency-applicable;
- explicit searched/unsearched boundaries and no state collapse;
- frozen card `\pi` policy/ambiguous and never posterior-by-spelling;
- zero backend requests, source edits, and publication leaks;
- protected/allowlist/receipt chain exact;
- one independently agreeing result review and a separate independently
  agreeing final-seal audit;
- stable decision and final candidate hard-link inode/byte equality;
- `publication_mode: disabled` and inherited non-claims.

The Phase 04 subplan must bind the exact P03 stable and terminal receipt-index
digests and inherit all semantic/mathematical/backend/publication non-claims.

## Stop Conditions

Stop before implementation for a plan `REVISE`, missing result/final review
reserve, P02 binding drift, partial entry state, or unauthorized allowlist
expansion.

Stop during execution for source/P02 artifact drift, missing inherited
obligation, symlink/path traversal, invented/null provenance, sibling context
leakage, state-schema violation, source-support without dependency
applicability, unrecorded budget exhaustion, unconditional symbol role,
candidate/source state promotion, engineering-to-mathematical reclassification,
backend/source-edit/publication activity, protected drift, unexpected path,
receipt failure, or review `REVISE`. Record and close fixable failures; do not
erase or reinterpret them.

## End-Of-Phase Procedure

1. Run the complete reviewed local ladder and mutations.
2. Write the per-obligation artifacts and three-ledger-plus-interpretation
   evidence bundle.
3. Write the twelve-section human result and machine decision candidate.
4. Obtain and bind a fresh result review; repair append-only on `REVISE`.
5. Build/validate the final candidate and obtain a different final-seal audit.
6. Create only the disabled stable hard link and independently verify bytes,
   inode, schema, criteria, vetoes, and non-claims.
7. Write the Phase 03 close, refresh the execution ledger/handoff, and only then
   draft/review Phase 04.
