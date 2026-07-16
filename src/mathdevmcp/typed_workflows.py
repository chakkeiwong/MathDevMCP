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
    source: dict
    typed_diagnostic: dict


def _context_text(root: str, label: str, *, file: str | None = None) -> str:
    index = build_index(Path(root))
    context = extract_context_for_label(index, label, before=2, after=2, file=file)
    return "\n".join(line.get("text", "") for line in context.get("excerpt", []))


def typed_obligation_for_label(root: str, label: str, *, backend: str = "sympy", context_text: str = "", file: str | None = None, source_digest: str | None = None) -> dict:
    audit = audit_derivation_for_label(root, label, backend=backend, file=file, source_digest=source_digest)
    obligation = next((item for item in audit["obligations"] if item.get("lhs") or item.get("rhs")), audit["obligations"][0])
    context = context_text or _context_text(root, label, file=file)
    typed = diagnose_typed_obligation(obligation, context_text=context)
    extraction = audit.get("target_extraction")
    targets = extraction.get("targets", []) if isinstance(extraction, dict) else []
    candidate = targets[0] if len(targets) == 1 and isinstance(targets[0], dict) else None
    observed_digest = (
        candidate.get("label_scoped_obligation", {}).get("document", {}).get("source_digest")
        if candidate is not None
        else None
    )
    source_binding_accepted = source_digest is None or observed_digest == source_digest
    canonical = candidate if source_binding_accepted else None
    source = (
        {
            "file": canonical.get("file"),
            "label": canonical.get("label"),
            "line_start": canonical.get("line_start"),
            "line_end": canonical.get("line_end"),
            "target": canonical.get("target"),
            "obligation_id": canonical.get("obligation_id"),
            "obligation_digest": canonical.get("obligation_digest"),
            "source_digest": canonical.get("label_scoped_obligation", {}).get("document", {}).get("source_digest"),
            "target_ingress": "validated_label_scoped_obligation",
        }
        if canonical
        else {"label": label, "file": file, "source_digest": source_digest, "status": "unresolved_source_target"}
    )
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
        source=source,
        typed_diagnostic=typed,
    )
    return attach_contract(asdict(result), "typed_obligation_label_diagnostic", doc_context=audit.get("doc_context"))
