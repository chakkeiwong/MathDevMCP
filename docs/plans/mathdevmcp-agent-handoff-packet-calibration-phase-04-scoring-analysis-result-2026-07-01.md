# Phase 4 Result: Scoring And Analysis

Date: 2026-07-01

Status: `PASSED_WITH_NUMERIC_BC_TIE`

## Phase Objective

Score collected responses against the frozen rubric, compare prompt conditions,
and identify whether human-framed packets improve downstream agent work on the
local selected cases.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Did the human-framed condition improve downstream agent work relative to baselines on the selected local cases? |
| Baseline/comparator | A/B conditions from the same frozen case set and response protocol. |
| Primary criterion | Mixed result: C strongly improves over A, but C and B tie on all frozen required and explanatory score totals. |
| Veto diagnostics | Passed: hard-veto summary appears before score totals; per-row hard-veto checklists are explicit; no hard vetoes scored. |
| Explanatory diagnostics | C is qualitatively more self-contained than B in proxy, missing-assumption, and code-structure cases, but this is not a scored C-over-B win under the frozen rubric. |
| Not concluded | No universal packet superiority, model benchmark validity, release readiness, scientific validation, proof correctness, or model reliability claim is concluded. |

## Artifacts

- Scored JSON:
  `.mathdevmcp/agent_handoff_packet_calibration/scored_responses.json`
- Scored Markdown:
  `.mathdevmcp/agent_handoff_packet_calibration/scored_responses.md`
- Scored JSON SHA256:
  `5b48e38477c15d90c7ba2b603a7cd23c5f236b1cb5e86c01ed72f911cc90decb`
- Scored Markdown SHA256:
  `c19315f4c43239b66a39c661722a56c01101713c30695ad9d87ad3c22d171c97`
- Response manifest SHA256:
  `d44786139e064c2321936c6d677b3b1f265c00612042334252268ae6a43d6182`

## Hard-Veto-First Summary

| Condition | Hard veto count | Rows with hard veto |
| --- | ---: | ---: |
| `A_task_only` | 0 | 0 |
| `B_evidence_only` | 0 | 0 |
| `C_human_framed` | 0 | 0 |

Every row has an explicit hard-veto checklist in the scored JSON. All frozen
hard vetoes are false for all rows.

## Required-Dimension Summary

| Condition | Required passes | Required total | Explanatory total |
| --- | ---: | ---: | ---: |
| `A_task_only` | 1/5 | 43/50 | 26/30 |
| `B_evidence_only` | 5/5 | 50/50 | 30/30 |
| `C_human_framed` | 5/5 | 50/50 | 30/30 |

Interpretation:

- A_task_only was usually boundary-safe but often lacked decisive packet
  evidence, so it missed localized next-action or evidence-use credit in four
  of five rows.
- B_evidence_only passed all required dimensions and was already strong on
  the selected cases.
- C_human_framed also passed all required dimensions and preserved B evidence
  without hard-veto regression.
- B and C tie numerically on the frozen rubric. Phase 4 therefore does not
  establish scored C-over-B superiority.

## Qualitative Finding

C provides bounded qualitative handoff-preference evidence: it preserves the
same machine evidence as B while adding self-contained framing that makes proxy
limits, missing assumptions, structural-vs-semantic boundaries, and next
review artifacts easier to reuse. This qualitative preference is not a scored
promotion criterion unless Phase 5 labels it as provisional or creates a
separate governed calibration.

## Failure Taxonomy

| Pattern | Affected condition(s) | Interpretation |
| --- | --- | --- |
| `task_only_missing_decisive_packet_evidence` | A | Task-only prompts can preserve boundaries but often cannot identify the concrete counterexample, backend certificate, or structural term mismatch. |
| `proxy_not_promotion_criterion` | B/C | Both B and C abstained from deriving the affine recursion from a scalar proxy; C made the proxy limitation most explicit. |
| `structural_not_semantic` | A/B/C | All rows avoided saying code is mathematically wrong; C supplied the clearest matched/missing-term review scaffold. |
| `missing_assumptions_boundary` | A/B/C | All rows avoided turning affine recovery prose into neural-solver guarantees; B/C grounded this in the missing-assumptions ledger. |

## Required Local Checks

| Check | Result |
| --- | --- |
| `python3 -m json.tool .mathdevmcp/agent_handoff_packet_calibration/scored_responses.json` | Passed |
| Row/schema focused check | Passed: 15 rows, required/explanatory score keys present, score ranges valid |
| Hard-veto checklist focused check | Passed: every row has checklist and all values are false |
| Tie/guardrail focused check | Passed: decision implication mentions B/C tie and Phase 5 guardrails exist |

## Claude Read-Only Review

Claude R1 scoring review returned `VERDICT: REVISE` with three material points:

1. zero hard-veto status needed explicit per-row checklist evidence;
2. C tied B numerically, so C could not be called scored-superior;
3. Phase 5 needed guardrails for provisional qualitative tie-break use.

Codex patched the scored JSON and Markdown, reran focused checks, and sent a
compact delta review. Claude R2 returned `VERDICT: AGREE`, with only a wording
caution to keep Phase 5 aligned with "no scored superiority."

Claude is not a scoring authority; Codex retains responsibility for the final
interpretation.

## Phase 5 Subplan Refresh

The Phase 5 subplan remains feasible with an added decision constraint:

- `freeze_local_standard_candidate` may only mean "provisional local handoff
  candidate by qualitative tie-break," not scored C-over-B superiority.
- If that qualitative tie-break is considered too soft, choose
  `expand_calibration` or `revise_packet_template` instead.
- Do not claim correctness of math claims, model reliability, release
  readiness, public benchmark validity, scientific validation, product
  capability, or agent authority.

## Handoff

Proceed to Phase 5. The available Phase 5 choices supported by Phase 4 are:

- `freeze_local_standard_candidate`, but only as a provisional qualitative
  handoff standard candidate, not a scored win over B;
- `expand_calibration`, if the B/C tie makes qualitative preference
  insufficient;
- `revise_packet_template`, if the project wants the rubric to capture
  self-contained handoff usefulness before freezing.
