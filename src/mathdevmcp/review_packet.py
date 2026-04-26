from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .agent_workflows import audit_likelihood_implementation
from .contracts import attach_contract


@dataclass(frozen=True)
class ReviewPacket:
    status: str
    severity: str
    summary: str
    source_label: str
    code_path: str
    recommended_actions: list[dict]
    evidence: dict


def _severity(audit: dict) -> str:
    if audit["status"] == "mismatch":
        return "high"
    if audit["status"] == "unverified":
        return "medium"
    return "low"


def _actions(audit: dict) -> list[dict]:
    actions: list[dict] = []
    for operation in audit["operation_consistency"].get("missing_operations", []):
        actions.append({"kind": "fix_or_explain_missing_operation", "target": operation, "severity": "high"})
    for assumption in audit["assumption_diagnostic"].get("missing_assumptions", []):
        actions.append({"kind": "state_or_verify_assumption", "target": assumption["text"], "severity": "medium"})
    if audit["proof_audit"].get("status") in {"inconclusive", "unverified"}:
        actions.append({"kind": "review_unverified_derivation", "target": audit["proof_audit"].get("label"), "severity": "medium"})
    return actions


def build_likelihood_review_packet(doc_root: str, label: str, code_path: str, *, required_operations: list[str] | None = None, context_text: str = "") -> dict:
    audit = audit_likelihood_implementation(doc_root, label, code_path, required_operations=required_operations, context_text=context_text)
    severity = _severity(audit)
    summary = f"Likelihood audit for {label} is {audit['status']} with {severity} severity."
    packet = ReviewPacket(
        status=audit["status"],
        severity=severity,
        summary=summary,
        source_label=label,
        code_path=str(Path(code_path)),
        recommended_actions=_actions(audit),
        evidence=audit,
    )
    return attach_contract(asdict(packet), "review_packet", doc_context=audit.get("provenance"))
