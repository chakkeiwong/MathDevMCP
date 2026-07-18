from __future__ import annotations

"""Immutable per-target checkpoints for document derivation-tree audits."""

from collections import defaultdict
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
    with _backend_env_scope(backend_env):
        doctor = doctor_report()
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
