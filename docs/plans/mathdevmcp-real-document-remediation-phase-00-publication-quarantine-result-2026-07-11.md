# Phase 00 Result: Publication Quarantine And Adversarial Safety

Date: 2026-07-11

Status: `PASS`

## Outcome

Phase 00 implemented a fail-closed document publication boundary. Raw
lower-level backend evidence remains visible once per branch as diagnostic
history, while every generic document promotion is false, every document repair
flag is false, and every retained candidate text is explicitly blocked and
non-applicable.

Apparent backend closure now compiles as a `document_partial_evidence_report`
with an evidence-binding veto. Ordinary open mathematical paths remain
actionable `document_gap_report` records. Adapter and target-worker failures are
distinguished as `engineering_error`.

Result-review repair round 1 also makes a ready-shaped edit/target mismatch
independently observable: only the mismatching control receives
`edit_target_mismatch`, classified as `evidence_binding_error`, while both
controls remain under the separate global publication veto.

Independent result review converged in round 3 with `VERDICT: AGREE`. Phase 00
is sealed as a bounded publication-quarantine pass; this does not relax any
non-claim or re-enable publication.

## Decision Table

| Decision | Primary criterion | Veto diagnostics | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| `pass` | Pass: effective promotion `0`, ready repairs `0`, true repair flags `0`, applicable edit keys `0`; mismatch veto and partial/gap diagnostics remain visible. | All predeclared vetoes false; independent result review round 3 agreed. | Synthetic Phase 00 scope does not exercise real-document shapes or backend conformance. | Draft and independently review the just-in-time Phase 01 subplan using the sealed P00 decision digest. | No exact binding, real-document capability, backend breadth, release readiness, or publication re-enablement. |

## Baseline And Change

Baseline commit: `a85fbb676eb4d551a8d78a70a5043524f308b7b9`.

Before implementation, the existing synthetic simple-algebra test passed while
requiring one ready repair with `publishable_as_repair=true` and no remaining
blocker ids. The recorded baseline test took 11.12 seconds.

After implementation, the same raw SymPy success is retained, but:

- document `publication_mode` is `disabled`;
- target status is `partial_evidence` rather than generic `proved`;
- effective `promoted_count` is `0`, while diagnostic `raw_promoted_count` is
  `1`;
- ready repair and publishable-repair counts are `0`;
- one partial-evidence item carries `legacy_unbound_document_evidence` and
  non-applicable candidate text;
- no `proposed_edit` or `proposed_text` key appears on a public document result.

Bounded evidence:

- `.local/mathdevmcp/evidence/p00-20260711/summaries/simple-algebra-before-after.json`
- `.local/mathdevmcp/evidence/p00-20260711/summaries/adversarial-summary.json`

## Implementation

| Path | Phase-local change |
| --- | --- |
| `src/mathdevmcp/document_derivation_tree.py` | Added document publication mode/vetoes, closed raw/effective promotion schema, legacy-unbound attempt views, partial-evidence compiler, non-applicable candidate fields, failure classes, compact/Markdown propagation, and emergency early-return kill switch. |
| `src/mathdevmcp/assumption_discovery.py` | Extended the existing square-root route-assumption rule to recognize canonical LaTeX `\sqrt{...}` syntax. |
| `tests/test_document_publication_quarantine.py` | Added synthetic adversarial, recursive-schema, surface-parity, failure, collision/mismatch, kill-switch, and lower-level-boundary tests. |
| `tests/test_document_derivation_tree.py` | Replaced unsafe publication assertions with the Phase 00 quarantine contract and updated blocked-candidate/raw-effective field expectations. |

No CLI, MCP facade, MCP server, lower-level controller, external adapter,
manifest/store, source-document, or real-document fixture was edited.

## Evidence Contract Assessment

| Contract field | Result |
| --- | --- |
| Question | Answered for the synthetic Phase 00 scope: document repair publication is disabled while diagnostic output remains structured. |
| Baseline | Reproduced before implementation: simple algebra published one repair. |
| Primary criterion | Passed in focused recursive and surface tests. |
| Veto diagnostics | All false in the candidate decision. |
| Explanatory only | Raw backend success, test counts, tool availability, and report counts were not used to override vetoes. |
| Non-claims | Preserved in result, summaries, code output, and decision. |

## Adversarial Evidence

| Fixture | Raw evidence | Effective outcome | Preserved requirement/failure class |
| --- | --- | --- | --- |
| Simple commutativity | SymPy raw promotion true | Partial evidence, no repair | `evidence_binding_error`; open formalization remains `mathematical_blocked` |
| `x / x = 1` | SymPy raw promotion true | Partial evidence, no repair | `denominator is nonzero`; binding and mathematical blockers |
| Canonical LaTeX `\sqrt{x}^{2}=x` | No effective promotion | Gap report | square-root argument nonnegative in target domain |
| Two distinct targets | Same legacy attempt id reproduced | Neither target promotes | `legacy_unbound` per branch |
| Matching and mismatching ready-shaped edits | Direct compiler-boundary controls | Both repair flags false | only mismatch receives `edit_target_mismatch` and `evidence_binding_error`; both retain publication veto |
| Adapter exception | Diagnostic attempt | Blocked | `engineering_error` |
| Serial/parallel worker exceptions | No completed target audit | Blocked | `engineering_error` |
| Library/CLI/facade/server/Markdown | Same synthetic input | Parity on disabled/zero repair | recursive raw/effective schema |
| Emergency kill switch | Missing input path | Pipeline not entered | explicit disabled engineering status |

## Verification

| Check | Result | Evidence |
| --- | --- | --- |
| Focused Phase 00 gate | `11 passed` in 96.50 s | `.local/mathdevmcp/evidence/p00-20260711/logs/focused-tests.log` |
| Selected synthetic surface gate | `7 passed, 7 deselected` in 65.73 s | `.local/mathdevmcp/evidence/p00-20260711/logs/surface-tests.log` |
| Standalone compatibility | `34 passed` in 0.20 s | `.local/mathdevmcp/evidence/p00-20260711/logs/adjacent-compatibility-tests.log` |
| Python compile | Exit `0` | `.local/mathdevmcp/evidence/p00-20260711/logs/compile-check.log` |
| Assignment audit | Exit `0`, 114 matched lines inspected | `.local/mathdevmcp/evidence/p00-20260711/logs/assignment-audit.log` |
| Protected dirty hashes | Six pre-existing dirty paths all `OK` | `.local/mathdevmcp/evidence/p00-20260711/logs/protected-dirty-check.log` |
| Implementation allowlist | Four expected paths; zero unexpected paths | `.local/mathdevmcp/evidence/p00-20260711/logs/touched-files.log` and `.local/mathdevmcp/evidence/p00-20260711/logs/unexpected-touched-files.log` |
| Diff hygiene | Exit `0` | `.local/mathdevmcp/evidence/p00-20260711/logs/diff-check.log` |

The six repository-document tests in `tests/test_document_derivation_tree.py`
were not run. This was deliberate: Phase 00 prohibits real-document execution.

## Independent Result Review And Repair

Round 1 returned `VERDICT: REVISE`. It found that the mismatch fixture proved
only global quarantine and that the result mentioned an unmanifested
supplementary test count. Repair round 1 added an explicit target comparison to
both ready-proposal validation and compiled-item classification, added a
matching control, removed the unsupported count, and regenerated every declared
runtime/static artifact. At that point the candidate awaited round-2 review;
Phase 00 was not sealed and Phase 01 remained closed.

Round 2 found no material implementation defect and confirmed the mismatch
repair, counts, and digests. It returned `REVISE` for a clerical evidence-scope
error: the suite exercises local SymPy on synthetic fixtures, so “no real
external backend” was inaccurate. Repair round 2 now records that synthetic
SymPy execution while preserving the actual boundaries: no backend ran on a
real document, no Sage or Lean route ran, and no adapter-conformance claim is
made. The post-repair focused gate passed `11` tests in 96.50 seconds. The
round-3 reviewer found no material or clerical defects and returned
`VERDICT: AGREE`.

## Run Manifest

Manifest:
`.local/mathdevmcp/evidence/p00-20260711/run-manifest.json`.

Key fields:

- commit: `a85fbb676eb4d551a8d78a70a5043524f308b7b9`;
- Python: `/home/chakwong/miniconda3/envs/tfgpu/bin/python3`, version 3.11.15;
- execution: CPU engineering tests; no GPU/CUDA command requested or
  initialized;
- data: deterministic synthetic source-local LaTeX fixtures;
- seeds: not applicable;
- backend scope: existing local SymPy paths ran on synthetic fixtures only; no
  backend ran on a real document, no Sage or Lean route ran, and no backend-
  conformance run occurred;
- forbidden actions: no real-document run, installation, network fetch, source
  edit, commit, push, or GPU command.

## Ledgers

| Ledger | Result |
| --- | --- |
| Engineering correctness | Candidate pass: focused, surface, compatibility, compile, recursive schema, kill-switch, protected-dirty, allowlist, and diff checks pass. |
| Mathematical/numerical validity | No new theorem or numerical-validity claim. Domain-sensitive assumptions remain open and visible; raw CAS success is not document proof. |
| Scientific/product interpretation | Publication quarantine is established only for the tested document workflow/surfaces. Capability, correctness of future exact binding, and release readiness remain unestablished. |

## Post-Run Red Team

Strongest alternative explanation: the recursive synthetic fixtures could still
miss a document-output path that is constructed only by a real source shape or
an optional integration. This does not overturn the quarantine implementation,
but it limits evidence to the Phase 00 synthetic contract and is why real-
document capability is not claimed.

Evidence that would overturn the candidate decision:

- any public result containing `publishable_as_repair=true`;
- `can_promote=true` outside the sole allowlisted branch raw-history path;
- `raw_promotion` or `raw_promoted_count` at any unapproved path;
- any `proposed_edit` or `proposed_text` key in document output;
- a lost nonzero/square-root assumption;
- an adapter/worker error reported only as mathematics;
- surface disagreement or modification of protected/unapproved paths.

Weakest evidence: CLI/MCP parity uses existing pass-through delegation and
synthetic subprocess/in-process calls; no protocol-level external MCP client or
real source corpus was run in Phase 00.

## Negative-Result Discipline

No scientific negative result is claimed. The reproduced legacy id collision
and edit mismatch are engineering/evidence-binding failures, not evidence
against symbolic checking or proof search. Their Phase 00 treatment is
containment; Phase 01 owns exact identity and binding repair.

## Non-Claims

- No backend attempt is a live document certificate.
- Phase 01 evidence manifests and exact binding do not exist yet.
- Phase 02 extraction fidelity, Phase 03 typed semantics, Phase 05 backend
  breadth, and Phase 06 final action selection are not established.
- Local SymPy ran only on synthetic fixtures; no backend ran on a real
  document, and no Sage, Lean, or backend-conformance run occurred.
- No source edit was applied.
- No default publication re-enablement, release readiness, or scientific claim
  is authorized.

## Sealed Handoff

Sealed `P00-decision.json` SHA-256:
`2b44b9ae8fe3f8fcce4f7903fd206a5279326212374b73dba9af59bb476592ea`.

Phase 01 may be planned, but not implemented, only after the final P00 decision
digest is recorded below and consumed as an explicit entry artifact. Phase 01
must keep document publication disabled, implement exact evidence identity and
binding without treating quarantine as evidence integrity, pass its own
skeptical/default audit, and converge in independent plan review before edits.
