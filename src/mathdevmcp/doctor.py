"""Runtime capability diagnostics for release and operator workflows."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import importlib.metadata
import importlib.util
import os
from pathlib import Path
import subprocess
import sys

from .backend_env import (
    backend_bin,
    backend_conda_env,
    backend_prefix,
    backend_python,
    backend_python_requested,
    backend_subprocess_env,
    run_backend_python,
)
from .contracts import contract_metadata
from .integration_versions import SUPPORTED_INTEGRATION_TOOLS, active_python_integration_status

REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Capability:
    name: str
    available: bool
    kind: str
    path: str | None
    version: str | None
    status: str
    detail: str
    environment_scope: str | None = None
    backend_requested: bool | None = None
    backend_env: str | None = None
    backend_prefix: str | None = None
    diagnostic_hint: str | None = None


@dataclass(frozen=True)
class DoctorReport:
    ok: bool
    python: dict
    capabilities: dict[str, dict]
    integrations: dict[str, dict]
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
    path = backend_bin(executable)
    if path is None and executable == "lean":
        elan_path = Path.home() / ".elan" / "bin" / "lean"
        if elan_path.exists():
            path = str(elan_path)
    if path is None:
        return Capability(name, False, "executable", None, None, "unavailable", f"{executable} was not found on PATH")
    version, detail = _run_version([path, *version_args], env=backend_subprocess_env())
    if detail != "available":
        return Capability(name, False, "executable", path, version, "unavailable", detail)
    return Capability(name, True, "executable", path, version, "available", detail)


def _local_integration_executable_path(name: str) -> str | None:
    if name == "jixia":
        candidate = REPO_ROOT / ".localresources" / "hypothesis_search_survey" / "code" / "jixia" / ".lake" / "build" / "bin" / "jixia"
        if candidate.exists():
            return str(candidate)
    return None


def _integration_executable_status(name: str) -> tuple[bool, str | None, str | None, str]:
    path = backend_bin(name) or _local_integration_executable_path(name)
    if path is None:
        return False, None, None, f"{name} executable was not found on PATH, backend bin, env override, or pinned local build path"
    if not Path(path).exists():
        return False, path, None, f"{name} executable path does not exist"
    if not os.access(path, os.X_OK):
        return False, path, None, f"{name} executable path is not executable"
    return True, path, None, "executable exists"


def _python_capability(name: str, module: str, package: str | None = None) -> Capability:
    requested = backend_python_requested()
    env_name = backend_conda_env()
    prefix = backend_prefix()
    prefix_text = str(prefix) if prefix is not None else None
    backend = run_backend_python(module, package=package)
    if backend[0]:
        return Capability(
            name,
            True,
            "python",
            backend_python(),
            backend[1],
            "available",
            backend[2],
            environment_scope="backend_python",
            backend_requested=requested,
            backend_env=env_name,
            backend_prefix=prefix_text,
        )
    if requested:
        return Capability(
            name,
            False,
            "python",
            backend_python(),
            None,
            "unavailable",
            backend[2],
            environment_scope="backend_python",
            backend_requested=True,
            backend_env=env_name,
            backend_prefix=prefix_text,
        )
    if importlib.util.find_spec(module) is None:
        hint = None
        if module == "lean_dojo":
            hint = (
                "LeanDojo is intentionally resolved through an isolated backend Python when available. "
                "Set MATHDEVMCP_BACKEND_CONDA_ENV=mathdevmcp-backends or run scripts/backend_env_doctor.sh to check it."
            )
        return Capability(
            name,
            False,
            "python",
            sys.executable,
            None,
            "unavailable",
            f"Python module {module} is not importable in active Python; no backend Python was selected.",
            environment_scope="active_python",
            backend_requested=False,
            backend_env=None,
            backend_prefix=None,
            diagnostic_hint=hint,
        )
    version = None
    try:
        version = importlib.metadata.version(package or module.replace("_", "-"))
    except importlib.metadata.PackageNotFoundError:
        version = "unknown"
    return Capability(
        name,
        True,
        "python",
        sys.executable,
        version,
        "available",
        f"Python module {module} imports in active Python; no backend Python was selected.",
        environment_scope="active_python",
        backend_requested=False,
        backend_env=None,
        backend_prefix=None,
    )


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


def _integration_statuses() -> dict[str, dict]:
    statuses = active_python_integration_status()
    for tool in SUPPORTED_INTEGRATION_TOOLS:
        if tool.kind == "lean_executable":
            available, path, version, detail = _integration_executable_status(tool.name)
            statuses[tool.name]["available"] = available
            statuses[tool.name]["path"] = path
            statuses[tool.name]["version"] = version
            statuses[tool.name]["version_status"] = "not_applicable"
            statuses[tool.name]["detail"] = detail
            continue
        if tool.module is None or tool.package is None:
            continue
        backend = run_backend_python(tool.module, package=tool.package)
        if not backend[0]:
            if backend_python_requested():
                statuses[tool.name]["backend_available"] = False
                statuses[tool.name]["backend_version"] = None
                statuses[tool.name]["backend_version_status"] = "missing"
                statuses[tool.name]["backend_detail"] = backend[2]
            continue
        statuses[tool.name]["backend_available"] = True
        statuses[tool.name]["backend_version"] = backend[1]
        statuses[tool.name]["backend_version_status"] = (
            "not_applicable"
            if tool.supported_version is None
            else "match"
            if backend[1] == tool.supported_version
            else "mismatch"
        )
        statuses[tool.name]["backend_detail"] = backend[2]
    for tool in SUPPORTED_INTEGRATION_TOOLS:
        status = statuses[tool.name]
        active_match = status.get("version_status") in {"match", "not_applicable"} and status.get("available") is True
        backend_match = status.get("backend_version_status") in {"match", "not_applicable"} and status.get("backend_available") is True
        if active_match and tool.kind == "lean_executable":
            status["resolved_available"] = True
            status["resolved_version"] = status.get("version")
            status["resolved_scope"] = "executable"
            status["resolved_version_status"] = status.get("version_status")
        elif backend_match and tool.kind in {"backend_python_package", "service_or_local_package"}:
            status["resolved_available"] = True
            status["resolved_version"] = status.get("backend_version")
            status["resolved_scope"] = "backend_python"
            status["resolved_version_status"] = status.get("backend_version_status")
        elif active_match:
            status["resolved_available"] = True
            status["resolved_version"] = status.get("version")
            status["resolved_scope"] = "active_python"
            status["resolved_version_status"] = status.get("version_status")
        elif backend_match:
            status["resolved_available"] = True
            status["resolved_version"] = status.get("backend_version")
            status["resolved_scope"] = "backend_python"
            status["resolved_version_status"] = status.get("backend_version_status")
        else:
            status["resolved_available"] = False
            status["resolved_version"] = status.get("backend_version") or status.get("version")
            status["resolved_scope"] = "unavailable"
            status["resolved_version_status"] = (
                status.get("backend_version_status")
                if status.get("backend_version_status") not in {None, "missing"}
                else status.get("version_status")
            )
    return statuses


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
        integrations=_integration_statuses(),
        conflicts=_pydantic_conflicts(),
        metadata=contract_metadata("doctor_report"),
    )
    return asdict(report)
