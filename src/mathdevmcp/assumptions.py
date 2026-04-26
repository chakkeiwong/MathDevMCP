from __future__ import annotations

from dataclasses import asdict, dataclass
import re

from .contracts import attach_contract
from .math_ir import obligation_from_audit_obligation
from .proof_audit import audit_derivation_for_label


@dataclass(frozen=True)
class AssumptionDiagnostic:
    status: str
    explicit_assumptions: list[dict]
    missing_assumptions: list[dict]
    symbol_roles: dict[str, str]
    obligation: dict


_ROLE_PATTERNS = {
    "covariance": r"covariance|S_t|Sigma|Σ",
    "state_vector": r"state vector|x_t|state",
    "shock_vector": r"shock vector|epsilon|shock",
    "transition_matrix": r"transition matrix|transition|A_t",
    "likelihood": r"likelihood|ell_t|\\ell",
    "value_function": r"value function|V\(",
    "policy_function": r"policy function|policy",
    "sdf": r"stochastic discount factor|SDF|pricing kernel",
    "euler_equation": r"Euler equation|euler",
}


def _role_for_symbol(symbol: str, context: str) -> str:
    for role, pattern in _ROLE_PATTERNS.items():
        if re.search(pattern, context, re.IGNORECASE) or re.search(pattern, symbol):
            return role
    return "unknown"


def _explicit_assumptions(context: str) -> list[dict]:
    assumptions: list[dict] = []
    for phrase in ["positive definite", "invertible", "symmetric", "differentiable", "stationary"]:
        if phrase in context.lower():
            assumptions.append({"text": phrase, "status": "explicit_assumption", "source": "context"})
    return assumptions


def _missing_for_ir(ir: dict, explicit: list[dict]) -> list[dict]:
    explicit_text = " ".join(item["text"] for item in explicit).lower()
    missing: list[dict] = []
    unresolved = set(ir.get("unresolved_constructs", []))
    if "matrix_inverse" in unresolved and "invertible" not in explicit_text and "positive definite" not in explicit_text:
        missing.append({"text": "invertibility or positive definiteness for inverse", "status": "inferred_missing_assumption", "source": "unresolved_constructs"})
    if "derivative" in unresolved and "differentiable" not in explicit_text:
        missing.append({"text": "differentiability for derivative", "status": "inferred_missing_assumption", "source": "unresolved_constructs"})
    if "determinant" in unresolved and "positive definite" not in explicit_text and "invertible" not in explicit_text:
        missing.append({"text": "nonzero determinant or positive definiteness", "status": "inferred_missing_assumption", "source": "unresolved_constructs"})
    return missing


def diagnose_assumptions_for_obligation(obligation: dict, *, context_text: str = "") -> dict:
    ir = obligation_from_audit_obligation(obligation)
    explicit = _explicit_assumptions(context_text)
    symbols = {symbol["name"]: _role_for_symbol(symbol["name"], context_text) for symbol in ir.get("symbols", [])}
    result = AssumptionDiagnostic(
        status="missing_assumptions" if _missing_for_ir(ir, explicit) else "ok",
        explicit_assumptions=explicit,
        missing_assumptions=_missing_for_ir(ir, explicit),
        symbol_roles=symbols,
        obligation=ir,
    )
    return attach_contract(asdict(result), "assumption_diagnostic")


def diagnose_assumptions_for_label(root: str, label: str, *, context_text: str = "") -> dict:
    audit = audit_derivation_for_label(root, label, backend="sympy")
    obligation = next((item for item in audit["obligations"] if item.get("lhs") or item.get("rhs")), audit["obligations"][0])
    result = diagnose_assumptions_for_obligation(obligation, context_text=context_text)
    result["label"] = label
    result["doc_context"] = audit.get("doc_context")
    return result
