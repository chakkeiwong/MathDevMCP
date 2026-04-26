from __future__ import annotations

from dataclasses import asdict, dataclass
import re

from .contracts import attach_contract


@dataclass(frozen=True)
class LeanArtifact:
    source_obligation_id: str
    theorem_name: str
    formalization_status: str
    certified: bool
    lean_source: str
    source_text: str
    provenance: dict
    missing_assumptions: list[str]


@dataclass(frozen=True)
class LeanExportResult:
    status: str
    reason: str
    target: str
    namespace: str
    artifacts: list[dict]
    counts: dict[str, int]


_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
_SAFE_EXPR = re.compile(r"^[A-Za-z0-9_+\-*/()., ^]+$")


def _sanitize_identifier(value: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9_]+", "_", value).strip("_").lower()
    if not safe:
        safe = "obligation"
    if safe[0].isdigit():
        safe = f"obligation_{safe}"
    return safe


def _symbols(*expressions: str) -> list[str]:
    names: set[str] = set()
    for expression in expressions:
        for name in _IDENTIFIER.findall(expression):
            if not name.isdigit():
                names.add(name)
    return sorted(names)


def _is_safe_expression(lhs: str, rhs: str) -> bool:
    return bool(lhs and rhs and _SAFE_EXPR.fullmatch(lhs) and _SAFE_EXPR.fullmatch(rhs))


def _lean_source(theorem_name: str, lhs: str, rhs: str, symbols: list[str], namespace: str, target: str) -> str:
    binders = f"({' '.join(symbols)} : {target})" if symbols else ""
    theorem_line = f"theorem {theorem_name} {binders} : {lhs} = {rhs} := by" if binders else f"theorem {theorem_name} : {lhs} = {rhs} := by"
    return f"namespace {namespace}\n\n{theorem_line}\n  sorry\n\nend {namespace}\n"


def _artifact_for_obligation(obligation: dict, namespace: str, target: str) -> dict:
    theorem_name = f"mathdevmcp_{_sanitize_identifier(str(obligation.get('id', 'obligation')))}"
    lhs = str(obligation.get("lhs", ""))
    rhs = str(obligation.get("rhs", ""))
    source_text = str(obligation.get("source_text", ""))
    provenance = obligation.get("provenance", {}) if isinstance(obligation.get("provenance", {}), dict) else {}
    if obligation.get("classification") in {"human_review", "not_extracted"} or not _is_safe_expression(lhs, rhs):
        return asdict(
            LeanArtifact(
                source_obligation_id=str(obligation.get("id", "")),
                theorem_name=theorem_name,
                formalization_status="needs_human_formalization",
                certified=False,
                lean_source="",
                source_text=source_text,
                provenance=provenance,
                missing_assumptions=["formal notation mapping"],
            )
        )
    if target == "raw":
        return asdict(
            LeanArtifact(
                source_obligation_id=str(obligation.get("id", "")),
                theorem_name=theorem_name,
                formalization_status="missing_type_assumptions",
                certified=False,
                lean_source="",
                source_text=source_text,
                provenance=provenance,
                missing_assumptions=["target type for symbols"],
            )
        )
    if target not in {"Nat", "Real"}:
        return asdict(
            LeanArtifact(
                source_obligation_id=str(obligation.get("id", "")),
                theorem_name=theorem_name,
                formalization_status="needs_human_formalization",
                certified=False,
                lean_source="",
                source_text=source_text,
                provenance=provenance,
                missing_assumptions=[f"unsupported Lean target type: {target}"],
            )
        )
    symbols = _symbols(lhs, rhs)
    return asdict(
        LeanArtifact(
            source_obligation_id=str(obligation.get("id", "")),
            theorem_name=theorem_name,
            formalization_status="skeleton_only",
            certified=False,
            lean_source=_lean_source(theorem_name, lhs, rhs, symbols, namespace, target),
            source_text=source_text,
            provenance=provenance,
            missing_assumptions=[],
        )
    )


def _counts(artifacts: list[dict]) -> dict[str, int]:
    counts = {
        "total": len(artifacts),
        "skeleton_only": 0,
        "needs_human_formalization": 0,
        "missing_type_assumptions": 0,
        "verified": 0,
    }
    for artifact in artifacts:
        status = artifact["formalization_status"]
        if status in counts:
            counts[status] += 1
        if artifact.get("certified") is True:
            counts["verified"] += 1
    return counts


def export_lean_obligations(obligations: list[dict], *, namespace: str = "MathDevMCP", target: str = "Nat") -> dict:
    artifacts = [_artifact_for_obligation(obligation, namespace, target) for obligation in obligations]
    counts = _counts(artifacts)
    if counts["skeleton_only"] and counts["skeleton_only"] == counts["total"]:
        status = "skeleton_only"
        reason = "All exportable obligations were emitted as Lean skeletons with placeholders."
    elif counts["skeleton_only"]:
        status = "partial"
        reason = "Some obligations were emitted as Lean skeletons; others need formalization work."
    else:
        status = "needs_human_formalization"
        reason = "No obligation was safe to export as a typed Lean skeleton."
    result = LeanExportResult(status=status, reason=reason, target=target, namespace=namespace, artifacts=artifacts, counts=counts)
    return attach_contract(asdict(result), "lean_export_result")
