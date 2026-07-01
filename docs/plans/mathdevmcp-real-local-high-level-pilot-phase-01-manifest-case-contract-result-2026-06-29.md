# Phase 01 Result: Manifest And Case Contract

Date: 2026-06-29

Status: `PASSED`

## Objective

Define a local pilot manifest contract and add five source-backed case records
with current executable probes and explicit forbidden-claim boundaries.

## Artifacts Created

- `benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json`

## Manifest Summary

The manifest contains exactly five cases:

1. `RLHL-01-ift-gradient-bias-sign`
2. `RLHL-04-kalman-prediction-error-loglik`
3. `RLHL-06-joseph-covariance-equivalence`
4. `RLHL-07-affine-pricing-master-recursion`
5. `RLHL-10-kalman-score-same-scalar-contract`

Each case has separate channels for:

- `source_snapshot`;
- `source_obligation`;
- `executable_probe`;
- `adapter_gap`;
- `forbidden_claims`.

The manifest records local source commit/status metadata where available. Some
sibling repositories are dirty, and this is recorded rather than hidden.

## Local Checks

```text
python3 -m json.tool benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json
```

Result: passed.

```text
python3 - <<'PY'
...
PY
```

Result: passed. Manifest has five cases and no missing referenced source paths.

```text
rg -n "release readiness|broad theorem|benchmark-gate evidence|scientific validity|pilot accuracy|source obligation|executable probe" benchmarks/real_tasks/holdout_local/high_level_pilot_cases.json docs/plans/mathdevmcp-real-local-high-level-pilot-phase-01-manifest-case-contract-subplan-2026-06-29.md
```

Result: passed. Non-claims and source/probe separation language are present.

## Evidence Contract Assessment

| Field | Assessment |
| --- | --- |
| Primary criterion | Passed. Manifest parses, references existing relative source paths, includes five selected cases, records snapshot metadata, and keeps source/probe/adapter/non-claim channels distinct. |
| Veto diagnostics | No Phase 1 veto fired. No absolute source paths, missing source paths, missing forbidden-claim boundaries, or blended case-status field were introduced. |
| Explanatory diagnostics | The local source repositories are not all clean; this is preserved as snapshot metadata and not converted into public fixture evidence. |
| Not concluded | Runner correctness, benchmark quality, public redistributability, and full derivation validity are not concluded. |

## Phase 02 Handoff

Proceed to Phase 02. The loader/runner/scorer must:

- validate the manifest schema and path policy;
- reject malformed or unsafe cases;
- dispatch only the declared executable probes;
- score probe result status/evidence/non-claims separately from source
  obligation and adapter-gap channels;
- include known-bad scorer tests for forbidden claims, blended channels,
  missing non-claims, and hidden adapter gaps.

## Next Subplan Review

Phase 02 subplan remains consistent after Phase 1. It has explicit objective,
entry conditions, artifacts, checks/reviews, evidence contract, forbidden
claims/actions, handoff conditions, stop conditions, and end-of-phase
requirements.
