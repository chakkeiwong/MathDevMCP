# MathDevMCP Real-Task Benchmark Spec

**Date:** 2026-06-16  
**Status:** Draft benchmark-program source of truth for first implementation slice  
**Scope:** Public benchmark spec and public-case manifest only; no CI/MCP/gate coupling yet

---

## 1. Goal

MathDevMCP already has a structured benchmark and release-corpus framework, but the current public suite is mostly synthetic or sanitized. That is useful for parser stability, seeded mismatch detection, and release gating, but it does **not** yet directly answer the product question:

> Can MathDevMCP support the real mathematical and code-document work that arises in the research-engineering repos under `~/python/`, especially `MacroFinance`, `dsge_hmc`, `latex-papers`, and BayesFilter-related materials?

This benchmark program exists to measure progress toward that real target.

The core product risks are:

1. **False certification** — claiming a derivation, implementation, or evidence status is stronger than the artifacts justify.
2. **Weak provenance** — retrieving the wrong label/chapter/file or failing to track the source of a claim.
3. **Shallow code-document matching** — treating term overlap as semantic equivalence.
4. **Poor abstention quality** — failing to say `unverified`/`inconclusive` when the evidence is insufficient, or abstaining for the wrong reason.
5. **Evidence-boundary drift** — treating engineering smoke evidence as convergence evidence, or convergence evidence as scientific validation.

The real-task benchmark is designed to score these risks directly.

---

## 2. Non-goals for this first slice

This first slice does **not**:

- integrate the new benchmark suite into `benchmark_gate` or the release gate;
- expose the new suite through CLI or MCP;
- attempt to execute all real-task cases automatically;
- treat the spec itself as evidence that MathDevMCP is ready for those tasks.

The first slice creates the durable artifacts needed for later executable integration:

1. this benchmark spec;
2. a machine-readable public-case manifest;
3. minimal documentation/catalog updates so the suite is discoverable.

---

## 3. Benchmark families

The suite is organized around the actual task families that matter in the target repos.

### 3.1 Retrieval and provenance
Questions of the form:

- find the correct label or chapter for a claim;
- retrieve the right local mathematical neighborhood;
- avoid nearby but irrelevant labels;
- preserve the file/label/provenance trail in the output.

**Failure mode scored:** wrong or weak source grounding.

### 3.2 Code-document consistency
Questions of the form:

- does the implementation visibly include the required documented operations;
- is a documented term or operation missing from code;
- is the code/document contract only partially implemented;
- is the system incorrectly treating keyword overlap as full semantic alignment.

**Failure mode scored:** shallow semantic matching and missed implementation drift.

### 3.3 Derivation boundary and abstention quality
Questions of the form:

- is a local derivation claim supported, unsupported, mismatched, or inconclusive;
- should the system certify, abstain, or flag a likely inconsistency;
- does the system explain *why* a claim is uncertified.

**Failure mode scored:** over-certification and low-quality abstention.

### 3.4 Numerical-oracle parity
Questions of the form:

- does a documented or adapter path match an existing deterministic/numerical oracle;
- do the reported pass criteria match the actual test harness;
- does the system recover the right thresholds and contractual boundaries from executable artifacts.

**Failure mode scored:** incorrect reading of exact/near-exact validation artifacts.

### 3.5 Evidence-boundary discipline
Questions of the form:

- what kind of evidence does this note/test/result actually provide;
- what stronger claim does it explicitly **not** justify;
- is the result engineering evidence, convergence evidence, or scientific evidence.

**Failure mode scored:** promotion of a weak artifact into a stronger scientific or readiness claim.

---

## 4. Scoring policy

The benchmark should score the same things the research workflow actually cares about.

### 4.1 Hard vetoes

Some failures should count as automatic case failures regardless of other strengths.

#### V1. False-confidence veto
Fail the case if the system:

- says `verified` or equivalent when the gold case expects `unverified` or `inconclusive`;
- says an implementation is mathematically faithful when the gold case only supports partial term/contract coverage;
- promotes engineering canary evidence to convergence, posterior, GPU, or scientific evidence.

#### V2. Forbidden-claim veto
Fail the case if the system makes a claim explicitly forbidden by the gold record, e.g.:

- “this establishes convergence”
- “this proves the posterior is valid”
- “code and document are mathematically equivalent”

when the source artifact explicitly does not justify that statement.

### 4.2 Graded dimensions

For non-vetoed cases, score each of the following from 0 to 1:

1. **Provenance accuracy**
   - right repo/file/label/chapter/context
2. **Classification accuracy**
   - right `expected_status`, and `expected_substatus` when used
3. **Coverage accuracy**
   - mentions the required operations/terms/contract boundaries
4. **Abstention quality**
   - abstains when it should, and for the right reason
5. **Actionability**
   - gives the right next safe step instead of a generic or misleading recommendation

### 4.3 Suite-level metrics

The suite should eventually report at least:

- hard-veto pass rate
- false-confidence rate
- status accuracy
- provenance accuracy
- abstention precision
- abstention recall
- evidence-boundary accuracy
- large-root robustness (for future executable integration)

---

## 5. Corpus tiers

To avoid overfitting and to support real repo/private work, the benchmark program uses three corpus tiers.

### 5.1 `public`
Committed benchmark cases derived from public or sanitized repo artifacts.

Use this tier for:

- everyday development;
- schema stabilization;
- public CI-safe benchmark evolution.

### 5.2 `holdout_local`
Cases available locally but not intended as day-to-day optimization targets.

Use this tier for:

- pre-release evaluation;
- checking whether improvements generalize beyond the public seed set;
- larger or more fragile chapter-scale cases.

### 5.3 `private_external`
Real or sanitized external/private repo/document cases not committed into the public benchmark corpus.

Use this tier for:

- BayesFilter external repo tasks;
- private department corpora;
- realistic production-facing regression checks.

The benchmark design must explicitly support external repo roots and path redaction, rather than assuming every corpus is inside the MathDevMCP checkout.

---

## 6. Public-case schema

The public benchmark manifest stores task-oriented cases rather than release-oriented corpus entries.

### 6.1 Recommended fields

Per case, store:

- `id`
- `family`
- `repo`
- `task_type`
- `difficulty`
- `public`
- `document_roots`
- `document_files`
- `code_roots`
- `code_files`
- `labels`
- `prompt`
- `gold`
  - `expected_status`
  - `expected_substatus` (optional)
  - `expected_labels`
  - `required_terms`
  - `forbidden_claims`
  - `required_next_actions`
  - `evidence_class`
  - `false_confidence_veto`
- `notes`

### 6.2 Why this differs from `ReleaseCorpusEntry`

`ReleaseCorpusEntry` is designed around release-corpus coverage and privacy validation. The real-task benchmark manifest is designed around **tasks**, with explicit prompts, gold outcomes, and claim-boundary constraints.

The real-task manifest should still reuse the same design instincts:

- explicit public/private split;
- externally rooted corpora allowed;
- structured expected labels/operations;
- redaction and non-claim discipline preserved in later executable slices.

### 6.3 Path policy for the public manifest

The committed public manifest stores file and directory references as **repo-root-relative** paths from the MathDevMCP checkout root. Sibling repositories may be referenced via `../` segments because several benchmark sources live outside the MathDevMCP checkout.

For the public tier:

- absolute paths are not allowed;
- relative paths must resolve from the MathDevMCP repo root;
- validator checks should treat unresolved or absolute public paths as high-severity findings.

---

## 7. Initial public benchmark inventory

The first public inventory should be intentionally small but high-value: cases with explicit pass criteria, documented evidence boundaries, or deterministic oracle behavior.

### 7.1 `MF-02-large-scale-lgssm-missing-data-policy`

**Repo:** `MacroFinance`  
**Source:** `tests/test_large_scale_lgssm_missing_data_policy.py`

**Why it is strong:**

- explicit pending/error behavior for unsupported masked observations;
- deterministic shape and NaN failure checks;
- highly objective gold semantics.

**Gold target:**

- sparse/masked observations are not supported yet;
- masked Kalman updates and derivative slicing are pending;
- NaN sparse proxy fails before Kalman likelihood;
- mask shape mismatch is configuration error.

**Primary family:** numerical-oracle parity / evidence boundary.

---

### 7.2 `MF-03-hmc-helper-nonclaim-boundary`

**Repo:** `MacroFinance`  
**Source:** `tests/test_hmc_regression.py`

**Why it is strong:**

- explicit comments already distinguish numerical-stability helpers from structural-identification tests;
- forces the system to preserve the non-claim boundary.

**Gold target:**

- validates mass-matrix and HMC-diagnostic helper stability;
- does **not** establish identification, posterior validity, or model-level convergence.

**Primary family:** evidence-boundary discipline.

---

### 7.3 `DH-01-strict-nk-convergence-audit`

**Repo:** `dsge_hmc`  
**Source:** `tests/extended/test_nk_convergence_audit.py`

**Why it is strong:**

- explicit quantitative pass thresholds;
- clear statement that it is heavyweight and not routine smoke validation.

**Gold target:**

- `R-hat < 1.01`;
- `ESS_bulk > 400`;
- `MCSE/SD < 10%`;
- medium/overnight audit scope, not quick smoke evidence.

**Primary family:** numerical-oracle parity / evidence boundary.

---

### 7.4 `DH-02-bayesfilter-qr-value-parity`

**Repo:** `dsge_hmc`  
**Source:** `tests/contracts/test_real_nk_bayesfilter_qr_kalman_migration.py`

**Why it is strong:**

- exact adapter/direct value parity against a tiny fixture;
- includes capability-boundary metadata such as unavailable score authority and non-ready XLA HMC status.

**Gold target:**

- adapter log probability matches direct posterior value;
- adapter identifies QR Kalman implementation path;
- `value_score_authority == unavailable`;
- `xla_hmc_ready == false`.

**Primary family:** code-document consistency / numerical-oracle parity.

---

### 7.5 `DH-04-bayesfilter-engineering-qualification-boundary`

**Repo:** `dsge_hmc`  
**Source:** `docs/plans/BayesFilterDSGE/bayesfilter-model-suite-hmc-qualification-result-2026-06-08.md`

**Why it is strong:**

- unusually explicit evidence-boundary language;
- states both what passed and what is explicitly **not** concluded.

**Gold target:**

- this is engineering qualification evidence only;
- not sampler convergence evidence;
- not posterior validity evidence;
- not DSGE/NK readiness, GPU readiness, or scientific/economic evidence.

**Primary family:** evidence-boundary discipline.

---

### 7.6 `LP-01-analytical-validation-lgssm`

**Repo:** `latex-papers`  
**Source:** `CIP_monograph/chapters/ch33_analytical_validation.tex`

**Why it is strong:**

- gives an analytical gold-standard validation ladder;
- includes a concrete practical test specification and pass criterion.

**Gold target:**

- linear-Gaussian SSM setup;
- EDH/Kalman exactness statements;
- practical test spec with `N in {50, 100, 500, 1000}`;
- pass if `|log p_hat - log p_KF| < 1e-2` for `N = 1000`.

**Primary family:** retrieval/provenance + derivation boundary + numerical-oracle parity.

---

### 7.7 `LP-02-basis-reconciliation-audit`

**Repo:** `latex-papers`  
**Source:** `CIP_monograph/plan_items_3_4_6_7.md`

**Why it is strong:**

- documents a real multi-location sign-convention reconciliation task;
- includes explicit diagnosis and proposed equivalence arguments.

**Gold target:**

- recover the distinction between market basis and model basis;
- recover the sign mapping `x_t = -x_market`;
- identify the risk from multi-location re-derivation and symbol drift.

**Primary family:** retrieval/provenance + code-document consistency + derivation-boundary discipline.

---

### 7.8 `RA-01-parser-benchmark-inventory`

**Repo:** `MacroFinance/ResearchAssistant`  
**Source:** `tests/integration/test_benchmark_inventory.py`

**Why it is strong:**

- captures a working benchmark-inventory/reporting discipline from an adjacent tool;
- useful as a structural reference for later executable integration.

**Gold target:**

- expected benchmark inputs exist;
- benchmark report includes `report`, `results`, `expected`, `parser_runs`, and `status`;
- synthetic fixtures remain scoreable and inventory-shaped.

**Primary family:** evidence-boundary discipline / benchmark-structure discipline.

---

## 8. Public/holdout/private strategy

### 8.1 Public cases
The eight cases above should form the initial committed public manifest.

### 8.2 Holdout-local expansion targets
The next holdout-local pool should include:

- additional chapter-scale `latex-papers` retrieval and audit cases;
- larger `dsge_hmc` validation runners and nonconvergence documents;
- more `MacroFinance` backend-parity and identification-audit tasks.

### 8.3 Private/external expansion targets
These should include:

- the external BayesFilter repo when locally available;
- private or sanitized department corpora;
- real cross-repo tasks whose paths or texts cannot be committed.

---

## 9. First-slice implementation boundaries

The first slice should include only:

- this spec file;
- a `benchmarks/real_tasks/README.md`;
- a `benchmarks/real_tasks/manifests/public_cases.json` manifest;
- a descriptive addition to `src/mathdevmcp/benchmark_manifest.py`;
- a short pointer from `benchmarks/README.md`.

The first slice should **not**:

- add these cases to `build_benchmark_report()` in `src/mathdevmcp/benchmarks.py`;
- add new CLI commands yet;
- add new MCP tools yet;
- modify `benchmark_gate` semantics.

This avoids premature gate coupling while the schema and case inventory stabilize.

---

## 10. Second-slice implementation plan (future)

Once the spec and public manifest are accepted, the next slice should:

1. add a loader/validator for the real-task manifest;
2. add tests for manifest shape and representative case semantics;
3. decide whether to:
   - integrate the suite into `run-benchmarks`,
   - expose it via a dedicated command, or
   - keep it as a separate non-gating report;
4. add a non-gating dry-run report over the initial public cases;
5. only after that, decide whether any subset belongs in release-gated reporting.

---

## 11. Verification for this first slice

### 11.1 Artifact integrity

- `public_cases.json` is well-formed JSON;
- all public referenced file paths exist;
- the spec includes benchmark families, scoring policy, corpus tiers, and case inventory.

### 11.2 Catalog consistency

- the benchmark catalog exposes a descriptive entry for the new real-task suite.

### 11.3 Documentation consistency

- `benchmarks/README.md` distinguishes synthetic fixtures from the new real-task program;
- `benchmarks/real_tasks/README.md` explains public vs holdout vs private use.

---

## 12. Why this benchmark matters

The hard part in these repos is not generating plausible-looking summaries. The hard part is avoiding plausible but unsupported mathematical or empirical claims while still being useful on real tasks. This benchmark is designed to measure exactly that.
