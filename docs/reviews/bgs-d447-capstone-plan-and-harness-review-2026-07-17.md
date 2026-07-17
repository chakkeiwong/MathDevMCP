# BGS D447 Capstone Plan And Harness Review

Date: 2026-07-17

Pre-execution verdict: `PASS_AFTER_VISIBLE_REPAIRS`

Post-execution verdict: `VALID_PARTIAL_CAPSTONE_WITH_REPAIRED_HARNESS`

Reviewed artifacts:

- `docs/plans/mathdevmcp-bgs-d447-staged-capstone-program-2026-07-17.md`
- `scripts/run_bgs_d447_staged_capstone.py`

## Material Findings And Repairs

| Finding | Why material | Repair |
| --- | --- | --- |
| D447 was initially described too close to a generalization test | D447 was created from D446 with an earlier MathDevMCP audit | Reclassified D446/D447 as contaminated paired regression sources and D447 as a scale capstone only |
| The first gate required all 593 physical labels to resolve through the mathematical index | Twenty labels are figures and seven equation labels follow nested `aligned` structures without established row ownership | Require 593/593 accounting, 573/573 exact mathematical lookup, 566/566 extractable resolution, and preserve the seven lookup-only ownership gaps |
| A paired derivation comparison could imply that D447 prose repairs should improve proof status | The underlying equations are mostly unchanged | Split document claim-boundary evidence from equation/backend evidence; prohibit prose-to-proof promotion |
| The fixed-point math/code check would mostly test identifier mismatch | The intended question is function-level `theta` versus fixed-point values | Added aliases for all non-scope terms so `theta` is the sole missing term; record the absent first-class scope diagnostic as a product gap |
| Report-claim classifier prompts used unrecognized `nonclaim` wording | The classifier would treat `proof` as a theorem cue and return a false mathematical-claim classification | Reworded probes with explicit `does not claim` language |
| Source checks assumed one result schema | Derivation, compact packet, and report results expose source provenance differently | Added normalized source-file extraction across `source`, `doc_context`, and obligation provenance |
| Branch-preservation gates searched arbitrary large payload text | Unrelated prose could create a false pass | Tie C.75 and C.77 gates to exact selected labels and nonzero extracted targets |
| A failed candidate behavior was classified as an invalid experiment | Valid negative evidence must remain distinguishable from harness/source corruption | Added `CAPSTONE_CANDIDATE_FAILED`; reserved `EVALUATION_INVALID` for invalid evidence or harness state |
| Full-capstone artifact resolution assumed one resolver shape | Resolved audit/fix coverage may live under `agent_handoff.coverage` | Check both direct and handoff coverage before judging completeness |
| Repeated full-directory parsing could dominate runtime | D446/D447 produce 566 duplicate labels and each high-level workflow may rebuild the index | Use one cached index for ingestion and exact lookup, isolate the complete deep workflow in a bounded subprocess, and preserve runtime as scale evidence |

## Required Boundaries Confirmed

- DynareMCP is read-only.
- D446 and D447 are frozen by SHA-256.
- CPU-only execution is explicit.
- Optional backend absence is diagnostic, not refutation.
- No source edit, publication, release, or scientific promotion is authorized.
- A typed abstention may be useful without becoming proof.
- The independent-generalization status is
  `not_tested_no_verified_clean_holdout`.

## Review Conclusion

The repaired plan and harness answer the declared questions with proportionate
artifacts and valid stop conditions. Remaining limitations are part of the
candidate under test rather than defects hidden by the harness. Execution may
start.

## Post-Execution Review

| Finding | Classification | Resolution |
| --- | --- | --- |
| Fixed paragraph and byte windows split two exact D447 repair phrases and falsely produced `CAPSTONE_CANDIDATE_FAILED` | harness invalidity | Detect predeclared phrases over frozen full-source text with normalized whitespace; restart-safe finalization reclassified the preserved run without replaying scientific workflows |
| Suffix-label suppression used a corpus-wide row-label set | version-collision defect | Deduplicate only when the same label is owned by an explicit row inside the same source display; added sibling-version regression coverage |
| Reused audit/fix evidence could omit its source filename | evidence-binding defect | Require both exact source digest and exact basename before reuse |
| Compact report byte counts were computed before final guardrail insertion | transport-accounting defect | Compute a fixed point over the final serialized payload and assert exact byte equality |
| Full-document planning completed but all three deep 566-label workflows timed out | candidate scale limitation | Preserve each bounded timeout; require resumable batches or shared parsed/evidence state rather than increasing a monolithic budget post hoc |
| Tree publication state was unavailable after timeout | observation gap | Report `not_observed_due_timeout`; do not interpret a false gate as publication enabled |
| The first-class fixed-point scope diagnostic remained `not_triggered` | product diagnostic gap | Preserve the localized missing-`theta` evidence and record scope classification as unfinished |
| D446/D447 have MathDevMCP contamination and no clean control was found | scientific generalization gap | Keep independent generalization `not_tested_no_verified_clean_holdout` |

Post-execution review decision:

`PARTIAL_CAPSTONE_SCALE_OR_TOOL_GAPS`

This decision supports tested workflow behavior on the frozen contaminated
regression/capstone sources. It does not support BGS correctness, theorem proof,
publication readiness, or independent generalization.

Verification completed with 1,649 repository tests passing and 4 skipped under
intentional CPU-only execution. Focused repaired-contract suites, Python
compilation, `git diff --check`, and frozen-source digest checks also passed.
