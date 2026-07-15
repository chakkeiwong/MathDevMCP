from __future__ import annotations

"""Closed Phase 05 contract for executable external-tool evidence."""

from copy import deepcopy
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

from .evidence_manifest import canonical_json_bytes, content_digest


P05_ADAPTER_REQUEST_SCHEMA = "p05_external_adapter_request@1"
P05_ADAPTER_RESULT_SCHEMA = "p05_external_adapter_result@1"
P06_NORMALIZED_CLAIM_EVIDENCE_SCHEMA = "p06_normalized_claim_evidence@1"
P06_CLAIM_EVIDENCE_VERIFIER_VERSION = "p06-claim-evidence-normalizer@1"
P06_GENERIC_REVALIDATION_READER = "generic_v1_manifest"
P06_REGISTERED_REVALIDATION_READER = "registered_external_adapter"
P05_ADAPTER_BOUNDARY = (
    "An adapter result records one exact tool action. Certification or "
    "refutation is promotable only when a real tool execution and a verified "
    "manifest are bound to the exact branch request and native input."
)

P05_ADAPTER_STATUSES = frozenset(
    {
        "certified",
        "refuted",
        "diagnostic",
        "unsupported",
        "unavailable",
        "translation_error",
        "execution_error",
        "timeout",
        "malformed_output",
        "truncated_output",
    }
)
P05_EXECUTION_KINDS = frozenset(
    {"not_run", "record_only", "fake_runner", "python_library", "subprocess"}
)
P05_NON_PROMOTING_STATUSES = P05_ADAPTER_STATUSES - {"certified", "refuted"}

_SHA256_KEYS = {
    "request_digest",
    "native_input_digest",
    "stdout_sha256",
    "stderr_sha256",
    "manifest_sha256",
}
_REQUEST_KEYS = {
    "schema_version",
    "branch_id",
    "branch_lineage",
    "obligation_digest",
    "normalized_target",
    "typed_assumptions",
    "native_input_digest",
    "native_input_media_type",
    "tool",
    "resource_limits",
    "expected_result_class",
    "backend_role",
    "unsupported_conclusions",
    "request_digest",
}
_TOOL_KEYS = {
    "name",
    "adapter_version",
    "backend_version",
    "requested_executable",
    "resolved_executable",
}
_RESOURCE_KEYS = {"timeout_ms", "max_output_bytes", "max_artifact_bytes"}
_RESULT_KEYS = {
    "schema_version",
    "status",
    "reason",
    "request",
    "execution",
    "evidence",
    "next_discriminator",
    "non_claims",
    "live_tool_executed",
    "can_promote",
    "publication_enabled",
    "boundary",
    "result_digest",
}
_EXECUTION_KEYS = {
    "kind",
    "runner_id",
    "command",
    "executable_path",
    "resolved_executable_path",
    "exit_code",
    "timed_out",
    "stdout_bytes",
    "stderr_bytes",
    "stdout_sha256",
    "stderr_sha256",
}
_EVIDENCE_KEYS = {
    "evidence_kind",
    "details",
    "output_ref",
    "manifest_ref",
    "manifest_sha256",
    "manifest_verified",
    "refutation_witness",
}
_P06_NORMALIZED_KEYS = {
    "schema_version",
    "manifest_family",
    "manifest_version",
    "manifest_ref",
    "manifest_sha256",
    "native_reader",
    "verifier_version",
    "integrity_state",
    "branch",
    "obligation",
    "typed_assumptions",
    "typed_assumption_digests",
    "assumption_encoding",
    "native_input",
    "tool",
    "backend_role",
    "accepted_input_class",
    "resource_limits",
    "execution",
    "outcome",
    "witness",
    "evidence_refs",
    "non_claims",
    "certifying",
    "normalization_digest",
}


class ExternalAdapterContractError(ValueError):
    """Raised when a Phase 05 adapter record violates the closed contract."""


@dataclass(frozen=True, slots=True)
class RevalidatingClaimEvidence:
    """Immutable native-reader inputs; constructing this object grants no authority."""

    reader: str
    _input_bytes: bytes = field(repr=False)

    def __init__(self, *, reader: str, inputs: Mapping[str, Any]) -> None:
        expected_keys = {
            P06_GENERIC_REVALIDATION_READER: {
                "artifact_root",
                "manifest_ref",
                "p04_branch",
                "p04_request",
                "p04_result",
            },
            P06_REGISTERED_REVALIDATION_READER: {
                "adapter_result",
                "p04_branch",
                "p04_request",
                "p04_result",
            },
        }
        if reader not in expected_keys:
            raise ExternalAdapterContractError(
                f"unregistered claim-evidence reader: {reader!r}"
            )
        if not isinstance(inputs, Mapping) or set(inputs) != expected_keys[reader]:
            raise ExternalAdapterContractError(
                "claim-evidence revalidation inputs do not match the reader"
            )
        object.__setattr__(self, "reader", reader)
        object.__setattr__(
            self,
            "_input_bytes",
            json.dumps(
                dict(inputs),
                allow_nan=False,
                ensure_ascii=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8"),
        )

    def __deepcopy__(self, memo: dict[int, Any]) -> RevalidatingClaimEvidence:
        _ = memo
        return self


def reader_verified_claim_evidence_record(value: Any) -> dict[str, Any]:
    """Rerun the registered native reader; the request itself has no authority."""
    if not isinstance(value, RevalidatingClaimEvidence):
        raise ExternalAdapterContractError(
            "normalized claim evidence has no reader authority; a native-reader "
            "revalidation request is required"
        )
    try:
        inputs = json.loads(value._input_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExternalAdapterContractError(
            "claim-evidence revalidation inputs are invalid"
        ) from exc
    if value.reader == P06_GENERIC_REVALIDATION_READER:
        return normalize_generic_v1_claim_evidence(
            artifact_root=inputs["artifact_root"],
            manifest_ref=inputs["manifest_ref"],
            p04_branch=inputs["p04_branch"],
            p04_request=inputs["p04_request"],
            p04_result=inputs["p04_result"],
        )
    if value.reader == P06_REGISTERED_REVALIDATION_READER:
        return normalize_registered_adapter_claim_evidence(
            adapter_result=inputs["adapter_result"],
            p04_branch=inputs["p04_branch"],
            p04_request=inputs["p04_request"],
            p04_result=inputs["p04_result"],
        )
    raise ExternalAdapterContractError(
        f"unregistered claim-evidence reader: {value.reader!r}"
    )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _require_exact_keys(value: Mapping[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        missing = sorted(expected - set(value))
        extra = sorted(set(value) - expected)
        raise ExternalAdapterContractError(
            f"{label} keys mismatch; missing={missing}, extra={extra}"
        )


def _require_string(value: Any, label: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value):
        raise ExternalAdapterContractError(f"{label} must be a non-empty string")
    return value


def _require_sha256(value: Any, label: str, *, optional: bool = False) -> str | None:
    if optional and value is None:
        return None
    text = _require_string(value, label)
    if len(text) != 64 or any(char not in "0123456789abcdef" for char in text):
        raise ExternalAdapterContractError(f"{label} must be a lowercase SHA-256 digest")
    return text


def _strict_real_path(value: str | None, label: str) -> str | None:
    if value is None:
        return None
    text = _require_string(value, label)
    path = Path(text)
    if not path.is_absolute():
        raise ExternalAdapterContractError(f"{label} must be absolute")
    return os.path.realpath(text)


def build_external_adapter_request(
    *,
    branch_id: str,
    branch_lineage: list[str] | tuple[str, ...],
    obligation_digest: str,
    normalized_target: str,
    typed_assumptions: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    native_input_bytes: bytes,
    native_input_media_type: str,
    tool_name: str,
    adapter_version: str,
    backend_version: str,
    requested_executable: str | None,
    resolved_executable: str | None,
    timeout_ms: int,
    max_output_bytes: int,
    max_artifact_bytes: int,
    expected_result_class: str,
    backend_role: str,
    unsupported_conclusions: list[str] | tuple[str, ...],
) -> dict[str, Any]:
    """Build a canonical request whose digest covers every decision-relevant field."""
    if not isinstance(native_input_bytes, bytes):
        raise ExternalAdapterContractError("native_input_bytes must be bytes")
    record = {
        "schema_version": P05_ADAPTER_REQUEST_SCHEMA,
        "branch_id": branch_id,
        "branch_lineage": list(branch_lineage),
        "obligation_digest": obligation_digest,
        "normalized_target": normalized_target,
        "typed_assumptions": deepcopy(list(typed_assumptions)),
        "native_input_digest": _sha256(native_input_bytes),
        "native_input_media_type": native_input_media_type,
        "tool": {
            "name": tool_name,
            "adapter_version": adapter_version,
            "backend_version": backend_version,
            "requested_executable": requested_executable,
            "resolved_executable": resolved_executable,
        },
        "resource_limits": {
            "timeout_ms": timeout_ms,
            "max_output_bytes": max_output_bytes,
            "max_artifact_bytes": max_artifact_bytes,
        },
        "expected_result_class": expected_result_class,
        "backend_role": backend_role,
        "unsupported_conclusions": list(unsupported_conclusions),
    }
    record["request_digest"] = content_digest(record)
    return validate_external_adapter_request(record)


def validate_external_adapter_request(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ExternalAdapterContractError("adapter request must be an object")
    record = deepcopy(dict(value))
    _require_exact_keys(record, _REQUEST_KEYS, "adapter request")
    if record["schema_version"] != P05_ADAPTER_REQUEST_SCHEMA:
        raise ExternalAdapterContractError("adapter request schema_version is invalid")
    _require_string(record["branch_id"], "branch_id")
    lineage = record["branch_lineage"]
    if (
        not isinstance(lineage, list)
        or not lineage
        or any(not isinstance(item, str) or not item for item in lineage)
        or lineage[-1] != record["branch_id"]
        or len(lineage) != len(set(lineage))
    ):
        raise ExternalAdapterContractError(
            "branch_lineage must be a unique non-empty path ending at branch_id"
        )
    _require_sha256(record["obligation_digest"], "obligation_digest")
    _require_string(record["normalized_target"], "normalized_target")
    assumptions = record["typed_assumptions"]
    if not isinstance(assumptions, list) or any(not isinstance(item, dict) for item in assumptions):
        raise ExternalAdapterContractError("typed_assumptions must be a list of objects")
    canonical_json_bytes(assumptions)
    _require_sha256(record["native_input_digest"], "native_input_digest")
    _require_string(record["native_input_media_type"], "native_input_media_type")

    tool = record["tool"]
    if not isinstance(tool, Mapping):
        raise ExternalAdapterContractError("tool must be an object")
    _require_exact_keys(tool, _TOOL_KEYS, "tool")
    for key in ("name", "adapter_version", "backend_version"):
        _require_string(tool[key], f"tool.{key}")
    requested = _strict_real_path(tool["requested_executable"], "tool.requested_executable")
    resolved = _strict_real_path(tool["resolved_executable"], "tool.resolved_executable")
    if requested is not None and resolved is not None and requested != resolved:
        raise ExternalAdapterContractError(
            "requested executable does not resolve to tool.resolved_executable"
        )

    limits = record["resource_limits"]
    if not isinstance(limits, Mapping):
        raise ExternalAdapterContractError("resource_limits must be an object")
    _require_exact_keys(limits, _RESOURCE_KEYS, "resource_limits")
    for key in _RESOURCE_KEYS:
        item = limits[key]
        if not isinstance(item, int) or isinstance(item, bool) or item <= 0:
            raise ExternalAdapterContractError(f"resource_limits.{key} must be positive")
    for key in ("expected_result_class", "backend_role"):
        _require_string(record[key], key)
    nonclaims = record["unsupported_conclusions"]
    if (
        not isinstance(nonclaims, list)
        or not nonclaims
        or any(not isinstance(item, str) or not item for item in nonclaims)
        or len(nonclaims) != len(set(nonclaims))
    ):
        raise ExternalAdapterContractError(
            "unsupported_conclusions must be a unique non-empty list of strings"
        )
    request_digest = record.pop("request_digest")
    _require_sha256(request_digest, "request_digest")
    if request_digest != content_digest(record):
        raise ExternalAdapterContractError("adapter request digest mismatch")
    record["request_digest"] = request_digest
    return record


def _validate_execution(execution: Any, request: Mapping[str, Any]) -> tuple[dict[str, Any], bool]:
    if not isinstance(execution, Mapping):
        raise ExternalAdapterContractError("execution must be an object")
    record = deepcopy(dict(execution))
    _require_exact_keys(record, _EXECUTION_KEYS, "execution")
    kind = record["kind"]
    if kind not in P05_EXECUTION_KINDS:
        raise ExternalAdapterContractError(f"unknown execution kind: {kind!r}")
    _require_string(record["runner_id"], "execution.runner_id")
    command = record["command"]
    if not isinstance(command, list) or any(not isinstance(item, str) or not item for item in command):
        raise ExternalAdapterContractError("execution.command must be a list of non-empty strings")
    executable = _strict_real_path(record["executable_path"], "execution.executable_path")
    resolved = _strict_real_path(
        record["resolved_executable_path"], "execution.resolved_executable_path"
    )
    if executable is not None and resolved is not None and executable != resolved:
        raise ExternalAdapterContractError("execution executable path mismatch")
    for key in ("stdout_bytes", "stderr_bytes"):
        item = record[key]
        if not isinstance(item, int) or isinstance(item, bool) or item < 0:
            raise ExternalAdapterContractError(f"execution.{key} must be non-negative")
    _require_sha256(record["stdout_sha256"], "execution.stdout_sha256", optional=True)
    _require_sha256(record["stderr_sha256"], "execution.stderr_sha256", optional=True)
    if not isinstance(record["timed_out"], bool):
        raise ExternalAdapterContractError("execution.timed_out must be boolean")
    if record["exit_code"] is not None and (
        not isinstance(record["exit_code"], int) or isinstance(record["exit_code"], bool)
    ):
        raise ExternalAdapterContractError("execution.exit_code must be an integer or null")
    if record["stdout_bytes"] + record["stderr_bytes"] > request["resource_limits"]["max_output_bytes"]:
        raise ExternalAdapterContractError("aggregate output byte count exceeds the request limit")

    tool = request["tool"]
    live = kind in {"python_library", "subprocess"}
    if kind == "subprocess":
        if not command or executable is None or resolved is None:
            raise ExternalAdapterContractError(
                "subprocess evidence requires command and exact executable paths"
            )
        if os.path.realpath(command[0]) != resolved:
            raise ExternalAdapterContractError("subprocess command executable mismatch")
        if tool["resolved_executable"] is None or os.path.realpath(tool["resolved_executable"]) != resolved:
            raise ExternalAdapterContractError("subprocess executable does not match tool identity")
    elif kind == "python_library":
        if command:
            raise ExternalAdapterContractError("python_library execution must not claim a subprocess command")
        if tool["requested_executable"] is not None or executable is not None or resolved is not None:
            raise ExternalAdapterContractError(
                "python_library execution must not claim executable-process evidence"
            )
    else:
        if command or executable is not None or resolved is not None or record["exit_code"] is not None:
            raise ExternalAdapterContractError(
                f"{kind} execution cannot carry process provenance"
            )
        if record["timed_out"]:
            raise ExternalAdapterContractError(f"{kind} execution cannot claim a process timeout")
        live = False
    return record, live


def build_external_adapter_result(
    *,
    request: Mapping[str, Any],
    status: str,
    reason: str,
    execution: Mapping[str, Any],
    evidence_kind: str,
    evidence_details: Mapping[str, Any] | None,
    output_ref: str | None,
    manifest_ref: str | None,
    manifest_sha256: str | None,
    manifest_verified: bool,
    refutation_witness: Mapping[str, Any] | None,
    next_discriminator: str,
    non_claims: list[str] | tuple[str, ...],
) -> dict[str, Any]:
    record = {
        "schema_version": P05_ADAPTER_RESULT_SCHEMA,
        "status": status,
        "reason": reason,
        "request": validate_external_adapter_request(request),
        "execution": deepcopy(dict(execution)),
        "evidence": {
            "evidence_kind": evidence_kind,
            "details": deepcopy(dict(evidence_details))
            if evidence_details is not None
            else None,
            "output_ref": output_ref,
            "manifest_ref": manifest_ref,
            "manifest_sha256": manifest_sha256,
            "manifest_verified": manifest_verified,
            "refutation_witness": deepcopy(dict(refutation_witness))
            if refutation_witness is not None
            else None,
        },
        "next_discriminator": next_discriminator,
        "non_claims": list(non_claims),
        "live_tool_executed": False,
        "can_promote": False,
        "publication_enabled": False,
        "boundary": P05_ADAPTER_BOUNDARY,
    }
    execution_record, live = _validate_execution(record["execution"], record["request"])
    record["execution"] = execution_record
    record["live_tool_executed"] = live
    record["can_promote"] = bool(
        status in {"certified", "refuted"}
        and live
        and manifest_verified
        and isinstance(output_ref, str)
        and output_ref
    )
    record["result_digest"] = content_digest(record)
    return validate_external_adapter_result(record)


def validate_external_adapter_result(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ExternalAdapterContractError("adapter result must be an object")
    record = deepcopy(dict(value))
    _require_exact_keys(record, _RESULT_KEYS, "adapter result")
    if record["schema_version"] != P05_ADAPTER_RESULT_SCHEMA:
        raise ExternalAdapterContractError("adapter result schema_version is invalid")
    if record["status"] not in P05_ADAPTER_STATUSES:
        raise ExternalAdapterContractError(f"unknown adapter status: {record['status']!r}")
    _require_string(record["reason"], "reason")
    request = validate_external_adapter_request(record["request"])
    execution, live = _validate_execution(record["execution"], request)
    record["request"] = request
    record["execution"] = execution
    if record["live_tool_executed"] is not live:
        raise ExternalAdapterContractError("live_tool_executed disagrees with execution provenance")

    evidence = record["evidence"]
    if not isinstance(evidence, Mapping):
        raise ExternalAdapterContractError("evidence must be an object")
    _require_exact_keys(evidence, _EVIDENCE_KEYS, "evidence")
    _require_string(evidence["evidence_kind"], "evidence.evidence_kind")
    details = evidence["details"]
    if details is not None:
        if not isinstance(details, Mapping):
            raise ExternalAdapterContractError("evidence.details must be an object or null")
        details_bytes = canonical_json_bytes(details)
        if len(details_bytes) > request["resource_limits"]["max_output_bytes"]:
            raise ExternalAdapterContractError("evidence.details exceeds the request output limit")
    for key in ("output_ref", "manifest_ref"):
        if evidence[key] is not None:
            _require_string(evidence[key], f"evidence.{key}")
    _require_sha256(
        evidence["manifest_sha256"], "evidence.manifest_sha256", optional=True
    )
    if not isinstance(evidence["manifest_verified"], bool):
        raise ExternalAdapterContractError("evidence.manifest_verified must be boolean")
    if evidence["manifest_verified"] and (
        evidence["manifest_ref"] is None or evidence["manifest_sha256"] is None
    ):
        raise ExternalAdapterContractError(
            "verified manifest evidence requires its reference and digest"
        )
    witness = evidence["refutation_witness"]
    if witness is not None:
        if not isinstance(witness, Mapping) or not witness:
            raise ExternalAdapterContractError("refutation_witness must be a non-empty object")
        canonical_json_bytes(witness)
    if record["status"] == "refuted" and witness is None:
        raise ExternalAdapterContractError("refuted status requires a concrete scoped witness")
    if record["status"] != "refuted" and witness is not None:
        raise ExternalAdapterContractError("only refuted status may carry a refutation witness")

    _require_string(record["next_discriminator"], "next_discriminator")
    nonclaims = record["non_claims"]
    if (
        not isinstance(nonclaims, list)
        or not nonclaims
        or any(not isinstance(item, str) or not item for item in nonclaims)
        or len(nonclaims) != len(set(nonclaims))
    ):
        raise ExternalAdapterContractError("non_claims must be a unique non-empty list")
    if not set(request["unsupported_conclusions"]).issubset(nonclaims):
        raise ExternalAdapterContractError(
            "result non_claims must retain every request unsupported conclusion"
        )
    if not isinstance(record["publication_enabled"], bool) or record["publication_enabled"]:
        raise ExternalAdapterContractError("Phase 05 adapter publication must remain disabled")
    if record["boundary"] != P05_ADAPTER_BOUNDARY:
        raise ExternalAdapterContractError("adapter result boundary mismatch")
    expected_can_promote = bool(
        record["status"] in {"certified", "refuted"}
        and live
        and evidence["manifest_verified"]
        and isinstance(evidence["output_ref"], str)
        and evidence["output_ref"]
    )
    if record["can_promote"] is not expected_can_promote:
        raise ExternalAdapterContractError("can_promote disagrees with evidence and execution")
    if record["status"] in P05_NON_PROMOTING_STATUSES and record["can_promote"]:
        raise ExternalAdapterContractError("a diagnostic/error status cannot promote")
    result_digest = record.pop("result_digest")
    _require_sha256(result_digest, "result_digest")
    if result_digest != content_digest(record):
        raise ExternalAdapterContractError("adapter result digest mismatch")
    record["result_digest"] = result_digest
    return record


def verify_live_adapter_manifest(value: Mapping[str, Any]) -> dict[str, Any]:
    """Independently verify the tool-specific on-disk manifest for live promotion."""
    result = validate_external_adapter_result(value)
    if result["live_tool_executed"] is not True or result["can_promote"] is not True:
        raise ExternalAdapterContractError(
            "live manifest verification requires a promotable live adapter result"
        )
    tool = result["request"]["tool"]["name"]
    manifest_ref = result["evidence"]["manifest_ref"]
    if tool == "sage":
        # Runtime import avoids a module cycle: the Sage adapter builds this contract.
        from .sage_adapter import verify_sage_execution_manifest

        try:
            verified = verify_sage_execution_manifest(str(manifest_ref))
        except (OSError, ValueError) as exc:
            raise ExternalAdapterContractError(
                f"Sage manifest verification failed: {exc}"
            ) from exc
    else:
        raise ExternalAdapterContractError(
            f"no live manifest verifier is registered for tool {tool!r}"
        )
    if verified.get("manifest_sha256") != result["evidence"]["manifest_sha256"]:
        raise ExternalAdapterContractError("live manifest file digest mismatch")
    manifest = verified.get("manifest")
    if not isinstance(manifest, Mapping) or manifest.get("request") != result["request"]:
        raise ExternalAdapterContractError("live manifest request does not match adapter result")
    if manifest.get("result", {}).get("status") != result["status"]:
        raise ExternalAdapterContractError("live manifest status does not match adapter result")
    if result["evidence"]["output_ref"] != manifest_ref:
        raise ExternalAdapterContractError("live adapter output_ref must be the verified manifest")
    if result["evidence"]["details"] != verified.get("payload"):
        raise ExternalAdapterContractError("live adapter evidence details do not match the manifest payload")
    if result["reason"] != verified.get("payload", {}).get("reason"):
        raise ExternalAdapterContractError("live adapter reason does not match the manifest payload")
    execution = result["execution"]
    if (
        execution["command"] != manifest.get("command")
        or os.path.realpath(str(execution["resolved_executable_path"]))
        != os.path.realpath(str(manifest.get("tool", {}).get("resolved_executable")))
        or execution["exit_code"] != manifest.get("execution", {}).get("exit_code")
        or execution["timed_out"] != manifest.get("execution", {}).get("timed_out")
    ):
        raise ExternalAdapterContractError("live adapter execution does not match the manifest")
    artifact_digests = verified.get("artifact_digests", {})
    stdout = artifact_digests.get("stdout.bin", {})
    stderr = artifact_digests.get("stderr.bin", {})
    if (
        execution["stdout_bytes"] != stdout.get("byte_count")
        or execution["stdout_sha256"] != stdout.get("sha256")
        or execution["stderr_bytes"] != stderr.get("byte_count")
        or execution["stderr_sha256"] != stderr.get("sha256")
    ):
        raise ExternalAdapterContractError("live adapter stream digests/counts do not match the manifest")
    return {
        "integrity_state": "verified",
        "tool": tool,
        "manifest_ref": manifest_ref,
        "manifest_sha256": verified["manifest_sha256"],
        "adapter_result_digest": result["result_digest"],
    }


def _validate_p04_claim_bundle(
    branch: Mapping[str, Any],
    request: Mapping[str, Any],
    result: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    """Validate exact Phase 04 records without accepting legacy-shaped copies."""
    from .derivation_search_orchestrator import P04_REQUEST_SCHEMA, P04_RESULT_SCHEMA
    from .derivation_search_tree import validate_branch_record

    branch_copy = deepcopy(dict(branch)) if isinstance(branch, Mapping) else {}
    branch_errors = validate_branch_record(branch_copy)
    if branch_errors:
        raise ExternalAdapterContractError(
            "normalized claim evidence requires a validated Phase 04 branch: "
            + "; ".join(branch_errors)
        )
    request_copy = deepcopy(dict(request)) if isinstance(request, Mapping) else {}
    request_keys = {
        "schema_version",
        "branch_id",
        "branch_lineage",
        "obligation_digest",
        "target",
        "typed_assumption_digests",
        "action_kind",
        "backend",
        "native_input",
        "native_input_digest",
        "timeout_ms",
        "max_output_bytes",
        "max_artifact_bytes",
        "formalization_plan_digest",
        "request_digest",
        "request_ref",
    }
    _require_exact_keys(request_copy, request_keys, "P04 request")
    if request_copy["schema_version"] != P04_REQUEST_SCHEMA:
        raise ExternalAdapterContractError("P04 request schema_version is invalid")
    expected_request_digest = content_digest(
        {
            key: request_copy[key]
            for key in request_copy
            if key not in {"request_digest", "request_ref"}
        }
    )
    if (
        request_copy["request_digest"] != expected_request_digest
        or request_copy["request_ref"]
        != f"artifact://p04/request/{expected_request_digest}"
    ):
        raise ExternalAdapterContractError("P04 request digest/reference mismatch")
    if (
        request_copy["branch_id"] != branch_copy["id"]
        or request_copy["branch_lineage"] != branch_copy["lineage"]
        or request_copy["obligation_digest"] != branch_copy["obligation_digest"]
        or request_copy["target"] != branch_copy["target"]
        or request_copy["typed_assumption_digests"]
        != branch_copy["typed_assumption_digests"]
        or request_copy["formalization_plan_digest"]
        != content_digest(branch_copy["formalization_plan"])
    ):
        raise ExternalAdapterContractError("P04 branch/request identity mismatch")
    native_input = request_copy["native_input"]
    if (
        not isinstance(native_input, str)
        or request_copy["native_input_digest"]
        != content_digest(native_input.encode("utf-8"))
    ):
        raise ExternalAdapterContractError("P04 native-input digest mismatch")

    result_copy = deepcopy(dict(result)) if isinstance(result, Mapping) else {}
    result_keys = {
        "schema_version",
        "branch_id",
        "request_digest",
        "status",
        "evidence_kind",
        "certification_status",
        "closed_blocker_ids",
        "reason",
        "output_ref",
        "raw_result_digest",
        "test_only",
        "live_tool_executed",
        "manifest_verified",
        "adapter_result_digest",
        "live_manifest_verification",
        "result_digest",
        "result_ref",
    }
    _require_exact_keys(result_copy, result_keys, "P04 result")
    if result_copy["schema_version"] != P04_RESULT_SCHEMA:
        raise ExternalAdapterContractError("P04 result schema_version is invalid")
    expected_result_digest = content_digest(
        {
            key: result_copy[key]
            for key in result_copy
            if key not in {"result_digest", "result_ref"}
        }
    )
    if (
        result_copy["result_digest"] != expected_result_digest
        or result_copy["result_ref"]
        != f"artifact://p04/result/{expected_result_digest}"
    ):
        raise ExternalAdapterContractError("P04 result digest/reference mismatch")
    if (
        result_copy["branch_id"] != branch_copy["id"]
        or result_copy["request_digest"] != request_copy["request_digest"]
        or request_copy["request_ref"] not in branch_copy["attempt_refs"]
        or result_copy["result_ref"] not in branch_copy["result_refs"]
    ):
        raise ExternalAdapterContractError("P04 branch/request/result identity mismatch")
    if result_copy["status"] not in {"proved", "refuted", "diagnostic", "failed", "timeout"}:
        raise ExternalAdapterContractError("P04 result status is invalid")
    if not isinstance(result_copy["closed_blocker_ids"], list) or any(
        not isinstance(item, str) or not item
        for item in result_copy["closed_blocker_ids"]
    ):
        raise ExternalAdapterContractError("P04 result blocker ids are invalid")
    return branch_copy, request_copy, result_copy


def _normalized_claim_evidence(
    *,
    manifest_family: str,
    manifest_version: str,
    manifest_ref: str,
    manifest_sha256: str,
    native_reader: str,
    branch: Mapping[str, Any],
    request: Mapping[str, Any],
    result: Mapping[str, Any],
    tool: Mapping[str, Any],
    backend_role: str,
    accepted_input_class: str,
    encoded_assumption_digests: list[str],
    assumption_encoding_complete: bool,
    native_input_media_type: str,
    resource_limits: Mapping[str, Any],
    execution_kind: str,
    live_tool_executed: bool,
    outcome: str,
    witness: Mapping[str, Any] | None,
    evidence_refs: list[str],
    non_claims: list[str],
    certifying: bool,
) -> dict[str, Any]:
    branch_copy, request_copy, result_copy = _validate_p04_claim_bundle(
        branch, request, result
    )
    record = {
        "schema_version": P06_NORMALIZED_CLAIM_EVIDENCE_SCHEMA,
        "manifest_family": manifest_family,
        "manifest_version": manifest_version,
        "manifest_ref": manifest_ref,
        "manifest_sha256": manifest_sha256,
        "native_reader": native_reader,
        "verifier_version": P06_CLAIM_EVIDENCE_VERIFIER_VERSION,
        "integrity_state": "registered_reader_verified",
        "branch": {
            "id": branch_copy["id"],
            "lineage": branch_copy["lineage"],
            "record_digest": content_digest(branch_copy),
            "request_digest": request_copy["request_digest"],
            "result_digest": result_copy["result_digest"],
        },
        "obligation": {
            "digest": branch_copy["obligation_digest"],
            "target": branch_copy["target"],
        },
        "typed_assumptions": branch_copy["typed_assumptions"],
        "typed_assumption_digests": branch_copy["typed_assumption_digests"],
        "assumption_encoding": {
            "encoded_assumption_digests": sorted(set(encoded_assumption_digests)),
            "complete": bool(assumption_encoding_complete),
            "evidence_refs": sorted(set(evidence_refs)),
        },
        "native_input": {
            "digest": request_copy["native_input_digest"],
            "media_type": native_input_media_type,
        },
        "tool": deepcopy(dict(tool)),
        "backend_role": backend_role,
        "accepted_input_class": accepted_input_class,
        "resource_limits": deepcopy(dict(resource_limits)),
        "execution": {
            "kind": execution_kind,
            "live_tool_executed": bool(live_tool_executed),
            "test_only": result_copy["test_only"] is True,
        },
        "outcome": {
            "status": outcome,
            "scope": branch_copy["target"],
            "p04_evidence_kind": result_copy["evidence_kind"],
            "p04_certification_status": result_copy["certification_status"],
            "placeholder_free": True,
            "conflict_free": True,
            "truncated": False,
        },
        "witness": deepcopy(dict(witness)) if isinstance(witness, Mapping) else None,
        "evidence_refs": sorted(set(evidence_refs)),
        "non_claims": sorted(set(non_claims)),
        "certifying": bool(certifying),
    }
    record["normalization_digest"] = content_digest(record)
    return validate_normalized_claim_evidence(record)


def validate_normalized_claim_evidence(value: Any) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise ExternalAdapterContractError("normalized claim evidence must be an object")
    record = deepcopy(dict(value))
    _require_exact_keys(record, _P06_NORMALIZED_KEYS, "normalized claim evidence")
    if record["schema_version"] != P06_NORMALIZED_CLAIM_EVIDENCE_SCHEMA:
        raise ExternalAdapterContractError("normalized claim evidence schema is invalid")
    if record["integrity_state"] != "registered_reader_verified":
        raise ExternalAdapterContractError("normalized evidence must come from a registered reader")
    if record["verifier_version"] != P06_CLAIM_EVIDENCE_VERIFIER_VERSION:
        raise ExternalAdapterContractError("normalized evidence verifier version is invalid")
    for key in (
        "manifest_family",
        "manifest_version",
        "manifest_ref",
        "manifest_sha256",
        "native_reader",
        "backend_role",
        "accepted_input_class",
    ):
        _require_string(record[key], key)
    _require_sha256(record["manifest_sha256"], "manifest_sha256")
    if not isinstance(record["certifying"], bool):
        raise ExternalAdapterContractError("normalized certifying flag must be boolean")
    family = (
        record["manifest_family"],
        record["manifest_version"],
        record["native_reader"],
    )
    if family not in {
        (
            "generic_evidence_manifest",
            "evidence_manifest@1",
            "verify_attempt_manifest",
        ),
        (
            "registered_external_adapter",
            "p05_sage_execution_manifest@3",
            "verify_live_adapter_manifest",
        ),
    }:
        raise ExternalAdapterContractError("unregistered normalized manifest family")

    branch = record["branch"]
    if not isinstance(branch, Mapping) or set(branch) != {
        "id",
        "lineage",
        "record_digest",
        "request_digest",
        "result_digest",
    }:
        raise ExternalAdapterContractError("normalized branch binding keys mismatch")
    _require_string(branch["id"], "branch.id")
    if (
        not isinstance(branch["lineage"], list)
        or not branch["lineage"]
        or branch["lineage"][-1] != branch["id"]
    ):
        raise ExternalAdapterContractError("normalized branch lineage is invalid")
    for key in ("record_digest", "request_digest", "result_digest"):
        _require_sha256(branch[key], f"branch.{key}")

    obligation = record["obligation"]
    if not isinstance(obligation, Mapping) or set(obligation) != {"digest", "target"}:
        raise ExternalAdapterContractError("normalized obligation keys mismatch")
    _require_sha256(obligation["digest"], "obligation.digest")
    _require_string(obligation["target"], "obligation.target")
    assumptions = record["typed_assumptions"]
    assumption_digests = record["typed_assumption_digests"]
    if (
        not isinstance(assumptions, list)
        or any(not isinstance(item, dict) for item in assumptions)
        or not isinstance(assumption_digests, list)
        or assumption_digests != [content_digest(item) for item in assumptions]
    ):
        raise ExternalAdapterContractError("normalized typed assumptions are invalid")
    assumption_encoding = record["assumption_encoding"]
    if not isinstance(assumption_encoding, Mapping) or set(assumption_encoding) != {
        "encoded_assumption_digests",
        "complete",
        "evidence_refs",
    }:
        raise ExternalAdapterContractError("normalized assumption encoding keys mismatch")
    encoded = assumption_encoding["encoded_assumption_digests"]
    if (
        not isinstance(encoded, list)
        or encoded != sorted(set(encoded))
        or any(item not in assumption_digests for item in encoded)
        or not isinstance(assumption_encoding["complete"], bool)
        or assumption_encoding["complete"]
        != (encoded == sorted(assumption_digests))
        or not isinstance(assumption_encoding["evidence_refs"], list)
        or not assumption_encoding["evidence_refs"]
    ):
        raise ExternalAdapterContractError("normalized assumption encoding is invalid")

    native_input = record["native_input"]
    if not isinstance(native_input, Mapping) or set(native_input) != {"digest", "media_type"}:
        raise ExternalAdapterContractError("normalized native-input keys mismatch")
    _require_sha256(native_input["digest"], "native_input.digest")
    _require_string(native_input["media_type"], "native_input.media_type")
    if not isinstance(record["tool"], Mapping) or not record["tool"]:
        raise ExternalAdapterContractError("normalized tool identity is invalid")
    canonical_json_bytes(record["tool"])
    if not isinstance(record["resource_limits"], Mapping) or not record["resource_limits"]:
        raise ExternalAdapterContractError("normalized resource limits are invalid")
    canonical_json_bytes(record["resource_limits"])

    execution = record["execution"]
    if not isinstance(execution, Mapping) or set(execution) != {
        "kind",
        "live_tool_executed",
        "test_only",
    }:
        raise ExternalAdapterContractError("normalized execution keys mismatch")
    _require_string(execution["kind"], "execution.kind")
    if not isinstance(execution["live_tool_executed"], bool) or not isinstance(
        execution["test_only"], bool
    ):
        raise ExternalAdapterContractError("normalized execution flags are invalid")
    if family[0] == "generic_evidence_manifest" and (
        record["certifying"]
        or execution["live_tool_executed"]
        or not execution["test_only"]
    ):
        raise ExternalAdapterContractError("generic v1 evidence must remain test-only and noncertifying")
    if family[0] == "registered_external_adapter" and (
        not record["certifying"]
        or not execution["live_tool_executed"]
        or execution["test_only"]
        or record["tool"].get("name") != "sage"
    ):
        raise ExternalAdapterContractError("registered Sage evidence must be live and certifying")

    outcome = record["outcome"]
    if not isinstance(outcome, Mapping) or set(outcome) != {
        "status",
        "scope",
        "p04_evidence_kind",
        "p04_certification_status",
        "placeholder_free",
        "conflict_free",
        "truncated",
    }:
        raise ExternalAdapterContractError("normalized outcome keys mismatch")
    for key in ("status", "scope", "p04_evidence_kind", "p04_certification_status"):
        _require_string(outcome[key], f"outcome.{key}")
    for key in ("placeholder_free", "conflict_free", "truncated"):
        if not isinstance(outcome[key], bool):
            raise ExternalAdapterContractError(f"outcome.{key} must be boolean")
    if record["certifying"] and (
        outcome["status"] not in {"certified", "refuted"}
        or not outcome["placeholder_free"]
        or not outcome["conflict_free"]
        or outcome["truncated"]
    ):
        raise ExternalAdapterContractError("certifying normalized outcome is invalid")
    if record["witness"] is not None and not isinstance(record["witness"], Mapping):
        raise ExternalAdapterContractError("normalized witness must be null or an object")
    for key in ("evidence_refs", "non_claims"):
        values = record[key]
        if (
            not isinstance(values, list)
            or not values
            or any(not isinstance(item, str) or not item for item in values)
            or values != sorted(set(values))
        ):
            raise ExternalAdapterContractError(f"normalized {key} must be a sorted unique non-empty list")
    expected_digest = content_digest(
        {key: record[key] for key in record if key != "normalization_digest"}
    )
    if record["normalization_digest"] != expected_digest:
        raise ExternalAdapterContractError("normalized evidence digest mismatch")
    return record


def normalize_generic_v1_claim_evidence(
    *,
    artifact_root: str | os.PathLike[str],
    manifest_ref: str,
    p04_branch: Mapping[str, Any],
    p04_request: Mapping[str, Any],
    p04_result: Mapping[str, Any],
) -> dict[str, Any]:
    """Reopen a generic v1 bundle and normalize it as test-only evidence."""
    from .evidence_manifest import EvidenceValidationError, verify_attempt_manifest

    try:
        verified = verify_attempt_manifest(artifact_root, manifest_ref)
    except (OSError, EvidenceValidationError, ValueError) as exc:
        raise ExternalAdapterContractError(
            f"generic v1 manifest verification failed: {exc}"
        ) from exc
    manifest = verified["manifest"]
    generic_request = manifest["request"]
    branch_copy, request_copy, result_copy = _validate_p04_claim_bundle(
        p04_branch, p04_request, p04_result
    )
    if (
        generic_request["branch"]["id"] != branch_copy["id"]
        or generic_request["branch"]["lineage"] != branch_copy["lineage"]
        or generic_request["obligation"]["digest"] != branch_copy["obligation_digest"]
        or generic_request["obligation"]["target"] != branch_copy["target"]
        or generic_request["typed_assumptions"] != branch_copy["typed_assumptions"]
        or generic_request["assumption_digest"]
        != content_digest(branch_copy["typed_assumptions"])
        or generic_request["native_input"]["digest"]
        != request_copy["native_input_digest"]
    ):
        raise ExternalAdapterContractError("generic v1 manifest/P04 binding mismatch")
    outcome = manifest["result"]["outcome"]
    if result_copy["status"] not in {
        "proved" if outcome == "certified" else "refuted" if outcome == "refuted" else "diagnostic"
    }:
        raise ExternalAdapterContractError("generic v1 outcome/P04 result mismatch")
    interpretation = manifest["interpretation"]
    native_entries = [
        item
        for item in manifest["integrity"]["artifact_inventory"]
        if item.get("role") == "native_input"
    ]
    if (
        len(native_entries) != 1
        or native_entries[0]["sha256"] != generic_request["native_input"]["digest"]
    ):
        raise ExternalAdapterContractError("generic v1 native-input artifact mismatch")
    return _normalized_claim_evidence(
        manifest_family="generic_evidence_manifest",
        manifest_version="evidence_manifest@1",
        manifest_ref=verified["manifest_ref"],
        manifest_sha256=verified["manifest_sha256"],
        native_reader="verify_attempt_manifest",
        branch=branch_copy,
        request=request_copy,
        result=result_copy,
        tool=generic_request["tool"],
        backend_role=generic_request["backend_role"],
        accepted_input_class=generic_request["expected_result_class"],
        encoded_assumption_digests=[],
        assumption_encoding_complete=False,
        native_input_media_type=generic_request["native_input"]["media_type"],
        resource_limits=generic_request["resource_limits"],
        execution_kind="cpu_test_double",
        live_tool_executed=False,
        outcome=outcome,
        witness=None,
        evidence_refs=[verified["manifest_ref"], result_copy["result_ref"]],
        non_claims=interpretation["non_claims"],
        certifying=False,
    )


def reverify_generic_v1_claim_evidence(
    *,
    artifact_root: str | os.PathLike[str],
    manifest_ref: str,
    p04_branch: Mapping[str, Any],
    p04_request: Mapping[str, Any],
    p04_result: Mapping[str, Any],
) -> RevalidatingClaimEvidence:
    """Build inert inputs whose consumers must re-open the generic manifest."""
    request = RevalidatingClaimEvidence(
        reader=P06_GENERIC_REVALIDATION_READER,
        inputs={
            "artifact_root": os.fspath(artifact_root),
            "manifest_ref": manifest_ref,
            "p04_branch": p04_branch,
            "p04_request": p04_request,
            "p04_result": p04_result,
        },
    )
    reader_verified_claim_evidence_record(request)
    return request


def normalize_registered_adapter_claim_evidence(
    *,
    adapter_result: Mapping[str, Any],
    p04_branch: Mapping[str, Any],
    p04_request: Mapping[str, Any],
    p04_result: Mapping[str, Any],
) -> dict[str, Any]:
    """Reverify one registered live manifest and bind it to exact Phase 04 records."""
    result = validate_external_adapter_result(adapter_result)
    branch_copy, request_copy, result_copy = _validate_p04_claim_bundle(
        p04_branch, p04_request, p04_result
    )
    receipt = verify_live_adapter_manifest(result)
    request = result["request"]
    if request["tool"]["name"] != "sage":
        raise ExternalAdapterContractError(
            "registered claim normalization has no assumption-encoding reader "
            f"for tool {request['tool']['name']!r}"
        )
    from .sage_adapter import verify_sage_execution_manifest

    try:
        native_projection = verify_sage_execution_manifest(receipt["manifest_ref"])
    except (OSError, ValueError) as exc:
        raise ExternalAdapterContractError(
            f"Sage assumption-encoding verification failed: {exc}"
        ) from exc
    if native_projection.get("manifest_sha256") != receipt["manifest_sha256"]:
        raise ExternalAdapterContractError(
            "assumption-encoding projection manifest digest mismatch"
        )
    encoded_assumption_digests = native_projection.get(
        "encoded_assumption_digests", []
    )
    assumption_encoding_evidence_refs = native_projection.get(
        "assumption_encoding_evidence_refs", []
    )
    if (
        request["branch_id"] != branch_copy["id"]
        or request["branch_lineage"] != branch_copy["lineage"]
        or request["obligation_digest"] != branch_copy["obligation_digest"]
        or request["normalized_target"] != branch_copy["target"]
        or request["typed_assumptions"] != branch_copy["typed_assumptions"]
        or request["native_input_digest"] != request_copy["native_input_digest"]
        or request["resource_limits"]["timeout_ms"] != request_copy["timeout_ms"]
        or request["resource_limits"]["max_output_bytes"]
        != request_copy["max_output_bytes"]
        or request["resource_limits"]["max_artifact_bytes"]
        > request_copy["max_artifact_bytes"]
    ):
        raise ExternalAdapterContractError("registered adapter/P04 binding mismatch")
    if (
        result_copy["adapter_result_digest"] != result["result_digest"]
        or result_copy["live_manifest_verification"] != receipt
        or result_copy["manifest_verified"] is not True
        or result_copy["live_tool_executed"] is not True
        or result_copy["test_only"] is True
    ):
        raise ExternalAdapterContractError("registered adapter/P04 result evidence mismatch")
    expected_status = "proved" if result["status"] == "certified" else "refuted"
    if result_copy["status"] != expected_status:
        raise ExternalAdapterContractError("registered adapter outcome/P04 result mismatch")
    return _normalized_claim_evidence(
        manifest_family="registered_external_adapter",
        manifest_version="p05_sage_execution_manifest@3",
        manifest_ref=receipt["manifest_ref"],
        manifest_sha256=receipt["manifest_sha256"],
        native_reader="verify_live_adapter_manifest",
        branch=branch_copy,
        request=request_copy,
        result=result_copy,
        tool=request["tool"],
        backend_role=request["backend_role"],
        accepted_input_class=request["expected_result_class"],
        encoded_assumption_digests=encoded_assumption_digests,
        assumption_encoding_complete=(
            encoded_assumption_digests
            == sorted(branch_copy["typed_assumption_digests"])
        ),
        native_input_media_type=request["native_input_media_type"],
        resource_limits=request["resource_limits"],
        execution_kind=result["execution"]["kind"],
        live_tool_executed=True,
        outcome=result["status"],
        witness=result["evidence"]["refutation_witness"],
        evidence_refs=[
            *assumption_encoding_evidence_refs,
            receipt["manifest_ref"],
            result_copy["result_ref"],
        ],
        non_claims=result["non_claims"],
        certifying=True,
    )


def reverify_registered_adapter_claim_evidence(
    *,
    adapter_result: Mapping[str, Any],
    p04_branch: Mapping[str, Any],
    p04_request: Mapping[str, Any],
    p04_result: Mapping[str, Any],
) -> RevalidatingClaimEvidence:
    """Build inert inputs whose consumers must rerun the registered reader."""
    request = RevalidatingClaimEvidence(
        reader=P06_REGISTERED_REVALIDATION_READER,
        inputs={
            "adapter_result": adapter_result,
            "p04_branch": p04_branch,
            "p04_request": p04_request,
            "p04_result": p04_result,
        },
    )
    reader_verified_claim_evidence_record(request)
    return request


def p04_injected_result_from_adapter(
    adapter_result: Mapping[str, Any],
    p04_request: Mapping[str, Any],
    *,
    closed_blocker_ids: list[str] | tuple[str, ...] = (),
) -> dict[str, Any]:
    """Map one validated Phase 05 result onto only its exact P04 request."""
    result = validate_external_adapter_result(adapter_result)
    if not isinstance(p04_request, Mapping):
        raise ExternalAdapterContractError("P04 request must be an object")
    branch_id = p04_request.get("branch_id")
    request_digest = p04_request.get("request_digest")
    native_digest = p04_request.get("native_input_digest")
    request = result["request"]
    if branch_id != request["branch_id"]:
        raise ExternalAdapterContractError("adapter/P04 branch binding mismatch")
    if p04_request.get("branch_lineage") != request["branch_lineage"]:
        raise ExternalAdapterContractError("adapter/P04 lineage binding mismatch")
    if p04_request.get("obligation_digest") != request["obligation_digest"]:
        raise ExternalAdapterContractError("adapter/P04 obligation binding mismatch")
    if p04_request.get("target") != request["normalized_target"]:
        raise ExternalAdapterContractError("adapter/P04 target binding mismatch")
    if native_digest != request["native_input_digest"]:
        raise ExternalAdapterContractError("adapter/P04 native-input binding mismatch")
    adapter_assumption_digests = [
        content_digest(item) for item in request["typed_assumptions"]
    ]
    if p04_request.get("typed_assumption_digests") != adapter_assumption_digests:
        raise ExternalAdapterContractError("adapter/P04 typed-assumption binding mismatch")
    limits = request["resource_limits"]
    if p04_request.get("timeout_ms") != limits["timeout_ms"]:
        raise ExternalAdapterContractError("adapter/P04 timeout binding mismatch")
    if p04_request.get("max_output_bytes") != limits["max_output_bytes"]:
        raise ExternalAdapterContractError("adapter/P04 output-limit binding mismatch")
    p04_artifact_limit = p04_request.get("max_artifact_bytes")
    if (
        not isinstance(p04_artifact_limit, int)
        or isinstance(p04_artifact_limit, bool)
        or limits["max_artifact_bytes"] > p04_artifact_limit
    ):
        raise ExternalAdapterContractError("adapter/P04 artifact-limit binding mismatch")
    _require_sha256(request_digest, "P04 request_digest")
    if any(not isinstance(item, str) or not item for item in closed_blocker_ids):
        raise ExternalAdapterContractError("closed_blocker_ids must contain non-empty strings")
    if len(set(closed_blocker_ids)) != len(closed_blocker_ids):
        raise ExternalAdapterContractError("closed_blocker_ids must be unique")

    status = result["status"]
    resolved_status = {
        "certified": "proved",
        "refuted": "refuted",
        "timeout": "timeout",
        "execution_error": "failed",
        "malformed_output": "failed",
        "truncated_output": "failed",
    }.get(status, "diagnostic")
    fake_runner = result["execution"]["kind"] == "fake_runner"
    live_manifest_verification = None
    if result["live_tool_executed"] and result["can_promote"]:
        live_manifest_verification = verify_live_adapter_manifest(result)
    p04_status = (
        resolved_status
        if resolved_status not in {"proved", "refuted"}
        or fake_runner
        or result["can_promote"] is True
        else "diagnostic"
    )
    certifying = status == "certified"
    refuting = status == "refuted"
    output_ref = result["evidence"]["output_ref"]
    # Fake-runner results may exercise P04 state mechanics, but remain test-only
    # and cannot satisfy the Phase 05 live-specialist or mathematical gate.
    test_only = fake_runner
    if certifying:
        evidence_kind = "certifying_backend"
        certification_status = "certified"
    elif refuting:
        evidence_kind = "counterexample"
        certification_status = "counterexample"
    else:
        evidence_kind = "diagnostic"
        certification_status = "diagnostic"
    return {
        "branch_id": branch_id,
        "request_digest": request_digest,
        "status": p04_status,
        "evidence_kind": evidence_kind,
        "certification_status": certification_status,
        "closed_blocker_ids": list(closed_blocker_ids),
        "reason": result["reason"],
        "output_ref": output_ref,
        "test_only": test_only,
        "adapter_result_digest": result["result_digest"],
        "adapter_result": result,
        "live_manifest_verification": live_manifest_verification,
    }
