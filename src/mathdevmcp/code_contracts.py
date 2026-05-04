"""Diagnostic code contracts for tensor-oriented implementations."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract


@dataclass(frozen=True)
class CodeContractFinding:
    kind: str
    status: str
    severity: str
    reason: str


def diagnose_code_contracts(ast_graph: dict) -> dict:
    operations = set(ast_graph.get("operations", []))
    source_text = " ".join(
        f"{node.get('target', '')} {node.get('expression', '')}"
        for node in ast_graph.get("nodes", [])
    ).lower()
    findings: list[dict] = []

    def add(kind: str, status: str, severity: str, reason: str) -> None:
        findings.append(asdict(CodeContractFinding(kind, status, severity, reason)))

    if "shape_reference" in operations or "shape_guard" in operations:
        add("shape_contract", "supported", "low", "Shape references or guards were found.")
    else:
        add("shape_contract", "unverified", "medium", "No explicit shape references or guards were found.")

    if "dtype" in source_text or "float64" in source_text or "float32" in source_text:
        add("dtype_contract", "supported", "low", "Dtype policy evidence was found.")
    else:
        add("dtype_contract", "unverified", "medium", "No explicit dtype policy evidence was found.")

    if "batch" in source_text or "vmap" in source_text or "vectorized_loop" in operations:
        add("batch_axis_contract", "supported", "low", "Batch/vectorization evidence was found.")
    else:
        add("batch_axis_contract", "unverified", "medium", "No batch-axis policy evidence was found.")

    if "jit" in source_text or "xla" in source_text or "custom_call" in source_text:
        add("xla_custom_op_boundary", "requires_review", "medium", "XLA/JIT/custom-op evidence should be reviewed as an implementation boundary.")

    if "isfinite" in source_text or "finite" in source_text:
        add("finite_value_contract", "supported", "low", "Finite-value evidence was found.")
    else:
        add("finite_value_contract", "unverified", "medium", "No finite target/gradient guard evidence was found.")

    status = "unverified" if any(item["status"] in {"unverified", "requires_review"} for item in findings) else "consistent"
    reason = "Code contracts have diagnostic gaps." if status == "unverified" else "Code contracts have supporting evidence."
    return attach_contract(
        {
            "status": status,
            "reason": reason,
            "findings": findings,
            "verification_boundary": "Code contracts are implementation diagnostics, not mathematical proof.",
        },
        "code_contract_diagnostics",
    )
