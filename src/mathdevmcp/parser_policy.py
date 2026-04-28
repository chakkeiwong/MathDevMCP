from __future__ import annotations

from dataclasses import asdict, dataclass
from collections.abc import Iterable

from .contracts import attach_contract
from .parser_benchmark import compare_parser_backends


@dataclass(frozen=True)
class ParserPolicyDecision:
    status: str
    reason: str
    selected_backend: str | None
    blocking_findings: list[dict]
    caveats: list[dict]
    backend_roles: list[dict]
    benchmark_report: dict


def decide_parser_policy(root: str, *, backends: list[str] | None = None, expected_labels: Iterable[str] | None = None) -> dict:
    report = compare_parser_backends(root, backends=backends or ["current", "latexml", "pandoc"], expected_labels=expected_labels)
    blocking: list[dict] = []
    caveats: list[dict] = []
    backend_roles: list[dict] = []
    current = next((item for item in report["results"] if item["backend"] == "current"), None)
    if current and current["quality_checks"]["label_preservation"] and current["quality_checks"]["provenance_available"]:
        selected = "current"
        status = "selected_for_proof_audit"
        reason = "Current parser preserves expected labels and line provenance for this corpus."
    elif current and current["quality_checks"]["provenance_available"]:
        selected = "current"
        status = "selected_for_context_only"
        reason = "Current parser has provenance, but expected label preservation is incomplete; certification should remain blocked."
    else:
        selected = None
        status = "blocked"
        reason = "No parser backend preserved required labels and provenance for proof-audit routing."
    if current is None:
        blocking.append({"backend": "current", "kind": "selected_parser_not_measured"})
    for result in report["results"]:
        backend = result["backend"]
        if backend == selected and status == "selected_for_proof_audit":
            role = "selected_for_proof_audit"
        elif backend == selected and status == "selected_for_context_only":
            role = "selected_for_context_only"
        elif backend == "current":
            role = "blocked"
        else:
            role = "measured_optional"
        backend_roles.append({"backend": backend, "role": role, "status": result["status"]})
        finding_target = blocking if backend == "current" else caveats
        severity = "high" if backend == "current" else "medium"
        if not result["quality_checks"]["label_preservation"]:
            finding_target.append(
                {
                    "backend": backend,
                    "kind": "missing_expected_labels",
                    "missing": result["details"].get("missing_expected_labels", []),
                    "severity": severity,
                }
            )
        if not result["quality_checks"]["provenance_available"]:
            finding_target.append({"backend": backend, "kind": "provenance_unavailable", "severity": severity})
    decision = ParserPolicyDecision(status, reason, selected, blocking, caveats, backend_roles, report)
    payload = attach_contract(asdict(decision), "parser_policy_decision")
    payload["legacy_status"] = "selected" if status == "selected_for_proof_audit" else status
    return payload
