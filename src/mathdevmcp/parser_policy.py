"""Parser backend selection policy for proof-audit routing.

Parser success is not mathematical verification. This module decides which
parser has enough label preservation and provenance to feed downstream audit
tools without losing source traceability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from collections.abc import Iterable

from .contracts import attach_contract
from .parser_benchmark import P02_FIDELITY_FIELDS, compare_p02_fidelity_vectors, compare_parser_backends


@dataclass(frozen=True)
class ParserPolicyDecision:
    status: str
    reason: str
    selected_backend: str | None
    blocking_findings: list[dict]
    caveats: list[dict]
    backend_roles: list[dict]
    benchmark_report: dict


def decide_parser_policy(root: str, *, backends: list[str] | None = None, expected_labels: Iterable[str] | None = None) -> dict:
    """Choose the parser role for a corpus and report any blocking findings."""
    report = compare_parser_backends(root, backends=backends or ["current", "latexml", "pandoc"], expected_labels=expected_labels)
    blocking: list[dict] = []
    caveats: list[dict] = []
    backend_roles: list[dict] = []
    current = next((item for item in report["results"] if item["backend"] == "current"), None)
    if current and current["quality_checks"]["label_preservation"] and current["quality_checks"]["provenance_available"]:
        selected = "current"
        status = "selected_for_proof_audit"
        reason = "Current parser preserves expected labels and line provenance for this corpus."
    elif current and current["quality_checks"]["provenance_available"]:
        selected = "current"
        status = "selected_for_context_only"
        reason = "Current parser has provenance, but expected label preservation is incomplete; certification should remain blocked."
    else:
        selected = None
        status = "blocked"
        reason = "No parser backend preserved required labels and provenance for proof-audit routing."
    if current is None:
        blocking.append({"backend": "current", "kind": "selected_parser_not_measured"})
    for result in report["results"]:
        backend = result["backend"]
        if backend == selected and status == "selected_for_proof_audit":
            role = "selected_for_proof_audit"
        elif backend == selected and status == "selected_for_context_only":
            role = "selected_for_context_only"
        elif backend == "current":
            role = "blocked"
        else:
            role = "measured_optional"
        backend_roles.append({"backend": backend, "role": role, "status": result["status"]})
        finding_target = blocking if backend == "current" else caveats
        severity = "high" if backend == "current" else "medium"
        if not result["quality_checks"]["label_preservation"]:
            finding_target.append(
                {
                    "backend": backend,
                    "kind": "missing_expected_labels",
                    "missing": result["details"].get("missing_expected_labels", []),
                    "severity": severity,
                }
            )
        if not result["quality_checks"]["provenance_available"]:
            finding_target.append({"backend": backend, "kind": "provenance_unavailable", "severity": severity})
    decision = ParserPolicyDecision(status, reason, selected, blocking, caveats, backend_roles, report)
    payload = attach_contract(asdict(decision), "parser_policy_decision")
    payload["legacy_status"] = "selected" if status == "selected_for_proof_audit" else status
    return payload


def select_p02_parser_backend(
    current: dict,
    specialists: Iterable[dict],
    *,
    frozen_identity: bool,
) -> dict:
    """Select by reviewed capability evidence; never by parser-success proxies."""
    current_vector = current.get("fidelity_vector")
    if not isinstance(current_vector, list):
        raise ValueError("current parser measurement lacks a fidelity vector")
    candidates: list[dict] = []
    vetoes: list[dict] = []
    for raw in specialists:
        item = dict(raw)
        status = item.get("capability_status")
        if status is None:
            # Keep the public compatibility path non-authoritative. Production
            # Formal P02 records use the closed capability fields below.
            vector = item.get("fidelity_vector")
            if not isinstance(vector, list):
                raise ValueError("specialist parser measurement lacks a fidelity vector")
            comparison = compare_p02_fidelity_vectors(current_vector, vector)
            source_mappable = item.get("source_mappable") is True
            eligible = comparison["relation"] == "candidate_materially_better" and source_mappable
            limitations = [] if source_mappable else ["no_independent_source_offsets"]
            contradictions = ["exact_requested_label_set"] if item.get("ownership_disagreement") is True else []
        else:
            if status not in {
                "valid_source_mappable",
                "valid_not_source_mappable",
                "malformed_output",
                "timed_out",
                "nonzero_exit",
                "version_mismatch",
                "invocation_mismatch",
                "source_mutated",
                "missing_artifact",
            }:
                raise ValueError("specialist parser measurement has an unknown capability status")
            limitations = item.get("limitation_codes")
            contradictions = item.get("contradictions")
            promotional = item.get("promotional_fields")
            diagnostic = item.get("diagnostic_observations")
            if not isinstance(limitations, list) or not isinstance(contradictions, list):
                raise ValueError("specialist capability record lacks limitation or contradiction lists")
            if not isinstance(promotional, list) or not isinstance(diagnostic, dict):
                raise ValueError("specialist capability record lacks reviewed observation fields")
            prefix = list(P02_FIDELITY_FIELDS[: len(promotional)])
            if promotional != prefix or any(field not in diagnostic for field in promotional):
                raise ValueError("specialist promotional fields are not a leading observed prefix")
            expected_contradictions = [field for field, matches in diagnostic.items() if matches is False]
            if contradictions != expected_contradictions:
                raise ValueError("specialist contradictions differ from reviewed observations")
            if status == "valid_source_mappable":
                if limitations or not promotional:
                    raise ValueError("source-mappable specialist has limitations or no promotion prefix")
            elif promotional or item.get("eligible_for_selection") is True:
                raise ValueError("limitation-only specialist is promotional or eligible")
            if status != "valid_source_mappable" and not limitations:
                raise ValueError("limitation-only specialist has no registered limitation")
            if status not in {"valid_source_mappable", "valid_not_source_mappable"} and diagnostic:
                raise ValueError("invalid specialist bytes cannot supply observations")
            vector = [
                1 if diagnostic.get(field) is True else 0
                for field in P02_FIDELITY_FIELDS
            ]
            comparison = compare_p02_fidelity_vectors(current_vector, vector)
            source_mappable = status == "valid_source_mappable"
            eligible = (
                item.get("eligible_for_selection") is True
                and source_mappable
                and not limitations
                and not contradictions
                and bool(promotional)
                and comparison["relation"] == "candidate_materially_better"
            )
        candidate = {
            "backend": str(item.get("backend", "unknown")),
            "parser_version": str(item.get("parser_version", "unknown")),
            "capability_status": status or ("valid_source_mappable" if source_mappable else "valid_not_source_mappable"),
            "fidelity_vector": vector,
            "comparison": comparison,
            "source_mappable": source_mappable,
            "limitation_codes": list(limitations),
            "contradictions": list(contradictions),
            "eligible_for_selection": eligible,
            "non_promotional_diagnostics": dict(item.get("non_promotional_diagnostics", {})),
        }
        candidates.append(candidate)
        if contradictions:
            vetoes.append(
                {
                    "backend": candidate["backend"],
                    "code": "independent_specialist_contradiction",
                    "fields": list(contradictions),
                }
            )
        elif candidate["capability_status"] in {
            "invocation_mismatch",
            "source_mutated",
            "missing_artifact",
            "version_mismatch",
        }:
            vetoes.append({"backend": candidate["backend"], "code": candidate["capability_status"]})

    selectable = [item for item in candidates if item["eligible_for_selection"]]
    selectable.sort(
        key=lambda item: (
            tuple(-value for value in item["fidelity_vector"]),
            item["backend"].encode("utf-8"),
        )
    )
    if frozen_identity and selectable:
        status = "oracle_amendment_required"
        selected_backend = "current"
        selected_version = str(current.get("parser_version", "p02_lightweight_locator@1"))
        reason = "A materially better specialist cannot rewrite a frozen obligation without reviewed oracle amendment."
        vetoes.append({"backend": selectable[0]["backend"], "code": "frozen_identity_requires_oracle_amendment"})
    elif selectable:
        winner = selectable[0]
        status = "specialist_selected"
        selected_backend = winner["backend"]
        selected_version = winner["parser_version"]
        reason = "A source-mappable specialist is lexicographically better at the first differing fidelity field."
    elif vetoes:
        status = "blocked_by_specialist_evidence"
        selected_backend = "current"
        selected_version = str(current.get("parser_version", "p02_lightweight_locator@1"))
        reason = "Independent specialist evidence triggered a reviewed parser veto; current is retained but not promoted."
    else:
        status = "current_retained"
        selected_backend = "current"
        selected_version = str(current.get("parser_version", "p02_lightweight_locator@1"))
        reason = "No source-mappable specialist is lexicographically better than the current exact-byte route."
    return {
        "schema_version": "p02_parser_selection@1",
        "status": status,
        "selected_backend": selected_backend,
        "selected_version": selected_version,
        "fidelity_fields": list(P02_FIDELITY_FIELDS),
        "current_fidelity_vector": list(current_vector),
        "specialists": candidates,
        "vetoes": vetoes,
        "reason": reason,
        "proxy_metrics_used_for_selection": [],
        "non_claim": "Parser capability selection is extraction routing only and is not mathematical evidence.",
    }
