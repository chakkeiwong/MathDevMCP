from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .assumptions import diagnose_assumptions_for_label
from .contracts import attach_contract
from .operation_consistency import compare_label_operations
from .proof_audit import audit_derivation_for_label


@dataclass(frozen=True)
class LikelihoodAuditResult:
    status: str
    reason: str
    proof_audit: dict
    assumption_diagnostic: dict
    operation_consistency: dict


def audit_likelihood_implementation(doc_root: str, label: str, code_path: str, *, required_operations: list[str] | None = None, context_text: str = "") -> dict:
    proof = audit_derivation_for_label(doc_root, label, backend="sympy")
    assumptions = diagnose_assumptions_for_label(doc_root, label, context_text=context_text)
    operations = compare_label_operations(doc_root, label, code_path, required_operations=required_operations)
    if operations["status"] == "mismatch":
        status = "mismatch"
        reason = "The likelihood implementation is missing required mathematical operations."
    elif assumptions["status"] == "missing_assumptions" or proof["status"] in {"inconclusive", "unverified"}:
        status = "unverified"
        reason = "The implementation operations are plausible, but proof or assumptions need review."
    else:
        status = "consistent"
        reason = "The checked likelihood implementation evidence is consistent."
    result = LikelihoodAuditResult(status, reason, proof, assumptions, operations)
    return attach_contract(asdict(result), "likelihood_implementation_audit", doc_context=proof.get("doc_context"))
