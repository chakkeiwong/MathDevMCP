# Phase 01 Independent Plan Review Bundle

Date: 2026-07-11

Review name: `mathdevmcp-real-document-remediation-p01-plan-r4`

Supervisor/executor: Codex

Reviewer: fresh independent Codex read-only reviewer; external Claude transport
is policy-denied after informed approval and no content may be sent

## Role Boundary

READ-ONLY REVIEW ONLY. Bounded local inspection commands are permitted. Do not
edit files, run tests/backends, launch agents, use external services, or change
state. Do not authorize publication or any human/product/scientific boundary.

## Objective

Determine whether the Phase 01 subplan is consistent, correct, feasible,
complete, fail-closed, and properly bounded before any implementation edit.

## Required Artifacts

- `docs/plans/mathdevmcp-real-document-remediation-phase-01-evidence-integrity-subplan-2026-07-11.md`;
- master plan sections 239-318, 362-434, 481-559, 631-689, 746-795,
  1124-1166, and 1211-1242;
- sealed P00 decision and its recorded digest;
- current relevant source/tests listed in the subplan allowlist;
- `.gitignore`, `pyproject.toml`, and platform precheck facts as needed.

Do not broaden into P02+ implementation or real documents.

## Findings Resolved Before Round 1

- The master artifact tree/decision requirement was circular if the bundle
  index literally included itself and phase decisions. The subplan defines a
  payload-index seal DAG with explicit exclusions and separate semantic/file
  digests.
- Canonicalization is schema-path-aware, rejects floats/duplicates/surrogates,
  preserves exact byte artifacts, and keeps ordered fields ordered.
- Artifact I/O uses directory-fd/no-follow/no-overwrite primitives, not a
  resolve-then-open check.
- Complete v1 context is optional/additive; incomplete/root-level document
  attempts remain legacy/unbound. P04 owns branch-local scheduling and P05 owns
  backend conformance.
- Pure promotion is separated from I/O verification and cannot enable P00
  publication.
- The integration command uses exact synthetic P01 node ids; it does not use a
  broad keyword selector that would collect the repository-document FOC tests.
- The implementation allowlist compares entry/exit content manifests rather
  than `HEAD`, so unchanged sealed P00 dirty paths do not mask or create P01
  touches.
- The durable fake-only generator produces and verifies the payload bundle and
  matrices.

These are proposed resolutions, not facts. Audit them skeptically.

## Round 1 Repairs To Audit

Round 1 returned `VERDICT: REVISE` against the prior frozen plan digest. Its
complete result is
`docs/reviews/mathdevmcp-real-document-remediation-phase-01-plan-review-r1-result-2026-07-11.md`.
The same subplan was patched without any source/test/script edit:

- P01 claim eligibility is always `ineligible`; only the separate
  non-mathematical `integrity_binding_verified` status may pass for a synthetic
  fixture, and a document regression forbids `exact_manifest_eligible`.
- All execution/result/integrity/interpretation manifest groups, enum and
  consistency requirements, bounded fingerprint/redaction rules, and
  missing-field/adversarial tests are explicit.
- Candidate and final decisions are distinct immutable artifacts. Result review
  binds the candidate digest; an exact final-byte gate and fresh final-seal
  audit bind the new final decision without a self-reference cycle.
- A fail-fast pre-edit gate checks the commit, sealed P00 digest/content,
  publication mode, P00 agreeing review, exact agreed P01 plan digest,
  Python/SymPy identity, no-follow/directory-fd support, and absent optional
  packages before snapshots or implementation edits.
- Commands run complete P01 modules and all safe adapter/search/controller
  compatibility files. Document tests remain exact synthetic selectors.
- The run manifest now has a full reproducibility/external-tool ledger contract.

These too are proposed repairs. Check their actual consistency and feasibility;
do not assume the summary is correct.

## Round 2 Repairs To Audit

Round 2 returned `VERDICT: REVISE` against plan SHA-256
`ae5c9038ff2349803f8f44ecb3dc02ee877c95b1944fc3f317eb854f7ba93d4a`.
Its complete result is
`docs/reviews/mathdevmcp-real-document-remediation-phase-01-plan-review-r2-result-2026-07-11.md`.
The same subplan was repaired without any implementation/test/script edit:

- All result attempts are append-only `rr01` through `rr05` roots. Every early
  local failure, candidate failure, result-review revision, or final-seal
  revision gets a strict no-overwrite `round-close.json`; successors bind that
  close digest. Only an audited final-decision candidate may be hard-linked
  without overwrite to the stable handoff.
- Governance records and summaries have exact registered schemas, duplicate/
  extra/missing-key and canonical-byte rejection, no-overwrite writers, pure
  review/audit binding verification, and an internally revalidated stable-
  publication API with no caller-supplied authorization value.
- Source label is a required, typed, NFC-validated v1 identity field; mutation
  changes the request digest.
- The pre-review `src/tests/scripts` manifest covers 267 files and hashes to
  `cec60b546cfca5d66ebca64ecf6c27884e71435e07af1557506287d931aaa880`.
  The protected planning/P00 aggregate hashes to
  `6546f1423f373411dc98a7d968ca5f6200e00b4222c891368da101a52e04a333`.
  The pre-edit gate must reproduce both before creating any entry artifact.
- The entry gate binds both final plan bytes and this review-bundle's exact
  bytes to the agreeing review result. Commands use fail-fast shell settings,
  private umask, append-only roots, and an exact command ledger.

These are proposed repairs, not accepted facts. Audit the actual plan and
commands, including early-failure and post-audit branches.

## Round 3 Repairs To Audit

Round 3 returned `VERDICT: REVISE` against plan SHA-256
`fdfb9273629d9ca3f8b2cc99f43dfe30c81fb87ad8527095ab04c5654a77b69c`
and bundle SHA-256
`5dbce1d666bcc42733a907fad676e3295d336119defa063c2feb982deaa8fe36`.
Its complete result is
`docs/reviews/mathdevmcp-real-document-remediation-phase-01-plan-review-r3-result-2026-07-11.md`.
The same subplan was repaired without any implementation/test/script edit:

- Result rounds are allocated only after an independent shell bootstrap has
  passed exact governance tests, compilation, shell syntax, and diff checks.
  Failed bootstrap attempts retain diagnostic ledgers but create no close and
  cannot become predecessors. A passing close has a fixed ASCII grammar and is
  revalidated independently by shell and production Python.
- Every governance record and nested object now has a closed schema, including
  both entry aggregates, stage-dependent close nullability, scoped-repair input,
  command receipts/index entries, summaries, predecessor fields, and
  `rr0[1-5]` values.
- Review/audit records have closed unique-line grammars. Stable publication
  accepts no boolean, token, or caller-constructed authorization object; it
  reopens and recomputes every immutable input before creating the hard link.
- Every formal result-round action, construction, review/audit binding, close,
  and publication appends a canonical hash-chained receipt and immutable index.
  Result review binds the candidate-gate head, final audit binds the final-
  candidate-gate head, and Phase 02 requires the terminal publication head.
- Fixed per-action binding maps remove open receipt metadata. Exact safe test
  argv replace keyword selectors. Early failures bind the immutable code
  revision captured at `init-round` and consume a strict scoped-repair input.
- If the stable hard link exists but terminal receipt sealing fails, P01 claims
  no pass and P02 remains closed. No retry, deletion, or overwrite is allowed.

These are proposed repairs, not accepted facts. Audit the exact schemas,
commands, failure transitions, circularity boundaries, and publication edge
case rather than relying on this summary.

## Frozen Inputs

- P01 subplan SHA-256:
  `d97b993da484c527f276fd75288130d619c2d5688725ceed8267ddc1b061ded2`.
- Frozen implementation-tree aggregate SHA-256:
  `cec60b546cfca5d66ebca64ecf6c27884e71435e07af1557506287d931aaa880`
  over 267 non-cache files.
- Frozen protected planning/P00 aggregate SHA-256:
  `6546f1423f373411dc98a7d968ca5f6200e00b4222c891368da101a52e04a333`.
- Sealed P00 decision SHA-256:
  `2b44b9ae8fe3f8fcce4f7903fd206a5279326212374b73dba9af59bb476592ea`.
- Local structural/work-package/fence/digest/diff checks pass after the repair.
- No P01 implementation or test/script edit has occurred.

## Review Questions

1. Does the seal DAG avoid every circular digest while still indexing every
   artifact relevant to exact binding?
2. Are canonical bytes, set-like paths, numbers, Unicode, exact bytes, ids, and
   logical paths specified tightly enough for independent implementation?
3. Can the filesystem contract be implemented safely with the observed Linux/
   Python primitives, including concurrency and crash behavior?
4. Does P01 avoid fabricating v1 identity from current root attempts and avoid
   pulling P02 extraction, P04 scheduling, P05 conformance, or P06 publication
   forward?
5. Are pure verification/promotion authority and legacy compatibility
   unambiguous and fail-closed?
6. Do tests, durable artifacts, logs, commands, allowlist, vetoes, stop
   conditions, rollback, and next-phase handoff fully cover P01-W1 through W5?
7. Identify wrong baselines, proxy criteria, hidden defaults, stale context,
   unsupported claims, infeasible primitives, missing adversarial cases, or
   commands whose artifacts cannot answer the question.
8. Do the candidate/result-review/final-decision/final-seal relationships bind
   exact immutable bytes without either circularity or an unreviewed pass?
9. Does the fail-fast entry command actually enforce every material entry
   condition before any implementation snapshot/edit, and are all selected
   compatibility commands safe within P01's fake/synthetic boundary?
10. Does every failure point have a no-overwrite, digest-bound successor path,
    and can the stable handoff be created only from an exact independently
    audited candidate with no raw-boolean bypass?
11. Are the exact governance schemas sufficiently closed and are their strict
    validators used at every decision/review/audit boundary?
12. Recompute the two frozen baseline aggregates and confirm they match before
    issuing a verdict. Report both the reviewed plan and reviewed bundle
    SHA-256 values in the result.
13. Does the bootstrap independently establish enough governance correctness to
    allocate a formal round, and can every later failure either produce a
    canonical predecessor close or stop explicitly as a governance-chain
    failure without manufacturing evidence?
14. Is every formal action represented in one non-circular receipt/index chain,
    including result construction, review/audit admission, close, stable hard-
    link publication, and the terminal Phase 02 handoff?

## Required Output

Findings first, severity ordered, with exact file/line references. Distinguish
material plan defects from clerical drift. Include exactly one full line for
each of these four bindings, with the actual lower-case digest substituted:

```text
Reviewed plan SHA-256: `<lowercase-64-hex>`
Reviewed bundle SHA-256: `<lowercase-64-hex>`
Implementation aggregate SHA-256 confirmed: `<lowercase-64-hex>`
Protected aggregate SHA-256 confirmed: `<lowercase-64-hex>`
```

Do not repeat or quote any reserved binding prefix elsewhere. End with exactly
one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
