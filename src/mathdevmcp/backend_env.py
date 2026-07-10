"""Backend environment discovery for optional mathematical tools.

The base MathDevMCP package must import in ordinary Python environments.
LeanDojo and similar heavy dependencies are resolved through explicit backend
environment variables so dependency conflicts stay out of the main workflow.
"""

from __future__ import annotations

import os
from pathlib import Path
import shutil
import subprocess


BACKEND_ENV_VAR = "MATHDEVMCP_BACKEND_CONDA_ENV"
BACKEND_PREFIX_VAR = "MATHDEVMCP_BACKEND_PREFIX"
BACKEND_PYTHON_VAR = "MATHDEVMCP_BACKEND_PYTHON"
LEAN_TOOLCHAIN_VAR = "MATHDEVMCP_LEAN_TOOLCHAIN"
DEFAULT_BACKEND_CONDA_ENV = "mathdevmcp-backends"


def backend_conda_env() -> str | None:
    value = os.environ.get(BACKEND_ENV_VAR, "").strip()
    return value or None


def backend_python_requested() -> bool:
    return any(os.environ.get(name, "").strip() for name in (BACKEND_ENV_VAR, BACKEND_PREFIX_VAR, BACKEND_PYTHON_VAR))


def backend_prefix() -> Path | None:
    explicit = os.environ.get(BACKEND_PREFIX_VAR, "").strip()
    if explicit:
        return Path(explicit)
    env_name = backend_conda_env()
    if not env_name:
        return None
    conda = shutil.which("conda")
    if conda is None:
        return None
    try:
        completed = subprocess.run(
            [conda, "env", "list"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception:
        return None
    if completed.returncode != 0:
        return None
    for line in completed.stdout.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        parts = stripped.replace("*", " ").split()
        if len(parts) >= 2 and parts[0] == env_name:
            return Path(parts[-1])
    return None


def backend_bin(executable: str) -> str | None:
    override = os.environ.get(f"MATHDEVMCP_{executable.upper()}_PATH", "").strip()
    if override:
        return override
    prefix = backend_prefix()
    if prefix is not None:
        candidate = prefix / "bin" / executable
        if candidate.exists():
            return str(candidate)
    if executable == "lean":
        elan_lean = Path.home() / ".elan" / "bin" / "lean"
        if elan_lean.exists():
            return str(elan_lean)
    return shutil.which(executable)


def backend_subprocess_env() -> dict[str, str]:
    env = os.environ.copy()
    prefix = backend_prefix()
    if prefix is not None:
        env["PATH"] = f"{prefix / 'bin'}{os.pathsep}{env.get('PATH', '')}"
    lean_toolchain = env.get(LEAN_TOOLCHAIN_VAR, "").strip()
    if lean_toolchain:
        env["ELAN_TOOLCHAIN"] = lean_toolchain
    return env


def backend_python() -> str | None:
    override = os.environ.get(BACKEND_PYTHON_VAR, "").strip()
    if override:
        return override
    prefix = backend_prefix()
    if prefix is not None:
        candidate = prefix / "bin" / "python"
        if candidate.exists():
            return str(candidate)
    return None


def run_backend_python(module: str, *, package: str | None = None, timeout: int = 10) -> tuple[bool, str | None, str]:
    python = backend_python()
    if python is None:
        return False, None, "No backend Python interpreter is configured."
    code = (
        "import importlib.metadata, importlib.util, sys; "
        f"module={module!r}; package={package or module.replace('_', '-')!r}; "
        "spec=importlib.util.find_spec(module); "
        "sys.exit(2) if spec is None else None; "
        "print(importlib.metadata.version(package))"
    )
    try:
        completed = subprocess.run([python, "-c", code], check=False, capture_output=True, text=True, timeout=timeout)
    except Exception as exc:
        return False, None, f"backend Python check failed: {exc}"
    output = (completed.stdout or completed.stderr).strip()
    if completed.returncode == 0:
        return True, output.splitlines()[0] if output else "unknown", f"Python module {module} imports in backend env"
    if completed.returncode == 2:
        return False, None, f"Python module {module} is not importable in backend env"
    return False, None, f"backend Python check exited with {completed.returncode}: {output.splitlines()[0] if output else ''}"
