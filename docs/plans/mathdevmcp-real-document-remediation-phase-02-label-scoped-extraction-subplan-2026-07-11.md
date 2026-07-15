# Phase 02 Label-Scoped Obligation Extraction Subplan

Date: 2026-07-11

Status: `DRAFT_REPAIRED_AFTER_PLAN_REVIEW_R8_PENDING_FINAL_R9`

## Phase Objective

Recover exactly the mathematical obligation owned by a requested LaTeX label
before semantic classification or backend routing. A Phase 02 pass means that
row ownership, continuation grouping, byte spans, canonical obligation
identity, scoped operator/symbol inventories, ambiguity, and file provenance
are correct for reviewed microfixtures and the two frozen real-document
displays. It does not mean that an obligation is mathematically true or backend
certified.

## Entry Conditions Inherited From Phase 01

Phase 02 planning and execution must reopen and verify both exact predecessor
artifacts:

- stable P01 decision ref:
  `.local/mathdevmcp/evidence/p01-20260711/phase-results/P01-decision.json`;
- stable P01 decision SHA-256:
  `7abc4b00714d0a216aa506cf3308d25a454443eb7316293ea05ec89f3d54a39a`;
- terminal P01 receipt-index ref:
  `.local/mathdevmcp/evidence/p01-20260711/result-rounds/rr03/receipts/receipt-index-23.json`;
- terminal P01 receipt-index SHA-256:
  `5781ab4a7ba23ff865847dd496839a4f827aee78462166606243ad4da591846a`.

The predecessor decision must remain strict canonical `pass`, publication mode
must remain `disabled`, all P01 vetoes must remain false, the terminal receipt
must remain exit zero with same-inode/same-digest publication bindings, and the
P00 quarantine regression must still pass. Any mismatch closes Phase 02 before
implementation.

## Baseline And Problem Record

The current code is not an acceptable comparator merely because existing tests
pass. Read-only diagnostics on 2026-07-11 measured:

- `EquationRow` has line spans but no byte spans, environment instance id,
  explicit-label state, `nonumber` state, or ownership status;
- `equation_locator.locate_equations_in_text` assigns
  `_find_label(row_text) or env_label`, causing unlabeled rows to inherit the
  first environment label;
- `eq:incremental-cash-flow` currently returns three targets: its first row, an
  incomplete continuation row, and the distinct `eq:incremental-npv` equation;
- `eq:foc-k` currently returns both FOC rows, while direct `eq:foc-b` lookup
  returns `label_not_found` because `latex_index.build_index` indexes only the
  first label in a multi-label display;
- indexing the full `docs` tree silently resolves duplicate labels to another
  document version, so file identity must be explicit and ambiguity cannot be
  hidden by dictionary overwrite;
- `document_derivation_tree._semantic_packet` computes operator/symbol
  inventories from the full display, contaminating a label-scoped obligation
  when a display owns multiple labels;
- the current target/parser tests pass `16` tests despite these failures, so
  test count and target count are explanatory only.

Frozen source inputs for Phase 02 are read-only:

| Source | SHA-256 | Required labels |
|---|---|---|
| `docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex` | `dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8` | `eq:incremental-cash-flow`, `eq:incremental-npv` |
| `docs/risky-debt-maliar-deep-learning-lecture-note.tex` | `d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1` | `eq:foc-k`, `eq:foc-b`, `prop:interior-foc` |

Source-digest drift is a veto, not permission to refresh the oracle after
observing output. A changed source requires a reviewed two-version amendment.

Frozen half-open UTF-8 byte oracle, measured before implementation:

| Source/owner | Environment interval | Owner-label interval | Owned row intervals | Excluded sibling intervals |
|---|---:|---:|---:|---:|
| final submission, `eq:incremental-cash-flow` | `[45275,45809)` | `[45513,45545)` | `[45291,45429)`, `[45434,45545)` | `[45550,45797)` |
| final submission, `eq:incremental-npv` | `[45275,45809)` | `[45771,45797)` | `[45550,45797)` | `[45291,45429)`, `[45434,45545)` |
| risky debt, `eq:foc-k` | `[29171,29396)` | `[29267,29283)` | `[29187,29283)` | `[29288,29384)` |
| risky debt, `eq:foc-b` | `[29171,29396)` | `[29368,29384)` | `[29288,29384)` | `[29187,29283)` |

Corresponding environment line ranges are 840-862 for the card display and
775-786 for the risky-debt display. Owned row line ranges are 841-846 and
847-850 for card cash flow, 851-861 for card NPV, 776-780 for `eq:foc-k`, and
781-785 for `eq:foc-b`. The oracle binds raw source bytes including labels and
`\nonumber`; normalized mathematical text is derived separately and cannot
replace the raw interval check.

The complete reviewed oracle is
`docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json`
with a SHA-256 that is recomputed and frozen immediately before each plan
review; the agreeing review must quote that digest, and the entry gate must
bind the same bytes. Its reviewed fixture files already exist with the exact
bytes and digests recorded
inside the oracle; neither fixture bytes nor expected output may be changed
after plan convergence. It freezes every positive and adversarial case's file
digest, owned/excluded spans, row shapes, grouping reasons, normalized target,
inventories, extraction state, and ambiguity codes, plus the four real-source
outcomes and the proposition-container outcome. The entry gate reopens the
oracle, verifies every fixture/source/span digest, and records the oracle file
digest before any production source, test, or script edit. A necessary oracle
amendment requires a visible two-version plan review and cannot be justified by
implementation output.

The compact oracle binds a second immutable file,
`docs/plans/mathdevmcp-real-document-remediation-phase-02-materialized-obligations-oracle-2026-07-11.json`,
containing the complete strict identity payload, canonical byte count, digest,
and id for all 17 expected file-scoped obligations. Its bound SHA-256 is
`ae7aa48fb8c475c7c37c75158a9ed6f83b21a686bc8cd8ca2b28c79b36bcb1ad`.
The materialized file, compact projections, and source-byte reconstruction must
all agree exactly; none is generated from implementation output. Any mismatch
is an oracle-integrity veto.

## Skeptical Plan Audit

- Wrong baseline: the baseline is the measured contaminated extraction above,
  not the passing legacy tests or prior generated reports.
- Proxy promotion: counts, parser availability, parser exit zero, and matching
  label names do not pass the phase. Exact owned bytes, spans, grouping reasons,
  inventories, and canonical digests are primary.
- Hidden assumptions: an unlabeled row is not automatically a continuation;
  the same label text in another file is not the requested source; a specialist
  parser is not better merely because it runs.
- Environment mismatch: LaTeXML `0.8.6` and Pandoc `2.9.2.1` are locally
  available, but they are optional extraction comparators. Their subprocess
  failures are engineering diagnostics, not mathematical or extraction
  refutations.
- Artifact fitness: every gate must emit exact source refs/digests, owned and
  excluded byte spans, grouping reasons, parser versions/results, zero backend
  request count, and the predecessor bindings.
- Stop conditions: source drift, ambiguous ownership rendered as extracted,
  cross-label bytes/operators, incomplete lhs/rhs entering an adapter, or an
  unreviewed scope expansion stops before Phase 03.

Audit decision: `PASS_FOR_PLAN_REVIEW_ONLY`. No Phase 02 implementation starts
until an independent reviewer agrees with this subplan and all plan findings
are repaired visibly.

## Evidence Contract

- Engineering question: can MathDevMCP produce one canonical, source-scoped
  obligation per intended label without borrowing bytes or operators from a
  sibling label, another document version, or an unjustified continuation?
- Exact comparator: current contaminated outputs recorded above plus explicit
  fixture oracles; never a target-count-only comparator.
- Primary criterion: for every reviewed case, the obligation's file digest,
  environment id, owned row ids, owned byte intervals, excluded sibling
  intervals, normalized target structure, operator/symbol inventories,
  eligibility, ambiguity/uncertainty state, and every other observable field
  match the predeclared oracle. Each full obligation validates against the
  strict schema and its canonical byte count, digest, and id are independently
  reconstructed from those exact bytes and match the predeclared complete
  materialized oracle. The golden case additionally exercises exhaustive
  identity mutation coverage. The two frozen FOC obligations must have distinct
  reconstructed digests.
- Veto diagnostics: source digest mismatch; duplicate or colliding obligation
  identity; cross-label byte/operator contamination; missing or overlapping
  spans; implicit label inheritance; unjustified continuation; ambiguous state
  converted to a target/math gap; incomplete lhs/rhs routed downstream; parser
  selected without better fidelity evidence; any backend request; P00/P01
  drift; publication flag true.
- Explanatory diagnostics: test counts, elapsed time, number of rows/labels,
  parser availability, and parser output size.
- Not concluded: mathematical truth, proof, semantic role correctness, context
  completeness, backend conformance, publication eligibility, real-document
  end-to-end usefulness, or release readiness.
- Preserved artifact: `.local/mathdevmcp/evidence/p02-20260711/` containing the
  entry record, extraction-only bundle/index, command logs, fixture and frozen
  obligation records, parser comparison records, mutation/ambiguity matrix,
  result-round receipts, and eventual stable decision or blocker close.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
|---|---|---|---|---|---|
| UTF-8 byte offsets, half-open `[start,end)` | P01 byte-digest contract and Python source bytes | Directly binds stored source bytes without character-width ambiguity | Unicode or comment stripping shifts spans | Non-ASCII macro/comment fixture round-trips exact bytes | Reviewed engineering default |
| Explicit row labels only | Master P02-W1 and observed inheritance bug | Prevents sibling ownership by environment label | Continuations become orphaned | Separate continuation grouper with reasons | Reviewed default |
| Continuation attaches only by the closed row grammar below | Master P02-W2 and reviewed oracle | Needed for multiline definitions without global inheritance | Rule absorbs a new obligation or misses a valid chain | Positive/adversarial cases bind exact row shapes and reasons | Reviewed hypothesis, limited to oracle grammar |
| Canonical obligation digest uses P01 canonical JSON | Sealed P01 integrity substrate | Stable identities and closed field validation already exist | Extraction schema accidentally depends on presentation order | Order/mutation/digest tests | Reviewed inherited default |
| Requested source file is part of lookup identity | Observed duplicate-label overwrite | Prevents same label in other versions from winning | Bare-label API remains ambiguous | Duplicate-label fixture and explicit ambiguity result | Reviewed default |
| Current parser first, specialists on uncertainty | Existing parser policy | Cheap source provenance with targeted differential evidence | Current parser is retained despite worse spans | Fidelity rubric compares exact label/span/row ownership | Baseline policy, not automatic selection |
| No backend execution | Master P02 entry boundary | Extraction must be valid before routing | Existing high-level path triggers attempts indirectly | Fake sentinel/monkeypatch and bundle backend-request count zero | Mandatory boundary |

### Closed row grammar and deterministic grouping

The localizer operates on UTF-8 bytes. It masks unescaped comments for grammar
decisions but retains them in `source_math`; recognizes braces and nested
`aligned` boundaries; splits only on top-level unescaped `\\`; trims leading/
trailing ASCII whitespace and the row terminator from each row span; and keeps
labels and `\nonumber`/`\notag` inside the owned raw span. Grammar text then
removes comments, labels, numbering suppressors, alignment `&`, and spacing
commands `\quad`/`\qquad`, collapses whitespace, and removes only one terminal
comma or period. It does not expand macros, reorder terms, or simplify algebra.
Top-level relation tokens are `=`, `\coloneqq`, `\equiv`, `\le`, `\ge`, `<`,
and `>` outside braces and nested environments. Phase 02 normalization emits
only the oracle-reviewed `equality`, `equality_chain`, and
`aligned_definition` kinds; other relation patterns fail closed.

The compact-oracle key `environment_locator` is authoritative for
environment pairing, half-open end bytes, supported nesting, row content,
separator recognition, outer ASCII trimming, empty rows, and line arithmetic.
Entry checks must independently re-locate every reviewed environment and row
from exact source bytes and match both oracle files. Invalid UTF-8, unbalanced
or crossed environments, invalid brace depth, or an owned row outside its
selected environment fails closed.

Classification is lexical and ownership-independent. Retain two raw booleans
before grammar-text removal: `has_number_suppressor` is true only when the
comment-masked row contains command token `\nonumber` or `\notag`, and
`had_row_terminator` is true only when the trimmed raw row was followed by the
top-level separator that created the row. The exact continuation-prefix regex,
applied after leading `&`, spacing commands, and ASCII whitespace are removed,
is `r"(?:[+\-*/]|\\(?:cdot|times)(?![A-Za-z]))"`. A leading unary sign is
intentionally treated as continuation syntax in Phase 02; this is surface
grouping, not a semantic claim.

Apply this closed precedence once to every row:

1. two or more explicit labels gives `multi_label_conflict`;
2. empty grammar text after label/spacing removal gives `label_only`;
3. invalid braces/nesting, any top-level relation other than `=` or
   `\coloneqq`, both relation types, or more than one relation token gives
   `unknown`;
4. a leading `=` with empty lhs and nonempty rhs gives
   `relation_chain_continuation`;
5. no top-level relation plus a match of the continuation-prefix regex gives
   `relation_continuation`;
6. exactly one `=` or `\coloneqq` with nonempty lhs/rhs gives the
   corresponding `relation_head`/`definition_head` only when both
   retained booleans are true; otherwise it gives
   `complete_relation`/`complete_definition`;
7. every remaining row gives `unknown`.

The closed row-shape enum is therefore `complete_relation`,
`complete_definition`, `relation_head`, `definition_head`,
`relation_continuation`, `relation_chain_continuation`, `label_only`,
`multi_label_conflict`, and `unknown`. No shape depends on a seed,
owner, attachment decision, or parser-policy result.

Rows in nested `aligned` retain both inner and outer environment ids; attachment
may cross only the reviewed outer-`equation`/inner-`aligned` boundary and only
when all owned rows share that exact environment stack. The algorithm is a
single deterministic allocation pass per environment stack:

1. Classify all rows without assigning owners. A row with more than one label
   becomes `multi_label_conflict`; each label gets an `ambiguous` diagnostic
   with no owned bytes, grouping reason `ambiguous_competing_owner`, and
   ambiguity code `multiple_explicit_labels_on_one_row`. This is
   pre-allocation label competition, distinct from post-candidate overlap.
2. Create one seed per remaining explicit label. The finite transition table is
   exact:

| Seed shape | Direction and accepted unlabeled sequence | Complete candidate |
|---|---|---|
| `complete_relation` | zero or more immediately following `relation_chain_continuation` rows in the same non-nested environment stack | seed plus that maximal sequence |
| `complete_definition` | no attachment | seed only |
| `relation_head` or `definition_head` | one or more immediately following unlabeled `relation_continuation` rows | seed plus that maximal nonempty sequence |
| `relation_continuation` | backward across zero or more immediately preceding unlabeled `relation_continuation` rows, then exactly one immediately preceding unlabeled `relation_head` or `definition_head` | head through seed |
| `relation_chain_continuation` | only the nested-aligned exception below | exception pair |
| `label_only`, `unknown` | no attachment | none; orphaned/ambiguous diagnostic |

The first column always names the explicit-label seed row. A labeled
continuation uses its backward row; a labeled head uses its forward row. No row
with an explicit label is ever absorbed under a different label.

3. The sole nested-aligned exception accepts exactly one immediately preceding
   unlabeled `complete_relation` for a labeled
   `relation_chain_continuation`, only when both rows have the same exact outer
   `equation`/inner `aligned` stack and no intervening source bytes other than
   the row terminator plus ASCII whitespace. Its reason is
   `nested_aligned_same_relation`. No label-only merge or implicit
   reclassification exists.
4. Every maximal scan stops before a row with any explicit label, a shape not
   named in that table cell, an environment-stack change, a blank math row,
   conflict, or `unknown`. A scan never skips a row and never crosses an
   environment boundary. A head without its required continuation and a
   continuation without its required head produces no complete candidate.
5. Allocation is by source order, but no row is committed until every seed's
   candidate set is computed. Disjoint sets commit. Overlapping candidate sets
   make all competing seeds `ambiguous`; there is no distance or first-wins
   tie-breaker. Unclaimed math rows are `orphaned`. There is no iterative
   reclassification after commitment.

The exact expected row shape and reason for every reviewed positive and
adversarial case is frozen in the machine oracle. Any `unknown`, unreviewed
transition, parser ownership disagreement, or candidate overlap fails closed
as `ambiguous`/`orphaned`; it cannot become an adapter-eligible target.
The compact-oracle keys `row_classifier` and `grouping_grammar` are the
authoritative executable registries for this prose. Entry checks must compile
their regexes, classify every reviewed raw row, apply every reviewed
transition, and match the compact row-shape/reason arrays before implementation
or result work.

The compact-oracle key `target_normalizer` is the authoritative closed
row-to-target transformation. It removes only comments, labels, numbering
suppressors, row separators, top-level alignment markers, spacing commands,
and surface whitespace/punctuation in its declared order; it preserves all
other token bytes. It composes only the five listed shape sequences, derives
members by top-level relation splitting, and regenerates `display_text` with
one space around relation delimiters. Entry checks independently reconstruct
every reviewed normalized target from owned source bytes and reject any
compact/full/source mismatch.

The closed initial reason registry is:

- `explicit_label_seed`;
- `backward_number_suppressed_relation_head`;
- `forward_relation_continuation`;
- `nested_aligned_same_relation`;
- `excluded_sibling_label`;
- `orphan_no_unique_owner`;
- `ambiguous_competing_owner`: either multiple explicit labels compete
  for one classified row before allocation or computed candidate owner sets
  overlap after allocation; the ambiguity code distinguishes the mechanisms;
- `ambiguous_parser_disagreement`.

Implementation may not add a row shape, attachment reason, transition, or
normalization rewrite, nor relax a stop condition, without a visible oracle
amendment and plan review.

## Implementation Work Packages

### P02-W1: Row Localization And Explicit Ownership Inputs

Files:

- `src/mathdevmcp/equation_locator.py`;
- `src/mathdevmcp/latex_index.py` only where needed to expose every row label
  without overwriting duplicates;
- `tests/test_latex_index.py` and new fixture-focused tests.

Changes:

- extend `EquationRow` with `byte_start`, `byte_end`, `environment_id`,
  `environment_start_byte`, `environment_end_byte`, `environment_starred`,
  `explicit_label`, `has_nonumber`, and row terminator/ownership diagnostics;
- replace environment-level label inheritance with explicit row-label
  extraction;
- make row splitting comment-aware, brace/nesting-aware enough for reviewed
  fixtures, and byte-preserving; nested `aligned` inside `equation` must not be
  truncated by the outer regex;
- expose all label occurrences and duplicate ambiguity rather than dictionary
  last-write selection.

Required tests include exact byte round-trip, labels at row start/end,
comments/macros, `\nonumber`/`\notag`, starred environments, nested `aligned`,
escaped row separators, duplicate labels across files, and no inherited label.

### P02-W2: Canonical Label-Scoped Obligation Grouper

Files:

- new `src/mathdevmcp/label_scoped_obligation.py`;
- new `tests/test_label_scoped_obligation.py`;
- `tests/fixtures/label_scoped_obligations/*.tex`.

Public functions:

- `group_display_rows`;
- `extract_label_scoped_obligations`;
- `validate_label_scoped_obligation`;
- `canonical_obligation_record` or an equivalently narrow constructor.

Each obligation must include schema/version, source file and digest,
environment id/type/starred state, owner label and owner-label span, ordered
owned rows, explicit continuation reasons, owned and excluded half-open byte
intervals, normalized equality/equality-chain/aligned-definition structure,
complete-lhs/rhs status, scoped operator/symbol inventories, extraction status,
uncertainties, and a content digest computed with P01 canonical bytes.

Ambiguous grouping produces a sealed diagnostic obligation with no adapter-
eligible target. Retrieval hits, parser suggestions, or grouping heuristics are
not mathematical evidence.

### Closed obligation and identity schema

`LabelScopedObligation` is strict `schema_version: "1.0"`; unknown, missing, or
extra keys fail validation. The top-level keys are exactly `schema_version`,
`obligation_id`, `obligation_digest`, `document`, `label`, `environment`,
`owned_rows`, `owned_spans`, `continuation_spans`, `excluded_spans`,
`source_math`, `normalized_target`, `operator_inventory`, `symbol_inventory`,
`extraction_state`, `adapter_eligible`, `ambiguities`, `uncertainties`, and
`provenance_refs`.

- `document` is exactly `logical_id`, workspace-relative `file`,
  `source_digest`, and `corpus_version` (`p02-frozen-20260711` for the frozen
  documents or `p02-reviewed-fixture-20260711` for fixtures).
- `environment` is exactly deterministic `environment_id` (source digest plus
  byte span), kind, starred boolean, ordered environment stack, byte/line span,
  parser backend/version, and normalization version. Physical host paths are
  forbidden.
- each ordered `owned_rows` item is exactly row id/index, byte/line span,
  explicit label plus label span or null, row shape, grouping reason,
  `has_nonumber`, environment stack, and raw-source digest;
  `row_index` is zero-based source order among all nonempty localized math
  rows in the selected environment, independent of obligation ownership;
  `owned_spans`, `continuation_spans`, and `excluded_spans` are source-ordered,
  non-overlapping half-open byte/line span objects. Excluded spans also carry
  `excluded_sibling_label` and its reason.
- `normalized_target` is exactly `kind`, ordered `members`, `display_text`,
  `complete_lhs_rhs`, and normalization version. Kinds are `equality`,
  `equality_chain`, `aligned_definition`, or `unavailable`; unavailable has
  empty members/text and false completeness.
- `operator_inventory` is an ordered subsequence of the closed order
  `definition`, `equality`, `conditional_expectation`, `conditional_bar`,
  `summation`, `maximum`, `minimum`, `derivative`, `indicator`, `transpose`,
  `integral`; `symbol_inventory` is exactly sorted unique
  `latex_commands`/`bare_identifiers` under the closed scanner below.
- `extraction_state` is exactly `valid_complete`, `ambiguous`, `orphaned`, or
  `invalid`. Only `valid_complete` may set `adapter_eligible: true`; every
  ambiguity/uncertainty item has exactly `code`, ordered nonempty
  `source_spans`, ordered nonempty `candidate_interpretations`, and nonempty
  `required_discriminator`. Each source span has exactly workspace-relative
  `file`, `start_byte`, and `end_byte`. Candidate interpretations are bounded
  strings, not free-form nested evidence. Closed diagnostic codes are
  `multiple_explicit_labels_on_one_row`, `missing_relation_head`,
  `duplicate_label_across_files`, `competing_owner_sets`,
  `parser_ownership_disagreement`, and `unknown_row_shape`. Ambiguities and
  uncertainties are source-ordered; the oracle freezes exact objects for every
  reviewed non-valid case and exact empty arrays for every valid case.
- `provenance_refs` is ordered file, environment, label, then owned-row refs;
  presentation ordering or artifact storage paths never enter it.

The exact derived-id formulas are frozen: `environment_id` is `env_` plus
SHA-256 of P01-canonical `{source_digest,start_byte,end_byte,environment_stack}`
where each stack item is exactly kind/starred; `row_id` is `row_` plus SHA-256
of P01-canonical `{source_digest,environment_id,row_index,start_byte,end_byte}`.
The golden vector freezes both payloads and ids. No line number, physical path,
timestamp, or Python object identity enters either id.

Identity inherits the master canonical serialization and the P01 strict
canonical JSON implementation. `identity_payload` is the entire validated
record excluding only derived `obligation_id`, derived `obligation_digest`,
artifact refs/locations, timestamps, and run id. It therefore includes every
document/environment/parser/normalization field, label, ordered owned/
continuation/excluded spans and rows, exact `source_math`, normalized target,
inventories, state, eligibility, ambiguities, uncertainties, and provenance.
`obligation_digest` is SHA-256 of canonical identity-payload bytes;
`obligation_id` is `obl_` plus that digest. Derived fields are verified, never
trusted. Arrays are ordered except the explicitly sorted unique inventories;
no field is implicitly dropped because empty or null.

The oracle's `golden_identity_vector` binds the positive case and exact mutate-
one-field coverage. Every listed identity mutation must change the digest;
only mutation of an excluded runtime/derived field may preserve it. Validation
also rejects self-digest inclusion, reordered spans/members, duplicate spans or
inventory members, source bytes inconsistent with spans, noncanonical bytes,
unknown enums, and an eligible non-complete record. The formal entry gate
computes and records the golden canonical bytes and digest before result work;
the implementation must match rather than generate the expected vector.

The oracle mutation paths use RFC 6901 JSON Pointers and its closed
type-specific replacement protocol. Coverage includes every identity-bearing
top-level object, every nested golden-vector leaf, and every empty identity
container (continuation spans, excluded spans, command inventory, ambiguities,
and uncertainties). Each mutation starts from a fresh copy and is hashed
without a filter that could discard unknown keys; schema-validity rejection is
a separate gate. The mutation gate must also derive the golden
leaf/empty-container path set independently and reject any missing, duplicate,
or unresolved listed path. Must-not-change paths resolve instead against the
oracle's explicit non-identity test envelope while the identity payload remains
byte-identical. Derived id/digest fields are verified but excluded; artifact
refs, timestamps, and run id remain outside the strict obligation schema and
cannot be smuggled into it.

### Closed scoped-inventory scanner

Inventories are computed only from `normalized_target.display_text`, never raw
excluded bytes, comments, labels, or whole-display text. Matching is
case-sensitive over Unicode NFC text and does not expand macros. Operator
membership uses these exact Python-compatible regexes, tested in the closed
order above; one match emits the operator once:

The machine-readable registry at oracle key inventory_scanner is the
authoritative executable form of this section and must agree field-for-field
with it. Entry and mutation gates compile every registered regex and run an
independent scanner over every fixture, duplicate-file scoped outcome, and
frozen-source normalized target display text; exact equality with both
operator and symbol inventories is required before implementation or result
work.

| Operator | Exact regex |
|---|---|
| `definition` | `r"\\coloneqq"` |
| `equality` | `r"(?<![\\:<>])="` |
| `conditional_expectation` | `r"\\E(?![A-Za-z])|\\mathbb\{E\}"` |
| `conditional_bar` | `r"\\mid(?![A-Za-z])|\\middle\s*\|"` |
| `summation` | `r"\\sum(?![A-Za-z])"` |
| `maximum` | `r"\\max(?![A-Za-z])"` |
| `minimum` | `r"\\min(?![A-Za-z])"` |
| `derivative` | `r"\\partial(?![A-Za-z])|\\frac\s*\{d(?:\s|\\[A-Za-z]+)*[^}]*\}\s*\{d|\\frac\s*\{\\partial[^}]*\}\s*\{\\partial"` |
| `indicator` | `r"\\1\s*\{"` |
| `transpose` | `r"\\top(?![A-Za-z])"` |
| `integral` | `r"\\int(?![A-Za-z])"` |

LaTeX commands are scanned left-to-right with exact token regex
`r"\\([A-Za-z]+)"`; the stored token includes its leading backslash. Commands
in the closed structural/operator exclusion set below are not symbols:

```text
begin end label nonumber notag left right middle mid quad qquad hspace vspace
mathrm mathrm mathcal mathbf mathbb text operatorname
frac dfrac tfrac partial sum max min int prod lim
equiv le ge lt gt cdot times
bar overline underline hat widehat tilde widetilde star top
```

Every other command is included, so reviewed domain commands such as `\Delta`,
`\E`, `\NPV`, `\delta`, `\pi`, `\beta`, and user `\Macro` remain. The list is
closed for Phase 02; adding/removing an exclusion requires oracle review.

For bare identifiers, first replace every command token (but not its brace
arguments) by one ASCII space, then scan capture group 1 from exact regex
`r"(?<![\\A-Za-z0-9])([A-Za-z][A-Za-z0-9]*)(?![A-Za-z0-9])"`. Underscore is
deliberately a separator, so both `CF` and `i` are visible in `CF_i`. Remove the closed structural words
`begin`, `end`, `label`, `nonumber`, `notag`; retain identifiers inside brace
arguments and roman/mathcal subscripts, which explains `acq`, `I`, and `id` in
the frozen NPV oracle. Sort unique command tokens and identifiers by UTF-8 byte
order. No semantic distinction among variable, function, index, or textual
identifier is claimed in Phase 02.

### P02-W3: Target And Document-Tree Integration

Files:

- `src/mathdevmcp/derivation_target_extraction.py`;
- `src/mathdevmcp/document_derivation_tree.py`;
- `src/mathdevmcp/derivation_audit_report.py` if necessary for the same public
  extraction contract;
- focused compatibility tests.

Changes:

- make block and label extraction consume validated obligations rather than raw
  rows;
- allow lookup by exact source file plus label; bare duplicate labels return an
  explicit ambiguity result, never arbitrary selection;
- emit at most one adapter-eligible target per scoped obligation, with equality
  chains represented structurally rather than truncated at the first `=`;
- never call an equality adapter or backend route planner for ambiguous,
  incomplete, or fallback-only extraction;
- replace `_select_label_rows`, `_display_for_row`, and `_semantic_packet` full-
  display ownership with obligation-level equivalents. Inventories and source
  spans come from owned bytes only;
- preserve additive compatibility fields where safe, but do not manufacture a
  label or complete target for legacy callers.

The existing user changes in `document_derivation_tree.py` are protected. Phase
02 edits must be narrow and layered on top of the P00 quarantine changes; no
quarantine behavior may be reverted or reformatted incidentally.

### P02-W4: Differential Parser Fidelity Route

Files:

- `src/mathdevmcp/parser_benchmark.py`;
- `src/mathdevmcp/parser_policy.py`;
- focused tests and extraction-only parser artifacts.

Changes:

- record exact executable/version evidence for current, LaTeXML, and Pandoc;
- compare label ownership, byte/source span fidelity, row boundaries, nested
  environment identity, and uncertainty on difficult fixtures;
- add an extraction-specific decision that selects a specialist only when it
  materially improves the primary fidelity rubric and can map output back to
  exact source bytes;
- mark disagreement or unresolvable provenance `ambiguous`; do not retain the
  current parser merely because it has line provenance, and do not select a
  specialist merely because it parsed.

No network or installation is authorized. Locally observed versions are
LaTeXML `0.8.6` and Pandoc `2.9.2.1`; formal evidence must remeasure them.

The compact-oracle key `parser_fidelity_profile` is authoritative. Formal
comparison must not call the current directory-recursive benchmark profile or
resolve executable/environment overrides. It uses only the two exact
`/usr/bin` paths, fixed version/fidelity argv, the 13 source allowlist, one
invocation per source, scratch-only outputs/logs/home, fixed environment and
timeouts, and immutable raw receipts. Its seven-bit fidelity vector is compared
lexicographically in the declared priority order. Exact label/span/source
agreement can therefore select or veto; parse success, counts, output size,
runtime, and scalar score cannot.

For the 17 frozen oracle obligations, parser selection is predeclared as
`current` / `p02_lightweight_locator@1` because those complete identities are
constructed from exact source bytes. Differential specialists are validators:
agreement preserves the frozen obligation; disagreement, better specialist
fidelity, or inability to map either output to exact bytes vetoes the frozen
positive expectation and records `parser_ownership_disagreement`; it cannot
rewrite the reviewed payload in place. Materially better specialist fidelity
requires a visible compact/full-oracle amendment and fresh plan review before a
result rerun, thereby honoring the master requirement to use the better route.
For a new, non-frozen input, the
specialist-selection rule remains active, and the selected backend/version
enters the newly constructed obligation identity. Thus availability never wins,
but reviewed frozen identities also cannot drift after implementation.

### P02-W5: Frozen Source Regressions And Evidence Bundle

Files:

- new `tests/test_document_derivation_real_regressions.py` or an equivalently
  focused extraction-only file;
- extraction artifact generator/governance support within the reviewed
  allowlist;
- no source-document edits.

Required frozen assertions:

- `eq:incremental-cash-flow` resolves only in the pinned final-submission file,
  produces one obligation, owns both cash-flow rows, excludes the NPV row, and
  its inventory contains no conditional expectation or summation operator;
- `eq:incremental-npv` is a distinct obligation and digest;
- `eq:foc-k` and `eq:foc-b` are independently retrievable, own disjoint spans,
  and have distinct obligation digests;
- `prop:interior-foc` may expose both child obligations as context but may not
  merge them into one target;
- source digest mismatch is explicit and stops frozen interpretation;
- the durable extraction bundle verifies with the P01 artifact primitives and
  records `backend_request_count: 0`, `source_edit_count: 0`, and publication
  disabled.

## Reviewed Implementation Allowlist

Only these implementation/test paths may change after plan convergence:

- `src/mathdevmcp/equation_locator.py`;
- `src/mathdevmcp/latex_index.py`;
- `src/mathdevmcp/label_scoped_obligation.py` (new);
- `src/mathdevmcp/derivation_target_extraction.py`;
- `src/mathdevmcp/document_derivation_tree.py`;
- `src/mathdevmcp/derivation_audit_report.py` only if the shared extraction
  boundary requires it;
- `src/mathdevmcp/parser_benchmark.py`;
- `src/mathdevmcp/parser_policy.py`;
- `src/mathdevmcp/extraction_evidence.py` (new P02-only schemas/reconstruction);
- `scripts/generate_p02_extraction_evidence.py` (new);
- `scripts/p02_governance.py` (new);
- `tests/test_latex_index.py`;
- `tests/test_derivation_target_extraction.py`;
- `tests/test_label_scoped_obligation.py` (new);
- `tests/test_parser_policy.py`;
- `tests/test_parser_benchmark.py`;
- `tests/test_document_derivation_real_regressions.py` (new);
- `tests/test_document_derivation_tree.py` only for additive compatibility
  assertions required by obligation-level integration;
- `tests/test_document_publication_quarantine.py` only for the P02 no-backend
  extraction quarantine node;
- `tests/test_extraction_evidence.py` (new);
- `tests/p02_no_backend_guard.py` (new fail-closed pytest plugin);
- `tests/test_derivation_audit_report.py` only for the extraction-boundary
  compatibility node required if `derivation_audit_report.py` changes.

The compact and materialized reviewed oracle files and all
`tests/fixtures/label_scoped_obligations/*.tex` files are immutable entry
inputs, not implementation allowlist paths. The two frozen document sources,
P00/P01 records, unrelated dirty paths, CLI, MCP, backend adapters,
semantics/context modules, and P03+ paths are protected. If implementation
requires another path, stop and amend/review this allowlist before editing it.

## Formal Governance And Seal Contract

Formal evidence root is
`.local/mathdevmcp/evidence/p02-20260711`. Plan convergence is followed by a
no-overwrite entry snapshot. The snapshot is created after the agreeing plan
review exists and before any Phase 02 implementation edit. Its fixed strict
`entry/entry-record.json` names the exact agreeing review rather than scanning
for a verdict at runtime, and binds the reviewed plan, compact oracle,
materialized oracle, exact P01 stable/terminal pair, pre-implementation
manifest, protected-dirty manifest, and immutable-input manifest containing
both oracles, all reviewed fixtures, and both frozen sources. The compact
oracle's `entry_snapshot_schema` freezes every key, fixed path, and review
grammar. Only the exact R9 result ref can be the agreeing review for these
final-budget candidate bytes; R10 and later are forbidden. Entry
creation fails if the Phase 02 phase root, entry root, or any target already
exists; preserved partial state requires human recovery, and no entry file is
rewritten or refreshed after implementation begins.

`init-round` reads only that fixed entry record. It reopens every bound file,
strictly parses the named plan review as `AGREE` with the entry plan/compact/
materialized digests, and never discovers a review through a glob, latest-file
rule, or caller argument. Before allocating `rr01`, it requires no predecessor.
Before allocating `rr02` through `rr05`, it derives and verifies the immediately
preceding round's close and terminal close-index as specified below. After all
pre-allocation checks pass, it creates the round and a sorted immutable
`src/tests/scripts` implementation manifest for the current post-implementation
bytes. `implementation_exit` later requires byte equality with that round
manifest; `allowlist` compares it to the pre-implementation entry manifest.

Entry creation is a supervisor bootstrap operation, not a Phase 02 production
action and not evidence that Phase 02 passed. It runs once from the workspace
root with the pinned Python, exact clean six-key environment, `-B -S`, and
`PYTHONPATH=src`, imports only the sealed P01
canonical/no-follow/no-replace primitives, and follows
`governance_action_profile.entry_bootstrap_profile`. The agreeing review ref is
the sole required parameter and must match the closed exact-R9 regex; all
other refs, manifest scopes, hashes, and output paths are derived. Before root
or snapshot work it verifies exact process argv, environment, and runtime
flags; root validation requires real non-symlink Git, source, and local-evidence
ancestor directories; before mkdir it verifies source/profile agreement on external argv, Git
argv, environment, and write order. It may invoke only the exact read-only Git status argv in that profile to enumerate
pre-existing dirty paths. No temporary repo script, shell redirection into the
entry root, glob-selected review, caller-supplied hash, overwrite, or
implementation/test edit is permitted. Before mkdir it derives all 13 unique
reviewed source refs/digests from fixture and frozen cases, requires exact
parser-allowlist equality, strict-decodes each source, applies the exact
comment mask, independently pairs supported begin/end tokens by exact name,
reconstructs each selected outer-to-inner ancestry chain, and requires equality
with the declared ordered outer-plus-nested environment spans. It verifies
every source, environment descriptor/pairing, label token/value, selected-
environment containment, owned, excluded, and owned-span-digest projection. It
strict-loads all 17 materialized records, verifies their canonical bytes,
digests, ids, and exact compact-path coverage, reconstructs canonical
environment stack descriptors/ids and selected descriptor/span/line bounds
from source, and requires exact materialized-identity equality. The operation builds all bytes in
memory, validates them, creates the absent phase and entry directories through
no-follow directory descriptors, then
writes the three manifests and canonical entry record with no-replace
primitives. Before reporting success it requires the new phase tree to contain
only the one entry directory and four expected regular files, reopens all four
outputs, strictly parses the reopened manifests, re-enumerates all three
complete scopes, reopens every current input no-follow, reconstructs each
manifest from current membership and bytes, and requires exact equality. Only
the four separately verified bootstrap outputs are excluded from post-write
dirty enumeration; any fifth output or other new path fails. Any failure after
the first mkdir is an entry-
bootstrap blocker: remove nothing and require human direction; every later
invocation rejects the preserved phase root before reading snapshot inputs.

Result rounds are append-only `rr01`
through `rr05`; a failed or `REVISE` round is closed and never edited.

`src/mathdevmcp/extraction_evidence.py` must define closed canonical P02 schemas
and independent reconstructors without modifying P01 sealed artifacts. It may
reuse P01 canonical JSON, digest, safe read, atomic no-replace write, and bundle
verification primitives. At minimum it defines:

- `p02_extraction_run_manifest@1`;
- `p02_phase_result@1` and the bounded human-result footer parser;
- `p02_entry_record@1`;
- `p02_candidate_decision@1`;
- `p02_final_decision@1`;
- `p02_command_receipt@1` and `p02_receipt_index@1`;
- `p02_round_close@1` and `p02_scoped_repair@1`;
- strict obligation/oracle/parser/mutation summary schemas;
- independent run, candidate, and final-decision reconstruction.

The supervisor writes one immutable round-specific Markdown result before
`bind_result`. It must contain the evidence-contract decision table, actual
commands/receipt heads, three evidence ledgers, external-tool consideration,
default/assumption audit, post-run red team, veto status, non-claims, and the
four exact final footer lines frozen by `human_result_profile`. The footer binds
the round, claimed decision, pre-result receipt-index, and disabled publication
mode. It cannot authorize anything: `bind_result` reopens the exact fixed path,
strictly parses the footer, independently reconstructs the decision, criteria,
vetoes, and non-claims from the receipt prefix and raw artifacts, requires exact
footer agreement, then writes no-overwrite `RR/P02-result.json` under
`p02_phase_result@1`. The receipt binds both the Markdown and machine result
refs/digests. An early failed check therefore gets a reconstructible blocked
result; a fully passing check prefix gets only
`candidate_pass_pending_independent_result_review`, never a final pass.

The P02 candidate decision must bind the exact P01 predecessor pair, plan and
implementation manifests, agreeing reviewed compact-oracle and
materialized-oracle digests plus the oracle/source manifest, both frozen source
digests, run manifest/result,
extraction bundle semantic/file digests, parser comparison, mutation/ambiguity
matrix, zero-backend/source-edit counts, primary criteria, veto map, and
non-claims. Final decision fields are derived only from the verified candidate,
agreeing result review, and exact review-binding receipt head. Stable
publication is a no-overwrite hard link to that audited final candidate and
reruns complete reconstruction and fixed-command verification before linking.

### Zero-backend and zero-source enforcement

`tests/p02_no_backend_guard.py` is loaded by every formal pytest command with
`-p tests.p02_no_backend_guard`. Before collection it atomically creates a
per-command invocation ledger and installs fail-closed wrappers around every
`external_tool_adapters.adapt_*` entry point, `derive_or_refute`, counterexample
and Lean-check entry point, branch-controller execution, and mathematical
backend subprocess/import route. Each forbidden attempt is appended and
fsynced before raising; successful teardown requires the ledger to be empty.
The guard permits only exact LaTeXML/Pandoc version/fidelity argv, environment,
source allowlist, result-round output/log locations, and timeouts in the
reviewed `parser_fidelity_profile`, owned by `parser_benchmark.py`; those
calls go to a separate parser ledger and cannot be
reported as backend evidence. Replacing or bypassing the guard fails teardown.
The module exposes the same `install_guard` context for non-pytest use;
`generate_p02_extraction_evidence.py` imports and installs it before importing
any document-tree, controller, adapter, or backend-capable module, and
governance verifies the guard-attestation record.

The generator runs below the same guard in its own process and embeds reopened
empty invocation ledgers. `backend_request_count` is independently
reconstructed as the total forbidden-attempt entries across all formal
command ledgers, never accepted from a generator or result field. A blocked
attempt still counts and permanently sets `backend_execution_detected`.

At entry, governance writes an immutable SHA-256 manifest for both frozen
documents, both reviewed oracle files, and every reviewed fixture. The
`zero_backend_source_edit_gate` and `protected_check` reopen exact bytes and
derive `source_edit_count` from entry/exit hash differences. The result writer
cannot supply that value. `implementation_exit` independently hashes every
non-cache file below `src`, `tests`, and `scripts`; `allowlist` accepts only
entry-to-exit changes in the reviewed allowlist. Fixture/both-oracle/frozen-
source hashes and all unrelated entry dirty paths must remain identical.

Closed P02 veto ids are:

- `predecessor_binding_failure`;
- `frozen_source_digest_failure`;
- `row_span_or_roundtrip_failure`;
- `label_or_file_ownership_failure`;
- `continuation_or_ambiguity_failure`;
- `duplicate_or_drifting_identity`;
- `cross_label_contamination`;
- `incomplete_target_routed`;
- `parser_fidelity_or_provenance_failure`;
- `artifact_or_bundle_integrity_failure`;
- `oracle_materialization_failure`;
- `independent_review_not_agreed`;
- `backend_execution_detected`;
- `source_edit_detected`;
- `publication_quarantine_failure`;
- `unexpected_implementation_path`;
- `protected_baseline_drift`;
- `governance_chain_failure`.

Closed P02 non-claims are:

- `no_mathematical_certification`;
- `no_semantic_resolution`;
- `no_backend_execution`;
- `no_publication_eligibility`;
- `no_source_document_edit`;
- `no_complete_latex_coverage`;
- `no_phase03_execution`;
- `no_release_readiness`.

The successful fixed action sequence is:

1. `init_round`;
2. `localizer_tests`;
3. `obligation_tests`;
4. `target_integration_tests`;
5. `parser_fidelity_tests`;
6. `frozen_regressions`;
7. `p00_quarantine`;
8. `generate_extraction_bundle`;
9. `mutation_ambiguity_gate`;
10. `zero_backend_source_edit_gate`;
11. `compile`;
12. `protected_check`;
13. `implementation_exit`;
14. `allowlist`;
15. `diff`;
16. `bind_result`;
17. `build_run_manifest`;
18. `build_candidate`;
19. `candidate_gate`;
20. `result_review_binding`;
21. `build_final_candidate`;
22. `final_candidate_gate`;
23. `final_seal_audit_binding`;
24. `stable_publication`.

The failure suffix is not part of that success sequence. It consists of exactly
`bind_scoped_repair` followed by `close_round`, at runtime receipt sequence
numbers determined by the failure point. Both are registered governance-native
actions and both are accepted by `run --action` only when the closed failure
state machine below selects them.

Every action has fixed interpreter-qualified argv, immutable stdout/stderr,
timing/exit receipt, and a complete receipt-index prefix. The result review
binds the candidate and receipt-index 19. The final-seal audit binds the final
candidate, candidate, agreeing review, final validation log, and receipt-index
22. Receipt 24 records stable/final same-inode and same-digest equality. A
post-link receipt failure preserves the link, claims no pass, forbids retry,
and requires human recovery direction.

### Frozen action and reconstruction profile

`PY` below is
`/home/chakwong/miniconda3/envs/tfgpu/bin/python3`; `RR` is the validated
workspace-relative `.local/mathdevmcp/evidence/p02-20260711/result-rounds/rr0N`
root. `init_round` is created only by the distinct external operation
`PY scripts/p02_governance.py init-round --round-root RR`; it is not a value
accepted by `run --action`. Actions 2 through 24 each have exactly one external
dispatcher invocation, `PY scripts/p02_governance.py run --round-root RR
--action ACTION`. Only `result_review_binding` and
`final_seal_audit_binding` append one exact round-specific `--artifact-ref`
value; every other extra argument is rejected.

The dispatcher has exactly two execution classes. A `subprocess` action starts
the one fixed child argv in the table. A `governance_native` action invokes its
named in-process handler exactly once and never calls `p02_governance.py`,
allocates a nested receipt, or launches a subprocess. The external dispatcher
argv is never a child argv. `init-round` is also `governance_native`, but uses
the separate initializer operation and handler.

At process entry, before round-root creation, mutation, log creation, or receipt
allocation, governance requires `MATHDEVMCP_P02_DISPATCH_DEPTH` to be absent.
It then sets it to literal `1` for the initializer/dispatcher scope. Every child
environment includes that value, so direct or indirect re-entry fails at the
same pre-allocation guard. Caller-supplied `MATHDEVMCP_P02_ROUND_ROOT` or
`MATHDEVMCP_P02_ACTION` is also rejected; governance derives them only after
no-symlink round validation.

Subprocess actions receive only the exact environment constructed by
`governance_action_profile.child_environment`: fixed `PATH`, result-round-local
`HOME` and `TMPDIR`, locale, `PYTHONHASHSEED`, `PYTHONPATH`, disabled pytest
plugin autoload, derived round/action values, and dispatch depth. Parser
subprocesses launched inside `parser_fidelity_tests` replace that environment,
rather than inherit it, with the smaller reviewed
`parser_fidelity_profile.environment`. No shell interpolation, wildcard,
alternate interpreter, keyword broadening, executable/environment override,
or caller-supplied extra argument is accepted.

| # | Action | Class / exact handler or child argv | Reconstructed evidence |
|---:|---|---|---|
| 1 | `init_round` | native `p02_native_init_round_v1` through distinct `init-round` | exact P01 pair, reviewed plan/compact-oracle/materialized-oracle/review digests, entry manifests, round predecessor |
| 2 | `localizer_tests` | subprocess `PY -m pytest -q -p tests.p02_no_backend_guard tests/test_latex_index.py` | logs, nonzero collected count, empty backend ledger, oracle row/span matches |
| 3 | `obligation_tests` | subprocess `PY -m pytest -q -p tests.p02_no_backend_guard tests/test_label_scoped_obligation.py tests/test_extraction_evidence.py` | nonzero collected count, strict/golden schemas, all 17 full materialized obligations, compact/full/source three-way equality, canonical bytes, mutation matrix |
| 4 | `target_integration_tests` | subprocess `PY -m pytest -q -p tests.p02_no_backend_guard tests/test_derivation_target_extraction.py tests/test_document_derivation_tree.py::test_document_tree_consumes_label_scoped_obligation_without_backend tests/test_document_derivation_tree.py::test_document_tree_prop_container_keeps_foc_children_separate_without_backend tests/test_derivation_audit_report.py::test_derivation_audit_extraction_boundary_uses_scoped_obligation_without_backend` | exact named nodes must exist; exact targets, no fallback routing, scoped inventories, context-container, quarantine |
| 5 | `parser_fidelity_tests` | subprocess `PY -m pytest -q -p tests.p02_no_backend_guard tests/test_parser_policy.py tests/test_parser_benchmark.py` | nonzero collected count, parser/version ledger, exact fidelity rubric and selection/ambiguity state |
| 6 | `frozen_regressions` | subprocess `PY -m pytest -q -p tests.p02_no_backend_guard tests/test_document_derivation_real_regressions.py` | four exact positive obligations and proposition-container oracle |
| 7 | `p00_quarantine` | subprocess `PY -m pytest -q -p tests.p02_no_backend_guard tests/test_document_publication_quarantine.py::test_edit_target_mismatch_cannot_bypass_compiler_quarantine tests/test_document_publication_quarantine.py::test_p02_extraction_paths_remain_quarantined_without_backend_calls` | exact nodes must exist; publication remains disabled/ineligible on extraction surfaces, empty backend ledger; sealed P01 supplies full P00 regression binding |
| 8 | `generate_extraction_bundle` | subprocess `PY scripts/generate_p02_extraction_evidence.py --round-root RR` | artifacts rebuilt from exact compact/materialized-oracle and source bytes plus empty invocation ledgers |
| 9 | `mutation_ambiguity_gate` | native `p02_native_mutation_ambiguity_gate_v1` | reopen/recompute golden, all 17 materialized identities, and every identity/oracle/ambiguity mutation |
| 10 | `zero_backend_source_edit_gate` | native `p02_native_zero_backend_source_edit_gate_v1` | invocation ledgers empty; immutable-input hashes unchanged |
| 11 | `compile` | subprocess exact `governance_action_profile.actions.compile.child_argv_template` | complete allowlist path inventory equals compiled inventory |
| 12 | `protected_check` | native `p02_native_protected_check_v1` | P01 terminal verification, protected-dirty and immutable-input manifests |
| 13 | `implementation_exit` | native `p02_native_implementation_exit_v1` | complete `src/tests/scripts` exit manifest and aggregate |
| 14 | `allowlist` | native `p02_native_allowlist_v1` | entry/exit delta is a subset of reviewed paths |
| 15 | `diff` | subprocess `/usr/bin/git diff --check` | exact logs/exit; explanatory formatting gate only |
| 16 | `bind_result` | native `p02_native_bind_result_v1` | strict result schema and complete reconstruction from raw artifacts |
| 17 | `build_run_manifest` | native `p02_native_build_run_manifest_v1` | strict run manifest bound to the exact preceding receipt-index head |
| 18 | `build_candidate` | native `p02_native_build_candidate_v1` | independently reconstructed candidate and immutable evidence bindings |
| 19 | `candidate_gate` | native `p02_native_candidate_gate_v1` | reopened candidate equals independent production reconstruction |
| 20 | `result_review_binding` | native `p02_native_result_review_binding_v1` | exact round-specific review bytes/verdict, candidate, and receipt-index 19 |
| 21 | `build_final_candidate` | native `p02_native_build_final_candidate_v1` | verified agreeing review plus candidate and review-binding head |
| 22 | `final_candidate_gate` | native `p02_native_final_candidate_gate_v1` | reopened final candidate equals independent production reconstruction |
| 23 | `final_seal_audit_binding` | native `p02_native_final_seal_audit_binding_v1` | exact round-specific audit bytes/verdict, final/candidate/review/log, and receipt-index 22 |
| 24 | `stable_publication` | native `p02_native_stable_publication_v1` | full reconstruction, no-overwrite link, stable/final same-inode and same-digest equality |

Failure-suffix actions have no success-sequence position:

| Action | Class / exact handler | Reconstructed evidence |
|---|---|---|
| `bind_scoped_repair` | native `p02_native_bind_scoped_repair_v1` | strict fixed-path scoped-repair input, exact triggering artifact, source receipt-index head, close reason, ordered failed actions, and nonempty repair requirements |
| `close_round` | native `p02_native_close_round_v1` | strict round close, every reached-stage ref/digest, entry/predecessor/exit manifests, source/review/audit bindings, log inventory, vetoes/non-claims, and immediately preceding repair-binding head |

### Closed failure and revised-round state machine

An underlying action always appends its own receipt/index even when its measured
exit is nonzero. A dispatcher exit zero means that measurement was durably
recorded; it does not turn a nonzero underlying action into a pass. The next
accepted action is derived only from the verified receipt chain:

1. A nonzero action from `localizer_tests` through `diff` stops the remaining
   checks. The supervisor writes the fixed round-specific human result.
   Governance next accepts `bind_result`; if that succeeds it accepts
   `build_run_manifest`; after that succeeds, or immediately after either
   construction action fails, it accepts only `bind_scoped_repair`.
2. A nonzero `bind_result`, `build_run_manifest`, `build_candidate`,
   `candidate_gate`, `result_review_binding`, `build_final_candidate`,
   `final_candidate_gate`, or `final_seal_audit_binding` accepts only
   `bind_scoped_repair`. No failed chain can enter or resume the success path.
3. A zero-exit `result_review_binding` whose strictly parsed verdict is
   `REVISE`, or a zero-exit `final_seal_audit_binding` whose strictly parsed
   verdict is `REVISE`, accepts only `bind_scoped_repair`. An agreeing review
   follows the success successor.
4. A nonzero `stable_publication` receipt accepts `bind_scoped_repair` only
   when the stable path is still absent. If the stable link exists after any
   publication or receipt/index failure, preserve it, claim no pass, forbid a
   retry or close receipt, set the out-of-chain governance blocker, and require
   human recovery direction.
5. Before `bind_scoped_repair`, the supervisor writes exactly once the fixed
   strict-canonical `RR/inputs/scoped-repair.json`. The action accepts no
   artifact argument, reopens that file plus its triggering artifact and exact
   source receipt-index snapshot, verifies all digests and state-derived close
   fields, and appends its receipt. Its only successor is `close_round`.
6. `close_round` accepts no artifact argument. It requires a zero-exit
   `bind_scoped_repair` head, constructs `RR/round-close.json` once from reopened
   chain/artifact bytes, and appends the terminal close receipt/index. A failed
   repair-binding or close action cannot be retried and is a
   `governance_chain_failure` requiring human direction.
7. Any failure to append or immediately verify a receipt/index leaves no
   trusted successor. It is a governance-chain stop, not permission to rerun an
   action or manufacture a close.

`p02_scoped_repair@1` has exactly `schema_version`, `phase`, `result_round`,
`close_reason`, `failed_actions`, `source_artifact_ref`,
`source_artifact_sha256`, `source_receipt_index_ref`,
`source_receipt_index_sha256`, and `repairs`. `close_reason` is exactly one of
`measured_action_failure`, `result_review_revise`, or
`final_seal_audit_revise`. `failed_actions` is the ordered nonempty list of all
nonzero receipt action ids for `measured_action_failure` and is empty for a
verified `REVISE`. The triggering source is the first failed canonical receipt
for a measured failure, the exact result-review file for result-review revise,
or the exact final-seal-audit file for final-seal revise. Its source index is
the immutable index headed by that trigger. `repairs` is nonempty and each
entry has exactly `finding_id`, `source_stage`, `severity`, `affected_paths`,
`required_change`, `required_check_ids`, and `non_claim`; enums, ordering, and
path scope are frozen by the compact oracle.

`p02_round_close@1` has exactly the keys frozen by
`governance_action_profile.round_close_schema`. It binds the scoped-repair
record, triggering artifact/index, the immediately preceding
`bind_scoped_repair` index, entry and round implementation manifests, exact P01
predecessor pair, prior P02 close/index pair when present, every reached result/
run/candidate/review/final/audit ref/digest pair, ordered logs, complete P02
veto map, non-claims, and repairs. Stage pairs are both null before an
unreached stage and both non-null only after a zero-exit binding/construction
receipt. A revised review/audit is bound even though it does not authorize the
next success stage. `independent_review_not_agreed` is true for either verified
`REVISE`; measured failures set the action-specific vetoes derived by the
compact registry. A canonical close always has at least one true veto and never
claims pass.

For `rrNN` after `rr01`, `init-round` requires the immediately preceding
`rr(NN-1)/round-close.json` plus its terminal receipt-index. It reopens both,
requires the terminal action to be zero-exit `close_round`, recomputes the
round-close digest and its binding from that receipt, verifies the close's
preceding repair-binding head, and rejects skipped round numbers or any
nonterminal/success-path index. Thus a repaired round cannot overwrite, rename,
or bypass its failed predecessor.

The compact oracle's `governance_action_profile` is the machine-readable
authority for both external and child argv templates, handler ids, action
order, exact compile inventory, environment construction, artifact-ref grammar,
and receipt fields. Governance rejects any one-token difference.

Every `p02_command_receipt@1` includes `execution_class`, `handler_id`,
`external_argv`, `child_argv`, and `child_environment_sha256`. For subprocess
actions, `execution_class` is `subprocess`, `handler_id` is null, and both child
fields are populated from the exact executed values. For governance-native
actions, `execution_class` is `governance_native`, `handler_id` is the exact
`p02_native_ACTION_v1` identifier, and both child fields are null. The
initializer follows the native rule. Receipt validation rejects any other
nullability or any equality between `external_argv` and non-null `child_argv`.
Each receipt also binds immutable stdout/stderr byte digest/count, exit/timing,
a closed action-specific binding map, prior head, and a complete immutable
receipt-index prefix.

Independent reconstruction trusts no generated summary or boolean. Run
reconstruction opens the exact receipt prefix, command logs/ledgers, entry/exit
manifests, both oracle files/source bytes, bundle/index, parser comparison,
mutation matrix, and result bytes, then derives every count, criterion, veto, and
digest. Candidate reconstruction reruns run reconstruction and exact field
equality. Final reconstruction reruns candidate reconstruction and parses the
bounded review binding from exact bytes. Candidate gate, final-candidate gate,
and stable publication each reopen and byte-compare the production record to
independent reconstruction. No candidate/final field is copied from a prior
decision without recomputation.

## Required Artifacts

- this subplan and all independent plan-review records;
- exact P01 stable/terminal predecessor verification log;
- P02 entry implementation/protected/source manifests;
- compact microfixture/frozen-source oracle with exact owned/excluded spans and
  its bound complete materialized-obligations oracle;
- canonical obligation schema, all 17 full identity vectors,
  golden/adversarial vectors, and compact/full/source reconstruction log;
- extraction-only bundle and bundle index;
- parser executable/version and fidelity comparison records;
- ambiguity/mutation matrix, including label, file, span, continuation reason,
  sibling row, source digest, operator inventory, and obligation digest tamper;
- fixed command receipts/logs and run manifest for each formal result round;
- Phase 02 human result, candidate decision, independent result review, final
  seal, stable decision, and terminal receipt/index, or an append-only blocker
  close;
- refreshed Phase 03 subplan only after a stable Phase 02 pass.

## Required Checks, Tests, And Reviews

Development diagnostics, smallest first:

```bash
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q -p tests.p02_no_backend_guard tests/test_label_scoped_obligation.py tests/test_extraction_evidence.py
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q -p tests.p02_no_backend_guard tests/test_latex_index.py tests/test_derivation_target_extraction.py
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q -p tests.p02_no_backend_guard tests/test_parser_policy.py tests/test_parser_benchmark.py
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q -p tests.p02_no_backend_guard tests/test_document_derivation_real_regressions.py
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m pytest -q -p tests.p02_no_backend_guard tests/test_document_publication_quarantine.py::test_p02_extraction_paths_remain_quarantined_without_backend_calls
env PYTHONPATH=src /home/chakwong/miniconda3/envs/tfgpu/bin/python3 -m py_compile src/mathdevmcp/equation_locator.py src/mathdevmcp/latex_index.py src/mathdevmcp/label_scoped_obligation.py src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/parser_policy.py src/mathdevmcp/parser_benchmark.py src/mathdevmcp/document_derivation_tree.py src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/extraction_evidence.py scripts/generate_p02_extraction_evidence.py scripts/p02_governance.py tests/p02_no_backend_guard.py tests/test_latex_index.py tests/test_derivation_target_extraction.py tests/test_label_scoped_obligation.py tests/test_parser_policy.py tests/test_parser_benchmark.py tests/test_document_derivation_real_regressions.py tests/test_document_derivation_tree.py tests/test_derivation_audit_report.py tests/test_extraction_evidence.py tests/test_document_publication_quarantine.py
git diff --check
```

Formal execution must use fixed receipt commands and append-only result rounds,
binding the exact P01 handoff, entry manifests, frozen source digests, result,
run manifest, candidate, review, final candidate, final-seal audit, and stable
publication. The Phase 01 governance implementation may be generalized only by
a separately reviewed P02 governance design; do not copy P01 constants and
pretend they constitute a P02 seal.

A fresh independent read-only reviewer must review this material subplan before
implementation. Review covers baseline correctness, row/grouping grammar,
canonical obligation schema, file/duplicate-label identity, frozen oracles,
parser fidelity rubric, zero-backend boundary, artifact/receipt seal design,
allowlist, checks, stop conditions, and P03 separation. Fixable findings patch
this same subplan visibly and rerun focused plan checks. Four historical
substantive rounds ended `REVISE`. The human supervisor explicitly authorized
up to five additional substantive Phase 02 plan-review rounds on 2026-07-11,
numbered R5 through R9; stop if the same material blocker remains unresolved at
the end of that additional budget. Silence, timeout, or a worker that returns no
verdict consumes no substantive round and is not agreement. This extension is
review budget only and grants no implementation, runtime, publication, source-
edit, product, model-file, funding, or scientific-claim authority.

After implementation, a fresh reviewer inspects the exact diff, obligations,
owned/excluded span table, parser comparison, mutation/ambiguity matrix,
receipts, run manifest, result, and candidate digest. A separate fresh final-
seal audit is required before stable publication. Reviewers are read-only and
cannot authorize source edits, backend runs, publication re-enablement, or
Phase 03 work.

## Evidence Ledgers

- Engineering correctness: parser/localizer behavior, span round-trip,
  deterministic canonical identity, store/reopen behavior, compatibility, and
  zero backend invocation.
- Extraction validity: source/label ownership, continuation justification,
  complete target structure, scoped inventories, duplicate ambiguity, and
  parser fidelity.
- Mathematical validity: always `not_tested`; no obligation is proved or
  refuted in Phase 02.
- Interpretation: a pass establishes only trustworthy extraction for the
  reviewed fixtures and frozen labels, not complete LaTeX coverage or document
  correctness.

## Forbidden Claims And Actions

- Do not enable repair publication or experimental publication.
- Do not execute SymPy, Sage, Lean, LeanSearch-v2, LeanExplore, jixia,
  Pantograph, LeanDojo, or any other mathematical backend for a Phase 02 target.
- Do not run the document derivation tree with positive backend attempts.
- Do not edit either frozen source document.
- Do not infer semantics, roles, assumptions, proof, counterexample, or
  mathematical blockers from extraction output.
- Do not treat a parser's availability, parse success, label recall, or output
  size alone as promotion evidence.
- Do not silently choose among duplicate labels in different files.
- Do not attach an unlabeled row by proximity alone or manufacture lhs/rhs.
- Do not route ambiguous/incomplete extraction downstream.
- Do not modify P03+ semantics, context, scheduling, backend, ranking,
  presentation, or publication capability.
- Do not install packages, use network/GPU, commit/push, perform destructive
  actions, or overwrite sealed P00/P01/P02 artifacts.

## Stop Conditions

Stop Phase 02, retain P00 quarantine and the P01 stable decision, write an
append-only blocker result, and leave Phase 03 closed if:

- either exact P01 predecessor digest changes or its terminal chain no longer
  verifies;
- either frozen source digest changes without a reviewed two-version amendment;
- compact/materialized oracle bytes, their binding, or independent source-byte
  reconstruction disagree;
- the row/continuation grammar remains ambiguous after the additional five
  human-authorized substantive plan-review rounds;
- any required fixture cannot express an exact owned/excluded span oracle;
- a label can still absorb sibling-label bytes/operators or resolve to the
  wrong file;
- duplicate obligation ids, digest drift, overlapping/invalid spans, or a
  mutation accepted by validation remains after the additional five human-
  authorized substantive repair/review rounds;
- ambiguous or incomplete extraction reaches an equality adapter/backend route;
- any backend request or source edit occurs;
- P00 quarantine or P01 integrity regress;
- specialist parser selection lacks exact source-fidelity evidence;
- work requires an unreviewed file, dependency, network/install, destructive
  action, product/default-policy decision, or P03+ implementation;
- the stable link is created but terminal sealing fails; preserve it, claim no
  pass, and require human recovery direction.

Ordinary focused test failures and fixable scoped review findings enter the
visible repair loop and are not stop reasons by themselves.

## Exact Next-Phase Handoff Conditions

Phase 03 planning opens only if all of the following are sealed:

- stable P02 decision `pass`, publication disabled, every P02 veto false;
- terminal P02 receipt/index binds the exact P01 stable and terminal-index
  digests plus the same P02 stable decision bytes/inode;
- exact frozen source digests match;
- compact oracle, materialized oracle, and independent source-byte
  reconstruction agree for all 17 complete identity payloads, byte counts,
  digests, and ids;
- all four frozen equation labels are `valid_complete`, adapter eligible, and
  match every exact oracle field; none may pass as ambiguous, orphaned,
  invalid, fallback, or manufactured;
- every positive microfixture, including aligned definition, nested chain,
  comment/non-ASCII byte offsets, label placement, and file-scoped duplicate
  lookup, is `valid_complete` with exact oracle output;
- only the designated multi-label-conflict and orphan fixtures may be
  `ambiguous`/`orphaned`, with no adapter-eligible target; bare duplicate-label
  lookup is ambiguous while both exact-file lookups remain valid;
- `prop:interior-foc` is exactly `context_container` with ordered children
  `eq:foc-k`, `eq:foc-b`, zero adapter-eligible container targets, and no merged
  equation target;
- `eq:incremental-cash-flow` owns only cash-flow rows and excludes NPV
  expectation/summation operators;
- `eq:foc-k` and `eq:foc-b` are independently retrievable with disjoint spans
  and distinct obligation digests;
- mutation, ambiguity, duplicate-label, parser-disagreement, no-backend,
  quarantine, compatibility, and artifact-reopen gates pass;
- extraction-only bundle and parser comparison verify from disk;
- independent material plan/result reviews and fresh final-seal audit agree;
- Phase 03 consumes exact stable P02/P01 digests and does not infer semantic or
  mathematical correctness from extraction validity.

At the end of Phase 02, write the phase result/close, refresh the stop handoff,
draft the Phase 03 subplan only on stable pass, and review that next subplan for
consistency, feasibility, artifact coverage, default discipline, and boundary
safety before any Phase 03 implementation.
