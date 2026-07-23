# Applied-Math Audit Gap-Closure Master Program

Date: 2026-07-22

Status: reviewed for execution

## Mission

Advance MathDevMCP as an exploratory, high-standard, rigorous, agent-facing
mathematical development system for applied mathematical work in economics,
finance, marketing, management, and related social science. Search broadly
across possible mathematical and empirical failures, but publish only claims
that retain source anchors, assumptions, tool provenance, and an explicit
uncertainty boundary.

This program addresses the remaining gaps in
`docs/reviews/applied-math-audit-orchestrator-2026-07-22-remaining-gaps.md`.
It is a root-cause repair program, not a keyword-tuning exercise.

## Root-Cause Diagnosis

The current orchestrator is a flat-text screen. It cannot reliably answer
relational mathematical questions because:

1. PDF extraction is reduced to one unlocated text string; equations have no
   page, crop, number, or surrounding-prose identity.
2. LaTeX objects are extracted independently; there is no claim/object graph
   connecting definitions, derivations, objectives, estimators, and results.
3. Obligations are selected by keywords and literal regexes; most selected
   obligations therefore become `not_checkable`.
4. Specialist routes are declarations only; no typed backend invocation or
   result binding exists.
5. ResearchAssistant is used as a parser transport, not as a source-first
   discovery provider for LaTeX, code, data, appendices, or errata.
6. Compact output and detailed artifacts do not yet expose a versioned,
   pageable claim/evidence schema suitable for repeated agent work.
7. The benchmark does not yet distinguish extracted evidence, deterministic
   backend findings, and fresh-agent inference at issue level.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Can a source-bound evidence graph plus executable generic checks materially reduce the `not_checkable` and missed relational issues observed in the Boehl blind test? |
| Candidate mechanism | Page/equation packets, typed claim IR, dependency edges, deterministic relationship validators, source-first discovery, and typed specialist adapters. |
| Expected failure modes | Parser corruption, false links between nearby equations, unsafe symbolic formalization, backend unavailability, source drift, and benchmark leakage. |
| Primary promotion criterion | Frozen fixtures show that every generated finding has a reproducible evidence chain and relational benchmark issues are either detected or explicitly classified with a reason. |
| Promotion veto | Missing source identity, unsupported equation normalization, hidden backend/provider errors, arbitrary command execution, a finding without an evidence chain, or compact/detail disagreement. |
| Continuation veto | Corrupt source/artifact, inability to distinguish tool output from agent inference, or a public-schema regression that cannot be repaired locally. |
| Repair trigger | Any relation edge without source anchors, any validator that promotes heuristic text to a defect, any specialist result without typed scope, or any benchmark score based on leaked answer-key information. |
| Must not conclude | General mathematical correctness, complete PDF understanding, causal validity, code equivalence, or general precision/recall from this corpus. |

## Evidence Contract

* Baseline: prior orchestrator artifact and qualified Boehl result, including
  3 exact, 1 partial, and 3 missed issues for a fresh agent using MathDevMCP
  evidence.
* Primary evidence: issue-level exact/partial/missed scoring on frozen fixtures,
  plus reproducible source anchors and validator traces.
* Hard vetoes: schema failure, digest mismatch, missing page/equation anchor,
  unhandled provider/backend failure, compact/detail inconsistency, or a
  confirmed defect produced without a deterministic or explicitly reviewed
  evidence route.
* Descriptive diagnostics: runtime, parser counts, candidate counts, payload
  size, and number of selected obligations.
* Artifacts: versioned IR schema, source/equation packets, dependency graph,
  validator traces, specialist manifests, benchmark manifest/results, phase
  close records, and final remaining-gap report.

## Skeptical Plan Audit

This program passed a pre-execution audit with the following corrections:

* Obligation count is not a success metric; relational issue recall is the
  primary benchmark measure.
* The Boehl answer key remains frozen and is read only after a blind artifact
  is written; no detector may be tuned against the same run.
* PDF parser output remains non-certifying. A page/equation candidate is an
  evidence packet, not a recovered theorem or faithful LaTeX.
* External tools are considered before native search. SymPy is used only for
  explicit, bounded expressions; DynareMCP is invoked only for `.mod` inputs;
  absent providers produce visible abstention records.
* No generic validator may execute arbitrary user code or shell commands.
* Low recall is a repair signal. The program stops only for invalid evidence,
  broken schema, or an unrecoverable public-contract defect.

## Phase Program

### Phase 0: Baseline And Contract Freeze

Objective: freeze current artifacts, schemas, fixtures, and benchmark scoring.

Entry: current worktree and prior orchestrator artifacts readable.

Artifacts: baseline manifest, issue-label manifest, schema version, phase-00
result.

Checks: focused tests, source digests, existing Boehl artifact hashes, and
clean diff inspection.

Evidence: baseline scores are descriptive; no general recall claim.

Forbidden: changing prior blind artifacts or tuning from the answer key.

Handoff: baseline manifest and scoring script are reproducible.

Stop: source drift or missing prior artifact prevents a fair comparison.

### Phase 1: Page-Aware Source And Mathematical Evidence Packets

Objective: preserve page, block, equation-number, line, crop/reference, parser,
and surrounding-prose evidence for PDF and LaTeX inputs.

Entry: Phase 0 baseline frozen.

Artifacts: `applied_math_evidence.py`, packet schema tests, PDF page packets,
LaTeX equation packets, parser limitation records.

Checks: multi-page PDF fixture, equation-number fixture, parser disagreement,
missing-page and source-change tests.

Evidence: raw text/image references remain available; normalized candidates are
marked non-certifying until checked.

Forbidden: inventing equations, silently merging parser outputs, or dropping
page identity.

Handoff: the same source object can be traced from document location to raw
text and candidate display math.

Stop: page identity cannot be preserved or provider failure is hidden.

### Phase 2: Claim IR And Dependency Graph

Objective: represent definitions, equations, assumptions, objectives, FOCs,
estimands, data transformations, results, and claims with typed edges.

Entry: evidence packets validate.

Artifacts: `applied_math_ir.py`, versioned schema validator, graph builder,
fixtures for economics/finance/marketing/management, graph diagnostics.

Checks: deterministic IDs, source-span conservation, duplicate/ambiguous edge
tests, cycle and unresolved-reference tests, compact/detail round trip.

Evidence: every node and edge retains source anchors, extraction tier,
confidence, and unresolved status.

Forbidden: treating adjacency or keyword similarity as proof of dependency.

Handoff: graph edges can be consumed by validators and rendered in reports.

Stop: graph loses raw evidence or cannot represent unresolved relationships.

### Phase 3: Executable Generic Obligation Engine

Objective: replace keyword-only selection with bounded, evidence-driven checks
for arithmetic, equality, dimensions, timing, level/log boundaries,
definition-use consistency, aggregation, and objective/FOC relationships.

Entry: typed IR and graph are available.

Artifacts: validator registry, trace format, SymPy route for explicit formulas,
safe parsers, generic fixture corpus, issue-level result records.

Checks: true/false paired fixtures, tolerance and domain tests, abstention on
ambiguous formalization, no arbitrary execution, and evidence-chain replay.

Evidence: a defect requires a closed target, assumptions, tool/version, and
source anchors; otherwise disposition is `not_checkable` or `supported_tension`.

Forbidden: keyword hits establishing defects, silent assumptions, or CAS output
being presented as economic interpretation.

Handoff: at least the C.75/C.77/C.79-style relational fixture issues produce
replayable candidate findings or explicit, reasoned abstentions.

Stop: any validator cannot distinguish a closed target from a heuristic.

### Phase 4: Source-First Discovery And Typed Specialists

Objective: use ResearchAssistant source discovery where available and actually
invoke DynareMCP for compatible `.mod` artifacts through a constrained adapter.

Entry: Phase 3 validator traces are stable.

Artifacts: source discovery adapter, specialist registry, Dynare route runner,
provider/backend manifests, injected-runner tests, failure records.

Checks: source-package discovery, official-code/data/appendix lookup, Dynare
symbol/equation/timing invocation, unavailable-provider behavior, path safety.

Evidence: provider, commit, command, input digest, output digest, operation,
and non-claim are recorded separately from MathDevMCP inference.

Forbidden: arbitrary shelling, automatic code execution for unknown files,
Dynare output being treated as paper equivalence, or provider absence as a
scientific refutation.

Handoff: each route is typed, bounded, reproducible, and visibly abstainable.

Stop: a backend can run without an input digest or result provenance.

### Phase 5: Claim-to-Evidence, Paging, And Public Contract

Objective: make reports usable for repeated LLM review without giant payloads
or loss of detail.

Entry: packets, graph, validators, and routes exist.

Artifacts: versioned `applied_math_claim_ir`, evidence-chain resolver, compact
projection, detail paging API, CLI/facade/server docs and tests.

Checks: compact/detail parity, deterministic page tokens, artifact tamper
checks, max payload bounds, exact record resolution, non-claim propagation.

Evidence: every promoted finding resolves to source -> object -> edge -> check
-> result; unsupported claims remain explicit.

Forbidden: hiding unresolved records behind counts or exposing mutable paths as
authority.

Handoff: an agent can start with compact output and retrieve exactly the
evidence needed for one finding.

Stop: detail cannot be resolved from compact handles or artifact integrity
fails.

### Phase 6: Frozen Cross-Domain And Boehl Regression

Objective: measure engineering closure against frozen cross-domain fixtures and
run an explicitly answer-key-informed Boehl regression. Preserve a separate
future protocol for a fresh, isolated blind discovery test.

Entry: public contract and validators pass.

Artifacts: frozen benchmark corpus/manifests, tool artifact,
answer-key-informed comparison, future blind-test protocol, cross-domain
scorecard, and phase result.

Checks: economics, finance, marketing, management, PDF-only, source-plus-code,
and identical Boehl papers. Score exact/partial/missed, false positives,
anchor completeness, and abstentions.

Evidence: scores are corpus-specific engineering/scientific diagnostics, not
population recall estimates.

Forbidden: labeling this session blind, hiding answer-key exposure, hard-coding
document-specific labels or equations into general validators, source drift,
mixing agent inference into tool-only scores, or ranking by finding count.

Handoff: every previous gap is closed, narrowed, or documented with an exact
reason and next experiment.

Stop: source drift or missing frozen output invalidates the regression arm;
answer-key exposure invalidates blind claims, not transparent regression
evidence.

### Phase 7: Independent Review And Release Decision

Objective: red-team code, contracts, documentation, evidence, and remaining
scientific limitations; decide colleague-facing experimental readiness.

Entry: Phase 6 scorecard complete.

Artifacts: review record, test summary, final remaining-gap report, master result
and reset memo.

Checks: focused and broad relevant tests, MCP stdio smoke, code/document review,
artifact hashes, and optional independent Claude read-only review.

Evidence: readiness is limited to demonstrated experimental scope.

Forbidden: production/scientific-completeness claims or commit/push without a
separate user request.

Handoff: final report states closed gaps, unresolved gaps, evidence, and next
repair direction.

Stop: public contract or evidence integrity remains defective.

## Automatic Phase Loop

At each phase close, the supervisor must run checks, write the result record,
refresh the next subplan, and review that subplan. A ready subplan launches
automatically. A material blocker is recorded and escalated; ordinary test
failures trigger repair and focused rerun. Low recall alone does not stop the
program.

## Subplan Requirement

Each phase has a companion subplan containing objective, inherited entry
conditions, artifacts, checks/tests/reviews, evidence contract, forbidden
claims/actions, exact handoff conditions, and stop conditions. Subplans are
created before their phase executes and are refreshed at the prior phase close.
