# MathDevMCP Holdout-Local Corpus Subplan

## Date

2026-06-17

## Source artifact scope

This subplan narrows and operationalizes Phase 3 of:

- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`

It also depends on the current public benchmark artifacts:

- `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`
- `benchmarks/real_tasks/README.md`
- `benchmarks/real_tasks/manifests/public_cases.json`
- `src/mathdevmcp/real_tasks_manifest.py`
- `src/mathdevmcp/real_tasks_report.py`

## Purpose

The holdout-local tier exists to evaluate whether improvements that appear on
the committed public benchmark corpus generalize beyond that public set.

The public benchmark is a development/calibration surface. The holdout-local
corpus is the first benchmark tier whose main purpose is to resist public-set
optimization pressure.

Holdout-local is therefore not “more public cases.” It is an evaluation
separation mechanism.

## Holdout-local is not the private/external tier

This subplan is only for `holdout_local`.

It is **not** the same as:

- external/private repo support,
- private corpus redaction policy,
- BayesFilter external-ingestion policy,
- release-gated private evidence.

Those belong to the later private/external tier.

## Skeptical audit

This holdout-local slice is valid only if it remains policy-first and does not
pretend to create evaluation evidence by itself.

- **Wrong baseline checked:** the public benchmark is a development surface, not
  already a trustworthy generalization benchmark.
- **Proxy-metric checked:** adding a holdout template is not the same as running
  holdout evaluation.
- **Stop condition checked:** this slice should stop at policy and scaffolding;
  it should not add a second executable manifest contract prematurely.
- **Hidden assumptions checked:** holdout-local availability may vary by machine
  and user; this subplan must allow local population without requiring
  committed local data.
- **Environment mismatch checked:** no CLI, MCP, gate, or private-corpus
  integration is required for this slice.
- **Artifact usefulness checked:** the outputs of this slice must make later
  calibration and evaluation boundaries clearer, not merely add directories.

## Validation summary

| Holdout-local concern | Why it matters | Current state | Plan decision |
|---|---|---|---|
| Public-set overfitting | The committed public cases are now visible and easy to optimize against | Public corpus exists and is loadable/reportable | Add explicit holdout-local policy and scaffolding |
| Repeated author exposure | Benchmark authors may unconsciously shape public cases to fit current product behavior | Not yet controlled structurally | Make author-exposure status one allowed disjointness axis |
| Task-template leakage | Cases can differ in file path but still reuse the same benchmark template | Not yet explicitly fenced | Require at least one meaningful disjointness axis |
| Public-calibration overclaim | Public benchmark improvement could be over-read as readiness evidence | Master plan already warns against this | Repeat and operationalize the non-claim rule here |
| Manifest sprawl | A second executable manifest contract would add complexity too early | Public manifest/loader/report already exist | Keep holdout-local at template/scaffolding level only |

## Holdout-local policy rules

### 1. Purpose rule

Holdout-local cases exist to evaluate generalization beyond the committed public
benchmark set.

A holdout-local case should be selected because it meaningfully protects against
public-set tuning, not because it is merely another convenient source artifact.

### 2. Disjointness rule

A holdout-local case should differ from public cases by at least one meaningful
axis.

Allowed disjointness axes include:

- different source repo area or document family;
- different label neighborhood or chapter neighborhood;
- different task template;
- different benchmark-author exposure status.

A case should not be considered holdout-local if it differs only by filename or
minor path placement while keeping the same effective benchmark template.

### 3. Non-claim rule

Improvement on the public benchmark set alone is **development/calibration
evidence**, not holdout evidence.

Until holdout-local evaluation has actually been run, no benchmark note or
report may imply:

- generalization beyond the public set,
- reduced overfitting risk,
- benchmark maturity beyond public calibration,
- readiness evidence derived from holdout behavior.

### 4. Usage rule

Holdout-local cases may be used for:

- milestone evaluation,
- pre-release benchmark sanity checks,
- public-calibration cross-checks,
- bounded local quality review.

Holdout-local cases should **not** be repeatedly optimized against as though
they were public development fixtures. If repeated iteration against a holdout
case becomes necessary, that case should either:

- be promoted into a public-like calibration corpus with explicit documentation,
  or
- be replaced by a fresh holdout candidate.

### 5. Storage rule

Holdout-local scaffolding may live in git as:

- policy docs,
- README guidance,
- manifest templates.

Actual populated local holdout manifests do **not** need to be committed.

This allows local users to maintain holdout inventories without turning the
holdout tier into another public benchmark surface.

## Scaffolding shape

This slice should add only lightweight scaffolding:

- `benchmarks/real_tasks/holdout_local/README.md`
- `benchmarks/real_tasks/manifests/holdout_local_cases.template.json`

The template should mirror the public case schema closely enough to discourage
schema drift, but it should remain clearly marked as:

- a template/scaffold,
- not committed evaluated data,
- not part of the current public report surface.

## What this slice should not do

This slice should **not**:

- create a second executable manifest loader/validator contract;
- add holdout-local data to the public report;
- connect holdout-local to `benchmark_gate`;
- add CI/release semantics;
- blur holdout-local with private/external policy.

## Deliverables

- this holdout-local corpus subplan;
- `benchmarks/real_tasks/holdout_local/README.md`;
- `benchmarks/real_tasks/manifests/holdout_local_cases.template.json`;
- a pointer from the top-level real-task README to the holdout-local scaffold.

## Exit criteria

This slice is complete when:

- holdout-local purpose is explicitly documented;
- minimum disjointness is defined;
- the non-claim boundary between public calibration and holdout evaluation is
  explicit;
- scaffolding exists for local holdout inventories;
- current public reporting and manifest contracts remain unchanged.

## Verification

### Primary verification

Read this subplan and confirm it defines:

- purpose,
- disjointness,
- non-claim boundary,
- usage policy,
- storage policy.

### Artifact verification

Confirm the following files exist and are consistent with this policy:

- `benchmarks/real_tasks/holdout_local/README.md`
- `benchmarks/real_tasks/manifests/holdout_local_cases.template.json`

### Documentation consistency

Confirm `benchmarks/real_tasks/README.md` points to the holdout-local scaffold
and still distinguishes:

- `public`
- `holdout_local`
- `private_external`

### Non-regression verification

Confirm this slice does not change:

- `benchmark_gate`
- the public report behavior
- the public manifest loader/validator contracts
- release-readiness logic
