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
    trace_map: dict[str, Any]
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
    function_args: dict[str, list[str]] = {}
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
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [arg.arg for arg in node.args.args]
            function_args[node.name] = args
    return names | calls, {"names": sorted(names), "calls": sorted(calls), "operators": sorted(operators), "function_args": function_args}


def _math_signature_terms(equation: str) -> set[str]:
    terms: set[str] = set()
    for match in re.finditer(r"([A-Za-z_\\][A-Za-z0-9_\\]*(?:\^\{[^{}]+\}|_\{[^{}]+\}|_[A-Za-z0-9]+)?)\s*\(([^)]*)\)", equation):
        args = [item.strip() for item in match.group(2).split(",") if item.strip()]
        if len(args) >= 2:
            terms.update(arg.strip("\\{} ") for arg in args if re.search(r"[A-Za-z]", arg))
    for match in re.finditer(r"\\sum_\{([^{}]+)\}\^\{([^{}]+)\}", equation):
        terms.update(token for token in _IDENTIFIER.findall(" ".join(match.groups())) if token not in {"sum"})
    if "\\mid" in equation or "|" in equation:
        terms.add("conditioning_scope")
    return {term for term in terms if term}


def _scope_diagnostic(equation: str, code_summary: dict[str, Any], matched: list[str], missing: list[str]) -> dict[str, Any]:
    math_scope_terms = _math_signature_terms(equation)
    function_args_map = code_summary.get("function_args") if isinstance(code_summary.get("function_args"), dict) else {}
    code_args = {arg for args in function_args_map.values() if isinstance(args, list) for arg in args}
    missing_scope_terms = sorted(term for term in math_scope_terms if term not in code_args and term not in matched)
    matched_scope_terms = sorted(term for term in math_scope_terms if term in code_args or term in matched)
    function_level_markers = sorted(math_scope_terms)
    reduced_code_signature = bool(function_args_map) and bool(missing_scope_terms) and bool(matched)
    is_likelihood_or_value = bool(re.search(r"likelihood|loglik|log_like|\\ell|NPV|V[_\^]|Q\(", equation, re.IGNORECASE))
    triggered = reduced_code_signature and (is_likelihood_or_value or len(missing_scope_terms) >= 2)
    return {
        "status": "scope_limited" if triggered else "not_triggered",
        "math_scope_terms": sorted(math_scope_terms),
        "code_function_args": sorted(code_args),
        "matched_scope_terms": matched_scope_terms,
        "missing_scope_terms": missing_scope_terms,
        "function_level_markers": function_level_markers,
        "supports": (
            "The code exposes structurally relevant terms for a value-level or instance-level slice of the mathematical expression."
            if triggered
            else ""
        ),
        "does_not_support": (
            "The code signature does not expose all function-level arguments, summation/index domains, or conditioning scope required by the mathematical claim."
            if triggered
            else ""
        ),
        "safe_wording": (
            "Treat this as scope-limited implementation evidence: it may support one evaluated slice, but it does not prove the full function-level formula."
            if triggered
            else ""
        ),
        "boundary": "Scope diagnostics are structural and non-executing; they are not code correctness proof.",
    }


def code_implements_equation(equation: str, code: str, *, aliases: dict[str, str] | None = None) -> dict:
    alias_map = aliases or {}
    equation_terms = _equation_terms(equation)
    code_terms, code_summary = _code_terms(code)
    mapped_terms = {alias_map.get(term, term) for term in equation_terms}
    matched = sorted(term for term in mapped_terms if term in code_terms)
    missing = sorted(term for term in mapped_terms if term not in code_terms)
    extras = sorted(term for term in code_terms - mapped_terms if term not in {"return", "def"})
    term_traces = [
        {
            "equation_term": term,
            "mapped_code_term": alias_map.get(term, term),
            "matched": alias_map.get(term, term) in code_terms,
            "source": "alias_map" if term in alias_map else "direct",
        }
        for term in sorted(equation_terms)
    ]
    mapped_counts: dict[str, int] = {}
    for item in term_traces:
        mapped_counts[item["mapped_code_term"]] = mapped_counts.get(item["mapped_code_term"], 0) + 1
    alias_collisions = [
        {
            "mapped_code_term": mapped,
            "equation_terms": [item["equation_term"] for item in term_traces if item["mapped_code_term"] == mapped],
        }
        for mapped, count in sorted(mapped_counts.items())
        if count > 1
    ]
    trace_map = {
        "equation_terms": sorted(equation_terms),
        "alias_map": dict(sorted(alias_map.items())),
        "mapped_terms": sorted(mapped_terms),
        "term_traces": term_traces,
        "alias_collisions": alias_collisions,
        "matched_terms": matched,
        "missing_terms": missing,
        "extra_code_terms": extras,
        "code_operations": code_summary,
        "boundary": (
            "This trace map records structural term visibility only. It is not "
            "semantic proof that the code implements the documented math."
        ),
    }
    conflicts: list[dict[str, Any]] = []
    if "transpose" in equation_terms and "T" not in code_terms and "transpose" not in code_terms:
        conflicts.append({"kind": "transpose_mismatch", "reason": "Equation mentions transpose but code lacks a visible transpose operation."})
    if any(term.endswith("_next") for term in equation_terms) and not any(term.endswith("_next") for term in code_terms):
        conflicts.append({"kind": "time_index_mismatch", "reason": "Equation mentions next-period symbol but code lacks matching next-period name."})
    missing_required = [term for term in missing if term in _KNOWN_FUNCTIONS or term in mapped_terms]
    scope_diagnostic = _scope_diagnostic(equation, code_summary, matched, missing)
    trace_map["scope_diagnostic"] = scope_diagnostic
    if scope_diagnostic["status"] == "scope_limited" and not conflicts:
        status = "scope_limited"
        reason = "Code evidence is scope-limited: it supports a value-level slice but not the full function-level mathematical claim."
    elif conflicts or missing_required:
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
                trace_map=trace_map,
                conflicts=conflicts,
                code_summary=code_summary,
                workbench_result=workbench,
            )
        ),
        "equation_code_match_result",
    )
