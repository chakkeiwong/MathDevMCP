# MathDevMCP Benchmark Acceptance Policy Proposal

## Date

2026-06-19

## Scope

This document proposes an objective benchmark acceptance policy for the current
MathDevMCP real-task benchmark program.

It is grounded in the current benchmark architecture and current maturity
artifacts, including:

- `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`
- `docs/plans/mathdevmcp-benchmark-category-scoring-subplan-2026-06-17.md`
- `docs/mathdevmcp-release-policy.md`
- `docs/mathdevmcp-support-matrix.md`
- current public and local scored-tier summaries

This policy is a **proposal**. It defines objective criteria for deciding when
the benchmark is good enough for different internal roles. It does **not** claim
that the current benchmark has already reached every higher role.

## Policy design principle

The benchmark should not be declared “good” because it feels mature.

It should be judged by objective acceptance criteria based on:

1. hard-veto safety errors,
2. missed-problem / abstention errors,
3. coverage requirements,
4. stability requirements,
5. and the claimed use tier.

The policy therefore mirrors the repo’s release-profile style:

- a benchmark use tier is only accepted when the required evidence for that tier
  is present;
- missing optional evidence may create caveats rather than blockers;
- stronger claims require stronger evidence tiers.

## Acceptance tiers

### Tier A — `calibration_only`

This tier means the benchmark is acceptable for:

- internal calibration,
- bounded regression tracking,
- artifact-level evaluation design,
- non-gating benchmark reports.

It does **not** mean:

- holdout-backed generalization evidence,
- workflow integration readiness,
- gate or release policy readiness.

### Tier B — `internal_accepted_with_caveats`

This tier means the benchmark is acceptable for stronger internal decision
support, but still with explicitly recorded caveats.

It may support:

- stronger internal prioritization,
- holdout-informed internal comparisons,
- internal process decisions about benchmark direction.

It still does **not** support:

- gate coupling,
- release-policy integration,
- public or scientific claims.

### Tier C — `internal_accepted`

This tier means the benchmark is broad and stable enough for stronger internal
non-public decision support with limited caveats.

This tier is **not yet justified** by the current benchmark state, but is kept
here so the policy is complete.

### Tier D — `policy_ready_candidate`

This tier means the benchmark is a candidate for later workflow/gate/release
integration review.

This tier requires an explicit later program phase and is **not** yet justified
by the current benchmark state.

## Error-type framing

### Type I benchmark errors

Type I errors are the dangerous false positives:

- false certification,
- forbidden stronger claims,
- evidence-boundary promotion,
- treating public-only or local-only evidence as stronger than it is.

These are the benchmark’s highest-risk error class.

### Type II benchmark errors

Type II errors are missed real problems:

- missing a documented mismatch,
- failing to abstain when the evidence is insufficient,
- missing required terms or required boundaries,
- missing a real blocker.

These matter, but they are secondary to uncontrolled Type I safety failures.

## Objective acceptance criteria

### 1. Hard-veto safety gate

These are non-compensatory.

A benchmark tier is **not accepted** for a given role if any of the following
conditions fail within the evidence scope claimed by that tier:

- false-confidence-veto failures exceed the allowed threshold;
- forbidden-claim violations exceed the allowed threshold;
- evidence-boundary promotions exceed the allowed threshold.

#### Proposed thresholds

For `calibration_only`:
- false-confidence-veto failure rate must be **low enough to be visible and
  bounded**, not silently washed out;
- explicit seeded false-confidence fixtures should not be silently ignored.

For `internal_accepted_with_caveats` and above:
- explicit seeded false-confidence cases should have **zero tolerated silent
  acceptance**;
- any remaining failures must be explicitly surfaced as blockers or caveats.

### 2. Detection and abstention gate

A benchmark tier is not strong enough for broader internal interpretation unless
it can also surface real problems.

Relevant measurable criteria:

- mismatch recall,
- abstention recall,
- required-term / required-boundary recall,
- classification accuracy across expected statuses.

#### Proposed thresholds

For `calibration_only`:
- may be incomplete and still acceptable if the benchmark remains clearly
  labeled developmental.

For `internal_accepted_with_caveats`:
- should have thresholded internal targets per category, not yet as release
  gate numbers.

At current maturity, these threshold targets should be treated as **tracked
metrics**, not pass/fail gate semantics.

### 3. Coverage gate

A benchmark is not “good” just because its current cases score well. It must
also be broad enough for its intended role.

Relevant measurable criteria:

- public case count
- scored public case count
- holdout case count
- scored holdout case count
- family coverage
- status coverage
- local/public tier coverage balance

#### Coverage minimums by tier

For `calibration_only`, require at least:

- public and holdout tiers both exist;
- every major public benchmark family represented at least once in the public
  corpus;
- public status coverage includes:
  - `consistent`
  - `unverified`
  - `mismatch`
  - `inconclusive`
- holdout tier contains more than one family and more than one judgment shape;
- the benchmark preserves explicit public vs holdout distinction.

For `internal_accepted_with_caveats`, add:

- public scored coverage is near complete or complete;
- holdout scored coverage is complete for the current holdout seed;
- holdout breadth is large enough that representativeness concerns are reduced
  from dominant blocker to caveat.

### 4. Stability gate

A benchmark is not acceptable for a stronger tier unless its key artifacts are
stable enough to rerun without ambiguity.

Relevant measurable criteria:

- manifest validates cleanly;
- scored reports rerun reproducibly;
- committed tests pass;
- local-only workflows remain clearly local-only;
- key calibration/dashboard notes are updated to match the current artifact
  state.

## Acceptance status vocabulary

Mirror the repo’s release-policy style.

### `not_accepted`

The benchmark does not meet the requirements for the proposed tier.

### `accepted_with_caveats`

The benchmark meets the minimum role requirements, but important weaknesses are
still present and must be explicitly named.

### `accepted`

The benchmark meets the role requirements without material remaining caveats for
that role.

## Current benchmark assessment against this policy

### Tier A — `calibration_only`

**Likely status:** `accepted`

Reason:

- public benchmark exists and is validated;
- public scored tier exists and is near fully covered (`11/12`);
- holdout-local tier exists, is populated, and is scoreable;
- public and local tiers are explicitly separated;
- calibration and strategic checkpoint notes repeatedly preserve non-claim
  boundaries;
- no workflow/gate/release coupling is implied.

### Tier B — `internal_accepted_with_caveats`

**Likely status:** `accepted_with_caveats`

Reason:

Strengths:
- public and local tiers are both structurally scoreable;
- both tiers now show at least some mismatch/veto-shaped behavior;
- local holdout seed is multi-family and fully scored relative to itself.

Caveats:
- holdout representativeness remains the dominant uncertainty;
- public-vs-local family breadth remains asymmetric;
- structural scoring is still the main evaluation layer;
- current calibration notes explicitly avoid stronger generalization claims.

This means the benchmark is useful for stronger internal reasoning than simple
calibration-only use, but still not yet strong enough for policy-bearing use.

### Tier C — `internal_accepted`

**Likely status:** `not_accepted`

Reason:

- holdout representativeness remains unresolved;
- the local tier is still small;
- current strategic checkpoints still recommend pause/review and explicitly say
  the next move should be chosen by representativeness value rather than assumed
  maturity.

### Tier D — `policy_ready_candidate`

**Likely status:** `not_accepted`

Reason:

- workflow integration has not begun;
- gate-candidate selection has not begun;
- release-policy integration has not begun;
- multiple notes explicitly reject current policy/gate promotion.

## Decision table

| Tier | Current likely status | Why |
|---|---|---|
| `calibration_only` | `accepted` | Public and local structural benchmark surfaces are real, validated, and usable for bounded internal calibration |
| `internal_accepted_with_caveats` | `accepted_with_caveats` | Cross-tier comparison is meaningful enough for stronger internal reasoning, but holdout representativeness remains the dominant caveat |
| `internal_accepted` | `not_accepted` | Holdout breadth and interpretive maturity are still too limited |
| `policy_ready_candidate` | `not_accepted` | Workflow, gate, and release-policy phases remain explicitly incomplete |

## What this policy does **not** do

This policy does **not** silently promote the current benchmark into a gate.

It only defines the objective criteria by which that promotion could later be
judged.

## Non-claim boundary

This policy proposal does **not** mean the benchmark is complete.

It means the benchmark can now be judged against explicit role-based criteria
rather than by intuition alone.
