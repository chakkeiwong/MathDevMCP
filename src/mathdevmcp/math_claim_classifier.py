from __future__ import annotations

"""Conservative classification of mathematical claim support."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract
from .math_debugging import CERTIFICATION_BOUNDARY


PROOF_CLASSIFICATIONS = {"backend_proved", "derived_identity"}


@dataclass(frozen=True)
class MathClaimClassification:
    claim: str
    classification: str
    reason: str
    evidence_sources: list[str]
    next_action: str
    proof_boundary: str
    diagnostics: list[dict[str, Any]]


def _metadata_contract(evidence: dict[str, Any]) -> str:
    metadata = evidence.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("contract"), str):
        return metadata["contract"]
    return ""


def _workbench_status(evidence: dict[str, Any]) -> str:
    workbench = evidence.get("workbench_result")
    if isinstance(workbench, dict) and isinstance(workbench.get("status"), str):
        return workbench["status"]
    status = evidence.get("status")
    return status if isinstance(status, str) else ""


def _backend_attempts(evidence: dict[str, Any]) -> list[dict[str, Any]]:
    attempts = evidence.get("backend_attempts")
    if isinstance(attempts, list):
        return [attempt for attempt in attempts if isinstance(attempt, dict)]
    workbench = evidence.get("workbench_result")
    if isinstance(workbench, dict) and isinstance(workbench.get("backend_attempts"), list):
        return [attempt for attempt in workbench["backend_attempts"] if isinstance(attempt, dict)]
    route = evidence.get("route_decision")
    if isinstance(route, dict) and isinstance(route.get("backend_attempt"), dict):
        return [route["backend_attempt"]]
    return []


def _has_certifying_backend(evidence: dict[str, Any]) -> bool:
    for attempt in _backend_attempts(evidence):
        if attempt.get("severity") == "certifying" and attempt.get("status") in {"proved", "verified", "equivalent"}:
            return True
    status = _workbench_status(evidence)
    contract = _metadata_contract(evidence)
    return status == "proved" and contract in {"derive_or_refute_result", "prove_or_refute_result", "proof_gap_result"}


def _evidence_source(evidence: dict[str, Any]) -> str:
    contract = _metadata_contract(evidence)
    if contract:
        return contract
    status = evidence.get("status")
    if isinstance(status, str):
        return f"status:{status}"
    return "untyped_evidence"


def _classify_from_evidence(claim: str, evidence: dict[str, Any]) -> tuple[str, str, str]:
    lowered = claim.lower()
    contract = _metadata_contract(evidence)
    status = _workbench_status(evidence)

    if status == "refuted" or evidence.get("counterexample") or evidence.get("counterexamples"):
        return "refuted", "Evidence contains a concrete refutation or refuted workbench status.", "inspect_counterexample"
    if status == "not_encodable":
        return "not_encodable", "The claim could not be encoded by the available route.", "rewrite_claim_or_select_backend"
    if status == "backend_unavailable":
        return "unsupported", "The requested backend was unavailable; this is not refutation.", "install_or_select_available_backend"
    if _has_certifying_backend(evidence):
        if contract == "derive_or_refute_result":
            return "derived_identity", "A scoped derivation obligation was certified by backend evidence.", "preserve_backend_certificate"
        return "backend_proved", "A scoped proof obligation was certified by backend evidence.", "preserve_backend_certificate"
    if contract == "equation_code_match_result":
        return "unsupported", "Structural code/equation matching is diagnostic and not mathematical proof.", "run_proof_or_human_review"
    if contract == "claim_support_packet":
        claim_status = evidence.get("claim_status")
        if claim_status == "model_assumption":
            return "assumption", "Claim-support packet marks this as a model assumption.", "record_assumption_scope"
        if claim_status == "empirical_regularity":
            return "empirical", "Claim-support packet marks this as empirical.", "link_data_or_experiment_evidence"
        if claim_status == "exact_identity":
            return "unsupported", "An exact-identity label still needs backend proof evidence.", "run_proof_or_refutation"
    if evidence.get("numeric") or status in {"numeric_supported", "diagnostic_evidence"}:
        return "numeric_supported", "Numeric evidence is diagnostic support only.", "seek_symbolic_proof_or_counterexample"
    if "define" in lowered or "definition" in lowered or ":=" in claim:
        return "definition", "Claim text appears definitional; applicability still depends on scope.", "record_definition_source"
    if "assume" in lowered or "assumption" in lowered:
        return "assumption", "Claim text is explicitly framed as an assumption.", "record_assumption_scope"
    return "unsupported", "No certifying or refuting evidence was supplied.", "run_derive_or_refute_or_add_source"


def classify_math_claim(claim: str, *, evidence: list[dict[str, Any]] | None = None) -> dict:
    evidence_items = evidence or []
    if not all(isinstance(item, dict) for item in evidence_items):
        raise ValueError("evidence must be a list of objects")

    diagnostics: list[dict[str, Any]] = []
    sources = [_evidence_source(item) for item in evidence_items]
    classifications = []
    for index, item in enumerate(evidence_items):
        classification, reason, next_action = _classify_from_evidence(claim, item)
        diagnostics.append(
            {
                "index": index,
                "source": sources[index],
                "classification": classification,
                "reason": reason,
                "next_action": next_action,
            }
        )
        classifications.append((classification, reason, next_action))

    if not classifications:
        classification, reason, next_action = _classify_from_evidence(claim, {})
    else:
        priority = [
            "refuted",
            "not_encodable",
            "backend_proved",
            "derived_identity",
            "assumption",
            "definition",
            "numeric_supported",
            "empirical",
            "unsupported",
        ]
        best = min(classifications, key=lambda item: priority.index(item[0]) if item[0] in priority else len(priority))
        classification, reason, next_action = best

    return attach_contract(
        asdict(
            MathClaimClassification(
                claim=claim,
                classification=classification,
                reason=reason,
                evidence_sources=sources,
                next_action=next_action,
                proof_boundary=CERTIFICATION_BOUNDARY,
                diagnostics=diagnostics,
            )
        ),
        "math_claim_classification",
    )
