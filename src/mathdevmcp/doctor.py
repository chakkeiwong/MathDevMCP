from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.metadata
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys

from .contracts import contract_metadata


@dataclass(frozen=True)
class Capability:
    name: str
    available: bool
    kind: str
    path: str | None
    version: str | None
    status: str
    detail: str


@dataclass(frozen=True)
class DoctorReport:
    ok: bool
    python: dict
    capabilities: dict[str, dict]
    conflicts: list[str]
    metadata: dict[str, str]


def _run_version(command: list[str], *, env: dict[str, str] | None = None, timeout: int = 10) -> tuple[str | None, str]:
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=timeout, env=env)
    except Exception as exc:
        return None, f"version check failed: {exc}"
    output = (completed.stdout or completed.stderr).strip()
    first_line = output.splitlines()[0] if output else ""
    if completed.returncode != 0:
        return first_line or None, f"version command exited with {completed.returncode}"
    return first_line or None, "available"


def _executable_capability(name: str, executable: str, version_args: list[str]) -> Capability:
    path = shutil.which(executable)
    if path is None and executable == "lean":
        elan_path = Path.home() / ".elan" / "bin" / "lean"
        if elan_path.exists():
            path = str(elan_path)
    if path is None:
        return Capability(name, False, "executable", None, None, "unavailable", f"{executable} was not found on PATH")
    version, detail = _run_version([path, *version_args])
    return Capability(name, True, "executable", path, version, "available", detail)


def _python_capability(name: str, module: str, package: str | None = None) -> Capability:
    if importlib.util.find_spec(module) is None:
        return Capability(name, False, "python", None, None, "unavailable", f"Python module {module} is not importable")
    version = None
    try:
        version = importlib.metadata.version(package or module.replace("_", "-"))
    except importlib.metadata.PackageNotFoundError:
        version = "unknown"
    return Capability(name, True, "python", sys.executable, version, "available", f"Python module {module} imports")


def _pydantic_conflicts() -> list[str]:
    conflicts: list[str] = []
    try:
        pydantic_version = importlib.metadata.version("pydantic")
    except importlib.metadata.PackageNotFoundError:
        return conflicts
    try:
        magic_pdf_version = importlib.metadata.version("magic-pdf")
    except importlib.metadata.PackageNotFoundError:
        return conflicts
    major_minor = tuple(int(part) for part in pydantic_version.split(".")[:2])
    if major_minor >= (2, 11):
        conflicts.append(
            f"magic-pdf {magic_pdf_version} declares pydantic<2.11, but active pydantic is {pydantic_version}; use a separate LeanDojo env if this matters."
        )
    return conflicts


def doctor_report() -> dict:
    capabilities = [
        _executable_capability("latexml", "latexml", ["--VERSION"]),
        _executable_capability("pandoc", "pandoc", ["--version"]),
        _executable_capability("lean", "lean", ["--version"]),
        _executable_capability("sage", "sage", ["--version"]),
        _python_capability("lean_dojo", "lean_dojo", "lean-dojo"),
        _python_capability("sympy", "sympy", "sympy"),
    ]
    python_info = {
        "executable": sys.executable,
        "version": sys.version.split()[0],
        "prefix": sys.prefix,
        "path_head": os.environ.get("PATH", "").split(os.pathsep)[:5],
    }
    report = DoctorReport(
        ok=True,
        python=python_info,
        capabilities={capability.name: asdict(capability) for capability in capabilities},
        conflicts=_pydantic_conflicts(),
        metadata=contract_metadata("doctor_report"),
    )
    return asdict(report)
