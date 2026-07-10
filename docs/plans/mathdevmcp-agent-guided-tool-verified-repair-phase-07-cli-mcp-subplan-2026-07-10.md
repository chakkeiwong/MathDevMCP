# Phase 07 Subplan: CLI And MCP Integration

Date: 2026-07-10

Status: `DRAFT_PENDING_PHASE_06`

## Phase Objective

Expose the agent-guided, tool-verified repair workflow through stable CLI and
MCP surfaces with explicit strict grounding options.

## Entry Conditions Inherited From Previous Phase

- Tool-grounded report compiler is implemented.
- Search paths preserve evidence and blockers.

## Required Artifacts

- CLI/MCP options such as `search_mode="agent_guided"` and
  `grounding_policy="strict"`.
- Output contract documentation.
- Tests for CLI/MCP parity and tool-use ledger.
- Phase result:
  `docs/plans/mathdevmcp-agent-guided-tool-verified-repair-phase-07-result-2026-07-10.md`

## Required Checks, Tests, Reviews

- CLI tests.
- MCP facade/server tests.
- Relevant document derivation-tree tests.
- `python3 -m py_compile` on modified modules.
- `git diff --check`.
- Read-only review of public-surface language.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can agents call the strict workflow directly and receive machine-readable evidence reports? |
| Baseline/comparator | Current `audit_document_derivation_tree` CLI/MCP exposure. |
| Primary criterion | CLI and MCP produce equivalent strict-grounding JSON/Markdown artifacts with explicit tool-use ledger. |
| Veto diagnostics | MCP omits strict fields; CLI and MCP disagree; defaults silently weaken evidence policy; no tool-use ledger. |
| Explanatory diagnostics | Compatibility aliases may remain. |
| Not concluded | No public release or full backward compatibility claim beyond tests. |
| Artifact | CLI/MCP code, tests, Phase 07 result. |

## Forbidden Claims Or Actions

- Do not make strict mode silently less strict for compatibility.
- Do not change public defaults without an explicit policy result.
- Do not hide backend unavailability.

## Exact Next-Phase Handoff Conditions

Advance to Phase 08 only if the workflow can be called consistently by local
agents and MCP clients.

## Stop Conditions

Stop if CLI/MCP schema changes require a human product/API decision not already
covered by the plan.

## End-Of-Subplan Actions

1. Run required local checks.
2. Write Phase 07 result / close record.
3. Draft or refresh Phase 08 subplan.
4. Review Phase 08 for consistency and boundary safety.
