"""Conservative temporal-binding audits for DSGE-style residual code."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re
from typing import Any

from .contracts import attach_contract, contract_metadata
from .latex_index import build_index, extract_context_for_label


@dataclass(frozen=True)
class TemporalBindingFinding:
    symbol: str
    role: str
    required_code_names: list[str]
    forbidden_code_names: list[str]
    status: str
    matched_names: list[str]
    forbidden_matches: list[str]
    reason: str


@dataclass(frozen=True)
class TemporalContractAudit:
    label: str
    doc_root: str
    code_path: str
    status: str
    reason: str
    findings: list[dict[str, Any]]
    doc_context: dict[str, Any]
    verification_boundary: str
    metadata: dict[str, str]


def _read_code(code: str | Path) -> tuple[str, str]:
    path = Path(code)
    return path.read_text(encoding="utf-8"), str(path)


def _contains_name(code_text: str, name: str) -> bool:
    pattern = rf"(?<![A-Za-z0-9_]){re.escape(name)}(?![A-Za-z0-9_])"
    return re.search(pattern, code_text) is not None


def _binding_finding(symbol: str, spec: dict[str, Any], code_text: str) -> TemporalBindingFinding:
    required = [str(item) for item in spec.get("code_names", [])]
    forbidden = [str(item) for item in spec.get("forbidden_code_names", [])]
    role = str(spec.get("role", ""))
    matched = [name for name in required if _contains_name(code_text, name)]
    forbidden_matches = [name for name in forbidden if _contains_name(code_text, name)]
    if forbidden_matches:
        status = "mismatch"
        reason = f"Forbidden timing names were present for {symbol}: {', '.join(forbidden_matches)}."
    elif matched:
        status = "matched"
        reason = f"Required timing names were present for {symbol}: {', '.join(matched)}."
    else:
        status = "missing"
        reason = f"No required timing names were found for {symbol}."
    return TemporalBindingFinding(
        symbol=symbol,
        role=role,
        required_code_names=required,
        forbidden_code_names=forbidden,
        status=status,
        matched_names=matched,
        forbidden_matches=forbidden_matches,
        reason=reason,
    )


def _aggregate_status(findings: list[TemporalBindingFinding]) -> tuple[str, str]:
    if any(finding.status == "mismatch" for finding in findings):
        return "mismatch", "At least one temporal binding used a forbidden timing source."
    if any(finding.status == "missing" for finding in findings):
        return "unverified", "No mismatched timing source was found, but one or more required bindings were missing."
    return "consistent", "All required temporal bindings were found and no forbidden timing sources were detected."


def audit_temporal_contract(root: str, label: str, code: str, required_bindings: dict[str, dict[str, Any]], *, before: int = 1, after: int = 1) -> dict[str, Any]:
    """Audit name-level current/next bindings between a label and code file.

    This workflow is diagnostic. It checks explicit code-name bindings supplied
    by the caller; it does not infer DSGE semantics, solve a model, or certify
    Dynare/reference equivalence.
    """

    index = build_index(Path(root))
    doc_context = extract_context_for_label(index, label, before=before, after=after)
    code_text, code_path = _read_code(code)
    findings = [_binding_finding(symbol, spec, code_text) for symbol, spec in required_bindings.items()]
    status, reason = _aggregate_status(findings)
    report = TemporalContractAudit(
        label=label,
        doc_root=str(Path(root).resolve()),
        code_path=code_path,
        status=status,
        reason=reason,
        findings=[asdict(finding) for finding in findings],
        doc_context=doc_context,
        verification_boundary=(
            "This temporal-contract audit is diagnostic. It checks explicit current/next code-name bindings "
            "against a labeled context, but it does not solve or validate the DSGE model, policy function, "
            "or Dynare/reference equivalence."
        ),
        metadata=contract_metadata("temporal_contract_audit"),
    )
    return attach_contract(asdict(report), "temporal_contract_audit", doc_context=doc_context)
