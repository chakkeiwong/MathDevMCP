# MathDevMCP Real-Task Benchmark Master Program Audit

## Audit stance

This audit treats the following as another developer’s plan set:

- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `docs/plans/mathdevmcp-benchmark-category-scoring-subplan-2026-06-17.md`

The goal is to tighten phase order, reduce scope ambiguity, and prevent proxy
metrics or benchmark growth from being mistaken for product or release
readiness.

## Overall assessment

The plan set is justified and materially stronger than the current ad hoc state.
It correctly makes false certification the top safety concern, keeps benchmark
integration non-gating through the middle phases, and distinguishes public,
holdout-local, and private/external corpora.

The main remaining risks are:

1. the category-scoring subplan could still be read as too metric-centric unless
   the master program’s safety invariant stays dominant;
2. Phase 3 and Phase 4 could sprawl if BayesFilter/private-corpus acquisition is
   treated as an immediate implementation obligation rather than a managed
   dependency;
3. Phase 6 reporting must be careful not to imply benchmark maturity before
   pilot calibration has happened.

Overall verdict at this stage: **proceed with constraints**.

## Required execution constraints

### Keep gate integration late

Do not let any implementation prompted by these plan docs move benchmark results
into `benchmark_gate`, release policy, or MCP/CLI workflow defaults before the
program reaches at least the pilot-calibration phase.

### Preserve hard-veto visibility

Any future report implementation must surface false-certification and
forbidden-claim failures as first-class fields. They must not be hidden in a
single global average.

### Treat holdout/private design as dependency-managed

The plans should not assume that BayesFilter external material, private corpus
material, or all holdout cases are immediately available. Those phases should
remain valid even when corpus acquisition is partial.

### Do not equate public corpus growth with readiness

Adding more public cases is valuable, but it is still only corpus growth.
Program progress should not be narrated as product readiness until reporting,
pilot calibration, and stability work are complete.

### Reporting must remain explicitly non-gating

Phase 6 should produce inspection/reporting artifacts only. A later workflow
surface should not silently turn those reports into required CI or release
checks.

## Missing details and fixes

1. The master program should explicitly say that phases may produce partial
   outputs without authorizing downstream policy claims. This is mostly present,
   but should remain visible in implementation and review.

2. The category-scoring subplan should continue to avoid the phrase “global
   benchmark score” unless it immediately explains that such a score is only
   secondary.

3. The master program should keep Phase 8 workflow integration separate from
   Phase 9 gate-candidate selection. Combining them would blur operational
   usability with policy authority.

4. Any later bounded review request should ask the reviewer not to widen the
   scope beyond one coherent next slice unless required for correctness.

## External bounded review disposition

A bounded second review returned **AGREE WITH CONSTRAINTS**. The review agreed
with the overall direction and anti-overclaiming stance, but identified four
issues that materially deserved tightening.

### Accepted and incorporated

1. **Phase 5 / Phase 4 coupling was too strong**
   - Accepted. The master program should not let incomplete private/external
     policy block public manifest/schema hardening.
   - Action: tighten Phase 5 language so public hardening can proceed while
     private/external policy remains dependency-managed.

2. **Public-set calibration needed a stronger non-readiness boundary**
   - Accepted. Public calibration results should be explicitly labeled as
     development/calibration evidence only.
   - Action: tighten Phase 7 language and the holdout-local phase so public-set
     improvements are not overinterpreted.

3. **Holdout realism needed a more operational definition**
   - Accepted. The master plan should define what holdout separation means at a
     minimum (e.g. task-template/label-neighborhood/family separation).
   - Action: add explicit holdout-disjointness language in Phase 3.

4. **Report ordering needed stronger constraints**
   - Accepted. Non-gating reports should present hard-veto and evidence-boundary
     failures before convenience summaries.
   - Action: tighten Phase 6 and the scoring subplan accordingly.

### Not adopted as a scope expansion

The review suggested stronger fences around private/external fallback behavior.
That concern was accepted in substance, but it did not require creating a new
phase. Instead, the existing Phase 4 language should be tightened so missing
external access produces a policy artifact rather than blocking unrelated public
progress.

### Post-review assessment

The review did not reveal a need to change the overall phase order. It did
reveal a need to reduce dependency coupling, formalize holdout separation, and
make calibration/report boundaries more explicit. Those are tightening edits,
not a program rewrite.

## Phase-by-phase audit

### Phase 0 — Program framing and governance

Proceed. This phase is necessary and appropriately conservative.

### Phase 1 — Category contracts and scoring rules

Proceed. This is the most important planning phase after governance. The main
constraint is that category metrics must remain subordinate to the safety
invariant.

### Phase 2 — Public corpus buildout

Proceed, but require category-balance checks. It is easy to overpopulate the
public suite with whichever repo has the easiest extractable cases.

### Phase 3 — Holdout-local corpus design

Proceed, but keep the objective bounded: define policy and candidate inventory
first, not full implementation of all holdout ingestion.

### Phase 4 — Private/external corpus design

Proceed cautiously. This phase should focus on representational policy,
redaction, and manifest expectations, not immediate full private corpus
execution.

### Phase 5 — Schema, loader, and validator hardening

Proceed. This phase is already underway and is a valid prerequisite for later
reporting.

### Phase 6 — Non-gating reporting

Proceed with an explicit warning: reports at this stage are diagnostic artifacts
for benchmark development, not operational readiness instruments.

### Phase 7 — Pilot execution and calibration

Proceed. This phase is essential and should be treated as a stop gate before any
serious workflow or policy integration.

### Phase 8 — Workflow integration

Proceed only after pilot calibration. This phase should be non-gating and should
collect operational experience rather than confer authority.

### Phase 9 — Gate-candidate selection

Proceed only if workflow integration shows stable and interpretable benchmark
behavior. This phase is correctly placed late.

### Phase 10 — Release-policy integration

Proceed only if Phase 9 produces a narrow, stable, and clearly justified subset.
The current plans are correct to treat this as optional and late.

## External bounded review request shape

When requesting the bounded external review, ask the reviewer to:

- review only the master program and category-scoring subplan;
- act as a skeptical second developer;
- focus on scope control, evidence-boundary honesty, hidden dependencies,
  premature gate coupling, holdout/private realism, and whether the phase order
  is minimal and safe;
- avoid broadening the plan unless necessary for correctness;
- return a constrained verdict such as `AGREE`, `AGREE WITH CONSTRAINTS`, or
  `REVISE`.

## Audit conclusion

Proceed with the plan set after preserving the constraints above.

The plans are strong enough to guide the next planning and implementation slices
because they:

- keep safety ahead of aggregate metrics;
- keep gate integration late;
- keep corpus-tier realism explicit;
- make each phase produce artifacts the next phase actually needs.
