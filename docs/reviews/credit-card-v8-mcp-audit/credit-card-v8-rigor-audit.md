# Compact Math Document Rigor Audit

Source: `credit_card_npv_component_proposal_v8.tex`
Source SHA-256: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
Coverage: `partial_coverage`; targets `9`; gaps `2`; concrete repairs `0`; diagnostic abstentions `2`

This is a bounded transport summary. Exact detailed records remain available through `resolve_agent_report`.
Detailed artifact: `f4fb29dcb0db92b11d4197e672830967f055e4f2647db67af93b79f8e92b67ed` (326275 bytes; state `verified`).

| Label | Relation | Source role | Line |
| --- | --- | --- | ---: |
| `eq:panel-npv-functional` | `equality` | `policy_value_recursion` | 683 |
| `eq:incremental-cash-flow` | `equality` | `accounting_identity` | 860 |
| `eq:pd-lgd-ead` | `equality` | `accounting_identity` | 2159 |
| `eq:balance-stock-flow` | `equality` | `accounting_identity` | 2240 |
| `eq:terminal-value-base` | `equality` | `placeholder_definition` | 7189 |
| `eq:ss-bellman` | `equality` | `policy_value_recursion` | 4086 |
| `eq:causal-cashflow-object` | `conditional_expectation_object` | `causal_estimand_object` | 4791 |
| `eq:experiment-late` | `equality` | `statistical_estimator` | 5607 |
| `eq:randomization-assumption` | `conditional_independence` | `identification_assumption` | 6015 |

## Gap Ledger

| Label | Classification | Problem | Evidence |
| --- | --- | --- | --- |
| `obligation_1` | `diagnostic_abstention` | The claim still needs human review before certification. | `proof_audit_v2:eq:incremental-cash-flow:obligation_1` |
| `obligation_1` | `diagnostic_abstention` | The complete source-bound target is localized but remains uncertified. | `proof_audit_v2:eq:incremental-cash-flow:obligation_1` |

## Role-Specific Obligation Ledger

### `eq:panel-npv-functional`

- Local obligations: `['policy_value_paths_defined', 'discount_terminal_terms_defined', 'probability_kernel_defined', 'conditioning_object_defined', 'measurability_and_integrability']`
- Downstream-only integration obligations: `[]`
- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.

### `eq:incremental-cash-flow`

- Local obligations: `['component_definitions', 'sign_units_timing_aligned', 'local_component_exhaustiveness']`
- Downstream-only integration obligations: `['downstream_counterfactual_mapping', 'downstream_discount_terminal_policy']`
- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.

### `eq:pd-lgd-ead`

- Local obligations: `['component_definitions', 'sign_units_timing_aligned', 'local_component_exhaustiveness']`
- Downstream-only integration obligations: `['downstream_counterfactual_mapping', 'downstream_discount_terminal_policy']`
- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.

### `eq:balance-stock-flow`

- Local obligations: `['component_definitions', 'sign_units_timing_aligned', 'local_component_exhaustiveness']`
- Downstream-only integration obligations: `['downstream_counterfactual_mapping', 'downstream_discount_terminal_policy']`
- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.

### `eq:terminal-value-base`

- Local obligations: `['terminal_denominator_nonzero', 'terminal_scalar_roles_units', 'terminal_sensitivity_boundary']`
- Downstream-only integration obligations: `[]`
- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.

### `eq:ss-bellman`

- Local obligations: `['bellman_state_action_domains', 'bellman_transition_kernel', 'bellman_reward_value_finite', 'bellman_horizon_boundary', 'bellman_policy_measurability']`
- Downstream-only integration obligations: `[]`
- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.

### `eq:causal-cashflow-object`

- Local obligations: `['probability_kernel_defined', 'conditioning_object_defined', 'measurability_and_integrability', 'causal_identification_separate']`
- Downstream-only integration obligations: `[]`
- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.

### `eq:experiment-late`

- Local obligations: `['late_nonzero_first_stage', 'late_assignment_independence', 'late_exclusion', 'late_monotonicity', 'late_sutva_scope', 'late_complier_interpretation']`
- Downstream-only integration obligations: `[]`
- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.

### `eq:randomization-assumption`

- Local obligations: `['assignment_mechanism_recorded', 'eligible_population_bound', 'randomization_unit_bound', 'interference_and_override_diagnostics', 'assignment_lineage_reconciled']`
- Downstream-only integration obligations: `[]`
- Boundary: the source role selects relevant checks but does not establish their assumptions or truth.


## Boundaries

- `document_rigor_audit_not_document_proof`: The report is a rigor gap/proposal ledger, not a proof of the document.
- `partial_coverage_not_exhaustive`: Limited target selection is not an exhaustive full-document audit.
- `leandojo_not_certificate`: LeanDojo proof search is not a certificate unless the reconstructed Lean source passes direct Lean checking without placeholders.
