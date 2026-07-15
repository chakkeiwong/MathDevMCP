from __future__ import annotations

"""Canonical, content-addressed evidence records for Phase 01.

This module deliberately keeps evidence identity, runtime allocation, and
mathematical authority separate. A verified manifest proves that named bytes
were sealed consistently; it does not prove the mathematical claim in them.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import stat
import threading
import unicodedata
from typing import Any, Callable, Mapping, Sequence


SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
GIT_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
ROUND_RE = re.compile(r"^rr0[1-5]$")
ATTEMPT_RE = re.compile(r"^b0[1-5]$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

P01_NON_CLAIMS = frozenset(
    {
        "no_real_document_extraction",
        "no_backend_conformance",
        "no_mathematical_certification",
        "no_branch_local_scheduler",
        "no_publication_eligibility",
        "no_source_document_edit",
        "no_multiprocess_support",
        "no_release_readiness",
    }
)

P01_VETO_KEYS = frozenset(
    {
        "canonical_identity_failure",
        "manifest_contract_failure",
        "artifact_store_failure",
        "path_or_symlink_failure",
        "sealed_overwrite_failure",
        "tamper_or_truncation_failure",
        "parallel_identity_failure",
        "exact_binding_failure",
        "conflict_detection_failure",
        "legacy_or_unsupported_certification",
        "cached_status_authority",
        "private_data_exposure",
        "claim_eligibility_leak",
        "publication_quarantine_failure",
        "unexpected_implementation_path",
        "protected_baseline_drift",
        "forbidden_execution",
        "governance_chain_failure",
    }
)

P01_CLOSE_REASONS = frozenset(
    {
        "local_check_failure",
        "candidate_gate_failure",
        "result_review_revise",
        "final_seal_audit_revise",
    }
)

P01_RECEIPT_BINDING_KEYS: dict[str, frozenset[str]] = {
    "init_round": frozenset(
        {
            "bootstrap_close_ref",
            "bootstrap_close_sha256",
            "bootstrap_shell_verification_ref",
            "bootstrap_shell_verification_sha256",
            "entry_implementation_manifest_sha256",
            "entry_protected_manifest_sha256",
            "implementation_exit_manifest_ref",
            "implementation_exit_manifest_sha256",
            "prior_round_close_ref",
            "prior_round_close_sha256",
            "prior_terminal_receipt_index_ref",
            "prior_terminal_receipt_index_sha256",
        }
    ),
    "canonical": frozenset(),
    "store": frozenset(),
    "promotion": frozenset(),
    "compatibility": frozenset(),
    "integration": frozenset(),
    "p00_quarantine": frozenset(),
    "generator": frozenset(),
    "compile": frozenset(),
    "protected_check": frozenset(),
    "implementation_exit": frozenset({"manifest_ref", "manifest_sha256"}),
    "allowlist": frozenset(),
    "assignment_audit": frozenset(),
    "diff": frozenset(),
    "bind_result": frozenset({"result_ref", "result_sha256"}),
    "build_run_manifest": frozenset(
        {"run_manifest_ref", "run_manifest_sha256", "bound_receipt_index_ref", "bound_receipt_index_sha256"}
    ),
    "build_candidate": frozenset(
        {
            "run_manifest_ref",
            "run_manifest_sha256",
            "candidate_ref",
            "candidate_sha256",
            "bound_receipt_index_ref",
            "bound_receipt_index_sha256",
        }
    ),
    "candidate_gate": frozenset(
        {
            "run_manifest_ref",
            "run_manifest_sha256",
            "candidate_ref",
            "candidate_sha256",
            "validated_receipt_index_ref",
            "validated_receipt_index_sha256",
            "payload_bundle_index_ref",
            "payload_bundle_index_digest",
            "payload_bundle_index_file_sha256",
        }
    ),
    "result_review_binding": frozenset(
        {
            "review_ref",
            "review_sha256",
            "candidate_ref",
            "candidate_sha256",
            "reviewed_receipt_index_ref",
            "reviewed_receipt_index_sha256",
        }
    ),
    "build_final_candidate": frozenset(
        {
            "final_candidate_ref",
            "final_candidate_sha256",
            "result_review_ref",
            "result_review_sha256",
            "reviewed_receipt_index_ref",
            "reviewed_receipt_index_sha256",
        }
    ),
    "final_candidate_gate": frozenset(
        {
            "final_candidate_ref",
            "final_candidate_sha256",
            "validation_log_ref",
            "validation_log_sha256",
            "validated_receipt_index_ref",
            "validated_receipt_index_sha256",
        }
    ),
    "final_seal_audit_binding": frozenset(
        {
            "audit_ref",
            "audit_sha256",
            "final_candidate_ref",
            "final_candidate_sha256",
            "candidate_ref",
            "candidate_sha256",
            "result_review_ref",
            "result_review_sha256",
            "validation_log_ref",
            "validation_log_sha256",
            "audited_receipt_index_ref",
            "audited_receipt_index_sha256",
        }
    ),
    "bind_scoped_repair": frozenset(
        {
            "scoped_repair_input_ref",
            "scoped_repair_input_sha256",
            "source_artifact_ref",
            "source_artifact_sha256",
            "source_receipt_index_ref",
            "source_receipt_index_sha256",
        }
    ),
    "close_round": frozenset(
        {
            "scoped_repair_input_ref",
            "scoped_repair_input_sha256",
            "round_close_ref",
            "round_close_sha256",
            "preceding_receipt_index_ref",
            "preceding_receipt_index_sha256",
        }
    ),
    "stable_publication": frozenset(
        {
            "stable_ref",
            "stable_sha256",
            "final_candidate_ref",
            "final_candidate_sha256",
            "audit_ref",
            "audit_sha256",
            "validation_log_ref",
            "validation_log_sha256",
            "same_inode",
            "same_digest",
        }
    ),
}

P01_PASS_ACTION_SEQUENCE = (
    "init_round",
    "canonical",
    "store",
    "promotion",
    "compatibility",
    "integration",
    "p00_quarantine",
    "generator",
    "compile",
    "protected_check",
    "implementation_exit",
    "allowlist",
    "assignment_audit",
    "diff",
    "bind_result",
    "build_run_manifest",
    "build_candidate",
    "candidate_gate",
    "result_review_binding",
    "build_final_candidate",
    "final_candidate_gate",
    "final_seal_audit_binding",
)

P01_PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
P01_PLAN_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-01-evidence-integrity-subplan-2026-07-11.md"
P01_EVIDENCE_ROOT_REF = ".local/mathdevmcp/evidence/p01-20260711"
P01_ENTRY_ROOT_REF = f"{P01_EVIDENCE_ROOT_REF}/entry"
P01_P00_NODES = (
    "test_simple_algebra_is_partial_evidence_not_repair",
    "test_x_over_x_preserves_nonzero_requirement_after_raw_backend_success",
    "test_latex_sqrt_preserves_real_domain_requirement",
    "test_siblings_collision_and_edit_mismatch_remain_legacy_unbound",
    "test_edit_target_mismatch_cannot_bypass_compiler_quarantine",
    "test_adapter_exception_is_engineering_error_not_only_math_gap",
    "test_serial_and_parallel_worker_exceptions_are_engineering_errors",
    "test_library_facade_server_and_cli_have_quarantine_parity",
    "test_emergency_kill_switch_returns_before_source_access_on_all_surfaces",
    "test_lower_level_controller_contract_remains_raw_and_unchanged",
    "test_phase01_document_surfaces_remain_ineligible_and_publication_false",
)

P01_REQUIRED_INVARIANT_IDS = (
    "verified_manifest",
    "source_digest",
    "source_span",
    "source_label",
    "obligation_digest",
    "normalized_target",
    "branch_id",
    "branch_lineage",
    "typed_assumptions",
    "assumption_digest",
    "native_input_digest",
    "tool_identity",
    "backend_role",
    "sealed_inventory",
    "result_outcome",
    "result_not_truncated",
    "no_conflict",
    "candidate_edit_binding",
    "no_evidence_vetoes",
    "no_engineering_vetoes",
    "publication_quarantine",
)
P01_REQUIRED_MUTATION_CASES = (
    ("source_bytes", "source_digest"),
    ("source_span", "source_span"),
    ("source_label", "source_label"),
    ("target", "normalized_target"),
    ("obligation", "obligation_digest"),
    ("assumptions", "typed_assumptions"),
    ("branch", "branch_id"),
    ("lineage", "branch_lineage"),
    ("native_input", "native_input_digest"),
    ("tool_version", "tool_identity"),
    ("backend_role", "backend_role"),
    ("conflict", "no_conflict"),
    ("edit_bytes", "candidate_edit_binding"),
    ("edit_span", "candidate_edit_binding"),
    ("publication_flag", "publication_quarantine"),
    ("result_outcome", "result_outcome"),
    ("result_truncation", "result_not_truncated"),
    ("artifact_role", "sealed_inventory"),
    ("artifact_inventory", "sealed_inventory"),
    ("evidence_veto", "no_evidence_vetoes"),
    ("engineering_veto", "no_engineering_vetoes"),
)
P01_REQUIRED_LEGACY_CASES = (
    ("current_v0", "0-legacy", "unbound_legacy_evidence"),
    ("legacy_uri", "0-legacy", "unbound_legacy_evidence"),
    ("partial_v1", "1.0", "invalid_or_partial_v1"),
    ("unknown_major", "2.0", "unknown_major_schema"),
)


def p01_fixed_action_argv(round_ref: str, action: str) -> list[str] | None:
    """Return the exact subprocess argv recorded for a fixed P01 check."""
    pytest = [P01_PYTHON, "-m", "pytest", "-q"]
    integration_nodes = [
        f"tests/test_document_publication_quarantine.py::{name}"
        for name in P01_P00_NODES[3:7]
    ] + [f"tests/test_document_publication_quarantine.py::{P01_P00_NODES[-1]}"]
    registry = {
        "canonical": [*pytest, "tests/test_evidence_manifest.py"],
        "store": [
            *pytest,
            "tests/test_evidence_manifest.py",
            "tests/test_promotion_policy.py::test_verified_manifests_are_required_for_integrity_binding",
        ],
        "promotion": [*pytest, "tests/test_promotion_policy.py"],
        "compatibility": [
            *pytest,
            "tests/test_external_tool_adapters.py",
            "tests/test_derivation_search_tree.py",
            "tests/test_derivation_branch_controller.py",
        ],
        "integration": [*pytest, *integration_nodes],
        "p00_quarantine": [
            *pytest,
            *[
                f"tests/test_document_publication_quarantine.py::{name}"
                for name in P01_P00_NODES
            ],
        ],
        "generator": [P01_PYTHON, "scripts/generate_p01_synthetic_evidence.py", "--round-root", round_ref],
        "compile": [
            P01_PYTHON,
            "-m",
            "py_compile",
            "src/mathdevmcp/evidence_manifest.py",
            "src/mathdevmcp/promotion_policy.py",
            "src/mathdevmcp/external_tool_adapters.py",
            "src/mathdevmcp/derivation_search_tree.py",
            "src/mathdevmcp/derivation_branch_controller.py",
            "src/mathdevmcp/document_derivation_tree.py",
            "scripts/generate_p01_synthetic_evidence.py",
            "scripts/p01_governance.py",
            "tests/test_evidence_manifest.py",
            "tests/test_promotion_policy.py",
        ],
        "protected_check": ["sha256sum", "-c", f"{P01_ENTRY_ROOT_REF}/protected-dirty-sha256.txt"],
        "diff": ["git", "diff", "--check"],
    }
    command = registry.get(action)
    return None if command is None else ["env", "PYTHONPATH=src", *command]


def p01_governance_action_argv(
    round_ref: str,
    action: str,
    *,
    artifact_ref: str | None = None,
) -> list[str]:
    command = [
        "env",
        "PYTHONPATH=src",
        P01_PYTHON,
        "scripts/p01_governance.py",
        "run",
        "--round-root",
        round_ref,
        "--action",
        action,
    ]
    if artifact_ref is not None:
        command.extend(["--artifact-ref", artifact_ref])
    return command

_SET_LIKE_NAMES = frozenset(
    {
        "typed_assumptions",
        "evidence_refs",
        "blocker_ids",
        "veto_ids",
        "non_claims",
        "unsupported_conclusions",
        "external_tool_considerations",
    }
)


class EvidenceValidationError(ValueError):
    """A record or artifact violates the reviewed evidence contract."""


class EvidenceConflictError(FileExistsError):
    """A caller attempted to overwrite or collide with sealed evidence."""


def _pairs_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceValidationError(f"duplicate JSON key: {key!r}")
        result[key] = value
    return result


def _normalize_json(value: Any, path: tuple[str, ...] = ()) -> Any:
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        raise EvidenceValidationError(f"floating-point value forbidden at {'.'.join(path) or '<root>'}")
    if isinstance(value, str):
        try:
            value.encode("utf-8", "strict")
        except UnicodeEncodeError as exc:
            raise EvidenceValidationError(f"isolated surrogate at {'.'.join(path) or '<root>'}") from exc
        return unicodedata.normalize("NFC", value)
    if isinstance(value, Mapping):
        normalized: dict[str, Any] = {}
        original_keys: dict[str, str] = {}
        for raw_key, child in value.items():
            if not isinstance(raw_key, str):
                raise EvidenceValidationError(f"non-string mapping key at {'.'.join(path) or '<root>'}")
            key = unicodedata.normalize("NFC", raw_key)
            if key in normalized:
                raise EvidenceValidationError(
                    f"mapping keys {original_keys[key]!r} and {raw_key!r} collide after NFC normalization"
                )
            original_keys[key] = raw_key
            normalized[key] = _normalize_json(child, (*path, key))
        return normalized
    if isinstance(value, (list, tuple)):
        items = [_normalize_json(child, (*path, "*")) for child in value]
        if path and path[-1] in _SET_LIKE_NAMES:
            encoded: list[tuple[str, bytes, Any]] = []
            seen: set[bytes] = set()
            for item in items:
                payload = json.dumps(
                    item,
                    ensure_ascii=False,
                    allow_nan=False,
                    sort_keys=True,
                    separators=(",", ":"),
                ).encode("utf-8")
                if payload in seen:
                    raise EvidenceValidationError(f"duplicate set-like element at {'.'.join(path)}")
                seen.add(payload)
                encoded.append((hashlib.sha256(payload).hexdigest(), payload, item))
            encoded.sort(key=lambda row: (row[0], row[1]))
            return [row[2] for row in encoded]
        return items
    raise EvidenceValidationError(f"unsupported JSON type {type(value).__name__} at {'.'.join(path) or '<root>'}")


Validator = Callable[[dict[str, Any]], None]


@dataclass(frozen=True)
class SchemaSpec:
    name: str
    required_keys: frozenset[str]
    validator: Validator


_SCHEMAS: dict[str, SchemaSpec] = {}


def _register(name: str, keys: Sequence[str], validator: Validator) -> None:
    _SCHEMAS[name] = SchemaSpec(name, frozenset(keys), validator)


def _require_exact_keys(record: Mapping[str, Any], keys: frozenset[str], where: str) -> None:
    actual = set(record)
    missing = sorted(keys - actual)
    extra = sorted(actual - keys)
    if missing or extra:
        raise EvidenceValidationError(f"{where} keys mismatch: missing={missing}, extra={extra}")


def _require_str(value: Any, name: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str) or (nonempty and not value):
        raise EvidenceValidationError(f"{name} must be {'a non-empty ' if nonempty else 'a '}string")
    return value


def _require_bool(value: Any, name: str) -> bool:
    if type(value) is not bool:
        raise EvidenceValidationError(f"{name} must be a boolean")
    return value


def _require_int(value: Any, name: str, *, minimum: int = 0, maximum: int | None = None) -> int:
    if type(value) is not int or value < minimum or (maximum is not None and value > maximum):
        suffix = f" through {maximum}" if maximum is not None else " or greater"
        raise EvidenceValidationError(f"{name} must be an integer {minimum}{suffix}")
    return value


def _require_digest(value: Any, name: str) -> str:
    text = _require_str(value, name)
    if not SHA256_RE.fullmatch(text):
        raise EvidenceValidationError(f"{name} must be a lower-case SHA-256")
    return text


def _require_round(value: Any, name: str = "result_round") -> str:
    text = _require_str(value, name)
    if not ROUND_RE.fullmatch(text):
        raise EvidenceValidationError(f"{name} must match rr0[1-5]")
    return text


def _require_enum(value: Any, allowed: set[str] | frozenset[str], name: str) -> str:
    text = _require_str(value, name)
    if text not in allowed:
        raise EvidenceValidationError(f"{name} must be one of {sorted(allowed)}")
    return text


def validate_logical_path(value: str, *, name: str = "logical_path") -> str:
    text = _require_str(value, name)
    if "\x00" in text or "\\" in text or text.endswith("/") or text.startswith(("/", "//")):
        raise EvidenceValidationError(f"{name} is not a normalized relative POSIX path")
    if re.match(r"^[A-Za-z]:", text):
        raise EvidenceValidationError(f"{name} must not contain a drive prefix")
    parts = text.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise EvidenceValidationError(f"{name} contains an empty, dot, or parent segment")
    pure = PurePosixPath(text)
    if pure.is_absolute() or pure.as_posix() != text:
        raise EvidenceValidationError(f"{name} is not canonical")
    return text


def _require_ref_digest(record: Mapping[str, Any], ref_key: str, digest_key: str, *, nullable: bool = False) -> None:
    ref = record.get(ref_key)
    digest = record.get(digest_key)
    if nullable and ref is None and digest is None:
        return
    if (ref is None) != (digest is None):
        raise EvidenceValidationError(f"{ref_key}/{digest_key} must be null or non-null together")
    validate_logical_path(ref, name=ref_key)
    _require_digest(digest, digest_key)


def _require_artifact_entry(value: Any, name: str = "artifact") -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvidenceValidationError(f"{name} must be an object")
    keys = frozenset({"logical_ref", "media_type", "sha256", "byte_count", "role"})
    _require_exact_keys(value, keys, name)
    validate_logical_path(value["logical_ref"], name=f"{name}.logical_ref")
    _require_str(value["media_type"], f"{name}.media_type")
    _require_digest(value["sha256"], f"{name}.sha256")
    _require_int(value["byte_count"], f"{name}.byte_count")
    _require_str(value["role"], f"{name}.role")
    return value


def _validate_generic(record: dict[str, Any]) -> None:
    _require_str(record.get("schema_version"), "schema_version")


REQUEST_KEYS = (
    "schema_version",
    "source",
    "obligation",
    "branch",
    "typed_assumptions",
    "assumption_digest",
    "native_input",
    "tool",
    "resource_limits",
    "expected_result_class",
    "backend_role",
    "unsupported_conclusions",
    "policy_version",
)


def _validate_request(record: dict[str, Any]) -> None:
    if record["schema_version"] != "1.0":
        raise EvidenceValidationError("evidence request schema_version must be 1.0")
    nested = {
        "source": {"logical_id", "file", "label", "digest", "spans", "parser_version"},
        "obligation": {"digest", "target"},
        "branch": {"id", "lineage"},
        "native_input": {"digest", "media_type"},
        "tool": {"name", "adapter_version", "backend_version", "executable_id"},
        "resource_limits": {"timeout_ms", "max_output_bytes"},
    }
    for key, keys in nested.items():
        value = record[key]
        if not isinstance(value, dict):
            raise EvidenceValidationError(f"{key} must be an object")
        _require_exact_keys(value, frozenset(keys), key)
    validate_logical_path(record["source"]["logical_id"], name="source.logical_id")
    validate_logical_path(record["source"]["file"], name="source.file")
    _require_str(record["source"]["label"], "source.label")
    _require_digest(record["source"]["digest"], "source.digest")
    _require_str(record["source"]["parser_version"], "source.parser_version")
    spans = record["source"]["spans"]
    if not isinstance(spans, list):
        raise EvidenceValidationError("source.spans must be an ordered list")
    for index, span in enumerate(spans):
        if not isinstance(span, dict):
            raise EvidenceValidationError(f"source.spans[{index}] must be an object")
        _require_exact_keys(span, frozenset({"start_byte", "end_byte"}), f"source.spans[{index}]")
        start = _require_int(span["start_byte"], f"source.spans[{index}].start_byte")
        end = _require_int(span["end_byte"], f"source.spans[{index}].end_byte")
        if end < start:
            raise EvidenceValidationError("source span end precedes start")
    _require_digest(record["obligation"]["digest"], "obligation.digest")
    _require_str(record["obligation"]["target"], "obligation.target")
    _require_str(record["branch"]["id"], "branch.id")
    if not isinstance(record["branch"]["lineage"], list) or not all(
        isinstance(item, str) and item for item in record["branch"]["lineage"]
    ):
        raise EvidenceValidationError("branch.lineage must be an ordered non-empty-string list")
    if not isinstance(record["typed_assumptions"], list) or not all(
        isinstance(item, dict) and set(item) == {"id", "kind", "statement"}
        for item in record["typed_assumptions"]
    ):
        raise EvidenceValidationError("typed_assumptions has an invalid shape")
    _require_digest(record["assumption_digest"], "assumption_digest")
    _require_digest(record["native_input"]["digest"], "native_input.digest")
    _require_str(record["native_input"]["media_type"], "native_input.media_type")
    for key in ("name", "adapter_version", "backend_version", "executable_id"):
        _require_str(record["tool"][key], f"tool.{key}")
    _require_int(record["resource_limits"]["timeout_ms"], "resource_limits.timeout_ms")
    _require_int(record["resource_limits"]["max_output_bytes"], "resource_limits.max_output_bytes", minimum=1)
    _require_str(record["expected_result_class"], "expected_result_class")
    _require_str(record["backend_role"], "backend_role")
    _require_str(record["policy_version"], "policy_version")
    if not isinstance(record["unsupported_conclusions"], list) or not all(
        isinstance(item, str) and item for item in record["unsupported_conclusions"]
    ):
        raise EvidenceValidationError("unsupported_conclusions must be a non-empty-string list")


MANIFEST_KEYS = (
    "schema_version",
    "request",
    "request_digest",
    "attempt_id",
    "execution_id",
    "run_id",
    "execution",
    "result",
    "integrity",
    "interpretation",
    "evidence_manifest_digest",
)


def _validate_manifest(record: dict[str, Any]) -> None:
    if record["schema_version"] != "1.0":
        raise EvidenceValidationError("evidence manifest schema_version must be 1.0")
    validate_evidence_request(record["request"])
    request_digest = content_digest(record["request"], schema="evidence_request@1")
    if record["request_digest"] != request_digest or record["attempt_id"] != f"att_{request_digest}":
        raise EvidenceValidationError("request_digest/attempt_id does not match request identity")
    _require_str(record["execution_id"], "execution_id")
    _require_str(record["run_id"], "run_id")
    execution = record["execution"]
    if not isinstance(execution, dict):
        raise EvidenceValidationError("execution must be an object")
    execution_keys = frozenset(
        {
            "started_at_utc",
            "ended_at_utc",
            "wall_time_ns",
            "exit_classification",
            "exit_code",
            "signal",
            "timeout",
            "device_execution",
            "environment",
            "runner_version",
        }
    )
    _require_exact_keys(execution, execution_keys, "execution")
    for key in ("started_at_utc", "ended_at_utc"):
        if not UTC_RE.fullmatch(_require_str(execution[key], f"execution.{key}")):
            raise EvidenceValidationError(f"execution.{key} must be canonical UTC seconds")
    _require_int(execution["wall_time_ns"], "execution.wall_time_ns")
    classification = _require_enum(
        execution["exit_classification"],
        {"completed", "timed_out", "runner_exception", "unavailable", "translation_failure"},
        "execution.exit_classification",
    )
    for key in ("exit_code", "signal"):
        if execution[key] is not None:
            _require_int(execution[key], f"execution.{key}", maximum=255)
    if execution["exit_code"] is not None and execution["signal"] is not None:
        raise EvidenceValidationError("execution exit_code and signal are mutually exclusive")
    timeout = _require_bool(execution["timeout"], "execution.timeout")
    if timeout != (classification == "timed_out"):
        raise EvidenceValidationError("execution timeout/classification mismatch")
    device = execution["device_execution"]
    if device != {"mode": "cpu_test_double", "gpu_requested": False, "gpu_initialized": False}:
        raise EvidenceValidationError("device_execution must declare the P01 CPU test-double boundary")
    environment = execution["environment"]
    if not isinstance(environment, dict):
        raise EvidenceValidationError("execution.environment must be an object")
    _require_exact_keys(
        environment,
        frozenset({"python_implementation", "python_version", "platform_system", "test_runner_version"}),
        "execution.environment",
    )
    for key, value in environment.items():
        token = _require_str(value, f"execution.environment.{key}")
        if len(token) > 128 or "/" in token or "\\" in token or "=" in token:
            raise EvidenceValidationError(f"execution.environment.{key} contains private/unbounded data")
    _require_str(execution["runner_version"], "execution.runner_version")

    result = record["result"]
    if not isinstance(result, dict):
        raise EvidenceValidationError("result must be an object")
    result_keys = frozenset(
        {
            "outcome",
            "stdout",
            "stderr",
            "structured_result",
            "stdout_truncated",
            "stderr_truncated",
            "redaction",
            "certificate",
        }
    )
    _require_exact_keys(result, result_keys, "result")
    outcome = _require_enum(
        result["outcome"],
        {
            "certified",
            "refuted",
            "unknown",
            "unsupported",
            "unavailable",
            "translation_error",
            "execution_error",
            "timeout",
            "integrity_error",
        },
        "result.outcome",
    )
    for key in ("stdout", "stderr", "structured_result"):
        _require_artifact_entry(result[key], f"result.{key}")
    for key in ("stdout_truncated", "stderr_truncated"):
        _require_bool(result[key], f"result.{key}")
    redaction = result["redaction"]
    if not isinstance(redaction, dict):
        raise EvidenceValidationError("result.redaction must be an object")
    _require_exact_keys(redaction, frozenset({"applied", "fields"}), "result.redaction")
    _require_bool(redaction["applied"], "result.redaction.applied")
    if not isinstance(redaction["fields"], list) or not all(isinstance(item, str) for item in redaction["fields"]):
        raise EvidenceValidationError("result.redaction.fields must be a string list")
    if result["certificate"] is not None:
        _require_artifact_entry(result["certificate"], "result.certificate")

    integrity = record["integrity"]
    if not isinstance(integrity, dict):
        raise EvidenceValidationError("integrity must be an object")
    _require_exact_keys(
        integrity,
        frozenset({"request_artifact", "artifact_inventory", "atomic_write_state", "integrity_state"}),
        "integrity",
    )
    _require_artifact_entry(integrity["request_artifact"], "integrity.request_artifact")
    if not isinstance(integrity["artifact_inventory"], list):
        raise EvidenceValidationError("integrity.artifact_inventory must be ordered")
    refs: set[str] = set()
    for index, artifact in enumerate(integrity["artifact_inventory"]):
        entry = _require_artifact_entry(artifact, f"integrity.artifact_inventory[{index}]")
        if entry["logical_ref"] in refs:
            raise EvidenceValidationError("artifact inventory contains duplicate refs")
        refs.add(entry["logical_ref"])
    inventory_by_ref = {entry["logical_ref"]: entry for entry in integrity["artifact_inventory"]}
    named_artifacts = [
        result["stdout"],
        result["stderr"],
        result["structured_result"],
        integrity["request_artifact"],
    ]
    if result["certificate"] is not None:
        named_artifacts.append(result["certificate"])
    if any(inventory_by_ref.get(entry["logical_ref"]) != entry for entry in named_artifacts):
        raise EvidenceValidationError("named request/result artifacts must exactly match artifact_inventory entries")
    if integrity["atomic_write_state"] != "manifest_published_last_no_overwrite":
        raise EvidenceValidationError("invalid atomic_write_state")
    if integrity["integrity_state"] != "sealed_pending_reader_verification":
        raise EvidenceValidationError("persisted integrity_state must remain pending reader verification")

    interpretation = record["interpretation"]
    if not isinstance(interpretation, dict):
        raise EvidenceValidationError("interpretation must be an object")
    _require_exact_keys(
        interpretation,
        frozenset({"certified_scope", "refuted_scope", "unresolved_assumption_ids", "blocker_ids", "veto_ids", "non_claims"}),
        "interpretation",
    )
    if interpretation["certified_scope"] is not None and interpretation["refuted_scope"] is not None:
        raise EvidenceValidationError("certified_scope and refuted_scope are mutually exclusive")
    for key in ("certified_scope", "refuted_scope"):
        if interpretation[key] is not None:
            _require_str(interpretation[key], f"interpretation.{key}")
    for key in ("unresolved_assumption_ids", "blocker_ids", "veto_ids", "non_claims"):
        if not isinstance(interpretation[key], list) or not all(isinstance(item, str) for item in interpretation[key]):
            raise EvidenceValidationError(f"interpretation.{key} must be a string list")
    if (outcome == "certified") != (interpretation["certified_scope"] is not None):
        raise EvidenceValidationError("certified outcome/scope mismatch")
    if (outcome == "refuted") != (interpretation["refuted_scope"] is not None):
        raise EvidenceValidationError("refuted outcome/scope mismatch")
    _validate_non_claims(interpretation["non_claims"])

    manifest_without_digest = dict(record)
    manifest_without_digest.pop("evidence_manifest_digest")
    expected = content_digest(manifest_without_digest)
    if record["evidence_manifest_digest"] != expected:
        raise EvidenceValidationError("evidence_manifest_digest mismatch")


def _validate_bundle_index(record: dict[str, Any]) -> None:
    if record["schema_version"] != "1.0" or record["index_kind"] != "payload_bundle_index":
        raise EvidenceValidationError("invalid payload bundle index metadata")
    if record["exclusions"] != ["bundle-index.json", "phase-results/", "review-governance/"]:
        raise EvidenceValidationError("payload bundle index exclusions are not exact")
    if not isinstance(record["artifacts"], list):
        raise EvidenceValidationError("bundle artifacts must be ordered")
    refs = []
    for index, value in enumerate(record["artifacts"]):
        refs.append(_require_artifact_entry(value, f"artifacts[{index}]")["logical_ref"])
    if refs != sorted(refs):
        raise EvidenceValidationError("bundle artifacts must sort by logical ref")
    if len(refs) != len(set(refs)):
        raise EvidenceValidationError("bundle artifacts contain duplicate refs")


def _validate_vetoes(value: Any) -> None:
    if not isinstance(value, dict) or set(value) != P01_VETO_KEYS or any(type(item) is not bool for item in value.values()):
        raise EvidenceValidationError("vetoes must be the exact P01 boolean map")


def _validate_non_claims(value: Any) -> None:
    if not isinstance(value, list) or set(value) != P01_NON_CLAIMS or len(value) != len(P01_NON_CLAIMS):
        raise EvidenceValidationError("non_claims must contain exactly the P01 non-claim ids")


def _require_string_list(value: Any, name: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value) or not all(
        isinstance(item, str) and item for item in value
    ):
        raise EvidenceValidationError(f"{name} must be an ordered non-empty-string list")
    return value


def _validate_environment(value: Any, name: str = "environment") -> None:
    if not isinstance(value, dict):
        raise EvidenceValidationError(f"{name} must be an object")
    keys = frozenset({"python_implementation", "python_version", "platform_system", "test_runner_version"})
    _require_exact_keys(value, keys, name)
    for key, item in value.items():
        token = _require_str(item, f"{name}.{key}")
        if len(token) > 128 or "/" in token or "\\" in token or "=" in token:
            raise EvidenceValidationError(f"{name}.{key} contains private or unbounded data")


def _validate_device_execution(value: Any, name: str = "device_execution") -> None:
    expected = {"mode": "cpu_test_double", "gpu_requested": False, "gpu_initialized": False}
    if value != expected:
        raise EvidenceValidationError(f"{name} must declare the P01 CPU test-double boundary")


def _validate_tool_consideration(value: Any, name: str) -> None:
    if not isinstance(value, dict):
        raise EvidenceValidationError(f"{name} must be an object")
    keys = frozenset(
        {
            "tool",
            "observed_availability_version_evidence",
            "possible_role",
            "selected",
            "reason_not_selected",
            "certifying_status",
            "phase_boundary",
        }
    )
    _require_exact_keys(value, keys, name)
    for key in keys - {"selected"}:
        _require_str(value[key], f"{name}.{key}", nonempty=False)
    _require_bool(value["selected"], f"{name}.selected")


def _validate_random_seed_policy(value: Any) -> None:
    if not isinstance(value, dict):
        raise EvidenceValidationError("random_seed_policy must be an object")
    keys = frozenset({"pseudorandom_test_seeds", "runtime_id_source", "runtime_ids_recorded", "boundary"})
    _require_exact_keys(value, keys, "random_seed_policy")
    seeds = value["pseudorandom_test_seeds"]
    if not isinstance(seeds, list):
        raise EvidenceValidationError("random_seed_policy.pseudorandom_test_seeds must be ordered")
    for index, seed in enumerate(seeds):
        _require_int(seed, f"random_seed_policy.pseudorandom_test_seeds[{index}]")
    if value["runtime_id_source"] != "secrets_token_hex_128":
        raise EvidenceValidationError("invalid random_seed_policy.runtime_id_source")
    _require_bool(value["runtime_ids_recorded"], "random_seed_policy.runtime_ids_recorded")
    if value["boundary"] != "runtime_ids_are_uniqueness_not_scientific_randomness":
        raise EvidenceValidationError("invalid random_seed_policy.boundary")


def _validate_run_manifest(record: dict[str, Any]) -> None:
    if record["schema_version"] != "p01_run_manifest@1" or record["phase"] != "P01":
        raise EvidenceValidationError("invalid run-manifest metadata")
    _require_round(record["result_round"])
    if not GIT_COMMIT_RE.fullmatch(_require_str(record["git_commit"], "git_commit")):
        raise EvidenceValidationError("git_commit must be a lower-case 40-hex object id")
    for key in (
        "implementation_entry_manifest_sha256",
        "implementation_exit_manifest_sha256",
        "implementation_diff_digest",
        "pre_candidate_receipt_index_sha256",
        "plan_sha256",
        "result_sha256",
    ):
        _require_digest(record[key], key)
    for key in (
        "pre_candidate_receipt_index_ref",
        "governance_receipt_family_ref",
        "plan_ref",
        "result_ref",
    ):
        validate_logical_path(record[key], name=key)
    _validate_environment(record["environment"])
    _validate_device_execution(record["device_execution"])
    _require_str(record["synthetic_data_version"], "synthetic_data_version")
    _validate_random_seed_policy(record["random_seed_policy"])
    inventory = record["artifact_inventory"]
    if not isinstance(inventory, list):
        raise EvidenceValidationError("artifact_inventory must be ordered")
    for index, item in enumerate(inventory):
        _require_artifact_entry(item, f"artifact_inventory[{index}]")
    considerations = record["external_tool_considerations"]
    if not isinstance(considerations, list):
        raise EvidenceValidationError("external_tool_considerations must be a list")
    for index, item in enumerate(considerations):
        _validate_tool_consideration(item, f"external_tool_considerations[{index}]")
    for key in ("started_at_utc", "ended_at_utc"):
        if not UTC_RE.fullmatch(_require_str(record[key], key)):
            raise EvidenceValidationError(f"{key} must be canonical UTC seconds")
    _require_int(record["wall_time_ns"], "wall_time_ns")
    _validate_non_claims(record["non_claims"])


def _validate_predecessor(value: Any, result_round: str) -> None:
    if not isinstance(value, dict):
        raise EvidenceValidationError("predecessor must be an object")
    keys = frozenset(
        {
            "entry_implementation_manifest_sha256",
            "entry_protected_manifest_sha256",
            "bootstrap_close_ref",
            "bootstrap_close_sha256",
            "prior_result_round",
            "prior_round_close_ref",
            "prior_round_close_sha256",
            "prior_terminal_receipt_index_ref",
            "prior_terminal_receipt_index_sha256",
        }
    )
    _require_exact_keys(value, keys, "predecessor")
    for key in ("entry_implementation_manifest_sha256", "entry_protected_manifest_sha256", "bootstrap_close_sha256"):
        _require_digest(value[key], f"predecessor.{key}")
    validate_logical_path(value["bootstrap_close_ref"], name="predecessor.bootstrap_close_ref")
    prior_keys = (
        "prior_result_round",
        "prior_round_close_ref",
        "prior_round_close_sha256",
        "prior_terminal_receipt_index_ref",
        "prior_terminal_receipt_index_sha256",
    )
    prior_values = [value[key] for key in prior_keys]
    if result_round == "rr01":
        if any(item is not None for item in prior_values):
            raise EvidenceValidationError("rr01 predecessor prior-round fields must all be null")
        return
    expected = f"rr{int(result_round[2:]) - 1:02d}"
    if any(item is None for item in prior_values) or value["prior_result_round"] != expected:
        raise EvidenceValidationError("candidate predecessor must bind the immediately prior round")
    for key in ("prior_round_close_ref", "prior_terminal_receipt_index_ref"):
        validate_logical_path(value[key], name=f"predecessor.{key}")
    for key in ("prior_round_close_sha256", "prior_terminal_receipt_index_sha256"):
        _require_digest(value[key], f"predecessor.{key}")


P01_PRIMARY_CRITERION_KEYS = frozenset(
    {
        "canonical_vectors_pass",
        "artifact_store_pass",
        "manifest_contract_pass",
        "mutation_matrix_pass",
        "parallel_identity_pass",
        "legacy_matrix_pass",
        "integrity_binding_fixture_pass",
        "claim_eligibility_ineligible",
        "publication_quarantine_pass",
        "all_pass",
    }
)


def _validate_primary_criterion(value: Any) -> None:
    if not isinstance(value, dict):
        raise EvidenceValidationError("primary_criterion must be an object")
    _require_exact_keys(value, P01_PRIMARY_CRITERION_KEYS, "primary_criterion")
    if any(type(item) is not bool for item in value.values()):
        raise EvidenceValidationError("primary_criterion values must be booleans")
    expected = all(value[key] for key in P01_PRIMARY_CRITERION_KEYS - {"all_pass"})
    if value["all_pass"] != expected:
        raise EvidenceValidationError("primary_criterion.all_pass must be the exact conjunction")


def _validate_candidate_decision(record: dict[str, Any]) -> None:
    if record["schema_version"] != "p01_candidate_decision@1" or record["phase"] != "P01":
        raise EvidenceValidationError("invalid candidate-decision metadata")
    result_round = _require_round(record["result_round"])
    if (
        record["decision"] != "candidate_pass_pending_independent_result_review"
        or record["publication_mode"] != "disabled"
        or record["claim_eligibility"] != "ineligible"
        or record["integrity_binding_status"] != "verified_for_synthetic_fixture"
    ):
        raise EvidenceValidationError("candidate-decision constants are invalid")
    _validate_predecessor(record["predecessor"], result_round)
    for stem in ("run_manifest", "result", "pre_candidate_receipt_index", "payload_bundle_index"):
        ref_key = f"{stem}_ref"
        if ref_key in record:
            validate_logical_path(record[ref_key], name=ref_key)
    for key in (
        "run_manifest_sha256",
        "result_sha256",
        "pre_candidate_receipt_index_sha256",
        "implementation_exit_manifest_sha256",
        "payload_bundle_index_digest",
        "payload_bundle_index_file_sha256",
    ):
        _require_digest(record[key], key)
    _validate_primary_criterion(record["primary_criterion"])
    if not record["primary_criterion"]["all_pass"]:
        raise EvidenceValidationError("candidate decision requires all primary criteria")
    _validate_vetoes(record["vetoes"])
    if any(record["vetoes"].values()):
        raise EvidenceValidationError("candidate decision cannot contain a true veto")
    _validate_non_claims(record["non_claims"])


P01_SCOPED_REPAIR_KEYS = frozenset(
    {"finding_id", "source_stage", "severity", "affected_paths", "required_change", "required_check_ids", "non_claim"}
)


def _validate_scoped_repair_entry(value: Any, name: str) -> None:
    if not isinstance(value, dict):
        raise EvidenceValidationError(f"{name} must be an object")
    _require_exact_keys(value, P01_SCOPED_REPAIR_KEYS, name)
    _require_str(value["finding_id"], f"{name}.finding_id")
    _require_enum(
        value["source_stage"],
        {"local_check", "candidate_gate", "result_review", "final_seal_audit"},
        f"{name}.source_stage",
    )
    _require_enum(value["severity"], {"high", "medium", "low"}, f"{name}.severity")
    paths = _require_string_list(value["affected_paths"], f"{name}.affected_paths", nonempty=True)
    for index, path in enumerate(paths):
        validate_logical_path(path, name=f"{name}.affected_paths[{index}]")
    _require_str(value["required_change"], f"{name}.required_change")
    _require_string_list(value["required_check_ids"], f"{name}.required_check_ids", nonempty=True)
    _require_str(value["non_claim"], f"{name}.non_claim")


def _validate_log_entry(value: Any, name: str) -> None:
    if not isinstance(value, dict):
        raise EvidenceValidationError(f"{name} must be an object")
    keys = frozenset({"logical_ref", "sha256", "byte_count", "role", "exit_code"})
    _require_exact_keys(value, keys, name)
    validate_logical_path(value["logical_ref"], name=f"{name}.logical_ref")
    _require_digest(value["sha256"], f"{name}.sha256")
    _require_int(value["byte_count"], f"{name}.byte_count")
    _require_str(value["role"], f"{name}.role")
    if value["exit_code"] is not None:
        _require_int(value["exit_code"], f"{name}.exit_code", maximum=255)


def _validate_round_close(record: dict[str, Any]) -> None:
    if record["schema_version"] != "p01_round_close@1" or record["phase"] != "P01":
        raise EvidenceValidationError("invalid round-close metadata")
    result_round = _require_round(record["result_round"])
    reason = _require_enum(record["close_reason"], P01_CLOSE_REASONS, "close_reason")
    reviewed_revise = reason in {"result_review_revise", "final_seal_audit_revise"}
    if reviewed_revise:
        if record["failed_action"] is not None:
            raise EvidenceValidationError("reviewed REVISE close must not name failed_action")
    else:
        check_id = _require_str(record["failed_action"], "failed_action")
        if check_id not in P01_RECEIPT_BINDING_KEYS or check_id in {
            "result_review_binding",
            "final_seal_audit_binding",
            "bind_scoped_repair",
            "close_round",
            "stable_publication",
        }:
            raise EvidenceValidationError("failed_action is not a valid local/candidate action")
    for key in (
        "entry_implementation_manifest_sha256",
        "entry_protected_manifest_sha256",
        "bootstrap_close_sha256",
        "implementation_exit_manifest_sha256",
        "receipt_index_before_close_sha256",
    ):
        _require_digest(record[key], key)
    for key in ("bootstrap_close_ref", "receipt_index_before_close_ref"):
        validate_logical_path(record[key], name=key)
    predecessor_keys = (
        "predecessor_close_ref",
        "predecessor_close_sha256",
        "predecessor_terminal_receipt_index_ref",
        "predecessor_terminal_receipt_index_sha256",
    )
    predecessor_values = [record[key] for key in predecessor_keys]
    if result_round == "rr01":
        if any(item is not None for item in predecessor_values):
            raise EvidenceValidationError("rr01 round-close predecessor fields must be null")
    else:
        if any(item is None for item in predecessor_values):
            raise EvidenceValidationError("successor round-close predecessor fields must be non-null")
        for key in ("predecessor_close_ref", "predecessor_terminal_receipt_index_ref"):
            validate_logical_path(record[key], name=key)
        for key in ("predecessor_close_sha256", "predecessor_terminal_receipt_index_sha256"):
            _require_digest(record[key], key)
    if not isinstance(record["log_inventory"], list):
        raise EvidenceValidationError("log_inventory must be ordered")
    for index, item in enumerate(record["log_inventory"]):
        _validate_log_entry(item, f"log_inventory[{index}]")
    if not isinstance(record["scoped_repairs"], list) or not record["scoped_repairs"]:
        raise EvidenceValidationError("scoped_repairs must be a nonempty ordered list")
    expected_stage = {
        "local_check_failure": "local_check",
        "candidate_gate_failure": "candidate_gate",
        "result_review_revise": "result_review",
        "final_seal_audit_revise": "final_seal_audit",
    }[reason]
    for index, item in enumerate(record["scoped_repairs"]):
        _validate_scoped_repair_entry(item, f"scoped_repairs[{index}]")
        if item["source_stage"] != expected_stage:
            raise EvidenceValidationError("scoped repair source_stage does not match close_reason")

    stage_pairs = (
        ("run_manifest_ref", "run_manifest_sha256"),
        ("result_ref", "result_sha256"),
        ("candidate_ref", "candidate_sha256"),
        ("result_review_ref", "result_review_sha256"),
        ("final_decision_candidate_ref", "final_decision_candidate_sha256"),
        ("final_seal_audit_ref", "final_seal_audit_sha256"),
    )
    required_by_reason = {
        "local_check_failure": (None, None, False, False, False, False),
        "candidate_gate_failure": (True, True, True, False, False, False),
        "result_review_revise": (True, True, True, True, False, False),
        "final_seal_audit_revise": (True, True, True, True, True, True),
    }[reason]
    for (ref_key, digest_key), required in zip(stage_pairs, required_by_reason, strict=True):
        if required is True:
            _require_ref_digest(record, ref_key, digest_key)
        elif required is False and (record[ref_key] is not None or record[digest_key] is not None):
            raise EvidenceValidationError(f"{ref_key}/{digest_key} must be null for {reason}")
        else:
            _require_ref_digest(record, ref_key, digest_key, nullable=True)
    if record["run_manifest_ref"] is not None and record["result_ref"] is None:
        raise EvidenceValidationError("run_manifest cannot be present before result binding")
    verdict = record["result_review_verdict"]
    if reason in {"local_check_failure", "candidate_gate_failure"}:
        if verdict is not None:
            raise EvidenceValidationError("pre-review close must have null result_review_verdict")
    else:
        expected_verdict = "REVISE" if reason == "result_review_revise" else "AGREE"
        if verdict != expected_verdict:
            raise EvidenceValidationError(f"{reason} requires result_review_verdict {expected_verdict}")
    _validate_vetoes(record["vetoes"])
    _validate_non_claims(record["non_claims"])


def _validate_scoped_repair(record: dict[str, Any]) -> None:
    if record["schema_version"] != "p01_scoped_repair@1" or record["phase"] != "P01":
        raise EvidenceValidationError("invalid scoped-repair metadata")
    _require_round(record["result_round"])
    reason = _require_enum(record["close_reason"], P01_CLOSE_REASONS, "close_reason")
    for stem in ("source_artifact", "source_receipt_index"):
        _require_ref_digest(record, f"{stem}_ref", f"{stem}_sha256")
    if not isinstance(record["repairs"], list) or not record["repairs"]:
        raise EvidenceValidationError("repairs must be a nonempty ordered list")
    expected_stage = {
        "local_check_failure": "local_check",
        "candidate_gate_failure": "candidate_gate",
        "result_review_revise": "result_review",
        "final_seal_audit_revise": "final_seal_audit",
    }[reason]
    for index, item in enumerate(record["repairs"]):
        _validate_scoped_repair_entry(item, f"repairs[{index}]")
        if item["source_stage"] != expected_stage:
            raise EvidenceValidationError("repair source_stage does not match close_reason")


def _validate_final_decision(record: dict[str, Any]) -> None:
    _require_round(record["result_round"])
    if record["schema_version"] != "p01_final_decision@1" or record["phase"] != "P01":
        raise EvidenceValidationError("invalid final-decision metadata")
    if record["decision"] != "pass" or record["publication_mode"] != "disabled":
        raise EvidenceValidationError("final decision constants are invalid")
    for key in (
        "payload_bundle_index_digest",
        "payload_bundle_index_file_sha256",
        "candidate_decision_sha256",
        "result_review_sha256",
        "reviewed_receipt_index_sha256",
    ):
        _require_digest(record[key], key)
    for key in ("candidate_decision_ref", "result_review_ref", "reviewed_receipt_index_ref"):
        validate_logical_path(record[key], name=key)
    _validate_vetoes(record["vetoes"])
    if any(record["vetoes"].values()):
        raise EvidenceValidationError("a pass final decision cannot contain a true veto")
    _validate_non_claims(record["non_claims"])


def _validate_receipt(record: dict[str, Any]) -> None:
    if record["schema_version"] != "p01_command_receipt@1" or record["phase"] != "P01":
        raise EvidenceValidationError("invalid receipt metadata")
    _require_round(record["result_round"])
    sequence = _require_int(record["sequence"], "sequence", minimum=1)
    check_id = _require_str(record["check_id"], "check_id")
    if check_id not in P01_RECEIPT_BINDING_KEYS:
        raise EvidenceValidationError("receipt check_id is not in the closed P01 registry")
    if not isinstance(record["command_argv"], list) or not record["command_argv"] or not all(
        isinstance(item, str) for item in record["command_argv"]
    ):
        raise EvidenceValidationError("command_argv must be a nonempty ordered string list")
    for key in ("started_at_utc", "ended_at_utc"):
        if not UTC_RE.fullmatch(_require_str(record[key], key)):
            raise EvidenceValidationError(f"{key} must be canonical UTC seconds")
    _require_int(record["wall_time_ns"], "wall_time_ns")
    _require_int(record["exit_code"], "exit_code", maximum=255)
    for stem in ("stdout", "stderr"):
        validate_logical_path(record[f"{stem}_ref"], name=f"{stem}_ref")
        _require_digest(record[f"{stem}_sha256"], f"{stem}_sha256")
        _require_int(record[f"{stem}_byte_count"], f"{stem}_byte_count")
    if sequence == 1:
        if record["prior_receipt_sha256"] is not None:
            raise EvidenceValidationError("first receipt prior digest must be null")
    else:
        _require_digest(record["prior_receipt_sha256"], "prior_receipt_sha256")
    bindings = record["bindings"]
    if not isinstance(bindings, dict):
        raise EvidenceValidationError("receipt bindings must be an object")
    _require_exact_keys(bindings, P01_RECEIPT_BINDING_KEYS[check_id], f"receipt bindings for {check_id}")
    for key, value in bindings.items():
        if key in {"same_inode", "same_digest"}:
            if value is not None and _require_bool(value, f"bindings.{key}") is not True:
                raise EvidenceValidationError(f"bindings.{key} must be true")
        elif key.endswith("_ref"):
            if value is not None:
                validate_logical_path(value, name=f"bindings.{key}")
        elif key.endswith("_sha256") or key == "payload_bundle_index_digest":
            if value is not None:
                _require_digest(value, f"bindings.{key}")
        else:
            _require_str(value, f"bindings.{key}")
    if check_id == "init_round":
        for key in (
            "bootstrap_close_ref",
            "bootstrap_close_sha256",
            "bootstrap_shell_verification_ref",
            "bootstrap_shell_verification_sha256",
            "entry_implementation_manifest_sha256",
            "entry_protected_manifest_sha256",
            "implementation_exit_manifest_ref",
            "implementation_exit_manifest_sha256",
        ):
            if bindings[key] is None:
                raise EvidenceValidationError(f"init_round binding {key} must be non-null")
        prior_keys = (
            "prior_round_close_ref",
            "prior_round_close_sha256",
            "prior_terminal_receipt_index_ref",
            "prior_terminal_receipt_index_sha256",
        )
        if record["result_round"] == "rr01":
            if any(bindings[key] is not None for key in prior_keys):
                raise EvidenceValidationError("rr01 init_round prior bindings must all be null")
        elif any(bindings[key] is None for key in prior_keys):
            raise EvidenceValidationError("successor init_round prior bindings must all be non-null")
    elif record["exit_code"] == 0 and any(value is None for value in bindings.values()):
        raise EvidenceValidationError(f"receipt bindings for {check_id} must be non-null")


def _validate_receipt_index(record: dict[str, Any]) -> None:
    if record["schema_version"] != "p01_receipt_index@1" or record["phase"] != "P01":
        raise EvidenceValidationError("invalid receipt-index metadata")
    _require_round(record["result_round"])
    receipts = record["receipts"]
    if not isinstance(receipts, list) or not receipts:
        raise EvidenceValidationError("receipt index must contain at least one receipt")
    for expected, entry in enumerate(receipts, start=1):
        if not isinstance(entry, dict):
            raise EvidenceValidationError("receipt index entry must be an object")
        _require_exact_keys(entry, frozenset({"sequence", "check_id", "receipt_ref", "receipt_sha256"}), "receipt entry")
        if entry["sequence"] != expected:
            raise EvidenceValidationError("receipt sequences must be contiguous")
        check_id = _require_str(entry["check_id"], "receipt.check_id")
        if check_id not in P01_RECEIPT_BINDING_KEYS:
            raise EvidenceValidationError("receipt index contains an unknown check_id")
        validate_logical_path(entry["receipt_ref"], name="receipt.receipt_ref")
        _require_digest(entry["receipt_sha256"], "receipt.receipt_sha256")
    if record["head_sequence"] != receipts[-1]["sequence"] or record["head_sha256"] != receipts[-1]["receipt_sha256"]:
        raise EvidenceValidationError("receipt index head mismatch")


def _validate_summary(record: dict[str, Any]) -> None:
    _require_round(record["result_round"])
    if record["schema_version"] != "p01_summary@1" or record["phase"] != "P01" or not isinstance(record["cases"], list):
        raise EvidenceValidationError("invalid P01 summary")
    _require_bool(record["all_pass"], "all_pass")


def _validate_case_summary(record: dict[str, Any], schema_version: str, keys: frozenset[str]) -> None:
    if record["schema_version"] != schema_version or record["phase"] != "P01":
        raise EvidenceValidationError(f"invalid {schema_version} metadata")
    _require_round(record["result_round"])
    cases = record["cases"]
    if not isinstance(cases, list):
        raise EvidenceValidationError(f"{schema_version}.cases must be ordered")
    for index, case in enumerate(cases):
        if not isinstance(case, dict):
            raise EvidenceValidationError(f"{schema_version}.cases[{index}] must be an object")
        _require_exact_keys(case, keys, f"{schema_version}.cases[{index}]")
        _require_str(case["case_id"], f"{schema_version}.cases[{index}].case_id")
        _require_bool(case["passed"], f"{schema_version}.cases[{index}].passed")
    all_pass = _require_bool(record["all_pass"], "all_pass")
    if all_pass != all(case["passed"] for case in cases):
        raise EvidenceValidationError(f"{schema_version}.all_pass must be the exact conjunction")


def _validate_mutation_summary(record: dict[str, Any]) -> None:
    keys = frozenset({"case_id", "mutated_field", "expected_veto_id", "observed_veto_ids", "passed"})
    _validate_case_summary(record, "p01_mutation_summary@1", keys)
    for index, case in enumerate(record["cases"]):
        for key in ("mutated_field", "expected_veto_id"):
            _require_str(case[key], f"cases[{index}].{key}")
        _require_string_list(case["observed_veto_ids"], f"cases[{index}].observed_veto_ids")


def _validate_parallel_summary(record: dict[str, Any]) -> None:
    keys = frozenset(
        {"case_id", "request_equal", "attempt_equal", "execution_distinct", "run_distinct", "deterministic_index", "passed"}
    )
    _validate_case_summary(record, "p01_parallel_summary@1", keys)
    for index, case in enumerate(record["cases"]):
        for key in keys - {"case_id"}:
            _require_bool(case[key], f"cases[{index}].{key}")
        expected = all(case[key] for key in keys - {"case_id", "passed"})
        if case["passed"] != expected:
            raise EvidenceValidationError("parallel case passed must be the exact conjunction")


def _validate_legacy_summary(record: dict[str, Any]) -> None:
    keys = frozenset(
        {"case_id", "input_schema_class", "expected_certification_state", "observed_certification_state", "passed"}
    )
    _validate_case_summary(record, "p01_legacy_summary@1", keys)
    for index, case in enumerate(record["cases"]):
        for key in keys - {"case_id", "passed"}:
            _require_str(case[key], f"cases[{index}].{key}")


def _validate_generator_result(record: dict[str, Any]) -> None:
    if record["schema_version"] != "p01_generator_result@1" or record["phase"] != "P01":
        raise EvidenceValidationError("invalid generator-result metadata")
    _require_round(record["result_round"])
    validate_logical_path(record["bundle_ref"], name="bundle_ref")
    _require_digest(record["payload_bundle_index_digest"], "payload_bundle_index_digest")
    _require_digest(record["payload_bundle_index_file_sha256"], "payload_bundle_index_file_sha256")
    if record["disk_verification_state"] != "verified":
        raise EvidenceValidationError("generator disk_verification_state must be verified")
    _require_string_list(record["invariant_ids"], "invariant_ids", nonempty=True)
    if _require_bool(record["all_pass"], "all_pass") is not True:
        raise EvidenceValidationError("generator result all_pass must be true")


_register("evidence_request@1", REQUEST_KEYS, _validate_request)
_register("evidence_manifest@1", MANIFEST_KEYS, _validate_manifest)
_register("payload_bundle_index@1", ("schema_version", "index_kind", "exclusions", "artifacts"), _validate_bundle_index)
_register(
    "p01_run_manifest@1",
    (
        "schema_version",
        "phase",
        "result_round",
        "git_commit",
        "implementation_entry_manifest_sha256",
        "implementation_exit_manifest_sha256",
        "implementation_diff_digest",
        "pre_candidate_receipt_index_ref",
        "pre_candidate_receipt_index_sha256",
        "governance_receipt_family_ref",
        "environment",
        "device_execution",
        "synthetic_data_version",
        "random_seed_policy",
        "plan_ref",
        "plan_sha256",
        "result_ref",
        "result_sha256",
        "artifact_inventory",
        "external_tool_considerations",
        "started_at_utc",
        "ended_at_utc",
        "wall_time_ns",
        "non_claims",
    ),
    _validate_run_manifest,
)
_register(
    "p01_candidate_decision@1",
    (
        "schema_version",
        "phase",
        "result_round",
        "decision",
        "publication_mode",
        "claim_eligibility",
        "integrity_binding_status",
        "predecessor",
        "run_manifest_ref",
        "run_manifest_sha256",
        "result_ref",
        "result_sha256",
        "pre_candidate_receipt_index_ref",
        "pre_candidate_receipt_index_sha256",
        "implementation_exit_manifest_sha256",
        "payload_bundle_index_ref",
        "payload_bundle_index_digest",
        "payload_bundle_index_file_sha256",
        "primary_criterion",
        "vetoes",
        "non_claims",
    ),
    _validate_candidate_decision,
)
_register(
    "p01_round_close@1",
    (
        "schema_version",
        "phase",
        "result_round",
        "close_reason",
        "failed_action",
        "entry_implementation_manifest_sha256",
        "entry_protected_manifest_sha256",
        "bootstrap_close_ref",
        "bootstrap_close_sha256",
        "predecessor_close_ref",
        "predecessor_close_sha256",
        "predecessor_terminal_receipt_index_ref",
        "predecessor_terminal_receipt_index_sha256",
        "implementation_exit_manifest_sha256",
        "receipt_index_before_close_ref",
        "receipt_index_before_close_sha256",
        "log_inventory",
        "run_manifest_ref",
        "run_manifest_sha256",
        "result_ref",
        "result_sha256",
        "candidate_ref",
        "candidate_sha256",
        "result_review_ref",
        "result_review_sha256",
        "result_review_verdict",
        "final_decision_candidate_ref",
        "final_decision_candidate_sha256",
        "final_seal_audit_ref",
        "final_seal_audit_sha256",
        "scoped_repairs",
        "vetoes",
        "non_claims",
    ),
    _validate_round_close,
)
_register(
    "p01_scoped_repair@1",
    (
        "schema_version",
        "phase",
        "result_round",
        "close_reason",
        "source_artifact_ref",
        "source_artifact_sha256",
        "source_receipt_index_ref",
        "source_receipt_index_sha256",
        "repairs",
    ),
    _validate_scoped_repair,
)
_register(
    "p01_final_decision@1",
    (
        "schema_version",
        "phase",
        "result_round",
        "decision",
        "publication_mode",
        "payload_bundle_index_digest",
        "payload_bundle_index_file_sha256",
        "candidate_decision_ref",
        "candidate_decision_sha256",
        "result_review_ref",
        "result_review_sha256",
        "reviewed_receipt_index_ref",
        "reviewed_receipt_index_sha256",
        "vetoes",
        "non_claims",
    ),
    _validate_final_decision,
)
_register(
    "p01_command_receipt@1",
    (
        "schema_version",
        "phase",
        "result_round",
        "sequence",
        "check_id",
        "command_argv",
        "started_at_utc",
        "ended_at_utc",
        "wall_time_ns",
        "exit_code",
        "stdout_ref",
        "stdout_sha256",
        "stdout_byte_count",
        "stderr_ref",
        "stderr_sha256",
        "stderr_byte_count",
        "prior_receipt_sha256",
        "bindings",
    ),
    _validate_receipt,
)
_register(
    "p01_receipt_index@1",
    ("schema_version", "phase", "result_round", "receipts", "head_sequence", "head_sha256"),
    _validate_receipt_index,
)
_register("p01_summary@1", ("schema_version", "phase", "result_round", "cases", "all_pass"), _validate_summary)
_register(
    "p01_mutation_summary@1",
    ("schema_version", "phase", "result_round", "cases", "all_pass"),
    _validate_mutation_summary,
)
_register(
    "p01_parallel_summary@1",
    ("schema_version", "phase", "result_round", "cases", "all_pass"),
    _validate_parallel_summary,
)
_register(
    "p01_legacy_summary@1",
    ("schema_version", "phase", "result_round", "cases", "all_pass"),
    _validate_legacy_summary,
)
_register(
    "p01_generator_result@1",
    (
        "schema_version",
        "phase",
        "result_round",
        "bundle_ref",
        "payload_bundle_index_digest",
        "payload_bundle_index_file_sha256",
        "disk_verification_state",
        "invariant_ids",
        "all_pass",
    ),
    _validate_generator_result,
)


def _schema_spec(schema: str | SchemaSpec | None) -> SchemaSpec | None:
    if schema is None:
        return None
    if isinstance(schema, SchemaSpec):
        return schema
    try:
        return _SCHEMAS[schema]
    except KeyError as exc:
        raise EvidenceValidationError(f"unknown schema: {schema}") from exc


def validate_schema(value: Any, *, schema: str | SchemaSpec) -> dict[str, Any]:
    spec = _schema_spec(schema)
    if not isinstance(value, dict):
        raise EvidenceValidationError(f"{spec.name} requires a JSON object")
    _require_exact_keys(value, spec.required_keys, spec.name)
    spec.validator(value)
    return value


def canonical_json_bytes(value: Any, *, schema: str | SchemaSpec | None = None) -> bytes:
    normalized = _normalize_json(value)
    spec = _schema_spec(schema)
    if spec is not None:
        validate_schema(normalized, schema=spec)
    return json.dumps(
        normalized,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def content_digest(bytes_or_value: bytes | bytearray | memoryview | Any, *, schema: str | SchemaSpec | None = None) -> str:
    if isinstance(bytes_or_value, (bytes, bytearray, memoryview)):
        payload = bytes(bytes_or_value)
    else:
        payload = canonical_json_bytes(bytes_or_value, schema=schema)
    return hashlib.sha256(payload).hexdigest()


def strict_load_canonical_json(
    bytes_or_path: bytes | bytearray | memoryview | str | os.PathLike[str],
    *,
    schema: str | SchemaSpec,
) -> dict[str, Any]:
    if isinstance(bytes_or_path, (bytes, bytearray, memoryview)):
        payload = bytes(bytes_or_path)
    else:
        path = Path(bytes_or_path)
        if path.is_absolute():
            parts = path.parts[1:]
            root = Path(path.anchor)
        else:
            parts = path.parts
            root = Path.cwd()
        if not parts or any(part in {"", ".", ".."} for part in parts):
            raise EvidenceValidationError("canonical JSON path must be normalized")
        payload, _ = _read_no_follow(root, PurePosixPath(*parts).as_posix())
    if payload.startswith(b"\xef\xbb\xbf"):
        raise EvidenceValidationError("UTF-8 BOM is forbidden")
    try:
        text = payload.decode("utf-8", "strict")
        loaded = json.loads(text, object_pairs_hook=_pairs_no_duplicates, parse_float=lambda raw: (_ for _ in ()).throw(EvidenceValidationError(f"float forbidden: {raw}")), parse_constant=lambda raw: (_ for _ in ()).throw(EvidenceValidationError(f"nonfinite forbidden: {raw}")))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError("invalid strict UTF-8 JSON") from exc
    canonical = canonical_json_bytes(loaded, schema=schema)
    if canonical != payload:
        raise EvidenceValidationError("record bytes are not canonical")
    return loaded


@dataclass
class RunBundle:
    artifact_root: Path
    root: Path
    run_id: str
    _lock: threading.RLock = field(default_factory=threading.RLock, repr=False)
    _sealed: bool = field(default=False, repr=False)


@dataclass(frozen=True)
class ExecutionAllocation:
    request_digest: str
    attempt_id: str
    execution_id: str
    logical_root: str
    request_ref: str


def _open_directory(path: Path) -> int:
    try:
        return os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as exc:
        raise EvidenceValidationError(f"unsafe or unavailable directory: {path}") from exc


def _ensure_directory(path: Path, *, mode: int = 0o700) -> None:
    if path.exists() or path.is_symlink():
        if path.is_symlink() or not path.is_dir():
            raise EvidenceValidationError(f"directory path is symlink or special: {path}")
        return
    path.mkdir(mode=mode, parents=True, exist_ok=False)
    fd = _open_directory(path)
    os.close(fd)


def _open_parent_dir(root: Path, logical_path: str, *, create: bool) -> tuple[int, str]:
    logical = validate_logical_path(logical_path)
    parts = logical.split("/")
    fd = _open_directory(root)
    try:
        for part in parts[:-1]:
            try:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            except FileNotFoundError:
                if not create:
                    raise
                os.mkdir(part, mode=0o700, dir_fd=fd)
                os.fsync(fd)
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd, parts[-1]
    except Exception:
        os.close(fd)
        raise


def _write_no_replace(root: Path, logical_path: str, data: bytes, *, mode: int = 0o600) -> dict[str, Any]:
    parent_fd, name = _open_parent_dir(root, logical_path, create=True)
    temporary_name = f".{name}.tmp-{secrets.token_hex(16)}"
    temporary_created = False
    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
        try:
            fd = os.open(temporary_name, flags, mode, dir_fd=parent_fd)
        except FileExistsError as exc:
            raise EvidenceConflictError(f"temporary publication collision: {logical_path}") from exc
        temporary_created = True
        try:
            view = memoryview(data)
            while view:
                written = os.write(fd, view)
                if written <= 0:
                    raise EvidenceValidationError("sealed artifact write made no progress")
                view = view[written:]
            os.fsync(fd)
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
                raise EvidenceValidationError("temporary artifact is not an exclusive regular file")
        finally:
            os.close(fd)
        try:
            os.link(
                temporary_name,
                name,
                src_dir_fd=parent_fd,
                dst_dir_fd=parent_fd,
                follow_symlinks=False,
            )
        except FileExistsError as exc:
            raise EvidenceConflictError(f"sealed destination already exists: {logical_path}") from exc
        os.fsync(parent_fd)
        os.unlink(temporary_name, dir_fd=parent_fd)
        temporary_created = False
        os.fsync(parent_fd)
        final_info = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if not stat.S_ISREG(final_info.st_mode) or final_info.st_nlink != 1:
            raise EvidenceValidationError("published artifact is not an exclusive regular file")
    finally:
        if temporary_created:
            try:
                os.unlink(temporary_name, dir_fd=parent_fd)
                os.fsync(parent_fd)
            except FileNotFoundError:
                pass
        os.close(parent_fd)
    return {"sha256": content_digest(data), "byte_count": len(data)}


def _read_no_follow(root: Path, logical_path: str) -> tuple[bytes, os.stat_result]:
    parent_fd, name = _open_parent_dir(root, logical_path, create=False)
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
        try:
            info = os.fstat(fd)
            if not stat.S_ISREG(info.st_mode):
                raise EvidenceValidationError(f"artifact is not regular: {logical_path}")
            chunks: list[bytes] = []
            while True:
                chunk = os.read(fd, 1024 * 1024)
                if not chunk:
                    break
                chunks.append(chunk)
            return b"".join(chunks), info
        finally:
            os.close(fd)
    finally:
        os.close(parent_fd)


def atomic_write_bytes_no_replace(
    root: str | os.PathLike[str],
    logical_path: str,
    data: bytes | bytearray | memoryview | str,
    *,
    mode: int = 0o600,
) -> dict[str, Any]:
    payload = data.encode("utf-8") if isinstance(data, str) else bytes(data)
    result = _write_no_replace(Path(root), logical_path, payload, mode=mode)
    return {"logical_ref": logical_path, **result}


def read_bytes_no_follow(
    root: str | os.PathLike[str], logical_path: str
) -> tuple[bytes, os.stat_result]:
    return _read_no_follow(Path(root), logical_path)


def _payload_file_refs(root: Path) -> list[str]:
    refs: list[str] = []

    def visit(directory_fd: int, prefix: str) -> None:
        for name in sorted(os.listdir(directory_fd), key=lambda item: item.encode("utf-8")):
            info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            ref = f"{prefix}/{name}" if prefix else name
            if stat.S_ISLNK(info.st_mode):
                raise EvidenceValidationError(f"symlink found while inventorying bundle: {ref}")
            if stat.S_ISDIR(info.st_mode):
                child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=directory_fd)
                try:
                    visit(child, ref)
                finally:
                    os.close(child)
            elif stat.S_ISREG(info.st_mode):
                if ref != "bundle-index.json" and not ref.startswith(("phase-results/", "review-governance/")):
                    refs.append(ref)
            else:
                raise EvidenceValidationError(f"special file found while inventorying bundle: {ref}")

    root_fd = _open_directory(root)
    try:
        visit(root_fd, "")
    finally:
        os.close(root_fd)
    return refs


def atomic_write_canonical_record(
    root_or_bundle: str | os.PathLike[str] | RunBundle,
    logical_path: str,
    value: Any,
    *,
    schema: str | SchemaSpec,
) -> dict[str, Any]:
    root = root_or_bundle.root if isinstance(root_or_bundle, RunBundle) else Path(root_or_bundle)
    payload = canonical_json_bytes(value, schema=schema)
    if isinstance(root_or_bundle, RunBundle):
        with root_or_bundle._lock:
            if root_or_bundle._sealed:
                raise EvidenceConflictError("payload bundle is already sealed")
            result = _write_no_replace(root, logical_path, payload)
    else:
        result = _write_no_replace(root, logical_path, payload)
    result.update({"logical_ref": logical_path, "media_type": "application/json", "role": "canonical_record"})
    return result


def create_run_bundle(artifact_root: str | os.PathLike[str], *, run_id: str | None = None) -> RunBundle:
    parent = Path(artifact_root)
    _ensure_directory(parent)
    chosen = run_id or f"run_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{secrets.token_hex(16)}"
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", chosen):
        raise EvidenceValidationError("run_id has an invalid format")
    root = parent / chosen
    try:
        root.mkdir(mode=0o700)
    except FileExistsError as exc:
        raise EvidenceConflictError(f"run bundle already exists: {chosen}") from exc
    fd = _open_directory(root)
    os.fsync(fd)
    os.close(fd)
    return RunBundle(parent, root, chosen)


def build_evidence_request(**fields: Any) -> dict[str, Any]:
    record = {"schema_version": "1.0", **fields}
    canonical_json_bytes(record, schema="evidence_request@1")
    return _normalize_json(record)


def validate_evidence_request(record: Any) -> dict[str, Any]:
    normalized = _normalize_json(record)
    return validate_schema(normalized, schema="evidence_request@1")


def allocate_execution(bundle: RunBundle, request: dict[str, Any]) -> ExecutionAllocation:
    validated = validate_evidence_request(request)
    request_digest = content_digest(validated, schema="evidence_request@1")
    attempt_id = f"att_{request_digest}"
    with bundle._lock:
        if bundle._sealed:
            raise EvidenceConflictError("payload bundle is already sealed")
        for _ in range(32):
            execution_id = f"exe_{secrets.token_hex(16)}"
            logical_root = f"attempts/{attempt_id}/executions/{execution_id}"
            try:
                _write_no_replace(bundle.root, f"{logical_root}/request.json", canonical_json_bytes(validated, schema="evidence_request@1"))
                return ExecutionAllocation(request_digest, attempt_id, execution_id, logical_root, f"{logical_root}/request.json")
            except EvidenceConflictError:
                continue
    raise EvidenceConflictError("could not allocate a unique execution id")


def atomic_write_artifact(
    bundle: RunBundle,
    logical_path: str,
    data: bytes | bytearray | memoryview | str,
    *,
    media_type: str = "application/octet-stream",
    role: str = "result_artifact",
) -> dict[str, Any]:
    payload = data.encode("utf-8") if isinstance(data, str) else bytes(data)
    with bundle._lock:
        if bundle._sealed:
            raise EvidenceConflictError("payload bundle is already sealed")
        result = _write_no_replace(bundle.root, logical_path, payload)
    return {"logical_ref": logical_path, "media_type": media_type, **result, "role": role}


def build_evidence_manifest(**fields: Any) -> dict[str, Any]:
    record = {"schema_version": "1.0", **fields}
    without = dict(record)
    without.pop("evidence_manifest_digest", None)
    record["evidence_manifest_digest"] = content_digest(without)
    canonical_json_bytes(record, schema="evidence_manifest@1")
    return _normalize_json(record)


def validate_evidence_manifest(record: Any) -> dict[str, Any]:
    normalized = _normalize_json(record)
    return validate_schema(normalized, schema="evidence_manifest@1")


def seal_attempt_manifest(
    bundle: RunBundle,
    request: dict[str, Any],
    execution: ExecutionAllocation,
    result_artifacts: Sequence[dict[str, Any]],
    *,
    execution_record: dict[str, Any],
    result_record: dict[str, Any],
    interpretation: dict[str, Any],
) -> dict[str, Any]:
    with bundle._lock:
        if bundle._sealed:
            raise EvidenceConflictError("payload bundle is already sealed")
        request_bytes, _ = _read_no_follow(bundle.root, execution.request_ref)
        request_artifact = {
            "logical_ref": execution.request_ref,
            "media_type": "application/json",
            "sha256": content_digest(request_bytes),
            "byte_count": len(request_bytes),
            "role": "request",
        }
        inventory = [request_artifact, *[dict(item) for item in result_artifacts]]
        manifest = build_evidence_manifest(
            request=request,
            request_digest=execution.request_digest,
            attempt_id=execution.attempt_id,
            execution_id=execution.execution_id,
            run_id=bundle.run_id,
            execution=execution_record,
            result=result_record,
            integrity={
                "request_artifact": request_artifact,
                "artifact_inventory": inventory,
                "atomic_write_state": "manifest_published_last_no_overwrite",
                "integrity_state": "sealed_pending_reader_verification",
            },
            interpretation=interpretation,
        )
        manifest_ref = f"{execution.logical_root}/manifest.json"
        atomic_write_canonical_record(bundle, manifest_ref, manifest, schema="evidence_manifest@1")
    return {"manifest_ref": manifest_ref, "manifest": manifest}


def verify_attempt_manifest(artifact_root: str | os.PathLike[str], manifest_ref: str) -> dict[str, Any]:
    root = Path(artifact_root)
    payload, _ = _read_no_follow(root, manifest_ref)
    manifest = strict_load_canonical_json(payload, schema="evidence_manifest@1")
    for entry in manifest["integrity"]["artifact_inventory"]:
        data, _ = _read_no_follow(root, entry["logical_ref"])
        if len(data) != entry["byte_count"] or content_digest(data) != entry["sha256"]:
            raise EvidenceValidationError(f"artifact digest/count mismatch: {entry['logical_ref']}")
    return {
        "schema_version": "1.0",
        "integrity_state": "verified",
        "manifest_ref": manifest_ref,
        "manifest_sha256": content_digest(payload),
        "manifest": manifest,
    }


def seal_bundle_index(bundle: RunBundle) -> dict[str, Any]:
    with bundle._lock:
        if bundle._sealed:
            raise EvidenceConflictError("payload bundle is already sealed")
        artifacts: list[dict[str, Any]] = []
        for ref in _payload_file_refs(bundle.root):
            data, _ = _read_no_follow(bundle.root, ref)
            artifacts.append(
                {
                    "logical_ref": ref,
                    "media_type": "application/json" if ref.endswith(".json") else "application/octet-stream",
                    "sha256": content_digest(data),
                    "byte_count": len(data),
                    "role": "payload",
                }
            )
        record = {
            "schema_version": "1.0",
            "index_kind": "payload_bundle_index",
            "exclusions": ["bundle-index.json", "phase-results/", "review-governance/"],
            "artifacts": artifacts,
        }
        semantic = content_digest(record, schema="payload_bundle_index@1")
        written = atomic_write_canonical_record(bundle.root, "bundle-index.json", record, schema="payload_bundle_index@1")
        bundle._sealed = True
    return {"bundle_index_ref": "bundle-index.json", "payload_bundle_index_digest": semantic, "payload_bundle_index_file_sha256": written["sha256"], "record": record}


def verify_bundle_index(artifact_root: str | os.PathLike[str], index_ref: str = "bundle-index.json") -> dict[str, Any]:
    root = Path(artifact_root)
    payload, _ = _read_no_follow(root, index_ref)
    record = strict_load_canonical_json(payload, schema="payload_bundle_index@1")
    disk_refs = _payload_file_refs(root)
    indexed_refs = [entry["logical_ref"] for entry in record["artifacts"]]
    if disk_refs != indexed_refs:
        raise EvidenceValidationError("payload bundle disk set does not exactly match bundle index")
    for entry in record["artifacts"]:
        data, _ = _read_no_follow(root, entry["logical_ref"])
        if len(data) != entry["byte_count"] or content_digest(data) != entry["sha256"]:
            raise EvidenceValidationError(f"bundle artifact digest/count mismatch: {entry['logical_ref']}")
    return {
        "bundle_index_ref": index_ref,
        "payload_bundle_index_digest": content_digest(record, schema="payload_bundle_index@1"),
        "payload_bundle_index_file_sha256": content_digest(payload),
        "disk_verification_state": "verified",
        "record": record,
    }


def verify_bootstrap_close(close_bytes: bytes, expected_bindings: Mapping[str, str]) -> dict[str, str]:
    try:
        text = close_bytes.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("bootstrap close must be ASCII") from exc
    if not text.endswith("\n") or "\r" in text:
        raise EvidenceValidationError("bootstrap close must use LF and end in LF")
    lines = text.splitlines()
    if len(lines) != 15 or lines[0] != "MATHDEVMCP_P01_BOOTSTRAP_CLOSE_V1" or lines[-1] != "END":
        raise EvidenceValidationError("bootstrap close line count/header/footer mismatch")
    names = (
        "bootstrap_attempt",
        "status",
        "entry_implementation_manifest_sha256",
        "entry_protected_manifest_sha256",
        "prior_result_round_close_ref",
        "prior_result_round_close_sha256",
        "implementation_exit_manifest_sha256",
        "bootstrap_command_ledger_sha256",
        "bootstrap_log_sha256",
        "bootstrap_log_byte_count",
        "bootstrap_exit_code",
        "bootstrap_result_note_ref",
        "bootstrap_result_note_sha256",
    )
    parsed: dict[str, str] = {}
    for line, name in zip(lines[1:-1], names, strict=True):
        prefix = f"{name}="
        if not line.startswith(prefix):
            raise EvidenceValidationError(f"bootstrap close expected {name}")
        parsed[name] = line[len(prefix) :]
    if not ATTEMPT_RE.fullmatch(parsed["bootstrap_attempt"]) or parsed["status"] != "PASS" or parsed["bootstrap_exit_code"] != "0":
        raise EvidenceValidationError("bootstrap close status/attempt/exit is invalid")
    for name in (
        "entry_implementation_manifest_sha256",
        "entry_protected_manifest_sha256",
        "implementation_exit_manifest_sha256",
        "bootstrap_command_ledger_sha256",
        "bootstrap_log_sha256",
        "bootstrap_result_note_sha256",
    ):
        _require_digest(parsed[name], name)
    if parsed["prior_result_round_close_sha256"] != "NONE":
        _require_digest(parsed["prior_result_round_close_sha256"], "prior_result_round_close_sha256")
    _require_int(int(parsed["bootstrap_log_byte_count"]), "bootstrap_log_byte_count")
    expected_ref = f"docs/plans/mathdevmcp-real-document-remediation-phase-01-bootstrap-{parsed['bootstrap_attempt']}-result-2026-07-11.md"
    if parsed["bootstrap_result_note_ref"] != expected_ref:
        raise EvidenceValidationError("bootstrap result-note ref/attempt mismatch")
    for key, expected in expected_bindings.items():
        if parsed.get(key) != expected:
            raise EvidenceValidationError(f"bootstrap binding mismatch for {key}")
    return parsed


def _verify_text_bindings(
    record_bytes: bytes,
    *,
    labels: Mapping[str, str],
    expected_bindings: Mapping[str, str],
) -> dict[str, str]:
    if len(record_bytes) > 65536 or record_bytes.startswith(b"\xef\xbb\xbf") or b"\x00" in record_bytes or b"\r" in record_bytes:
        raise EvidenceValidationError("review/audit bytes violate size or encoding boundary")
    try:
        text = record_bytes.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("review/audit must be strict UTF-8") from exc
    lines = text.splitlines()
    result: dict[str, str] = {}
    for key, label in labels.items():
        pattern = re.compile(rf"^{re.escape(label)}: `([^`]+)`$")
        matches = [match.group(1) for line in lines if (match := pattern.fullmatch(line))]
        occurrences = sum(label in line for line in lines)
        if len(matches) != 1 or occurrences != 1:
            raise EvidenceValidationError(f"reserved label {label!r} must occur exactly once as a full line")
        result[key] = matches[0]
        if result[key] != expected_bindings[key]:
            raise EvidenceValidationError(f"review/audit binding mismatch for {key}")
    verdicts = [line for line in lines if line.startswith("VERDICT:")]
    if len(verdicts) != 1 or verdicts[0] not in {"VERDICT: AGREE", "VERDICT: REVISE"}:
        raise EvidenceValidationError("review/audit must contain one valid verdict")
    if next((line for line in reversed(lines) if line.strip()), None) != verdicts[0]:
        raise EvidenceValidationError("review/audit verdict must be the final nonempty line")
    result["verdict"] = verdicts[0].split(": ", 1)[1]
    return result


def verify_result_review_bindings(review_bytes: bytes, expected_bindings: Mapping[str, str]) -> dict[str, str]:
    return _verify_text_bindings(
        review_bytes,
        labels={
            "result_round": "Reviewed result round",
            "candidate_sha256": "Reviewed candidate SHA-256",
            "run_manifest_sha256": "Reviewed run manifest SHA-256",
            "result_sha256": "Reviewed result SHA-256",
            "payload_bundle_index_digest": "Reviewed payload bundle-index digest",
            "payload_bundle_index_file_sha256": "Reviewed payload bundle-index file SHA-256",
            "receipt_index_sha256": "Reviewed governance receipt-index SHA-256",
        },
        expected_bindings=expected_bindings,
    )


def verify_final_seal_audit_bindings(audit_bytes: bytes, expected_bindings: Mapping[str, str]) -> dict[str, str]:
    return _verify_text_bindings(
        audit_bytes,
        labels={
            "result_round": "Audited result round",
            "final_candidate_sha256": "Audited final-decision candidate SHA-256",
            "candidate_sha256": "Audited candidate SHA-256",
            "result_review_sha256": "Audited result-review SHA-256",
            "validation_log_sha256": "Audited final-candidate validation-log SHA-256",
            "receipt_index_sha256": "Audited governance receipt-index SHA-256",
        },
        expected_bindings=expected_bindings,
    )


def verify_receipt_index(
    artifact_root: str | os.PathLike[str],
    index_ref: str,
) -> dict[str, Any]:
    """Reopen an immutable receipt index and its complete measured chain."""
    root = Path(artifact_root)
    index_bytes, _ = _read_no_follow(root, index_ref)
    index = strict_load_canonical_json(index_bytes, schema="p01_receipt_index@1")
    verified_receipts: list[dict[str, Any]] = []
    prior_digest: str | None = None
    seen_checks: set[str] = set()
    index_path = PurePosixPath(index_ref)
    if index_path.parent.name != "receipts" or index_path.parent.parent.name != index["result_round"]:
        raise EvidenceValidationError("receipt index path does not identify its result-round root")
    round_prefix = f"{index_path.parent.parent.as_posix()}/"
    for entry in index["receipts"]:
        if not entry["receipt_ref"].startswith(f"{round_prefix}receipts/"):
            raise EvidenceValidationError("receipt-index entry is not round-local")
        receipt_bytes, _ = _read_no_follow(root, entry["receipt_ref"])
        receipt_digest = content_digest(receipt_bytes)
        if receipt_digest != entry["receipt_sha256"]:
            raise EvidenceValidationError("receipt-index entry digest mismatch")
        receipt = strict_load_canonical_json(receipt_bytes, schema="p01_command_receipt@1")
        if (
            receipt["result_round"] != index["result_round"]
            or receipt["sequence"] != entry["sequence"]
            or receipt["check_id"] != entry["check_id"]
            or receipt["prior_receipt_sha256"] != prior_digest
        ):
            raise EvidenceValidationError("receipt-index entry metadata or prior link mismatch")
        if receipt["check_id"] in seen_checks:
            raise EvidenceValidationError("receipt chain repeats an action id")
        seen_checks.add(receipt["check_id"])
        for stem in ("stdout", "stderr"):
            if not receipt[f"{stem}_ref"].startswith(round_prefix):
                raise EvidenceValidationError(f"receipt {stem} ref is not round-local")
            stream, _ = _read_no_follow(root, receipt[f"{stem}_ref"])
            if (
                len(stream) != receipt[f"{stem}_byte_count"]
                or content_digest(stream) != receipt[f"{stem}_sha256"]
            ):
                raise EvidenceValidationError(f"receipt {stem} digest/count mismatch")
        verified_receipts.append(
            {
                "entry": entry,
                "record": receipt,
                "receipt_sha256": receipt_digest,
            }
        )
        prior_digest = receipt_digest
    return {
        "index_ref": index_ref,
        "index_sha256": content_digest(index_bytes),
        "record": index,
        "receipts": verified_receipts,
    }


def _require_receipt_snapshot(
    root: Path,
    terminal: dict[str, Any],
    *,
    index_ref: str,
    index_sha256: str,
    head_check_id: str,
) -> dict[str, Any]:
    snapshot = verify_receipt_index(root, index_ref)
    if snapshot["index_sha256"] != index_sha256:
        raise EvidenceValidationError("bound receipt-index digest mismatch")
    terminal_entries = terminal["record"]["receipts"]
    snapshot_entries = snapshot["record"]["receipts"]
    if terminal_entries[: len(snapshot_entries)] != snapshot_entries:
        raise EvidenceValidationError("bound receipt index is not an exact terminal-chain prefix")
    if snapshot["receipts"][-1]["record"]["check_id"] != head_check_id:
        raise EvidenceValidationError(f"bound receipt index must end in {head_check_id}")
    return snapshot


def _only_receipt(terminal: dict[str, Any], check_id: str) -> dict[str, Any]:
    matches = [item["record"] for item in terminal["receipts"] if item["record"]["check_id"] == check_id]
    if len(matches) != 1:
        raise EvidenceValidationError(f"terminal receipt chain must contain exactly one {check_id}")
    receipt = matches[0]
    if receipt["exit_code"] != 0:
        raise EvidenceValidationError(f"receipt {check_id} must have exit code zero")
    return receipt


def _require_bindings(bindings: Mapping[str, Any], expected: Mapping[str, Any], where: str) -> None:
    mismatched = sorted(key for key, value in expected.items() if bindings.get(key) != value)
    if mismatched:
        raise EvidenceValidationError(f"{where} bindings mismatch: {mismatched}")


def _p01_round_ref_from_index(index_ref: str) -> str:
    path = PurePosixPath(index_ref)
    if path.parent.name != "receipts" or not ROUND_RE.fullmatch(path.parent.parent.name):
        raise EvidenceValidationError("P01 receipt index is not below a result round")
    return path.parent.parent.as_posix()


def _p01_receipt_map(chain: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    receipts = {item["record"]["check_id"]: item["record"] for item in chain["receipts"]}
    if len(receipts) != len(chain["receipts"]):
        raise EvidenceValidationError("P01 receipt map contains repeated actions")
    return receipts


def _p01_artifact_entry(
    root: Path,
    ref: str,
    role: str,
    *,
    media_type: str = "text/plain",
) -> dict[str, Any]:
    data, _ = _read_no_follow(root, ref)
    return {
        "logical_ref": ref,
        "media_type": media_type,
        "sha256": content_digest(data),
        "byte_count": len(data),
        "role": role,
    }


def _p01_require_action_prefix(chain: Mapping[str, Any], expected_actions: Sequence[str]) -> None:
    actual = [item["record"]["check_id"] for item in chain["receipts"]]
    if actual != list(expected_actions):
        raise EvidenceValidationError(f"P01 action prefix mismatch: {actual}")
    if any(item["record"]["exit_code"] != 0 for item in chain["receipts"]):
        raise EvidenceValidationError("P01 reconstruction requires zero-exit receipts")


def _p01_verify_receipt_commands(chain: Mapping[str, Any], round_ref: str) -> None:
    receipts = _p01_receipt_map(chain)
    init = receipts["init_round"]
    init_bindings = init["bindings"]
    expected_init = [
        "env",
        "PYTHONPATH=src",
        P01_PYTHON,
        "scripts/p01_governance.py",
        "init-round",
        "--round",
        init["result_round"],
        "--entry-root",
        P01_ENTRY_ROOT_REF,
        "--bootstrap-close",
        init_bindings["bootstrap_close_ref"],
        "--bootstrap-shell-verification",
        init_bindings["bootstrap_shell_verification_ref"],
        "--round-root",
        round_ref,
        "--prior-round-close",
        init_bindings["prior_round_close_ref"] or "NONE",
        "--prior-terminal-receipt-index",
        init_bindings["prior_terminal_receipt_index_ref"] or "NONE",
    ]
    if init["command_argv"] != expected_init:
        raise EvidenceValidationError("init_round receipt argv does not match the fixed command")
    for action, receipt in receipts.items():
        if action == "init_round":
            continue
        expected = p01_fixed_action_argv(round_ref, action)
        if expected is None:
            artifact_ref = None
            if action == "result_review_binding":
                artifact_ref = receipt["bindings"]["review_ref"]
            elif action == "final_seal_audit_binding":
                artifact_ref = receipt["bindings"]["audit_ref"]
            expected = p01_governance_action_argv(round_ref, action, artifact_ref=artifact_ref)
        if receipt["command_argv"] != expected:
            raise EvidenceValidationError(f"{action} receipt argv does not match the fixed command")


def _p01_parse_manifest(data: bytes) -> dict[str, str]:
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("implementation manifest is not strict UTF-8") from exc
    parsed: dict[str, str] = {}
    for line in text.splitlines():
        digest, separator, ref = line.partition("  ")
        if separator != "  " or not SHA256_RE.fullmatch(digest) or not ref or ref in parsed:
            raise EvidenceValidationError("implementation manifest has invalid sha256sum grammar")
        validate_logical_path(ref, name="implementation manifest ref")
        parsed[ref] = digest
    return parsed


def _p01_implementation_delta_digest(root: Path, exit_manifest_ref: str) -> str:
    entry_bytes, _ = _read_no_follow(root, f"{P01_ENTRY_ROOT_REF}/implementation-entry-sha256.txt")
    exit_bytes, _ = _read_no_follow(root, exit_manifest_ref)
    before = _p01_parse_manifest(entry_bytes)
    after = _p01_parse_manifest(exit_bytes)
    changed = [
        {"logical_ref": ref, "entry_sha256": before.get(ref), "exit_sha256": after.get(ref)}
        for ref in sorted(set(before) | set(after), key=lambda item: item.encode("utf-8"))
        if before.get(ref) != after.get(ref)
    ]
    return content_digest(changed)


def _p01_entry_protected_digest(root: Path) -> str:
    data, _ = _read_no_follow(root, f"{P01_ENTRY_ROOT_REF}/protected-dirty-sha256.txt")
    lines = data.splitlines(keepends=True)
    if len(lines) < 11:
        raise EvidenceValidationError("entry protected manifest has fewer than the frozen 11 records")
    return content_digest(b"".join(lines[:11]))


def _p01_verify_bootstrap_predecessor(
    root: Path,
    *,
    result_round: str,
    init_bindings: Mapping[str, Any],
) -> None:
    entry_bytes, _ = _read_no_follow(root, f"{P01_ENTRY_ROOT_REF}/implementation-entry-sha256.txt")
    entry_implementation_sha256 = content_digest(entry_bytes)
    entry_protected_sha256 = _p01_entry_protected_digest(root)
    if (
        init_bindings["entry_implementation_manifest_sha256"] != entry_implementation_sha256
        or init_bindings["entry_protected_manifest_sha256"] != entry_protected_sha256
    ):
        raise EvidenceValidationError("init_round entry aggregates do not recompute")

    bootstrap_bytes, _ = _read_no_follow(root, init_bindings["bootstrap_close_ref"])
    shell_bytes, _ = _read_no_follow(root, init_bindings["bootstrap_shell_verification_ref"])
    if (
        content_digest(bootstrap_bytes) != init_bindings["bootstrap_close_sha256"]
        or content_digest(shell_bytes) != init_bindings["bootstrap_shell_verification_sha256"]
    ):
        raise EvidenceValidationError("bootstrap close or shell-verification digest changed")
    bootstrap = verify_bootstrap_close(
        bootstrap_bytes,
        {
            "entry_implementation_manifest_sha256": entry_implementation_sha256,
            "entry_protected_manifest_sha256": entry_protected_sha256,
            "implementation_exit_manifest_sha256": init_bindings["implementation_exit_manifest_sha256"],
        },
    )
    try:
        shell_text = shell_bytes.decode("ascii", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("bootstrap shell verification must be ASCII") from exc
    shell_lines = shell_text.splitlines()
    shell_names = (
        "bootstrap_close_ref",
        "bootstrap_close_sha256",
        "bootstrap_command_ledger_ref",
        "bootstrap_command_ledger_sha256",
        "bootstrap_run_log_ref",
        "bootstrap_run_log_sha256",
        "bootstrap_result_note_ref",
        "bootstrap_result_note_sha256",
        "status",
    )
    if (
        not shell_text.endswith("\n")
        or "\r" in shell_text
        or len(shell_lines) != 10
        or shell_lines[0] != "MATHDEVMCP_P01_BOOTSTRAP_SHELL_VERIFICATION_V1"
    ):
        raise EvidenceValidationError("bootstrap shell verification grammar is invalid")
    shell: dict[str, str] = {}
    for line, name in zip(shell_lines[1:], shell_names, strict=True):
        prefix = f"{name}="
        if not line.startswith(prefix):
            raise EvidenceValidationError(f"bootstrap shell verification expected {name}")
        shell[name] = line[len(prefix) :]
    if (
        shell["status"] != "PASS"
        or shell["bootstrap_close_ref"] != init_bindings["bootstrap_close_ref"]
        or shell["bootstrap_close_sha256"] != init_bindings["bootstrap_close_sha256"]
        or shell["bootstrap_command_ledger_sha256"] != bootstrap["bootstrap_command_ledger_sha256"]
        or shell["bootstrap_run_log_sha256"] != bootstrap["bootstrap_log_sha256"]
        or shell["bootstrap_result_note_ref"] != bootstrap["bootstrap_result_note_ref"]
        or shell["bootstrap_result_note_sha256"] != bootstrap["bootstrap_result_note_sha256"]
    ):
        raise EvidenceValidationError("bootstrap shell verification does not bind the reopened close")
    for ref_key, digest_key in (
        ("bootstrap_command_ledger_ref", "bootstrap_command_ledger_sha256"),
        ("bootstrap_run_log_ref", "bootstrap_run_log_sha256"),
        ("bootstrap_result_note_ref", "bootstrap_result_note_sha256"),
    ):
        validate_logical_path(shell[ref_key], name=ref_key)
        artifact_bytes, _ = _read_no_follow(root, shell[ref_key])
        if content_digest(artifact_bytes) != shell[digest_key]:
            raise EvidenceValidationError(f"bootstrap artifact digest mismatch: {shell[ref_key]}")
    run_log_bytes, _ = _read_no_follow(root, shell["bootstrap_run_log_ref"])
    if len(run_log_bytes) != int(bootstrap["bootstrap_log_byte_count"]):
        raise EvidenceValidationError("bootstrap run-log byte count does not recompute")

    predecessor_keys = (
        "prior_round_close_ref",
        "prior_round_close_sha256",
        "prior_terminal_receipt_index_ref",
        "prior_terminal_receipt_index_sha256",
    )
    if result_round == "rr01":
        if any(init_bindings[key] is not None for key in predecessor_keys):
            raise EvidenceValidationError("rr01 init_round prior bindings must all be null")
        if bootstrap["prior_result_round_close_ref"] != "NONE" or bootstrap["prior_result_round_close_sha256"] != "NONE":
            raise EvidenceValidationError("rr01 bootstrap predecessor must be NONE")
        return

    if any(init_bindings[key] is None for key in predecessor_keys):
        raise EvidenceValidationError("successor init_round predecessor bindings are incomplete")
    prior_close_ref = init_bindings["prior_round_close_ref"]
    prior_index_ref = init_bindings["prior_terminal_receipt_index_ref"]
    prior_close_bytes, _ = _read_no_follow(root, prior_close_ref)
    prior_close = strict_load_canonical_json(prior_close_bytes, schema="p01_round_close@1")
    prior_index = verify_receipt_index(root, prior_index_ref)
    prior_close_sha256 = content_digest(prior_close_bytes)
    expected_prior_round = f"rr{int(result_round[2:]) - 1:02d}"
    terminal = prior_index["receipts"][-1]["record"]
    if (
        prior_close["result_round"] != expected_prior_round
        or prior_close_sha256 != init_bindings["prior_round_close_sha256"]
        or prior_index["index_sha256"] != init_bindings["prior_terminal_receipt_index_sha256"]
        or terminal["check_id"] != "close_round"
        or terminal["exit_code"] != 0
        or terminal["bindings"]["round_close_ref"] != prior_close_ref
        or terminal["bindings"]["round_close_sha256"] != prior_close_sha256
        or bootstrap["prior_result_round_close_ref"] != prior_close_ref
        or bootstrap["prior_result_round_close_sha256"] != prior_close_sha256
    ):
        raise EvidenceValidationError("successor predecessor does not reconstruct from the prior terminal close")


def _p01_load_canonical_line_json(data: bytes, *, where: str) -> dict[str, Any]:
    if not data.endswith(b"\n") or data.count(b"\n") != 1:
        raise EvidenceValidationError(f"{where} must be one canonical JSON line")
    payload = data[:-1]
    try:
        loaded = json.loads(
            payload.decode("utf-8", "strict"),
            object_pairs_hook=_pairs_no_duplicates,
            parse_float=lambda raw: (_ for _ in ()).throw(EvidenceValidationError(f"float forbidden: {raw}")),
            parse_constant=lambda raw: (_ for _ in ()).throw(EvidenceValidationError(f"nonfinite forbidden: {raw}")),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"{where} is not strict canonical JSON") from exc
    if not isinstance(loaded, dict) or canonical_json_bytes(loaded) != payload:
        raise EvidenceValidationError(f"{where} is not a canonical JSON object")
    return loaded


def _p01_environment_measurement(root: Path, chain: Mapping[str, Any]) -> dict[str, Any]:
    receipts = _p01_receipt_map(chain)
    init = receipts["init_round"]
    stdout, _ = _read_no_follow(root, init["stdout_ref"])
    measured = _p01_load_canonical_line_json(stdout, where="init_round stdout")
    keys = {
        "bootstrap",
        "implementation_exit_manifest_sha256",
        "git_commit",
        "python_executable",
        "python_implementation",
        "python_version",
        "platform_system",
        "pytest_version",
        "pythonpath",
    }
    if set(measured) != keys:
        raise EvidenceValidationError("init_round environment measurement keys mismatch")
    if (
        measured["bootstrap"] not in {f"b0{value}" for value in range(1, 6)}
        or measured["implementation_exit_manifest_sha256"]
        != init["bindings"]["implementation_exit_manifest_sha256"]
        or not GIT_COMMIT_RE.fullmatch(_require_str(measured["git_commit"], "git_commit"))
        or measured["python_executable"] != P01_PYTHON
        or measured["pythonpath"] != "src"
    ):
        raise EvidenceValidationError("init_round environment measurement does not match the fixed P01 runtime")
    for key in ("python_implementation", "python_version", "platform_system", "pytest_version"):
        token = _require_str(measured[key], key)
        if len(token) > 128 or "/" in token or "\\" in token or "=" in token:
            raise EvidenceValidationError(f"init_round environment token is unsafe: {key}")
    return measured


def reconstruct_p01_run_manifest(
    artifact_root: str | os.PathLike[str],
    receipt_index_ref: str,
) -> dict[str, Any]:
    """Reconstruct the P01 run manifest from its immutable bind-result prefix."""
    root = Path(artifact_root)
    chain = verify_receipt_index(root, receipt_index_ref)
    round_ref = _p01_round_ref_from_index(receipt_index_ref)
    expected_actions = P01_PASS_ACTION_SEQUENCE[:15]
    _p01_require_action_prefix(chain, expected_actions)
    _p01_verify_receipt_commands(chain, round_ref)
    receipts = _p01_receipt_map(chain)
    init = receipts["init_round"]["bindings"]
    result_binding = receipts["bind_result"]["bindings"]
    measured = _p01_environment_measurement(root, chain)
    _p01_verify_bootstrap_predecessor(
        root,
        result_round=chain["record"]["result_round"],
        init_bindings=init,
    )
    result_bytes, _ = _read_no_follow(root, result_binding["result_ref"])
    if content_digest(result_bytes) != result_binding["result_sha256"]:
        raise EvidenceValidationError("bound result bytes changed")
    entry_bytes, _ = _read_no_follow(root, f"{P01_ENTRY_ROOT_REF}/implementation-entry-sha256.txt")
    exit_bytes, _ = _read_no_follow(root, init["implementation_exit_manifest_ref"])
    if (
        content_digest(entry_bytes) != init["entry_implementation_manifest_sha256"]
        or content_digest(exit_bytes) != init["implementation_exit_manifest_sha256"]
    ):
        raise EvidenceValidationError("entry/exit implementation manifest binding changed")
    implementation_exit = receipts["implementation_exit"]["bindings"]
    _require_bindings(
        implementation_exit,
        {
            "manifest_ref": init["implementation_exit_manifest_ref"],
            "manifest_sha256": init["implementation_exit_manifest_sha256"],
        },
        "implementation_exit",
    )
    inventory = []
    for item in chain["receipts"]:
        receipt = item["record"]
        inventory.extend(
            [
                _p01_artifact_entry(
                    root,
                    item["entry"]["receipt_ref"],
                    f"{receipt['check_id']}_receipt",
                    media_type="application/json",
                ),
                _p01_artifact_entry(root, receipt["stdout_ref"], f"{receipt['check_id']}_stdout"),
                _p01_artifact_entry(root, receipt["stderr_ref"], f"{receipt['check_id']}_stderr"),
            ]
        )
    inventory.append(
        _p01_artifact_entry(
            root,
            receipt_index_ref,
            "pre_candidate_receipt_index",
            media_type="application/json",
        )
    )
    started = chain["receipts"][0]["record"]["started_at_utc"]
    ended = chain["receipts"][-1]["record"]["ended_at_utc"]
    wall_time_ns = sum(item["record"]["wall_time_ns"] for item in chain["receipts"])
    plan_bytes, _ = _read_no_follow(root, P01_PLAN_REF)
    record = {
        "schema_version": "p01_run_manifest@1",
        "phase": "P01",
        "result_round": chain["record"]["result_round"],
        "git_commit": measured["git_commit"],
        "implementation_entry_manifest_sha256": content_digest(entry_bytes),
        "implementation_exit_manifest_sha256": content_digest(exit_bytes),
        "implementation_diff_digest": _p01_implementation_delta_digest(root, init["implementation_exit_manifest_ref"]),
        "pre_candidate_receipt_index_ref": receipt_index_ref,
        "pre_candidate_receipt_index_sha256": chain["index_sha256"],
        "governance_receipt_family_ref": f"{round_ref}/receipts",
        "environment": {
            "python_implementation": measured["python_implementation"],
            "python_version": measured["python_version"],
            "platform_system": measured["platform_system"],
            "test_runner_version": f"pytest-{measured['pytest_version']}",
        },
        "device_execution": {"mode": "cpu_test_double", "gpu_requested": False, "gpu_initialized": False},
        "synthetic_data_version": "p01-synthetic-1",
        "random_seed_policy": {
            "pseudorandom_test_seeds": [],
            "runtime_id_source": "secrets_token_hex_128",
            "runtime_ids_recorded": True,
            "boundary": "runtime_ids_are_uniqueness_not_scientific_randomness",
        },
        "plan_ref": P01_PLAN_REF,
        "plan_sha256": content_digest(plan_bytes),
        "result_ref": result_binding["result_ref"],
        "result_sha256": result_binding["result_sha256"],
        "artifact_inventory": inventory,
        "external_tool_considerations": [
            {
                "tool": "fake_runner",
                "observed_availability_version_evidence": "embedded p01-generator-1",
                "possible_role": "synthetic identity and integrity fixture",
                "selected": True,
                "reason_not_selected": "",
                "certifying_status": "test_only_noncertifying",
                "phase_boundary": "P01 integrity only",
            },
            {
                "tool": "SymPy",
                "observed_availability_version_evidence": "1.14.0 from entry-gated environment",
                "possible_role": "synthetic P00 quarantine regression",
                "selected": False,
                "reason_not_selected": "P05 owns real adapter conformance",
                "certifying_status": "not_certifying_in_p01",
                "phase_boundary": "used only by separate P00 synthetic regression",
            },
            {
                "tool": "Sage_Lean_and_specialist_search",
                "observed_availability_version_evidence": "not invoked",
                "possible_role": "later mathematical certification or search",
                "selected": False,
                "reason_not_selected": "forbidden by P01 phase boundary",
                "certifying_status": "not_run",
                "phase_boundary": "deferred to P05 or later reviewed phase",
            },
        ],
        "started_at_utc": started,
        "ended_at_utc": ended,
        "wall_time_ns": wall_time_ns,
        "non_claims": list(P01_NON_CLAIMS),
    }
    canonical_json_bytes(record, schema="p01_run_manifest@1")
    return _normalize_json(record)


def verify_p01_run_manifest(
    artifact_root: str | os.PathLike[str],
    *,
    run_manifest_ref: str,
    bind_result_receipt_index_ref: str,
) -> dict[str, Any]:
    root = Path(artifact_root)
    run_bytes, _ = _read_no_follow(root, run_manifest_ref)
    run_manifest = strict_load_canonical_json(run_bytes, schema="p01_run_manifest@1")
    expected = reconstruct_p01_run_manifest(root, bind_result_receipt_index_ref)
    if canonical_json_bytes(run_manifest, schema="p01_run_manifest@1") != canonical_json_bytes(
        expected,
        schema="p01_run_manifest@1",
    ):
        raise EvidenceValidationError("run manifest does not equal independent reconstruction")
    return {
        "run_manifest": run_manifest,
        "run_manifest_sha256": content_digest(run_bytes),
    }


def _p01_summary_records(root: Path, round_ref: str) -> dict[str, dict[str, Any]]:
    specs = {
        "mutation": ("summaries/mutation-matrix.json", "p01_mutation_summary@1"),
        "parallel": ("summaries/serial-parallel-identity.json", "p01_parallel_summary@1"),
        "legacy": ("summaries/legacy-matrix.json", "p01_legacy_summary@1"),
        "generator": ("summaries/generator-result.json", "p01_generator_result@1"),
    }
    return {
        name: strict_load_canonical_json(root / round_ref / ref, schema=schema)
        for name, (ref, schema) in specs.items()
    }


def _p01_verify_summary_contract(summaries: Mapping[str, Mapping[str, Any]], result_round: str) -> None:
    if any(record["result_round"] != result_round for record in summaries.values()):
        raise EvidenceValidationError("P01 summary result round mismatch")
    mutation = summaries["mutation"]
    observed_mutations = [
        (case["case_id"], case["mutated_field"], case["expected_veto_id"])
        for case in mutation["cases"]
    ]
    expected_mutations = [(case_id, case_id, veto_id) for case_id, veto_id in P01_REQUIRED_MUTATION_CASES]
    if observed_mutations != expected_mutations or not mutation["all_pass"]:
        raise EvidenceValidationError("mutation summary does not contain the exact required case/veto matrix")
    for case in mutation["cases"]:
        if not case["passed"] or case["expected_veto_id"] not in case["observed_veto_ids"]:
            raise EvidenceValidationError("mutation summary has an unobserved required veto")
    parallel = summaries["parallel"]
    if len(parallel["cases"]) != 1 or parallel["cases"][0]["case_id"] != "identical_request_thread_and_run_identity" or not parallel["all_pass"]:
        raise EvidenceValidationError("parallel summary does not contain the exact required identity case")
    legacy = summaries["legacy"]
    observed_legacy = [
        (case["case_id"], case["input_schema_class"], case["expected_certification_state"])
        for case in legacy["cases"]
    ]
    if observed_legacy != list(P01_REQUIRED_LEGACY_CASES) or not legacy["all_pass"]:
        raise EvidenceValidationError("legacy summary does not contain the exact required cases")
    for case in legacy["cases"]:
        if not case["passed"] or case["observed_certification_state"] != case["expected_certification_state"]:
            raise EvidenceValidationError("legacy summary has a mismatched observed state")
    generator = summaries["generator"]
    if list(generator["invariant_ids"]) != list(P01_REQUIRED_INVARIANT_IDS) or not generator["all_pass"]:
        raise EvidenceValidationError("generator summary does not bind the exact invariant set")


def reconstruct_p01_candidate(
    artifact_root: str | os.PathLike[str],
    receipt_index_ref: str,
) -> tuple[dict[str, Any], dict[str, str]]:
    """Reconstruct a P01 candidate from its immutable build-run prefix."""
    root = Path(artifact_root)
    chain = verify_receipt_index(root, receipt_index_ref)
    round_ref = _p01_round_ref_from_index(receipt_index_ref)
    _p01_require_action_prefix(chain, P01_PASS_ACTION_SEQUENCE[:16])
    _p01_verify_receipt_commands(chain, round_ref)
    receipts = _p01_receipt_map(chain)
    build_run = receipts["build_run_manifest"]["bindings"]
    bound_run_prefix = verify_receipt_index(root, build_run["bound_receipt_index_ref"])
    if bound_run_prefix["index_sha256"] != build_run["bound_receipt_index_sha256"]:
        raise EvidenceValidationError("build_run_manifest bound receipt-index digest changed")
    verified_run = verify_p01_run_manifest(
        root,
        run_manifest_ref=build_run["run_manifest_ref"],
        bind_result_receipt_index_ref=bound_run_prefix["index_ref"],
    )
    run = verified_run["run_manifest"]
    if verified_run["run_manifest_sha256"] != build_run["run_manifest_sha256"]:
        raise EvidenceValidationError("run manifest bytes changed after construction")
    bind_result_index_ref = run["pre_candidate_receipt_index_ref"]
    bind_result_prefix = verify_receipt_index(root, bind_result_index_ref)
    if bind_result_prefix["record"]["receipts"] != chain["record"]["receipts"][:15]:
        raise EvidenceValidationError("run-manifest receipt prefix is not the exact round prefix")
    summaries = _p01_summary_records(root, round_ref)
    _p01_verify_summary_contract(summaries, chain["record"]["result_round"])
    generator = summaries["generator"]
    bundle_ref = f"{generator['bundle_ref']}/bundle-index.json"
    bundle = verify_bundle_index(root / PurePosixPath(generator["bundle_ref"]))
    if (
        bundle["payload_bundle_index_digest"] != generator["payload_bundle_index_digest"]
        or bundle["payload_bundle_index_file_sha256"] != generator["payload_bundle_index_file_sha256"]
    ):
        raise EvidenceValidationError("generator/bundle index bindings do not recompute")
    init = receipts["init_round"]["bindings"]
    result_round = chain["record"]["result_round"]
    _p01_verify_bootstrap_predecessor(root, result_round=result_round, init_bindings=init)
    prior_round = None if result_round == "rr01" else f"rr{int(result_round[2:]) - 1:02d}"
    criteria = {
        "canonical_vectors_pass": receipts["canonical"]["exit_code"] == 0,
        "artifact_store_pass": receipts["store"]["exit_code"] == 0,
        "manifest_contract_pass": receipts["canonical"]["exit_code"] == 0 and receipts["store"]["exit_code"] == 0,
        "mutation_matrix_pass": summaries["mutation"]["all_pass"],
        "parallel_identity_pass": summaries["parallel"]["all_pass"],
        "legacy_matrix_pass": summaries["legacy"]["all_pass"],
        "integrity_binding_fixture_pass": generator["all_pass"],
        "claim_eligibility_ineligible": receipts["promotion"]["exit_code"] == 0,
        "publication_quarantine_pass": receipts["p00_quarantine"]["exit_code"] == 0,
        "all_pass": False,
    }
    criteria["all_pass"] = all(value for key, value in criteria.items() if key != "all_pass")
    record = {
        "schema_version": "p01_candidate_decision@1",
        "phase": "P01",
        "result_round": result_round,
        "decision": "candidate_pass_pending_independent_result_review",
        "publication_mode": "disabled",
        "claim_eligibility": "ineligible",
        "integrity_binding_status": "verified_for_synthetic_fixture",
        "predecessor": {
            "entry_implementation_manifest_sha256": init["entry_implementation_manifest_sha256"],
            "entry_protected_manifest_sha256": init["entry_protected_manifest_sha256"],
            "bootstrap_close_ref": init["bootstrap_close_ref"],
            "bootstrap_close_sha256": init["bootstrap_close_sha256"],
            "prior_result_round": prior_round,
            "prior_round_close_ref": init["prior_round_close_ref"],
            "prior_round_close_sha256": init["prior_round_close_sha256"],
            "prior_terminal_receipt_index_ref": init["prior_terminal_receipt_index_ref"],
            "prior_terminal_receipt_index_sha256": init["prior_terminal_receipt_index_sha256"],
        },
        "run_manifest_ref": build_run["run_manifest_ref"],
        "run_manifest_sha256": build_run["run_manifest_sha256"],
        "result_ref": run["result_ref"],
        "result_sha256": run["result_sha256"],
        "pre_candidate_receipt_index_ref": receipt_index_ref,
        "pre_candidate_receipt_index_sha256": chain["index_sha256"],
        "implementation_exit_manifest_sha256": init["implementation_exit_manifest_sha256"],
        "payload_bundle_index_ref": bundle_ref,
        "payload_bundle_index_digest": bundle["payload_bundle_index_digest"],
        "payload_bundle_index_file_sha256": bundle["payload_bundle_index_file_sha256"],
        "primary_criterion": criteria,
        "vetoes": {key: False for key in P01_VETO_KEYS},
        "non_claims": list(P01_NON_CLAIMS),
    }
    canonical_json_bytes(record, schema="p01_candidate_decision@1")
    summary_digests = {}
    for name, relative in (
        ("mutation_summary_sha256", "summaries/mutation-matrix.json"),
        ("parallel_summary_sha256", "summaries/serial-parallel-identity.json"),
        ("legacy_summary_sha256", "summaries/legacy-matrix.json"),
        ("generator_summary_sha256", "summaries/generator-result.json"),
    ):
        data, _ = _read_no_follow(root, f"{round_ref}/{relative}")
        summary_digests[name] = content_digest(data)
    return _normalize_json(record), summary_digests


def verify_p01_candidate(
    artifact_root: str | os.PathLike[str],
    *,
    candidate_ref: str,
    build_run_receipt_index_ref: str,
) -> dict[str, Any]:
    root = Path(artifact_root)
    candidate_bytes, _ = _read_no_follow(root, candidate_ref)
    candidate = strict_load_canonical_json(candidate_bytes, schema="p01_candidate_decision@1")
    expected, summary_digests = reconstruct_p01_candidate(root, build_run_receipt_index_ref)
    if canonical_json_bytes(candidate, schema="p01_candidate_decision@1") != canonical_json_bytes(expected, schema="p01_candidate_decision@1"):
        raise EvidenceValidationError("candidate does not equal independent reconstruction")
    report = {
        "candidate_sha256": content_digest(candidate_bytes),
        "run_manifest_sha256": candidate["run_manifest_sha256"],
        "build_run_receipt_index_sha256": candidate["pre_candidate_receipt_index_sha256"],
        "implementation_diff_digest": strict_load_canonical_json(
            root / candidate["run_manifest_ref"], schema="p01_run_manifest@1"
        )["implementation_diff_digest"],
        "python_executable": P01_PYTHON,
        "pythonpath": "src",
        **summary_digests,
        "payload_bundle_index_digest": candidate["payload_bundle_index_digest"],
        "payload_bundle_index_file_sha256": candidate["payload_bundle_index_file_sha256"],
        "status": "PASS",
    }
    return {
        "candidate": candidate,
        "candidate_sha256": content_digest(candidate_bytes),
        "report": report,
        "report_bytes": canonical_json_bytes(report) + b"\n",
    }


def reconstruct_p01_final_decision(
    artifact_root: str | os.PathLike[str],
    result_review_receipt_index_ref: str,
) -> dict[str, Any]:
    """Reconstruct the final P01 record from the exact agreeing-review head."""
    root = Path(artifact_root)
    chain = verify_receipt_index(root, result_review_receipt_index_ref)
    round_ref = _p01_round_ref_from_index(result_review_receipt_index_ref)
    _p01_require_action_prefix(chain, P01_PASS_ACTION_SEQUENCE[:19])
    _p01_verify_receipt_commands(chain, round_ref)
    receipts = _p01_receipt_map(chain)
    result_round = chain["record"]["result_round"]
    candidate_gate = receipts["candidate_gate"]
    review_binding = receipts["result_review_binding"]
    if chain["receipts"][-1]["record"] != review_binding:
        raise EvidenceValidationError("final reconstruction requires result_review_binding at the exact head")

    reviewed_prefix = _require_receipt_snapshot(
        root,
        chain,
        index_ref=review_binding["bindings"]["reviewed_receipt_index_ref"],
        index_sha256=review_binding["bindings"]["reviewed_receipt_index_sha256"],
        head_check_id="candidate_gate",
    )
    candidate_gate_prefix = _require_receipt_snapshot(
        root,
        chain,
        index_ref=candidate_gate["bindings"]["validated_receipt_index_ref"],
        index_sha256=candidate_gate["bindings"]["validated_receipt_index_sha256"],
        head_check_id="build_candidate",
    )
    candidate_ref = f"{round_ref}/P01-candidate-decision.json"
    candidate_bytes, _ = _read_no_follow(root, candidate_ref)
    candidate = strict_load_canonical_json(candidate_bytes, schema="p01_candidate_decision@1")
    candidate_sha256 = content_digest(candidate_bytes)
    if candidate["result_round"] != result_round:
        raise EvidenceValidationError("final reconstruction candidate round mismatch")
    verified_candidate = verify_p01_candidate(
        root,
        candidate_ref=candidate_ref,
        build_run_receipt_index_ref=candidate["pre_candidate_receipt_index_ref"],
    )
    candidate_validation_ref = f"{round_ref}/logs/candidate-validation.log"
    candidate_validation_bytes, _ = _read_no_follow(root, candidate_validation_ref)
    candidate_gate_stdout, _ = _read_no_follow(root, candidate_gate["stdout_ref"])
    if (
        candidate_validation_bytes != verified_candidate["report_bytes"]
        or candidate_gate_stdout != verified_candidate["report_bytes"]
    ):
        raise EvidenceValidationError("candidate validation report does not equal independent reconstruction")
    _require_bindings(
        candidate_gate["bindings"],
        {
            "run_manifest_ref": candidate["run_manifest_ref"],
            "run_manifest_sha256": candidate["run_manifest_sha256"],
            "candidate_ref": candidate_ref,
            "candidate_sha256": candidate_sha256,
            "validated_receipt_index_ref": candidate_gate_prefix["index_ref"],
            "validated_receipt_index_sha256": candidate_gate_prefix["index_sha256"],
            "payload_bundle_index_ref": candidate["payload_bundle_index_ref"],
            "payload_bundle_index_digest": candidate["payload_bundle_index_digest"],
            "payload_bundle_index_file_sha256": candidate["payload_bundle_index_file_sha256"],
        },
        "candidate_gate",
    )

    expected_review_ref = (
        "docs/reviews/mathdevmcp-real-document-remediation-phase-01-"
        f"result-review-{result_round}-result-2026-07-11.md"
    )
    review_ref = review_binding["bindings"]["review_ref"]
    if review_ref != expected_review_ref:
        raise EvidenceValidationError("result-review binding is not the exact round-specific path")
    review_bytes, _ = _read_no_follow(root, review_ref)
    review_sha256 = content_digest(review_bytes)
    _require_bindings(
        review_binding["bindings"],
        {
            "review_ref": review_ref,
            "review_sha256": review_sha256,
            "candidate_ref": candidate_ref,
            "candidate_sha256": candidate_sha256,
            "reviewed_receipt_index_ref": reviewed_prefix["index_ref"],
            "reviewed_receipt_index_sha256": reviewed_prefix["index_sha256"],
        },
        "result_review_binding",
    )
    review_result = verify_result_review_bindings(
        review_bytes,
        {
            "result_round": result_round,
            "candidate_sha256": candidate_sha256,
            "run_manifest_sha256": candidate["run_manifest_sha256"],
            "result_sha256": candidate["result_sha256"],
            "payload_bundle_index_digest": candidate["payload_bundle_index_digest"],
            "payload_bundle_index_file_sha256": candidate["payload_bundle_index_file_sha256"],
            "receipt_index_sha256": reviewed_prefix["index_sha256"],
        },
    )
    review_stdout, _ = _read_no_follow(root, review_binding["stdout_ref"])
    if review_result["verdict"] != "AGREE" or review_stdout != b"VERDICT=AGREE\n":
        raise EvidenceValidationError("final reconstruction requires an agreeing result review")

    record = {
        "schema_version": "p01_final_decision@1",
        "phase": "P01",
        "result_round": result_round,
        "decision": "pass",
        "publication_mode": "disabled",
        "payload_bundle_index_digest": candidate["payload_bundle_index_digest"],
        "payload_bundle_index_file_sha256": candidate["payload_bundle_index_file_sha256"],
        "candidate_decision_ref": candidate_ref,
        "candidate_decision_sha256": candidate_sha256,
        "result_review_ref": review_ref,
        "result_review_sha256": review_sha256,
        "reviewed_receipt_index_ref": chain["index_ref"],
        "reviewed_receipt_index_sha256": chain["index_sha256"],
        "vetoes": candidate["vetoes"],
        "non_claims": candidate["non_claims"],
    }
    canonical_json_bytes(record, schema="p01_final_decision@1")
    return _normalize_json(record)


def verify_p01_final_decision_candidate(
    artifact_root: str | os.PathLike[str],
    *,
    final_candidate_ref: str,
    build_final_receipt_index_ref: str,
) -> dict[str, Any]:
    """Verify exact final bytes and the successful build receipt that named them."""
    root = Path(artifact_root)
    chain = verify_receipt_index(root, build_final_receipt_index_ref)
    round_ref = _p01_round_ref_from_index(build_final_receipt_index_ref)
    _p01_require_action_prefix(chain, P01_PASS_ACTION_SEQUENCE[:20])
    _p01_verify_receipt_commands(chain, round_ref)
    build_final = _only_receipt(chain, "build_final_candidate")
    if chain["receipts"][-1]["record"] != build_final:
        raise EvidenceValidationError("final verification requires build_final_candidate at the exact head")
    review_prefix = _require_receipt_snapshot(
        root,
        chain,
        index_ref=build_final["bindings"]["reviewed_receipt_index_ref"],
        index_sha256=build_final["bindings"]["reviewed_receipt_index_sha256"],
        head_check_id="result_review_binding",
    )
    expected = reconstruct_p01_final_decision(root, review_prefix["index_ref"])
    expected_ref = f"{round_ref}/P01-final-decision-candidate.json"
    if final_candidate_ref != expected_ref:
        raise EvidenceValidationError("final candidate ref is not the exact round-local path")
    final_bytes, _ = _read_no_follow(root, final_candidate_ref)
    final_candidate = strict_load_canonical_json(final_bytes, schema="p01_final_decision@1")
    expected_bytes = canonical_json_bytes(expected, schema="p01_final_decision@1")
    if final_bytes != expected_bytes:
        raise EvidenceValidationError("final decision does not equal independent reconstruction")
    final_sha256 = content_digest(final_bytes)
    _require_bindings(
        build_final["bindings"],
        {
            "final_candidate_ref": final_candidate_ref,
            "final_candidate_sha256": final_sha256,
            "result_review_ref": expected["result_review_ref"],
            "result_review_sha256": expected["result_review_sha256"],
            "reviewed_receipt_index_ref": review_prefix["index_ref"],
            "reviewed_receipt_index_sha256": review_prefix["index_sha256"],
        },
        "build_final_candidate",
    )
    return {
        "final_candidate": final_candidate,
        "final_candidate_sha256": final_sha256,
        "build_final_receipt_index_ref": chain["index_ref"],
        "build_final_receipt_index_sha256": chain["index_sha256"],
    }


def publish_stable_phase_decision(
    artifact_root: str | os.PathLike[str],
    *,
    candidate_ref: str,
    review_ref: str,
    audit_ref: str,
    validation_log_ref: str,
    governance_receipt_index_ref: str,
    stable_ref: str,
) -> dict[str, Any]:
    root = Path(artifact_root)
    final_bytes, final_stat = _read_no_follow(root, candidate_ref)
    strict_load_canonical_json(final_bytes, schema="p01_final_decision@1")
    final_sha256 = content_digest(final_bytes)
    terminal = verify_receipt_index(root, governance_receipt_index_ref)
    round_ref = _p01_round_ref_from_index(governance_receipt_index_ref)
    _p01_require_action_prefix(terminal, P01_PASS_ACTION_SEQUENCE)
    _p01_verify_receipt_commands(terminal, round_ref)
    final_gate = _only_receipt(terminal, "final_candidate_gate")
    verified_final = verify_p01_final_decision_candidate(
        root,
        final_candidate_ref=candidate_ref,
        build_final_receipt_index_ref=final_gate["bindings"]["validated_receipt_index_ref"],
    )
    final_candidate = verified_final["final_candidate"]
    if verified_final["final_candidate_sha256"] != final_sha256:
        raise EvidenceValidationError("final candidate digest changed during reconstruction")
    original_ref = final_candidate["candidate_decision_ref"]
    original_bytes, _ = _read_no_follow(root, original_ref)
    original = strict_load_canonical_json(original_bytes, schema="p01_candidate_decision@1")
    original_sha256 = content_digest(original_bytes)
    run_bytes, _ = _read_no_follow(root, original["run_manifest_ref"])
    run_manifest = strict_load_canonical_json(run_bytes, schema="p01_run_manifest@1")
    run_sha256 = content_digest(run_bytes)
    result_bytes, _ = _read_no_follow(root, original["result_ref"])
    result_sha256 = content_digest(result_bytes)
    bundle_index_bytes, _ = _read_no_follow(root, original["payload_bundle_index_ref"])
    bundle_index = strict_load_canonical_json(bundle_index_bytes, schema="payload_bundle_index@1")
    bundle_file_sha256 = content_digest(bundle_index_bytes)
    bundle_semantic_digest = content_digest(bundle_index, schema="payload_bundle_index@1")
    review_bytes, _ = _read_no_follow(root, review_ref)
    review_sha256 = content_digest(review_bytes)
    audit_bytes, _ = _read_no_follow(root, audit_ref)
    audit_sha256 = content_digest(audit_bytes)
    validation_bytes, _ = _read_no_follow(root, validation_log_ref)
    validation_sha256 = content_digest(validation_bytes)
    if terminal["record"]["result_round"] != final_candidate["result_round"]:
        raise EvidenceValidationError("terminal receipt round does not match final candidate")

    if (
        final_candidate["candidate_decision_ref"] != original_ref
        or final_candidate["candidate_decision_sha256"] != original_sha256
        or final_candidate["result_review_ref"] != review_ref
        or final_candidate["result_review_sha256"] != review_sha256
        or final_candidate["payload_bundle_index_digest"] != bundle_semantic_digest
        or final_candidate["payload_bundle_index_file_sha256"] != bundle_file_sha256
        or final_candidate["vetoes"] != original["vetoes"]
        or final_candidate["non_claims"] != original["non_claims"]
    ):
        raise EvidenceValidationError("final decision does not exactly bind the reviewed candidate payload")
    if (
        original["run_manifest_sha256"] != run_sha256
        or original["result_sha256"] != result_sha256
        or original["payload_bundle_index_digest"] != bundle_semantic_digest
        or original["payload_bundle_index_file_sha256"] != bundle_file_sha256
        or run_manifest["result_round"] != original["result_round"]
        or run_manifest["result_ref"] != original["result_ref"]
        or run_manifest["result_sha256"] != result_sha256
    ):
        raise EvidenceValidationError("candidate/run/result/payload bindings do not recompute")

    init_round = _only_receipt(terminal, "init_round")
    implementation_exit = _only_receipt(terminal, "implementation_exit")
    bind_result = _only_receipt(terminal, "bind_result")
    build_run = _only_receipt(terminal, "build_run_manifest")
    build_candidate = _only_receipt(terminal, "build_candidate")
    candidate_gate = _only_receipt(terminal, "candidate_gate")
    review_binding = _only_receipt(terminal, "result_review_binding")
    build_final = _only_receipt(terminal, "build_final_candidate")
    final_seal = _only_receipt(terminal, "final_seal_audit_binding")
    if terminal["receipts"][-1]["record"] != final_seal:
        raise EvidenceValidationError("stable publication requires final_seal_audit_binding at the terminal head")

    run_prefix = _require_receipt_snapshot(
        root,
        terminal,
        index_ref=run_manifest["pre_candidate_receipt_index_ref"],
        index_sha256=run_manifest["pre_candidate_receipt_index_sha256"],
        head_check_id="bind_result",
    )
    candidate_prefix = _require_receipt_snapshot(
        root,
        terminal,
        index_ref=original["pre_candidate_receipt_index_ref"],
        index_sha256=original["pre_candidate_receipt_index_sha256"],
        head_check_id="build_run_manifest",
    )
    review_prefix = _require_receipt_snapshot(
        root,
        terminal,
        index_ref=review_binding["bindings"]["reviewed_receipt_index_ref"],
        index_sha256=review_binding["bindings"]["reviewed_receipt_index_sha256"],
        head_check_id="candidate_gate",
    )
    final_build_prefix = _require_receipt_snapshot(
        root,
        terminal,
        index_ref=final_candidate["reviewed_receipt_index_ref"],
        index_sha256=final_candidate["reviewed_receipt_index_sha256"],
        head_check_id="result_review_binding",
    )
    final_gate_prefix = _require_receipt_snapshot(
        root,
        terminal,
        index_ref=final_gate["bindings"]["validated_receipt_index_ref"],
        index_sha256=final_gate["bindings"]["validated_receipt_index_sha256"],
        head_check_id="build_final_candidate",
    )
    audit_prefix = _require_receipt_snapshot(
        root,
        terminal,
        index_ref=final_seal["bindings"]["audited_receipt_index_ref"],
        index_sha256=final_seal["bindings"]["audited_receipt_index_sha256"],
        head_check_id="final_candidate_gate",
    )

    _require_bindings(
        init_round["bindings"],
        {
            "bootstrap_close_ref": original["predecessor"]["bootstrap_close_ref"],
            "bootstrap_close_sha256": original["predecessor"]["bootstrap_close_sha256"],
            "entry_implementation_manifest_sha256": original["predecessor"]["entry_implementation_manifest_sha256"],
            "entry_protected_manifest_sha256": original["predecessor"]["entry_protected_manifest_sha256"],
            "implementation_exit_manifest_sha256": original["implementation_exit_manifest_sha256"],
        },
        "init_round",
    )
    if (
        run_manifest["implementation_entry_manifest_sha256"]
        != init_round["bindings"]["entry_implementation_manifest_sha256"]
        or run_manifest["implementation_exit_manifest_sha256"]
        != init_round["bindings"]["implementation_exit_manifest_sha256"]
        or original["implementation_exit_manifest_sha256"]
        != implementation_exit["bindings"]["manifest_sha256"]
        or implementation_exit["bindings"]["manifest_ref"]
        != init_round["bindings"]["implementation_exit_manifest_ref"]
    ):
        raise EvidenceValidationError("entry/implementation-exit bindings do not recompute")
    _require_bindings(
        bind_result["bindings"],
        {"result_ref": original["result_ref"], "result_sha256": result_sha256},
        "bind_result",
    )

    _require_bindings(
        build_run["bindings"],
        {
            "run_manifest_ref": original["run_manifest_ref"],
            "run_manifest_sha256": run_sha256,
            "bound_receipt_index_ref": run_prefix["index_ref"],
            "bound_receipt_index_sha256": run_prefix["index_sha256"],
        },
        "build_run_manifest",
    )
    _require_bindings(
        build_candidate["bindings"],
        {
            "run_manifest_ref": original["run_manifest_ref"],
            "run_manifest_sha256": run_sha256,
            "candidate_ref": original_ref,
            "candidate_sha256": original_sha256,
            "bound_receipt_index_ref": candidate_prefix["index_ref"],
            "bound_receipt_index_sha256": candidate_prefix["index_sha256"],
        },
        "build_candidate",
    )
    candidate_gate_snapshot = _require_receipt_snapshot(
        root,
        terminal,
        index_ref=candidate_gate["bindings"]["validated_receipt_index_ref"],
        index_sha256=candidate_gate["bindings"]["validated_receipt_index_sha256"],
        head_check_id="build_candidate",
    )
    verified_candidate = verify_p01_candidate(
        root,
        candidate_ref=original_ref,
        build_run_receipt_index_ref=original["pre_candidate_receipt_index_ref"],
    )
    candidate_gate_stdout, _ = _read_no_follow(root, candidate_gate["stdout_ref"])
    candidate_validation_ref = f"{_p01_round_ref_from_index(governance_receipt_index_ref)}/logs/candidate-validation.log"
    candidate_validation_bytes, _ = _read_no_follow(root, candidate_validation_ref)
    if (
        candidate_gate_stdout != verified_candidate["report_bytes"]
        or candidate_validation_bytes != verified_candidate["report_bytes"]
    ):
        raise EvidenceValidationError("candidate validation report does not equal independent reconstruction")
    _require_bindings(
        candidate_gate["bindings"],
        {
            "run_manifest_ref": original["run_manifest_ref"],
            "run_manifest_sha256": run_sha256,
            "candidate_ref": original_ref,
            "candidate_sha256": original_sha256,
            "validated_receipt_index_ref": candidate_gate_snapshot["index_ref"],
            "validated_receipt_index_sha256": candidate_gate_snapshot["index_sha256"],
            "payload_bundle_index_ref": original["payload_bundle_index_ref"],
            "payload_bundle_index_digest": bundle_semantic_digest,
            "payload_bundle_index_file_sha256": bundle_file_sha256,
        },
        "candidate_gate",
    )
    _require_bindings(
        review_binding["bindings"],
        {
            "review_ref": review_ref,
            "review_sha256": review_sha256,
            "candidate_ref": original_ref,
            "candidate_sha256": original_sha256,
            "reviewed_receipt_index_ref": review_prefix["index_ref"],
            "reviewed_receipt_index_sha256": review_prefix["index_sha256"],
        },
        "result_review_binding",
    )
    _require_bindings(
        build_final["bindings"],
        {
            "final_candidate_ref": candidate_ref,
            "final_candidate_sha256": final_sha256,
            "result_review_ref": review_ref,
            "result_review_sha256": review_sha256,
            "reviewed_receipt_index_ref": final_build_prefix["index_ref"],
            "reviewed_receipt_index_sha256": final_build_prefix["index_sha256"],
        },
        "build_final_candidate",
    )
    _require_bindings(
        final_gate["bindings"],
        {
            "final_candidate_ref": candidate_ref,
            "final_candidate_sha256": final_sha256,
            "validation_log_ref": validation_log_ref,
            "validation_log_sha256": validation_sha256,
            "validated_receipt_index_ref": final_gate_prefix["index_ref"],
            "validated_receipt_index_sha256": final_gate_prefix["index_sha256"],
        },
        "final_candidate_gate",
    )
    _require_bindings(
        final_seal["bindings"],
        {
            "audit_ref": audit_ref,
            "audit_sha256": audit_sha256,
            "final_candidate_ref": candidate_ref,
            "final_candidate_sha256": final_sha256,
            "candidate_ref": original_ref,
            "candidate_sha256": original_sha256,
            "result_review_ref": review_ref,
            "result_review_sha256": review_sha256,
            "validation_log_ref": validation_log_ref,
            "validation_log_sha256": validation_sha256,
            "audited_receipt_index_ref": audit_prefix["index_ref"],
            "audited_receipt_index_sha256": audit_prefix["index_sha256"],
        },
        "final_seal_audit_binding",
    )
    review_result = verify_result_review_bindings(
        review_bytes,
        {
            "result_round": final_candidate["result_round"],
            "candidate_sha256": original_sha256,
            "run_manifest_sha256": run_sha256,
            "result_sha256": result_sha256,
            "payload_bundle_index_digest": bundle_semantic_digest,
            "payload_bundle_index_file_sha256": bundle_file_sha256,
            "receipt_index_sha256": review_prefix["index_sha256"],
        },
    )
    audit_result = verify_final_seal_audit_bindings(
        audit_bytes,
        {
            "result_round": final_candidate["result_round"],
            "final_candidate_sha256": final_sha256,
            "candidate_sha256": original_sha256,
            "result_review_sha256": review_sha256,
            "validation_log_sha256": validation_sha256,
            "receipt_index_sha256": audit_prefix["index_sha256"],
        },
    )
    if review_result["verdict"] != "AGREE" or audit_result["verdict"] != "AGREE":
        raise EvidenceValidationError("stable publication requires agreeing review and audit")
    current_final_bytes, current_final_stat = _read_no_follow(root, candidate_ref)
    if (
        content_digest(current_final_bytes) != final_sha256
        or (current_final_stat.st_dev, current_final_stat.st_ino) != (final_stat.st_dev, final_stat.st_ino)
    ):
        raise EvidenceValidationError("final candidate changed during stable-publication validation")
    source_parent, source_name = _open_parent_dir(root, candidate_ref, create=False)
    stable_parent, stable_name = _open_parent_dir(root, stable_ref, create=True)
    try:
        try:
            os.link(source_name, stable_name, src_dir_fd=source_parent, dst_dir_fd=stable_parent, follow_symlinks=False)
        except FileExistsError as exc:
            raise EvidenceConflictError(f"stable decision already exists: {stable_ref}") from exc
        os.fsync(stable_parent)
    finally:
        os.close(source_parent)
        os.close(stable_parent)
    stable_bytes, stable_stat = _read_no_follow(root, stable_ref)
    same_inode = (final_stat.st_dev, final_stat.st_ino) == (stable_stat.st_dev, stable_stat.st_ino)
    same_digest = final_sha256 == content_digest(stable_bytes)
    if not same_inode or not same_digest:
        raise EvidenceValidationError("stable publication did not preserve candidate inode and bytes")
    return {
        "stable_ref": stable_ref,
        "stable_sha256": content_digest(stable_bytes),
        "same_inode": same_inode,
        "same_digest": same_digest,
        "receipt_head_sha256": terminal["record"]["head_sha256"],
    }


def normalize_legacy_evidence(record: Any) -> dict[str, Any]:
    if not isinstance(record, dict):
        return {
            "schema_version": "0-legacy",
            "certification_state": "unbound_legacy_evidence",
            "claim_eligibility": "ineligible",
            "publication_enabled": False,
        }
    schema_version = str(record.get("schema_version", ""))
    if schema_version.startswith("1"):
        try:
            original = _normalize_json(record)
            _require_digest(original.get("evidence_manifest_digest"), "evidence_manifest_digest")
            without_digest = dict(original)
            without_digest.pop("evidence_manifest_digest")
            if original["evidence_manifest_digest"] != content_digest(without_digest):
                raise EvidenceValidationError("extended v1 self digest mismatch")
            required = set(MANIFEST_KEYS)
            if not required <= set(original):
                raise EvidenceValidationError("extended v1 record is missing required fields")
            base = {key: original[key] for key in MANIFEST_KEYS}
            base["schema_version"] = "1.0"
            base_without_digest = dict(base)
            base_without_digest.pop("evidence_manifest_digest")
            base["evidence_manifest_digest"] = content_digest(base_without_digest)
            validate_evidence_manifest(base)
        except (EvidenceValidationError, TypeError, ValueError):
            return {
                "schema_version": "unsupported",
                "certification_state": "invalid_or_partial_v1",
                "claim_eligibility": "ineligible",
                "publication_enabled": False,
            }
        return {
            "schema_version": schema_version,
            "certification_state": "sealed_pending_reader_verification",
            "ignored_additive_metadata": sorted(set(record) - set(MANIFEST_KEYS)),
            "claim_eligibility": "ineligible",
            "publication_enabled": False,
        }
    if schema_version and not schema_version.startswith("0"):
        return {
            "schema_version": "unsupported",
            "certification_state": "unknown_major_schema",
            "claim_eligibility": "ineligible",
            "publication_enabled": False,
        }
    return {
        "schema_version": "0-legacy",
        "certification_state": "unbound_legacy_evidence",
        "claim_eligibility": "ineligible",
        "publication_enabled": False,
    }
