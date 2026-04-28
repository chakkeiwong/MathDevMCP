from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from .backend_env import backend_bin, backend_subprocess_env
from .contracts import attach_contract


@dataclass(frozen=True)
class LeanCheckResult:
    status: str
    reason: str
    evidence: list[dict]


_PLACEHOLDER_MARKERS = ("sorry", "admit")


def _lean_path() -> str | None:
    configured = backend_bin("lean")
    if configured is not None:
        return configured
    env_path = os.environ.get("PATH", "")
    elan_bin = str(Path.home() / ".elan" / "bin")
    path = f"{elan_bin}:{env_path}"
    return shutil.which("lean", path=path)


def _source_hash(source: str) -> str:
    return hashlib.sha256(source.encode("utf-8")).hexdigest()


def _uses_placeholder(source: str) -> bool:
    return any(marker in source for marker in _PLACEHOLDER_MARKERS)


def _lean_version(lean: str) -> str:
    try:
        completed = subprocess.run([lean, "--version"], check=False, capture_output=True, text=True, timeout=5, env=backend_subprocess_env())
    except Exception:
        return "unavailable"
    return (completed.stdout or completed.stderr).strip()


def _evidence(kind: str, *, command: list[str], source: str, uses_sorry: bool, lean_version: str, returncode: int | None = None, stdout: str = "", stderr: str = "", reason: str) -> dict:
    return {
        "kind": kind,
        "backend": "lean",
        "backend_status": kind.removeprefix("lean_"),
        "reason": reason,
        "command": command,
        "returncode": returncode,
        "stdout": stdout[-2000:],
        "stderr": stderr[-2000:],
        "uses_sorry": uses_sorry,
        "source_sha256": _source_hash(source),
        "lean_version": lean_version,
        "severity": "certifying" if kind == "lean_verified" else ("blocking" if kind == "lean_failed" else "diagnostic"),
    }


def check_lean_source(source: str, *, timeout_seconds: int = 10, allow_sorry: bool = False) -> dict:
    lean = _lean_path()
    uses_sorry = _uses_placeholder(source)
    if lean is None:
        evidence = _evidence(
            "lean_unavailable",
            command=["lean", "<tempfile>"],
            source=source,
            uses_sorry=uses_sorry,
            lean_version="unavailable",
            reason="Lean executable was not found.",
        )
        return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")

    version = _lean_version(lean)
    if uses_sorry and not allow_sorry:
        evidence = _evidence(
            "lean_placeholder",
            command=[lean, "<not-run>"],
            source=source,
            uses_sorry=True,
            lean_version=version,
            reason="Lean source contains a placeholder proof and certified mode disallows placeholders.",
        )
        return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")

    with tempfile.TemporaryDirectory(prefix="mathdevmcp-lean-") as tmp:
        lean_file = Path(tmp) / "Check.lean"
        lean_file.write_text(source, encoding="utf-8")
        command = [lean, str(lean_file)]
        try:
            completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=timeout_seconds, env=backend_subprocess_env())
        except FileNotFoundError:
            evidence = _evidence(
                "lean_unavailable",
                command=command,
                source=source,
                uses_sorry=uses_sorry,
                lean_version=version,
                reason="Lean executable was not found.",
            )
            return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")
        except subprocess.TimeoutExpired:
            evidence = _evidence(
                "lean_timeout",
                command=command,
                source=source,
                uses_sorry=uses_sorry,
                lean_version=version,
                reason=f"Lean check timed out after {timeout_seconds} seconds.",
            )
            return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")

    if completed.returncode == 0 and not uses_sorry:
        evidence = _evidence(
            "lean_verified",
            command=command,
            source=source,
            uses_sorry=False,
            lean_version=version,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            reason="Lean accepted the source without placeholder proofs.",
        )
        return attach_contract(asdict(LeanCheckResult("verified", evidence["reason"], [evidence])), "lean_check_result")
    if completed.returncode == 0 and uses_sorry:
        evidence = _evidence(
            "lean_placeholder",
            command=command,
            source=source,
            uses_sorry=True,
            lean_version=version,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            reason="Lean accepted the source, but the proof uses a placeholder.",
        )
        return attach_contract(asdict(LeanCheckResult("inconclusive", evidence["reason"], [evidence])), "lean_check_result")
    evidence = _evidence(
        "lean_failed",
        command=command,
        source=source,
        uses_sorry=uses_sorry,
        lean_version=version,
        returncode=completed.returncode,
        stdout=completed.stdout,
        stderr=completed.stderr,
        reason="Lean rejected the supplied proof artifact.",
    )
    return attach_contract(asdict(LeanCheckResult("mismatch", evidence["reason"], [evidence])), "lean_check_result")
