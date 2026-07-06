from __future__ import annotations

"""Gap and proposal builders for agent-consumable assumption workflows."""

import re
from typing import Any


ASSUMPTION_VALIDATION_POLICY = "route_rule_non_certifying"
ASSUMPTION_VALIDATION_BOUNDARY = (
    "Rule validation only checks that the proposed assumption matches a "
    "deterministic route requirement; it is not a proof certificate and does "
    "not prove global minimality."
)


def _math(text: str) -> str:
    return text


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return slug or "assumption"


def _target_terms(target: str, assumption: dict[str, Any]) -> list[str]:
    used_by = assumption.get("used_by")
    terms = [target] if target else []
    if isinstance(used_by, list):
        for item in used_by:
            if isinstance(item, str) and item and item not in terms:
                terms.append(item)
    return terms


def _location(target: str, source: dict[str, Any] | None = None) -> str:
    source = source or {}
    file = source.get("file") or source.get("path")
    label = source.get("label")
    line = source.get("line_start")
    if file and label and line:
        return f"{file} > {label} > line {line}"
    if file and label:
        return f"{file} > {label}"
    if file and line:
        return f"{file} > line {line}"
    if label:
        return str(label)
    return target or "direct target"


def _source_prefix(source: dict[str, Any] | None = None) -> str:
    source = source or {}
    for key in ("label", "block_id", "file", "path"):
        value = source.get(key)
        if isinstance(value, str) and value:
            return _slug(value)
    return "direct_target"


def _problem_for(assumption: dict[str, Any]) -> str:
    text = str(assumption.get("text", "route-required assumption")).strip()
    source = str(assumption.get("source", "route")).strip()
    return f"Missing route-required assumption: {text} ({source})."


def _assumption_kind(assumption: dict[str, Any], target: str = "", source: dict[str, Any] | None = None) -> str:
    text = str(assumption.get("text", "")).strip()
    label = str((source or {}).get("label", ""))
    target_text = target.lower()
    if text == "conditional expectation law is defined and the random payoff terms are integrable":
        if label == "prop:risky-pricing" or "zero-profit" in target_text or "risky debt rate" in target_text:
            return "risky_pricing_expectation"
        if label == "prop:interior-foc" or "first-order conditions" in target_text or "v^\\star_" in target_text:
            return "interior_foc_expectation"
        return "conditional_expectation_integrability"
    if text == "lender pricing uses the stated zero-profit risk-free discounting convention":
        return "zero_profit_pricing_convention"
    if text == "differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present":
        return "foc_expectation_differentiation"
    return _slug(text)


def _why_for(assumption: dict[str, Any], target: str = "", source: dict[str, Any] | None = None) -> str:
    kind = _assumption_kind(assumption, target, source)
    if kind == "risky_pricing_expectation":
        return (
            "The zero-profit equation treats a state-contingent lender payoff as a "
            "finite conditional expected payoff. That route needs a transition law "
            "for next-period shocks, measurable default/recovery/payoff terms, and "
            "finite conditional first moments."
        )
    if kind in {"interior_foc_expectation", "foc_expectation_differentiation"}:
        return (
            "The FOC proof differentiates an expected continuation value. That route "
            "needs a conditional law, continuation-value differentiability, "
            "integrable derivatives or a dominated-differentiation condition, and "
            "choice-independent transition probabilities so no kernel-derivative "
            "terms are omitted."
        )
    if kind == "zero_profit_pricing_convention":
        return (
            "The pricing equation equates the lender's expected risky payoff with a "
            "risk-free required payoff. That is an economic valuation convention, "
            "not a purely algebraic consequence of the payoff partition."
        )
    categories = assumption.get("route_categories") if isinstance(assumption.get("route_categories"), list) else []
    category_set = {str(item) for item in categories}
    source = str(assumption.get("source", "")).lower()
    text = str(assumption.get("text", "This assumption")).strip()
    if "covariance_condition" in category_set or "logdet" in source or "determinant" in source:
        return "Determinant and logdet notation require a valid determinant domain; covariance-style uses usually require positive definiteness."
    if "shape_condition" in category_set or "matrix" in source or "inverse" in source:
        return "Matrix operations require shape, square, invertibility, or conformability conditions before the expression is well posed."
    if "domain_condition" in category_set and "division" in source:
        return "Division is undefined at a zero denominator, so the derivation needs a nonzero-domain condition."
    if "domain_condition" in category_set and "square root" in source:
        return "Square-root notation needs a nonnegative argument on the stated domain."
    if "smoothness_condition" in category_set:
        return "Derivative notation requires differentiability on the domain where the derivative is used."
    if "rank_condition" in category_set:
        return "Rank-dependent arguments require the stated rank condition before the route is valid."
    if "integrability_condition" in category_set or "conditional expectation" in source:
        return "Conditional expectation expressions require a defined conditional law and integrability of the random payoff terms."
    return f"The route diagnostic marked `{text}` as required before this target can be treated as well posed."


def _proposal_text(assumption: dict[str, Any], target: str = "", source: dict[str, Any] | None = None) -> str:
    text = str(assumption.get("text", "")).strip()
    if text == "denominator is nonzero":
        return "Assume every denominator in this claim is nonzero on the stated domain."
    if text == "matrix operand is square and invertible":
        return "Assume the matrix operand is square and invertible on the stated domain."
    if text == "matrix operand is square with valid determinant domain, usually positive definite for logdet":
        return "Assume the matrix operand is square and has a valid determinant domain; for covariance/logdet use, assume it is positive definite."
    if text == "Jacobian matrix is square and nonsingular with valid log-absolute-determinant domain":
        return "Assume the transformation is differentiable and its Jacobian matrix is square and nonsingular on the stated domain, so the log-absolute-determinant term is well defined."
    if text == "square-root argument is nonnegative in the target domain":
        return "Assume the square-root argument is nonnegative on the target domain."
    if text == "target function is differentiable on the stated domain":
        return "Assume the target function is differentiable on the stated domain."
    if text == "matrix dimensions are conformable for the operation":
        return "Assume all matrix dimensions in this operation are conformable."
    if text == "matrix has the stated full-rank condition":
        return "Assume the matrix satisfies the stated full-rank condition."
    kind = _assumption_kind(assumption, target, source)
    if kind == "risky_pricing_expectation":
        return (
            "Assume a conditional transition law for \\(z'\\mid z\\); assume "
            "\\(D(k',b',z')R(k',z')\\) and "
            "\\((1-D(k',b',z'))b'(1+\\widetilde r(z,k',b'))\\) are measurable "
            "and conditionally integrable; and assume the zero-profit pricing "
            "equation is evaluated for \\(b'>0\\)."
        )
    if kind == "interior_foc_expectation":
        return (
            "Assume the conditional law of \\(z'\\mid z\\) is defined and independent "
            "of the choice being differentiated; assume \\(V^\\star(k',b',z')\\) is "
            "differentiable in \\(k'\\) and \\(b'\\) on the interior continuation "
            "region; assume \\(V^\\star_k\\) and \\(V^\\star_b\\) are conditionally "
            "integrable or dominated so differentiation can pass through "
            "\\(\\E[\\cdot\\mid z]\\)."
        )
    if text == "conditional expectation law is defined and the random payoff terms are integrable":
        return "Assume the conditional law of next-period shocks is defined given the current state and that every random payoff term inside the conditional expectation is integrable."
    if text == "lender pricing uses the stated zero-profit risk-free discounting convention":
        return "Assume lenders are risk-neutral or price under the stated pricing measure, the risk-free gross return is \\(1+r\\), and the promised debt payoff is priced by the zero-profit conditional expected payoff equation for positive debt."
    if text == "differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present":
        return "Assume the transition law for \\(z'\\) conditional on \\(z\\) is independent of the choice being differentiated, the continuation value derivatives are integrable, and differentiation may be interchanged with the conditional expectation."
    return f"State or verify the route-required assumption: {text}."


def _possible_assumption_sets(assumption: dict[str, Any], target: str = "", source: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    text = str(assumption.get("text", "")).strip()
    kind = _assumption_kind(assumption, target, source)
    if kind == "risky_pricing_expectation":
        return [
            {
                "id": "finite_state_risky_pricing",
                "role": "simple sufficient condition",
                "assumptions": [
                    _math("The transition law \\(P(z'\\mid z)\\) has finite support."),
                    _math("For every support point, \\(D(k',b',z')\\), \\(R(k',z')\\), and \\(\\widetilde r(z,k',b')\\) are finite and measurable."),
                    _math("The payoff partition is exhaustive: default payoff is \\(D R\\), solvent payoff is \\((1-D)b'(1+\\widetilde r)\\)."),
                    _math("The pricing convention is risk-neutral zero profit with gross risk-free return \\(1+r\\) and \\(b'>0\\)."),
                ],
                "closes": "The right side becomes a finite weighted sum equal to the lender's required risk-free payoff.",
            },
            {
                "id": "kernel_integrability_risky_pricing",
                "role": "general sufficient condition",
                "assumptions": [
                    _math("A conditional kernel \\(Q(dz'\\mid z)\\) is specified."),
                    _math("The maps \\(z'\\mapsto D(k',b',z')R(k',z')\\) and \\(z'\\mapsto (1-D(k',b',z'))b'(1+\\widetilde r(z,k',b'))\\) are \\(Q(\\cdot\\mid z)\\)-measurable."),
                    _math("Both payoff terms have finite conditional first moments under \\(Q(\\cdot\\mid z)\\)."),
                    _math("Debt is priced under the stated risk-neutral or pricing-measure convention."),
                ],
                "closes": "The expected risky payoff is a finite scalar, so the zero-profit equality is well posed.",
            },
        ]
    if kind == "interior_foc_expectation":
        return [
            {
                "id": "finite_state_interior_foc",
                "role": "simple sufficient condition",
                "assumptions": [
                    _math("The conditional law \\(P(z'\\mid z)\\) has finite support and does not depend on \\(k'\\) or \\(b'\\)."),
                    _math("For every support point, \\(V^\\star(\\cdot,\\cdot,z')\\) is differentiable at \\((k',b')\\) in the continuation region."),
                    _math("The finite sums of \\(V^\\star_k(k',b',z')\\) and \\(V^\\star_b(k',b',z')\\) are well defined."),
                    _math("The action \\((k',b')\\) is interior and the cash-flow/risky-rate functions are differentiable along the stated route."),
                ],
                "closes": "The derivative of the finite expected continuation value is the finite expected derivative.",
            },
            {
                "id": "dominated_interchange_interior_foc",
                "role": "continuous-state sufficient condition",
                "assumptions": [
                    _math("A conditional kernel \\(Q(dz'\\mid z)\\) is specified and is independent of \\(k'\\) and \\(b'\\)."),
                    _math("There are integrable envelopes dominating local derivatives of \\(V^\\star(k',b',z')\\) with respect to \\(k'\\) and \\(b'\\)."),
                    _math("The current state is a smooth continuation state, the action is interior, and the proof is away from default/borrowing kinks."),
                    _math("The current cash-flow term \\(e(k,k',b,b',z;\\widetilde r)\\) and \\(\\widetilde r(z,k',b')\\) are differentiable in the choice variables."),
                ],
                "closes": "Dominated convergence or a Leibniz rule justifies moving the derivative through \\(\\E[\\cdot\\mid z]\\).",
            },
        ]
    if text == "conditional expectation law is defined and the random payoff terms are integrable":
        return [
            {
                "id": "minimal_probability_integrability",
                "role": "minimal route condition",
                "assumptions": [
                    _math("A conditional probability law for next-period shocks \\(z'\\) given current \\(z\\) is fixed."),
                    "The payoff terms inside the conditional expectation are measurable with respect to that law.",
                    "The recovery and promised-payoff terms have finite conditional first moments.",
                ],
                "closes": "Makes the conditional expectation in the pricing or FOC expression well defined.",
            },
            {
                "id": "finite_state_sufficient_condition",
                "role": "strong sufficient condition",
                "assumptions": [
                    _math("The shock process has finite support conditional on each current \\(z\\)."),
                    "Recovery, default, value-derivative, and payoff terms are finite at every next-period shock node.",
                ],
                "closes": "Turns the conditional expectation into a finite weighted sum, avoiding measure-theoretic integrability questions.",
            },
            {
                "id": "dominated_continuous_sufficient_condition",
                "role": "continuous-state sufficient condition",
                "assumptions": [
                    "The conditional transition kernel exists and is fixed at the current state.",
                    "The random payoff or value-derivative expression is dominated by an integrable envelope.",
                ],
                "closes": "Supports existence of the conditional expectation, and when paired with smoothness can support differentiating expected continuation values.",
            },
        ]
    if text == "lender pricing uses the stated zero-profit risk-free discounting convention":
        return [
            {
                "id": "risk_neutral_lender_measure",
                "role": "economic pricing assumption",
                "assumptions": [
                    "Lenders are risk-neutral or the expectation is taken under the pricing measure used for debt valuation.",
                    "The risk-free gross return over the period is \\(1+r\\).",
                    "Positive promised debt \\(b'>0\\) is the instrument being priced.",
                ],
                "closes": "Justifies equating the required risk-free payoff \\(b'(1+r)\\) with the conditional expected lender payoff.",
            },
            {
                "id": "discounted_zero_profit_equivalent",
                "role": "equivalent convention",
                "assumptions": [
                    "Debt price is normalized so that the date-\\(t\\) loan amount and date-\\(t+1\\) payoff are compared using the risk-free return.",
                    "Recovery and solvent promised payoff are the exhaustive lender payoff states.",
                ],
                "closes": "Justifies the zero-profit equation after moving the risk-free discount factor to the left side.",
            },
        ]
    if text == "differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present":
        return [
            {
                "id": "choice_independent_transition_kernel",
                "role": "standard dynamic-programming route",
                "assumptions": [
                    "The conditional law of \\(z'\\) depends on current \\(z\\), not directly on the choice \\(k'\\) or \\(b'\\).",
                    "The continuation value \\(V^\\star(k',b',z')\\) is differentiable in \\(k'\\) and \\(b'\\) on the interior continuation region.",
                    "The derivatives \\(V^\\star_k(k',b',z')\\) and \\(V^\\star_b(k',b',z')\\) are conditionally integrable.",
                ],
                "closes": "Allows \\(\\partial/\\partial k'\\) and \\(\\partial/\\partial b'\\) to pass through the conditional expectation without transition-kernel derivative terms.",
            },
            {
                "id": "dominated_differentiation_route",
                "role": "continuous-state sufficient condition",
                "assumptions": [
                    "There is an integrable envelope dominating the local derivatives of the continuation value.",
                    "The current action is interior and away from default and borrowing kinks.",
                    "The risky-rate function and cash-flow function are differentiable along the chosen interior route.",
                ],
                "closes": "Justifies the Euler FOC step by a dominated-convergence or Leibniz-rule argument.",
            },
        ]
    return [
        {
            "id": "route_rule_assumption",
            "role": "route condition",
            "assumptions": [_proposal_text(assumption)],
            "closes": "States the deterministic route condition detected by the assumption rule.",
        }
    ]


def _mathematical_reasoning(assumption: dict[str, Any]) -> list[str]:
    return _mathematical_reasoning_for(assumption)


def _mathematical_reasoning_for(assumption: dict[str, Any], target: str = "", source: dict[str, Any] | None = None) -> list[str]:
    text = str(assumption.get("text", "")).strip()
    kind = _assumption_kind(assumption, target, source)
    if kind == "risky_pricing_expectation":
        return [
            _math("Mathematically missing: a conditional probability law \\(Q(dz'\\mid z)\\) or finite transition probabilities for \\(z'\\mid z\\)."),
            _math("Mathematically missing: measurability and conditional integrability of \\(D(k',b',z')R(k',z')\\) and \\((1-D(k',b',z'))b'(1+\\widetilde r(z,k',b'))\\)."),
            _math("Mathematically missing: the economic valuation convention that the conditional expected risky payoff is set equal to \\(b'(1+r)\\) for \\(b'>0\\)."),
            "Why missing: the proof partitions default and solvent payoffs, but a payoff partition alone does not define the expectation operator or the zero-profit pricing measure.",
        ]
    if kind in {"interior_foc_expectation", "foc_expectation_differentiation"}:
        return [
            _math("Mathematically missing: a conditional law \\(Q(dz'\\mid z)\\) for the continuation shock."),
            _math("Mathematically missing: differentiability of \\(V^\\star(k',b',z')\\) in \\(k'\\) and \\(b'\\) on the smooth interior continuation region."),
            _math("Mathematically missing: conditional integrability or domination of \\(V^\\star_k(k',b',z')\\) and \\(V^\\star_b(k',b',z')\\)."),
            _math("Mathematically missing: choice-independence of \\(Q(dz'\\mid z)\\), or else the derivative of the expectation includes transition-kernel derivative terms."),
            "Why missing: the proof says the derivative of the continuation term is the expected derivative, but that is an interchange-of-derivative-and-expectation step, not a formal consequence of differentiability alone.",
        ]
    if text == "conditional expectation law is defined and the random payoff terms are integrable":
        return [
            "The displayed equation contains a conditional expectation, so the expression is not a real-valued equation until a conditional law for the next-period shock is fixed.",
            "The random variables inside the expectation include recovery, default indicators, promised payoffs, or value derivatives; these must be measurable and integrable.",
            "Without these conditions the expectation may be undefined or infinite, so the zero-profit or FOC equation cannot be used as an equality of finite quantities.",
        ]
    if text == "lender pricing uses the stated zero-profit risk-free discounting convention":
        return [
            "The pricing equation equates the lender's required risk-free payoff with an expected risky payoff.",
            "That step is an economic pricing assumption: it requires risk-neutral valuation or an explicitly chosen pricing measure and payoff timing convention.",
            "Without the convention, the same payoff expression could require risk premia, stochastic discount factors, or a different discounting normalization.",
        ]
    if text == "differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present":
        return [
            "The proof differentiates the expected continuation value with respect to \\(k'\\) and \\(b'\\).",
            "That step is valid only if the derivative can pass through the conditional expectation and the conditional law does not add extra derivative terms.",
            "If the transition law depends on the differentiated choice, the FOC needs additional terms involving derivatives of the transition kernel.",
        ]
    return [
        "The target uses notation whose route rule requires this assumption before the expression is well posed.",
    ]


def _derivation_route(assumption: dict[str, Any], target: str = "", source: dict[str, Any] | None = None) -> list[dict[str, str]]:
    text = str(assumption.get("text", "")).strip()
    kind = _assumption_kind(assumption, target, source)
    if kind == "risky_pricing_expectation":
        return [
            {
                "step": "Define payoff random variable",
                "detail": _math("Let \\(Y(z')=D(k',b',z')R(k',z')+(1-D(k',b',z'))b'(1+\\widetilde r(z,k',b'))\\)."),
            },
            {
                "step": "Make conditional expectation well defined",
                "detail": _math("Under \\(Q(dz'\\mid z)\\) and integrability, \\(\\E[Y(z')\\mid z]=\\int Y(z')Q(dz'\\mid z)\\), or \\(\\sum_{z'}P(z'\\mid z)Y(z')\\) in finite state."),
            },
            {
                "step": "Apply zero-profit convention",
                "detail": _math("Risk-neutral zero profit requires \\(\\E[Y(z')\\mid z]=b'(1+r)\\) for the positive promised debt position \\(b'>0\\)."),
            },
            {
                "step": "Recover displayed pricing equation",
                "detail": _math("Substitute \\(Y(z')\\) back into the equality to obtain the displayed risky-debt pricing condition."),
            },
        ]
    if kind in {"interior_foc_expectation", "foc_expectation_differentiation"}:
        return [
            {
                "step": "Start from smooth interior objective",
                "detail": _math("For fixed current state, define \\(F(k',b')=e(k,k',b,b',z;\\widetilde r)+\\eta(e(k,k',b,b',z;\\widetilde r))+\\beta\\E[V^\\star(k',b',z')\\mid z]\\)."),
            },
            {
                "step": "Differentiate current cash flow",
                "detail": _math("By the chain rule, \\(\\partial(e+\\eta(e))/\\partial x=(1+\\eta'(e))\\,d\\bar e/dx=m(\\bar e)d\\bar e/dx\\) for \\(x\\in\\{k',b'\\}\\)."),
            },
            {
                "step": "Interchange derivative and expectation",
                "detail": _math("Under a choice-independent transition law \\(Q(dz'\\mid z)\\) and integrability/domination, \\(\\partial_x\\E[V^\\star(k',b',z')\\mid z]=\\E[V^\\star_x(k',b',z')\\mid z]\\)."),
            },
            {
                "step": "Exclude omitted kernel terms",
                "detail": _math("If \\(Q\\) depended on \\(x\\), a term like \\(\\int V^\\star(k',b',z')\\,\\partial_x Q(dz'\\mid z)\\) would appear; the assumption rules this out."),
            },
            {
                "step": "Apply interior optimality",
                "detail": _math("Set \\(\\partial F/\\partial k'=0\\) and \\(\\partial F/\\partial b'=0\\), giving the two Euler FOC equations."),
            },
        ]
    if text == "conditional expectation law is defined and the random payoff terms are integrable":
        return [
            {
                "step": "Define the conditional law",
                "detail": "Fix the transition kernel or conditional distribution for \\(z'\\) given the current state \\(z\\).",
            },
            {
                "step": "Check payoff measurability and integrability",
                "detail": "Verify the default indicator, recovery payoff, promised payoff, or value derivative terms are measurable and have finite conditional expectation.",
            },
            {
                "step": "Rewrite expectation as a well-defined operator",
                "detail": "Treat \\(\\E[\\cdot\\mid z]\\) as an integral or finite weighted sum over \\(z'\\).",
            },
            {
                "step": "Use the displayed equation",
                "detail": "Only after the expectation is finite does the pricing or FOC residual define a valid scalar equality.",
            },
        ]
    if text == "lender pricing uses the stated zero-profit risk-free discounting convention":
        return [
            {
                "step": "State the lender valuation convention",
                "detail": "Assume risk-neutral zero-profit pricing or specify the pricing measure.",
            },
            {
                "step": "Partition lender payoffs",
                "detail": "Default payoff is recovery; solvent payoff is promised debt repayment.",
            },
            {
                "step": "Take conditional expected payoff",
                "detail": "Compute the conditional expectation of those state-contingent payoffs under the stated pricing law.",
            },
            {
                "step": "Equate to risk-free required payoff",
                "detail": "Set the expected risky payoff equal to \\(b'(1+r)\\) for positive promised debt.",
            },
        ]
    if text == "differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present":
        return [
            {
                "step": "Start from the interior objective",
                "detail": "Use \\(e+\\eta(e)+\\beta\\E[V^\\star(k',b',z')\\mid z]\\) on the smooth continuation region.",
            },
            {
                "step": "Differentiate current cash flow",
                "detail": "Apply the chain rule to \\(e+\\eta(e)\\), giving \\(m(\\bar e)d\\bar e/dk'\\) and \\(m(\\bar e)d\\bar e/db'\\).",
            },
            {
                "step": "Differentiate continuation value",
                "detail": "Under interchange and kernel-independence assumptions, the derivative is \\(\\E[V^\\star_k(k',b',z')\\mid z]\\) or \\(\\E[V^\\star_b(k',b',z')\\mid z]\\).",
            },
            {
                "step": "Apply interior optimality",
                "detail": "Set the derivative of the smooth objective to zero for each interior choice dimension.",
            },
        ]
    return [
        {
            "step": "State route assumption",
            "detail": "Add or verify the detected assumption before applying the derivation step.",
        }
    ]


def build_assumption_gaps(
    target: str,
    assumptions: list[dict[str, Any]],
    *,
    source: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Convert missing assumption records into localized gap objects."""
    gaps: list[dict[str, Any]] = []
    for index, assumption in enumerate(assumptions, start=1):
        if assumption.get("status") != "missing":
            continue
        text = str(assumption.get("text", "assumption")).strip()
        gap_id = f"assumption_gap_{_source_prefix(source)}_{index}_{_slug(text)}"
        route_sources = assumption.get("route_category_sources")
        evidence_refs = [str(item) for item in route_sources if isinstance(item, str)] if isinstance(route_sources, list) else []
        if not evidence_refs:
            source_name = str(assumption.get("source", "assumption_discovery"))
            evidence_refs = [f"assumptions_required:{_slug(source_name)}"]
        gaps.append(
            {
                "id": gap_id,
                "location": _location(target, source),
                "problem": _problem_for(assumption),
                "why": _why_for(assumption, target, source),
                "affected_terms": _target_terms(target, assumption),
                "route_categories": list(assumption.get("route_categories", [])) if isinstance(assumption.get("route_categories"), list) else [],
                "route_kind": _assumption_kind(assumption, target, source),
                "source": "assumptions_required",
                "source_context": dict(source or {}),
                "evidence_refs": evidence_refs,
                "severity": "medium",
                "assumption": assumption,
            }
        )
    return gaps


def validate_assumption_proposal(proposal: dict[str, Any], gap: dict[str, Any]) -> dict[str, Any]:
    """Return non-certifying validation metadata for an assumption proposal."""
    route_categories = gap.get("route_categories") if isinstance(gap.get("route_categories"), list) else []
    return {
        "policy": ASSUMPTION_VALIDATION_POLICY,
        "status": "validated_by_rule" if route_categories else "diagnostic_only",
        "certifying": False,
        "reason": "The proposal was derived from the deterministic assumption route rule for this gap.",
        "backend_attempts": [
            {
                "backend": "assumption_rule",
                "status": "validated_by_rule" if route_categories else "diagnostic_only",
                "severity": "diagnostic",
                "reason": "Matched route categories: " + ", ".join(str(item) for item in route_categories)
                if route_categories
                else "No route category was available for stronger rule validation.",
            }
        ],
        "boundary": ASSUMPTION_VALIDATION_BOUNDARY,
        "gap_id": gap.get("id"),
        "proposal_id": proposal.get("id"),
    }


def build_assumption_proposals(gaps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build concrete assumption proposals linked to assumption gaps."""
    proposals: list[dict[str, Any]] = []
    for index, gap in enumerate(gaps, start=1):
        assumption = gap.get("assumption") if isinstance(gap.get("assumption"), dict) else {}
        target = str(gap.get("affected_terms", [""])[0]) if gap.get("affected_terms") else ""
        source = gap.get("source_context") if isinstance(gap.get("source_context"), dict) else {}
        proposal = {
            "id": f"assumption_proposal_{_slug(str(gap.get('id', index)))}",
            "gap_ids": [gap["id"]],
            "type": "add_assumption",
            "location": gap["location"],
            "proposal_text": _proposal_text(assumption, target, source),
            "rationale": f"This proposal closes `{gap['id']}` by stating the route-required condition before using the affected expression.",
            "missing_assumptions": _mathematical_reasoning_for(assumption, target, source),
            "possible_assumption_sets": _possible_assumption_sets(assumption, target, source),
            "derivation_route": _derivation_route(assumption, target, source),
            "route_kind": gap.get("route_kind"),
            "evidence_refs": list(gap.get("evidence_refs", [])),
            "application_status": "not_applied",
        }
        proposal["validation"] = validate_assumption_proposal(proposal, gap)
        proposals.append(proposal)
    return proposals


def build_unknown_route_gap(target: str, *, source: dict[str, Any] | None = None) -> dict[str, Any]:
    """Represent a target where the bounded assumption rules found no route."""
    return {
        "id": f"assumption_gap_{_source_prefix(source)}_unknown_route",
        "location": _location(target, source),
        "problem": "No route-required assumptions were detected by the bounded assumption rule set.",
        "why": "This is an evidence gap, not proof that no assumptions are needed. The target may require domain, shape, regularity, semantic, or source-backed assumptions outside the current rules.",
        "affected_terms": [target] if target else [],
        "route_categories": [],
        "source": "assumptions_required",
        "evidence_refs": ["assumptions_required:bounded_rule_set_no_match"],
        "severity": "low",
    }


def build_unknown_route_proposal(gap: dict[str, Any]) -> dict[str, Any]:
    proposal = {
        "id": f"assumption_proposal_{_slug(str(gap.get('id', 'unknown_route')))}",
        "gap_ids": [gap["id"]],
        "type": "formalize_assumption",
        "location": gap["location"],
        "proposal_text": "Formalize the target into a typed obligation or add a domain-specific assumption rule before claiming the assumption set is complete.",
        "rationale": "The bounded rule set could not identify route assumptions, so the next useful artifact is a typed target or domain-specific rule.",
        "missing_assumptions": [
            "The current bounded rules cannot identify a deterministic assumption route for this target.",
            "This is not evidence that no assumptions are needed; it means the target needs a typed obligation or domain-specific route rule.",
        ],
        "possible_assumption_sets": [
            {
                "id": "typed_obligation_first",
                "role": "next deterministic artifact",
                "assumptions": [
                    "Formalize the objects, domains, and operators in the target.",
                    "Add domain-specific rules only after the formalized target identifies the relevant operations.",
                ],
                "closes": "Makes the missing-assumption question inspectable by deterministic tools.",
            }
        ],
        "derivation_route": [
            {
                "step": "Formalize target",
                "detail": "Convert the source expression into a typed obligation with explicit objects and operations.",
            },
            {
                "step": "Run assumption discovery again",
                "detail": "Use the typed target or new domain rule to identify concrete route assumptions.",
            },
        ],
        "evidence_refs": list(gap.get("evidence_refs", [])),
        "application_status": "not_applied",
    }
    proposal["validation"] = {
        "policy": ASSUMPTION_VALIDATION_POLICY,
        "status": "not_encodable",
        "certifying": False,
        "reason": "No deterministic assumption route was available for this target.",
        "backend_attempts": [
            {
                "backend": "assumption_rule",
                "status": "not_encodable",
                "severity": "diagnostic",
                "reason": "The bounded rule set did not match this target.",
            }
        ],
        "boundary": ASSUMPTION_VALIDATION_BOUNDARY,
        "gap_id": gap.get("id"),
        "proposal_id": proposal.get("id"),
    }
    return proposal


def summarize_assumption_validation(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    statuses: dict[str, int] = {}
    attempts = 0
    for proposal in proposals:
        validation = proposal.get("validation") if isinstance(proposal.get("validation"), dict) else {}
        status = str(validation.get("status", "missing"))
        statuses[status] = statuses.get(status, 0) + 1
        backend_attempts = validation.get("backend_attempts")
        if isinstance(backend_attempts, list):
            attempts += len(backend_attempts)
    return {
        "policy": ASSUMPTION_VALIDATION_POLICY,
        "status_counts": statuses,
        "proposal_count": len(proposals),
        "backend_attempt_count": attempts,
        "certifying": False,
        "boundary": ASSUMPTION_VALIDATION_BOUNDARY,
    }


def build_assumption_tool_uses(
    target: str,
    *,
    provided_assumptions: list[str] | None = None,
    source_tool: str = "assumptions_required",
) -> list[dict[str, Any]]:
    return [
        {
            "tool": source_tool,
            "arguments": {
                "target": target,
                "provided_assumptions": list(provided_assumptions or []),
            },
            "purpose": "Detect route-required assumptions with a bounded deterministic rule set.",
            "status": "completed",
            "output_contract": "assumption_discovery_result",
        },
        {
            "tool": "build_assumption_gaps",
            "arguments": {"target": target},
            "purpose": "Convert missing assumption records into localized gap objects.",
            "status": "completed",
            "output_contract": "assumption_gap_list",
        },
        {
            "tool": "build_assumption_proposals",
            "arguments": {"gap_count": "derived"},
            "purpose": "Create concrete assumption proposals linked to detected gaps.",
            "status": "completed",
            "output_contract": "assumption_proposal_list",
        },
    ]
