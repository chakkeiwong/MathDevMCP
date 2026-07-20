# MathDevMCP Actionable Document-Rigor Repair Master Plan

Date: 2026-07-18

Status: `COMPLETED_WITH_STATED_LIMITS`

Baseline:
`docs/plans/mathdevmcp-industry-dsge-pilot-regression-measurement-result-2026-07-18.md`

## Mission Fit

Repair the focused mathematical-document audit so that it is exploratory in
finding possible obligations and rigorous at the claim boundary, while becoming
useful for actual scholarly exposition repair.

The workflow must distinguish:

- mathematical certification;
- document-context closure of an exposition obligation;
- a bounded candidate exposition patch;
- a diagnostic or source-review blocker.

It must not absorb general prose, motivation, pedagogy, typography, or
readability certification into MathDevMCP.

## Objective

Close the ten acceptance gaps frozen in
`tests/test_industry_dsge_readability_pilot_regression.py`:

1. context-aware positive/negative closure;
2. exact context-support spans;
3. role-first equation routing;
4. stable semantic issue aggregation;
5. symbolic-versus-numeric diagnostic routing;
6. correct inverse-condition wording;
7. macro-safe section hierarchy;
8. actionable-only proposal status and counts;
9. bounded non-certifying exposition patches;
10. a compact actionable human report.

## Research Intent And Evidence Contract

| Field | Pre-run contract |
| --- | --- |
| Engineering question | Can the focused audit convert raw proof-audit route evidence into context-aware, role-aware, deduplicated mathematical-exposition issues without weakening certification boundaries? |
| Exact baseline | Repo-local repaired and missing-condition fixtures, SHA-256 values recorded in the measurement result; pre-repair result `11 passed, 10 xfailed`. |
| Primary criterion | All ten strict acceptance targets become ordinary passing regressions; the repaired fixture has no false-persistent Leontief issue; the negative fixture remains open with one bounded candidate patch. |
| Hard vetoes | Closing the negative fixture; treating context prose as proof; suppressing unresolved source/local claims without a typed status; emitting numeric diagnostics without a numeric target; source-span or section-path corruption; existing adjacent test regressions. |
| Explanatory diagnostics | Gap counts, report lines/bytes, backend provenance size, and raw route-record counts. |
| Product budget | Actionable Markdown for the four-label fixture is below 200 lines and excludes detailed backend provenance. |
| Artifact | Updated fixtures/tests, implementation, execution result, and post-execution review under `docs/plans` and `docs/reviews`. |
| Not concluded | Mathematical proof, source fidelity, general document correctness, readability, pedagogy, publication readiness, release readiness, or cross-document generalization. |

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Early diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Four paragraphs before/one after | Pilot repair location plus the Domar reuse diagnostic | Captures the defining condition, source display, interpretation, dependent definition, and target display without unbounded document search | A relevant condition may be farther away, or nearby unrelated text may be misattributed | Positive Leontief and Domar closure plus the negative control; cited spans remain visible | Reviewed bounded default for focused exposition audit |
| Deterministic cue/structure classification | Existing source-routing design | Reproducible and auditable; no model call is needed for the frozen cases | Lexical ambiguity or false role assignment | Unknown/ambiguous state and exact cue spans; negative role fixtures | Baseline classifier, not semantic truth |
| `rho(Omega)<1` as sufficient exposition wording | Standard Neumann-series condition for a square matrix/operator in the scoped finite-dimensional fixture | It is the exact condition already stated in the repaired source | Could be copied into an inapplicable structured problem or mistaken for necessity | Emit only for inverse-plus-power-series pattern; label as non-certificate; human review required | Reviewed candidate patch template |
| One issue family for matrix domain plus Neumann convergence | Downstream human triage feedback | Groups one scholar-level concern while preserving shape/invertibility/convergence subevidence | Over-merging distinct matrix problems | Stable label-scoped ID and explicit subevidence; unrelated labels cannot merge | Reviewed fixture-scoped family rule |
| Actionable report below 200 lines | Downstream memo | Makes four-label results inspectable | Short output could omit vetoes or nonclaims | Required one-line boundary, status, spans, patch, and detailed-evidence pointer | Product interface budget, not scientific metric |
| No numeric solve route without numeric target/artifact | Mathematical task distinction | A symbolic exposition statement cannot be validated by a residual without a numerical instance | Missing a useful implementation check when code exists | Existing numeric-artifact tests must continue to receive numeric diagnostics | Reviewed routing rule |

## External-Tool-First Audit

The selected repairs are LaTeX structural parsing, deterministic role/context
classification, issue projection, and report composition. Existing external
mathematical backends do not solve those product tasks.

- SymPy remains available for encodable algebra but is not used to certify
  source prose or general matrix theorems.
- Lean/Sage remain detailed-evidence routes and are not removed or downgraded.
- A certifying backend is not required to say that the document explicitly
  states an assumption; that is a source-span observation, not a proof.
- No new proof/search algorithm is introduced.

## Phases

### Phase 1: Structural Source And Context Integrity

Objective: establish correct section hierarchy and bounded neighboring context.

Implementation:

- replace flat `[^{}]+` heading matching with a comment-aware balanced-brace
  scanner for `part/chapter/section/subsection/subsubsection`;
- use one structural heading source for index and rigor locations where
  feasible;
- pass an explicit four-before/one-after paragraph window through the high-level audit
  task and record them in tool-use/audit configuration.

Acceptance:

- macro-bearing BCRM section path is correct;
- repaired context includes the assumption paragraph and interpretation;
- existing include-order, fallback, duplicate-label, and ordinary-heading tests
  pass.

Stop condition: any source span, input ordering, or label ownership regression.

### Phase 2: Role-First Exposition Semantics

Objective: classify what a display is doing before generating proof-like work.

Implementation:

- add a source-bound `equation_roles` projection supporting multiple roles;
- cover at least definition, conditional identity, maintained assumption,
  accounting identity, and unknown;
- retain cue/source spans and distinguish inferred roles from author-supplied or
  source-evidenced roles;
- do not convert role classification into truth or proof.

Acceptance:

- Leontief is `definition` plus `conditional_identity`;
- the constant-returns restriction includes `maintained_assumption`;
- definitions and stated assumptions are not routed as theorem-proof requests.

Stop condition: ambiguous evidence is silently classified without an unknown or
inferred boundary.

### Phase 3: Context Closure And Semantic Issue Families

Objective: decide whether document context closes each exposition obligation and
deduplicate route artifacts.

Implementation:

- build exact label-scoped context-support records with line spans and text;
- distinguish `resolved_by_existing_context`, `partially_resolved`,
  `unresolved`, and `context_ambiguous`;
- create stable semantic issue IDs and aggregate route evidence as subevidence;
- preserve raw detailed audit/fix evidence behind `source_reports`;
- make the negative fixture a mandatory false-closure veto.

Acceptance:

- repaired Leontief issue is resolved with exact `rho(Omega)<1` span;
- negative Leontief issue remains unresolved;
- one issue owns dimension, invertibility, and convergence subevidence.

Stop condition: the negative control closes or source spans cannot be tied to the
target file.

### Phase 4: Actionable Patches, Statuses, And Diagnostic Families

Objective: close the document repair loop without claiming certification.

Implementation:

- emit a bounded sufficient-condition candidate for the recognized
  inverse-plus-Neumann pattern;
- label it `candidate_exposition_patch_not_certificate` and require human
  review;
- count only `actionable_patch` and `actionable_assumption_text` as proposals;
- use explicit statuses for resolved context, formalization/source review, and
  backend non-encodability;
- correct inverse wording to make invertibility the general requirement;
- suppress numeric solve diagnostics for symbolic exposition when no numeric
  artifact or implementation target exists.

Acceptance:

- repaired fixture has no actionable patch because no repair is needed;
- negative fixture has exactly one bounded actionable assumption patch;
- diagnostic abstentions are not advertised or counted as proposals;
- existing explicit numeric-artifact tests retain their numeric route.

Stop condition: patch wording is presented as source truth, necessity, or proof.

### Phase 5: Actionable Report And Interface Composition

Objective: make the normal human-facing result concise while preserving forensic
evidence.

Implementation:

- add `actionable_markdown` to the detailed result;
- show one row per semantic issue, exact context support, candidate patch or
  exact blocker, and one-line nonclaim;
- omit doctor/Lean/tool-route payloads from actionable Markdown;
- retain detailed JSON/source reports and compact artifact transport;
- project semantic issues and actionable statuses into compact MCP responses.

Acceptance:

- four-label actionable Markdown is below 200 lines;
- it contains no backend-provenance section;
- it retains an evidence/source-report pointer and claim boundary;
- CLI, facade, server, and artifact round-trip checks pass.

Stop condition: compact/actionable output erases a veto, source identity, or
nonclaim needed to interpret an issue.

### Phase 6: Test Conversion, Full Verification, And Close Review

Objective: turn the measurement boundary into durable repaired behavior.

Implementation:

- remove obsolete defect characterizations or invert them into repaired
  regressions;
- remove XFAIL markers only after each target passes for the intended reason;
- run focused, adjacent, changed-surface, and full repository tests;
- rerun the exact fixture audit and record before/after semantic and size data;
- inspect the diff and write a skeptical post-execution review.

Acceptance:

- no XFAIL/XPASS remains in the pilot regression module;
- all ten target behaviors pass;
- full repository suite passes except documented pre-existing skips;
- no publication or release state changes.

Stop condition: any full-suite regression, false closure, evidence-boundary
regression, or unexplained change outside the planned files.

## Skeptical Plan Audit

Verdict: `PASS_AFTER_REVISION`

Material revisions made during review:

1. **Wrong baseline:** the plan now binds to the repo-local positive/negative
   fixture pair, not the mutable downstream dossier.
2. **Proxy promotion:** report length is an interface budget only. Semantic
   positive/negative closure is the primary criterion.
3. **Unsafe order:** status/report work was moved after structural, role, and
   closure correctness so formatting cannot hide wrong triage.
4. **False closure:** the matched missing-condition fixture is a hard veto in
   every closure phase.
5. **Certification erosion:** context closure is explicitly a document-source
   observation, not mathematical proof. Raw proof/backend evidence is retained.
6. **Overfitting:** fixture-specific patterns must be expressed as bounded
   mathematical structures with unknown/ambiguous fallbacks. No broad claim of
   equation-role accuracy is permitted.
7. **Numeric regression:** suppression applies only without a numeric artifact or
   implementation target; existing explicit numeric tests remain gates.
8. **Shared worktree:** implementation must preserve existing resumability edits
   and exclude the out-of-scope `skills/` tree and downstream memo from staging.
   Their authorship is not inferred from the dirty worktree.
9. **Commit scope:** the final commit may include the completed resumability
   program already present in overlapping production files only after the full
   suite and diff review pass; unrelated `skills/` content remains
   excluded.
10. **XFAIL misuse:** XFAIL markers are not a final success state. Phase 6 must
    convert them to ordinary passing regressions.

## Review And Handoff Conditions

Execution may begin because the baseline is reproducible, the negative control
is explicit, the scientific boundary is preserved, and all planned actions are
local/reversible.

Close only when:

- the exact acceptance module is fully green without XFAIL;
- adjacent and full tests pass;
- the execution result separates engineering correctness, mathematical
  validity, and product interpretation;
- a post-execution skeptical review finds no unresolved material issue;
- the commit diff contains only intended repository work and push succeeds.

## Execution Close

The implementation and local skeptical close review are complete. The exact
fixture result, verification evidence, discovered provenance regression, and
remaining limits are recorded in:

- `docs/plans/mathdevmcp-industry-dsge-actionable-rigor-repair-result-2026-07-18.md`;
- `docs/reviews/mathdevmcp-industry-dsge-actionable-rigor-repair-execution-review-2026-07-18.md`.

The repaired fixture now has zero top-level gaps and proposals, while the
matched negative fixture remains open with one human-reviewed,
non-certifying assumption patch. This completes the bounded engineering
program; it does not establish theorem correctness, general readability, or
cross-document generalization.
