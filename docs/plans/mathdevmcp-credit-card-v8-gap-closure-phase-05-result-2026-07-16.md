# Phase 05 Result: Role-Specific Obligations

Date: 2026-07-16

Decision: `PASS`

## Objective Result

Exact source-evidenced v8 targets now use a closed role-specific obligation
contract. Local correctness obligations and downstream integration obligations
are separate. Targets without a reviewed specialist builder retain the prior
generic diagnostic route.

## Evidence

- PD/LGD/EAD and stock-flow identities receive component-definition,
  sign/unit/timing, and local-exhaustiveness obligations only.
- Counterfactual and discount/terminal requirements are recorded separately as
  downstream integration obligations, not local blockers.
- Terminal value receives exact denominator, scalar/unit, sensitivity, and
  placeholder/economic-boundary obligations.
- Conditional expectation receives kernel, conditioning-object,
  measurability/integrability, and separate causal-identification obligations.
- LATE receives nonzero first stage, assignment independence, exclusion,
  monotonicity, SUTVA/unit, and local-complier interpretation obligations.
- Randomization receives mechanism, population, unit, interference/override,
  and lineage obligations without claiming the assumption holds.
- Bellman receives state/action/feasibility, transition, finiteness,
  horizon/boundary, and policy-measurability obligations.
- No Bellman `conformable_product_required` blocker appears.
- Cue-free generic NPV/Bellman and theorem/proposition FOC paths preserve their
  established generic behavior.
- Focused exact/fallback suite: `3 passed`; broader preceding role/tree suite
  passed 52 tests with four dispatch failures, all diagnosed and repaired.

## Decision Table

| Decision | Primary criterion | Veto status | Main uncertainty | Next justified action | Not concluded |
| --- | --- | --- | --- | --- | --- |
| Pass Phase 05 | Role relevance and negative controls | No generic NPV spillover or false Bellman shape blocker | Specialist results remain disconnected or absent | Integrate deterministic external-tool execution | Assumption truth, minimality, causal identification, or policy optimality |

## Residual Risks

- Role builders are closed and intentionally incomplete; unsupported roles use
  the generic route.
- The obligation sets are candidate sufficient/review conditions, not globally
  minimal mathematical assumptions.
- Source prose can route but cannot discharge empirical or scientific
  obligations.

## Non-Claims

- Randomization is not established.
- LATE is not identified from the displayed ratio alone.
- Bellman notation is not a proof of optimality.
- No source or publication state changed.

## Phase 06 Handoff

Supported deterministic routes may now execute only after exact role and local
obligation binding. Phase 06 should integrate the existing terminal-value SymPy
adapter and one bounded scalar accounting normalization into proof/tree/fix
state while unsupported causal/policy lanes return typed actionable abstention.
