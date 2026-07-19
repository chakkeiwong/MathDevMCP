# MathDevMCP Resumable Capstone Closable-Gap Program

Date: 2026-07-18

Status: `EXECUTED_WITH_LIMITS`

Predecessor:
`docs/plans/mathdevmcp-resumable-full-document-gap-remediation-result-2026-07-18.md`

Supervisor and executor: Codex

## Mission And Scope

Close the remaining engineering gaps that can be resolved from existing
source-bound D447 checkpoints and repository contracts, while refusing to turn
engineering completion into a mathematical or scientific claim.

This program addresses:

1. the incomplete public Phase 6 packet-reuse path;
2. bounded consumption of the approximately 94 MB full-tree evidence without
   requiring the monolithic aggregate in consumer memory;
3. one final source-ownership diagnostic over the 132 relation-shape and seven
   nested-display abstention classes;
4. corrected close evidence for the predecessor program.

This program does not attempt to prove the remaining D447 mathematics, enable
publication, or establish independent generalization. Those require scoped
scientific questions, formalization/source evidence, and a provenance-clean
holdout respectively.

## Closure Matrix

| Predecessor gap | Classification | This program's acceptance |
| --- | --- | --- |
| Most mathematical obligations remain unresolved | not closable as one engineering task | preserve a source-bound prioritized ledger and nonclaim; no blanket proof claim |
| 132 relation-shape labels lack canonical tree targets | bounded diagnostic only | revalidate exact typed abstentions; promote only if current extraction yields one complete owned target under the unchanged source digest |
| Seven nested-alignment labels lack row ownership | bounded diagnostic only | revalidate with the current byte-preserving locator; retain abstention unless exact no-sibling-collapse ownership passes |
| Publication disabled | correct boundary, not a gap | assert disabled throughout |
| 94 MB tree artifact burdens consumers | closable | page validated per-target checkpoint records directly with bounded payloads and exact resolver bindings |
| Packet reuse lacked post-repair D447/public-surface evidence | closable | public CLI/facade/FastMCP reuse exact validated audit checkpoints; cached/uncached semantic projections match on predeclared D447 labels |
| No clean independent holdout | external scientific input required | record `not_tested_no_verified_clean_holdout`; do not select a holdout after observing results |

## Research Intent And Evidence Contract

| Field | Pre-run contract |
| --- | --- |
| Engineering question | Can public packet and tree-consumption surfaces reuse exact existing checkpoints without recomputation, semantic drift, unbounded response payloads, or weakened claim boundaries? |
| Candidate mechanism | Explicit audit-checkpoint selectors plus an immutably persisted resumable-tree page token bound to session, ordered record IDs, page boundary, and resolver scope. |
| Exact baseline | Frozen D447 source SHA-256 `c5cfc66061ce90b053cf7e1df6eb770bababfcda85aa54c26546437037da0690`; existing full audit session and 434-target tree session under `.local/mathdevmcp/evidence/resumable-d447-remediation-20260718/full/`. |
| Primary pass criterion | Cached and uncached packet semantic projections match for the predeclared labels; all public cached routes report validated checkpoint provenance; every tree record appears exactly once across bounded pages and exact resolution reconstructs its record. |
| Hard vetoes | Path-only trust, source/session/label/obligation/config mismatch accepted, packet audit recomputation on a requested cached route, missing/duplicate tree records, page-token tamper accepted, response above 30,720 bytes, publication enabled, or abstention promoted without exact source ownership. |
| Explanatory diagnostics | Wall time, peak RSS when available, artifact byte counts, page counts, and cached/uncached timing ratios. |
| What timing means | Descriptive engineering evidence only. Few calls do not statistically establish superiority. |
| Artifact | Implementation/tests plus an execution result and skeptical close review under `docs/plans` and `docs/reviews`. |
| Not concluded | Mathematical correctness, proof, source-author error, publication readiness, default superiority, or independent generalization. |

## Predeclared D447 Packet Sample

Use three labels selected before the new timing results:

- first canonical target: `eq:author-counterfactual-window`;
- central paper-equation target: `eq:bgs-paper-c71-restated`;
- final canonical target: `eq:sw-wage-phillips`.

For each label run one uncached and one checkpoint-reused proof packet in the
same CPU-only environment. Compare canonical semantic projections after
excluding only audit provenance mode/record ID and runtime. Also build negative
evidence from the exact same audit result. Record individual timings without
ranking claims.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Existing full D447 audit/tree sessions | predecessor verified artifacts | exact source/configuration/record identities already exist | stale or cross-version record accepted | validate source digest, session identity, every selected record, and current schema | reviewed baseline evidence |
| Explicit checkpoint selector arguments | existing artifact/session identity design | makes reuse visible and fail-closed | hidden fallback recomputes after invalid selector | selector supplied means any validation failure raises; no fallback | reviewed design |
| Tree pages default to 20, maximum 100 | existing document-response limits | matches established MCP ergonomics | target record too large for budget | reduce effective page size; if one projection cannot fit, return artifact-bound minimal summary | hypothesis with payload veto |
| Direct per-record paging | immutable tree checkpoints | avoids loading the 94 MB aggregate | global summary fields unavailable | page contract says per-target checkpoint surface and does not claim full aggregate synthesis | reviewed bounded route |
| Three D447 packet labels | predeclared first/central/final canonical positions | samples document position and real target complexity within bounded cost | not representative of all 434 targets | descriptive-only timing and no generalization | diagnostic sample |
| Current extractor for abstention recheck | exact source-bound authority | promotion requires current exact ownership | fitting a special parser to D447 labels | no new ownership heuristic; retain abstention on ambiguity | reviewed safety default |

## External-Tool-First Audit

- The packet and paging repairs are artifact-identity and transport problems;
  SymPy, Sage, Lean, LeanSearch, Pantograph, and LeanDojo do not solve them.
- The 132 relation-shape audit uses the existing source-bound LaTeX extraction
  stack. CAS/provers are inapplicable before a mathematical target exists.
- The seven nested labels already received a current-locator and LaTeXML 0.8.6
  comparison. A new in-house ownership algorithm is forbidden in this program;
  the diagnostic will only revalidate current evidence after intervening parser
  changes.
- Backend absence or parser abstention is diagnostic and never a refutation.

## Phase 1: Public Audit-Checkpoint Packet Reuse

Objective: make the already tested internal packet reuse available through
normal CLI, facade, and FastMCP calls.

Implementation:

- add public loading of one audit record by session ID and exact label;
- require `checkpoint_root`, `checkpoint_session_id`, and
  `checkpoint_record_id` together;
- validate session, source digest, ordered label index, record ID, obligation,
  and packet configuration before use;
- use the validated record for proof packets and for negative-evidence packets;
- report `reused_validated_checkpoint` provenance in detailed and compact proof
  packets and corresponding evidence provenance in negative packets;
- never silently fall back to recomputation after a checkpoint selector is
  supplied.

Checks:

- direct library, CLI, facade, and FastMCP semantic parity;
- wrong root/session/record/label/source/summary configuration fails closed;
- monkeypatched audit producer proves zero recomputation on reuse;
- compact transport remains bounded and resolves exact detailed bytes.

Stop condition: any public route accepts a mismatched record or hides fallback
recomputation.

## Phase 2: Bounded Resumable-Tree Record Surface

Objective: consume validated target checkpoints without loading or resolving
the 94 MB monolithic tree artifact.

Implementation:

- load and validate a tree session plus its immutable record inventory;
- produce compact pages in canonical target order;
- bind page tokens to session ID, source digest, ordered record IDs, page
  offset/limit, and resolver scope;
- expose exact record resolution only for target IDs scoped by an issued page;
- make response and resolver payloads obey the 30,720-byte public budget;
- expose library, CLI, facade, and FastMCP surfaces;
- retain `publication_disabled` and local-byte-identity-only authority.

Checks:

- every record appears once across pages;
- tampered tokens, swapped sessions, missing/extra records, wrong target IDs,
  and source drift fail closed;
- exact resolver output matches the checkpoint's canonical record bytes;
- a full 434-record page walk uses bounded response sizes without reading the
  monolithic aggregate.

Stop condition: page construction requires loading `full-tree.json`, loses
ordering, or cannot bound a single-target response.

## Phase 3: Abstention-Class Revalidation

Objective: determine whether intervening extraction changes close any of the
132 plus seven source-ownership gaps without inventing targets.

Checks:

- source digest remains frozen;
- every label resolves to exactly one current classification;
- compare current canonical/typed-abstention status to the frozen inventory;
- for any apparent promotion, require complete owned spans, one label, exact
  obligation digest, and no sibling-branch collapse;
- otherwise retain the original typed abstention and report why external
  mathematical backends remain inapplicable.

Acceptance: exact accounting and honest classification. Zero promotions is a
valid result, not a failed phase.

## Phase 4: D447 Evidence, Regression, And Close

Execution:

- run focused and public-surface tests;
- run the predeclared three-label cached/uncached packet comparison;
- walk and resolve all 434 tree checkpoints through the bounded surface;
- run changed-surface and full repository tests CPU-only;
- write the result and skeptical close review;
- amend the predecessor close record to distinguish completed and remaining
  gaps accurately.

Close only when:

- Phases 1 and 2 pass all hard vetoes;
- Phase 3 accounts for all 139 abstention labels without unsafe promotion;
- exact D447 evidence artifacts are preserved;
- the full suite passes except documented optional/environment skips;
- no scientific, publication, or generalization claim is inferred.

## Skeptical Pre-Execution Audit

Verdict: `PASS_AFTER_REVISION`

Revisions made before execution:

1. The first scope treated packet latency as optional. The predecessor plan
   required public semantic reuse checks, so this is now an acceptance gap.
2. The first tree proposal reused the existing document-response compiler,
   which requires the monolithic audit and would not answer the bounded-memory
   question. The plan now pages immutable per-target records directly.
3. Runtime improvement was initially phrased as a pass criterion. It is now
   explanatory only; exact reuse and semantic parity are primary.
4. The 132 and seven abstentions were initially listed as repairs. They are now
   diagnostic revalidation phases with exact-ownership promotion vetoes.
5. Scientific closure and clean-holdout selection were removed from execution:
   neither can be manufactured from existing repository artifacts.
6. Checkpoint paths are not authority. All reuse routes must validate session,
   source, label, obligation, configuration, and record identity.
7. The three-label packet sample is frozen before timing to prevent selecting
   descriptively favorable cases after results are visible.
8. Publication disabled is classified as a correct boundary, not repair debt.

Execution may proceed because all planned mutations are local and reversible,
the scientific boundaries are explicit, and the evidence artifacts directly
answer the two closable engineering questions.
