# Claude Read-Only Review Bundle

Date: 2026-07-13
Review name: `mathdevmcp-p03-rr01-result-review`
Supervisor/executor: Codex
Reviewer: Claude Opus read-only reviewer, maximum effort

## Role Boundary

Claude must not edit files, run mutating commands, launch agents, execute
backends, or authorize human/runtime/model/funding/product/scientific-claim
boundaries. This is the single reserved Phase 03 result-review round. It is not
the separate final-seal audit.

## Objective

Skeptically determine whether the sealed formal P03 `rr01` candidate is
internally reconstructible and satisfies the reviewed context-only evidence
contract without promoting retrieval, lexical similarity, source support, or
test counts into semantic equivalence, mathematical proof, or publication.

## Artifacts To Inspect

Inspect only these bounded local artifacts and the specific implementation
seams named below. Do not inspect the whole repository.

- `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/P03-candidate-decision.json`
  SHA-256 `9c195cffdd6fa71c72df9b23a1c4e016468fafd5b95bb4c70d9c680f974e7422`
- `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/P03-result.json`
  SHA-256 `293cee9644249c31ec0adec9e3da69e3dec092ddc1260969252b76f2fde8f7e6`
- `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/run-manifest.json`
  SHA-256 `42d08d8572ba8b43cc301f37d7d014a2f20d76871e5bf13b333114ead3ffa9e4`
- `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/candidate-validation.json`
  SHA-256 `af6ddbd4ab9d1562f4200c337e81b2e93b33ac0cd9584025f5d0231330d6d070`
- `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/receipts/receipt-index-19.json`
  SHA-256 `41738c534588a9ba6423f111204295a658c26961c919d3a1f4457e59cb37944e`
- `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/context-bundle/bundle-index.json`
  SHA-256 `d7aad02b0d5d2a70a4f8b5589d94011721bea7d00b36b05a7e180d6915bbc75e`
- `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/context-bundle/manifests.json`
  SHA-256 `52f1371e4f854fc30350c11a7162db3d42b033c8c1c68a0051670f5a8116f56e`
- `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/context-bundle/mutation-matrix.json`
  SHA-256 `d4caa5bd9f451896de3f1467d9145d63236b21a2846c7fd454029a8086fa89a6`
- `.local/mathdevmcp/evidence/p03-20260712/result-rounds/rr01/context-bundle/guard-index.json`
  SHA-256 `d007257a5f06a345b4110ecafe690707162bdd980365f6c96025cf4db1995d79`
- `docs/plans/mathdevmcp-real-document-remediation-phase-03-semantic-resolution-and-corpus-context-result-rr01-2026-07-12.md`
  SHA-256 `4c7e8138c98b05cc645d44141fc037d2fa9ba9908a6c0aebe44427707746e430`
- Reviewed plan:
  `docs/plans/mathdevmcp-real-document-remediation-phase-03-semantic-resolution-and-corpus-context-subplan-2026-07-12.md`
  SHA-256 `b0172a6122205d9378c4393bee270116ca501616da0a939b960f2ac16213c4f4`
- Reconstruction/governance seams:
  `src/mathdevmcp/context_evidence.py` functions
  `reconstruct_context_bundle`, `validate_p03_phase_result`,
  `validate_p03_run_manifest`, `validate_p03_candidate`, and
  `expected_p03_next_action`; `scripts/p03_governance.py` functions
  `_verify_receipt_index`, `_build_phase_result_record`,
  `_build_run_manifest_record`, `_build_candidate_record`, and
  `_candidate_gate`.

## Reconstructed Facts To Challenge

- Exact partition: 14 context searches plus three zero-traversal extraction
  vetoes over the 17 inherited P02 obligation digests.
- Terminal search states: two `source_supported`, two
  `candidate_assumption`, ten `not_found_after_search`; the three extraction
  vetoes have no semantic traversal.
- All stated/source-supported claims must have exact file digest, non-null
  source span, entry dependency path, and explicit applicability.
- Typed assumption support and encoding remain orthogonal; no context record is
  backend-certified, and the mathematical ledger is empty.
- Bundle semantic digest:
  `1e084430c49b5cd0c0d98ce46848c6e58385c7993bf427f6e109db885d9c0853`.
- Seven formal guards report zero forbidden/backend/source-edit/publication
  attempts and no replacement errors.
- Round and exit implementation manifests are identical; protected, allowlist,
  and diff actions pass; unexpected-paths is empty.
- Candidate reports all ten primary criteria true and all 16 vetoes false.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Does the exact sealed candidate justify a Phase 03 candidate pass under its bounded context-only engineering contract? |
| Baseline/comparator | Stable P02 obligations plus the reviewed pre-P03 directory-wide/local-window/spelling heuristic behavior; P02 extraction success is not semantic correctness. |
| Primary criterion | Exact 14/3 partition, constituent reconstruction, exact applicable provenance, closed state schemas, uncertainty preservation, card `\pi` non-posterior-by-spelling, state-lane separation, zero operations, mutation rejection, and governance/protected/allowlist integrity. |
| Veto diagnostics | Any omitted/duplicated obligation, extraction-veto traversal, invented or incomplete provenance, sibling leakage, incomplete search called absence, lexical/candidate promotion, support/encoding collapse, context error called mathematics, backend/source edit/publication operation, protected/allowlist/receipt mismatch, or unsupported human-result claim. |
| Explanatory diagnostics | Test counts, retrieved-node counts, fewer reported gaps, lexical scores, wall time, and reviewer agreement. |
| Not concluded | No search completeness beyond budgets, semantic equivalence, sufficient/minimal assumptions, mathematical proof/refutation, backend fitness, general LaTeX support, source repair, publication, Phase 04, release readiness, or scientific correctness. |

## Review Questions

1. Independently reconstruct the candidate from the named result, run manifest,
   bundle constituents, and receipt chain. Is any summary field trusted where a
   constituent should be reopened?
2. Inspect all 17 manifests, focusing on the two `source_supported` cases, ten
   `not_found_after_search` cases, and three extraction vetoes. Is any state
   unsupported by exact provenance/search completeness or promoted from lexical
   evidence?
3. Does the mutation matrix execute actual validators on one-field mutations,
   or merely declare success? Are material reviewed mutations missing?
4. Do run-manifest inventory, guard index/attestations, implementation delta,
   protected/allowlist artifacts, and receipt-index 19 close the governance and
   no-backend/no-source-edit boundary?
5. Does the human result accurately report residual uncertainty, including the
   historical P02 compatibility exception, without treating it as a P03 pass?
6. Identify any unsupported claim, hidden default, wrong comparator, proxy
   promotion, unfair state comparison, stale binding, or authority transfer.

## Required Output

Return findings first, ordered by severity with artifact/function references.
If there are no material findings, say so explicitly and state residual risks.
Then include these exact binding lines once each:

```text
Reviewed result round: `rr01`
Reviewed candidate SHA-256: `9c195cffdd6fa71c72df9b23a1c4e016468fafd5b95bb4c70d9c680f974e7422`
Reviewed run manifest SHA-256: `42d08d8572ba8b43cc301f37d7d014a2f20d76871e5bf13b333114ead3ffa9e4`
Reviewed result SHA-256: `293cee9644249c31ec0adec9e3da69e3dec092ddc1260969252b76f2fde8f7e6`
Reviewed context bundle semantic digest: `1e084430c49b5cd0c0d98ce46848c6e58385c7993bf427f6e109db885d9c0853`
Reviewed context bundle-index SHA-256: `d7aad02b0d5d2a70a4f8b5589d94011721bea7d00b36b05a7e180d6915bbc75e`
Reviewed mutation matrix SHA-256: `d4caa5bd9f451896de3f1467d9145d63236b21a2846c7fd454029a8086fa89a6`
Reviewed guard-index SHA-256: `d007257a5f06a345b4110ecafe690707162bdd980365f6c96025cf4db1995d79`
Reviewed governance receipt-index SHA-256: `41738c534588a9ba6423f111204295a658c26961c919d3a1f4457e59cb37944e`
```

End with exactly one final line: `VERDICT: AGREE` or `VERDICT: REVISE`.
