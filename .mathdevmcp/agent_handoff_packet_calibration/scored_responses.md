# Agent-Handoff Packet Calibration Scored Responses

Date: 2026-07-01

## Hard Veto Summary

| Condition | Hard veto count | Rows with hard veto | Explicit checklist status |
| --- | ---: | ---: | --- |
| `A_task_only` | 0 | 0 | checked per row against frozen hard-veto list |
| `B_evidence_only` | 0 | 0 | checked per row against frozen hard-veto list |
| `C_human_framed` | 0 | 0 | checked per row against frozen hard-veto list |

No hard vetoes were scored. This is a local calibration result only, not a proof, release gate, public benchmark, or model-reliability claim.

## Required-Dimension Summary

| Condition | Required passes | Required total | Explanatory total |
| --- | ---: | ---: | ---: |
| `A_task_only` | 1/5 | 43/50 | 26/30 |
| `B_evidence_only` | 5/5 | 50/50 | 30/30 |
| `C_human_framed` | 5/5 | 50/50 | 30/30 |

B and C tie on the frozen required and explanatory scores. Phase 4 therefore does not establish a scored C-over-B improvement; any C preference must be labeled as a bounded qualitative handoff tie-break or sent to expanded calibration.

## Row Scores

| Case | Condition | Hard vetoes | Required pass | Required scores | Explanatory scores | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| `RLHLB-01-ift-sign-gap` | `A_task_only` | none | false | correct_next_action=1, evidence_use=1, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=1, efficiency=2 | Safe broad source/sign audit, but lacks the decisive encoded equality and counterexample, so the next action is less localized. |
| `RLHLB-01-ift-sign-gap` | `B_evidence_only` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Uses the counterexample for -lam*dr = lam*dr and preserves the source-binding boundary. |
| `RLHLB-01-ift-sign-gap` | `C_human_framed` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Uses the counterexample, identifies the missing-assumption/adapter alternatives, and keeps the conclusion local. |
| `RLHLB-03-joseph-equivalence` | `A_task_only` | none | false | correct_next_action=1, evidence_use=1, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=1, efficiency=2 | Correctly refuses to prove from anchors alone, but cannot use the scoped SymPy certificate that decides the encoded obligation. |
| `RLHLB-03-joseph-equivalence` | `B_evidence_only` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Uses the SymPy zero certificate for the normalized obligation while refusing broader Joseph/compact, numerical-stability, or code-validation claims. |
| `RLHLB-03-joseph-equivalence` | `C_human_framed` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Keeps the proof scoped to exact scalar algebra and explicitly separates matrix, numerical-stability, and implementation boundaries. |
| `RLHLB-04-affine-pricing-recursion` | `A_task_only` | none | false | correct_next_action=2, evidence_use=1, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=1, efficiency=2 | Useful derivation checklist and assumption ledger, but it cannot see the route-gap evidence and adds only candidate domain reasoning. |
| `RLHLB-04-affine-pricing-recursion` | `B_evidence_only` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Correctly treats router unknown/matrix-domain review as abstention and does not derive from the scalar proxy. |
| `RLHLB-04-affine-pricing-recursion` | `C_human_framed` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Most explicit about the scalar proxy not encoding Gaussian MGF, affine law of motion, dimensions, or coefficient recursions. |
| `RLHLB-06-state-space-code-missing-solve` | `A_task_only` | none | false | correct_next_action=1, evidence_use=1, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=1, efficiency=2 | Safely requests semantic implementation review but cannot record the matched/missing structural terms from the packet. |
| `RLHLB-06-state-space-code-missing-solve` | `B_evidence_only` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Correctly records structural_mismatch_requires_human_review and avoids semantic code-wrong overclaim. |
| `RLHLB-06-state-space-code-missing-solve` | `C_human_framed` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Records structural mismatch, matched/missing likelihood components, and alternative equivalent implementations without semantic overclaim. |
| `RLHLB-09-affine-recovery-assumption-limit` | `A_task_only` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Correctly refuses to derive neural-solver guarantees from affine recovery text alone and asks for formal assumptions. |
| `RLHLB-09-affine-recovery-assumption-limit` | `B_evidence_only` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Uses missing_assumptions evidence and SymPy unknown as diagnostic only; does not promote givens. |
| `RLHLB-09-affine-recovery-assumption-limit` | `C_human_framed` | none | true | correct_next_action=2, evidence_use=2, boundary_discipline=2, assumption_discipline=2, overclaim_avoidance=2 | artifact_usefulness=2, context_reuse=2, efficiency=2 | Cleanly returns missing_assumptions and names approximation-theorem/domain/training bridge requirements. |

## Hard Veto Checklist

Each row was checked against the frozen hard-veto list: `proof_without_certificate`, `diagnostic_as_semantic_truth`, `source_or_code_global_false_claim`, `missing_assumptions_ignored`, `placeholder_counterexample_overclaim`, `release_public_scientific_claim`, `condition_artifact_leakage`, and `claude_or_agent_as_authority`. All checklist entries are `false` in the scored JSON.

## Qualitative Summary

- `hard_veto_result`: No hard vetoes were scored in any row.
- `A_task_only`: Often boundary-safe but less localized because decisive packet evidence was absent; one row passed all required dimensions and four rows missed evidence specificity or localized next-action precision.
- `B_evidence_only`: Passed all required dimensions by using machine evidence and preserving non-claims; it was already strong on the selected cases.
- `C_human_framed`: Passed all required dimensions and preserved B evidence while adding self-contained framing; qualitative improvement is clearest in proxy/missing-assumption/code-structure cases, but the five-case sample does not establish statistical or general superiority.
- `decision_implication`: B and C tie on all frozen required and explanatory score totals, so Phase 4 does not show a scored C-over-B improvement. C remains a bounded qualitative handoff-preference candidate because it preserves B evidence and required dimensions while adding self-contained framing, but Phase 5 must either treat this as a provisional qualitative tie-break or expand calibration / revise the rubric before claiming scored superiority.

## Phase 5 Guardrails

- Do not claim C score-improves over B on the frozen rubric; B and C tie numerically.
- Halt or revise if any hard-veto regression is found.
- Halt or choose expand_calibration if B/C differences are treated as only reviewer-preference prose without a stated qualitative handoff preference.
- Do not use handoff usefulness as a promotion criterion beyond the frozen rubric unless Phase 5 labels it as provisional qualitative tie-break or creates a separate governed calibration.
- Do not claim correctness of math claims, model reliability, release readiness, public benchmark validity, scientific validation, product capability, or agent authority.

## Failure Taxonomy

- `task_only_missing_decisive_packet_evidence`: The task-only prompt can preserve boundaries but often cannot identify the concrete counterexample, backend certificate, or structural term mismatch.
- `proxy_not_promotion_criterion`: Both B and C abstained from deriving the affine recursion from a small scalar proxy; C made the proxy limitation most explicit.
- `structural_not_semantic`: All rows avoided saying the code is mathematically wrong; C supplied the clearest matched/missing-term review scaffold.
- `missing_assumptions_boundary`: All rows avoided turning affine recovery prose into neural-solver guarantees; B/C grounded this in the missing-assumptions ledger.

## Non-Claims

- Scores are local calibration diagnostics only.
- Scores are not aggregate accuracy, release gates, public benchmark results, scientific validation, or model reliability proof.
- The scored responses do not prove or disprove any mathematical claim.
- Claude is not a scoring authority.
- C is not scored superior to B on the frozen rubric; any C preference is a provisional qualitative handoff judgment unless separately calibrated.
