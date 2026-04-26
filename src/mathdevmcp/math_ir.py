from __future__ import annotations

from dataclasses import asdict, dataclass
import re
from typing import Literal

from .contracts import contract_metadata


ObligationKind = Literal["equation", "inequality", "definition", "unknown"]
Suitability = Literal["normalization", "symbolic", "lean_candidate", "human_review"]


@dataclass(frozen=True)
class SymbolRecord:
    name: str
    role: str
    source: str


@dataclass(frozen=True)
class AssumptionRecord:
    text: str
    status: str
    source: str


@dataclass(frozen=True)
class MathObligation:
    id: str
    kind: ObligationKind
    lhs: str
    rhs: str
    raw_text: str
    parser_backend: str
    symbols: list[dict]
    assumptions: list[dict]
    unresolved_constructs: list[str]
    backend_suitability: Suitability
    provenance: dict
    metadata: dict[str, str]


_UNRESOLVED_PATTERNS = {
    "derivative": r"\\partial|\\nabla|Derivative",
    "matrix_inverse": r"\^-1|\^{-1}|inverse",
    "trace": r"\\operatorname\{tr\}|\\tr|trace",
    "determinant": r"\\det|logdet|det",
    "expectation": r"\\mathbb\{E\}|E\[|expectation",
    "transpose": r"'|\\top|transpose",
}


def _symbols(text: str) -> list[dict]:
    names = sorted({token for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text) if token not in {"begin", "end", "label"}})
    return [asdict(SymbolRecord(name=name, role="unknown", source="expression")) for name in names]


def _unresolved(text: str) -> list[str]:
    return [name for name, pattern in _UNRESOLVED_PATTERNS.items() if re.search(pattern, text)]


def _kind(lhs: str, rhs: str) -> ObligationKind:
    if lhs and rhs:
        return "equation"
    return "unknown"


def _suitability(unresolved_constructs: list[str], lhs: str, rhs: str) -> Suitability:
    if unresolved_constructs:
        return "human_review"
    if lhs == rhs:
        return "normalization"
    if re.fullmatch(r"[A-Za-z0-9_+\-*/()., ^]+", lhs) and re.fullmatch(r"[A-Za-z0-9_+\-*/()., ^]+", rhs):
        return "symbolic"
    return "human_review"


def obligation_from_audit_obligation(obligation: dict, *, parser_backend: str = "current") -> dict:
    lhs = str(obligation.get("lhs", ""))
    rhs = str(obligation.get("rhs", ""))
    raw_text = str(obligation.get("source_text") or f"{lhs} = {rhs}")
    unresolved = _unresolved(raw_text)
    result = MathObligation(
        id=str(obligation.get("id", "")),
        kind=_kind(lhs, rhs),
        lhs=lhs,
        rhs=rhs,
        raw_text=raw_text,
        parser_backend=parser_backend,
        symbols=_symbols(raw_text),
        assumptions=[],
        unresolved_constructs=unresolved,
        backend_suitability=_suitability(unresolved, lhs, rhs),
        provenance=obligation.get("provenance", {}) if isinstance(obligation.get("provenance", {}), dict) else {},
        metadata=contract_metadata("math_obligation"),
    )
    return asdict(result)


def validate_math_obligation(payload: dict) -> list[str]:
    errors: list[str] = []
    if payload.get("metadata", {}).get("contract") != "math_obligation":
        errors.append("metadata.contract must be math_obligation")
    for field in ["id", "kind", "lhs", "rhs", "raw_text", "parser_backend", "backend_suitability"]:
        if field not in payload:
            errors.append(f"missing {field}")
    if payload.get("kind") not in {"equation", "inequality", "definition", "unknown"}:
        errors.append("kind is invalid")
    if payload.get("backend_suitability") not in {"normalization", "symbolic", "lean_candidate", "human_review"}:
        errors.append("backend_suitability is invalid")
    if not isinstance(payload.get("symbols", []), list):
        errors.append("symbols must be a list")
    if not isinstance(payload.get("unresolved_constructs", []), list):
        errors.append("unresolved_constructs must be a list")
    return errors
