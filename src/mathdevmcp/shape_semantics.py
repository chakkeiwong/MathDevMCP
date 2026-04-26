from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract


@dataclass(frozen=True)
class ShapeSemanticReport:
    status: str
    reason: str
    evidence: list[dict]
    missing_policies: list[dict]


def analyze_shape_semantics(ast_graph: dict, *, require_batch_policy: bool = False, require_broadcasting_policy: bool = False) -> dict:
    nodes = ast_graph.get("nodes", [])
    evidence = [
        {"operation": node.get("operation"), "line": node.get("line"), "expression": node.get("expression")}
        for node in nodes
        if node.get("operation") in {"shape_guard", "covariance_guard", "shape_reference", "cholesky", "vectorized_loop", "scan_loop"}
    ]
    operations = set(ast_graph.get("operations", []))
    missing: list[dict] = []
    if require_batch_policy and operations.intersection({"vectorized_loop", "scan_loop"}) and not any("batch" in str(item.get("expression", "")).lower() for item in evidence):
        missing.append({"kind": "batch_axis_policy_required", "severity": "medium", "reason": "Vectorized or scan code should state batch/time-axis policy explicitly."})
    if require_broadcasting_policy and "matmul" in operations and not any("broadcast" in str(item.get("expression", "")).lower() for item in evidence):
        missing.append({"kind": "broadcasting_policy_required", "severity": "medium", "reason": "Matrix operations should state broadcasting policy when batch dimensions may be present."})
    if "inverse_or_solve" in operations and not any(item["operation"] in {"covariance_guard", "cholesky"} for item in evidence):
        missing.append({"kind": "invertibility_or_spd_guard_required", "severity": "high", "reason": "Solve/inverse operation lacks explicit SPD, Cholesky, or covariance guard evidence."})
    status = "unverified" if missing else "supported"
    reason = "Shape semantics have missing diagnostic policies." if missing else "Shape semantic evidence was extracted without blocking gaps."
    return attach_contract(asdict(ShapeSemanticReport(status, reason, evidence, missing)), "shape_semantic_report")
