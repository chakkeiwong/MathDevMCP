# Compact Document Derivation Tree Audit

Source: `/home/chakwong/python/MathDevMCP/docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex`
Publication mode: `disabled`
Targets: `9`; gaps: `9`; repairs: `0`

This is a bounded transport summary. Exact detailed records remain in the digest-bound document artifact and page-token resolver.

| Label | Relation | Source role | Tree status | Specialist | Binding | Local obligations | Next action |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| `eq:panel-npv-functional` | `equality` | `policy_value_recursion` | `partial` | `typed_abstention` | `verified_current_evidence` | 5 | `blocked_for_human_or_formalization_choice` |
| `eq:incremental-cash-flow` | `equality` | `accounting_identity` | `partial` | `typed_abstention` | `verified_current_evidence` | 3 | `resolve_formalization_required` |
| `eq:pd-lgd-ead` | `equality` | `accounting_identity` | `partial` | `structurally_consistent` | `verified_current_evidence` | 3 | `resolve_formalization_required` |
| `eq:balance-stock-flow` | `equality` | `accounting_identity` | `partial` | `typed_abstention` | `verified_current_evidence` | 3 | `resolve_branch_bound_backend_execution_required` |
| `eq:terminal-value-base` | `equality` | `placeholder_definition` | `partial` | `algebraically_consistent` | `verified_current_evidence` | 3 | `resolve_formalization_required` |
| `eq:ss-bellman` | `equality` | `policy_value_recursion` | `partial` | `typed_abstention` | `verified_current_evidence` | 5 | `resolve_macro_translation_required` |
| `eq:causal-cashflow-object` | `conditional_expectation_object` | `causal_estimand_object` | `partial_evidence` | `typed_abstention` | `verified_current_evidence` | 4 | `resolve_conditioning_scope_translation_required` |
| `eq:experiment-late` | `equality` | `statistical_estimator` | `partial` | `typed_abstention` | `verified_current_evidence` | 6 | `resolve_macro_translation_required` |
| `eq:randomization-assumption` | `conditional_independence` | `identification_assumption` | `partial_evidence` | `typed_abstention` | `verified_current_evidence` | 5 | `resolve_formalization_required` |

## Exact Targets

### `eq:panel-npv-functional`

- Source digest: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
- Obligation: `obl_0ad9e77a200f3ab4397ce3fdf92ab7ec947c19c59fcd29bfb5bc4296f5602d68` / `0ad9e77a200f3ab4397ce3fdf92ab7ec947c19c59fcd29bfb5bc4296f5602d68`
- Binding: `{'binding_id': 'document_binding_258b4e7d6a33c004b9d89c613f067d1685af1b18d57a621e60a98946b510b468', 'binding_digest': '258b4e7d6a33c004b9d89c613f067d1685af1b18d57a621e60a98946b510b468'}`
- Specialist: `typed_abstention`; tool `None`; result `typed_abstention`
- Remaining local obligations: `['policy_value_paths_defined', 'discount_terminal_terms_defined', 'probability_kernel_defined', 'conditioning_object_defined', 'measurability_and_integrability']`

```tex
\Delta \NPV_i(a;d,s,\pi) = -C_i^{\mathrm{acq}}(a) + \E\!\left[ \sum_{h=0}^{H}\delta_h\Delta CF_{i,t+h}(a,\pi;s) +\delta_H\Delta TV_{i,t+H}(a,\pi;s) \mid X_{it}^{d} \right]
```

### `eq:incremental-cash-flow`

- Source digest: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
- Obligation: `obl_940ce16045ada1c2511e5fee4b1c78f3d1647886abd143ad1c5a1e588694c9b4` / `940ce16045ada1c2511e5fee4b1c78f3d1647886abd143ad1c5a1e588694c9b4`
- Binding: `{'binding_id': 'document_binding_a12c41d495357e6903688cc1a56f37552cff1c376db27edc8855556ba9b1d818', 'binding_digest': 'a12c41d495357e6903688cc1a56f37552cff1c376db27edc8855556ba9b1d818'}`
- Specialist: `typed_abstention`; tool `None`; result `typed_abstention`
- Remaining local obligations: `['component_definitions', 'sign_units_timing_aligned', 'local_component_exhaustiveness']`

```tex
\Delta CF_{i,t+h}(a,\pi;s) = \Delta PPNR_{i,t+h}(a,\pi;s) - \Delta EL_{i,t+h}(a,\pi;s) - \Delta Kchg_{i,t+h}(a,\pi;s) - \Delta Tax_{i,t+h}(a,\pi;s) + \Delta RelValue_{i,t+h}(a,\pi;s)
```

### `eq:pd-lgd-ead`

- Source digest: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
- Obligation: `obl_047784019a3ed01b3efa9c877aa23e2f518f74909071af0bdd64ce4d09b89a24` / `047784019a3ed01b3efa9c877aa23e2f518f74909071af0bdd64ce4d09b89a24`
- Binding: `{'binding_id': 'document_binding_c325bc86fa1169b8979ea3ea2ae72ca6f29d3cc556e95120d0fbec45c8ef94ff', 'binding_digest': 'c325bc86fa1169b8979ea3ea2ae72ca6f29d3cc556e95120d0fbec45c8ef94ff'}`
- Specialist: `structurally_consistent`; tool `sympy`; result `structurally_consistent`
- Remaining local obligations: `['component_definitions', 'sign_units_timing_aligned', 'local_component_exhaustiveness']`

```tex
EL_{i,t,h}(a) = PD_{i,t,h}(a)\, LGD_{i,t,h}(a)\, EAD_{i,t,h}(a)
```

### `eq:balance-stock-flow`

- Source digest: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
- Obligation: `obl_5d27537791c673d0f85dcfdbcfa67a1461995483a20023010e1881492ffa0caf` / `5d27537791c673d0f85dcfdbcfa67a1461995483a20023010e1881492ffa0caf`
- Binding: `{'binding_id': 'document_binding_d3e62d9da3ae06839e25e3979fa62dc223763a2d7c2ad923a4e8bbe204b715b9', 'binding_digest': 'd3e62d9da3ae06839e25e3979fa62dc223763a2d7c2ad923a4e8bbe204b715b9'}`
- Specialist: `typed_abstention`; tool `None`; result `typed_abstention`
- Remaining local obligations: `['component_definitions', 'sign_units_timing_aligned', 'local_component_exhaustiveness']`

```tex
B_{i,t+1} = B_{it} + S^{\mathrm{purchase}}_{it} + S^{\mathrm{cashadv}}_{it} + BT_{it} + Fee_{it} + Int_{it} - Pay_{it} - Credit_{it} - Chargeoff_{it} - OtherAdj_{it}
```

### `eq:terminal-value-base`

- Source digest: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
- Obligation: `obl_e30098a0fca1418294bee1d1326a7d0146ffaf87868803c2638111dcc7d8e60c` / `e30098a0fca1418294bee1d1326a7d0146ffaf87868803c2638111dcc7d8e60c`
- Binding: `{'binding_id': 'document_binding_e8c1fe4da562f189877224f6919591bf57ae36ed604c349159e5c2de11f171bf', 'binding_digest': 'e8c1fe4da562f189877224f6919591bf57ae36ed604c349159e5c2de11f171bf'}`
- Specialist: `algebraically_consistent`; tool `sympy`; result `algebraically_consistent`
- Remaining local obligations: `['terminal_denominator_nonzero', 'terminal_scalar_roles_units', 'terminal_sensitivity_boundary']`

```tex
\Delta TV_{i,H_{\mathrm{val}}} = \frac{\rho_i \, \widehat{\Delta CF}_{i,H_{\mathrm{val}}+1}} {r_{\mathrm{disc}}+\lambda_i+q_i}
```

### `eq:ss-bellman`

- Source digest: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
- Obligation: `obl_89291c822e1ad634ca670fbc0e7cae5bc76eb841f3cf3f10750f83e359104d16` / `89291c822e1ad634ca670fbc0e7cae5bc76eb841f3cf3f10750f83e359104d16`
- Binding: `{'binding_id': 'document_binding_c167fac54b0871ee15f48eee22fad535036be73b33891e100e441c42e0bfc6de', 'binding_digest': 'c167fac54b0871ee15f48eee22fad535036be73b33891e100e441c42e0bfc6de'}`
- Specialist: `typed_abstention`; tool `None`; result `typed_abstention`
- Remaining local obligations: `['bellman_state_action_domains', 'bellman_transition_kernel', 'bellman_reward_value_finite', 'bellman_horizon_boundary', 'bellman_policy_measurability']`

```tex
V_t^{\star}(b,O;s) = \max_{a\in\mathcal{A}_{t}(O,b;d,s,\pi^{gov})} \Bigl\{ \bar r_t(b,O,a;s,\pi^{down}) + \delta\,\E\left[V_{t+1}^{\star}(b',O';s)\mid b,O,a,s,\pi^{down}\right] \Bigr\}
```

### `eq:causal-cashflow-object`

- Source digest: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
- Obligation: `obl_2043ff659a2c53200273a428ab923078d91f274feb6769ad5b9dcd3ab9e63694` / `2043ff659a2c53200273a428ab923078d91f274feb6769ad5b9dcd3ab9e63694`
- Binding: `{'binding_id': 'document_binding_df316f978e4fcf76abe698aad0dac3a87507af1fca6d5fce40a98b4daef70a16', 'binding_digest': 'df316f978e4fcf76abe698aad0dac3a87507af1fca6d5fce40a98b4daef70a16'}`
- Specialist: `typed_abstention`; tool `None`; result `typed_abstention`
- Remaining local obligations: `['probability_kernel_defined', 'conditioning_object_defined', 'measurability_and_integrability', 'causal_identification_separate']`

```tex
\E\!\left[Y_i(a)-Y_i(a_0)\mid X_i, d, s, \pi\right]
```

### `eq:experiment-late`

- Source digest: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
- Obligation: `obl_26a5190e5c95d27967563168247d7cdbe825107bc7b2f8d7491c785e5d302df4` / `26a5190e5c95d27967563168247d7cdbe825107bc7b2f8d7491c785e5d302df4`
- Binding: `{'binding_id': 'document_binding_ff9b9446a6ae987a6de917a8b3b5992c88cde5002e628f4d16a4552b5a2166ab', 'binding_digest': 'ff9b9446a6ae987a6de917a8b3b5992c88cde5002e628f4d16a4552b5a2166ab'}`
- Specialist: `typed_abstention`; tool `None`; result `typed_abstention`
- Remaining local obligations: `['late_nonzero_first_stage', 'late_assignment_independence', 'late_exclusion', 'late_monotonicity', 'late_sutva_scope', 'late_complier_interpretation']`

```tex
\tau^{e}_{Y,\mathrm{LATE}} = \frac{\E[Y_i\mid Z_{ie}=1]-\E[Y_i\mid Z_{ie}=0]} {\E[D_{ie}\mid Z_{ie}=1]-\E[D_{ie}\mid Z_{ie}=0]}
```

### `eq:randomization-assumption`

- Source digest: `e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b`
- Obligation: `obl_1bef8104e6a761dea3d4618663ecba54ea95a79021dc0d5b45d293b070c16b9b` / `1bef8104e6a761dea3d4618663ecba54ea95a79021dc0d5b45d293b070c16b9b`
- Binding: `{'binding_id': 'document_binding_8fb21e7f16ed4ffe641aae7d2cb69eea4cf4a6cf0db618bb1db29ecd0279efed', 'binding_digest': '8fb21e7f16ed4ffe641aae7d2cb69eea4cf4a6cf0db618bb1db29ecd0279efed'}`
- Specialist: `typed_abstention`; tool `None`; result `typed_abstention`
- Remaining local obligations: `['assignment_mechanism_recorded', 'eligible_population_bound', 'randomization_unit_bound', 'interference_and_override_diagnostics', 'assignment_lineage_reconciled']`

```tex
Z_{ie} \perp\!\!\!\perp \{Y_i(a_e),Y_i(a_{0e}),\NPV_i(a_e),\NPV_i(a_{0e})\} \mid i\in\mathcal{P}_e
```

## Boundaries

- Current evidence binding establishes source/evidence identity and replay, not mathematical or scientific truth.
- Specialist CAS checks are scoped diagnostics; typed abstentions are not refutations.
- No candidate edit is applicable while publication mode is disabled.
- This selected-label audit does not establish whole-document correctness.
