# Phase 02 Independent Plan Review Round 3 Bundle

Date: 2026-07-11

Review name: `mathdevmcp-real-document-remediation-p02-plan-r3`

Supervisor/executor: Codex

Reviewer: fresh independent Codex read-only reviewer; external Claude transport
is policy-denied, so no content is sent externally

## Role Boundary

READ-ONLY REVIEW ONLY. Bounded local inspection and digest/reconstruction
commands are permitted. Do not edit files, run production implementation or
mathematical backends, launch agents, use network/external services, or change
state. Do not authorize publication, source edits, Phase 03, or a human,
runtime, product, funding, model-file, or scientific-claim boundary.

## Objective

Determine whether the repaired Phase 02 subplan and predeclared extraction
oracle are consistent, correct, feasible, deterministic, fail-closed, and
complete enough to implement without choosing expected outputs after seeing
implementation behavior.

## Required Artifacts

- `docs/plans/mathdevmcp-real-document-remediation-phase-02-label-scoped-extraction-subplan-2026-07-11.md`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json`;
- `docs/reviews/mathdevmcp-real-document-remediation-phase-02-plan-review-r1-result-2026-07-11.md`;
- `docs/reviews/mathdevmcp-real-document-remediation-phase-02-plan-review-r2-result-2026-07-11.md`;
- the exact reviewed fixture files under
  `tests/fixtures/label_scoped_obligations/`;
- the frozen source files, sealed P01 predecessor pair, and relevant current
  extraction/parser/governance code only where needed to assess feasibility and
  boundary safety.

Do not broaden into Phase 02 implementation or Phase 03 semantics.

## Prior Findings And Claimed Repairs

Round 1 and round 2 both returned `REVISE`. Their durable result records above
are authoritative. Round 2 found three material blockers; the current bytes
claim these visible repairs:

1. The plan now freezes operator patterns, command tokenization and exclusion,
   bare-identifier preprocessing/regex/exclusion, ordering, uniqueness, input
   scope, and NFC/case/macro policies. The oracle independently carries the
   same closed machine-readable registry at `inventory_scanner`.
2. Every reviewed non-valid case now freezes full ambiguity objects with exact
   code, source spans, candidate interpretations, and required discriminator;
   every reviewed case freezes an exact uncertainties array.
3. The golden identity vector now gives an RFC 6901 mutation protocol, an
   explicit non-identity envelope, 93 must-change paths covering every nested
   leaf and empty identity container plus top-level/nested objects, and five
   must-not-change paths. Mutation hashing may not filter unknown keys;
   strict-schema rejection is tested separately.

These are claims to audit, not accepted facts. Recompute and inspect actual
bytes. In particular, look for semantic disagreement between plan prose and
the machine registry, mutation paths that cannot be executed as specified,
incomplete oracle records, or fixes that merely restate rather than close a
finding.

## Frozen Bindings

- Reviewed plan SHA-256:
  `92c3965c7401fd7f962e8d2f362bf9aae55378ac3b858a54871789b51abfa95c`.
- Reviewed oracle SHA-256:
  `c4b267b10a3beaa6476664954089eb12fe39f36d84b5ebfd7b9e5003e97402e4`.
- Round-1 result SHA-256:
  `1ec17aa32265c4cc755de9638985c477c543ca6bcc01e295bcf77c87fdb0fa42`.
- Round-2 result SHA-256:
  `45e4404d95cd22bf8be66e447755647d540decfdf2e9d87dddba1c3adad4459f`.
- P01 stable decision SHA-256:
  `7abc4b00714d0a216aa506cf3308d25a454443eb7316293ea05ec89f3d54a39a`.
- P01 terminal receipt-index SHA-256:
  `5781ab4a7ba23ff865847dd496839a4f827aee78462166606243ad4da591846a`.
- Golden canonical byte count/digest:
  `2375` /
  `f33683e1a14962db2c3713952311df87f34a84b0a75163b21ec1c526b4571d5e`.

Local pre-review checks report valid JSON, clean `git diff --check`, exact
inventory equality for all 17 expected targets, exact hashes for 15 source
bindings and 20 owned spans, recomputation of both derived ids and the golden
canonical vector, 93 must-change digest mutations, five identity-exclusion
mutations, and complete golden leaf/empty-container path coverage. Recompute
material bindings rather than trusting this statement.

## Review Questions

1. Do the three round-2 repairs close the actual findings without creating a
   new contradiction or implementation-defined choice?
2. Does every reviewed case freeze enough exact input and output to prevent
   implementation-shaped tests, including duplicate-file and adversarial
   cases?
3. Are byte-span conventions, row terminator handling, comments, labels,
   numbering suppressors, nested environments, and environment-stack identity
   mutually consistent in plan and oracle?
4. Is the row grammar/allocation algorithm deterministic, terminating,
   ownership-disjoint, and fail-closed without importing Phase 03 semantics?
5. Do normalized target kinds/members and every expected inventory follow the
   closed machine scanner exactly, including non-obvious command exclusions and
   underscore behavior?
6. Is the strict obligation schema and identity payload non-circular,
   complete, canonically ordered, and exhaustively mutation-testable?
7. Can exact source-file lookup coexist with compatibility behavior without
   arbitrary duplicate-label selection?
8. Does parser selection use exact source/ownership fidelity rather than
   availability, parse success, label counts, or output size?
9. Can the guard and fixed action profile establish zero mathematical backend
   requests while permitting only the bounded parser subprocesses? Identify
   bypasses, false positives, or commands whose artifacts cannot prove this.
10. Are source-edit count, allowlist, protected-dirty preservation, result
    reconstruction, review binding, final audit, and stable publication derived
    independently and non-circularly?
11. Do exact commands collect the intended nonzero tests, compile every
    possible changed Python path, preserve P00/P01, and avoid backend-executing
    tests?
12. Do the stop/handoff conditions require the four frozen equations to be
    exact valid obligations, keep the proposition a context container, and
    preserve all non-claims?
13. Identify wrong baselines, proxy promotion criteria, hidden defaults, stale
    context, infeasible primitives, unsupported claims, missing mutation cases,
    or boundary violations.

## Required Output

Findings first, severity ordered, with exact file/line references. Distinguish
material execution blockers from optional improvements. If no material finding
remains, state that explicitly and identify residual risks or later
implementation checks without converting them into blockers.

Include exactly one line for each binding below with the actual recomputed
lower-case digest:

```text
Reviewed plan SHA-256: `<lowercase-64-hex>`
Reviewed oracle SHA-256: `<lowercase-64-hex>`
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
