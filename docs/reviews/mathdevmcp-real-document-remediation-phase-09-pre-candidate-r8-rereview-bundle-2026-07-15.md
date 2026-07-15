# MathDevMCP Phase 09 Pre-Candidate R8 Rereview Bundle

Date: 2026-07-15
Supervisor/executor: Codex root
Reviewer: fresh local Codex read-only reviewer

## Role Boundary

Do not edit files, create an attestation or candidate, run a mathematical
backend, audit a document, use a network service, initialize a GPU, or
authorize publication, defaults, release, source edits, or scientific claims.

## Objective

Determine whether the implemented R8 trust-closure repair closes every
material R7 finding without introducing a new false-safe, false-unsafe,
classification, feasibility, or authority defect. Candidate launch remains
closed unless the final verdict is unqualified `AGREE`.

## Bounded Artifacts

- `docs/plans/mathdevmcp-real-document-remediation-phase-09-final-red-team-and-decision-subplan-2026-07-15.md`
- `scripts/run_p09_final_red_team.py`
- `tests/p09_no_live_backend_guard.py`
- `tests/p09_guarded_cli_entry.py`
- `tests/test_document_derivation_red_team.py`
- `docs/reviews/mathdevmcp-real-document-remediation-phase-09-pre-candidate-implementation-review-r7-record-2026-07-15.md`

Inspect literal accepted P08/P00/source artifacts only to test a concrete
binding concern. Do not inspect unrelated files.

Exact identities at bundle creation:

- plan: `35af0f1cc29281dca962f7c519fea0583583841870616a1d70f041b269a990be`
- runner: `573dd20a196130e626983d9c6cf3154f871d02c3a1aca685b864905e2b16c650`
- parent guard: `b75175e1f3ca3bdfb43e73313cb5ebb14dfb5c7bd720e4de39e739f013ace579`
- child bootstrap: `1bbcff85847641db5584e63aadbd9342138f25c1119110b38f7830c3cdd33b88`
- red-team tests: `678fc7900e28cf43b8d15b21a55e29faeee62f0e481132b229f6c5bc18a8e36d`
- R7 review record: `a0b0f6558782a05b6a302118600813a44df51b04b79b118338ec08fe379b158f`

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Is R8 safe and complete enough to run the exact guarded named suite and, only if it passes, launch the first immutable candidate? |
| Baseline | Literal accepted P08 chain, fixed P08C1/P08D code identities, four source/comparator files, two P00 inputs, fixed status algorithm, and complete current source/test/fixture closure. |
| Primary criterion | Every replay module is authenticated against accepted and attested identities before execution; parent/child guards cover the same process/network routes and measured audit/backend aliases; runtime identity binds the pinned interpreter, standard library, transitive distribution closure, declared files, and actual import trees; every live handoff rebinds code/runtime/material inputs for every candidate status; test cases require exact globally collected and passed node IDs. |
| Vetoes | Any route to false safe, material evidence classified blocked, environment inability classified unsafe, guard bypass, stale review/state acceptance, prefix-spoofed evidence, or required check that cannot answer the phase question. |
| Not concluded | Agreement is not Phase 09 evidence, proof, corpus generalization, publication/default/release authority, full-suite health, or mission completion. |

## Required Checks

1. Re-audit all five R7 findings against the implementation, not the plan
   summary.
2. Verify every P08C1/P08D mapped code file matches its fixed accepted digest
   and the guarded-suite binding before either replay module is compiled or
   executed. Verify a mismatch cannot execute any replay byte.
3. Compare parent, child, and candidate process/socket route sets. Verify the
   child patches loaded document-audit and mathematical-backend aliases after
   CLI import and emits attempt-derived, independently validated counters.
4. Verify runtime identity pins the resolved interpreter bytes, non-package
   standard-library tree, marker-aware transitive dependency closure, fixed
   versions, complete declared distribution inventories, and actual top-level
   import trees at guarded-suite start/end and candidate/final live handoffs.
   Look specifically for unrecorded-file, dependency-upgrade, bytecode, symlink,
   import-origin, and mutable-baseline gaps.
5. Verify `require_live_state=True` always rebinds current code, runtime,
   material inputs, and available predecessor inventories for `SAFE`, `UNSAFE`,
   and `BLOCKED` candidates, and that verify-candidate, finalize, staged retry,
   and verify-final all use that path.
6. Verify every test-backed case names literal node IDs, including every
   parametrized ID; case evidence must equal the registered list and the same
   IDs must appear in global collected and passed lists. Prefix lookalikes must
   fail.
7. Look independently for wrong baselines, proxy promotion, hidden defaults,
   missing stop conditions, stale context, environment mismatch, incomplete
   artifact coverage, and successful commands that do not answer the phase
   question.

Focused local diagnostics already passed but do not authorize advancement:

```text
53 passed in 4.70s
262 tests collected
Python compilation passed
git diff --check passed
```

Only stale `named-suite-r5.json` and `named-suite-r6.json` exist. Neither
`named-suite-r7.json`, `named-suite-r8.json`, nor `named-suite-r9.json` exists,
and no Phase 09 candidate run root exists.

## Required Output

Findings first, ordered by severity, with exact file/line references. If there
are no material findings, state that explicitly and identify residual risks or
testing gaps. End with exactly one line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
