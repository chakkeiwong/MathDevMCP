# Phase 06 Claim-Boundary Repair Rereview Bundle

Date: 2026-07-14

Supervisor/executor: Codex

Reviewer: fresh read-only Codex reviewer

## Role Boundary

Review only. Do not edit files, launch backends or agents, use network/GPU/model
APIs, or authorize publication, Phase 07, release, defaults, or scientific
claims. Inspect only the artifacts listed below. Ignore unrelated dirty
worktree changes.

## Objective

Determine whether the four `HIGH` findings in the Phase 06 R1 review are
materially repaired without weakening validity-gated ranking or product
publication quarantine.

## Artifacts

- `docs/reviews/mathdevmcp-real-document-remediation-phase-06-result-review-r1-result-2026-07-14.md`
- `src/mathdevmcp/external_adapter_contract.py`
- `src/mathdevmcp/sage_adapter.py`
- `src/mathdevmcp/derivation_branch_controller.py`, specifically
  `_phase06_ranking_input()` and `rank_repair_branches()`
- `src/mathdevmcp/promotion_policy.py`, specifically
  `evaluate_phase06_promotion()` and `verify_phase06_promotion_decision()`
- `src/mathdevmcp/document_derivation_tree.py`, specifically
  `_validate_ready_proposal()`
- `tests/test_claim_evidence_normalization.py`
- `tests/test_sage_adapter.py`
- `tests/test_phase06_promotion_policy.py`

Do not inspect historical P00-P05 governance artifacts or the whole repository.

## Implemented Repair Claims To Challenge

1. `RevalidatingClaimEvidence` is only an immutable snapshot of reader inputs.
   Construction confers no authority. Every call to
   `reader_verified_claim_evidence_record()` reruns the generic or registered
   native reader against current artifacts.
2. Ranking accepts evidence separately by branch id and grants exact evidence
   only after complete Phase 04 branch validation plus exact lineage, branch
   content digest, obligation, target, typed assumptions, and assumption-digest
   equality. Legacy branch payload fields cannot carry evidence authority.
3. The Sage reader reconstructs `SagePolynomialObligation` from the verified
   request/payload, regenerates the exact script with the bound version prefix,
   requires byte-for-byte equality, and emits reader-derived assumption
   encoding digests/references. Registered normalization consumes only that
   projection.
4. Persisted promotion decisions use the closed v2 schema and authority marker
   `internal_consistency_only_requires_native_evidence_reevaluation`. The
   verifier validates edit bytes/digest, manifest refs, sorted unique id sets,
   typed-veto consistency, exact decision/eligibility/veto/reason
   reconstruction, and a true deterministic-reconstruction invariant.
   Product repair validation explicitly rejects persisted-only authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can caller-controlled, replayed, redigested, or persisted-only data still obtain exact-evidence or repair authority? |
| Baseline | The four R1 `HIGH` findings above. |
| Primary criterion | Each finding is closed at the consumer boundary, not merely hidden behind Python-private state or an outer digest. |
| Veto diagnostics | Constructible authority; no native reread; post-request artifact mutation ignored; same-id branch replay; asserted Sage encoding; arbitrary redigested Sage script accepted; redigested decision mutation accepted; persisted-only product repair accepted. |
| Explanatory only | Test count, runtime, serialization order, and absent historical R3 bytes. |
| Not concluded | Mathematical proof, backend soundness in general, best repair, real-document usefulness, publication, Phase 07, release, or mission completion. |

## Verification Evidence

- Focused Sage/normalization/promotion suite after adversarial tests:
  `94 passed in 1.29s`.
- Phase 04-06 adjacency ladder: `211 passed, 1 skipped in 2.06s`; the skip is
  the pre-existing environment-dependent real-adapter smoke.
- Plan-prescribed focused ladder after receipt-compatibility repair:
  `184 passed in 1.53s`.
- Final reader/ranking/promotion focused rerun: `133 passed in 1.37s`.
- Full real-document plus publication-quarantine suite:
  `29 passed in 316.44s`; peak RSS `148940 KB`, no swap.
- Python compilation and whitespace/diff hygiene passed.
- No Sage/Lean/GPU/network/model/API execution occurred.

## Required Review Questions

1. Can direct construction, private-field mutation, serialization, or artifact
   mutation after request creation bypass a fresh native-reader evaluation?
2. Can evidence for one validated Phase 04 branch be replayed onto a changed
   same-id branch or smuggled inside a legacy branch payload?
3. Does the Sage reader derive the sole `QQ` assumption encoding from the exact
   regenerated script, including target sides and expected version prefix?
4. Can a fully redigested persisted decision change veto ids, manifest refs,
   edit content/digest, reconstruction status, eligibility, decision, vetoes,
   or reason while still validating?
5. Can any persisted decision, even internally consistent and exact-eligible,
   authorize an applicable product repair without native reevaluation?
6. Did any repair weaken the existing hard validity gates, honest
   incomparability, or publication-disabled product boundary?

Report findings first, ordered by severity, with exact file/function references.
End with exactly one line:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
