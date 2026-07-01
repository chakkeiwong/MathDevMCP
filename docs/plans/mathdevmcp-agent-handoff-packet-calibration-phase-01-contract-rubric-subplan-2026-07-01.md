# Phase 1 Subplan: Calibration Contract And Rubric

Date: 2026-07-01

Status: `REVISED_AFTER_CLAUDE_R1_PENDING_PHASE_0`

## Phase Objective

Define the calibration conditions, scoring dimensions, hard vetoes, and
artifact contract before any downstream agent responses are collected.

## Entry Conditions Inherited From Previous Phase

- Phase 0 has frozen the packet baseline.
- Selected case IDs and packet artifact paths are recorded.
- No downstream model subject responses have been generated.

## Required Artifacts

- Phase 1 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-01-contract-rubric-result-2026-07-01.md`.
- Rubric artifact:
  `.mathdevmcp/agent_handoff_packet_calibration/scoring_rubric.json`.
- Calibration contract artifact:
  `.mathdevmcp/agent_handoff_packet_calibration/calibration_contract.json`.
- Condition fairness checklist embedded in the contract.
- Refreshed Phase 2 subplan.
- Ledger entry.

## Required Checks, Tests, And Reviews

- Validate JSON artifacts with `python3 -m json.tool`.
- Local consistency check that all five case IDs have three condition slots.
- Verify hard vetoes are first-class row fields and dominate aggregate
  summaries.
- Verify artifact usefulness and context reuse are explanatory unless
  correctness, boundaries, assumption discipline, and overclaim avoidance pass.
- Claude read-only review of compact rubric/contract brief.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What will count as better downstream agent work? |
| Baseline/comparator | Three predeclared prompt conditions A/B/C. |
| Primary criterion | Rubric includes required pass dimensions, explanatory dimensions, hard vetoes, and fair A/B/C condition constraints before responses exist. |
| Veto diagnostics | Rubric rewards verbosity alone; proxy score hides hard vetoes; artifact usefulness/context reuse treated as promotion criteria without correctness/boundary pass; criteria are changed after seeing responses; condition definitions leak framing into A/B. |
| Explanatory diagnostics | Rubric dimension descriptions, hard-veto list, condition fairness checklist. |
| Not concluded | Calibration result, packet superiority, model reliability, or release/public/scientific validity. |

## Forbidden Claims And Actions

- Do not collect or score agent responses in Phase 1.
- Do not tune scoring criteria after seeing responses.
- Do not collapse hard vetoes into aggregate scores.
- Do not let Claude approve boundary crossings.
- Do not let downstream agents adjudicate packet correctness.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if:

- contract and rubric artifacts exist and validate as JSON;
- all selected cases and conditions are enumerated;
- hard vetoes are explicit;
- fairness checklist requires equal task skeleton, output sections, length band,
  retry policy, and B/C machine-evidence parity;
- Claude either agrees or any fixable findings are patched through the repair
  loop, or a reviewer-unavailable result is recorded with local justification.

## Stop Conditions

Stop if:

- a fair A/B/C condition split cannot be defined;
- scoring requires human/expert labels unavailable at this stage;
- Claude/Codex find unresolved proxy-metric or leakage flaws.

## End-Of-Phase Protocol

Run local JSON checks, write the result, refresh/review Phase 2, append the
ledger, then advance or stop.
