"""Fail-closed backend guard for formal Phase 02 extraction commands."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import importlib
import importlib.abc
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any, Iterator, Mapping, Sequence

from mathdevmcp.evidence_manifest import canonical_json_bytes
from mathdevmcp.extraction_evidence import load_profile


_FORMAL_ROOT_PREFIX = Path(".local/mathdevmcp/evidence/p02r3-20260712/result-rounds")
_BLOCKED_IMPORT_ROOTS = frozenset({"sympy", "sage", "sageall", "pantograph", "lean_dojo", "leandojo"})
_BLOCKED_EXECUTABLES = frozenset(
    {
        "lean",
        "lake",
        "elan",
        "sage",
        "leansearch",
        "leanexplore",
        "jixia",
        "pantograph",
    }
)
_SHELL_EXECUTABLES = frozenset({"bash", "dash", "fish", "ksh", "sh", "zsh"})
_BLOCKED_PYTHON_MARKERS = (
    "sympy",
    "sage",
    "lean_dojo",
    "leandojo",
    "mathdevmcp.external_tool_adapters",
    "mathdevmcp.derive_or_refute",
)

_ACTIVE_GUARD: "BackendGuard | None" = None


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _repo_root() -> Path:
    root = Path.cwd().absolute()
    if not (root / ".git").exists() or not (root / "src/mathdevmcp").is_dir():
        raise RuntimeError("Phase 02 backend guard must run from the MathDevMCP workspace root")
    return root


def _safe_round_root(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        raise RuntimeError("formal Phase 02 round root must be workspace-relative")
    if path.parent != _FORMAL_ROOT_PREFIX or path.name not in {f"rr0{i}" for i in range(1, 6)}:
        raise RuntimeError("formal Phase 02 round root is outside the reviewed result-round root")
    return path


def _create_no_replace(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise OSError("short write while creating Phase 02 guard artifact")
            view = view[written:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


class _BlockedImportFinder(importlib.abc.MetaPathFinder):
    def __init__(self, guard: "BackendGuard") -> None:
        self.guard = guard

    def find_spec(self, fullname: str, path: Any = None, target: Any = None) -> None:
        root = fullname.split(".", 1)[0]
        if root in _BLOCKED_IMPORT_ROOTS:
            self.guard.forbidden("python_import", fullname, {"module": fullname})
        return None


class BackendGuard:
    def __init__(self, *, round_root: str | Path | None, action: str, formal: bool) -> None:
        self.root = _repo_root()
        self.action = action
        self.formal = formal
        if formal:
            if round_root is None:
                raise RuntimeError("formal Phase 02 guard requires a round root")
            self.round_root = _safe_round_root(round_root)
            base = self.root / self.round_root / "ledgers"
        else:
            self.round_root = None
            base = Path(tempfile.mkdtemp(prefix="mathdevmcp-p02-guard-"))
        token = re_safe(action)
        self.ledger_path = base / f"backend-invocations-{token}.jsonl"
        self.attestation_path = base / f"backend-guard-attestation-{token}.json"
        self._patches: list[tuple[Any, str, Any, Any]] = []
        self._finder = _BlockedImportFinder(self)
        self._sequence = 0
        self._installed = False
        self._parser_profile = self._load_parser_profile()
        self._expected_parser_calls = self._parser_call_registry()
        self._observed_parser_calls: set[str] = set()
        self._active_parser_run_argv: list[str] | None = None

    def _load_parser_profile(self) -> dict[str, Any]:
        effective, _materialized = load_profile(self.root)
        return effective["parser_fidelity_profile"]

    def _parser_call_registry(self) -> dict[str, list[str]]:
        registry: dict[str, list[str]] = {}
        for backend, executable in self._parser_profile["executables"].items():
            registry[f"{backend}:version"] = list(executable["version_argv"])
            for source_ref in self._parser_profile["source_allowlist"]:
                case = hashlib.sha256(source_ref.encode("utf-8")).hexdigest()
                registry[f"{backend}:{source_ref}"] = [
                    value.replace("RR", self.round_root.as_posix() if self.round_root is not None else "RR")
                    .replace("CASE", case)
                    .replace("SOURCE", source_ref)
                    for value in executable["fidelity_argv_template"]
                ]
        if len(registry) != 28:
            raise RuntimeError("Phase 02R2 parser profile does not define exactly 2+26 calls")
        return registry

    def _record(self, kind: str, target: str, details: Mapping[str, Any]) -> None:
        self._sequence += 1
        record = {
            "schema_version": "p02_forbidden_backend_attempt@1",
            "sequence": self._sequence,
            "action": self.action,
            "kind": kind,
            "target": target,
            "details": dict(details),
            "recorded_at_utc": _utc_now(),
        }
        payload = canonical_json_bytes(record) + b"\n"
        descriptor = os.open(self.ledger_path, os.O_WRONLY | os.O_APPEND | getattr(os, "O_NOFOLLOW", 0))
        try:
            view = memoryview(payload)
            while view:
                written = os.write(descriptor, view)
                if written <= 0:
                    raise OSError("short Phase 02 guard-ledger write")
                view = view[written:]
            os.fsync(descriptor)
        finally:
            os.close(descriptor)

    def forbidden(self, kind: str, target: str, details: Mapping[str, Any]) -> None:
        self._record(kind, target, details)
        raise RuntimeError(f"Phase 02 forbids mathematical backend access: {kind}:{target}")

    def _patch(self, owner: Any, name: str, replacement: Any) -> None:
        original = getattr(owner, name)
        setattr(owner, name, replacement)
        self._patches.append((owner, name, original, replacement))

    def _forbidden_wrapper(self, target: str):
        def wrapper(*args: Any, **kwargs: Any) -> None:
            self.forbidden(
                "python_entry_point",
                target,
                {"positional_count": len(args), "keyword_names": sorted(str(key) for key in kwargs)},
            )

        wrapper.__name__ = f"p02_forbidden_{target.rsplit('.', 1)[-1]}"
        wrapper.__qualname__ = wrapper.__name__
        setattr(wrapper, "__p02_backend_guard__", self)
        return wrapper

    def _patch_module_entry(self, module_name: str, name: str) -> None:
        module = importlib.import_module(module_name)
        if hasattr(module, name):
            self._patch(module, name, self._forbidden_wrapper(f"{module_name}.{name}"))

    @staticmethod
    def _argv(args: Sequence[Any], kwargs: Mapping[str, Any]) -> list[str] | None:
        value = args[0] if args else kwargs.get("args")
        if isinstance(value, (str, os.PathLike)):
            return [os.fspath(value)]
        if isinstance(value, (list, tuple)) and all(isinstance(item, (str, os.PathLike)) for item in value):
            return [os.fspath(item) for item in value]
        return None

    def _parser_call_key(self, argv: list[str], kwargs: Mapping[str, Any]) -> str | None:
        if not self.formal or self.action != "parser_fidelity_tests" or self.round_root is None:
            return None
        profile = self._parser_profile
        executable = argv[0] if argv else ""
        backend = next((name for name, item in profile["executables"].items() if item["path"] == executable), None)
        if backend is None:
            return None
        executable_profile = profile["executables"][backend]
        key = next((item for item, expected in self._expected_parser_calls.items() if argv == expected), None)
        if key is None or not key.startswith(f"{backend}:"):
            return None
        expected_environment = {
            key: value.replace("RR", self.round_root.as_posix())
            for key, value in profile["environment"].items()
        }
        if set(kwargs) != {"capture_output", "check", "cwd", "env", "timeout"}:
            return None
        if kwargs["env"] != expected_environment or Path(kwargs["cwd"]).absolute() != self.root:
            return None
        if kwargs["capture_output"] is not True or kwargs["check"] is not False:
            return None
        timeout_key = "version_timeout_seconds" if key.endswith(":version") else "source_timeout_seconds"
        if kwargs["timeout"] != executable_profile[timeout_key]:
            return None
        return key

    def _allowed_parser_call(self, argv: list[str], kwargs: Mapping[str, Any]) -> bool:
        return self._parser_call_key(argv, kwargs) is not None

    def _register_parser_call(self, argv: list[str], kwargs: Mapping[str, Any]) -> str | None:
        key = self._parser_call_key(argv, kwargs)
        if key is None:
            return None
        if key in self._observed_parser_calls:
            self.forbidden("subprocess", "duplicate_reviewed_parser_invocation", {"argv": argv})
        self._observed_parser_calls.add(key)
        return key

    def _subprocess_is_forbidden(self, argv: list[str] | None, kwargs: Mapping[str, Any]) -> tuple[bool, str]:
        if kwargs.get("shell", False):
            return True, "shell_command"
        if argv is None:
            return False, "unstructured_non_shell_command"
        if self._allowed_parser_call(argv, kwargs):
            return False, "reviewed_parser_exception"
        executable = Path(argv[0]).name.lower() if argv else ""
        route_executables = {
            Path(token).name.lower()
            for token in argv
            if token and not token.startswith("-") and "=" not in token
        }
        route_has_python = any(name.startswith("python") for name in route_executables)
        if executable in {"latexml", "pandoc"}:
            return True, "unreviewed_parser_invocation"
        if executable in _BLOCKED_EXECUTABLES:
            return True, "mathematical_backend_executable"
        if route_executables & _BLOCKED_EXECUTABLES:
            return True, "wrapped_mathematical_backend_executable"
        if route_executables & _SHELL_EXECUTABLES:
            return True, "shell_executable"
        if self.formal and route_has_python:
            return True, "unreviewed_python_subprocess"
        if route_has_python and any(marker in " ".join(argv).lower() for marker in _BLOCKED_PYTHON_MARKERS):
            return True, "mathematical_backend_python_route"
        return False, "non_backend_subprocess"

    def _patch_os_process_launch(self) -> None:
        for name in (
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
        ):
            if hasattr(os, name):
                self._patch(os, name, self._forbidden_wrapper(f"os.{name}"))

    def _patch_subprocess(self) -> None:
        original_run = subprocess.run
        original_popen = subprocess.Popen

        def guarded_run(*args: Any, **kwargs: Any):
            argv = self._argv(args, kwargs)
            blocked, reason = self._subprocess_is_forbidden(argv, kwargs)
            if blocked:
                self.forbidden("subprocess", reason, {"argv": argv, "shell": bool(kwargs.get("shell", False))})
            parser_key = self._register_parser_call(argv, kwargs) if argv is not None else None
            if parser_key is None:
                return original_run(*args, **kwargs)
            if self._active_parser_run_argv is not None:
                self.forbidden("subprocess", "nested_parser_invocation", {"argv": argv})
            self._active_parser_run_argv = argv
            try:
                return original_run(*args, **kwargs)
            finally:
                self._active_parser_run_argv = None

        guard = self

        class GuardedPopen(original_popen):
            def __init__(popen_self, *args: Any, **kwargs: Any) -> None:
                argv = guard._argv(args, kwargs)
                if guard._active_parser_run_argv is not None and argv == guard._active_parser_run_argv:
                    super().__init__(*args, **kwargs)
                    return
                executable = Path(argv[0]).name.lower() if argv else ""
                if executable in {"latexml", "pandoc"}:
                    guard.forbidden(
                        "subprocess",
                        "direct_parser_popen",
                        {"argv": argv, "shell": bool(kwargs.get("shell", False))},
                    )
                blocked, reason = guard._subprocess_is_forbidden(argv, kwargs)
                if blocked:
                    guard.forbidden(
                        "subprocess",
                        reason,
                        {"argv": argv, "shell": bool(kwargs.get("shell", False))},
                    )
                super().__init__(*args, **kwargs)

        setattr(guarded_run, "__p02_backend_guard__", self)
        setattr(GuardedPopen, "__p02_backend_guard__", self)
        self._patch(subprocess, "run", guarded_run)
        self._patch(subprocess, "Popen", GuardedPopen)

    def install(self) -> "BackendGuard":
        if self._installed:
            raise RuntimeError("Phase 02 backend guard cannot be installed twice")
        _create_no_replace(self.ledger_path, b"")
        sys.meta_path.insert(0, self._finder)

        # Import and patch lower-level functions first so later from-imports
        # bind the guard wrappers rather than the original backend entries.
        targets = [
            ("mathdevmcp.counterexample_search", "find_counterexample"),
            ("mathdevmcp.derive_or_refute", "derive_or_refute"),
            ("mathdevmcp.proof_obligations", "check_proof_obligation"),
            ("mathdevmcp.lean_check", "check_lean_source"),
            ("mathdevmcp.symbolic_backend", "check_symbolic_obligation"),
            ("mathdevmcp.numeric_runner", "run_numeric_diagnostic_plan"),
            ("mathdevmcp.derive_from", "derive_from"),
        ]
        for module_name, name in targets:
            self._patch_module_entry(module_name, name)

        adapters = importlib.import_module("mathdevmcp.external_tool_adapters")
        for name in sorted(item for item in vars(adapters) if item.startswith("adapt_") and callable(getattr(adapters, item))):
            self._patch(adapters, name, self._forbidden_wrapper(f"mathdevmcp.external_tool_adapters.{name}"))
        self._patch_module_entry("mathdevmcp.derivation_branch_controller", "can_derive_with_budget")
        self._patch_subprocess()
        self._patch_os_process_launch()
        self._installed = True
        return self

    def close(self) -> dict[str, Any]:
        if not self._installed:
            raise RuntimeError("Phase 02 backend guard is not installed")
        replacement_errors: list[str] = []
        for owner, name, _original, replacement in self._patches:
            if getattr(owner, name) is not replacement:
                replacement_errors.append(f"{getattr(owner, '__name__', type(owner).__name__)}.{name}")
        if self._finder not in sys.meta_path:
            replacement_errors.append("sys.meta_path.import_guard")
        if self.formal and self.action == "parser_fidelity_tests":
            missing = sorted(set(self._expected_parser_calls) - self._observed_parser_calls)
            extra = sorted(self._observed_parser_calls - set(self._expected_parser_calls))
            if missing or extra:
                replacement_errors.append(
                    f"parser_invocation_closure:missing={len(missing)}:extra={len(extra)}"
                )
        raw = self.ledger_path.read_bytes()
        entries = [line for line in raw.splitlines() if line]
        attestation = {
            "schema_version": "p02_backend_guard_attestation@1",
            "action": self.action,
            "ledger_ref": (
                self.ledger_path.relative_to(self.root).as_posix()
                if self.formal
                else self.ledger_path.as_posix()
            ),
            "ledger_sha256": hashlib.sha256(raw).hexdigest(),
            "forbidden_attempt_count": len(entries),
            "guard_replacement_errors": replacement_errors,
            "parser_exception_enabled": self.formal and self.action == "parser_fidelity_tests",
            "closed_at_utc": _utc_now(),
        }
        _create_no_replace(self.attestation_path, canonical_json_bytes(attestation))
        for owner, name, original, replacement in reversed(self._patches):
            if getattr(owner, name) is replacement:
                setattr(owner, name, original)
        if self._finder in sys.meta_path:
            sys.meta_path.remove(self._finder)
        self._installed = False
        if replacement_errors:
            raise RuntimeError(f"Phase 02 backend guard was replaced or bypassed: {replacement_errors}")
        if entries:
            raise RuntimeError(f"Phase 02 recorded {len(entries)} forbidden backend attempt(s)")
        return attestation


def re_safe(value: str) -> str:
    token = "".join(char if char.isalnum() or char in "_-" else "_" for char in value)
    return token or "unknown"


def guard_is_active() -> bool:
    return _ACTIVE_GUARD is not None and _ACTIVE_GUARD._installed


@contextmanager
def install_guard(
    *,
    round_root: str | Path | None = None,
    action: str = "standalone",
    formal: bool | None = None,
) -> Iterator[BackendGuard]:
    global _ACTIVE_GUARD
    if _ACTIVE_GUARD is not None:
        raise RuntimeError("nested Phase 02 backend guards are forbidden")
    is_formal = bool(round_root is not None) if formal is None else formal
    guard = BackendGuard(round_root=round_root, action=action, formal=is_formal).install()
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
        raise RuntimeError("Phase 02 pytest backend guard is already active")
    round_root = os.environ.get("MATHDEVMCP_P02_ROUND_ROOT")
    action = os.environ.get("MATHDEVMCP_P02_ACTION", "development_pytest")
    formal = round_root is not None
    _ACTIVE_GUARD = BackendGuard(round_root=round_root, action=action, formal=formal).install()


def pytest_unconfigure(config: Any) -> None:
    global _ACTIVE_GUARD
    if _ACTIVE_GUARD is None:
        raise RuntimeError("Phase 02 pytest backend guard disappeared before teardown")
    try:
        _ACTIVE_GUARD.close()
    finally:
        _ACTIVE_GUARD = None
