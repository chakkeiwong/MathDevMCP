from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib.util import find_spec
import re

from .contracts import attach_contract
from .proof_obligations import check_proof_obligation


@dataclass(frozen=True)
class SymbolicBackendResult:
    status: str
    reason: str
    backend: str
    evidence: list[dict]


_SAFE = re.compile(r"^[A-Za-z0-9_+\-*/()., ^]+$")


def check_symbolic_obligation(lhs: str, rhs: str, *, backend: str = "auto") -> dict:
    if not (_SAFE.fullmatch(lhs) and _SAFE.fullmatch(rhs)):
        evidence = [{"kind": "backend_not_encodable", "backend": backend, "reason": "Expression is outside the conservative symbolic grammar.", "severity": "diagnostic"}]
        return attach_contract(asdict(SymbolicBackendResult("inconclusive", evidence[0]["reason"], backend, evidence)), "symbolic_backend_result")
    if backend in {"auto", "sympy"}:
        result = check_proof_obligation(lhs, rhs, backend="sympy")
        return attach_contract(asdict(SymbolicBackendResult(result["status"], result["reason"], "sympy", result["evidence"])), "symbolic_backend_result")
    if backend == "sage":
        if find_spec("sageall") is None and find_spec("sage.all") is None:
            evidence = [{"kind": "backend_unavailable", "backend": "sage", "reason": "Sage Python module is not importable in this environment.", "severity": "diagnostic"}]
            return attach_contract(asdict(SymbolicBackendResult("inconclusive", evidence[0]["reason"], "sage", evidence)), "symbolic_backend_result")
    evidence = [{"kind": "backend_not_encodable", "backend": backend, "reason": f"Unsupported symbolic backend: {backend}.", "severity": "diagnostic"}]
    return attach_contract(asdict(SymbolicBackendResult("inconclusive", evidence[0]["reason"], backend, evidence)), "symbolic_backend_result")
