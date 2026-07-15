# MathDevMCP Phase 03R2 Round-Close Recovery Subplan

Date: 2026-07-13

Status: `SUPERSEDED_BY_ACADEMIC_GOVERNANCE_RESET_DO_NOT_EXECUTE`

This recovery plan is retained as history. It must not be executed. The legacy
round-close protocol is no longer a P03 advancement criterion under
`docs/plans/mathdevmcp-academic-governance-reset-2026-07-13.md`.

Supervisor/executor: Codex

Reviewer: fresh read-only Codex reviewer because the previously attempted
Claude transmission was blocked before disclosure; do not retry or route around
that policy boundary.

## Phase Objective

Recover only the failed P03 `rr01` round-close boundary without rewriting,
deleting, retrying, or reinterpreting any existing receipt. Preserve receipt
22 as the measured failed `close_round`, repair the controller's prefix-binding
defect, create one separately reviewed and no-overwrite
`round-close-recovery.json`, and permit `rr02` initialization only when the
failed chain plus recovery artifact reconstruct exactly.

This recovery does not pass P03, approve the semantic repair, spend the
distinct final-seal audit, or authorize P04.

## Entry Conditions

All conditions are required before implementation:

- P00-P02 remain sealed and unchanged.
- P03 `rr01` candidate remains rejected by the exact result review at SHA-256
  `4524a31392a3f44313eef1ca365c7f6772c738374aa08b090b34a6a163f5abbd`.
- Receipt-index 20 is
  `c1ea34780bfa7f964e1159beb9b7d50b1d1bc9e6cd988150fc93907411e3bd1c`
  and binds verdict `REVISE`.
- Canonical scoped repair is
  `d56ffeea654bba740c74dca8b9b4fb086dd2121c860c194fb8d3bda077edc8e8`
  and binds receipt-index 20.
- Receipt 21 is
  `43aeade9321f1ffc71c2cbc667aa60f254ce2de308bb97a9dae9d6ed5601d182`
  and receipt-index 21 is
  `0a84685796cbe33b98e89806afe82ca3c8d868fcaa79d5678be171be831b60cb`.
- Receipt 22 is
  `1b06a16752b50549f6576e859d9dcd801f25fd56e99b72c489a7fd954e04f4e1`,
  records action `close_round`, exit code 1, null bindings, and exact stderr
  `EvidenceValidationError: Phase 03 scoped-repair trigger binding mismatch`.
- Terminal receipt-index 22 is
  `fc222e0e65cf252b07687427dab2f9be52deb81c2bb4d38c625e181430f64429`.
- `round-close.json`, `round-close-recovery.json`, the P03 stable decision, and
  `rr02` are absent.
- The current semantic scoped repair touches only
  `src/mathdevmcp/context_evidence.py` and `tests/test_context_evidence.py` and
  has a passing focused/expanded local baseline; those checks are explanatory
  until a fresh formal round.
- Human review authority is recorded canonically in
  `docs/plans/mathdevmcp-real-document-remediation-phase-03r2-round-close-recovery-review-budget-2026-07-13.json`.
- R1 review returned `REVISE` at SHA-256
  `83a710e15064c0a8d8b72452c1f2801ef8fd1715f539564b3a81191673ac0779`;
  its five findings are repaired visibly in this plan/bootstrap before R2.
- Canonical budget consumption binds R1, R2, and R3 `REVISE`, reserves the two
  remaining rounds for recovery-result review and replacement P03 result
  review, and leaves zero of the five additional rounds unallocated while
  preserving the distinct final-seal reservation.
- R2 review returned `REVISE` at SHA-256
  `458ffeacfd9c4bd5e5294d965210d619b62e107b5d92ae197fb64d9dbfe95147`;
  exact repaired-label grammar and fail-closed second-create behavior are
  patched before R3.
- R3 is the third of the five additional rounds. The remaining two are
  allocated to recovery-result review and replacement P03 result review, so no
  additional round remains unallocated. The original final-seal audit is
  separately reserved outside those five and remains untouched.
- R3 returned `REVISE` at SHA-256
  `39f3e3a2fa4eb53705bbaf79c79a900e26a7f7c3bee85698c6f0310b4ddbb6d0`
  only because the two stale plan passages now repaired below contradicted the
  already-correct bootstrap/accounting. A fresh plan review requires one new
  human-authorized round; the two named later reviews and final-seal audit may
  not be repurposed.

## Skeptical Plan Audit

The original close plan does not survive audit. `_close_round` removes the
`bind_scoped_repair` receipt from the in-memory receipt list before revalidating
the repair trigger, but it leaves `chain["index_ref"]` and
`chain["index_sha256"]` bound to receipt-index 21. The repair correctly names
receipt-index 20, so the handler rejects its own valid input. Retrying is
forbidden and would still be wrong because action identity cannot repeat.

Rejected alternatives:

- rewriting receipt 22 to exit zero destroys append-only measurement;
- deleting receipt/index 22 hides a real failed action;
- manually creating ordinary `round-close.json` falsely implies the registered
  action succeeded;
- loosening `_predecessor_bindings` to accept any failed close makes a proxy
  artifact a promotion criterion;
- initializing `rr02` without a reviewed recovery crosses the explicit human
  recovery boundary;
- treating 53 local passing tests as closure confuses explanatory checks with
  governance authority.

The recovery is justified only if it is additive, binds the exact failed
state, proves the defect on a disposable chain, and remains ineligible for any
scientific or phase-pass claim.

## Default And Assumption Audit

| Choice | Provenance | Justification | Failure mode | Earliest diagnostic | Status |
| --- | --- | --- | --- | --- | --- |
| Preserve index 22 as terminal history | Reviewed append-only contract | It is the actual measured head | Recovery erases failure | exact no-follow digest reopen | Reviewed default |
| Add a distinct recovery-close schema | Human-recovery stop rule | Separates recovery authority from ordinary action success | Artifact masquerades as receipt success | schema forbids `action_exit_code: 0` and records original exit 1 | Recovery hypothesis |
| Bind source index 20 when reconstructing repair trigger | Scoped-repair record and receipt order | Index 20 is the review-trigger head; 21 only binds the repair | Off-by-one recurs | unit regression calls `_close_round` on disposable chain | Reviewed repair |
| Permit recovered predecessor only for `rr01 -> rr02` | Exact observed failure | Prevents generic bypass | Later failures silently accepted | literal round/ref/digest registry | Recovery hypothesis |
| One-shot no-overwrite recovery creation | Prior recovery discipline | Prevents retry or alternate bytes | Partial artifact or concurrent writer | preflight digest and `O_EXCL` create | Reviewed default |
| CPU-only, backend-free checks | P03 contract | No mathematical backend is relevant to governance repair | test import triggers broader system | no-backend guard in disposable rehearsal | Reviewed default |

## Required Artifacts

Before recovery creation:

- this exact subplan;
- canonical five-round review authority record;
- canonical R1 consumption/carry-forward record;
- immutable R1/R2 `REVISE` results, repaired R3 bundle, and exact R3
  `VERDICT: AGREE`;
- `docs/plans/p03r2_round_close_recovery_20260713.py` with read-only `audit`,
  no-write `preflight`, and readiness-bound one-shot `create` modes;
- focused governance regression tests in the frozen allowlisted
  `tests/test_context_evidence.py`;
- repaired `scripts/p03_governance.py`.

After agreeing recovery-result review:

- exact recovery-result review artifact;
- canonical review-budget consumption/carry-forward record;
- no-overwrite
  `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/round-close-recovery.json`;
- a human-readable recovery close/result note;
- disposable rehearsal evidence under `/tmp`, never treated as formal evidence.

The recovery-close record must bind at least:

- schema, phase, recovery id, and `rr01`;
- decision `blocked` and publication `disabled`;
- exact result review, receipt/index 20, scoped repair, receipt/index 21,
  receipt/index 22, stderr, and original controller digests;
- repaired controller and focused-test digests;
- recovery plan, plan review, result review, bootstrap, and authority digests;
- immutable R1 review plus canonical budget-consumption digest;
- `original_close_action_exit_code: 1`;
- a readiness digest over every create input;
- exact non-claims.

It must not contain or imply a successful ordinary `close_round` receipt.

## Implementation Scope

Allowed existing files:

- `scripts/p03_governance.py`;
- `tests/test_context_evidence.py`.

Allowed additive recovery artifacts:

- the plan/review/budget/bootstrap/result files named here;
- exact `rr01/round-close-recovery.json` after all reviews agree.

The controller repair must:

1. reconstruct the pre-binding prefix with receipt-index 20 identity, not a
   truncated list paired with receipt-index 21 metadata;
2. add an exact validator for the one allowed recovered predecessor;
3. keep the normal successful-close route unchanged;
4. reject wrong round, absent/mismatched receipt, changed stderr, changed
   review/repair/controller/review artifacts, ordinary `round-close.json`
   substitution, recovery artifact overwrite, or nonzero recovery check;
5. leave `expected_p03_next_action` and the frozen 24+2 action registry
   unchanged.

## Required Checks And Reviews

Run in this order:

1. Compile the recovery bootstrap, governance, context evidence, and tests
   without writing repository bytecode.
2. Run focused semantic boundary tests, including the digest-rebound
   falsified-budget mutation.
3. Run focused governance regressions proving the original close defect and
   corrected source-prefix behavior on a disposable tree.
4. Run mutations against every fixed recovery digest/ref, original exit code,
   stderr, absence condition, review verdict, and readiness digest.
   Include full receipt/index/log reconstruction for receipts 1-22, exact
   index-20/index-21 prefixes, receipt-13 implementation-manifest binding,
   exact-key recovery equality, and second-create rejection.
5. Run the complete P03 context/graph/report suite CPU-only.
6. Copy the repository to `/tmp`, preserve the real repository untouched, and
   rehearse the exact failed-rr01 recovery plus `rr02` initialization.
7. In the disposable `rr02`, run the registered formal ladder through
   `candidate_gate`; do not fabricate review/final audit results.
8. Obtain a fresh read-only recovery-result review over exact repaired code,
   bootstrap, checks, and rehearsal artifacts.
9. Only on `AGREE`, run recovery `preflight`, capture its readiness digest, and
   run one exact readiness-bound `create` in the real repository.
10. Independently reopen the recovery artifact and prove real `rr02`
    initialization is now eligible before invoking it.

Claude is not retried. Review uses a fresh read-only Codex agent, which cannot
edit, execute recovery, authorize publication, or cross human/scientific
boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can the exact failed `rr01` close be represented additively and can `rr02` inherit it without rewriting history or weakening normal predecessor validation? |
| Baseline | Exact receipt/index 22 failed head, absent ordinary/recovery close, and current fail-closed `rr02` initializer. |
| Primary pass criterion | Exact failure reconstruction, corrected source-prefix unit regression, all recovery mutations rejected, no-overwrite recovery record, and disposable `rr02` initialization/formal candidate ladder success. |
| Veto diagnostics | Any changed/missing old byte, repeated action, fake successful receipt, generic failed-close acceptance, unexpected path, review mismatch, noncanonical artifact, overwrite, backend/source-edit/publication attempt, or real `rr02` allocation before recovery agreement. |
| Explanatory only | Test count, wall time, reviewer agreement, and semantic mutation count. |
| Not concluded | P03 pass, semantic equivalence, search completeness beyond budgets, mathematical proof, backend fitness, source repair, publication, P04, or release readiness. |
| Preserved artifact | Exact recovery-close JSON plus immutable failed receipts and fresh `rr02` receipt chain. |

## Forbidden Claims And Actions

- Do not modify, delete, relink, rename, or retry any `rr01` receipt/index/log,
  review, scoped repair, candidate, result, or bundle artifact.
- Do not create ordinary `rr01/round-close.json`.
- Do not claim failed receipt 22 passed or that the recovery is an action
  receipt.
- Do not spend or substitute the distinct final-seal audit.
- Do not use Claude after the recorded disclosure-policy denial.
- Do not run mathematical backends, models, network, GPU, installers, frozen
  source edits, publication, commit, push, or P04.
- Do not update the visible execution ledger or stop handoff until P03 reaches
  stable disabled-publication close.

## Exact Next-Phase Handoff Conditions

Formal P03 `rr02` may initialize only when:

- a newly authorized fresh plan review returns exact `AGREE` over the repaired
  post-R3 plan/bootstrap;
- the immutable R1/R2/R3 `REVISE` history and canonical five-round consumption
  record bind that fresh agreeing review;
- the separately allocated recovery-result review later returns exact `AGREE`;
- every fixed old artifact reopens at the digest above;
- the repaired controller and bootstrap match reviewed digests;
- focused/full/disposable checks pass without backend/source/publication
  attempts;
- real recovery preflight returns `READY_NO_WRITE` with a captured digest;
- one readiness-bound create writes exactly one canonical recovery record;
- the recovery record independently reconstructs;
- ordinary `round-close.json`, stable P03 decision, and `rr02` remain absent
  until that reconstruction completes;
- `_predecessor_bindings` accepts only this exact recovered predecessor.

After initialization, `rr02` starts at registered action 1 and follows the
unchanged 24-action pass ladder. A new result-review round is required because
the `rr01` review was consumed by `REVISE`. The original distinct final-seal
audit remains reserved.

## Stop Conditions

Stop before code changes for R3 plan-review `REVISE` or malformed review budget.
Stop before recovery creation for any failed check, rehearsal mismatch,
recovery-result `REVISE`, old-byte drift, concurrent writer, or inability to
prove no-overwrite creation. Stop after any partial recovery write, preserve it,
and require new human direction; never delete or retry it. Stop formal `rr02`
at the first registered failure or review `REVISE` and use only the reviewed
append-only route.

## End Procedure

1. Record local checks and exact artifact digests.
2. Write the P03R2 recovery result/close record.
3. Create and independently verify the recovery-close JSON once.
4. Refresh the next subplan only after `rr02` candidate evidence exists.
5. Review that next material subplan/result for consistency, correctness,
   feasibility, artifact coverage, and boundary safety.
