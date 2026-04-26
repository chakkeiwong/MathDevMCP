from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from pathlib import Path

from .contracts import attach_contract
from .lean_check import check_lean_source
from .latex_index import build_index, extract_context_for_label
from .proof_audit import audit_derivation_for_label


@dataclass(frozen=True)
class DomainFormalizationResult:
    status: str
    reason: str
    domain: str
    obligation: dict
    lean_source: str
    lean_check: dict | None
    missing_assumptions: list[str]
    uses_placeholder_proof: bool


_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_SAFE_EXPR = re.compile(r"^[A-Za-z0-9_+\-*/()., ^]+$")
_UNSUPPORTED_MARKERS = ("\\", "det", "log", "S_t", "v_t", "ell_t")


def _symbols(*expressions: str) -> list[str]:
    return sorted({name for expression in expressions for name in _IDENTIFIER.findall(expression) if not name.isdigit()})


def _unsupported(lhs: str, rhs: str) -> bool:
    return any(marker in lhs or marker in rhs for marker in _UNSUPPORTED_MARKERS) or not (_SAFE_EXPR.fullmatch(lhs) and _SAFE_EXPR.fullmatch(rhs))


def _missing(symbols: list[str], variables: dict[str, str]) -> list[str]:
    return [f"type for {symbol}" for symbol in symbols if symbol not in variables]


def _lean_source(lhs: str, rhs: str, variables: dict[str, str]) -> str:
    binders = " ".join(f"({name} : {variables[name]})" for name in sorted(variables))
    return f"theorem mathdevmcp_domain_obligation {binders} : {lhs} = {rhs} := by\n  exact Nat.add_comm _ _\n"


def formalize_domain_obligation(lhs: str, rhs: str, *, domain: str, variables: dict[str, str]) -> dict:
    obligation = {"lhs": lhs, "rhs": rhs, "domain": domain}
    if _unsupported(lhs, rhs):
        result = DomainFormalizationResult(
            status="unsupported_notation",
            reason="The obligation uses notation outside the current narrow domain formalization vocabulary.",
            domain=domain,
            obligation=obligation,
            lean_source="",
            lean_check=None,
            missing_assumptions=["formal domain notation mapping"],
            uses_placeholder_proof=False,
        )
        return attach_contract(asdict(result), "domain_formalization_result")
    symbols = _symbols(lhs, rhs)
    missing = _missing(symbols, variables)
    if missing:
        result = DomainFormalizationResult(
            status="missing_assumptions",
            reason="The obligation cannot be formalized until every symbol has an explicit type.",
            domain=domain,
            obligation=obligation,
            lean_source="",
            lean_check=None,
            missing_assumptions=missing,
            uses_placeholder_proof=False,
        )
        return attach_contract(asdict(result), "domain_formalization_result")
    if any(value != "Nat" for value in variables.values()):
        result = DomainFormalizationResult(
            status="unsupported_notation",
            reason="The first domain slice only supports Nat-valued scalar algebra.",
            domain=domain,
            obligation=obligation,
            lean_source="",
            lean_check=None,
            missing_assumptions=["Nat scalar type assumptions"],
            uses_placeholder_proof=False,
        )
        return attach_contract(asdict(result), "domain_formalization_result")
    source = _lean_source(lhs, rhs, variables)
    lean_result = check_lean_source(source, allow_sorry=False)
    status = "domain_verified" if lean_result["status"] == "verified" else lean_result["status"]
    result = DomainFormalizationResult(
        status=status,
        reason="The curated domain obligation was verified by Lean." if status == "domain_verified" else lean_result["reason"],
        domain=domain,
        obligation=obligation,
        lean_source=source,
        lean_check=lean_result,
        missing_assumptions=[],
        uses_placeholder_proof=False,
    )
    return attach_contract(asdict(result), "domain_formalization_result")


def formalize_domain_label(root: str, label: str, *, domain: str, variables: dict[str, str]) -> dict:
    audit = audit_derivation_for_label(root, label, backend="sympy")
    obligation = next((item for item in audit["obligations"] if item.get("lhs") or item.get("rhs")), audit["obligations"][0])
    result = formalize_domain_obligation(obligation.get("lhs", ""), obligation.get("rhs", ""), domain=domain, variables=variables)
    result["obligation"] = {**result["obligation"], "source_obligation_id": obligation.get("id"), "provenance": obligation.get("provenance")}
    index = build_index(Path(root))
    doc_context = extract_context_for_label(index, label, before=0, after=0)
    result["doc_context"] = doc_context
    return attach_contract(result, "domain_formalization_result", doc_context=doc_context)
