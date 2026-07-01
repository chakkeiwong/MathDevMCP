# MathDevMCP Forbidden-Claim Semantics Remedy Result

## Status

`PASSED_LOCAL_CHECKS`

## Objective

Repair the normalized real-task candidate-answer contract so asserted forbidden
claims remain hard veto failures while explicitly rejected/detected forbidden
claims can be preserved as audit evidence.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Can normalized real-task scoring distinguish asserted forbidden claims from explicitly rejected/detected forbidden claims while preserving the hard false-confidence veto? |
| Baseline/comparator | Previous `claims`-only scorer where any forbidden phrase in `claims` was treated as asserted. |
| Primary criterion | Met locally. Forbidden phrases in asserted `claims` still produce mismatch/veto failure; the same phrase in `rejected_claims` is recorded in details and does not veto when all other gold fields match. |
| Veto diagnostics | Passed locally. Existing asserted-claim violation tests still pass; malformed present `rejected_claims` fails closed as inconclusive; bounded normalizer leaves unqualified forbidden phrases in asserted `claims`. |
| Explanatory diagnostics | Public fixture/report and local holdout scoring tests pass with both violation and rejected-claim calibration probes. |
| Not concluded | Free-form semantic correctness, model capability, benchmark readiness, release readiness, workflow readiness, gate candidacy, or scientific validity. |

## Changes Made

- Added optional normalized candidate field `rejected_claims`.
- Kept `claims` as the asserted/promoted-claims channel.
- Updated structural scoring to veto only asserted forbidden claims while
  recording `rejected_forbidden_claims` in result details.
- Updated bounded MF-04 and DH-06 answer normalization to split exact forbidden
  phrases into asserted or rejected channels only under conservative exact
  rejection contexts.
- Added public DH-06 calibration fixture for the safe rejected-forbidden-claim
  path while preserving the existing DH-06 violation fixture.
- Added public, local-holdout, and normalizer tests for the new boundary.

## Claude Review Attempt

Claude was used only as a read-only reviewer, but no substantive plan review was
returned.

Attempts:

```bash
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name forbidden-claim-semantics-plan-review-r1 --model opus --effort max '...bounded read-only plan review...'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name forbidden-claim-semantics-probe --model opus --effort max 'Reply with OK.'
bash /home/chakwong/python/claudecodex/scripts/claude_worker.sh --cwd /home/chakwong/python/MathDevMCP --name forbidden-claim-semantics-plan-review-r2 --model opus --effort max '...smaller bounded read-only plan review...'
claude --print '...short bounded read-only plan review...'
```

Result:

- Minimal probe returned `OK`.
- Both wrapper review prompts and direct `claude --print` review prompt
  produced no output before being interrupted.
- No Claude approval or blocker is claimed.
- Execution proceeded under the local supervisor plan because the repair was
  bounded, locally testable, and no substantive reviewer objection was received.

## Commands Run

```bash
python3 -m py_compile src/mathdevmcp/real_tasks_scoring.py src/mathdevmcp/real_tasks_answer_normalization.py
PYTHONPATH=src python -m pytest -q tests/test_real_tasks_scoring.py tests/test_real_tasks_candidate_fixtures.py tests/test_real_tasks_scored_report.py tests/test_real_tasks_holdout_local_scoring.py tests/test_real_tasks_answer_normalization.py
git diff --check
```

## Check Results

- Python compile check: passed.
- Focused pytest bundle: `42 passed in 0.09s`.
- `git diff --check`: passed.

## Boundary And Non-Claims

- Phase 9 remains `STOPPED_NO_GATE_CANDIDATE`.
- This result does not add a workflow, CLI, CI job, blocking status, dashboard,
  default policy, release policy, or gate candidate.
- Public fixture/report results remain structural calibration evidence only.
- Local holdout scoring remains local-only and is not public benchmark,
  benchmark-gate, or release-readiness evidence.
- The bounded normalizer remains a whitelist prototype, not a general semantic
  evaluator.

## Residual Risk

The new `rejected_claims` field is a structural normalized-answer channel. It
does not solve general natural-language negation or semantic entailment. Any
future broadening beyond the current whitelist should get a separate evidence
contract and reviewer pass before execution.
