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
_IDENTIFIER_CHARS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'.")


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
    """Detect Lean placeholder tokens outside comments, strings, and identifiers.

    This is a conservative scanner, not a full Lean lexer. Its job is to avoid
    obvious false positives such as comments and identifiers while preserving
    the safety rule that actual `sorry`/`admit` tokens cannot certify a proof.
    """
    index = 0
    length = len(source)
    block_comment_depth = 0
    in_string = False
    while index < length:
        current = source[index]
        nxt = source[index + 1] if index + 1 < length else ""

        if block_comment_depth:
            if current == "/" and nxt == "-":
                block_comment_depth += 1
                index += 2
                continue
            if current == "-" and nxt == "/":
                block_comment_depth -= 1
                index += 2
                continue
            index += 1
            continue

        if in_string:
            if current == "\\":
                index += 2
                continue
            if current == '"':
                in_string = False
            index += 1
            continue

        if current == "-" and nxt == "-":
            newline = source.find("\n", index + 2)
            if newline == -1:
                break
            index = newline + 1
            continue
        if current == "/" and nxt == "-":
            block_comment_depth = 1
            index += 2
            continue
        if current == '"':
            in_string = True
            index += 1
            continue

        for marker in _PLACEHOLDER_MARKERS:
            if source.startswith(marker, index):
                before = source[index - 1] if index > 0 else ""
                after_index = index + len(marker)
                after = source[after_index] if after_index < length else ""
                if before not in _IDENTIFIER_CHARS and after not in _IDENTIFIER_CHARS:
                    return True
        index += 1
    return False


def _lean_version(lean: str) -> str:
    try:
        completed = subprocess.run([lean, "--version"], check=False, capture_output=True, text=True, timeout=5, env=backend_subprocess_env())
    except Exception:
        return "unavailable"
    return (completed.stdout or completed.stderr).strip()


def _lean_environment_failure(output: str) -> bool:
    lowered = output.lower()
    markers = (
        "error during download",
        "could not resolve host",
        "could not resolve hostname",
        "connection refused",
        "failed to download",
        "toolchain",
    )
    return any(marker in lowered for marker in markers)


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
        "evidence_kind": "deterministic_backend",
        "diagnostic_only": kind not in {"lean_verified", "lean_failed"},
        "certificate": {"backend": "lean", "source_sha256": _source_hash(source)} if kind == "lean_verified" else None,
        "verification_boundary": "Lean accepted the source without placeholders." if kind == "lean_verified" else reason,
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
    combined_output = "\n".join(part for part in (completed.stdout, completed.stderr) if part)
    if _lean_environment_failure(combined_output):
        evidence = _evidence(
            "lean_unavailable",
            command=command,
            source=source,
            uses_sorry=uses_sorry,
            lean_version=version,
            returncode=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
            reason="Lean execution failed because the configured toolchain or network-dependent environment is unavailable.",
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
