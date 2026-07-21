from __future__ import annotations

"""Immutable per-target checkpoints for document derivation-tree audits."""

from collections import defaultdict
import base64
import hashlib
import json
from pathlib import Path
from typing import Any

from .document_derivation_tree import (
    DOCUMENT_PUBLICATION_MODE,
    STRICT_GROUNDING_POLICY,
    _backend_env_scope,
    _display_index,
    _section_map,
    _select_label_scoped_targets,
    _target_failure_result,
    _target_result_for_row,
    audit_document_derivation_tree,
)
from .doctor import doctor_report
from .equation_locator import locate_equations_in_file
from .evidence_manifest import (
    EvidenceConflictError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    read_bytes_no_follow,
)
from .latex_index import build_index


TREE_SESSION_SCHEMA = "resumable_document_tree_session@1"
TREE_RECORD_SCHEMA = "resumable_document_tree_target_record@1"
TREE_PAGE_SCHEMA = "resumable_document_tree_page@1"
TREE_ISSUED_PAGE_SCHEMA = "resumable_document_tree_issued_page@1"
TREE_PUBLIC_BYTES = 30_720


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _tree_session_identity(session: dict[str, Any]) -> dict[str, Any]:
    return {
        key: session[key]
        for key in (
            "schema_version",
            "tex_path",
            "source_digest",
            "labels",
            "bindings",
            "options",
            "backend_snapshot",
        )
    }


def validate_resumable_tree_session(session: dict[str, Any]) -> dict[str, Any]:
    if session.get("schema_version") != TREE_SESSION_SCHEMA:
        raise ValueError("resumable tree session schema mismatch")
    if session.get("session_id") != "tree_session_" + _digest(_tree_session_identity(session)):
        raise ValueError("resumable tree session identity mismatch")
    path = Path(str(session.get("tex_path", ""))).resolve()
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != session.get("source_digest"):
        raise ValueError("resumable tree session source drift")
    labels = session.get("labels")
    bindings = session.get("bindings")
    if not isinstance(labels, list) or labels != list(dict.fromkeys(labels)) or not labels:
        raise ValueError("resumable tree session labels are invalid")
    if not isinstance(bindings, list) or len(bindings) != len(labels):
        raise ValueError("resumable tree session binding coverage mismatch")
    for index, (label, binding) in enumerate(zip(labels, bindings, strict=True)):
        if (
            not isinstance(binding, dict)
            or binding.get("index") != index
            or binding.get("label") != label
            or not binding.get("obligation_id")
            or not binding.get("obligation_digest")
        ):
            raise ValueError("resumable tree session binding mismatch")
    return session


def create_resumable_tree_session(
    tex_path: str | Path,
    labels: list[str],
    *,
    source_digest: str,
    budget_profile: str = "standard",
    max_attempts: int = 3,
    backend_env: str = "mathdevmcp-backends",
    search_mode: str = "agent_guided",
    grounding_policy: str = STRICT_GROUNDING_POLICY,
) -> tuple[dict[str, Any], dict[str, Any]]:
    path = Path(tex_path).resolve()
    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != source_digest:
        raise ValueError("source digest does not match tree target")
    if labels != list(dict.fromkeys(labels)) or not labels:
        raise ValueError("labels must be nonempty and unique in requested order")
    if search_mode != "agent_guided" or grounding_policy != STRICT_GROUNDING_POLICY:
        raise ValueError("unsupported tree search or grounding configuration")

    text = path.read_text(encoding="utf-8")
    sections = _section_map(text)
    rows = locate_equations_in_file(path, root=path.parent)
    displays = _display_index(path, text, root=path.parent)
    latex_index = build_index(path.parent)
    selected_rows, extraction = _select_label_scoped_targets(
        path,
        rows,
        focus_labels=labels,
        max_labels=len(labels),
        index=latex_index,
    )
    if extraction.get("failure_count") or [row.get("label") for row in selected_rows] != labels:
        raise ValueError("tree labels do not resolve to exact ordered targets")
    with _backend_env_scope(backend_env) as config:
        doctor = doctor_report(backend_config=config)
    snapshot = {
        "capabilities": doctor.get("capabilities", {}),
        "integrations": doctor.get("integrations", {}),
        "python": {
            key: doctor.get("python", {}).get(key)
            for key in ("executable", "prefix", "version")
        },
        "conflicts": doctor.get("conflicts", []),
    }
    bindings = [
        {
            "index": index,
            "label": row.get("label"),
            "row_id": row.get("id"),
            "row_index": row.get("row_index"),
            "obligation_id": row.get("obligation_id"),
            "obligation_digest": row.get("obligation_digest"),
        }
        for index, row in enumerate(selected_rows)
    ]
    identity = {
        "schema_version": TREE_SESSION_SCHEMA,
        "tex_path": str(path),
        "source_digest": source_digest,
        "labels": list(labels),
        "bindings": bindings,
        "options": {
            "budget_profile": budget_profile,
            "max_attempts": max_attempts,
            "backend_env": backend_env,
            "search_mode": search_mode,
            "grounding_policy": grounding_policy,
        },
        "backend_snapshot": snapshot,
    }
    session = {
        **identity,
        "session_id": "tree_session_" + _digest(identity),
        "authority": "local_byte_identity_only",
        "non_claim": "The session binds tree computation inputs; it is not proof or publication authority.",
    }
    validate_resumable_tree_session(session)
    rows_by_label: dict[str, list[dict[str, Any]]] = defaultdict(list)
    rows_by_environment: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("label"):
            rows_by_label[str(row["label"])].append(row)
        if row.get("environment_id"):
            rows_by_environment[str(row["environment_id"])].append(row)
    context = {
        "path": path,
        "sections": sections,
        "selected_rows": selected_rows,
        "rows_by_label": rows_by_label,
        "rows_by_environment": rows_by_environment,
        "latex_index": latex_index,
        "displays": displays,
        "capabilities": snapshot["capabilities"],
        "integrations": snapshot["integrations"],
    }
    return session, context


def persist_resumable_tree_session(session: dict[str, Any], artifact_root: str | Path) -> dict[str, Any]:
    validate_resumable_tree_session(session)
    root = Path(artifact_root)
    root.mkdir(parents=True, exist_ok=True)
    ref = f"resumable-trees/{session['session_id']}/session.json"
    payload = canonical_json_bytes(session)
    try:
        result = atomic_write_bytes_no_replace(root, ref, payload)
    except EvidenceConflictError:
        existing, _ = read_bytes_no_follow(root, ref)
        if existing != payload:
            raise ValueError("resumable tree session persistence conflict") from None
        result = {"sha256": hashlib.sha256(payload).hexdigest(), "byte_count": len(payload)}
    return {"ref": ref, "sha256": result["sha256"], "byte_count": result["byte_count"]}


def _tree_record_ref(session_id: str, index: int, label: str) -> str:
    return f"resumable-trees/{session_id}/targets/{index:06d}-{hashlib.sha256(label.encode()).hexdigest()}.json"


def validate_resumable_tree_record(
    record: dict[str, Any],
    session: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    validate_resumable_tree_session(session)
    binding = session["bindings"][index]
    expected = {
        "schema_version": TREE_RECORD_SCHEMA,
        "session_id": session["session_id"],
        "index": index,
        "label": binding["label"],
        "source_digest": session["source_digest"],
        "obligation_id": binding["obligation_id"],
        "obligation_digest": binding["obligation_digest"],
    }
    if any(record.get(key) != value for key, value in expected.items()):
        raise ValueError("resumable tree record binding mismatch")
    result = record.get("result")
    if not isinstance(result, dict) or any(result.get(key) != binding.get(key) for key in ("label", "obligation_id", "obligation_digest")):
        raise ValueError("resumable tree result binding mismatch")
    if result.get("publication_mode") != DOCUMENT_PUBLICATION_MODE or result.get("tree", {}).get("publication_mode") != DOCUMENT_PUBLICATION_MODE:
        raise ValueError("resumable tree record publication boundary mismatch")
    identity = {**expected, "result_sha256": _digest(result)}
    if record.get("record_id") != "tree_record_" + _digest(identity):
        raise ValueError("resumable tree record identity mismatch")
    return record


def _load_record(root: Path, ref: str) -> dict[str, Any] | None:
    path = root / ref
    if not path.exists() and not path.is_symlink():
        return None
    payload, _ = read_bytes_no_follow(root, ref)
    try:
        record = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("resumable tree record is invalid JSON") from exc
    if not isinstance(record, dict) or canonical_json_bytes(record) != payload:
        raise ValueError("resumable tree record is not canonical")
    return record


def load_resumable_tree_session(artifact_root: str | Path, session_id: str) -> dict[str, Any]:
    root = Path(artifact_root)
    ref = f"resumable-trees/{session_id}/session.json"
    payload, _ = read_bytes_no_follow(root, ref)
    try:
        session = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("resumable tree session is invalid JSON") from exc
    if not isinstance(session, dict) or canonical_json_bytes(session) != payload:
        raise ValueError("resumable tree session is not canonical")
    if session.get("session_id") != session_id:
        raise ValueError("resumable tree session path identity mismatch")
    return validate_resumable_tree_session(session)


def load_resumable_tree_target_record(
    artifact_root: str | Path,
    session: dict[str, Any],
    index: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    validate_resumable_tree_session(session)
    labels = session.get("labels")
    if not isinstance(labels, list) or not 0 <= index < len(labels):
        raise ValueError("resumable tree target index is out of range")
    ref = _tree_record_ref(str(session["session_id"]), index, str(labels[index]))
    root = Path(artifact_root)
    record = _load_record(root, ref)
    if record is None:
        raise ValueError("resumable tree target record is missing")
    validate_resumable_tree_record(record, session, index)
    payload, _ = read_bytes_no_follow(root, ref)
    return record, {
        "ref": ref,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "byte_count": len(payload),
        "authority": "local_byte_identity_only",
    }


def _tree_page_token(payload: dict[str, Any]) -> str:
    raw = canonical_json_bytes(payload)
    envelope = {"payload": payload, "sha256": hashlib.sha256(raw).hexdigest()}
    encoded = base64.urlsafe_b64encode(canonical_json_bytes(envelope)).decode("ascii").rstrip("=")
    return encoded


def _decode_tree_page_token(token: str) -> dict[str, Any]:
    if not isinstance(token, str) or not token:
        raise ValueError("tree page token must be a non-empty string")
    try:
        padded = token + "=" * (-len(token) % 4)
        envelope = json.loads(base64.urlsafe_b64decode(padded.encode("ascii")).decode("utf-8"))
    except (ValueError, UnicodeError, json.JSONDecodeError, base64.binascii.Error) as exc:
        raise ValueError("tree page token is invalid") from exc
    payload = envelope.get("payload") if isinstance(envelope, dict) else None
    if not isinstance(payload, dict) or envelope.get("sha256") != hashlib.sha256(canonical_json_bytes(payload)).hexdigest():
        raise ValueError("tree page token digest mismatch")
    if payload.get("schema_version") != TREE_PAGE_SCHEMA:
        raise ValueError("tree page token schema mismatch")
    return payload


def _issued_tree_page_ref(session_id: str, token: str) -> str:
    token_digest = hashlib.sha256(token.encode("ascii")).hexdigest()
    return f"resumable-trees/{session_id}/pages/{token_digest}.json"


def _persist_issued_tree_page(
    artifact_root: str | Path,
    session_id: str,
    token: str,
) -> dict[str, Any]:
    ref = _issued_tree_page_ref(session_id, token)
    record = {
        "schema_version": TREE_ISSUED_PAGE_SCHEMA,
        "session_id": session_id,
        "token": token,
        "authority": "local_byte_identity_only",
        "non_claim": "An issued local page token scopes exact checkpoint resolution; it is not an access-control credential or mathematical authority.",
    }
    payload = canonical_json_bytes(record)
    root = Path(artifact_root)
    try:
        result = atomic_write_bytes_no_replace(root, ref, payload)
    except EvidenceConflictError:
        existing, _ = read_bytes_no_follow(root, ref)
        if existing != payload:
            raise ValueError("issued tree page persistence conflict") from None
        result = {
            "sha256": hashlib.sha256(payload).hexdigest(),
            "byte_count": len(payload),
        }
    return {
        "ref": ref,
        "sha256": result["sha256"],
        "byte_count": result["byte_count"],
        "authority": "local_byte_identity_only",
    }


def _validate_issued_tree_page(
    artifact_root: str | Path,
    token: str,
) -> dict[str, Any]:
    token_payload = _decode_tree_page_token(token)
    session_id = str(token_payload.get("session_id", ""))
    ref = _issued_tree_page_ref(session_id, token)
    try:
        payload, _ = read_bytes_no_follow(Path(artifact_root), ref)
    except (FileNotFoundError, ValueError) as exc:
        raise ValueError("tree page token was not issued by this artifact root") from exc
    try:
        record = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("issued tree page record is invalid JSON") from exc
    if (
        not isinstance(record, dict)
        or canonical_json_bytes(record) != payload
        or record.get("schema_version") != TREE_ISSUED_PAGE_SCHEMA
        or record.get("session_id") != session_id
        or record.get("token") != token
    ):
        raise ValueError("issued tree page record binding mismatch")
    return token_payload


def _tree_record_inventory(artifact_root: str | Path, session: dict[str, Any]) -> list[dict[str, Any]]:
    expected_refs = [
        _tree_record_ref(str(session["session_id"]), index, str(label))
        for index, label in enumerate(session["labels"])
    ]
    target_directory = (
        Path(artifact_root)
        / "resumable-trees"
        / str(session["session_id"])
        / "targets"
    )
    if not target_directory.is_dir():
        raise ValueError("resumable tree target directory is missing")
    expected_names = {Path(ref).name for ref in expected_refs}
    observed_names = {
        entry.name
        for entry in target_directory.iterdir()
        if entry.is_file() and not entry.is_symlink()
    }
    if observed_names != expected_names or any(
        not entry.is_file() or entry.is_symlink()
        for entry in target_directory.iterdir()
    ):
        raise ValueError("resumable tree target record inventory mismatch")
    records: list[dict[str, Any]] = []
    for index in range(len(session["labels"])):
        record, artifact = load_resumable_tree_target_record(artifact_root, session, index)
        records.append(
            {
                "index": index,
                "label": session["labels"][index],
                "record_id": record["record_id"],
                "obligation_id": record["obligation_id"],
                "obligation_digest": record["obligation_digest"],
                "record_sha256": artifact["sha256"],
                "byte_count": artifact["byte_count"],
                "ref": artifact["ref"],
            }
        )
    return records


def page_resumable_tree_records(
    artifact_root: str | Path,
    session_id: str,
    *,
    offset: int = 0,
    limit: int = 20,
    page_token: str | None = None,
) -> dict[str, Any]:
    """Return bounded summaries over validated target checkpoints."""
    if not 1 <= int(limit) <= 100:
        raise ValueError("tree page limit must be between 1 and 100")
    session = load_resumable_tree_session(artifact_root, session_id)
    inventory = _tree_record_inventory(artifact_root, session)
    inventory_digest = _digest(inventory)
    if page_token:
        token = _validate_issued_tree_page(artifact_root, page_token)
        if token.get("session_id") != session_id or token.get("source_digest") != session["source_digest"] or token.get("inventory_digest") != inventory_digest:
            raise ValueError("tree page token session or inventory mismatch")
        offset = int(token["next_offset"])
        limit = int(token["limit"])
    if offset < 0 or offset > len(inventory):
        raise ValueError("tree page offset is out of range")
    selected = inventory[offset : offset + int(limit)]

    def response_for(items: list[dict[str, Any]]) -> dict[str, Any]:
        next_offset = offset + len(items)
        token_payload = {
            "schema_version": TREE_PAGE_SCHEMA,
            "session_id": session_id,
            "source_digest": session["source_digest"],
            "inventory_digest": inventory_digest,
            "offset": offset,
            "next_offset": next_offset,
            "limit": int(limit),
            "record_bindings": [
                {
                    key: item[key]
                    for key in ("index", "record_id", "record_sha256", "obligation_digest")
                }
                for item in items
            ],
        }
        return {
            "schema_version": TREE_PAGE_SCHEMA,
            "session_id": session_id,
            "source_digest": session["source_digest"],
            "status": "complete" if next_offset == len(inventory) else "partial",
            "publication_enabled": False,
            "publication_mode": DOCUMENT_PUBLICATION_MODE,
            "total_count": len(inventory),
            "offset": offset,
            "requested_limit": int(limit),
            "returned_count": len(items),
            "records": items,
            "page_token": _tree_page_token(token_payload),
            "continuation_token": _tree_page_token(token_payload) if next_offset < len(inventory) else None,
            "inventory_digest": inventory_digest,
            "non_claims": [
                "This page exposes validated checkpoint metadata, not a full-document proof or publication result.",
                "Exact large records remain local artifacts addressed by their recorded digest and reference.",
            ],
        }

    response = response_for(selected)
    while len(canonical_json_bytes(response)) > TREE_PUBLIC_BYTES and len(selected) > 1:
        selected.pop()
        response = response_for(selected)
    if not selected or len(canonical_json_bytes(response)) > TREE_PUBLIC_BYTES:
        raise ValueError("one resumable tree summary exceeds the public payload budget")
    response["payload_guardrail"] = {
        "status": "met",
        "public_target_bytes": TREE_PUBLIC_BYTES,
        "canonical_byte_count": 0,
    }
    while True:
        size = len(canonical_json_bytes(response))
        if response["payload_guardrail"]["canonical_byte_count"] == size:
            break
        response["payload_guardrail"]["canonical_byte_count"] = size
    if size > TREE_PUBLIC_BYTES:
        raise ValueError("resumable tree page exceeds the public payload budget")
    response["issued_page_artifact"] = _persist_issued_tree_page(
        artifact_root,
        session_id,
        response["page_token"],
    )
    while True:
        size = len(canonical_json_bytes(response))
        if response["payload_guardrail"]["canonical_byte_count"] == size:
            break
        response["payload_guardrail"]["canonical_byte_count"] = size
    if size > TREE_PUBLIC_BYTES:
        raise ValueError("resumable tree page exceeds the public payload budget")
    return response


def resolve_resumable_tree_record(
    artifact_root: str | Path,
    page_token: str,
    index: int,
    *,
    record_sha256: str,
    byte_offset: int = 0,
    byte_limit: int = 16_384,
) -> dict[str, Any]:
    """Stream canonical checkpoint bytes scoped by one issued bounded page."""
    token = _validate_issued_tree_page(artifact_root, page_token)
    session_id = str(token["session_id"])
    session = load_resumable_tree_session(artifact_root, session_id)
    if token.get("source_digest") != session["source_digest"]:
        raise ValueError("tree record page token session mismatch")
    if not int(token["offset"]) <= int(index) < int(token["next_offset"]):
        raise ValueError("tree record index is outside the page token scope")
    if byte_offset < 0 or not 1 <= byte_limit <= 16_384:
        raise ValueError("tree record byte range is invalid")
    record, artifact = load_resumable_tree_target_record(artifact_root, session, int(index))
    bindings = token.get("record_bindings")
    binding = next(
        (
            item
            for item in bindings
            if isinstance(item, dict) and item.get("index") == int(index)
        ),
        None,
    ) if isinstance(bindings, list) else None
    if not isinstance(binding, dict) or any(
        binding.get(key) != value
        for key, value in (
            ("record_id", record["record_id"]),
            ("record_sha256", artifact["sha256"]),
            ("obligation_digest", record["obligation_digest"]),
        )
    ):
        raise ValueError("tree record differs from the page token binding")
    if artifact["sha256"] != record_sha256:
        raise ValueError("tree record digest mismatch")
    payload = canonical_json_bytes(record)
    if byte_offset > len(payload):
        raise ValueError("tree record byte offset is out of range")
    chunk = payload[byte_offset : byte_offset + byte_limit]
    next_offset = byte_offset + len(chunk)
    return {
        "schema_version": "resumable_document_tree_record_resolution@1",
        "session_id": session_id,
        "index": int(index),
        "label": record["label"],
        "record_id": record["record_id"],
        "obligation_id": record["obligation_id"],
        "obligation_digest": record["obligation_digest"],
        "artifact": artifact,
        "byte_offset": byte_offset,
        "byte_limit": byte_limit,
        "returned_byte_count": len(chunk),
        "next_byte_offset": next_offset if next_offset < len(payload) else None,
        "canonical_record_base64": base64.b64encode(chunk).decode("ascii"),
        "publication_enabled": False,
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "non_claim": "The handle proves local artifact identity and does not create mathematical or publication authority.",
    }


def run_resumable_tree_targets(
    session: dict[str, Any],
    context: dict[str, Any],
    artifact_root: str | Path,
    *,
    max_new_records: int | None = None,
) -> dict[str, Any]:
    validate_resumable_tree_session(session)
    if max_new_records is not None and max_new_records < 0:
        raise ValueError("max_new_records must be nonnegative")
    root = Path(artifact_root)
    root.mkdir(parents=True, exist_ok=True)
    completed: list[dict[str, Any]] = []
    produced = 0
    for index, (label, row) in enumerate(zip(session["labels"], context["selected_rows"], strict=True)):
        ref = _tree_record_ref(session["session_id"], index, label)
        record = _load_record(root, ref)
        reused = record is not None
        if record is None:
            if max_new_records is not None and produced >= max_new_records:
                continue
            try:
                result = _target_result_for_row(
                    row,
                    path=context["path"],
                    sections=context["sections"],
                    rows_by_label=context["rows_by_label"],
                    rows_by_environment=context["rows_by_environment"],
                    latex_index=context["latex_index"],
                    displays=context["displays"],
                    budget_profile=session["options"]["budget_profile"],
                    max_attempts=session["options"]["max_attempts"],
                    capabilities=context["capabilities"],
                    integrations=context["integrations"],
                )
            except Exception as exc:  # Keep the monolithic workflow's typed failure behavior.
                result = _target_failure_result(row, exc, index=index)
            binding = session["bindings"][index]
            result.setdefault("obligation_id", binding["obligation_id"])
            result.setdefault("obligation_digest", binding["obligation_digest"])
            identity = {
                "schema_version": TREE_RECORD_SCHEMA,
                "session_id": session["session_id"],
                "index": index,
                "label": label,
                "source_digest": session["source_digest"],
                "obligation_id": binding["obligation_id"],
                "obligation_digest": binding["obligation_digest"],
                "result_sha256": _digest(result),
            }
            record = {
                **{key: value for key, value in identity.items() if key != "result_sha256"},
                "record_id": "tree_record_" + _digest(identity),
                "result": result,
                "authority": "local_byte_identity_only",
                "non_claim": "This target checkpoint is diagnostic tree evidence, not a proof or publishable repair.",
            }
            validate_resumable_tree_record(record, session, index)
            atomic_write_bytes_no_replace(root, ref, canonical_json_bytes(record))
            produced += 1
        validate_resumable_tree_record(record, session, index)
        completed.append({"index": index, "label": label, "ref": ref, "reused": reused, "record": record})
    return {
        "schema_version": "resumable_document_tree_batch@1",
        "session_id": session["session_id"],
        "requested_count": len(session["labels"]),
        "completed_count": len(completed),
        "produced_count": produced,
        "reused_count": sum(1 for item in completed if item["reused"]),
        "pending_count": len(session["labels"]) - len(completed),
        "complete": len(completed) == len(session["labels"]),
        "records": completed,
    }


def assemble_resumable_tree_result(session: dict[str, Any], batch: dict[str, Any]) -> dict[str, Any]:
    validate_resumable_tree_session(session)
    records = batch.get("records")
    if batch.get("session_id") != session["session_id"] or batch.get("complete") is not True or not isinstance(records, list):
        raise ValueError("resumable tree batch is incomplete or cross-session")
    ordered = sorted(records, key=lambda item: item.get("index", -1))
    if [item.get("index") for item in ordered] != list(range(len(session["labels"]))):
        raise ValueError("resumable tree batch coverage mismatch")
    for item in ordered:
        validate_resumable_tree_record(item["record"], session, item["index"])
    options = session["options"]
    result = audit_document_derivation_tree(
        session["tex_path"],
        focus_labels=list(session["labels"]),
        max_labels=len(session["labels"]),
        budget_profile=options["budget_profile"],
        max_attempts=options["max_attempts"],
        backend_env=options["backend_env"],
        search_mode=options["search_mode"],
        grounding_policy=options["grounding_policy"],
        workers=1,
        precomputed_target_results=[item["record"]["result"] for item in ordered],
    )
    result["resumable_evidence"] = {
        "schema_version": "resumable_document_tree_aggregate@1",
        "session_id": session["session_id"],
        "source_digest": session["source_digest"],
        "labels": list(session["labels"]),
        "record_ids": [item["record"]["record_id"] for item in ordered],
        "publication_mode": DOCUMENT_PUBLICATION_MODE,
        "authority": "local_byte_identity_only",
        "non_claim": "Complete target reuse is not whole-document proof or publication authority.",
    }
    return result
