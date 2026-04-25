from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib.util import find_spec
import re

from .contracts import attach_contract
from .derivation import derive_step
from .math_normalization import normalize_math_text


BACKENDS = {"auto", "sympy", "sage", "z3"}
MAX_EXPRESSION_LENGTH = 500
_ALLOWED_EXPRESSION = re.compile(r"^[A-Za-z0-9_+\-*/()., ^]+$")


@dataclass(frozen=True)
class ProofObligation:
    lhs: str
    rhs: str
    assumptions: list[str]
    backend: str
    status: str
    reason: str
    evidence: list[dict]


def _backend_evidence(kind: str, backend: str, backend_status: str, reason: str, *, lhs: str, rhs: str, assumptions: list[str], severity: str) -> dict:
    return {
        "kind": kind,
        "backend": backend,
        "backend_status": backend_status,
        "reason": reason,
        "normalized_lhs": normalize_math_text(lhs),
        "normalized_rhs": normalize_math_text(rhs),
        "assumptions": assumptions,
        "severity": severity,
    }


def _validate_expression_input(lhs: str, rhs: str) -> str | None:
    if len(lhs) > MAX_EXPRESSION_LENGTH or len(rhs) > MAX_EXPRESSION_LENGTH:
        return f"Expressions must be at most {MAX_EXPRESSION_LENGTH} characters."
    if not _ALLOWED_EXPRESSION.fullmatch(lhs) or not _ALLOWED_EXPRESSION.fullmatch(rhs):
        return "Expressions may only contain symbols, numbers, arithmetic operators, parentheses, commas, spaces, and dots."
    return None


def _sympy_check(lhs: str, rhs: str, assumptions: list[str]) -> tuple[str, dict]:
    validation_error = _validate_expression_input(lhs, rhs)
    if validation_error is not None:
        evidence = _backend_evidence(
            "backend_not_encodable",
            "sympy",
            "not_encodable",
            validation_error,
            lhs=lhs,
            rhs=rhs,
            assumptions=assumptions,
            severity="diagnostic",
        )
        return "inconclusive", evidence
    if find_spec("sympy") is None:
        evidence = _backend_evidence(
            "backend_unavailable",
            "sympy",
            "unavailable",
            "SymPy is not installed in this environment.",
            lhs=lhs,
            rhs=rhs,
            assumptions=assumptions,
            severity="diagnostic",
        )
        return "inconclusive", evidence
    try:
        import sympy as sp
        from sympy.parsing.sympy_parser import parse_expr

        lhs_expr = parse_expr(lhs, evaluate=False)
        rhs_expr = parse_expr(rhs, evaluate=False)
        difference = sp.simplify(lhs_expr - rhs_expr)
    except Exception as exc:
        evidence = _backend_evidence(
            "backend_not_encodable",
            "sympy",
            "not_encodable",
            f"SymPy could not encode this obligation: {exc}",
            lhs=lhs,
            rhs=rhs,
            assumptions=assumptions,
            severity="diagnostic",
        )
        return "inconclusive", evidence

    if difference == 0:
        evidence = _backend_evidence(
            "backend_verified",
            "sympy",
            "proved",
            "SymPy simplified lhs - rhs to zero.",
            lhs=lhs,
            rhs=rhs,
            assumptions=assumptions,
            severity="certifying",
        )
        evidence["backend_expression"] = str(difference)
        return "equivalent", evidence
    if difference.is_number and difference != 0:
        evidence = _backend_evidence(
            "backend_counterexample",
            "sympy",
            "disproved",
            "SymPy simplified lhs - rhs to a nonzero numeric value.",
            lhs=lhs,
            rhs=rhs,
            assumptions=assumptions,
            severity="blocking",
        )
        evidence["backend_expression"] = str(difference)
        return "mismatch", evidence

    evidence = _backend_evidence(
        "backend_unknown",
        "sympy",
        "unknown",
        "SymPy could not certify or refute this obligation by simplification.",
        lhs=lhs,
        rhs=rhs,
        assumptions=assumptions,
        severity="diagnostic",
    )
    evidence["backend_expression"] = str(difference)
    return "unverified", evidence


def _unimplemented_backend(backend: str, lhs: str, rhs: str, assumptions: list[str]) -> tuple[str, dict]:
    evidence = _backend_evidence(
        "backend_not_encodable",
        backend,
        "not_encodable",
        f"The {backend} adapter is planned but not implemented for this bounded proof-obligation slice.",
        lhs=lhs,
        rhs=rhs,
        assumptions=assumptions,
        severity="diagnostic",
    )
    return "inconclusive", evidence


def check_proof_obligation(lhs: str, rhs: str, assumptions: list[str] | None = None, backend: str = "auto") -> dict:
    if backend not in BACKENDS:
        evidence = _backend_evidence(
            "backend_not_encodable",
            backend,
            "not_encodable",
            f"Unsupported backend: {backend}.",
            lhs=lhs,
            rhs=rhs,
            assumptions=assumptions or [],
            severity="diagnostic",
        )
        result = ProofObligation(
            lhs=lhs,
            rhs=rhs,
            assumptions=assumptions or [],
            backend=backend,
            status="inconclusive",
            reason="The requested backend is not supported.",
            evidence=[evidence],
        )
        return attach_contract(asdict(result), "proof_obligation_result")

    assumption_list = assumptions or []
    baseline = derive_step(lhs, rhs)
    if baseline["status"] == "equivalent":
        evidence = _backend_evidence(
            "normalized_match",
            "normalizer",
            "proved",
            "The two sides match after MathDevMCP normalization.",
            lhs=lhs,
            rhs=rhs,
            assumptions=assumption_list,
            severity="certifying",
        )
        result = ProofObligation(
            lhs=lhs,
            rhs=rhs,
            assumptions=assumption_list,
            backend=backend,
            status="equivalent",
            reason="The proof obligation is certified by exact normalization.",
            evidence=[evidence],
        )
        return attach_contract(asdict(result), "proof_obligation_result")

    if backend in {"auto", "sympy"}:
        status, evidence = _sympy_check(lhs, rhs, assumption_list)
        if status in {"equivalent", "mismatch"} or backend == "sympy":
            result = ProofObligation(
                lhs=lhs,
                rhs=rhs,
                assumptions=assumption_list,
                backend="sympy" if backend == "sympy" else "auto",
                status=status,
                reason=evidence["reason"],
                evidence=[evidence],
            )
            return attach_contract(asdict(result), "proof_obligation_result")
        baseline["evidence"].append(evidence)

    if backend in {"sage", "z3"}:
        status, evidence = _unimplemented_backend(backend, lhs, rhs, assumption_list)
        result = ProofObligation(
            lhs=lhs,
            rhs=rhs,
            assumptions=assumption_list,
            backend=backend,
            status=status,
            reason=evidence["reason"],
            evidence=[evidence],
        )
        return attach_contract(asdict(result), "proof_obligation_result")

    result = ProofObligation(
        lhs=lhs,
        rhs=rhs,
        assumptions=assumption_list,
        backend=backend,
        status=baseline["status"],
        reason=baseline["reason"],
        evidence=baseline["evidence"],
    )
    return attach_contract(asdict(result), "proof_obligation_result")
