from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract


@dataclass(frozen=True)
class ShapeDiagnosticResult:
    status: str
    reason: str
    missing_constraints: list[dict]
    satisfied_constraints: list[dict]
    ast_evidence: list[dict]


def diagnose_shape_constraints(typed_diagnostic: dict, *, ast_graph: dict | None = None) -> dict:
    constraints = typed_diagnostic.get("obligation", {}).get("dimension_constraints", [])
    ast_nodes = (ast_graph or {}).get("nodes", [])
    ast_evidence = [
        {"operation": node.get("operation"), "line": node.get("line"), "expression": node.get("expression")}
        for node in ast_nodes
        if node.get("operation") in {"shape_guard", "covariance_guard", "shape_reference"}
    ]
    missing = [constraint for constraint in constraints if constraint.get("status") == "missing_assumption"]
    satisfied = [constraint for constraint in constraints if constraint.get("status") == "explicit_or_satisfied"]
    if missing and ast_evidence:
        status = "partially_supported"
        reason = "Typed constraints are missing from math context, but AST shape/covariance guard evidence exists."
    elif missing:
        status = "needs_assumptions"
        reason = "Typed shape/dimension constraints need explicit assumptions."
    else:
        status = "supported"
        reason = "No missing typed shape/dimension constraints were found."
    result = ShapeDiagnosticResult(status, reason, missing, satisfied, ast_evidence)
    return attach_contract(asdict(result), "shape_diagnostic_result")
