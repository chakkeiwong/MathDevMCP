"""Fail-closed pytest guard for the Phase 09 non-live verification set."""

from __future__ import annotations

import builtins
from datetime import datetime, timezone
import hashlib
import importlib.abc
import importlib.metadata
import io
import json
import os
from pathlib import Path
import platform
import socket
import subprocess
import sys
from typing import Any, Mapping, Sequence


WORKSPACE = Path(__file__).resolve().parent.parent
BOOTSTRAP = Path(__file__).resolve().parent / "p09_guarded_cli_entry.py"
FIXED_COLLECTION = "global_evidence_ref_records"
CHILD_ENV_KEYS = frozenset(
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
BLOCKED_PACKAGE_ROOTS = frozenset(
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
_ORIGINAL_POPEN = subprocess.Popen
_PATCHES: list[tuple[Any, str, Any, Any]] = []
_FINDER: "_BlockedImportFinder | None" = None
_FORBIDDEN_ATTEMPTS: list[dict[str, Any]] = []
_CLI_INVOCATION_COUNT = 0
_CLI_GUARD_ATTESTATIONS: list[dict[str, Any]] = []
_PYTEST_TEMP_ROOT: Path | None = None
_PASSED_NODEIDS: list[str] = []
_FAILED_NODEIDS: list[str] = []
_SKIPPED_NODEIDS: list[str] = []
_COLLECTION_FAILED_NODEIDS: list[str] = []
_COLLECTION_SKIPPED_NODEIDS: list[str] = []
_COLLECTED_NODEIDS: list[str] = []
_CODE_BINDINGS_START: list[dict[str, Any]] | None = None
_RUNTIME_IDENTITY_START: dict[str, Any] | None = None
RUNTIME_DISTRIBUTIONS = {
    "anyio": "4.13.0",
    "httpx": "0.28.1",
    "mcp": "1.27.0",
    "pydantic": "2.12.5",
    "pytest": "9.0.2",
}
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


class P09GuardError(RuntimeError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def import_is_forbidden(fullname: str) -> bool:
    return not isinstance(fullname, str) or not fullname or fullname.split(".", 1)[0] in BLOCKED_PACKAGE_ROOTS


def _record_forbidden(kind: str, target: str) -> None:
    _FORBIDDEN_ATTEMPTS.append(
        {"sequence": len(_FORBIDDEN_ATTEMPTS) + 1, "kind": kind, "target": target}
    )
    raise P09GuardError(f"Phase 09 guard rejected {kind}:{target}")


class _BlockedImportFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname: str, path: Any = None, target: Any = None) -> None:
        if import_is_forbidden(fullname):
            _record_forbidden("python_import", fullname)
        return None


def _patch(owner: Any, name: str, replacement: Any) -> None:
    original = getattr(owner, name)
    setattr(owner, name, replacement)
    _PATCHES.append((owner, name, original, replacement))


def _blocked_call(target: str, *, kind: str = "call"):
    def wrapper(*args: Any, **kwargs: Any) -> None:
        _record_forbidden(kind, target)

    return wrapper


def _blocked_socket_class(original: type[socket.socket]):
    class BlockedSocket(original):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _record_forbidden("network", "socket.socket")

    BlockedSocket.__name__ = "socket"
    BlockedSocket.__qualname__ = "socket"
    BlockedSocket.__module__ = "socket"
    return BlockedSocket


def _blocked_popen_class(original: type[Any]):
    class BlockedPopen(original):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            _record_forbidden("process", "subprocess.Popen")

    BlockedPopen.__name__ = "Popen"
    BlockedPopen.__qualname__ = "Popen"
    BlockedPopen.__module__ = "subprocess"
    return BlockedPopen


def _flags_request_write(flags: int) -> bool:
    return bool(flags & _WRITE_FLAGS) or bool(
        _O_TMPFILE and flags & _O_TMPFILE == _O_TMPFILE
    )


def _path_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _write_allowed(value: Any, *, dir_fd: int | None = None) -> bool:
    if isinstance(value, int):
        return True
    if _PYTEST_TEMP_ROOT is None:
        return False
    try:
        path = Path(os.fspath(value))
    except TypeError:
        return False
    if path.is_absolute():
        absolute = path.absolute()
    elif dir_fd is not None:
        try:
            absolute = (Path(os.readlink(f"/proc/self/fd/{dir_fd}")) / path).absolute()
        except (OSError, ValueError):
            return False
    else:
        absolute = (Path.cwd() / path).absolute()
    raw_attestation = os.environ.get("MATHDEVMCP_P09_TEST_ATTESTATION")
    if raw_attestation:
        attestation = Path(raw_attestation)
        if not attestation.is_absolute():
            attestation = WORKSPACE / attestation
        expected_parent = WORKSPACE / ".local/mathdevmcp/evidence/p09-20260715/preflight"
        if (
            absolute == attestation.absolute()
            and attestation.parent.resolve() == expected_parent.resolve()
        ):
            return True
    return _path_under(absolute, _PYTEST_TEMP_ROOT)


def _require_write_allowed(operation: str, value: Any, *, dir_fd: int | None = None) -> None:
    if not _write_allowed(value, dir_fd=dir_fd):
        _record_forbidden("filesystem_write", operation)


def _install_filesystem_guard() -> None:
    original_open = builtins.open
    original_io_open = io.open
    original_os_open = os.open

    def guarded_open(file: Any, mode: str = "r", *args: Any, **kwargs: Any):
        if any(marker in mode for marker in ("w", "a", "x", "+")):
            _require_write_allowed("builtins.open", file)
        return original_open(file, mode, *args, **kwargs)

    def guarded_io_open(file: Any, mode: str = "r", *args: Any, **kwargs: Any):
        if any(marker in mode for marker in ("w", "a", "x", "+")):
            _require_write_allowed("io.open", file)
        return original_io_open(file, mode, *args, **kwargs)

    def guarded_os_open(path: Any, flags: int, *args: Any, **kwargs: Any):
        if _flags_request_write(flags):
            _require_write_allowed("os.open", path, dir_fd=kwargs.get("dir_fd"))
        return original_os_open(path, flags, *args, **kwargs)

    _patch(builtins, "open", guarded_open)
    _patch(io, "open", guarded_io_open)
    _patch(os, "open", guarded_os_open)

    def single_path(name: str, original: Any):
        def wrapper(path: Any, *args: Any, **kwargs: Any):
            _require_write_allowed(f"os.{name}", path, dir_fd=kwargs.get("dir_fd"))
            return original(path, *args, **kwargs)

        return wrapper

    for name in ("unlink", "remove", "rmdir", "mkdir", "makedirs"):
        if hasattr(os, name):
            _patch(os, name, single_path(name, getattr(os, name)))

    def two_paths(name: str, original: Any):
        def wrapper(src: Any, dst: Any, *args: Any, **kwargs: Any):
            _require_write_allowed(f"os.{name}.src", src, dir_fd=kwargs.get("src_dir_fd"))
            _require_write_allowed(f"os.{name}.dst", dst, dir_fd=kwargs.get("dst_dir_fd"))
            return original(src, dst, *args, **kwargs)

        return wrapper

    for name in ("rename", "replace", "link", "symlink"):
        if hasattr(os, name):
            _patch(os, name, two_paths(name, getattr(os, name)))


def _child_environment(test_root: Path) -> dict[str, str]:
    return {
        "CUDA_VISIBLE_DEVICES": "-1",
        "PYTHONHASHSEED": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONIOENCODING": "utf-8",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "MATHDEVMCP_P09_TEST_ROOT": str(test_root),
    }


def _validate_cli_contract(
    *,
    argv: Sequence[str],
    cwd: str | os.PathLike[str],
    env: Mapping[str, str],
    input_bytes: bytes,
    timeout: int,
    shell: bool,
    invocation_count: int,
) -> dict[str, Any]:
    expected_argv = [sys.executable, "-I", "-B", str(BOOTSTRAP)]
    if list(argv) != expected_argv or shell is not False:
        raise P09GuardError("guarded CLI argv or shell mode differs from the exact contract")
    if Path(cwd).resolve() != WORKSPACE:
        raise P09GuardError("guarded CLI cwd differs from the workspace")
    if set(env) != CHILD_ENV_KEYS:
        raise P09GuardError("guarded CLI environment keys differ from the minimal contract")
    test_root = Path(env["MATHDEVMCP_P09_TEST_ROOT"])
    if env != _child_environment(test_root):
        raise P09GuardError("guarded CLI environment values differ from the exact contract")
    if timeout != 30 or invocation_count != 0:
        raise P09GuardError("guarded CLI timeout or invocation count differs from the contract")
    if len(input_bytes) > 4096 or not input_bytes:
        raise P09GuardError("guarded CLI stdin exceeds its bound")
    try:
        payload = json.loads(input_bytes.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise P09GuardError("guarded CLI stdin is not JSON") from exc
    if not isinstance(payload, dict) or set(payload) != {
        "artifact_root",
        "collection",
        "page_token",
    } or _canonical(payload) != input_bytes:
        raise P09GuardError("guarded CLI stdin is not the canonical closed schema")
    if payload["collection"] != FIXED_COLLECTION or not isinstance(payload["page_token"], str):
        raise P09GuardError("guarded CLI collection or token is outside the contract")
    if test_root.is_symlink() or not test_root.is_dir():
        raise P09GuardError("guarded CLI pytest root is missing or symlinked")
    artifact_root = Path(payload["artifact_root"])
    if artifact_root.is_symlink() or not artifact_root.is_dir():
        raise P09GuardError("guarded CLI artifact root is missing or symlinked")
    if not _path_under(artifact_root.resolve(), test_root.resolve()):
        raise P09GuardError("guarded CLI artifact root escapes pytest temporary storage")
    return payload


def run_guarded_cli_probe(
    *, page_token: str, artifact_root: Path, test_root: Path
) -> dict[str, Any]:
    global _CLI_INVOCATION_COUNT
    payload = {
        "artifact_root": str(artifact_root),
        "collection": FIXED_COLLECTION,
        "page_token": page_token,
    }
    input_bytes = _canonical(payload)
    env = _child_environment(test_root)
    argv = [sys.executable, "-I", "-B", str(BOOTSTRAP)]
    _validate_cli_contract(
        argv=argv,
        cwd=WORKSPACE,
        env=env,
        input_bytes=input_bytes,
        timeout=30,
        shell=False,
        invocation_count=_CLI_INVOCATION_COUNT,
    )
    _CLI_INVOCATION_COUNT += 1
    process = _ORIGINAL_POPEN(
        argv,
        cwd=WORKSPACE,
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False,
    )
    try:
        stdout, stderr = process.communicate(input=input_bytes, timeout=30)
    except subprocess.TimeoutExpired as exc:
        process.kill()
        process.communicate()
        raise P09GuardError("guarded CLI bootstrap exceeded its fixed timeout") from exc
    if process.returncode != 0 or stderr != b"" or len(stdout) > 8192:
        raise P09GuardError("guarded CLI bootstrap process failed its output contract")
    try:
        result = json.loads(stdout.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise P09GuardError("guarded CLI bootstrap output is not JSON") from exc
    if not isinstance(result, dict) or _canonical(result) + b"\n" != stdout:
        raise P09GuardError("guarded CLI bootstrap output is not canonical")
    child_guard = result.get("guard_attestation")
    if (
        result.get("schema_version") != "p09_guarded_cli_result@2"
        or not isinstance(child_guard, dict)
        or child_guard.get("schema_version") != "p09_child_guard_attestation@1"
        or child_guard.get("attempts") != []
        or child_guard.get("forbidden_attempt_count") != 0
        or child_guard.get("process_attempt_count") != 0
        or child_guard.get("mathematical_backend_attempt_count") != 0
        or child_guard.get("document_audit_invocation_count") != 0
        or child_guard.get("network_attempt_count") != 0
        or child_guard.get("resolved_verb") != "resolve-document-derivation-records"
    ):
        raise P09GuardError("guarded CLI child attestation boundary mismatch")
    _CLI_GUARD_ATTESTATIONS.append(dict(child_guard))
    return result


def guard_attestation() -> dict[str, Any]:
    backend_attempts = sum(
        item["kind"] == "mathematical_backend"
        or (
            item["kind"] == "python_import"
            and item["target"].split(".", 1)[0] in MATHEMATICAL_IMPORT_ROOTS
        )
        for item in _FORBIDDEN_ATTEMPTS
    )
    return {
        "schema_version": "p09_pytest_guard_attestation@2",
        "forbidden_attempt_count": len(_FORBIDDEN_ATTEMPTS),
        "guarded_cli_invocation_count": _CLI_INVOCATION_COUNT,
        "guarded_cli_attestations": list(_CLI_GUARD_ATTESTATIONS),
        "mathematical_backend_attempt_count": backend_attempts,
        "document_audit_invocation_count": sum(
            item["kind"] == "document_audit" for item in _FORBIDDEN_ATTEMPTS
        ),
        "network_attempt_count": sum(
            item["kind"] == "network" for item in _FORBIDDEN_ATTEMPTS
        ),
    }


def _sha256(value: bytes | Any) -> str:
    raw = value if isinstance(value, bytes) else _canonical(value)
    return hashlib.sha256(raw).hexdigest()


def _repo_binding(ref: str) -> dict[str, Any]:
    path = WORKSPACE / ref
    if path.is_symlink() or not path.is_file():
        raise P09GuardError(f"guard attestation code ref is absent or symlinked: {ref}")
    raw = path.read_bytes()
    return {"ref": ref, "sha256": _sha256(raw), "byte_count": len(raw)}


def _guard_code_refs() -> list[str]:
    refs = {
        "pyproject.toml",
        "scripts/run_p08c1_target_fidelity_replay.py",
        "scripts/run_p08d_frozen_payload_replay.py",
        "scripts/run_p09_final_red_team.py",
        "tests/p09_guarded_cli_entry.py",
        "tests/p09_no_live_backend_guard.py",
    }
    refs.update(
        path.relative_to(WORKSPACE).as_posix()
        for path in (WORKSPACE / "src/mathdevmcp").rglob("*.py")
    )
    refs.update(
        path.relative_to(WORKSPACE).as_posix()
        for path in (WORKSPACE / "tests").rglob("*.py")
    )
    fixture_root = WORKSPACE / "tests/fixtures"
    if fixture_root.is_dir() and not fixture_root.is_symlink():
        refs.update(
            path.relative_to(WORKSPACE).as_posix()
            for path in fixture_root.rglob("*")
            if path.is_file()
        )
    return sorted(refs, key=lambda value: value.encode("utf-8"))


def _code_bindings() -> list[dict[str, Any]]:
    return [_repo_binding(ref) for ref in _guard_code_refs()]


def _runtime_identity(*, require_loaded: bool) -> dict[str, Any]:
    expected_origins = {
        "mathdevmcp": str((WORKSPACE / "src/mathdevmcp/__init__.py").resolve()),
        "p09_guard": str(Path(__file__).resolve()),
        "p09_runner": str((WORKSPACE / "scripts/run_p09_final_red_team.py").resolve()),
    }
    if require_loaded:
        runner = _runner_module()
        observed = {
            "mathdevmcp": str(Path(sys.modules["mathdevmcp"].__file__).resolve()),
            "p09_guard": str(Path(__file__).resolve()),
            "p09_runner": str(Path(runner.__file__).resolve()),
        }
        if observed != expected_origins:
            raise P09GuardError("loaded Phase 09 module origins differ from the workspace")
    return {
        "schema_version": "p09_guarded_test_runtime_identity@3",
        "cwd": str(Path.cwd().resolve()),
        "python_executable": sys.executable,
        "python_version": platform.python_version(),
        "pythonpath": os.environ.get("PYTHONPATH"),
        "dont_write_bytecode": sys.dont_write_bytecode,
        "module_origins": expected_origins,
        "root_distribution_versions": {
            name: importlib.metadata.version(name)
            for name in sorted(RUNTIME_DISTRIBUTIONS)
        },
    }


def _install_scoped_execution_guards() -> None:
    for module_name in (
        "mathdevmcp.document_derivation_tree",
        "mathdevmcp.math_document_rigor",
        "mathdevmcp.lean_check",
        "mathdevmcp.sympy_adapter",
        "mathdevmcp.sage_adapter",
        "mathdevmcp.leandojo_backend",
    ):
        __import__(module_name)
    for module_name, module in list(sys.modules.items()):
        if not module_name.startswith("mathdevmcp.") or module is None:
            continue
        for name in DOCUMENT_AUDIT_ENTRY_NAMES:
            if hasattr(module, name):
                _patch(
                    module,
                    name,
                    _blocked_call(f"{module_name}.{name}", kind="document_audit"),
                )
        for name in BACKEND_ENTRY_NAMES:
            if hasattr(module, name):
                _patch(
                    module,
                    name,
                    _blocked_call(f"{module_name}.{name}", kind="mathematical_backend"),
                )


def _runner_module() -> Any:
    for module in sys.modules.values():
        if getattr(module, "__file__", None) == str(WORKSPACE / "scripts/run_p09_final_red_team.py"):
            return module
    raise P09GuardError("Phase 09 runner module was not loaded by the named suite")


def _case_evidence(runner: Any) -> dict[str, Any]:
    records: dict[str, Any] = {}
    collected = set(_COLLECTED_NODEIDS)
    passed = set(_PASSED_NODEIDS)
    for case_id, nodeids in runner.TEST_CASE_NODEIDS.items():
        required = list(nodeids)
        matched = [nodeid for nodeid in required if nodeid in passed]
        records[case_id] = {
            "required_nodeids": required,
            "passed_nodeids": matched,
            "passed": set(required) <= collected and matched == required,
        }
    return records


def _append_unique(values: list[str], nodeid: str) -> None:
    if nodeid not in values:
        values.append(nodeid)


def pytest_runtest_logreport(report: Any) -> None:
    if getattr(report, "wasxfail", None):
        if report.nodeid not in _FAILED_NODEIDS:
            _append_unique(_SKIPPED_NODEIDS, report.nodeid)
        if report.nodeid in _PASSED_NODEIDS:
            _PASSED_NODEIDS.remove(report.nodeid)
        return
    if report.failed:
        _append_unique(_FAILED_NODEIDS, report.nodeid)
        if report.nodeid in _PASSED_NODEIDS:
            _PASSED_NODEIDS.remove(report.nodeid)
        if report.nodeid in _SKIPPED_NODEIDS:
            _SKIPPED_NODEIDS.remove(report.nodeid)
    elif report.skipped:
        if report.nodeid not in _FAILED_NODEIDS:
            _append_unique(_SKIPPED_NODEIDS, report.nodeid)
        if report.nodeid in _PASSED_NODEIDS:
            _PASSED_NODEIDS.remove(report.nodeid)
    elif (
        report.when == "call"
        and report.passed
        and report.nodeid not in _FAILED_NODEIDS
        and report.nodeid not in _SKIPPED_NODEIDS
    ):
        _append_unique(_PASSED_NODEIDS, report.nodeid)


def pytest_collectreport(report: Any) -> None:
    if report.failed:
        _append_unique(_COLLECTION_FAILED_NODEIDS, report.nodeid)
    elif report.skipped:
        _append_unique(_COLLECTION_SKIPPED_NODEIDS, report.nodeid)


def pytest_collection_modifyitems(session: Any, config: Any, items: Sequence[Any]) -> None:
    _COLLECTED_NODEIDS[:] = [item.nodeid for item in items]


def pytest_sessionfinish(session: Any, exitstatus: int) -> None:
    raw_ref = os.environ.get("MATHDEVMCP_P09_TEST_ATTESTATION")
    if not raw_ref:
        return
    destination = Path(raw_ref)
    if not destination.is_absolute():
        destination = WORKSPACE / destination
    expected_parent = WORKSPACE / ".local/mathdevmcp/evidence/p09-20260715/preflight"
    if destination.parent.resolve() != expected_parent.resolve() or destination.suffix != ".json":
        raise P09GuardError("guarded named-suite attestation destination is outside the preflight root")
    if destination.parent.is_symlink() or not destination.parent.is_dir():
        raise P09GuardError("guarded named-suite preflight root is absent or symlinked")
    if destination.exists() or destination.is_symlink():
        raise P09GuardError("guarded named-suite attestation is no-overwrite")
    runner = _runner_module()
    if runner._current_code_refs() != _guard_code_refs():
        raise P09GuardError("guard and runner code-closure definitions differ")
    if _CODE_BINDINGS_START is None or _RUNTIME_IDENTITY_START is None:
        raise P09GuardError("guard start-state identity was not captured")
    code_bindings = _code_bindings()
    runtime_identity = _runtime_identity(require_loaded=True)
    case_evidence = _case_evidence(runner)
    terminal_nodeids = sorted(
        set(_PASSED_NODEIDS) | set(_FAILED_NODEIDS) | set(_SKIPPED_NODEIDS)
    )
    guard = guard_attestation()
    code_unchanged = code_bindings == _CODE_BINDINGS_START
    runtime_unchanged = runtime_identity == _RUNTIME_IDENTITY_START
    record = {
        "schema_version": "p09_guarded_named_suite_attestation@3",
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "pytest_args": list(session.config.invocation_params.args),
        "environment": {
            key: os.environ.get(key)
            for key in (
                "CUDA_VISIBLE_DEVICES",
                "PYTHONHASHSEED",
                "PYTHONDONTWRITEBYTECODE",
                "PYTEST_DISABLE_PLUGIN_AUTOLOAD",
                "PYTHONPATH",
            )
        },
        "runtime_identity": runtime_identity,
        "runtime_identity_unchanged": runtime_unchanged,
        "exit_status": int(exitstatus),
        "all_passed": (
            exitstatus == 0
            and bool(_COLLECTED_NODEIDS)
            and not _FAILED_NODEIDS
            and not _SKIPPED_NODEIDS
            and not _COLLECTION_FAILED_NODEIDS
            and not _COLLECTION_SKIPPED_NODEIDS
            and sorted(_COLLECTED_NODEIDS) == terminal_nodeids
            and code_unchanged
            and runtime_unchanged
            and guard["forbidden_attempt_count"] == 0
            and guard["guarded_cli_invocation_count"] == 1
            and len(guard["guarded_cli_attestations"]) == 1
            and all(item["passed"] for item in case_evidence.values())
        ),
        "collected_nodeids": sorted(_COLLECTED_NODEIDS),
        "passed_nodeids": sorted(_PASSED_NODEIDS),
        "failed_nodeids": sorted(_FAILED_NODEIDS),
        "skipped_nodeids": sorted(_SKIPPED_NODEIDS),
        "collection_failed_nodeids": sorted(_COLLECTION_FAILED_NODEIDS),
        "collection_skipped_nodeids": sorted(_COLLECTION_SKIPPED_NODEIDS),
        "case_evidence": case_evidence,
        "guard_attestation": guard,
        "code_bindings_start": _CODE_BINDINGS_START,
        "code_bindings_end": code_bindings,
        "code_bindings_unchanged": code_unchanged,
        "code_bindings": code_bindings,
        "code_bindings_digest": _sha256(code_bindings),
    }
    record["attestation_digest"] = _sha256(record)
    destination.write_bytes(_canonical(record))


def pytest_configure(config: Any) -> None:
    global _FINDER
    resolved_path = [
        str((Path.cwd() if not item else Path(item)).resolve()) for item in sys.path
    ]
    if (
        Path.cwd().resolve() != WORKSPACE.resolve()
        or os.environ.get("CUDA_VISIBLE_DEVICES") != "-1"
        or os.environ.get("PYTHONHASHSEED") != "0"
        or os.environ.get("PYTHONDONTWRITEBYTECODE") != "1"
        or os.environ.get("PYTEST_DISABLE_PLUGIN_AUTOLOAD") != "1"
        or os.environ.get("PYTHONPATH") != "src"
        or not sys.dont_write_bytecode
        or sys.executable != "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
        or platform.python_version() != "3.11.15"
        or len(resolved_path) < 2
        or resolved_path[0] != str(WORKSPACE.resolve())
        or resolved_path[1] != str((WORKSPACE / "src").resolve())
    ):
        raise P09GuardError("Phase 09 pytest requires CPU-only deterministic startup")
    loaded = sorted(name for name in sys.modules if import_is_forbidden(name))
    if loaded:
        raise P09GuardError(f"blocked packages loaded before Phase 09 guard: {loaded}")
    _FINDER = _BlockedImportFinder()
    sys.meta_path.insert(0, _FINDER)
    blocked_socket = _blocked_socket_class(socket.socket)
    _patch(socket, "socket", blocked_socket)
    if hasattr(socket, "SocketType"):
        _patch(socket, "SocketType", blocked_socket)
    _patch(subprocess, "Popen", _blocked_popen_class(subprocess.Popen))
    for owner, names in (
        (subprocess, PROCESS_FUNCTIONS),
        (os, OS_PROCESS_FUNCTIONS),
        (socket, SOCKET_FUNCTIONS),
    ):
        for name in names:
            if hasattr(owner, name):
                kind = "network" if owner is socket else "process"
                _patch(
                    owner,
                    name,
                    _blocked_call(
                        f"{getattr(owner, '__name__', owner)}.{name}", kind=kind
                    ),
                )


def pytest_sessionstart(session: Any) -> None:
    global _CODE_BINDINGS_START, _PYTEST_TEMP_ROOT, _RUNTIME_IDENTITY_START
    _CODE_BINDINGS_START = _code_bindings()
    _RUNTIME_IDENTITY_START = _runtime_identity(require_loaded=False)
    factory = session.config._tmp_path_factory
    _PYTEST_TEMP_ROOT = factory.getbasetemp().resolve()
    _install_filesystem_guard()
    _install_scoped_execution_guards()


def pytest_unconfigure(config: Any) -> None:
    global _FINDER
    for owner, name, original, replacement in reversed(_PATCHES):
        if getattr(owner, name) is replacement:
            setattr(owner, name, original)
    _PATCHES.clear()
    if _FINDER is not None and _FINDER in sys.meta_path:
        sys.meta_path.remove(_FINDER)
    _FINDER = None
    if _FORBIDDEN_ATTEMPTS:
        raise P09GuardError(
            f"Phase 09 guard recorded {len(_FORBIDDEN_ATTEMPTS)} forbidden attempt(s)"
        )
