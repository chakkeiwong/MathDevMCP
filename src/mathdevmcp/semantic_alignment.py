from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract


@dataclass(frozen=True)
class SemanticAlignmentFinding:
    kind: str
    status: str
    severity: str
    reason: str


@dataclass(frozen=True)
class SemanticAlignmentReport:
    status: str
    reason: str
    required_operations: list[str]
    observed_operations: list[str]
    findings: list[dict]


def align_document_to_code(proof_audit_v2: dict, ast_graph: dict, *, required_operations: list[str] | None = None) -> dict:
    required = required_operations or _required_from_audit(proof_audit_v2)
    observed = set(ast_graph.get("operations", []))
    findings: list[dict] = []
    for operation in required:
        if operation in observed:
            findings.append(asdict(SemanticAlignmentFinding("required_operation_present", "consistent", "diagnostic", f"Required operation {operation} is present in code evidence.")))
        else:
            findings.append(asdict(SemanticAlignmentFinding("required_operation_missing", "mismatch", "high", f"Required operation {operation} is missing from code evidence.")))
    if "shape_guard" not in observed and any(op in required for op in {"logdet", "inverse_or_solve", "quadratic_form"}):
        findings.append(asdict(SemanticAlignmentFinding("shape_guard_missing", "unverified", "medium", "Matrix-heavy document obligation lacks code shape-guard evidence.")))
    if not required:
        findings.append(asdict(SemanticAlignmentFinding("no_required_operations", "inconclusive", "medium", "No required operations were inferred for semantic alignment.")))
    if any(item["status"] == "mismatch" for item in findings):
        status = "mismatch"
        reason = "Code is missing at least one required documented operation."
    elif any(item["status"] in {"unverified", "inconclusive"} for item in findings):
        status = "unverified"
        reason = "Code has required operations, but some semantic evidence remains diagnostic-only."
    else:
        status = "consistent"
        reason = "Required documented operations are present in code evidence."
    return attach_contract(
        asdict(SemanticAlignmentReport(status, reason, required, sorted(observed), findings)),
        "semantic_alignment_report",
    )


def _required_from_audit(proof_audit_v2: dict) -> list[str]:
    required: set[str] = set()
    for obligation in proof_audit_v2.get("obligations", []):
        unresolved = set(obligation.get("typed_diagnostic", {}).get("obligation", {}).get("unresolved_constructs", []))
        if "determinant" in unresolved:
            required.add("logdet")
        if "matrix_inverse" in unresolved:
            required.add("inverse_or_solve")
        if "transpose" in unresolved:
            required.add("quadratic_form")
        if "derivative" in unresolved:
            required.add("gradient")
    return sorted(required)
