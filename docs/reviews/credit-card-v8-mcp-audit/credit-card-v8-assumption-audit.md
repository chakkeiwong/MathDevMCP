# Assumption Gap/Proposal Report

Question: Which explicit assumptions are needed by the selected v8 mathematical objects?

Status: `proposal_ready`

## Coverage

- Targets inspected: 9
- Gaps: 9
- Proposals: 9

## Tool Uses

| Tool | Purpose | Status |
| --- | --- | --- |
| `build_index` | Extract LaTeX labels and source locations for assumption auditing. | `completed` |
| `assumptions_required` | Detect route-required assumptions with a bounded deterministic rule set. | `completed` |
| `build_assumption_gaps` | Convert missing assumption records into localized gap objects. | `completed` |
| `build_assumption_proposals` | Create concrete assumption proposals linked to detected gaps. | `completed` |
| `build_role_specific_obligations` | Replace generic string-route gaps with source-role-local mathematical obligations. | `role_specific_obligations` |
| `assumptions_required` | Detect route-required assumptions with a bounded deterministic rule set. | `completed` |
| `build_assumption_gaps` | Convert missing assumption records into localized gap objects. | `completed` |
| `build_assumption_proposals` | Create concrete assumption proposals linked to detected gaps. | `completed` |
| `build_role_specific_obligations` | Replace generic string-route gaps with source-role-local mathematical obligations. | `role_specific_obligations` |
| `assumptions_required` | Detect route-required assumptions with a bounded deterministic rule set. | `completed` |
| `build_assumption_gaps` | Convert missing assumption records into localized gap objects. | `completed` |
| `build_assumption_proposals` | Create concrete assumption proposals linked to detected gaps. | `completed` |
| `build_role_specific_obligations` | Replace generic string-route gaps with source-role-local mathematical obligations. | `role_specific_obligations` |
| `assumptions_required` | Detect route-required assumptions with a bounded deterministic rule set. | `completed` |
| `build_assumption_gaps` | Convert missing assumption records into localized gap objects. | `completed` |
| `build_assumption_proposals` | Create concrete assumption proposals linked to detected gaps. | `completed` |
| `build_role_specific_obligations` | Replace generic string-route gaps with source-role-local mathematical obligations. | `role_specific_obligations` |
| `assumptions_required` | Detect route-required assumptions with a bounded deterministic rule set. | `completed` |
| `build_assumption_gaps` | Convert missing assumption records into localized gap objects. | `completed` |
| `build_assumption_proposals` | Create concrete assumption proposals linked to detected gaps. | `completed` |
| `build_role_specific_obligations` | Replace generic string-route gaps with source-role-local mathematical obligations. | `role_specific_obligations` |
| `assumptions_required` | Detect route-required assumptions with a bounded deterministic rule set. | `completed` |
| `build_assumption_gaps` | Convert missing assumption records into localized gap objects. | `completed` |
| `build_assumption_proposals` | Create concrete assumption proposals linked to detected gaps. | `completed` |
| `build_role_specific_obligations` | Replace generic string-route gaps with source-role-local mathematical obligations. | `role_specific_obligations` |
| `assumptions_required` | Detect route-required assumptions with a bounded deterministic rule set. | `completed` |
| `build_assumption_gaps` | Convert missing assumption records into localized gap objects. | `completed` |
| `build_assumption_proposals` | Create concrete assumption proposals linked to detected gaps. | `completed` |
| `build_role_specific_obligations` | Replace generic string-route gaps with source-role-local mathematical obligations. | `role_specific_obligations` |
| `assumptions_required` | Detect route-required assumptions with a bounded deterministic rule set. | `completed` |
| `build_assumption_gaps` | Convert missing assumption records into localized gap objects. | `completed` |
| `build_assumption_proposals` | Create concrete assumption proposals linked to detected gaps. | `completed` |
| `build_role_specific_obligations` | Replace generic string-route gaps with source-role-local mathematical obligations. | `role_specific_obligations` |
| `assumptions_required` | Detect route-required assumptions with a bounded deterministic rule set. | `completed` |
| `build_assumption_gaps` | Convert missing assumption records into localized gap objects. | `completed` |
| `build_assumption_proposals` | Create concrete assumption proposals linked to detected gaps. | `completed` |
| `build_role_specific_obligations` | Replace generic string-route gaps with source-role-local mathematical obligations. | `role_specific_obligations` |

## Gaps And Proposals

### eq:panel-npv-functional

- Proposal: `assumption_proposal_0ad9e77a200f3ab4_role_policy_value_recursion`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:panel-npv-functional > line 683`
  - Problem: The source-evidenced `policy_value_recursion` target has 5 undischarged local obligations.
  - Why: A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. These local obligations must be bound or discharged before claim promotion.
  - Proposed assumption: State, source-bind, or discharge the 5 local obligations for the source-evidenced `policy_value_recursion` route; do not import downstream conditions as local correctness requirements.
  - Validation: `validated_by_source_role_rule`; Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.
  - Evidence refs: `source:e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b:0ad9e77a200f3ab4397ce3fdf92ab7ec947c19c59fcd29bfb5bc4296f5602d68`, `routing_role:role_4c3eda1e521b7b4e5b80ea51ad5beaeb03eb2be794a007ee02b5dd5df366485f`, `role_obligation:policy_value_paths_defined`, `role_obligation:discount_terminal_terms_defined`, `role_obligation:probability_kernel_defined`, `role_obligation:conditioning_object_defined`, `role_obligation:measurability_and_integrability`

  - Mathematical missing-assumption reasoning:
    - policy_value_paths_defined (valuation_scope_condition): Action, baseline, scenario, downstream policy, horizon, and information set. Why missing: A discounted contrast is ambiguous without aligned paths and scope.
    - discount_terminal_terms_defined (valuation_condition): Discount factors and terminal-value convention on the stated horizon. Why missing: The aggregate depends on timing and tail treatment.
    - probability_kernel_defined (probability_condition): A probability space or conditional kernel for the random object. Why missing: Conditional expectation is undefined without a law.
    - conditioning_object_defined (information_condition): The conditioning sigma-field, state, or covariate object. Why missing: The conditional bar determines the information scope.
    - measurability_and_integrability (integrability_condition): Measurability and finite conditional first moments for the integrand. Why missing: The expectation may otherwise be undefined or infinite.

  - Possible sufficient assumption sets:
    - `finite_horizon_policy_value` (valuation sufficient condition): The policy-value functional is well defined.
      - Action and baseline paths share scenario, policy, horizon, and information.
      - Discount and terminal terms are finite and defined.
      - The conditional cash-flow object is integrable.
    - `conditional_kernel_integrability` (general sufficient condition): The conditional expectation is well defined.
      - A conditional kernel is fixed.
      - The integrand is measurable.
      - The integrand has a finite conditional first moment.

  - How the derivation works under the assumptions:
    - Align paths: Bind action/baseline, scenario, downstream policy, horizon, and information.
    - Define valuation terms: Bind discount factors and terminal convention.
    - Bind probability objects: Define the random object, conditioning object, and conditional kernel.
    - Check integrability: Establish measurability and finite conditional first moments.
    - Preserve causal boundary: Do not infer identification from well-defined expectation notation.

### eq:incremental-cash-flow

- Proposal: `assumption_proposal_940ce16045ada1c2_role_accounting_identity`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:incremental-cash-flow > line 860`
  - Problem: The source-evidenced `accounting_identity` target has 3 undischarged local obligations.
  - Why: A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. These local obligations must be bound or discharged before claim promotion.
  - Proposed assumption: State, source-bind, or discharge the 3 local obligations for the source-evidenced `accounting_identity` route; do not import downstream conditions as local correctness requirements.
  - Validation: `validated_by_source_role_rule`; Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.
  - Evidence refs: `source:e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b:940ce16045ada1c2511e5fee4b1c78f3d1647886abd143ad1c5a1e588694c9b4`, `routing_role:role_9054aec76ac3d5e6d35ed05b4707bdaa612d1c30f433ebf345bc12b5f613f32f`, `role_obligation:component_definitions`, `role_obligation:sign_units_timing_aligned`, `role_obligation:local_component_exhaustiveness`

  - Mathematical missing-assumption reasoning:
    - component_definitions (accounting_definition_condition): Definitions for every component in the local identity. Why missing: Undefined components make reconciliation ambiguous.
    - sign_units_timing_aligned (accounting_alignment_condition): A common sign, unit/currency, and timing convention. Why missing: Misaligned conventions can make a syntactically valid sum economically inconsistent.
    - local_component_exhaustiveness (accounting_exhaustiveness_condition): A statement of local exhaustiveness or a named residual/adjustment term. Why missing: An accounting identity needs a declared local boundary for omitted components.

  - Possible sufficient assumption sets:
    - `local_accounting_contract` (local sufficient condition): The local accounting identity is well posed.
      - All displayed components are defined.
      - Signs, units, and timing are aligned.
      - The displayed components are locally exhaustive or include a residual.

  - How the derivation works under the assumptions:
    - Define components: Bind each local component to its accounting meaning.
    - Align conventions: Check signs, units, and timing.
    - Reconcile locally: Check the sum without importing downstream valuation requirements.

### eq:pd-lgd-ead

- Proposal: `assumption_proposal_047784019a3ed01b_role_accounting_identity`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:pd-lgd-ead > line 2159`
  - Problem: The source-evidenced `accounting_identity` target has 3 undischarged local obligations.
  - Why: A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. These local obligations must be bound or discharged before claim promotion.
  - Proposed assumption: State, source-bind, or discharge the 3 local obligations for the source-evidenced `accounting_identity` route; do not import downstream conditions as local correctness requirements.
  - Validation: `validated_by_source_role_rule`; Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.
  - Evidence refs: `source:e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b:047784019a3ed01b3efa9c877aa23e2f518f74909071af0bdd64ce4d09b89a24`, `routing_role:role_14a32134fa9454bea6f77698b6c9b7503024487862eafa3f31c5210e2fbb49c8`, `role_obligation:component_definitions`, `role_obligation:sign_units_timing_aligned`, `role_obligation:local_component_exhaustiveness`

  - Mathematical missing-assumption reasoning:
    - component_definitions (accounting_definition_condition): Definitions for every component in the local identity. Why missing: Undefined components make reconciliation ambiguous.
    - sign_units_timing_aligned (accounting_alignment_condition): A common sign, unit/currency, and timing convention. Why missing: Misaligned conventions can make a syntactically valid sum economically inconsistent.
    - local_component_exhaustiveness (accounting_exhaustiveness_condition): A statement of local exhaustiveness or a named residual/adjustment term. Why missing: An accounting identity needs a declared local boundary for omitted components.

  - Possible sufficient assumption sets:
    - `local_accounting_contract` (local sufficient condition): The local accounting identity is well posed.
      - All displayed components are defined.
      - Signs, units, and timing are aligned.
      - The displayed components are locally exhaustive or include a residual.

  - How the derivation works under the assumptions:
    - Define components: Bind each local component to its accounting meaning.
    - Align conventions: Check signs, units, and timing.
    - Reconcile locally: Check the sum without importing downstream valuation requirements.

### eq:balance-stock-flow

- Proposal: `assumption_proposal_5d27537791c673d0_role_accounting_identity`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:balance-stock-flow > line 2240`
  - Problem: The source-evidenced `accounting_identity` target has 3 undischarged local obligations.
  - Why: A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. These local obligations must be bound or discharged before claim promotion.
  - Proposed assumption: State, source-bind, or discharge the 3 local obligations for the source-evidenced `accounting_identity` route; do not import downstream conditions as local correctness requirements.
  - Validation: `validated_by_source_role_rule`; Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.
  - Evidence refs: `source:e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b:5d27537791c673d0f85dcfdbcfa67a1461995483a20023010e1881492ffa0caf`, `routing_role:role_367da26d2fc5d28bd44cad3bf492fb37c6077276f8e63b838b0b6aa92948d54e`, `role_obligation:component_definitions`, `role_obligation:sign_units_timing_aligned`, `role_obligation:local_component_exhaustiveness`

  - Mathematical missing-assumption reasoning:
    - component_definitions (accounting_definition_condition): Definitions for every component in the local identity. Why missing: Undefined components make reconciliation ambiguous.
    - sign_units_timing_aligned (accounting_alignment_condition): A common sign, unit/currency, and timing convention. Why missing: Misaligned conventions can make a syntactically valid sum economically inconsistent.
    - local_component_exhaustiveness (accounting_exhaustiveness_condition): A statement of local exhaustiveness or a named residual/adjustment term. Why missing: An accounting identity needs a declared local boundary for omitted components.

  - Possible sufficient assumption sets:
    - `local_accounting_contract` (local sufficient condition): The local accounting identity is well posed.
      - All displayed components are defined.
      - Signs, units, and timing are aligned.
      - The displayed components are locally exhaustive or include a residual.

  - How the derivation works under the assumptions:
    - Define components: Bind each local component to its accounting meaning.
    - Align conventions: Check signs, units, and timing.
    - Reconcile locally: Check the sum without importing downstream valuation requirements.

### eq:terminal-value-base

- Proposal: `assumption_proposal_e30098a0fca14182_role_placeholder_definition`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:terminal-value-base > line 7189`
  - Problem: The source-evidenced `placeholder_definition` target has 3 undischarged local obligations.
  - Why: A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. These local obligations must be bound or discharged before claim promotion.
  - Proposed assumption: State, source-bind, or discharge the 3 local obligations for the source-evidenced `placeholder_definition` route; do not import downstream conditions as local correctness requirements.
  - Validation: `validated_by_source_role_rule`; Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.
  - Evidence refs: `source:e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b:e30098a0fca1418294bee1d1326a7d0146ffaf87868803c2638111dcc7d8e60c`, `routing_role:role_1dc66a422bff11ee09177d26781a56aa7a329992bba2262280f01bdc605b211c`, `role_obligation:terminal_denominator_nonzero`, `role_obligation:terminal_scalar_roles_units`, `role_obligation:terminal_sensitivity_boundary`

  - Mathematical missing-assumption reasoning:
    - terminal_denominator_nonzero (domain_condition): The exact terminal-value denominator is nonzero on the scoped domain. Why missing: Division is undefined at a zero denominator.
    - terminal_scalar_roles_units (type_and_unit_condition): Scalar roles, compatible time units, and signs for persistence, discount, hazard, and decay terms. Why missing: A scalar quotient can be dimensionally or temporally incoherent.
    - terminal_sensitivity_boundary (definition_boundary_condition): Sensitivity cases and an explicit boundary between placeholder definition and economic validity. Why missing: Algebraic consistency does not establish a defensible extrapolation.

  - Possible sufficient assumption sets:
    - `terminal_placeholder_contract` (definition-scoped sufficient condition): The terminal definition is algebraically well posed without claiming economic validity.
      - The exact denominator is nonzero.
      - All terms use compatible units and timing.
      - The formula remains an explicit stress-tested placeholder.

  - How the derivation works under the assumptions:
    - Bind scalar terms: Define every numerator and denominator term with units.
    - Check denominator: Verify the exact denominator is nonzero before cross-multiplication.
    - Stress definition: Report zero-tail and alternative persistence/decay cases separately.

### eq:ss-bellman

- Proposal: `assumption_proposal_89291c822e1ad634_role_policy_value_recursion`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:ss-bellman > line 4086`
  - Problem: The source-evidenced `policy_value_recursion` target has 5 undischarged local obligations.
  - Why: A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. These local obligations must be bound or discharged before claim promotion.
  - Proposed assumption: State, source-bind, or discharge the 5 local obligations for the source-evidenced `policy_value_recursion` route; do not import downstream conditions as local correctness requirements.
  - Validation: `validated_by_source_role_rule`; Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.
  - Evidence refs: `source:e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b:89291c822e1ad634ca670fbc0e7cae5bc76eb841f3cf3f10750f83e359104d16`, `routing_role:role_5a4a23f00e7c08b45264a2f0e22b69747f60dee6f46fd23bc76856019872ecd8`, `role_obligation:bellman_state_action_domains`, `role_obligation:bellman_transition_kernel`, `role_obligation:bellman_reward_value_finite`, `role_obligation:bellman_horizon_boundary`, `role_obligation:bellman_policy_measurability`

  - Mathematical missing-assumption reasoning:
    - bellman_state_action_domains (dynamic_programming_condition): State/belief and action domains with a nonempty feasible set. Why missing: The maximum is not well posed without its domain.
    - bellman_transition_kernel (probability_condition): A transition kernel for next state/observation conditional on current state and action. Why missing: The continuation expectation needs a law.
    - bellman_reward_value_finite (integrability_condition): Measurable finite rewards and integrable continuation value. Why missing: The objective may otherwise be undefined or infinite.
    - bellman_horizon_boundary (recursion_boundary_condition): A horizon plus terminal/transversality/contraction boundary. Why missing: A recursion needs a closing condition.
    - bellman_policy_measurability (policy_regularness_condition): A measurable admissible policy/selector or finite-action substitute. Why missing: An optimizer may not define an admissible policy without selection conditions.

  - Possible sufficient assumption sets:
    - `finite_or_regular_bellman_contract` (sufficient dynamic-programming conditions): The Bellman operator is well defined without proving global optimality for the document model.
      - Feasible actions are nonempty.
      - Rewards and transitions are measurable and finite/integrable.
      - A terminal or contraction condition is stated.
      - A measurable policy selector exists or action sets are finite.

  - How the derivation works under the assumptions:
    - Bind domains: Define state, action, feasibility, and policy class.
    - Bind reward and kernel: Define finite rewards and stochastic transitions.
    - Close recursion: State terminal/transversality/contraction conditions.
    - Certify only scoped properties: Do not infer economic validity or global optimality from symbolic form.

### eq:causal-cashflow-object

- Proposal: `assumption_proposal_2043ff659a2c5320_role_causal_estimand_object`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:causal-cashflow-object > line 4791`
  - Problem: The source-evidenced `causal_estimand_object` target has 4 undischarged local obligations.
  - Why: A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. These local obligations must be bound or discharged before claim promotion.
  - Proposed assumption: State, source-bind, or discharge the 4 local obligations for the source-evidenced `causal_estimand_object` route; do not import downstream conditions as local correctness requirements.
  - Validation: `validated_by_source_role_rule`; Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.
  - Evidence refs: `source:e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b:2043ff659a2c53200273a428ab923078d91f274feb6769ad5b9dcd3ab9e63694`, `routing_role:role_1f8d18ddbfe61114b4a10f637f819b60db2f0c5addef5a2d2f966a90ec0216ef`, `role_obligation:probability_kernel_defined`, `role_obligation:conditioning_object_defined`, `role_obligation:measurability_and_integrability`, `role_obligation:causal_identification_separate`

  - Mathematical missing-assumption reasoning:
    - probability_kernel_defined (probability_condition): A probability space or conditional kernel for the random object. Why missing: Conditional expectation is undefined without a law.
    - conditioning_object_defined (information_condition): The conditioning sigma-field, state, or covariate object. Why missing: The conditional bar determines the information scope.
    - measurability_and_integrability (integrability_condition): Measurability and finite conditional first moments for the integrand. Why missing: The expectation may otherwise be undefined or infinite.
    - causal_identification_separate (causal_boundary_condition): A separate identification argument for the causal interpretation. Why missing: Well-defined potential-outcome notation does not identify it from observed data.

  - Possible sufficient assumption sets:
    - `conditional_kernel_integrability` (general sufficient condition): The conditional expectation is well defined.
      - A conditional kernel is fixed.
      - The integrand is measurable.
      - The integrand has a finite conditional first moment.

  - How the derivation works under the assumptions:
    - Bind probability objects: Define the random object, conditioning object, and conditional kernel.
    - Check integrability: Establish measurability and finite conditional first moments.
    - Preserve causal boundary: Do not infer identification from well-defined expectation notation.

### eq:experiment-late

- Proposal: `assumption_proposal_26a5190e5c95d279_role_statistical_estimator`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:experiment-late > line 5607`
  - Problem: The source-evidenced `statistical_estimator` target has 6 undischarged local obligations.
  - Why: A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. These local obligations must be bound or discharged before claim promotion.
  - Proposed assumption: State, source-bind, or discharge the 6 local obligations for the source-evidenced `statistical_estimator` route; do not import downstream conditions as local correctness requirements.
  - Validation: `validated_by_source_role_rule`; Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.
  - Evidence refs: `source:e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b:26a5190e5c95d27967563168247d7cdbe825107bc7b2f8d7491c785e5d302df4`, `routing_role:role_3b44932b13bf22e9959d7b4ad5acfc0e7b6fa40831193ca2a33b1108cfba8ec5`, `role_obligation:late_nonzero_first_stage`, `role_obligation:late_assignment_independence`, `role_obligation:late_exclusion`, `role_obligation:late_monotonicity`, `role_obligation:late_sutva_scope`, `role_obligation:late_complier_interpretation`

  - Mathematical missing-assumption reasoning:
    - late_nonzero_first_stage (instrument_relevance_condition): A nonzero assignment-to-receipt first stage for the exact eligible population. Why missing: The LATE denominator must be nonzero.
    - late_assignment_independence (identification_condition): Instrument assignment independence in the scoped population. Why missing: Algebra alone cannot identify the causal contrast.
    - late_exclusion (identification_condition): Exclusion of direct assignment effects outside treatment receipt. Why missing: Direct assignment pathways invalidate the IV interpretation.
    - late_monotonicity (identification_condition): Monotonic treatment take-up with no defiers in the scoped design. Why missing: Without monotonicity the ratio lacks the local complier interpretation.
    - late_sutva_scope (causal_scope_condition): SUTVA/no-interference and a defined randomization/treatment unit. Why missing: Spillovers or treatment-version ambiguity change the estimand.
    - late_complier_interpretation (interpretation_boundary): An explicit local-complier interpretation and transport non-claim. Why missing: LATE is not the population ATE without additional evidence.

  - Possible sufficient assumption sets:
    - `late_identification_contract` (standard IV sufficient conditions): The ratio has a scoped local-complier causal interpretation.
      - The first stage is nonzero.
      - Assignment is independent in the eligible population.
      - Exclusion and monotonicity hold.
      - Treatment versions and interference are controlled.

  - How the derivation works under the assumptions:
    - Check first stage: Verify the exact denominator contrast is nonzero.
    - Bind IV assumptions: Record independence, exclusion, monotonicity, and treatment-unit evidence.
    - Limit interpretation: Report a local complier effect and require separate transport evidence.

### eq:randomization-assumption

- Proposal: `assumption_proposal_1bef8104e6a761de_role_identification_assumption`
  - Location: `credit_card_npv_component_proposal_v8.tex > eq:randomization-assumption > line 6015`
  - Problem: The source-evidenced `identification_assumption` target has 5 undischarged local obligations.
  - Why: A routing role identifies the relevant mathematical checks but does not establish their assumptions or truth. These local obligations must be bound or discharged before claim promotion.
  - Proposed assumption: State, source-bind, or discharge the 5 local obligations for the source-evidenced `identification_assumption` route; do not import downstream conditions as local correctness requirements.
  - Validation: `validated_by_source_role_rule`; Source-role-local proposals are diagnostic candidates, not proof or globally minimal assumption sets.
  - Evidence refs: `source:e5dad21cb32c1f715261a9a4415511a3a8d9bd10958aa34126c9be8236e3709b:1bef8104e6a761dea3d4618663ecba54ea95a79021dc0d5b45d293b070c16b9b`, `routing_role:role_fbd990fb41ace1bb9061e77dcfa4cb4d4307fa5d3092d584a9027bb1a0053910`, `role_obligation:assignment_mechanism_recorded`, `role_obligation:eligible_population_bound`, `role_obligation:randomization_unit_bound`, `role_obligation:interference_and_override_diagnostics`, `role_obligation:assignment_lineage_reconciled`

  - Mathematical missing-assumption reasoning:
    - assignment_mechanism_recorded (design_evidence_condition): The random assignment mechanism and probabilities. Why missing: A displayed independence statement does not establish how assignment occurred.
    - eligible_population_bound (population_scope_condition): The exact eligible population and analysis cohort. Why missing: Randomization validity is population scoped.
    - randomization_unit_bound (design_evidence_condition): The account/customer/household/branch randomization unit. Why missing: A unit mismatch can create dependence and contamination.
    - interference_and_override_diagnostics (design_veto_condition): Diagnostics for spillovers, overrides, re-contact, suppression, and campaign merging. Why missing: Operational violations can destroy the stated independence.
    - assignment_lineage_reconciled (lineage_condition): Reconciled assignment, exposure, override, and outcome lineage. Why missing: Lost or altered assignment records make the assumption untestable operationally.

  - Possible sufficient assumption sets:
    - `randomization_design_record` (evidence needed to assess the stated assumption): Provides evidence relevant to, but not automatic proof of, the stated independence.
      - Assignment was generated by the recorded random mechanism.
      - The eligible population and unit are fixed.
      - No material interference or override occurred.
      - Lineage reconciles assignment to analysis.

  - How the derivation works under the assumptions:
    - Reconstruct design: Bind mechanism, probabilities, population, and randomization unit.
    - Run veto diagnostics: Check interference, overrides, re-contact, suppression, and merges.
    - Reconcile lineage: Compare randomized assignment, exposure, and analyzed outcomes.
    - Retain assumption boundary: Do not mark independence true merely because it is stated.

## Non-Claims

- `assumption_report_not_proof_certificate`: The assumption report proposes route conditions only; it does not prove the target or certify global minimality.
- `general_theorem_proving_not_claimed`: This scoped workflow result does not claim general theorem-proving ability.
- `release_readiness_not_claimed`: This scoped workflow result does not claim release readiness.
- `route_assumptions_not_global_minimality`: Route-required assumptions are not claimed to be globally minimal.
