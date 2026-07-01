from __future__ import annotations

"""Local-only source packet helpers for real high-level pilot obligations."""

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any

from .contracts import attach_contract
from .real_local_high_level_pilot import default_manifest_path


PACKET_CONTRACT = "real_local_source_packet_report"
OBLIGATION_CONTRACT = "real_local_source_obligation_ir_report"
ADAPTER_RESULT_CONTRACT = "real_local_source_adapter_result"
PACKET_MAX_CONTEXT_LINES = 2


@dataclass(frozen=True)
class SourcePacket:
    case_id: str
    title: str
    source_role: str
    source_path: str
    line_range: str
    line_start: int
    line_end: int
    context_before: int
    context_after: int
    extracted_line_start: int
    extracted_line_end: int
    line_count: int
    excerpt: str
    content_sha256: str
    source_obligation_question: str
    policy_boundary: list[str]


ROUTE_REQUIREMENTS: dict[str, dict[str, Any]] = {
    "RLHL-01-ift-gradient-bias-sign": {
        "adapter_route": "ift_sign_consistency",
        "required_terms": ["G^{\\mathrm{IFT}}", "G^{\\mathrm{FD}}", "\\tilde\\lambda", "dr", "d\\btheta"],
        "required_assumptions": ["source adjoint convention", "theorem-local algebra only"],
    },
    "RLHL-04-kalman-prediction-error-loglik": {
        "adapter_route": "kalman_prediction_error_loglik",
        "required_terms": ["chain rule", "Gaussian", "log\\det", "S_t", "v_t", "observed components"],
        "required_assumptions": ["linear Gaussian state-space model", "positive-definite innovation covariance", "mask policy"],
    },
    "RLHL-06-joseph-covariance-equivalence": {
        "adapter_route": "joseph_covariance_equivalence",
        "required_terms": ["Joseph", "compact", "Kalman gain", "S_t", "R", "rounding"],
        "required_assumptions": ["standard Kalman gain relation", "exact-arithmetic boundary", "numerical caveat"],
    },
    "RLHL-07-affine-pricing-master-recursion": {
        "adapter_route": "affine_pricing_master_recursion",
        "required_terms": ["exponential affine", "Gaussian", "moment", "\\mathcal{A}_n", "\\mathcal{B}_n"],
        "required_assumptions": ["conditional normality", "Gaussian MGF", "coefficient collection"],
    },
    "RLHL-10-kalman-score-same-scalar-contract": {
        "adapter_route": "kalman_score_same_scalar",
        "required_terms": ["logdet", "solve", "S_tw_t=v_t", "score", "same scalar"],
        "required_assumptions": ["invertible innovation covariance", "differentiability", "same-scalar contract"],
    },
}


def _root_path(root: str | Path | None = None) -> Path:
    return Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]


def _parse_line_range(raw: object) -> tuple[int, int]:
    if not isinstance(raw, str) or "-" not in raw:
        raise ValueError("line_range must be a string of the form START-END")
    left, right = raw.split("-", 1)
    try:
        start = int(left)
        end = int(right)
    except ValueError as exc:
        raise ValueError("line_range bounds must be integers") from exc
    if start < 1 or end < start:
        raise ValueError("line_range must satisfy 1 <= start <= end")
    return start, end


def _load_manifest(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _packet_policy_boundary() -> list[str]:
    return [
        "Source packets are local provenance records only.",
        "Source packets are not proof, refutation, scientific validation, or release evidence.",
        "Source packets must not be promoted to benchmark-gate evidence.",
    ]


def _obligation_policy_boundary() -> list[str]:
    return [
        "Obligation IR records are routing and evidence-contract records only.",
        "Obligation IR records are not proof, refutation, scientific validation, or release evidence.",
        "Source, executable-probe, and residual-adapter channels must remain separate.",
        "adapter_required may clear only after a source-anchored local-schema adapter check.",
    ]


def _adapter_policy_boundary() -> list[str]:
    return [
        "Adapter results are local source-obligation diagnostics only.",
        "Adapter results are not release readiness, public benchmark evidence, or broad theorem proving.",
        "Adapter results must preserve source/probe/residual channel separation.",
    ]


def _packet_from_source(
    *,
    root_path: Path,
    case: dict[str, Any],
    source: dict[str, Any],
    context_before: int,
    context_after: int,
) -> SourcePacket:
    raw_path = source.get("path")
    if not isinstance(raw_path, str) or not raw_path:
        raise ValueError("source path must be a non-empty relative string")
    source_path = Path(raw_path)
    if source_path.is_absolute():
        raise ValueError("source path must be relative")
    if context_before < 0 or context_after < 0:
        raise ValueError("context line counts must be non-negative")
    if context_before > PACKET_MAX_CONTEXT_LINES or context_after > PACKET_MAX_CONTEXT_LINES:
        raise ValueError(f"context line counts must be <= {PACKET_MAX_CONTEXT_LINES}")
    start, end = _parse_line_range(source.get("line_range"))
    path = (root_path / source_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"source path does not exist: {raw_path}")
    lines = path.read_text(encoding="utf-8").splitlines()
    extracted_start = max(1, start - context_before)
    extracted_end = min(len(lines), end + context_after)
    if extracted_end < extracted_start:
        raise ValueError("line_range is outside the source file")
    excerpt_lines = lines[extracted_start - 1 : extracted_end]
    excerpt = "\n".join(excerpt_lines)
    digest = hashlib.sha256(excerpt.encode("utf-8")).hexdigest()
    obligation = case.get("source_obligation") if isinstance(case.get("source_obligation"), dict) else {}
    return SourcePacket(
        case_id=str(case.get("id", "")),
        title=str(case.get("title", "")),
        source_role=str(source.get("role", "")),
        source_path=raw_path,
        line_range=str(source.get("line_range", "")),
        line_start=start,
        line_end=end,
        context_before=context_before,
        context_after=context_after,
        extracted_line_start=extracted_start,
        extracted_line_end=extracted_end,
        line_count=len(excerpt_lines),
        excerpt=excerpt,
        content_sha256=digest,
        source_obligation_question=str(obligation.get("question", "")),
        policy_boundary=_packet_policy_boundary(),
    )


def extract_source_packets(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
    *,
    context_before: int = 0,
    context_after: int = 0,
) -> dict[str, Any]:
    """Extract bounded local source packets from the high-level pilot manifest."""
    root_path = _root_path(root)
    path = Path(manifest_path).resolve() if manifest_path is not None else default_manifest_path(root_path)
    findings: list[dict[str, Any]] = []
    packets: list[dict[str, Any]] = []
    try:
        payload = _load_manifest(path)
    except Exception as exc:
        return attach_contract(
            {
                "status": "inconclusive",
                "manifest_path": str(path),
                "packets": [],
                "findings": [{"severity": "high", "kind": "manifest_load_failed", "detail": str(exc)}],
                "summary": {"case_total": 0, "packet_total": 0, "aggregate_accuracy": None},
                "policy_boundary": _packet_policy_boundary(),
            },
            PACKET_CONTRACT,
        )

    raw_cases = payload.get("cases", []) if isinstance(payload, dict) else []
    cases = [case for case in raw_cases if isinstance(case, dict)]
    if len(cases) != len(raw_cases):
        findings.append({"severity": "high", "kind": "manifest_case_not_object"})

    for case in cases:
        case_id = str(case.get("id", "<unknown>"))
        snapshot = case.get("source_snapshot")
        source_files = snapshot.get("source_files") if isinstance(snapshot, dict) else None
        if not isinstance(source_files, list) or not source_files:
            findings.append({"severity": "high", "kind": "source_files_missing", "case_id": case_id})
            continue
        for index, source in enumerate(source_files):
            if not isinstance(source, dict):
                findings.append({"severity": "high", "kind": "source_file_not_object", "case_id": case_id, "index": index})
                continue
            try:
                packets.append(
                    _packet_from_source(
                        root_path=root_path,
                        case=case,
                        source=source,
                        context_before=context_before,
                        context_after=context_after,
                    ).__dict__
                )
            except Exception as exc:
                findings.append(
                    {
                        "severity": "high",
                        "kind": "source_packet_extraction_failed",
                        "case_id": case_id,
                        "index": index,
                        "detail": str(exc),
                    }
                )

    status = "consistent" if not any(item.get("severity") == "high" for item in findings) else "inconclusive"
    return attach_contract(
        {
            "status": status,
            "manifest_path": str(path),
            "packets": packets,
            "findings": findings,
            "summary": {
                "case_total": len(cases),
                "packet_total": len(packets),
                "aggregate_accuracy": None,
            },
            "policy_boundary": _packet_policy_boundary()
            + [
                "Packet status must not clear adapter_required.",
                "Packet extraction does not evaluate the mathematical obligation.",
            ],
        },
        PACKET_CONTRACT,
    )


def _packets_by_case(packets: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for packet in packets:
        case_id = packet.get("case_id")
        if isinstance(case_id, str):
            grouped.setdefault(case_id, []).append(packet)
    return grouped


def _term_present(term: str, packets: list[dict[str, Any]]) -> bool:
    text = "\n".join(str(packet.get("excerpt", "")) for packet in packets).lower()
    normalized = term.lower()
    if normalized in text:
        return True
    aliases = {
        "chain rule": ["chain rule"],
        "gaussian": ["gaussian", "normality", "normal"],
        "moment": ["moment", "mgf"],
        "exponential affine": ["exponential affine", "exponential-affine"],
        "same scalar": ["same scalar", "same-scalar"],
        "solve": ["solve", "s_t w_t", "s_tw_t"],
        "kalman gain": ["kalman gain", "k_t"],
        "compact": ["compact"],
        "rounding": ["rounding"],
    }
    return any(alias in text for alias in aliases.get(normalized, []))


def build_source_obligation_ir(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    """Build route-ready source-obligation IR without clearing any adapter gap."""
    packet_report = extract_source_packets(root=root, manifest_path=manifest_path)
    if packet_report.get("status") != "consistent":
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "Source packets did not validate; obligation IR was not built.",
                "packet_report": packet_report,
                "obligations": [],
                "findings": [{"severity": "high", "kind": "packet_report_inconclusive"}],
                "summary": {"case_total": 0, "obligation_total": 0, "aggregate_accuracy": None},
                "policy_boundary": _obligation_policy_boundary(),
            },
            OBLIGATION_CONTRACT,
        )

    root_path = _root_path(root)
    path = Path(manifest_path).resolve() if manifest_path is not None else default_manifest_path(root_path)
    payload = _load_manifest(path)
    cases = [case for case in payload.get("cases", []) if isinstance(case, dict)]
    grouped = _packets_by_case(packet_report.get("packets", []))
    obligations: list[dict[str, Any]] = []
    findings: list[dict[str, Any]] = []
    for case in cases:
        case_id = str(case.get("id", ""))
        route = ROUTE_REQUIREMENTS.get(case_id)
        case_packets = grouped.get(case_id, [])
        if route is None:
            findings.append({"severity": "high", "kind": "missing_route_requirements", "case_id": case_id})
            continue
        required_terms = list(route["required_terms"])
        present_terms = [term for term in required_terms if _term_present(term, case_packets)]
        missing_terms = [term for term in required_terms if term not in present_terms]
        obligation = case.get("source_obligation", {}) if isinstance(case.get("source_obligation"), dict) else {}
        probe = case.get("executable_probe", {}) if isinstance(case.get("executable_probe"), dict) else {}
        gap = case.get("adapter_gap", {}) if isinstance(case.get("adapter_gap"), dict) else {}
        obligations.append(
            {
                "case_id": case_id,
                "title": case.get("title"),
                "adapter_route": route["adapter_route"],
                "pre_adapter_status": "adapter_required",
                "source_channel": {
                    "question": obligation.get("question"),
                    "expected_boundary": obligation.get("expected_boundary"),
                    "packet_hashes": [packet["content_sha256"] for packet in case_packets],
                    "source_anchors": [
                        {
                            "path": packet["source_path"],
                            "line_start": packet["line_start"],
                            "line_end": packet["line_end"],
                            "content_sha256": packet["content_sha256"],
                        }
                        for packet in case_packets
                    ],
                    "required_terms": required_terms,
                    "present_terms": present_terms,
                    "missing_terms": missing_terms,
                    "required_assumptions": list(route["required_assumptions"]),
                },
                "probe_channel": {
                    "workflow": probe.get("workflow"),
                    "kind": probe.get("kind"),
                    "status": "not_run_in_source_ir",
                    "may_clear_adapter_required": False,
                },
                "residual_adapter_channel": {
                    "status": gap.get("status", "adapter_required"),
                    "needed": gap.get("needed", []),
                    "clearance_requirements": [
                        "source anchors",
                        "required-term coverage",
                        "adapter route",
                        "deterministic check evidence",
                        "non-claims",
                    ],
                    "may_clear_from_probe_or_tests": False,
                },
                "forbidden_claims": case.get("forbidden_claims", []),
                "policy_boundary": _obligation_policy_boundary(),
            }
        )

    status = "consistent" if not any(item.get("severity") == "high" for item in findings) else "inconclusive"
    return attach_contract(
        {
            "status": status,
            "manifest_path": str(path),
            "packet_report": {
                "status": packet_report.get("status"),
                "summary": packet_report.get("summary"),
                "metadata": packet_report.get("metadata"),
            },
            "obligations": obligations,
            "findings": findings,
            "summary": {
                "case_total": len(cases),
                "obligation_total": len(obligations),
                "pre_adapter_required": sum(1 for item in obligations if item.get("pre_adapter_status") == "adapter_required"),
                "aggregate_accuracy": None,
            },
            "policy_boundary": _obligation_policy_boundary(),
        },
        OBLIGATION_CONTRACT,
    )


def _obligation_by_case(ir_report: dict[str, Any], case_id: str) -> dict[str, Any]:
    for obligation in ir_report.get("obligations", []):
        if isinstance(obligation, dict) and obligation.get("case_id") == case_id:
            return obligation
    raise KeyError(f"source obligation not found: {case_id}")


def _packet_text_for_case(root: str | Path | None, manifest_path: str | Path | None, case_id: str) -> str:
    packets = extract_source_packets(root=root, manifest_path=manifest_path).get("packets", [])
    return "\n".join(str(packet.get("excerpt", "")) for packet in packets if packet.get("case_id") == case_id)


def evaluate_ift_sign_adapter(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
    *,
    case_id: str = "RLHL-01-ift-gradient-bias-sign",
) -> dict[str, Any]:
    """Evaluate the local IFT sign-consistency source obligation."""
    ir_report = build_source_obligation_ir(root=root, manifest_path=manifest_path)
    if ir_report.get("status") != "consistent":
        return attach_contract(
            {
                "case_id": case_id,
                "adapter_route": "ift_sign_consistency",
                "status": "inconclusive",
                "reason": "Obligation IR did not validate.",
                "source_anchors": [],
                "checks": {"ir_consistent": False},
                "evidence": [],
                "non_claims": _adapter_policy_boundary(),
            },
            ADAPTER_RESULT_CONTRACT,
        )
    obligation = _obligation_by_case(ir_report, case_id)
    text = _packet_text_for_case(root, manifest_path, case_id)
    theorem_negative = "-\\tilde\\lambda^\\top \\frac{dr}{d\\btheta}" in text
    proof_positive = "= \\tilde\\lambda^\\top \\frac{dr}{d\\btheta}" in text
    adjoint_negative = "\\tilde\\lambda^\\top = -\\bar z^\\top J_z^{-1}" in text
    checks = {
        "ir_consistent": True,
        "route_match": obligation.get("adapter_route") == "ift_sign_consistency",
        "source_anchors_present": bool(obligation.get("source_channel", {}).get("source_anchors")),
        "theorem_negative_sign_present": theorem_negative,
        "proof_positive_sign_present": proof_positive,
        "adjoint_negative_convention_present": adjoint_negative,
        "probe_not_used_for_clearance": obligation.get("probe_channel", {}).get("may_clear_adapter_required") is False,
    }
    mismatch = theorem_negative and proof_positive and adjoint_negative
    status = "inconsistency_candidate" if mismatch and all(checks.values()) else "human_review_required"
    reason = (
        "The bounded source packets contain a negative boxed theorem sign and a positive proof-final sign under the recorded negative adjoint convention."
        if status == "inconsistency_candidate"
        else "The bounded source packets did not contain enough unambiguous sign evidence for this adapter."
    )
    return attach_contract(
        {
            "case_id": case_id,
            "adapter_route": "ift_sign_consistency",
            "status": status,
            "reason": reason,
            "source_anchors": obligation["source_channel"]["source_anchors"],
            "required_terms": obligation["source_channel"]["required_terms"],
            "present_terms": obligation["source_channel"]["present_terms"],
            "checks": checks,
            "evidence": [
                {
                    "kind": "source_sign_comparison",
                    "severity": "diagnostic",
                    "theorem_sign": "negative" if theorem_negative else "not_found",
                    "proof_final_sign": "positive" if proof_positive else "not_found",
                    "adjoint_convention": "negative" if adjoint_negative else "not_found",
                    "source": "bounded_source_packets",
                }
            ],
            "clearance": {
                "adapter_required_cleared": status == "inconsistency_candidate",
                "cleared_by": "source_anchored_local_schema_check" if status == "inconsistency_candidate" else None,
                "not_cleared_by": ["executable_probe", "pytest", "benchmark_gate", "adapter_confidence"],
            },
            "forbidden_claims": obligation.get("forbidden_claims", []),
            "non_claims": _adapter_policy_boundary()
            + [
                "This result does not claim the whole DSGE note is false.",
                "This result does not claim practical HMC conclusions are invalid.",
            ],
        },
        ADAPTER_RESULT_CONTRACT,
    )


def _lower_case_packet_text(root: str | Path | None, manifest_path: str | Path | None, case_id: str) -> str:
    return _packet_text_for_case(root, manifest_path, case_id).lower()


def evaluate_kalman_likelihood_adapter(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
    *,
    case_id: str = "RLHL-04-kalman-prediction-error-loglik",
) -> dict[str, Any]:
    """Evaluate the local Kalman prediction-error likelihood source obligation."""
    ir_report = build_source_obligation_ir(root=root, manifest_path=manifest_path)
    if ir_report.get("status") != "consistent":
        return attach_contract(
            {
                "case_id": case_id,
                "adapter_route": "kalman_prediction_error_loglik",
                "status": "inconclusive",
                "reason": "Obligation IR did not validate.",
                "source_anchors": [],
                "checks": {"ir_consistent": False},
                "evidence": [],
                "non_claims": _adapter_policy_boundary(),
            },
            ADAPTER_RESULT_CONTRACT,
        )
    obligation = _obligation_by_case(ir_report, case_id)
    text = _lower_case_packet_text(root, manifest_path, case_id)
    checks = {
        "ir_consistent": True,
        "route_match": obligation.get("adapter_route") == "kalman_prediction_error_loglik",
        "source_anchors_present": bool(obligation.get("source_channel", {}).get("source_anchors")),
        "linear_gaussian_present": "linear gaussian" in text,
        "chain_rule_present": "chain rule" in text,
        "gaussian_predictive_present": "gaussian" in text and "predictive distribution" in text,
        "logdet_term_present": "log\\det" in text,
        "quadratic_term_present": "s_t^{-1}" in text and "v_t" in text,
        "positive_definite_or_spd_present": "s_t\\succ 0" in text or "positive definite" in text,
        "mask_or_observed_components_present": "observed components" in text or "masked panel" in text,
        "no_observation_skip_present": "no components are observed" in text and "skipped" in text,
        "probe_not_used_for_clearance": obligation.get("probe_channel", {}).get("may_clear_adapter_required") is False,
    }
    support = all(checks.values())
    status = "source_supported" if support else "human_review_required"
    reason = (
        "The bounded source packets support the prediction-error log-likelihood under linear Gaussian innovations, positive-definite innovation covariance, and observed-component masking boundaries."
        if support
        else "The bounded source packets did not contain all required likelihood derivation and domain-assumption evidence."
    )
    return attach_contract(
        {
            "case_id": case_id,
            "adapter_route": "kalman_prediction_error_loglik",
            "status": status,
            "reason": reason,
            "source_anchors": obligation["source_channel"]["source_anchors"],
            "required_terms": obligation["source_channel"]["required_terms"],
            "present_terms": obligation["source_channel"]["present_terms"],
            "checks": checks,
            "assumptions": [
                "linear Gaussian state-space model",
                "positive-definite selected innovation covariance",
                "observed-component selection for masked panels",
                "skip likelihood contribution when no components are observed",
            ],
            "evidence": [
                {
                    "kind": "kalman_likelihood_source_coverage",
                    "severity": "diagnostic",
                    "source": "bounded_source_packets",
                    "covered": sorted(key for key, value in checks.items() if value),
                    "missing": sorted(key for key, value in checks.items() if not value),
                }
            ],
            "clearance": {
                "adapter_required_cleared": status == "source_supported",
                "cleared_by": "source_anchored_local_schema_check" if status == "source_supported" else None,
                "not_cleared_by": ["executable_probe", "pytest", "benchmark_gate", "adapter_confidence"],
            },
            "forbidden_claims": obligation.get("forbidden_claims", []),
            "non_claims": _adapter_policy_boundary()
            + [
                "This result does not claim nonlinear filters are exact.",
                "This result does not validate score, Hessian, sampler, or production implementation correctness.",
            ],
        },
        ADAPTER_RESULT_CONTRACT,
    )


def evaluate_joseph_equivalence_adapter(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
    *,
    case_id: str = "RLHL-06-joseph-covariance-equivalence",
) -> dict[str, Any]:
    """Evaluate the local Joseph/compact covariance equivalence obligation."""
    ir_report = build_source_obligation_ir(root=root, manifest_path=manifest_path)
    if ir_report.get("status") != "consistent":
        return attach_contract(
            {
                "case_id": case_id,
                "adapter_route": "joseph_covariance_equivalence",
                "status": "inconclusive",
                "reason": "Obligation IR did not validate.",
                "source_anchors": [],
                "checks": {"ir_consistent": False},
                "evidence": [],
                "non_claims": _adapter_policy_boundary(),
            },
            ADAPTER_RESULT_CONTRACT,
        )
    obligation = _obligation_by_case(ir_report, case_id)
    text = _lower_case_packet_text(root, manifest_path, case_id)
    checks = {
        "ir_consistent": True,
        "route_match": obligation.get("adapter_route") == "joseph_covariance_equivalence",
        "source_anchors_present": bool(obligation.get("source_channel", {}).get("source_anchors")),
        "joseph_form_present": "joseph form" in text and "k_t r k_t" in text.replace("^\\top", ""),
        "compact_form_present": "compact" in text and "(i-k_th)" in text.replace(" ", ""),
        "kalman_gain_present": "k_t &= p_{t|t-1}h^\\top s_t^{-1}" in text or "kalman gain" in text,
        "spd_condition_present": "s_t\\succ 0" in text,
        "equivalence_claim_present": "algebraically equivalent" in text or "same exact linear gaussian likelihood" in text,
        "numerical_caveat_present": "rounding" in text or "numerical stability" in text,
        "probe_not_used_for_clearance": obligation.get("probe_channel", {}).get("may_clear_adapter_required") is False,
    }
    support = all(checks.values())
    status = "source_supported" if support else "human_review_required"
    reason = (
        "The bounded source packets support exact-arithmetic Joseph/compact covariance equivalence with the Kalman gain relation and numerical caveat preserved."
        if support
        else "The bounded source packets did not contain all required Joseph equivalence evidence."
    )
    return attach_contract(
        {
            "case_id": case_id,
            "adapter_route": "joseph_covariance_equivalence",
            "status": status,
            "reason": reason,
            "source_anchors": obligation["source_channel"]["source_anchors"],
            "required_terms": obligation["source_channel"]["required_terms"],
            "present_terms": obligation["source_channel"]["present_terms"],
            "checks": checks,
            "assumptions": [
                "standard Kalman gain relation",
                "positive-definite innovation covariance",
                "exact-arithmetic algebraic equivalence",
                "numerical-stability caveat for floating-point updates",
            ],
            "evidence": [
                {
                    "kind": "joseph_equivalence_source_coverage",
                    "severity": "diagnostic",
                    "source": "bounded_source_packets",
                    "covered": sorted(key for key, value in checks.items() if value),
                    "missing": sorted(key for key, value in checks.items() if not value),
                }
            ],
            "clearance": {
                "adapter_required_cleared": status == "source_supported",
                "cleared_by": "source_anchored_local_schema_check" if status == "source_supported" else None,
                "not_cleared_by": ["executable_probe", "pytest", "benchmark_gate", "adapter_confidence"],
            },
            "forbidden_claims": obligation.get("forbidden_claims", []),
            "non_claims": _adapter_policy_boundary()
            + [
                "This result does not claim the compact form preserves positive semidefiniteness under rounding.",
                "This result does not validate a particular backend implementation.",
            ],
        },
        ADAPTER_RESULT_CONTRACT,
    )


def evaluate_affine_recursion_adapter(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
    *,
    case_id: str = "RLHL-07-affine-pricing-master-recursion",
) -> dict[str, Any]:
    """Evaluate the local affine-pricing master-recursion obligation."""
    ir_report = build_source_obligation_ir(root=root, manifest_path=manifest_path)
    if ir_report.get("status") != "consistent":
        return attach_contract(
            {
                "case_id": case_id,
                "adapter_route": "affine_pricing_master_recursion",
                "status": "inconclusive",
                "reason": "Obligation IR did not validate.",
                "source_anchors": [],
                "checks": {"ir_consistent": False},
                "evidence": [],
                "non_claims": _adapter_policy_boundary(),
            },
            ADAPTER_RESULT_CONTRACT,
        )
    obligation = _obligation_by_case(ir_report, case_id)
    text = _lower_case_packet_text(root, manifest_path, case_id)
    compact = text.replace(" ", "")
    checks = {
        "ir_consistent": True,
        "route_match": obligation.get("adapter_route") == "affine_pricing_master_recursion",
        "source_anchors_present": bool(obligation.get("source_channel", {}).get("source_anchors")),
        "state_transition_present": "\\mathbf{x}_{t+1}" in text and "\\boldsymbol{\\varepsilon}" in text,
        "exponential_affine_ansatz_present": "exponential affine conjecture" in text or "exp\\!\\bigl(\\mathcal{a}_n" in text,
        "pricing_expectation_present": "\\mathbb{e}_t" in text and "v_{t+1}(n-1)" in text,
        "conditional_normality_present": "conditional normality" in text or "\\sim n(" in text,
        "gaussian_mgf_present": "exp\\!\\bigl(\\mathbf{c}'" in text and "\\tfrac{1}{2}" in text and "q}_\\delta" in text,
        "b_recursion_present": "\\mathcal{b}_n&=" in compact or "\\mathcal{b}_n&=" in text,
        "a_recursion_present": "\\mathcal{a}_n&=" in compact or "\\mathcal{a}_n&=" in text,
        "initial_conditions_present": "\\mathcal{a}_0 = 0" in text and "\\mathcal{b}_0 = \\mathbf{0}" in text,
        "coefficient_collection_present": "collecting the" in text and "dependent and constant terms" in text,
        "probe_not_used_for_clearance": obligation.get("probe_channel", {}).get("may_clear_adapter_required") is False,
    }
    support = all(checks.values())
    status = "source_supported" if support else "human_review_required"
    reason = (
        "The bounded source packet supports the affine recursion through ansatz substitution, Gaussian MGF, and coefficient collection for A_n and B_n."
        if support
        else "The bounded source packet did not contain all required affine recursion evidence."
    )
    return attach_contract(
        {
            "case_id": case_id,
            "adapter_route": "affine_pricing_master_recursion",
            "status": status,
            "reason": reason,
            "source_anchors": obligation["source_channel"]["source_anchors"],
            "required_terms": obligation["source_channel"]["required_terms"],
            "present_terms": obligation["source_channel"]["present_terms"],
            "checks": checks,
            "assumptions": [
                "risk-neutral linear Gaussian transition",
                "exponential-affine continuation-value ansatz",
                "Gaussian moment-generating function",
                "coefficient collection into constant and state-dependent terms",
            ],
            "evidence": [
                {
                    "kind": "affine_recursion_source_coverage",
                    "severity": "diagnostic",
                    "source": "bounded_source_packets",
                    "covered": sorted(key for key, value in checks.items() if value),
                    "missing": sorted(key for key, value in checks.items() if not value),
                }
            ],
            "clearance": {
                "adapter_required_cleared": status == "source_supported",
                "cleared_by": "source_anchored_local_schema_check" if status == "source_supported" else None,
                "not_cleared_by": ["executable_probe", "pytest", "benchmark_gate", "adapter_confidence"],
            },
            "forbidden_claims": obligation.get("forbidden_claims", []),
            "non_claims": _adapter_policy_boundary()
            + [
                "This result does not claim empirical pricing validity or identification.",
                "This result does not claim later non-affine approximations are exact.",
            ],
        },
        ADAPTER_RESULT_CONTRACT,
    )


def evaluate_kalman_score_adapter(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
    *,
    case_id: str = "RLHL-10-kalman-score-same-scalar-contract",
) -> dict[str, Any]:
    """Evaluate the local Kalman solve-form score and same-scalar obligation."""
    ir_report = build_source_obligation_ir(root=root, manifest_path=manifest_path)
    if ir_report.get("status") != "consistent":
        return attach_contract(
            {
                "case_id": case_id,
                "adapter_route": "kalman_score_same_scalar",
                "status": "inconclusive",
                "reason": "Obligation IR did not validate.",
                "source_anchors": [],
                "checks": {"ir_consistent": False},
                "evidence": [],
                "non_claims": _adapter_policy_boundary(),
            },
            ADAPTER_RESULT_CONTRACT,
        )
    obligation = _obligation_by_case(ir_report, case_id)
    text = _lower_case_packet_text(root, manifest_path, case_id)
    checks = {
        "ir_consistent": True,
        "route_match": obligation.get("adapter_route") == "kalman_score_same_scalar",
        "source_anchors_present": bool(obligation.get("source_channel", {}).get("source_anchors")),
        "innovation_derivatives_present": "\\dot v_t" in text and "\\dot s_t" in text,
        "inverse_derivative_rule_present": "\\partial_i s^{-1}" in text,
        "score_contribution_present": "per-time score" in text and "\\frac{\\partial \\ell_t}" in text,
        "solve_relation_present": "s_tw_t=v_t" in text.replace(" ", ""),
        "solve_score_present": "\\label{eq:bf-solve-score}" in text and "w_t^\\top" in text,
        "source_label_present": "eq:solve\\_score\\_proved" in text,
        "trace_or_factor_caveat_present": "trace" in text and ("factor solves" in text or "trace estimators" in text),
        "value_oracle_present": "value oracle" in text,
        "same_scalar_boundary_present": "same scalar likelihood" in text and "valid for hmc only" in text,
        "prior_transform_boundary_present": "prior and parameter" in text and "transform terms" in text,
        "probe_not_used_for_clearance": obligation.get("probe_channel", {}).get("may_clear_adapter_required") is False,
    }
    support = all(checks.values())
    status = "source_supported" if support else "human_review_required"
    reason = (
        "The bounded source packets support the solve-form Kalman score contribution and same-scalar HMC-gradient boundary."
        if support
        else "The bounded source packets did not contain all required score and same-scalar boundary evidence."
    )
    return attach_contract(
        {
            "case_id": case_id,
            "adapter_route": "kalman_score_same_scalar",
            "status": status,
            "reason": reason,
            "source_anchors": obligation["source_channel"]["source_anchors"],
            "required_terms": obligation["source_channel"]["required_terms"],
            "present_terms": obligation["source_channel"]["present_terms"],
            "checks": checks,
            "assumptions": [
                "invertible innovation covariance",
                "differentiability of innovation and innovation covariance",
                "solve relation S_t w_t = v_t",
                "analytic gradient corresponds to the same scalar likelihood plus prior and transform terms",
            ],
            "evidence": [
                {
                    "kind": "kalman_score_source_coverage",
                    "severity": "diagnostic",
                    "source": "bounded_source_packets",
                    "covered": sorted(key for key, value in checks.items() if value),
                    "missing": sorted(key for key, value in checks.items() if not value),
                }
            ],
            "clearance": {
                "adapter_required_cleared": status == "source_supported",
                "cleared_by": "source_anchored_local_schema_check" if status == "source_supported" else None,
                "not_cleared_by": ["executable_probe", "pytest", "benchmark_gate", "adapter_confidence"],
            },
            "forbidden_claims": obligation.get("forbidden_claims", []),
            "non_claims": _adapter_policy_boundary()
            + [
                "This result does not claim HMC validity, posterior correctness, or sampler convergence.",
                "This result does not claim Hessian readiness or backend correctness.",
            ],
        },
        ADAPTER_RESULT_CONTRACT,
    )


ADAPTER_DISPATCH = {
    "RLHL-01-ift-gradient-bias-sign": evaluate_ift_sign_adapter,
    "RLHL-04-kalman-prediction-error-loglik": evaluate_kalman_likelihood_adapter,
    "RLHL-06-joseph-covariance-equivalence": evaluate_joseph_equivalence_adapter,
    "RLHL-07-affine-pricing-master-recursion": evaluate_affine_recursion_adapter,
    "RLHL-10-kalman-score-same-scalar-contract": evaluate_kalman_score_adapter,
}


def run_source_adapter_report(
    root: str | Path | None = None,
    manifest_path: str | Path | None = None,
) -> dict[str, Any]:
    """Run all local source adapters and preserve separate evidence ledgers."""
    ir_report = build_source_obligation_ir(root=root, manifest_path=manifest_path)
    if ir_report.get("status") != "consistent":
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "Obligation IR did not validate; source adapters were not run.",
                "source_obligation_ledger": [],
                "adapter_result_ledger": [],
                "residual_gap_ledger": [],
                "probe_reference": {"included": False, "may_clear_adapter_required": False},
                "summary": {
                    "case_total": 0,
                    "source_supported": 0,
                    "inconsistency_candidate": 0,
                    "human_review_required": 0,
                    "adapter_required_residual": 0,
                    "aggregate_accuracy": None,
                },
                "policy_boundary": _adapter_policy_boundary(),
            },
            "real_local_source_adapter_report",
        )

    source_ledger: list[dict[str, Any]] = []
    adapter_ledger: list[dict[str, Any]] = []
    residual_ledger: list[dict[str, Any]] = []
    for obligation in ir_report["obligations"]:
        case_id = obligation["case_id"]
        source_ledger.append(
            {
                "case_id": case_id,
                "adapter_route": obligation["adapter_route"],
                "source_anchors": obligation["source_channel"]["source_anchors"],
                "pre_adapter_status": obligation["pre_adapter_status"],
            }
        )
        adapter = ADAPTER_DISPATCH[case_id](root=root, manifest_path=manifest_path)
        adapter_ledger.append(adapter)
        if not adapter.get("clearance", {}).get("adapter_required_cleared"):
            residual_ledger.append(
                {
                    "case_id": case_id,
                    "adapter_route": obligation["adapter_route"],
                    "status": "adapter_required",
                    "reason": adapter.get("reason"),
                    "missing_checks": sorted(
                        key for key, value in adapter.get("checks", {}).items() if value is False
                    ),
                    "next_action": "review_source_packet_scope_or_extend_manifest_under_governance",
                }
            )

    source_supported = sum(1 for item in adapter_ledger if item.get("status") == "source_supported")
    inconsistency_candidate = sum(1 for item in adapter_ledger if item.get("status") == "inconsistency_candidate")
    human_review_required = sum(1 for item in adapter_ledger if item.get("status") == "human_review_required")
    status = "passed" if not residual_ledger else "partial"
    return attach_contract(
        {
            "status": status,
            "reason": (
                "All source obligations have source-anchored local-schema adapter clearance."
                if status == "passed"
                else "At least one source obligation remains adapter-required under the frozen source-packet schema."
            ),
            "source_obligation_ledger": source_ledger,
            "adapter_result_ledger": adapter_ledger,
            "residual_gap_ledger": residual_ledger,
            "probe_reference": {
                "included": False,
                "may_clear_adapter_required": False,
                "reason": "Executable probes remain in the separate real-local high-level pilot report.",
            },
            "summary": {
                "case_total": len(adapter_ledger),
                "source_supported": source_supported,
                "inconsistency_candidate": inconsistency_candidate,
                "human_review_required": human_review_required,
                "adapter_required_residual": len(residual_ledger),
                "aggregate_accuracy": None,
            },
            "policy_boundary": _adapter_policy_boundary()
            + [
                "Source-adapter, executable-probe, and residual-gap ledgers are intentionally separate.",
                "No single aggregate source/probe accuracy metric is emitted.",
                "A partial report is not a failed source derivation and not release evidence.",
            ],
        },
        "real_local_source_adapter_report",
    )
