from __future__ import annotations

"""Bounded structural matching between equations and Python code."""

import ast
from dataclasses import asdict, dataclass
import re
from typing import Any

from .contracts import attach_contract
from .math_debugging import math_question, workbench_result


_IDENTIFIER = re.compile(r"\b[A-Za-z_][A-Za-z0-9_]*\b")
_KNOWN_FUNCTIONS = {"logdet", "solve", "trace", "sqrt", "exp", "log", "det", "inv"}


@dataclass(frozen=True)
class EquationCodeMatchResult:
    status: str
    reason: str
    equation: str
    matched_terms: list[str]
    missing_terms: list[str]
    extra_code_terms: list[str]
    conflicts: list[dict[str, Any]]
    code_summary: dict[str, Any]
    workbench_result: dict[str, Any]


def _equation_terms(equation: str) -> set[str]:
    identifiers = set(_IDENTIFIER.findall(equation))
    return {item for item in identifiers if item not in {"and", "or"}}


def _code_terms(code: str) -> tuple[set[str], dict[str, Any]]:
    tree = ast.parse(code)
    names: set[str] = set()
    calls: set[str] = set()
    operators: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                calls.add(func.id)
            elif isinstance(func, ast.Attribute):
                calls.add(func.attr)
        elif isinstance(node, ast.BinOp):
            operators.add(type(node.op).__name__)
    return names | calls, {"names": sorted(names), "calls": sorted(calls), "operators": sorted(operators)}


def code_implements_equation(equation: str, code: str, *, aliases: dict[str, str] | None = None) -> dict:
    alias_map = aliases or {}
    equation_terms = _equation_terms(equation)
    code_terms, code_summary = _code_terms(code)
    mapped_terms = {alias_map.get(term, term) for term in equation_terms}
    matched = sorted(term for term in mapped_terms if term in code_terms)
    missing = sorted(term for term in mapped_terms if term not in code_terms)
    extras = sorted(term for term in code_terms - mapped_terms if term not in {"return", "def"})
    conflicts: list[dict[str, Any]] = []
    if "transpose" in equation_terms and "T" not in code_terms and "transpose" not in code_terms:
        conflicts.append({"kind": "transpose_mismatch", "reason": "Equation mentions transpose but code lacks a visible transpose operation."})
    if any(term.endswith("_next") for term in equation_terms) and not any(term.endswith("_next") for term in code_terms):
        conflicts.append({"kind": "time_index_mismatch", "reason": "Equation mentions next-period symbol but code lacks matching next-period name."})
    missing_required = [term for term in missing if term in _KNOWN_FUNCTIONS or term in mapped_terms]
    if conflicts or missing_required:
        status = "mismatch"
        reason = "Code is missing required equation terms or has structural conflicts."
    else:
        status = "consistent"
        reason = "Code contains the bounded equation terms under the supplied aliases."
    question = math_question("code_implements_equation", equation, context={"aliases": alias_map})
    workbench = workbench_result(
        question,
        status="unknown" if status == "consistent" else "refuted",
        reason=(
            "Structural code/equation evidence is diagnostic and not semantic proof."
            if status == "consistent"
            else reason
        ),
        actions=[] if status == "consistent" else [{"kind": "inspect_missing_or_conflicting_code_terms"}],
    )
    return attach_contract(
        asdict(
            EquationCodeMatchResult(
                status=status,
                reason=reason,
                equation=equation,
                matched_terms=matched,
                missing_terms=missing,
                extra_code_terms=extras,
                conflicts=conflicts,
                code_summary=code_summary,
                workbench_result=workbench,
            )
        ),
        "equation_code_match_result",
    )
