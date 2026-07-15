# Phase 02R2 Recovery Plan Review R11 Bundle

Date: 2026-07-12

Review name: `mathdevmcp-p02r2-recovery-plan-r11`

Supervisor/executor: Codex

Role: read-only material plan review. Do not edit files, create the P02R2
evidence root, run parser jobs, launch mathematical backends, use network or
install tools, or authorize publication, source edits, Phase 03, product
capability, funding, model-file, or scientific claims.

## Objective

Determine whether the additive Phase 02R2 recovery plan, machine overlay, and
one-shot bootstrap consistently repair the runtime-discovered parser-contract
contradiction while preserving the frozen R9 plan/oracles/materialized
identities and old sealed entry.

The core policy is:

- current byte-preserving source reconstruction is primary but must pass exact
  compact/materialized/source and mutation evidence;
- LaTeXML and Pandoc remain required exact-profile external diagnostics;
- malformed or non-source-mappable output is a visible capability limitation,
  blocks that specialist's promotion, and does not alone refute exact current
  reconstruction;
- a valid independently supported specialist contradiction on any declared
  observable field remains a phase veto;
- current/oracle-derived source spans cannot be relabeled as specialist
  evidence;
- publication remains disabled and mathematical backends remain forbidden.

## Review Artifacts

Read completely:

1. `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-capability-scoped-parser-recovery-subplan-2026-07-12.md`;
2. `docs/plans/mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json`;
3. `docs/plans/p02r2_entry_bootstrap_20260712.py`;
4. `docs/reviews/mathdevmcp-real-document-remediation-phase-02-runtime-parser-contract-review-r10-result-2026-07-11.md`;
5. `docs/plans/mathdevmcp-real-document-remediation-phase-02-pre-round-parser-contract-blocker-result-2026-07-11.md`.

Inspect the frozen base plan/oracle/materialized oracle, frozen R9 bootstrap,
old entry, or current parser implementation only where needed to verify exact
bindings, patch baselines, feasibility, and non-circularity. Do not broaden
into general Phase 02 implementation review.

## Exact Bindings

- Recovery plan SHA-256:
  `4aa494feea22369eab6c6137e6d873d5a65cb37a2f4906f5cf2217d623a63b16`.
- Recovery oracle SHA-256:
  `d478b2bb8cd0d595df5ed823e5377d6b99ed229cd4a2cdbf7ef6f9b83b44a870`.
- Recovery bootstrap SHA-256:
  `bf28573a42bda21050783de25f17616a53e9649a35919c175c97489e2bbc04f8`.
- Base plan SHA-256:
  `3f9cb7ce3c70bdb2b06f41a1ec1510658044c3a3f33acb1593005c2ca2c7c2c8`.
- Base compact oracle SHA-256:
  `3b5792cd82992402e58b6826d6d9b897fa097a7d369e540053179c6a9b910b1c`.
- Materialized oracle SHA-256:
  `ae7aa48fb8c475c7c37c75158a9ed6f83b21a686bc8cd8ca2b28c79b36bcb1ad`.
- Prior entry SHA-256:
  `91acda4ce19058350bb3b40500ac33e46b785f8f29d3e1cfe0a8fbe90b2f4e79`.

## Local Pre-Review Evidence

- Recovery bootstrap compiles.
- Recovery oracle strict JSON parses with 33 unique entry keys, 11 unique
  exact baseline patches, nine unique capability states, seven observable
  fields, and status precedence equal to the status enum.
- Every patch pointer resolves and its expected base value matches the frozen
  compact oracle.
- Reused frozen-bootstrap validators independently reopen and validate all 13
  reviewed sources and all 17 materialized source/environment projections.
- Old entry and its protected/immutable manifests reopen and match current
  bytes.
- New P02R2 root and old Phase 02 `rr01` are absent.
- Recovery control files pass `git diff --check`.

These are local checks, not authority to agree.

## Review Questions

1. Does the additive overlay enumerate every semantic/path change needed, with
   all unlisted base fields remaining exact, or can stale old-root/ref/parser
   semantics leak into effective execution?
2. Is the capability contract coherent for malformed,
   valid-not-source-mappable, and valid-source-mappable results, including
   deterministic status precedence and exact field/nullability rules?
3. Can a non-source-mappable but structurally valid specialist expose an
   independently supported contradiction without becoming promotion-eligible?
4. Does the independence rule prevent circular use of current/oracle spans,
   including through tests, post-processing, or source-text lookup seeded by
   expected positions?
5. Are malformed LaTeXML exit-zero outputs classified before any observation,
   while valid Pandoc raw math can remain capability-limited without being
   treated as agreement?
6. Does the revised veto distinguish capability absence from a genuine
   contradiction without weakening current-parser exactness, invocation/raw
   evidence, source-mutation, or unjustified-selection vetoes?
7. Does the new namespace preserve the old entry as immutable diagnostic
   predecessor rather than silently reinterpret it as a pass?
8. Does the one-shot bootstrap reject pre-existing/partial state, bind every
   recovery/frozen/P01 input, enforce R11-R14 sequence and digests, and
   reconstruct complete implementation/protected/immutable scopes after
   writing?
9. Is reuse of the exact frozen R9 bootstrap source as a read-only validator
   explicit, digest-bound, non-circular, and limited to appropriate functions?
10. Can any review selector, `runpy`, JSON parser, glob, symlink, dirty-path,
    manifest, environment, argv, or namespace edge bypass the entry gate?
11. Are the evidence contract, default audit, tests, disposable dry-run gate,
    failure closure, review/final gates, and stop/handoff conditions sufficient
    and feasible?
12. Identify wrong baselines, proxy promotion, hidden defaults, stale context,
    unfair comparisons, unsupported claims, commands whose artifacts do not
    answer the question, or any material implementation invention left open.

## Required Output

Findings first, severity ordered, with exact file/line references. Distinguish
material blockers from optional improvements. If a material problem is
fixable, return `REVISE`; do not redesign files yourself.

Include exactly these seven recomputed binding lines:

```text
Reviewed recovery plan SHA-256: `<lowercase-64-hex>`
Reviewed recovery oracle SHA-256: `<lowercase-64-hex>`
Reviewed recovery bootstrap SHA-256: `<lowercase-64-hex>`
Reviewed base plan SHA-256: `<lowercase-64-hex>`
Reviewed base compact oracle SHA-256: `<lowercase-64-hex>`
Reviewed materialized oracle SHA-256: `<lowercase-64-hex>`
Reviewed prior entry SHA-256: `<lowercase-64-hex>`
```
End with exactly one final line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
