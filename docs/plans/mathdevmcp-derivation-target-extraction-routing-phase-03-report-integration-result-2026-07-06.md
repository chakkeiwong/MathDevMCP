# Phase 3 Result: Report Integration

Date: 2026-07-06

Status: `PASSED`

## Objective

Integrate target extraction and route planning into
`audit_and_propose_derivations` so label reports group extracted obligations
under parent labels and route each obligation through the existing derivation
gap/proposal workflow.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Can reports use extracted obligations instead of full blocks while preserving existing report usefulness? |
| Baseline/comparator | Current label reports routed full proposition blocks. |
| Primary criterion | Passed: label reports now record extracted target count, fallback count, parent label, equation label, line, lhs/rhs, route plan, validation, and assumption repairs. |
| Veto diagnostics | Passed: direct-target support remains; label fallback remains explicit; route plans are visible and non-certifying; proposal fields remain present. |
| Explanatory diagnostics | Report coverage now includes label count, extracted target count, fallback target count, gap count, proposal count, and route plans. |
| Not concluded | No proof of the risky-debt note and no source edits. |
| Artifact | Updated `src/mathdevmcp/derivation_audit_report.py`, `src/mathdevmcp/derivation_gap_proposals.py`, and `tests/test_derivation_audit_report.py`. |

## Implementation Summary

- Label reports now call `extract_derivation_targets_for_label`.
- Each extracted target is routed through `plan_backend_routes`.
- Each extracted target is then passed to `derive_from` with explicit `lhs` and
  `rhs` when available.
- Markdown now includes:
  - `Extracted Targets`;
  - `Backend Route Plans`;
  - target labels, parent labels, line locations, lhs/rhs, route candidates,
    tools, evidence contracts, and non-certifying route boundaries.
- Direct target reports still work and now include a visible route-planning
  tool-use record.
- Shared gap locations now include `parent_label > equation_label > line` when
  the extracted equation label differs from the parent proposition label.

## Repair During Phase

The first report test run found two location issues:

- text-only fallback labels should keep the old single-label location;
- extracted equation gaps should include both parent proposition label and
  equation label.

`derivation_gap_proposals._location` was patched to include the parent label
only when it differs from the extracted target label.

## Checks Run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_derivation_audit_report.py -q` | First run found the location issue; after repair, 6 passed. |
| `python3 -m pytest tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py -q` | Passed: 8 passed. |
| `python3 -m pytest tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q` | Passed: 24 passed. |
| `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derivation_target_extraction.py src/mathdevmcp/backend_route_planner.py src/mathdevmcp/derivation_gap_proposals.py` | Passed. |

## Boundary

Report integration does not make route plans certifying evidence. Proof or
refutation claims still require downstream backend certificates or concrete
counterexamples attached to the scoped obligation.

## Next-Phase Handoff

Proceed to Phase 4 because:

- report tests verify extracted obligation grouping;
- direct target and label paths both work;
- fallback behavior is explicit;
- Phase 4 subplan names the risky-debt output path and inspection criteria.
