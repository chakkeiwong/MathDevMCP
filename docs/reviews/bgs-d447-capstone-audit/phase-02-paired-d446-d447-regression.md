# Paired D446/D447 Regression

Status: `passed`

D447 is a contaminated repaired successor, so this is a regression test rather than an independent holdout.

## Gates

- `all_documented_repairs_present_only_in_d447`: `True`
- `boundary_prose_not_math_claim`: `True`
- `deposit_bridge_diagnostic_only`: `True`
- `fixed_point_mismatch_localized_to_theta`: `True`
- `obc_external_route_recorded`: `True`
- `paired_derivation_results_preserved`: `True`

## Repair Delta

| Repair | Label | D446 phrases present | D447 phrases present |
| --- | --- | --- | --- |
| `opening_audit_boundary` | `opening` | `[False, False]` | `[True, True]` |
| `risk_premium_boundary` | `eq:sw-bgs-risk-premium-conversion` | `[False, False]` | `[True, True]` |
| `obc_boundary` | `eq:bgs-obc-policy-shortfall` | `[False, False]` | `[True, True]` |
| `likelihood_scope_boundary` | `eq:crosscheck-kernel-decomposition` | `[False, False]` | `[True, True]` |

## Derivation Statuses

- `eq:bgs-obc-policy-shortfall`: D446 `inconclusive`; D447 `inconclusive`
- `eq:crosscheck-kernel-decomposition`: D446 `inconclusive`; D447 `inconclusive`
- `eq:sw-bgs-risk-premium-conversion`: D446 `inconclusive`; D447 `inconclusive`

Changed boundary prose is document evidence, not proof of unchanged equations.
