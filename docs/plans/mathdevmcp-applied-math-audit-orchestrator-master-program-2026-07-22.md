# MathDevMCP Applied-Math Audit Orchestrator Master Program

Date: 2026-07-22

Status: reviewed and approved for execution

## Mission

Build one LLM-facing, artifact-backed MathDevMCP function for auditing applied
mathematical research in economics, finance, marketing, management, and related
social science. The function is a general orchestrator. ResearchAssistant is a
source/PDF/code intake provider; MathDevMCP owns the discipline-neutral claim
and obligation contract; DynareMCP and other specialist systems are optional
adapters selected per component.

The first release is an experimental diagnostic workbench. It must improve
coverage accounting and routing without claiming autonomous mathematical proof,
complete PDF understanding, causal identification, or scientific validity.

## Public Target

```text
audit_applied_math_document(
    sources=[...],
    code_paths=[...],
    data_paths=[...],
    mode="screen|deep|reproduce",
    specialist_policy="auto|none|explicit",
    response_mode="compact|detailed",
    artifact_root=...
)
```

The response is a compact summary with durable artifact handles. Lower-level
functions remain available for focused reruns and detailed evidence paging.

## Research Intent Ledger

| Field | Contract |
| --- | --- |
| Main question | Does a single general applied-math audit call route source evidence and applicable checks more completely than the existing isolated-label workflow? |
| Candidate mechanism | Source-first intake, discipline-neutral claim graph, obligation coverage ledger, optional specialist adapters, and explicit disposition for every obligation. |
| Expected failure modes | PDF equation corruption, over-broad domain inference, method misclassification, specialist overreach, duplicate findings, large payloads, and obligations silently disappearing. |
| Promotion criterion | The public function has a stable schema; every selected obligation has a disposition; source/parser/backend provenance is preserved; focused fixtures exercise routing and abstention; the repeated Boehl benchmark is scored by issue-level recall rather than diagnostic count. |
| Promotion veto | A missing obligation disposition, source digest mismatch, hidden provider failure, unsupported specialist invocation, unbounded response, or a claim of proof from extraction/structural evidence. |
| Continuation veto | No valid source input, corrupted artifact, or test harness that cannot distinguish tool output from agent inference. Low recall is a repair signal, not an automatic stop. |
| Repair trigger | Any missed required obligation, false positive caused by parser damage, backend tolerance error, or specialist result used outside its declared domain. |
| Must not conclude | General PDF capability, paper correctness, causal validity, posterior validity, exact code equivalence, or superiority from one case. |

## Evidence Contract

| Field | Contract |
| --- | --- |
| Baseline | Existing MathDevMCP focused tools plus the qualified blind Boehl discovery result: ResearchAssistant `0/7`, autonomous MathDevMCP `0/7`, fresh agent `3 exact/1 partial/3 missed`. |
| Primary measure | Per-obligation disposition coverage and benchmark issue-level exact/partial/missed matching. |
| Hard veto diagnostics | Invalid schema, missing source digest, unrecorded provider failure, missing disposition, or forbidden cross-MCP claim. |
| Explanatory diagnostics | Parser count, response size, runtime, candidate count, specialist availability, and false-positive categories. |
| Artifact | Orchestrator source/tests, compact/detailed audit artifacts, fixture corpus, benchmark comparison, phase close records, and final result under `docs/reviews/`. |
| Non-claims | A complete coverage ledger means every selected obligation was accounted for, not that every obligation was solved. |

## General Applied-Math Scope

The core obligation families are discipline-neutral:

1. algebra/calculus and transformations;
2. definitions, notation, indexing, and symbol identity;
3. dimensions, units, scales, and frequency conventions;
4. timing, conditioning, information, and event order;
5. optimization objectives, constraints, FOCs, and boundary cases;
6. probability, likelihood, normalization, support, and uncertainty language;
7. identification, estimands, and causal-condition boundaries;
8. linearization, approximation, expansion-point, and retained-order checks;
9. accounting, aggregation, ownership, stock-flow, and decomposition checks;
10. algorithm, convergence, initialization, and implementation alignment;
11. numerical/table/figure arithmetic and reproducibility checks;
12. claim-to-evidence and source/code/data dependency checks.

Domain templates may add obligations, but no template is allowed to redefine
the core IR or claim authority. DynareMCP is one optional dynamic-model adapter.

## Phase Structure

### Phase 0: Contract And Benchmark Freeze

Objective: freeze the public API, status vocabulary, evidence classes, baseline,
and repeated benchmark before implementation changes.

Entry conditions: current MathDevMCP worktree and qualified blind Boehl artifacts
are readable; existing tests are runnable.

Required artifacts: this master plan, Phase 0 subplan, baseline manifest, and
an issue-level benchmark definition that does not alter the frozen blind report.

Checks: inspect current contracts, tool surface, blind hashes, and maintainability
baseline; run a focused test slice.

Evidence contract: the baseline numbers above are descriptive only; no claim of
general recall is made.

Forbidden claims/actions: no code edits before the plan audit; no changing blind
discovery artifacts; no making DynareMCP mandatory.

Handoff: baseline and schema decisions recorded, plan audit passes.

Stop: frozen artifacts unavailable or baseline cannot be reproduced.

### Phase 1: Discipline-Neutral Applied-Math IR

Objective: define and validate a compact claim/object/equation/dependency IR
with source spans, evidence tiers, assumptions, and uncertainty.

Entry conditions: Phase 0 complete.

Required artifacts: `applied_math_ir` module, schema validator, source digest
records, fixture examples for economics, finance, marketing/management, and a
Phase 1 result note.

Checks: schema tests, malformed-input tests, deterministic digest tests, source
span and non-claim tests.

Evidence contract: source extraction is evidence transport; IR normalization is
not proof and must retain raw text/image references.

Forbidden: inventing equations from OCR; silently upgrading inferred roles to
facts; importing a parallel Dynare-only IR as the core contract.

Handoff: IR validates and can represent a PDF-only document and a structured
LaTeX document with the same top-level contract.

Stop: representation cannot preserve uncertainty or source anchors.

### Phase 2: Obligation Generation And Coverage Ledger

Objective: generate applicable general obligations and require exactly one
disposition for every selected obligation.

Entry conditions: Phase 1 IR passes.

Required artifacts: obligation catalog, rule-to-evidence mapping, disposition
taxonomy, compact coverage projection, fixture obligations and Phase 2 result.

Checks: coverage conservation tests, duplicate IDs, unsupported-family
abstentions, parser-damage fixtures, and payload-size tests.

Evidence contract: `confirmed_defect`, `supported_tension`, `consistent_under_checked_assumptions`, `not_reproduced`, `not_checkable`, `extraction_blocked`, `backend_abstention`, and `not_applicable` are distinct.

Forbidden: using raw finding count as success; treating an abstention as a pass
or a failure; promoting a proxy metric.

Handoff: selected obligations and all dispositions reconstruct exactly from the
compact artifact and detailed artifact.

Stop: any selected obligation can disappear from the report.

### Phase 3: Source-First And Specialist Routing

Objective: route PDF/LaTeX/source/code/data inputs through ResearchAssistant,
MathDevMCP, and optional specialists without cross-domain overclaiming.

Entry conditions: Phase 2 passes.

Required artifacts: source intake adapter, specialist registry, DynareMCP
optional adapter, route manifest, unavailable-specialist fixtures, Phase 3
subplan/result.

Checks: source-first preference, no-source fallback, Dynare `.mod` applicability,
non-Dynare `not_applicable`, provider failure visibility, injected runner tests.

Evidence contract: specialist output remains tiered (`source`, `backend`,
`runtime`, `agent_inference`); only declared operations can produce backend
evidence.

Forbidden: shelling arbitrary user commands, treating Dynare output as proof of
paper semantics, or using specialist absence as a scientific refutation.

Handoff: routes are deterministic and every route has a reason and limitation.

Stop: provider failures are hidden or specialist scope is ambiguous.

### Phase 4: Single Public Orchestrator

Objective: expose `audit_applied_math_document` through library, CLI, facade,
and experimental all-profile MCP surfaces with compact-by-default artifacts.

Entry conditions: Phases 1--3 complete.

Required artifacts: orchestrator module, facade/server/CLI wiring, documentation,
focused interface tests, response-size and persistence tests, Phase 4 close.

Checks: one-call PDF/TeX smoke, mode validation, resume/artifact resolution,
stable tool-count checks, malformed input behavior, `git diff --check`.

Evidence contract: compact response carries counts, top findings, coverage,
artifact handles, and non-claims; detailed records are opt-in/pageable.

Forbidden: one giant unbounded JSON response; source edits; publication or
release enablement; silent model-file execution.

Handoff: one LLM call produces a valid audit envelope for a small fixture.

Stop: facade/CLI/server disagree or compact response cannot resolve details.

### Phase 5: Cross-Domain Regression And Boehl Re-Test

Objective: measure whether the orchestrator improves discovery coverage on
structured and PDF-only fixtures, including the qualified blind Boehl case.

Entry conditions: Phase 4 passes.

Required artifacts: fixture corpus, test runner, blind re-test manifest, issue
comparison, benchmark result, Phase 5 result.

Checks: economics structural fixture, finance identity/units fixture, marketing
causal/estimand fixture, management optimization fixture, PDF extraction fixture,
and the identical Boehl answer-key comparison. Separate tool-only from fresh
agent-assisted scores.

Evidence contract: exact/partial/missed, false-positive, abstention, and
source-anchor metrics are descriptive for this corpus. Passing a hard screen is
not superiority evidence.

Forbidden: opening the answer key before a fresh blind artifact is frozen; using
the Boehl answer key to tune the same run; claiming generalization from one
paper.

Handoff: benchmark artifacts answer whether coverage improved and which gaps
remain.

Stop: leakage, source drift, or missing frozen output invalidates the blind arm;
other fixtures may still report engineering results.

### Phase 6: Maintainability, Review, And Closeout

Objective: review implementation, documentation, boundaries, and evidence;
record remaining gaps and decide whether the experimental function is usable by
colleagues.

Entry conditions: Phase 5 artifacts complete.

Required artifacts: code review record, test summary, maintainability result,
remaining-gap report, final program result, and optional independent review.

Checks: focused suite, broad relevant suite, MCP stdio smoke, maintainability,
documentation links, diff inspection, and artifact hash checks.

Evidence contract: readiness is limited to the implemented experimental scope;
unimplemented domain validators remain visible.

Forbidden: calling the system production-grade or scientifically complete;
committing/pushing without explicit user request.

Handoff: final result names what improved, what did not, and the next repair
program.

Stop: unresolved correctness defect in the public contract or failed evidence
integrity.

## Execution Policy

At the end of each phase: run required checks, write a result/close record,
refresh the next subplan, review the handoff conditions, and launch the next
phase only when the conditions pass. A low benchmark score triggers repair or a
qualified result; it is not a reason to stop when the harness is valid.

## Final Success Boundary

Success means one usable, bounded, general applied-math audit function exists,
with explicit evidence and coverage accounting, optional specialist routing,
and measurable benchmark artifacts. It does not mean autonomous discovery of
all errors in arbitrary papers.
