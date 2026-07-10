# Phase 1 Subplan: Version-Aware Evidence Selection

Date: 2026-07-07

Status: `DRAFT_PENDING_PHASE_0`

## Phase Objective

Add exact file/include/exclude filtering to LaTeX search and label lookup so
versioned report directories do not mix old and current draft evidence.

## Entry Conditions

- Phase 0 passed.
- Master program dependency order accepted.

## Required Artifacts

- Updated search/lookup implementation.
- CLI/MCP/FastMCP argument exposure where applicable.
- Focused tests with sibling D446/D447 or old/final fixtures.
- Phase 1 result record.

## Required Checks/Tests/Reviews

- Focused tests for `search_latex` and `latex_label_lookup` filters.
- Interface tests for MCP facade/server if signatures change.
- `git diff --check`.
- Review next Phase 2 subplan for dependency consistency.

## Evidence Contract

| Field | Contract |
| --- | --- |
| Question | Can agents constrain LaTeX evidence to exact/current files before audit? |
| Baseline/comparator | Existing root-wide search that can mix D446/D447 or old/final files. |
| Primary criterion | Exact file and glob filters include intended file hits and exclude sibling draft hits. |
| Veto diagnostics | Filter ignored; label lookup returns excluded file; old/final contamination in tests; interface silently drops filters. |
| Explanatory diagnostics | Match counts, filenames, argument echo. |
| Not concluded | Search ranking quality or full document audit correctness. |

## Forbidden Claims/Actions

- Do not change ranking semantics beyond filtering.
- Do not edit downstream report documents.

## Exact Next-Phase Handoff Conditions

Proceed to Phase 2 only if filtered evidence selection is implemented and
focused tests prove old/current sibling isolation.

## Stop Conditions

Stop if current index/search architecture cannot support file filtering without
a larger design change. The stop handoff must include the minimal failing
filtering diagnostic, the unavailable dependency or architectural blocker, and
the next design question for human review.
