#!/usr/bin/env python3
"""Isolated, pre-import guarded entry for one Phase 09 resolver CLI probe."""

from __future__ import annotations

import contextlib
import importlib.abc
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
from typing import Any


FIXED_COLLECTION = "global_evidence_ref_records"
EXPECTED_ENV_KEYS = frozenset(
    {
        "CUDA_VISIBLE_DEVICES",
        "PYTHONHASHSEED",
        "PYTHONDONTWRITEBYTECODE",
        "PYTHONIOENCODING",
        "LANG",
        "LC_ALL",
        "MATHDEVMCP_P09_TEST_ROOT",
    }
)
BLOCKED_ROOTS = frozenset(
    {
        "anthropic",
        "cupy",
        "jax",
        "lean_dojo",
        "leandojo",
        "openai",
        "pantograph",
        "sage",
        "sageall",
        "sympy",
        "tensorflow",
        "torch",
    }
)
MATHEMATICAL_IMPORT_ROOTS = frozenset(
    {"lean_dojo", "leandojo", "pantograph", "sage", "sageall", "sympy"}
)
BACKEND_ENTRY_NAMES = frozenset(
    {
        "attempt_leandojo_tiny_theorem",
        "check_lean_source",
        "run_sage_polynomial_obligation",
        "run_sympy_scalar_obligation",
    }
)
DOCUMENT_AUDIT_ENTRY_NAMES = frozenset(
    {
        "audit_document_derivation_tree",
        "audit_math_document_rigor",
        "high_level_audit_document_derivation_tree",
        "high_level_audit_math_document_rigor",
    }
)
PROCESS_FUNCTIONS = (
    "run",
    "call",
    "check_call",
    "check_output",
    "getoutput",
    "getstatusoutput",
)
OS_PROCESS_FUNCTIONS = (
    "system",
    "popen",
    "fork",
    "forkpty",
    "execl",
    "execle",
    "execlp",
    "execlpe",
    "execv",
    "execve",
    "execvp",
    "execvpe",
    "spawnl",
    "spawnle",
    "spawnlp",
    "spawnlpe",
    "spawnv",
    "spawnve",
    "spawnvp",
    "spawnvpe",
    "posix_spawn",
    "posix_spawnp",
)
SOCKET_FUNCTIONS = (
    "create_connection",
    "create_server",
    "socketpair",
    "fromfd",
    "fromshare",
    "getaddrinfo",
    "gethostbyname",
    "gethostbyname_ex",
    "gethostbyaddr",
    "getnameinfo",
)


class GuardError(RuntimeError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _path_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


class _Finder(importlib.abc.MetaPathFinder):
    def __init__(self, attempts: list[dict[str, Any]]) -> None:
        self.attempts = attempts

    def find_spec(self, fullname: str, path: Any = None, target: Any = None) -> None:
        if fullname.split(".", 1)[0] in BLOCKED_ROOTS:
            _record_attempt(self.attempts, "python_import", fullname)
        return None


def _record_attempt(attempts: list[dict[str, Any]], kind: str, target: str) -> None:
    attempts.append({"sequence": len(attempts) + 1, "kind": kind, "target": target})
    raise GuardError(f"blocked child {kind} call")


def _blocked_call(attempts: list[dict[str, Any]], kind: str, target: str):
    def wrapper(*args: Any, **kwargs: Any) -> None:
        _record_attempt(attempts, kind, target)

    return wrapper


def _block_calls(attempts: list[dict[str, Any]]) -> None:
    def blocked(label: str, *, kind: str):
        def wrapper(*args: Any, **kwargs: Any) -> None:
            _record_attempt(attempts, kind, label)

        return wrapper

    original_socket = socket.socket

    class BlockedSocket(original_socket):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _record_attempt(attempts, "network", "socket.socket")

    BlockedSocket.__name__ = "socket"
    BlockedSocket.__qualname__ = "socket"
    BlockedSocket.__module__ = "socket"
    socket.socket = BlockedSocket
    if hasattr(socket, "SocketType"):
        socket.SocketType = BlockedSocket

    original_popen = subprocess.Popen

    class BlockedPopen(original_popen):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _record_attempt(attempts, "process", "subprocess.Popen")

    BlockedPopen.__name__ = "Popen"
    BlockedPopen.__qualname__ = "Popen"
    BlockedPopen.__module__ = "subprocess"
    subprocess.Popen = BlockedPopen

    for owner, names in (
        (subprocess, PROCESS_FUNCTIONS),
        (os, OS_PROCESS_FUNCTIONS),
        (socket, SOCKET_FUNCTIONS),
    ):
        for name in names:
            if hasattr(owner, name):
                kind = "network" if owner is socket else "process"
                setattr(
                    owner,
                    name,
                    blocked(f"{getattr(owner, '__name__', owner)}.{name}", kind=kind),
                )


def _patch_loaded_aliases(
    attempts: list[dict[str, Any]], modules: dict[str, Any]
) -> None:
    for module_name, module in list(modules.items()):
        if not module_name.startswith("mathdevmcp.") or module is None:
            continue
        for name in DOCUMENT_AUDIT_ENTRY_NAMES:
            if hasattr(module, name):
                setattr(
                    module,
                    name,
                    _blocked_call(attempts, "document_audit", f"{module_name}.{name}"),
                )
        for name in BACKEND_ENTRY_NAMES:
            if hasattr(module, name):
                setattr(
                    module,
                    name,
                    _blocked_call(
                        attempts, "mathematical_backend", f"{module_name}.{name}"
                    ),
                )


def _guard_attestation(attempts: list[dict[str, Any]]) -> dict[str, Any]:
    backend_attempts = sum(
        item["kind"] == "mathematical_backend"
        or (
            item["kind"] == "python_import"
            and item["target"].split(".", 1)[0] in MATHEMATICAL_IMPORT_ROOTS
        )
        for item in attempts
    )
    return {
        "schema_version": "p09_child_guard_attestation@1",
        "attempts": list(attempts),
        "forbidden_attempt_count": len(attempts),
        "process_attempt_count": sum(item["kind"] == "process" for item in attempts),
        "mathematical_backend_attempt_count": backend_attempts,
        "document_audit_invocation_count": sum(
            item["kind"] == "document_audit" for item in attempts
        ),
        "network_attempt_count": sum(item["kind"] == "network" for item in attempts),
        "resolved_verb": "resolve-document-derivation-records",
    }


def _validated_input() -> tuple[Path, str]:
    bootstrap = Path(__file__).resolve()
    workspace = bootstrap.parent.parent.resolve()
    if (
        Path.cwd().resolve() != workspace
        or sys.argv != [str(bootstrap)]
        or sys.flags.isolated != 1
        or sys.flags.dont_write_bytecode != 1
        or set(os.environ) != EXPECTED_ENV_KEYS
        or os.environ.get("CUDA_VISIBLE_DEVICES") != "-1"
        or os.environ.get("PYTHONHASHSEED") != "0"
        or os.environ.get("PYTHONDONTWRITEBYTECODE") != "1"
        or os.environ.get("PYTHONIOENCODING") != "utf-8"
        or os.environ.get("LANG") != "C.UTF-8"
        or os.environ.get("LC_ALL") != "C.UTF-8"
    ):
        raise GuardError("isolated child invocation boundary mismatch")
    raw = sys.stdin.buffer.read(4097)
    if not raw or len(raw) > 4096:
        raise GuardError("child stdin exceeds its bound")
    try:
        payload = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GuardError("child stdin is not JSON") from exc
    if not isinstance(payload, dict) or set(payload) != {
        "artifact_root",
        "collection",
        "page_token",
    } or _canonical(payload) != raw:
        raise GuardError("child stdin schema is not canonical and closed")
    if payload["collection"] != FIXED_COLLECTION or not isinstance(payload["page_token"], str):
        raise GuardError("child resolver inputs differ from the fixed route")
    test_root = Path(os.environ["MATHDEVMCP_P09_TEST_ROOT"])
    artifact_root = Path(payload["artifact_root"])
    if (
        test_root.is_symlink()
        or not test_root.is_dir()
        or artifact_root.is_symlink()
        or not artifact_root.is_dir()
        or not _path_under(artifact_root.resolve(), test_root.resolve())
    ):
        raise GuardError("child artifact root escapes pytest temporary storage")
    return artifact_root, payload["page_token"]


def main() -> int:
    original_stdout = sys.stdout
    try:
        artifact_root, page_token = _validated_input()
        attempts: list[dict[str, Any]] = []
        sys.meta_path.insert(0, _Finder(attempts))
        _block_calls(attempts)
        workspace = Path(__file__).resolve().parent.parent
        sys.path.insert(0, str(workspace / "src"))

        from mathdevmcp import cli

        _patch_loaded_aliases(attempts, sys.modules)

        captured_stdout = io.BytesIO()
        captured_stderr = io.BytesIO()
        stdout_wrapper = io.TextIOWrapper(captured_stdout, encoding="utf-8")
        stderr_wrapper = io.TextIOWrapper(captured_stderr, encoding="utf-8")
        with contextlib.redirect_stdout(stdout_wrapper), contextlib.redirect_stderr(stderr_wrapper):
            returncode = cli.main(
                [
                    "resolve-document-derivation-records",
                    page_token,
                    FIXED_COLLECTION,
                    "--artifact-root",
                    str(artifact_root),
                ]
            )
            stdout_wrapper.flush()
            stderr_wrapper.flush()
        cli_stdout = captured_stdout.getvalue()
        cli_stderr = captured_stderr.getvalue()
        if returncode != 2 or cli_stdout != b"" or len(cli_stderr) > 4096:
            raise GuardError("resolver CLI did not return the fixed invalid-input envelope")
        error = json.loads(cli_stderr.decode("utf-8", "strict"))
        serialized = cli_stderr.decode("utf-8", "strict")
        if (
            not isinstance(error, dict)
            or error.get("ok") is not False
            or error.get("error", {}).get("type") != "invalid_arguments"
            or "Traceback" in serialized
            or page_token in serialized
            or str(artifact_root) in serialized
            or attempts
        ):
            raise GuardError("resolver CLI leaked private input or crossed the child guard")
        result = {
            "schema_version": "p09_guarded_cli_result@2",
            "cli_returncode": returncode,
            "cli_stdout_empty": True,
            "cli_error_type": "invalid_arguments",
            "cli_traceback_absent": True,
            "private_input_scan_passed": True,
            "guard_attestation": _guard_attestation(attempts),
        }
        original_stdout.buffer.write(_canonical(result) + b"\n")
        original_stdout.buffer.flush()
        return 0
    except Exception:
        sys.__stderr__.buffer.write(
            _canonical({"status": "ERROR_P09_GUARDED_CLI", "detail": "guarded invocation rejected"})
            + b"\n"
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
