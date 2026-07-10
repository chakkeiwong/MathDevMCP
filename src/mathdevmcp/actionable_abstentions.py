from __future__ import annotations

"""Deterministic missing-obligation payloads for useful abstention."""

import re
from typing import Any

from .contracts import attach_contract


ACTIONABLE_ABSTENTION_CONTRACT = "actionable_abstention_payload"


def _norm(text: str) -> str:
    return " ".join(str(text or "").split())


def _has_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns)


def _obligation(
    obligation_id: str,
    kind: str,
    mathematically_missing: str,
    why_missing: str,
    closes: str,
    evidence_ref: str,
) -> dict[str, str]:
    return {
        "id": obligation_id,
        "kind": kind,
        "mathematically_missing": mathematically_missing,
        "why_missing": why_missing,
        "closes": closes,
        "evidence_ref": evidence_ref,
    }


def _dedupe_dicts(items: list[dict[str, Any]], key: str = "id") -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in items:
        item_key = str(item.get(key, ""))
        if item_key in seen:
            continue
        seen.add(item_key)
        result.append(item)
    return result


def _expectation_payload() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _obligation(
            "conditional_law_defined",
            "probability_condition",
            "A conditional probability law for the random variables inside the expectation.",
            "A conditional expectation is not a real-valued operator until the conditioning law or kernel is specified.",
            "Makes the expectation operator well defined.",
            "actionable_abstention:conditional_expectation",
        ),
        _obligation(
            "measurable_integrable_payoff_terms",
            "integrability_condition",
            "Measurability and finite conditional first moments for every payoff, value, or derivative term inside the expectation.",
            "Without measurability and integrability, the expectation may be undefined or infinite.",
            "Turns the displayed expression into a finite scalar equality.",
            "actionable_abstention:conditional_expectation",
        ),
        _obligation(
            "conditioning_information_defined",
            "information_condition",
            "A definition of the conditioning information set, state, or sigma-field.",
            "The notation after the conditional bar determines what information the expectation conditions on.",
            "Fixes the scope of the conditional expectation used in the derivation.",
            "actionable_abstention:conditional_expectation",
        ),
    ]
    assumption_sets = [
        {
            "id": "finite_state_conditional_expectation",
            "role": "simple sufficient condition",
            "assumptions": [
                "The conditioned shock or path has finite support.",
                "Every payoff/value term inside the expectation is finite at each support point.",
                "The conditioning state or information set is explicitly defined.",
            ],
            "closes": "The expectation becomes a finite weighted sum.",
        },
        {
            "id": "kernel_integrability_condition",
            "role": "general sufficient condition",
            "assumptions": [
                "A conditional kernel or probability law is fixed for the random object.",
                "All random terms inside the expectation are measurable under that law.",
                "Those terms are dominated by an integrable envelope or have finite conditional first moments.",
            ],
            "closes": "The expectation is a well-defined finite conditional integral.",
        },
    ]
    route = [
        {
            "step": "Define conditional law",
            "detail": "Specify the kernel or conditional distribution used by the expectation.",
        },
        {
            "step": "Check integrability",
            "detail": "Verify each random payoff, value, or derivative term has a finite conditional expectation.",
        },
        {
            "step": "Use expectation as scalar",
            "detail": "Only after those checks should the equality be treated as a scalar derivation step.",
        },
    ]
    return obligations, assumption_sets, route


def _npv_payload() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _obligation(
            "baseline_and_action_paths_defined",
            "counterfactual_condition",
            "Definitions of the baseline path and the action path used in the incremental NPV.",
            "An incremental NPV is a contrast; without both paths, the delta notation is ambiguous.",
            "Makes the counterfactual comparison well posed.",
            "actionable_abstention:npv_identity",
        ),
        _obligation(
            "cash_flow_components_exhaustive",
            "accounting_identity_condition",
            "A statement that the listed cash-flow components are exhaustive and share the same sign convention.",
            "A cash-flow decomposition is an accounting identity only after omitted components and sign conventions are ruled out.",
            "Justifies replacing total incremental cash flow by the listed component sum.",
            "actionable_abstention:npv_identity",
        ),
        _obligation(
            "discount_horizon_terminal_value_defined",
            "valuation_condition",
            "Definitions of the horizon, discount factors, and terminal-value term.",
            "The NPV sum depends on time indexing, discounting, and the terminal payoff convention.",
            "Makes the finite-horizon valuation expression well defined.",
            "actionable_abstention:npv_identity",
        ),
    ]
    assumption_sets = [
        {
            "id": "finite_horizon_incremental_npv",
            "role": "simple sufficient condition",
            "assumptions": [
                "The baseline and action paths are defined on the same horizon and information set.",
                "All cash-flow components use the same currency, time index, and sign convention.",
                "Discount factors and terminal value are finite and defined for the horizon.",
            ],
            "closes": "The incremental NPV expression is a finite, aligned accounting/valuation identity.",
        }
    ]
    route = [
        {
            "step": "Define two paths",
            "detail": "Write the action path and baseline path under the same information set.",
        },
        {
            "step": "Decompose cash flow",
            "detail": "Show the incremental cash-flow term equals the exhaustive component sum with a single sign convention.",
        },
        {
            "step": "Discount and aggregate",
            "detail": "Apply the stated discount factors and terminal-value convention over the finite horizon.",
        },
    ]
    return obligations, assumption_sets, route


def _bellman_payload() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _obligation(
            "state_action_spaces_defined",
            "dynamic_programming_condition",
            "Definitions of state, belief state, feasible action set, and nonemptiness of the feasible action set.",
            "A Bellman maximization is not well posed until its domain and feasible controls are defined.",
            "Makes the optimization domain explicit.",
            "actionable_abstention:bellman_recursion",
        ),
        _obligation(
            "transition_kernel_defined",
            "probability_condition",
            "A transition law for next-period states conditional on current state and action.",
            "The continuation value is an expectation over next states; that expectation needs a transition kernel.",
            "Defines the stochastic continuation operator.",
            "actionable_abstention:bellman_recursion",
        ),
        _obligation(
            "reward_and_value_integrable",
            "integrability_condition",
            "Finite reward and integrable continuation value under each admissible action.",
            "The objective may be undefined or infinite without boundedness or integrability conditions.",
            "Makes the Bellman objective finite for comparison across actions.",
            "actionable_abstention:bellman_recursion",
        ),
        _obligation(
            "terminal_boundary_condition_defined",
            "recursion_boundary_condition",
            "A terminal, transversality, or boundary condition for the recursive value.",
            "A recursion cannot be checked as a dynamic-programming equation without a boundary condition.",
            "Closes the recursive definition.",
            "actionable_abstention:bellman_recursion",
        ),
    ]
    assumption_sets = [
        {
            "id": "finite_state_finite_action_bellman",
            "role": "simple sufficient condition",
            "assumptions": [
                "The state and action sets are finite or compact with a nonempty feasible set.",
                "Rewards are finite and measurable.",
                "A transition matrix or kernel is specified for each admissible action.",
                "A terminal value or contraction condition is stated.",
            ],
            "closes": "The Bellman operator is well defined and can be audited as a dynamic-programming recursion.",
        }
    ]
    route = [
        {
            "step": "Declare state and actions",
            "detail": "Specify the domain over which the maximum is taken.",
        },
        {
            "step": "Define transition and reward",
            "detail": "State the reward map and transition law used to form expected continuation value.",
        },
        {
            "step": "Apply Bellman operator",
            "detail": "Under finiteness/integrability and a boundary condition, evaluate reward plus discounted expected continuation value.",
        },
    ]
    return obligations, assumption_sets, route


def _shape_payload() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _obligation(
            "dimension_declarations",
            "shape_condition",
            "Dimensions for every vector, matrix, and transposed object in the expression.",
            "Matrix products and transposes are undefined unless the operands have conformable dimensions.",
            "Makes the matrix expression syntactically and semantically well formed.",
            "actionable_abstention:shape_conformability",
        ),
        _obligation(
            "scalar_vector_matrix_roles",
            "type_condition",
            "A scalar/vector/matrix role for each ambiguous symbol.",
            "The same notation can denote scalars, vectors, or matrices; the product type changes with that role.",
            "Prevents a shape-compatible expression from being misread as a different object.",
            "actionable_abstention:shape_conformability",
        ),
    ]
    assumption_sets = [
        {
            "id": "explicit_dimension_contract",
            "role": "minimal shape contract",
            "assumptions": [
                "Declare the dimension of every matrix and vector appearing in the product.",
                "State that adjacent matrix products are conformable.",
                "State whether transpose notation denotes an inner product, outer product, or matrix transpose.",
            ],
            "closes": "Makes the expression well typed before any algebraic or proof audit.",
        }
    ]
    route = [
        {
            "step": "Assign dimensions",
            "detail": "Map each symbol to a scalar, vector, or matrix with explicit dimensions.",
        },
        {
            "step": "Check products",
            "detail": "Verify adjacent dimensions match and the final expression has the claimed scalar/vector/matrix type.",
        },
    ]
    return obligations, assumption_sets, route


def _obc_payload() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _obligation(
            "complementarity_relation_defined",
            "complementarity_condition",
            "A precise relation between the max/min notation, slack variable, multiplier, and inequality constraint.",
            "Occasionally-binding-constraint notation can mean a projection, a complementarity system, or a policy rule.",
            "Separates algebraic equivalence from implementation mask validation.",
            "actionable_abstention:obc_complementarity",
        ),
        _obligation(
            "regime_boundary_specified",
            "piecewise_condition",
            "A statement of the binding and nonbinding regimes and boundary behavior.",
            "A max/min formula does not by itself prove which regime applies or how the boundary is handled.",
            "Makes the piecewise derivation auditable.",
            "actionable_abstention:obc_complementarity",
        ),
    ]
    assumption_sets = [
        {
            "id": "kkt_complementarity_contract",
            "role": "standard sufficient condition",
            "assumptions": [
                "State the inequality constraint.",
                "State nonnegativity of the multiplier or slack.",
                "State the complementary slackness equation.",
                "State the mapping between the mathematical regimes and any implementation mask.",
            ],
            "closes": "Turns the max/min notation into a checkable complementarity contract.",
        }
    ]
    route = [
        {
            "step": "Write KKT/complementarity system",
            "detail": "State primal feasibility, multiplier/slack sign, and complementary slackness.",
        },
        {
            "step": "Derive max/min form",
            "detail": "Show the displayed max/min formula is equivalent to the stated regimes under those conditions.",
        },
        {
            "step": "Audit implementation separately",
            "detail": "If there is a mask, validate that it implements the same regimes; algebra alone does not certify the mask.",
        },
    ]
    return obligations, assumption_sets, route


def _malformed_latex_payload() -> tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]:
    obligations = [
        _obligation(
            "balanced_replacement_latex",
            "parser_provenance_condition",
            "Balanced LaTeX delimiters and a complete displayed-math environment for the proposed replacement.",
            "A malformed replacement cannot be safely applied or checked by symbolic/formal tools.",
            "Makes the replacement text parseable before mathematical validation.",
            "actionable_abstention:malformed_replacement_latex",
        ),
        _obligation(
            "source_span_reconstruction",
            "provenance_condition",
            "A source span that contains the full equality, not only a fragment of a multiline expression.",
            "Partial source reconstruction can drop closing delimiters or terms and create a false repair.",
            "Lets the audit reconstruct the intended proof target from complete evidence.",
            "actionable_abstention:malformed_replacement_latex",
        ),
    ]
    assumption_sets = [
        {
            "id": "complete_source_span_first",
            "role": "repair precondition",
            "assumptions": [
                "The cited source span contains the complete displayed expression.",
                "The proposed replacement compiles as standalone LaTeX display math.",
                "The proof target is extracted from the same complete replacement.",
            ],
            "closes": "Prevents a partial parser reconstruction from being treated as a mathematical edit.",
        }
    ]
    route = [
        {
            "step": "Recover full source span",
            "detail": "Extract the entire displayed equation or align environment around the cited line.",
        },
        {
            "step": "Check LaTeX structure",
            "detail": "Verify delimiters and begin/end environments are balanced before presenting replacement text.",
        },
        {
            "step": "Rerun derivation audit",
            "detail": "Only after parseable replacement text exists should proof-audit run on the reconstructed target.",
        },
    ]
    return obligations, assumption_sets, route


def build_actionable_abstention_payload(
    *,
    text: str = "",
    problem: str = "",
    why_not_concrete: str = "",
    location: str = "",
    kind: str = "",
    evidence_refs: list[str] | None = None,
) -> dict[str, Any]:
    """Return deterministic obligations that make an abstention actionable."""
    haystack = "\n".join([text, problem, why_not_concrete, location, kind])
    obligations: list[dict[str, str]] = []
    assumption_sets: list[dict[str, Any]] = []
    route: list[dict[str, str]] = []
    domains: list[str] = []

    def add(domain: str, payload: tuple[list[dict[str, str]], list[dict[str, Any]], list[dict[str, str]]]) -> None:
        domain_obligations, domain_sets, domain_route = payload
        domains.append(domain)
        obligations.extend(domain_obligations)
        assumption_sets.extend(domain_sets)
        route.extend(domain_route)

    if "failed conservative" in why_not_concrete.lower() or "malformed" in haystack.lower():
        add("malformed_replacement_latex", _malformed_latex_payload())
    if _has_any(haystack, (r"\\E\b", r"\\mathbb\{E\}", r"conditional expectation", r"\\mid")):
        add("conditional_expectation", _expectation_payload())
    if _has_any(haystack, (r"\\NPV", r"\bNPV\b", r"\\Delta CF", r"PPNR", r"Kchg", r"terminal value", r"TV_")):
        add("npv_accounting_identity", _npv_payload())
    if _has_any(haystack, (r"V[_\^].*\\star", r"\\max_", r"Bellman", r"feasible action", r"J\^\{\\varphi\}")):
        add("bellman_value_recursion", _bellman_payload())
    if _has_any(haystack, (r"conformable", r"transpose", r"matrix product", r"\\top", r"dimension")):
        add("shape_conformability", _shape_payload())
    if _has_any(haystack, (r"complementarity", r"occasionally.binding", r"\\max\{", r"\\min\{", r"binding constraint", r"\bOBC\b")):
        add("obc_complementarity", _obc_payload())

    if not obligations:
        obligations.append(
            _obligation(
                "formalized_local_obligation",
                "formalization_condition",
                "A typed local obligation with defined symbols, domains, and operator meanings.",
                "The diagnostic source does not yet expose enough structure for a mathematical repair.",
                "Creates the next deterministic target for assumption discovery or proof audit.",
                "actionable_abstention:generic_formalization",
            )
        )
        assumption_sets.append(
            {
                "id": "typed_obligation_first",
                "role": "next deterministic artifact",
                "assumptions": [
                    "Define every symbol, domain, and operator in the cited source line.",
                    "Choose whether the line is a definition, identity, optimization condition, estimator, or diagnostic.",
                    "Rerun the relevant assumption/proof audit after the typed obligation exists.",
                ],
                "closes": "Makes the abstention inspectable by deterministic tooling.",
            }
        )
        route.append(
            {
                "step": "Formalize local obligation",
                "detail": "Convert the cited line into a typed obligation before proposing a document edit.",
            }
        )
        domains.append("generic_formalization")

    obligations = _dedupe_dicts(obligations)
    assumption_sets = _dedupe_dicts(assumption_sets)
    route = _dedupe_dicts(route, key="step")
    domains = list(dict.fromkeys(domains))
    if "malformed_replacement_latex" in domains:
        next_tool = "audit_derivation_v2_label"
        purpose = "Recover a complete parseable source span, then rerun the derivation audit."
    elif "conditional_expectation" in domains or "shape_conformability" in domains:
        next_tool = "audit_and_propose_assumptions"
        purpose = "Generate explicit assumption proposals for the missing route conditions."
    else:
        next_tool = "audit_and_propose_fix"
        purpose = "Regenerate concrete proposals after adding the listed obligations."
    safe_wording = (
        "Do not treat this item as a document edit yet. State the missing obligations below, "
        "choose a sufficient assumption set, and rerun the smallest next audit before promoting it to a repair."
    )
    return attach_contract(
        {
            "status": "actionable_abstention",
            "domains": domains,
            "blocker_kind": "+".join(domains),
            "missing_obligations": obligations,
            "possible_assumption_sets": assumption_sets,
            "how_derivation_can_work": route,
            "safe_wording": safe_wording,
            "next_audit": {
                "tool": next_tool,
                "purpose": purpose,
            },
            "evidence_refs": list(evidence_refs or []),
            "non_claim": "These obligations are deterministic diagnostics, not proof certificates and not globally minimal assumption sets.",
            "source_summary": _norm(haystack)[:500],
        },
        ACTIONABLE_ABSTENTION_CONTRACT,
    )
