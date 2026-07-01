from __future__ import annotations

"""Bounded counterexample search for mathematical debugging workflows."""

from dataclasses import asdict, dataclass
from importlib.util import find_spec
import itertools
import re
from typing import Any

from .contracts import attach_contract
from .math_debugging import (
    backend_attempt_record,
    counterexample_record,
    math_question,
    workbench_obligation,
    workbench_result,
)


_SAFE_SCALAR = re.compile(r"^[A-Za-z0-9_+\-*/()., ^]+$")
_IDENTIFIER = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
_SAFE_FUNCTIONS = {"exp", "log", "sin", "cos", "sqrt"}
_DEFAULT_DOMAIN = [-2, -1, 0, 1, 2]


@dataclass(frozen=True)
class CounterexampleSearchResult:
    status: str
    reason: str
    lhs: str
    rhs: str
    backend: str
    search_space: dict[str, Any]
    counterexample: dict[str, Any] | None
    workbench_result: dict[str, Any]


def _matrix_multiply(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    return [
        [sum(left[row][k] * right[k][col] for k in range(len(right))) for col in range(len(right[0]))]
        for row in range(len(left))
    ]


def _noncommutative_matrix_counterexample(lhs: str, rhs: str) -> dict[str, Any] | None:
    normalized_lhs = "".join(lhs.split())
    normalized_rhs = "".join(rhs.split())
    if {normalized_lhs, normalized_rhs} != {"A*B", "B*A"}:
        return None
    a = [[1, 1], [0, 1]]
    b = [[1, 0], [1, 1]]
    ab = _matrix_multiply(a, b)
    ba = _matrix_multiply(b, a)
    lhs_value = ab if normalized_lhs == "A*B" else ba
    rhs_value = ba if normalized_rhs == "B*A" else ab
    if lhs_value == rhs_value:
        return None
    return counterexample_record(
        assignments={"A": a, "B": b},
        lhs_value=lhs_value,
        rhs_value=rhs_value,
        reason="Fixed 2x2 matrices show matrix multiplication is not commutative.",
        backend="bounded_matrix_probe",
        seed=None,
    )


def _sympy_locals(lhs: str, rhs: str) -> dict[str, object]:
    import sympy as sp

    safe_functions = {
        "exp": sp.exp,
        "log": sp.log,
        "sin": sp.sin,
        "cos": sp.cos,
        "sqrt": sp.sqrt,
    }
    identifiers = set(_IDENTIFIER.findall(lhs)) | set(_IDENTIFIER.findall(rhs))
    locals_dict: dict[str, object] = {name: safe_functions[name] for name in identifiers & _SAFE_FUNCTIONS}
    for name in sorted(identifiers - _SAFE_FUNCTIONS):
        locals_dict[name] = sp.Symbol(name)
    return locals_dict


def _scalar_counterexample(lhs: str, rhs: str, domain: list[int]) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    if not (_SAFE_SCALAR.fullmatch(lhs) and _SAFE_SCALAR.fullmatch(rhs)):
        return None, {"status": "not_encodable", "reason": "Expression is outside the conservative scalar grammar."}
    if find_spec("sympy") is None:
        return None, {"status": "backend_unavailable", "reason": "SymPy is not installed in this environment."}
    try:
        import sympy as sp
        from sympy.parsing.sympy_parser import parse_expr

        locals_dict = _sympy_locals(lhs, rhs)
        lhs_expr = parse_expr(lhs, local_dict=locals_dict, evaluate=False)
        rhs_expr = parse_expr(rhs, local_dict=locals_dict, evaluate=False)
        symbols = sorted((lhs_expr.free_symbols | rhs_expr.free_symbols), key=lambda item: item.name)
        if not symbols:
            if sp.simplify(lhs_expr - rhs_expr) != 0:
                return (
                    counterexample_record(
                        assignments={},
                        lhs_value=str(lhs_expr),
                        rhs_value=str(rhs_expr),
                        reason="Constant expressions evaluate differently.",
                        backend="sympy_finite_domain",
                    ),
                    {"status": "searched", "points": 1, "symbols": []},
                )
            return None, {"status": "searched", "points": 1, "symbols": []}
        points = 0
        for values in itertools.product(domain, repeat=len(symbols)):
            assignments = dict(zip(symbols, values, strict=True))
            points += 1
            try:
                lhs_value = sp.simplify(lhs_expr.subs(assignments))
                rhs_value = sp.simplify(rhs_expr.subs(assignments))
            except Exception:
                continue
            if lhs_value != rhs_value:
                readable_assignments = {symbol.name: value for symbol, value in assignments.items()}
                return (
                    counterexample_record(
                        assignments=readable_assignments,
                        lhs_value=str(lhs_value),
                        rhs_value=str(rhs_value),
                        reason="Finite-domain substitution produced different lhs/rhs values.",
                        backend="sympy_finite_domain",
                    ),
                    {"status": "searched", "points": points, "symbols": [symbol.name for symbol in symbols]},
                )
        return None, {"status": "searched", "points": points, "symbols": [symbol.name for symbol in symbols]}
    except Exception as exc:
        return None, {"status": "not_encodable", "reason": f"SymPy could not encode this search: {exc}"}


def find_counterexample(lhs: str, rhs: str, *, domain: list[int] | None = None) -> dict:
    search_domain = domain or _DEFAULT_DOMAIN
    matrix_counterexample = _noncommutative_matrix_counterexample(lhs, rhs)
    if matrix_counterexample is not None:
        attempt = backend_attempt_record(
            backend="bounded_matrix_probe",
            status="refuted",
            reason=matrix_counterexample["reason"],
            severity="blocking",
        )
        question = math_question("find_counterexample", f"{lhs} == {rhs}", context={"domain": "fixed_2x2_matrix"})
        obligation = workbench_obligation(
            "counterexample-obligation-1",
            lhs=lhs,
            rhs=rhs,
            status="refuted",
            reason=matrix_counterexample["reason"],
            backend_attempts=[attempt],
            counterexample=matrix_counterexample,
        )
        result = workbench_result(
            question,
            status="refuted",
            reason="A concrete counterexample was found.",
            obligations=[obligation],
            backend_attempts=[attempt],
            counterexamples=[matrix_counterexample],
        )
        return attach_contract(
            asdict(
                CounterexampleSearchResult(
                    status="refuted",
                    reason="A concrete counterexample was found.",
                    lhs=lhs,
                    rhs=rhs,
                    backend="bounded_matrix_probe",
                    search_space={"kind": "fixed_2x2_matrix"},
                    counterexample=matrix_counterexample,
                    workbench_result=result,
                )
            ),
            "counterexample_search_result",
        )

    scalar_counterexample, search_space = _scalar_counterexample(lhs, rhs, search_domain)
    if scalar_counterexample is not None:
        status = "refuted"
        reason = "A finite-domain scalar counterexample was found."
        severity = "blocking"
    elif search_space.get("status") == "not_encodable":
        status = "not_encodable"
        reason = str(search_space.get("reason"))
        severity = "diagnostic"
    elif search_space.get("status") == "backend_unavailable":
        status = "backend_unavailable"
        reason = str(search_space.get("reason"))
        severity = "diagnostic"
    else:
        status = "unknown"
        reason = "No counterexample was found in the bounded finite search domain."
        severity = "diagnostic"

    attempt = backend_attempt_record(
        backend="sympy_finite_domain",
        status=status,
        reason=reason,
        evidence=[],
        severity=severity,
    )
    question = math_question("find_counterexample", f"{lhs} == {rhs}", context={"domain": search_domain})
    obligation = workbench_obligation(
        "counterexample-obligation-1",
        lhs=lhs,
        rhs=rhs,
        status=status,
        reason=reason,
        backend_attempts=[attempt],
        counterexample=scalar_counterexample,
    )
    result = workbench_result(
        question,
        status=status,
        reason=reason,
        obligations=[obligation],
        backend_attempts=[attempt],
        counterexamples=[scalar_counterexample] if scalar_counterexample else [],
    )
    return attach_contract(
        asdict(
            CounterexampleSearchResult(
                status=status,
                reason=reason,
                lhs=lhs,
                rhs=rhs,
                backend="sympy_finite_domain",
                search_space={"kind": "finite_integer_domain", "domain": search_domain, **search_space},
                counterexample=scalar_counterexample,
                workbench_result=result,
            )
        ),
        "counterexample_search_result",
    )
