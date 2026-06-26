# MathDevMCP Real-Task Benchmark Structural Scoring Calibration Note

## Date

2026-06-18

## Scope

This note records the first calibration-oriented interpretation of the new
**structural scoring layer** for the public real-task benchmark corpus.

It is grounded in:

- `benchmarks/real_tasks/manifests/public_cases.json`
- `src/mathdevmcp/real_tasks_manifest.py`
- `src/mathdevmcp/real_tasks_report.py`
- `src/mathdevmcp/real_tasks_scoring.py`
- `src/mathdevmcp/real_tasks_scored_report.py`
- `docs/plans/mathdevmcp-benchmark-category-scoring-subplan-2026-06-17.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-public-pilot-calibration-note-2026-06-17.md`

This is a **structural scoring calibration note**. It evaluates what the new
scoring layer can and cannot honestly support at this stage.

## Evidence contract

### Question

What does the first executable structural scoring layer already establish about
benchmark mechanics, and what remains out of scope until a richer evaluator and
holdout execution exist?

### Exact baseline / comparator

The baseline is the current public benchmark stack **before semantic/free-form
benchmark execution**:

- public manifest,
- public manifest loader/validator,
- public report,
- structural scorer for normalized candidate answers,
- non-gating scored report.

This note compares the current benchmark apparatus to its earlier
artifact-only state. It does **not** compare benchmarked model outputs against a
previous system run over holdout or private corpora.

### Primary criterion

The primary criterion is whether the structural scorer can now execute the
manifest-defined public gold contracts in a reproducible, deterministic, and
non-gating way.

### Veto diagnostics

This note would be considered unsound if any of the following were true:

- the scorer silently overrode the benchmark’s false-confidence veto policy;
- the scored report implied semantic benchmark execution rather than structural
  scoring of normalized candidate answers;
- the new scoring layer introduced gate, CLI, MCP, or release-readiness
  coupling;
- the scorer could not handle representative committed-manifest strings such as
  `R-hat < 1.01`, `MCSE/SD < 10%`, or the explicit forbidden-claim cases.

### Explanatory-only diagnostics

The following are useful, but not by themselves promotion criteria:

- unit-test counts,
- scored batch totals,
- by-status and by-family summaries,
- the mere existence of `mismatch`/`inconclusive` public cases.

These help characterize the current scorer, but they do not yet establish that
benchmark performance interpretation is mature.

### What will not be concluded

This note does **not** conclude that:

- MathDevMCP now has a semantic evaluator for free-form model outputs;
- the public benchmark is fully calibrated;
- category precision/recall is ready for policy interpretation;
- holdout-local or private-external evaluation is ready;
- the benchmark may now influence `benchmark_gate` or release policy.

### Planned artifact

This note preserves the interpretation boundary between:

- deterministic structural scoring over normalized candidate answers, and
- richer semantic evaluation or policy-bearing benchmark execution.

## Structural scoring findings

### 1. The benchmark now has its first executable scoring layer

The real-task benchmark stack is no longer limited to:

- corpus definition,
- schema validation,
- and non-gating corpus reporting.

It now also includes:

- single-case structural scoring via `score_real_task_case(...)`;
- batch scored reporting via `score_real_task_public_candidates(...)`.

Interpretation:

- the benchmark can now score normalized candidate answers against public gold
  contracts;
- this is an important transition from static artifact inventory to executable
  benchmark mechanics.

### 2. The scorer is intentionally deterministic and narrow

The scoring layer checks only manifest-defined structural properties:

- status / substatus,
- expected labels,
- required terms,
- forbidden claims,
- required next actions,
- evidence class,
- false-confidence veto behavior.

Interpretation:

- this is appropriate for a first executable slice;
- it is safer than prematurely introducing a general semantic evaluator;
- but it also means the current scorer is only as strong as the normalized
  answer object it receives.

### 3. The scorer preserves the benchmark’s safety invariant

The new scorer explicitly preserves:

- forbidden-claim detection;
- false-confidence veto checks;
- `inconclusive` output for malformed candidate objects.

Representative sanity check already demonstrated:

- safe candidate for `MF-03-hmc-helper-nonclaim-boundary` → `consistent`
- forbidden-claim candidate for the same case → `mismatch`
- `false_confidence_veto_clear` becomes `False`

Interpretation:

- the most important benchmark safety mechanic remains active in the first
  executable scoring layer.

### 4. The scored report remains explicitly non-gating

The batch scored report explicitly states that it is:

- a non-gating scored report,
- over normalized candidate answers,
- not semantic benchmark execution over free-form model outputs,
- not holdout-local or private-external evidence,
- not release-readiness evidence.

Interpretation:

- this is the correct boundary for the current maturity level;
- the benchmark has gained executable scoring without silent policy drift.

## Verification results

Focused tests:

- `tests/test_real_tasks_scoring.py`: passed
- `tests/test_real_tasks_scored_report.py`: passed

Adjacent regressions:

- `tests/test_real_tasks_manifest.py`: passed
- `tests/test_real_tasks_report.py`: passed
- `tests/test_schema_contracts.py`: passed

Representative scored batch sanity check:

- one safe candidate produced `consistent`
- one forbidden-claim candidate produced `mismatch`
- scored report surfaced:
  - mixed `consistent`/`mismatch` statuses,
  - explicit `false_confidence_veto_failures`,
  - missing public case IDs for unscored cases,
  - non-gating policy boundary text.

## Calibration interpretation

### What this executable scoring layer *does* justify

At this stage, the new scorer justifies the following claims:

1. the public benchmark can now be executed in a deterministic structural way;
2. the manifest gold contract is rich enough to support nontrivial executable
   checks on normalized candidate answers;
3. false-confidence veto behavior is preserved in executable scoring;
4. the benchmark can now support early scored calibration experiments over the
   public tier.

### What it still does **not** justify

At this stage, the scorer does **not** justify the following claims:

1. that structural scoring is a semantic evaluator for free-form benchmark
   answers;
2. that category metrics computed from this layer alone would reflect full model
   understanding;
3. that holdout or private-evaluation readiness has improved;
4. that benchmark policy or release coupling is justified.

## Main calibration uncertainties

1. **Literalism risk**
   - the scorer matches structural fields and normalized phrases;
   - it does not yet evaluate paraphrase quality or deeper semantic reasoning.

2. **Candidate-object dependency**
   - the current layer assumes answers are already normalized into a structured
     candidate object;
   - a later layer will need to decide how candidate objects are produced from
     free-form model outputs.

3. **Category thinness still matters**
   - even with executable scoring, some categories still have few public cases,
     limiting the stability of category-level aggregate interpretation.

4. **Holdout-local remains policy/scaffold only**
   - this scorer currently improves public-tier calibration only;
   - it does not yet support generalization claims.

5. **Negative/ambiguous cases are improved but still sparse**
   - the public set now includes `mismatch` and `inconclusive` cases;
   - but this is still a small seed, not a fully stress-tested failure surface.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the structural scorer as a valid first executable benchmark layer | Met | No scoring-boundary veto found | Structural scoring is still literal and candidate-object-dependent | Use it for bounded public-tier calibration and richer corpus shaping, not yet for semantic benchmark execution or policy | No semantic evaluator, no generalization evidence, no gate/readiness implication |

## Post-run red-team note

### Strongest alternative explanation

The structural scorer may look more useful than it really is because the current
public cases were hand-authored with explicit required phrases, forbidden
claims, and next actions. A later semantic evaluator might reveal that the
current scoring contract is still too brittle for realistic free-form outputs.

### What result would overturn confidence

Confidence in the current interpretation would weaken if:

- future scored calibration showed frequent false mismatches caused only by
  harmless paraphrase variation;
- structural scoring proved unable to support stable category metrics even on
  the current public set;
- future richer candidate extraction blurred the current clean veto behavior.

### Weakest part of the evidence

The weakest part of the current evidence is not correctness of the structural
scorer itself; it is the narrowness of what the structural scorer measures.

## Next hypotheses to test

1. **Structured-candidate adequacy hypothesis**
   - Normalized candidate-answer objects can support useful early category
     calibration before semantic scoring exists.

2. **Public negative-case sufficiency hypothesis**
   - The current enriched public status mix is sufficient for an initial scored
     calibration pass without immediate further corpus expansion.

3. **Semantic-gap hypothesis**
   - The next major limitation will come not from the scorer contract, but from
     how free-form model responses are normalized into candidate-answer objects.

4. **Holdout carry-forward hypothesis**
   - The current structural scorer can later be reused unchanged on holdout-local
     candidate objects once that tier becomes evaluable.

## Next justified action

The next justified action is not benchmark gating.

The next justified action is one of:

1. run a bounded scored calibration exercise over a curated set of normalized
   candidate answers for the current public cases, or
2. enrich the public corpus further only where the scorer reveals thin coverage
   or brittle literal matching.
