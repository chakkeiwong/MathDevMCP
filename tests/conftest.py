"""Shared pytest fixtures for environment-dependent tests.

The MathDevMCP server and CLI degrade to `severity: diagnostic` abstention
when optional backends (pandoc, sympy, Lean, LaTeXML, lean-dojo) are absent
— that's the runtime contract guarded by `governance.verified_claim_policy`.
The test suite mirrors this: tests that exercise a specific backend skip
cleanly with a clear reason when the backend isn't installed, instead of
failing and obscuring the real signal.

Use the fixtures by adding them to a test's parameters:

    def test_foo(requires_pandoc):
        ...

The fixture body runs before the test, calls `pytest.skip` if the dep is
missing, and otherwise returns silently.
"""

from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

from mathdevmcp.backend_env import backend_bin, run_backend_python


def _pandoc_available() -> bool:
    return shutil.which("pandoc") is not None


def _lean_available() -> bool:
    configured = backend_bin("lean")
    if configured is not None:
        return True
    env_path = os.environ.get("PATH", "")
    elan_bin = str(Path.home() / ".elan" / "bin")
    return shutil.which("lean", path=f"{elan_bin}:{env_path}") is not None


def _backend_has_lean_dojo() -> bool:
    # Mirror release_policy._run_backend_python_with_default_env: when the
    # caller hasn't picked a backend conda env, the policy defaults to
    # "mathdevmcp-backends". Match that here so the skip predicate aligns
    # with what the release-readiness gate would actually observe.
    previous = os.environ.get("MATHDEVMCP_BACKEND_CONDA_ENV")
    if not previous:
        os.environ["MATHDEVMCP_BACKEND_CONDA_ENV"] = "mathdevmcp-backends"
    try:
        ok, _version, _detail = run_backend_python("lean_dojo", package="lean-dojo")
        return ok
    finally:
        if previous is None:
            os.environ.pop("MATHDEVMCP_BACKEND_CONDA_ENV", None)
        else:
            os.environ["MATHDEVMCP_BACKEND_CONDA_ENV"] = previous


@pytest.fixture
def requires_pandoc() -> None:
    if not _pandoc_available():
        pytest.skip("pandoc not on PATH; install via your system package manager")


@pytest.fixture
def requires_lean() -> None:
    if not _lean_available():
        pytest.skip(
            "Lean toolchain not installed (no `lean` on PATH or under ~/.elan/bin); "
            "see scripts/setup_backend_env.sh"
        )


@pytest.fixture
def requires_backend_lean_dojo() -> None:
    if not _backend_has_lean_dojo():
        pytest.skip(
            "lean-dojo not importable in MATHDEVMCP_BACKEND_CONDA_ENV "
            "(default: mathdevmcp-backends); run scripts/setup_backend_env.sh"
        )
