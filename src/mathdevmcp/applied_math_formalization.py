"""Small, fail-closed formalization routes for applied-math audit candidates.

Only a conservative expression grammar is accepted. The function is useful for
closed synthetic or source-authenticated targets; parser-only PDF expressions
remain diagnostic and are rejected by the promotion gate.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
import json
import os
from pathlib import Path
import re
import resource
import subprocess
import sys
from typing import Any


MAX_EXPRESSION_CHARS = 1_000
MAX_AST_NODES = 256
MAX_DEPTH = 32
MAX_SYMBOLS = 64
MAX_INTEGER_DIGITS = 20
MAX_EXPONENT_MAGNITUDE = 12
SAFE_NAMES = frozenset({"pi", "E"})


@dataclass(frozen=True)
class FormalizationLimits:
    timeout_seconds: float = 2.0
    max_output_bytes: int = 16_384
    max_memory_bytes: int = 256 * 1024 * 1024


class FormalizationError(ValueError):
    pass


def _validate_tree(tree: ast.AST, *, expression: str) -> dict[str, Any]:
    nodes = 0
    max_depth = 0
    symbols: set[str] = set()
    for node in ast.walk(tree):
        nodes += 1
        if nodes > MAX_AST_NODES:
            raise FormalizationError("expression exceeds AST-node limit")
        depth = 0
        parent = getattr(node, "_mathdev_parent", None)
        while parent is not None:
            depth += 1
            parent = getattr(parent, "_mathdev_parent", None)
        max_depth = max(max_depth, depth)
        if isinstance(node, ast.Name):
            symbols.add(node.id)
            if node.id not in SAFE_NAMES and not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", node.id):
                raise FormalizationError(f"identifier is not allowlisted: {node.id}")
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, bool) or not isinstance(node.value, (int, float)):
                raise FormalizationError("only numeric constants are allowed")
            if isinstance(node.value, int) and len(str(abs(node.value))) > MAX_INTEGER_DIGITS:
                raise FormalizationError("integer literal exceeds digit limit")
        elif isinstance(node, (ast.Expression, ast.Load, ast.BinOp, ast.UnaryOp, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.UAdd, ast.USub)):
            pass
        else:
            raise FormalizationError(f"AST node is outside the safe grammar: {type(node).__name__}")
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Pow):
            exponent = node.right
            if isinstance(exponent, ast.Constant) and isinstance(exponent.value, (int, float)):
                if abs(float(exponent.value)) > MAX_EXPONENT_MAGNITUDE:
                    raise FormalizationError("exponent exceeds magnitude limit")
    if max_depth > MAX_DEPTH:
        raise FormalizationError("expression nesting exceeds depth limit")
    if len(symbols) > MAX_SYMBOLS:
        raise FormalizationError("expression exceeds symbol limit")
    return {"ast_nodes": nodes, "max_depth": max_depth, "symbols": sorted(symbols)}


def _parse(expression: str) -> tuple[str, dict[str, Any]]:
    if not isinstance(expression, str) or not expression.strip():
        raise FormalizationError("expression must be a non-empty string")
    if len(expression) > MAX_EXPRESSION_CHARS:
        raise FormalizationError("expression exceeds character limit")
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise FormalizationError("expression is not valid Python-style arithmetic") from exc
    # Add parent links for the bounded depth audit without changing the source
    # expression or allowing execution.
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            setattr(child, "_mathdev_parent", parent)
    return expression, _validate_tree(tree, expression=expression)


def _resource_limits(limits: FormalizationLimits):
    def apply() -> None:
        cpu = max(1, int(limits.timeout_seconds))
        resource.setrlimit(resource.RLIMIT_CPU, (cpu, cpu))
        resource.setrlimit(resource.RLIMIT_AS, (limits.max_memory_bytes, limits.max_memory_bytes))
        resource.setrlimit(resource.RLIMIT_STACK, (32 * 1024 * 1024, 32 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_FSIZE, (limits.max_output_bytes, limits.max_output_bytes))
        resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
    return apply


def _run_worker(lhs: str, rhs: str, limits: FormalizationLimits) -> dict[str, Any]:
    worker = Path(__file__).with_name("applied_math_sympy_worker.py").resolve()
    env = {
        "PATH": os.environ.get("PATH", ""),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "CUDA_VISIBLE_DEVICES": "-1",
    }
    try:
        completed = subprocess.run(
            (sys.executable, "-I", str(worker)),
            input=json.dumps({"lhs": lhs, "rhs": rhs}),
            text=True,
            capture_output=True,
            check=False,
            cwd="/tmp",
            env=env,
            timeout=limits.timeout_seconds,
            preexec_fn=_resource_limits(limits),
        )
    except subprocess.TimeoutExpired:
        return {"status": "timeout"}
    if len(completed.stdout.encode("utf-8")) > limits.max_output_bytes:
        return {"status": "truncated_output"}
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {"status": "execution_error", "returncode": completed.returncode}
    if completed.returncode != 0 or payload.get("status") == "error":
        return {"status": "execution_error", "returncode": completed.returncode, "worker": payload}
    return payload


def formalize_equality(
    lhs: str,
    rhs: str,
    *,
    source_state: str,
    source_relation_explicit: bool,
    assumptions: list[str] | None = None,
    limits: FormalizationLimits | None = None,
) -> dict[str, Any]:
    """Check an explicit equality while enforcing the promotion boundary."""

    limits = limits or FormalizationLimits()
    if source_state not in {"source_authenticated", "independently_verified_transcription"}:
        return {
            "status": "backend_abstention",
            "reason_code": "unauthenticated_transcription",
            "non_claim": "A parser-only expression cannot support a promoted mathematical defect.",
        }
    if not source_relation_explicit:
        return {
            "status": "supported_tension",
            "reason_code": "relation_not_explicit_in_source",
            "non_claim": "A backend mismatch between unrelated expressions is not a document defect.",
        }
    try:
        lhs_text, lhs_meta = _parse(lhs)
        rhs_text, rhs_meta = _parse(rhs)
    except FormalizationError as exc:
        return {
            "status": "backend_abstention",
            "reason_code": "formalization_rejected",
            "detail": str(exc),
        }
    result = _run_worker(lhs_text, rhs_text, limits)
    status = str(result.get("status", "inconclusive"))
    if status == "domain_conditions_required":
        return {
            "status": "backend_abstention",
            "reason_code": "domain_conditions_required",
            "backend": "sympy",
            "backend_evidence": result,
            "assumptions": list(assumptions or []),
            "non_claim": "Symbolic simplification cannot establish equality across unresolved denominator domains.",
        }
    return {
        "status": "confirmed_defect" if status == "mismatch" else "consistent_under_checked_assumptions" if status == "equivalent" else "backend_abstention",
        "backend_status": status,
        "backend": "sympy",
        "backend_evidence": result,
        "assumptions": list(assumptions or []),
        "limits": {
            "expression_chars": MAX_EXPRESSION_CHARS,
            "ast_nodes": MAX_AST_NODES,
            "depth": MAX_DEPTH,
            "symbols": MAX_SYMBOLS,
            "integer_digits": MAX_INTEGER_DIGITS,
            "exponent_magnitude": MAX_EXPONENT_MAGNITUDE,
            "timeout_seconds": limits.timeout_seconds,
            "max_output_bytes": limits.max_output_bytes,
            "max_memory_bytes": limits.max_memory_bytes,
        },
        "lhs_metadata": lhs_meta,
        "rhs_metadata": rhs_meta,
        "non_claim": "Symbolic equality is scoped to the supplied expressions and assumptions; it does not establish economic interpretation.",
    }
