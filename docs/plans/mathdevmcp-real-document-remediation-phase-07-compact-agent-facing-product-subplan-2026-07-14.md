# MathDevMCP Real-Document Remediation Phase 07 Subplan

Date: 2026-07-14

Status: `SKEPTICAL_AUDIT_PASS_READY_FOR_EXECUTION`

## Phase Objective

Make the completed document-derivation audit usable through CLI and MCP within
an agent context window without weakening its evidence, assumption, veto,
source-provenance, action, or non-claim boundaries.

Phase 07 is a bounded product/presentation phase. It compiles views from an
already completed audit result. It does not alter extraction, context
resolution, branch expansion, backend routing or execution, evidence reading,
ranking, promotion eligibility, or source documents.

The intended product contract is:

```text
completed document audit
  -> response compiler
       -> compact (default CLI/MCP)
       -> detailed (compatibility/debugging)
       -> artifact_only (small transport, complete global boundary)
  -> optional canonical detailed artifact
```

Publication remains disabled in every response mode.

## Governing Policy And Superseded Clauses

This phase follows
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md` and the
project `AGENTS.md` policy.

The following Phase 07 clauses in the 2026-07-10 master plan are stale and are
not execution requirements:

- a verified aggregate P00-P06 cryptographic gate manifest;
- `publication_mode` or `promotion_gate_manifest` CLI/MCP arguments;
- experimental publication exposure in Phase 07;
- content-addressing every plan, review, or command transition.

The scientific and safety clauses remain active: publication quarantine,
explicit assumptions and provenance, exact evidence identity where a claim
depends on it, external-tool boundaries, no source edit, and no promotion of a
diagnostic response into proof.

## Entry Conditions

1. Phase 06 is closed with
   `PASS_ENGINEERING_SELECTION_AND_ELIGIBILITY_CONTRACT` in
   `docs/plans/mathdevmcp-real-document-remediation-phase-06-failure-ledgers-ranking-action-selection-result-2026-07-14.md`.
2. The Phase 06 repaired-plan rereview verdict is `AGREE`.
3. The native reader remains the authority at every eligibility-bearing use;
   this phase may display its results but may not cache or recreate authority.
4. Document repair publication is disabled and remains disabled throughout
   this phase.
5. The existing dirty worktree is intentional and must be preserved. No
   unrelated file may be reverted or reformatted.
6. No real document, external mathematical backend, GPU, network service, or
   external reviewer is needed for the implementation gate.

## Scope

### In scope

- Add `src/mathdevmcp/document_derivation_response.py` as a pure response
  compiler over a completed `document_derivation_tree_audit` mapping.
- Add `compact`, `detailed`, and `artifact_only` response modes.
- Make `compact` the CLI, facade, and FastMCP default while retaining an
  explicit `detailed` compatibility mode.
- Deduplicate blocker prose while preserving every blocker id and affected
  target id.
- Preserve complete global sets of veto ids, unresolved-assumption ids,
  decision/action ids, source refs, evidence refs, and non-claims.
- Add deterministic target pagination with an opaque cursor bound to the
  completed audit identity and the presentation-filter identity.
- Resume CLI/MCP pagination from the exact persisted detailed-audit bytes;
  never rerun the audit to serve a continuation page.
- Persist canonical detailed JSON only when an artifact root is explicitly
  supplied.
- Return logical artifact URIs and content metadata, never the absolute local
  artifact path.
- Align CLI, facade, and FastMCP arguments and semantic results.
- Mark the FastMCP tool as structured output if the installed FastMCP surface
  supports the existing `dict` return contract.

### Out of scope

- Changes to `audit_document_derivation_tree` execution or its raw library
  result contract.
- New backend behavior, real-document backend execution, or any Sage, Lean,
  LeanSearch, LeanExplore, jixia, Pantograph, LeanDojo, GPU, or network
  execution. Existing deterministic in-process SymPy calls exercised by the
  current synthetic document-audit regression suite are permitted as Tier 1
  engineering checks only; they are not Phase 07 scientific evidence and may
  not be extended into new backend cases.
- Any source-document edit or candidate repair application.
- Publication enablement, experimental publication, release/default changes,
  or a scientific-capability claim.
- A new in-house mathematical search, derivation, proof, ranking, or promotion
  algorithm.
- Reconstructing or rerunning the missing historical Sage R3 manifest.
- Broad tool-catalog redesign. Tool descriptions may be clarified only where
  necessary to describe the new response modes.

## Required Artifacts

### Code

- `src/mathdevmcp/document_derivation_response.py`
- focused integration edits in:
  - `src/mathdevmcp/cli.py`;
  - `src/mathdevmcp/mcp_facade.py`;
  - `src/mathdevmcp/mcp_server.py`.

### Tests

- `tests/test_document_derivation_response.py`
- focused compatibility updates in existing document-audit, facade, server,
  and surface-sync tests only where the new default requires an explicit
  `response_mode="detailed"`.

### Records

- this subplan;
- a Phase 07 result/close record containing the actual commands, outcomes,
  payload measurements, residual risks, decision table, and next handoff;
- a Phase 08 subplan or a blocker record, drafted only after Phase 07 evidence
  is known.

## Response Contract

### Completed-audit input

The response compiler accepts one already completed audit mapping. It must not
accept a source path, call the audit workflow, execute a backend, or infer a
new mathematical status. The raw library function remains available for
callers that require the existing full audit and Markdown result.

An `audit_result_id` is computed from canonical JSON after removing only
presentation-local fields (`markdown`, `output_md`, and `output_json`). An
`audit_request_id` is separately computed from the canonical normalized values
of every audit-defining input: logical source identity, `focus_labels` in
caller order, `max_labels`, `budget_profile`, `max_attempts`, `backend_env`,
`search_mode`, `grounding_policy`, and `workers`. Output paths, response mode,
artifact root, target limit, and target cursor are presentation inputs and are
not part of this request id. Both ids are presentation/cursor/artifact
bindings, not certificates or promotion authority.

The persisted detailed record has schema
`p07_document_derivation_artifact@1` and contains the canonical audit-request
record plus the completed raw audit without embedded Markdown or explicit
output-path fields. Continuation loads this exact record; it never reconstructs
an audit request from selected result fields.

### Common boundary

Every response mode uses metadata contract `document_derivation_response` and
schema version `p07_document_derivation_response@1`. The MCP facade registry
advertises `document_derivation_response`; detailed mode preserves the raw
audit's original `metadata` as `audit_metadata` rather than advertising the raw
contract as the transport contract.

Every response mode contains:

- response schema and mode;
- `audit_result_id`;
- `audit_request_id`;
- diagnostic audit status and coverage boundary;
- `publication_mode: disabled` and effective promotion false;
- the complete recursively collected veto-id set;
- the complete recursively collected unresolved-assumption-id set, with
  deterministic synthetic ids only when the detailed item lacks an id;
- the complete action/decision-id set exposed by the completed audit;
- all unique non-claims from the completed audit;
- page metadata and a completeness declaration;
- optional logical detailed-artifact metadata.

Reference completeness is split deliberately:

- the common boundary transports a complete global reference inventory:
  unique evidence-reference strings, unique source-reference identities,
  counts, and canonical digests;
- compact targets transport the exact source/evidence reference records needed
  for targets on the current page;
- detailed transport and the persisted detailed artifact resolve every global
  reference to its full record;
- artifact-only does not transport full reference records, but its inventory
  must match the verified detailed artifact and its artifact state must be
  `verified`.

A compact response without a persisted artifact therefore preserves global
identity/completeness and exact current-page refs, but does not claim that
off-page full records are transport-resolvable. It reports that limitation
explicitly.

Global veto, assumption, promotion, coverage, and non-claim summaries are never
paginated or filtered away.

### Compact mode

Compact mode contains the common boundary plus:

- one deterministic summary per target on the current page;
- target id, label, source location/ref, status, failure classifications, veto
  ids, unresolved assumptions, evidence refs, blocker ids, and the selected
  discriminating action when present;
- a clearly marked presentation-only fallback next step only when the
  completed audit supplies no authoritative Phase 06 action;
- a document-level blocker catalog deduplicated by canonical kind, text, and
  scope, retaining all original blocker ids and affected target ids;
- a cursor for the next target page when more targets remain.

No target is treated as closed merely because it is not on the current page.
Coverage counts always refer to the full completed audit.

### Detailed mode

Detailed mode preserves the completed audit's semantic fields and target
ordering, removes embedded Markdown from transport JSON, moves the raw
`metadata` to `audit_metadata`, applies the transport path policy below, and
adds the v1 response metadata/common boundary. The persisted canonical detailed
artifact may retain local paths because it remains local and is never returned
as transport content.

### Artifact-only mode

Artifact-only mode requires an explicit artifact root. It returns the common
boundary and logical detailed-artifact metadata but no target detail page.
The mode is invalid when the detailed artifact cannot be written and verified.

### Artifact behavior

When `artifact_root` is supplied, write canonical detailed JSON under a
response-owned directory keyed by both `audit_result_id` and
`audit_request_id`. Both are required because two distinct audit requests can
legitimately produce identical audit bytes. Refuse a symlinked root or
destination, refuse escape from the resolved root, and never overwrite
different bytes at an existing identity path. Return only a URI such as:

```text
mathdevmcp-artifact://document-derivation/<audit-result-id>/<audit-request-id>/detailed.json
```

The response also returns the detailed artifact SHA-256 and byte count. These
fields establish local byte identity only; they do not certify mathematics.

For a first CLI/MCP request, `artifact_root` is optional unless the requested
mode is `artifact_only` or the caller intends to follow `next_cursor`. A
CLI/MCP continuation request supplies both `target_cursor` and the same
`artifact_root`; the handler decodes the cursor, loads
`document-derivation/<audit-result-id>/<audit-request-id>/detailed.json`, verifies its digest and
identity, recomputes the caller's complete `audit_request_id`, requires equality
with the persisted request, and compiles the next page without calling the
audit workflow. A continuation cursor without `artifact_root`, a
missing/mismatched artifact, or any changed audit-defining argument is rejected.
The pure response compiler may paginate an in-memory completed mapping
directly.

### Transport path and privacy policy

Transport JSON follows this explicit policy:

- top-level and tool-argument `tex_path`/`root` fields become a stable logical
  `mathdevmcp-source://<audit-result-id>/<basename>` reference; absolute source
  paths are not returned;
- source-provenance records retain relative `file`, label, line/byte spans,
  section path, evidence ref, and mathematical snippet; an absolute `file`
  value is replaced by its basename plus the logical source ref;
- backend-environment fields named `executable`, `prefix`, `backend_prefix`,
  `path`, or `path_head` are replaced by availability/version-preserving
  redaction markers; capability state and tool version remain;
- `output_md`, `output_json`, artifact-root, cache, temporary, and manifest
  filesystem paths become typed logical refs or `<redacted-local-path>`;
- evidence ids, evidence logical refs, source labels/spans, mathematical input,
  status, stderr classifications, vetoes, and non-claims are retained unless a
  value itself contains an absolute private path;
- error/detail/free-text strings receive a defense-in-depth replacement of the
  source parent, artifact root, home directory, Python prefix, and absolute
  temporary/backend path substrings.

Redaction occurs only after `audit_request_id`, `audit_result_id`, reference
inventory, and persisted artifact bytes are computed. Semantic parity excludes
only the enumerated local-path representations; ids, status, promotion,
coverage, vetoes, assumptions, actions/decisions, evidence/source identity,
and non-claims must remain equal.

### Pagination

- `target_limit` defaults to 20 and accepts 1 through 100.
- `target_cursor` is opaque to callers.
- The decoded cursor contains a version, audit identity, filter identity, and
  next offset plus an integrity checksum.
- A cursor from another audit, another target ordering/filter, or another
  schema version is rejected.
- Changing `target_limit` does not change audit or filter identity.
- Page union in cursor order equals the unpaginated detailed target order.
- A CLI/MCP cursor never authorizes or triggers a fresh audit or backend run.

## CLI And MCP Arguments

| Surface | Argument | Default | Rule |
| --- | --- | --- | --- |
| CLI | `--response-mode` | `compact` | `compact`, `detailed`, or `artifact_only` |
| CLI | `--artifact-root` | empty | Optional explicit local parent; required for `artifact_only` |
| CLI | `--target-limit` | `20` | Integer 1-100 |
| CLI | `--target-cursor` | empty | Opaque cursor from the same audit/filter identity |
| facade/FastMCP | `response_mode` | `compact` | Same values and semantics as CLI |
| facade/FastMCP | `artifact_root` | null | Same explicit persistence boundary as CLI |
| facade/FastMCP | `target_limit` | `20` | Same range as CLI |
| facade/FastMCP | `target_cursor` | null | Same identity validation as CLI |

For CLI/MCP continuation pages, `target_cursor` requires `artifact_root`. All
audit-defining arguments remain required/defaulted exactly as for the first
call and must reproduce the persisted `audit_request_id`; `tex_path` is not
reread or re-audited.

Existing audit inputs, `--output-md`, `--output-json`, and `--print-markdown`
remain accepted. Explicit output files are raw detailed audit artifacts for
backward compatibility; transport responses expose them only through redacted
logical output-reference records. `--print-markdown` remains an explicit
compatibility escape hatch and bypasses response JSON formatting only.

There is no Phase 07 publication argument.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering question | Can CLI/MCP return a bounded, actionable view of an already completed document audit without losing any claim-boundary information or changing audit semantics? |
| Exact baseline | Current raw `audit_document_derivation_tree` result returned nearly whole by facade/server and nearly whole minus Markdown by CLI. The raw library result is the semantic reference. |
| Primary pass criterion | For adversarial synthetic completed-audit fixtures and focused local synthetic fixtures, all three response modes agree with the raw reference on status, publication state, promotion false, coverage, complete veto ids, complete unresolved-assumption ids, action/decision ids, global reference inventory, page/full reference resolution as declared, and non-claims; CLI/facade/server compact results are semantically identical after excluding transport-only `ok`; persisted pagination union preserves target order without a second audit call. |
| Veto diagnostics | Any omitted veto or unresolved assumption; any response-mode status/promotion change; invalid cursor accepted; changed audit-defining continuation input accepted; continuation reruns an audit; global boundary paginated away; reference-inventory mismatch; absolute private source/backend/output/error/artifact path returned; artifact bytes/digest mismatch; artifact-only success without an artifact; default publication not disabled; response compilation reruns an audit/backend. Any one veto fails the phase. |
| Explanatory diagnostics | Canonical compact byte count, pretty CLI byte count, blocker deduplication ratio, and target count. These explain usability only. |
| Product guardrail | Canonical compact JSON should be at most 25,600 bytes for the focused synthetic fixture. If correctness requires more, retain complete boundary information, record the overage, and use pagination/artifact-only refinement rather than dropping evidence. |
| What will not be concluded | Mathematical correctness, proof, backend breadth, real-document usefulness, publication eligibility, release readiness, or that 25,600 bytes is universally optimal. |
| Preserved artifact | Phase 07 result record plus tests; optional local detailed JSON generated in tests under temporary roots. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Earliest diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| `compact` CLI/MCP default | Master Phase 07 product goal and prior real-use payloads of 1.4-2.3 MB | Directly addresses agent context-window usability | Existing callers expect raw top-level fields | Explicit detailed-mode compatibility tests and changed-default tests | Reviewed product default for Phase 07 |
| Raw library audit remains detailed | Existing public function and test corpus | Avoids making presentation concerns alter scientific execution | Divergence between raw and transport paths | Compile all views from a captured raw mapping and parity-check | Compatibility constraint |
| Target limit 20 | Stale master proposal, not scientific evidence | Small deterministic default with an explicit 1-100 range | A few very large targets may still exceed guardrail | Maximum-veto fixture byte measurement | Convenience product default, revisable |
| 25,600-byte target | Master quantitative guardrail | Useful bounded-context regression signal | Proxy becomes correctness gate and causes omission | Test completeness before size and fail omission mutations | Explanatory product guardrail only |
| SHA-256 ids/cursor checksum | Existing project content-digest convention | Deterministic local identity without secrets | Mistaken for authenticity or proof | Explicit `authority: presentation_only` and non-claim tests | Identity convenience, not authority |
| Content-addressed detailed artifact | Master product requirement; active policy permits digests where scientific identity matters | Lets compact actions point to exact local details | Collision/path confusion or overwrite | Different-byte existing-file, symlink, digest, and containment tests | Reviewed local artifact default when explicitly requested |
| No artifact persistence by default | Academic proportionality and least-surprise CLI/MCP behavior | Avoids implicit writes and private-path leakage | Compact response lacks resolvable full detail and cannot continue across calls | Explicit `not_persisted` artifact state; artifact-only and cross-call continuation require root | Reviewed safety default |
| Presentation fallback action | Needed for legacy/failed targets lacking a Phase 06 action | Keeps every open target actionable without inventing mathematical authority | Fallback is mistaken for ranked action | `authority: presentation_only`, source blocker refs, mutation tests | Bounded compatibility fallback |
| Recursive completeness collectors | Raw schemas contain boundary fields at several levels | Machine-checkable parity is safer than hand-picked prose | False positives from unrelated `status` fields or missed aliases | Adversarial nested fixtures and collector unit tests | Implementation hypothesis to validate |
| Path redaction in transport only | Master privacy requirement and current doctor/source-path fields | Prevents source/backend/output/artifact leakage while retaining local detailed bytes | Redaction changes identity, destroys source localization, or misses a free-text path | Compute identity before redaction; field-policy and adversarial free-text tests across source, doctor, evidence/output, error, and artifact records | Reviewed transport rule |
| Full audit-request identity on continuation | R1 skeptical review of cross-call pagination | Prevents a cursor for one focus/budget/environment request from being replayed with another | Stale audit silently presented as the new request | Mutate each audit-defining argument independently and require rejection before source/backend access | Reviewed correctness constraint |
| Response contract v1 | R1 skeptical review of default output transition | Makes the changed MCP/CLI default explicit and machine-discoverable | Registry advertises the raw audit contract while returning compact data | Registry, detailed `audit_metadata`, and actual FastMCP output-schema tests | Reviewed compatibility boundary |

No scientific, numerical, mathematical, ML, or backend default is introduced
by this phase.

## Skeptical Plan Audit

The plan must be reviewed before implementation against these questions:

1. **Wrong baseline:** The raw completed audit, not the existing `_compact_tree`
   name or byte size, is the semantic baseline.
2. **Proxy promotion:** Payload size and deduplication counts are explanatory;
   neither can override completeness or claim-boundary vetoes.
3. **Missing stop conditions:** Any semantic drift, boundary omission, path
   leak, cursor mismatch acceptance, or implicit backend execution stops the
   phase for repair.
4. **Unfair comparison:** Compactness and continuation pages are compared
   against the same captured/persisted audit result, not separate executions
   whose backend/environment results may differ.
5. **Hidden assumptions:** Target identity, unresolved-assumption detection,
   fallback actions, artifact containment, and cursor filtering are explicit
   implementation hypotheses with mutation tests.
6. **Stale context:** Aggregate gate and experimental-publication requirements
   are removed under the active academic-governance reset.
7. **Environment mismatch:** New response tests use captured synthetic mappings
   and temporary artifact roots. Existing document regression tests may use
   their current deterministic in-process SymPy path as engineering adjacency;
   no executable Sage/Lean, optional adapter smoke, GPU, or network is allowed.
8. **Artifact relevance:** Tests preserve exact mode-parity sets and payload
   bytes; they answer the presentation question but cannot establish
   real-document scientific usefulness.
9. **Misleading pass pre-mortem:** A response could be small because nested
   vetoes were missed. Independent recursive collectors and deletion mutation
   tests must fail such a response.
10. **Misleading failure pre-mortem:** A payload can exceed 25,600 bytes solely
    because correctness requires many unique vetoes. That is a product finding,
    not scientific failure; retain the evidence and report the overage.

Implementation may start only after the audit records `PASS` or the plan is
visibly repaired and rereviewed.

### Skeptical audit outcome

The first fresh read-only Codex review returned `REVISE` on 2026-07-14 for five
material contract defects: backend-test scope, incomplete continuation-request
binding, an unnamed MCP output-contract transition, ambiguous global reference
completeness, and underspecified path redaction. The subplan was visibly
repaired in all five areas. A focused fresh rereview found no remaining
material blocker and returned `VERDICT: AGREE`.

Local skeptical audit also found and repaired the cross-call pagination flaw
before implementation: continuation pages now load exact verified persisted
bytes and never repeat the raw audit. The plan therefore records
`SKEPTICAL_AUDIT_PASS` and may proceed under the stated evidence contract.

## Work Packages

### P07-W1: Pure response compiler

Implement canonical serialization, audit identity, recursive boundary
collection, compact/detailed/artifact-only compilation, redaction, and a
semantic parity validator. The compiler must not import or call the raw audit
function.

Required tests include:

- complete nested veto, unresolved-assumption, action/decision, evidence-ref,
  source-ref, and non-claim preservation;
- mutation removal of each required common-boundary field fails validation;
- response mode cannot change status, coverage, promotion, or publication;
- detailed output excludes embedded Markdown but preserves semantic targets;
- disabled/early-return audit results compile without source access.
- v1 response metadata is authoritative while detailed `audit_metadata`
  preserves the raw audit contract.

### P07-W2: Deduplication, pagination, and artifacts

Implement blocker grouping, stable target order, cursor binding, page metadata,
safe optional persistence, and logical artifact refs.

Required tests include:

- duplicate blocker prose appears once with all blocker and target ids;
- page union equals detailed target order;
- cursor from another result/filter/schema is rejected;
- changing page size with a valid cursor preserves order;
- a persisted continuation page performs zero raw-audit calls and rejects a
  cursor without its exact artifact root;
- changing each of `tex_path`, `focus_labels`, `max_labels`, `budget_profile`,
  `max_attempts`, `backend_env`, `search_mode`, `grounding_policy`, or `workers`
  rejects continuation before source/backend access;
- global veto/assumption/non-claim summaries are identical on every page;
- artifact bytes match returned SHA-256/byte count;
- symlink/escape/different-byte collision attempts fail;
- no absolute artifact root or private home prefix appears in responses.
- source, doctor/backend, evidence/output, error/detail, and artifact metadata
  obey the explicit transport path policy without changing semantic ids.

### P07-W3: CLI integration

Add the four presentation arguments, compile after one raw audit call on an
initial request, load verified persisted bytes on a continuation request, keep
explicit Markdown compatibility, and make compact JSON the default.

Required tests include default compact, explicit detailed, artifact-only,
cursor continuation, invalid limits/modes, output compatibility, and no
embedded Markdown in JSON modes.

### P07-W4: Facade and FastMCP integration

Add argument parsing once in the facade and mirror it in FastMCP. The facade
must call the raw audit exactly once for an initial request and zero times for
a continuation request, then compile the requested response. Set structured
output for this wrapper if supported by the installed MCP version, and inspect
the actual registered input and output schemas.

Required tests include facade/server parity, facade structured invalid-argument
results, registry output-contract transition, actual FastMCP input
fields/defaults and non-null generic-object output schema, and default compact
behavior.

### P07-W5: Downstream actionability and regression

Add a deterministic compact consumer test that can identify each page target,
its blocking scope, the next action/artifact or explicit choice blocker, exact
evidence/source refs, publication veto, and non-claim boundary without loading
the detailed artifact.

Run focused document-response tests, relevant document/publication adjacency,
and diff/compile hygiene. Do not run the long real-document suite merely to
measure formatting.

## Required Checks

Initial focused commands:

```bash
PYTHONPATH=src python3 -m pytest \
  tests/test_document_derivation_response.py \
  tests/test_document_derivation_tree.py \
  tests/test_document_publication_quarantine.py \
  tests/test_mcp_facade.py \
  tests/test_mcp_server.py \
  tests/test_mcp_surface_sync.py -q \
  -k 'document_derivation or response_mode or compact or artifact_only or publication or mcp_surface'

PYTHONPATH=src python3 -m mathdevmcp.cli audit-document-derivation-tree --help

python3 -m py_compile \
  src/mathdevmcp/document_derivation_response.py \
  src/mathdevmcp/cli.py \
  src/mathdevmcp/mcp_facade.py \
  src/mathdevmcp/mcp_server.py

git diff --check
```

After focused repair, run relevant adjacency without optional real backends:

```bash
PYTHONPATH=src python3 -m pytest \
  tests/test_document_derivation_response.py \
  tests/test_document_derivation_tree.py \
  tests/test_document_publication_quarantine.py \
  tests/test_document_derivation_real_regressions.py \
  tests/test_failure_ledgers.py \
  tests/test_phase06_promotion_policy.py \
  tests/test_promotion_policy.py \
  tests/test_mcp_facade.py \
  tests/test_mcp_server.py \
  tests/test_mcp_surface_sync.py -q
```

If collection shows unrelated pre-existing failures, isolate and record them;
do not modify unrelated code to force a green total.

## Forbidden Claims And Actions

- Do not claim proof, mathematical correctness, globally minimal assumptions,
  substantive real-document usefulness, publication eligibility, release
  readiness, or mission completion.
- Do not enable publication or add a publication/promotion-gate argument.
- Do not treat compact size, schema validity, or an `AGREE` review as
  scientific evidence.
- Do not omit a veto, unresolved assumption, evidence identity, source scope,
  or non-claim to satisfy a payload target.
- Do not rerun or reconstruct the missing historical Sage R3 evidence.
- Do not run executable/optional external backends, GPU, network, Claude
  review, source-document edits, installs, commits, pushes, or destructive
  commands. The existing deterministic in-process SymPy regression path is the
  sole backend-test exception described above.
- Do not make the response compiler an alternate audit, ranking, evidence
  reader, or promotion authority.
- Do not revert or rewrite unrelated dirty worktree changes.

## Phase Result And Decision Table Requirements

The result record must state:

- files changed and why;
- exact checks and outcomes;
- compact canonical and CLI-pretty byte measurements;
- semantic parity and mutation-test outcomes;
- artifact digest/containment results;
- whether FastMCP structured schema was actually observed;
- engineering correctness, mathematical-validity, and scientific-interpretation
  ledgers kept separate;
- strongest alternative explanation and weakest evidence;
- a decision table with decision, primary criterion status, veto status, main
  uncertainty, next justified action, and non-conclusions.

Allowed close statuses are:

- `PASS_COMPACT_AGENT_FACING_PRODUCT`;
- `BLOCKED_PRODUCT_CONTRACT`;
- `FAIL_BOUNDARY_OR_SEMANTIC_PARITY`.

## Exact Phase 08 Handoff Conditions

Draft and automatically launch the Phase 08 planning/review step only if:

1. all primary semantic-parity criteria pass;
2. every veto diagnostic is false;
3. compact is the verified CLI/MCP default and detailed mode preserves the raw
   audit semantics;
4. artifact-only cannot succeed without a verified local detailed artifact;
5. cursor and redaction adversarial tests pass;
6. publication remains disabled;
7. the Phase 07 result record is written;
8. the Phase 08 subplan is skeptically audited under the active academic
   governance reset.

Phase 08 may plan frozen real-document validation, but it must not launch a
real-document/backend run until its scientific evidence contract, default and
assumption audit, run manifest, resource budget, and stop conditions are
reviewed. That is the next genuine scientific boundary.

## Stop Conditions

Stop Phase 07 and write a blocker or failure result if:

- any response mode changes mathematical/audit status or effective promotion;
- a complete veto or unresolved assumption cannot be represented compactly;
- the compiler would need to rerun an audit/backend to construct a response;
- safe artifact containment or non-overwrite semantics cannot be established;
- an identity-mismatched cursor is accepted;
- a continuation page would require rerunning the raw audit;
- an absolute private artifact path is returned;
- publication is enabled or a source edit becomes necessary;
- implementation requires a new scientific/default decision, external
  disclosure, install, network access, destructive operation, or user funding;
- unrelated dirty work prevents a safe focused edit.

Ordinary test or implementation defects are repair-loop events, not reasons to
stop. Diagnose, patch visibly, rerun focused checks, and continue while the
phase remains inside this contract.
