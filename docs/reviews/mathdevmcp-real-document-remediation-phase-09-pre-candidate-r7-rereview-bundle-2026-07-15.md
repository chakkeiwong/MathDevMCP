# MathDevMCP Phase 09 Pre-Candidate R7 Rereview Bundle

Date: 2026-07-15
Supervisor/executor: Codex root
Reviewer: fresh local Codex read-only reviewer

## Role Boundary

Do not edit files, create an attestation or candidate, run a mathematical
backend, audit a document, use a network service, or authorize publication,
defaults, release, source edits, or scientific claims.

## Objective

Determine whether the implemented R7 repair closes every material R6 finding
without introducing a new false-safe, false-unsafe, classification, feasibility,
or authority defect. Candidate launch remains closed unless the final verdict
is unqualified `AGREE`.

## Bounded Artifacts

- `docs/plans/mathdevmcp-real-document-remediation-phase-09-final-red-team-and-decision-subplan-2026-07-15.md`
- `scripts/run_p09_final_red_team.py`
- `tests/p09_no_live_backend_guard.py`
- `tests/p09_guarded_cli_entry.py`
- `tests/test_document_derivation_red_team.py`
- `docs/reviews/mathdevmcp-real-document-remediation-phase-09-pre-candidate-implementation-review-r6-record-2026-07-15.md`

Inspect literal accepted P08/P00/source artifacts only to test a concrete
binding concern. Do not inspect unrelated files.

Exact identities at bundle creation:

- plan: `681408e45a5fafc2e1a89a414d49ef045451f1082e0732b9aec481c073b38f46`
- runner: `81509b73d4c1f16df6305af00b9b292dab8636968086ae51e1471f610bceca1c`
- parent guard: `ab33ec5c532084a55d975e4900c18d5d8be285b03f71eeecd4f8b0098398f3b1`
- child bootstrap: `6f6d5426f8a09d3c40bcd2cc4074b4f98e598eff70c06337c8dddbb3d912e9bd`
- red-team tests: `ba2db1c19b3519f5325d7e88f1a50287aea9ed9907153214ac3d7ee4717dc17f`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is R7 safe and complete enough to run the exact guarded named suite and, only if it passes, launch the first immutable candidate? |
| Baseline | Literal accepted P08 chain, four source/comparator files, two P00 inputs, fixed status algorithm, and complete current source/test/fixture closure. |
| Primary criterion | No unverified byte executes; tested and sealed code/runtime are identical; guard claims are measured; material inputs remain bound through final verification; environment/evidence classifications are correct; all test-backed cases have exact passing nodes; handoff digests are mandatory. |
| Vetoes | Any route to false safe, material evidence classified blocked, environment inability classified unsafe, guard bypass, stale review/state acceptance, or required check that cannot answer the phase question. |
| Not concluded | Agreement is not Phase 09 evidence, proof, corpus generalization, publication/default/release authority, full-suite health, or mission completion. |

## Required Checks

1. Re-audit all seven R6 findings against the implementation, not the plan
   summary.
2. Verify every dynamically executed reconstruction module is authenticated
   before compile/exec and readable snapshot corruption cannot execute or become
   `BLOCKED` merely because loading precedes validation.
3. Verify the guarded suite binds complete code and runtime identities before
   collection and after execution, records collection/setup/call/teardown
   outcomes, requires collected equals passed, and cannot seal changed bytes.
4. Verify backend/document-audit/network counters are derived from actual
   guards and relevant aliases cannot bypass the block.
5. Verify source/comparator/P00/P08 material inputs, current code, and runtime
   identity are rechecked at candidate verify, finalization, and final verify.
6. Verify CPython mismatch is `BLOCKED`, evidence mismatch is `UNSAFE`, Lean
   case evidence is production-test-backed, and both verify digests are
   required.
7. Look for wrong baselines, proxy promotion, hidden defaults, missing stop
   conditions, stale context, environment mismatch, incomplete artifact
   coverage, and successful commands that do not answer the stated question.

Focused local diagnostics already passed but do not authorize advancement:

```text
41 passed in 4.30s
```

The four Phase 09 Python files compile, `git diff --check` passes, the full
named suite collects 249 tests under the guard, and no candidate run root
exists. No attestation was written by these diagnostics.

## Required Output

Findings first, ordered by severity, with exact file/line references. End with
exactly one line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
