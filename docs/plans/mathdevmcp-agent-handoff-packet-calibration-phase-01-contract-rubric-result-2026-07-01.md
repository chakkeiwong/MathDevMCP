# Phase 1 Result: Calibration Contract And Rubric

Date: 2026-07-01

Status: `PASSED`

## Phase Objective

Define the calibration conditions, scoring dimensions, hard vetoes, and artifact
contract before any downstream agent responses are collected.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What will count as better downstream agent work? |
| Baseline/comparator | Three predeclared prompt conditions: `A_task_only`, `B_evidence_only`, `C_human_framed`. |
| Primary criterion | Passed: rubric includes required pass dimensions, explanatory dimensions, hard vetoes, and fair A/B/C controls before responses exist. |
| Veto diagnostics | No rubric reward for verbosity alone; hard vetoes are first-class row fields; artifact usefulness/context reuse are explanatory unless required dimensions pass; criteria frozen before responses. |
| Not concluded | No calibration result, packet superiority, model reliability, release readiness, public benchmark validity, or scientific validation is concluded. |

## Artifacts

- `.mathdevmcp/agent_handoff_packet_calibration/calibration_contract.json`
- `.mathdevmcp/agent_handoff_packet_calibration/scoring_rubric.json`

SHA256:

```text
023f099fedd596503ce9821edf8aa28cd705093ec77779b3551cee35a87cca2a  .mathdevmcp/agent_handoff_packet_calibration/calibration_contract.json
948ae1d7318462cb4dd3058aef08c2dcc2d36baa312f7f0090a226f66dcb4945  .mathdevmcp/agent_handoff_packet_calibration/scoring_rubric.json
```

## Contract Summary

```text
contract_status phase_01_frozen_before_response_collection
case_count 5
conditions ['A_task_only', 'B_evidence_only', 'C_human_framed']
fairness_controls_true True
required_dimensions ['correct_next_action', 'evidence_use', 'boundary_discipline', 'assumption_discipline', 'overclaim_avoidance']
explanatory_dimensions ['artifact_usefulness', 'context_reuse', 'efficiency']
hard_veto_count 8
aggregate_accuracy None
```

## Checks

Passed:

```bash
python3 -m json.tool .mathdevmcp/agent_handoff_packet_calibration/calibration_contract.json
python3 -m json.tool .mathdevmcp/agent_handoff_packet_calibration/scoring_rubric.json
```

## Phase 2 Subplan Review

Local review:

- Phase 2 correctly starts only after rubric/contract freeze.
- Phase 2 does not collect model responses.
- Required fixture checks cover 15 prompts, A/B/C payload separation, B/C
  evidence parity, identical skeleton/output/length/retry policy, and no large
  source excerpts.
- Stop conditions cover prompt leakage and unfair condition separation.

## Handoff

Exact next-phase handoff conditions are met. Proceed to Phase 2.
