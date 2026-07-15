from __future__ import annotations

"""External-tool adapter evidence normalized for derivation search trees."""

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import time
from typing import Any, Callable, Mapping

from .counterexample_search import find_counterexample
from .derivation_search_tree import BackendAttempt, PROMOTION_BOUNDARY
from .derive_or_refute import derive_or_refute
from .evidence_manifest import (
    ExecutionAllocation,
    RunBundle,
    allocate_execution,
    atomic_write_artifact,
    build_evidence_request,
    content_digest,
    create_run_bundle,
    seal_attempt_manifest,
    verify_attempt_manifest,
)
from .lean_check import (
    LeanDiagnosticContext,
    LeanTargetBinding,
    check_lean_source,
    lean_execution_matches_binding,
    validate_lean_diagnostic_context,
    validate_lean_target_binding,
)


EXTERNAL_TOOL_ADAPTER_BOUNDARY = (
    "External-tool adapters produce bounded evidence attempts for the search "
    "tree. They do not run branch search or certify more than the underlying "
    "backend result certifies."
)

EXTERNAL_TOOL_ADAPTER_RESULT_CONTRACT = "external_tool_adapter_attempt_result"


@dataclass(frozen=True)
class AdapterAttemptResult:
    status: str
    reason: str
    attempt: dict[str, Any]
    source_contract: str | None
    source_status: str | None
    raw_result: dict[str, Any] | None
    evidence_attachment: dict[str, Any] | None
    certification_state: str
    claim_eligibility: str
    publication_enabled: bool
    boundary: str


@dataclass(frozen=True)
class EvidenceContext:
    """Complete caller-supplied v1 identity for one scoped adapter action."""

    source_logical_id: str
    source_file: str
    source_label: str
    source_bytes: bytes
    source_spans: tuple[dict[str, int], ...]
    parser_version: str
    obligation_digest: str
    normalized_target: str
    branch_id: str
    branch_lineage: tuple[str, ...]
    typed_assumptions: tuple[dict[str, str], ...]
    native_input_bytes: bytes
    native_input_media_type: str
    tool_name: str
    adapter_version: str
    backend_version: str
    executable_id: str
    timeout_ms: int
    max_output_bytes: int
    expected_result_class: str
    backend_role: str
    unsupported_conclusions: tuple[str, ...]
    policy_version: str


@dataclass(frozen=True)
class _PreparedEvidence:
    bundle: RunBundle
    execution: ExecutionAllocation
    request: dict[str, Any]
    native_artifact: dict[str, Any]


def _contract(payload: dict[str, Any] | None) -> str | None:
    if not isinstance(payload, dict):
        return None
    metadata = payload.get("metadata")
    if isinstance(metadata, dict) and isinstance(metadata.get("contract"), str):
        return metadata["contract"]
    return None


def _stable_ref(tool: str, payload: dict[str, Any] | None, *, fallback: str) -> str:
    contract = _contract(payload) or "untyped"
    source_status = payload.get("status") if isinstance(payload, dict) else fallback
    digest_input = f"{tool}|{contract}|{source_status}|{fallback}".encode("utf-8")
    digest = hashlib.sha256(digest_input).hexdigest()[:16]
    return f"mathdevmcp://external-tool-adapter/{tool}/{digest}"


def _exception_payload(tool: str, exc: Exception) -> dict[str, Any]:
    return {
        "status": "adapter_error",
        "reason": f"{tool} adapter call failed: {type(exc).__name__}: {exc}",
        "metadata": {"schema_version": "1.0", "contract": "external_tool_adapter_error"},
    }


def _attempt(
    *,
    attempt_id: str,
    tool: str,
    status: str,
    evidence_kind: str,
    certification_status: str,
    input_summary: str,
    output_ref: str | None = None,
    timeout_seconds: float | None = None,
    version: str | None = None,
) -> dict[str, Any]:
    return asdict(
        BackendAttempt(
            id=attempt_id,
            tool=tool,
            status=status,
            evidence_kind=evidence_kind,
            certification_status=certification_status,
            input_summary=input_summary,
            output_ref=output_ref,
            timeout_seconds=timeout_seconds,
            version=version,
            boundary=PROMOTION_BOUNDARY,
        )
    )


def _adapter_result(
    *,
    status: str,
    reason: str,
    attempt: dict[str, Any],
    raw_result: dict[str, Any] | None,
    evidence_attachment: dict[str, Any] | None = None,
) -> dict[str, Any]:
    is_v1 = evidence_attachment is not None
    result = AdapterAttemptResult(
        status=status,
        reason=reason,
        attempt=attempt,
        source_contract=_contract(raw_result),
        source_status=str(raw_result.get("status")) if isinstance(raw_result, dict) and raw_result.get("status") else None,
        raw_result=raw_result,
        evidence_attachment=evidence_attachment,
        certification_state="verified_manifest" if is_v1 else "unbound_legacy_evidence",
        claim_eligibility="ineligible",
        publication_enabled=False,
        boundary=EXTERNAL_TOOL_ADAPTER_BOUNDARY,
    )
    payload = asdict(result)
    payload["metadata"] = {"schema_version": "1.0", "contract": EXTERNAL_TOOL_ADAPTER_RESULT_CONTRACT}
    return payload


def _utc_seconds(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _build_request(context: EvidenceContext) -> dict[str, Any]:
    assumptions = [dict(item) for item in context.typed_assumptions]
    return build_evidence_request(
        source={
            "logical_id": context.source_logical_id,
            "file": context.source_file,
            "label": context.source_label,
            "digest": hashlib.sha256(context.source_bytes).hexdigest(),
            "spans": [dict(item) for item in context.source_spans],
            "parser_version": context.parser_version,
        },
        obligation={"digest": context.obligation_digest, "target": context.normalized_target},
        branch={"id": context.branch_id, "lineage": list(context.branch_lineage)},
        typed_assumptions=assumptions,
        assumption_digest=content_digest(assumptions),
        native_input={
            "digest": hashlib.sha256(context.native_input_bytes).hexdigest(),
            "media_type": context.native_input_media_type,
        },
        tool={
            "name": context.tool_name,
            "adapter_version": context.adapter_version,
            "backend_version": context.backend_version,
            "executable_id": context.executable_id,
        },
        resource_limits={"timeout_ms": context.timeout_ms, "max_output_bytes": context.max_output_bytes},
        expected_result_class=context.expected_result_class,
        backend_role=context.backend_role,
        unsupported_conclusions=list(context.unsupported_conclusions),
        policy_version=context.policy_version,
    )


def _prepare_evidence(
    context: EvidenceContext | None,
    artifact_root: str | Path | None,
    *,
    expected_tool: str,
) -> _PreparedEvidence | None:
    if context is None or artifact_root is None:
        return None
    if context.tool_name != expected_tool:
        raise ValueError(f"EvidenceContext tool {context.tool_name!r} does not match adapter tool {expected_tool!r}")
    request = _build_request(context)
    bundle = create_run_bundle(artifact_root)
    execution = allocate_execution(bundle, request)
    native = atomic_write_artifact(
        bundle,
        f"{execution.logical_root}/native-input.bin",
        context.native_input_bytes,
        media_type=context.native_input_media_type,
        role="native_input",
    )
    return _PreparedEvidence(bundle, execution, request, native)


def _bounded(data: bytes, maximum: int) -> tuple[bytes, bool]:
    if len(data) <= maximum:
        return data, False
    return data[:maximum], True


def _outcome(status: str) -> str:
    if status == "integrity_error":
        return "integrity_error"
    if status in {"proved", "verified"}:
        return "certified"
    if status in {"refuted", "counterexample_found", "mismatch"}:
        return "refuted"
    if "timeout" in status:
        return "timeout"
    if status in {"backend_unavailable", "unavailable"}:
        return "unavailable"
    if status in {"not_encodable", "translation_error", "missing_assumptions"}:
        return "translation_error"
    if status in {"adapter_error", "execution_error"}:
        return "execution_error"
    return "unknown"


def _seal_prepared(
    prepared: _PreparedEvidence | None,
    context: EvidenceContext | None,
    raw_result: dict[str, Any],
    *,
    status: str,
    reason: str,
    started: datetime,
    ended: datetime,
    wall_time_ns: int,
) -> dict[str, Any] | None:
    if prepared is None or context is None:
        return None
    execution_status = status
    stdout_bytes, stdout_truncated = _bounded((reason + "\n").encode("utf-8"), context.max_output_bytes)
    stderr_text = reason if status == "adapter_error" else ""
    stderr_bytes, stderr_truncated = _bounded(stderr_text.encode("utf-8"), context.max_output_bytes)
    try:
        structured_full = json.dumps(
            raw_result,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        structured_full = json.dumps(
            {"status": "integrity_error", "reason": f"raw result was not strict JSON: {type(exc).__name__}"},
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        status = "integrity_error"
    structured_bytes = structured_full
    structured_role = "structured_result"
    structured_media_type = "application/json"
    integrity_blockers: list[str] = []
    if len(structured_full) > context.max_output_bytes:
        structured_bytes = structured_full[: context.max_output_bytes]
        structured_role = "structured_result_truncated"
        structured_media_type = "application/octet-stream"
        integrity_blockers.append("structured_result_truncated")
        status = "integrity_error"
    stdout = atomic_write_artifact(
        prepared.bundle,
        f"{prepared.execution.logical_root}/stdout.txt",
        stdout_bytes,
        media_type="text/plain",
        role="stdout",
    )
    stderr = atomic_write_artifact(
        prepared.bundle,
        f"{prepared.execution.logical_root}/stderr.txt",
        stderr_bytes,
        media_type="text/plain",
        role="stderr",
    )
    structured = atomic_write_artifact(
        prepared.bundle,
        f"{prepared.execution.logical_root}/result.json",
        structured_bytes,
        media_type=structured_media_type,
        role=structured_role,
    )
    timed_out = "timeout" in execution_status
    execution_record = {
        "started_at_utc": _utc_seconds(started),
        "ended_at_utc": _utc_seconds(ended),
        "wall_time_ns": wall_time_ns,
        "exit_classification": "timed_out" if timed_out else "runner_exception" if execution_status == "adapter_error" else "completed",
        "exit_code": None if timed_out or execution_status == "adapter_error" else 0,
        "signal": None,
        "timeout": timed_out,
        "device_execution": {"mode": "cpu_test_double", "gpu_requested": False, "gpu_initialized": False},
        "environment": {
            "python_implementation": platform.python_implementation(),
            "python_version": platform.python_version(),
            "platform_system": platform.system(),
            "test_runner_version": "p01-fake-runner",
        },
        "runner_version": context.adapter_version,
    }
    result_record = {
        "outcome": _outcome(status),
        "stdout": stdout,
        "stderr": stderr,
        "structured_result": structured,
        "stdout_truncated": stdout_truncated,
        "stderr_truncated": stderr_truncated,
        "redaction": {"applied": False, "fields": []},
        "certificate": None,
    }
    interpretation = {
        "certified_scope": "synthetic fixture only" if result_record["outcome"] == "certified" else None,
        "refuted_scope": "synthetic fixture only" if result_record["outcome"] == "refuted" else None,
        "unresolved_assumption_ids": [],
        "blocker_ids": integrity_blockers,
        "veto_ids": integrity_blockers,
        "non_claims": list(context.unsupported_conclusions),
    }
    sealed = seal_attempt_manifest(
        prepared.bundle,
        prepared.request,
        prepared.execution,
        [prepared.native_artifact, stdout, stderr, structured],
        execution_record=execution_record,
        result_record=result_record,
        interpretation=interpretation,
    )
    verified = verify_attempt_manifest(prepared.bundle.root, sealed["manifest_ref"])
    return {
        "schema_version": "1.0",
        "binding_status": "verified_manifest",
        "run_id": prepared.bundle.run_id,
        "request_digest": prepared.execution.request_digest,
        "attempt_id": prepared.execution.attempt_id,
        "execution_id": prepared.execution.execution_id,
        "manifest_ref": f"{prepared.bundle.run_id}/{sealed['manifest_ref']}",
        "manifest_sha256": verified["manifest_sha256"],
        "integrity_state": "verified",
        "claim_eligibility": "ineligible",
        "publication_enabled": False,
    }


def _derive_status_mapping(result: dict[str, Any], *, tool: str) -> tuple[str, str, str]:
    status = str(result.get("status", "unknown"))
    if status == "proved":
        return "proved", "certifying_backend", "certified"
    if status == "refuted":
        counterexample_search = result.get("counterexample_search")
        if isinstance(counterexample_search, dict) and counterexample_search.get("counterexample"):
            return "counterexample_found", "counterexample", "counterexample"
        return "refuted", "scoped_contradiction", "refuting"
    if status in {"backend_unavailable", "not_encodable", "missing_assumptions"}:
        return status, "diagnostic", "diagnostic"
    if status == "adapter_error":
        return status, "diagnostic", "diagnostic"
    return status if status else "unknown", "diagnostic", "diagnostic"


def adapt_algebra_check(
    target: str,
    *,
    lhs: str | None = None,
    rhs: str | None = None,
    tool: str = "sympy",
    timeout_seconds: float | None = None,
    runner: Callable[..., dict[str, Any]] | None = None,
    evidence_context: EvidenceContext | None = None,
    artifact_root: str | Path | None = None,
) -> dict[str, Any]:
    """Run or wrap a scoped algebra derivation/refutation attempt."""
    prepared = _prepare_evidence(evidence_context, artifact_root, expected_tool=tool)
    started = datetime.now(timezone.utc)
    start_ns = time.monotonic_ns()
    call = runner or derive_or_refute
    try:
        result = call(target, lhs=lhs, rhs=rhs, backend=tool)
    except Exception as exc:
        result = _exception_payload(tool, exc)
    ended = datetime.now(timezone.utc)
    wall_time_ns = time.monotonic_ns() - start_ns
    status, evidence_kind, certification_status = _derive_status_mapping(result, tool=tool)
    output_ref = _stable_ref(tool, result, fallback=status) if evidence_kind != "diagnostic" else None
    attempt = _attempt(
        attempt_id=f"{tool}_algebra_attempt",
        tool=tool,
        status=status,
        evidence_kind=evidence_kind,
        certification_status=certification_status,
        input_summary=target,
        output_ref=output_ref,
        timeout_seconds=timeout_seconds,
    )
    attachment = _seal_prepared(
        prepared,
        evidence_context,
        result,
        status=status,
        reason=str(result.get("reason", "Adapter produced a bounded algebra attempt.")),
        started=started,
        ended=ended,
        wall_time_ns=wall_time_ns,
    )
    attempt["evidence_schema_version"] = "1.0" if attachment else "0-legacy"
    attempt["evidence_binding"] = "verified_manifest" if attachment else "unbound_legacy_evidence"
    if attachment:
        attempt["evidence_attachment"] = attachment
        attempt["output_ref"] = attachment["manifest_ref"]
    return _adapter_result(
        status=status,
        reason=str(result.get("reason", "Adapter produced a bounded algebra attempt.")),
        attempt=attempt,
        raw_result=result,
        evidence_attachment=attachment,
    )


def _counterexample_status_mapping(result: dict[str, Any]) -> tuple[str, str, str]:
    status = str(result.get("status", "unknown"))
    if status == "refuted" and result.get("counterexample"):
        return "counterexample_found", "counterexample", "counterexample"
    if status in {"backend_unavailable", "not_encodable", "unknown", "adapter_error"}:
        return status, "diagnostic", "diagnostic"
    return status, "diagnostic", "diagnostic"


def adapt_counterexample_search(
    lhs: str,
    rhs: str,
    *,
    timeout_seconds: float | None = None,
    runner: Callable[..., dict[str, Any]] | None = None,
    evidence_context: EvidenceContext | None = None,
    artifact_root: str | Path | None = None,
) -> dict[str, Any]:
    """Run or wrap bounded counterexample search evidence."""
    expected_tool = evidence_context.tool_name if evidence_context is not None else "counterexample"
    prepared = _prepare_evidence(evidence_context, artifact_root, expected_tool=expected_tool)
    started = datetime.now(timezone.utc)
    start_ns = time.monotonic_ns()
    call = runner or find_counterexample
    try:
        result = call(lhs, rhs)
    except Exception as exc:
        result = _exception_payload("counterexample", exc)
    ended = datetime.now(timezone.utc)
    wall_time_ns = time.monotonic_ns() - start_ns
    status, evidence_kind, certification_status = _counterexample_status_mapping(result)
    output_ref = _stable_ref("counterexample", result, fallback=status) if evidence_kind == "counterexample" else None
    attempt = _attempt(
        attempt_id="bounded_counterexample_attempt",
        tool=str(result.get("backend", "bounded_counterexample")) if isinstance(result, dict) else "bounded_counterexample",
        status=status,
        evidence_kind=evidence_kind,
        certification_status=certification_status,
        input_summary=f"{lhs} = {rhs}",
        output_ref=output_ref,
        timeout_seconds=timeout_seconds,
    )
    attachment = _seal_prepared(
        prepared,
        evidence_context,
        result,
        status=status,
        reason=str(result.get("reason", "Adapter produced a bounded counterexample attempt.")),
        started=started,
        ended=ended,
        wall_time_ns=wall_time_ns,
    )
    attempt["evidence_schema_version"] = "1.0" if attachment else "0-legacy"
    attempt["evidence_binding"] = "verified_manifest" if attachment else "unbound_legacy_evidence"
    if attachment:
        attempt["evidence_attachment"] = attachment
        attempt["output_ref"] = attachment["manifest_ref"]
    return _adapter_result(
        status=status,
        reason=str(result.get("reason", "Adapter produced a bounded counterexample attempt.")),
        attempt=attempt,
        raw_result=result,
        evidence_attachment=attachment,
    )


def _lean_status_mapping(
    result: dict[str, Any], *, exact_live_certificate: bool
) -> tuple[str, str, str]:
    status = str(result.get("status", "inconclusive"))
    if status == "verified" and exact_live_certificate:
        return "proved", "lean_check", "certified"
    # A source-only acceptance or rejected proof term is diagnostic, not a
    # certificate or a refutation of the theorem. source_status preserves the
    # raw backend label in the enclosing adapter result.
    return "diagnostic", "diagnostic", "diagnostic"


def _lean_context_matches_binding(
    context: EvidenceContext | None,
    source: str,
    validation: dict[str, Any] | None,
) -> bool:
    if context is None or validation is None or not validation.get("can_certify"):
        return False
    record = validation["record"]
    return bool(
        context.tool_name == "lean"
        and context.branch_id == record["branch_id"]
        and " ".join(context.normalized_target.split()) == record["normalized_target"]
        and context.native_input_bytes == source.encode("utf-8")
        and [dict(item) for item in context.typed_assumptions] == record["typed_assumptions"]
        and os.path.realpath(context.executable_id) == record["executable_path"]
        and context.backend_version == record["executable_version"]
    )


def adapt_lean_check(
    source: str,
    *,
    timeout_seconds: float | None = None,
    allow_sorry: bool = False,
    runner: Callable[..., dict[str, Any]] | None = None,
    target_binding: LeanTargetBinding | None = None,
    evidence_context: EvidenceContext | None = None,
    artifact_root: str | Path | None = None,
) -> dict[str, Any]:
    """Run or wrap direct Lean checking as the final formal certificate route."""
    prepared = _prepare_evidence(evidence_context, artifact_root, expected_tool="lean")
    started = datetime.now(timezone.utc)
    start_ns = time.monotonic_ns()
    binding_validation = (
        validate_lean_target_binding(source, target_binding)
        if target_binding is not None
        else None
    )
    call = runner or check_lean_source
    try:
        if binding_validation is not None and not binding_validation["can_certify"]:
            result = {
                "status": "binding_error",
                "reason": "Lean target binding failed: " + "; ".join(binding_validation["errors"]),
                "metadata": {"schema_version": "1.0", "contract": "p05_lean_target_binding_error"},
            }
        elif runner is not None:
            result = call(
                source,
                timeout_seconds=int(timeout_seconds or 10),
                allow_sorry=allow_sorry,
            )
        elif target_binding is not None:
            result = call(
                source,
                timeout_seconds=int(timeout_seconds or 10),
                allow_sorry=allow_sorry,
                executable=target_binding.executable_path,
                project_root=target_binding.project_root,
                lean_toolchain=target_binding.lean_toolchain,
            )
        else:
            result = call(
                source,
                timeout_seconds=int(timeout_seconds or 10),
                allow_sorry=allow_sorry,
            )
    except Exception as exc:
        result = _exception_payload("lean", exc)
    ended = datetime.now(timezone.utc)
    wall_time_ns = time.monotonic_ns() - start_ns
    execution_matches = bool(
        runner is None
        and binding_validation is not None
        and binding_validation.get("can_certify")
        and lean_execution_matches_binding(result, binding_validation["record"])
        and _lean_context_matches_binding(evidence_context, source, binding_validation)
    )
    candidate_status, _, _ = _lean_status_mapping(
        result, exact_live_certificate=execution_matches
    )
    output_ref = None
    attempt = _attempt(
        attempt_id="lean_check_attempt",
        tool="lean",
        status=candidate_status,
        evidence_kind="diagnostic",
        certification_status="diagnostic",
        input_summary=f"Lean source sha256={hashlib.sha256(source.encode('utf-8')).hexdigest()}",
        output_ref=output_ref,
        timeout_seconds=timeout_seconds,
    )
    attachment = _seal_prepared(
        prepared,
        evidence_context,
        result,
        status=candidate_status,
        reason=str(result.get("reason", "Adapter produced a bounded Lean attempt.")),
        started=started,
        ended=ended,
        wall_time_ns=wall_time_ns,
    )
    exact_live_certificate = execution_matches and attachment is not None
    status, evidence_kind, certification_status = _lean_status_mapping(
        result, exact_live_certificate=exact_live_certificate
    )
    attempt["status"] = status
    attempt["evidence_kind"] = evidence_kind
    attempt["certification_status"] = certification_status
    attempt["evidence_schema_version"] = "1.0" if attachment else "0-legacy"
    attempt["evidence_binding"] = "verified_manifest" if attachment else "unbound_legacy_evidence"
    attempt["lean_target_binding"] = binding_validation
    attempt["live_execution_binding_verified"] = execution_matches
    if attachment:
        attempt["evidence_attachment"] = attachment
        attempt["output_ref"] = attachment["manifest_ref"]
    payload = _adapter_result(
        status=status,
        reason=str(result.get("reason", "Adapter produced a bounded Lean attempt.")),
        attempt=attempt,
        raw_result=result,
        evidence_attachment=attachment,
    )
    payload["lean_target_binding"] = binding_validation
    payload["live_execution_binding_verified"] = execution_matches
    return payload


def diagnostic_external_attempt(
    *,
    tool: str,
    input_summary: str,
    evidence_kind: str,
    status: str,
    reason: str,
    output_ref: str | None = None,
    version: str | None = None,
    timeout_seconds: float | None = None,
) -> dict[str, Any]:
    """Create evidence-only attempts for retrieval/static/proof-state adapters."""
    attempt = _attempt(
        attempt_id=f"{tool}_{evidence_kind}_attempt",
        tool=tool,
        status=status,
        evidence_kind=evidence_kind,
        certification_status="diagnostic",
        input_summary=input_summary,
        output_ref=output_ref,
        timeout_seconds=timeout_seconds,
        version=version,
    )
    raw = {
        "status": status,
        "reason": reason,
        "metadata": {"schema_version": "1.0", "contract": f"{tool}_{evidence_kind}_diagnostic"},
    }
    return _adapter_result(status=status, reason=reason, attempt=attempt, raw_result=raw)


def adapt_retrieval_evidence(
    *,
    tool: str,
    query: str,
    hits: list[dict[str, Any]] | None = None,
    version: str | None = None,
    lean_context: LeanDiagnosticContext | None = None,
) -> dict[str, Any]:
    """Record LeanSearch/LeanExplore premise retrieval as evidence-only."""
    precondition = (
        validate_lean_diagnostic_context(lean_context)
        if lean_context is not None
        else None
    )
    allowed = bool(precondition and precondition["can_execute_diagnostic_route"])
    hit_count = len(hits or []) if allowed else 0
    result = diagnostic_external_attempt(
        tool=tool,
        input_summary=query,
        evidence_kind="retrieval",
        status="retrieved" if hit_count else "precondition_missing" if precondition is None else "precondition_invalid" if not allowed else "no_hits",
        reason=(
            f"{tool} returned {hit_count} premise/declaration candidates. Retrieval is not proof."
            if allowed
            else f"{tool} retrieval was not executed because a verified local Lean goal context is required."
        ),
        output_ref=f"mathdevmcp://retrieval/{tool}/{hit_count}" if hit_count else None,
        version=version,
    )
    result["execution_mode"] = "record_only"
    result["can_promote"] = False
    result["lean_precondition"] = precondition
    return result


def adapt_static_extraction_evidence(
    *,
    tool: str = "jixia",
    target: str,
    extracted: dict[str, Any] | None = None,
    version: str | None = None,
    lean_context: LeanDiagnosticContext | None = None,
) -> dict[str, Any]:
    """Record static Lean source extraction as evidence-only."""
    precondition = (
        validate_lean_diagnostic_context(lean_context)
        if lean_context is not None
        else None
    )
    allowed = bool(precondition and precondition["can_execute_diagnostic_route"])
    result = diagnostic_external_attempt(
        tool=tool,
        input_summary=target,
        evidence_kind="static_extraction",
        status="extracted" if allowed and extracted else "precondition_missing" if precondition is None else "precondition_invalid" if not allowed else "not_extracted",
        reason=(
            f"{tool} static extraction is diagnostic unless followed by a certifying backend check."
            if allowed
            else f"{tool} static extraction was not executed because a verified local Lean file/goal context is required."
        ),
        output_ref=f"mathdevmcp://static-extraction/{tool}" if allowed and extracted else None,
        version=version,
    )
    result["execution_mode"] = "record_only"
    result["can_promote"] = False
    result["lean_precondition"] = precondition
    return result


def adapt_proof_state_evidence(
    *,
    tool: str,
    target: str,
    trace: list[dict[str, Any]] | None = None,
    version: str | None = None,
    timeout_seconds: float | None = None,
    lean_context: LeanDiagnosticContext | None = None,
) -> dict[str, Any]:
    """Record Pantograph/LeanDojo proof-state interaction as evidence-only."""
    precondition = (
        validate_lean_diagnostic_context(lean_context)
        if lean_context is not None
        else None
    )
    allowed = bool(precondition and precondition["can_execute_diagnostic_route"])
    trace_count = len(trace or []) if allowed else 0
    result = diagnostic_external_attempt(
        tool=tool,
        input_summary=target,
        evidence_kind="proof_state",
        status="explored" if trace_count else "precondition_missing" if precondition is None else "precondition_invalid" if not allowed else "not_explored",
        reason=(
            f"{tool} proof-state traces are diagnostic until direct Lean verification succeeds."
            if allowed
            else f"{tool} proof-state interaction was not executed because a verified local Lean goal context is required."
        ),
        output_ref=f"mathdevmcp://proof-state/{tool}/{trace_count}" if trace_count else None,
        version=version,
        timeout_seconds=timeout_seconds,
    )
    result["execution_mode"] = "record_only"
    result["can_promote"] = False
    result["lean_precondition"] = precondition
    return result
