"""Source-bound comparison and integration contracts for rigor reports."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
from typing import Any

from .contracts import SCHEMA_VERSION, attach_contract
from .evidence_manifest import content_digest


LIFECYCLE_CONTRACT = "math_document_rigor_lifecycle"
EDITORIAL_CONTRACT_VERSION = "exposition_surface_diagnostics@1"
OBLIGATION_METADATA_VERSION = "obligation_metadata@1"
REPORT_PROFILES = frozenset({"actionable", "forensic"})
FORENSIC_COLLECTIONS = {
    "issues": ("issues",),
    "gaps": ("gaps",),
    "proposals": ("proposals",),
    "tool_uses": ("tool_uses",),
    "targets": ("target_selection", "targets"),
    "raw_route_gaps": ("source_reports", "raw_route_gaps"),
    "raw_route_proposals": ("source_reports", "raw_route_proposals"),
}

_OPEN_SEVERITY = {
    "resolved_by_existing_context": 0,
    "partially_resolved": 1,
    "improved_but_open": 1,
    "needs_formalization": 2,
    "unresolved": 3,
}


def semantic_issue_projection(issue: Mapping[str, Any]) -> dict[str, Any]:
    """Project one issue onto stable, report-runtime-independent semantics."""
    return {
        key: issue.get(key)
        for key in (
            "issue_id",
            "label",
            "family",
            "status",
            "roles",
            "location",
            "unresolved_obligations",
            "existing_context_support",
            "candidate_patch",
            "patch_class",
            "math_nonclaim",
        )
        if issue.get(key) not in (None, "", [], {})
    }


def semantic_issue_digest(issue: Mapping[str, Any]) -> str:
    return content_digest(semantic_issue_projection(issue))


def _report_identity(report: Mapping[str, Any]) -> dict[str, Any]:
    source = report.get("source") if isinstance(report.get("source"), Mapping) else {}
    selection = report.get("target_selection") if isinstance(report.get("target_selection"), Mapping) else {}
    labels = sorted(
        str(item.get("label"))
        for item in selection.get("targets", [])
        if isinstance(item, Mapping) and item.get("label")
    )
    metadata = report.get("metadata") if isinstance(report.get("metadata"), Mapping) else {}
    return {
        "source_digest": source.get("source_digest"),
        "source_file": source.get("file"),
        "canonical_path": source.get("canonical_path"),
        "labels": labels,
        "schema_version": metadata.get("schema_version"),
        "contract": metadata.get("contract"),
    }


def _validated_revision_manifest(
    manifest: Mapping[str, Any] | None,
    *,
    prior: Mapping[str, Any],
    current: Mapping[str, Any],
) -> bool:
    if manifest is None:
        return False
    expected = {
        "schema_version": "rigor_report_revision@1",
        "prior_source_digest": prior.get("source_digest"),
        "current_source_digest": current.get("source_digest"),
        "source_file": current.get("source_file"),
        "labels": current.get("labels"),
        "relation": "controlled_revision",
    }
    return all(manifest.get(key) == value for key, value in expected.items())


def compare_rigor_reports(
    current_report: Mapping[str, Any],
    prior_report: Mapping[str, Any],
    *,
    revision_manifest: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Compare issue lifecycle only after report and source identities validate."""
    current_identity = _report_identity(current_report)
    prior_identity = _report_identity(prior_report)
    reasons: list[str] = []
    for key in ("source_file", "canonical_path", "labels", "schema_version", "contract"):
        if prior_identity.get(key) != current_identity.get(key):
            reasons.append(f"mismatched_{key}")
    same_source = prior_identity.get("source_digest") == current_identity.get("source_digest")
    if not same_source and not _validated_revision_manifest(
        revision_manifest,
        prior=prior_identity,
        current=current_identity,
    ):
        reasons.append("unbound_source_revision")
    if current_identity.get("schema_version") != SCHEMA_VERSION:
        reasons.append("unsupported_current_schema")
    if reasons:
        return attach_contract(
            {
                "status": "inconclusive",
                "reasons": sorted(set(reasons)),
                "prior_identity": prior_identity,
                "current_identity": current_identity,
                "transitions": [],
                "status_counts": {},
                "non_claim": "An inconclusive comparison cannot establish issue closure or regression.",
            },
            LIFECYCLE_CONTRACT,
        )

    prior_issues = {
        str(item.get("issue_id")): item
        for item in prior_report.get("issues", [])
        if isinstance(item, Mapping) and item.get("issue_id")
    }
    current_issues = {
        str(item.get("issue_id")): item
        for item in current_report.get("issues", [])
        if isinstance(item, Mapping) and item.get("issue_id")
    }
    transitions: list[dict[str, Any]] = []
    for issue_id in sorted(set(prior_issues) | set(current_issues)):
        before = prior_issues.get(issue_id)
        after = current_issues.get(issue_id)
        if before is None:
            lifecycle = "new"
        elif after is None:
            lifecycle = "closed"
        else:
            before_score = _OPEN_SEVERITY.get(str(before.get("status")), 2)
            after_score = _OPEN_SEVERITY.get(str(after.get("status")), 2)
            if after_score == 0 and before_score > 0:
                lifecycle = "closed"
            elif after_score < before_score:
                lifecycle = "improved_but_open"
            elif after_score > before_score:
                lifecycle = "regressed"
            else:
                before_open = set(str(item) for item in before.get("unresolved_obligations", []))
                after_open = set(str(item) for item in after.get("unresolved_obligations", []))
                if after_open < before_open:
                    lifecycle = "improved_but_open"
                elif before_open < after_open:
                    lifecycle = "regressed"
                else:
                    lifecycle = "unchanged"
        transitions.append(
            {
                "issue_id": issue_id,
                "status": lifecycle,
                "prior_status": before.get("status") if before is not None else None,
                "current_status": after.get("status") if after is not None else None,
                "prior_issue_digest": semantic_issue_digest(before) if before is not None else None,
                "current_issue_digest": semantic_issue_digest(after) if after is not None else None,
            }
        )
    status_counts = {
        status: sum(item["status"] == status for item in transitions)
        for status in ("closed", "improved_but_open", "unchanged", "regressed", "new")
    }
    return attach_contract(
        {
            "status": "compared",
            "prior_identity": prior_identity,
            "current_identity": current_identity,
            "source_relation": "same_bytes" if same_source else "controlled_revision",
            "transitions": transitions,
            "status_counts": status_counts,
            "non_claim": "Lifecycle status compares report obligations; it does not prove the mathematics or source truth.",
        },
        LIFECYCLE_CONTRACT,
    )


def validate_obligation_metadata(
    metadata: Mapping[str, Any] | None,
    *,
    source: Mapping[str, Any],
    selected_labels: Sequence[str],
) -> dict[str, list[dict[str, Any]]]:
    """Validate advisory author metadata without allowing it to alter source facts."""
    if metadata is None:
        return {}
    if metadata.get("schema_version") != OBLIGATION_METADATA_VERSION:
        raise ValueError(f"obligation metadata schema_version must be {OBLIGATION_METADATA_VERSION}")
    supplied_source = metadata.get("source")
    if not isinstance(supplied_source, Mapping) or any(
        supplied_source.get(key) != source.get(key) for key in ("file", "source_digest")
    ):
        raise ValueError("obligation metadata source identity does not match the audited document")
    entries = metadata.get("entries")
    if not isinstance(entries, list):
        raise ValueError("obligation metadata entries must be a list")
    allowed_labels = set(selected_labels)
    result: dict[str, list[dict[str, Any]]] = {}
    seen_ids: set[tuple[str, str]] = set()
    for entry in entries:
        if not isinstance(entry, Mapping) or not isinstance(entry.get("label"), str):
            raise ValueError("each obligation metadata entry must have a string label")
        label = str(entry["label"])
        if label not in allowed_labels:
            raise ValueError("obligation metadata contains an unknown or unselected label")
        obligations = entry.get("obligations")
        if not isinstance(obligations, list):
            raise ValueError("obligation metadata obligations must be a list")
        for obligation in obligations:
            if not isinstance(obligation, Mapping):
                raise ValueError("obligation metadata records must be objects")
            obligation_id = obligation.get("id")
            statement = obligation.get("statement")
            provenance = obligation.get("provenance")
            if not isinstance(obligation_id, str) or not obligation_id or not isinstance(statement, str) or not statement:
                raise ValueError("obligation metadata requires non-empty id and statement strings")
            if provenance != "author_supplied":
                raise ValueError("caller obligation metadata provenance must be author_supplied")
            key = (label, obligation_id)
            if key in seen_ids:
                raise ValueError("obligation metadata contains a conflicting duplicate id")
            seen_ids.add(key)
            result.setdefault(label, []).append(
                {
                    "id": obligation_id,
                    "statement": statement,
                    "provenance": "author_supplied",
                    "authority": "advisory_not_source_truth",
                }
            )
    return result


def build_editorial_integration_records(
    issues: Sequence[Mapping[str, Any]],
    *,
    source: Mapping[str, Any],
    obligation_metadata: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
) -> list[dict[str, Any]]:
    supplied = obligation_metadata or {}
    records: list[dict[str, Any]] = []
    for issue in issues:
        label = str(issue.get("label") or "")
        inferred = [
            {"id": str(item), "provenance": "inferred", "authority": "diagnostic_only"}
            for item in issue.get("unresolved_obligations", [])
        ]
        source_evidenced = [
            {
                "id": f"source_support_{index}",
                "provenance": "source_evidenced",
                "source_span": dict(span),
            }
            for index, span in enumerate(issue.get("existing_context_support", []), start=1)
            if isinstance(span, Mapping)
        ]
        record = {
            "schema_version": EDITORIAL_CONTRACT_VERSION,
            "issue_id": issue.get("issue_id"),
            "issue_digest": semantic_issue_digest(issue),
            "label": label,
            "location": issue.get("location"),
            "roles": issue.get("roles", []),
            "status": issue.get("status"),
            "source": dict(source),
            "support": source_evidenced,
            "unresolved_obligations": inferred,
            "author_metadata": [dict(item) for item in supplied.get(label, [])],
            "candidate_patch": issue.get("candidate_patch"),
            "patch_class": issue.get("patch_class"),
            "surface_diagnostics": issue.get("exposition_surface_diagnostics", {}),
            "requires_human_review": bool(issue.get("candidate_patch")),
            "nonclaims": [
                issue.get("math_nonclaim", "Diagnostic evidence is not proof."),
                "Author-supplied metadata is advisory and cannot override extracted source spans or backend evidence.",
                "This record does not certify readability, source truth, publication readiness, or mathematical proof.",
            ],
        }
        record["record_digest"] = content_digest(record)
        records.append(record)
    return records


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def bytes_sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def page_rigor_report_records(
    artifact_root: str,
    sha256: str,
    collection: str,
    *,
    offset: int = 0,
    limit: int = 100,
) -> dict[str, Any]:
    """Resolve a bounded allowlisted forensic collection from one exact report artifact."""
    from .agent_report_artifacts import resolve_agent_report

    if collection not in FORENSIC_COLLECTIONS:
        raise ValueError(f"collection must be one of: {', '.join(sorted(FORENSIC_COLLECTIONS))}")
    if offset < 0:
        raise ValueError("offset must be non-negative")
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100")
    resolved = resolve_agent_report(artifact_root, sha256)
    report = resolved["report"]
    if report.get("metadata", {}).get("contract") != "math_document_rigor_audit":
        raise ValueError("artifact is not a math document rigor report")
    value: Any = report
    for key in FORENSIC_COLLECTIONS[collection]:
        value = value.get(key) if isinstance(value, Mapping) else None
    if not isinstance(value, list):
        value = []
    page = value[offset : offset + limit]
    records = []
    for index, record in enumerate(page, start=offset):
        digest = bytes_sha256(canonical_json_bytes(record))
        records.append({"index": index, "record_sha256": digest, "record": record})
    next_offset = offset + len(page)
    return attach_contract(
        {
            "status": "resolved",
            "artifact": resolved["artifact"],
            "collection": collection,
            "offset": offset,
            "limit": limit,
            "total_count": len(value),
            "records": records,
            "next_offset": next_offset if next_offset < len(value) else None,
            "non_claim": "Selective retrieval changes transport only; it does not filter canonical evidence or establish proof.",
        },
        "math_document_rigor_record_page",
    )
