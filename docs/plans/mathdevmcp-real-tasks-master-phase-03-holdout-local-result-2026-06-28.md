# MathDevMCP Real-Task Master Phase 3 Result: Holdout-Local

## Status

`PASSED`

## Phase Objective

Confirm that the holdout-local tier reduces public-set overfitting pressure
while preserving local-only boundaries and avoiding generalization claims.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the holdout-local tier add representativeness value beyond the public corpus while staying local-only? |
| Baseline/comparator | Current public corpus, holdout-local policy, and current local seed. |
| Primary criterion | Met for the current local-only seed. Holdout-local policy/scaffold exists, local scoring is bounded/non-gating, and the current local seed spans multiple families. |
| Veto diagnostics | Passed. Local score output explicitly states it is not public benchmark evidence, not benchmark-gate evidence, not release-readiness evidence, and local artifacts should not be committed by default. |
| Explanatory diagnostics | Local holdout case total `8`; scored candidate total `8`; missing candidate IDs none; status mix `7 consistent`, `1 mismatch`; false-confidence-veto failures `1`. |
| Not concluded | Holdout-backed generalization, policy readiness, representative task distribution, public benchmark evidence. |

## Commands Run

```bash
git status --short
test -f docs/plans/mathdevmcp-real-tasks-master-phase-03-holdout-local-subplan-2026-06-28.md && test -f benchmarks/real_tasks/holdout_local/README.md && test -f docs/plans/mathdevmcp-real-tasks-master-phase-04-private-external-subplan-2026-06-28.md
PYTHONPATH=src python -m pytest -q tests/test_real_tasks_holdout_local.py tests/test_real_tasks_holdout_local_scoring.py
PYTHONPATH=src python -c '... score_local_holdout_candidate_fixtures(root) ...'
```

## Check Results

- Required Phase 3 and Phase 4 handoff artifacts were present.
- `tests/test_real_tasks_holdout_local.py` and
  `tests/test_real_tasks_holdout_local_scoring.py`: `15 passed`.
- Live local holdout fixture score:
  - local holdout case total: `8`;
  - scored candidate total: `8`;
  - missing candidate case IDs: none;
  - by status:
    - `consistent`: `7`;
    - `mismatch`: `1`;
  - false-confidence-veto failures: `1`;
  - by family:
    - `evidence_boundary_discipline`: `4`;
    - `retrieval_and_provenance`: `1`;
    - `numerical_oracle_parity`: `1`;
    - `derivation_boundary_and_abstention`: `1`;
    - `code_document_consistency`: `1`.

## Freshness And Dirty-Worktree Note

The live local holdout state is newer than some current-state notes that still
mention a seven-case local seed. This result records the current local-only
score as of this phase without editing or committing populated `.local`
artifacts.

## Phase 4 Handoff

Proceed to Phase 4 because:

- holdout-local policy and local-only boundary are explicit;
- local discovery/scoring tests pass;
- local seed state is summarized without exposing case contents;
- the Phase 4 subplan exists and now treats private/external policy as
  candidate options requiring human approval before data inclusion or binding
  policy adoption.

## Next Subplan Review

The Phase 4 subplan was repaired after Claude review to add:

- explicit human approval before data inclusion, external source use,
  operational private-data handling, or binding policy adoption;
- a Phase 4-to-Phase 5 revalidation edge if admissibility, provenance, privacy,
  or redaction constraints change Phase 2/3 assumptions.

## Non-Claims

This Phase 3 pass does not conclude that:

- holdout-local evidence is public benchmark evidence;
- the local seed is representative of the broader task distribution;
- local scoring is policy/gate/release evidence;
- the benchmark has holdout-backed generalization evidence.
