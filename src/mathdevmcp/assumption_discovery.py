from __future__ import annotations

"""Route-required assumption discovery for math debugging workflows."""

from dataclasses import asdict, dataclass
import re
from typing import Any

from .contracts import attach_contract
from .math_debugging import assumption_record, math_question, workbench_obligation, workbench_result


_ASSUMPTION_RULES = [
    {
        "kind": "division_nonzero",
        "patterns": [re.compile(r"/"), re.compile(r"\*\*-1\b"), re.compile(r"\^-1\b")],
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
        "patterns": [re.compile(r"\blogdet\s*\("), re.compile(r"\bdet\s*\(")],
        "text": "matrix operand is square with valid determinant domain, usually positive definite for logdet",
        "source": "determinant or logdet",
        "route_categories": ["covariance_condition", "domain_condition"],
    },
    {
        "kind": "sqrt_domain",
        "patterns": [re.compile(r"\bsqrt\s*\(")],
        "text": "square-root argument is nonnegative in the target domain",
        "source": "square root",
        "route_categories": ["domain_condition"],
    },
    {
        "kind": "differentiability",
        "patterns": [re.compile(r"\\partial"), re.compile(r"\bd/d"), re.compile(r"\bgrad\s*\("), re.compile(r"\bderivative\s*\(")],
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


def _provided(text: str, provided_assumptions: list[str]) -> bool:
    normalized_text = " ".join(text.lower().split())
    normalized_provided = [" ".join(item.lower().split()) for item in provided_assumptions]
    return any(normalized_text in item or item in normalized_text for item in normalized_provided)


def assumptions_required(target: str, *, provided_assumptions: list[str] | None = None) -> dict:
    provided = provided_assumptions or []
    assumptions: list[dict[str, Any]] = []
    for rule in _ASSUMPTION_RULES:
        if not any(pattern.search(target) for pattern in rule["patterns"]):
            continue
        status = "provided" if _provided(rule["text"], provided) else "missing"
        assumptions.append(
            assumption_record(
                rule["text"],
                status=status,
                source=rule["source"],
                necessity="required_by_route",
                used_by=[rule["kind"]],
                route_categories=list(rule["route_categories"]),
                route_category_sources=[f"assumption_rule:{rule['kind']}"],
            )
        )

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
