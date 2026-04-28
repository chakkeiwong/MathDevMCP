from __future__ import annotations

import ast
from pathlib import Path

from .contracts import attach_contract
from .release_corpus import validate_release_corpus_manifest


def governance_policy() -> dict:
    policy = {
        "external_command_policy": {
            "allowlist": ["latexml", "pandoc", "lean", "lake", "sage"],
            "timeout_required": True,
            "structured_failure_required": True,
            "network_requires_explicit_configuration": True,
        },
        "release_dependency_policy": {
            "latexml": "optional_measured_backend",
            "pandoc": "required_for_release_candidate",
            "lean": "required_for_direct_checking",
            "lean_dojo": "optional_proof_search_boundary",
            "sage": "required_when_symbolic_sage_routes_are_enabled",
        },
        "private_corpus_policy": {
            "no_private_documents_in_git": True,
            "commit_only_manifest_stubs": True,
            "no_exfiltration": "Private source documents and code should not be sent to external services by MathDevMCP workflows.",
        },
        "artifact_policy": {
            "generated_lean_skeletons_are_not_certificates": True,
            "numeric_diagnostics_require_safe_artifacts": True,
            "retain_benchmark_and_doctor_outputs_for_release_reviews": True,
        },
        "verified_claim_policy": {
            "requires_deterministic_backend_evidence": True,
            "diagnostic_evidence_is_not_proof": True,
            "expected_abstention_is_quality_signal": True,
        },
    }
    return attach_contract({"status": "consistent", "reason": "Governance policy is available for release review.", "policy": policy}, "governance_policy")


_SUBPROCESS_CALLS = {"run", "call", "check_call", "check_output", "Popen"}


def _subprocess_call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name) and node.value.id == "subprocess":
        if node.attr in _SUBPROCESS_CALLS:
            return f"subprocess.{node.attr}"
    return None


def scan_subprocess_timeout_policy(root: str | Path) -> dict:
    root_path = Path(root)
    src_root = root_path / "src" / "mathdevmcp"
    findings: list[dict] = []
    for path in sorted(src_root.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError as exc:
            findings.append({"kind": "source_parse_failed", "severity": "high", "file": str(path.relative_to(root_path)), "line": exc.lineno})
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            call_name = _subprocess_call_name(node.func)
            if call_name is None:
                continue
            has_timeout = any(keyword.arg == "timeout" for keyword in node.keywords)
            if not has_timeout:
                findings.append(
                    {
                        "kind": "subprocess_timeout_missing",
                        "severity": "high",
                        "file": str(path.relative_to(root_path)),
                        "line": getattr(node, "lineno", 0),
                        "call": call_name,
                    }
                )
    status = "consistent" if not findings else "mismatch"
    reason = "All MathDevMCP subprocess calls include explicit timeouts." if status == "consistent" else "At least one subprocess call is missing a timeout."
    return attach_contract({"status": status, "reason": reason, "findings": findings}, "subprocess_timeout_policy_report")


def validate_governance(root: str | Path | None = None) -> dict:
    policy_report = governance_policy()
    root_path = Path(root) if root is not None else None
    corpus_report = validate_release_corpus_manifest(root_path / "benchmarks" / "fixtures" if root_path is not None else None)
    subprocess_report = scan_subprocess_timeout_policy(root_path) if root_path is not None else {"status": "not_run", "findings": []}
    findings: list[dict] = []
    policy = policy_report["policy"]
    command_policy = policy["external_command_policy"]
    if not command_policy.get("timeout_required"):
        findings.append({"kind": "external_command_timeout_policy_disabled", "severity": "high"})
    if not command_policy.get("structured_failure_required"):
        findings.append({"kind": "structured_failure_policy_disabled", "severity": "high"})
    for command in {"latexml", "pandoc", "lean", "lake", "sage"} - set(command_policy.get("allowlist", [])):
        findings.append({"kind": "external_command_missing_from_allowlist", "severity": "high", "command": command})
    if not policy["private_corpus_policy"].get("no_private_documents_in_git"):
        findings.append({"kind": "private_corpus_git_policy_disabled", "severity": "high"})
    for finding in corpus_report.get("findings", []):
        findings.append({"kind": "release_corpus_" + finding["kind"], "severity": finding["severity"], "entry": finding.get("entry")})
    for finding in subprocess_report.get("findings", []):
        findings.append({"kind": finding["kind"], "severity": finding["severity"], "file": finding.get("file"), "line": finding.get("line")})
    status = "consistent" if not any(finding["severity"] == "high" for finding in findings) else "mismatch"
    reason = "Governance checks passed." if status == "consistent" else "Governance checks found blocking issues."
    return attach_contract(
        {
            "status": status,
            "reason": reason,
            "findings": findings,
            "policy": policy_report,
            "release_corpus_validation": corpus_report,
            "subprocess_timeout_validation": subprocess_report,
        },
        "governance_validation_report",
    )
