from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .contracts import attach_contract
from .latex_index import build_index, extract_context_for_label
from .math_ir import diagnose_typed_obligation
from .proof_audit import audit_derivation_for_label


@dataclass(frozen=True)
class TypedObligationLabelDiagnostic:
    status: str
    reason: str
    label: str
    doc_context: dict
    typed_diagnostic: dict


def _context_text(root: str, label: str) -> str:
    index = build_index(Path(root))
    context = extract_context_for_label(index, label, before=2, after=2)
    return "\n".join(line.get("text", "") for line in context.get("excerpt", []))


def typed_obligation_for_label(root: str, label: str, *, backend: str = "sympy", context_text: str = "") -> dict:
    audit = audit_derivation_for_label(root, label, backend=backend)
    obligation = next((item for item in audit["obligations"] if item.get("lhs") or item.get("rhs")), audit["obligations"][0])
    context = context_text or _context_text(root, label)
    typed = diagnose_typed_obligation(obligation, context_text=context)
    if typed["status"] == "needs_assumptions":
        status = "unverified"
        reason = "Typed obligation diagnostics found missing assumptions or dimension constraints."
    elif typed["status"] == "typed_review":
        status = "unverified"
        reason = "Typed obligation contains structured notation that requires review or backend routing."
    else:
        status = "consistent"
        reason = "Typed obligation metadata is ready for bounded backend routing."
    result = TypedObligationLabelDiagnostic(
        status=status,
        reason=reason,
        label=label,
        doc_context=audit.get("doc_context", {}),
        typed_diagnostic=typed,
    )
    return attach_contract(asdict(result), "typed_obligation_label_diagnostic", doc_context=audit.get("doc_context"))
