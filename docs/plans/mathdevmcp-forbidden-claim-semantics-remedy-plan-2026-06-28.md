# MathDevMCP Forbidden-Claim Semantics Remedy Plan

## Status

`EXECUTED_LOCAL_CHECKS_PASSED_CLAUDE_REVIEW_UNAVAILABLE`

## Objective

Repair the normalized real-task candidate-answer contract so the scorer can
distinguish forbidden claims that are asserted or promoted from forbidden
claims that are explicitly rejected, detected, or preserved as non-claims.

This is post-Phase-9 repair/calibration work. It does not reopen the Phase 9
gate-candidate stop and does not authorize workflow, CI, release-policy, or
scientific-readiness movement.

## Problem

`RealTaskCandidateAnswer` currently has one `claims` list. The scorer treats
every forbidden phrase in that list as an asserted forbidden claim:

- `forbidden_claims_absent` searches only `claims`;
- `false_confidence_veto_clear` fails when a forbidden phrase is found there;
- there is no structured channel for a candidate to say "this forbidden claim
  was detected and rejected."

That preserves safety, but it cannot represent a safe normalized answer that
mentions an exact forbidden phrase only to reject it.

## Skeptical Plan Audit

| Risk | Audit result |
| --- | --- |
| Wrong baseline | Baseline is the current scorer behavior in `src/mathdevmcp/real_tasks_scoring.py` plus focused tests/fixtures. Phase 8/9 artifacts remain non-gating background, not a promotion baseline. |
| Proxy metrics as promotion criteria | Focused pytest results are only engineering evidence that the structural contract behaves as specified. They are not benchmark, semantic, release, or scientific evidence. |
| Missing stop conditions | Stop if hard false-confidence veto weakens, if malformed candidate fields stop failing closed, if public/local holdout boundaries are crossed, if Claude finds a material unresolved issue, or if focused tests fail. |
| Unfair comparison | No benchmark score improvement will be claimed. The comparison is old structural representation versus revised structural representation on explicit assertion/rejection probes. |
| Hidden assumptions | The scorer can trust normalized candidate fields only as a structural contract. Free-form semantic interpretation remains bounded to existing whitelist normalizers. |
| Stale context | Current scoring, normalization, public fixture, holdout scoring, and Phase 8/9 stop files were re-inspected on 2026-06-28 before writing this plan. |
| Artifact relevance | The planned code diff, fixture update, focused tests, and close record directly answer whether assertion and rejection are separated without weakening veto behavior. |

Audit conclusion: execution may proceed after Claude read-only review if the
review finds no material blocker or after any fixable blocker is patched and
focused plan checks are rerun.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can normalized real-task scoring distinguish asserted forbidden claims from explicitly rejected/detected forbidden claims while preserving the hard false-confidence veto? |
| Baseline/comparator | Current `claims`-only scorer and existing tests where forbidden phrases in `claims` produce mismatch/veto failure. |
| Primary pass criterion | A forbidden phrase in asserted `claims` still causes `forbidden_claims_absent = false`, `false_confidence_veto_clear = false`, and score `mismatch`; the same forbidden phrase in the new rejected/non-claim channel can be recorded without causing a veto when all other gold fields match. |
| Veto diagnostics | Any weakening of asserted-forbidden-claim failure; any broad semantic normalizer that reclassifies unsafe claims as rejected without exact bounded rejection context; malformed optional fields passing as valid; local holdout or public fixture evidence being claimed as gate/release/scientific evidence. |
| Explanatory diagnostics | Public fixture counts, scored report summaries, and normalizer composition tests. These explain behavior but do not promote the benchmark. |
| Not concluded | Free-form semantic correctness, model capability, benchmark readiness, release readiness, workflow readiness, gate candidacy, or scientific validity. |
| Preserving artifact | This plan plus a result/close record under `docs/plans/`, the code diff, fixture diff, and focused pytest output. |

## Execution Steps

1. Add a backwards-compatible `rejected_claims: list[str]` normalized candidate
   field.
   - `claims` remains the asserted/promoted-claim channel.
   - Missing `rejected_claims` defaults to an empty list.
   - Present non-list or non-string `rejected_claims` is malformed and scores
     inconclusive.

2. Update the structural scorer.
   - Continue checking forbidden claims only against asserted `claims`.
   - Record any gold forbidden phrases found in `rejected_claims` under result
     details for auditability.
   - Preserve existing quality-check names so report summaries remain stable.

3. Update bounded answer normalization.
   - Keep existing whitelist case support only.
   - Split exact forbidden phrase mentions into asserted `claims` versus
     `rejected_claims` only when an exact, conservative rejection prefix is
     present.
   - If an exact forbidden phrase is present without the bounded rejection
     context, keep it in asserted `claims` so the hard veto still fires.

4. Update tests and public calibration fixtures.
   - Add scorer tests for accepted rejected-claim evidence.
   - Add scorer tests for malformed optional rejected-claim fields.
   - Preserve tests proving asserted forbidden claims fail.
   - Add a public calibration fixture that records a rejected DH-06 forbidden
     claim safely while keeping the existing DH-06 violation fixture.
   - Add normalizer composition coverage for a safe exact rejected-claim mention.

5. Run focused local checks.
   - `PYTHONPATH=src python -m pytest -q tests/test_real_tasks_scoring.py tests/test_real_tasks_candidate_fixtures.py tests/test_real_tasks_scored_report.py tests/test_real_tasks_holdout_local_scoring.py tests/test_real_tasks_answer_normalization.py`
   - `git diff --check`

6. Write a result/close record.
   - Include commands run, test results, changed files, evidence-contract result,
     non-claims, and any residual risk.

## Forbidden Claims And Actions

- Do not weaken or remove the hard false-confidence veto for asserted claims.
- Do not reinterpret all negated prose with broad semantic heuristics.
- Do not claim benchmark-score improvement, model capability, release readiness,
  workflow readiness, gate candidacy, or scientific validity.
- Do not modify Phase 9's `STOPPED_NO_GATE_CANDIDATE` decision.
- Do not treat local holdout artifacts as public benchmark evidence.
- Do not let Claude authorize execution boundaries; Claude is read-only review
  only.

## Stop Conditions

Stop and write a blocker result if:

- Claude identifies a material issue that is not fixable within this bounded
  remedy;
- focused tests fail after a reasonable local fix attempt;
- the implementation would require changing public benchmark policy or Phase 9
  gate conclusions;
- representing rejected claims requires broad semantic inference outside the
  bounded normalizer whitelist;
- required artifacts cannot be written or checked locally.

## Claude Review Scope

Claude should review only this plan's objective, evidence contract, execution
steps, forbidden actions, and stop conditions. Claude is asked for a concrete
read-only verdict: `AGREE`, `AGREE_WITH_NITS`, or `BLOCKED`, with fixable
issues listed. Claude must not edit files, run implementation, authorize
boundary crossings, or reinterpret Phase 9 policy.
