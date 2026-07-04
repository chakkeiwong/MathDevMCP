# MathDevMCP Holdout-Local Candidate Inventory

## Date

2026-06-18

## Purpose

This note lists a small set of **example holdout-local candidate families** that
are strong next population targets.

It is an inventory recommendation, not a committed scored case set.

The point is to make local holdout population easier while preserving the rule
that holdout-local is an evaluation-separation mechanism rather than an
additional public corpus.

## Candidate inventory

### 1. Larger `latex-papers` chapter-neighborhood cases

**Candidate family:** broader chapter neighborhoods or adjacent sections around
already-public mathematical topics.

**Why it should remain holdout-local**

- different label/chapter neighborhood than the current public `LP-01` and
  `LP-02` cases;
- stronger long-context retrieval/provenance stress;
- likely more vulnerable to public-template leakage if committed too early.

**Disjointness axes**

- `different_label_neighborhood`
- `different_task_template`

**Why not public yet**

These cases would be valuable for generalization checks, but they should not be
turned into another easy public retrieval template before holdout evaluation is
established.

---

### 2. Deeper `dsge_hmc` result-note families adjacent to current public blockers

**Candidate family:** result notes and audits adjacent to the current public
`DH-05`, `DH-06`, and `DH-07` failure-style cases, but from different workstream
subphases or blocker families.

**Why it should remain holdout-local**

- would exercise similar evidence-boundary discipline while changing the exact
  blocker pattern;
- useful for testing whether the benchmark is learning a public template or a
  real blocker-preservation behavior.

**Disjointness axes**

- `different_source_family`
- `different_author_exposure_status`

**Why not public yet**

Too many closely related public blocker notes would make the public set easier
to tune against without proving broader generalization.

---

### 3. `MacroFinance` result-note families not yet represented publicly

**Candidate family:** additional result notes that preserve strong engineering,
convergence, or authorization boundaries different from the current public
MacroFinance examples.

**Why it should remain holdout-local**

- helps balance the corpus beyond the current public MacroFinance cases;
- gives a local place to test new evidence-boundary distinctions without
  immediately expanding the public surface.

**Disjointness axes**

- `different_source_family`
- `different_task_template`

**Why not public yet**

The current public MacroFinance set is still small and targeted. Additional
families are valuable, but should first help local evaluation rather than public
calibration expansion.

---

### 4. BayesFilter-adjacent local materials that should stay off the public surface

**Candidate family:** BayesFilter-related local notes, inventories, or execution
artifacts that are structurally similar to public migration/readiness cases but
are better kept out of the public benchmark corpus.

**Why it should remain holdout-local**

- BayesFilter-adjacent work is especially prone to stale-path, local-runtime,
  and author-exposure issues;
- useful for evaluating whether the benchmark generalizes to nearby but not
  identical migration/readiness language.

**Disjointness axes**

- `different_source_family`
- `different_author_exposure_status`

**Why not public yet**

These are good stress tests for local generalization but are too easy to blur
into private/external or execution-specific policy if promoted too early.

---

### 5. Public-template adversarial variants kept local

**Candidate family:** carefully chosen variants of public case families that
change the effective benchmark template enough to test leakage, but are still
recognizably related.

**Why it should remain holdout-local**

- directly tests whether improvements are just public-template memorization;
- useful as a local challenge set before expanding the public corpus.

**Disjointness axes**

- `different_task_template`
- `different_author_exposure_status`

**Why not public yet**

By design these are the closest cases to public templates, so they are the most
important to keep off the public surface while the benchmark is still young.

## How to use this inventory

For each candidate family:

1. choose one concrete local artifact;
2. verify at least one disjointness axis;
3. record it in a local holdout manifest or local note;
4. keep it local unless a deliberate public-promotion decision is made.

## Non-claim boundary

This inventory does **not** mean these cases have been populated, scored, or
used in evaluation yet.

It only means they are good next candidates for local holdout population.
