# Independent Code And Evidence Review: Generic Semantic Equation Audit

Date: 2026-07-22

Verdict: **REVISE**

Scope: read-only review of Phases 1-4 of
`docs/plans/mathdevmcp-generic-semantic-equation-audit-master-program-2026-07-22.md`.
Inspected `src/mathdevmcp/applied_math_semantics.py`, its integration in
`src/mathdevmcp/applied_math_audit.py`, the semantic fixture corpus and tests,
and the public README contracts. Same-paper answer-key and comparison artifacts
were not inspected.

## Findings

### 1. High: Relation selection crosses source documents and has no locality bound

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:559-564` combines blocks from all
  source packets into one global profile list.
- `src/mathdevmcp/applied_math_semantics.py:405-412` groups that global list
  only by inferred role.
- `src/mathdevmcp/applied_math_semantics.py:464-485` pairs level and linearized
  profiles by normalized left-hand symbols and a generic object cue, without
  requiring a shared source packet, source digest, page neighborhood, section,
  or explicit cross-reference.
- Master plan lines 204-228 require conservative hypotheses, distant-reference
  checks, and zero false relations.

A read-only probe with a level equation in `a.pdf` and a linearized equation in
`b.pdf` produced one `level_to_linearized` hypothesis and a
`supported_tension`; the hypothesis explicitly contained both source packet
IDs, and `semantic_validation_errors` was empty. Another probe put two unrelated
equations forty prose lines apart in one source and also produced a tension.

This is a false-pairing defect, not merely low recall. The public tool accepts
multiple sources, so cross-document pairing is reachable through the supported
orchestrator. Pairing must be partitioned by source identity and then require a
bounded, evidenced relation within that source. A distant explicit reference
needs a distinct supported route; distance cannot be ignored.

Required fix: partition candidate selection by source packet/digest, require an
explicit or bounded source-local relation predicate, encode that predicate and
distance in the hypothesis evidence, and add cross-PDF, distant-section,
same-symbol/different-object, and explicit-distant-reference tests.

### 2. High: A label after a form feed can bind the previous page's formula to a current-page block

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:90-97` computes `page_start` but
  does not use it to clamp `equation_start` or `raw_lines`.
- `src/mathdevmcp/applied_math_semantics.py:127-150` selects a preceding
  equality without rejecting a form-feed crossing.
- `src/mathdevmcp/applied_math_semantics.py:151-171` assigns the label's page to
  the resulting block even when its raw/formula text came from the prior page.
- Master plan lines 156-177 forbid silent page-boundary crossing and require an
  exact page/line identity.

For parser text containing a formula on page 1, a form feed, prose on page 2,
and standalone `(A.1)` on page 2, the block was anchored as page 2 but its
`raw_text` and `formula_text` included the page-1 equation. Validation reported
no error. The stored line range was document-global while the page field implied
a page-local range, further making the anchor ambiguous.

Required fix: hard-clamp every raw, formula, context, and inherited-role window
to a single page; reject or explicitly abstain when a label cannot bind to a
same-page display; define whether line offsets are page-local or document-global
and validate them against the packet text. Add label-before/after-form-feed,
empty-page, and split-display boundary tests.

### 3. High: The normalization sign check reports algebraically consistent layouts as tensions

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:200-207` classifies the entire
  right-hand side only by its first character.
- `src/mathdevmcp/applied_math_semantics.py:414-420` equates a positive-leading
  RHS with a positive movement of the return term.
- Master plan lines 204-221 require normalization sign/timing comparison, not a
  first-character proxy.

For the normalization `M_t/M_{t-1} R_{t-1}=1`, the algebraically consistent
linearized form `m_t = z_t - r_{t-1}` produced
`normalization_sign_tension` and a public `supported_tension`. The equivalent
layout `m_t + r_{t-1} = z_t` did the same. The code does not locate the return
term, determine its side, or determine its signed coefficient; `rhs_sign` is not
the claimed mathematical quantity.

Claimed target: the sign and date of the return movement implied by the unit
product normalization. Actual quantity: whether the last equality's RHS begins
with `-`. They are different. The emitted tension is wrong relative to the
stated target.

Required fix: represent signed terms and equation side for the identified
movement family, or abstain when that structure cannot be recovered. Test
permuted term order, movement on either side, subtraction after another term,
unary signs, OCR spacing, and unresolved multiple-return expressions.

### 4. High: Coefficient and ownership checks can silently certify mismatches as `no_tension`

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:384-390` declares coefficient
  families equivalent when the two equations share any one coefficient.
- `src/mathdevmcp/applied_math_semantics.py:486-496` turns that set-intersection
  proxy into `no_semantic_tension_nominated`.
- `src/mathdevmcp/applied_math_semantics.py:272-280` resolves conflicting scope
  prose by always choosing aggregate first.
- `src/mathdevmcp/applied_math_semantics.py:438-457` treats two shared generic
  symbol families as preservation when the linearized scope is unresolved.

A level response with coefficients `{alpha, beta}` and a linearized response
with `{alpha, gamma}` was reported `no_tension` because the incidental intercept
`alpha` overlapped, even though the response coefficient changed from `beta` to
`gamma`. Separately, an entity-specific level relation and a linearized relation
that dropped the entity superscripts was reported
`ownership_scope_preserved_by_bound_symbols` because generic `P/K/S/B` families
overlapped. Prose containing both entity-specific and aggregate scope is also
resolved to aggregate rather than marked conflicted.

These no-tension outcomes are unsupported. The code has no term-to-coefficient
alignment or ownership-qualified symbol identity from which preservation
follows.

Required fix: compare coefficients attached to mapped material terms, preserve
qualifiers/superscripts in symbol families, represent conflicting scope as
ambiguous, and abstain instead of inferring preservation from generic symbol
overlap. Add incidental-shared-coefficient, dropped-superscript, conflicting-
scope, and renamed-term alignment tests.

### 5. High: The whole-artifact validator does not enforce the advertised reference or source integrity

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:577-641` validates only a subset of
  the versioned records and references.
- `src/mathdevmcp/applied_math_audit.py:611-625` publishes validator errors but
  always reports `completed_with_limits`.
- Master plan lines 96-111 require every reference and source/extraction digest
  to resolve, plus authentication/disposition enforcement.

Read-only mutation probes showed that all of the following corruptions return an
empty validation-error list:

- unknown hypothesis `block_refs`;
- unknown hypothesis `source_packet_refs`;
- unknown finding evidence-chain packets, objects, edges, or check;
- a profile authentication state changed independently of its block/packet;
- a block source digest changed to a different valid-looking SHA-256.

The validator also does not verify block text/digests against the source packet,
profile packet/authentication equality with its block, hypothesis endpoint
source coherence, check outcome/kind enums, finding semantic refs against its
evidence chain, deterministic ID recomputation, or duplicate labels. Cue-span
validation checks only a permissive combined length and does not record which
text coordinate space each cue uses.

Required fix: implement full graph and content validation, including exact
packet-to-block digest/text/anchor binding, profile-to-block field inheritance,
hypothesis/check/finding reference parity, allowed states/outcomes, deterministic
ID recomputation, cue coordinate-space identity, and duplicate-label
disposition. Semantic validation errors must veto semantic findings or make the
public result fail closed rather than merely increment a summary counter.

### 6. High: The planned timing comparison is not implemented

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:342` extracts a limited list of time
  shift strings.
- `src/mathdevmcp/applied_math_semantics.py:405-508` never reads `time_shifts`
  and has no timing check.
- Master plan lines 15-18 and 204-221 include timing and lag/lead movement in the
  bounded target and required Phase 3 checks.

The implementation can emit a normalization sign check but cannot compare the
normalization date with the movement date, nor compare timing across level and
linearized endpoints. Therefore Phase 3 is incomplete even on its stated
engineering scope.

Required fix: either add a source-bound, term-specific timing validator with
positive/negative/ambiguous cases or explicitly remove timing from the
implemented Phase 1-4 claim. The current extraction also needs tests for
subscripts/braces, Unicode minus, leads, multiple dates, and OCR variants.

### 7. Medium: Detailed audit artifacts are mutable at a supposedly immutable identity

Anchors:

- `src/mathdevmcp/applied_math_audit.py:644-659` derives the artifact filename
  from source records and request options but omits extraction/parser output,
  then writes with replace semantics.
- `README.md:181-186` calls the detailed artifact immutable and instructs users
  to resolve it later by exact digest.

Two runs over the same PDF and request options with different same-length parser
bodies produced the same artifact path and different artifact digests. The
second run overwrote the first bytes, after which paging with the first returned
digest failed. Thus an already returned artifact reference is not durable.

Required fix: name artifacts by the canonical detailed payload digest or include
the exact extraction identity in a no-replace request identity, and use
collision-safe immutable persistence. Add a repeat-request test with changed
provider output and verify that every previously returned path/digest remains
resolvable.

### 8. Medium: The claimed exact corpus oracle is partial and omits the adversarial cases that exposed these defects

Anchors:

- `tests/test_applied_math_semantics.py:30-58` compares only block labels, role
  values, hypothesis/check kinds, finding check kinds, and forbidden
  dispositions.
- `tests/fixtures/applied_math_semantics/corpus.json:1-186` contains twelve
  parser-only cases but no corpus digest, per-case source digest oracle, exact
  blocks, profiles, cue spans, endpoints, reference graph, outcomes/reasons, or
  expected IDs.
- `tests/test_applied_math_semantics.py:41-43` converts profiles to a label-keyed
  dictionary, so duplicate labels silently overwrite one another.

The tests called an `exact_oracle` do not enforce the master plan's zero
unexpected field/reference output. They also omit cross-source pairing, distant
unrelated equations, page-boundary labels, duplicate labels, alternative
algebraic layouts, incidental coefficient overlap, conflicting ownership cues,
corrupted semantic references, provider-output artifact collision, and timing
comparison. The two additional tests at lines 101-159 encode narrow positive
behavior and include an unsupported ownership-preservation expectation.

Required fix: make the corpus content-addressed, freeze full canonical expected
records or an equally strict stage-by-stage oracle, assert exact counts and
referential fields, and add the adversarial cases above. The existing corpus
passing is evidence only for those twelve handcrafted layouts.

## Checks Run

- `PYTHONPATH=src pytest -q tests/test_applied_math_semantics.py tests/test_applied_math_audit.py`
  - 36 passed.
- `PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_stdio_smoke.py tests/test_mcp_surface_sync.py`
  - 68 passed.
- Read-only targeted probes reproduced cross-source and distant pairing,
  page-boundary misbinding, false normalization tension, missed coefficient and
  ownership mismatches, incomplete semantic validation, and artifact overwrite.

No literal paper name, disclosed source digest, target equation number, or named
same-paper issue token was found in the reviewed production semantic module.
Parser-derived semantic findings remain `supported_tension`; no parser-only
promotion to `confirmed_defect` or `consistent_under_checked_assumptions` was
observed. Paging allowlisting and compact semantic counts are implemented, and
the focused public-surface tests pass. These controls do not offset the false
pairing and evidence-integrity defects above.

## Verdict

**REVISE.** Phases 1-4 are not satisfied. Phase 1 silently crosses page
boundaries; Phase 3 makes false relation and semantic classifications and omits
timing; Phase 4's whole-artifact validation and immutable artifact identity are
not enforced. The master plan makes unresolved high-severity findings a Phase 4
stop condition, so same-paper replay should not be treated as promotion evidence
until these issues are repaired and independently re-reviewed.
