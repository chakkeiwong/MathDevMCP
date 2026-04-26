from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract
from .parser_benchmark import compare_parser_backends


@dataclass(frozen=True)
class ParserPolicyDecision:
    status: str
    reason: str
    selected_backend: str | None
    blocking_findings: list[dict]
    benchmark_report: dict


def decide_parser_policy(root: str, *, backends: list[str] | None = None) -> dict:
    report = compare_parser_backends(root, backends=backends or ["current", "latexml", "pandoc"])
    blocking: list[dict] = []
    current = next((item for item in report["results"] if item["backend"] == "current"), None)
    if current and current["quality_checks"]["label_preservation"] and current["quality_checks"]["provenance_available"]:
        selected = "current"
        status = "selected"
        reason = "Current parser preserves expected labels and line provenance for this corpus."
    else:
        selected = None
        status = "blocked"
        reason = "No parser backend preserved required labels and provenance for proof-audit routing."
    for result in report["results"]:
        if not result["quality_checks"]["label_preservation"]:
            blocking.append({"backend": result["backend"], "kind": "missing_expected_labels", "missing": result["details"].get("missing_expected_labels", [])})
        if not result["quality_checks"]["provenance_available"]:
            blocking.append({"backend": result["backend"], "kind": "provenance_unavailable"})
    decision = ParserPolicyDecision(status, reason, selected, blocking, report)
    return attach_contract(asdict(decision), "parser_policy_decision")
