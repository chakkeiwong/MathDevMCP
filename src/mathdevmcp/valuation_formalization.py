from __future__ import annotations

"""Narrow, source-bound validation for supported valuation definitions."""

from typing import Any, Mapping

from .assumption_discovery import assumptions_required
from .claim_semantics import source_role_controls_routing, validate_claim_semantics
from .contracts import attach_contract


TERMINAL_VALUE_TARGET = "dTV = rho*dCF_next/(r_disc + lambda_attrition + q)"
_SOURCE_TOKENS = (r"\Delta TV", r"\frac", r"r_{\mathrm{disc}}", r"\lambda_i", "q_i")
_UNSUPPORTED_MARKERS = (r"\E", "expectation", "causal", "policy", "argmax", "argmin")


def _compact_target(value: str) -> str:
    return "".join(str(value).split())


def validate_terminal_value_definition(
    normalized_target: str,
    *,
    provided_assumptions: list[str] | None = None,
    claim_semantics: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Check only the supported scalar placeholder's role, domain, and algebra."""
    role = validate_claim_semantics(claim_semantics)
    base = {
        "template_id": "valuation_terminal_value_v1",
        "normalized_target": normalized_target,
        "claim_semantics": role,
        "non_claims": [
            "Algebraic consistency under a source definition is not proof of economic validity.",
            "This result does not validate calibration, persistence, attrition, causal, expectation, or policy semantics.",
            "This result is not a universal terminal-value theorem or publication authorization.",
        ],
    }
    if not source_role_controls_routing(role) or role.get("role") != "definition":
        return attach_contract(
            {
                **base,
                "status": "inconclusive",
                "reason": "A validated source-evidenced definition role is required before valuation formalization.",
                "backend_attempt": None,
                "assumption_diagnostic": None,
            },
            "valuation_terminal_value_validation",
        )
    raw_source_target = str((claim_semantics or {}).get("source_target", ""))
    if str((claim_semantics or {}).get("label", "")) != "eq:terminal-value-base" or not all(
        token in raw_source_target for token in _SOURCE_TOKENS
    ):
        return attach_contract(
            {
                **base,
                "status": "unsupported_notation",
                "reason": "The source-bound definition does not match the reviewed terminal-value source projection.",
                "backend_attempt": None,
                "assumption_diagnostic": None,
            },
            "valuation_terminal_value_validation",
        )
    if any(marker.lower() in normalized_target.lower() for marker in _UNSUPPORTED_MARKERS):
        return attach_contract(
            {
                **base,
                "status": "unsupported_semantics",
                "reason": "Expectation, causal, or policy semantics are outside this scalar algebra adapter.",
                "backend_attempt": None,
                "assumption_diagnostic": None,
            },
            "valuation_terminal_value_validation",
        )
    if _compact_target(normalized_target) != _compact_target(TERMINAL_VALUE_TARGET):
        return attach_contract(
            {
                **base,
                "status": "unsupported_notation",
                "reason": "The normalized target is outside the reviewed terminal-value projection.",
                "backend_attempt": None,
                "assumption_diagnostic": None,
            },
            "valuation_terminal_value_validation",
        )

    assumptions = assumptions_required(normalized_target, provided_assumptions=provided_assumptions)
    if assumptions["missing_assumptions"]:
        return attach_contract(
            {
                **base,
                "status": "missing_assumptions",
                "reason": "The exact terminal-value denominator requires an explicit nonzero assumption.",
                "assumption_diagnostic": assumptions,
                "backend_attempt": None,
            },
            "valuation_terminal_value_validation",
        )

    try:
        import sympy as sp
    except Exception as exc:  # pragma: no cover - optional dependency failure.
        return attach_contract(
            {
                **base,
                "status": "backend_unavailable",
                "reason": f"SymPy is unavailable: {exc}",
                "assumption_diagnostic": assumptions,
                "backend_attempt": {"backend": "sympy", "status": "unavailable", "severity": "diagnostic"},
            },
            "valuation_terminal_value_validation",
        )

    d_tv, rho, d_cf_next, r_disc, lambda_attrition, q = sp.symbols(
        "dTV rho dCF_next r_disc lambda_attrition q", real=True
    )
    denominator = r_disc + lambda_attrition + q
    definition_rhs = rho * d_cf_next / denominator
    residual = sp.simplify((d_tv * denominator - rho * d_cf_next).subs(d_tv, definition_rhs))
    passed = residual == 0
    return attach_contract(
        {
            **base,
            "status": "algebraically_consistent" if passed else "inconclusive",
            "reason": (
                "SymPy confirmed the scoped cross-multiplication identity under the exact nonzero denominator assumption."
                if passed
                else "The scoped SymPy cross-multiplication diagnostic did not reduce to zero."
            ),
            "assumption_diagnostic": assumptions,
            "backend_attempt": {
                "backend": "sympy",
                "status": "passed" if passed else "unknown",
                "severity": "diagnostic",
                "input": {
                    "definition": TERMINAL_VALUE_TARGET,
                    "denominator": "r_disc + lambda_attrition + q",
                    "cross_multiplication": "dTV*(r_disc + lambda_attrition + q) - rho*dCF_next",
                },
                "residual": str(residual),
                "certification_boundary": "This backend result checks scalar algebra under the declared definition and domain only.",
            },
        },
        "valuation_terminal_value_validation",
    )
