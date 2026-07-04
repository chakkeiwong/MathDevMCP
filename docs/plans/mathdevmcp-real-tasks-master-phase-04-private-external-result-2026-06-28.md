# MathDevMCP Real-Task Master Phase 4 Result: Private/External Corpus

## Status

`PASSED_AS_OPTIONS_ONLY`

## Phase Objective

Define candidate private/external corpus representation, redaction, and fallback
policy options without leaking paths or blocking public benchmark hardening when
private or external material is unavailable.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can private/external tasks be represented safely without hidden access assumptions or path leaks? |
| Baseline/comparator | Master program Phase 4 and existing real-task public/holdout docs. |
| Primary criterion | Met for options-only planning. Existing docs distinguish public, holdout-local, and private/external tiers; the Phase 4 subplan explicitly prevents data inclusion, external source use, operational private-data handling, or binding policy adoption without human approval. |
| Veto diagnostics | Passed. No external fetch, private data access, private path commit, or binding policy adoption occurred. |
| Explanatory diagnostics | Existing docs mention private/external, redaction, local-only, and not-release/not-public boundaries. |
| Not concluded | Private/external execution completeness, BayesFilter availability, release readiness, or binding private/external corpus policy. |

## Commands Run

```bash
git status --short
test -f docs/plans/mathdevmcp-real-tasks-master-phase-04-private-external-subplan-2026-06-28.md && test -f benchmarks/real_tasks/README.md && test -f docs/plans/mathdevmcp-real-tasks-master-phase-05-schema-loader-validator-subplan-2026-06-28.md
rg -n "private/external|redaction|not public|not release-readiness|private|external|not committed|not a benchmark failure" benchmarks/real_tasks docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md docs/plans/mathdevmcp-real-tasks-master-phase-04-private-external-subplan-2026-06-28.md
PYTHONPATH=src python -m pytest -q tests/test_real_tasks_manifest.py tests/test_real_tasks_holdout_local.py
```

## Check Results

- Required Phase 4 and Phase 5 handoff artifacts were present.
- Boundary search found:
  - private/external tier language in `benchmarks/real_tasks/README.md`;
  - holdout-local is not the same as private/external;
  - private/external has additional privacy/redaction requirements;
  - master-program language treats external/private access as dependency-managed;
  - Phase 4 subplan requires human approval before data inclusion or binding
    policy adoption.
- `tests/test_real_tasks_manifest.py` and
  `tests/test_real_tasks_holdout_local.py`: `20 passed`.

## Revalidation Edge

No Phase 4 changes were made to admissibility, provenance, privacy, or redaction
constraints. Therefore Phase 2/3 artifacts do not need to be reopened before
Phase 5.

## Freshness And Dirty-Worktree Note

The worktree remains dirty with pre-existing benchmark docs and visible
execution artifacts. Phase 4 did not fetch external sources, read private data,
or write private/external corpus artifacts.

## Phase 5 Handoff

Proceed to Phase 5 because:

- private/external access remains dependency-managed and options-only;
- no hidden external/private access assumption blocks public loader hardening;
- no Phase 2/3 revalidation was triggered;
- the Phase 5 subplan exists:
  `docs/plans/mathdevmcp-real-tasks-master-phase-05-schema-loader-validator-subplan-2026-06-28.md`.

## Next Subplan Review

The Phase 5 subplan was repaired after Claude review to require re-audit or
deferral if Phase 4 changes admissibility/provenance/privacy/redaction
constraints, and to label schema/validator status provisional until post-pilot
review.

## Non-Claims

This Phase 4 pass does not conclude that:

- private/external real-task execution is complete;
- BayesFilter or external access is available;
- private data may be included;
- any private/external policy has been adopted;
- release readiness is supported.
