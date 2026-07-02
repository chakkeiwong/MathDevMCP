# Phase 1 Subplan: Usefulness Contract And Rubric

Date: 2026-07-01

Status: `READY_FOR_PHASE_1_EXECUTION`

## Phase Objective

Define the downstream-agent usefulness benchmark contract: question,
comparators, prompt variants, response contract, scoring rubric, hard vetoes,
promotion criteria, and non-claims.

## Entry Conditions Inherited From Previous Phase

- Phase 0 result exists.
- Baseline artifacts and current behavior are characterized.
- Approval boundaries for response collection are explicit.
- No implementation behavior has been changed for this program.

## Required Artifacts

- Phase 1 result:
  `docs/plans/mathdevmcp-downstream-agent-usefulness-phase-01-contract-rubric-result-2026-07-01.md`.
- Benchmark contract draft under `.mathdevmcp/downstream_agent_usefulness/` or
  a documented blocker if runtime artifact creation is deferred.
- Rubric draft with required dimensions, hard vetoes, and non-claims.
- Updated ledger and stop handoff if execution stops.

## Required Checks, Tests, Reviews

- Local schema/content check that every rubric dimension has a score scale,
  pass rule, and veto interaction.
- Grep/check for forbidden promotion language in the contract artifact.
- Claude read-only review of a compact Phase 1 contract brief.
- Codex skeptical review of baseline, proxy metrics, stop conditions, and
  approval boundaries.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | What would count as evidence that packets help downstream agents perform the math task better? |
| Baseline/comparator | A_task_only, B_evidence_only or machine-evidence packet, and C_human_framed packet conditions. |
| Primary criterion | A frozen rubric distinguishes task correctness, evidence use, self-contained reasoning, boundary discipline, and actionability before responses are collected. |
| Veto diagnostics | Rubric changed after seeing responses; packet completeness alone treated as task success; C-over-B tie hidden; malformed outputs excluded; Claude used as scorer authority; aggregate-only pass rule. |
| Explanatory diagnostics | Rubric coverage matrix, hard-veto list, non-claim list, scoring examples if included. |
| Not concluded | No usefulness result, no model reliability, no proof correctness, no promotion decision. |

## Forbidden Claims Or Actions

- Do not collect responses in Phase 1.
- Do not score existing responses under a changed rubric as if it were
  predeclared.
- Do not make C the winner by definition.
- Do not allow aggregate averages to override hard vetoes.

## Exact Next-Phase Handoff Conditions

Advance to Phase 2 only if:

- contract and rubric are frozen or a blocker is written;
- hard vetoes and non-claims are explicit;
- the Phase 2 case-corpus subplan is reviewed for source boundaries,
  feasibility, and artifact coverage.

## Stop Conditions

Stop if:

- the usefulness question cannot be separated from packet-format quality;
- scoring cannot avoid post-hoc criteria;
- Claude/Codex review finds an unfixable proxy-promotion or boundary flaw;
- response collection would be needed to finish this phase.

## Phase Close Protocol

At phase close:

1. run required local checks;
2. write the Phase 1 result/close record;
3. draft or refresh the Phase 2 subplan;
4. review the Phase 2 subplan for consistency, correctness, feasibility,
   artifact coverage, and boundary safety.
