from __future__ import annotations

"""Closed, non-promoting SymPy derivative construction contract for Phase 08."""

import ast
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import stat
import sys
from typing import Any, Mapping


SYMPY_DERIVATIVE_ADAPTER_VERSION = "p08-sympy-derivative-adapter@1"
SYMPY_DERIVATIVE_OPERATION = "construct_scalar_derivative_then_compare"
SYMPY_DERIVATIVE_REQUEST_SCHEMA = "p08_sympy_derivative_request@1"
SYMPY_DERIVATIVE_WORKER_SCHEMA = "p08_sympy_derivative_worker_output@1"
SYMPY_DERIVATIVE_RESULT_SCHEMA = "p08_sympy_derivative_result@1"
SYMPY_DERIVATIVE_STATUSES = frozenset(
    {
        "backend_checked",
        "source_target_mismatch",
        "unsupported",
        "unavailable",
        "execution_error",
        "timeout",
        "malformed_output",
        "truncated_output",
    }
)
MAX_EXPRESSION_CHARS = 1_000
MAX_AST_NODES = 256
REGISTERED_EXPRESSION = "bp/(1 + rt) + tau*rt*bp/((1 + rt)*(1 + r))"
REGISTERED_EXPECTED_DERIVATIVE = "bp/(1 + rt)**2 * (-1 + tau/(1 + r))"
REGISTERED_WORKER_PROJECTION_SHA256 = (
    "2c1aea968e5166840a3cb3a6d58c6a5c5954dca7f810a1d7a8e4940682c2b1f0"
)
REGISTERED_WORKER_PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
REGISTERED_WORKER_PYTHON_FLAGS = (
    "-I",
    "-S",
    "-B",
    "-X",
    "pycache_prefix=/dev/null",
)
SYMPY_EXPECTED_VERSION = "1.14.0"
SYMPY_SITE_PACKAGES = "/home/chakwong/miniconda3/envs/tfgpu/lib/python3.11/site-packages"
SYMPY_EXPECTED_ORIGIN = SYMPY_SITE_PACKAGES + "/sympy/__init__.py"
SYMPY_EXPECTED_ORIGIN_SHA256 = (
    "4e9476348ba105feab28d82f5bcf6cdba2e3e84de6e059bbfe7a13728c0a4ab0"
)
SYMPY_EXPECTED_PACKAGE_FILE_COUNT = 1570
SYMPY_EXPECTED_PACKAGE_BYTE_COUNT = 26924280
SYMPY_EXPECTED_PACKAGE_SHA256 = (
    "af117224ea4e7fa1b33489def2aa1d925914cb30468dc0f6624b14d8ff46a00e"
)
MPMATH_EXPECTED_VERSION = "1.3.0"
MPMATH_EXPECTED_ORIGIN = SYMPY_SITE_PACKAGES + "/mpmath/__init__.py"
MPMATH_EXPECTED_ORIGIN_SHA256 = (
    "b241584d2c1fc0304b0a1015ea923749d7b0800411dd406dcab7c82bf25d9fe8"
)
MPMATH_EXPECTED_PACKAGE_FILE_COUNT = 94
MPMATH_EXPECTED_PACKAGE_BYTE_COUNT = 1955297
MPMATH_EXPECTED_PACKAGE_SHA256 = (
    "b073444f164f541e9ae5c0a84003a1dfce6199465a93e3435ece58cba2e8f12c"
)
REGISTERED_WORKER_ENVIRONMENT = {
    "CUDA_VISIBLE_DEVICES": "-1",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
}
_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_SAFE_BINARY = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)
_SAFE_UNARY = (ast.UAdd, ast.USub)
_REQUEST_KEYS = {
    "schema_version",
    "adapter_version",
    "operation",
    "candidate_id",
    "source_obligations",
    "expression",
    "expected_derivative",
    "differentiated_variable",
    "symbols",
    "held_constant",
    "typed_assumptions",
    "resource_limits",
    "unsupported_conclusions",
    "request_digest",
}
_WORKER_KEYS = {
    "schema_version",
    "adapter_version",
    "operation",
    "request_digest",
    "sympy_version",
    "sympy_site_packages",
    "sympy_origin",
    "sympy_origin_sha256",
    "sympy_package_file_count",
    "sympy_package_byte_count",
    "sympy_package_sha256",
    "mpmath_version",
    "mpmath_origin",
    "mpmath_origin_sha256",
    "mpmath_package_file_count",
    "mpmath_package_byte_count",
    "mpmath_package_sha256",
    "site_packages_module_roots",
    "constructed_derivative",
    "constructed_derivative_srepr",
    "source_target",
    "source_target_srepr",
    "difference",
    "difference_srepr",
    "denominator_factors",
    "typed_assumptions",
}
_WORKER_PROJECTION_KEYS = (
    "sympy_version",
    "sympy_site_packages",
    "sympy_origin",
    "sympy_origin_sha256",
    "sympy_package_file_count",
    "sympy_package_byte_count",
    "sympy_package_sha256",
    "mpmath_version",
    "mpmath_origin",
    "mpmath_origin_sha256",
    "mpmath_package_file_count",
    "mpmath_package_byte_count",
    "mpmath_package_sha256",
    "site_packages_module_roots",
    "constructed_derivative",
    "constructed_derivative_srepr",
    "source_target",
    "source_target_srepr",
    "difference",
    "difference_srepr",
    "denominator_factors",
)


class SympyDerivativeContractError(ValueError):
    """Raised when a Phase 08 derivative record is not closed."""


def _tree_identity(site_packages: Path, roots: tuple[str, ...]) -> tuple[int, int, str]:
    """Hash the actual reviewed trees while excluding unusable cache files."""
    try:
        site = site_packages.resolve(strict=True)
        records: list[tuple[str, str, bytes | None]] = []
        file_count = 0
        byte_count = 0
        for root_name in roots:
            root = site / root_name
            root.relative_to(site)
            pending = [root]
            while pending:
                path = pending.pop()
                status = path.lstat()
                relative = path.relative_to(site).as_posix()
                relative_in_root = path.relative_to(root)
                in_cache = "__pycache__" in relative_in_root.parts
                if stat.S_ISLNK(status.st_mode):
                    raise SympyDerivativeContractError(
                        f"reviewed backend tree contains a symlink: {relative}"
                    )
                if stat.S_ISDIR(status.st_mode):
                    if in_cache and path.name != "__pycache__":
                        raise SympyDerivativeContractError(
                            f"reviewed backend cache contains a directory: {relative}"
                        )
                    if not in_cache:
                        records.append(("directory", relative, None))
                    pending.extend(sorted(path.iterdir(), key=lambda item: item.name, reverse=True))
                    continue
                if not stat.S_ISREG(status.st_mode):
                    raise SympyDerivativeContractError(
                        f"reviewed backend tree contains a special file: {relative}"
                    )
                if in_cache:
                    if path.suffix != ".pyc" or status.st_mode & 0o111:
                        raise SympyDerivativeContractError(
                            f"reviewed backend cache contains an unexpected file: {relative}"
                        )
                    continue
                if path.suffix in {".pyc", ".pyo"}:
                    raise SympyDerivativeContractError(
                        f"reviewed backend tree contains legacy executable bytecode: {relative}"
                    )
                if status.st_mode & 0o111:
                    raise SympyDerivativeContractError(
                        f"reviewed backend tree contains an unexpected executable file: {relative}"
                    )
                raw = path.read_bytes()
                records.append(("file", relative, raw))
                file_count += 1
                byte_count += len(raw)
        tree_hash = hashlib.sha256()
        for kind, relative, raw in sorted(records, key=lambda item: item[1]):
            if kind == "directory":
                tree_hash.update(b"D\0" + relative.encode("utf-8") + b"\0")
                continue
            assert raw is not None
            tree_hash.update(
                b"F\0"
                + relative.encode("utf-8")
                + b"\0"
                + len(raw).to_bytes(8, "big")
                + hashlib.sha256(raw).digest()
            )
        return file_count, byte_count, tree_hash.hexdigest()
    except SympyDerivativeContractError:
        raise
    except (OSError, ValueError, UnicodeError) as exc:
        raise SympyDerivativeContractError("reviewed backend tree is unavailable") from exc


def _expected_backend_provenance() -> dict[str, Any]:
    try:
        site = Path(SYMPY_SITE_PACKAGES).resolve(strict=True)
        expected = {
            "sympy": (SYMPY_EXPECTED_VERSION, "sympy-1.14.0.dist-info"),
            "mpmath": (MPMATH_EXPECTED_VERSION, "mpmath-1.3.0.dist-info"),
        }
        by_name: dict[str, list[Any]] = {name: [] for name in expected}
        for distribution in importlib.metadata.distributions(path=[site.as_posix()]):
            name = (distribution.metadata.get("Name") or "").lower()
            if name in by_name:
                by_name[name].append(distribution)
        for name, (version, dist_info) in expected.items():
            distributions = by_name[name]
            if len(distributions) != 1:
                raise SympyDerivativeContractError(
                    f"pinned site-packages does not contain exactly one {name} distribution"
                )
            distribution = distributions[0]
            if distribution.version != version:
                raise SympyDerivativeContractError(
                    f"installed {name} distribution version differs from the reviewed version"
                )
            if Path(distribution._path).resolve() != (site / dist_info).resolve():
                raise SympyDerivativeContractError(
                    f"installed {name} metadata origin differs from the reviewed tree"
                )
        sympy_origin = (site / "sympy/__init__.py").resolve(strict=True)
        mpmath_origin = (site / "mpmath/__init__.py").resolve(strict=True)
        if sympy_origin.as_posix() != SYMPY_EXPECTED_ORIGIN:
            raise SympyDerivativeContractError("SymPy origin differs from the pinned path")
        if mpmath_origin.as_posix() != MPMATH_EXPECTED_ORIGIN:
            raise SympyDerivativeContractError("mpmath origin differs from the pinned path")
        sympy_origin_sha256 = hashlib.sha256(sympy_origin.read_bytes()).hexdigest()
        mpmath_origin_sha256 = hashlib.sha256(mpmath_origin.read_bytes()).hexdigest()
        if sympy_origin_sha256 != SYMPY_EXPECTED_ORIGIN_SHA256:
            raise SympyDerivativeContractError("SymPy origin digest differs from the reviewed bytes")
        if mpmath_origin_sha256 != MPMATH_EXPECTED_ORIGIN_SHA256:
            raise SympyDerivativeContractError("mpmath origin digest differs from the reviewed bytes")
        sympy_identity = _tree_identity(site, ("sympy", "sympy-1.14.0.dist-info"))
        mpmath_identity = _tree_identity(site, ("mpmath", "mpmath-1.3.0.dist-info"))
        if sympy_identity != (
            SYMPY_EXPECTED_PACKAGE_FILE_COUNT,
            SYMPY_EXPECTED_PACKAGE_BYTE_COUNT,
            SYMPY_EXPECTED_PACKAGE_SHA256,
        ):
            raise SympyDerivativeContractError("SymPy tree differs from the reviewed bytes")
        if mpmath_identity != (
            MPMATH_EXPECTED_PACKAGE_FILE_COUNT,
            MPMATH_EXPECTED_PACKAGE_BYTE_COUNT,
            MPMATH_EXPECTED_PACKAGE_SHA256,
        ):
            raise SympyDerivativeContractError("mpmath tree differs from the reviewed bytes")
    except (importlib.metadata.PackageNotFoundError, OSError) as exc:
        raise SympyDerivativeContractError("reviewed backend provenance is unavailable") from exc
    return {
        "sympy_site_packages": site.as_posix(),
        "sympy_origin": sympy_origin.as_posix(),
        "sympy_origin_sha256": sympy_origin_sha256,
        "sympy_package_file_count": sympy_identity[0],
        "sympy_package_byte_count": sympy_identity[1],
        "sympy_package_sha256": sympy_identity[2],
        "mpmath_origin": mpmath_origin.as_posix(),
        "mpmath_origin_sha256": mpmath_origin_sha256,
        "mpmath_package_file_count": mpmath_identity[0],
        "mpmath_package_byte_count": mpmath_identity[1],
        "mpmath_package_sha256": mpmath_identity[2],
    }


def _import_pinned_sympy() -> Any:
    provenance = _expected_backend_provenance()
    site_packages = provenance["sympy_site_packages"]
    if site_packages not in sys.path:
        sys.path.append(site_packages)
    import sympy as sp

    if Path(sp.__file__).resolve().as_posix() != provenance["sympy_origin"]:
        raise SympyDerivativeContractError("imported SymPy does not come from the pinned distribution")
    return sp


def _site_packages_module_roots(*, strict: bool) -> list[str]:
    site = Path(SYMPY_SITE_PACKAGES).resolve()
    roots: set[str] = set()
    for module in sys.modules.values():
        module_file = getattr(module, "__file__", None)
        if not isinstance(module_file, str):
            continue
        try:
            relative = Path(module_file).resolve().relative_to(site)
        except (OSError, ValueError):
            continue
        root = relative.parts[0] if relative.parts else ""
        if root not in {"sympy", "mpmath"}:
            if strict:
                raise SympyDerivativeContractError(
                    f"unreviewed site-packages module entered the worker: {root or '<root>'}"
                )
            continue
        if relative.suffix in {".pyc", ".pyo"}:
            raise SympyDerivativeContractError(
                f"reviewed backend module loaded from bytecode: {relative.as_posix()}"
            )
        roots.add(root)
    if roots != {"sympy", "mpmath"}:
        raise SympyDerivativeContractError("worker did not load the complete reviewed dependency roots")
    return sorted(roots)


def _require_registered_worker_runtime() -> None:
    if (
        sys.executable != REGISTERED_WORKER_PYTHON
        or sys.flags.isolated != 1
        or sys.flags.no_site != 1
        or sys.flags.no_user_site != 1
        or sys.flags.ignore_environment != 1
        or sys.flags.safe_path is not True
        or sys.flags.dont_write_bytecode != 1
        or sys.pycache_prefix != "/dev/null"
        or not Path("/dev/null").is_char_device()
    ):
        raise SympyDerivativeContractError("worker runtime is not isolated and source-only")
    site = Path(SYMPY_SITE_PACKAGES).resolve()
    for entry in sys.path:
        try:
            if Path(entry).resolve() == site:
                raise SympyDerivativeContractError(
                    "pinned site-packages entered sys.path before provenance validation"
                )
        except OSError:
            continue


def canonical_json_bytes(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise SympyDerivativeContractError("value is not canonical JSON data") from exc


def _digest(value: Any) -> str:
    raw = bytes(value) if isinstance(value, (bytes, bytearray, memoryview)) else canonical_json_bytes(value)
    return hashlib.sha256(raw).hexdigest()


def derivative_capability_descriptor() -> dict[str, Any]:
    return {
        "adapter_version": SYMPY_DERIVATIVE_ADAPTER_VERSION,
        "operation": SYMPY_DERIVATIVE_OPERATION,
        "request_schema": SYMPY_DERIVATIVE_REQUEST_SCHEMA,
        "worker_output_schema": SYMPY_DERIVATIVE_WORKER_SCHEMA,
        "result_schema": SYMPY_DERIVATIVE_RESULT_SCHEMA,
        "status_registry": sorted(SYMPY_DERIVATIVE_STATUSES),
        "imports_sympy_at_module_import": False,
        "can_promote": False,
        "publication_enabled": False,
    }


def _validate_expression(text: Any, names: set[str], label: str) -> str:
    if not isinstance(text, str) or not text or len(text) > MAX_EXPRESSION_CHARS:
        raise SympyDerivativeContractError(f"{label} must be a bounded non-empty expression")
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        raise SympyDerivativeContractError(f"{label} is invalid scalar syntax") from exc
    nodes = list(ast.walk(tree))
    if len(nodes) > MAX_AST_NODES:
        raise SympyDerivativeContractError(f"{label} exceeds the AST-node limit")
    for node in nodes:
        if isinstance(node, (ast.Expression, ast.Load, *_SAFE_BINARY, *_SAFE_UNARY)):
            continue
        if isinstance(node, ast.BinOp):
            if not isinstance(node.op, _SAFE_BINARY):
                raise SympyDerivativeContractError(f"{label} has an unsupported binary operator")
            if isinstance(node.op, ast.Pow):
                exponent = node.right
                if not (
                    isinstance(exponent, ast.Constant)
                    and isinstance(exponent.value, int)
                    and not isinstance(exponent.value, bool)
                    or isinstance(exponent, ast.UnaryOp)
                    and isinstance(exponent.op, (ast.UAdd, ast.USub))
                    and isinstance(exponent.operand, ast.Constant)
                    and isinstance(exponent.operand.value, int)
                    and not isinstance(exponent.operand.value, bool)
                ):
                    raise SympyDerivativeContractError(f"{label} powers require integer literals")
            continue
        if isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, _SAFE_UNARY):
                raise SympyDerivativeContractError(f"{label} has an unsupported unary operator")
            continue
        if isinstance(node, ast.Name):
            if node.id not in names:
                raise SympyDerivativeContractError(f"{label} has undeclared symbol {node.id!r}")
            continue
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, int) or isinstance(node.value, bool):
                raise SympyDerivativeContractError(f"{label} supports integer literals only")
            continue
        raise SympyDerivativeContractError(f"{label} has unsupported syntax {type(node).__name__}")
    return text


def _closed_symbols(value: Any) -> list[dict[str, str]]:
    if not isinstance(value, list) or len(value) != 4:
        raise SympyDerivativeContractError("symbols must declare exactly four real scalars")
    records = []
    for item in value:
        if not isinstance(item, Mapping) or set(item) != {"name", "domain", "role"}:
            raise SympyDerivativeContractError("symbol record schema mismatch")
        name = item.get("name")
        if not isinstance(name, str) or not _NAME.fullmatch(name):
            raise SympyDerivativeContractError("invalid symbol name")
        if item.get("domain") != "real" or item.get("role") not in {"differentiated", "held_constant"}:
            raise SympyDerivativeContractError("symbol domain/role mismatch")
        records.append(dict(item))
    if [item["name"] for item in records] != ["bp", "r", "rt", "tau"]:
        raise SympyDerivativeContractError("symbol order/names differ from the registered request")
    if [item["name"] for item in records if item["role"] == "differentiated"] != ["rt"]:
        raise SympyDerivativeContractError("exactly rt must be differentiated")
    return records


def _closed_assumptions(value: Any) -> list[dict[str, Any]]:
    expected = [
        {"id": "real_scalars", "kind": "domain", "symbols": ["bp", "r", "rt", "tau"], "domain": "real"},
        {"id": "nonzero_one_plus_r", "kind": "nonzero_polynomial", "expression": "1 + r"},
        {"id": "nonzero_one_plus_rt", "kind": "nonzero_polynomial", "expression": "1 + rt"},
        {
            "id": "differentiable_in_rt",
            "kind": "differentiability",
            "expression": "bp/(1 + rt) + tau*rt*bp/((1 + rt)*(1 + r))",
            "variable": "rt",
            "domain": "real_where_registered_denominators_nonzero",
        },
    ]
    if value != expected:
        raise SympyDerivativeContractError("typed assumptions differ from the registered exact set")
    return [dict(item) for item in expected]


def build_derivative_request(
    *,
    source_expression_obligation_digest: str,
    source_target_obligation_digest: str,
    timeout_seconds: int = 10,
    max_output_bytes: int = 262_144,
    max_artifact_bytes: int = 1_048_576,
) -> dict[str, Any]:
    request = {
        "schema_version": SYMPY_DERIVATIVE_REQUEST_SCHEMA,
        "adapter_version": SYMPY_DERIVATIVE_ADAPTER_VERSION,
        "operation": SYMPY_DERIVATIVE_OPERATION,
        "candidate_id": "eq:cashflow-rate-derivative",
        "source_obligations": {
            "expression": source_expression_obligation_digest,
            "target": source_target_obligation_digest,
        },
        "expression": REGISTERED_EXPRESSION,
        "expected_derivative": REGISTERED_EXPECTED_DERIVATIVE,
        "differentiated_variable": "rt",
        "symbols": [
            {"name": "bp", "domain": "real", "role": "held_constant"},
            {"name": "r", "domain": "real", "role": "held_constant"},
            {"name": "rt", "domain": "real", "role": "differentiated"},
            {"name": "tau", "domain": "real", "role": "held_constant"},
        ],
        "held_constant": ["bp", "r", "tau"],
        "typed_assumptions": [
            {"id": "real_scalars", "kind": "domain", "symbols": ["bp", "r", "rt", "tau"], "domain": "real"},
            {"id": "nonzero_one_plus_r", "kind": "nonzero_polynomial", "expression": "1 + r"},
            {"id": "nonzero_one_plus_rt", "kind": "nonzero_polynomial", "expression": "1 + rt"},
            {
                "id": "differentiable_in_rt",
                "kind": "differentiability",
                "expression": REGISTERED_EXPRESSION,
                "variable": "rt",
                "domain": "real_where_registered_denominators_nonzero",
            },
        ],
        "resource_limits": {
            "timeout_seconds": timeout_seconds,
            "max_input_bytes": 262_144,
            "max_stdout_bytes": max_output_bytes,
            "max_stderr_bytes": max_output_bytes,
            "max_artifact_bytes": max_artifact_bytes,
            "bundle_overhead_bytes": 16_384,
        },
        "unsupported_conclusions": [
            "no_formal_proof",
            "no_general_cas_soundness",
            "no_whole_document_correctness",
            "no_publication",
            "no_p04_promotion",
        ],
    }
    request["request_digest"] = _digest(request)
    return validate_derivative_request(request)


def validate_derivative_request(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != _REQUEST_KEYS:
        raise SympyDerivativeContractError("derivative request keys mismatch")
    request = dict(value)
    if request["schema_version"] != SYMPY_DERIVATIVE_REQUEST_SCHEMA:
        raise SympyDerivativeContractError("derivative request schema mismatch")
    if request["adapter_version"] != SYMPY_DERIVATIVE_ADAPTER_VERSION or request["operation"] != SYMPY_DERIVATIVE_OPERATION:
        raise SympyDerivativeContractError("derivative adapter version/operation mismatch")
    if request["candidate_id"] != "eq:cashflow-rate-derivative":
        raise SympyDerivativeContractError("derivative candidate mismatch")
    source = request["source_obligations"]
    if not isinstance(source, Mapping) or set(source) != {"expression", "target"}:
        raise SympyDerivativeContractError("source obligation binding mismatch")
    if any(not isinstance(item, str) or not re.fullmatch(r"[0-9a-f]{64}", item) for item in source.values()):
        raise SympyDerivativeContractError("source obligation digest is invalid")
    symbols = _closed_symbols(request["symbols"])
    names = {item["name"] for item in symbols}
    _validate_expression(request["expression"], names, "expression")
    _validate_expression(request["expected_derivative"], names, "expected_derivative")
    if request["expression"] != REGISTERED_EXPRESSION or request["expected_derivative"] != REGISTERED_EXPECTED_DERIVATIVE:
        raise SympyDerivativeContractError("expressions differ from the pre-registered candidate")
    if request["differentiated_variable"] != "rt" or request["held_constant"] != ["bp", "r", "tau"]:
        raise SympyDerivativeContractError("variable or held-constant binding mismatch")
    _closed_assumptions(request["typed_assumptions"])
    limits = request["resource_limits"]
    if limits != {
        "timeout_seconds": 10,
        "max_input_bytes": 262_144,
        "max_stdout_bytes": 262_144,
        "max_stderr_bytes": 262_144,
        "max_artifact_bytes": 1_048_576,
        "bundle_overhead_bytes": 16_384,
    }:
        raise SympyDerivativeContractError("resource limits differ from the reviewed exact values")
    if request["unsupported_conclusions"] != [
        "no_formal_proof",
        "no_general_cas_soundness",
        "no_whole_document_correctness",
        "no_publication",
        "no_p04_promotion",
    ]:
        raise SympyDerivativeContractError("unsupported conclusions mismatch")
    expected = _digest({key: child for key, child in request.items() if key != "request_digest"})
    if request["request_digest"] != expected:
        raise SympyDerivativeContractError("derivative request digest mismatch")
    if len(canonical_json_bytes(request)) > limits["max_input_bytes"]:
        raise SympyDerivativeContractError("derivative request exceeds input limit")
    return request


def _integer_literal(node: ast.AST) -> int | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, int) and not isinstance(node.value, bool):
        return node.value
    if (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, (ast.UAdd, ast.USub))
        and isinstance(node.operand, ast.Constant)
        and isinstance(node.operand.value, int)
        and not isinstance(node.operand.value, bool)
    ):
        return node.operand.value if isinstance(node.op, ast.UAdd) else -node.operand.value
    return None


def _ast_to_sympy(node: ast.AST, local: Mapping[str, Any], sp: Any) -> Any:
    if isinstance(node, ast.Expression):
        return _ast_to_sympy(node.body, local, sp)
    if isinstance(node, ast.Constant):
        return sp.Integer(node.value)
    if isinstance(node, ast.Name):
        return local[node.id]
    if isinstance(node, ast.UnaryOp):
        value = _ast_to_sympy(node.operand, local, sp)
        return value if isinstance(node.op, ast.UAdd) else sp.Mul(sp.Integer(-1), value, evaluate=False)
    if isinstance(node, ast.BinOp):
        left = _ast_to_sympy(node.left, local, sp)
        right = _ast_to_sympy(node.right, local, sp)
        if isinstance(node.op, ast.Add):
            return sp.Add(left, right, evaluate=False)
        if isinstance(node.op, ast.Sub):
            return sp.Add(left, sp.Mul(sp.Integer(-1), right, evaluate=False), evaluate=False)
        if isinstance(node.op, ast.Mult):
            return sp.Mul(left, right, evaluate=False)
        if isinstance(node.op, ast.Div):
            return sp.Mul(left, sp.Pow(right, sp.Integer(-1), evaluate=False), evaluate=False)
        if isinstance(node.op, ast.Pow):
            exponent = _integer_literal(node.right)
            if exponent is None:
                raise SympyDerivativeContractError("validated power lost integer exponent")
            return sp.Pow(left, sp.Integer(exponent), evaluate=False)
    raise SympyDerivativeContractError("validated AST cannot be translated")


def _normalized_factor_base(poly_expr: Any, r: Any, rt: Any, sp: Any) -> tuple[Any, str]:
    poly = sp.Poly(poly_expr, r, rt, domain=sp.QQ)
    if poly.total_degree() <= 0:
        raise SympyDerivativeContractError("registered factor must be nonconstant")
    monic = sp.Poly(poly.monic(), r, rt, domain=sp.QQ).as_expr()
    expanded = sp.expand(monic)
    return expanded, sp.srepr(expanded)


def _denominator_factors(expression: Any, r: Any, rt: Any, sp: Any) -> list[dict[str, Any]]:
    denominator = sp.together(expression, deep=True).as_numer_denom()[1]
    polynomial = sp.Poly(denominator, r, rt, domain=sp.QQ)
    _unit, factors = sp.factor_list(polynomial)
    records = []
    for factor, multiplicity in factors:
        base, identity = _normalized_factor_base(factor.as_expr(), r, rt, sp)
        records.append(
            {
                "base": str(base),
                "base_srepr": identity,
                "multiplicity": int(multiplicity),
            }
        )
    records.sort(key=lambda item: item["base_srepr"])
    return records


def compute_worker_record(
    request: Mapping[str, Any], *, enforce_worker_runtime: bool = False
) -> dict[str, Any]:
    """Execute the registered SymPy operation; caller owns process isolation."""
    validated = validate_derivative_request(request)
    if enforce_worker_runtime:
        _require_registered_worker_runtime()
    sp = _import_pinned_sympy()

    symbols = {name: sp.Symbol(name, real=True) for name in ("bp", "r", "rt", "tau")}
    expression = _ast_to_sympy(ast.parse(validated["expression"], mode="eval"), symbols, sp)
    constructed = sp.diff(expression, symbols["rt"])
    target = _ast_to_sympy(ast.parse(validated["expected_derivative"], mode="eval"), symbols, sp)
    difference = sp.simplify(constructed - target)
    registered = []
    for item in validated["typed_assumptions"]:
        if item["kind"] != "nonzero_polynomial":
            continue
        factor = _ast_to_sympy(ast.parse(item["expression"], mode="eval"), symbols, sp)
        base, identity = _normalized_factor_base(factor, symbols["r"], symbols["rt"], sp)
        registered.append({"base": str(base), "base_srepr": identity})
    registered.sort(key=lambda item: item["base_srepr"])
    if len({item["base_srepr"] for item in registered}) != 2:
        raise SympyDerivativeContractError("registered nonzero assumptions are not bijective")
    factors = {
        "expression": _denominator_factors(expression, symbols["r"], symbols["rt"], sp),
        "constructed_derivative": _denominator_factors(constructed, symbols["r"], symbols["rt"], sp),
        "source_target": _denominator_factors(target, symbols["r"], symbols["rt"], sp),
        "registered_nonzero": registered,
    }
    registered_ids = {item["base_srepr"] for item in registered}
    expression_ids = {item["base_srepr"] for item in factors["expression"]}
    constructed_ids = {item["base_srepr"] for item in factors["constructed_derivative"]}
    target_ids = {item["base_srepr"] for item in factors["source_target"]}
    if expression_ids != registered_ids or not constructed_ids <= registered_ids or not target_ids <= registered_ids:
        raise SympyDerivativeContractError("denominator factors do not match registered assumptions")
    provenance = _expected_backend_provenance()
    module_roots = _site_packages_module_roots(strict=enforce_worker_runtime)
    mpmath = sys.modules.get("mpmath")
    if (
        mpmath is None
        or getattr(mpmath, "__version__", None) != MPMATH_EXPECTED_VERSION
        or Path(getattr(mpmath, "__file__", "")).resolve().as_posix()
        != provenance["mpmath_origin"]
    ):
        raise SympyDerivativeContractError("imported mpmath does not match reviewed provenance")
    return {
        "schema_version": SYMPY_DERIVATIVE_WORKER_SCHEMA,
        "adapter_version": SYMPY_DERIVATIVE_ADAPTER_VERSION,
        "operation": SYMPY_DERIVATIVE_OPERATION,
        "request_digest": validated["request_digest"],
        "sympy_version": sp.__version__,
        **provenance,
        "mpmath_version": mpmath.__version__,
        "site_packages_module_roots": module_roots,
        "constructed_derivative": str(constructed),
        "constructed_derivative_srepr": sp.srepr(constructed),
        "source_target": str(target),
        "source_target_srepr": sp.srepr(target),
        "difference": str(difference),
        "difference_srepr": sp.srepr(difference),
        "denominator_factors": factors,
        "typed_assumptions": validated["typed_assumptions"],
    }


def validate_worker_record(value: Any, request: Mapping[str, Any]) -> dict[str, Any]:
    validated_request = validate_derivative_request(request)
    if not isinstance(value, Mapping) or set(value) != _WORKER_KEYS:
        raise SympyDerivativeContractError("worker record keys mismatch")
    record = dict(value)
    if record["schema_version"] != SYMPY_DERIVATIVE_WORKER_SCHEMA:
        raise SympyDerivativeContractError("worker schema mismatch")
    if record["adapter_version"] != SYMPY_DERIVATIVE_ADAPTER_VERSION or record["operation"] != SYMPY_DERIVATIVE_OPERATION:
        raise SympyDerivativeContractError("worker adapter binding mismatch")
    if record["request_digest"] != validated_request["request_digest"]:
        raise SympyDerivativeContractError("worker request binding mismatch")
    if (
        record["sympy_version"] != SYMPY_EXPECTED_VERSION
        or record["mpmath_version"] != MPMATH_EXPECTED_VERSION
    ):
        raise SympyDerivativeContractError("worker tool version differs from the reviewed versions")
    if (
        record["sympy_site_packages"] != SYMPY_SITE_PACKAGES
        or
        not isinstance(record["sympy_origin"], str)
        or record["sympy_origin"] != SYMPY_EXPECTED_ORIGIN
        or not re.fullmatch(r"[0-9a-f]{64}", record["sympy_origin_sha256"])
    ):
        raise SympyDerivativeContractError("worker SymPy provenance is malformed")
    expected_provenance = _expected_backend_provenance()
    if any(record[key] != expected for key, expected in expected_provenance.items()):
        raise SympyDerivativeContractError(
            "worker SymPy/mpmath provenance differs from the reviewed trees"
        )
    if record["site_packages_module_roots"] != ["mpmath", "sympy"]:
        raise SympyDerivativeContractError("worker dependency closure differs from the reviewed roots")
    for key in (
        "constructed_derivative",
        "constructed_derivative_srepr",
        "source_target",
        "source_target_srepr",
        "difference",
        "difference_srepr",
    ):
        if not isinstance(record[key], str) or not record[key]:
            raise SympyDerivativeContractError(f"worker field is invalid: {key}")
    if record["typed_assumptions"] != validated_request["typed_assumptions"]:
        raise SympyDerivativeContractError("worker assumption projection mismatch")
    factors = record["denominator_factors"]
    if not isinstance(factors, Mapping) or set(factors) != {
        "expression",
        "constructed_derivative",
        "source_target",
        "registered_nonzero",
    }:
        raise SympyDerivativeContractError("worker denominator-factor schema mismatch")
    r_id = "Add(Symbol('r', real=True), Integer(1))"
    rt_id = "Add(Symbol('rt', real=True), Integer(1))"
    expected_factor_sets = {
        "expression": [(r_id, 1), (rt_id, 1)],
        "constructed_derivative": [(r_id, 2), (rt_id, 2)],
        "source_target": [(r_id, 1), (rt_id, 2)],
    }
    for lane, expected in expected_factor_sets.items():
        values = factors[lane]
        if (
            not isinstance(values, list)
            or any(not isinstance(item, Mapping) or set(item) != {"base", "base_srepr", "multiplicity"} for item in values)
            or sorted((item["base_srepr"], item["multiplicity"]) for item in values) != expected
            or any(not isinstance(item["base"], str) or not item["base"] for item in values)
        ):
            raise SympyDerivativeContractError(f"worker denominator factors mismatch: {lane}")
    registered = factors["registered_nonzero"]
    if (
        not isinstance(registered, list)
        or any(not isinstance(item, Mapping) or set(item) != {"base", "base_srepr"} for item in registered)
        or sorted(item["base_srepr"] for item in registered) != [r_id, rt_id]
        or any(not isinstance(item["base"], str) or not item["base"] for item in registered)
    ):
        raise SympyDerivativeContractError("worker registered nonzero factors mismatch")
    if record["constructed_derivative_srepr"] == record["source_target_srepr"]:
        raise SympyDerivativeContractError("construction and source-target records must remain distinct")
    projection = {key: record[key] for key in _WORKER_PROJECTION_KEYS}
    if _digest(projection) != REGISTERED_WORKER_PROJECTION_SHA256:
        raise SympyDerivativeContractError(
            "worker projection differs from the registered SymPy 1.14 known answer"
        )
    return record


def worker_record_bytes(record: Mapping[str, Any], request: Mapping[str, Any]) -> bytes:
    return canonical_json_bytes(validate_worker_record(record, request)) + b"\n"


def parse_worker_stdout(raw: bytes, request: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, bytes) or not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise SympyDerivativeContractError("worker stdout must contain exactly one LF-terminated object")
    body = raw[:-1]
    try:
        value = json.loads(body.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SympyDerivativeContractError("worker stdout is invalid JSON") from exc
    record = validate_worker_record(value, request)
    if canonical_json_bytes(record) != body:
        raise SympyDerivativeContractError("worker stdout is not canonical JSON")
    return record


def build_derivative_result(
    *,
    request: Mapping[str, Any],
    worker_record: Mapping[str, Any] | None,
    native_input: bytes,
    stdout: bytes,
    stderr: bytes,
    execution: Mapping[str, Any],
    failure_status: str | None = None,
    failure_reason: str | None = None,
) -> dict[str, Any]:
    validated_request = validate_derivative_request(request)
    if native_input != canonical_json_bytes(validated_request):
        raise SympyDerivativeContractError("native input differs from the canonical request")
    if failure_status is None:
        if worker_record is None:
            raise SympyDerivativeContractError("successful result requires a worker record")
        record = validate_worker_record(worker_record, validated_request)
        if stdout != worker_record_bytes(record, validated_request):
            raise SympyDerivativeContractError("stdout differs from the canonical worker record")
        status = "backend_checked" if record["difference_srepr"] == "Integer(0)" else "source_target_mismatch"
        reason = (
            "SymPy constructed the scoped derivative and the independent exact comparison returned zero."
            if status == "backend_checked"
            else "SymPy constructed the derivative but it did not match the exact source target."
        )
    else:
        if failure_status not in SYMPY_DERIVATIVE_STATUSES - {"backend_checked", "source_target_mismatch"}:
            raise SympyDerivativeContractError("invalid derivative failure status")
        status = failure_status
        reason = failure_reason or "The derivative worker did not produce usable evidence."
        record = None
    result = {
        "schema_version": SYMPY_DERIVATIVE_RESULT_SCHEMA,
        "status": status,
        "reason": reason,
        "request": validated_request,
        "execution": dict(execution),
        "raw_bindings": {
            "native-input.json": {"sha256": _digest(native_input), "byte_count": len(native_input)},
            "stdout.bin": {"sha256": _digest(stdout), "byte_count": len(stdout)},
            "stderr.bin": {"sha256": _digest(stderr), "byte_count": len(stderr)},
        },
        "worker_record": record,
        "claim_class": (
            "backend_checked_computational_support" if status == "backend_checked" else "no_mathematical_evidence"
        ),
        "can_promote": False,
        "publication_enabled": False,
        "formal_proof_certified": False,
        "non_claims": list(validated_request["unsupported_conclusions"]),
        "boundary": "Separate Phase 08 computational-support schema; not accepted by P05/P04 promotion and not proof or publication authority.",
    }
    result["result_digest"] = _digest(result)
    return validate_derivative_result(result)


def validate_derivative_result(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise SympyDerivativeContractError("derivative result must be an object")
    result = dict(value)
    expected_keys = {
        "schema_version",
        "status",
        "reason",
        "request",
        "execution",
        "raw_bindings",
        "worker_record",
        "claim_class",
        "can_promote",
        "publication_enabled",
        "formal_proof_certified",
        "non_claims",
        "boundary",
        "result_digest",
    }
    if set(result) != expected_keys or result["schema_version"] != SYMPY_DERIVATIVE_RESULT_SCHEMA:
        raise SympyDerivativeContractError("derivative result schema/keys mismatch")
    if result["status"] not in SYMPY_DERIVATIVE_STATUSES:
        raise SympyDerivativeContractError("unknown derivative result status")
    request = validate_derivative_request(result["request"])
    if result["worker_record"] is not None:
        validate_worker_record(result["worker_record"], request)
    if result["status"] in {"backend_checked", "source_target_mismatch"} and result["worker_record"] is None:
        raise SympyDerivativeContractError("mathematical worker status requires a worker record")
    if result["status"] == "backend_checked" and result["worker_record"]["difference_srepr"] != "Integer(0)":
        raise SympyDerivativeContractError("backend_checked requires exact zero difference")
    expected_claim = "backend_checked_computational_support" if result["status"] == "backend_checked" else "no_mathematical_evidence"
    if result["claim_class"] != expected_claim:
        raise SympyDerivativeContractError("derivative claim class mismatch")
    if result["can_promote"] is not False or result["publication_enabled"] is not False or result["formal_proof_certified"] is not False:
        raise SympyDerivativeContractError("derivative result crossed its authority boundary")
    execution = result["execution"]
    execution_keys = {
        "kind",
        "runner_id",
        "command",
        "executable",
        "environment",
        "exit_code",
        "timed_out",
        "overflow",
        "wall_time_ms",
        "live_tool_executed",
        "run_id",
        "run_binding_digest",
        "code_identity_digest",
    }
    if not isinstance(execution, Mapping) or set(execution) != execution_keys:
        raise SympyDerivativeContractError("derivative execution schema mismatch")
    if result["status"] in {"backend_checked", "source_target_mismatch"}:
        if (
            execution["kind"] != "subprocess"
            or execution["runner_id"] != SYMPY_DERIVATIVE_ADAPTER_VERSION
            or execution["live_tool_executed"] is not True
            or execution["exit_code"] != 0
            or execution["timed_out"] is not False
            or execution["overflow"] is not False
        ):
            raise SympyDerivativeContractError("worker-backed status requires a clean live subprocess")
    if not isinstance(execution["command"], list) or not execution["command"]:
        raise SympyDerivativeContractError("derivative execution command is missing")
    if (
        execution["command"][:-1]
        != [REGISTERED_WORKER_PYTHON, *REGISTERED_WORKER_PYTHON_FLAGS]
        or not isinstance(execution["command"][-1], str)
        or not Path(execution["command"][-1]).is_absolute()
        or execution["executable"] != REGISTERED_WORKER_PYTHON
    ):
        raise SympyDerivativeContractError("derivative execution command differs from the source-only registry")
    if execution["environment"] != REGISTERED_WORKER_ENVIRONMENT:
        raise SympyDerivativeContractError("derivative execution environment differs from the isolated registry")
    if type(execution["wall_time_ms"]) is not int or execution["wall_time_ms"] < 0:
        raise SympyDerivativeContractError("derivative execution wall time is invalid")
    for key in ("run_binding_digest", "code_identity_digest"):
        if not isinstance(execution[key], str) or not re.fullmatch(r"[0-9a-f]{64}", execution[key]):
            raise SympyDerivativeContractError(f"derivative execution {key} is invalid")
    if not isinstance(execution["run_id"], str) or not execution["run_id"]:
        raise SympyDerivativeContractError("derivative execution run id is invalid")
    if result["non_claims"] != request["unsupported_conclusions"]:
        raise SympyDerivativeContractError("derivative result non-claims mismatch")
    bindings = result["raw_bindings"]
    if not isinstance(bindings, Mapping) or set(bindings) != {"native-input.json", "stdout.bin", "stderr.bin"}:
        raise SympyDerivativeContractError("derivative raw-binding schema mismatch")
    for binding in bindings.values():
        if not isinstance(binding, Mapping) or set(binding) != {"sha256", "byte_count"}:
            raise SympyDerivativeContractError("derivative raw binding is malformed")
        if not isinstance(binding["sha256"], str) or not re.fullmatch(r"[0-9a-f]{64}", binding["sha256"]):
            raise SympyDerivativeContractError("derivative raw digest is invalid")
        if type(binding["byte_count"]) is not int or binding["byte_count"] < 0:
            raise SympyDerivativeContractError("derivative raw byte count is invalid")
    expected = _digest({key: child for key, child in result.items() if key != "result_digest"})
    if result["result_digest"] != expected:
        raise SympyDerivativeContractError("derivative result digest mismatch")
    return result


def worker_main() -> int:
    raw = sys.stdin.buffer.read(262_145)
    if len(raw) > 262_144:
        sys.stderr.write("input exceeds registered limit\n")
        return 2
    try:
        request_value = json.loads(raw.decode("utf-8", "strict"))
        request = validate_derivative_request(request_value)
        if canonical_json_bytes(request) != raw:
            raise SympyDerivativeContractError("worker stdin is not canonical request bytes")
        record = compute_worker_record(request, enforce_worker_runtime=True)
        sys.stdout.buffer.write(worker_record_bytes(record, request))
        return 0
    except Exception as exc:
        sys.stderr.write(f"{type(exc).__name__}: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(worker_main())
