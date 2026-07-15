from __future__ import annotations

"""Bounded Sage executable adapter for exact univariate polynomials over QQ."""

import ast
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import selectors
import shutil
import stat
import subprocess
import tempfile
import time
from typing import Any, Callable, Mapping

from .external_adapter_contract import (
    ExternalAdapterContractError,
    build_external_adapter_request,
    build_external_adapter_result,
    validate_external_adapter_request,
)
from .evidence_manifest import content_digest


SAGE_ADAPTER_VERSION = "p05-sage-adapter@3"
SAGE_MANIFEST_SCHEMA = "p05_sage_execution_manifest@3"
SAGE_RESULT_SENTINEL = "MATHDEVMCP_P05_SAGE_RESULT="
SAGE_MAX_EXPRESSION_CHARS = 1_000
SAGE_MAX_AST_NODES = 256
SAGE_MAX_SYNTACTIC_DEGREE = 64
SAGE_MAX_INTEGER_BITS = 256
SAGE_MAX_EXPONENT = 64
SAGE_MAX_SCRATCH_ENTRIES = 2_048
SAGE_MAX_SCRATCH_DEPTH = 32
SAGE_MAX_SCRATCH_PATH_CHARS = 512
SAGE_MAX_MANIFEST_BYTES = 10_485_760
_NAME_CHARS = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_")
_MANIFEST_KEYS = {
    "schema_version",
    "request",
    "request_digest",
    "tool",
    "command",
    "environment",
    "execution",
    "result",
    "artifacts",
    "scratch",
    "non_claims",
    "publication_enabled",
    "manifest_digest",
}
_SAGE_ARTIFACT_ROLES = {
    "input.py": "native_input",
    "stdout.bin": "stdout",
    "stderr.bin": "stderr",
    "result.json": "structured_result",
}
_SAGE_ENVIRONMENT_KEYS = {
    "CUDA_VISIBLE_DEVICES",
    "DOT_SAGE",
    "HOME",
    "LANG",
    "LC_ALL",
    "PATH",
    "PYTHONDONTWRITEBYTECODE",
    "PYTHONNOUSERSITE",
    "TMPDIR",
}
_SAGE_SCRATCH_ROOTS = ("home", "dot-sage", "tmp")


class SageAdapterError(ValueError):
    """Raised for invalid Sage adapter input or evidence."""


@dataclass(frozen=True)
class SagePolynomialObligation:
    branch_id: str
    branch_lineage: tuple[str, ...]
    obligation_digest: str
    target: str
    lhs: str
    rhs: str
    variable: str = "x"
    domain: str = "QQ"


def _canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_identifier(value: str) -> bool:
    return (
        isinstance(value, str)
        and bool(value)
        and value[0].isalpha()
        and all(char in _NAME_CHARS for char in value)
    )


def _parse_polynomial(text: str, variable: str) -> tuple[ast.Expression | None, int, str | None]:
    if not isinstance(text, str) or not text.strip():
        return None, 0, "Polynomial expression must be non-empty."
    if len(text) > SAGE_MAX_EXPRESSION_CHARS:
        return None, 0, f"Polynomial expression exceeds {SAGE_MAX_EXPRESSION_CHARS} characters."
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        return None, 0, f"Invalid polynomial syntax: {exc.msg}."
    nodes = list(ast.walk(tree))
    if len(nodes) > SAGE_MAX_AST_NODES:
        return None, 0, f"Polynomial expression exceeds {SAGE_MAX_AST_NODES} AST nodes."

    def degree(node: ast.AST) -> tuple[int, str | None]:
        if isinstance(node, ast.Expression):
            return degree(node.body)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, int) and not isinstance(node.value, bool):
                if abs(node.value).bit_length() > SAGE_MAX_INTEGER_BITS:
                    return 0, f"Integer literal exceeds {SAGE_MAX_INTEGER_BITS} bits."
                return 0, None
            return 0, "Only integer literals are supported in QQ polynomial input."
        if isinstance(node, ast.Name):
            if node.id == variable:
                return 1, None
            return 0, f"Undeclared polynomial symbol: {node.id}."
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            return degree(node.operand)
        if isinstance(node, ast.BinOp):
            left_degree, left_error = degree(node.left)
            if left_error:
                return 0, left_error
            right_degree, right_error = degree(node.right)
            if right_error:
                return 0, right_error
            if isinstance(node.op, (ast.Add, ast.Sub)):
                return max(left_degree, right_degree), None
            if isinstance(node.op, ast.Mult):
                return left_degree + right_degree, None
            if isinstance(node.op, ast.Div):
                if right_degree != 0:
                    return 0, "QQ polynomial division supports constant denominators only."
                if not isinstance(node.right, ast.Constant) or not isinstance(node.right.value, int):
                    return 0, "QQ polynomial denominators must be nonzero integer literals."
                if node.right.value == 0:
                    return 0, "QQ polynomial denominator cannot be zero."
                return left_degree, None
            if isinstance(node.op, ast.Pow):
                if (
                    not isinstance(node.right, ast.Constant)
                    or not isinstance(node.right.value, int)
                    or isinstance(node.right.value, bool)
                    or node.right.value < 0
                    or node.right.value > SAGE_MAX_EXPONENT
                ):
                    return 0, (
                        "Polynomial exponents must be nonnegative integer literals "
                        f"at most {SAGE_MAX_EXPONENT}."
                    )
                return left_degree * node.right.value, None
            return 0, f"Unsupported polynomial operator: {type(node.op).__name__}."
        return 0, f"Unsupported polynomial construct: {type(node).__name__}."

    polynomial_degree, error = degree(tree)
    if error is not None:
        return None, 0, error
    if polynomial_degree > SAGE_MAX_SYNTACTIC_DEGREE:
        return None, polynomial_degree, (
            f"Syntactic degree {polynomial_degree} exceeds the reviewed bound "
            f"{SAGE_MAX_SYNTACTIC_DEGREE}."
        )
    return tree, polynomial_degree, None


def _sage_source(node: ast.AST, variable: str) -> str:
    if isinstance(node, ast.Expression):
        return _sage_source(node.body, variable)
    if isinstance(node, ast.Constant):
        return f"QQ({node.value})"
    if isinstance(node, ast.Name) and node.id == variable:
        return variable
    if isinstance(node, ast.UnaryOp):
        sign = "+" if isinstance(node.op, ast.UAdd) else "-"
        return f"({sign}{_sage_source(node.operand, variable)})"
    if isinstance(node, ast.BinOp):
        operator = {
            ast.Add: "+",
            ast.Sub: "-",
            ast.Mult: "*",
            ast.Div: "/",
            ast.Pow: "**",
        }[type(node.op)]
        return (
            f"({_sage_source(node.left, variable)} {operator} "
            f"{_sage_source(node.right, variable)})"
        )
    raise SageAdapterError(f"unsupported validated polynomial AST: {type(node).__name__}")


def generate_sage_polynomial_script(
    obligation: SagePolynomialObligation,
    *,
    expected_version_prefix: str = "9.5",
) -> bytes:
    """Generate deterministic Sage code without evaluating user text."""
    if obligation.domain != "QQ":
        raise SageAdapterError(f"unsupported Sage polynomial domain: {obligation.domain}")
    if not _is_identifier(obligation.variable):
        raise SageAdapterError(f"unsupported Sage variable: {obligation.variable!r}")
    if not isinstance(expected_version_prefix, str) or not expected_version_prefix:
        raise SageAdapterError("expected Sage version prefix must be non-empty")
    lhs_tree, lhs_degree, lhs_error = _parse_polynomial(obligation.lhs, obligation.variable)
    rhs_tree, rhs_degree, rhs_error = _parse_polynomial(obligation.rhs, obligation.variable)
    error = lhs_error or rhs_error
    if error is not None:
        raise SageAdapterError(error)
    assert lhs_tree is not None and rhs_tree is not None
    degree_bound = max(lhs_degree, rhs_degree)
    variable_json = json.dumps(obligation.variable, ensure_ascii=True)
    script = f'''from sage.version import version as sage_version
import json

expected_version_prefix = {json.dumps(expected_version_prefix)}
if not str(sage_version).startswith(expected_version_prefix):
    payload = {{
        "schema_version": "p05_sage_polynomial_result@1",
        "status": "unavailable",
        "reason": "Sage version drifted from the pre-registered prefix; polynomial action was not run.",
        "sage_version": str(sage_version),
        "domain": "QQ",
        "variable": {variable_json},
        "input_lhs": {json.dumps(obligation.lhs)},
        "input_rhs": {json.dumps(obligation.rhs)},
        "lhs": "<not-run>",
        "rhs": "<not-run>",
        "difference": "<not-run>",
        "witness": None,
    }}
    print({json.dumps(SAGE_RESULT_SENTINEL)} + json.dumps(payload, sort_keys=True, separators=(",", ":")))
    raise SystemExit(0)

from sage.all import PolynomialRing, QQ

R = PolynomialRing(QQ, names=({variable_json},))
({obligation.variable},) = R._first_ngens(1)
lhs = R({_sage_source(lhs_tree, obligation.variable)})
rhs = R({_sage_source(rhs_tree, obligation.variable)})
difference = lhs - rhs
witness = None
status = "certified" if difference == 0 else "refuted"
reason = "Sage proved exact polynomial equality over QQ." if difference == 0 else "Sage found a concrete QQ evaluation where the polynomials differ."
if difference != 0:
    for candidate in range(0, {degree_bound + 2}):
        point = QQ(candidate)
        lhs_value = lhs(point)
        rhs_value = rhs(point)
        if lhs_value != rhs_value:
            witness = {{"assignment": {{{variable_json}: str(point)}}, "lhs": str(lhs_value), "rhs": str(rhs_value)}}
            break
payload = {{
    "schema_version": "p05_sage_polynomial_result@1",
    "status": status,
    "reason": reason,
    "sage_version": str(sage_version),
    "domain": "QQ",
    "variable": {variable_json},
    "input_lhs": {json.dumps(obligation.lhs)},
    "input_rhs": {json.dumps(obligation.rhs)},
    "lhs": str(lhs),
    "rhs": str(rhs),
    "difference": str(difference),
    "witness": witness,
}}
print({json.dumps(SAGE_RESULT_SENTINEL)} + json.dumps(payload, sort_keys=True, separators=(",", ":")))
'''
    return script.encode("ascii")


def _planned_command(executable: str, script_path: str = "<script.py>") -> list[str]:
    return [executable, "--python", script_path]


def _bounded_subprocess(
    command: list[str],
    *,
    timeout_seconds: float,
    max_output_bytes: int,
    environment: Mapping[str, str],
) -> dict[str, Any]:
    started = _utc_now()
    start_ns = time.monotonic_ns()
    try:
        process = subprocess.Popen(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=dict(environment),
            close_fds=True,
        )
    except OSError as exc:
        return {
            "started_at_utc": started,
            "ended_at_utc": _utc_now(),
            "wall_time_ns": time.monotonic_ns() - start_ns,
            "exit_code": None,
            "timed_out": False,
            "truncated": False,
            "stdout": b"",
            "stderr": str(exc).encode("utf-8", errors="replace")[:max_output_bytes],
            "runner_error": f"{type(exc).__name__}: {exc}",
        }
    assert process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ, "stdout")
    selector.register(process.stderr, selectors.EVENT_READ, "stderr")
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    deadline = time.monotonic() + timeout_seconds
    timed_out = False
    truncated = False
    while selector.get_map():
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            timed_out = True
            process.kill()
            break
        events = selector.select(timeout=min(0.1, remaining))
        for key, _ in events:
            try:
                chunk = os.read(key.fileobj.fileno(), 65_536)
            except BlockingIOError:
                continue
            if not chunk:
                selector.unregister(key.fileobj)
                continue
            buffer = buffers[key.data]
            remaining_bytes = max_output_bytes - sum(len(item) for item in buffers.values())
            buffer.extend(chunk[: max(0, remaining_bytes)])
            if len(chunk) > remaining_bytes:
                truncated = True
                process.kill()
                break
        if truncated:
            break
        if process.poll() is not None and not events:
            # EOF notifications close both registered streams on the next pass.
            continue
    selector.close()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:  # pragma: no cover - defensive cleanup
        process.kill()
        process.wait()
    return {
        "started_at_utc": started,
        "ended_at_utc": _utc_now(),
        "wall_time_ns": time.monotonic_ns() - start_ns,
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "truncated": truncated,
        "stdout": bytes(buffers["stdout"]),
        "stderr": bytes(buffers["stderr"]),
        "runner_error": None,
    }


def _write_new(path: Path, data: bytes) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)


def _read_regular_no_follow(
    path: Path,
    *,
    max_bytes: int | None = None,
    expected_size: int | None = None,
    require_single_link: bool = False,
) -> bytes:
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise SageAdapterError(f"Sage artifact cannot be opened safely: {path.name}: {exc}") from exc
    try:
        metadata = os.fstat(descriptor)
        if not stat.S_ISREG(metadata.st_mode):
            raise SageAdapterError(f"Sage artifact is not a regular file: {path.name}")
        if require_single_link and metadata.st_nlink != 1:
            raise SageAdapterError(f"Sage artifact has multiple hard links: {path.name}")
        if expected_size is not None and metadata.st_size != expected_size:
            raise SageAdapterError(f"Sage artifact size changed before reading: {path.name}")
        if max_bytes is not None and metadata.st_size > max_bytes:
            raise SageAdapterError(f"Sage artifact exceeds its read bound: {path.name}")
        chunks: list[bytes] = []
        observed = 0
        while True:
            chunk = os.read(descriptor, 65_536)
            if not chunk:
                break
            observed += len(chunk)
            if max_bytes is not None and observed > max_bytes:
                raise SageAdapterError(f"Sage artifact grew beyond its read bound: {path.name}")
            chunks.append(chunk)
        data = b"".join(chunks)
        if expected_size is not None and len(data) != expected_size:
            raise SageAdapterError(f"Sage artifact changed during reading: {path.name}")
        return data
    finally:
        os.close(descriptor)


def _execution_environment(run_root: Path, executable: str) -> dict[str, str]:
    home = run_root / "home"
    dotsage = run_root / "dot-sage"
    temporary = run_root / "tmp"
    home.mkdir(mode=0o700)
    dotsage.mkdir(mode=0o700)
    temporary.mkdir(mode=0o700)
    return {
        "PATH": f"{Path(executable).parent}:/usr/bin:/bin",
        "HOME": str(home),
        "DOT_SAGE": str(dotsage),
        "TMPDIR": str(temporary),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "CUDA_VISIBLE_DEVICES": "-1",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }


def _scratch_inventory(root: Path, *, max_file_bytes: int) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    observed_file_bytes = 0
    for scratch_root in _SAGE_SCRATCH_ROOTS:
        base = root / scratch_root
        try:
            metadata = base.lstat()
        except OSError as exc:
            raise SageAdapterError(
                f"Sage scratch root is unavailable: {scratch_root}: {exc}"
            ) from exc
        if not stat.S_ISDIR(metadata.st_mode) or stat.S_ISLNK(metadata.st_mode):
            raise SageAdapterError(f"Sage scratch root is not a real directory: {scratch_root}")
        inventory.append(
            {
                "path": scratch_root,
                "kind": "directory",
                "mode": stat.S_IMODE(metadata.st_mode),
                "byte_count": 0,
                "sha256": None,
            }
        )
        if len(inventory) > SAGE_MAX_SCRATCH_ENTRIES:
            raise SageAdapterError("Sage scratch entry count exceeds its bound")
        pending = [base]
        while pending:
            directory = pending.pop()
            try:
                entries = sorted(directory.iterdir(), key=lambda item: item.name)
            except OSError as exc:
                raise SageAdapterError(
                    f"Sage scratch directory cannot be inventoried: {directory.name}: {exc}"
                ) from exc
            for entry in entries:
                relative = entry.relative_to(root).as_posix()
                parts = Path(relative).parts
                if (
                    len(relative) > SAGE_MAX_SCRATCH_PATH_CHARS
                    or len(parts) - 1 > SAGE_MAX_SCRATCH_DEPTH
                    or any(part in {"", ".", ".."} for part in parts)
                ):
                    raise SageAdapterError(f"Sage scratch path exceeds its bound: {relative}")
                try:
                    item_metadata = entry.lstat()
                except OSError as exc:
                    raise SageAdapterError(
                        f"Sage scratch entry cannot be inspected: {relative}: {exc}"
                    ) from exc
                if stat.S_ISLNK(item_metadata.st_mode):
                    raise SageAdapterError(f"Sage scratch contains a symlink: {relative}")
                mode = stat.S_IMODE(item_metadata.st_mode)
                if stat.S_ISDIR(item_metadata.st_mode):
                    item = {
                        "path": relative,
                        "kind": "directory",
                        "mode": mode,
                        "byte_count": 0,
                        "sha256": None,
                    }
                    pending.append(entry)
                elif stat.S_ISREG(item_metadata.st_mode):
                    if item_metadata.st_nlink != 1:
                        raise SageAdapterError(
                            f"Sage scratch file has multiple hard links: {relative}"
                        )
                    if item_metadata.st_size < 0:
                        raise SageAdapterError(f"Sage scratch file size is invalid: {relative}")
                    observed_file_bytes += item_metadata.st_size
                    if observed_file_bytes > max_file_bytes:
                        raise SageAdapterError("Sage scratch file bytes exceed the artifact limit")
                    data = _read_regular_no_follow(
                        entry,
                        max_bytes=max_file_bytes,
                        expected_size=item_metadata.st_size,
                        require_single_link=True,
                    )
                    item = {
                        "path": relative,
                        "kind": "file",
                        "mode": mode,
                        "byte_count": len(data),
                        "sha256": _sha256(data),
                    }
                else:
                    raise SageAdapterError(
                        f"Sage scratch contains a special file: {relative}"
                    )
                inventory.append(item)
                if len(inventory) > SAGE_MAX_SCRATCH_ENTRIES:
                    raise SageAdapterError("Sage scratch entry count exceeds its bound")
    return sorted(inventory, key=lambda item: item["path"])


def _validate_run_root_layout(
    root: Path, *, sealed: bool, max_artifact_bytes: int
) -> tuple[dict[str, int], list[dict[str, Any]]]:
    expected_files = {"input.py"}
    if sealed:
        expected_files |= {"stdout.bin", "stderr.bin", "result.json", "manifest.json"}
    expected_dirs = set(_SAGE_SCRATCH_ROOTS)
    observed_files: dict[str, int] = {}
    observed_dirs: set[str] = set()
    for entry in root.iterdir():
        metadata = entry.lstat()
        if stat.S_ISLNK(metadata.st_mode):
            raise SageAdapterError(f"Sage run root contains a symlink: {entry.name}")
        if stat.S_ISDIR(metadata.st_mode):
            if entry.name not in expected_dirs:
                raise SageAdapterError(
                    f"Sage run-root layout contains an unexpected directory: {entry.name}"
                )
            observed_dirs.add(entry.name)
        elif stat.S_ISREG(metadata.st_mode):
            if entry.name not in expected_files:
                raise SageAdapterError(
                    f"Sage run-root layout contains an unexpected file: {entry.name}"
                )
            if metadata.st_nlink != 1:
                raise SageAdapterError(
                    f"Sage evidence file has multiple hard links: {entry.name}"
                )
            if metadata.st_size < 0 or metadata.st_size > max_artifact_bytes:
                raise SageAdapterError(f"Sage evidence file exceeds its bound: {entry.name}")
            observed_files[entry.name] = len(
                _read_regular_no_follow(
                    entry,
                    max_bytes=max_artifact_bytes,
                    expected_size=metadata.st_size,
                    require_single_link=True,
                )
            )
        else:
            raise SageAdapterError(f"Sage run root contains a special file: {entry.name}")
    if observed_dirs != expected_dirs or set(observed_files) != expected_files:
        raise SageAdapterError("Sage run-root layout does not match the closed inventory")
    return observed_files, _scratch_inventory(
        root, max_file_bytes=max_artifact_bytes
    )


def _default_runner(
    *,
    executable: str,
    script_bytes: bytes,
    timeout_seconds: float,
    max_output_bytes: int,
    artifact_root: Path,
) -> dict[str, Any]:
    artifact_root.mkdir(parents=True, exist_ok=True, mode=0o700)
    run_root = Path(tempfile.mkdtemp(prefix="sage-run-", dir=artifact_root))
    script_path = run_root / "input.py"
    _write_new(script_path, script_bytes)
    command = _planned_command(executable, str(script_path))
    environment = _execution_environment(run_root, executable)
    result = _bounded_subprocess(
        command,
        timeout_seconds=timeout_seconds,
        max_output_bytes=max_output_bytes,
        environment=environment,
    )
    return {
        **result,
        "command": command,
        "environment": environment,
        "run_root": str(run_root),
    }


def _strict_json(text: str) -> Any:
    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    return json.loads(text, object_pairs_hook=no_duplicates, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def _parse_sage_output(stdout: bytes, expected_version_prefix: str) -> tuple[str, str, dict[str, Any] | None]:
    try:
        text = stdout.decode("utf-8")
    except UnicodeDecodeError:
        return "malformed_output", "Sage stdout was not UTF-8.", None
    lines = text.splitlines()
    if len(lines) != 1 or not lines[0].startswith(SAGE_RESULT_SENTINEL):
        return "malformed_output", "Sage stdout must contain exactly one sentinel result line.", None
    try:
        payload = _strict_json(lines[0][len(SAGE_RESULT_SENTINEL) :])
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        return "malformed_output", f"Sage sentinel JSON was invalid: {exc}.", None
    expected_keys = {
        "schema_version",
        "status",
        "reason",
        "sage_version",
        "domain",
        "variable",
        "input_lhs",
        "input_rhs",
        "lhs",
        "rhs",
        "difference",
        "witness",
    }
    if not isinstance(payload, dict) or set(payload) != expected_keys:
        return "malformed_output", "Sage result keys do not match the closed schema.", None
    if payload["schema_version"] != "p05_sage_polynomial_result@1":
        return "malformed_output", "Sage result schema version is invalid.", None
    if payload["status"] not in {"certified", "refuted", "unavailable"}:
        return "malformed_output", "Sage result status is invalid.", None
    for key in (
        "reason",
        "sage_version",
        "domain",
        "variable",
        "input_lhs",
        "input_rhs",
        "lhs",
        "rhs",
        "difference",
    ):
        if not isinstance(payload[key], str) or not payload[key]:
            return "malformed_output", f"Sage result {key} must be non-empty.", None
    version_matches = payload["sage_version"].startswith(expected_version_prefix)
    if payload["status"] == "unavailable":
        if version_matches or payload["difference"] != "<not-run>" or payload["witness"] is not None:
            return "malformed_output", "Unavailable Sage preflight result is inconsistent.", None
        return "unavailable", payload["reason"], payload
    if not version_matches:
        return "malformed_output", "Executed Sage result version does not match the bound version prefix.", None
    if payload["status"] == "certified":
        if payload["difference"] != "0" or payload["witness"] is not None:
            return "malformed_output", "Certified Sage result has inconsistent difference/witness.", None
    else:
        witness = payload["witness"]
        if not isinstance(witness, dict) or set(witness) != {"assignment", "lhs", "rhs"}:
            return "malformed_output", "Refuted Sage result lacks a concrete evaluation witness.", None
        if not isinstance(witness["assignment"], dict) or len(witness["assignment"]) != 1:
            return "malformed_output", "Sage witness assignment is invalid.", None
        if not all(isinstance(item, str) and item for item in witness.values() if not isinstance(item, dict)):
            return "malformed_output", "Sage witness values must be non-empty strings.", None
        if witness["lhs"] == witness["rhs"]:
            return "malformed_output", "Sage refutation witness does not distinguish lhs and rhs.", None
    return payload["status"], payload["reason"], payload


def _artifact_entry(name: str, data: bytes, role: str) -> dict[str, Any]:
    return {"path": name, "sha256": _sha256(data), "byte_count": len(data), "role": role}


def _seal_manifest(
    *,
    request: Mapping[str, Any],
    raw: Mapping[str, Any],
    script_bytes: bytes,
    payload: Mapping[str, Any],
    status: str,
    non_claims: list[str],
) -> dict[str, str]:
    run_root = Path(str(raw["run_root"]))
    _, scratch_inventory = _validate_run_root_layout(
        run_root,
        sealed=False,
        max_artifact_bytes=request["resource_limits"]["max_artifact_bytes"],
    )
    scratch_file_bytes = sum(
        item["byte_count"] for item in scratch_inventory if item["kind"] == "file"
    )
    stdout = bytes(raw["stdout"])
    stderr = bytes(raw["stderr"])
    result_bytes = _canonical_bytes(payload)
    files = {
        "stdout.bin": stdout,
        "stderr.bin": stderr,
        "result.json": result_bytes,
    }
    for name, data in files.items():
        _write_new(run_root / name, data)
    artifacts = [
        _artifact_entry("input.py", script_bytes, "native_input"),
        _artifact_entry("stdout.bin", stdout, "stdout"),
        _artifact_entry("stderr.bin", stderr, "stderr"),
        _artifact_entry("result.json", result_bytes, "structured_result"),
    ]
    manifest = {
        "schema_version": SAGE_MANIFEST_SCHEMA,
        "request": dict(request),
        "request_digest": request["request_digest"],
        "tool": {
            "name": "sage",
            "adapter_version": SAGE_ADAPTER_VERSION,
            "reported_version": payload["sage_version"],
            "requested_executable": request["tool"]["requested_executable"],
            "resolved_executable": request["tool"]["resolved_executable"],
        },
        "command": list(raw["command"]),
        "environment": {
            key: raw["environment"][key]
            for key in (
                "CUDA_VISIBLE_DEVICES",
                "DOT_SAGE",
                "HOME",
                "LANG",
                "LC_ALL",
                "PATH",
                "PYTHONDONTWRITEBYTECODE",
                "PYTHONNOUSERSITE",
                "TMPDIR",
            )
        },
        "execution": {
            "started_at_utc": raw["started_at_utc"],
            "ended_at_utc": raw["ended_at_utc"],
            "wall_time_ns": raw["wall_time_ns"],
            "exit_code": raw["exit_code"],
            "timed_out": raw["timed_out"],
            "truncated": raw["truncated"],
        },
        "result": {"status": status, "payload_sha256": _sha256(result_bytes)},
        "artifacts": artifacts,
        "scratch": {
            "roots": list(_SAGE_SCRATCH_ROOTS),
            "limits": {
                "max_entries": SAGE_MAX_SCRATCH_ENTRIES,
                "max_depth": SAGE_MAX_SCRATCH_DEPTH,
                "max_path_chars": SAGE_MAX_SCRATCH_PATH_CHARS,
            },
            "entry_count": len(scratch_inventory),
            "file_bytes": scratch_file_bytes,
            "inventory": scratch_inventory,
        },
        "non_claims": list(non_claims),
        "publication_enabled": False,
    }
    manifest["manifest_digest"] = _sha256(_canonical_bytes(manifest))
    manifest_bytes = _canonical_bytes(manifest)
    total_artifact_bytes = sum(
        len(item)
        for item in (script_bytes, stdout, stderr, result_bytes, manifest_bytes)
    )
    total_artifact_bytes += scratch_file_bytes
    if total_artifact_bytes > request["resource_limits"]["max_artifact_bytes"]:
        raise SageAdapterError("Sage artifact bundle exceeds the request artifact limit")
    _write_new(run_root / "manifest.json", manifest_bytes)
    verified = verify_sage_execution_manifest(run_root / "manifest.json")
    return {
        "manifest_ref": str(run_root / "manifest.json"),
        "manifest_sha256": verified["manifest_sha256"],
    }


def verify_sage_execution_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    if not manifest_path.is_absolute() or manifest_path.name != "manifest.json":
        raise SageAdapterError("Sage manifest must be an absolute manifest.json path")
    root = manifest_path.parent
    if root.is_symlink() or not root.is_dir():
        raise SageAdapterError("Sage manifest run root must be a real directory")
    raw = _read_regular_no_follow(
        manifest_path,
        max_bytes=SAGE_MAX_MANIFEST_BYTES,
        require_single_link=True,
    )
    try:
        value = _strict_json(raw.decode("utf-8"))
    except (UnicodeDecodeError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SageAdapterError(f"Sage manifest is not strict UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict) or set(value) != _MANIFEST_KEYS:
        raise SageAdapterError("Sage manifest keys do not match the closed schema")
    if raw != _canonical_bytes(value):
        raise SageAdapterError("Sage manifest JSON is not canonical")
    if value["schema_version"] != SAGE_MANIFEST_SCHEMA:
        raise SageAdapterError("Sage manifest schema version is invalid")
    request = validate_external_adapter_request(value["request"])
    if value["request_digest"] != request["request_digest"]:
        raise SageAdapterError("Sage manifest request binding mismatch")
    if request["tool"]["name"] != "sage" or request["tool"]["adapter_version"] != SAGE_ADAPTER_VERSION:
        raise SageAdapterError("Sage manifest request names the wrong tool or adapter")
    if request["native_input_media_type"] != "text/x-python":
        raise SageAdapterError("Sage manifest request native-input media type is invalid")
    typed_assumptions = request["typed_assumptions"]
    if len(typed_assumptions) != 1:
        raise SageAdapterError("Sage request typed domain assumption is invalid")
    domain_assumption = typed_assumptions[0]
    if (
        set(domain_assumption) != {"id", "kind", "symbol", "domain"}
        or domain_assumption.get("kind") != "domain"
        or not _is_identifier(domain_assumption.get("symbol"))
        or domain_assumption.get("domain") != "QQ"
        or domain_assumption.get("id")
        != f"domain_{domain_assumption.get('symbol')}"
    ):
        raise SageAdapterError("Sage request typed domain assumption is invalid")
    if value["publication_enabled"] is not False:
        raise SageAdapterError("Sage manifest publication must remain disabled")
    if value["non_claims"] != request["unsupported_conclusions"]:
        raise SageAdapterError("Sage manifest non-claims do not match the request")
    without_digest = dict(value)
    digest = without_digest.pop("manifest_digest")
    if digest != _sha256(_canonical_bytes(without_digest)):
        raise SageAdapterError("Sage manifest digest mismatch")

    tool = value["tool"]
    if not isinstance(tool, dict) or set(tool) != {
        "name",
        "adapter_version",
        "reported_version",
        "requested_executable",
        "resolved_executable",
    }:
        raise SageAdapterError("Sage manifest tool record is invalid")
    if (
        tool["name"] != "sage"
        or tool["adapter_version"] != SAGE_ADAPTER_VERSION
        or tool["requested_executable"] != request["tool"]["requested_executable"]
        or tool["resolved_executable"] != request["tool"]["resolved_executable"]
    ):
        raise SageAdapterError("Sage manifest tool identity does not match the request")
    expected_prefix_field = request["tool"]["backend_version"]
    if not expected_prefix_field.startswith("expected_prefix:"):
        raise SageAdapterError("Sage request has no bound expected-version prefix")
    expected_version_prefix = expected_prefix_field.removeprefix("expected_prefix:")
    if not expected_version_prefix or not isinstance(tool["reported_version"], str):
        raise SageAdapterError("Sage manifest expected/reported version is invalid")

    observed_layout, observed_scratch = _validate_run_root_layout(
        root,
        sealed=True,
        max_artifact_bytes=request["resource_limits"]["max_artifact_bytes"],
    )
    scratch = value["scratch"]
    expected_scratch_limits = {
        "max_entries": SAGE_MAX_SCRATCH_ENTRIES,
        "max_depth": SAGE_MAX_SCRATCH_DEPTH,
        "max_path_chars": SAGE_MAX_SCRATCH_PATH_CHARS,
    }
    if not isinstance(scratch, dict) or set(scratch) != {
        "roots",
        "limits",
        "entry_count",
        "file_bytes",
        "inventory",
    }:
        raise SageAdapterError("Sage manifest scratch record is invalid")
    observed_scratch_bytes = sum(
        item["byte_count"] for item in observed_scratch if item["kind"] == "file"
    )
    expected_scratch = {
        "roots": list(_SAGE_SCRATCH_ROOTS),
        "limits": expected_scratch_limits,
        "entry_count": len(observed_scratch),
        "file_bytes": observed_scratch_bytes,
        "inventory": observed_scratch,
    }
    if _canonical_bytes(scratch) != _canonical_bytes(expected_scratch):
        raise SageAdapterError("Sage manifest scratch inventory mismatch")
    if (
        sum(observed_layout.values()) + observed_scratch_bytes
        > request["resource_limits"]["max_artifact_bytes"]
    ):
        raise SageAdapterError("Sage artifact bundle exceeds the request artifact limit")
    artifacts = value["artifacts"]
    if not isinstance(artifacts, list) or [item.get("path") for item in artifacts if isinstance(item, dict)] != list(_SAGE_ARTIFACT_ROLES):
        raise SageAdapterError("Sage manifest artifact inventory order is invalid")
    artifact_bytes: dict[str, bytes] = {}
    seen: set[str] = set()
    for artifact in artifacts:
        if not isinstance(artifact, dict) or set(artifact) != {"path", "sha256", "byte_count", "role"}:
            raise SageAdapterError("Sage manifest artifact entry is invalid")
        name = artifact["path"]
        if name in seen or name not in _SAGE_ARTIFACT_ROLES:
            raise SageAdapterError("Sage manifest artifact path is invalid")
        if artifact["role"] != _SAGE_ARTIFACT_ROLES[name]:
            raise SageAdapterError(f"Sage manifest artifact role mismatch: {name}")
        seen.add(name)
        data = _read_regular_no_follow(
            root / name,
            max_bytes=request["resource_limits"]["max_artifact_bytes"],
            expected_size=observed_layout[name],
            require_single_link=True,
        )
        if len(data) != artifact["byte_count"] or _sha256(data) != artifact["sha256"]:
            raise SageAdapterError(f"Sage artifact digest mismatch: {name}")
        artifact_bytes[name] = data
    if seen != set(_SAGE_ARTIFACT_ROLES):
        raise SageAdapterError("Sage manifest artifact inventory is incomplete")
    if _sha256(artifact_bytes["input.py"]) != request["native_input_digest"]:
        raise SageAdapterError("Sage script does not match the request native input")
    if len(artifact_bytes["stdout.bin"]) + len(artifact_bytes["stderr.bin"]) > request["resource_limits"]["max_output_bytes"]:
        raise SageAdapterError("Sage aggregate output exceeds the request output limit")

    command = value["command"]
    resolved = value["tool"]["resolved_executable"]
    expected_script = str(root / "input.py")
    if (
        not isinstance(command, list)
        or len(command) != 3
        or os.path.realpath(command[0]) != os.path.realpath(resolved)
        or command[1] != "--python"
        or os.path.realpath(command[2]) != os.path.realpath(expected_script)
    ):
        raise SageAdapterError("Sage manifest command/executable mismatch")
    environment = value["environment"]
    if not isinstance(environment, dict) or set(environment) != _SAGE_ENVIRONMENT_KEYS:
        raise SageAdapterError("Sage manifest environment allowlist is invalid")
    expected_environment = {
        "PATH": f"{Path(tool['requested_executable']).parent}:/usr/bin:/bin",
        "HOME": str(root / "home"),
        "DOT_SAGE": str(root / "dot-sage"),
        "TMPDIR": str(root / "tmp"),
        "PYTHONNOUSERSITE": "1",
        "PYTHONDONTWRITEBYTECODE": "1",
        "CUDA_VISIBLE_DEVICES": "-1",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
    }
    if environment != expected_environment:
        raise SageAdapterError("Sage manifest environment does not match the bounded allowlist")
    for directory_name in ("home", "dot-sage", "tmp"):
        directory = root / directory_name
        if directory.is_symlink() or not directory.is_dir():
            raise SageAdapterError(f"Sage bounded environment directory is invalid: {directory_name}")

    execution = value["execution"]
    if not isinstance(execution, dict) or set(execution) != {
        "started_at_utc",
        "ended_at_utc",
        "wall_time_ns",
        "exit_code",
        "timed_out",
        "truncated",
    }:
        raise SageAdapterError("Sage manifest execution record is invalid")
    for key in ("started_at_utc", "ended_at_utc"):
        try:
            datetime.strptime(execution[key], "%Y-%m-%dT%H:%M:%SZ")
        except (TypeError, ValueError) as exc:
            raise SageAdapterError(f"Sage execution {key} is invalid") from exc
    if execution["ended_at_utc"] < execution["started_at_utc"]:
        raise SageAdapterError("Sage execution time ordering is invalid")
    if not isinstance(execution["wall_time_ns"], int) or isinstance(execution["wall_time_ns"], bool) or execution["wall_time_ns"] < 0:
        raise SageAdapterError("Sage execution wall_time_ns is invalid")
    if type(execution["timed_out"]) is not bool or type(execution["truncated"]) is not bool:
        raise SageAdapterError("Sage execution timeout/truncation flags are invalid")
    if execution["timed_out"] or execution["truncated"]:
        raise SageAdapterError("A timed-out or truncated Sage run cannot verify")
    if execution["exit_code"] != 0:
        raise SageAdapterError("A nonzero Sage run cannot verify")

    result_record = value["result"]
    if not isinstance(result_record, dict) or set(result_record) != {"status", "payload_sha256"}:
        raise SageAdapterError("Sage manifest result record is invalid")
    try:
        payload = _strict_json(artifact_bytes["result.json"].decode("utf-8"))
    except (UnicodeDecodeError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise SageAdapterError(f"Sage structured result is invalid: {exc}") from exc
    if not isinstance(payload, dict) or artifact_bytes["result.json"] != _canonical_bytes(payload):
        raise SageAdapterError("Sage structured result is not canonical JSON")
    parsed_status, _, stdout_payload = _parse_sage_output(
        artifact_bytes["stdout.bin"], expected_version_prefix
    )
    if stdout_payload is None or stdout_payload != payload:
        raise SageAdapterError("Sage stdout and structured result payloads differ")
    if (
        result_record["status"] != parsed_status
        or result_record["status"] not in {"certified", "refuted"}
        or result_record["payload_sha256"] != _sha256(artifact_bytes["result.json"])
    ):
        raise SageAdapterError("Sage manifest result status/payload binding mismatch")
    if tool["reported_version"] != payload["sage_version"] or not tool["reported_version"].startswith(expected_version_prefix):
        raise SageAdapterError("Sage manifest reported version does not match the result or prefix")
    if (
        payload["domain"] != domain_assumption["domain"]
        or payload["variable"] != domain_assumption["symbol"]
    ):
        raise SageAdapterError(
            "Sage payload domain/variable does not match the request typed domain assumption"
        )
    executed_target = " ".join(
        f"{payload['input_lhs']} = {payload['input_rhs']}".split()
    )
    if executed_target != request["normalized_target"]:
        raise SageAdapterError("Sage payload input sides do not match the request target")
    expected_obligation = SagePolynomialObligation(
        branch_id=request["branch_id"],
        branch_lineage=tuple(request["branch_lineage"]),
        obligation_digest=request["obligation_digest"],
        target=request["normalized_target"],
        lhs=payload["input_lhs"],
        rhs=payload["input_rhs"],
        variable=domain_assumption["symbol"],
        domain=domain_assumption["domain"],
    )
    expected_script = generate_sage_polynomial_script(
        expected_obligation,
        expected_version_prefix=expected_version_prefix,
    )
    if artifact_bytes["input.py"] != expected_script:
        raise SageAdapterError(
            "Sage script is not the deterministic encoding of the verified request"
        )
    encoded_assumption_digest = content_digest(domain_assumption)
    script_digest = _sha256(expected_script)
    return {
        "integrity_state": "verified",
        "manifest_ref": str(manifest_path),
        "manifest_sha256": _sha256(raw),
        "manifest": value,
        "payload": payload,
        "artifact_digests": {
            name: {"sha256": _sha256(data), "byte_count": len(data)}
            for name, data in artifact_bytes.items()
        },
        "encoded_assumption_digests": [encoded_assumption_digest],
        "assumption_encoding_evidence_refs": [
            f"{manifest_path}#input.py:{script_digest}"
        ],
        "scratch_inventory": observed_scratch,
    }


def _nonexecuted_result(
    *,
    request: Mapping[str, Any],
    status: str,
    reason: str,
) -> dict[str, Any]:
    return build_external_adapter_result(
        request=request,
        status=status,
        reason=reason,
        execution={
            "kind": "not_run",
            "runner_id": SAGE_ADAPTER_VERSION,
            "command": [],
            "executable_path": None,
            "resolved_executable_path": None,
            "exit_code": None,
            "timed_out": False,
            "stdout_bytes": 0,
            "stderr_bytes": 0,
            "stdout_sha256": _sha256(b""),
            "stderr_sha256": _sha256(b""),
        },
        evidence_kind="diagnostic",
        evidence_details=None,
        output_ref=None,
        manifest_ref=None,
        manifest_sha256=None,
        manifest_verified=False,
        refutation_witness=None,
        next_discriminator="Repair preflight or translation before any Sage process is launched.",
        non_claims=list(request["unsupported_conclusions"]),
    )


def run_sage_polynomial_obligation(
    obligation: SagePolynomialObligation,
    *,
    executable: str | None = None,
    expected_version_prefix: str = "9.5",
    timeout_seconds: float = 30.0,
    max_output_bytes: int = 1_048_576,
    max_artifact_bytes: int = 10_485_760,
    artifact_root: str | Path | None = None,
    runner: Callable[..., Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Execute or fake-run one exact Sage polynomial obligation."""
    requested = executable or os.environ.get("MATHDEVMCP_SAGE_PATH") or shutil.which("sage")
    resolved = os.path.realpath(requested) if requested and Path(requested).is_file() else None
    expected_target = " ".join(f"{obligation.lhs} = {obligation.rhs}".split())
    actual_target = " ".join(obligation.target.split())
    try:
        if actual_target != expected_target:
            raise SageAdapterError(
                "Normalized target does not exactly match the encoded lhs = rhs."
            )
        script_bytes = generate_sage_polynomial_script(
            obligation, expected_version_prefix=expected_version_prefix
        )
        translation_error = None
    except SageAdapterError as exc:
        script_bytes = _canonical_bytes(
            {
                "schema_version": "p05_sage_translation_failure@1",
                "lhs": obligation.lhs,
                "rhs": obligation.rhs,
                "variable": obligation.variable,
                "domain": obligation.domain,
            }
        )
        translation_error = str(exc)
    request = build_external_adapter_request(
        branch_id=obligation.branch_id,
        branch_lineage=obligation.branch_lineage,
        obligation_digest=obligation.obligation_digest,
        normalized_target=obligation.target,
        typed_assumptions=[
            {
                "id": f"domain_{obligation.variable}",
                "kind": "domain",
                "symbol": obligation.variable,
                "domain": obligation.domain,
            }
        ],
        native_input_bytes=script_bytes,
        native_input_media_type="text/x-python",
        tool_name="sage",
        adapter_version=SAGE_ADAPTER_VERSION,
        backend_version=f"expected_prefix:{expected_version_prefix}",
        requested_executable=requested,
        resolved_executable=resolved,
        timeout_ms=max(1, int(timeout_seconds * 1_000)),
        max_output_bytes=max_output_bytes,
        max_artifact_bytes=max_artifact_bytes,
        expected_result_class="exact_univariate_polynomial_identity_over_QQ",
        backend_role="scoped_specialist_certificate",
        unsupported_conclusions=(
            "no_multivariate_or_nonpolynomial_claim",
            "no_domain_beyond_QQ",
            "no_general_sage_soundness",
            "no_real_document_repair_capability",
            "no_publication",
        ),
    )
    if translation_error is not None:
        return _nonexecuted_result(
            request=request, status="unsupported", reason=translation_error
        )
    if requested is None or resolved is None:
        return _nonexecuted_result(
            request=request,
            status="unavailable",
            reason="The requested Sage executable is unavailable.",
        )
    if artifact_root is None and runner is None:
        return _nonexecuted_result(
            request=request,
            status="execution_error",
            reason="A bounded artifact_root is required for live Sage execution.",
        )

    planned = _planned_command(requested)
    try:
        raw_value = (
            runner(
                executable=requested,
                resolved_executable=resolved,
                command=planned,
                script_bytes=script_bytes,
                timeout_seconds=timeout_seconds,
                max_output_bytes=max_output_bytes,
            )
            if runner is not None
            else _default_runner(
                executable=requested,
                script_bytes=script_bytes,
                timeout_seconds=timeout_seconds,
                max_output_bytes=max_output_bytes,
                artifact_root=Path(artifact_root),
            )
        )
    except TimeoutError:
        raw_value = {"timed_out": True, "stdout": b"", "stderr": b"", "exit_code": None}
    except Exception as exc:
        raw_value = {
            "runner_error": f"{type(exc).__name__}: {exc}",
            "timed_out": False,
            "stdout": b"",
            "stderr": b"",
            "exit_code": None,
        }
    if not isinstance(raw_value, Mapping):
        raw_value = {"malformed": True, "stdout": b"", "stderr": b"", "exit_code": None}
    raw = dict(raw_value)
    stdout = raw.get("stdout", b"")
    stderr = raw.get("stderr", b"")
    if not isinstance(stdout, bytes) or not isinstance(stderr, bytes):
        stdout, stderr = b"", b""
        status, reason, payload = "malformed_output", "Sage runner streams must be bytes.", None
    elif len(stdout) + len(stderr) > max_output_bytes or raw.get("truncated") is True:
        status, reason, payload = "truncated_output", "Sage output exceeded the bound.", None
        stdout = stdout[:max_output_bytes]
        stderr = stderr[: max(0, max_output_bytes - len(stdout))]
    elif raw.get("timed_out") is True:
        status, reason, payload = "timeout", "Sage execution exceeded the timeout.", None
    elif raw.get("runner_error") or raw.get("exit_code") not in {0, None}:
        status, reason, payload = "execution_error", (
            str(raw.get("runner_error"))
            if raw.get("runner_error")
            else f"Sage exited with code {raw.get('exit_code')}."
        ), None
    elif raw.get("exit_code") is None and runner is None:
        status, reason, payload = "execution_error", "Live Sage execution returned no exit code.", None
    else:
        status, reason, payload = _parse_sage_output(stdout, expected_version_prefix)
        if payload is not None and (
            payload["domain"] != obligation.domain
            or payload["variable"] != obligation.variable
            or payload["input_lhs"] != obligation.lhs
            or payload["input_rhs"] != obligation.rhs
        ):
            status, reason, payload = "malformed_output", "Sage output domain/variable binding mismatch.", None

    fake = runner is not None
    if not fake and raw.get("runner_error") and raw.get("exit_code") is None:
        return _nonexecuted_result(
            request=request,
            status="execution_error",
            reason=f"Sage process did not launch: {raw['runner_error']}",
        )
    manifest_ref = manifest_sha256 = None
    manifest_verified = False
    if not fake and status in {"certified", "refuted"} and payload is not None:
        nonclaims = list(request["unsupported_conclusions"])
        try:
            sealed = _seal_manifest(
                request=request,
                raw=raw,
                script_bytes=script_bytes,
                payload=payload,
                status=status,
                non_claims=nonclaims,
            )
        except Exception as exc:
            # The subprocess already ran; sealing failures must retain that provenance.
            status = "execution_error"
            reason = (
                "Sage completed, but its evidence manifest could not be sealed and "
                f"verified: {type(exc).__name__}: {exc}"
            )
            payload = None
        else:
            manifest_ref = sealed["manifest_ref"]
            manifest_sha256 = sealed["manifest_sha256"]
            manifest_verified = True
    execution = {
        "kind": "fake_runner" if fake else "subprocess",
        "runner_id": "injected_sage_runner" if fake else SAGE_ADAPTER_VERSION,
        "command": [] if fake else list(raw.get("command", [])),
        "executable_path": None if fake else requested,
        "resolved_executable_path": None if fake else resolved,
        "exit_code": None if fake else raw.get("exit_code"),
        "timed_out": bool(raw.get("timed_out")) if not fake else False,
        "stdout_bytes": len(stdout),
        "stderr_bytes": len(stderr),
        "stdout_sha256": _sha256(stdout),
        "stderr_sha256": _sha256(stderr),
    }
    output_ref = manifest_ref if manifest_verified else (
        f"mathdevmcp://sage/fake/{_sha256(stdout)}" if fake and status in {"certified", "refuted"} else None
    )
    witness = payload.get("witness") if status == "refuted" and payload is not None else None
    try:
        return build_external_adapter_result(
            request=request,
            status=status,
            reason=reason,
            execution=execution,
            evidence_kind=(
                "sage_polynomial_identity"
                if status == "certified"
                else "sage_concrete_evaluation"
                if status == "refuted"
                else "diagnostic"
            ),
            evidence_details=payload if isinstance(payload, Mapping) else None,
            output_ref=output_ref,
            manifest_ref=manifest_ref,
            manifest_sha256=manifest_sha256,
            manifest_verified=manifest_verified,
            refutation_witness=witness,
            next_discriminator=(
                "No further discriminator is claimed; inspect the exact Sage manifest."
                if status in {"certified", "refuted"}
                else "Repair the executable, translation, or process result before another specialist rung."
            ),
            non_claims=list(request["unsupported_conclusions"]),
        )
    except ExternalAdapterContractError as exc:
        return _nonexecuted_result(
            request=request,
            status="malformed_output",
            reason=f"Sage evidence failed the external adapter contract: {exc}",
        )
