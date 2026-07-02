# Phase 1 Result: Usefulness Contract And Rubric

Date: 2026-07-01

Status: `PASSED_WITH_CLAUDE_REVIEW_UNAVAILABLE`

## Phase Objective

Define the downstream-agent usefulness benchmark contract: question,
comparators, prompt variants, response contract, scoring rubric, hard vetoes,
promotion criteria, and non-claims.

## Skeptical Audit

Checked before closing Phase 1:

- Wrong baseline: avoided. The contract starts from commit `0e7f9a2`, the
  prior local packet-standard candidate, and the explicit B/C tie limitation.
- Proxy metrics: avoided. Packet completeness and formatting are not primary
  success criteria; task outcome, evidence use, reasoning, gaps, boundaries,
  and actionability are required dimensions.
- Missing stop conditions: avoided. Response collection remains a later
  explicit approval boundary.
- Unfair comparison: controlled. A/B/C payload differences are declared, and
  B/C machine-evidence parity is required.
- Hidden assumptions: recorded. One-response-per-prompt evidence is diagnostic
  unless later justified; C is not winner by definition.
- Stale context: Phase 0 baseline and prior calibration artifacts were read.
- Environment mismatch: no model responses or external services were used.
- Artifact mismatch: artifacts define contract/rubric only, not results.

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | What would count as evidence that packets help downstream agents perform the math task better? |
| Baseline/comparator | A_task_only, B_evidence_only, and C_human_framed prompt conditions. |
| Primary criterion | Passed: a frozen rubric distinguishes task correctness, decisive evidence use, self-contained reasoning, assumption/gap handling, boundary discipline, and actionability before responses are collected. |
| Veto diagnostics | Passed locally: no response collection, no post-hoc scoring, no C-by-definition rule, no aggregate-only promotion, no Claude worker role. |
| Explanatory diagnostics | JSON contract/rubric validation, hard-veto list, non-claim list, grep for promotion-sensitive terms. |
| Not concluded | No downstream-agent usefulness result, model reliability, proof correctness, release readiness, public benchmark validity, product capability, or promotion decision. |

## Artifacts

- `.mathdevmcp/downstream_agent_usefulness/benchmark_contract.json`
- `.mathdevmcp/downstream_agent_usefulness/scoring_rubric.json`

## Contract Summary

Prompt conditions:

- `A_task_only`: task statement, bounded context summary, source provenance,
  requested output schema, and forbidden claims.
- `B_evidence_only`: A plus machine evidence, status, gaps, assumptions,
  backend/counterexample/proof-step ledgers, and non-claims, without human
  narrative framing.
- `C_human_framed`: B plus human-framed packet reasoning, narrative answer,
  and recommended next action.

Required dimensions:

- `task_outcome_correctness`
- `decisive_evidence_use`
- `self_contained_reasoning`
- `assumption_and_gap_handling`
- `boundary_and_nonclaim_discipline`
- `actionability_for_next_agent`

Hard-veto policy:

- hard vetoes dominate numeric scores;
- per-case results must be reported before aggregate summaries;
- C cannot be promoted if it has a hard-veto regression, loses B's machine
  evidence, or lacks predeclared usefulness improvement over B.

## Required Local Checks

| Check | Result |
| --- | --- |
| JSON/schema/content validation | Passed: `contract_and_rubric_valid`, `required_dimensions=6`, `hard_vetoes=8`. |
| Promotion-sensitive grep | Passed: matches are non-claims, vetoes, or forbidden-claim guardrails. |
| `git diff --check` on Phase 1 artifacts | Passed. |

## Claude Review Status

Claude compact Phase 1 review produced no usable output before supervisor
interruption. This is recorded as reviewer unavailable and not approval.

Phase 1 did not collect responses, score responses, change implementation
behavior, use network/model workers, or cross a promotion/scientific/product
boundary.

## Next Subplan Review

Phase 2 subplan was reviewed locally for:

- sequencing: it follows a frozen contract/rubric;
- correctness: it requires workflow family, evidence class, expected output,
  source boundary, and scoring applicability for every case;
- feasibility: it can start from existing local benchmark artifacts;
- artifact coverage: it requires a case manifest, evidence matrix, source
  boundary note, and result record;
- boundary safety: it forbids response collection, excessive copied text, and
  diagnostic-to-certified relabeling.

## Handoff To Phase 2

Advance to Phase 2 is allowed because:

- contract and rubric are frozen;
- hard vetoes and non-claims are explicit;
- response collection remains gated;
- Phase 2 can design fixtures without model responses.
