from __future__ import annotations

"""High-level structural math-to-code audit workflow."""

from typing import Any

from .equation_code_match import code_implements_equation
from .high_level_contracts import action, validate_high_level_result
from .high_level_workflows import package_code_audit_result


def audit_math_to_code(
    math: str,
    code: str,
    *,
    aliases: dict[str, str] | None = None,
) -> dict[str, Any]:
    """Audit whether code structurally matches a mathematical expression."""
    low_level = code_implements_equation(math, code, aliases=aliases)
    result = package_code_audit_result(low_level, question="Does this code implement the supplied math?")
    result["actions"].append(
        action(
            "human_review",
            "Review structural matches, missing terms, aliases, and audit-only extras before treating code as correct.",
        )
    )
    errors = validate_high_level_result(result)
    if errors:
        raise ValueError(f"invalid audit_math_to_code result: {errors}")
    return result
