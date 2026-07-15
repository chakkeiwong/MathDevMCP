"""Fail-closed import/process/network/write guard for formal Phase 03 actions."""

from __future__ import annotations

import builtins
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib.abc
import io
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from typing import Any, Iterator


_FORMAL_PARENT = Path(".local/mathdevmcp/evidence/p03-20260712/result-rounds")
_FROZEN_SOURCES = frozenset(
    {
        "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
        "docs/risky-debt-maliar-deep-learning-lecture-note.tex",
    }
)
_BLOCKED_PROJECT_MODULES = frozenset(
    {
        "mathdevmcp.agent_hypothesis_expansion",
        "mathdevmcp.counterexample_search",
        "mathdevmcp.derivation_branch_controller",
        "mathdevmcp.derivation_search_tree",
        "mathdevmcp.derivation_tree_expansion",
        "mathdevmcp.derive_from",
        "mathdevmcp.derive_or_refute",
        "mathdevmcp.doctor",
        "mathdevmcp.document_derivation_tree",
        "mathdevmcp.external_tool_adapters",
        "mathdevmcp.formalization",
        "mathdevmcp.lean_check",
        "mathdevmcp.numeric_runner",
        "mathdevmcp.promotion_policy",
        "mathdevmcp.proof_obligations",
        "mathdevmcp.propose_fix",
        "mathdevmcp.symbolic_backend",
    }
)
_BLOCKED_PACKAGE_ROOTS = frozenset(
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
_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
_O_TMPFILE = getattr(os, "O_TMPFILE", 0)


def _flags_request_write(flags: int) -> bool:
    if flags & _WRITE_FLAGS:
        return True
    return bool(_O_TMPFILE and flags & _O_TMPFILE == _O_TMPFILE)


_ACTIVE_GUARD: "ContextOnlyGuard | None" = None


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _repo_root() -> Path:
    root = Path.cwd().absolute()
    if not (root / ".git").exists() or not (root / "src/mathdevmcp").is_dir():
        raise RuntimeError("Phase 03 guard must run from the MathDevMCP workspace root")
    return root


def _safe_round_root(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute() or path.parent != _FORMAL_PARENT or path.name not in {f"rr0{i}" for i in range(1, 6)}:
        raise RuntimeError("formal Phase 03 round root is outside the reviewed result-round root")
    return path


def _write_no_replace(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        view = memoryview(payload)
        while view:
            count = os.write(descriptor, view)
            if count <= 0:
                raise OSError("short write while creating Phase 03 guard artifact")
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def import_is_forbidden(fullname: str) -> bool:
    if not isinstance(fullname, str) or not fullname:
        return True
    root = fullname.split(".", 1)[0]
    if root in _BLOCKED_PACKAGE_ROOTS:
        return True
    return any(fullname == item or fullname.startswith(item + ".") for item in _BLOCKED_PROJECT_MODULES)


def path_is_frozen_source(root: Path, value: str | os.PathLike[str]) -> bool:
    path = Path(value)
    absolute = path.absolute() if path.is_absolute() else (root / path).absolute()
    try:
        logical = absolute.relative_to(root).as_posix()
    except ValueError:
        return False
    return logical in _FROZEN_SOURCES


class _BlockedImportFinder(importlib.abc.MetaPathFinder):
    def __init__(self, guard: "ContextOnlyGuard") -> None:
        self.guard = guard

    def find_spec(self, fullname: str, path: Any = None, target: Any = None) -> None:
        if import_is_forbidden(fullname):
            self.guard.forbidden("python_import", fullname, {"module": fullname})
        return None


class ContextOnlyGuard:
    def __init__(self, *, round_root: str | Path | None, action: str, formal: bool) -> None:
        self.root = _repo_root()
        self.action = action
        self.formal = formal
        self._patches: list[tuple[Any, str, Any, Any]] = []
        self._finder = _BlockedImportFinder(self)
        self._installed = False
        self._attempts: list[dict[str, Any]] = []
        if formal:
            if round_root is None:
                raise RuntimeError("formal Phase 03 guard requires a round root")
            self.round_root = _safe_round_root(round_root)
            guard_root = self.root / self.round_root / "governance/guard"
            tmpdir_raw = os.environ.get("TMPDIR")
            if not tmpdir_raw:
                raise RuntimeError("formal Phase 03 guard requires round-local TMPDIR")
            self.tmpdir = Path(tmpdir_raw).absolute()
            expected_tmp = (self.root / self.round_root / "governance/tmp").absolute()
            if self.tmpdir != expected_tmp:
                raise RuntimeError("formal Phase 03 TMPDIR differs from the reviewed round-local path")
            if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
                raise RuntimeError("formal Phase 03 requires CUDA_VISIBLE_DEVICES=-1")
        else:
            self.round_root = None
            guard_root = Path(tempfile.mkdtemp(prefix="mathdevmcp-p03-guard-"))
            self.tmpdir = guard_root
        token = "".join(char if char.isalnum() or char in "_-" else "_" for char in action) or "unknown"
        guard_root.mkdir(parents=True, exist_ok=True)
        self.ledger_path = guard_root / f"forbidden-attempts-{token}.jsonl"
        self.attestation_path = guard_root / f"guard-attestation-{token}.json"
        _write_no_replace(self.ledger_path, b"")
        self.allowed_write_roots = [self.tmpdir]
        if self.round_root is not None:
            self.allowed_write_roots.append((self.root / self.round_root).absolute())

    def _record(self, kind: str, target: str, details: dict[str, Any]) -> None:
        record = {
            "schema_version": "p03_forbidden_attempt@1",
            "sequence": len(self._attempts) + 1,
            "action": self.action,
            "kind": kind,
            "target": target,
            "details": details,
            "recorded_at_utc": _utc_now(),
        }
        self._attempts.append(record)
        payload = _canonical(record) + b"\n"
        descriptor = os.open(
            self.ledger_path,
            os.O_WRONLY | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0),
        )
        try:
            os.write(descriptor, payload)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def forbidden(self, kind: str, target: str, details: dict[str, Any]) -> None:
        self._record(kind, target, details)
        raise RuntimeError(f"Phase 03 context-only guard rejected {kind}:{target}")

    def _patch(self, owner: Any, name: str, replacement: Any) -> None:
        original = getattr(owner, name)
        setattr(owner, name, replacement)
        self._patches.append((owner, name, original, replacement))

    def _write_allowed(self, value: Any, *, dir_fd: int | None = None) -> bool:
        if isinstance(value, int):
            return True
        try:
            path = Path(os.fspath(value))
        except TypeError:
            return False
        if path.is_absolute():
            absolute = path.absolute()
        elif dir_fd is not None:
            try:
                base = Path(os.readlink(f"/proc/self/fd/{dir_fd}"))
            except (OSError, TypeError, ValueError):
                return False
            absolute = (base / path).absolute()
        else:
            absolute = (Path.cwd() / path).absolute()
        if path_is_frozen_source(self.root, absolute):
            return False
        return any(absolute == allowed or allowed in absolute.parents for allowed in self.allowed_write_roots)

    def _require_write_allowed(self, operation: str, value: Any, *, dir_fd: int | None = None) -> None:
        if not self._write_allowed(value, dir_fd=dir_fd):
            self.forbidden("filesystem_write", operation, {"path": os.fspath(value) if not isinstance(value, int) else value})

    def _patch_processes(self) -> None:
        def blocked_process(target: str):
            def wrapper(*args: Any, **kwargs: Any) -> None:
                self.forbidden(
                    "process_launch",
                    target,
                    {"positional_count": len(args), "keyword_names": sorted(map(str, kwargs))},
                )

            return wrapper

        for owner, names in (
            (subprocess, ("run", "Popen", "call", "check_call", "check_output")),
            (
                os,
                (
                    "system",
                    "popen",
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
                ),
            ),
        ):
            for name in names:
                if hasattr(owner, name):
                    self._patch(owner, name, blocked_process(f"{getattr(owner, '__name__', owner)}.{name}"))

    def _patch_network(self) -> None:
        def blocked_network(target: str):
            def wrapper(*args: Any, **kwargs: Any) -> None:
                self.forbidden(
                    "network",
                    target,
                    {"positional_count": len(args), "keyword_names": sorted(map(str, kwargs))},
                )

            return wrapper

        for name in ("socket", "create_connection", "getaddrinfo"):
            if hasattr(socket, name):
                self._patch(socket, name, blocked_network(f"socket.{name}"))

    def _patch_filesystem(self) -> None:
        original_open = builtins.open
        original_io_open = io.open
        original_os_open = os.open

        def guarded_open(file: Any, mode: str = "r", *args: Any, **kwargs: Any):
            if any(marker in mode for marker in ("w", "a", "x", "+")):
                self._require_write_allowed("builtins.open", file)
            return original_open(file, mode, *args, **kwargs)

        def guarded_io_open(file: Any, mode: str = "r", *args: Any, **kwargs: Any):
            if any(marker in mode for marker in ("w", "a", "x", "+")):
                self._require_write_allowed("io.open", file)
            return original_io_open(file, mode, *args, **kwargs)

        def guarded_os_open(path: Any, flags: int, *args: Any, **kwargs: Any):
            if _flags_request_write(flags):
                self._require_write_allowed("os.open", path, dir_fd=kwargs.get("dir_fd"))
            return original_os_open(path, flags, *args, **kwargs)

        self._patch(builtins, "open", guarded_open)
        self._patch(io, "open", guarded_io_open)
        self._patch(os, "open", guarded_os_open)

        def single_path(name: str, original: Any):
            def wrapper(path: Any, *args: Any, **kwargs: Any):
                self._require_write_allowed(f"os.{name}", path, dir_fd=kwargs.get("dir_fd"))
                return original(path, *args, **kwargs)

            return wrapper

        for name in ("unlink", "remove", "rmdir", "mkdir", "makedirs"):
            if hasattr(os, name):
                self._patch(os, name, single_path(name, getattr(os, name)))

        def two_paths(name: str, original: Any):
            def wrapper(src: Any, dst: Any, *args: Any, **kwargs: Any):
                self._require_write_allowed(
                    f"os.{name}.src",
                    src,
                    dir_fd=kwargs.get("src_dir_fd"),
                )
                self._require_write_allowed(
                    f"os.{name}.dst",
                    dst,
                    dir_fd=kwargs.get("dst_dir_fd"),
                )
                return original(src, dst, *args, **kwargs)

            return wrapper

        for name in ("rename", "replace", "link", "symlink"):
            if hasattr(os, name):
                self._patch(os, name, two_paths(name, getattr(os, name)))

    def install(self) -> "ContextOnlyGuard":
        if self._installed:
            raise RuntimeError("Phase 03 guard cannot be installed twice")
        forbidden_loaded = sorted(name for name in sys.modules if import_is_forbidden(name))
        if forbidden_loaded:
            raise RuntimeError(f"forbidden modules were loaded before Phase 03 guard: {forbidden_loaded}")
        sys.meta_path.insert(0, self._finder)
        self._patch_processes()
        self._patch_network()
        self._patch_filesystem()
        self._installed = True
        return self

    def close(self) -> dict[str, Any]:
        if not self._installed:
            raise RuntimeError("Phase 03 guard is not installed")
        replacement_errors = [
            f"{getattr(owner, '__name__', type(owner).__name__)}.{name}"
            for owner, name, _original, replacement in self._patches
            if getattr(owner, name) is not replacement
        ]
        if self._finder not in sys.meta_path:
            replacement_errors.append("sys.meta_path.import_guard")
        raw = self.ledger_path.read_bytes()
        entries = [line for line in raw.splitlines() if line]
        attestation = {
            "schema_version": "p03_context_only_guard_attestation@1",
            "action": self.action,
            "ledger_ref": (
                self.ledger_path.relative_to(self.root).as_posix()
                if self.formal
                else self.ledger_path.as_posix()
            ),
            "ledger_sha256": hashlib.sha256(raw).hexdigest(),
            "forbidden_attempt_count": len(entries),
            "guard_replacement_errors": replacement_errors,
            "backend_request_count": 0,
            "source_edit_count": 0,
            "publication_count": 0,
            "closed_at_utc": _utc_now(),
        }
        # Restore first so the immutable attestation can be written by the
        # original primitives without creating a self-recorded write attempt.
        for owner, name, original, replacement in reversed(self._patches):
            if getattr(owner, name) is replacement:
                setattr(owner, name, original)
        if self._finder in sys.meta_path:
            sys.meta_path.remove(self._finder)
        self._installed = False
        _write_no_replace(self.attestation_path, _canonical(attestation))
        if replacement_errors:
            raise RuntimeError(f"Phase 03 guard replacement integrity failed: {replacement_errors}")
        if entries:
            raise RuntimeError(f"Phase 03 guard recorded {len(entries)} forbidden attempt(s)")
        return attestation


def guard_is_active() -> bool:
    return _ACTIVE_GUARD is not None and _ACTIVE_GUARD._installed


@contextmanager
def install_guard(
    *,
    round_root: str | Path | None = None,
    action: str = "standalone",
    formal: bool | None = None,
) -> Iterator[ContextOnlyGuard]:
    global _ACTIVE_GUARD
    if _ACTIVE_GUARD is not None:
        raise RuntimeError("nested Phase 03 guards are forbidden")
    is_formal = bool(round_root is not None) if formal is None else formal
    guard = ContextOnlyGuard(round_root=round_root, action=action, formal=is_formal).install()
    _ACTIVE_GUARD = guard
    try:
        yield guard
    finally:
        try:
            guard.close()
        finally:
            _ACTIVE_GUARD = None


def pytest_configure(config: Any) -> None:
    global _ACTIVE_GUARD
    if _ACTIVE_GUARD is not None:
        raise RuntimeError("Phase 03 pytest guard is already active")
    round_root = os.environ.get("MATHDEVMCP_P03_ROUND_ROOT")
    action = os.environ.get("MATHDEVMCP_P03_ACTION", "pytest")
    if not round_root:
        raise RuntimeError("Phase 03 pytest guard requires MATHDEVMCP_P03_ROUND_ROOT")
    _ACTIVE_GUARD = ContextOnlyGuard(round_root=round_root, action=action, formal=True).install()


def pytest_unconfigure(config: Any) -> None:
    global _ACTIVE_GUARD
    if _ACTIVE_GUARD is None:
        return
    try:
        _ACTIVE_GUARD.close()
    finally:
        _ACTIVE_GUARD = None
