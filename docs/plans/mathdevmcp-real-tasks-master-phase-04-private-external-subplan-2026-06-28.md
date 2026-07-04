# MathDevMCP Real-Task Master Phase 4 Subplan: Private/External Corpus

## Phase Objective

Define candidate private/external corpus representation, redaction, and fallback
policy options without leaking paths or blocking public benchmark hardening when
private or external material is unavailable.

## Entry Conditions Inherited From Previous Phase

- Phase 3 holdout-local tier is separated from public corpus and remains
  local-only.
- The program needs private/external policy, not immediate full private corpus
  execution.

## Required Artifacts

- `benchmarks/real_tasks/README.md`
- `benchmarks/real_tasks/holdout_local/README.md`
- `docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
- `scripts/create_sanitized_private_corpus.sh` if private/external sanitized
  release-corpus behavior is used as a reference only
- Phase result:
  `docs/plans/mathdevmcp-real-tasks-master-phase-04-private-external-result-2026-06-28.md`
- Next subplan:
  `docs/plans/mathdevmcp-real-tasks-master-phase-05-schema-loader-validator-subplan-2026-06-28.md`

## Required Checks, Tests, And Reviews

- Local checks:
  - `rg -n "private/external|redaction|not public|not release-readiness" benchmarks/real_tasks docs/plans/mathdevmcp-real-tasks-benchmark-master-program-2026-06-17.md`
  - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_manifest.py tests/test_real_tasks_holdout_local.py`
- Review:
  - Codex self-review required.
- Claude read-only review required if a new private/external policy artifact is
  created or if sanitized external corpus conventions are reused.
- Human approval required before any data inclusion, external source use,
  operational private-data handling, or binding policy adoption.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can private/external tasks be represented safely without hidden access assumptions or path leaks? |
| Baseline/comparator | Master program Phase 4 and existing real-task public/holdout docs. |
| Primary pass criterion | Candidate policy/options state redaction, path, access, and fallback boundaries clearly without authorizing data inclusion or operational handling. |
| Veto diagnostics | Private paths leak, missing external access becomes hidden blocker, private evidence is merged into public/holdout claims. |
| Explanatory diagnostics | Existing release-corpus private fixtures may inform redaction patterns but do not certify real-task private readiness. |
| Not concluded | Private/external execution completeness, BayesFilter availability, release readiness. |
| Artifacts | Phase result, policy/fallback note if needed, refreshed Phase 5 subplan. |

## Forbidden Claims And Actions

- Do not fetch external repositories or private data without explicit approval.
- Do not commit private paths, credentials, or non-redacted content.
- Do not block public Phase 5 hardening on incomplete private/external access.
- Do not treat sanitized release-corpus behavior as real-task private benchmark
  completion.
- Do not adopt binding private/external corpus policy or operational data
  handling rules without human signoff.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 5 only if:

- missing private/external access is represented as policy/fallback state, not a
  hidden blocker;
- public manifest hardening can proceed independently;
- any changed admissibility, provenance, privacy, or redaction constraints have
  been propagated into a required re-audit of Phase 2/3 outputs before Phase 5
  treats those outputs as inputs;
- Phase 5 subplan preserves future tier-aware extension points.

## Stop Conditions

- Stop if continuation requires private data, credentials, external clone/fetch,
  or a privacy decision not already authorized.
- Stop if redaction policy cannot be stated concretely.
- Stop if a proposed private/external artifact would blur public, holdout-local,
  and private tiers.
- Stop if Phase 4 findings would materially change public or holdout
  admissibility/provenance rules and Phase 2/3 artifacts have not yet been
  re-audited against those changes.

## End-Of-Subplan Requirements

1. Run the required local checks.
2. Write the phase result / close record.
3. Draft or refresh the Phase 5 subplan.
4. Review the Phase 5 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
