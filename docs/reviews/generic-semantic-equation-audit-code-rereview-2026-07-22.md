# Independent Re-Review: Generic Semantic Equation Audit Phase 1-4 Repair

Date: 2026-07-22

Verdict: **REVISE**

Scope: read-only independent re-review of the repaired Phase 1-4 implementation
against the prior review and
`docs/plans/mathdevmcp-generic-semantic-equation-audit-phase-04-repair-result-2026-07-22.md`.
Same-paper comparison and answer-key artifacts were not inspected.

## Findings

### 1. High: Source-locality bounds still authorize false equation pairing across explicitly different objects

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:456-482` treats any two profiles in
  one source within one page and 48 global parser lines as a valid relation
  basis; object identity is not part of the predicate.
- `src/mathdevmcp/applied_math_semantics.py:403-409` records every textual label
  mention as an `explicit_label_ref`, without classifying whether the prose
  asserts, denies, or merely cites a relation.
- `src/mathdevmcp/applied_math_semantics.py:563-587` pairs ownership endpoints
  using only shared normalized LHS families plus that locality predicate.
- `src/mathdevmcp/applied_math_semantics.py:592-632` similarly pairs
  level/linearized endpoints using normalized LHS families and generic
  `return`/`response index` cues.

Read-only probes produced the following false `supported_tension` findings with
empty semantic validation errors:

- a level **bond** return followed by an explicitly unrelated **equity** return
  with the same normalized `j` LHS family produced
  `coefficient_family_mismatch`;
- a **team** ownership definition followed by the starting capital of a
  **different division** produced `ownership_scope_mismatch`;
- a customer response index followed by a different employee response index
  produced `coefficient_family_mismatch`;
- distant prose saying `Unlike the unrelated accounting equation (A.1)` or
  `see equation (A.1); no mathematical relation is intended` enabled
  `explicit_label_cross_reference` pairing and a tension.

The relation evidence stored at `src/mathdevmcp/applied_math_semantics.py:616`
is only `shared left-object family` and `linearization object cue`; it does not
record the actual object identity, cue spans establishing sameness, or the
assertive polarity of an explicit reference. Thus the repaired code fixes
cross-file pairing and unbounded unreferenced pairing, but it still fails the
Phase 3 zero-false-relation boundary.

Required fix: model source-local object identity separately from generic object
class; require affirmative relation evidence or a unique, sufficiently specific
object mapping; treat negated, contrastive, bibliographic, and bare label
mentions as abstentions. Add same-symbol/different-object tests for return,
response, and ownership routes, plus negative and non-relational label-reference
tests.

### 2. High: Normalization sign parsing still reports algebraically consistent expressions as tensions

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:229-248` assigns a return term's sign
  only from whether the text immediately preceding the token ends in `-`.
- `src/mathdevmcp/applied_math_semantics.py:547-559` turns that lexical sign into
  a public normalization tension.
- The repair record lines 15 and 20 claim reordered consistent layouts pass and
  that adversarial normalization permutations were added.

For `M_t/M_{t-1} R_{t-1}=1`, both of these algebraically consistent movements
produced `normalization_sign_tension` and a semantic `supported_tension`:

- `m_t = z_t - (r_{t-1})`;
- `m_t = z_t - 1*r_{t-1}`.

The parser sees `(` or `1*` immediately before `r`, so it labels the movement
positive. The same problem occurs for `-(1/2) r_{t-1}`. This is wrong relative
to the claimed normalization-sign target, not merely an unsupported recall
case.

Required fix: parse the signed additive term containing the return, including
parentheses and explicit scalar factors, or abstain whenever the term sign
cannot be established. Add parenthesized, scalar-multiplied, nested unary-sign,
and OCR-spacing cases on both equation sides.

### 3. High: Whole-artifact validation checks graph shape but not semantic content or verdict consistency

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:786-815` validates profile
  inheritance, IDs, and cue coordinates but does not rebuild the profile from
  its block or compare any candidate value with the rebuilt value.
- `src/mathdevmcp/applied_math_semantics.py:817-831` does not compare the stored
  `relation_basis` with `_relation_basis(endpoints)` or validate hypothesis kind
  against endpoint roles.
- `src/mathdevmcp/applied_math_semantics.py:833-845` validates check references,
  outcome vocabulary, and ID shape but does not rerun the semantic check or
  enforce kind/outcome compatibility.
- `src/mathdevmcp/applied_math_semantics.py:849-865` does not bind finding
  summary, evidence check kind, family, or evidence-chain result to the linked
  check.
- The repair record line 17 claims whole-artifact source coherence and
  check/hypothesis/finding parity.

All of these read-only mutations returned an empty validation-error list:

- change a profile role or material coefficient value without changing its
  source block;
- replace the stored relation basis with an explicit-reference basis pointing
  to a missing packet and distance 999;
- change a tension check's `outcome` to `no_tension`;
- construct an internally ID-consistent `no_semantic_tension_nominated` check
  and remove the finding for source profiles that actually yield a coefficient
  mismatch;
- change a linked tension kind to `leading_sign_mismatch` while updating the
  check/finding IDs and references coherently;
- change a finding's evidence check kind, summary, or evidence-chain result to
  claim `confirmed_defect`/`no_tension`.

`build_semantic_audit` correctly withholds findings when its validator reports
an error (`src/mathdevmcp/applied_math_semantics.py:696-713`), but these semantic
corruptions are not reported. Therefore the fail-closed guarantee does not
cover the mathematical/semantic content the artifact purports to preserve.

Required fix: rebuild canonical profiles, hypotheses, checks, and findings from
the bound blocks/packets and compare complete canonical records, or perform
equivalent field-by-field semantic validation. In particular, recompute profile
values, exact relation basis, hypothesis eligibility/kind, check kind/outcome,
and the full finding envelope from the linked check.

### 4. High: Unresolved normalization timing is silently classified as `no_tension`

Anchors:

- `src/mathdevmcp/applied_math_semantics.py:266-274` returns `None` when the
  normalization has zero or multiple uniquely dated return terms.
- `src/mathdevmcp/applied_math_semantics.py:550-559` treats `None` timing as a
  no-tension result whenever the movement sign is negative.
- The repair record lines 15 and 18 say multiple-return layouts abstain and that
  the normalization return date is compared with the uniquely located movement
  date.

The normalization `M_t/M_{t-1} R^a_{t-1} R^b_t = 1` with movement
`m_t = -r^a_{t-1} + z_t` produced `no_semantic_tension_nominated`, not an
abstention, even though the normalization contains two return dates and
`normalization_return_time` is unresolved. A normalization whose return has no
recoverable date behaves the same way.

This is a fail-open negative classification. It does not emit a substantive
finding, but it contradicts the explicit ambiguity contract and can make the
semantic check ledger claim that no tension was nominated without having
performed the promised timing comparison.

Required fix: emit a dedicated normalization-time abstention whenever
`normalization_return_time` is unresolved; distinguish missing, multiple, and
unsupported date syntax. Add multiple normalization-return, undated return,
multiple `=1` relation, and unsupported lag-order cases.

### 5. Medium: The new tests cover the first review's exact probes but not the residual semantic boundaries

Anchors:

- `tests/test_applied_math_semantics.py:164-224` covers cross-source and simple
  distant reference behavior, but not same-source different-object or negative
  reference semantics.
- `tests/test_applied_math_semantics.py:252-285` covers two reordered
  normalization forms and multiple movement returns, but not parentheses,
  scalar factors, or ambiguity in the normalization relation itself.
- `tests/test_applied_math_semantics.py:357-373` mutates structural references
  and authentication inheritance only; it does not mutate semantic values,
  relation basis content, check verdicts, or finding meaning.

The repaired corpus and regression suite therefore do not yet establish the
Phase 4 whole-artifact or Phase 3 zero-false-relation criteria outside the exact
repair examples.

## Prior Findings Rechecked

The following prior issues are materially repaired:

- cross-source relations are rejected;
- distant unreferenced relations are rejected;
- block raw/formula/context windows no longer cross form-feed boundaries;
- incidental coefficient overlap no longer establishes equivalence;
- conflicting or one-sided ownership scope abstains;
- duplicate labels and the previously tested broken graph references are
  detected, and detected validation failure withholds semantic findings;
- detailed artifacts are now content-addressed and written no-replace; changed
  provider output yields a second durable path and the first digest remains
  pageable;
- parser-only semantic findings remain `supported_tension`; no promotion to
  `confirmed_defect` or checked consistency was observed;
- the repair record explicitly disclaims broad level/linearized timing
  equivalence. Public README text makes no broader timing claim.

No reviewed production/test source contained the paper name, disclosed target
digests, target equation labels, or named same-paper issue phrases.

## Checks Run

- `PYTHONPATH=src pytest -q tests/test_applied_math_semantics.py tests/test_applied_math_audit.py`
  - 58 passed.
- `PYTHONPATH=src pytest -q tests/test_mcp_facade.py tests/test_mcp_server.py tests/test_mcp_stdio_smoke.py tests/test_mcp_surface_sync.py tests/test_research_assistant_pdf.py`
  - 76 passed.
- `PYTHONPATH=src python -m compileall -q src tests`
  - passed.
- `git diff --check`
  - passed.
- Targeted read-only probes reproduced every residual issue above and confirmed
  the listed repaired behaviors.

## Verdict

**REVISE.** The repair closes several concrete defects, but high-severity
semantic correctness and evidence-integrity issues remain. The Phase 4 stop
condition still applies: same-paper replay may remain diagnostic, but it must
not be used as Phase 1-4 promotion evidence until false object pairing,
normalization term parsing/ambiguity, and canonical semantic validation are
repaired and independently re-reviewed.
