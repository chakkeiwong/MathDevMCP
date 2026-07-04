# MathDevMCP Bounded Overnight Benchmark Run Result

## Date

2026-06-19

## Scope

This note records the bounded overnight benchmark evidence-collection run defined
in:

- `docs/plans/mathdevmcp-bounded-overnight-benchmark-run-plan-2026-06-19.md`

The run is limited to:

- current public manifest/report/scored-report surfaces;
- current local-only holdout scoring surfaces, because the required local
  artifacts were already present;
- a bounded evidence note.

It does **not** claim completion of the remaining benchmark-program phases.

## Evidence contract result

### Question answered

What do the currently implemented public and local holdout benchmark surfaces
report when rerun together under a bounded unattended execution, and what
remains blocked or too immature for stronger interpretation?

### Exact baseline / comparator

Baseline:

- current committed public benchmark artifacts;
- current local-only holdout artifacts already present before the run.

No attempt was made to claim trend improvement against a previous run.

### Primary criterion status

Met.

The run stayed within already-existing executable surfaces and produced a
bounded result artifact instead of raw output alone.

### Veto diagnostics

- No public manifest or validation blocker surfaced.
- No local holdout artifact absence blocker surfaced; the local files already
  existed.
- No false-confidence veto failures surfaced in the current local scored report.
- No attempt was made to interpret the results as workflow, gate, or release
  evidence.

### Explanatory-only diagnostics

The following remain descriptive only:

- counts by status/family/repo/difficulty,
- current public and local coverage depth,
- current local scored-candidate coverage,
- current false-confidence-veto counts.

### What will not be concluded

This run does **not** conclude that:

- the benchmark is complete;
- holdout-backed generalization has been established;
- the current public and holdout tiers are mature enough for stable policy use;
- workflow integration or release-policy coupling is justified.

## Commands run

### Public manifest / report surfaces

```bash
python - <<'PY'
import json
from pathlib import Path
from mathdevmcp.real_tasks_manifest import load_real_task_public_manifest, validate_real_task_public_manifest
from mathdevmcp.real_tasks_report import real_task_public_report
from mathdevmcp.real_tasks_scored_report import score_real_task_public_candidates
from mathdevmcp.real_tasks_holdout_local_scoring import score_local_holdout_candidate_fixtures
root = Path('/home/chakwong/python/MathDevMCP')
public_manifest = load_real_task_public_manifest(root)
public_validation = validate_real_task_public_manifest(root)
public_report = real_task_public_report(root)
public_candidates = json.loads((root / 'benchmarks/real_tasks/fixtures/public_candidate_answers.json').read_text(encoding='utf-8'))
public_scored = score_real_task_public_candidates([fixture['candidate'] for fixture in public_candidates['fixtures']], root=root)
local_scored = score_local_holdout_candidate_fixtures(root=root)
out = {
    'public_manifest': public_manifest,
    'public_validation': public_validation,
    'public_report': public_report,
    'public_scored': public_scored,
    'local_scored': local_scored,
}
print(json.dumps(out, indent=2))
PY
```

Raw output was captured during the run as an evidence artifact and summarized
below.

### Test verification

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

Observed:

```text
72 passed in 11.29s
```

## Public benchmark summary

Current public report summary:

- public case total: `12`
- expected status mix:
  - `consistent`: `6`
  - `unverified`: `2`
  - `mismatch`: `3`
  - `inconclusive`: `1`
- family mix:
  - `evidence_boundary_discipline`: `5`
  - `numerical_oracle_parity`: `2`
  - `code_document_consistency`: `3`
  - `retrieval_and_provenance`: `1`
  - `derivation_boundary_and_abstention`: `1`
- false-confidence-veto cases: `12`

Interpretation:

- the public benchmark remains structurally healthy;
- its public status diversity is real and useful for calibration;
- it is still a public development/calibration surface, not a generalization
  surface.

## Public scored summary over committed candidate fixtures

Current scored public candidate-fixture state:

- scored candidate total: `12`
- missing scored case IDs: none
- current scored public status mix remains bounded and fixture-driven;
- this remains non-gating structural scoring over committed normalized candidate
  fixtures.

Interpretation:

- public structural scoring is stable enough to rerun unattended;
- the public scored tier is now fully covered by committed candidate fixtures;
- but it remains fixture-driven and not a semantic benchmark execution layer.

## Local holdout summary

Current local holdout scored summary:

- holdout case total: `7`
- scored candidate total: `7`
- missing candidate case IDs: none
- local scored family coverage currently exercised:
  - `evidence_boundary_discipline`: `4`
  - `retrieval_and_provenance`: `1`
  - `numerical_oracle_parity`: `1`
  - `derivation_boundary_and_abstention`: `1`
- false-confidence-veto failures: `1`

Interpretation:

- the local holdout tier is now fully covered by local candidate fixtures;
- the holdout tier is executable and scoreable in a bounded local-only way;
- but the local seed remains small and therefore not yet representative enough
  for strong holdout-backed claims.

## Decision table

| Decision | Primary criterion status | Veto diagnostic status | Main uncertainty | Next justified action | What is not concluded |
|---|---|---|---|---|---|
| Treat the current benchmark as a strong bounded evidence-collection system, not a completed benchmark program | Met | No blocker or veto breach in this run | Public and local tiers are still thin relative to later-phase maturity goals | Deepen holdout-local coverage and later holdout-informed calibration before considering workflow or policy moves | No benchmark completion claim, no generalization claim, no policy/gate readiness |

## Remaining blocked or immature areas

The overnight run confirms that these areas are still outside current maturity:

1. **Broader holdout coverage**
   - local holdout exists and is scoreable, but the seed is still tiny.

2. **Private/external tier execution**
   - not attempted and still structurally future work.

3. **Workflow integration**
   - not attempted and still not justified.

4. **Gate / release coupling**
   - explicitly out of scope and still not justified.

## Post-run red-team note

### Strongest alternative explanation

The current benchmark surfaces may appear stable because they are still operating
on carefully built public fixtures and a tiny, hand-curated local holdout seed.
That is meaningful progress, but still short of representative benchmark
maturity.

### What would overturn confidence

Confidence in the current interpretation would weaken if:

- broader local holdout population introduced many new veto failures or revealed
  public-template leakage;
- holdout-informed calibration showed strong divergence between public and local
  structural behavior;
- later semantic layers destabilized the current structural boundaries.

### Weakest part of the evidence

The weakest part of the current evidence is not command stability. It is the
small size and boundedness of the local holdout tier.

## Next justified action

The next justified action is **not** to push further toward workflow or release
integration.

The next justified action is to continue the benchmark under the master program
by:

1. broadening local holdout coverage,
2. broadening holdout-informed calibration,
3. and only later revisiting whether any stronger phase transition is justified.

## Non-claim boundary

This note does **not** mean the benchmark is complete.

It means the benchmark can now support a bounded unattended public + existing-
local evidence run without violating its current safety boundaries.
