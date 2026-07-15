# Phase 02 Independent Plan Review Bundle

Date: 2026-07-11

Review name: `mathdevmcp-real-document-remediation-p02-plan-r2`

Supervisor/executor: Codex

Reviewer: fresh independent Codex read-only reviewer; external Claude transport
is policy-denied, so no content is sent externally

## Role Boundary

READ-ONLY REVIEW ONLY. Bounded local inspection and digest/reconstruction
commands are permitted. Do not edit files, run implementation tests, execute
mathematical backends, launch agents, use network/external services, or change
state. Do not authorize publication, source edits, Phase 03, or a human/
product/scientific boundary.

## Objective

Determine whether the repaired Phase 02 subplan and predeclared extraction
oracle are consistent, correct, feasible, deterministic, fail-closed, and
complete enough to implement without choosing expected outputs after seeing
implementation behavior.

## Required Artifacts

- `docs/plans/mathdevmcp-real-document-remediation-phase-02-label-scoped-extraction-subplan-2026-07-11.md`;
- `docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json`;
- `docs/reviews/mathdevmcp-real-document-remediation-phase-02-plan-review-r1-result-2026-07-11.md`;
- the exact reviewed fixture files under
  `tests/fixtures/label_scoped_obligations/`;
- the four source artifacts named in the plan/oracle and the sealed P01
  predecessor pair;
- relevant current extraction/parser/governance source only where needed to
  assess feasibility and boundary safety.

Do not broaden into Phase 02 implementation or Phase 03 semantics.

## Round 1 Findings To Re-Audit

Round 1 returned `REVISE` against plan SHA-256
`c43e2d057c75564fafbcdae2fc4ad1d1391e9c7de20667b4d922b66a1f5cae9f`.
Its complete durable record is the review result listed above. The same plan
has now been visibly repaired, and pre-implementation fixtures/oracle were
created before any production source/test/governance implementation edit.

The proposed repairs are:

- a machine-readable oracle freezes exact bytes/digests, environment/label/
  owned/excluded spans, owned-span hashes, row shapes/reasons, normalized
  structures, inventories, extraction states, and ambiguity outcomes for
  positive/adversarial fixtures, four frozen equations, duplicate-file lookup,
  and the proposition container;
- a closed surface normalization, row-shape enum, deterministic allocation/
  conflict algorithm, nested-aligned exception, and fail-closed unknown route;
- a strict obligation schema, exact environment/row id formulas, complete
  identity payload, mutation contract, and independent 2,375-byte golden
  vector;
- a process-wide no-backend guard, independently reconstructed invocation and
  source-edit counts, immutable input and implementation manifests, explicit
  action argv/reconstruction profile, exact test nodes, and complete compile
  coverage;
- the handoff requires all four real equations and all positive fixtures to be
  exact `valid_complete`; only named adversarial cases may be ambiguous/
  orphaned, and the proposition is a non-target context container.

These are proposed repairs, not accepted facts. Audit actual bytes and internal
consistency rather than relying on this summary.

## Frozen Bindings

- Reviewed plan SHA-256:
  `8b0dcc49e71ee7dcadf5415e78602e070d49991013f5c7baf4106ff5e1a662b2`.
- Reviewed oracle SHA-256:
  `5d314b59d3c4936682803e5a01e5d00689b2a92572255214f103b804fe6f15c3`.
- Round-1 review SHA-256:
  `1ec17aa32265c4cc755de9638985c477c543ca6bcc01e295bcf77c87fdb0fa42`.
- P01 stable decision SHA-256:
  `7abc4b00714d0a216aa506cf3308d25a454443eb7316293ea05ec89f3d54a39a`.
- P01 terminal receipt-index SHA-256:
  `5781ab4a7ba23ff865847dd496839a4f827aee78462166606243ad4da591846a`.
- Golden canonical byte count/digest:
  `2375` /
  `f33683e1a14962db2c3713952311df87f34a84b0a75163b21ec1c526b4571d5e`.

Local pre-review checks report that JSON parsing, diff whitespace, all fixture/
frozen source hashes, every recorded owned-span hash, both derived golden ids,
and the golden canonical digest pass. Recompute material bindings rather than
trusting that statement.

## Review Questions

1. Does every reviewed case have enough frozen exact input/output to prevent
   implementation-shaped tests, including duplicate-file and adversarial
   cases?
2. Are byte-span conventions, row terminator handling, comments, non-ASCII,
   labels, numbering suppressors, nested environments, and environment stack
   identities mutually consistent in plan and oracle?
3. Is the row grammar and allocation algorithm deterministic, terminating,
   ownership-disjoint, and fail-closed, without silently importing semantic
   judgment from Phase 03?
4. Do the normalized target kinds/members, operator/symbol inventories, and
   expected real-document outputs follow the declared surface rules?
5. Is the strict obligation schema and identity payload non-circular, complete,
   canonically ordered, and independently testable from the golden vector?
6. Can exact source-file lookup coexist with a backward-compatible index
   without arbitrary duplicate-label selection?
7. Is parser fidelity evaluated by exact source/ownership evidence rather than
   availability, parse success, label counts, or output size?
8. Can the proposed guard and action profile actually establish zero
   mathematical backend requests while permitting bounded LaTeXML/Pandoc
   extraction comparison? Identify import/call/subprocess bypasses or false
   positives.
9. Are source-edit count, allowlist, protected-dirty preservation, and result/
   candidate/final reconstruction derived from raw artifacts rather than
   trusted summaries?
10. Do exact commands collect the intended nonzero tests, compile every
    possible changed Python path, preserve P00 quarantine/P01 integrity, and
    avoid existing tests that deliberately execute backends?
11. Are result review, final-seal audit, stable hard-link publication, failure
    closure, and terminal handoff non-circular and complete?
12. Do stop conditions and the Phase 03 handoff distinguish positive exact
    outcomes from reviewed ambiguity and preserve all non-claims?
13. Identify wrong baselines, proxy criteria, hidden defaults, stale context,
    infeasible primitives, unsupported claims, missing mutation cases, or
    commands whose artifacts cannot answer the engineering question.

## Required Output

Findings first, severity ordered, with exact file/line references. Distinguish
material execution blockers from optional improvements. Include exactly one
line for each binding below with the actual recomputed lower-case digest:

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
