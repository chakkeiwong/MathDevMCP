# Review Bundle: Derivation Target Extraction And Backend Routing Plan

READ-ONLY REVIEW ONLY.

Do not edit files, run experiments, launch agents, or change state.

## Objective

Review the next MathDevMCP derivation-lane plan. The goal is to improve the
current report workflow from full LaTeX proposition blocks to smaller extracted
equation/align-row obligations with deterministic backend route plans.

## Artifacts To Review

- `docs/plans/mathdevmcp-derivation-target-extraction-routing-master-program-2026-07-06.md`
- Phase 0-6 subplans under:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-phase-*`
- Visible runbook:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-visible-gated-execution-runbook-2026-07-06.md`
- Overnight plan:
  `docs/plans/mathdevmcp-derivation-target-extraction-routing-gated-overnight-execution-plan-2026-07-06.md`

## Current Baseline

The existing report workflow can write:

- `docs/reviews/risky-debt-derivation-gap-proposals.md`

It is useful and non-handwavy, but the recorded limitation is that labels are
sent as full LaTeX proposition blocks. The next plan should extract smaller
targets such as `eq:risky-pricing`, `eq:foc-k`, and `eq:foc-b`.

## Evidence Contract To Check

| Field | Contract |
| --- | --- |
| Question | Can MathDevMCP extract small derivation obligations from source labels and route them through deterministic tools without hallucinated proof claims? |
| Baseline/comparator | Current full-block `audit_and_propose_derivations` report. |
| Primary criterion | V2 risky-debt report groups extracted obligations under parent labels, preserves provenance, records backend route plans, and never promotes diagnostics to proof. |
| Veto diagnostics | Malformed lhs/rhs extraction; missing source location; backend diagnostic reported as proof; hidden backend unavailability; lost assumption repairs; generic fixes. |
| Not concluded | No proof of risky-debt correctness; no automatic source edits; no global theorem proving. |

## Specific Review Questions

1. Are phases ordered correctly: extraction before routing before report
   integration before risky-debt experiment?
2. Do subplans include objective, entry conditions, artifacts, checks/reviews,
   evidence contract, forbidden claims, handoff conditions, and stop
   conditions?
3. Are pass criteria based on artifacts that answer the phase question?
4. Are proof/refutation boundaries preserved?
5. Is the repair loop concrete enough to avoid stopping for non-blockers?
6. Does the overnight plan avoid launching detached work without explicit
   approval?

## Required Verdict Format

Findings first.

End with exactly one of:

```text
VERDICT: AGREE
```

or

```text
VERDICT: REVISE
```
