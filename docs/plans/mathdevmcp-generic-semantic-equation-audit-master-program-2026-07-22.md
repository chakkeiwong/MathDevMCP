# Generic Semantic Equation Audit Master Program

Date: 2026-07-22

Status: Phase 1-4 repairs implemented; pending final independent re-review

## Mission And Bounded Target

Improve the experimental `audit_applied_math_document` workflow at the root
cause exposed by Fresh R5: source and claim integrity are now fail-closed, but
generic semantic discovery remains shallow. The bounded target is a reusable,
discipline-neutral semantic pass for labeled equation blocks in applied
economics, finance, marketing, management, and related social science.

The system may nominate source-bound sign, coefficient, normalization,
normalization-term timing, ownership-domain, and level-to-linearized tensions.
It does not implement broad timing equivalence across arbitrary equations. It may not authenticate
parser transcription, infer author intent, or promote a PDF-only relation to a
confirmed mathematical defect.

## Baseline And Gaps

Fresh R5 is the frozen baseline:

- source digests: `bb3f7278...fd29` and `c02de985...e4052`;
- artifact digest:
  `7bff5934a88fd8cda0e0f3b4f48a3a1edf89c7397b500fb93ff73bebd812a244`;
- 11 source-bound `supported_tension` findings, zero confirmed defects, zero
  claim-IR validation errors;
- seven-item comparison: 3 exact, 1 partial, 3 missed;
- missed: deposit-return normalization/sign/timing, entrant bank-held ownership
  domain, and long-bond sign/coefficient consistency;
- partial: timing/object separation across the level and linearized blocks;
- eight selected obligation families remain `not_checkable`.

Root causes:

1. PDF labels and formulas are split across lines, but extraction operates on
   individual lines rather than label-centered equation blocks.
2. The IR lacks typed semantic fields for equation role, object family,
   equality status, time shifts, coefficient families, leading signs,
   ownership domain, and normalization statements.
3. Relation selection is mostly shared-word proximity and cannot distinguish
   a level definition from its linearized counterpart or a distractor.
4. No generic validator compares typed normalization sign/timing, ownership
   scope, or level/linearized coefficient and sign profiles.
5. Parser-only evidence cannot support a confirmed defect; visual/page-region
   authentication remains unavailable in the current provider output.
6. Adjacent local source discovery does not fetch or authenticate remote author
   source packages, code, YAML, or errata.
7. The visible formalizer matrix is not an end-to-end semantic benchmark, and
   there is no sealed cross-domain holdout.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can generic label-centered equation blocks and typed semantic relations recover useful timing/sign/coefficient/ownership tensions without reintroducing paper-specific rules or false promotion? |
| Mechanism under test | Generic block segmentation, role/object metadata, symbol/time/sign profiles, explicit relation hypotheses, and conservative semantic validators. |
| Expected failure mode | OCR fragments or nearby prose produce a wrong role, wrong symbol family, or false pair; a proxy semantic match is mistaken for mathematical verification. |
| Promotion criterion | On a content-addressed machine-readable corpus: every expected parser-only tension is nominated, every no-tension/ambiguous case emits no semantic finding, zero unexpected blocks/profiles/hypotheses/checks/findings occur, every semantic finding has resolvable packet/profile/hypothesis/check references, and parser-only evidence produces no substantive correctness disposition. |
| Promotion veto | A Boehl label/token/phrase in production logic; an unbound relation; source-specific score tuning; a parser-only promotion; an inferred role represented as a fact; or a false relation on an ambiguous fixture. |
| Continuation veto | Source drift, corrupted artifact, failed IR validation, or inability to distinguish semantic nomination from authentication. A low Boehl score is not a continuation veto. |
| Repair trigger | Any false pair, missing evidence reference, duplicate semantic finding, source-specific token, or typed fixture miss. |
| Must not conclude | General recall, faithful OCR, author intent, mathematical correctness, code equivalence, causal validity, posterior validity, or release readiness. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Label-centered window | Actual parser output places labels on separate lines | Smallest source-local unit that reconstructs fragmented displays | Window absorbs unrelated equations/prose | adversarial adjacent-label fixture | hypothesis |
| Generic role cues in prose | Equation-exposition rubric and common scholarly wording | Roles such as definition/linearized/normalization are often stated in prose | lexical cue becomes author intent | renamed and distractor fixtures | hypothesis |
| Symbol/time/sign profiles | Existing parser text | Supports relation nomination without executing OCR as code | glyph corruption creates wrong profile | parser-variant fixtures and raw-text retention | hypothesis |
| Same object family for relation pairing | Local role/object overlap plus explicit cross-reference | Stronger than shared words alone | wrong nearby object selected | competing-candidate fixture | hypothesis |
| Parser-only findings remain tensions | Existing authentication contract | Preserves rigorous claim boundary | true defects remain unconfirmed | promotion-veto tests | reviewed default |
| Boehl replay after fixture freeze | User-requested diagnostic | Measures same-paper discoverability | leakage and local optimization | describe as tuned replay only | descriptive only |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Engineering comparator | Current implementation output on the exact content-addressed fixture bytes, recorded before semantic production edits, versus the repaired implementation on the identical bytes. |
| Same-paper descriptive comparator | Fresh R5 seven-item issue inventory, opened only after the isolated replay artifact/report are frozen. This is not a scientific comparator or causal before/after estimate. |
| Primary pass criteria | Exact machine-oracle match with zero unexpected outputs; 100% tension nomination on positive cases; no semantic finding on consistent/ambiguous/distractor parser-only cases; zero substantive correctness dispositions from parser-only evidence; 100% resolvable packet/profile/hypothesis/check binding; zero forbidden source-specific tokens. |
| Veto diagnostics | Invalid IR, duplicate IDs, source digest mismatch, relation without role/object evidence, unauthenticated promotion, or false semantic pair. |
| Explanatory diagnostics | Finding count, pair count, role confidence, unresolved metadata, parser count, payload size, and same-paper exact/partial/missed score. |
| What will not be concluded | Same-paper score changes do not establish generalization or scientific correctness. Passing synthetic fixtures does not establish real-PDF recall. |
| Result artifacts | Content-addressed corpus/oracle, baseline run manifest and score, phase records, semantic fixture scorecard, independent review, isolated replay report/manifest/artifact, and post-hoc comparison under `docs/reviews/`. |

Parser-only negative cases have exactly one allowed outcome: `no semantic
tension nominated` with an optional diagnostic abstention reason. They may not
emit `consistent_under_checked_assumptions`, `not_reproduced`, or any other
substantive correctness disposition. Checked consistency remains available
only to authenticated, explicit, assumption-bound backend routes outside this
semantic nomination pass.

## Versioned Semantic Artifact Contract

The detailed artifact will add these canonical collections:

| Collection | Schema | Required deterministic identity and bindings |
| --- | --- | --- |
| `equation_blocks` | `applied_math_equation_block/1.0` | block ID from source digest, page, line range, label, raw text; packet reference and extraction digest |
| `semantic_profiles` | `applied_math_semantic_profile/1.0` | profile ID from block ID and profile version; block/packet refs; candidate fields with cue spans and confidence |
| `relation_hypotheses` | `applied_math_relation_hypothesis/1.0` | hypothesis ID from ordered profile endpoints and relation kind; evidence refs, ambiguity status and reason |
| `semantic_checks` | `applied_math_semantic_check/1.0` | check ID from hypothesis/profile and check kind; exact input refs, diagnostic outcome, limits and non-claim |
| semantic findings | existing finding envelope plus semantic refs | exact packet, profile, hypothesis and check references; `supported_tension` only for parser evidence |

A whole-artifact validator must resolve every reference, validate source and
extraction digests, reject duplicate IDs, enforce cue-span bounds, and enforce
authentication/disposition rules. All five collections must be pageable and
the compact summary must reconstruct their counts and artifact identity.

## External-Tool-First Route

- ResearchAssistant remains the source/PDF intake provider. Its one-parser,
  low-confidence output is preserved as non-certifying evidence.
- SymPy remains available only for closed authenticated expressions; semantic
  profiles do not become SymPy inputs automatically.
- DynareMCP remains optional for supplied `.mod` files and does not establish
  paper/code equivalence.
- No new proof/search algorithm is introduced. This program adds orchestration,
  typed evidence, and conservative relation nomination.

## Phases

### Phase 0: Freeze Semantic Fixtures And Baseline

Objective: freeze generic structured fixtures for normalization sign/timing,
ownership domain, level/linearized coefficient/sign, renaming, competing pairs,
fragmented labels, and ambiguous distractors.

Entry conditions: Fresh R5 artifact and current focused tests pass.

Artifacts: fixture matrix, machine-readable corpus/oracle with full SHA-256,
baseline run manifest, current-implementation output on the exact fixture
bytes, and Phase 0 result.

Checks: at least four positive relation cases, four no-tension cases, and four
ambiguous cases across at least three application domains; exact input bytes,
source/authentication state, page/line boundaries, expected and forbidden
blocks/profiles/hypotheses/checks/findings/dispositions/reason codes; zero
unexpected outputs; corpus digest; no Boehl labels, symbols, phrases, or
answer-key prose. Record current output on the identical bytes before edits.

Evidence: visible engineering fixtures, not a sealed holdout.

Forbidden: changing production code before fixture freeze; treating fixture
success as paper-level recall.

Handoff: every planned semantic field and validator has positive, negative,
and ambiguous coverage in a reconstructable oracle, and the old baseline is
scored on the same bytes.

Stop: fixtures cannot discriminate intended relation from a distractor.

### Phase 1: Label-Centered Equation Blocks

Objective: reconstruct bounded equation blocks around standalone or inline
labels while retaining raw page text, line ranges, source digest, and parser
status.

Entry conditions: Phase 0 fixtures frozen.

Artifacts: block segmenter, IR schema extension, fragmentation tests, result.

Checks: standalone labels, inline labels, multiple labels per page, prose
references that are not displays, blank-line fragments, page boundaries,
duplicate labels, deterministic IDs, and source binding.

Evidence: a block is a parser candidate, not an authenticated transcription.

Forbidden: converting reconstructed text to certified LaTeX or crossing page
boundaries silently.

Handoff: each candidate block has one disposition and bounded context.

Stop: block identity cannot be tied to an exact source/page/line range.

### Phase 2: Typed Semantic Profiles

Objective: derive candidate equation role, equality status, object cues,
coefficient families, time shifts, sign profile, ownership scope, and
normalization cues from each block and its local prose.

Entry conditions: Phase 1 blocks validate.

Artifacts: semantic-profile builder, confidence/evidence records, tests,
result.

Checks: varied notation and wording, OCR spacing, Unicode minus/Greek symbols,
subscripts/superscripts, role ambiguity, unresolved fields, and raw-evidence
retention.

Evidence: every inferred field is `candidate` with cue spans and confidence;
unresolved fields remain explicit.

Forbidden: domain-specific variable lists, paper labels, silent role
resolution, or claims that symbol profiles reproduce the equation.

Handoff: relation selection can use typed evidence without treating it as fact.

Stop: a profile cannot explain which source cue produced each material field.

### Phase 3: Relation Hypotheses And Semantic Validators

Objective: build conservative bounded level-to-linearized,
normalization-to-movement, and explicitly scoped ownership hypotheses and emit supported tensions only when
typed evidence is sufficient.

Entry conditions: Phase 2 profiles pass.

Artifacts: relation selector, ambiguity reasons, validators, evidence chains,
end-to-end tests, result.

Checks: material coefficient-family mismatch, leading-sign mismatch,
term-specific normalization sign/date implication, explicit ownership-domain preservation, renamed
variables, distant references, competing candidates, duplicates, and no-match
abstention.

Evidence: parser-only results are `supported_tension`; a mathematical verdict
requires later authenticated transcription and explicit derivation.

Forbidden: pairing by score alone, selecting a relation because it improves
the Boehl result, or producing a confirmed defect.

Handoff: generic fixture scorecard passes with zero false relations.

Stop: any ambiguous/distractor fixture emits a semantic finding.

### Phase 4: Public Contract And Maintainability

Objective: integrate blocks, profiles, hypotheses, findings, paging, compact
summary, documentation, and source-specific-rule scans into the existing
public function.

Entry conditions: Phase 3 passes.

Artifacts: updated audit artifact and public docs, the five versioned pageable
semantic collections, whole-artifact validator, contract tests, result.

Checks: compact/detail parity, artifact identity, facade/server/CLI surfaces,
stable/all MCP smoke, response bounds, full relevant suite, compileall, diff
check, and independent code review.

Evidence: new semantic fields are diagnostic and artifact-backed.

Forbidden: new public function unless the existing orchestrator cannot carry
the contract; hidden backend execution; unbounded payload.

Handoff: implementation and exact replay prompt are frozen.

Stop: public contract regression or unresolved high-severity review finding.

### Phase 5: Fresh Same-Paper Tuned Replay

Objective: provision a content-addressed temporary workspace containing only
the frozen implementation/runtime files, the two PDFs, exact prompt, and empty
output root; run a fresh agent there; freeze its artifact/report/manifest; then
compare against the prior seven-item inventory outside that workspace.

Entry conditions: Phase 4 close, source and implementation digests frozen,
isolated workspace manifest frozen, prior plans/reviews absent from the
workspace, fresh output directory empty, prompt contains no answer-key content.

Artifacts: fresh replay JSON, report, run manifest, self-reported access log,
post-hoc comparison, result.

Checks: input digests, implementation/runtime digests, workspace allowlist and
absence of prior artifacts, fresh-agent self-report,
finding evidence bindings, false-positive review, exact/partial/missed score,
and unchanged claim boundary.

Evidence: instruction-compliant tuned replay in a content-bounded workspace;
the workspace manifest establishes absent repository context, while process-
level access outside the workspace remains self-reported and not OS-enforced.

Forbidden: calling the replay blind/holdout, adaptive reruns after comparison,
or claiming general recall.

Handoff: final report separates closed engineering gaps from residual
scientific and provider gaps.

Stop: leakage, source drift, implementation drift, or corrupt artifact.

### Phase 6: Independent Closeout

Objective: independently red-team code, fixtures, replay protocol, and final
claims; close only if no high-severity evidence-integrity issue remains.

Entry conditions: Phase 5 artifacts frozen.

Artifacts: independent review, final result, reset memo, next-program scope.

Checks: focused and broad tests, source-specific token scan, artifact hashes,
fixture/result reconstruction, replay non-access record, and diff inspection.

Evidence: candidate rejection and research-direction rejection remain
separate. Low recall triggers future work rather than unsupported claims.

Forbidden: release-readiness, paper-correctness, or generalization claims.

Handoff: final status states exactly what closed and what remains.

Stop: any high-severity contract or evidence defect remains.

## Pre-Mortem

The program could pass while misleading us if fixtures encode only one wording,
if block windows accidentally include the answer relation, or if same-paper
improvement comes from generic-looking but effectively paper-shaped cues. It
could fail for parser fragmentation rather than semantic logic. Earliest
diagnostics are renamed cross-domain fixtures, adjacent distractors, explicit
source-specific token scans, per-field cue spans, and end-to-end fixture traces.

The visible twelve cases support only the claim that the predeclared
engineering contract is implemented. One implementation attempt and one
focused repair loop are allowed before the oracle is frozen for scoring; no
claim of discipline-neutral generality follows. A future independently authored
sealed corpus with paraphrase, ordering, OCR, window-size, and unrelated-
equation perturbations is required for viability beyond this contract.

## Exact Execution Surfaces

- Deterministic semantic fixtures call the Python orchestrator with an injected
  parser payload. They test segmentation, profiles, relations, checks and
  artifact validation; they do not test ResearchAssistant or MCP transport.
- Public interface checks separately exercise CLI, facade, server, stable/all
  profiles, paging and artifact persistence.
- The same-paper replay separately exercises the real ResearchAssistant CLI
  provider from an isolated temporary workspace.

Phase 0 manifest records: full source/artifact/corpus digests and paths, git
commit plus dirty status, Python and package versions, ResearchAssistant
version/commit/dirty status, MCP profile, exact commands, timeouts, expected
outputs, prompt/model identity where available, CPU-only document execution,
and stop status. Unmatched Fresh R5 agent/model/environment fields are reported
as confounders; no score change is attributed causally to this implementation.

## Skeptical Plan Audit

Independent review verdict was `REVISE` on seven issues: non-executable oracle,
unverifiable replay isolation, ambiguous parser-only consistency, unresolved
artifact bindings, proxy genericity, incomplete baseline identity, and
confounded before/after scoring. This revision addresses them through a
content-addressed machine oracle and baseline on identical bytes, explicit no-
tension parser outcomes, versioned resolvable semantic records, a whole-
artifact validator, narrowed engineering claims, exact run manifests, separate
execution surfaces, and a content-bounded replay workspace. Execution may
begin only after the corpus/oracle and baseline manifest are written and their
digests recorded.
