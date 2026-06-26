# MathDevMCP Holdout-Local Population Example

## Date

2026-06-19

## Purpose

This note demonstrates one **example local holdout population workflow** using
the holdout-local recipe and candidate inventory.

It is not a committed holdout case, not a scored result, and not holdout
execution evidence.

The goal is simply to show what a local developer or agent should record when
starting holdout-local population for one candidate family.

## Chosen candidate family

Chosen family:

- larger `latex-papers` chapter-neighborhood cases not yet represented in the
  public benchmark corpus.

Why this family is a strong example:

- it is clearly local-evaluation oriented rather than public-calibration
  oriented;
- it stress-tests longer-context retrieval/provenance behavior;
- it is meaningfully distinct from the current public `LP-01` and `LP-02`
  templates.

## Candidate source example

A representative local candidate source for this example workflow would be:

- a broader or adjacent chapter neighborhood in `../latex-papers/CIP_monograph/`
  beyond the current public benchmarked materials.

This note intentionally does **not** commit a populated local manifest entry or
claim that this candidate has already been evaluated.

## Apply the holdout-local recipe

### Step 1 — Choose the candidate artifact

Selected candidate type:

- larger `latex-papers` chapter-neighborhood retrieval/provenance task.

### Step 2 — Check disjointness against the public corpus

Closest public cases:

- `LP-01-analytical-validation-lgssm`
- `LP-02-basis-reconciliation-audit`

Disjointness rationale:

- `different_label_neighborhood`
  - the candidate is intentionally outside the current public chapter/label
    neighborhood used by `LP-01` and `LP-02`.
- `different_task_template`
  - the target is broader neighborhood retrieval/provenance stress rather than
    the exact analytical-validation or basis-reconciliation templates already in
    the public corpus.

This is enough to justify holdout-local status under the current policy.

### Step 3 — Classify the candidate structurally

Provisional local classification for this example:

- family: `retrieval_and_provenance`
- expected status: likely `consistent` or `unverified`, depending on the exact
  candidate and the evidence boundary of the local prompt
- source repo area: `latex-papers/CIP_monograph`
- holdout reason: broad chapter-neighborhood retrieval/provenance stress not
  already represented publicly

### Step 4 — Record the local holdout metadata

If this example were turned into a real local entry, the local record should at
minimum capture:

- source path or neighborhood
- public case(s) it is intentionally distinct from
- holdout reason
- disjointness axes
- intended category/family
- expected status
- forbidden stronger claims if the case is boundary-sensitive

### Step 5 — Optional local normalized candidate-answer expectation

For this example, a local normalized candidate-answer object may be helpful later
if the user wants to test retrieval/provenance scoring deterministically.

But that object should stay local unless a deliberate public-promotion decision
is made.

### Step 6 — Keep the populated example local

This example should remain:

- a workflow illustration,
- not a committed populated holdout case,
- not a scored holdout artifact.

## Example local-inventory sketch

If a developer wanted to record this example locally, a concise local entry might
look like:

```yaml
id: HOLDOUT-LATEX-NEIGHBORHOOD-001
family: retrieval_and_provenance
repo: latex-papers
holdout_reason: broader chapter-neighborhood retrieval stress not covered by LP-01/LP-02
disjointness_axes:
  - different_label_neighborhood
  - different_task_template
closest_public_cases:
  - LP-01-analytical-validation-lgssm
  - LP-02-basis-reconciliation-audit
status_intent: local_holdout_candidate_only
```

This note is only a sketch of what a local developer would maintain; it is not a
committed evaluated holdout case.

## Non-claim boundary

This example does **not** mean:

- a holdout-local case has been populated and scored;
- the benchmark now has holdout evidence;
- public-case overfitting risk has already been reduced in practice;
- the benchmark now supports generalization claims.

It only demonstrates how to begin holdout-local population without violating the
current holdout policy.

## Verification

This note is successful if a future developer or agent can read it and answer:

1. why this candidate family stays local rather than public;
2. which disjointness axes justify that decision;
3. what minimum local metadata should be recorded;
4. why this example is still population guidance rather than evaluation evidence.
