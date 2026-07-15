# MathDevMCP Phase 09 Pre-Candidate R6 Rereview Bundle

Date: 2026-07-15
Review name: `mathdevmcp-phase09-pre-candidate-r6`
Supervisor/executor: Codex
Reviewer: Claude Opus/max, read-only

## Role Boundary

Claude must not edit files, run mutating commands, launch the Phase 09
candidate, invoke a mathematical backend, audit a document, use the network
other than the review API, or authorize publication/default/release/scientific
claims. Codex remains supervisor and executor.

## Objective

Perform a fresh skeptical pre-candidate review of the implemented Phase 09 R6
contract. Decide whether any material correctness, evidence-binding,
classification, lifecycle, fail-closed, feasibility, or authority defect still
requires repair before the immutable `create-candidate` command may run.

## Artifacts To Inspect

- `docs/plans/mathdevmcp-real-document-remediation-phase-09-final-red-team-and-decision-subplan-2026-07-15.md`
- `scripts/run_p09_final_red_team.py`
- `tests/p09_no_live_backend_guard.py`
- `tests/p09_guarded_cli_entry.py`
- `tests/test_document_derivation_red_team.py`
- `docs/reviews/mathdevmcp-real-document-remediation-phase-09-pre-candidate-implementation-review-r4-record-2026-07-15.md`
- `docs/reviews/mathdevmcp-real-document-remediation-phase-09-pre-candidate-implementation-review-r5-record-2026-07-15.md`

Inspect the literal P08 evidence roots referenced by the runner only when needed
to test a concrete binding or classification concern. Do not inspect unrelated
repository files.

Reviewed identities at bundle creation:

- plan: `531a4e6666a6ebce031b9c90d05ebabf86ab6254d5c156abf073cae17f866287`
- runner: `05011b6e86d57a4766c5a7fd15f7328358303f9e8b009605591f85b091e3cbfa`
- parent guard: `047989794c3f81bf973eebcd35391522c2d5e27482b1923293b57398b5290e54`
- child bootstrap: `6f6d5426f8a09d3c40bcd2cc4074b4f98e598eff70c06337c8dddbb3d912e9bd`
- red-team tests: `7c6ab8d7eac4939f777226e9cd94c6e14b5b223304efedbee861720578e8e58d`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is R6 safe and complete enough to launch the first immutable Phase 09 candidate? |
| Baseline/comparator | Literal accepted P08A/P08B/P08C/P08C1/P08D roots and fixed decisions; stale Phase 09 preflights and the historical full-suite count have no authority. |
| Primary criterion | Every material predecessor, current-code, test, status, review, finalization, and non-live execution boundary is fail-closed and internally consistent, with no known route to a false safe candidate. |
| Veto diagnostics | Wrong or incomplete bindings, proxy promotion, unrecorded skip/failure, unsafe evidence classified blocked, environment block classified unsafe, backend/network/document-audit escape, stale review acceptance, non-atomic or non-recoverable finalization, or an untested material status path. |
| Explanatory diagnostics | Style, naming, redundant governance, and tests that improve confidence without exposing a false-safe or boundary-crossing route. |
| Not concluded | Agreement is not candidate evidence, proof, whole-document correctness, publication/default/release authority, full-suite health, or mission completion. |

## Required Skeptical Checks

1. Recheck the R4 and R5 repair claims against implementation, not prose.
2. Verify R6 records setup/call/teardown failures and skips with deterministic
   precedence and cannot count a non-executed test as passed.
3. Verify the attestation binds the exact invocation, environment, case node
   evidence, and complete current source/test/fixture closure, and that stale
   preflights cannot authorize candidate creation.
4. Verify malformed readable predecessor evidence becomes `UNSAFE`, while a
   genuine runtime/interpreter/authority inability becomes `BLOCKED`.
5. Verify candidate creation, independent verification, review binding,
   recoverable finalization, and final verification cannot accept drift or an
   unrelated review.
6. Look explicitly for wrong baselines, hidden defaults, proxy criteria,
   missing stop conditions, stale context, environment mismatch, and commands
   whose artifacts would not answer the phase question.

Focused local evidence already obtained, but not sufficient by itself:

```text
1 passed in 0.02s
```

The focused check was
`test_guard_attestation_accounts_for_non_call_outcomes_without_duplicates`;
the four Phase 09 Python files also compiled. No candidate run root exists.

## Required Output

Report findings first, ordered by severity, with exact file and line references.
Do not return agreement if a material unexamined default or false-safe path
remains. End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
