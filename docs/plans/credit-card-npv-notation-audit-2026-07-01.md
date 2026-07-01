# Credit Card NPV Proposal Notation Audit

Date: 2026-07-01

## Main Issue

The proposal has accumulated notation from literature review, valuation
architecture, and experimental design. Some symbols are overloaded. The
hardening pass should add a notation glossary and avoid changing every equation
unless necessary, because broad symbol rewrites are high-risk.

## Known Overloads

| Symbol | Current uses | Hardening treatment |
|---|---|---|
| `Z` | Lifecycle state in one place; randomized assignment in experimental section | Add glossary warning; use `Z^{assign}` or `R` in future experimental expansions. |
| `D` | Delinquency/default state; treatment received in experiments | Add glossary warning; use `T^{recv}` in future experimental expansions. |
| `S` | Spend, source component, sometimes state-like notation | Glossary distinguishes state vector from spend amount. |
| `P` | Payment behavior and probability-like notation | Glossary clarifies local meaning. |
| `H` | Generic horizon, observed horizon, valuation horizon | Use `H_obs` and `H_val` where horizon split matters. |
| `pi` | Downstream policy bundle | Keep stable; define once. |
| `s` | Scenario/valuation bundle | Keep stable; define once. |

## Recommended Minimal Fix

1. Add a notation conventions subsection near the valuation spine.
2. Add an appendix notation glossary.
3. Avoid mass renaming in this pass except where new sections can use cleaner
   notation.
4. In final re-architecture, consider a full notation normalization.

## Acceptance Check

The proposal should clearly warn readers that local equation symbols are
defined locally and that decision context, scenario, downstream policy, action,
baseline, and horizon are the stable global objects.
