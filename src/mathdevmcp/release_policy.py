from __future__ import annotations

import importlib.metadata
import subprocess
from pathlib import Path

from .contracts import attach_contract
from .doctor import doctor_report
from .governance import governance_policy
from .parser_policy import decide_parser_policy


def release_readiness_report(root: str | Path) -> dict:
    from .benchmarks import benchmark_gate_report

    root_path = Path(root)
    gate = benchmark_gate_report(root_path, include_release_policy=False)
    doctor = doctor_report()
    parser = decide_parser_policy(str(root_path / "benchmarks" / "fixtures"), backends=["current"])
    governance = governance_policy()
    dirty = bool(_git(root_path, ["status", "--short"]).strip())
    commit = _git(root_path, ["rev-parse", "--short", "HEAD"]).strip() or "unknown"
    blockers: list[dict] = []
    caveats: list[dict] = []
    if not gate["passed"]:
        blockers.append({"kind": "benchmark_gate_failed", "severity": "high"})
    if parser.get("status") not in {"selected", "selected_for_proof_audit"}:
        blockers.append({"kind": "parser_policy_not_selected_for_proof_audit", "severity": "high"})
    if dirty:
        caveats.append({"kind": "dirty_worktree", "severity": "medium"})
    lean = doctor["capabilities"].get("lean", {})
    if lean.get("detail") != "available":
        caveats.append({"kind": "lean_version_or_toolchain_caveat", "severity": "medium", "detail": lean.get("detail"), "version": lean.get("version")})
    if doctor.get("conflicts"):
        caveats.append({"kind": "dependency_conflicts", "severity": "medium", "conflicts": doctor["conflicts"]})
    if blockers:
        recommendation = "not_ready"
        reason = "Release readiness has blocking findings."
    elif caveats:
        recommendation = "ready_with_caveats"
        reason = "Release gates passed with documented caveats."
    else:
        recommendation = "ready"
        reason = "Release gates passed without detected caveats."
    return attach_contract(
        {
            "status": recommendation,
            "reason": reason,
            "package_version": _package_version(),
            "git_commit": commit,
            "dirty_worktree": dirty,
            "benchmark_gate": gate,
            "doctor_summary": doctor,
            "parser_policy": parser,
            "governance_policy": governance,
            "schema_version": "1.0",
            "blockers": blockers,
            "caveats": caveats,
        },
        "release_readiness_report",
    )


def _git(root: Path, args: list[str]) -> str:
    try:
        completed = subprocess.run(["git", *args], cwd=root, check=False, capture_output=True, text=True, timeout=5)
    except Exception:
        return ""
    if completed.returncode != 0:
        return ""
    return completed.stdout


def _package_version() -> str:
    try:
        return importlib.metadata.version("mathdevmcp")
    except importlib.metadata.PackageNotFoundError:
        return "editable_or_uninstalled"
