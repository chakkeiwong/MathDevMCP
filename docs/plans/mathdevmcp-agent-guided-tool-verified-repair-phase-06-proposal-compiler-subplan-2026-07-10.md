# Phase 06 Subplan: Tool-Grounded Proposal Compiler

Date: 2026-07-10

Status: `DRAFT_PENDING_PHASE_05`

## Phase Objective

Replace top-ranked-branch rendering with a strict compiler that emits repair
proposals only from closed or partially closed tool-grounded paths and emits
gap reports for blocked paths.

## Entry Conditions Inherited From Previous Phase

- Recursive search paths include hypotheses, backend evidence, exact blockers,
  and closure status.
- Expansion rules produce candidate paths with source-local details.

## Required Artifacts

- Report compiler for:
  closed repairs, partial repairs, refutations, invalid expansions, and exact
  gap reports.
- Tests that every published repair step has an evidence ref.
- Updated Markdown/JSON report rendering.
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-06-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- Document report tests.
- Tree report tests.
- Frozen fixture assertions for blocked branch gap reports.
- `python3 -m py_compile` on modified modules.
- `git diff --check`.
- Read-only review of report claims.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can reports publish only evidence-grounded repairs and exact blockers? |
| Baseline/comparator | Current document-ready proposal section generated from ranked branch evidence. |
| Primary criterion | Closed/partial paths render as proposals with evidence; blocked paths render as gap reports; no raw agent hypothesis text becomes a fix. |
| Veto diagnostics | Blocked path rendered as repair; missing location/problem/why/fix/evidence; diagnostic status presented as proof; no remaining blockers for partial path. |
| Explanatory diagnostics | Reports may be more conservative and longer. |
| Not concluded | No claim that all document issues are found. |
| Artifact | Compiler code, tests, generated smoke reports, Phase 06 result. |

## Forbidden Claims Or Actions

- Do not select a branch by ranking score alone.
- Do not publish agent hypothesis prose as proposed LaTeX without validation.
- Do not omit blockers to make reports look cleaner.

## Exact Next-Phase Handoff Conditions

Advance to Phase 07 only if CLI/MCP can expose the stricter report contract
without ambiguity.

## Stop Conditions

Stop if the public report schema cannot preserve compatibility and strict
evidence fields at the same time.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 06 result / close record.
3. Draft or refresh Phase 07 subplan.
4. Review Phase 07 for consistency and boundary safety.
