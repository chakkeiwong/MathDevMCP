from __future__ import annotations

"""Role-specific local obligations for exact source-bound mathematical objects."""

from typing import Any, Mapping

from .contracts import attach_contract


ROLE_OBLIGATION_CONTRACT = "role_specific_obligation_result"
SPECIALIST_BUILDER_ROLES = frozenset(
    {
        "accounting_identity",
        "placeholder_definition",
        "policy_value_recursion",
        "causal_estimand_object",
        "identification_assumption",
        "statistical_estimator",
    }
)


def has_role_specific_builder(routing_role: Mapping[str, Any], *, target: str) -> bool:
    role = str(routing_role.get("role", ""))
    if routing_role.get("authority") != "source_evidenced_role" or role not in SPECIALIST_BUILDER_ROLES:
        return False
    return role != "statistical_estimator" or "LATE" in target.upper()


def _item(identifier: str, kind: str, missing: str, why: str, closes: str) -> dict[str, str]:
    return {
        "id": identifier,
        "kind": kind,
        "mathematically_missing": missing,
        "why_missing": why,
        "closes": closes,
        "evidence_ref": f"role_obligation:{identifier}",
    }


def _step(name: str, detail: str) -> dict[str, str]:
    return {"step": name, "detail": detail}


def _expectation() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _item("probability_kernel_defined", "probability_condition", "A probability space or conditional kernel for the random object.", "Conditional expectation is undefined without a law.", "Defines the expectation operator."),
        _item("conditioning_object_defined", "information_condition", "The conditioning sigma-field, state, or covariate object.", "The conditional bar determines the information scope.", "Fixes the conditioning scope."),
        _item("measurability_and_integrability", "integrability_condition", "Measurability and finite conditional first moments for the integrand.", "The expectation may otherwise be undefined or infinite.", "Makes the object a finite conditional integral."),
    ]
    sets = [{"id": "conditional_kernel_integrability", "role": "general sufficient condition", "assumptions": ["A conditional kernel is fixed.", "The integrand is measurable.", "The integrand has a finite conditional first moment."], "closes": "The conditional expectation is well defined."}]
    route = [_step("Bind probability objects", "Define the random object, conditioning object, and conditional kernel."), _step("Check integrability", "Establish measurability and finite conditional first moments."), _step("Preserve causal boundary", "Do not infer identification from well-defined expectation notation.")]
    return obligations, sets, route


def _accounting() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _item("component_definitions", "accounting_definition_condition", "Definitions for every component in the local identity.", "Undefined components make reconciliation ambiguous.", "Fixes the objects being reconciled."),
        _item("sign_units_timing_aligned", "accounting_alignment_condition", "A common sign, unit/currency, and timing convention.", "Misaligned conventions can make a syntactically valid sum economically inconsistent.", "Makes the local arithmetic comparable."),
        _item("local_component_exhaustiveness", "accounting_exhaustiveness_condition", "A statement of local exhaustiveness or a named residual/adjustment term.", "An accounting identity needs a declared local boundary for omitted components.", "Closes the local reconciliation boundary."),
    ]
    sets = [{"id": "local_accounting_contract", "role": "local sufficient condition", "assumptions": ["All displayed components are defined.", "Signs, units, and timing are aligned.", "The displayed components are locally exhaustive or include a residual."], "closes": "The local accounting identity is well posed."}]
    route = [_step("Define components", "Bind each local component to its accounting meaning."), _step("Align conventions", "Check signs, units, and timing."), _step("Reconcile locally", "Check the sum without importing downstream valuation requirements.")]
    return obligations, sets, route


def _terminal() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _item("terminal_denominator_nonzero", "domain_condition", "The exact terminal-value denominator is nonzero on the scoped domain.", "Division is undefined at a zero denominator.", "Makes the scalar definition algebraically well defined."),
        _item("terminal_scalar_roles_units", "type_and_unit_condition", "Scalar roles, compatible time units, and signs for persistence, discount, hazard, and decay terms.", "A scalar quotient can be dimensionally or temporally incoherent.", "Makes the definition typed and unit-consistent."),
        _item("terminal_sensitivity_boundary", "definition_boundary_condition", "Sensitivity cases and an explicit boundary between placeholder definition and economic validity.", "Algebraic consistency does not establish a defensible extrapolation.", "Prevents algebraic validation from becoming an economic claim."),
    ]
    sets = [{"id": "terminal_placeholder_contract", "role": "definition-scoped sufficient condition", "assumptions": ["The exact denominator is nonzero.", "All terms use compatible units and timing.", "The formula remains an explicit stress-tested placeholder."], "closes": "The terminal definition is algebraically well posed without claiming economic validity."}]
    route = [_step("Bind scalar terms", "Define every numerator and denominator term with units."), _step("Check denominator", "Verify the exact denominator is nonzero before cross-multiplication."), _step("Stress definition", "Report zero-tail and alternative persistence/decay cases separately.")]
    return obligations, sets, route


def _late() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _item("late_nonzero_first_stage", "instrument_relevance_condition", "A nonzero assignment-to-receipt first stage for the exact eligible population.", "The LATE denominator must be nonzero.", "Makes the ratio defined and establishes relevance."),
        _item("late_assignment_independence", "identification_condition", "Instrument assignment independence in the scoped population.", "Algebra alone cannot identify the causal contrast.", "Supports the IV independence condition."),
        _item("late_exclusion", "identification_condition", "Exclusion of direct assignment effects outside treatment receipt.", "Direct assignment pathways invalidate the IV interpretation.", "Supports the exclusion condition."),
        _item("late_monotonicity", "identification_condition", "Monotonic treatment take-up with no defiers in the scoped design.", "Without monotonicity the ratio lacks the local complier interpretation.", "Supports the complier estimand."),
        _item("late_sutva_scope", "causal_scope_condition", "SUTVA/no-interference and a defined randomization/treatment unit.", "Spillovers or treatment-version ambiguity change the estimand.", "Fixes the causal unit and treatment versions."),
        _item("late_complier_interpretation", "interpretation_boundary", "An explicit local-complier interpretation and transport non-claim.", "LATE is not the population ATE without additional evidence.", "Prevents population overgeneralization."),
    ]
    sets = [{"id": "late_identification_contract", "role": "standard IV sufficient conditions", "assumptions": ["The first stage is nonzero.", "Assignment is independent in the eligible population.", "Exclusion and monotonicity hold.", "Treatment versions and interference are controlled."], "closes": "The ratio has a scoped local-complier causal interpretation."}]
    route = [_step("Check first stage", "Verify the exact denominator contrast is nonzero."), _step("Bind IV assumptions", "Record independence, exclusion, monotonicity, and treatment-unit evidence."), _step("Limit interpretation", "Report a local complier effect and require separate transport evidence.")]
    return obligations, sets, route


def _randomization() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _item("assignment_mechanism_recorded", "design_evidence_condition", "The random assignment mechanism and probabilities.", "A displayed independence statement does not establish how assignment occurred.", "Binds the design that could support independence."),
        _item("eligible_population_bound", "population_scope_condition", "The exact eligible population and analysis cohort.", "Randomization validity is population scoped.", "Fixes the population in the independence statement."),
        _item("randomization_unit_bound", "design_evidence_condition", "The account/customer/household/branch randomization unit.", "A unit mismatch can create dependence and contamination.", "Fixes the assignment unit."),
        _item("interference_and_override_diagnostics", "design_veto_condition", "Diagnostics for spillovers, overrides, re-contact, suppression, and campaign merging.", "Operational violations can destroy the stated independence.", "Defines vetoes for compromised assignment."),
        _item("assignment_lineage_reconciled", "lineage_condition", "Reconciled assignment, exposure, override, and outcome lineage.", "Lost or altered assignment records make the assumption untestable operationally.", "Preserves design provenance."),
    ]
    sets = [{"id": "randomization_design_record", "role": "evidence needed to assess the stated assumption", "assumptions": ["Assignment was generated by the recorded random mechanism.", "The eligible population and unit are fixed.", "No material interference or override occurred.", "Lineage reconciles assignment to analysis."], "closes": "Provides evidence relevant to, but not automatic proof of, the stated independence."}]
    route = [_step("Reconstruct design", "Bind mechanism, probabilities, population, and randomization unit."), _step("Run veto diagnostics", "Check interference, overrides, re-contact, suppression, and merges."), _step("Reconcile lineage", "Compare randomized assignment, exposure, and analyzed outcomes."), _step("Retain assumption boundary", "Do not mark independence true merely because it is stated.")]
    return obligations, sets, route


def _bellman() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _item("bellman_state_action_domains", "dynamic_programming_condition", "State/belief and action domains with a nonempty feasible set.", "The maximum is not well posed without its domain.", "Defines the optimization domain."),
        _item("bellman_transition_kernel", "probability_condition", "A transition kernel for next state/observation conditional on current state and action.", "The continuation expectation needs a law.", "Defines the stochastic continuation operator."),
        _item("bellman_reward_value_finite", "integrability_condition", "Measurable finite rewards and integrable continuation value.", "The objective may otherwise be undefined or infinite.", "Makes action values comparable."),
        _item("bellman_horizon_boundary", "recursion_boundary_condition", "A horizon plus terminal/transversality/contraction boundary.", "A recursion needs a closing condition.", "Closes the recursive definition."),
        _item("bellman_policy_measurability", "policy_regularness_condition", "A measurable admissible policy/selector or finite-action substitute.", "An optimizer may not define an admissible policy without selection conditions.", "Connects the value recursion to a policy object."),
    ]
    sets = [{"id": "finite_or_regular_bellman_contract", "role": "sufficient dynamic-programming conditions", "assumptions": ["Feasible actions are nonempty.", "Rewards and transitions are measurable and finite/integrable.", "A terminal or contraction condition is stated.", "A measurable policy selector exists or action sets are finite."], "closes": "The Bellman operator is well defined without proving global optimality for the document model."}]
    route = [_step("Bind domains", "Define state, action, feasibility, and policy class."), _step("Bind reward and kernel", "Define finite rewards and stochastic transitions."), _step("Close recursion", "State terminal/transversality/contraction conditions."), _step("Certify only scoped properties", "Do not infer economic validity or global optimality from symbolic form.")]
    return obligations, sets, route


def _policy_value() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    expectation_obligations, expectation_sets, expectation_route = _expectation()
    obligations = [
        _item("policy_value_paths_defined", "valuation_scope_condition", "Action, baseline, scenario, downstream policy, horizon, and information set.", "A discounted contrast is ambiguous without aligned paths and scope.", "Defines the valuation object."),
        _item("discount_terminal_terms_defined", "valuation_condition", "Discount factors and terminal-value convention on the stated horizon.", "The aggregate depends on timing and tail treatment.", "Makes the finite-horizon aggregation well defined."),
        *expectation_obligations,
    ]
    sets = [{"id": "finite_horizon_policy_value", "role": "valuation sufficient condition", "assumptions": ["Action and baseline paths share scenario, policy, horizon, and information.", "Discount and terminal terms are finite and defined.", "The conditional cash-flow object is integrable."], "closes": "The policy-value functional is well defined."}, *expectation_sets]
    route = [_step("Align paths", "Bind action/baseline, scenario, downstream policy, horizon, and information."), _step("Define valuation terms", "Bind discount factors and terminal convention."), *expectation_route]
    return obligations, sets, route


def build_role_specific_obligations(
    *,
    target: str,
    normalized_target: Mapping[str, Any],
    routing_role: Mapping[str, Any],
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    """Build local obligations from an exact source-evidenced role."""
    role = str(routing_role.get("role", "unsupported_or_ambiguous"))
    authority = str(routing_role.get("authority", "role_ambiguous"))
    if authority != "source_evidenced_role":
        role = "unsupported_or_ambiguous"
    if role == "accounting_identity":
        local, sets, route = _accounting()
    elif role == "placeholder_definition":
        local, sets, route = _terminal()
    elif role == "causal_estimand_object":
        local, sets, route = _expectation()
        local.append(_item("causal_identification_separate", "causal_boundary_condition", "A separate identification argument for the causal interpretation.", "Well-defined potential-outcome notation does not identify it from observed data.", "Preserves the distinction between causal object and identification evidence."))
    elif role == "identification_assumption":
        local, sets, route = _randomization()
    elif role == "statistical_estimator" and "LATE" in target.upper():
        local, sets, route = _late()
    elif role == "policy_value_recursion" and "maximum" in set(normalized_target.get("operator_inventory", [])):
        local, sets, route = _bellman()
    elif role == "policy_value_recursion" and "\\max" in target:
        local, sets, route = _bellman()
    elif role == "policy_value_recursion":
        local, sets, route = _policy_value()
    else:
        local = [_item("typed_local_obligation", "formalization_condition", "A typed local obligation and source role discriminator.", "The current source evidence does not authorize a specialist role route.", "Creates a safe next formalization target.")]
        sets = [{"id": "typed_obligation_first", "role": "next deterministic artifact", "assumptions": ["Define symbols, domains, operators, and intended role."], "closes": "Creates a typed local obligation."}]
        route = [_step("Formalize locally", "Create a typed obligation without inferring a scientific role.")]
    downstream: list[dict[str, str]] = []
    if role == "accounting_identity":
        downstream = [
            _item("downstream_counterfactual_mapping", "downstream_integration_condition", "A separate mapping from the local identity to action-versus-baseline paths.", "Needed for downstream incremental NPV, not for local accounting equality.", "Connects the identity to a valuation consumer."),
            _item("downstream_discount_terminal_policy", "downstream_integration_condition", "A separate discount/horizon/terminal policy for downstream valuation.", "Valuation choices do not determine local identity correctness.", "Connects local outputs to NPV aggregation."),
        ]
    return attach_contract(
        {
            "status": "role_specific_obligations" if role != "unsupported_or_ambiguous" else "typed_abstention",
            "role": role,
            "role_authority": authority,
            "relation_kind": normalized_target.get("kind"),
            "local_obligations": local,
            "downstream_integration_obligations": downstream,
            "possible_assumption_sets": sets,
            "derivation_route": route,
            "next_audit": {"tool": "audit_and_propose_assumptions", "purpose": "Bind or discharge the role-specific local obligations before backend promotion."},
            "evidence_refs": list(evidence_refs or []),
            "non_claims": [
                "The listed conditions are role-scoped candidates, not globally minimal assumptions.",
                "A source-stated role or assumption is not thereby mathematically, empirically, causally, or economically valid.",
                "Downstream integration conditions are not local correctness blockers.",
            ],
        },
        ROLE_OBLIGATION_CONTRACT,
    )
