from __future__ import annotations

import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys

from .contracts import attach_contract


def _git(root: Path, args: list[str]) -> str:
    try:
        completed = subprocess.run(["git", *args], cwd=root, check=False, capture_output=True, text=True, timeout=5)
    except Exception:
        return ""
    if completed.returncode != 0:
        return ""
    return completed.stdout.strip()


def release_evidence_metadata(root: str | Path, *, output_dir: str | Path | None = None, command_line: list[str] | None = None) -> dict:
    root_path = Path(root).resolve()
    package_version = "editable_or_uninstalled"
    try:
        package_version = importlib.metadata.version("mathdevmcp")
    except importlib.metadata.PackageNotFoundError:
        pass
    payload = {
        "root": str(root_path),
        "output_dir": str(Path(output_dir).resolve()) if output_dir else None,
        "git_commit": _git(root_path, ["rev-parse", "--short", "HEAD"]) or "unknown",
        "dirty_worktree": bool(_git(root_path, ["status", "--short"])),
        "package_version": package_version,
        "python_executable": sys.executable,
        "backend_conda_env": os.environ.get("MATHDEVMCP_BACKEND_CONDA_ENV", "mathdevmcp-backends"),
        "lean_toolchain": os.environ.get("MATHDEVMCP_LEAN_TOOLCHAIN", "leanprover/lean4:v4.20.0"),
        "command_line": command_line or [],
        "private_paths_redacted": True,
    }
    return attach_contract(payload, "release_evidence_metadata")
