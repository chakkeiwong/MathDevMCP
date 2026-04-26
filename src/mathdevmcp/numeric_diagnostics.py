from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract


@dataclass(frozen=True)
class NumericDiagnosticSuggestion:
    kind: str
    target: str
    priority: str
    reason: str


def suggest_numeric_diagnostics(typed_diagnostic: dict) -> dict:
    obligation = typed_diagnostic.get("obligation", {})
    unresolved = set(obligation.get("unresolved_constructs", []))
    suggestions: list[dict] = []
    if "determinant" in unresolved:
        suggestions.append(asdict(NumericDiagnosticSuggestion("logdet_domain_check", "determinant/logdet operand", "high", "Log determinant requires square positive-definite or otherwise valid matrix input.")))
    if "matrix_inverse" in unresolved:
        suggestions.append(asdict(NumericDiagnosticSuggestion("linear_solve_residual_check", "inverse/solve operand", "high", "Inverse notation should be checked with solve residuals and conditioning diagnostics.")))
    if "derivative" in unresolved:
        suggestions.append(asdict(NumericDiagnosticSuggestion("finite_difference_gradient_check", "derivative expression", "medium", "Derivative notation should be sanity-checked against finite differences when executable code exists.")))
    if "trace" in unresolved:
        suggestions.append(asdict(NumericDiagnosticSuggestion("trace_shape_check", "trace operand", "medium", "Trace requires square matrix input and should be shape-checked.")))
    status = "suggested" if suggestions else "not_applicable"
    reason = "Numeric diagnostics were suggested for unresolved typed constructs." if suggestions else "No numeric diagnostic suggestions were needed."
    return attach_contract({"status": status, "reason": reason, "suggestions": suggestions}, "numeric_diagnostic_suggestions")
