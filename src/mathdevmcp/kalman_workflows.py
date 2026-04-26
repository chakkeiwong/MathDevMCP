from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path

from .agent_workflows import audit_likelihood_implementation
from .contracts import attach_contract
from .diagnostic_tests import suggest_diagnostic_tests
from .notation import infer_symbol_hints
from .review_packet import build_likelihood_review_packet


KALMAN_LIKELIHOOD_OPERATIONS = ["logdet", "inverse_or_solve", "quadratic_form"]


@dataclass(frozen=True)
class KalmanAuditResult:
    status: str
    reason: str
    likelihood_audit: dict
    symbol_hints: dict
    diagnostic_suggestions: dict


def audit_kalman_likelihood(doc_root: str, label: str, code_path: str, *, context_text: str = "Kalman innovation covariance residual likelihood") -> dict:
    likelihood = audit_likelihood_implementation(
        doc_root,
        label,
        code_path,
        required_operations=KALMAN_LIKELIHOOD_OPERATIONS,
        context_text=context_text,
    )
    symbols = [symbol["name"] for obligation in likelihood["proof_audit"].get("obligations", []) for symbol in obligation.get("evidence", []) if False]
    if not symbols:
        symbols = ["S_t", "v_t", "F_t", "H_t"]
    hints = infer_symbol_hints(symbols, context_text=context_text)
    diagnostics = suggest_diagnostic_tests(likelihood)
    if likelihood["status"] == "mismatch":
        status = "mismatch"
        reason = "Kalman likelihood implementation is missing required likelihood operations."
    elif likelihood["status"] == "unverified":
        status = "unverified"
        reason = "Kalman likelihood operations are present or partially present, but assumptions/proof need review."
    else:
        status = "consistent"
        reason = "Kalman likelihood audit found the required operation-level evidence."
    result = KalmanAuditResult(status, reason, likelihood, hints, diagnostics)
    return attach_contract(asdict(result), "kalman_likelihood_audit", doc_context=likelihood.get("provenance"))


def build_kalman_review_packet(doc_root: str, label: str, code_path: str, *, context_text: str = "Kalman innovation covariance residual likelihood") -> dict:
    packet = build_likelihood_review_packet(
        doc_root,
        label,
        code_path,
        required_operations=KALMAN_LIKELIHOOD_OPERATIONS,
        context_text=context_text,
    )
    kalman = audit_kalman_likelihood(doc_root, label, code_path, context_text=context_text)
    packet["summary"] = f"Kalman likelihood review for {label} is {packet['status']} with {packet['severity']} severity."
    packet["evidence"]["kalman_likelihood_audit"] = kalman
    packet["recommended_actions"].extend(kalman["diagnostic_suggestions"].get("suggestions", []))
    return attach_contract(packet, "kalman_review_packet")
