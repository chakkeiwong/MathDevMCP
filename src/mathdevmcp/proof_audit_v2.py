"""Release-facing proof-audit workflow with explicit certification boundaries.

The v2 audit combines parser policy, typed diagnostics, shape diagnostics,
numeric suggestions, backend attempts, and abstention logic. Its most important
job is preventing diagnostic evidence from being reported as a certificate.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from collections.abc import Iterable
from copy import deepcopy
from pathlib import Path

from .contracts import attach_contract, contract_metadata
from .math_ir import diagnose_typed_obligation
from .matrix_ir import parse_matrix_obligation
from .numeric_diagnostics import suggest_numeric_diagnostics
from .numeric_runner import run_numeric_diagnostic_plan
from .parser_policy import decide_parser_policy
from .proof_audit import audit_derivation_for_label
from .routing import route_typed_diagnostic
from .shape_diagnostics import diagnose_shape_constraints
from .status_taxonomy import classify_status


_CERTIFYING_PARSER_STATUSES = {"selected", "selected_for_proof_audit"}


@dataclass(frozen=True)
class ProofAuditV2Obligation:
    id: str
    label: str
    source_text: str
    lhs: str
    rhs: str
    kind: str
    parser_backend: str | None
    source_binding_status: str
    specialist_parser_readiness: str
    parser_policy: dict
    typed_diagnostic: dict
    matrix_ir: dict
    route_decision: dict
    shape_diagnostic: dict
    numeric_diagnostics: dict
    backend_attempts: list[dict]
    status: str
    substatus: str
    severity: str
    reason: str
    evidence_kind: str
    diagnostic_only: bool
    certificate: dict | None
    verification_boundary: str
    actions: list[dict]
    provenance: dict
    metadata: dict[str, str]


@dataclass(frozen=True)
class ProofAuditV2Report:
    label: str
    doc_root: str
    status: str
    reason: str
    counts: dict[str, int]
    substatus_counts: dict[str, int]
    high_priority_actions: list[dict]
    obligations: list[dict]
    parser_policy: dict
    source_binding_status: str
    specialist_parser_readiness: str
    base_audit_status: str
    doc_context: dict
    target_extraction: dict


def _context_text(doc_context: dict) -> str:
    paragraphs = doc_context.get("paragraphs")
    if isinstance(paragraphs, list) and paragraphs:
        return "\n".join(str(item.get("text", "")) for item in paragraphs)
    excerpt = doc_context.get("excerpt", [])
    if isinstance(excerpt, list):
        return "\n".join(str(item.get("text", "")) for item in excerpt)
    return ""


def _backend_attempts(base_obligation: dict) -> list[dict]:
    attempts: list[dict] = []
    for evidence in base_obligation.get("evidence", []):
        attempts.append(
            {
                "source": "proof_audit",
                "status": base_obligation.get("status"),
                "classification": base_obligation.get("classification"),
                "evidence": evidence,
            }
        )
    return attempts


def _evidence_boundary(status: str, attempts: list[dict], reason: str) -> tuple[str, bool, dict | None, str]:
    has_certifying = any(attempt.get("evidence", {}).get("severity") == "certifying" for attempt in attempts)
    has_blocking = any(attempt.get("evidence", {}).get("severity") == "blocking" for attempt in attempts)
    if status == "verified" and has_certifying:
        certificate = next((attempt.get("evidence") for attempt in attempts if attempt.get("evidence", {}).get("severity") == "certifying"), None)
        return "deterministic_backend", False, certificate, "Deterministic backend evidence certified the scoped obligation."
    if status == "mismatch" and has_blocking:
        return "deterministic_backend", False, None, "Deterministic backend evidence refuted the scoped obligation."
    return "diagnostic_bundle", True, None, f"{reason} A deterministic backend certificate is required before this can become verified."


def _actions(
    *,
    base_obligation: dict,
    parser_policy: dict,
    route: dict,
    shape: dict,
    numeric: dict,
    status: str,
) -> list[dict]:
    actions: list[dict] = []
    if parser_policy.get("status") not in _CERTIFYING_PARSER_STATUSES:
        actions.append(
            {
                "kind": "fix_parser_provenance_before_certification",
                "severity": "high",
                "reason": parser_policy.get("reason", "Parser policy did not select a proof-audit backend."),
            }
        )
    if base_obligation.get("classification") == "not_extracted":
        actions.append(
            {
                "kind": "split_or_rewrite_ambiguous_derivation_row",
                "severity": "high",
                "reason": "The derivation row was not split into a safe proof obligation.",
            }
        )
    for constraint in shape.get("missing_constraints", []):
        actions.append(
            {
                "kind": "state_or_verify_missing_constraint",
                "target": constraint.get("kind"),
                "severity": "high",
                "reason": constraint.get("reason", "A required shape or dimension constraint is missing."),
            }
        )
    if route.get("route") == "human_review":
        actions.append(
            {
                "kind": "human_formalization_or_review",
                "severity": "high" if status in {"unverified", "inconclusive"} else "medium",
                "reason": route.get("reason", "The obligation requires human review."),
            }
        )
    for suggestion in numeric.get("suggestions", []):
        actions.append(
            {
                "kind": suggestion.get("kind"),
                "target": suggestion.get("target"),
                "severity": suggestion.get("priority", "medium"),
                "reason": suggestion.get("reason", "Run a bounded numeric diagnostic when a safe encoding exists."),
            }
        )
    if status == "mismatch":
        actions.append(
            {
                "kind": "investigate_backend_refutation",
                "severity": "high",
                "reason": "A deterministic backend refuted the extracted obligation.",
            }
        )
    return actions


def _obligation_status_and_reason(
    *,
    base_obligation: dict,
    parser_policy: dict,
    route: dict,
    shape: dict,
) -> tuple[str, str]:
    base_status = base_obligation.get("status", "inconclusive")
    if parser_policy.get("status") not in _CERTIFYING_PARSER_STATUSES:
        return "inconclusive", "Parser policy did not select a provenance-preserving backend for certification."
    if base_status == "mismatch":
        return "mismatch", base_obligation.get("reason", "A backend refuted the obligation.")
    if base_obligation.get("classification") == "not_extracted":
        return "inconclusive", "The row could not be extracted as a safe proof obligation."
    if shape.get("missing_constraints"):
        return "unverified", "The obligation has missing shape, dimension, or regularity constraints."
    if base_obligation.get("classification") == "human_review":
        return "unverified", base_obligation.get(
            "reason",
            "The exact source relation requires manual formalization before backend certification.",
        )
    if route.get("route") == "human_review":
        return "unverified", "The obligation uses notation that requires human review or manual formalization."
    if base_status == "verified":
        return "verified", "The extracted obligation was verified by a deterministic bounded backend."
    if base_status == "unverified":
        return "unverified", base_obligation.get("reason", "The obligation remains unsupported.")
    return "inconclusive", base_obligation.get("reason", "No deterministic backend evidence certified or refuted the obligation.")


def _counts(obligations: list[dict]) -> dict[str, int]:
    counts = {"total": len(obligations), "verified": 0, "mismatch": 0, "unverified": 0, "inconclusive": 0}
    for obligation in obligations:
        status = obligation.get("status", "inconclusive")
        if status in counts:
            counts[status] += 1
        else:
            counts["inconclusive"] += 1
    return counts


def _substatus_counts(obligations: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for obligation in obligations:
        substatus = str(obligation.get("substatus", "unknown"))
        counts[substatus] = counts.get(substatus, 0) + 1
    return counts


def _aggregate(counts: dict[str, int]) -> tuple[str, str]:
    if counts["mismatch"]:
        return "mismatch", "At least one proof-audit v2 obligation was refuted by backend evidence."
    if counts["verified"] and counts["verified"] == counts["total"]:
        return "verified", "Every proof-audit v2 obligation was verified by deterministic backend evidence."
    if counts["verified"] or counts["unverified"]:
        return "unverified", "At least one obligation remains unverified or diagnostic-only."
    return "inconclusive", "No proof-audit v2 obligation could be certified or refuted."


def _compact_obligation(obligation: dict) -> dict:
    return {
        "id": obligation["id"],
        "label": obligation["label"],
        "source_text": obligation["source_text"],
        "lhs": obligation["lhs"],
        "rhs": obligation["rhs"],
        "kind": obligation["kind"],
        "source_binding_status": obligation["source_binding_status"],
        "specialist_parser_readiness": obligation["specialist_parser_readiness"],
        "status": obligation["status"],
        "substatus": obligation["substatus"],
        "severity": obligation["severity"],
        "reason": obligation["reason"],
        "evidence_kind": obligation["evidence_kind"],
        "diagnostic_only": obligation["diagnostic_only"],
        "verification_boundary": obligation["verification_boundary"],
        "route": obligation["route_decision"].get("route"),
        "matrix_ir_status": obligation["matrix_ir"].get("status"),
        "missing_constraints": obligation["shape_diagnostic"].get("missing_constraints", []),
        "actions": obligation["actions"],
        "provenance": obligation["provenance"],
        "metadata": obligation["metadata"],
    }


def _durable_parser_policy(parser: dict) -> dict:
    """Exclude wall-clock proxies from durable proof-evidence identity."""
    durable = deepcopy(parser)
    benchmark = durable.get("benchmark_report")
    if isinstance(benchmark, dict):
        for result in benchmark.get("results", []):
            if isinstance(result, dict):
                result.pop("runtime_seconds", None)
        benchmark["durable_identity_exclusions"] = [
            "results[*].runtime_seconds is an explanatory runtime proxy and is not used for parser selection"
        ]
    return durable


def audit_derivation_v2_for_label(
    root: str,
    label: str,
    *,
    before: int = 0,
    after: int = 0,
    paragraph_context: bool = False,
    backend: str = "sympy",
    cache_path: str | Path | None = None,
    parser_backends: list[str] | None = None,
    parser_expected_labels: Iterable[str] | None = None,
    numeric_artifacts: dict[str, dict] | None = None,
    assumption_manifest: dict | None = None,
    summary_only: bool = False,
    file: str | None = None,
    source_digest: str | None = None,
) -> dict:
    base = audit_derivation_for_label(
        root,
        label,
        before=before,
        after=after,
        paragraph_context=paragraph_context,
        backend=backend,
        cache_path=cache_path,
        file=file,
        source_digest=source_digest,
    )
    expected_labels = (
        list(parser_expected_labels)
        if parser_expected_labels is not None
        else [label]
        if file is not None or source_digest is not None
        else None
    )
    parser = decide_parser_policy(root, backends=parser_backends or ["current"], expected_labels=expected_labels)
    target_extraction = base.get("target_extraction", {})
    targets = target_extraction.get("targets", []) if isinstance(target_extraction, dict) else []
    exact_target = targets[0] if len(targets) == 1 and isinstance(targets[0], dict) else None
    observed_digest = (
        exact_target.get("label_scoped_obligation", {}).get("document", {}).get("source_digest")
        if exact_target is not None
        else None
    )
    if exact_target is not None and (source_digest is None or observed_digest == source_digest):
        source_binding_status = "accepted_exact_source"
    elif target_extraction.get("status") == "ambiguous":
        source_binding_status = "ambiguous_label"
    elif source_digest is not None and observed_digest != source_digest:
        source_binding_status = "source_digest_mismatch"
    else:
        source_binding_status = "source_label_missing"
    specialist_parser_readiness = str(parser.get("status", "blocked"))
    selected_backend = parser.get("selected_backend") or "current"
    context = _context_text(base.get("doc_context", {}))
    obligations: list[dict] = []
    for base_obligation in base.get("obligations", []):
        typed = diagnose_typed_obligation(
            base_obligation,
            parser_backend=selected_backend,
            context_text=context,
            assumption_manifest=assumption_manifest,
        )
        matrix_ir = parse_matrix_obligation(
            str(base_obligation.get("source_text") or f"{base_obligation.get('lhs', '')} = {base_obligation.get('rhs', '')}"),
            provenance=base_obligation.get("provenance", {}),
        )
        route = route_typed_diagnostic(typed, label=label)
        shape = diagnose_shape_constraints(typed)
        numeric = suggest_numeric_diagnostics(typed)
        if numeric_artifacts:
            executed = []
            for suggestion in numeric.get("suggestions", []):
                artifact = numeric_artifacts.get(suggestion.get("kind"))
                if artifact is not None:
                    executed.append(run_numeric_diagnostic_plan({"kind": suggestion.get("kind"), "artifact": artifact}))
            if executed:
                numeric = {**numeric, "executed": executed}
        status, reason = _obligation_status_and_reason(
            base_obligation=base_obligation,
            parser_policy=parser,
            route=route,
            shape=shape,
        )
        actions = _actions(
            base_obligation=base_obligation,
            parser_policy=parser,
            route=route,
            shape=shape,
            numeric=numeric,
            status=status,
        )
        classification = classify_status(
            status,
            reason,
            parser_policy=parser,
            base_obligation=base_obligation,
            route=route,
            shape=shape,
            actions=actions,
            source_binding_status=source_binding_status,
        )
        actions = classification["actions"]
        backend_attempts = _backend_attempts(base_obligation)
        evidence_kind, diagnostic_only, certificate, verification_boundary = _evidence_boundary(status, backend_attempts, reason)
        obligation = ProofAuditV2Obligation(
            id=str(base_obligation.get("id", "")),
            label=label,
            source_text=str(base_obligation.get("source_text", "")),
            lhs=str(base_obligation.get("lhs", "")),
            rhs=str(base_obligation.get("rhs", "")),
            kind=typed.get("obligation", {}).get("kind", "unknown"),
            parser_backend=parser.get("selected_backend"),
            source_binding_status=source_binding_status,
            specialist_parser_readiness=specialist_parser_readiness,
            parser_policy=parser,
            typed_diagnostic=typed,
            matrix_ir=matrix_ir,
            route_decision=route,
            shape_diagnostic=shape,
            numeric_diagnostics=numeric,
            backend_attempts=backend_attempts,
            status=status,
            substatus=classification["substatus"],
            severity=classification["severity"],
            reason=reason,
            evidence_kind=evidence_kind,
            diagnostic_only=diagnostic_only,
            certificate=certificate,
            verification_boundary=verification_boundary,
            actions=actions,
            provenance=base_obligation.get("provenance", {}),
            metadata=contract_metadata("proof_audit_v2_obligation"),
        )
        obligations.append(asdict(obligation))
    counts = _counts(obligations)
    substatus_counts = _substatus_counts(obligations)
    status, reason = _aggregate(counts)
    high_priority_actions = [
        {**action, "obligation_id": obligation["id"]}
        for obligation in obligations
        for action in obligation["actions"]
        if action.get("severity") == "high"
    ]
    report_obligations = [_compact_obligation(item) for item in obligations] if summary_only else obligations
    report = ProofAuditV2Report(
        label=label,
        doc_root=str(Path(root).resolve()),
        status=status,
        reason=reason,
        counts=counts,
        substatus_counts=substatus_counts,
        high_priority_actions=high_priority_actions,
        obligations=report_obligations,
        parser_policy=_durable_parser_policy(parser),
        source_binding_status=source_binding_status,
        specialist_parser_readiness=specialist_parser_readiness,
        base_audit_status=base.get("status", "inconclusive"),
        doc_context=base.get("doc_context", {}),
        target_extraction=base.get("target_extraction", {}),
    )
    return attach_contract(asdict(report), "proof_audit_v2_result", doc_context=base.get("doc_context", {}))
