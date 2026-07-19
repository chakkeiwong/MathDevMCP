from __future__ import annotations

"""Immutable session and per-label checkpoints for resumable document audits."""

import hashlib
import json
from pathlib import Path
from typing import Any, Callable

from .derivation_target_extraction import extract_derivation_targets_for_label
from .evidence_manifest import (
    EvidenceConflictError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    read_bytes_no_follow,
)
from .latex_index import build_index
from .parser_policy import decide_parser_policy, project_parser_policy_expected_labels


SESSION_SCHEMA = "resumable_document_audit_session@1"
LABEL_RECORD_SCHEMA = "resumable_label_audit_record@1"
PACKET_AUDIT_OPTIONS = {
    "backend": "sympy",
    "paragraph_context": False,
    "before": 0,
    "after": 0,
    "task_context": "general_math_audit",
    "parser_backends": ["current"],
}


def _digest(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def _durable_parser_policy(parser: dict[str, Any]) -> dict[str, Any]:
    """Project parser selection evidence onto canonical, non-proxy identity."""

    benchmark = parser.get("benchmark_report")
    results = benchmark.get("results", []) if isinstance(benchmark, dict) else []
    durable_results: list[dict[str, Any]] = []
    for result in results:
        if not isinstance(result, dict):
            continue
        details = result.get("details")
        quality = result.get("quality_checks")
        durable_results.append(
            {
                "backend": result.get("backend"),
                "status": result.get("status"),
                "reason": result.get("reason"),
                "labels_found": result.get("labels_found"),
                "environments_found": result.get("environments_found"),
                "align_like_found": result.get("align_like_found"),
                "provenance_quality": result.get("provenance_quality"),
                "quality_checks": dict(quality) if isinstance(quality, dict) else {},
                "expected_labels": list(details.get("expected_labels", [])) if isinstance(details, dict) else [],
                "missing_expected_labels": list(details.get("missing_expected_labels", [])) if isinstance(details, dict) else [],
            }
        )
    metadata = parser.get("metadata")
    return {
        "contract": metadata.get("contract") if isinstance(metadata, dict) else None,
        "schema_version": metadata.get("schema_version") if isinstance(metadata, dict) else None,
        "status": parser.get("status"),
        "legacy_status": parser.get("legacy_status"),
        "reason": parser.get("reason"),
        "selected_backend": parser.get("selected_backend"),
        "blocking_findings": parser.get("blocking_findings", []),
        "caveats": parser.get("caveats", []),
        "backend_roles": parser.get("backend_roles", []),
        "backend_evidence": durable_results,
        "excluded_explanatory_fields": [
            "benchmark runtime",
            "recall, precision, and provenance-score proxy metrics",
            "redundant parser label inventory outside the requested-label binding",
        ],
    }


def _source_path(root: Path, target_file: str) -> Path:
    path = (root / target_file).resolve()
    if root not in path.parents or not path.is_file():
        raise ValueError("target_file must resolve to a regular file under root")
    return path


def _session_identity(session: dict[str, Any]) -> dict[str, Any]:
    return {
        key: session[key]
        for key in (
            "schema_version",
            "root",
            "target_file",
            "source_digest",
            "labels",
            "bindings",
            "options",
            "parser_policy",
            "label_parser_policies",
        )
    }


def validate_resumable_audit_session(session: dict[str, Any]) -> dict[str, Any]:
    if session.get("schema_version") != SESSION_SCHEMA:
        raise ValueError("resumable audit session schema mismatch")
    identity = _session_identity(session)
    if session.get("session_id") != "session_" + _digest(identity):
        raise ValueError("resumable audit session identity mismatch")
    root = Path(str(session.get("root", ""))).resolve()
    source = _source_path(root, str(session.get("target_file", "")))
    if hashlib.sha256(source.read_bytes()).hexdigest() != session.get("source_digest"):
        raise ValueError("resumable audit session source drift")
    labels = session.get("labels")
    bindings = session.get("bindings")
    if not isinstance(labels, list) or not isinstance(bindings, list) or len(labels) != len(bindings):
        raise ValueError("resumable audit session coverage mismatch")
    if labels != list(dict.fromkeys(labels)) or any(
        not isinstance(binding, dict)
        or binding.get("label") != label
        or binding.get("source_digest") != session.get("source_digest")
        or binding.get("binding_type") not in {"canonical_target", "typed_abstention"}
        or not binding.get("obligation_id")
        or not binding.get("obligation_digest")
        for label, binding in zip(labels, bindings, strict=True)
    ):
        raise ValueError("resumable audit session binding mismatch")
    label_parser_policies = session.get("label_parser_policies")
    if (
        not isinstance(label_parser_policies, list)
        or len(label_parser_policies) != len(labels)
        or any(
            not isinstance(item, dict)
            or item.get("label") != label
            or not isinstance(item.get("policy"), dict)
            for label, item in zip(labels, label_parser_policies, strict=True)
        )
    ):
        raise ValueError("resumable audit session per-label parser policy mismatch")
    return session


def persist_resumable_audit_session(session: dict[str, Any], artifact_root: str | Path) -> dict[str, Any]:
    validate_resumable_audit_session(session)
    root = Path(artifact_root)
    root.mkdir(parents=True, exist_ok=True)
    ref = f"resumable-audits/{session['session_id']}/session.json"
    payload = canonical_json_bytes(session)
    try:
        result = atomic_write_bytes_no_replace(root, ref, payload)
    except EvidenceConflictError:
        existing, _ = read_bytes_no_follow(root, ref)
        if existing != payload:
            raise ValueError("resumable audit session persistence conflict") from None
        result = {"sha256": hashlib.sha256(payload).hexdigest(), "byte_count": len(payload)}
    return {"ref": ref, "sha256": result["sha256"], "byte_count": result["byte_count"]}


def load_resumable_audit_session(artifact_root: str | Path, session_id: str) -> dict[str, Any]:
    root = Path(artifact_root)
    ref = f"resumable-audits/{session_id}/session.json"
    payload, _ = read_bytes_no_follow(root, ref)
    try:
        session = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("resumable audit session is invalid JSON") from exc
    if not isinstance(session, dict) or canonical_json_bytes(session) != payload:
        raise ValueError("resumable audit session is not canonical")
    if session.get("session_id") != session_id:
        raise ValueError("resumable audit session path identity mismatch")
    return validate_resumable_audit_session(session)


def create_resumable_audit_session(
    root: str | Path,
    target_file: str,
    labels: list[str],
    *,
    source_digest: str,
    backend: str = "sympy",
    paragraph_context: bool = True,
    context_before: int = 4,
    context_after: int = 1,
    task_context: str = "symbolic_exposition",
    summary_only: bool = True,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    root_path = Path(root).resolve()
    source_path = _source_path(root_path, target_file)
    actual_digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
    if actual_digest != source_digest:
        raise ValueError("source digest does not match target_file")
    ordered_labels = list(dict.fromkeys(labels))
    if ordered_labels != labels or not ordered_labels:
        raise ValueError("labels must be nonempty and unique in requested order")
    index = build_index(root_path)
    bindings: list[dict[str, Any]] = []
    for label in ordered_labels:
        result = extract_derivation_targets_for_label(index, label, file=target_file)
        targets = [item for item in result.get("targets", []) if isinstance(item, dict)]
        obligations = [item for item in result.get("obligations", []) if isinstance(item, dict)]
        if result.get("status") == "extracted" and len(targets) == 1:
            target = targets[0]
            obligation = target.get("label_scoped_obligation")
            binding_type = "canonical_target"
        elif len(obligations) == 1 and result.get("status") in {"quarantined", "ambiguous"}:
            target = obligations[0]
            obligation = obligations[0]
            binding_type = "typed_abstention"
        else:
            raise ValueError(f"label {label} does not resolve to one source-bound audit obligation")
        if not isinstance(obligation, dict):
            raise ValueError(f"label {label} lacks a source-bound audit obligation")
        observed_digest = obligation.get("document", {}).get("source_digest")
        if observed_digest != source_digest:
            raise ValueError(f"label {label} obligation source digest mismatch")
        bindings.append(
            {
                "label": label,
                "binding_type": binding_type,
                "obligation_id": target.get("obligation_id"),
                "obligation_digest": target.get("obligation_digest"),
                "source_digest": observed_digest,
                "extraction_status": result.get("status"),
                "extraction_reason": result.get("reason"),
            }
        )
    parser_policy = decide_parser_policy(
        str(root_path),
        backends=["current"],
        expected_labels=ordered_labels,
    )
    label_parser_policies = [
        {
            "label": label,
            "policy": _durable_parser_policy(
                project_parser_policy_expected_labels(parser_policy, [label])
            ),
        }
        for label in ordered_labels
    ]
    identity = {
        "schema_version": SESSION_SCHEMA,
        "root": str(root_path),
        "target_file": target_file,
        "source_digest": source_digest,
        "labels": ordered_labels,
        "bindings": bindings,
        "options": {
            "backend": backend,
            "paragraph_context": paragraph_context,
            "before": context_before,
            "after": context_after,
            "task_context": task_context,
            "summary_only": summary_only,
            "parser_backends": ["current"],
        },
        "parser_policy": _durable_parser_policy(parser_policy),
        "label_parser_policies": label_parser_policies,
    }
    session = {
        **identity,
        "session_id": "session_" + _digest(identity),
        "authority": "local_byte_identity_only",
        "non_claim": "The session binds source and audit configuration; it is not an audit result or proof.",
    }
    validate_resumable_audit_session(session)
    return session, index, parser_policy


def _record_ref(session_id: str, index: int, label: str) -> str:
    label_digest = hashlib.sha256(label.encode("utf-8")).hexdigest()
    return f"resumable-audits/{session_id}/labels/{index:06d}-{label_digest}.json"


def load_resumable_audit_label_record(
    artifact_root: str | Path,
    session: dict[str, Any],
    index: int,
    record_id: str,
) -> dict[str, Any]:
    """Load one exact checkpoint and validate every session binding."""
    validate_resumable_audit_session(session)
    labels = session.get("labels")
    if not isinstance(labels, list) or not 0 <= index < len(labels):
        raise ValueError("resumable audit record index is out of range")
    ref = _record_ref(str(session["session_id"]), index, str(labels[index]))
    root = Path(artifact_root)
    record = _load_record(root, ref)
    if record is None:
        raise ValueError("resumable audit checkpoint is missing")
    validate_resumable_label_record(record, session, index)
    if record.get("record_id") != record_id:
        raise ValueError("resumable audit checkpoint record identity mismatch")
    return record


def load_packet_audit_checkpoint(
    artifact_root: str | Path,
    session_id: str,
    record_index: int,
    record_id: str,
    *,
    root: str | Path,
    label: str,
    target_file: str | None,
    source_digest: str | None,
    summary_only: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Load a checkpoint that is semantically identical to a public packet audit."""

    session = load_resumable_audit_session(artifact_root, session_id)
    labels = session.get("labels")
    if not isinstance(labels, list) or not 0 <= record_index < len(labels):
        raise ValueError("packet checkpoint record index is out of range")
    if session.get("root") != str(Path(root).resolve()):
        raise ValueError("checkpoint session root does not match packet root")
    if labels[record_index] != label:
        raise ValueError("checkpoint label does not match packet label")
    if session.get("target_file") != target_file or session.get("source_digest") != source_digest:
        raise ValueError("checkpoint source binding does not match packet request")
    expected_options = {**PACKET_AUDIT_OPTIONS, "summary_only": summary_only}
    if session.get("options") != expected_options:
        raise ValueError("checkpoint audit configuration does not match packet route")
    record = load_resumable_audit_label_record(
        artifact_root,
        session,
        record_index,
        record_id,
    )
    return session, record


def _expected_binding(session: dict[str, Any], index: int) -> dict[str, Any]:
    labels = session.get("labels")
    bindings = session.get("bindings")
    if not isinstance(labels, list) or not isinstance(bindings, list) or index >= len(labels) or index >= len(bindings):
        raise ValueError("session label inventory is invalid")
    binding = bindings[index]
    if not isinstance(binding, dict) or binding.get("label") != labels[index]:
        raise ValueError("session label binding is invalid")
    return binding


def validate_resumable_label_record(
    record: dict[str, Any],
    session: dict[str, Any],
    index: int,
) -> dict[str, Any]:
    binding = _expected_binding(session, index)
    expected = {
        "schema_version": LABEL_RECORD_SCHEMA,
        "session_id": session.get("session_id"),
        "index": index,
        "label": binding.get("label"),
        "source_digest": session.get("source_digest"),
        "obligation_id": binding.get("obligation_id"),
        "obligation_digest": binding.get("obligation_digest"),
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise ValueError(f"resumable label record {key} mismatch")
    result = record.get("result")
    if not isinstance(result, dict) or result.get("label") != binding.get("label"):
        raise ValueError("resumable label record result mismatch")
    if result.get("metadata", {}).get("contract") != "proof_audit_v2_result":
        raise ValueError("resumable label record contract mismatch")
    expected_configuration = {
        "backend": session.get("options", {}).get("backend"),
        "paragraph_context": session.get("options", {}).get("paragraph_context"),
        "summary_only": session.get("options", {}).get("summary_only"),
        "file": session.get("target_file"),
        "source_digest": session.get("source_digest"),
        "parser_backends": session.get("options", {}).get("parser_backends"),
    }
    for key in ("before", "after", "task_context"):
        if key in session.get("options", {}):
            expected_configuration[key] = session["options"][key]
    if result.get("audit_configuration") != expected_configuration:
        raise ValueError("resumable label record audit configuration mismatch")
    if result.get("doc_root") != session.get("root"):
        raise ValueError("resumable label record root mismatch")
    targets = result.get("target_extraction", {}).get("targets", [])
    obligations = result.get("target_extraction", {}).get("obligations", [])
    if binding.get("binding_type") == "canonical_target":
        candidates = targets
    else:
        candidates = obligations
        if targets:
            raise ValueError("resumable typed-abstention record unexpectedly contains an adapter target")
        if result.get("source_binding_status") != "source_bound_typed_abstention":
            raise ValueError("resumable typed-abstention source status mismatch")
    if len(candidates) != 1 or candidates[0].get("obligation_id") != binding.get("obligation_id") or candidates[0].get("obligation_digest") != binding.get("obligation_digest"):
        raise ValueError("resumable label record obligation mismatch")
    identity = {key: record[key] for key in expected}
    identity["result_sha256"] = _digest(result)
    if record.get("record_id") != "record_" + _digest(identity):
        raise ValueError("resumable label record identity mismatch")
    return record


def _load_record(root: Path, ref: str) -> dict[str, Any] | None:
    path = root / ref
    if not path.exists() and not path.is_symlink():
        return None
    payload, _ = read_bytes_no_follow(root, ref)
    try:
        record = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("resumable label record is invalid JSON") from exc
    if not isinstance(record, dict) or canonical_json_bytes(record) != payload:
        raise ValueError("resumable label record is not canonical")
    return record


def run_resumable_label_audits(
    session: dict[str, Any],
    artifact_root: str | Path,
    producer: Callable[[str], dict[str, Any]],
    *,
    max_new_records: int | None = None,
) -> dict[str, Any]:
    validate_resumable_audit_session(session)
    if max_new_records is not None and max_new_records < 0:
        raise ValueError("max_new_records must be nonnegative")
    root = Path(artifact_root)
    root.mkdir(parents=True, exist_ok=True)
    labels = session.get("labels")
    if not isinstance(labels, list):
        raise ValueError("session labels are invalid")
    completed: list[dict[str, Any]] = []
    produced = 0
    attempted = 0
    failures: list[dict[str, Any]] = []
    for index, label in enumerate(labels):
        ref = _record_ref(str(session.get("session_id")), index, str(label))
        record = _load_record(root, ref)
        reused = record is not None
        if record is None:
            if max_new_records is not None and attempted >= max_new_records:
                continue
            attempted += 1
            try:
                result = producer(str(label))
            except Exception as exc:
                failures.append(
                    {
                        "index": index,
                        "label": label,
                        "failure_classification": "record_production_failure",
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
                continue
            binding = _expected_binding(session, index)
            identity = {
                "schema_version": LABEL_RECORD_SCHEMA,
                "session_id": session.get("session_id"),
                "index": index,
                "label": label,
                "source_digest": session.get("source_digest"),
                "obligation_id": binding.get("obligation_id"),
                "obligation_digest": binding.get("obligation_digest"),
                "result_sha256": _digest(result),
            }
            record = {
                **{key: identity[key] for key in identity if key != "result_sha256"},
                "record_id": "record_" + _digest(identity),
                "result": result,
                "authority": "local_byte_identity_only",
                "non_claim": "This checkpoint preserves diagnostic evidence bytes; it is not a proof or publication authority.",
            }
            validate_resumable_label_record(record, session, index)
            atomic_write_bytes_no_replace(root, ref, canonical_json_bytes(record))
            produced += 1
        validate_resumable_label_record(record, session, index)
        completed.append({"index": index, "label": label, "ref": ref, "reused": reused, "record": record})
    completed_indices = {item["index"] for item in completed}
    return {
        "schema_version": "resumable_label_audit_batch@1",
        "session_id": session.get("session_id"),
        "requested_count": len(labels),
        "completed_count": len(completed),
        "produced_count": produced,
        "attempted_count": attempted,
        "reused_count": sum(1 for item in completed if item["reused"]),
        "failed_count": len(failures),
        "failures": failures,
        "pending_count": len(labels) - len(completed),
        "complete": len(completed) == len(labels),
        "completed_indices": sorted(completed_indices),
        "records": completed,
    }


def ordered_results_from_batch(batch: dict[str, Any]) -> list[dict[str, Any]]:
    if batch.get("complete") is not True:
        raise ValueError("resumable batch is incomplete")
    records = batch.get("records")
    if not isinstance(records, list):
        raise ValueError("resumable batch records are invalid")
    ordered = sorted(records, key=lambda item: int(item["index"]))
    if [item["index"] for item in ordered] != list(range(len(ordered))):
        raise ValueError("resumable batch coverage is not exact")
    return [item["record"]["result"] for item in ordered]


def validate_resumable_audit_batch(
    batch: dict[str, Any],
    session: dict[str, Any],
    *,
    require_complete: bool = True,
) -> dict[str, Any]:
    validate_resumable_audit_session(session)
    if batch.get("session_id") != session.get("session_id"):
        raise ValueError("resumable batch session mismatch")
    records = batch.get("records")
    if not isinstance(records, list):
        raise ValueError("resumable batch records are invalid")
    ordered = sorted(records, key=lambda item: int(item.get("index", -1)))
    indices = [item.get("index") for item in ordered]
    if len(indices) != len(set(indices)) or any(index not in range(len(session["labels"])) for index in indices):
        raise ValueError("resumable batch record coverage is invalid")
    for item in ordered:
        index = int(item["index"])
        if item.get("label") != session["labels"][index] or not isinstance(item.get("record"), dict):
            raise ValueError("resumable batch record envelope mismatch")
        validate_resumable_label_record(item["record"], session, index)
    complete = indices == list(range(len(session["labels"])))
    if require_complete and (batch.get("complete") is not True or not complete):
        raise ValueError("resumable batch is incomplete")
    if batch.get("completed_count") != len(records) or batch.get("pending_count") != len(session["labels"]) - len(records):
        raise ValueError("resumable batch count mismatch")
    return batch


def _audit_fix_semantic_projection(low_level: dict[str, Any]) -> dict[str, Any]:
    return {
        key: low_level.get(key)
        for key in (
            "status",
            "question",
            "source",
            "coverage",
            "audited_evidence",
            "proposal_changes",
            "proposal_details",
            "validation",
            "proposal",
            "non_claims",
            "certification_boundary",
        )
    }


def validate_resumable_audit_fix_result(result: dict[str, Any]) -> dict[str, Any]:
    if result.get("workflow") != "audit_and_propose_fix":
        raise ValueError("resumable aggregate workflow mismatch")
    evidence = result.get("evidence")
    low = evidence[0].get("low_level") if isinstance(evidence, list) and evidence and isinstance(evidence[0], dict) else None
    if not isinstance(low, dict):
        raise ValueError("resumable aggregate low-level report missing")
    provenance = low.get("resumable_evidence")
    if not isinstance(provenance, dict) or provenance.get("schema_version") != "resumable_audit_fix_aggregate@1":
        raise ValueError("resumable aggregate provenance missing")
    semantic_digest = _digest(_audit_fix_semantic_projection(low))
    identity = {
        "schema_version": provenance.get("schema_version"),
        "session_id": provenance.get("session_id"),
        "source_digest": provenance.get("source_digest"),
        "labels": provenance.get("labels"),
        "record_ids": provenance.get("record_ids"),
        "aggregate_options": provenance.get("aggregate_options"),
        "semantic_result_sha256": semantic_digest,
    }
    if provenance.get("semantic_result_sha256") != semantic_digest:
        raise ValueError("resumable aggregate semantic result drift")
    if provenance.get("aggregate_id") != "aggregate_" + _digest(identity):
        raise ValueError("resumable aggregate identity mismatch")
    source = low.get("source") if isinstance(low.get("source"), dict) else {}
    labels = low.get("coverage", {}).get("audited_labels", [])
    audited_labels = [item.get("label") for item in labels if isinstance(item, dict)]
    if source.get("source_digest") != provenance.get("source_digest") or audited_labels != provenance.get("labels"):
        raise ValueError("resumable aggregate source or label binding mismatch")
    return result


def build_resumable_audit_fix_result(
    session: dict[str, Any],
    batch: dict[str, Any],
    question: str,
    *,
    validate_proposed_fixes: bool = False,
    certifier_policy: str = "require_attempt_when_encodable",
    backend_order: list[str] | tuple[str, ...] | None = None,
) -> dict[str, Any]:
    """Assemble the existing audit/fix workflow from exact checkpoint evidence."""

    validate_resumable_audit_batch(batch, session)
    from .audit_and_propose_fix import audit_and_propose_fix

    result = audit_and_propose_fix(
        question,
        root=session["root"],
        labels=list(session["labels"]),
        target_file=session["target_file"],
        source_digest=session["source_digest"],
        backend=session["options"]["backend"],
        paragraph_context=bool(session["options"]["paragraph_context"]),
        context_before=int(session["options"]["before"]),
        context_after=int(session["options"]["after"]),
        task_context=str(session["options"]["task_context"]),
        summary_only=bool(session["options"]["summary_only"]),
        validate_proposed_fixes=validate_proposed_fixes,
        certifier_policy=certifier_policy,
        backend_order=backend_order,
        precomputed_label_audits=ordered_results_from_batch(batch),
    )
    low = result["evidence"][0]["low_level"]
    aggregate_options = {
        "question": question,
        "validate_proposed_fixes": validate_proposed_fixes,
        "certifier_policy": certifier_policy,
        "backend_order": list(backend_order) if backend_order is not None else None,
    }
    semantic_digest = _digest(_audit_fix_semantic_projection(low))
    identity = {
        "schema_version": "resumable_audit_fix_aggregate@1",
        "session_id": session["session_id"],
        "source_digest": session["source_digest"],
        "labels": list(session["labels"]),
        "record_ids": [item["record"]["record_id"] for item in sorted(batch["records"], key=lambda item: item["index"])],
        "aggregate_options": aggregate_options,
        "semantic_result_sha256": semantic_digest,
    }
    provenance = {
        **identity,
        "aggregate_id": "aggregate_" + _digest(identity),
        "authority": "local_byte_identity_only",
        "non_claim": "Checkpoint continuity does not establish mathematical correctness or publication authority.",
    }
    low["resumable_evidence"] = provenance
    result["agent_handoff"]["resumable_evidence"] = provenance
    return validate_resumable_audit_fix_result(result)


def run_session_label_audits(
    session: dict[str, Any],
    artifact_root: str | Path,
    *,
    max_new_records: int | None = None,
    index: dict[str, Any] | None = None,
    parser_policy: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Run a bounded batch using only configuration bound by the session."""

    validate_resumable_audit_session(session)
    options = session["options"]
    shared_index = index or build_index(Path(session["root"]))
    shared_parser = parser_policy or decide_parser_policy(
        session["root"],
        backends=list(options["parser_backends"]),
        expected_labels=list(session["labels"]),
    )
    if _durable_parser_policy(shared_parser) != session["parser_policy"]:
        raise ValueError("resumable audit session parser policy drift")
    projected_parsers = {
        label: project_parser_policy_expected_labels(shared_parser, [label])
        for label in session["labels"]
    }
    if [
        {"label": label, "policy": _durable_parser_policy(projected_parsers[label])}
        for label in session["labels"]
    ] != session["label_parser_policies"]:
        raise ValueError("resumable audit session per-label parser policy drift")

    from .proof_audit_v2 import audit_derivation_v2_for_label

    def produce(label: str) -> dict[str, Any]:
        return audit_derivation_v2_for_label(
            session["root"],
            label,
            paragraph_context=bool(options["paragraph_context"]),
            before=int(options["before"]),
            after=int(options["after"]),
            task_context=str(options["task_context"]),
            summary_only=bool(options["summary_only"]),
            backend=str(options["backend"]),
            parser_backends=list(options["parser_backends"]),
            file=str(session["target_file"]),
            source_digest=str(session["source_digest"]),
            index=shared_index,
            parser_policy=projected_parsers[label],
        )

    return run_resumable_label_audits(
        session,
        artifact_root,
        produce,
        max_new_records=max_new_records,
    )
