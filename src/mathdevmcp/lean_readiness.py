"""Offline-friendly Lean, Lake, and LeanDojo readiness diagnostics."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess

from .contracts import attach_contract
from .doctor import doctor_report
from .lean_check import check_lean_source


def _toolchain_file(root: str | Path | None) -> dict:
    if root is None:
        return {"path": None, "exists": False, "toolchain": None}
    path = Path(root) / "lean-toolchain"
    if not path.exists():
        return {"path": str(path), "exists": False, "toolchain": None}
    return {"path": str(path), "exists": True, "toolchain": path.read_text(encoding="utf-8").strip()}


def _version(path: str | None) -> dict:
    if path is None:
        return {"status": "unavailable", "version": None, "reason": "Executable not found."}
    try:
        result = subprocess.run([path, "--version"], check=False, capture_output=True, text=True, timeout=5)
    except subprocess.TimeoutExpired:
        return {"status": "inconclusive", "version": None, "reason": "Version check timed out."}
    except Exception as exc:
        return {"status": "inconclusive", "version": None, "reason": f"Version check failed: {exc.__class__.__name__}."}
    output = (result.stdout or result.stderr).strip().splitlines()
    return {"status": "available" if result.returncode == 0 else "inconclusive", "version": output[0] if output else None, "reason": "Version check completed."}


def lean_readiness(root: str | Path | None = None) -> dict:
    doctor = doctor_report()
    lean_cap = doctor.get("capabilities", {}).get("lean", {})
    lean_path = lean_cap.get("path") or shutil.which("lean")
    lake_path = shutil.which("lake")
    lean_version = _version(lean_path)
    tiny_check = (
        check_lean_source("theorem mathdevmcp_tiny : 1 = 1 := rfl\n", timeout_seconds=5)
        if lean_version.get("status") == "available"
        else {"status": "inconclusive", "reason": "Lean executable is unavailable."}
    )
    direct_status = "available" if tiny_check.get("status") == "verified" else "inconclusive"
    lake_version = _version(lake_path)
    leandojo = doctor.get("capabilities", {}).get("lean_dojo", {})
    result = {
        "status": "ready_with_caveats" if direct_status == "available" else "inconclusive",
        "reason": "Lean readiness diagnostics completed.",
        "direct_lean": {
            "status": direct_status,
            "path": lean_path,
            "version": lean_version,
            "tiny_theorem_check": tiny_check,
        },
        "lake_project": {
            "status": "available" if lake_version.get("status") == "available" else "inconclusive",
            "path": lake_path,
            "version": lake_version,
            "toolchain_file": _toolchain_file(root),
        },
        "lean_dojo": {
            "status": "available" if leandojo.get("available") else "unavailable",
            "path": leandojo.get("path"),
            "detail": leandojo.get("detail"),
        },
        "certification_boundary": "Readiness diagnostics are not proof; only successful Lean checking of supplied source can certify a scoped Lean artifact.",
    }
    return attach_contract(result, "lean_readiness")
