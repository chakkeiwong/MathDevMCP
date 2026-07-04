# Phase 5 Subplan: Contract Decision And Handoff

Date: 2026-07-01

Status: `LOCAL_REVIEWED_READY_AFTER_PHASE_4`

## Phase Objective

Use the scored local calibration to decide whether to freeze the human-framed
packet as the current agent-handoff standard, revise it, or expand calibration
before freezing.

## Entry Conditions Inherited From Previous Phase

- Phase 4 scored comparison exists.
- Hard vetoes and failure taxonomy are recorded.
- No release/public/scientific/model-reliability claim has been made.

Phase 4 refresh note: B and C tie on all frozen required and explanatory score
totals. Phase 5 must not claim scored C-over-B superiority. Any C preference
must be labeled as a provisional qualitative handoff tie-break, or Phase 5 must
choose `expand_calibration` / `revise_packet_template`.

## Local Skeptical Audit Before Execution

Audit result: passed with guardrails.

- Wrong baseline risk: Phase 5 must compare against both A and B, not only A.
- Proxy metric risk: self-contained handoff usefulness is qualitative under the
  frozen rubric and cannot be promoted as scored superiority.
- Missing stop condition risk: stop or choose `expand_calibration` if the
  decision would require a general or statistical claim.
- Hidden assumption risk: the five selected cases are local/non-gating and do
  not establish general model reliability.
- Artifact-answerability risk: Phase 5 must cite the scored table and Phase 4
  result, including the B/C tie and hard-veto checklist.

## Required Artifacts

- Phase 5 result:
  `docs/plans/mathdevmcp-agent-handoff-packet-calibration-phase-05-contract-decision-handoff-result-2026-07-01.md`.
- Final visible stop handoff:
  `docs/plans/mathdevmcp-agent-handoff-packet-calibration-visible-stop-handoff-2026-07-01.md`.
- Updated review trail if Claude reviews the decision.
- Optional follow-up issue/plan for Markdown packet report generator or packet
  template revisions.
- Ledger entry.

## Required Checks, Tests, And Reviews

- Verify all required phase results exist or blockers are recorded.
- Verify no claims exceed the local evidence.
- Claude read-only review of final decision brief.
- If docs or code are changed, run focused relevant tests.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What should be done with the human-framed packet standard after local agent-handoff calibration? |
| Baseline/comparator | Phase 4 scored A/B/C comparison and hard-veto analysis. |
| Primary criterion | Final decision is one of `freeze_local_standard_candidate`, `revise_packet_template`, `expand_calibration`, `blocked_no_model_use_approval`, or `blocked_inconclusive_scoring`, with evidence and non-claims explicit. |
| Veto diagnostics | Freezing despite hard-veto regressions; claiming generality beyond local cases; ignoring model-use limitations; hiding unresolved approval blockers; treating local freeze as default release/product policy. |
| Explanatory diagnostics | Per-case score summary, failure taxonomy, Claude review, human-facing next action. |
| Not concluded | General downstream-agent reliability, release readiness, public benchmark validity, scientific validation, or proof correctness. |

## Forbidden Claims And Actions

- Do not promote local calibration to public benchmark or release gate.
- Do not claim the packet standard is universally optimal.
- Do not change production/default policy without separate governed decision.
- Do not omit unresolved blockers from the final handoff.
- Do not claim proof of packet optimality or transfer beyond selected cases.

## Exact Next-Phase Handoff Conditions

This is the final phase. Completion requires:

- Phase 5 result written;
- stop handoff written;
- review trail updated;
- tests/checks recorded;
- next human decision stated if any approval or expansion is needed.

## Stop Conditions

Stop if:

- Phase 4 evidence is missing or inconsistent;
- final decision would cross a human policy boundary;
- final decision would claim C score-improves over B under the frozen rubric;
- final decision would use handoff usefulness as a promotion criterion without
  labeling it provisional or separately governed;
- Claude/Codex do not converge after five review rounds on a material final
  decision issue.

## End-Of-Phase Protocol

Run final checks, write result and handoff, append ledger, and stop.
