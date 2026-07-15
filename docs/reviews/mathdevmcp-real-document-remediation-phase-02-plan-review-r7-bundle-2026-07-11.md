# Phase 02 Independent Plan Review Round 7 Bundle

Date: 2026-07-11

Review name: `mathdevmcp-real-document-remediation-p02-plan-r7`

Supervisor/executor: Codex

Reviewer: fresh independent Codex read-only reviewer; external Claude transport
is policy-denied, so no content is sent externally

## Role Boundary

READ-ONLY REVIEW ONLY. Bounded local inspection and digest/reconstruction
commands are permitted. Do not edit files, create the formal P02 entry root,
run Phase 02 implementation, execute parser fidelity jobs or mathematical
backends, launch agents, use network/external services, or change repository
state. Do not authorize publication, source edits, Phase 03, or a human,
runtime, product, funding, model-file, or scientific-claim boundary.

## Objective

Determine whether the repaired Phase 02 plan, compact extraction/governance
oracle, complete materialized oracle, and standalone entry bootstrap are
consistent, correct, feasible, deterministic, fail-closed, and complete enough
to implement without inventing entry grammar, failure closure, result binding,
identity fields, or expected outputs after implementation begins.

## Required Artifacts

- `docs/plans/mathdevmcp-real-document-remediation-phase-02-label-scoped-extraction-subplan-2026-07-11.md`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02-materialized-obligations-oracle-2026-07-11.json`;
- `docs/plans/p02_entry_bootstrap_20260711.py`;
- `docs/reviews/mathdevmcp-real-document-remediation-phase-02-plan-review-r6-result-2026-07-11.md`;
- earlier Phase 02 review results where needed to assess regression;
- exact reviewed fixtures, two frozen sources, sealed P00/P01 evidence trees,
  and relevant current code only where needed for feasibility.

Do not broaden into Phase 02 implementation or Phase 03 semantics.

## Round 6 Finding And Claimed Repair

Round 6 returned `REVISE` with one material blocker. The compact entry-bootstrap
profile required repeated `--agreeing-plan-review-ref` options to be rejected,
but normal single-value `argparse` handling accepted repeated occurrences and
silently used the final value.

The current bytes claim this visible repair:

1. Before constructing `ArgumentParser`, reading the environment, resolving the
   workspace root, or touching any file, the bootstrap requires `sys.argv[1:]`
   to contain exactly two tokens and requires the first token to equal the full
   literal `--agreeing-plan-review-ref`.
2. The validated two-token vector is passed to an `ArgumentParser` with
   `allow_abbrev=False`; the value must still pass the closed R6+ review-ref
   regex and strict agreeing-review grammar later in the bootstrap.
3. Repeated options, abbreviated options, `--option=value`, positional-only
   values, missing values, unknown options, and extra arguments therefore fail
   before workspace or entry-root work. The one exact option/value form remains
   accepted.
4. The plan status now records repair after R6 and pending R7. The compact and
   materialized oracles were not changed.

These are claims to audit, not accepted facts. Look especially for a Python
argv form that bypasses the two-token guard, an error path that performs root or
file work first, source/profile disagreement, or a valid profile invocation
that was accidentally rejected.

## Frozen Bindings

- Reviewed plan SHA-256:
  `6de640b7d65c5236587244427e1437bafc462a2bcad74d18fac85f08d5a566e9`.
- Reviewed compact oracle SHA-256:
  `ea5a22c52dfc3920d7ad7f2bb9334b1a70fbd6c41c0144acc903ac94d97cca50`.
- Reviewed materialized oracle SHA-256:
  `ae7aa48fb8c475c7c37c75158a9ed6f83b21a686bc8cd8ca2b28c79b36bcb1ad`.
- Reviewed entry bootstrap SHA-256:
  `3a1e9cf497e28356e7574e235427bfc7e77679b18d5a78e9dbfe2538651fcac5`.
- Round-6 result SHA-256:
  `114c39895a48bb9e6ac79d778450ea30ab11a3f99894e171257e671f410a5a59`.
- P01 stable decision SHA-256:
  `7abc4b00714d0a216aa506cf3308d25a454443eb7316293ea05ec89f3d54a39a`.
- P01 terminal receipt-index SHA-256:
  `5781ab4a7ba23ff865847dd496839a4f827aee78462166606243ad4da591846a`.
- Golden canonical byte count/digest:
  `2375` /
  `f33683e1a14962db2c3713952311df87f34a84b0a75163b21ec1c526b4571d5e`.

## Local Pre-Review Evidence

- Skeptical audit passed for plan review: the baseline remains measured
  cross-label contamination rather than legacy test success; exact owned bytes,
  spans, identities, and digests remain primary; parser execution/counts are
  non-promotional; publication, backend execution, source edits, and Phase 03
  remain prohibited; failure, review, post-link, and chain stop conditions are
  explicit.
- Bootstrap compilation, strict parsing of both JSON files, and
  `git diff --check` passed. The formal
  `.local/mathdevmcp/evidence/p02-20260711` root remained absent.
- In a fresh `/tmp` mirror, repeated, extra, abbreviated, equal-sign, and
  positional invocations each exited nonzero and left the P02 root absent.
- In that mirror, the one exact invocation succeeded and wrote four entry
  files containing 15 immutable-input, 285 implementation, and 534 protected
  records. The two-record increase from the prior test is explained by the new
  R6 result and disposable synthetic R7 bootstrap review. A second exact
  invocation failed and all four file digests remained unchanged.
- Independent source materialization reproduced 17 complete obligations and
  unchanged materialized-oracle SHA-256 `ae7aa48...`.
- Combined contract audit passed: 26 actions, nine subprocess and 17 native;
  20 unique outcome transitions; 22 compile paths; exact 22/33/57-key
  entry/result/close schemas; nine nullable stage pairs; six representative
  terminal traces; 17 unique complete identities; golden canonical bytes 2375;
  93 must-change and five must-not-change mutations; 13 parser sources, seven
  fidelity fields, and both multi-label ambiguity routes.

Recompute material bindings and a representative cross-section rather than
trusting these statements. Do not create formal entry evidence.

## Review Questions

1. Does the two-token pre-parser guard exactly close the R6 repeated-option
   finding while accepting the sole profiled option/value invocation?
2. Are abbreviation, equal-sign syntax, repetition, missing value, positional
   value, unknown option, and extra argument rejected before root or file work?
3. Do bootstrap source and compact profile agree on argv, environment,
   review-ref grammar, fixed refs, manifests, write order, no-follow/no-replace,
   partial failure, and no-retry semantics?
4. Can any glob, latest-file selection, caller hash, caller ref override, dirty
   path escape, or unprotected input influence entry selection?
5. Does the entry bootstrap avoid circular dependence on unimplemented P02
   production schemas while binding its own source, agreeing review,
   pre-implementation bytes, immutable inputs, protected state, and sealed
   predecessor evidence?
6. Does the failure suffix close every reachable nonzero action and verified
   `REVISE` with a unique successor and no path back to candidate/publication?
7. Are source trigger index, current pre-repair index, pre-close index, and
   terminal close index distinct and correctly bound for early and late
   failures?
8. Can `bind_scoped_repair` and `close_round` execute once in process without
   recursion, nested receipts, subprocesses, arbitrary refs, or sequence
   conflicts, and can successors accept only the immediately prior close/index?
9. Are nullable stages, verdicts, logs, diagnostics, vetoes, non-claims, and
   repairs reconstructible without trusting booleans or narrative prose?
10. Is post-link publication failure fail-closed without retry, deletion,
    fabricated close, or false pass?
11. Are all action execution classes, handler/child nullability, exact argv,
    environment, artifact-ref grammar, binding keys, and compile paths mutually
    consistent and feasible?
12. Does `bind_result` independently reconstruct blocked/candidate state from
    raw receipts and artifacts, treating the Markdown footer only as a
    consistency assertion, including early-failure paths?
13. Do all 17 compact/materialized/source identities, source spans, grouping
    routes, parser-fidelity boundaries, mutation contracts, zero-backend/source
    rules, and publication quarantine remain closed and unchanged?
14. Are fixed tests, implementation allowlist, and protected-state checks
    feasible against the current dirty worktree without overwriting user work?
15. Do stop/handoff conditions retain every non-claim and prohibit Phase 03
    from a revised, closed, chain-failed, unaudited, or unpublished P02 round?
16. Identify wrong baselines, proxy promotion criteria, silent defaults, stale
    context, environment mismatches, infeasible primitives, unsupported claims,
    missing mutations, or boundary violations.

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
Reviewed entry bootstrap SHA-256: `<lowercase-64-hex>`
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
