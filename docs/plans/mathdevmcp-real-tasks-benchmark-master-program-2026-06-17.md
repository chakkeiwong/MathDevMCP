# MathDevMCP Real-Task Benchmark Master Program

## Purpose

This master program turns the existing real-task benchmark artifacts into a
phased benchmark buildout program for MathDevMCP.

The benchmark exists to answer a narrow product question:

> Is MathDevMCP getting better at the real mathematical, code-document, and
> evidence-boundary tasks that appear in `MacroFinance`, `dsge_hmc`,
> `latex-papers`, and BayesFilter-related workflows?

The benchmark is **not** a release certificate, mathematical proof engine, or
scientific validation device. It is a structured product-quality program whose
outputs may later inform workflow and release policy only after the benchmark
itself becomes stable and calibrated.

This program builds on the current benchmark artifacts:

- `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`
- `benchmarks/real_tasks/README.md`
- `benchmarks/real_tasks/manifests/public_cases.json`
- `src/mathdevmcp/real_tasks_manifest.py`
- `tests/test_real_tasks_manifest.py`

## Product and safety invariant

MathDevMCP must remain conservative.

No benchmark pass, retrieval hit, consistency result, parity summary,
engineering qualification note, or aggregate metric may be promoted into a
verified mathematical claim, convergence claim, posterior-validity claim, GPU
readiness claim, or scientific result unless a separate artifact with the
appropriate evidence contract justifies that stronger claim.

False certification remains a hard veto throughout this program.

## Evidence boundary

The benchmark program produces **engineering/product-quality evidence** about
MathDevMCP behavior.

It does not, by itself, prove:

- mathematical correctness of every verified-looking claim in the target repos;
- convergence or posterior validity for the models referenced by benchmark
  cases;
- scientific adequacy of the benchmarked workflows;
- release readiness of MathDevMCP unless a later release policy explicitly and
  narrowly adopts a mature subset of benchmark evidence.

## Program-level skeptical audit

Before any benchmark-program phase is allowed to influence workflow or release
policy, this program must preserve the following guardrails.

- **Wrong baseline check:** the current public benchmark set is only an initial
  seed, not a representative final benchmark. Public coverage growth is not the
  same as real-task readiness.
- **Proxy-metric check:** precision, recall, or F1 are not safety guarantees.
  Hard false-certification vetoes must survive every aggregation layer.
- **Stop-condition check:** the program must stop before workflow or release
  integration if the benchmark remains uncalibrated, thin, or overly public-set
  optimized.
- **Hidden-assumption check:** BayesFilter/external-repo access,
  holdout-local availability, and private corpus handling are dependencies, not
  already-satisfied assumptions.
- **Environment-mismatch check:** no phase before workflow integration may
  silently assume CLI, MCP, or gate coupling.
- **Artifact-usefulness check:** each phase must produce an artifact that the
  next phase actually consumes.

### Phase-completion boundary

Completing an early phase means only that the corresponding artifact is ready to
serve as input to the next phase. It does **not** authorize downstream policy
claims, workflow-gate coupling, or release interpretation until the later
calibration, integration, and gate-candidate phases explicitly earn those
transitions.

## Validation summary

| Program area | Why it exists | Current state | Program decision |
|---|---|---|---|
| Benchmark objective and categories | Needed to keep the benchmark tied to real tasks instead of toy fixtures | Defined in the benchmark spec, but not yet elevated into a full phased program | Accept and formalize in this master program |
| Public corpus | Needed for stable iteration and schema hardening | Initial 8-case public manifest exists | Accept as Phase 2 input, not as final coverage |
| Holdout/private strategy | Needed to prevent overfitting and preserve realism | Mentioned in spec, not yet programmatically built out | Make this an explicit mid-program phase |
| Loader/validator | Needed before any reporting or integration | Exists for the public manifest | Treat as prerequisite-hardening phase, not as benchmark execution |
| Reporting | Needed for usable benchmark signals | Not yet implemented | Make it a separate non-gating phase |
| Workflow/release integration | Tempting next step, but unsafe too early | Not started | Defer to late phases with explicit entry gates |

## Program phases

### Phase 0 — Program framing and governance

**Goal**

Freeze the benchmark purpose, safety invariant, evidence boundary, and
non-claims.

**Prerequisites**

- user goal and target repos identified;
- first benchmark spec exists.

**Work scope**

- define benchmark purpose and non-goals;
- define safety-critical failure modes;
- define the benchmark as engineering/product-quality evidence rather than a
  release certificate.

**Outputs**

- this master program;
- explicit benchmark safety invariant;
- explicit evidence-boundary section.

**Exit criteria**

- benchmark purpose is stable enough for later category scoring;
- false certification is explicitly a hard veto;
- benchmark non-claims are written down.

**How this enables the next phase**

Phase 1 depends on a fixed understanding of what kinds of errors are ordinary
classification misses and which are safety-critical.

---

### Phase 1 — Category contracts and scoring rules

**Goal**

Define how each benchmark category is scored and what precision/recall mean for
that category.

**Prerequisites**

- Phase 0 complete.

**Work scope**

- define scoring contracts for:
  - retrieval/provenance,
  - code-document consistency,
  - derivation/abstention,
  - numerical-oracle parity,
  - evidence-boundary discipline;
- define hard vetoes and non-claims per category;
- define how category scores are aggregated without washing out false
  certification.

**Outputs**

- category-scoring subplan;
- per-category precision and recall definitions;
- cross-category aggregation policy.

**Exit criteria**

- each category has explicit precision, recall, and veto semantics;
- a later evaluator can score a case without inventing category-specific logic
  ad hoc.

**How this enables the next phase**

Phase 2 needs stable scoring semantics to know what fields public cases must
carry and how gold expectations should be written.

---

### Phase 2 — Public corpus buildout

**Goal**

Expand and stabilize the committed public benchmark corpus using public or
sanitized artifacts from the target repos.

**Prerequisites**

- Phase 1 scoring contracts complete.

**Work scope**

- select public-safe benchmark cases by source repo and category;
- write/normalize case metadata and gold expectations;
- check category balance and avoid overconcentrating on a single failure mode.

**Outputs**

- updated public manifest and supporting notes;
- public-case inventory with explicit category coverage;
- representative cases for all major benchmark families.

**Exit criteria**

- every benchmark category has meaningful public coverage;
- each public case has stable gold semantics;
- public manifest remains loader/validator clean.

**How this enables the next phase**

Phase 3 uses the public set to decide what must remain outside daily tuning and
what belongs in holdout-local evaluation.

---

### Phase 3 — Holdout-local corpus design

**Goal**

Design a non-public evaluation tier that prevents overfitting to the public
benchmark set.

**Prerequisites**

- Phase 2 public corpus exists with enough variety to identify likely tuning
  targets.

**Work scope**

- define what should remain local/holdout only;
- identify larger, more fragile, or too-easy-to-overfit cases;
- define holdout selection and reporting policy;
- define a minimum disjointness rule for holdout cases so they are not merely
  public-like cases with different file names.

Minimum holdout disjointness should be expressed using at least one of:

- different source repo area or document family,
- different label neighborhood or chapter neighborhood,
- different task template,
- different benchmark-author exposure status.

**Outputs**

- holdout-local corpus policy;
- holdout candidate inventory;
- rules separating public from holdout use;
- lightweight scaffolding artifacts for holdout-local inventory templates and
  README guidance.

**Exit criteria**

- holdout rationale is explicit and reviewable;
- holdout-local cases are structurally representable in the benchmark program;
- public-case tuning and holdout evaluation are explicitly separated in later
  reports.

**How this enables the next phase**

Phase 4 extends the same tiering logic to private and external corpora, where
privacy and sibling-repo issues matter more strongly.

---

### Phase 4 — Private/external corpus design

**Goal**

Support realistic external/private tasks without leaking paths or confusing
private-case behavior with public benchmark behavior.

**Prerequisites**

- Phase 3 corpus-tier logic complete.

**Work scope**

- define private/external corpus policy;
- define sibling-repo and external-root representation rules;
- define redaction and privacy expectations for private cases;
- define the minimum safe fallback artifact when external/private access is not
  currently available.

**Outputs**

- private/external corpus policy;
- redaction rules;
- external/BayesFilter ingestion strategy;
- optional private manifest template direction;
- fallback note describing what remains blocked vs what public work may proceed.

**Exit criteria**

- private/external cases can be represented structurally;
- path and privacy assumptions are explicit;
- lack of external/private access is turned into a policy artifact rather than
  a hidden blocker.

**How this enables the next phase**

Phase 5 hardens the schema and loaders with a clear understanding of public,
holdout-local, and private/external tiers.

---

### Phase 5 — Schema, loader, and validator hardening

**Goal**

Make the benchmark artifacts machine-checkable, portable, and stable.

**Prerequisites**

- Phase 2 public schema fields are stable enough to encode.

Phase 4 private/external policy should inform later tier-aware expansion, but
missing private/external completeness must not block public manifest, loader,
validator, and reporting hardening for the public corpus.

**Work scope**

- harden manifest loader and validator;
- add path-policy and malformed-input tests;
- preserve portability and tier-aware validation semantics.

**Outputs**

- manifest loader/validator;
- focused tests;
- stable manifest contract.

**Current status**

Started:
- `src/mathdevmcp/real_tasks_manifest.py`
- `tests/test_real_tasks_manifest.py`

**Exit criteria**

- public manifest validates cleanly;
- malformed manifests fail predictably;
- path policy is portable and enforced.

**How this enables the next phase**

Phase 6 depends on a stable machine-readable benchmark corpus and loader
contract before benchmark reports can be trusted.

---

### Phase 6 — Non-gating reporting

**Goal**

Produce useful benchmark summaries without turning the benchmark into a gate.

**Prerequisites**

- Phase 5 manifest/loader contract stable;
- enough public cases to produce meaningful summaries.

**Work scope**

- add non-gating reporting over the real-task manifest;
- summarize cases by category, repo, evidence class, and difficulty;
- expose per-category precision/recall and false-certification summaries in a
  report layer;
- require report ordering that places hard-veto and evidence-boundary failures
  before any convenience summary or aggregate score.

**Outputs**

- non-gating benchmark report;
- category-level summary tables;
- safety vs usefulness metric separation.

**Exit criteria**

- benchmark results are reviewable without reading raw case JSON;
- no coupling to `benchmark_gate` yet;
- report structure makes hard-veto and boundary failures impossible to miss.

**How this enables the next phase**

Phase 7 uses the reporting layer to run pilot benchmark passes and study whether
metrics and cases are actually informative.

---

### Phase 7 — Pilot execution and calibration

**Goal**

Run the benchmark, inspect failure patterns, and recalibrate the suite.

**Prerequisites**

- Phase 6 reporting complete.

**Work scope**

- run the public benchmark suite against current MathDevMCP behavior;
- inspect category imbalance, over-abstention, under-detection, and brittle
  cases;
- revise case difficulty and scoring assumptions if needed.

Public-set improvements produced in this phase must be labeled as
**calibration/development evidence only**. They do not yet constitute benchmark
readiness evidence, holdout performance evidence, or policy justification.

Changes allowed in calibration should be tracked separately by type:

- case edits,
- threshold edits,
- severity-label edits,
- aggregation/reporting edits.

These changes should not be silently merged into one generic “recalibration”
label.

**Outputs**

- pilot benchmark report;
- calibration memo;
- case revision proposals;
- category-balance observations.

**Exit criteria**

- at least one pilot run has been reviewed;
- metric behavior is understandable and not obviously misleading;
- calibration outputs are clearly labeled as public-set development evidence.

**How this enables the next phase**

Phase 8 depends on confidence that the benchmark is useful enough to become part
of routine workflow.

---

### Phase 8 — Workflow integration

**Goal**

Make the benchmark part of normal development practice without making it a hard
release gate.

**Prerequisites**

- Phase 7 pilot and calibration complete.

**Work scope**

- decide how developers run the benchmark;
- optionally add a CLI/report entrypoint;
- optionally add non-gating CI/report usage.

**Outputs**

- benchmark execution workflow;
- optional local command/report surface;
- non-gating integration guidance.

**Exit criteria**

- benchmark execution is stable enough for repeated local use;
- integration does not generate noisy or misleading policy signals.

**How this enables the next phase**

Only after workflow integration produces stable operational experience should
any subset be considered for gating.

---

### Phase 9 — Gate-candidate selection

**Goal**

Determine whether any subset of the benchmark is mature enough to influence
policy.

**Prerequisites**

- Phase 8 stable execution experience;
- known flakiness and maintenance characteristics.

**Work scope**

- identify stable, safety-relevant subsets;
- identify fragile or overfitted subsets that must remain advisory;
- evaluate whether any false-certification or boundary-discipline checks are
  mature enough to matter operationally.

**Outputs**

- gate-candidate shortlist;
- stability/flakiness note;
- recommendation on whether to keep the benchmark fully non-gating or adopt a
  narrow gated subset.

**Exit criteria**

- only stable, well-understood benchmark slices are considered for policy use.

**How this enables the next phase**

Phase 10 only exists if Phase 9 concludes that a narrow, stable subset deserves
policy coupling.

---

### Phase 10 — Release-policy integration

**Goal**

If justified, integrate a narrow mature subset of the benchmark into release or
product policy.

**Prerequisites**

- Phase 9 gate-candidate shortlist and recommendation.

**Work scope**

- define what benchmark failures are blocking vs advisory;
- update release/readiness policy narrowly;
- document what benchmark pass means and what it still does not mean.

**Outputs**

- narrow release-policy integration note;
- mature subset definition;
- explicit policy boundary.

**Exit criteria**

- no unstable or poorly interpreted subset is promoted into policy;
- benchmark integration remains evidence-bounded and conservative.

**How this completes the program**

The benchmark becomes an operational quality instrument only for the subset that
earns that role through earlier phases.

## Risks and mitigations

### Risk 1: public-set overfitting
Mitigation:
- treat holdout-local and private/external tiers as required program phases;
- do not interpret public benchmark improvement as full real-task readiness.

### Risk 2: false confidence hidden by aggregate metrics
Mitigation:
- keep false-certification as a hard veto;
- do not let aggregate precision/recall wash out safety-critical errors.

### Risk 3: premature gate coupling
Mitigation:
- keep reporting non-gating through Phases 6–8;
- make gate-candidate selection a separate late program phase.

### Risk 4: external corpus dependence blocks early progress
Mitigation:
- keep BayesFilter/private coverage as dependency-managed phases rather than
  prerequisites for starting the public benchmark program.

## What will not be concluded

Even if the early phases complete successfully, this program does **not** yet
conclude that:

- MathDevMCP is scientifically validated for all target workflows;
- benchmark passes imply release readiness;
- benchmark categories exhaust all mathematically relevant failure modes;
- BayesFilter or private corpus support is complete simply because the public
  benchmark is healthy.

## Done definition

The master benchmark program is complete only when:

- category scoring contracts are explicit and stable;
- public, holdout-local, and private/external corpus strategies exist;
- manifest contracts and tests are stable;
- non-gating reports are usable;
- pilot runs have calibrated the benchmark;
- workflow integration is stable;
- any gated subset, if one exists, is narrow and justified.
