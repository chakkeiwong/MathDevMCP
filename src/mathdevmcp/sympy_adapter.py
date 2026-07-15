from __future__ import annotations

"""Typed, bounded SymPy adapter for the reviewed Phase 05 scalar scope."""

import ast
from dataclasses import dataclass
import hashlib
import importlib.metadata
import importlib.util
import json
import multiprocessing
import re
from typing import Any, Callable, Mapping

from .external_adapter_contract import (
    ExternalAdapterContractError,
    build_external_adapter_request,
    build_external_adapter_result,
)


SYMPY_ADAPTER_VERSION = "p05-sympy-adapter@1"
SYMPY_SUPPORTED_DOMAINS = frozenset({"integer", "rational", "real"})
SYMPY_SUPPORTED_PREDICATES = frozenset({"nonzero", "positive", "nonnegative"})
SYMPY_MAX_EXPRESSION_CHARS = 1_000
SYMPY_MAX_AST_NODES = 256
SYMPY_MAX_INTEGER_BITS = 256
SYMPY_MAX_ABS_EXPONENT = 64
_NAME = re.compile(r"^[A-Za-z][A-Za-z0-9_]*$")
_SAFE_FUNCTIONS = frozenset({"sqrt", "exp", "log", "sin", "cos"})
_SAFE_BINARY = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)
_SAFE_UNARY = (ast.UAdd, ast.USub)


@dataclass(frozen=True)
class SympySymbol:
    name: str
    domain: str
    predicates: tuple[str, ...] = ()


@dataclass(frozen=True)
class SympyScalarObligation:
    branch_id: str
    branch_lineage: tuple[str, ...]
    obligation_digest: str
    target: str
    lhs: str
    rhs: str
    symbols: tuple[SympySymbol, ...]


def _json_bytes(value: Any) -> bytes:
    return json.dumps(
        value, ensure_ascii=True, allow_nan=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _native_payload(obligation: SympyScalarObligation) -> dict[str, Any]:
    return {
        "schema_version": "p05_sympy_scalar_input@1",
        "lhs": obligation.lhs,
        "rhs": obligation.rhs,
        "symbols": [
            {
                "name": symbol.name,
                "domain": symbol.domain,
                "predicates": sorted(symbol.predicates),
            }
            for symbol in sorted(obligation.symbols, key=lambda item: item.name)
        ],
    }


def sympy_native_input_bytes(obligation: SympyScalarObligation) -> bytes:
    """Return deterministic adapter-native input bytes."""
    return _json_bytes(_native_payload(obligation))


def _typed_assumptions(obligation: SympyScalarObligation) -> list[dict[str, Any]]:
    assumptions: list[dict[str, Any]] = []
    for symbol in sorted(obligation.symbols, key=lambda item: item.name):
        assumptions.append(
            {
                "id": f"domain_{symbol.name}",
                "kind": "domain",
                "symbol": symbol.name,
                "domain": symbol.domain,
            }
        )
        assumptions.extend(
            {
                "id": f"{predicate}_{symbol.name}",
                "kind": "predicate",
                "symbol": symbol.name,
                "predicate": predicate,
            }
            for predicate in sorted(symbol.predicates)
        )
    return assumptions


def _validate_symbols(symbols: tuple[SympySymbol, ...]) -> str | None:
    if not symbols:
        return "At least one declared symbol is required for this scalar adapter."
    names: set[str] = set()
    for symbol in symbols:
        if not _NAME.fullmatch(symbol.name) or symbol.name in _SAFE_FUNCTIONS:
            return f"Unsupported symbol name: {symbol.name!r}."
        if symbol.name in names:
            return f"Duplicate symbol declaration: {symbol.name}."
        names.add(symbol.name)
        if symbol.domain not in SYMPY_SUPPORTED_DOMAINS:
            return f"Unsupported scalar domain for {symbol.name}: {symbol.domain}."
        predicates = set(symbol.predicates)
        if len(predicates) != len(symbol.predicates):
            return f"Duplicate predicates were declared for {symbol.name}."
        unknown = predicates - SYMPY_SUPPORTED_PREDICATES
        if unknown:
            return f"Unsupported predicates for {symbol.name}: {sorted(unknown)}."
        if "positive" in predicates and "nonnegative" in predicates:
            return f"Redundant positive/nonnegative predicates for {symbol.name}."
    return None


def _parse_expression(text: str, declared: set[str]) -> tuple[ast.Expression | None, str | None]:
    if not isinstance(text, str) or not text.strip():
        return None, "Expression must be a non-empty string."
    if len(text) > SYMPY_MAX_EXPRESSION_CHARS:
        return None, f"Expression exceeds {SYMPY_MAX_EXPRESSION_CHARS} characters."
    try:
        tree = ast.parse(text, mode="eval")
    except SyntaxError as exc:
        return None, f"Expression is not valid bounded scalar syntax: {exc.msg}."
    nodes = list(ast.walk(tree))
    if len(nodes) > SYMPY_MAX_AST_NODES:
        return None, f"Expression exceeds {SYMPY_MAX_AST_NODES} AST nodes."
    for node in nodes:
        if isinstance(node, ast.Expression):
            continue
        if isinstance(node, ast.BinOp):
            if not isinstance(node.op, _SAFE_BINARY):
                return None, f"Unsupported binary operator: {type(node.op).__name__}."
            if isinstance(node.op, ast.Pow):
                exponent = _integer_literal(node.right)
                if exponent is None:
                    return None, "Powers require an exact integer-literal exponent."
                if abs(exponent) > SYMPY_MAX_ABS_EXPONENT:
                    return None, (
                        f"Power exponent magnitude exceeds {SYMPY_MAX_ABS_EXPONENT}."
                    )
            continue
        if isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, _SAFE_UNARY):
                return None, f"Unsupported unary operator: {type(node.op).__name__}."
            continue
        if isinstance(node, (*_SAFE_BINARY, *_SAFE_UNARY)):
            continue
        if isinstance(node, ast.Call):
            if (
                not isinstance(node.func, ast.Name)
                or node.func.id not in _SAFE_FUNCTIONS
                or node.keywords
                or len(node.args) != 1
            ):
                return None, "Only one-argument sqrt/exp/log/sin/cos calls are supported."
            continue
        if isinstance(node, ast.Name):
            if node.id not in declared and node.id not in _SAFE_FUNCTIONS:
                return None, f"Undeclared symbol or function: {node.id}."
            continue
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, int) or isinstance(node.value, bool):
                return None, "Only integer literals are supported."
            if abs(node.value).bit_length() > SYMPY_MAX_INTEGER_BITS:
                return None, f"Integer literal exceeds {SYMPY_MAX_INTEGER_BITS} bits."
            continue
        if isinstance(node, ast.Load):
            continue
        return None, f"Unsupported expression construct: {type(node).__name__}."
    return tree, None


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


def _required_predicates(
    lhs: ast.AST, rhs: ast.AST
) -> tuple[dict[str, set[str]], str | None]:
    required: dict[str, set[str]] = {}
    for tree in (lhs, rhs):
        for node in ast.walk(tree):
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                denominator = _integer_literal(node.right)
                if denominator is not None:
                    if denominator == 0:
                        return required, "Division by zero is outside the adapter scope."
                elif isinstance(node.right, ast.Name):
                    required.setdefault(node.right.id, set()).add("nonzero")
                else:
                    return required, (
                        "Compound denominators require an expression-level nonzero proof, "
                        "which the initial typed schema cannot encode."
                    )
            if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
                exponent = _integer_literal(node.right)
                if exponent is not None and exponent < 0:
                    base = _integer_literal(node.left)
                    if base is not None:
                        if base == 0:
                            return required, "A zero base with negative exponent is undefined."
                    elif isinstance(node.left, ast.Name):
                        required.setdefault(node.left.id, set()).add("nonzero")
                    else:
                        return required, (
                            "A compound base with negative exponent requires an "
                            "expression-level nonzero proof."
                        )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "sqrt"
            ):
                argument = _integer_literal(node.args[0])
                if argument is not None:
                    if argument < 0:
                        return required, "A negative square-root argument is outside the real scope."
                elif isinstance(node.args[0], ast.Name):
                    required.setdefault(node.args[0].id, set()).add("nonnegative")
                else:
                    return required, (
                        "A compound square-root argument requires an expression-level "
                        "nonnegative proof."
                    )
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "log"
            ):
                argument = _integer_literal(node.args[0])
                if argument is not None:
                    if argument <= 0:
                        return required, "A nonpositive logarithm argument is outside the real scope."
                elif isinstance(node.args[0], ast.Name):
                    required.setdefault(node.args[0].id, set()).add("positive")
                else:
                    return required, (
                        "A compound logarithm argument requires an expression-level positive proof."
                    )
    return required, None


def _check_required_predicates(
    required: Mapping[str, set[str]], symbols: tuple[SympySymbol, ...]
) -> str | None:
    by_name = {symbol.name: set(symbol.predicates) for symbol in symbols}
    for name, predicates in sorted(required.items()):
        declared = by_name[name]
        if "nonzero" in predicates and not ({"nonzero", "positive"} & declared):
            return f"Missing required nonzero predicate for denominator symbol {name}."
        if "nonnegative" in predicates and not ({"nonnegative", "positive"} & declared):
            return f"Missing required nonnegative predicate for square-root symbol {name}."
        if "positive" in predicates and "positive" not in declared:
            return f"Missing required positive predicate for logarithm symbol {name}."
    return None


def _sympy_assumptions(symbol: SympySymbol) -> dict[str, bool]:
    assumptions: dict[str, bool] = {}
    if symbol.domain == "integer":
        assumptions["integer"] = True
    elif symbol.domain == "rational":
        assumptions["rational"] = True
    elif symbol.domain == "real":
        assumptions["real"] = True
    if "nonzero" in symbol.predicates:
        assumptions["nonzero"] = True
    if "positive" in symbol.predicates:
        assumptions["positive"] = True
    if "nonnegative" in symbol.predicates:
        assumptions["nonnegative"] = True
    return assumptions


def _ast_to_sympy(node: ast.AST, local: Mapping[str, Any], sp: Any) -> Any:
    if isinstance(node, ast.Expression):
        return _ast_to_sympy(node.body, local, sp)
    if isinstance(node, ast.Constant):
        return sp.Integer(node.value)
    if isinstance(node, ast.Name):
        return local[node.id]
    if isinstance(node, ast.UnaryOp):
        value = _ast_to_sympy(node.operand, local, sp)
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp):
        left = _ast_to_sympy(node.left, local, sp)
        right = _ast_to_sympy(node.right, local, sp)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left**right
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        return getattr(sp, node.func.id)(_ast_to_sympy(node.args[0], local, sp))
    raise ValueError(f"unsupported validated AST node: {type(node).__name__}")


def _compute(payload: Mapping[str, Any]) -> dict[str, Any]:
    import sympy as sp

    symbol_records = payload["symbols"]
    local = {
        item["name"]: sp.Symbol(
            item["name"],
            **_sympy_assumptions(
                SympySymbol(
                    item["name"], item["domain"], tuple(item["predicates"])
                )
            ),
        )
        for item in symbol_records
    }
    lhs_tree = ast.parse(payload["lhs"], mode="eval")
    rhs_tree = ast.parse(payload["rhs"], mode="eval")
    lhs = _ast_to_sympy(lhs_tree, local, sp)
    rhs = _ast_to_sympy(rhs_tree, local, sp)
    difference = sp.simplify(lhs - rhs)
    if difference == 0:
        status = "certified"
        reason = "SymPy simplified the typed scalar difference to exact zero."
    elif (
        not difference.free_symbols
        and difference.is_zero is False
        and difference.is_finite is True
    ):
        status = "refuted"
        reason = "SymPy reduced the typed scalar difference to a nonzero constant."
    else:
        status = "diagnostic"
        reason = "SymPy did not decide the typed scalar identity by exact simplification."
    return {
        "status": status,
        "reason": reason,
        "sympy_version": sp.__version__,
        "canonical_lhs": str(lhs),
        "canonical_rhs": str(rhs),
        "srepr_lhs": sp.srepr(lhs),
        "srepr_rhs": sp.srepr(rhs),
        "srepr_difference": sp.srepr(difference),
        "difference": str(difference),
        "refutation_witness": (
            {"kind": "constant_difference", "difference": str(difference)}
            if status == "refuted"
            else None
        ),
    }


def _worker(payload: Mapping[str, Any], sender: Any) -> None:
    try:
        sender.send({"ok": True, "value": _compute(payload)})
    except BaseException as exc:  # pragma: no cover - defensive process boundary
        sender.send(
            {
                "ok": False,
                "error_type": type(exc).__name__,
                "error": str(exc),
            }
        )
    finally:
        sender.close()


def _default_runner(payload: Mapping[str, Any], *, timeout_seconds: float) -> dict[str, Any]:
    """Run SymPy in a killable child process under the adapter timeout."""
    try:
        context = multiprocessing.get_context("fork")
    except ValueError:  # pragma: no cover - non-POSIX fallback
        context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)
    process = context.Process(target=_worker, args=(dict(payload), sender))
    process.start()
    sender.close()
    process.join(timeout_seconds)
    if process.is_alive():
        process.terminate()
        process.join()
        receiver.close()
        return {
            "status": "timeout",
            "reason": f"SymPy execution exceeded {timeout_seconds:g} seconds.",
        }
    if not receiver.poll():
        receiver.close()
        return {
            "status": "execution_error",
            "reason": f"SymPy worker exited with code {process.exitcode} without a result.",
        }
    message = receiver.recv()
    receiver.close()
    if not isinstance(message, dict) or message.get("ok") is not True:
        return {
            "status": "execution_error",
            "reason": (
                "SymPy worker failed: "
                f"{message.get('error_type', 'unknown')}: {message.get('error', '')}"
            ),
        }
    value = message.get("value")
    if not isinstance(value, dict):
        return {"status": "malformed_output", "reason": "SymPy worker returned no object."}
    return value


def _status_reason(
    status: str, reason: str, *, request: Mapping[str, Any], runner_kind: str, raw: Mapping[str, Any]
) -> dict[str, Any]:
    manifest_ref = raw.get("manifest_ref")
    manifest_sha256 = raw.get("manifest_sha256")
    manifest_verified = raw.get("manifest_verified") is True
    evidence_payload = raw.get("evidence_payload")
    output_ref = raw.get("output_ref")
    if output_ref is None and evidence_payload is not None:
        output_ref = f"mathdevmcp://sympy/{hashlib.sha256(_json_bytes(evidence_payload)).hexdigest()}"
    return build_external_adapter_result(
        request=request,
        status=status,
        reason=reason,
        execution={
            "kind": runner_kind,
            "runner_id": SYMPY_ADAPTER_VERSION if runner_kind == "python_library" else "injected_sympy_runner",
            "command": [],
            "executable_path": None,
            "resolved_executable_path": None,
            "exit_code": None,
            "timed_out": status == "timeout" and runner_kind == "python_library",
            "stdout_bytes": len(_json_bytes(evidence_payload)) if evidence_payload is not None else 0,
            "stderr_bytes": 0,
            "stdout_sha256": hashlib.sha256(
                _json_bytes(evidence_payload) if evidence_payload is not None else b""
            ).hexdigest(),
            "stderr_sha256": hashlib.sha256(b"").hexdigest(),
        },
        evidence_kind=(
            "sympy_identity"
            if status == "certified"
            else "constant_counterexample"
            if status == "refuted"
            else "diagnostic"
        ),
        evidence_details=evidence_payload if isinstance(evidence_payload, Mapping) else None,
        output_ref=output_ref,
        manifest_ref=manifest_ref if isinstance(manifest_ref, str) else None,
        manifest_sha256=manifest_sha256 if isinstance(manifest_sha256, str) else None,
        manifest_verified=manifest_verified,
        refutation_witness=(
            raw.get("refutation_witness")
            if status == "refuted" and isinstance(raw.get("refutation_witness"), Mapping)
            else None
        ),
        next_discriminator=(
            "No further discriminator is claimed; inspect the exact scoped certificate."
            if status in {"certified", "refuted"}
            else "Repair the typed input or run a stronger applicable certifying route."
        ),
        non_claims=list(request["unsupported_conclusions"]),
    )


def run_sympy_scalar_obligation(
    obligation: SympyScalarObligation,
    *,
    timeout_seconds: float = 10.0,
    max_output_bytes: int = 262_144,
    runner: Callable[..., Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    """Translate and run one exact typed scalar obligation.

    An injected runner is always classified as a fake runner. The default route
    executes the installed SymPy package in a bounded child process.
    """
    payload = _native_payload(obligation)
    native = _json_bytes(payload)
    try:
        sympy_version = (
            importlib.metadata.version("sympy")
            if importlib.util.find_spec("sympy") is not None
            else "unavailable"
        )
    except importlib.metadata.PackageNotFoundError:
        sympy_version = "unavailable"
    request = build_external_adapter_request(
        branch_id=obligation.branch_id,
        branch_lineage=obligation.branch_lineage,
        obligation_digest=obligation.obligation_digest,
        normalized_target=obligation.target,
        typed_assumptions=_typed_assumptions(obligation),
        native_input_bytes=native,
        native_input_media_type="application/vnd.mathdevmcp.sympy-scalar+json",
        tool_name="sympy",
        adapter_version=SYMPY_ADAPTER_VERSION,
        backend_version=sympy_version,
        requested_executable=None,
        resolved_executable=None,
        timeout_ms=max(1, int(timeout_seconds * 1_000)),
        max_output_bytes=max_output_bytes,
        max_artifact_bytes=max_output_bytes,
        expected_result_class="typed_scalar_identity",
        backend_role="scoped_symbolic_certificate",
        unsupported_conclusions=(
            "no_matrix_or_noncommutative_claim",
            "no_complex_branch_cut_claim",
            "no_probability_or_expectation_claim",
            "no_general_cas_soundness",
            "no_real_document_repair_capability",
            "no_publication",
        ),
    )
    runner_kind = "fake_runner" if runner is not None else "python_library"

    expected_target = " ".join(f"{obligation.lhs} = {obligation.rhs}".split())
    actual_target = " ".join(obligation.target.split())
    validation_error = (
        "Normalized target does not exactly match the encoded lhs = rhs."
        if actual_target != expected_target
        else _validate_symbols(obligation.symbols)
    )
    lhs_tree, lhs_error = _parse_expression(
        obligation.lhs, {item.name for item in obligation.symbols}
    )
    rhs_tree, rhs_error = _parse_expression(
        obligation.rhs, {item.name for item in obligation.symbols}
    )
    translation_error = validation_error or lhs_error or rhs_error
    if translation_error is not None:
        return _status_reason(
            "unsupported" if validation_error else "translation_error",
            translation_error,
            request=request,
            runner_kind="not_run",
            raw={},
        )
    assert lhs_tree is not None and rhs_tree is not None
    required_predicates, construct_error = _required_predicates(lhs_tree, rhs_tree)
    predicate_error = construct_error or _check_required_predicates(
        required_predicates, obligation.symbols
    )
    if predicate_error is not None:
        return _status_reason(
            "translation_error",
            predicate_error,
            request=request,
            runner_kind="not_run",
            raw={},
        )
    if sympy_version == "unavailable" and runner is None:
        return _status_reason(
            "unavailable",
            "SymPy is not installed in the active Python environment.",
            request=request,
            runner_kind="not_run",
            raw={},
        )

    call = runner or _default_runner
    try:
        raw_value = call(payload, timeout_seconds=timeout_seconds)
    except TimeoutError:
        raw_value = {"status": "timeout", "reason": "Injected SymPy runner timed out."}
    except Exception as exc:
        raw_value = {
            "status": "execution_error",
            "reason": f"SymPy runner failed: {type(exc).__name__}: {exc}",
        }
    if not isinstance(raw_value, Mapping):
        raw_value = {
            "status": "malformed_output",
            "reason": "SymPy runner output was not an object.",
        }
    raw = dict(raw_value)
    status = raw.get("status")
    if status not in {
        "certified",
        "refuted",
        "diagnostic",
        "unavailable",
        "execution_error",
        "timeout",
        "malformed_output",
        "truncated_output",
    }:
        status = "malformed_output"
        raw = {"status": status, "reason": "SymPy runner returned an unknown status."}
    evidence_payload = {
        key: raw[key]
        for key in (
            "sympy_version",
            "canonical_lhs",
            "canonical_rhs",
            "srepr_lhs",
            "srepr_rhs",
            "srepr_difference",
            "difference",
        )
        if key in raw
    }
    raw["evidence_payload"] = evidence_payload
    if len(_json_bytes(evidence_payload)) > max_output_bytes:
        status = "truncated_output"
        raw = {"status": status, "reason": "SymPy evidence exceeded the output limit."}
    reason = raw.get("reason")
    if not isinstance(reason, str) or not reason:
        status = "malformed_output"
        reason = "SymPy runner returned no reason."
        raw = {"status": status, "reason": reason}
    if status == "refuted" and not isinstance(raw.get("refutation_witness"), Mapping):
        status = "malformed_output"
        reason = "A SymPy refutation requires a concrete constant-difference witness."
        raw = {"status": status, "reason": reason}
    try:
        return _status_reason(
            status,
            reason,
            request=request,
            runner_kind=runner_kind,
            raw=raw,
        )
    except ExternalAdapterContractError as exc:
        return _status_reason(
            "malformed_output",
            f"SymPy evidence failed the adapter contract: {exc}",
            request=request,
            runner_kind=runner_kind,
            raw={},
        )
