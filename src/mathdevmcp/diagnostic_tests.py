from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract


@dataclass(frozen=True)
class DiagnosticSuggestion:
    kind: str
    reason: str
    target: str
    priority: str


def suggest_diagnostic_tests(audit: dict) -> dict:
    suggestions: list[dict] = []
    missing_ops = set(audit.get("operation_consistency", {}).get("missing_operations", []))
    missing_assumptions = {item.get("text", "") for item in audit.get("assumption_diagnostic", {}).get("missing_assumptions", [])}
    proof = audit.get("proof_audit", {})
    if "logdet" in missing_ops:
        suggestions.append(asdict(DiagnosticSuggestion("synthetic_logdet_likelihood_test", "A required log determinant operation is missing.", "logdet", "high")))
    if "inverse_or_solve" in missing_ops:
        suggestions.append(asdict(DiagnosticSuggestion("linear_solve_consistency_test", "A required inverse/solve operation is missing.", "inverse_or_solve", "high")))
    if any("differentiability" in item for item in missing_assumptions) or "derivative" in str(proof):
        suggestions.append(asdict(DiagnosticSuggestion("finite_difference_gradient_check", "Derivative-related obligations need numerical validation.", "gradient", "medium")))
    if "hamiltonian" in str(audit).lower():
        suggestions.append(asdict(DiagnosticSuggestion("hmc_energy_conservation_smoke", "Hamiltonian context should have an energy conservation smoke check.", "hamiltonian", "medium")))
    return attach_contract({"suggestions": suggestions}, "diagnostic_suggestions")
