# Phase 02R2 Timeout-Veto Adjudication Result

Date: 2026-07-12

Reviewer: fresh independent Codex read-only reviewer

Status: `ADDITIVE_P02R3_REQUIRED`

## Finding

The sealed Phase 02R2 contract is internally inconsistent on the measured
LaTeXML timeout case.

- The recovery plan makes `source mutation, timeout, or unclassified nonzero
  exit` a parser veto at
  `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-capability-scoped-parser-recovery-subplan-2026-07-12.md:225`.
- The same plan forbids letting absent or otherwise limited specialist output
  alone refute exact current reconstruction at
  `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-capability-scoped-parser-recovery-subplan-2026-07-12.md:421`.
- The recovery oracle explicitly replaces the inherited timeout-veto rule with
  a narrower rule under which a correctly classified specialist limitation
  alone blocks that specialist but does not refute exact current reconstruction
  at
  `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json:255`.
- The oracle's `limitation_boundary` and `contradiction_rule` permit a parser
  veto for evidence/provenance failure or a valid independently observed
  requested-label contradiction, neither of which occurred in the disposable
  profile.

The plan makes exact oracle patches authoritative against inherited Phase 02
values, but it does not establish precedence between the recovery oracle and
contradictory prose inside the same sealed P02R2 plan. A code-only repair would
therefore choose a veto policy after observing real output. That exceeds the
earlier implementation-closure authority and is not permitted.

## Required Action

Use an additive P02R3 plan, oracle, evidence namespace, and one-shot entry. The
new contract must explicitly state whether a correctly classified `timed_out`
or classified nonzero-exit limitation, with exact invocation/source evidence
and no independent contradiction, blocks only specialist promotion or also
sets the phase veto. Preserve the P02R2 plan, oracle, entry, and disposable
diagnostic evidence unchanged.

## Non-Claims

- The current byte-preserving scanner is not refuted.
- LaTeXML is not generally unsuitable for mathematical documents.
- A timeout is not agreement, proof, source mapping, or parser promotion
  evidence.
- The disposable run is not a formal Phase 02 result round.
- Phase 02 has not passed and Phase 03 is not authorized.

VERDICT: ADDITIVE_P02R3_REQUIRED
