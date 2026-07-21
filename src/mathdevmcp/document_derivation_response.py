from __future__ import annotations

"""Bounded transport views over a completed document-derivation audit."""

from collections.abc import Mapping, Sequence
from copy import deepcopy
import base64
import binascii
import hashlib
import json
import os
from pathlib import Path
import re
import struct
import sys
from typing import Any

from .artifact_storage import write_bytes_no_replace
from .contracts import contract_metadata
from .failure_ledgers import validate_discriminating_action


DOCUMENT_DERIVATION_RESPONSE_CONTRACT = "document_derivation_response"
DOCUMENT_DERIVATION_RESPONSE_SCHEMA = "p08_document_derivation_response@2"
DOCUMENT_DERIVATION_ARTIFACT_SCHEMA = "p07_document_derivation_artifact@1"
DOCUMENT_DERIVATION_CURSOR_SCHEMA = "p08_document_derivation_cursor@2"
DOCUMENT_DERIVATION_REQUEST_SCHEMA = "p07_document_derivation_request@1"
DOCUMENT_DERIVATION_SELECTOR_SCHEMA = "p08d_document_derivation_selector@1"
DOCUMENT_DERIVATION_RESOLVER_SCOPE_SCHEMA = (
    "p08d_document_derivation_resolver_scope@1"
)
DOCUMENT_DERIVATION_RECORD_PAGE_SCHEMA = (
    "p08d_document_derivation_record_page@1"
)
DOCUMENT_DERIVATION_FILTER_SCHEMA = "p07_document_derivation_response@1"
RESPONSE_MODES = frozenset({"compact", "detailed", "artifact_only"})
MIN_TARGET_LIMIT = 1
MAX_TARGET_LIMIT = 100
DEFAULT_TARGET_LIMIT = 20
COMPACT_PAYLOAD_TARGET_BYTES = 25_600
PUBLIC_TRANSPORT_TARGET_BYTES = 30_720
DOCUMENT_DERIVATION_BYTE_POLICY = "p08d_compact_byte_policy@1"
DOCUMENT_DERIVATION_ACTION_POLICY = "p08d_unresolved_choice_action_policy@1"
DOCUMENT_DERIVATION_COMPATIBILITY_TEXT = (
    "MathDevMCP structured result; read structuredContent."
)

_TOKEN_MAGIC = b"MDP2"
_TOKEN_BYTE_POLICY_CODE = 1
_TOKEN_DIGEST_COUNT = 7
_TOKEN_SIZE = len(_TOKEN_MAGIC) + 8 + _TOKEN_DIGEST_COUNT * 32

_GLOBAL_RESOLVER_COLLECTIONS = (
    "global_blocker_records",
    "global_evidence_ref_records",
    "global_source_ref_records",
)
_TARGET_RESOLVER_COLLECTIONS = (
    "blocker_records",
    "evidence_ref_records",
    "source_ref_records",
    "unresolved_assumption_records",
    "candidate_assumption_records",
    "selected_action",
    "label_scoped_obligation",
    "typed_repair_obligation",
    "math_obligation",
    "source_span",
    "target_text",
)


def document_derivation_resolver_catalog() -> dict[str, Any]:
    """Return the closed resolver vocabulary used by CLI and MCP clients."""
    return {
        "schema_version": DOCUMENT_DERIVATION_RESOLVER_SCOPE_SCHEMA,
        "global_collections": list(_GLOBAL_RESOLVER_COLLECTIONS),
        "target_collections": list(_TARGET_RESOLVER_COLLECTIONS),
        "target_id_rule": "omit target_id for global collections; require an exact page target_id for target collections",
    }

_PRESENTATION_FIELDS = frozenset({"markdown", "output_md", "output_json"})
_BACKEND_PATH_KEYS = frozenset(
    {"executable", "prefix", "backend_prefix", "path_head"}
)
_OUTPUT_PATH_KEYS = frozenset(
    {"output_md", "output_json", "artifact_root", "cache", "cache_path", "temp_path"}
)
_ABSOLUTE_PATH_FRAGMENT = re.compile(
    r"(?<![A-Za-z0-9_.-])/(?:home|tmp|usr|opt|var|run|mnt|srv)"
    r"(?:/[^/\s'\"`<>|,;?&#=]+)*"
)


def _canonical_json_bytes(value: Any) -> bytes:
    """Serialize losslessly; unlike evidence schemas, presentation keeps duplicates."""
    try:
        text = json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise ValueError("document derivation response contains non-JSON data") from exc
    return text.encode("utf-8")


def _canonical_digest(value: Any) -> str:
    return hashlib.sha256(_canonical_json_bytes(value)).hexdigest()


def _without_presentation_fields(audit: Mapping[str, Any]) -> dict[str, Any]:
    value = deepcopy(dict(audit))
    for key in _PRESENTATION_FIELDS:
        value.pop(key, None)
    return value


def _normalized_source_identity(tex_path: str | Path) -> str:
    return str(Path(tex_path).expanduser().resolve(strict=False))


def build_document_derivation_audit_request(
    tex_path: str | Path,
    *,
    focus_labels: Sequence[str] | None = None,
    max_labels: int | None = 30,
    budget_profile: str = "standard",
    max_attempts: int = 3,
    backend_env: str = "mathdevmcp-backends",
    search_mode: str = "agent_guided",
    grounding_policy: str = "strict",
    workers: int = 1,
) -> dict[str, Any]:
    """Build the complete presentation identity for one raw audit invocation."""
    labels = [] if focus_labels is None else [str(item) for item in focus_labels]
    if any(not item for item in labels):
        raise ValueError("focus_labels must contain non-empty strings")
    request = {
        "schema_version": DOCUMENT_DERIVATION_REQUEST_SCHEMA,
        "source_identity": _normalized_source_identity(tex_path),
        "focus_labels": labels,
        "max_labels": None if max_labels is None else int(max_labels),
        "budget_profile": str(budget_profile),
        "max_attempts": int(max_attempts),
        "backend_env": str(backend_env),
        "search_mode": str(search_mode),
        "grounding_policy": str(grounding_policy),
        "workers": int(workers) if workers is not None else 1,
        "authority": "presentation_identity_only",
    }
    if request["max_labels"] is not None and request["max_labels"] <= 0:
        request["max_labels"] = None
    if request["max_attempts"] < 0:
        raise ValueError("max_attempts must be non-negative")
    request["audit_request_id"] = "request_" + _canonical_digest(request)
    return request


def audit_result_id(audit: Mapping[str, Any]) -> str:
    return "audit_" + _canonical_digest(_without_presentation_fields(audit))


def _walk(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key)
            child_path = (*path, key)
            yield child_path, key, child
            yield from _walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = (*path, str(index))
            yield child_path, str(index), child
            yield from _walk(child, child_path)


def _string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value if isinstance(item, (str, int)) and str(item)]
    return []


def _collect_veto_ids(value: Any) -> list[str]:
    ids: set[str] = set()
    for _, key, child in _walk(value):
        if (
            ("veto" in key and key.endswith("_ids"))
            or key in {"launch_vetoes", "vetoes"}
        ):
            ids.update(_string_values(child))
    if (
        isinstance(value, Mapping)
        and value.get("integrity_binding_verified") is True
        and "legacy_unbound_document_evidence"
        not in _string_values(value.get("veto_ids", []))
    ):
        ids.discard("legacy_unbound_document_evidence")
    return sorted(ids)


def _assumption_record(value: Mapping[str, Any]) -> dict[str, Any]:
    record = {
        key: deepcopy(value.get(key))
        for key in (
            "id",
            "status",
            "text",
            "statement",
            "assumptions",
            "role",
            "branch_id",
            "source",
            "evidence_refs",
            "source_refs",
        )
        if key in value
    }
    if not isinstance(record.get("id"), str) or not record["id"]:
        record["id"] = "assumption_" + _canonical_digest(dict(value))
        record["id_authority"] = "synthetic_presentation_identity"
    return record


def _collect_unresolved_assumptions(value: Any) -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path, key, child in _walk(value):
        if key.endswith("unresolved_assumption_ids") or key.endswith("missing_assumption_ids") or key.endswith("blocked_by_assumption_ids"):
            for item in _string_values(child):
                records.setdefault(item, {"id": item, "status": "unresolved"})
        if key in {
            "missing_route_assumptions",
            "missing_or_unresolved_assumptions",
            "unresolved_assumptions",
        }:
            for item in _string_values(child):
                item_id = "assumption_" + _canonical_digest({"field": key, "text": item})
                records.setdefault(
                    item_id,
                    {
                        "id": item_id,
                        "status": "unresolved",
                        "text": item,
                        "id_authority": "synthetic_presentation_identity",
                    },
                )
        if not isinstance(child, Mapping):
            continue
        status = str(child.get("status", ""))
        assumption_context = any("assumption" in part for part in path)
        if status not in {"missing", "unresolved"} or not assumption_context:
            continue
        record = _assumption_record(child)
        records.setdefault(str(record["id"]), record)
    return [records[key] for key in sorted(records)]


def _collect_candidate_assumptions(value: Any) -> list[dict[str, Any]]:
    records: dict[bytes, dict[str, Any]] = {}
    for path, key, child in _walk(value):
        if key == "proposed_assumptions":
            for item in _string_values(child):
                record = {
                    "id": "candidate_assumption_" + _canonical_digest(item),
                    "status": "candidate",
                    "text": item,
                    "id_authority": "synthetic_presentation_identity",
                }
                records.setdefault(_canonical_json_bytes(record), record)
        if not isinstance(child, Mapping):
            continue
        status = str(child.get("status", ""))
        candidate_context = len(path) >= 2 and path[-2] in {
            "possible_assumption_sets",
            "typed_assumptions",
        }
        if status not in {"candidate", "proposed_sufficient"} and not candidate_context:
            continue
        record = _assumption_record(child)
        if not any(record.get(field) for field in ("id", "text", "statement", "assumptions")):
            continue
        record.setdefault("status", "candidate")
        records.setdefault(_canonical_json_bytes(record), record)
    return [records[key] for key in sorted(records)]


def _collect_action_decision_ids(value: Any) -> list[str]:
    ids: set[str] = set()
    for _, key, child in _walk(value):
        if key in {"action_id", "decision_id", "selected_action_id", "promotion_decision_id"}:
            ids.update(_string_values(child))
        elif key.endswith("_action_ids") or key.endswith("_decision_ids"):
            ids.update(_string_values(child))
    return sorted(ids)


def _dedupe_values(values: Sequence[Any]) -> list[Any]:
    by_bytes: dict[bytes, Any] = {}
    for value in values:
        try:
            key = _canonical_json_bytes(value)
        except (TypeError, ValueError):
            key = _canonical_json_bytes(str(value))
            value = str(value)
        by_bytes.setdefault(key, deepcopy(value))
    return [by_bytes[key] for key in sorted(by_bytes)]


def _collect_non_claims(value: Any) -> list[Any]:
    items: list[Any] = []
    for _, key, child in _walk(value):
        if key not in {"non_claim", "non_claims"}:
            continue
        if isinstance(child, list):
            items.extend(child)
        elif child not in (None, ""):
            items.append(child)
    return _dedupe_values(items)


def _source_ref_records(value: Any) -> list[Any]:
    refs: list[Any] = []
    for _, key, child in _walk(value):
        if "source_ref" not in key:
            continue
        if isinstance(child, Mapping):
            refs.append(deepcopy(dict(child)))
        elif isinstance(child, list):
            refs.extend(
                deepcopy(dict(item)) if isinstance(item, Mapping) else str(item)
                for item in child
                if isinstance(item, (Mapping, str)) and item
            )
        elif isinstance(child, str) and child:
            refs.append(child)
    unique: dict[str, Any] = {}
    for ref in refs:
        ref_id = "source_ref_" + _canonical_digest(ref)
        unique.setdefault(ref_id, ref)
    return [unique[key] for key in sorted(unique)]


def _source_ref_entries(value: Any) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for record in _source_ref_records(value):
        ref_id = "source_ref_" + _canonical_digest(record)
        if isinstance(record, Mapping):
            entries.append({**deepcopy(dict(record)), "source_ref_id": ref_id})
        else:
            entries.append({"source_ref_id": ref_id, "ref": str(record)})
    return entries


def _collect_evidence_refs(value: Any) -> list[str]:
    refs: set[str] = set()
    for _, key, child in _walk(value):
        is_evidence_ref = (
            "evidence_ref" in key
            or key in {"manifest_ref", "request_ref", "result_ref", "output_ref", "artifact_ref"}
            or key.endswith("_manifest_ref")
            or key.endswith("_request_ref")
            or key.endswith("_result_ref")
            or key.endswith("_output_ref")
            or key.endswith("_artifact_ref")
            or key in {"attempt_refs", "request_refs", "result_refs", "output_refs", "artifact_refs", "manifest_refs"}
        )
        if is_evidence_ref:
            refs.update(_string_values(child))
    return sorted(refs)


def _evidence_ref_entries(value: Any) -> list[dict[str, str]]:
    return [
        {"evidence_ref_id": "evidence_ref_" + _canonical_digest(ref), "ref": ref}
        for ref in _collect_evidence_refs(value)
    ]


def _collect_failure_classifications(value: Any) -> list[str]:
    if isinstance(value, Mapping) and "failure_classifications" in value:
        return sorted(set(_string_values(value.get("failure_classifications"))))
    classifications: set[str] = set()
    for _, key, child in _walk(value):
        if key == "failure_classification" or key == "failure_classifications":
            classifications.update(_string_values(child))
    return sorted(classifications)


def _execution_summary(audit: Mapping[str, Any]) -> dict[str, Any]:
    execution = audit.get("execution") if isinstance(audit.get("execution"), Mapping) else {}
    return {
        key: deepcopy(execution[key])
        for key in (
            "mode",
            "workers_requested",
            "workers_used",
            "target_count",
            "failure_count",
            "failures",
            "pipeline_entered",
            "boundary",
        )
        if key in execution
    }


def _reference_inventory(value: Any) -> dict[str, Any]:
    evidence_entries = _evidence_ref_entries(value)
    evidence_refs = [item["ref"] for item in evidence_entries]
    evidence_ref_ids = [item["evidence_ref_id"] for item in evidence_entries]
    source_ref_ids = [item["source_ref_id"] for item in _source_ref_entries(value)]
    return {
        "evidence_refs": evidence_refs,
        "evidence_ref_ids": evidence_ref_ids,
        "evidence_ref_count": len(evidence_refs),
        "evidence_ref_digest": _canonical_digest(evidence_ref_ids),
        "source_ref_ids": source_ref_ids,
        "source_ref_count": len(source_ref_ids),
        "source_ref_digest": _canonical_digest(source_ref_ids),
        "full_records": "detailed_or_verified_artifact",
    }


def _target_id(target: Mapping[str, Any], index: int) -> str:
    for key in ("id", "row_id", "label"):
        value = target.get(key)
        if isinstance(value, str) and value:
            suffix = f":{target.get('row_index')}" if key == "label" and target.get("row_index") is not None else ""
            return f"target:{value}{suffix}"
    return "target_" + _canonical_digest({"index": index, "target": dict(target)})


def _target_order(audit: Mapping[str, Any]) -> list[str]:
    targets = audit.get("targets") if isinstance(audit.get("targets"), list) else []
    return [_target_id(item, index) for index, item in enumerate(targets) if isinstance(item, Mapping)]


def _filter_id(audit: Mapping[str, Any]) -> str:
    return "filter_" + _canonical_digest(
        {"schema_version": DOCUMENT_DERIVATION_FILTER_SCHEMA, "target_order": _target_order(audit)}
    )


def _blocker_records(value: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for _, key, child in _walk(value):
        if "blocker" not in key or key.endswith("_ids") or key.endswith("_count"):
            continue
        if isinstance(child, Mapping):
            records.append(deepcopy(dict(child)))
        elif isinstance(child, list):
            records.extend(deepcopy(dict(item)) for item in child if isinstance(item, Mapping))
    unique: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = str(record.get("id", "")) or "blocker_" + _canonical_digest(record)
        normalized = deepcopy(record)
        normalized["id"] = record_id
        unique.setdefault(_canonical_digest(normalized), normalized)
    return [unique[key] for key in sorted(unique)]


def _selected_action(value: Any) -> dict[str, Any] | None:
    if isinstance(value, Mapping):
        tree = value.get("tree") if isinstance(value.get("tree"), Mapping) else value
        ranking = tree.get("branch_ranking") if isinstance(tree.get("branch_ranking"), Mapping) else {}
        action = ranking.get("selected_action")
        if isinstance(action, Mapping) and action:
            return deepcopy(dict(action))
    for _, key, child in _walk(value):
        if key == "selected_action" and isinstance(child, Mapping) and child:
            return deepcopy(dict(child))
    return None


def _fallback_action(target_id: str, blockers: list[dict[str, Any]]) -> dict[str, Any]:
    blocker_ids = sorted(str(item["id"]) for item in blockers)
    next_evidence = next(
        (
            str(item.get("required_next_evidence"))
            for item in blockers
            if isinstance(item.get("required_next_evidence"), str) and item.get("required_next_evidence")
        ),
        "Inspect the target's exact blocker and evidence references before choosing a mathematical route.",
    )
    payload = {
        "action_kind": "inspect_blocker_evidence",
        "target_ids": [target_id],
        "blocker_ids": blocker_ids,
        "required_next_evidence": next_evidence,
        "expected_artifact": {
            "kind": "scoped_diagnostic_followup",
            "binding_fields": ["target_id", "blocker_ids"],
        },
        "authority": "presentation_only",
        "non_claim": "This fallback is not a ranked mathematical action or publication authority.",
    }
    payload["action_id"] = "fallback_action_" + _canonical_digest(payload)
    return payload


def _logical_source_ref(result_id: str, source_identity: str) -> str:
    name = Path(source_identity).name or "document.tex"
    return f"mathdevmcp-source://{result_id}/{name}"


def _known_private_prefixes(
    source_identity: str,
    artifact_root: str | Path | None,
) -> list[str]:
    prefixes = {
        str(Path(source_identity).parent),
        str(Path.home()),
        str(Path(sys.prefix)),
    }
    if artifact_root is not None:
        prefixes.add(str(Path(artifact_root).expanduser().resolve(strict=False)))
    return sorted((item for item in prefixes if item and item != "/"), key=len, reverse=True)


def _redact_free_text(text: str, prefixes: Sequence[str]) -> str:
    result = text
    for prefix in prefixes:
        result = result.replace(prefix, "<redacted-local-root>")
    return _ABSOLUTE_PATH_FRAGMENT.sub("<redacted-local-path>", result)


def _redact_transport(
    value: Any,
    *,
    result_id: str,
    source_identity: str,
    artifact_root: str | Path | None,
    key: str = "",
    path: tuple[str, ...] = (),
) -> Any:
    logical_source = _logical_source_ref(result_id, source_identity)
    prefixes = _known_private_prefixes(source_identity, artifact_root)
    if isinstance(value, Mapping):
        return {
            str(child_key): _redact_transport(
                child,
                result_id=result_id,
                source_identity=source_identity,
                artifact_root=artifact_root,
                key=str(child_key),
                path=(*path, str(child_key)),
            )
            for child_key, child in value.items()
        }
    if isinstance(value, list):
        if key == "path_head":
            return ["<redacted-local-path>" for _ in value]
        return [
            _redact_transport(
                child,
                result_id=result_id,
                source_identity=source_identity,
                artifact_root=artifact_root,
                key=key,
                path=(*path, str(index)),
            )
            for index, child in enumerate(value)
        ]
    if not isinstance(value, str):
        return deepcopy(value)
    if key == "tex_path":
        return logical_source
    if key == "root" and (len(path) == 1 or "arguments" in path):
        return logical_source
    if key == "file" and Path(value).is_absolute():
        return f"{logical_source}#{Path(value).name}"
    if key in _BACKEND_PATH_KEYS or key in _OUTPUT_PATH_KEYS:
        return "<redacted-local-path>" if value else value
    path_bearing_key = (
        "path" in key
        or key.endswith("_dir")
        or key.endswith("_root")
        or "manifest" in key
    )
    if path_bearing_key and Path(value).is_absolute():
        return "<redacted-local-path>"
    return _redact_free_text(value, prefixes)


def _compact_action(action: Mapping[str, Any]) -> dict[str, Any]:
    return deepcopy(dict(action))


def _compact_target(
    target: Mapping[str, Any],
    *,
    index: int,
    result_id: str,
    source_identity: str,
    artifact_root: str | Path | None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    target_id = _target_id(target, index)
    blockers = _blocker_records(target)
    action = _selected_action(target) or _fallback_action(target_id, blockers)
    assumptions = _collect_unresolved_assumptions(target)
    candidate_assumptions = _collect_candidate_assumptions(target)
    source_refs = _source_ref_entries(target)
    compact = {
        "target_id": target_id,
        "label": target.get("label"),
        "row_id": target.get("row_id"),
        "row_index": target.get("row_index"),
        "location": target.get("location"),
        "status": target.get("status"),
        "publication_mode": target.get("publication_mode", "disabled"),
        "promotion": deepcopy(target.get("promotion", {})),
        "failure_classifications": sorted(
            set(_string_values(target.get("failure_classifications", [])))
        ),
        "veto_ids": _collect_veto_ids(target),
        "unresolved_assumptions": assumptions,
        "candidate_assumptions": candidate_assumptions,
        "blocker_ids": sorted({str(item["id"]) for item in blockers}),
        "selected_action": _compact_action(action),
        "source_evidence": _compact_source_evidence(target),
        "evidence_refs": _evidence_ref_entries(target),
        "source_refs": source_refs,
        "reference_resolution": "exact_current_page_records",
    }
    return (
        _redact_transport(
            compact,
            result_id=result_id,
            source_identity=source_identity,
            artifact_root=artifact_root,
        ),
        blockers,
    )


def _blocker_catalog(
    target_blockers: Sequence[tuple[str, Sequence[Mapping[str, Any]]]],
    *,
    result_id: str,
    source_identity: str,
    artifact_root: str | Path | None,
) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for target_id, blockers in target_blockers:
        for blocker in blockers:
            scope = blocker.get("scope") if isinstance(blocker.get("scope"), Mapping) else {}
            identity = {
                "kind": blocker.get("kind"),
                "problem": blocker.get("problem"),
                "why": blocker.get("why"),
                "required_next_evidence": blocker.get("required_next_evidence"),
                "scope": scope,
            }
            group_id = "blocker_group_" + _canonical_digest(identity)
            group = groups.setdefault(
                group_id,
                {
                    "group_id": group_id,
                    **deepcopy(identity),
                    "blocker_ids": [],
                    "affected_target_ids": [],
                    "evidence_refs": [],
                },
            )
            group["blocker_ids"].append(str(blocker.get("id")))
            group["affected_target_ids"].append(target_id)
            group["evidence_refs"].extend(_collect_evidence_refs(blocker))
    for group in groups.values():
        for key in ("blocker_ids", "affected_target_ids", "evidence_refs"):
            group[key] = sorted(set(group[key]))
    catalog = [groups[key] for key in sorted(groups)]
    return _redact_transport(
        catalog,
        result_id=result_id,
        source_identity=source_identity,
        artifact_root=artifact_root,
    )


def _outcome_policy() -> dict[str, dict[str, Any]]:
    return {
        name: {
            "stop": True,
            "means": (
                f"The action ended with scoped outcome {name}; record it in the "
                "appropriate ledger."
            ),
            "does_not_mean": (
                "It does not by itself establish document proof, repair correctness, "
                "publication authority, or scientific optimality."
            ),
        }
        for name in (
            "unavailable",
            "unsupported",
            "timeout",
            "execution_error",
            "malformed",
            "certified",
            "refuted",
            "unknown",
        )
    }


_REGISTERED_ACTION_POLICY: dict[str, Any] = {
    "schema_version": "p06_discriminating_action@1",
    "action_kind": "blocked_for_human_or_formalization_choice",
    "ledger_entry_ids": ["unresolved_branch_choice"],
    "prerequisites": ["resolve_nondominated_branch_choice"],
    "tool_route": {
        "tool": None,
        "role": "local_function",
        "route": "mathdevmcp.failure_ledgers.select_next_discriminating_action",
        "availability_state": "available",
    },
    "budget": {
        "profile": "synthetic_local",
        "max_attempts": 1,
        "timeout_ms": None,
        "max_output_bytes": None,
        "provenance": (
            "Phase 06 smallest-discriminator default; unknown fields remain null"
        ),
    },
    "expected_artifact": {
        "kind": "formalization_choice_record",
        "schema_version": "p06_formalization_choice@1",
        "binding_fields": ["branch_ids", "target_id"],
        "path_role": "decision_blocker",
    },
    "outcomes": _outcome_policy(),
    "non_claims": [
        "the action does not authorize publication or source editing",
        "the selected action is a discriminator, not a predicted success",
    ],
}


def _checked_indices(
    indices: Sequence[Any],
    values: Sequence[str],
    *,
    field: str,
    allow_duplicates: bool,
) -> list[str]:
    if any(
        not isinstance(index, int)
        or isinstance(index, bool)
        or index < 0
        or index >= len(values)
        for index in indices
    ):
        raise ValueError(f"{field} contains an out-of-range index")
    if not allow_duplicates and len(indices) != len(set(indices)):
        raise ValueError(f"{field} contains a duplicate index")
    return [values[index] for index in indices]


def _project_action(
    action: Mapping[str, Any],
    global_veto_ids: list[str],
) -> dict[str, Any]:
    validated = validate_discriminating_action(action)
    if _canonical_json_bytes(validated) != _canonical_json_bytes(action):
        raise ValueError("selected action changes under the Phase 06 validator")
    expected = {
        **deepcopy(_REGISTERED_ACTION_POLICY),
        "action_id": action.get("action_id"),
        "target_ids": deepcopy(action.get("branch_ids")),
        "branch_ids": deepcopy(action.get("branch_ids")),
        "launch_vetoes": deepcopy(action.get("launch_vetoes")),
    }
    if _canonical_json_bytes(expected) != _canonical_json_bytes(action):
        if action.get("outcomes") == _outcome_policy():
            without_outcomes = deepcopy(dict(validated))
            without_outcomes.pop("outcomes", None)
            return {
                "representation": "shared_outcome_policy",
                "policy_id": DOCUMENT_DERIVATION_ACTION_POLICY,
                "action": without_outcomes,
            }
        return {
            "representation": "inline_validated",
            "action": deepcopy(dict(validated)),
        }
    return {
        "representation": "registered_policy",
        "policy_id": DOCUMENT_DERIVATION_ACTION_POLICY,
        "action_id": action["action_id"],
        "action_kind": action["action_kind"],
        "branch_ids": deepcopy(action["branch_ids"]),
        "launch_veto_indices": [
            global_veto_ids.index(value) for value in action["launch_vetoes"]
        ],
        "prerequisite": "resolve_nondominated_branch_choice",
        "expected_artifact_kind": "formalization_choice_record",
    }


def expand_document_derivation_action(
    projection: Mapping[str, Any],
    global_veto_ids: Sequence[str],
) -> dict[str, Any]:
    """Expand a compact selected action to the exact stored action contract."""
    if projection.get("representation") == "inline_validated":
        action = projection.get("action")
        if not isinstance(action, Mapping):
            raise ValueError("inline action projection is invalid")
        validated = validate_discriminating_action(action)
        if _canonical_json_bytes(validated) != _canonical_json_bytes(action):
            raise ValueError("inline action changes under the Phase 06 validator")
        return validated
    if projection.get("representation") == "shared_outcome_policy":
        if projection.get("policy_id") != DOCUMENT_DERIVATION_ACTION_POLICY:
            raise ValueError("unknown shared action outcome policy")
        action = projection.get("action")
        if not isinstance(action, Mapping) or "outcomes" in action:
            raise ValueError("shared-outcome action projection is invalid")
        expanded = {**deepcopy(dict(action)), "outcomes": _outcome_policy()}
        validated = validate_discriminating_action(expanded)
        if _canonical_json_bytes(validated) != _canonical_json_bytes(expanded):
            raise ValueError("shared-outcome action changes under the Phase 06 validator")
        return validated
    if projection.get("policy_id") != DOCUMENT_DERIVATION_ACTION_POLICY:
        raise ValueError("unknown action projection policy")
    launch_indices = projection.get("launch_veto_indices")
    if not isinstance(launch_indices, list):
        raise ValueError("projected launch veto indices are invalid")
    action = {
        **deepcopy(_REGISTERED_ACTION_POLICY),
        "action_id": projection["action_id"],
        "target_ids": deepcopy(projection["branch_ids"]),
        "branch_ids": deepcopy(projection["branch_ids"]),
        "launch_vetoes": _checked_indices(
            launch_indices,
            list(global_veto_ids),
            field="launch_veto_indices",
            allow_duplicates=False,
        ),
    }
    if action["action_kind"] != projection.get("action_kind"):
        raise ValueError("projected action kind differs from registered policy")
    if action["prerequisites"] != [projection.get("prerequisite")]:
        raise ValueError("projected prerequisite differs from registered policy")
    if action["expected_artifact"]["kind"] != projection.get(
        "expected_artifact_kind"
    ):
        raise ValueError("projected artifact kind differs from registered policy")
    return validate_discriminating_action(action)


def _raw_blocker_records(value: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for _, key, child in _walk(value):
        if "blocker" not in key or key.endswith("_ids") or key.endswith("_count"):
            continue
        if isinstance(child, Mapping):
            records.append(deepcopy(dict(child)))
        elif isinstance(child, list):
            records.extend(
                deepcopy(dict(item)) for item in child if isinstance(item, Mapping)
            )
    by_binding: dict[bytes, dict[str, Any]] = {}
    for record in records:
        identity = str(record.get("id", "")) or "blocker_" + _canonical_digest(record)
        binding = _record_binding(identity, record)
        by_binding.setdefault(_canonical_json_bytes(binding), record)
    return [by_binding[key] for key in sorted(by_binding)]


def _record_binding(identity: str, record: Any) -> dict[str, str]:
    if not identity:
        raise ValueError("record identity must be nonempty")
    return {"identity": identity, "raw_record_sha256": _canonical_digest(record)}


def _record_bindings(
    records: Sequence[Mapping[str, Any]],
    identity_key: str,
) -> list[dict[str, str]]:
    bindings = [_record_binding(str(record[identity_key]), record) for record in records]
    encoded = [_canonical_json_bytes(item) for item in bindings]
    if len(encoded) != len(set(encoded)):
        raise ValueError(f"{identity_key} collection contains a duplicate record binding")
    return bindings


def _blocker_bindings(value: Any) -> list[dict[str, str]]:
    return [
        _record_binding(
            str(record.get("id", "")) or "blocker_" + _canonical_digest(record),
            record,
        )
        for record in _raw_blocker_records(value)
    ]


def _target_content_identity(raw_target: Mapping[str, Any]) -> dict[str, str]:
    packet = raw_target.get("semantic_work_packet")
    if not isinstance(packet, Mapping):
        raise ValueError("artifact-indexed target has no semantic work packet")
    obligation = packet.get("typed_repair_obligation")
    label_scoped = packet.get("label_scoped_obligation")
    source_span = packet.get("source_span")
    target_text = packet.get("target")
    if not isinstance(obligation, Mapping):
        raise ValueError("semantic work packet has no typed repair obligation")
    math_obligation = obligation.get("math_obligation")
    if not isinstance(math_obligation, Mapping):
        raise ValueError("typed repair obligation has no math obligation")
    if not isinstance(label_scoped, Mapping):
        raise ValueError("semantic work packet has no label-scoped obligation")
    if not isinstance(source_span, Mapping):
        raise ValueError("semantic work packet has no source span")
    if not isinstance(target_text, str) or not target_text:
        raise ValueError("semantic work packet has no target text")
    for value, field in (
        (packet.get("id"), "semantic work packet"),
        (obligation.get("id"), "typed repair obligation"),
        (math_obligation.get("id"), "math obligation"),
        (label_scoped.get("obligation_id"), "label-scoped obligation"),
        (label_scoped.get("obligation_digest"), "label-scoped obligation digest"),
    ):
        if not isinstance(value, str) or not value:
            raise ValueError(f"{field} identity is missing")
    return {
        "semantic_work_packet_id": str(packet["id"]),
        "label_scoped_obligation_id": str(label_scoped["obligation_id"]),
        "label_scoped_obligation_digest": str(label_scoped["obligation_digest"]),
        "label_scoped_obligation_sha256": _canonical_digest(label_scoped),
        "typed_repair_obligation_id": str(obligation["id"]),
        "typed_repair_obligation_sha256": _canonical_digest(obligation),
        "math_obligation_id": str(math_obligation["id"]),
        "math_obligation_sha256": _canonical_digest(math_obligation),
        "source_span_sha256": _canonical_digest(source_span),
        "target_text_sha256": _canonical_digest(target_text),
    }


def _target_record_collections(
    compact_target: Mapping[str, Any],
    raw_target: Mapping[str, Any],
    *,
    result_id: str,
    source_identity: str,
) -> dict[str, Any]:
    blockers = _raw_blocker_records(raw_target)
    evidence_refs = _evidence_ref_entries(raw_target)
    source_refs = _source_ref_entries(raw_target)
    unresolved = _collect_unresolved_assumptions(raw_target)
    candidates = _collect_candidate_assumptions(raw_target)
    selected_action = _selected_action(raw_target)
    if not isinstance(selected_action, Mapping):
        raise ValueError("stored audit target has no selected action")
    expected = {
        "evidence_refs": compact_target["evidence_refs"],
        "source_refs": compact_target["source_refs"],
        "unresolved_assumptions": compact_target["unresolved_assumptions"],
        "candidate_assumptions": compact_target["candidate_assumptions"],
    }
    actual = {
        "evidence_refs": evidence_refs,
        "source_refs": source_refs,
        "unresolved_assumptions": unresolved,
        "candidate_assumptions": candidates,
    }
    normalized_actual = _redact_transport(
        actual,
        result_id=result_id,
        source_identity=source_identity,
        artifact_root=None,
    )
    if _canonical_json_bytes(normalized_actual) != _canonical_json_bytes(expected):
        raise ValueError("raw target collections differ from compact projection")
    blocker_ids = sorted(
        {
            str(item.get("id", "")) or "blocker_" + _canonical_digest(item)
            for item in blockers
        }
    )
    if blocker_ids != compact_target["blocker_ids"]:
        raise ValueError("raw blocker identities differ from compact projection")
    if _canonical_json_bytes(selected_action) != _canonical_json_bytes(
        compact_target["selected_action"]
    ):
        raise ValueError("raw selected action differs from compact projection")
    packet = raw_target["semantic_work_packet"]
    obligation = packet["typed_repair_obligation"]
    math_obligation = obligation["math_obligation"]
    label_scoped = packet["label_scoped_obligation"]
    return {
        "content_identity": _target_content_identity(raw_target),
        "blocker_records": _blocker_bindings(raw_target),
        "evidence_ref_records": _record_bindings(evidence_refs, "evidence_ref_id"),
        "source_ref_records": _record_bindings(source_refs, "source_ref_id"),
        "unresolved_assumption_records": _record_bindings(unresolved, "id"),
        "candidate_assumption_records": _record_bindings(candidates, "id"),
        "selected_action": [
            _record_binding(str(selected_action["action_id"]), selected_action)
        ],
        "label_scoped_obligation": [
            _record_binding(str(label_scoped["obligation_id"]), label_scoped)
        ],
        "typed_repair_obligation": [
            _record_binding(str(obligation["id"]), obligation)
        ],
        "math_obligation": [
            _record_binding(str(math_obligation["id"]), math_obligation)
        ],
        "source_span": [
            _record_binding(f"{packet['id']}#source_span", packet["source_span"])
        ],
        "target_text": [
            _record_binding(f"{packet['id']}#target", packet["target"])
        ],
    }


def _collection_map(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    target_indices: Sequence[int],
) -> dict[str, Any]:
    evidence_refs = _evidence_ref_entries(audit)
    source_refs = _source_ref_entries(audit)
    inventory = compact["reference_inventory"]
    if [item["ref"] for item in evidence_refs] != inventory["evidence_refs"]:
        raise ValueError("global evidence records differ from compact projection")
    if [item["evidence_ref_id"] for item in evidence_refs] != inventory[
        "evidence_ref_ids"
    ]:
        raise ValueError("global evidence identities differ from compact projection")
    if [item["source_ref_id"] for item in source_refs] != inventory[
        "source_ref_ids"
    ]:
        raise ValueError("global source identities differ from compact projection")
    targets: dict[str, Any] = {}
    for target_index in target_indices:
        target = compact["targets"][target_index]
        raw_target = audit["targets"][target_index]
        targets[target["target_id"]] = _target_record_collections(
            target,
            raw_target,
            result_id=str(compact["audit_result_id"]),
            source_identity=_normalized_source_identity(
                str(audit.get("tex_path") or ".")
            ),
        )
    return {
        "global": {
            "global_blocker_records": _blocker_bindings(audit),
            "global_evidence_ref_records": _record_bindings(
                evidence_refs, "evidence_ref_id"
            ),
            "global_source_ref_records": _record_bindings(
                source_refs, "source_ref_id"
            ),
        },
        "targets": targets,
    }


def _resolver_scope_descriptor(collections: Mapping[str, Any]) -> dict[str, Any]:
    global_values = collections.get("global")
    target_values = collections.get("targets")
    if not isinstance(global_values, Mapping) or set(global_values) != set(
        _GLOBAL_RESOLVER_COLLECTIONS
    ):
        raise ValueError("resolver global scope is not the closed collection set")
    if not isinstance(target_values, Mapping):
        raise ValueError("resolver target scope is not a mapping")
    scopes: list[dict[str, Any]] = []
    for collection in _GLOBAL_RESOLVER_COLLECTIONS:
        bindings = global_values[collection]
        scopes.append(
            {
                "scope_kind": "global",
                "target_id": None,
                "collection": collection,
                "record_count": len(bindings),
                "record_bindings": deepcopy(bindings),
            }
        )
    expected_target_keys = {"content_identity", *_TARGET_RESOLVER_COLLECTIONS}
    for target_id, per_target in target_values.items():
        if not isinstance(target_id, str) or not target_id:
            raise ValueError("resolver target scope has no target identity")
        if not isinstance(per_target, Mapping) or set(per_target) != expected_target_keys:
            raise ValueError("resolver target scope is not the closed collection set")
        for collection in _TARGET_RESOLVER_COLLECTIONS:
            bindings = per_target[collection]
            scopes.append(
                {
                    "scope_kind": "target",
                    "target_id": target_id,
                    "collection": collection,
                    "record_count": len(bindings),
                    "record_bindings": deepcopy(bindings),
                }
            )
    return {
        "schema_version": DOCUMENT_DERIVATION_RESOLVER_SCOPE_SCHEMA,
        "global_target_sentinel": None,
        "scopes": scopes,
    }


def _page_boundary(
    compact: Mapping[str, Any],
    target_indices: Sequence[int],
    *,
    page_index: int,
    previous_offset: int,
    next_offset: int,
    requested_target_limit: int,
) -> dict[str, Any]:
    return {
        "response_schema_version": DOCUMENT_DERIVATION_RESPONSE_SCHEMA,
        "artifact_schema_version": DOCUMENT_DERIVATION_ARTIFACT_SCHEMA,
        "compact_representation": "artifact_indexed",
        "byte_policy_version": DOCUMENT_DERIVATION_BYTE_POLICY,
        "canonical_limit": COMPACT_PAYLOAD_TARGET_BYTES,
        "transport_limit": PUBLIC_TRANSPORT_TARGET_BYTES,
        "requested_target_limit": requested_target_limit,
        "page_index": page_index,
        "previous_offset": previous_offset,
        "next_offset": next_offset,
        "target_ids": [
            compact["targets"][index]["target_id"] for index in target_indices
        ],
        "filter_id": compact["page"]["filter_id"],
    }


def _identity_digest(value: Any, prefix: str, field: str) -> bytes:
    if not isinstance(value, str) or not value.startswith(prefix):
        raise ValueError(f"{field} is not a {prefix} identity")
    suffix = value[len(prefix) :]
    if len(suffix) != 64 or suffix.lower() != suffix:
        raise ValueError(f"{field} digest length or case is invalid")
    try:
        return bytes.fromhex(suffix)
    except ValueError as exc:
        raise ValueError(f"{field} digest is not lowercase hexadecimal") from exc


def decode_document_derivation_cursor(cursor: str) -> dict[str, Any]:
    """Decode the strict v2 page capability; v1 JSON cursors require a restart."""
    if not isinstance(cursor, str) or not cursor or "=" in cursor:
        raise ValueError("page token must be nonempty unpadded base64url")
    try:
        raw = base64.b64decode(
            cursor + "=" * (-len(cursor) % 4),
            altchars=b"-_",
            validate=True,
        )
    except (binascii.Error, ValueError, TypeError) as exc:
        raise ValueError("page token is not strict base64url") from exc
    if len(raw) != _TOKEN_SIZE or raw[: len(_TOKEN_MAGIC)] != _TOKEN_MAGIC:
        if raw.startswith(b"{") and b"p07_document_derivation_cursor@1" in raw:
            raise ValueError(
                "Phase 07 target_cursor is unsupported; rerun the initial compact "
                "request to obtain a Phase 08 page_token"
            )
        raise ValueError("page token version or length is invalid")
    if base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=") != cursor:
        raise ValueError("page token is not canonical base64url")
    position = len(_TOKEN_MAGIC)
    policy, requested_limit, page_index, previous_offset, next_offset = struct.unpack(
        "!BBHHH", raw[position : position + 8]
    )
    position += 8
    chunks = [
        raw[position + index * 32 : position + (index + 1) * 32]
        for index in range(_TOKEN_DIGEST_COUNT)
    ]
    payload = raw[:-32]
    if policy != _TOKEN_BYTE_POLICY_CODE or hashlib.sha256(payload).digest() != chunks[-1]:
        raise ValueError("page token policy or checksum is invalid")
    if not MIN_TARGET_LIMIT <= requested_limit <= MAX_TARGET_LIMIT:
        raise ValueError("page token requested target limit is invalid")
    if not previous_offset < next_offset <= 65_535 or page_index > previous_offset:
        raise ValueError("page token offsets are invalid")
    return {
        "schema_version": DOCUMENT_DERIVATION_CURSOR_SCHEMA,
        "selector_schema_version": DOCUMENT_DERIVATION_SELECTOR_SCHEMA,
        "audit_result_id": "audit_" + chunks[0].hex(),
        "audit_request_id": "request_" + chunks[1].hex(),
        "artifact_sha256": chunks[2].hex(),
        "filter_id": "filter_" + chunks[3].hex(),
        "byte_policy_version": DOCUMENT_DERIVATION_BYTE_POLICY,
        "requested_target_limit": requested_limit,
        "page_index": page_index,
        "previous_offset": previous_offset,
        "next_offset": next_offset,
        "page_boundary_digest": chunks[4].hex(),
        "resolver_scope_digest": chunks[5].hex(),
        "checksum": chunks[6].hex(),
    }


def _encode_document_derivation_cursor(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    target_indices: Sequence[int],
    *,
    page_index: int,
    previous_offset: int,
    next_offset: int,
    requested_target_limit: int,
) -> str:
    if not MIN_TARGET_LIMIT <= requested_target_limit <= MAX_TARGET_LIMIT:
        raise ValueError("page token requested target limit is invalid")
    if any(
        value > 65_535
        for value in (page_index, previous_offset, next_offset)
    ):
        raise ValueError("page token index exceeds the closed two-byte range")
    boundary = _page_boundary(
        compact,
        target_indices,
        page_index=page_index,
        previous_offset=previous_offset,
        next_offset=next_offset,
        requested_target_limit=requested_target_limit,
    )
    scope = _resolver_scope_descriptor(_collection_map(compact, audit, target_indices))
    payload = b"".join(
        [
            _TOKEN_MAGIC,
            struct.pack(
                "!BBHHH",
                _TOKEN_BYTE_POLICY_CODE,
                requested_target_limit,
                page_index,
                previous_offset,
                next_offset,
            ),
            _identity_digest(compact["audit_result_id"], "audit_", "audit_result_id"),
            _identity_digest(compact["audit_request_id"], "request_", "audit_request_id"),
            bytes.fromhex(compact["artifact"]["sha256"]),
            _identity_digest(compact["page"]["filter_id"], "filter_", "filter_id"),
            bytes.fromhex(_canonical_digest(boundary)),
            bytes.fromhex(_canonical_digest(scope)),
        ]
    )
    raw = payload + hashlib.sha256(payload).digest()
    token = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    if len(raw) != 236 or len(token) != 315:
        raise ValueError("page token fixed-width contract drift")
    if decode_document_derivation_cursor(token)["artifact_sha256"] != compact[
        "artifact"
    ]["sha256"]:
        raise ValueError("page token failed artifact round trip")
    return token


def _artifact_path(root: Path, result_id: str, request_id: str) -> Path:
    if not re.fullmatch(r"audit_[0-9a-f]{64}", result_id):
        raise ValueError("audit result identity is invalid")
    if not re.fullmatch(r"request_[0-9a-f]{64}", request_id):
        raise ValueError("audit request identity is invalid")
    return root / "document-derivation" / result_id / request_id / "detailed.json"


def _safe_artifact_root(root_value: str | Path, *, create: bool) -> Path:
    root = Path(root_value).expanduser()
    if root.exists() and root.is_symlink():
        raise ValueError("artifact_root must not be a symlink")
    if create:
        root.mkdir(parents=True, exist_ok=True)
    if not root.exists() or not root.is_dir():
        raise ValueError("artifact_root must be an existing directory")
    if root.is_symlink():
        raise ValueError("artifact_root must not be a symlink")
    return root.resolve(strict=True)


def _safe_child_directory(root: Path, name: str) -> Path:
    if not name or name in {".", ".."} or "/" in name or "\\" in name:
        raise ValueError("artifact directory name is invalid")
    child = root / name
    if child.exists() and child.is_symlink():
        raise ValueError("artifact directory must not be a symlink")
    child.mkdir(exist_ok=True)
    resolved = child.resolve(strict=True)
    if resolved == root or root not in resolved.parents:
        raise ValueError("artifact directory escapes artifact_root")
    return resolved


def _assert_artifact_path_has_no_symlink(root: Path, destination: Path) -> None:
    try:
        relative = destination.relative_to(root)
    except ValueError as exc:
        raise ValueError("detailed artifact path escapes artifact_root") from exc
    current = root
    for part in relative.parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("detailed artifact path must not contain symlinks")


def _artifact_record(
    audit: Mapping[str, Any],
    audit_request: Mapping[str, Any],
) -> dict[str, Any]:
    stripped = _without_presentation_fields(audit)
    result_id = audit_result_id(stripped)
    return {
        "schema_version": DOCUMENT_DERIVATION_ARTIFACT_SCHEMA,
        "audit_result_id": result_id,
        "audit_request_id": audit_request["audit_request_id"],
        "audit_request": deepcopy(dict(audit_request)),
        "audit": stripped,
        "authority": "local_byte_identity_only",
        "non_claim": "This artifact is a diagnostic audit record, not a mathematical certificate or publication authority.",
    }


def _persist_detailed_artifact(
    audit: Mapping[str, Any],
    audit_request: Mapping[str, Any],
    artifact_root: str | Path,
) -> dict[str, Any]:
    root = _safe_artifact_root(artifact_root, create=True)
    record = _artifact_record(audit, audit_request)
    payload = _canonical_json_bytes(record)
    result_id = str(record["audit_result_id"])
    request_id = str(record["audit_request_id"])
    artifact_kind_root = _safe_child_directory(root, "document-derivation")
    result_root = _safe_child_directory(artifact_kind_root, result_id)
    request_root = _safe_child_directory(result_root, request_id)
    destination = request_root / "detailed.json"
    _assert_artifact_path_has_no_symlink(root, destination)
    if root not in destination.resolve(strict=False).parents:
        raise ValueError("detailed artifact path escapes artifact_root")
    write_bytes_no_replace(destination, payload)
    digest = hashlib.sha256(payload).hexdigest()
    return {
        "state": "verified",
        "logical_uri": (
            f"mathdevmcp-artifact://document-derivation/{result_id}/{request_id}/detailed.json"
        ),
        "sha256": digest,
        "byte_count": len(payload),
        "media_type": "application/json",
        "schema_version": DOCUMENT_DERIVATION_ARTIFACT_SCHEMA,
        "authority": "local_byte_identity_only",
    }


def _load_verified_artifact_from_token(
    artifact_root: str | Path | None,
    page_token: str,
) -> tuple[Path, dict[str, Any], dict[str, Any], dict[str, Any]]:
    if artifact_root is None:
        raise ValueError("artifact_root is required with page token")
    token = decode_document_derivation_cursor(page_token)
    root = _safe_artifact_root(artifact_root, create=False)
    destination = _artifact_path(
        root,
        str(token["audit_result_id"]),
        str(token["audit_request_id"]),
    )
    _assert_artifact_path_has_no_symlink(root, destination)
    if not destination.is_file():
        raise ValueError("persisted detailed artifact is missing or unsafe")
    if root not in destination.resolve(strict=True).parents:
        raise ValueError("persisted detailed artifact escapes artifact_root")
    payload = destination.read_bytes()
    actual_sha256 = hashlib.sha256(payload).hexdigest()
    if actual_sha256 != token["artifact_sha256"]:
        raise ValueError("persisted detailed artifact digest mismatch")
    try:
        record = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("persisted detailed artifact is not valid JSON") from exc
    if not isinstance(record, dict) or _canonical_json_bytes(record) != payload:
        raise ValueError("persisted detailed artifact is not canonical")
    if record.get("schema_version") != DOCUMENT_DERIVATION_ARTIFACT_SCHEMA:
        raise ValueError("persisted detailed artifact schema mismatch")
    if (
        record.get("audit_result_id") != token["audit_result_id"]
        or record.get("audit_request_id") != token["audit_request_id"]
    ):
        raise ValueError("persisted detailed artifact token identity mismatch")
    audit_request = record.get("audit_request")
    if not isinstance(audit_request, dict):
        raise ValueError("persisted detailed artifact request is invalid")
    expected_request = deepcopy(audit_request)
    request_id = expected_request.pop("audit_request_id", None)
    if request_id != "request_" + _canonical_digest(expected_request):
        raise ValueError("persisted detailed artifact request identity mismatch")
    audit = record.get("audit")
    if not isinstance(audit, dict) or audit_result_id(audit) != token["audit_result_id"]:
        raise ValueError("persisted detailed artifact audit identity mismatch")
    expected_record = _artifact_record(audit, audit_request)
    if _canonical_json_bytes(record) != _canonical_json_bytes(expected_record):
        raise ValueError("persisted detailed artifact does not reconstruct exactly")
    artifact = {
        "state": "verified",
        "logical_uri": (
            "mathdevmcp-artifact://document-derivation/"
            f"{token['audit_result_id']}/{token['audit_request_id']}/detailed.json"
        ),
        "sha256": actual_sha256,
        "byte_count": len(payload),
        "media_type": "application/json",
        "schema_version": DOCUMENT_DERIVATION_ARTIFACT_SCHEMA,
        "authority": "local_byte_identity_only",
    }
    return root, audit, audit_request, artifact


def load_document_derivation_continuation(
    artifact_root: str | Path | None,
    target_cursor: str,
    audit_request: Mapping[str, Any],
) -> dict[str, Any]:
    """Load exact persisted audit bytes for a continuation without source access."""
    _, audit, stored_request, _ = _load_verified_artifact_from_token(
        artifact_root, target_cursor
    )
    cursor = decode_document_derivation_cursor(target_cursor)
    request_id = audit_request.get("audit_request_id")
    if (
        request_id != cursor["audit_request_id"]
        or _canonical_json_bytes(dict(audit_request))
        != _canonical_json_bytes(stored_request)
    ):
        raise ValueError("continuation audit request does not match the persisted audit")
    return audit


def _common_boundary(
    audit: Mapping[str, Any],
    audit_request: Mapping[str, Any],
    *,
    response_mode: str,
    artifact: Mapping[str, Any],
    page: Mapping[str, Any],
    artifact_root: str | Path | None,
) -> dict[str, Any]:
    result_id = audit_result_id(audit)
    unresolved = _collect_unresolved_assumptions(audit)
    candidate_assumptions = _collect_candidate_assumptions(audit)
    promotion = audit.get("promotion") if isinstance(audit.get("promotion"), Mapping) else {}
    raw_status = audit.get("status")
    if not isinstance(raw_status, str) or not raw_status:
        coverage = audit.get("coverage") if isinstance(audit.get("coverage"), Mapping) else {}
        raw_status = coverage.get("status")
    common = {
        "metadata": contract_metadata(DOCUMENT_DERIVATION_RESPONSE_CONTRACT),
        "response_schema_version": DOCUMENT_DERIVATION_RESPONSE_SCHEMA,
        "response_mode": response_mode,
        "response_status": "compiled",
        "authority": "diagnostic_presentation_only",
        "audit_result_id": result_id,
        "audit_request_id": audit_request["audit_request_id"],
        "audit_status": raw_status,
        "status": raw_status,
        "audit_status_source": "status" if audit.get("status") else "coverage.status",
        "source_ref": _logical_source_ref(result_id, str(audit_request["source_identity"])),
        "publication_mode": audit.get("publication_mode"),
        "promotion": deepcopy(dict(promotion)),
        "coverage": deepcopy(audit.get("coverage", {})),
        "failure_classifications": _collect_failure_classifications(audit),
        "veto_ids": _collect_veto_ids(audit),
        "unresolved_assumption_ids": sorted(str(item["id"]) for item in unresolved),
        "candidate_assumption_ids": sorted(
            {str(item["id"]) for item in candidate_assumptions}
        ),
        "action_decision_ids": _collect_action_decision_ids(audit),
        "reference_inventory": _reference_inventory(audit),
        "non_claims": _collect_non_claims(audit),
        "execution_summary": _execution_summary(audit),
        "artifact": deepcopy(dict(artifact)),
        "page": deepcopy(dict(page)),
        "completeness": {
            "global_veto_ids": "complete",
            "global_unresolved_assumption_ids": "complete",
            "global_candidate_assumption_ids": "complete",
            "global_action_decision_ids": "complete",
            "global_reference_inventory": "complete",
            "global_non_claims": "complete",
            "off_page_full_reference_records": (
                "verified_artifact" if artifact.get("state") == "verified" else "not_transport_resolvable"
            ),
            "boundary": "Pagination never removes global claim-boundary summaries.",
        },
        "output_references": [],
    }
    for key in ("output_md", "output_json"):
        value = audit.get(key)
        if isinstance(value, str) and value:
            common["output_references"].append(
                {
                    "kind": key,
                    "logical_uri": f"mathdevmcp-output://{result_id}/{key}/{Path(value).name}",
                    "state": "written_by_raw_audit",
                }
            )
    return _redact_transport(
        common,
        result_id=result_id,
        source_identity=str(audit_request["source_identity"]),
        artifact_root=artifact_root,
    )


def _compact_projection_source(
    audit: Mapping[str, Any],
    audit_request: Mapping[str, Any],
    artifact: Mapping[str, Any],
    artifact_root: str | Path,
) -> dict[str, Any]:
    targets = [item for item in audit.get("targets", []) if isinstance(item, Mapping)]
    compact_targets = [
        _compact_target(
            target,
            index=index,
            result_id=audit_result_id(audit),
            source_identity=str(audit_request["source_identity"]),
            artifact_root=artifact_root,
        )[0]
        for index, target in enumerate(targets)
    ]
    page = {
        "offset": 0,
        "limit": len(targets),
        "included_target_count": len(targets),
        "total_target_count": len(targets),
        "target_ids": [item["target_id"] for item in compact_targets],
        "filter_id": _filter_id(audit),
    }
    source = _common_boundary(
        audit,
        audit_request,
        response_mode="compact",
        artifact=artifact,
        page=page,
        artifact_root=artifact_root,
    )
    source["targets"] = compact_targets
    return source


def _page_identity_tables(targets: Sequence[Mapping[str, Any]]) -> dict[str, list[str]]:
    return {
        "blocker_ids": list(
            dict.fromkeys(value for target in targets for value in target["blocker_ids"])
        ),
        "evidence_refs": list(
            dict.fromkeys(
                item["ref"] for target in targets for item in target["evidence_refs"]
            )
        ),
        "source_ref_ids": list(
            dict.fromkeys(
                item["source_ref_id"]
                for target in targets
                for item in target["source_refs"]
            )
        ),
    }


_COMPACT_ID_PREFIXES = (
    "candidate_assumption_",
    "assumption_",
    "action_",
    "ledger_",
)


def _compact_opaque_id(value: str) -> str:
    for index, prefix in enumerate(_COMPACT_ID_PREFIXES):
        if value.startswith(prefix):
            suffix = value[len(prefix) :]
            if re.fullmatch(r"[0-9a-f]{64}", suffix):
                encoded = base64.urlsafe_b64encode(bytes.fromhex(suffix)).decode("ascii").rstrip("=")
                return f"{index}:{encoded}"
    return value


def _expand_opaque_id(value: str) -> str:
    match = re.fullmatch(r"([0-9]):([A-Za-z0-9_-]{43})", value)
    if match is None:
        return value
    index = int(match.group(1))
    if index >= len(_COMPACT_ID_PREFIXES):
        raise ValueError("opaque identity prefix index is invalid")
    try:
        digest = base64.urlsafe_b64decode(match.group(2) + "=").hex()
    except (binascii.Error, ValueError) as exc:
        raise ValueError("opaque identity digest is invalid base64url") from exc
    return _COMPACT_ID_PREFIXES[index] + digest


def _compact_opaque_ids(values: Sequence[str]) -> list[str]:
    return [_compact_opaque_id(str(value)) for value in values]


def _expand_opaque_ids(values: Sequence[str]) -> list[str]:
    return [_expand_opaque_id(str(value)) for value in values]


def _common_string_prefix(values: Sequence[str]) -> str:
    if not values:
        return ""
    prefix = os.path.commonprefix([str(value) for value in values])
    return prefix if len(prefix) >= 8 else ""


def _compact_source_evidence(raw_target: Mapping[str, Any]) -> dict[str, Any]:
    packet = raw_target.get("semantic_work_packet")
    if not isinstance(packet, Mapping):
        raise ValueError("stored audit target has no semantic work packet")
    role = packet.get("routing_role") if isinstance(packet.get("routing_role"), Mapping) else {}
    specialist = packet.get("specialist_execution") if isinstance(packet.get("specialist_execution"), Mapping) else {}
    specialist_result = specialist.get("result") if isinstance(specialist.get("result"), Mapping) else {}
    source_span = packet.get("source_span") if isinstance(packet.get("source_span"), Mapping) else {}
    normalized = packet.get("normalized_target") if isinstance(packet.get("normalized_target"), Mapping) else {}
    if normalized and normalized.get("display_text") != packet.get("target"):
        raise ValueError("normalized display text differs from the canonical target")
    compact_normalized = {
        key: deepcopy(value)
        for key, value in normalized.items()
        if key != "display_text"
    }
    return {
        "source": {
            key: deepcopy(source_span.get(key))
            for key in (
                "file",
                "label",
                "start_byte",
                "end_byte",
                "source_digest",
                "obligation_id",
                "obligation_digest",
            )
        },
        "target": packet.get("target"),
        "normalized_target": compact_normalized,
        "routing_role": {
            key: deepcopy(role.get(key))
            for key in (
                "status",
                "role",
                "authority",
                "routing_effect",
                "role_id",
                "role_digest",
            )
        },
        "specialist_execution": {
            "status": specialist.get("status"),
            "selected_tool": specialist.get("selected_tool"),
            "backend_environment": deepcopy(specialist.get("backend_environment", {})),
            "result": {
                "status": specialist_result.get("status"),
                "reason": specialist_result.get("reason"),
                "backend_attempt": deepcopy(specialist_result.get("backend_attempt")),
            },
        },
        "binding_ref": deepcopy(raw_target.get("document_evidence_binding_ref", {})),
        "boundary": {
            "claim_eligibility": raw_target.get("claim_eligibility", "ineligible"),
            "publication_enabled": raw_target.get("publication_enabled", False),
            "promotion_allowed": False,
        },
    }


def _project_indexed_target(
    compact: Mapping[str, Any],
    target: Mapping[str, Any],
    raw_target: Mapping[str, Any],
    tables: Mapping[str, list[str]],
    target_values: Mapping[str, Any],
) -> dict[str, Any]:
    selected_action = _selected_action(raw_target)
    if not isinstance(selected_action, Mapping):
        raise ValueError("stored audit target has no selected action")
    return {
        "target_id": target["target_id"],
        "label": target["label"],
        "row_id": target["row_id"],
        "row_index": target["row_index"],
        "location": target["location"],
        "content_identity": _target_content_identity(raw_target),
        "status": target["status"],
        "publication_mode": target["publication_mode"],
        "promotion_ref": "global",
        "failure_classification_indices": [
            compact["failure_classifications"].index(value)
            for value in target["failure_classifications"]
        ],
        "veto_indices": [
            compact["veto_ids"].index(value) for value in target["veto_ids"]
        ],
        "unresolved_assumption_indices": [
            compact["unresolved_assumption_ids"].index(item["identity"])
            for item in target_values["unresolved_assumption_records"]
        ],
        "candidate_assumption_indices": [
            compact["candidate_assumption_ids"].index(item["identity"])
            for item in target_values["candidate_assumption_records"]
        ],
        "unresolved_assumption_record_count": len(
            target_values["unresolved_assumption_records"]
        ),
        "candidate_assumption_record_count": len(
            target_values["candidate_assumption_records"]
        ),
        "blocker_record_count": len(target_values["blocker_records"]),
        "blocker_indices": [
            tables["blocker_ids"].index(value) for value in target["blocker_ids"]
        ],
        "evidence_ref_indices": [
            tables["evidence_refs"].index(item["ref"])
            for item in target["evidence_refs"]
        ],
        "source_ref_indices": [
            tables["source_ref_ids"].index(item["source_ref_id"])
            for item in target["source_refs"]
        ],
        "selected_action": _project_action(
            selected_action, list(compact["veto_ids"])
        ),
        "source_evidence": _compact_source_evidence(raw_target),
    }


def _finalize_compact_size(response: dict[str, Any]) -> None:
    response["canonical_byte_count"] = 0
    while True:
        sizes = document_derivation_public_surface_sizes(response)
        measured = sizes["canonical_response"]
        status = (
            "met"
            if _public_page_fits(sizes)
            else "exceeded_complete_boundary_preserved"
        )
        if (
            response["canonical_byte_count"] == measured
            and response["payload_guardrail"]["status"] == status
        ):
            return
        response["canonical_byte_count"] = measured
        response["payload_guardrail"]["status"] = status


def document_derivation_public_surface_sizes(
    response: Mapping[str, Any],
) -> dict[str, int]:
    """Measure the exact compact CLI/facade/FastMCP/stdio envelopes."""
    payload = deepcopy(dict(response))
    facade = {**payload, "ok": True}
    call_result = {
        "content": [
            {"type": "text", "text": DOCUMENT_DERIVATION_COMPATIBILITY_TEXT}
        ],
        "structuredContent": facade,
        "isError": False,
    }
    stdio = {"jsonrpc": "2.0", "id": 1, "result": call_result}
    sizes = {
        "canonical_response": len(_canonical_json_bytes(payload)),
        "cli_stdout": len(_canonical_json_bytes(payload) + b"\n"),
        "facade": len(_canonical_json_bytes(facade)),
        "call_tool_result": len(_canonical_json_bytes(call_result) + b"\n"),
        "stdio_jsonrpc_line": len(_canonical_json_bytes(stdio) + b"\n"),
    }
    page = response.get("page")
    if isinstance(page, Mapping) and isinstance(page.get("page_token"), str):
        sizes["page_token"] = len(page["page_token"])
    return sizes


def _public_page_fits(sizes: Mapping[str, int]) -> bool:
    return sizes["canonical_response"] <= COMPACT_PAYLOAD_TARGET_BYTES and all(
        sizes[surface] <= PUBLIC_TRANSPORT_TARGET_BYTES
        for surface in (
            "cli_stdout",
            "facade",
            "call_tool_result",
            "stdio_jsonrpc_line",
        )
    )


def _compile_artifact_indexed_page(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    *,
    page_index: int,
    previous_offset: int,
    target_count: int,
    requested_target_limit: int,
) -> dict[str, Any]:
    if target_count < 1:
        raise ValueError("artifact-indexed page must contain at least one target")
    target_indices = list(range(previous_offset, previous_offset + target_count))
    targets = [compact["targets"][index] for index in target_indices]
    raw_targets = [audit["targets"][index] for index in target_indices]
    collections = _collection_map(compact, audit, target_indices)
    tables = _page_identity_tables(targets)
    projections = [
        _project_indexed_target(
            compact,
            target,
            raw_target,
            tables,
            collections["targets"][target["target_id"]],
        )
        for target, raw_target in zip(targets, raw_targets, strict=True)
    ]
    next_offset = previous_offset + target_count
    page_token = _encode_document_derivation_cursor(
        compact,
        audit,
        target_indices,
        page_index=page_index,
        previous_offset=previous_offset,
        next_offset=next_offset,
        requested_target_limit=requested_target_limit,
    )
    global_values = collections["global"]
    response = {
        "metadata": deepcopy(compact["metadata"]),
        "response_schema_version": DOCUMENT_DERIVATION_RESPONSE_SCHEMA,
        "response_mode": "compact",
        "compact_representation": "artifact_indexed",
        "authority": compact["authority"],
        "audit_result_id": compact["audit_result_id"],
        "audit_request_id": compact["audit_request_id"],
        "response_status": compact["response_status"],
        "audit_status": compact["audit_status"],
        "status": compact["status"],
        "audit_status_source": compact["audit_status_source"],
        "source_ref": compact["source_ref"],
        "publication_mode": compact["publication_mode"],
        "promotion": deepcopy(compact["promotion"]),
        "coverage": deepcopy(compact["coverage"]),
        "failure_classifications": deepcopy(compact["failure_classifications"]),
        "veto_ids": _compact_opaque_ids(compact["veto_ids"]),
        "unresolved_assumption_ids": _compact_opaque_ids(compact["unresolved_assumption_ids"]),
        "candidate_assumption_ids": _compact_opaque_ids(compact["candidate_assumption_ids"]),
        "action_decision_ids": _compact_opaque_ids(compact["action_decision_ids"]),
        "opaque_id_prefixes": list(_COMPACT_ID_PREFIXES),
        "non_claims": deepcopy(compact["non_claims"]),
        "execution_summary": deepcopy(compact["execution_summary"]),
        "output_references": deepcopy(compact["output_references"]),
        "artifact": {
            "state": "verified",
            "schema_version": DOCUMENT_DERIVATION_ARTIFACT_SCHEMA,
            "sha256": compact["artifact"]["sha256"],
            "byte_count": compact["artifact"]["byte_count"],
            "authority": "local_byte_identity_only",
        },
        "record_inventory": {
            "global_blocker_record_count": len(
                global_values["global_blocker_records"]
            ),
            "global_evidence_ref_count": len(
                global_values["global_evidence_ref_records"]
            ),
            "global_source_ref_count": len(
                global_values["global_source_ref_records"]
            ),
            "resolution": "page_token",
        },
        "page_identity_tables": {
            **tables,
            "blocker_id_prefix": _common_string_prefix(tables["blocker_ids"]),
            "blocker_ids": [
                value[len(_common_string_prefix(tables["blocker_ids"])) :]
                for value in _compact_opaque_ids(tables["blocker_ids"])
            ],
        },
        "targets": projections,
        "page": {
            "page_index": page_index,
            "previous_offset": previous_offset,
            "next_offset": next_offset,
            "requested_limit": requested_target_limit,
            "effective_limit": target_count,
            "included_target_count": target_count,
            "total_target_count": len(compact["targets"]),
            "target_ids": [target["target_id"] for target in targets],
            "continuation_available": next_offset < len(compact["targets"]),
            "filter_id": compact["page"]["filter_id"],
            "byte_policy_version": DOCUMENT_DERIVATION_BYTE_POLICY,
            "page_token": page_token,
            "resolver_catalog": document_derivation_resolver_catalog(),
        },
        "completeness": {
            "global_boundary": "complete",
            "current_target_identities": "literal_page_tables",
            "global_and_full_records": "verified_page_token",
        },
        "payload_guardrail": {
            "canonical_target_bytes": COMPACT_PAYLOAD_TARGET_BYTES,
            "transport_target_bytes": PUBLIC_TRANSPORT_TARGET_BYTES,
            "status": "pending",
            "authority": "product_usability_only",
        },
    }
    _finalize_compact_size(response)
    for target, raw_target, projection in zip(
        targets, raw_targets, projections, strict=True
    ):
        selected = _selected_action(raw_target)
        expanded = expand_document_derivation_action(
            projection["selected_action"], compact["veto_ids"]
        )
        if _canonical_json_bytes(expanded) != _canonical_json_bytes(selected):
            raise ValueError("projected action does not reconstruct exactly")
        if projection["content_identity"] != _target_content_identity(raw_target):
            raise ValueError("content identity does not reconstruct exactly")
        if _checked_indices(
            projection["failure_classification_indices"],
            compact["failure_classifications"],
            field="failure_classification_indices",
            allow_duplicates=False,
        ) != target["failure_classifications"]:
            raise ValueError("failure classification indices do not reconstruct exactly")
        if _checked_indices(
            projection["veto_indices"],
            compact["veto_ids"],
            field="veto_indices",
            allow_duplicates=False,
        ) != target["veto_ids"]:
            raise ValueError("veto indices do not reconstruct exactly")
        if _checked_indices(
            projection["blocker_indices"],
            tables["blocker_ids"],
            field="blocker_indices",
            allow_duplicates=False,
        ) != target["blocker_ids"]:
            raise ValueError("blocker indices do not reconstruct exactly")
        if _checked_indices(
            projection["evidence_ref_indices"],
            tables["evidence_refs"],
            field="evidence_ref_indices",
            allow_duplicates=False,
        ) != [item["ref"] for item in target["evidence_refs"]]:
            raise ValueError("evidence indices do not reconstruct exactly")
        if _checked_indices(
            projection["source_ref_indices"],
            tables["source_ref_ids"],
            field="source_ref_indices",
            allow_duplicates=False,
        ) != [item["source_ref_id"] for item in target["source_refs"]]:
            raise ValueError("source indices do not reconstruct exactly")
        target_values = collections["targets"][target["target_id"]]
        if _checked_indices(
            projection["unresolved_assumption_indices"],
            compact["unresolved_assumption_ids"],
            field="unresolved_assumption_indices",
            allow_duplicates=True,
        ) != [
            item["identity"]
            for item in target_values["unresolved_assumption_records"]
        ]:
            raise ValueError("unresolved assumption indices do not reconstruct exactly")
        if _checked_indices(
            projection["candidate_assumption_indices"],
            compact["candidate_assumption_ids"],
            field="candidate_assumption_indices",
            allow_duplicates=True,
        ) != [
            item["identity"]
            for item in target_values["candidate_assumption_records"]
        ]:
            raise ValueError("candidate assumption indices do not reconstruct exactly")
        for count_field, collection in (
            ("unresolved_assumption_record_count", "unresolved_assumption_records"),
            ("candidate_assumption_record_count", "candidate_assumption_records"),
            ("blocker_record_count", "blocker_records"),
        ):
            if projection[count_field] != len(target_values[collection]):
                raise ValueError(f"{count_field} does not reconstruct exactly")
    return response


def _longest_prefix_page(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    *,
    page_index: int,
    previous_offset: int,
    requested_target_limit: int,
) -> tuple[dict[str, Any], dict[str, int]]:
    remaining = len(compact["targets"]) - previous_offset
    maximum = min(requested_target_limit, remaining)
    selected: tuple[dict[str, Any], dict[str, int]] | None = None
    for target_count in range(1, maximum + 1):
        response = _compile_artifact_indexed_page(
            compact,
            audit,
            page_index=page_index,
            previous_offset=previous_offset,
            target_count=target_count,
            requested_target_limit=requested_target_limit,
        )
        sizes = document_derivation_public_surface_sizes(response)
        if not _public_page_fits(sizes):
            break
        selected = response, sizes
    if selected is not None:
        return selected
    response = _compile_artifact_indexed_page(
        compact,
        audit,
        page_index=page_index,
        previous_offset=previous_offset,
        target_count=1,
        requested_target_limit=requested_target_limit,
    )
    return response, document_derivation_public_surface_sizes(response)


def _validated_page_from_token(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    token: str,
    requested_target_limit: int,
) -> dict[str, Any]:
    decoded = decode_document_derivation_cursor(token)
    for field, expected in (
        ("audit_result_id", compact["audit_result_id"]),
        ("audit_request_id", compact["audit_request_id"]),
        ("artifact_sha256", compact["artifact"]["sha256"]),
        ("filter_id", compact["page"]["filter_id"]),
        ("requested_target_limit", requested_target_limit),
    ):
        if decoded[field] != expected:
            raise ValueError(f"page token {field} mismatch")
    page_index = 0
    offset = 0
    while offset < len(compact["targets"]):
        page, _ = _longest_prefix_page(
            compact,
            audit,
            page_index=page_index,
            previous_offset=offset,
            requested_target_limit=requested_target_limit,
        )
        if page_index == decoded["page_index"]:
            if page["page"]["page_token"] != token:
                raise ValueError("page token is not an exact greedy page boundary")
            return page
        offset = int(page["page"]["next_offset"])
        page_index += 1
    raise ValueError("page token page index is outside the greedy partition")


def _page_after_validated_token(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    token: str,
    requested_target_limit: int,
) -> tuple[int, int]:
    page = _validated_page_from_token(
        compact, audit, token, requested_target_limit
    )
    next_offset = int(page["page"]["next_offset"])
    if next_offset >= len(compact["targets"]):
        raise ValueError("page token has no continuation target")
    return int(page["page"]["page_index"]) + 1, next_offset


def _compile_inline_complete(
    audit: Mapping[str, Any],
    audit_request: Mapping[str, Any],
    artifact: Mapping[str, Any],
    *,
    requested_target_limit: int,
) -> dict[str, Any]:
    raw_targets = [
        item for item in audit.get("targets", []) if isinstance(item, Mapping)
    ]
    result_id = audit_result_id(audit)
    compact_targets: list[dict[str, Any]] = []
    for index, raw_target in enumerate(raw_targets):
        compact, _ = _compact_target(
            raw_target,
            index=index,
            result_id=result_id,
            source_identity=str(audit_request["source_identity"]),
            artifact_root=None,
        )
        compact["raw_record_sha256"] = _canonical_digest(raw_target)
        compact["record"] = _redact_transport(
            raw_target,
            result_id=result_id,
            source_identity=str(audit_request["source_identity"]),
            artifact_root=None,
        )
        compact["reference_resolution"] = "inline_complete_record"
        compact_targets.append(compact)
    page = {
        "page_index": 0,
        "previous_offset": 0,
        "next_offset": len(compact_targets),
        "requested_limit": requested_target_limit,
        "effective_limit": len(compact_targets),
        "included_target_count": len(compact_targets),
        "total_target_count": len(compact_targets),
        "target_ids": [item["target_id"] for item in compact_targets],
        "continuation_available": False,
        "filter_id": _filter_id(audit),
        "byte_policy_version": DOCUMENT_DERIVATION_BYTE_POLICY,
        "page_token": None,
    }
    response = _common_boundary(
        audit,
        audit_request,
        response_mode="compact",
        artifact=artifact,
        page=page,
        artifact_root=None,
    )
    response["compact_representation"] = "inline_complete"
    response["targets"] = compact_targets
    response["record_inventory"] = {
        "global_blocker_record_count": len(_raw_blocker_records(audit)),
        "global_evidence_ref_count": len(_evidence_ref_entries(audit)),
        "global_source_ref_count": len(_source_ref_entries(audit)),
        "target_record_count": len(compact_targets),
        "resolution": "inline_complete",
    }
    response["blocker_catalog"] = _blocker_catalog(
        [
            (_target_id(target, index), _blocker_records(target))
            for index, target in enumerate(raw_targets)
        ],
        result_id=result_id,
        source_identity=str(audit_request["source_identity"]),
        artifact_root=None,
    )
    response["completeness"] = {
        "global_boundary": "complete",
        "current_target_identities": "inline_complete_records",
        "global_and_full_records": "inline_complete",
        "global_veto_ids": "complete",
        "global_unresolved_assumption_ids": "complete",
        "global_candidate_assumption_ids": "complete",
        "global_action_decision_ids": "complete",
        "global_reference_inventory": "complete",
        "global_non_claims": "complete",
        "off_page_full_reference_records": "inline_complete",
        "boundary": "No target is omitted when artifact persistence is absent.",
    }
    response["payload_guardrail"] = {
        "canonical_target_bytes": COMPACT_PAYLOAD_TARGET_BYTES,
        "transport_target_bytes": PUBLIC_TRANSPORT_TARGET_BYTES,
        "status": "pending",
        "authority": "product_usability_only",
    }
    _finalize_compact_size(response)
    return response


def _resolver_record(
    identity: str,
    record: Any,
    *,
    audit: Mapping[str, Any],
    artifact_root: Path,
) -> dict[str, Any]:
    return {
        "identity": identity,
        "raw_record_sha256": _canonical_digest(record),
        "record": _redact_transport(
            record,
            result_id=audit_result_id(audit),
            source_identity=str(audit.get("tex_path") or "."),
            artifact_root=artifact_root,
        ),
    }


def _resolver_collections_for_target(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    target_index: int,
    artifact_root: Path,
) -> dict[tuple[str | None, str], list[dict[str, Any]]]:
    target = audit["targets"][target_index]
    compact_target = compact["targets"][target_index]
    selected_action = _selected_action(target)
    if not isinstance(selected_action, Mapping):
        raise ValueError("stored audit target has no selected action")
    packet = target.get("semantic_work_packet")
    if not isinstance(packet, Mapping):
        raise ValueError("stored audit target has no semantic work packet")
    label_scoped = packet["label_scoped_obligation"]
    obligation = packet["typed_repair_obligation"]
    math_obligation = obligation["math_obligation"]

    def record(identity: str, value: Any) -> dict[str, Any]:
        return _resolver_record(
            identity, value, audit=audit, artifact_root=artifact_root
        )

    return {
        (None, "global_blocker_records"): [
            record(
                str(item.get("id", "")) or "blocker_" + _canonical_digest(item),
                item,
            )
            for item in _raw_blocker_records(audit)
        ],
        (None, "global_evidence_ref_records"): [
            record(item["evidence_ref_id"], item)
            for item in _evidence_ref_entries(audit)
        ],
        (None, "global_source_ref_records"): [
            record(item["source_ref_id"], item) for item in _source_ref_entries(audit)
        ],
        (compact_target["target_id"], "blocker_records"): [
            record(
                str(item.get("id", "")) or "blocker_" + _canonical_digest(item),
                item,
            )
            for item in _raw_blocker_records(target)
        ],
        (compact_target["target_id"], "evidence_ref_records"): [
            record(item["evidence_ref_id"], item)
            for item in _evidence_ref_entries(target)
        ],
        (compact_target["target_id"], "source_ref_records"): [
            record(item["source_ref_id"], item)
            for item in _source_ref_entries(target)
        ],
        (compact_target["target_id"], "unresolved_assumption_records"): [
            record(item["id"], item)
            for item in _collect_unresolved_assumptions(target)
        ],
        (compact_target["target_id"], "candidate_assumption_records"): [
            record(item["id"], item)
            for item in _collect_candidate_assumptions(target)
        ],
        (compact_target["target_id"], "selected_action"): [
            record(str(selected_action["action_id"]), selected_action)
        ],
        (compact_target["target_id"], "label_scoped_obligation"): [
            record(str(label_scoped["obligation_id"]), label_scoped)
        ],
        (compact_target["target_id"], "typed_repair_obligation"): [
            record(str(obligation["id"]), obligation)
        ],
        (compact_target["target_id"], "math_obligation"): [
            record(str(math_obligation["id"]), math_obligation)
        ],
        (compact_target["target_id"], "source_span"): [
            record(f"{packet['id']}#source_span", packet["source_span"])
        ],
        (compact_target["target_id"], "target_text"): [
            record(f"{packet['id']}#target", packet["target"])
        ],
    }


def _resolver_page_payload(
    compact: Mapping[str, Any],
    *,
    page_index: int,
    target_id: str | None,
    collection: str,
    offset: int,
    limit: int,
    records: Sequence[dict[str, Any]],
    resolver_scope_digest: str,
) -> tuple[dict[str, Any], dict[str, int]]:
    if not records:
        if offset != 0:
            raise ValueError("resolver offset is outside the empty collection")
        response = {
            "schema_version": DOCUMENT_DERIVATION_RECORD_PAGE_SCHEMA,
            "authority": "diagnostic_presentation_only",
            "audit_result_id": compact["audit_result_id"],
            "audit_request_id": compact["audit_request_id"],
            "artifact": {
                "state": "verified",
                "schema_version": DOCUMENT_DERIVATION_ARTIFACT_SCHEMA,
                "sha256": compact["artifact"]["sha256"],
                "byte_count": compact["artifact"]["byte_count"],
            },
            "page_index": page_index,
            "target_id": target_id,
            "collection": collection,
            "offset": 0,
            "limit": limit,
            "total_record_count": 0,
            "returned_record_count": 0,
            "records": [],
            "next_offset": None,
            "resolver_scope_digest": resolver_scope_digest,
            "payload_guardrail": {
                "transport_target_bytes": PUBLIC_TRANSPORT_TARGET_BYTES,
                "status": "met",
                "authority": "product_usability_only",
            },
            "non_claim": (
                "Resolved records are evidence navigation, not proof or publication "
                "authority."
            ),
        }
        return response, document_derivation_public_surface_sizes(response)
    if offset < 0 or offset >= len(records):
        raise ValueError("resolver offset is outside the nonempty collection")
    selected: list[dict[str, Any]] = []
    response: dict[str, Any] = {}
    sizes: dict[str, int] = {}
    for item in records[offset : offset + limit]:
        candidate = [*selected, item]
        next_offset = offset + len(candidate)
        response = {
            "schema_version": DOCUMENT_DERIVATION_RECORD_PAGE_SCHEMA,
            "authority": "diagnostic_presentation_only",
            "audit_result_id": compact["audit_result_id"],
            "audit_request_id": compact["audit_request_id"],
            "artifact": {
                "state": "verified",
                "schema_version": DOCUMENT_DERIVATION_ARTIFACT_SCHEMA,
                "sha256": compact["artifact"]["sha256"],
                "byte_count": compact["artifact"]["byte_count"],
            },
            "page_index": page_index,
            "target_id": target_id,
            "collection": collection,
            "offset": offset,
            "limit": limit,
            "total_record_count": len(records),
            "returned_record_count": len(candidate),
            "records": candidate,
            "next_offset": next_offset if next_offset < len(records) else None,
            "resolver_scope_digest": resolver_scope_digest,
            "payload_guardrail": {
                "transport_target_bytes": PUBLIC_TRANSPORT_TARGET_BYTES,
                "status": "met",
                "authority": "product_usability_only",
            },
            "non_claim": (
                "Resolved records are evidence navigation, not proof or publication "
                "authority."
            ),
        }
        sizes = document_derivation_public_surface_sizes(response)
        if any(
            sizes[key] > PUBLIC_TRANSPORT_TARGET_BYTES
            for key in (
                "cli_stdout",
                "facade",
                "call_tool_result",
                "stdio_jsonrpc_line",
            )
        ):
            if not selected:
                response["payload_guardrail"]["status"] = (
                    "exceeded_complete_record_preserved"
                )
                return response, document_derivation_public_surface_sizes(response)
            break
        selected = candidate
    if not selected:
        raise ValueError("resolver did not select a complete record")
    if len(response["records"]) != len(selected):
        next_offset = offset + len(selected)
        response["records"] = selected
        response["returned_record_count"] = len(selected)
        response["next_offset"] = (
            next_offset if next_offset < len(records) else None
        )
        sizes = document_derivation_public_surface_sizes(response)
    return response, sizes


def resolve_document_derivation_records(
    page_token: str,
    collection: str,
    *,
    artifact_root: str | Path,
    target_id: str | None = None,
    offset: int = 0,
    limit: int = 100,
) -> dict[str, Any]:
    """Resolve one exact raw-record collection authorized by a v2 page token."""
    if not isinstance(page_token, str) or not page_token:
        raise ValueError("page_token must be a non-empty string")
    if not isinstance(collection, str) or not collection:
        raise ValueError("collection must be a non-empty string")
    valid_collections = {*_GLOBAL_RESOLVER_COLLECTIONS, *_TARGET_RESOLVER_COLLECTIONS}
    if collection not in valid_collections:
        raise ValueError(
            "collection must be one of: " + ", ".join(sorted(valid_collections))
        )
    try:
        offset_value = int(offset)
        limit_value = int(limit)
    except (TypeError, ValueError) as exc:
        raise ValueError("resolver offset and limit must be integers") from exc
    if offset_value < 0:
        raise ValueError("resolver offset must be non-negative")
    if not MIN_TARGET_LIMIT <= limit_value <= MAX_TARGET_LIMIT:
        raise ValueError(
            f"resolver limit must be between {MIN_TARGET_LIMIT} and {MAX_TARGET_LIMIT}"
        )
    root, audit, audit_request, artifact = _load_verified_artifact_from_token(
        artifact_root, page_token
    )
    compact = _compact_projection_source(audit, audit_request, artifact, root)
    decoded = decode_document_derivation_cursor(page_token)
    page = _validated_page_from_token(
        compact,
        audit,
        page_token,
        int(decoded["requested_target_limit"]),
    )
    previous_offset = int(page["page"]["previous_offset"])
    next_offset = int(page["page"]["next_offset"])
    target_indices = list(range(previous_offset, next_offset))
    bindings = _collection_map(compact, audit, target_indices)
    scope_descriptor = _resolver_scope_descriptor(bindings)
    scope_digest = _canonical_digest(scope_descriptor)
    if scope_digest != decoded["resolver_scope_digest"]:
        raise ValueError("page token resolver scope digest mismatch")
    allowed_pairs = {
        (entry["target_id"], entry["collection"])
        for entry in scope_descriptor["scopes"]
    }
    pair = (target_id, collection)
    if pair not in allowed_pairs:
        raise ValueError(
            "target_id and collection are outside the page token scope; "
            f"global collections: {', '.join(_GLOBAL_RESOLVER_COLLECTIONS)}; "
            f"target collections: {', '.join(_TARGET_RESOLVER_COLLECTIONS)}"
        )
    collections: dict[tuple[str | None, str], list[dict[str, Any]]] = {}
    for position, target_index in enumerate(target_indices):
        for key, records in _resolver_collections_for_target(
            compact, audit, target_index, root
        ).items():
            if key[0] is None and position > 0:
                continue
            collections[key] = records
    records = collections[pair]
    expected_scope = next(
        entry
        for entry in scope_descriptor["scopes"]
        if (entry["target_id"], entry["collection"]) == pair
    )
    actual_bindings = [
        {
            "identity": item["identity"],
            "raw_record_sha256": item["raw_record_sha256"],
        }
        for item in records
    ]
    if _canonical_json_bytes(actual_bindings) != _canonical_json_bytes(
        expected_scope["record_bindings"]
    ):
        raise ValueError("resolver records do not match the page token scope")
    response, _ = _resolver_page_payload(
        compact,
        page_index=int(page["page"]["page_index"]),
        target_id=target_id,
        collection=collection,
        offset=offset_value,
        limit=limit_value,
        records=records,
        resolver_scope_digest=scope_digest,
    )
    serialized = _canonical_json_bytes(response).decode("utf-8")
    if _ABSOLUTE_PATH_FRAGMENT.search(serialized):
        raise ValueError("resolver response contains an absolute local path")
    return response


def _artifact_indexed_validation_errors(
    audit: Mapping[str, Any],
    response: Mapping[str, Any],
) -> list[str]:
    errors: list[str] = []
    page = response.get("page")
    artifact = response.get("artifact")
    tables = response.get("page_identity_tables")
    projections = response.get("targets")
    inventory = response.get("record_inventory")
    if not isinstance(page, Mapping):
        return ["artifact-indexed page is invalid"]
    if not isinstance(artifact, Mapping):
        return ["artifact-indexed artifact binding is invalid"]
    if not isinstance(tables, Mapping):
        return ["artifact-indexed page identity tables are invalid"]
    if not isinstance(projections, list):
        return ["artifact-indexed targets are invalid"]
    if not isinstance(inventory, Mapping):
        return ["artifact-indexed record inventory is invalid"]
    if response.get("opaque_id_prefixes") != list(_COMPACT_ID_PREFIXES):
        errors.append("artifact-indexed opaque identity prefix registry mismatch")
    expanded_tables = deepcopy(dict(tables))
    try:
        blocker_prefix = tables.get("blocker_id_prefix", "")
        if not isinstance(blocker_prefix, str):
            raise ValueError("blocker identity prefix is not a string")
        expanded_tables.pop("blocker_id_prefix", None)
        expanded_tables["blocker_ids"] = _expand_opaque_ids(
            [blocker_prefix + str(item) for item in tables.get("blocker_ids", [])]
        )
    except ValueError as exc:
        errors.append(f"artifact-indexed blocker identity expansion failed: {exc}")
    tables = expanded_tables
    if (
        artifact.get("state") != "verified"
        or artifact.get("schema_version") != DOCUMENT_DERIVATION_ARTIFACT_SCHEMA
        or re.fullmatch(r"[0-9a-f]{64}", str(artifact.get("sha256", ""))) is None
        or not isinstance(artifact.get("byte_count"), int)
        or isinstance(artifact.get("byte_count"), bool)
        or int(artifact["byte_count"]) <= 0
    ):
        errors.append("artifact-indexed artifact binding is not verified")
    integer_fields = (
        "page_index",
        "previous_offset",
        "next_offset",
        "requested_limit",
        "effective_limit",
        "included_target_count",
        "total_target_count",
    )
    if any(
        not isinstance(page.get(field), int) or isinstance(page.get(field), bool)
        for field in integer_fields
    ):
        return [*errors, "artifact-indexed page integers are invalid"]
    page_index = int(page["page_index"])
    previous_offset = int(page["previous_offset"])
    next_offset = int(page["next_offset"])
    requested_limit = int(page["requested_limit"])
    raw_targets = [
        item for item in audit.get("targets", []) if isinstance(item, Mapping)
    ]
    if (
        page_index < 0
        or previous_offset < 0
        or not previous_offset < next_offset <= len(raw_targets)
        or not MIN_TARGET_LIMIT <= requested_limit <= MAX_TARGET_LIMIT
    ):
        return [*errors, "artifact-indexed page boundary is invalid"]
    expected_compact_targets = [
        _compact_target(
            target,
            index=index,
            result_id=audit_result_id(audit),
            source_identity=_normalized_source_identity(
                str(audit.get("tex_path") or ".")
            ),
            artifact_root=None,
        )[0]
        for index, target in enumerate(raw_targets)
    ]
    expected_targets = expected_compact_targets[previous_offset:next_offset]
    expected_target_ids = [target["target_id"] for target in expected_targets]
    target_count = len(expected_targets)
    if page.get("target_ids") != expected_target_ids:
        errors.append("artifact-indexed page target IDs differ from audit order")
    if (
        page.get("effective_limit") != target_count
        or page.get("included_target_count") != target_count
        or page.get("total_target_count") != len(raw_targets)
        or page.get("continuation_available") is not (next_offset < len(raw_targets))
        or page.get("filter_id") != _filter_id(audit)
        or page.get("byte_policy_version") != DOCUMENT_DERIVATION_BYTE_POLICY
    ):
        errors.append("artifact-indexed page metadata mismatch")
    expected_tables = _page_identity_tables(expected_targets)
    if _canonical_json_bytes(tables) != _canonical_json_bytes(expected_tables):
        errors.append("artifact-indexed page identity tables mismatch")
    if len(projections) != target_count:
        errors.append("artifact-indexed target count mismatch")
    else:
        compact = {
            "audit_result_id": audit_result_id(audit),
            "audit_request_id": response.get("audit_request_id"),
            "artifact": deepcopy(dict(artifact)),
            "page": {"filter_id": _filter_id(audit)},
            "targets": expected_compact_targets,
            "reference_inventory": _reference_inventory(audit),
            "failure_classifications": _collect_failure_classifications(audit),
            "veto_ids": _collect_veto_ids(audit),
            "unresolved_assumption_ids": sorted(
                str(item["id"]) for item in _collect_unresolved_assumptions(audit)
            ),
            "candidate_assumption_ids": sorted(
                {str(item["id"]) for item in _collect_candidate_assumptions(audit)}
            ),
        }
        target_indices = list(range(previous_offset, next_offset))
        try:
            collections = _collection_map(compact, audit, target_indices)
        except (KeyError, TypeError, ValueError) as exc:
            errors.append(f"artifact-indexed collection reconstruction failed: {exc}")
            collections = None
        for relative_index, (expected, raw_target, projection) in enumerate(
            zip(
                expected_targets,
                raw_targets[previous_offset:next_offset],
                projections,
                strict=True,
            )
        ):
            if not isinstance(projection, Mapping):
                errors.append(f"artifact-indexed target {relative_index} is invalid")
                continue
            scalar_fields = (
                "target_id",
                "label",
                "row_id",
                "row_index",
                "location",
                "status",
                "publication_mode",
            )
            if any(projection.get(field) != expected.get(field) for field in scalar_fields):
                errors.append(f"artifact-indexed target {relative_index} scalar mismatch")
            try:
                if _canonical_json_bytes(projection.get("source_evidence")) != _canonical_json_bytes(
                    _compact_source_evidence(raw_target)
                ):
                    errors.append(
                        f"artifact-indexed target {relative_index} source evidence mismatch"
                    )
                if projection.get("content_identity") != _target_content_identity(raw_target):
                    errors.append(
                        f"artifact-indexed target {relative_index} content identity mismatch"
                    )
                selected = _selected_action(raw_target)
                if not isinstance(selected, Mapping) or _canonical_json_bytes(
                    expand_document_derivation_action(
                        projection.get("selected_action", {}),
                        compact["veto_ids"],
                    )
                ) != _canonical_json_bytes(selected):
                    errors.append(
                        f"artifact-indexed target {relative_index} action mismatch"
                    )
                if _checked_indices(
                    projection.get("failure_classification_indices", []),
                    compact["failure_classifications"],
                    field="failure_classification_indices",
                    allow_duplicates=False,
                ) != expected["failure_classifications"]:
                    errors.append(
                        f"artifact-indexed target {relative_index} failure membership mismatch"
                    )
                if _checked_indices(
                    projection.get("veto_indices", []),
                    compact["veto_ids"],
                    field="veto_indices",
                    allow_duplicates=False,
                ) != expected["veto_ids"]:
                    errors.append(
                        f"artifact-indexed target {relative_index} veto membership mismatch"
                    )
                if _checked_indices(
                    projection.get("blocker_indices", []),
                    expected_tables["blocker_ids"],
                    field="blocker_indices",
                    allow_duplicates=False,
                ) != expected["blocker_ids"]:
                    errors.append(
                        f"artifact-indexed target {relative_index} blocker membership mismatch"
                    )
                if _checked_indices(
                    projection.get("evidence_ref_indices", []),
                    expected_tables["evidence_refs"],
                    field="evidence_ref_indices",
                    allow_duplicates=False,
                ) != [item["ref"] for item in expected["evidence_refs"]]:
                    errors.append(
                        f"artifact-indexed target {relative_index} evidence membership mismatch"
                    )
                if _checked_indices(
                    projection.get("source_ref_indices", []),
                    expected_tables["source_ref_ids"],
                    field="source_ref_indices",
                    allow_duplicates=False,
                ) != [item["source_ref_id"] for item in expected["source_refs"]]:
                    errors.append(
                        f"artifact-indexed target {relative_index} source membership mismatch"
                    )
                if collections is not None:
                    values = collections["targets"][expected["target_id"]]
                    if _checked_indices(
                        projection.get("unresolved_assumption_indices", []),
                        compact["unresolved_assumption_ids"],
                        field="unresolved_assumption_indices",
                        allow_duplicates=True,
                    ) != [
                        item["identity"]
                        for item in values["unresolved_assumption_records"]
                    ]:
                        errors.append(
                            f"artifact-indexed target {relative_index} unresolved membership mismatch"
                        )
                    if _checked_indices(
                        projection.get("candidate_assumption_indices", []),
                        compact["candidate_assumption_ids"],
                        field="candidate_assumption_indices",
                        allow_duplicates=True,
                    ) != [
                        item["identity"]
                        for item in values["candidate_assumption_records"]
                    ]:
                        errors.append(
                            f"artifact-indexed target {relative_index} candidate membership mismatch"
                        )
                    for count_field, collection in (
                        ("unresolved_assumption_record_count", "unresolved_assumption_records"),
                        ("candidate_assumption_record_count", "candidate_assumption_records"),
                        ("blocker_record_count", "blocker_records"),
                    ):
                        if projection.get(count_field) != len(values[collection]):
                            errors.append(
                                f"artifact-indexed target {relative_index} {count_field} mismatch"
                            )
            except (KeyError, TypeError, ValueError) as exc:
                errors.append(
                    f"artifact-indexed target {relative_index} reconstruction failed: {exc}"
                )
        if collections is not None:
            expected_inventory = {
                "global_blocker_record_count": len(
                    collections["global"]["global_blocker_records"]
                ),
                "global_evidence_ref_count": len(
                    collections["global"]["global_evidence_ref_records"]
                ),
                "global_source_ref_count": len(
                    collections["global"]["global_source_ref_records"]
                ),
                "resolution": "page_token",
            }
            if _canonical_json_bytes(inventory) != _canonical_json_bytes(
                expected_inventory
            ):
                errors.append("artifact-indexed record inventory mismatch")
            try:
                token = decode_document_derivation_cursor(str(page.get("page_token", "")))
                expected_token_fields = {
                    "audit_result_id": audit_result_id(audit),
                    "audit_request_id": response.get("audit_request_id"),
                    "artifact_sha256": artifact.get("sha256"),
                    "filter_id": _filter_id(audit),
                    "requested_target_limit": requested_limit,
                    "page_index": page_index,
                    "previous_offset": previous_offset,
                    "next_offset": next_offset,
                    "page_boundary_digest": _canonical_digest(
                        _page_boundary(
                            compact,
                            target_indices,
                            page_index=page_index,
                            previous_offset=previous_offset,
                            next_offset=next_offset,
                            requested_target_limit=requested_limit,
                        )
                    ),
                    "resolver_scope_digest": _canonical_digest(
                        _resolver_scope_descriptor(collections)
                    ),
                }
                if any(
                    token.get(field) != expected
                    for field, expected in expected_token_fields.items()
                ):
                    errors.append("artifact-indexed page token semantic binding mismatch")
            except (TypeError, ValueError) as exc:
                errors.append(f"artifact-indexed page token is invalid: {exc}")
    return errors


def validate_document_derivation_response(
    audit: Mapping[str, Any],
    response: Mapping[str, Any],
) -> list[str]:
    """Return semantic-boundary errors without treating presentation as authority."""
    errors: list[str] = []
    required = {
        "metadata",
        "response_schema_version",
        "response_mode",
        "audit_status",
        "status",
        "audit_result_id",
        "audit_request_id",
        "publication_mode",
        "promotion",
        "coverage",
        "failure_classifications",
        "execution_summary",
        "veto_ids",
        "unresolved_assumption_ids",
        "candidate_assumption_ids",
        "action_decision_ids",
        "reference_inventory",
        "non_claims",
        "artifact",
        "page",
        "completeness",
        "payload_guardrail",
        "canonical_byte_count",
    }
    artifact_indexed = (
        response.get("response_mode") == "compact"
        and response.get("compact_representation") == "artifact_indexed"
    )
    if artifact_indexed:
        required.discard("reference_inventory")
    for key in sorted(required - set(response)):
        errors.append(f"missing response field: {key}")
    metadata = response.get("metadata")
    if not isinstance(metadata, Mapping) or metadata.get("contract") != DOCUMENT_DERIVATION_RESPONSE_CONTRACT:
        errors.append("response metadata contract mismatch")
    if response.get("response_schema_version") != DOCUMENT_DERIVATION_RESPONSE_SCHEMA:
        errors.append("response schema version mismatch")
    if response.get("response_mode") not in RESPONSE_MODES:
        errors.append("response mode is invalid")
    if response.get("audit_result_id") != audit_result_id(audit):
        errors.append("audit result identity mismatch")
    expected_status = audit.get("status")
    if not isinstance(expected_status, str) or not expected_status:
        coverage = audit.get("coverage") if isinstance(audit.get("coverage"), Mapping) else {}
        expected_status = coverage.get("status")
    if response.get("audit_status") != expected_status:
        errors.append("audit status differs from completed audit")
    if response.get("status") != expected_status:
        errors.append("status alias differs from completed audit")
    if audit.get("publication_mode") != "disabled" or response.get("publication_mode") != "disabled":
        errors.append("publication mode must remain disabled")
    raw_promotion = audit.get("promotion") if isinstance(audit.get("promotion"), Mapping) else {}
    response_promotion = response.get("promotion") if isinstance(response.get("promotion"), Mapping) else {}
    if raw_promotion.get("can_promote") is True or response_promotion.get("can_promote") is True:
        errors.append("effective promotion must remain false")
    if _canonical_json_bytes(response_promotion) != _canonical_json_bytes(raw_promotion):
        errors.append("promotion differs from completed audit")
    if _canonical_json_bytes(response.get("coverage")) != _canonical_json_bytes(audit.get("coverage", {})):
        errors.append("coverage differs from completed audit")
    expected_sets = {
        "veto_ids": _collect_veto_ids(audit),
        "unresolved_assumption_ids": sorted(
            str(item["id"]) for item in _collect_unresolved_assumptions(audit)
        ),
        "candidate_assumption_ids": sorted(
            {str(item["id"]) for item in _collect_candidate_assumptions(audit)}
        ),
        "action_decision_ids": _collect_action_decision_ids(audit),
        "reference_inventory": _reference_inventory(audit),
        "non_claims": _collect_non_claims(audit),
        "failure_classifications": _collect_failure_classifications(audit),
        "execution_summary": _execution_summary(audit),
    }
    if artifact_indexed:
        expected_sets.pop("reference_inventory")
        for compacted_key in (
            "veto_ids",
            "unresolved_assumption_ids",
            "candidate_assumption_ids",
            "action_decision_ids",
        ):
            expected = expected_sets.pop(compacted_key)
            try:
                expanded = _expand_opaque_ids(response.get(compacted_key, []))
            except (TypeError, ValueError) as exc:
                errors.append(f"{compacted_key} compact identity expansion failed: {exc}")
                continue
            if expanded != expected:
                errors.append(f"{compacted_key} differs from completed audit")
    for key, expected in expected_sets.items():
        source_identity = _normalized_source_identity(str(audit.get("tex_path") or "."))
        normalized_expected = _redact_transport(
            expected,
            result_id=audit_result_id(audit),
            source_identity=source_identity,
            artifact_root=None,
        )
        if _canonical_json_bytes(response.get(key)) != _canonical_json_bytes(normalized_expected):
            errors.append(f"{key} differs from completed audit")
    if "canonical_byte_count" in response:
        try:
            measured = len(_canonical_json_bytes(response))
        except ValueError:
            measured = -1
        if response.get("canonical_byte_count") != measured:
            errors.append("canonical_byte_count does not match response bytes")
    guardrail = response.get("payload_guardrail")
    if isinstance(guardrail, Mapping):
        if response.get("response_mode") == "compact":
            try:
                expected_status = (
                    "met"
                    if _public_page_fits(
                        document_derivation_public_surface_sizes(response)
                    )
                    else "exceeded_complete_boundary_preserved"
                )
            except ValueError:
                expected_status = "invalid"
            if guardrail.get("canonical_target_bytes") != COMPACT_PAYLOAD_TARGET_BYTES:
                errors.append("payload guardrail canonical target mismatch")
            if guardrail.get("transport_target_bytes") != PUBLIC_TRANSPORT_TARGET_BYTES:
                errors.append("payload guardrail transport target mismatch")
        else:
            expected_status = "not_applicable"
            if guardrail.get("target_byte_count") != COMPACT_PAYLOAD_TARGET_BYTES:
                errors.append("payload guardrail target mismatch")
        if guardrail.get("status") != expected_status:
            errors.append("payload guardrail status mismatch")
    if response.get("response_mode") == "compact":
        representation = response.get("compact_representation")
        if representation not in {"artifact_indexed", "inline_complete"}:
            errors.append("compact representation is invalid")
        raw_targets = [
            item for item in audit.get("targets", []) if isinstance(item, Mapping)
        ]
        if representation == "inline_complete":
            transported = response.get("targets")
            if not isinstance(transported, list) or len(transported) != len(raw_targets):
                errors.append("inline complete target count differs from completed audit")
            else:
                source_identity = _normalized_source_identity(
                    str(audit.get("tex_path") or ".")
                )
                for index, (raw_target, target) in enumerate(
                    zip(raw_targets, transported, strict=True)
                ):
                    if not isinstance(target, Mapping):
                        errors.append(f"inline target {index} is invalid")
                        continue
                    expected_record = _redact_transport(
                        raw_target,
                        result_id=audit_result_id(audit),
                        source_identity=source_identity,
                        artifact_root=None,
                    )
                    if _canonical_json_bytes(target.get("record")) != _canonical_json_bytes(
                        expected_record
                    ):
                        errors.append(f"inline target {index} record differs from completed audit")
                    if target.get("raw_record_sha256") != _canonical_digest(raw_target):
                        errors.append(f"inline target {index} raw digest mismatch")
            page = response.get("page")
            if not isinstance(page, Mapping) or page.get("page_token") is not None:
                errors.append("inline complete response must not emit a page token")
        elif representation == "artifact_indexed":
            errors.extend(_artifact_indexed_validation_errors(audit, response))
    return errors


def validate_document_derivation_response_options(
    *,
    response_mode: str,
    artifact_root: str | Path | None,
    target_limit: int | None,
    target_cursor: str | None,
) -> int:
    """Validate transport-only arguments before an expensive raw audit."""
    if response_mode not in RESPONSE_MODES:
        raise ValueError("response_mode must be compact, detailed, or artifact_only")
    decoded = decode_document_derivation_cursor(target_cursor) if target_cursor else None
    if target_limit is None:
        limit = (
            int(decoded["requested_target_limit"])
            if decoded is not None
            else DEFAULT_TARGET_LIMIT
        )
    else:
        try:
            limit = int(target_limit)
        except (TypeError, ValueError) as exc:
            raise ValueError("target_limit must be an integer") from exc
    if not MIN_TARGET_LIMIT <= limit <= MAX_TARGET_LIMIT:
        raise ValueError(f"target_limit must be between {MIN_TARGET_LIMIT} and {MAX_TARGET_LIMIT}")
    if response_mode != "compact" and target_cursor:
        raise ValueError("target_cursor is supported only in compact mode")
    if response_mode == "artifact_only" and artifact_root is None:
        raise ValueError("artifact_root is required for artifact_only mode")
    if target_cursor and artifact_root is None:
        raise ValueError("artifact_root is required with target_cursor")
    if decoded is not None and limit != decoded["requested_target_limit"]:
        raise ValueError("target_limit must equal the page token requested target limit")
    return limit


def compile_document_derivation_response(
    audit: Mapping[str, Any],
    audit_request: Mapping[str, Any],
    *,
    response_mode: str = "compact",
    artifact_root: str | Path | None = None,
    target_limit: int | None = None,
    target_cursor: str | None = None,
) -> dict[str, Any]:
    """Compile a bounded view from a completed audit without executing tools."""
    limit = validate_document_derivation_response_options(
        response_mode=response_mode,
        artifact_root=artifact_root,
        target_limit=target_limit,
        target_cursor=target_cursor,
    )
    if audit.get("publication_mode") != "disabled":
        raise ValueError("document derivation responses require publication_mode=disabled")
    promotion = audit.get("promotion")
    if isinstance(promotion, Mapping) and promotion.get("can_promote") is True:
        raise ValueError("document derivation responses cannot transport effective promotion authority")
    request_id = audit_request.get("audit_request_id")
    expected_request = deepcopy(dict(audit_request))
    expected_request.pop("audit_request_id", None)
    if request_id != "request_" + _canonical_digest(expected_request):
        raise ValueError("audit_request_id does not match the canonical audit request")
    audit_source = audit.get("tex_path")
    if isinstance(audit_source, str) and audit_source:
        if _normalized_source_identity(audit_source) != audit_request.get("source_identity"):
            raise ValueError("completed audit source does not match the audit request")

    stripped = _without_presentation_fields(audit)
    result_id = audit_result_id(stripped)
    artifact = (
        _persist_detailed_artifact(stripped, audit_request, artifact_root)
        if artifact_root is not None
        else {
            "state": "not_persisted",
            "logical_uri": None,
            "sha256": None,
            "byte_count": None,
            "authority": "none",
        }
    )
    targets = [item for item in stripped.get("targets", []) if isinstance(item, Mapping)]
    target_order = _target_order(stripped)
    if len(target_order) != len(set(target_order)):
        raise ValueError("completed audit contains duplicate target identities")
    filter_id = _filter_id(stripped)
    if response_mode == "compact":
        if artifact_root is None or not targets:
            if target_cursor:
                raise ValueError("artifact_root is required with target_cursor")
            response = _compile_inline_complete(
                stripped,
                audit_request,
                artifact,
                requested_target_limit=limit,
            )
        else:
            compact = _compact_projection_source(
                stripped,
                audit_request,
                artifact,
                artifact_root,
            )
            page_index = 0
            offset = 0
            if target_cursor:
                page_index, offset = _page_after_validated_token(
                    compact,
                    stripped,
                    target_cursor,
                    limit,
                )
            response, _ = _longest_prefix_page(
                compact,
                stripped,
                page_index=page_index,
                previous_offset=offset,
                requested_target_limit=limit,
            )
    elif response_mode == "detailed":
        page = {
            "offset": 0,
            "limit": len(targets),
            "included_target_count": len(targets),
            "total_target_count": len(targets),
            "target_ids": _target_order(stripped),
            "next_cursor": None,
            "continuation_available": False,
            "filter_id": filter_id,
        }
        redacted = _redact_transport(
            stripped,
            result_id=result_id,
            source_identity=str(audit_request["source_identity"]),
            artifact_root=artifact_root,
        )
        raw_metadata = redacted.pop("metadata", None)
        response = redacted
        response.update(
            _common_boundary(
                audit,
                audit_request,
                response_mode=response_mode,
                artifact=artifact,
                page=page,
                artifact_root=artifact_root,
            )
        )
        response["audit_metadata"] = raw_metadata
        response["reference_records"] = {
            "evidence_refs": _redact_transport(
                _evidence_ref_entries(stripped),
                result_id=result_id,
                source_identity=str(audit_request["source_identity"]),
                artifact_root=artifact_root,
            ),
            "source_refs": _redact_transport(
                _source_ref_entries(stripped),
                result_id=result_id,
                source_identity=str(audit_request["source_identity"]),
                artifact_root=artifact_root,
            ),
        }
    else:
        page = {
            "offset": 0,
            "limit": 0,
            "included_target_count": 0,
            "total_target_count": len(targets),
            "target_ids": [],
            "next_cursor": None,
            "continuation_available": False,
            "filter_id": filter_id,
        }
        response = _common_boundary(
            audit,
            audit_request,
            response_mode=response_mode,
            artifact=artifact,
            page=page,
            artifact_root=artifact_root,
        )

    if response_mode != "compact":
        response["payload_guardrail"] = {
            "target_byte_count": COMPACT_PAYLOAD_TARGET_BYTES,
            "status": "not_applicable",
            "authority": "product_usability_only",
            "boundary": "Payload size never authorizes omission of claim-boundary records.",
        }
        response["canonical_byte_count"] = 0
        while True:
            measured = len(_canonical_json_bytes(response))
            if measured == response["canonical_byte_count"]:
                break
            response["canonical_byte_count"] = measured
    errors = validate_document_derivation_response(stripped, response)
    if errors:
        raise ValueError(f"document derivation response parity failed: {errors}")
    return response


def canonical_document_derivation_response_bytes(response: Mapping[str, Any]) -> bytes:
    return _canonical_json_bytes(dict(response))
