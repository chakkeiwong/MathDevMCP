# Phase 4 Result: Risky-Debt V2 Experiment

Date: 2026-07-06

Status: `PASSED`

## Objective

Generate a v2 risky-debt derivation report using extracted obligations and
inspect whether it improves on the current full-block report.

## Evidence Contract

| Field | Result |
| --- | --- |
| Question | Does extracted-obligation reporting improve risky-debt derivation audit usefulness? |
| Baseline/comparator | `docs/reviews/risky-debt-derivation-gap-proposals.md`, which routed two full proposition blocks. |
| Primary criterion | Passed: v2 separates `eq:risky-pricing`, `eq:foc-k`, and `eq:foc-b` with target-level provenance and preserves assumption repair details. |
| Veto diagnostics | Passed: locations are present; assumption repairs remain; backend route plans are visible; route plans are non-certifying; no generic `collect more evidence` style proposal is introduced. |
| Explanatory diagnostics | V2 coverage: 3 targets, 3 gaps, 3 proposals, 3 extracted targets, 0 full-block fallbacks, 0 certifying proposals. |
| Not concluded | No proof of the risky-debt note, no source edit, and no scientific validation. |
| Artifact | `docs/reviews/risky-debt-derivation-gap-proposals-v2.md`. |

## Command Run

```bash
python3 -m mathdevmcp.cli audit-and-propose-derivations "Audit risky-debt derivations with extracted obligations" --root docs --label prop:risky-pricing --label prop:interior-foc --output docs/reviews/risky-debt-derivation-gap-proposals-v2.md
```

The command succeeded. Its JSON stdout was very large, so the Markdown artifact
was inspected directly.

## Inspection Evidence

`docs/reviews/risky-debt-derivation-gap-proposals-v2.md` contains:

- `Extracted target count: 3`;
- `Full-block fallback count: 0`;
- extracted targets `eq:risky-pricing`, `eq:foc-k`, and `eq:foc-b`;
- equation-level locations such as
  `risky-debt-maliar-deep-learning-lecture-note.tex > prop:interior-foc > eq:foc-b > line 781`;
- backend route plans for each extracted target;
- route statuses `requires_formalization` for LaTeX-heavy counterexample, Sage,
  and Lean routes;
- `Linked assumption repairs`;
- `Mathematically missing` reasoning;
- `How the derivation works under the assumptions`;
- the route boundary: route planning is diagnostic only.

## Repair During Phase

Initial v2 inspection showed route plans marked bounded counterexample and Sage
routes as ready for LaTeX-heavy risky-debt expressions, while the downstream
derivation route still reported those expressions as not encodable. The route
planner was tightened so LaTeX/domain-heavy targets are marked
`requires_formalization` for bounded counterexample and Sage routes. The v2
report was regenerated after that repair.

## Checks Run

| Command | Result |
| --- | --- |
| `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_target_extraction.py tests/test_backend_route_planner.py -q` | Passed: 14 passed. |
| `rg -n 'Extracted target count: 3\|Full-block fallback count: 0\|Target: \`eq:risky-pricing\`\|Target: \`eq:foc-k\`\|Target: \`eq:foc-b\`\|requires_formalization\|risky-debt-maliar-deep-learning-lecture-note\\.tex > prop:interior-foc > eq:foc-b > line 781\|Linked assumption repairs\|Mathematically missing\|Route planning is diagnostic only' docs/reviews/risky-debt-derivation-gap-proposals-v2.md` | Passed: all required markers found. |

## Boundary

The v2 report is more useful for agents because it names smaller obligations and
formalization routes, but it remains a diagnostic proposal artifact. It does not
prove the equations and does not apply any fixes.

## Next-Phase Handoff

Proceed to Phase 5 because:

- the v2 report preserves or improves required fields;
- focused tests pass;
- public-surface regression tests are named in the Phase 5 subplan.
