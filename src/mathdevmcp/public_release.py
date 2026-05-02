"""Public release surface checks.

These checks deliberately inspect product-surface files and contracts rather
than mathematical correctness. They answer whether the public package boundary
is coherent enough to claim public release readiness.
"""

from __future__ import annotations

import ast
import tomllib
from pathlib import Path
from typing import Any

from .contracts import attach_contract
from .mcp_facade import MCP_TOOL_SPECS
from .release_policy import RELEASE_PROFILES


PUBLIC_RELEASE_CHECK_VERSION = "2026-04-public-surface"


def public_release_check(root: str | Path) -> dict[str, Any]:
    """Return a structured public product-surface readiness report."""
    root_path = Path(root)
    checks = [
        _check_ci_workflow(root_path),
        _check_packaging_metadata(root_path),
        _check_mcp_surface(root_path),
        _check_support_matrix(root_path),
        _check_docs_release_boundary(root_path),
        _check_quality_gate(root_path),
        _check_private_path_leaks(root_path),
    ]
    blockers = [finding for check in checks for finding in check["findings"] if finding["severity"] == "high"]
    caveats = [finding for check in checks for finding in check["findings"] if finding["severity"] != "high"]
    status = "consistent" if not blockers else "mismatch"
    reason = "Public release surface checks passed." if status == "consistent" else "Public release surface checks have blockers."
    return attach_contract(
        {
            "status": status,
            "reason": reason,
            "check_version": PUBLIC_RELEASE_CHECK_VERSION,
            "checks": checks,
            "blockers": blockers,
            "caveats": caveats,
        },
        "public_release_check",
    )


def public_release_blockers(root: str | Path) -> list[dict[str, Any]]:
    report = public_release_check(root)
    return [
        {
            "kind": finding["kind"],
            "severity": "high",
            "detail": finding.get("detail", finding.get("path", "")),
            "check": finding.get("check"),
        }
        for finding in report["blockers"]
    ]


def _check_ci_workflow(root: Path) -> dict[str, Any]:
    path = root / ".github" / "workflows" / "ci.yml"
    findings: list[dict[str, Any]] = []
    if not path.exists():
        findings.append({"check": "ci_workflow", "severity": "high", "kind": "ci_release_gate_missing", "path": str(path)})
    else:
        text = path.read_text(encoding="utf-8")
        required_markers = ["pytest", "release_smoke.sh", "release_matrix.sh", "audit_release_report_substance.sh", "public-release-check", "release-hypothesis-check"]
        for marker in required_markers:
            if marker not in text:
                findings.append({"check": "ci_workflow", "severity": "high", "kind": "ci_required_command_missing", "detail": marker})
    return _check_result("ci_workflow", findings)


def _check_packaging_metadata(root: Path) -> dict[str, Any]:
    path = root / "pyproject.toml"
    findings: list[dict[str, Any]] = []
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    project = data.get("project", {})
    optional = project.get("optional-dependencies", {})
    for field in ["name", "version", "description", "requires-python"]:
        if not project.get(field):
            findings.append({"check": "packaging_metadata", "severity": "high", "kind": "packaging_metadata_missing", "detail": field})
    if project.get("dependencies", []) != []:
        findings.append({"check": "packaging_metadata", "severity": "high", "kind": "base_dependencies_not_lightweight", "detail": ", ".join(project.get("dependencies", []))})
    for group in ["dev", "mcp", "symbolic", "leandojo", "all", "quality"]:
        if group not in optional:
            findings.append({"check": "packaging_metadata", "severity": "high", "kind": "optional_dependency_group_missing", "detail": group})
    if "mcp" not in optional.get("mcp", []):
        findings.append({"check": "packaging_metadata", "severity": "high", "kind": "mcp_extra_missing_runtime_dependency"})
    if "license" not in project:
        findings.append({"check": "packaging_metadata", "severity": "medium", "kind": "license_metadata_missing"})
    return _check_result("packaging_metadata", findings)


def _check_mcp_surface(root: Path) -> dict[str, Any]:
    readme = root / "mcp" / "README.md"
    text = readme.read_text(encoding="utf-8") if readme.exists() else ""
    findings: list[dict[str, Any]] = []
    registry_names = {spec.name for spec in MCP_TOOL_SPECS}
    server_names = {spec.exposed_server_name for spec in MCP_TOOL_SPECS}
    missing_server = sorted(server_names - _server_exposed_tools(root))
    if missing_server:
        findings.append({"check": "mcp_surface", "severity": "high", "kind": "mcp_server_exposure_missing", "detail": ", ".join(missing_server)})
    for name in sorted(registry_names | server_names):
        if f"`{name}`" not in text:
            findings.append({"check": "mcp_surface", "severity": "high", "kind": "mcp_readme_tool_missing", "detail": name})
    if "/home/chakwong" in text:
        findings.append({"check": "mcp_surface", "severity": "high", "kind": "mcp_readme_local_path"})
    return _check_result("mcp_surface", findings)


def _server_exposed_tools(root: Path) -> set[str]:
    """Read server exposure without importing the optional `mcp` package."""
    path = root / "src" / "mathdevmcp" / "mcp_server.py"
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except OSError:
        return set()
    names: set[str] = set()
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            for decorator in node.decorator_list:
                if (
                    isinstance(decorator, ast.Call)
                    and isinstance(decorator.func, ast.Attribute)
                    and decorator.func.attr == "tool"
                ):
                    names.add(node.name)
    return names


def _check_support_matrix(root: Path) -> dict[str, Any]:
    path = root / "docs" / "mathdevmcp-support-matrix.md"
    findings: list[dict[str, Any]] = []
    if not path.exists():
        findings.append({"check": "support_matrix", "severity": "high", "kind": "support_matrix_missing", "path": str(path)})
        return _check_result("support_matrix", findings)
    text = path.read_text(encoding="utf-8")
    for profile in sorted(RELEASE_PROFILES):
        if profile not in text:
            findings.append({"check": "support_matrix", "severity": "high", "kind": "support_matrix_profile_missing", "detail": profile})
    for marker in ["base", "MCP", "symbolic", "LeanDojo", "LaTeXML", "private corpus", "public"]:
        if marker not in text:
            findings.append({"check": "support_matrix", "severity": "medium", "kind": "support_matrix_topic_missing", "detail": marker})
    return _check_result("support_matrix", findings)


def _check_docs_release_boundary(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    docs = [
        root / "README.md",
        root / "docs" / "mathdevmcp-release-policy.md",
        root / "docs" / "mathdevmcp-maintainer-guide.md",
        root / "docs" / "mathdevmcp-deployment-guide.md",
    ]
    for path in docs:
        text = path.read_text(encoding="utf-8")
        if "public industrial release" not in text:
            findings.append({"check": "docs_release_boundary", "severity": "high", "kind": "public_release_boundary_missing", "path": str(path.relative_to(root))})
    return _check_result("docs_release_boundary", findings)


def _check_quality_gate(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    script = root / "scripts" / "quality_gate.sh"
    if not script.exists():
        findings.append({"check": "quality_gate", "severity": "high", "kind": "quality_gate_missing", "path": str(script)})
    for directory in [root / "src", root / "tests"]:
        for path in directory.rglob("*.py"):
            try:
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            except SyntaxError as exc:
                findings.append({"check": "quality_gate", "severity": "high", "kind": "python_syntax_error", "path": str(path.relative_to(root)), "detail": str(exc)})
    return _check_result("quality_gate", findings)


def _check_private_path_leaks(root: Path) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    evidence_dir = root / "docs" / "generated" / "release_report"
    banned = ["/tmp/mathdevmcp", "/home/chakwong", "manifest.json"]
    if evidence_dir.exists():
        for path in evidence_dir.glob("*.txt"):
            text = path.read_text(encoding="utf-8")
            for marker in banned:
                if marker in text:
                    findings.append({"check": "private_path_leaks", "severity": "high", "kind": "generated_evidence_path_leak", "path": str(path.relative_to(root)), "detail": marker})
    return _check_result("private_path_leaks", findings)


def _check_result(name: str, findings: list[dict[str, Any]]) -> dict[str, Any]:
    status = "consistent" if not any(item["severity"] == "high" for item in findings) else "mismatch"
    return {"name": name, "status": status, "findings": findings}
