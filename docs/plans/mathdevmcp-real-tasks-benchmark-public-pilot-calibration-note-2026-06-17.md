# MathDevMCP Real-Task Benchmark Public-Set Pilot Calibration Note

## Date

2026-06-17

## Scope

This note records the first calibration-oriented interpretation of the current
**public** real-task benchmark artifacts.

It is grounded in:

- `benchmarks/real_tasks/manifests/public_cases.json`
- `src/mathdevmcp/real_tasks_manifest.py`
- `src/mathdevmcp/real_tasks_report.py`
- `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `docs/plans/mathdevmcp-benchmark-category-scoring-subplan-2026-06-17.md`
- `docs/plans/mathdevmcp-holdout-local-corpus-subplan-2026-06-17.md`

This is a **public-set pilot calibration note**. It is not a benchmark execution
result note for holdout-local or private/external corpora.

## Evidence contract

### Question

What does the current public real-task benchmark corpus already tell us about
MathDevMCP benchmark structure and category coverage, and what does it still
not justify us to claim before holdout-local evaluation and executable scoring
are in place?

### Exact baseline / comparator

The baseline is the current committed public benchmark artifact stack:

- public manifest,
- public manifest loader/validator,
- non-gating public report,
- benchmark spec and master-program planning stack.

This note does **not** compare MathDevMCP outputs on benchmark cases against a
prior benchmark run. It is a structural calibration note over the current public
corpus and reporting surfaces.

### Primary criterion

The primary criterion for this note is whether the current public benchmark can
be honestly interpreted as:

- a valid **development/calibration surface**,
- with explicit safety-oriented case metadata,
- without being overclaimed as a generalization or readiness benchmark.

### Veto diagnostics

This note would be considered structurally unsound if any of the following were
true:

- the committed public manifest did not load or validate cleanly;
- the public report implied pass/fail gate semantics or release readiness;
- the current artifacts implied holdout or private-external evidence that does
  not yet exist;
- the benchmark planning stack failed to preserve false-certification as a hard
  veto.

### Explanatory-only diagnostics

The following are useful descriptive signals, but not by themselves promotion
criteria:

- counts by category;
- counts by repo;
- counts by difficulty;
- counts by expected status;
- total number of public cases.

These help us understand the public surface, but they do not by themselves prove
coverage adequacy or benchmark maturity.

### What will not be concluded

This note does **not** conclude that:

- MathDevMCP performs well on the public benchmark tasks;
- the benchmark is calibrated well enough for holdout or release interpretation;
- public-case improvement would imply generalization;
- the current case distribution is already representative;
- the benchmark is ready for `benchmark_gate`, CI pass/fail semantics, or
  release policy coupling.

### Planned artifact

This note itself is the artifact preserving the interpretation boundary between:

- public corpus inventory/report structure, and
- actual benchmark performance or generalization evidence.

## Public-set structural findings

### 1. The public benchmark is now a real machine-readable artifact stack

The benchmark is no longer only a planning idea.

The current public stack includes:

- a committed public case manifest;
- a typed loader/validator;
- focused manifest tests;
- a non-gating report surface;
- a benchmark spec, master program, scoring subplan, and holdout-local policy
  scaffold.

That means the public benchmark now has enough structure to serve as a real
calibration/development surface.

### 2. The current public corpus is still small but now has a broader status mix

Current public case count: **12**.

Current public expected-status distribution:

- `consistent`: 6
- `unverified`: 2
- `mismatch`: 3
- `inconclusive`: 1

Current public family distribution:

- `evidence_boundary_discipline`: 5
- `numerical_oracle_parity`: 2
- `code_document_consistency`: 3
- `retrieval_and_provenance`: 1
- `derivation_boundary_and_abstention`: 1

Current public repo distribution:

- `MacroFinance`: 3
- `dsge_hmc`: 6
- `latex-papers`: 2
- `MacroFinance/ResearchAssistant`: 1

Current public difficulty distribution:

- `easy`: 2
- `medium`: 6
- `hard`: 4

Interpretation:

- the corpus now spans multiple repos and all major benchmark families;
- the status mix is healthier because contradiction and uncertainty handling are
  now represented in the public tier;
- but some families still remain thin, so the public set is still best
  understood as an initial calibration surface rather than a mature balanced
  benchmark.

### 3. The public benchmark is safety-oriented by construction

Every currently committed public case has:

- explicit gold expectations,
- forbidden claims,
- required next actions,
- `false_confidence_veto = true`.

This is a strong design choice and aligns with the product’s main risk model:
false certification is more dangerous than a cautious abstention.

Interpretation:

- the benchmark is already biased in the right direction for safety;
- but the current note cannot yet say whether later executable scoring will
  preserve that discipline in practice.

### 4. The current public report is correctly non-gating

The current public report explicitly says that it is:

- public-corpus inventory/report evidence only;
- not benchmark execution evidence;
- not holdout-local or private-external evidence;
- not release-readiness evidence;
- not a pass/fail gate.

Interpretation:

- this is the right boundary for the current program stage;
- the report is useful for inspection and planning, but not yet for policy.

## Calibration interpretation

### What the current public benchmark *does* justify

At this stage, the public benchmark justifies the following claims:

1. MathDevMCP now has a committed real-task public benchmark corpus.
2. That public corpus is structurally valid and machine-checkable.
3. The corpus already encodes the most important safety boundary: false
   confidence is a hard veto.
4. The benchmark program now has enough structure to begin later executable
   scoring and public-set calibration work.

### What the current public benchmark does **not** yet justify

At this stage, the public benchmark does **not** justify the following claims:

1. that MathDevMCP performs well on the benchmark;
2. that the benchmark is balanced enough for meaningful category-level metric
   comparison;
3. that public-set improvements would imply generalization;
4. that holdout-local or private-external coverage is ready;
5. that any release or workflow gate should consume this benchmark.

## Main calibration uncertainties

1. **Category thinness**
   - some categories currently have only one public case;
   - category-level precision/recall interpretation will remain fragile until
     those categories grow.

2. **Status distribution is improving but still informative to watch**
   - the public set now contains `consistent`, `unverified`, `mismatch`, and
     `inconclusive` cases;
   - this is much better for exercising contradiction detection and uncertainty
     handling;
   - but the distribution is still small enough that category-level metrics may
     remain unstable.

3. **Difficulty labels are not empirically calibrated yet**
   - `easy` / `medium` / `hard` are structurally present, but no executed
     evidence yet shows that those labels correspond to actual product
     difficulty.

4. **Holdout-local is policy-only so far**
   - the holdout tier now has a subplan, README, and template, but not yet a
     populated evaluated corpus.

5. **Scoring contracts are not yet executable metrics**
   - the category-scoring subplan defines what precision and recall mean, but we
     do not yet have an evaluator that computes those metrics from actual model
     responses.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the current public benchmark as a valid development/calibration surface only | Met | No structural veto found in the current public manifest/report stack | Thin category counts, skewed status mix, no holdout results yet | Expand holdout-local from policy/scaffold toward an eventual evaluable local inventory, and later add executable category scoring | No generalization, no benchmark performance result, no gate/readiness implication |

## Post-run red-team note

### Strongest alternative explanation

The current public benchmark may look healthy largely because it is still small,
carefully hand-constructed, and dominated by cases whose safety contract is
already well understood. A later executable scoring layer might reveal that the
benchmark is much harder to interpret than the structural artifacts suggest.

### What result would overturn confidence

Confidence in the current interpretation would be weakened if:

- later executable scoring showed that the current gold fields are too thin to
  support reproducible judgments;
- holdout-local population revealed that public-set templates were easier and
  more repetitive than they appeared;
- category-level metrics proved too unstable because the current family counts
  are too low.

### Weakest part of the evidence

The weakest part of the current evidence is not schema correctness; it is the
small size and narrow status distribution of the current public corpus.

## Next hypotheses to test

1. **Executable scoring hypothesis**
   - The current public gold fields are sufficient to support reproducible
     category-level scoring without ad hoc human judgment.

2. **Category-balance hypothesis**
   - Adding a small number of new public cases in thin categories will improve
     public calibration without undermining the role of the holdout-local tier.

3. **Negative-case hypothesis**
   - The public corpus needs at least a small set of `mismatch` or
     `inconclusive` public cases before category-level pilot metrics are
     informative.

4. **Holdout-readiness hypothesis**
   - The current holdout-local policy/template is enough to begin a later local
     holdout inventory without changing the public manifest contract.

## Next justified action

The next justified action is **not** benchmark gating or policy coupling.

The next justified action is to continue the benchmark buildout in one of two
bounded directions:

1. enrich the corpus shape where it is visibly thin (especially negative and
   ambiguity cases), or
2. implement the first executable scoring layer that uses the current public
   gold contracts while preserving all current non-claim boundaries.
