# Phase 02 Subplan: Agent Hypothesis Expansion Interface

Date: 2026-07-10

Status: `DRAFT_PENDING_PHASE_01`

## Phase Objective

Represent agent brainstorming as validated candidate expansions attached to
exact blocker nodes, not as repair text.

## Entry Conditions Inherited From Previous Phase

- Strict closure/report contracts exist.
- Tests prevent diagnostic-only paths from publishing as repairs.

## Required Artifacts

- `propose_hypothesis_expansions` interface or equivalent.
- Validation for blocker id, route, assumptions, expected backend/tool,
  success criterion, failure criterion, and provenance.
- Tests for accepted, rejected, and downgraded hypotheses.
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-02-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- Focused hypothesis-validation tests.
- Relevant existing derivation-tree tests.
- `python3 -m py_compile` on modified modules.
- `git diff --check`.
- Read-only review if the interface gives the agent new authority.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can agent-generated mathematical ideas be admitted only as structured, non-certifying candidate branches? |
| Baseline/comparator | Current deterministic branch templates with no explicit agent-hypothesis schema. |
| Primary criterion | Vague or unsupported hypotheses are rejected or downgraded; valid hypotheses preserve exact blocker, assumptions, route, backend expectation, and non-claim provenance. |
| Veto diagnostics | Hypothesis lacks blocker id; assumptions are implicit; expected backend absent; success/failure criteria vague; raw agent text enters report. |
| Explanatory diagnostics | Initial implementation may use deterministic templates before external LLM integration. |
| Not concluded | Agent hypotheses are not repairs, proofs, or validated assumptions. |
| Artifact | Interface code, validation tests, Phase 02 result. |

## Forbidden Claims Or Actions

- Do not call an external agent from tests.
- Do not let LLM output bypass schema validation.
- Do not call a hypothesis valid merely because it sounds plausible.

## Exact Next-Phase Handoff Conditions

Advance to Phase 03 only if candidate expansions can be attached to exact
blockers and invalid hypotheses are rejected with useful reasons.

## Stop Conditions

Stop if the schema cannot represent the current blocker taxonomy without
weakening evidence requirements.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 02 result / close record.
3. Draft or refresh Phase 03 subplan.
4. Review Phase 03 for consistency and boundary safety.
