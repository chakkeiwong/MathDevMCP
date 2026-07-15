# MathDevMCP P08C1 Target-Fidelity Review R2

Read-only review. Codex is supervisor/executor. Do not edit or run commands.

The R1 probe returned `OK`, but its broad primary prompt timed out; bounded
fallback `AGREE` is insufficient. This R2 intentionally asks only two material
questions.

## Claim Under Review

Focused equation labels can no longer enter document audit as physical locator
rows or enclosing displays. They enter as exact P08A-compatible label-scoped
obligations, and the passing replay verifies all five obligation records and
their typed-tree inputs. This authorizes only refreshing P08D's payload
baseline, not proof, publication, default, release, or Phase 08 closure.

## Inspect Only

1. `src/mathdevmcp/document_derivation_tree.py:2334-2414`
   (`_requested_equation_labels`, `_select_label_scoped_targets`).
2. `src/mathdevmcp/document_derivation_tree.py:2540-2698`
   (`_semantic_packet_from_label_scoped_target`).
3. `src/mathdevmcp/document_derivation_tree.py:3275-3345`
   (`_target_result_for_row`).
4. `src/mathdevmcp/document_derivation_tree.py:3535-3575`
   (audit ingress wiring).
5. `scripts/run_p08c1_target_fidelity_replay.py:204-297`
   (exact audit/packet/typed-tree validator).
6. `scripts/run_p08c1_target_fidelity_replay.py:375-404` and
   `scripts/run_p08c1_target_fidelity_replay.py:496-548`
   (comparison reconstruction and verify).
7. `tests/test_document_derivation_real_regressions.py:76-169` and
   `tests/test_document_derivation_tree.py:187-205`.
8. `.local/mathdevmcp/evidence/p08-20260714/p08c1/20260714T121103Z-fc7811786801/target-fidelity.json`
   (6,202 bytes) and `decision.json` (1,199 bytes).

Current identities: document workflow
`bfca60ab36e83bda0dd53426fa5a87ba32912e794a87afa6808012ff0fc44b48`;
replay runner
`93481a566c0f49e1b2e266040630e9509d998193abbd39f52536324fd6df58a5`;
fidelity record
`4fd07445dd796fba570fe46c9fa6daf4362ba5f12a740b64ff942a0cea81872b`.

## Questions

1. Is there any path in these regions by which a focused equation label can be
   accepted as an incomplete locator row, absorb sibling mathematics, be
   duplicated/reordered, or be counted covered after validated extraction
   fails?
2. Can the replay/verify logic pass while any of target, lhs/rhs, exact
   obligation record/identity, spans, inventories, order, or typed-tree input
   differs from P08A, or while a partial failed attempt is treated as passing?

Report only material findings with file/line citations. Style and the known
fact that this is not mathematical proof are non-findings. End exactly with:

`VERDICT: AGREE` or `VERDICT: REVISE`.
