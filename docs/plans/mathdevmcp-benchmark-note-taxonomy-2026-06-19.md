# MathDevMCP Benchmark Note Taxonomy

## Date

2026-06-19

## Purpose

The benchmark note stack has grown enough that document role ambiguity is now a
real benchmark-governance problem.

This note defines a small taxonomy for benchmark-related notes so that future
updates know:

- which notes are governing source-of-truth artifacts,
- which notes are current-state synthesis artifacts,
- which notes are historical evidence snapshots,
- and which notes should remain frozen rather than being repeatedly rewritten to
  look current.

The goal is not to create bureaucracy. The goal is to reduce ambiguity about
where the current benchmark truth should live.

## Note classes

### 1. Governing source-of-truth

**Examples:**

- `docs/plans/mathdevmcp-real-tasks-benchmark-spec-2026-06-16.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `docs/plans/mathdevmcp-benchmark-acceptance-policy-proposal-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-driven-improvement-program-2026-06-19.md`

**Purpose:**

Defines the benchmark’s structure, scope, policy, and intended phase order.

**Update policy:**

- may be updated in place if they are still the governing policy document;
- changes should remain deliberate and should preserve explicit evidence
  boundaries.

**Claim boundary:**

These notes define policy, not measured benchmark state.

---

### 2. Current synthesis

**Examples:**

- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-current-state-assessment-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-acceptance-assessment-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-calibration-milestone-note-2026-06-19.md`

**Purpose:**

Summarizes the best current interpretation of the benchmark’s present state.

**Update policy:**

- this is the primary layer that may be updated to reflect the latest benchmark
  truth;
- if a later note supersedes the current interpretation, either update the
  current synthesis note or create a newer synthesis note that clearly grounds
  itself in the prior one.

**Claim boundary:**

These notes may state what the benchmark currently supports, but they must still
preserve explicit non-claims about benchmark completion, generalization, or
policy readiness.

---

### 3. Historical evidence snapshot

**Examples:**

- result notes
- structural calibration pass notes
- holdout population notes
- fixture/broadening notes
- bounded overnight result notes

Representative files include:

- `docs/plans/mathdevmcp-bounded-overnight-benchmark-run-result-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-calibration-result-note-2026-06-19.md`
- `docs/plans/mathdevmcp-public-candidate-fixture-coverage-note-2026-06-19.md`
- `docs/plans/mathdevmcp-holdout-local-broadened-population-note-2026-06-19.md`

**Purpose:**

Capture one bounded run, one bounded calibration pass, or one bounded benchmark
change as historical evidence.

**Update policy:**

- should generally be treated as frozen historical snapshots;
- do **not** rewrite them to make them “current” unless correcting a factual
  error introduced during that same snapshot;
- if later interpretation changes, create or update a **current synthesis** note
  instead.

**Claim boundary:**

These notes are evidence inputs for later synthesis. They are not the canonical
place to keep the latest benchmark state synchronized.

---

### 4. Strategic checkpoints

**Examples:**

- the benchmark checkpoint series
- pause/review checkpoint

Representative files:

- `docs/plans/mathdevmcp-benchmark-master-program-strategic-review-checkpoint-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-master-program-strategic-review-checkpoint-ii-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-master-program-strategic-review-checkpoint-iii-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-master-program-strategic-review-checkpoint-iv-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-pause-review-checkpoint-2026-06-19.md`

**Purpose:**

Record bounded strategic judgments at a point in the benchmark’s evolution.

**Update policy:**

- treat each checkpoint as a historical strategic snapshot;
- later checkpoints may supersede earlier strategic interpretation in practice,
  but the earlier checkpoint should not usually be rewritten into the later one;
- if practical supersession matters, record it in the current synthesis layer.

**Claim boundary:**

Strategic checkpoints are historically valuable because they show how the
benchmark’s governing judgment evolved.

---

### 5. Living execution memos

**Examples:**

This class is not yet central in the benchmark stack, but it exists elsewhere in
repo practice and may become relevant later if benchmark work starts using a
long-running operational memo pattern.

**Purpose:**

Maintain an explicitly current execution checkpoint for a live workstream.

**Update policy:**

- may be updated in place while the memo remains the active live execution
  record;
- should explicitly say when they supersede earlier execution memos.

**Claim boundary:**

These are execution-management artifacts, not benchmark acceptance or release
artifacts by themselves.

## Lightweight header convention

Future benchmark notes may add a lightweight header block like this:

```markdown
Role: current-synthesis | historical-snapshot | strategic-checkpoint | governing-source-of-truth | living-execution-memo
Current-state status: living | historical
Supersedes for current interpretation: <optional note paths>
Grounded in: <optional note paths>
```

### Guidance on use

- Do **not** retroactively stamp every historical note unless needed.
- Use this header first on new notes, or when a current synthesis note is being
  actively maintained.
- Historical notes may remain without the header if their role is already clear
  from title and content.

## Practical maintenance rule

The benchmark stack should follow this practical rule:

1. **Preserve history**
   - keep result/calibration/broadening/checkpoint notes as historical evidence.

2. **Centralize reinterpretation**
   - keep the latest benchmark state in the current synthesis layer.

3. **Do not rewrite old notes merely to make them current**
   - when the benchmark state changes, prefer updating the current synthesis
     notes or writing a newer synthesis note.

4. **Use governing notes for policy, not current measured state**
   - spec/master-policy notes define structure and criteria, while synthesis
     notes report current reality.

## What this taxonomy should prevent

This taxonomy should help prevent:

- stale current-state notes competing with each other;
- historical evidence notes being silently rewritten into present-tense truth;
- confusion about which note should be updated after a benchmark run or
  calibration pass;
- overclaiming from old snapshots that were never intended to remain current.

## Non-claim boundary

This taxonomy does **not** by itself make the benchmark more complete or more
accepted.

It only reduces ambiguity about how benchmark notes should be maintained and
interpreted.
