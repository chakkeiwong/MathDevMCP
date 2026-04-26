from __future__ import annotations

from dataclasses import asdict, dataclass
import re

from .contracts import attach_contract


@dataclass(frozen=True)
class NotationRecord:
    symbol: str
    role: str
    status: str
    source_text: str


_ROLE_KEYWORDS = {
    "covariance_matrix": ["covariance", "positive definite", "spd"],
    "state_vector": ["state vector", "state"],
    "shock_vector": ["shock vector", "shock"],
    "transition_matrix": ["transition matrix", "transition"],
    "likelihood": ["likelihood", "log likelihood"],
    "sdf": ["stochastic discount factor", "pricing kernel", "sdf"],
    "euler_equation": ["euler equation"],
}


def extract_notation_records(text: str) -> dict:
    records: list[dict] = []
    for match in re.finditer(r"([A-Za-z]_[A-Za-z0-9]+|[A-Z])\s+(?:is|denotes|represents)\s+([^.;\n]+)", text):
        symbol, desc = match.group(1), match.group(2)
        desc_lower = desc.lower()
        role = "unknown"
        for candidate, keywords in _ROLE_KEYWORDS.items():
            if any(keyword in desc_lower for keyword in keywords):
                role = candidate
                break
        records.append(asdict(NotationRecord(symbol, role, "explicit_notation", match.group(0))))
    return attach_contract({"records": records}, "notation_records")


def infer_symbol_hints(symbols: list[str], context_text: str = "") -> dict:
    hints: dict[str, dict] = {}
    context = context_text.lower()
    for symbol in symbols:
        role = "unknown"
        shape = "unknown"
        if symbol.startswith("S") or "covariance" in context:
            role = "covariance_candidate"
            shape = "matrix_candidate"
        elif symbol.startswith("v") or "residual" in context:
            role = "residual_candidate"
            shape = "vector_candidate"
        elif symbol.endswith("_t"):
            role = "time_indexed_candidate"
        hints[symbol] = {"role_hint": role, "shape_hint": shape, "status": "candidate_not_assumption"}
    return attach_contract({"hints": hints}, "symbol_hints")
