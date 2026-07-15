# Phase 02 Independent Plan Review Round 5 Bundle

Date: 2026-07-11

Review name: `mathdevmcp-real-document-remediation-p02-plan-r5`

Supervisor/executor: Codex

Reviewer: fresh independent Codex read-only reviewer; external Claude transport
is policy-denied, so no content is sent externally

## Role Boundary

READ-ONLY REVIEW ONLY. Bounded local inspection and digest/reconstruction
commands are permitted. Do not edit files, run Phase 02 implementation,
execute parser fidelity jobs or mathematical backends, launch agents, use
network/external services, or change repository state. Do not authorize
publication, source edits, Phase 03, or a human, runtime, product, funding,
model-file, or scientific-claim boundary.

## Objective

Determine whether the repaired Phase 02 subplan, compact extraction oracle,
and complete materialized oracle are consistent, correct, feasible,
deterministic, fail-closed, and complete enough to implement without choosing
identity-bearing fields, execution semantics, or expected results after
observing implementation behavior.

## Required Artifacts

- `docs/plans/mathdevmcp-real-document-remediation-phase-02-label-scoped-extraction-subplan-2026-07-11.md`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02-materialized-obligations-oracle-2026-07-11.json`;
- `docs/reviews/mathdevmcp-real-document-remediation-phase-02-plan-review-r1-result-2026-07-11.md`;
- `docs/reviews/mathdevmcp-real-document-remediation-phase-02-plan-review-r2-result-2026-07-11.md`;
- `docs/reviews/mathdevmcp-real-document-remediation-phase-02-plan-review-r3-result-2026-07-11.md`;
- `docs/reviews/mathdevmcp-real-document-remediation-phase-02-plan-review-r4-result-2026-07-11.md`;
- exact reviewed fixtures, two frozen source files, and sealed P01 predecessor
  pair named by the plan;
- relevant current locator/parser/governance code only where necessary to
  assess feasibility and boundary safety.

Do not broaden into Phase 02 implementation or Phase 03 semantics.

## Round 4 Findings And Claimed Repairs

Round 4 returned `REVISE` with two material blockers. Its durable result record
above is authoritative. The current bytes claim these visible repairs:

1. The action profile no longer treats governance-native work as a recursive
   child invocation of the external dispatcher. `init_round` now uses a
   distinct `init-round` operation. Actions 2 through 24 use one external
   `run --action` invocation. The compact oracle freezes all 24 actions,
   sequence numbers, execution classes, handler ids or child argv, exact child
   environment, compile inventory, review artifact-ref grammar, dispatch-depth
   guard, and closed receipt nullability. The nine subprocess actions are 2-8,
   11, and 15; all other actions are native. Native handlers run once in
   process and may not invoke governance, allocate nested receipts, or launch a
   subprocess. Re-entry fails before round mutation or receipt allocation.
2. `ambiguous_competing_owner` now explicitly covers both multiple explicit
   labels competing for one classified row before allocation and overlapping
   candidate owner sets after allocation. The diagnostic code distinguishes
   `multiple_explicit_labels_on_one_row` from `competing_owner_sets`.

The supervisor also recorded the human's explicit grant of five additional
substantive Phase 02 plan-review rounds, R5 through R9. That extension is review
budget only and must not be interpreted as execution or boundary authority.

These are claims to audit, not accepted facts. Look especially for external
argv being reused as child argv, a native handler with child fields, recursive
or nested receipt allocation, a dispatch-depth guard that runs after mutation,
an action missing from the registry, prose/registry disagreement, an
artifact-ref escape, an incomplete compile inventory, or a receipt schema that
cannot distinguish native from subprocess execution. Also verify that the
multi-label reason repair did not mutate the 17 complete obligation payloads
or weaken the allocation grammar.

## Frozen Bindings

- Reviewed plan SHA-256:
  `d132ef87b0189958b30962dec18ab308d25fe216c225585585730bab78bdd9a9`.
- Reviewed compact oracle SHA-256:
  `dc6410bc7554b5e305f1e1337d9971c686e5bd45f828e0d9dc5916840d6ecc6e`.
- Reviewed materialized oracle SHA-256:
  `ae7aa48fb8c475c7c37c75158a9ed6f83b21a686bc8cd8ca2b28c79b36bcb1ad`.
- Round-4 result SHA-256:
  `12b12eb0ca444806f8c6878a35eccb4372b00dd85fdbbe3dcf1a2bb9cd85f938`.
- P01 stable decision SHA-256:
  `7abc4b00714d0a216aa506cf3308d25a454443eb7316293ea05ec89f3d54a39a`.
- P01 terminal receipt-index SHA-256:
  `5781ab4a7ba23ff865847dd496839a4f827aee78462166606243ad4da591846a`.
- Golden canonical byte count/digest:
  `2375` /
  `f33683e1a14962db2c3713952311df87f34a84b0a75163b21ec1c526b4571d5e`.

Local pre-review checks report:

- valid compact and materialized JSON plus clean `git diff --check`;
- exactly 24 unique ordered actions, contiguous sequence 1-24, nine exact
  subprocess actions, 15 exact native actions, and 22 unique sorted compile
  paths;
- no native child argv, exact native handler ids, no governance child
  invocation, and artifact refs accepted only by the two review/audit actions;
- the dispatch-depth guard, rejected caller environment keys, receipt fields,
  and native/subprocess nullability agree between plan and registry;
- both reviewed multi-label records use the broadened reason and exact distinct
  diagnostic code;
- independent source materialization reproduced all 17 complete obligations
  and preserved materialized-oracle SHA-256 `ae7aa48...`;
- the earlier localization, classifier, normalizer, inventory, source-span,
  parser-profile, complete-identity, and mutation diagnostics remain reported
  as passing.

Recompute material bindings and a representative cross-section rather than
trusting this statement. Do not execute the implementation or parser/backend
jobs.

## Review Questions

1. Do the two round-4 repairs close the actual findings without weakening the
   primary exact-field criterion or introducing an implementation-defined
   choice?
2. Is `init-round` a genuinely distinct non-recursive operation, and can every
   later external dispatcher action execute exactly once without treating the
   dispatcher argv as a child argv?
3. Are execution classes, handler ids, child argv/environment, receipt
   nullability, action order, failure recording, and receipt-index semantics
   closed and mutually consistent?
4. Does the depth guard reject caller injection and direct or indirect re-entry
   before any filesystem mutation, log creation, handler work, child process,
   or receipt allocation?
5. Can native handlers produce their required artifacts without hidden
   subprocesses or nested receipts, and are all genuinely subprocess-backed
   tasks classified as such?
6. Are the exact child environments sufficient and bounded, including the
   parser environment replacement, pytest guard loading, local temp/home paths,
   and the zero-backend boundary?
7. Does the complete compile child argv cover every Python implementation path
   that the allowlist permits, including conditional audit-report paths?
8. Are review/audit artifact refs accepted only by their exact round-specific
   native actions, with no generic path or extra-argument escape?
9. Does the broadened `ambiguous_competing_owner` mapping deterministically
   cover the pre-allocation multi-label fixture while retaining the distinct
   post-allocation overlap route?
10. Do environment localization, row classification, grouping, target
    normalization, inventory scanning, and all 17 compact/materialized/source
    projections remain mutually consistent after the repair?
11. Does each complete payload still reconstruct from frozen source bytes,
    with exact canonical bytes, obligation digest/id, environment/row identity,
    provenance, owned/excluded spans, and non-valid-case boundaries?
12. Are parser fidelity, specialist selection, immutable-input protection,
    zero backend/source edit enforcement, result reconstruction, and stable
    publication still fail-closed and non-circular?
13. Do fixed commands collect nonzero intended tests, preserve P00/P01, and
    avoid proxy promotion or accidental backend execution?
14. Do stop and Phase 03 handoff conditions retain every non-claim and require
    exact positive/adversarial outcomes rather than counts or booleans?
15. Identify wrong baselines, proxy promotion criteria, silent defaults, stale
    context, infeasible primitives, unsupported claims, missing mutations, or
    boundary violations.

## Required Output

Findings first, severity ordered, with exact file/line references. Distinguish
material execution blockers from optional improvements. If no material finding
remains, state that explicitly and identify residual implementation/testing
risks without converting them into blockers.

Include exactly one line for each binding below with the actual recomputed
lower-case digest:

```text
Reviewed plan SHA-256: `<lowercase-64-hex>`
Reviewed compact oracle SHA-256: `<lowercase-64-hex>`
Reviewed materialized oracle SHA-256: `<lowercase-64-hex>`
Reviewed bundle SHA-256: `<lowercase-64-hex>`
```

End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
