# MathDevMCP Holdout-Local Population Recipe

## Date

2026-06-18

## Purpose

This note gives a bounded local workflow for beginning **holdout-local**
population without collapsing the holdout tier into another public benchmark
surface.

It is a recipe, not a result note.

The goal is to help a local developer or agent decide:

- which candidate artifacts belong in `holdout_local`,
- why they are holdout-local rather than public,
- what minimal information to record for a local holdout case,
- and what must remain local unless a deliberate public-promotion decision is
  made.

## Prerequisites

Before using this recipe, the following should already exist:

- the public benchmark manifest;
- the holdout-local policy scaffold:
  - `docs/plans/mathdevmcp-holdout-local-corpus-subplan-2026-06-17.md`
  - `benchmarks/real_tasks/holdout_local/README.md`
  - `benchmarks/real_tasks/manifests/holdout_local_cases.template.json`
- the public candidate-answer fixture shape:
  - `benchmarks/real_tasks/fixtures/public_candidate_answers.json`

This recipe assumes that holdout-local remains a local evaluation tier and that
no populated holdout data is committed by default.

## Step-by-step local population workflow

### Step 1 — Choose a candidate source artifact

Pick a candidate artifact from a target repo area that is **not** already part
of the public benchmark surface.

Good candidate source types:

- a larger chapter neighborhood not yet represented publicly;
- a result note that preserves a blocker or boundary different from the public
  set;
- a task template that is meaningfully different from the current public cases;
- a BayesFilter-adjacent local source that should remain off the public surface.

### Step 2 — Check disjointness against the public corpus

Before calling the candidate holdout-local, verify that it differs from the
public set by at least one required disjointness axis.

Required checklist:

- `different_source_family`
- `different_label_neighborhood`
- `different_task_template`
- `different_author_exposure_status`

At least one axis must be defensible.

If the candidate differs only by filename or minor path placement while using
essentially the same benchmark template, it should **not** be treated as a
meaningful holdout-local case.

### Step 3 — Classify the candidate structurally

Record the candidate’s:

- benchmark category/family,
- expected status,
- source repo area,
- brief description of the benchmarked judgment,
- holdout reason,
- chosen disjointness axis or axes.

This is a classification step, not an evaluation result.

### Step 4 — Record the local holdout entry

Locally record enough structure so the case can later be scored or normalized.

A local developer may begin by initializing a private local scaffold from the
committed template using the holdout-local helper, then editing that local file
rather than creating ad hoc JSON from scratch.

Minimum suggested local fields:

- `id`
- `family`
- `repo`
- `task_type`
- `difficulty`
- `document_roots`
- `document_files`
- `code_roots`
- `code_files`
- `prompt`
- `gold.expected_status`
- `gold.required_terms`
- `gold.forbidden_claims`
- `gold.required_next_actions`
- `holdout_reason`
- `disjointness_axes`

The committed template file provides a scaffold for this shape.

### Step 5 — Optionally draft a local normalized candidate-answer expectation

If it helps later scoring or review, locally draft a normalized candidate-answer
object in the same general shape used by the public fixture set.

This is optional at population time.

The purpose is only to reduce future local ambiguity, not to create a new
committed benchmark artifact.

### Step 6 — Keep the populated artifact local

Unless there is a deliberate promotion decision, the populated holdout-local
entry should stay local.

Do not commit it by default.

If repeated iteration against the same holdout candidate becomes necessary, the
case should be reconsidered as either:

- a public calibration candidate, or
- a candidate to be replaced by a fresher holdout example.

## Disjointness checklist

Use this checklist explicitly for every holdout-local candidate.

| Axis | Question |
|---|---|
| `different_source_family` | Is the case drawn from a different repo area or document family than the closest public case? |
| `different_label_neighborhood` | Does it depend on a different label/chapter neighborhood rather than a renamed version of a public context? |
| `different_task_template` | Does it require a different kind of judgment than the nearest public case? |
| `different_author_exposure_status` | Has this case been materially less exposed during public benchmark authoring/tuning? |

A candidate should not be accepted into local holdout inventory without at least
one justified positive answer.

## Non-claim boundary

Adding a candidate to a local holdout inventory does **not** mean:

- the case has been evaluated,
- the case has been scored,
- the public benchmark now generalizes,
- overfitting risk has been reduced in practice,
- benchmark maturity has increased beyond public calibration.

Population is not evaluation.

## What to record in a local holdout case

A concise local note or local JSON/YAML entry should record:

- where the case came from;
- why it is holdout-local;
- what public case it is intentionally *not* equivalent to;
- what benchmark category it belongs to;
- what stronger claim it should guard against.

This is the minimum record needed to make later holdout evaluation interpretable.

## What not to commit

Do not commit by default:

- populated local holdout manifests,
- scored holdout outputs,
- local semantic candidate-answer drafts,
- local-only result notes derived from holdout execution,
- anything that would effectively turn the holdout set into a public tuning
  surface.

## Relationship to public candidate fixtures

The committed public candidate-answer fixtures are calibration fixtures for the
public tier.

They are useful as a shape reference, but they should **not** be copied blindly
into the holdout tier without checking disjointness. If the local holdout entry
reuses the same effective template, it is no longer functioning as a meaningful
holdout.

## Verification

This recipe is considered usable if a local developer can read it and answer:

1. how to choose a holdout-local candidate;
2. how to justify disjointness;
3. what minimum metadata to record;
4. what not to commit;
5. why local population is still not the same as holdout evaluation.
