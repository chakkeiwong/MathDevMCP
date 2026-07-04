# MathDevMCP Real-Task Benchmark Program Status Dashboard

Role: current-synthesis
Current-state status: living
Grounded in:
- docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md
## Date

2026-06-19

## Purpose

This dashboard gives a compact execution view of the benchmark program against:

- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`

It is intended to answer three questions quickly:

1. what phases are complete enough for now,
2. what phases are only partially complete,
3. what the most justified next program actions are.

## Current program goal

Build a benchmark program that measures whether MathDevMCP is improving on real
mathematical, code-document, derivation, and evidence-boundary tasks from
`MacroFinance`, `dsge_hmc`, `latex-papers`, and BayesFilter-related workflows,
while keeping false certification as a hard veto and keeping benchmark evidence
strictly below release/scientific readiness claims unless later phases earn a
stronger role.

## Status table

| Phase | Name | Status | Evidence/artifacts | Remaining work |
|---|---|---|---|---|
| 0 | Program framing and governance | Complete enough for now | Benchmark spec, master program, audit | Revisit only if program scope changes materially |
| 1 | Category contracts and scoring rules | Complete enough for now | Category scoring subplan | Later refinement only if calibration reveals category-contract flaws |
| 2 | Public corpus buildout | In progress | Public manifest, richer 12-case public corpus, candidate fixtures | More category balancing; possibly more thin-family cases |
| 3 | Holdout-local corpus design | In progress | Holdout subplan, README, template, recipe, candidate inventory, example workflow note, local discovery helper, local scaffold initializer, first local population checkpoint note, local-only holdout scoring layer, local candidate-fixture scaffold and runner | Broader local holdout population, broader local scoring coverage, later holdout-informed calibration, and eventual decisions about whether richer holdout scoring is justified |
| 4 | Private/external corpus design | Mostly remaining | Policy framing only in master program and related notes | Actual private/external representation and later execution policy |
| 5 | Schema, loader, validator hardening | Complete for public tier | Public manifest loader/validator + tests | Future extension for holdout/private tiers if justified |
| 6 | Non-gating reporting | Complete for public tier | Public report + scored report | Future richer reporting only after more calibration |
| 7 | Pilot execution and calibration | In progress | Public pilot calibration note, structural scoring calibration note | Broader scored calibration and later holdout-informed calibration |
| 8 | Workflow integration | Not started | None by design | Decide whether/when to add CLI or routine workflow surfaces |
| 9 | Gate-candidate selection | Not started | None by design | Determine if any subset is stable enough for operational use |
| 10 | Release-policy integration | Not started | None by design | Only after gate-candidate selection justifies it |

## Completed / strong foundation layers

### Program and planning layer

Completed enough for now:

- `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `docs/plans/mathdevmcp-benchmark-category-scoring-subplan-2026-06-17.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-audit-2026-06-17.md`

### Public corpus and contract layer

Completed for the current public slice:

- `benchmarks/real_tasks/manifests/public_cases.json`
- `src/mathdevmcp/real_tasks_manifest.py`
- `tests/test_real_tasks_manifest.py`

### Public reporting and scoring layer

Completed for the current non-gating structural slice:

- `src/mathdevmcp/real_tasks_report.py`
- `src/mathdevmcp/real_tasks_scoring.py`
- `src/mathdevmcp/real_tasks_scored_report.py`
- `tests/test_real_tasks_report.py`
- `tests/test_real_tasks_scoring.py`
- `tests/test_real_tasks_scored_report.py`

### Fixture and normalization layer

Completed as bounded prototypes:

- `benchmarks/real_tasks/fixtures/public_candidate_answers.json`
- `tests/test_real_tasks_candidate_fixtures.py`
- `src/mathdevmcp/real_tasks_answer_normalization.py`
- `tests/test_real_tasks_answer_normalization.py`
- `docs/plans/mathdevmcp-answer-normalization-prototype-calibration-note-2026-06-19.md`

### Holdout-local policy/scaffold layer

Completed as policy/scaffold only:

- `docs/plans/mathdevmcp-holdout-local-corpus-subplan-2026-06-17.md`
- `benchmarks/real_tasks/holdout_local/README.md`
- `benchmarks/real_tasks/manifests/holdout_local_cases.template.json`
- `docs/plans/mathdevmcp-holdout-local-population-recipe-2026-06-18.md`
- `docs/plans/mathdevmcp-holdout-local-candidate-inventory-2026-06-18.md`
- `docs/plans/mathdevmcp-holdout-local-population-example-2026-06-19.md`

### Holdout-local operational starter layer

Completed as bounded local workflow helpers only:

- `src/mathdevmcp/real_tasks_holdout_local.py`
- `tests/test_real_tasks_holdout_local.py`

### Holdout-local first population checkpoint

Completed as a local-only checkpoint:

- `.local/mathdevmcp/holdout_local_cases.json` (ignored local artifact)
- `docs/plans/mathdevmcp-holdout-local-first-population-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-local-broadened-population-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-local-further-broadened-seed-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-local-broader-seed-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-local-broader-seed-note-ii-2026-06-19.md`

### Holdout-local first scoring layer

Completed as a bounded local-only scoring surface:

- `src/mathdevmcp/real_tasks_holdout_local_scoring.py`
- `tests/test_real_tasks_holdout_local_scoring.py`
- `docs/plans/mathdevmcp-holdout-local-first-scoring-boundary-note-2026-06-19.md`

### Holdout-local candidate-fixture layer

Completed as local-only execution scaffolding:

- `benchmarks/real_tasks/fixtures/holdout_local_candidate_answers.template.json`
- `docs/plans/mathdevmcp-holdout-local-candidate-fixture-boundary-note-2026-06-19.md`
- `.local/mathdevmcp/holdout_local_candidate_answers.json` (ignored local artifact)

## In-progress areas

### Public corpus maturity

The public corpus is real and structurally useful, but still not fully mature.

Current public corpus status:

- case count: 12
- expected statuses represented:
  - `consistent`
  - `unverified`
  - `mismatch`
  - `inconclusive`

What remains:

- further improve thin categories,
- decide whether more retrieval/provenance or derivation-heavy public cases are
  needed,
- avoid overfitting public growth to the current structural scorer.

### Calibration maturity

Calibration has started, but remains public-tier and structure-first.

Current calibration artifacts:

- `docs/plans/mathdevmcp-real-tasks-benchmark-public-pilot-calibration-note-2026-06-17.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-structural-scoring-calibration-note-2026-06-18.md`
- `docs/plans/mathdevmcp-answer-normalization-prototype-calibration-note-2026-06-19.md`

What remains:

- more scored calibration over representative candidates,
- later holdout-informed calibration,
- eventually deciding where structural scoring stops being enough.

### Holdout-local operational readiness

Holdout-local is no longer only a policy idea; it now has a small operational
starter layer, a first local-only scoring surface, and local candidate-fixture
scaffolding.

Current holdout-local operational artifacts:

- `src/mathdevmcp/real_tasks_holdout_local.py`
- `src/mathdevmcp/real_tasks_holdout_local_scoring.py`
- `tests/test_real_tasks_holdout_local.py`
- `tests/test_real_tasks_holdout_local_scoring.py`
- `benchmarks/real_tasks/fixtures/holdout_local_candidate_answers.template.json`
- `.local/mathdevmcp/holdout_local_cases.json` (ignored local artifact)
- `.local/mathdevmcp/holdout_local_candidate_answers.json` (ignored local artifact)

Interpretation:

- the benchmark can now discover whether a local holdout manifest exists;
- it can initialize a local scaffold from the committed template without
  overwriting existing local work;
- it can score explicitly provided normalized candidate answers against local
  holdout cases using a local-only, non-gating surface;
- it can scaffold local candidate-answer fixtures for repeated local execution;
- it now has a small seven-case local seed, with full local candidate-fixture
  coverage;
- and it is still far short of broad populated holdout evaluation or
  holdout-backed generalization claims.

## Clearly remaining program work

### 1. Real holdout-local population

The holdout-local tier now has:

- policy and scaffold artifacts,
- local discovery and initialization helpers,
- one first local-only populated holdout checkpoint,
- one first local-only scoring surface,
- one local candidate-fixture scaffold/runner path,
- and a small seven-case local seed.

It is therefore no longer merely conceptual, but it is still not yet a mature
holdout-backed evaluation tier.

Remaining tasks:

- additional local holdout entries maintained outside the public corpus only when they add real representativeness value,
- broader holdout scoring/evaluation over the current seven-case local seed only if that materially improves the calibration signal,
- eventually holdout-informed calibration.

### 2. Private/external tier implementation

This is still mostly future work.

Remaining tasks:

- private/external manifest and validation policy if needed,
- BayesFilter/external benchmark handling,
- redaction-safe external/private evaluation structure.

### 3. Workflow integration decisions

The benchmark is intentionally still library-/artifact-level.

Remaining tasks:

- decide whether a CLI surface is justified,
- decide whether local developer workflow integration is useful,
- keep all of that explicitly non-gating until later phases are earned.

### 4. Gate/release decisions

Still entirely future work.

No current artifact should be interpreted as:

- benchmark gate readiness,
- CI pass/fail benchmark policy,
- release-policy integration,
- scientific-readiness evidence.

## Current best interpretation

The benchmark program is now in a **strong foundation + early execution** state.

That means:

- the benchmark is real,
- parts of it are executable,
- calibration has begun,
- but it is still not mature enough to support holdout-backed generalization or
  policy use.

## Most justified next actions

### Highest-priority remaining work
1. continue holdout-local from a small seven-case local seed only when new additions add clear representativeness value;
2. continue scored calibration in a bounded way;
3. decide later whether more public cases or better normalization are more
   valuable than immediate workflow integration.

### Actions that are still premature
- benchmark gating;
- release-policy coupling;
- broad semantic evaluator claims;
- treating public-tier success as generalization evidence.

## Non-claim boundary

This dashboard does **not** mean the benchmark is complete.

It means the benchmark program now has enough structure to be managed
intentionally under the master program rather than through ad hoc changes.
