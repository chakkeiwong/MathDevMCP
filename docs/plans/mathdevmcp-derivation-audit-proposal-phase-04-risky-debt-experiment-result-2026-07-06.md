# Phase 4 Result: Risky-Debt Derivation Report Experiment

Date: 2026-07-06

Status: `PASSED_WITH_RECORDED_LIMITATION`

## Objective

Apply `audit_and_propose_derivations` to the risky-debt lecture note labels and
inspect whether the generated Markdown is concrete enough for another agent to
use.

## Command

```bash
python3 -c 'from mathdevmcp.derivation_audit_report import audit_and_propose_derivations; r=audit_and_propose_derivations("Audit risky-debt derivations", root="docs", labels=["prop:risky-pricing", "prop:interior-foc"], output_path="docs/reviews/risky-debt-derivation-gap-proposals.md"); print({"status": r["status"], "targets": r["coverage"]["target_count"], "gaps": r["coverage"]["gap_count"], "proposals": r["coverage"]["proposal_count"], "validation": r["validation"]["status_counts"], "coverage_gaps": r["coverage"]["coverage_gaps"]})'
```

Observed summary:

```text
{'status': 'proposal_ready', 'targets': 2, 'gaps': 2, 'proposals': 2, 'validation': {'blocked_by_missing_assumptions': 2}, 'coverage_gaps': []}
```

## Artifact

- `docs/reviews/risky-debt-derivation-gap-proposals.md`

## Required-Field Inspection

Passed:

- `Location`
- `Problem`
- `Why`
- `Proposed fix`
- `Derivation route`
- `Backend plan`
- `Validation`
- `Evidence refs`
- linked assumption repairs
- possible sufficient assumption sets
- how the derivation works under assumptions
- non-claims
- exact tool-use arguments

No generic `collect_more_evidence` wording was found.

## Mathematical Content Observed

For `prop:risky-pricing`, the report proposes:

- conditional transition law for `z' | z`;
- measurability and conditional integrability for default/recovery and solvent
  payoff terms;
- zero-profit/risk-neutral pricing convention for positive promised debt;
- finite-state and kernel-integrability sufficient assumption sets;
- a derivation route through payoff random variable definition, conditional
  expectation, zero-profit convention, and substitution back into the displayed
  pricing equation.

For `prop:interior-foc`, the report proposes:

- conditional law for continuation shocks;
- differentiability of `V^\star(k',b',z')` in `k'` and `b'`;
- conditional integrability or domination of value derivatives;
- choice-independence of the transition law to avoid omitted kernel-derivative
  terms;
- finite-state and dominated-interchange sufficient assumption sets;
- a derivation route through the smooth interior objective, chain rule,
  derivative-expectation interchange, kernel-term exclusion, and interior
  optimality.

## Required Checks

Passed:

- `python3 -m pytest tests/test_derivation_audit_report.py tests/test_derivation_gap_proposals.py tests/test_derive_from.py tests/test_derive_or_refute.py -q`
  - `28 passed`
- `python3 -m compileall -q src/mathdevmcp/derivation_audit_report.py src/mathdevmcp/derive_from.py src/mathdevmcp/derivation_gap_proposals.py`
  - passed

Pending until this result file is included:

- `git diff --check -- docs/reviews/risky-debt-derivation-gap-proposals.md docs/plans/mathdevmcp-derivation-audit-proposal-phase-04-risky-debt-experiment-result-2026-07-06.md`

## Evidence Contract Result

| Field | Result |
| --- | --- |
| Question | Does the new report workflow produce a useful derivation gap/proposal report for risky-debt labels? |
| Primary criterion | Passed for localized, concrete missing-assumption derivation proposals. |
| Veto diagnostics | No missing locations; no generic proposal text; tool-use arguments visible; validation boundary visible; no proof closure claimed. |
| Not concluded | The risky-debt note is not proven correct; no edits were applied; proposed assumptions are not certified sufficient by backend rerun. |

## Recorded Limitation

The label target sent to `derive_from` is currently the full LaTeX proposition
block. That is enough for deterministic assumption discovery, but too broad for
backend proof search. A later phase should add smaller target extraction from
displayed equations or proof-audit obligations so Lean/Sage/SymPy can attempt
more focused derivation routes.

## Next Handoff

Phase 5 should expose the report workflow through CLI/MCP parity and add tests
for the public surface. Phase 6 should improve target extraction if the public
workflow needs smaller equation-level obligations for backend proof attempts.
