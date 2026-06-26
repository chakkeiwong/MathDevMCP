# MathDevMCP Bounded Overnight Benchmark Run Plan

## Date

2026-06-19

## Purpose

This plan defines a **bounded overnight evidence-collection run** for the
current benchmark program.

It is not a plan to complete the remaining master-program phases overnight.

Its purpose is to:

- rerun the existing public structural benchmark surfaces;
- rerun the existing local holdout scoring surfaces **only if** the required
  local artifacts already exist;
- capture a bounded evidence note describing what was run, what was blocked,
  and what still cannot be concluded.

## Governing artifacts

This overnight plan is constrained by:

- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-status-dashboard-2026-06-19.md`
- `docs/plans/mathdevmcp-benchmark-master-program-strategic-review-checkpoint-ii-2026-06-19.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-public-pilot-calibration-note-2026-06-17.md`
- `docs/plans/mathdevmcp-holdout-informed-structural-calibration-note-2026-06-19.md`

## Evidence contract

### Question

What do the currently implemented public and local holdout benchmark surfaces
say when rerun together under a bounded unattended execution, and what remains
blocked or out of scope afterward?

### Exact baseline / comparator

The baseline is the current committed benchmark artifact stack plus the current
local-only holdout artifacts already present at runtime.

This run does **not** compare against a previous overnight run or attempt to
prove trend improvement.

### Primary criterion

The primary criterion is that the overnight run:

- executes only already-implemented public and local surfaces,
- preserves all current non-claim boundaries,
- and emits a bounded result note instead of only raw command output.

### Veto diagnostics

The run is considered blocked, downgraded, or non-promotable if any of the
following occur:

- required local holdout artifacts are missing;
- false-confidence or forbidden-claim failures are surfaced by the structural
  scoring layers;
- current summary artifacts disagree materially with runtime outputs;
- the run drifts into workflow/gate/release-style interpretation.

### Explanatory-only diagnostics

The following are descriptive only:

- case counts,
- by-family summaries,
- by-status summaries,
- holdout coverage counts,
- fixture coverage counts.

### What will not be concluded

This run will **not** conclude that:

- the benchmark is complete,
- the benchmark is generalization-ready,
- holdout-backed calibration is mature,
- any gate or release policy is justified,
- any semantic evaluator is complete.

## Allowed overnight work

### Public tier

Allowed:

- public manifest load/validation
- public non-gating report generation
- public structural scored-report generation over committed candidate fixtures

### Local holdout tier

Allowed only if the artifacts already exist:

- `.local/mathdevmcp/holdout_local_cases.json`
- `.local/mathdevmcp/holdout_local_candidate_answers.json`

If they exist, allowed work is:

- local holdout discovery/initialization checks as needed,
- local holdout scored report over the existing local candidate fixtures

### Output artifact

Required:

- write `docs/plans/mathdevmcp-bounded-overnight-benchmark-run-result-2026-06-19.md`

## Explicitly out of scope

The overnight run must **not**:

- invent new public cases,
- invent new holdout-local cases,
- execute private/external corpora,
- perform workflow integration,
- perform gate-candidate selection,
- perform release-policy integration,
- claim benchmark completion,
- claim holdout-backed generalization.

## Stop / downgrade conditions

### 1. Missing local holdout artifacts

If either local holdout artifact is absent:

- `.local/mathdevmcp/holdout_local_cases.json`
- `.local/mathdevmcp/holdout_local_candidate_answers.json`

then the overnight run must still complete the public side, but record the local
holdout step as blocked/skipped and stop short of holdout-informed
interpretation.

### 2. Structural veto failures

If any false-confidence or forbidden-claim failures are surfaced by the scoring
layers, the result note must record them prominently and must not smooth them
into aggregate success language.

### 3. Artifact inconsistency

If runtime outputs materially disagree with the current dashboard or calibration
notes, the run must record the discrepancy and stop short of stronger
interpretation.

### 4. Scope drift

If the run would require changing benchmark artifacts or widening workflow
surfaces to continue, it must stop and record that the remaining work is still
policy- or coverage-dependent.

## Execution steps

### Step 1 — public manifest and public report

Run the current public surfaces:

```bash
python - <<'PY'
from pathlib import Path
from mathdevmcp.real_tasks_manifest import load_real_task_public_manifest, validate_real_task_public_manifest
from mathdevmcp.real_tasks_report import real_task_public_report
root = Path('/home/chakwong/python/MathDevMCP')
print(load_real_task_public_manifest(root))
print(validate_real_task_public_manifest(root))
print(real_task_public_report(root))
PY
```

### Step 2 — public structural scored report over committed candidate fixtures

```bash
python - <<'PY'
import json
from pathlib import Path
from mathdevmcp.real_tasks_scored_report import score_real_task_public_candidates
root = Path('/home/chakwong/python/MathDevMCP')
payload = json.loads((root / 'benchmarks/real_tasks/fixtures/public_candidate_answers.json').read_text())
print(score_real_task_public_candidates([fixture['candidate'] for fixture in payload['fixtures']], root=root))
PY
```

### Step 3 — local holdout scored report if local artifacts already exist

```bash
python - <<'PY'
from pathlib import Path
from mathdevmcp.real_tasks_holdout_local_scoring import score_local_holdout_candidate_fixtures
root = Path('/home/chakwong/python/MathDevMCP')
print(score_local_holdout_candidate_fixtures(root=root))
PY
```

If local artifacts are absent, the result should be recorded as expected
`inconclusive`, not as benchmark failure.

### Step 4 — test verification

```bash
pytest -q \
  tests/test_real_tasks_manifest.py \
  tests/test_real_tasks_report.py \
  tests/test_real_tasks_scoring.py \
  tests/test_real_tasks_scored_report.py \
  tests/test_real_tasks_answer_normalization.py \
  tests/test_real_tasks_candidate_fixtures.py \
  tests/test_real_tasks_holdout_local.py \
  tests/test_real_tasks_holdout_local_scoring.py \
  tests/test_schema_contracts.py
```

## Required result note contents

The result note should include:

- the exact question answered;
- exact commands run;
- public summary outputs;
- local holdout summary outputs, or explicit blocked/skipped explanation;
- veto diagnostics;
- what remains blocked or thin;
- what will not be concluded;
- next justified action.

## Verification

This plan is acceptable only if:

- it stays limited to already-existing executable surfaces;
- it contains explicit stop conditions;
- it requires a bounded result note;
- it does not attempt to finish workflow/gate/release phases overnight.
