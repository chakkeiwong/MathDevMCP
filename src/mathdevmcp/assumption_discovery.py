from __future__ import annotations

"""Route-required assumption discovery for math debugging workflows."""

from dataclasses import asdict, dataclass
import re
from typing import Any

from .contracts import attach_contract
from .math_debugging import assumption_record, math_question, workbench_obligation, workbench_result


_ASSUMPTION_RULES = [
    {
        "kind": "jacobian_logdet_domain",
        "patterns": [
            re.compile(r"\\log\s*\|?\\det\s+J", re.IGNORECASE),
            re.compile(r"jacobian[^.\n]*\\det", re.IGNORECASE),
        ],
        "text": "Jacobian matrix is square and nonsingular with valid log-absolute-determinant domain",
        "source": "Jacobian log-determinant",
        "route_categories": ["domain_condition", "shape_condition", "smoothness_condition"],
    },
    {
        "kind": "division_nonzero",
        "patterns": [re.compile(r"/"), re.compile(r"\\(?:frac|dfrac|tfrac)\b"), re.compile(r"\*\*-1\b"), re.compile(r"\^-1\b")],
        "text": "denominator is nonzero",
        "source": "division or reciprocal",
        "route_categories": ["domain_condition"],
    },
    {
        "kind": "inverse_invertible",
        "patterns": [re.compile(r"\binv\s*\("), re.compile(r"\bsolve\s*\(")],
        "text": "matrix operand is square and invertible",
        "source": "inverse or solve",
        "route_categories": ["domain_condition", "shape_condition"],
    },
    {
        "kind": "logdet_domain",
        "patterns": [re.compile(r"\blogdet\s*\("), re.compile(r"\bdet\s*\("), re.compile(r"\\det\b")],
        "text": "matrix operand is square with valid determinant domain, usually positive definite for logdet",
        "source": "determinant or logdet",
        "route_categories": ["covariance_condition", "domain_condition"],
    },
    {
        "kind": "conditional_expectation_integrability",
        "patterns": [
            re.compile(r"\\E\b"),
            re.compile(r"\\mathbb\{E\}"),
            re.compile(r"conditional expectation", re.IGNORECASE),
        ],
        "text": "conditional expectation law is defined and the random payoff terms are integrable",
        "source": "conditional expectation",
        "route_categories": ["probability_condition", "integrability_condition", "domain_condition"],
    },
    {
        "kind": "zero_profit_pricing_convention",
        "patterns": [
            re.compile(r"zero-profit", re.IGNORECASE),
            re.compile(r"risk-free return", re.IGNORECASE),
            re.compile(r"lender prices debt", re.IGNORECASE),
            re.compile(r"risky debt rate", re.IGNORECASE),
        ],
        "text": "lender pricing uses the stated zero-profit risk-free discounting convention",
        "source": "zero-profit risky-debt pricing",
        "route_categories": ["pricing_condition", "economic_condition", "domain_condition"],
    },
    {
        "kind": "foc_expectation_differentiation",
        "patterns": [
            re.compile(r"first-order conditions", re.IGNORECASE),
            re.compile(r"\\label\{prop:interior-foc\}"),
            re.compile(r"\\E\s*\[V\^\\star_[kb]", re.DOTALL),
        ],
        "text": "differentiation under the conditional expectation is justified and no omitted transition-derivative terms are present",
        "source": "interior FOC expectation derivative",
        "route_categories": ["smoothness_condition", "integrability_condition", "probability_condition"],
    },
    {
        "kind": "sqrt_domain",
        "patterns": [
            re.compile(r"\bsqrt\s*\("),
            re.compile(r"\\sqrt(?:\s*\[[^\]]*\])?\s*\{"),
        ],
        "text": "square-root argument is nonnegative in the target domain",
        "source": "square root",
        "route_categories": ["domain_condition"],
    },
    {
        "kind": "differentiability",
        "patterns": [
            re.compile(r"\\partial"),
            re.compile(r"\\frac\s*\{d[^{}]*\}\s*\{d"),
            re.compile(r"\bd/d"),
            re.compile(r"\bgrad\s*\("),
            re.compile(r"\bderivative\s*\("),
        ],
        "explicit_patterns": [re.compile(r"\bdifferentiable\b", re.IGNORECASE)],
        "text": "target function is differentiable on the stated domain",
        "source": "derivative",
        "route_categories": ["smoothness_condition"],
    },
    {
        "kind": "matrix_conformability",
        "patterns": [re.compile(r"@"), re.compile(r"\btrace\s*\("), re.compile(r"\btr\s*\("), re.compile(r"\btranspose\s*\(")],
        "text": "matrix dimensions are conformable for the operation",
        "source": "matrix operation",
        "route_categories": ["shape_condition"],
    },
    {
        "kind": "rank_condition",
        "patterns": [re.compile(r"\brank\s*\("), re.compile(r"full rank", re.IGNORECASE)],
        "text": "matrix has the stated full-rank condition",
        "source": "rank condition",
        "route_categories": ["rank_condition"],
    },
]


@dataclass(frozen=True)
class AssumptionDiscoveryResult:
    status: str
    reason: str
    target: str
    provided_assumptions: list[str]
    assumptions: list[dict[str, Any]]
    missing_assumptions: list[dict[str, Any]]
    workbench_result: dict[str, Any]


def _canonical_expression(text: str) -> str:
    value = str(text).lower()
    value = re.sub(r"\\mathrm\{([^{}]+)\}", r"\1", value)
    value = re.sub(r"\\(?:widehat|hat)\{([^{}]+)\}", r"\1", value)
    value = value.replace(r"\lambda", "lambda").replace(r"\rho", "rho")
    value = re.sub(r"_\{([^{}]+)\}", r"_\1", value)
    value = value.replace("{", "").replace("}", "")
    return re.sub(r"[\s`$()]", "", value)


def _balanced_group(text: str, start: int) -> tuple[str, int] | None:
    if start >= len(text) or text[start] != "{":
        return None
    depth = 0
    for index in range(start, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return text[start + 1 : index], index + 1
    return None


def _denominator_expression(target: str) -> str | None:
    for marker in (r"\frac", r"\dfrac", r"\tfrac"):
        offset = 0
        while True:
            position = target.find(marker, offset)
            if position < 0:
                break
            numerator_start = position + len(marker)
            while numerator_start < len(target) and target[numerator_start].isspace():
                numerator_start += 1
            numerator = _balanced_group(target, numerator_start)
            if numerator is None:
                break
            denominator_start = numerator[1]
            while denominator_start < len(target) and target[denominator_start].isspace():
                denominator_start += 1
            denominator = _balanced_group(target, denominator_start)
            if denominator is not None and denominator[0].strip():
                return denominator[0].strip()
            offset = numerator[1]
    parenthesized = re.search(r"/\s*\(([^()]+)\)", target)
    if parenthesized:
        return parenthesized.group(1).strip()
    plain = re.search(r"/\s*([A-Za-z_][A-Za-z0-9_]*(?:\s*[+\-]\s*[A-Za-z_][A-Za-z0-9_]*)*)", target)
    return plain.group(1).strip() if plain else None


def _nonzero_assumption_expression(assumption: str) -> str | None:
    match = re.search(r"(.+?)\s*(?:!=|≠|\\ne)\s*0(?:\b|$)", assumption)
    return match.group(1).strip() if match else None


def _provided(text: str, provided_assumptions: list[str], *, requirement_expression: str | None = None) -> tuple[bool, str | None]:
    normalized_text = " ".join(text.lower().split())
    normalized_provided = [" ".join(item.lower().split()) for item in provided_assumptions]
    for original, normalized in zip(provided_assumptions, normalized_provided):
        if normalized_text in normalized or normalized in normalized_text:
            return True, original
        provided_expression = _nonzero_assumption_expression(original)
        if requirement_expression and provided_expression and _canonical_expression(provided_expression) == _canonical_expression(requirement_expression):
            return True, original
    return False, None


def _explicit_in_target(rule: dict[str, Any], target: str) -> bool:
    patterns = rule.get("explicit_patterns")
    if not isinstance(patterns, list):
        return False
    return any(pattern.search(target) for pattern in patterns)


def assumptions_required(target: str, *, provided_assumptions: list[str] | None = None) -> dict:
    provided = provided_assumptions or []
    assumptions: list[dict[str, Any]] = []
    for rule in _ASSUMPTION_RULES:
        if not any(pattern.search(target) for pattern in rule["patterns"]):
            continue
        requirement_expression = _denominator_expression(target) if rule["kind"] == "division_nonzero" else None
        supplied, discharged_by = _provided(
            rule["text"],
            provided,
            requirement_expression=requirement_expression,
        )
        status = "provided" if supplied or _explicit_in_target(rule, target) else "missing"
        record = assumption_record(
                rule["text"],
                status=status,
                source=rule["source"],
                necessity="required_by_route",
                used_by=[rule["kind"]],
                route_categories=list(rule["route_categories"]),
                route_category_sources=[f"assumption_rule:{rule['kind']}"],
            )
        if requirement_expression:
            record["requirement_expression"] = requirement_expression
            record["discharged_by"] = discharged_by
            record["matching_policy"] = "canonical_exact_expression_nonzero"
        assumptions.append(record)

    missing = [item for item in assumptions if item["status"] == "missing"]
    if missing:
        status = "missing_assumptions"
        reason = "At least one route-required assumption is missing."
    elif assumptions:
        status = "unknown"
        reason = "All route-detected assumptions were provided, but this diagnostic route does not prove the target."
    else:
        status = "unknown"
        reason = "No route-required assumptions were detected by the bounded rule set."

    question = math_question(
        "assumptions_required",
        target,
        assumptions=provided,
        context={"necessity_boundary": "route-required or sufficient, not minimal necessity"},
    )
    obligation = workbench_obligation(
        "assumption-obligation-1",
        lhs=target,
        rhs="well-posed under route assumptions",
        status=status,
        reason=reason,
        assumptions=provided,
        missing_assumptions=missing,
    )
    workbench = workbench_result(
        question,
        status=status,
        reason=reason,
        obligations=[obligation],
        assumptions=assumptions,
        actions=[
            {"kind": "state_or_verify_assumption", "assumption": item["text"], "source": item["source"]}
            for item in missing
        ],
    )
    return attach_contract(
        asdict(
            AssumptionDiscoveryResult(
                status=status,
                reason=reason,
                target=target,
                provided_assumptions=provided,
                assumptions=assumptions,
                missing_assumptions=missing,
                workbench_result=workbench,
            )
        ),
        "assumption_discovery_result",
    )
