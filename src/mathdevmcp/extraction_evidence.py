"""Strict Phase 02 extraction evidence, receipts, and reconstruction."""

from __future__ import annotations

import ast
import builtins
from copy import deepcopy
import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sysconfig
from types import FunctionType, ModuleType
from typing import Any, Iterable, Mapping, Sequence

from .evidence_manifest import (
    EvidenceValidationError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
    strict_load_canonical_json,
    verify_receipt_index as verify_p01_receipt_index,
)
from .label_scoped_obligation import (
    FIXTURE_CORPUS_VERSION,
    FROZEN_CORPUS_VERSION,
    extract_label_scoped_obligations,
    identity_payload,
    validate_label_scoped_obligation,
)


P02_PHASE = "P02"
P02_REVISION = "P02R3"
P02_EVIDENCE_ROOT_REF = ".local/mathdevmcp/evidence/p02r3-20260712"
P02_ENTRY_RECORD_REF = f"{P02_EVIDENCE_ROOT_REF}/entry/entry-record.json"
P02_PLAN_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-02r3-"
    "timeout-policy-recovery-subplan-2026-07-12.md"
)
P02_ORACLE_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-02r3-"
    "timeout-policy-recovery-oracle-2026-07-12.json"
)
P02_R2_PLAN_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-02r2-"
    "capability-scoped-parser-recovery-subplan-2026-07-12.md"
)
P02_R2_ORACLE_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-02r2-"
    "recovery-oracle-2026-07-12.json"
)
P02_R2_ENTRY_RECORD_REF = ".local/mathdevmcp/evidence/p02r2-20260712/entry/entry-record.json"
P02_BASE_PLAN_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-02-"
    "label-scoped-extraction-subplan-2026-07-11.md"
)
P02_BASE_ORACLE_REF = (
    "docs/plans/mathdevmcp-real-document-remediation-phase-02-"
    "extraction-oracle-2026-07-11.json"
)
P02_MATERIALIZED_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-02-materialized-obligations-oracle-2026-07-11.json"
P02_PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
P02_GOVERNANCE_REF = "scripts/p02_governance.py"
P02_ROUND_RE = re.compile(r"^rr0[1-5]$")
P02_SHA_RE = re.compile(r"^[0-9a-f]{64}$")
P02_GIT_OID_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
P02_UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

PARSER_VERSION_RECEIPT_KEYS = frozenset(
    {
        "argv",
        "backend",
        "environment",
        "exit_code",
        "schema_version",
        "stderr",
        "stdout",
        "timed_out",
        "timeout_seconds",
        "wall_time_ns",
    }
)
PARSER_SOURCE_RECEIPT_KEYS = frozenset(
    {
        "argv",
        "backend",
        "case_token",
        "environment",
        "exit_code",
        "log",
        "output",
        "schema_version",
        "source_ref",
        "source_sha256_after",
        "source_sha256_before",
        "stderr",
        "stdout",
        "timed_out",
        "timeout_seconds",
        "version_receipt_ref",
        "version_receipt_sha256",
        "wall_time_ns",
    }
)
PARSER_RAW_ARTIFACT_KEYS = frozenset({"byte_count", "present", "ref", "sha256"})
PARSER_RAW_INPUT_KEYS = frozenset(
    {
        "artifact_byte_count",
        "artifact_ref",
        "artifact_sha256",
        "invocation_receipt_ref",
        "invocation_receipt_sha256",
        "role",
        "value_type",
    }
)
PARSER_RAW_OUTPUT_KEYS = frozenset({"observed_value", "raw_observable_field"})
PARSER_PROJECTION_KEYS = frozenset(
    {"expected_value", "observable_field", "schema_version", "source_ref", "source_sha256"}
)
PARSER_OBSERVATION_PROVENANCE_KEYS = frozenset(
    {
        "extractor_id",
        "extractor_module_ref",
        "extractor_module_sha256",
        "forbidden_lineage",
        "raw_inputs",
        "raw_output",
    }
)
PARSER_COMPARISON_PROVENANCE_KEYS = frozenset(
    {
        "comparison_id",
        "expected_value",
        "expected_value_ref",
        "expected_value_sha256",
        "matched_requested_value",
        "matches_expected",
        "missing_requested_value",
        "raw_observed_value",
        "unscoped_extra_value",
    }
)
PARSER_SPECIALIST_KEYS = frozenset(
    {
        "backend",
        "capability_status",
        "comparison_provenance",
        "contradictions",
        "diagnostic_observations",
        "eligible_for_selection",
        "invocation_receipt_ref",
        "invocation_receipt_sha256",
        "limitation_codes",
        "observation_provenance",
        "promotional_fields",
        "source_ref",
    }
)
PARSER_CASE_KEYS = frozenset(
    {
        "case_token",
        "current_fidelity",
        "expected_value_ref",
        "expected_value_sha256",
        "schema_version",
        "selected_backend",
        "selected_version",
        "selection_reason",
        "source_ref",
        "source_sha256",
        "specialists",
    }
)
PARSER_VERSION_BINDING_KEYS = frozenset(
    {"backend", "receipt_ref", "receipt_sha256", "version_matches"}
)
PARSER_COMPARISON_KEYS = frozenset(
    {
        "case_count",
        "cases",
        "current_reconstruction_exact",
        "implementation_manifest_ref",
        "implementation_manifest_sha256",
        "invocation_count",
        "materially_better_specialist_count",
        "non_claims",
        "parser_veto",
        "phase",
        "profile_schema_version",
        "pure_extractor_module_ref",
        "pure_extractor_module_sha256",
        "result_round",
        "revision",
        "schema_version",
        "selected_backend_counts",
        "source_invocation_count",
        "version_invocation_count",
        "version_receipts",
    }
)

PARSER_NON_CLAIMS = [
    "Parser availability, parse success, output size, and runtime do not promote a parser.",
    "Parser comparison is extraction evidence only and is not mathematical certification.",
]

PARSER_BUNDLE_ROLES = {
    "obligations": "source_reconstructed_label_scoped_obligations",
    "reconstruction_summary": "source_oracle_reconstruction_summary",
    "parser_comparison": "differential_parser_fidelity_comparison",
    "mutation_matrix": "identity_mutation_and_ambiguity_matrix",
    "backend_ledger_index": "zero_backend_guard_ledger_index",
}

RECEIPT_KEYS = frozenset(
    {
        "schema_version",
        "phase",
        "result_round",
        "sequence",
        "check_id",
        "execution_class",
        "handler_id",
        "external_argv",
        "child_argv",
        "child_environment_sha256",
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
    }
)
RECEIPT_INDEX_KEYS = frozenset(
    {"schema_version", "phase", "result_round", "receipts", "head_sequence", "head_sha256"}
)
RECEIPT_INDEX_ENTRY_KEYS = frozenset({"sequence", "check_id", "receipt_ref", "receipt_sha256"})
INIT_PREDECESSOR_BINDING_KEYS = frozenset(
    {
        "predecessor_round_close_ref",
        "predecessor_round_close_sha256",
        "predecessor_terminal_receipt_index_ref",
        "predecessor_terminal_receipt_index_sha256",
    }
)
BUNDLE_INDEX_KEYS = frozenset(
    {
        "schema_version",
        "phase",
        "result_round",
        "artifact_inventory",
        "obligation_count",
        "unique_obligation_count",
        "semantic_digest",
        "backend_request_count",
        "source_edit_count",
        "publication_mode",
        "all_source_reconstructions_exact",
        "non_claims",
    }
)
BUNDLE_ARTIFACT_KEYS = frozenset({"logical_ref", "sha256", "byte_count", "role"})
OBLIGATION_BUNDLE_KEYS = frozenset(
    {"schema_version", "phase", "result_round", "obligation_count", "obligations"}
)
OBLIGATION_BUNDLE_ENTRY_KEYS = frozenset({"oracle_path", "obligation"})
RECONSTRUCTION_SUMMARY_KEYS = frozenset(
    {
        "schema_version",
        "phase",
        "result_round",
        "compact_oracle_sha256",
        "materialized_oracle_sha256",
        "obligation_count",
        "unique_obligation_count",
        "all_materialized_records_exact",
        "all_source_reconstructions_exact",
        "source_digests",
        "obligation_digests",
        "frozen_positive_obligation_digests",
        "backend_request_count",
        "source_edit_count",
        "publication_mode",
        "non_claims",
    }
)
GUARD_LEDGER_ENTRY_KEYS = frozenset(
    {
        "action",
        "ledger_ref",
        "ledger_sha256",
        "ledger_byte_count",
        "forbidden_attempt_count",
    }
)
LEDGER_INDEX_ATTESTATION_KEYS = frozenset(
    {
        "schema_version",
        "action",
        "ledger_ref",
        "ledger_sha256",
        "forbidden_attempt_count",
        "guard_replacement_errors",
        "parser_exception_enabled",
        "closed_at_utc",
        "attestation_ref",
        "attestation_sha256",
    }
)
MUTATION_KEYS = frozenset(
    {
        "schema_version",
        "phase",
        "result_round",
        "golden_canonical_byte_count",
        "golden_digest",
        "must_change_count",
        "must_change_pass_count",
        "must_not_change_count",
        "must_not_change_pass_count",
        "materialized_obligation_count",
        "unique_obligation_count",
        "ambiguity_case_count",
        "all_pass",
    }
)
LEDGER_INDEX_KEYS = frozenset(
    {
        "schema_version",
        "phase",
        "result_round",
        "ledgers",
        "attestations",
        "forbidden_attempt_count",
        "all_guards_intact",
    }
)
RUN_MANIFEST_KEYS = frozenset(
    {
        "schema_version",
        "phase",
        "result_round",
        "git_commit",
        "started_at_utc",
        "ended_at_utc",
        "wall_time_ns",
        "environment",
        "device_execution",
        "random_seed_policy",
        "plan_ref",
        "plan_sha256",
        "result_ref",
        "result_sha256",
        "governance_receipt_family_ref",
        "pre_candidate_receipt_index_ref",
        "pre_candidate_receipt_index_sha256",
        "entry_record_ref",
        "entry_record_sha256",
        "implementation_entry_manifest_sha256",
        "implementation_round_manifest_sha256",
        "implementation_delta_digest",
        "source_data_version",
        "frozen_source_digests",
        "external_tool_considerations",
        "artifact_inventory",
        "non_claims",
    }
)
RUN_MANIFEST_TOOL_KEYS = frozenset(
    {"tool", "role", "availability_version_evidence", "selected", "certifying_status"}
)
RUN_MANIFEST_PARSER_VERSION_EVIDENCE_KEYS = frozenset(
    {
        "evidence_type",
        "measured_version",
        "version_matches",
        "version_receipt_ref",
        "version_receipt_sha256",
    }
)
CANDIDATE_KEYS = frozenset(
    {
        "schema_version",
        "phase",
        "result_round",
        "decision",
        "publication_mode",
        "claim_eligibility",
        "entry_record_ref",
        "entry_record_sha256",
        "p01_stable_decision_ref",
        "p01_stable_decision_sha256",
        "p01_terminal_receipt_index_ref",
        "p01_terminal_receipt_index_sha256",
        "reviewed_plan_ref",
        "reviewed_plan_sha256",
        "reviewed_compact_oracle_ref",
        "reviewed_compact_oracle_sha256",
        "reviewed_materialized_oracle_ref",
        "reviewed_materialized_oracle_sha256",
        "implementation_entry_manifest_ref",
        "implementation_entry_manifest_sha256",
        "implementation_round_manifest_ref",
        "implementation_round_manifest_sha256",
        "protected_manifest_ref",
        "protected_manifest_sha256",
        "immutable_input_manifest_ref",
        "immutable_input_manifest_sha256",
        "run_manifest_ref",
        "run_manifest_sha256",
        "result_ref",
        "result_sha256",
        "pre_candidate_receipt_index_ref",
        "pre_candidate_receipt_index_sha256",
        "extraction_bundle_index_ref",
        "extraction_bundle_index_sha256",
        "extraction_bundle_semantic_digest",
        "parser_comparison_ref",
        "parser_comparison_sha256",
        "mutation_ambiguity_matrix_ref",
        "mutation_ambiguity_matrix_sha256",
        "backend_ledger_index_ref",
        "backend_ledger_index_sha256",
        "frozen_source_digests",
        "backend_request_count",
        "source_edit_count",
        "primary_criterion",
        "vetoes",
        "non_claims",
    }
)
FINAL_KEYS = frozenset(
    {
        "schema_version",
        "phase",
        "result_round",
        "decision",
        "publication_mode",
        "candidate_decision_ref",
        "candidate_decision_sha256",
        "result_review_ref",
        "result_review_sha256",
        "reviewed_receipt_index_ref",
        "reviewed_receipt_index_sha256",
        "p01_stable_decision_ref",
        "p01_stable_decision_sha256",
        "extraction_bundle_semantic_digest",
        "primary_criterion",
        "vetoes",
        "non_claims",
    }
)

P02_GUARDED_ACTIONS = (
    "localizer_tests",
    "obligation_tests",
    "target_integration_tests",
    "parser_fidelity_tests",
    "frozen_regressions",
    "p00_quarantine",
    "generate_extraction_bundle",
)


def extraction_artifact_refs(round_ref: str) -> dict[str, str]:
    result_round = PurePosixPath(round_ref).name
    if round_ref != _round_ref(result_round):
        raise EvidenceValidationError("extraction artifact round root mismatch")
    return {
        "bundle_index": f"{round_ref}/extraction-bundle/bundle-index.json",
        "obligations": f"{round_ref}/extraction-bundle/obligations.json",
        "reconstruction_summary": f"{round_ref}/extraction-bundle/reconstruction-summary.json",
        "parser_comparison": f"{round_ref}/parser/parser-comparison.json",
        "mutation_matrix": f"{round_ref}/summaries/mutation-ambiguity-matrix.json",
        "backend_ledger_index": f"{round_ref}/ledgers/backend-ledger-index.json",
    }


def _require_keys(value: Any, keys: frozenset[str], name: str) -> dict[str, Any]:
    if type(value) is not dict or set(value) != set(keys) or len(value) != len(keys):
        raise EvidenceValidationError(f"{name} keys differ from the closed Phase 02 schema")
    return value


def _require_string(value: Any, name: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value):
        raise EvidenceValidationError(f"{name} must be a string")
    return value


def _require_int(value: Any, name: str, *, nonnegative: bool = False) -> int:
    if type(value) is not int or (nonnegative and value < 0):
        raise EvidenceValidationError(f"{name} must be an integer")
    return value


def _require_bool(value: Any, name: str) -> bool:
    if type(value) is not bool:
        raise EvidenceValidationError(f"{name} must be a boolean")
    return value


def _require_sha(value: Any, name: str) -> str:
    text = _require_string(value, name)
    if P02_SHA_RE.fullmatch(text) is None:
        raise EvidenceValidationError(f"{name} must be a lower-case SHA-256")
    return text


def _logical_ref(value: Any, name: str) -> str:
    text = _require_string(value, name)
    path = PurePosixPath(text)
    if path.is_absolute() or text != path.as_posix() or any(part in {"", ".", ".."} for part in path.parts):
        raise EvidenceValidationError(f"{name} must be a normalized workspace-relative ref")
    return text


def _round_ref(result_round: str) -> str:
    if P02_ROUND_RE.fullmatch(result_round) is None:
        raise EvidenceValidationError("invalid Phase 02 result round")
    return f"{P02_EVIDENCE_ROOT_REF}/result-rounds/{result_round}"


def _read(root: Path, ref: str) -> bytes:
    raw, info = read_bytes_no_follow(root, _logical_ref(ref, "artifact ref"))
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError(f"artifact is not regular: {ref}")
    return raw


def _strict_json_object(raw: bytes, name: str, *, require_canonical: bool) -> dict[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"{name} violates strict JSON byte rules")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise EvidenceValidationError(f"{name} contains a duplicate key: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=reject_duplicates,
            parse_constant=lambda token: (_ for _ in ()).throw(
                EvidenceValidationError(f"{name} contains non-finite JSON: {token}")
            ),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"{name} is not strict JSON") from exc
    if type(value) is not dict:
        raise EvidenceValidationError(f"{name} must be a JSON object")
    if require_canonical and canonical_json_bytes(value) != raw:
        raise EvidenceValidationError(f"{name} is not canonical JSON")
    return value


def _strict_json(raw: bytes, name: str) -> dict[str, Any]:
    return _strict_json_object(raw, name, require_canonical=True)


def _strict_reviewed_json(raw: bytes, name: str) -> dict[str, Any]:
    """Load immutable reviewed JSON without imposing generated-artifact layout."""
    return _strict_json_object(raw, name, require_canonical=False)


def canonical_non_claims(value: Any) -> list[str]:
    """Return the canonical set-like representation used for persisted non-claims."""
    if type(value) is not list or not value or any(type(item) is not str or not item for item in value):
        raise EvidenceValidationError("P02 non-claims registry must contain nonempty strings")
    normalized = json.loads(canonical_json_bytes({"non_claims": value}).decode("utf-8"))["non_claims"]
    if len(normalized) != len(value):
        raise EvidenceValidationError("P02 non-claims registry contains duplicates")
    return normalized


def _resolve_profile_pointer(value: Any, pointer: str) -> tuple[dict[str, Any], str]:
    if not pointer.startswith("/"):
        raise EvidenceValidationError("P02 profile patch path is not absolute")
    tokens = [item.replace("~1", "/").replace("~0", "~") for item in pointer[1:].split("/")]
    current = value
    for token in tokens[:-1]:
        if type(current) is not dict or token not in current:
            raise EvidenceValidationError(f"P02 profile patch path does not resolve: {pointer}")
        current = current[token]
    if type(current) is not dict or tokens[-1] not in current:
        raise EvidenceValidationError(f"P02 profile patch path does not resolve: {pointer}")
    return current, tokens[-1]


def load_recovery_oracle(root: str | os.PathLike[str] = ".") -> dict[str, Any]:
    root_path = Path(root)
    recovery = _strict_reviewed_json(_read(root_path, P02_ORACLE_REF), "P02R3 recovery oracle")
    if (
        recovery.get("schema_version") != "p02r3_timeout_recovery_oracle@1"
        or recovery.get("phase") != P02_PHASE
        or recovery.get("revision") != P02_REVISION
    ):
        raise EvidenceValidationError("P02R3 recovery oracle metadata mismatch")
    bindings = recovery.get("base_bindings")
    if type(bindings) is not dict:
        raise EvidenceValidationError("P02R3 base bindings are missing")
    expected_ref_keys = {
        "p02r2_plan_ref",
        "p02r2_oracle_ref",
        "p02r2_bootstrap_ref",
        "p02r2_agreeing_review_ref",
        "p02r2_entry_ref",
        "timeout_blocker_ref",
        "timeout_adjudication_ref",
        "materialized_oracle_ref",
        "timeout_diagnostic_log_ref",
        "timeout_diagnostic_xml_ref",
    }
    if {key for key in bindings if key.endswith("_ref")} != expected_ref_keys:
        raise EvidenceValidationError("P02R3 base binding registry mismatch")
    for ref_key in expected_ref_keys:
        digest_key = ref_key.removesuffix("_ref") + "_sha256"
        ref = _logical_ref(bindings.get(ref_key), f"P02R3 {ref_key}")
        digest = _require_sha(bindings.get(digest_key), f"P02R3 {digest_key}")
        if content_digest(_read(root_path, ref)) != digest:
            raise EvidenceValidationError(f"P02R3 frozen binding drift: {ref_key}")
    if (
        bindings["p02r2_plan_ref"] != P02_R2_PLAN_REF
        or bindings["p02r2_oracle_ref"] != P02_R2_ORACLE_REF
        or bindings["p02r2_entry_ref"] != P02_R2_ENTRY_RECORD_REF
        or bindings["materialized_oracle_ref"] != P02_MATERIALIZED_REF
    ):
        raise EvidenceValidationError("P02R3 predecessor refs differ from production constants")
    refs = recovery.get("recovery_refs")
    if (
        type(refs) is not dict
        or refs.get("recovery_plan_ref") != P02_PLAN_REF
        or refs.get("recovery_oracle_ref") != P02_ORACLE_REF
        or refs.get("evidence_root_ref") != P02_EVIDENCE_ROOT_REF
        or refs.get("entry_record_ref") != P02_ENTRY_RECORD_REF
    ):
        raise EvidenceValidationError("P02R3 recovery refs differ from production constants")
    patches = recovery.get("profile_patch")
    if type(patches) is not list or len(patches) != 11:
        raise EvidenceValidationError("P02R3 profile patch registry mismatch")
    return recovery


def load_profile(root: str | os.PathLike[str] = ".") -> tuple[dict[str, Any], dict[str, Any]]:
    root_path = Path(root)
    recovery = load_recovery_oracle(root_path)
    r2 = _strict_reviewed_json(_read(root_path, P02_R2_ORACLE_REF), "P02R2 recovery oracle")
    if (
        r2.get("schema_version") != "p02r2_recovery_oracle@1"
        or r2.get("phase") != P02_PHASE
        or r2.get("revision") != "P02R2"
        or content_digest(_read(root_path, P02_R2_ORACLE_REF))
        != recovery["base_bindings"]["p02r2_oracle_sha256"]
    ):
        raise EvidenceValidationError("P02R2 transitive recovery binding mismatch")
    r2_bindings = r2.get("base_bindings")
    if type(r2_bindings) is not dict:
        raise EvidenceValidationError("P02R2 transitive base bindings are missing")
    for ref_key in (
        "base_plan_ref",
        "base_compact_oracle_ref",
        "base_materialized_oracle_ref",
        "prior_entry_ref",
        "runtime_contract_review_ref",
        "pre_round_blocker_ref",
    ):
        digest_key = ref_key.removesuffix("_ref") + "_sha256"
        ref = _logical_ref(r2_bindings.get(ref_key), f"P02R2 {ref_key}")
        digest = _require_sha(r2_bindings.get(digest_key), f"P02R2 {digest_key}")
        if content_digest(_read(root_path, ref)) != digest:
            raise EvidenceValidationError(f"P02R2 transitive binding drift: {ref_key}")
    if (
        r2_bindings["base_plan_ref"] != P02_BASE_PLAN_REF
        or r2_bindings["base_compact_oracle_ref"] != P02_BASE_ORACLE_REF
        or r2_bindings["base_materialized_oracle_ref"] != P02_MATERIALIZED_REF
    ):
        raise EvidenceValidationError("P02R2 transitive base refs differ from production constants")
    compact = _strict_reviewed_json(_read(root_path, P02_BASE_ORACLE_REF), "base compact oracle")
    materialized = _strict_reviewed_json(_read(root_path, P02_MATERIALIZED_REF), "materialized oracle")
    if compact.get("schema_version") != "p02_reviewed_extraction_oracle@1":
        raise EvidenceValidationError("base compact oracle metadata mismatch")
    if materialized.get("schema_version") != "p02_materialized_obligations_oracle@1":
        raise EvidenceValidationError("materialized oracle metadata mismatch")
    if content_digest(_read(root_path, P02_MATERIALIZED_REF)) != compact["materialized_obligations_oracle"]["sha256"]:
        raise EvidenceValidationError("materialized oracle binding mismatch")
    if content_digest(_read(root_path, P02_BASE_ORACLE_REF)) != r2_bindings["base_compact_oracle_sha256"]:
        raise EvidenceValidationError("base compact oracle transitive binding mismatch")
    effective = deepcopy(compact)
    patches = r2.get("profile_patch")
    if type(patches) is not list or len(patches) != 12:
        raise EvidenceValidationError("P02R2 effective profile patch registry mismatch")
    seen: set[str] = set()
    for patch in patches:
        if type(patch) is not dict or set(patch) != {"path", "expected_base_value", "replacement"}:
            raise EvidenceValidationError("P02R2 effective profile patch schema mismatch")
        pointer = _require_string(patch["path"], "P02R2 profile patch path")
        if pointer in seen:
            raise EvidenceValidationError("P02R2 effective profile patch path is duplicated")
        seen.add(pointer)
        parent, key = _resolve_profile_pointer(effective, pointer)
        if parent[key] != patch["expected_base_value"]:
            raise EvidenceValidationError(f"P02R2 effective profile patch baseline drift: {pointer}")
        parent[key] = deepcopy(patch["replacement"])
    effective["governance_action_profile"]["entry_snapshot_schema"] = deepcopy(r2["entry_schema"])
    effective["governance_action_profile"]["entry_bootstrap_profile"] = deepcopy(
        r2["entry_bootstrap_profile"]
    )
    effective["parser_capability_contract"] = deepcopy(r2["parser_capability_contract"])
    seen.clear()
    for patch in recovery["profile_patch"]:
        if type(patch) is not dict or set(patch) != {"path", "expected_base_value", "replacement"}:
            raise EvidenceValidationError("P02R3 effective profile patch schema mismatch")
        pointer = _require_string(patch["path"], "P02R3 profile patch path")
        if pointer in seen:
            raise EvidenceValidationError("P02R3 effective profile patch path is duplicated")
        seen.add(pointer)
        parent, key = _resolve_profile_pointer(effective, pointer)
        if parent[key] != patch["expected_base_value"]:
            raise EvidenceValidationError(f"P02R3 effective profile patch baseline drift: {pointer}")
        parent[key] = deepcopy(patch["replacement"])
    effective["governance_action_profile"]["entry_snapshot_schema"] = deepcopy(recovery["entry_schema"])
    effective["governance_action_profile"]["entry_bootstrap_profile"] = deepcopy(
        recovery["entry_bootstrap_profile"]
    )
    close_schema = effective["governance_action_profile"]["round_close_schema"]
    close_schema["non_claims"] = canonical_non_claims(close_schema["non_claims"])
    return effective, materialized


def governance_profile(root: str | os.PathLike[str] = ".") -> dict[str, Any]:
    return load_profile(root)[0]["governance_action_profile"]


def implementation_allowlist(root: str | os.PathLike[str] = ".") -> tuple[str, ...]:
    argv = governance_profile(root)["actions"]["compile"]["child_argv_template"]
    expected_prefix = [P02_PYTHON, "-m", "py_compile"]
    if argv[:3] != expected_prefix:
        raise EvidenceValidationError("compile action does not expose the Phase 02 allowlist")
    refs = tuple(argv[3:])
    if list(refs) != sorted(set(refs), key=lambda item: item.encode("utf-8")):
        raise EvidenceValidationError("Phase 02 implementation allowlist is not sorted unique")
    return refs


def _sorted_unique_strings(value: Any, name: str) -> list[str]:
    if type(value) is not list or any(type(item) is not str or not item for item in value):
        raise EvidenceValidationError(f"{name} must be a list of nonempty strings")
    expected = sorted(set(value), key=lambda item: item.encode("utf-8"))
    if value != expected:
        raise EvidenceValidationError(f"{name} must be sorted unique by UTF-8 bytes")
    return value


def _string_mapping(value: Any, name: str) -> dict[str, str]:
    if type(value) is not dict or any(type(key) is not str or type(item) is not str for key, item in value.items()):
        raise EvidenceValidationError(f"{name} must be an object of strings")
    return value


def _parser_ref(value: Any, round_ref: str, name: str) -> str:
    ref = _logical_ref(value, name)
    if not ref.startswith(f"{round_ref}/parser/"):
        raise EvidenceValidationError(f"{name} is outside the validated parser root")
    return ref


def _ensure_safe_directory(root: Path, ref: str, name: str) -> None:
    current = root
    for part in PurePosixPath(_logical_ref(ref, name)).parts:
        current = current / part
        try:
            info = current.lstat()
        except FileNotFoundError as exc:
            raise EvidenceValidationError(f"{name} is missing: {ref}") from exc
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise EvidenceValidationError(f"{name} is not a no-follow directory: {ref}")


def _artifact_absent_no_follow(root: Path, ref: str, round_ref: str) -> bool:
    _parser_ref(ref, round_ref, "absent parser artifact ref")
    parent = PurePosixPath(ref).parent.as_posix()
    _ensure_safe_directory(root, parent, "parser artifact parent")
    path = root / ref
    try:
        info = path.lstat()
    except FileNotFoundError:
        return True
    if stat.S_ISLNK(info.st_mode):
        raise EvidenceValidationError(f"missing parser artifact path is a symlink: {ref}")
    return False


def validate_parser_raw_artifact_binding(
    root: str | os.PathLike[str],
    value: Any,
    *,
    round_ref: str,
    expected_ref: str | None = None,
    name: str = "parser raw artifact",
) -> dict[str, Any]:
    root_path = Path(root)
    record = _require_keys(value, PARSER_RAW_ARTIFACT_KEYS, name)
    ref = _parser_ref(record["ref"], round_ref, f"{name} ref")
    _require_bool(record["present"], f"{name} present")
    if expected_ref is not None:
        _parser_ref(expected_ref, round_ref, f"{name} expected ref")
        if ref != expected_ref:
            raise EvidenceValidationError(f"{name} ref differs from the fixed profile path")
    if record["present"]:
        digest = _require_sha(record["sha256"], f"{name} sha256")
        byte_count = _require_int(record["byte_count"], f"{name} byte count", nonnegative=True)
        raw = _read(root_path, ref)
        if len(raw) != byte_count or content_digest(raw) != digest:
            raise EvidenceValidationError(f"{name} digest/count mismatch")
    else:
        if record["sha256"] is not None or record["byte_count"] is not None:
            raise EvidenceValidationError(f"{name} absent binding must have null digest/count")
        if not _artifact_absent_no_follow(root_path, ref, round_ref):
            raise EvidenceValidationError(f"{name} claims an existing path is absent")
    return record


def _attribute_chain(node: ast.Attribute) -> str | None:
    parts: list[str] = [node.attr]
    value: ast.expr = node.value
    while isinstance(value, ast.Attribute):
        parts.append(value.attr)
        value = value.value
    if not isinstance(value, ast.Name):
        return None
    parts.append(value.id)
    return ".".join(reversed(parts))


def _function_locals(node: ast.FunctionDef) -> set[str]:
    result = {item.arg for item in (*node.args.posonlyargs, *node.args.args, *node.args.kwonlyargs)}
    if node.args.vararg is not None:
        result.add(node.args.vararg.arg)
    if node.args.kwarg is not None:
        result.add(node.args.kwarg.arg)
    result.update(
        item.id
        for item in ast.walk(node)
        if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Store)
    )
    result.update(
        item.name
        for item in ast.walk(node)
        if isinstance(item, ast.ExceptHandler) and item.name is not None
    )
    return result


def _validate_store_target(target: ast.AST, forbidden: set[str], function_name: str) -> None:
    if isinstance(target, ast.Name):
        if not isinstance(target.ctx, ast.Store) or target.id in forbidden:
            raise EvidenceValidationError(f"pure extractor {function_name} has a forbidden store target")
        return
    if isinstance(target, (ast.Tuple, ast.List)) and isinstance(target.ctx, ast.Store):
        for item in target.elts:
            _validate_store_target(item, forbidden, function_name)
        return
    raise EvidenceValidationError(f"pure extractor {function_name} has a non-local store target")


def _audit_pure_extractor_function(node: ast.FunctionDef, contract: Mapping[str, Any]) -> None:
    name = node.name
    expected_parameters = contract["positional_parameters"]
    if (
        [item.arg for item in node.args.args] != expected_parameters
        or node.args.posonlyargs
        or node.args.kwonlyargs
        or node.args.vararg is not None
        or node.args.kwarg is not None
        or node.args.defaults
        or node.args.kw_defaults
        or node.decorator_list
        or node.returns is not None
        or node.type_comment is not None
        or any(item.annotation is not None or item.type_comment is not None for item in node.args.args)
    ):
        raise EvidenceValidationError(f"pure extractor {name} signature/decoration mismatch")
    forbidden_nodes = {
        ast.AsyncFunctionDef,
        ast.Await,
        ast.ClassDef,
        ast.Delete,
        ast.Global,
        ast.Import,
        ast.ImportFrom,
        ast.Lambda,
        ast.ListComp,
        ast.SetComp,
        ast.DictComp,
        ast.GeneratorExp,
        ast.NamedExpr,
        ast.Nonlocal,
        ast.With,
        ast.AsyncWith,
        ast.Yield,
        ast.YieldFrom,
    }
    for descendant in ast.walk(node):
        if descendant is not node and isinstance(descendant, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            raise EvidenceValidationError(f"pure extractor {name} contains a nested callable/class")
        if type(descendant) in forbidden_nodes:
            raise EvidenceValidationError(f"pure extractor {name} contains {type(descendant).__name__}")
        if isinstance(descendant, ast.Name) and isinstance(descendant.ctx, ast.Del):
            raise EvidenceValidationError(f"pure extractor {name} contains a delete target")

    globals_allowed = set(contract["referenced_globals"])
    builtins_allowed = set(contract["referenced_builtins"])
    builtin_calls_allowed = set(contract["builtin_callable_allowlist"])
    imported_attributes_allowed = set(contract["imported_attribute_allowlist"])
    imported_calls_allowed = set(contract["imported_callable_allowlist"])
    value_attributes_allowed = set(contract["value_attribute_read_allowlist"])
    value_methods_allowed = set(contract["value_method_call_allowlist"])
    forbidden_stores = globals_allowed | builtins_allowed | set(contract["callable_dependency_allowlist"])

    for descendant in ast.walk(node):
        if isinstance(descendant, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets = descendant.targets if isinstance(descendant, ast.Assign) else [descendant.target]
            for target in targets:
                _validate_store_target(target, forbidden_stores, name)
        elif isinstance(descendant, (ast.For, ast.AsyncFor)):
            _validate_store_target(descendant.target, forbidden_stores, name)
        elif isinstance(descendant, ast.comprehension):
            _validate_store_target(descendant.target, forbidden_stores, name)
        elif isinstance(descendant, ast.ExceptHandler) and descendant.name is not None:
            if descendant.name in forbidden_stores:
                raise EvidenceValidationError(f"pure extractor {name} has a forbidden exception target")

    local_names = _function_locals(node)
    loaded_nonlocals = {
        item.id
        for item in ast.walk(node)
        if isinstance(item, ast.Name) and isinstance(item.ctx, ast.Load) and item.id not in local_names
    }
    if loaded_nonlocals != globals_allowed | builtins_allowed:
        raise EvidenceValidationError(f"pure extractor {name} loaded-name registry mismatch")

    imported_attributes_seen: set[str] = set()
    value_attributes_seen: set[str] = set()
    for item in ast.walk(node):
        if not isinstance(item, ast.Attribute) or not isinstance(item.ctx, ast.Load):
            continue
        if item.attr.startswith("__") and item.attr.endswith("__"):
            raise EvidenceValidationError(f"pure extractor {name} uses a dunder attribute")
        chain = _attribute_chain(item)
        if chain in imported_attributes_allowed:
            imported_attributes_seen.add(chain)
            continue
        if item.attr in value_attributes_allowed:
            value_attributes_seen.add(item.attr)
            continue
        parent_is_call = any(
            isinstance(call, ast.Call) and call.func is item for call in ast.walk(node)
        )
        if parent_is_call and item.attr in value_methods_allowed and not isinstance(
            item.value, (ast.Call, ast.Subscript, ast.Lambda)
        ):
            continue
        raise EvidenceValidationError(f"pure extractor {name} attribute is not registered: {chain or item.attr}")
    if imported_attributes_seen != imported_attributes_allowed or value_attributes_seen != value_attributes_allowed:
        raise EvidenceValidationError(f"pure extractor {name} attribute registry is not exact")

    builtin_calls_seen: set[str] = set()
    imported_calls_seen: set[str] = set()
    value_methods_seen: set[str] = set()
    for call in (item for item in ast.walk(node) if isinstance(item, ast.Call)):
        if isinstance(call.func, ast.Name):
            if call.func.id not in builtin_calls_allowed:
                raise EvidenceValidationError(f"pure extractor {name} calls an unregistered name")
            builtin_calls_seen.add(call.func.id)
        elif isinstance(call.func, ast.Attribute):
            chain = _attribute_chain(call.func)
            if chain in imported_calls_allowed:
                imported_calls_seen.add(chain)
            elif call.func.attr in value_methods_allowed and not isinstance(
                call.func.value, (ast.Call, ast.Subscript, ast.Lambda)
            ):
                value_methods_seen.add(call.func.attr)
            else:
                raise EvidenceValidationError(f"pure extractor {name} calls an unregistered attribute")
        else:
            raise EvidenceValidationError(f"pure extractor {name} has an indirect call")
    if (
        not builtin_calls_seen <= builtin_calls_allowed
        or not imported_calls_seen <= imported_calls_allowed
        or not value_methods_seen <= value_methods_allowed
    ):
        raise EvidenceValidationError(f"pure extractor {name} callable registry is not exact")


def validate_pure_extractor_module_bytes(
    raw: bytes,
    contract: Mapping[str, Any],
    *,
    module_ref: str | None = None,
) -> dict[str, Any]:
    pure = contract["pure_extractor_module_contract"]
    module_ref = module_ref or pure["module_ref"]
    if raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError("pure extractor module violates strict source-byte rules")
    try:
        text = raw.decode("utf-8", "strict")
        tree = ast.parse(text, filename=module_ref, mode="exec", type_comments=True)
    except (UnicodeDecodeError, SyntaxError) as exc:
        raise EvidenceValidationError("pure extractor module is not strict valid Python") from exc
    function_contracts = pure["function_contracts"]
    expected_functions = list(function_contracts)
    expected_imports = pure["allowed_imports"]
    if len(tree.body) != len(expected_imports) + len(expected_functions):
        raise EvidenceValidationError("pure extractor module top-level statement count mismatch")
    for node, expected in zip(tree.body[: len(expected_imports)], expected_imports, strict=True):
        if not isinstance(node, ast.Import) or len(node.names) != 1:
            raise EvidenceValidationError("pure extractor module import shape mismatch")
        alias = node.names[0]
        if expected != {"form": "import", "module": alias.name, "alias": alias.asname}:
            raise EvidenceValidationError("pure extractor module import registry mismatch")
    functions = tree.body[len(expected_imports) :]
    if not all(isinstance(node, ast.FunctionDef) for node in functions):
        raise EvidenceValidationError("pure extractor module has a non-function top-level statement")
    if [node.name for node in functions] != expected_functions:
        raise EvidenceValidationError("pure extractor module function order mismatch")
    for node in functions:
        _audit_pure_extractor_function(node, function_contracts[node.name])

    module_name = "mathdevmcp.parser_capability_extractors"
    spec = importlib.util.spec_from_file_location(module_name, module_ref)
    if spec is None:
        raise EvidenceValidationError("pure extractor module spec could not be created")
    module = ModuleType(module_name)
    module.__cached__ = None
    module.__file__ = module_ref
    module.__loader__ = spec.loader
    module.__package__ = "mathdevmcp"
    module.__spec__ = spec
    try:
        code = compile(tree, module_ref, "exec", dont_inherit=True)
        exec(code, module.__dict__)
    except Exception as exc:
        raise EvidenceValidationError("statically accepted pure extractor module failed to load") from exc
    expected_namespace = {
        "__builtins__",
        "__cached__",
        "__doc__",
        "__file__",
        "__loader__",
        "__name__",
        "__package__",
        "__spec__",
        "json",
        "re",
        "ET",
        *expected_functions,
    }
    if set(module.__dict__) != expected_namespace or module.__doc__ is not None:
        raise EvidenceValidationError("pure extractor runtime module namespace mismatch")
    if module.__dict__["__builtins__"] is not builtins.__dict__:
        raise EvidenceValidationError("pure extractor runtime builtins mismatch")
    stdlib = Path(sysconfig.get_path("stdlib")).resolve()
    for alias in ("json", "re", "ET"):
        imported = module.__dict__[alias]
        if not isinstance(imported, ModuleType):
            raise EvidenceValidationError("pure extractor imported global is not a module")
        origin = getattr(imported, "__file__", None)
        if origin is None or stdlib not in Path(origin).resolve().parents:
            raise EvidenceValidationError("pure extractor imported module is not from the standard library")
    for name, function_contract in function_contracts.items():
        function = module.__dict__[name]
        if (
            type(function) is not FunctionType
            or function.__module__ != module_name
            or function.__name__ != name
            or function.__qualname__ != name
            or function.__globals__ is not module.__dict__
            or function.__closure__ is not None
            or function.__defaults__ is not None
            or function.__kwdefaults__ is not None
            or function.__annotations__ != {}
            or function.__code__.co_freevars != ()
            or function.__code__.co_cellvars != ()
            or list(inspect.signature(function).parameters) != function_contract["positional_parameters"]
            or any(
                parameter.kind is not inspect.Parameter.POSITIONAL_OR_KEYWORD
                or parameter.default is not inspect.Parameter.empty
                or parameter.annotation is not inspect.Parameter.empty
                for parameter in inspect.signature(function).parameters.values()
            )
            or inspect.signature(function).return_annotation is not inspect.Signature.empty
        ):
            raise EvidenceValidationError(f"pure extractor runtime function mismatch: {name}")
        for dotted in function_contract["imported_attribute_allowlist"]:
            root_name, attribute = dotted.split(".", 1)
            imported_attribute = getattr(module.__dict__[root_name], attribute)
            expected_module = module.__dict__[root_name].__name__
            if getattr(imported_attribute, "__module__", None) != expected_module:
                raise EvidenceValidationError(f"pure extractor imported attribute origin mismatch: {dotted}")
    return {
        "module": module,
        "functions": {name: module.__dict__[name] for name in expected_functions},
        "module_ref": module_ref,
        "module_sha256": content_digest(raw),
    }


def verify_pure_extractor_module(
    root: str | os.PathLike[str],
    implementation_manifest_ref: str,
) -> dict[str, Any]:
    root_path = Path(root)
    result_round = PurePosixPath(implementation_manifest_ref).parent.name
    round_ref = _round_ref(result_round)
    expected_manifest_ref = f"{round_ref}/implementation-round-sha256.txt"
    if implementation_manifest_ref != expected_manifest_ref:
        raise EvidenceValidationError("parser implementation manifest ref mismatch")
    manifest_raw = _read(root_path, implementation_manifest_ref)
    manifest = parse_sha256_manifest(manifest_raw)
    contract = load_profile(root_path)[0]["parser_capability_contract"]
    module_ref = contract["pure_extractor_module_contract"]["module_ref"]
    if module_ref not in manifest:
        raise EvidenceValidationError("pure extractor module is absent from the round implementation manifest")
    module_raw = _read(root_path, module_ref)
    if content_digest(module_raw) != manifest[module_ref]:
        raise EvidenceValidationError("pure extractor module differs from the round implementation manifest")
    result = validate_pure_extractor_module_bytes(module_raw, contract, module_ref=module_ref)
    result.update(
        {
            "implementation_manifest_ref": implementation_manifest_ref,
            "implementation_manifest_sha256": content_digest(manifest_raw),
            "implementation_manifest": manifest,
        }
    )
    return result


def _parser_environment(profile: Mapping[str, Any], round_ref: str) -> dict[str, str]:
    return {key: value.replace("RR", round_ref) for key, value in profile["environment"].items()}


def _parser_case_token(source_ref: str) -> str:
    return hashlib.sha256(source_ref.encode("utf-8")).hexdigest()


def _parser_version_ref(round_ref: str, backend: str) -> str:
    return f"{round_ref}/parser/receipts/{backend}-version-raw.json"


def _parser_source_receipt_ref(round_ref: str, backend: str, source_ref: str) -> str:
    return f"{round_ref}/parser/receipts/{backend}-{_parser_case_token(source_ref)}-raw.json"


def _parser_observation_ref(round_ref: str, backend: str, source_ref: str) -> str:
    return f"{round_ref}/parser/observations/{backend}-{_parser_case_token(source_ref)}-raw-output.json"


def _parser_projection_ref(round_ref: str, source_ref: str) -> str:
    return f"{round_ref}/parser/expected-values/{_parser_case_token(source_ref)}-exact-requested-label-set.json"


def _validate_exit_state(value: Mapping[str, Any], name: str) -> None:
    exit_code = value["exit_code"]
    if exit_code is not None and type(exit_code) is not int:
        raise EvidenceValidationError(f"{name} exit code must be an integer or null")
    timed_out = _require_bool(value["timed_out"], f"{name} timed out")
    if timed_out != (exit_code is None):
        raise EvidenceValidationError(f"{name} timeout/exit-code nullability mismatch")
    _require_int(value["wall_time_ns"], f"{name} wall time", nonnegative=True)


def _strict_version_matches(backend: str, raw: bytes, expected_version: str) -> bool:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError:
        return False
    if backend == "latexml":
        matches = re.findall(r"LaTeXML version ([0-9]+(?:\.[0-9]+)*)", text)
    elif backend == "pandoc":
        matches = re.findall(r"(?m)^pandoc ([0-9]+(?:\.[0-9]+)*)[ \t]*$", text)
    else:
        raise EvidenceValidationError("unregistered parser backend")
    return matches == [expected_version]


def validate_parser_version_receipt(
    root: str | os.PathLike[str],
    value: Any,
    *,
    round_ref: str,
    backend: str,
    profile: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    profile = profile or load_profile(root_path)[0]["parser_fidelity_profile"]
    if backend not in profile["executables"]:
        raise EvidenceValidationError("parser version receipt backend is not registered")
    executable = profile["executables"][backend]
    record = _require_keys(value, PARSER_VERSION_RECEIPT_KEYS, "parser version receipt")
    if record["schema_version"] != "p02r2_parser_version_invocation_receipt@1" or record["backend"] != backend:
        raise EvidenceValidationError("parser version receipt metadata mismatch")
    if record["argv"] != executable["version_argv"]:
        raise EvidenceValidationError("parser version receipt argv mismatch")
    if _string_mapping(record["environment"], "parser version environment") != _parser_environment(profile, round_ref):
        raise EvidenceValidationError("parser version receipt environment mismatch")
    if _require_int(record["timeout_seconds"], "parser version timeout") != executable["version_timeout_seconds"]:
        raise EvidenceValidationError("parser version receipt timeout mismatch")
    if record["timeout_seconds"] <= 0:
        raise EvidenceValidationError("parser version timeout must be positive")
    _validate_exit_state(record, "parser version receipt")
    stdout_ref = f"{round_ref}/parser/receipts/{backend}-version.stdout"
    stderr_ref = f"{round_ref}/parser/receipts/{backend}-version.stderr"
    validate_parser_raw_artifact_binding(
        root_path, record["stdout"], round_ref=round_ref, expected_ref=stdout_ref, name="parser version stdout"
    )
    validate_parser_raw_artifact_binding(
        root_path, record["stderr"], round_ref=round_ref, expected_ref=stderr_ref, name="parser version stderr"
    )
    if not record["stdout"]["present"] or not record["stderr"]["present"]:
        raise EvidenceValidationError("parser version streams must be present")
    return record


def verify_parser_version_receipt(
    root: str | os.PathLike[str],
    round_ref: str,
    backend: str,
    *,
    profile: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    profile = profile or load_profile(root_path)[0]["parser_fidelity_profile"]
    ref = _parser_version_ref(round_ref, backend)
    raw = _read(root_path, ref)
    record = validate_parser_version_receipt(
        root_path, _strict_json(raw, f"{backend} parser version receipt"), round_ref=round_ref, backend=backend, profile=profile
    )
    streams = _read(root_path, record["stdout"]["ref"]) + _read(root_path, record["stderr"]["ref"])
    version_matches = (
        not record["timed_out"]
        and record["exit_code"] == 0
        and _strict_version_matches(backend, streams, profile["executables"][backend]["measured_version"])
    )
    return {"ref": ref, "sha256": content_digest(raw), "record": record, "version_matches": version_matches}


def _expected_parser_artifact_refs(round_ref: str, backend: str, source_ref: str) -> dict[str, str | None]:
    case_token = _parser_case_token(source_ref)
    stdout_ref = f"{round_ref}/parser/receipts/{backend}-{case_token}.stdout"
    stderr_ref = f"{round_ref}/parser/receipts/{backend}-{case_token}.stderr"
    if backend == "latexml":
        return {
            "stdout": stdout_ref,
            "stderr": stderr_ref,
            "output": f"{round_ref}/parser/latexml/{case_token}.xml",
            "log": f"{round_ref}/parser/latexml/{case_token}.log",
        }
    if backend == "pandoc":
        return {"stdout": stdout_ref, "stderr": stderr_ref, "output": stdout_ref, "log": None}
    raise EvidenceValidationError("unregistered parser backend")


def validate_parser_source_receipt(
    root: str | os.PathLike[str],
    value: Any,
    *,
    round_ref: str,
    backend: str,
    source_ref: str,
    version: Mapping[str, Any],
    profile: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    profile = profile or load_profile(root_path)[0]["parser_fidelity_profile"]
    if backend not in profile["executables"] or source_ref not in profile["source_allowlist"]:
        raise EvidenceValidationError("parser source receipt is outside the reviewed invocation closure")
    executable = profile["executables"][backend]
    record = _require_keys(value, PARSER_SOURCE_RECEIPT_KEYS, "parser source invocation receipt")
    case_token = _parser_case_token(source_ref)
    if (
        record["schema_version"] != "p02r2_parser_source_invocation_receipt@1"
        or record["backend"] != backend
        or record["source_ref"] != source_ref
        or record["case_token"] != case_token
    ):
        raise EvidenceValidationError("parser source receipt metadata mismatch")
    expected_argv = [
        item.replace("RR", round_ref).replace("CASE", case_token).replace("SOURCE", source_ref)
        for item in executable["fidelity_argv_template"]
    ]
    if record["argv"] != expected_argv:
        raise EvidenceValidationError("parser source receipt argv mismatch")
    if _string_mapping(record["environment"], "parser source environment") != _parser_environment(profile, round_ref):
        raise EvidenceValidationError("parser source receipt environment mismatch")
    timeout = _require_int(record["timeout_seconds"], "parser source timeout")
    if timeout <= 0 or timeout != executable["source_timeout_seconds"]:
        raise EvidenceValidationError("parser source receipt timeout mismatch")
    _validate_exit_state(record, "parser source receipt")
    _require_sha(record["source_sha256_before"], "parser source digest before")
    _require_sha(record["source_sha256_after"], "parser source digest after")
    if (
        record["version_receipt_ref"] != version["ref"]
        or record["version_receipt_sha256"] != version["sha256"]
    ):
        raise EvidenceValidationError("parser source receipt version binding mismatch")
    expected_refs = _expected_parser_artifact_refs(round_ref, backend, source_ref)
    for field in ("stdout", "stderr", "output"):
        validate_parser_raw_artifact_binding(
            root_path,
            record[field],
            round_ref=round_ref,
            expected_ref=str(expected_refs[field]),
            name=f"parser source {field}",
        )
    if backend == "latexml":
        if record["log"] is None:
            raise EvidenceValidationError("LaTeXML source receipt log binding is null")
        validate_parser_raw_artifact_binding(
            root_path,
            record["log"],
            round_ref=round_ref,
            expected_ref=str(expected_refs["log"]),
            name="parser source log",
        )
    elif record["log"] is not None or record["output"] != record["stdout"]:
        raise EvidenceValidationError("Pandoc output/log binding mismatch")
    if not record["stdout"]["present"] or not record["stderr"]["present"]:
        raise EvidenceValidationError("parser source stdout/stderr must be present")
    return record


def _parser_receipt_closure(
    root: Path,
    round_ref: str,
    profile: Mapping[str, Any],
) -> tuple[dict[str, dict[str, Any]], dict[tuple[str, str], tuple[str, bytes]]]:
    receipts_ref = f"{round_ref}/parser/receipts"
    _ensure_safe_directory(root, receipts_ref, "parser receipt directory")
    directory = root / receipts_ref
    expected_versions = {_parser_version_ref(round_ref, backend) for backend in profile["executables"]}
    expected_sources = {
        _parser_source_receipt_ref(round_ref, backend, source_ref)
        for source_ref in profile["source_allowlist"]
        for backend in profile["executables"]
    }
    actual: set[str] = set()
    for item in directory.glob("*-raw.json"):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise EvidenceValidationError("parser raw invocation receipt is not a no-follow regular file")
        actual.add(item.relative_to(root).as_posix())
    if actual != expected_versions | expected_sources:
        raise EvidenceValidationError("parser raw invocation receipts do not close at exact 2+26")
    versions = {
        backend: verify_parser_version_receipt(root, round_ref, backend, profile=profile)
        for backend in profile["executables"]
    }
    source_raw = {
        (backend, source_ref): (
            _parser_source_receipt_ref(round_ref, backend, source_ref),
            _read(root, _parser_source_receipt_ref(round_ref, backend, source_ref)),
        )
        for source_ref in profile["source_allowlist"]
        for backend in profile["executables"]
    }
    return versions, source_raw


def _parser_expected_sources(root: Path, profile: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    verified = verify_materialized_obligations(root)
    grouped: dict[str, dict[str, Any]] = {}
    for record in verified["records"].values():
        source_ref = record["document"]["file"]
        source_sha256 = record["document"]["source_digest"]
        item = grouped.setdefault(source_ref, {"source_sha256": source_sha256, "labels": []})
        if item["source_sha256"] != source_sha256:
            raise EvidenceValidationError("one parser source has inconsistent reviewed digests")
        item["labels"].append(record["label"])
    if set(grouped) != set(profile["source_allowlist"]):
        raise EvidenceValidationError("reviewed requested-label projection does not cover the parser source allowlist")
    for source_ref, item in grouped.items():
        item["labels"] = sorted(set(item["labels"]), key=lambda value: value.encode("utf-8"))
        source_raw = _read(root, source_ref)
        if content_digest(source_raw) != item["source_sha256"]:
            raise EvidenceValidationError("parser source differs from the reviewed source digest")
    return grouped


def _raw_binding_state(
    root: Path,
    value: Any,
    *,
    round_ref: str,
    expected_ref: str,
    required: bool,
) -> tuple[bool, bool, dict[str, Any] | None]:
    if type(value) is not dict or set(value) != set(PARSER_RAW_ARTIFACT_KEYS):
        return False, False, None
    if value.get("ref") != expected_ref or type(value.get("present")) is not bool:
        return False, False, value
    if not value["present"]:
        if value.get("sha256") is not None or value.get("byte_count") is not None:
            return False, False, value
        try:
            absent = _artifact_absent_no_follow(root, expected_ref, round_ref)
        except EvidenceValidationError:
            return False, True, value
        return absent, required, value
    if P02_SHA_RE.fullmatch(value.get("sha256", "")) is None or type(value.get("byte_count")) is not int or value["byte_count"] < 0:
        return False, False, value
    try:
        raw = _read(root, expected_ref)
    except (EvidenceValidationError, FileNotFoundError):
        return True, True, value
    if len(raw) != value["byte_count"] or content_digest(raw) != value["sha256"]:
        return False, False, value
    return True, False, value


def _malformed_limitations(backend: str, inputs: Sequence[bytes]) -> list[str]:
    joined = b"\n".join(inputs).decode("utf-8", "replace")
    if "undefined environment" in joined or "undefined-environment" in joined:
        return ["undefined_environment"]
    if "undefined control sequence" in joined.lower() or "undefined macro" in joined.lower():
        return ["undefined_macro_affecting_target"]
    if "<ERROR" in joined or ":ERROR" in joined:
        return ["error_node_in_target_output"]
    return ["malformed_label_ownership" if backend == "latexml" else "collapsed_row_ownership"]


def _source_state(
    root: Path,
    round_ref: str,
    backend: str,
    source_ref: str,
    raw: bytes,
    version: Mapping[str, Any],
    profile: Mapping[str, Any],
    expected: Mapping[str, Any],
    pure: Mapping[str, Any],
) -> dict[str, Any]:
    receipt_ref = _parser_source_receipt_ref(round_ref, backend, source_ref)
    receipt_sha256 = content_digest(raw)
    base = {
        "backend": backend,
        "source_ref": source_ref,
        "receipt_ref": receipt_ref,
        "receipt_sha256": receipt_sha256,
        "record": None,
        "raw_inputs": [],
        "raw_output": None,
        "observation_ref": _parser_observation_ref(round_ref, backend, source_ref),
    }
    try:
        record = _strict_json(raw, f"{backend} parser source receipt")
    except EvidenceValidationError:
        return {**base, "status": "invocation_mismatch", "limitations": ["invocation_mismatch"]}
    if type(record) is not dict or set(record) != set(PARSER_SOURCE_RECEIPT_KEYS):
        return {**base, "record": record, "status": "invocation_mismatch", "limitations": ["invocation_mismatch"]}
    before = record.get("source_sha256_before")
    after = record.get("source_sha256_after")
    if P02_SHA_RE.fullmatch(before if type(before) is str else "") and P02_SHA_RE.fullmatch(
        after if type(after) is str else ""
    ) and before != after:
        return {**base, "record": record, "status": "source_mutated", "limitations": ["source_mutated"]}
    executable = profile["executables"][backend]
    case_token = _parser_case_token(source_ref)
    expected_argv = [
        item.replace("RR", round_ref).replace("CASE", case_token).replace("SOURCE", source_ref)
        for item in executable["fidelity_argv_template"]
    ]
    scalar_exact = (
        record.get("schema_version") == "p02r2_parser_source_invocation_receipt@1"
        and record.get("backend") == backend
        and record.get("source_ref") == source_ref
        and record.get("case_token") == case_token
        and record.get("argv") == expected_argv
        and record.get("environment") == _parser_environment(profile, round_ref)
        and type(record.get("timeout_seconds")) is int
        and record["timeout_seconds"] == executable["source_timeout_seconds"]
        and type(record.get("timed_out")) is bool
        and type(record.get("wall_time_ns")) is int
        and record["wall_time_ns"] >= 0
        and (record.get("exit_code") is None or type(record.get("exit_code")) is int)
        and record["timed_out"] == (record.get("exit_code") is None)
        and before == expected["source_sha256"]
        and after == expected["source_sha256"]
        and record.get("version_receipt_ref") == version["ref"]
        and record.get("version_receipt_sha256") == version["sha256"]
    )
    expected_refs = _expected_parser_artifact_refs(round_ref, backend, source_ref)
    binding_states: dict[str, tuple[bool, bool, dict[str, Any] | None]] = {}
    for field in ("stdout", "stderr"):
        binding_states[field] = _raw_binding_state(
            root, record.get(field), round_ref=round_ref, expected_ref=str(expected_refs[field]), required=True
        )
    output_required = backend == "pandoc"
    binding_states["output"] = _raw_binding_state(
        root, record.get("output"), round_ref=round_ref, expected_ref=str(expected_refs["output"]), required=output_required
    )
    if backend == "latexml":
        binding_states["log"] = _raw_binding_state(
            root, record.get("log"), round_ref=round_ref, expected_ref=str(expected_refs["log"]), required=True
        )
        log_exact = True
    else:
        log_exact = record.get("log") is None
        if record.get("output") != record.get("stdout"):
            scalar_exact = False
    if not scalar_exact or not log_exact or any(not state[0] and not state[1] for state in binding_states.values()):
        return {**base, "record": record, "status": "invocation_mismatch", "limitations": ["invocation_mismatch"]}
    if any(state[1] for state in binding_states.values()):
        return {**base, "record": record, "status": "missing_artifact", "limitations": ["missing_artifact"]}
    if not version["version_matches"]:
        return {**base, "record": record, "status": "version_mismatch", "limitations": ["version_mismatch"]}
    if record["timed_out"]:
        return {**base, "record": record, "status": "timed_out", "limitations": ["timeout"]}
    if record["exit_code"] != 0:
        return {**base, "record": record, "status": "nonzero_exit", "limitations": ["nonzero_exit"]}
    if backend == "latexml" and not record["output"]["present"]:
        return {
            **base,
            "record": record,
            "status": "malformed_output",
            "limitations": ["malformed_label_ownership"],
        }
    contract = load_profile(root)[0]["parser_capability_contract"]
    registry_items = [
        (extractor_id, item)
        for extractor_id, item in contract["extractor_registry"].items()
        if item["backend"] == backend
    ]
    if len(registry_items) != 1:
        raise EvidenceValidationError("parser backend does not have exactly one registered extractor")
    extractor_id, registry = registry_items[0]
    input_bytes: list[bytes] = []
    raw_inputs: list[dict[str, Any]] = []
    for role, value_type, field in zip(
        registry["input_roles"],
        registry["input_value_types"],
        registry["input_receipt_artifact_fields"],
        strict=True,
    ):
        binding = record[field]
        if not binding["present"]:
            return {**base, "record": record, "status": "missing_artifact", "limitations": ["missing_artifact"]}
        artifact_raw = _read(root, binding["ref"])
        input_bytes.append(artifact_raw)
        raw_inputs.append(
            {
                "artifact_byte_count": binding["byte_count"],
                "artifact_ref": binding["ref"],
                "artifact_sha256": binding["sha256"],
                "invocation_receipt_ref": receipt_ref,
                "invocation_receipt_sha256": receipt_sha256,
                "role": role,
                "value_type": value_type,
            }
        )
    function = pure["functions"][registry["function_name"]]
    try:
        output = function(*input_bytes)
    except ValueError:
        return {
            **base,
            "record": record,
            "raw_inputs": raw_inputs,
            "status": "malformed_output",
            "limitations": _malformed_limitations(backend, input_bytes),
        }
    except Exception as exc:
        raise EvidenceValidationError("pure parser extractor raised an unreviewed exception") from exc
    validate_parser_raw_output(output, registry=registry)
    status = "valid_source_mappable" if registry["promotion_capable"] else "valid_not_source_mappable"
    limitations = [] if status == "valid_source_mappable" else [
        "no_independent_source_offsets",
        "global_label_set_only",
        "collapsed_row_ownership",
    ]
    return {
        **base,
        "record": record,
        "raw_inputs": raw_inputs,
        "raw_output": output,
        "extractor_id": extractor_id,
        "registry": registry,
        "status": status,
        "limitations": limitations,
    }


def validate_parser_raw_output(value: Any, *, registry: Mapping[str, Any]) -> dict[str, Any]:
    record = _require_keys(value, PARSER_RAW_OUTPUT_KEYS, "parser raw extractor output")
    if record["raw_observable_field"] != registry["raw_observable_field"]:
        raise EvidenceValidationError("parser raw extractor field mismatch")
    _sorted_unique_strings(record["observed_value"], "parser raw observed value")
    return record


def _collect_parser_states(
    root: Path,
    round_ref: str,
    implementation_manifest_ref: str,
    *,
    require_observations: bool,
) -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    result_round = PurePosixPath(round_ref).name
    if round_ref != _round_ref(result_round):
        raise EvidenceValidationError("parser result-round root mismatch")
    effective, _ = load_profile(root)
    profile = effective["parser_fidelity_profile"]
    pure = verify_pure_extractor_module(root, implementation_manifest_ref)
    versions, source_raw = _parser_receipt_closure(root, round_ref, profile)
    expected = _parser_expected_sources(root, profile)
    states: list[dict[str, Any]] = []
    for source_ref in profile["source_allowlist"]:
        for backend in profile["executables"]:
            _ref, raw = source_raw[(backend, source_ref)]
            state = _source_state(
                root, round_ref, backend, source_ref, raw, versions[backend], profile, expected[source_ref], pure
            )
            observation_ref = state["observation_ref"]
            if state["raw_output"] is None:
                if not _artifact_absent_no_follow(root, observation_ref, round_ref):
                    raise EvidenceValidationError("parser observation exists for a non-observation capability state")
            elif require_observations:
                observation_raw = _read(root, observation_ref)
                observed = validate_parser_raw_output(
                    _strict_json(observation_raw, "parser raw observation artifact"), registry=state["registry"]
                )
                if observed != state["raw_output"]:
                    raise EvidenceValidationError("parser raw observation differs from independent extraction")
            else:
                if not _artifact_absent_no_follow(root, observation_ref, round_ref):
                    raise EvidenceValidationError("parser raw observation output already exists")
            states.append(state)
    observations_ref = f"{round_ref}/parser/observations"
    _ensure_safe_directory(root, observations_ref, "parser observation directory")
    expected_observation_refs = {
        state["observation_ref"] for state in states if state["raw_output"] is not None
    }
    actual_observation_refs: set[str] = set()
    for item in (root / observations_ref).glob("*.json"):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise EvidenceValidationError("parser raw observation is not a no-follow regular file")
        actual_observation_refs.add(item.relative_to(root).as_posix())
    if require_observations:
        if actual_observation_refs != expected_observation_refs:
            raise EvidenceValidationError("parser raw observations do not exactly cover successful extraction")
    elif actual_observation_refs:
        raise EvidenceValidationError("parser raw observations exist before the raw-observation build step")
    if len(versions) != 2 or len(states) != 26:
        raise EvidenceValidationError("parser invocation reconstruction does not close at exact 2+26")
    return versions, expected, states, pure


def build_parser_raw_observations(
    root: str | os.PathLike[str],
    round_ref: str,
    implementation_manifest_ref: str,
) -> list[dict[str, Any]]:
    root_path = Path(root)
    _versions, _expected, states, _pure = _collect_parser_states(
        root_path, round_ref, implementation_manifest_ref, require_observations=False
    )
    return [
        {"ref": state["observation_ref"], "record": state["raw_output"]}
        for state in states
        if state["raw_output"] is not None
    ]


def verify_parser_timeout_gate(
    root: str | os.PathLike[str],
    round_ref: str,
    implementation_manifest_ref: str,
) -> dict[str, int | bool]:
    """Reconstruct the separate zero-timeout action gate from sealed receipts."""
    root_path = Path(root)
    versions, _expected, states, _pure = _collect_parser_states(
        root_path, round_ref, implementation_manifest_ref, require_observations=True
    )
    version_timeout_count = sum(int(item["record"]["timed_out"]) for item in versions.values())
    source_timeout_count = sum(int(item["record"]["timed_out"]) for item in states)
    return {
        "all_invocations_completed_within_ceiling": version_timeout_count + source_timeout_count == 0,
        "source_timeout_count": source_timeout_count,
        "timed_out_invocation_count": version_timeout_count + source_timeout_count,
        "version_timeout_count": version_timeout_count,
    }


def validate_expected_value_projection(
    value: Any,
    *,
    source_ref: str,
    source_sha256: str,
    expected_value: Sequence[str],
) -> dict[str, Any]:
    record = _require_keys(value, PARSER_PROJECTION_KEYS, "parser expected-value projection")
    if (
        record["schema_version"] != "p02r2_expected_label_value_projection@1"
        or record["source_ref"] != source_ref
        or record["source_sha256"] != source_sha256
        or record["observable_field"] != "exact_requested_label_set"
        or record["expected_value"] != list(expected_value)
    ):
        raise EvidenceValidationError("parser expected-value projection mismatch")
    _require_sha(record["source_sha256"], "parser projection source digest")
    _sorted_unique_strings(record["expected_value"], "parser expected-value projection")
    return record


def build_expected_value_projections(
    root: str | os.PathLike[str],
    round_ref: str,
) -> list[dict[str, Any]]:
    root_path = Path(root)
    implementation_manifest_ref = f"{round_ref}/implementation-round-sha256.txt"
    _versions, expected, _states, _pure = _collect_parser_states(
        root_path, round_ref, implementation_manifest_ref, require_observations=True
    )
    profile = load_profile(root_path)[0]["parser_fidelity_profile"]
    result: list[dict[str, Any]] = []
    for source_ref in profile["source_allowlist"]:
        ref = _parser_projection_ref(round_ref, source_ref)
        if not _artifact_absent_no_follow(root_path, ref, round_ref):
            raise EvidenceValidationError("parser expected-value projection already exists")
        item = expected[source_ref]
        record = {
            "expected_value": item["labels"],
            "observable_field": "exact_requested_label_set",
            "schema_version": "p02r2_expected_label_value_projection@1",
            "source_ref": source_ref,
            "source_sha256": item["source_sha256"],
        }
        validate_expected_value_projection(
            record,
            source_ref=source_ref,
            source_sha256=item["source_sha256"],
            expected_value=item["labels"],
        )
        result.append({"ref": ref, "record": record})
    return result


def validate_parser_raw_inputs(
    root: str | os.PathLike[str],
    value: Any,
    *,
    round_ref: str,
    registry: Mapping[str, Any],
    receipt_ref: str,
    receipt_sha256: str,
    receipt: Mapping[str, Any],
) -> list[dict[str, Any]]:
    root_path = Path(root)
    if type(value) is not list or len(value) != len(registry["input_roles"]):
        raise EvidenceValidationError("parser raw inputs do not match the extractor arity")
    seen_roles: set[str] = set()
    seen_refs: set[str] = set()
    for index, (item, role, value_type, artifact_field) in enumerate(
        zip(
            value,
            registry["input_roles"],
            registry["input_value_types"],
            registry["input_receipt_artifact_fields"],
            strict=True,
        )
    ):
        record = _require_keys(item, PARSER_RAW_INPUT_KEYS, f"parser raw input {index}")
        artifact_ref = _parser_ref(record["artifact_ref"], round_ref, f"parser raw input {index} ref")
        artifact_sha256 = _require_sha(record["artifact_sha256"], f"parser raw input {index} digest")
        artifact_byte_count = _require_int(
            record["artifact_byte_count"], f"parser raw input {index} byte count", nonnegative=True
        )
        if (
            record["role"] != role
            or record["value_type"] != value_type
            or record["invocation_receipt_ref"] != receipt_ref
            or record["invocation_receipt_sha256"] != receipt_sha256
        ):
            raise EvidenceValidationError("parser raw input registry/receipt binding mismatch")
        if role in seen_roles or artifact_ref in seen_refs:
            raise EvidenceValidationError("parser raw inputs contain a duplicate role or artifact ref")
        seen_roles.add(role)
        seen_refs.add(artifact_ref)
        binding = receipt[artifact_field]
        if (
            type(binding) is not dict
            or not binding.get("present")
            or binding.get("ref") != artifact_ref
            or binding.get("sha256") != artifact_sha256
            or binding.get("byte_count") != artifact_byte_count
        ):
            raise EvidenceValidationError("parser raw input differs from its receipt artifact binding")
        raw = _read(root_path, artifact_ref)
        if len(raw) != artifact_byte_count or content_digest(raw) != artifact_sha256:
            raise EvidenceValidationError("parser raw input artifact digest/count mismatch")
    return value


def _validate_observation_provenance(
    root: Path,
    value: Any,
    *,
    round_ref: str,
    state: Mapping[str, Any],
    pure: Mapping[str, Any],
) -> dict[str, Any]:
    record = _require_keys(value, PARSER_OBSERVATION_PROVENANCE_KEYS, "parser observation provenance")
    registry = state["registry"]
    if (
        record["extractor_id"] != state["extractor_id"]
        or record["extractor_module_ref"] != registry["module_ref"]
        or record["extractor_module_ref"] != pure["module_ref"]
        or record["extractor_module_sha256"] != pure["module_sha256"]
        or record["forbidden_lineage"] != []
    ):
        raise EvidenceValidationError("parser observation provenance module/lineage mismatch")
    validate_parser_raw_inputs(
        root,
        record["raw_inputs"],
        round_ref=round_ref,
        registry=registry,
        receipt_ref=state["receipt_ref"],
        receipt_sha256=state["receipt_sha256"],
        receipt=state["record"],
    )
    validate_parser_raw_output(record["raw_output"], registry=registry)
    if record["raw_output"] != state["raw_output"]:
        raise EvidenceValidationError("parser observation provenance raw output mismatch")
    return record


def _coverage_comparison(
    raw_observed: Sequence[str],
    expected: Sequence[str],
    *,
    projection_ref: str,
    projection_sha256: str,
) -> dict[str, Any]:
    raw_set = set(raw_observed)
    expected_set = set(expected)
    matched = sorted(raw_set & expected_set, key=lambda item: item.encode("utf-8"))
    missing = sorted(expected_set - raw_set, key=lambda item: item.encode("utf-8"))
    extra = sorted(raw_set - expected_set, key=lambda item: item.encode("utf-8"))
    return {
        "comparison_id": "p02r2_requested_label_coverage_comparison_v1",
        "expected_value": list(expected),
        "expected_value_ref": projection_ref,
        "expected_value_sha256": projection_sha256,
        "matched_requested_value": matched,
        "matches_expected": not missing and matched == list(expected),
        "missing_requested_value": missing,
        "raw_observed_value": list(raw_observed),
        "unscoped_extra_value": extra,
    }


def _validate_comparison_provenance(
    value: Any,
    *,
    state: Mapping[str, Any],
    projection_ref: str,
    projection_sha256: str,
    expected_value: Sequence[str],
) -> dict[str, Any]:
    record = _require_keys(value, PARSER_COMPARISON_PROVENANCE_KEYS, "parser comparison provenance")
    expected = _coverage_comparison(
        state["raw_output"]["observed_value"],
        expected_value,
        projection_ref=projection_ref,
        projection_sha256=projection_sha256,
    )
    if record != expected:
        raise EvidenceValidationError("parser comparison provenance differs from requested-label coverage")
    for key in (
        "expected_value",
        "matched_requested_value",
        "missing_requested_value",
        "raw_observed_value",
        "unscoped_extra_value",
    ):
        _sorted_unique_strings(record[key], f"parser comparison {key}")
    return record


def _specialist_record(
    root: Path,
    round_ref: str,
    state: Mapping[str, Any],
    pure: Mapping[str, Any],
    projection_ref: str,
    projection_sha256: str,
    expected_value: Sequence[str],
) -> dict[str, Any]:
    field = "exact_requested_label_set"
    observations: dict[str, bool] = {}
    observation_provenance: dict[str, Any] = {}
    comparison_provenance: dict[str, Any] = {}
    if state["raw_output"] is not None:
        observation = {
            "extractor_id": state["extractor_id"],
            "extractor_module_ref": state["registry"]["module_ref"],
            "extractor_module_sha256": pure["module_sha256"],
            "forbidden_lineage": [],
            "raw_inputs": state["raw_inputs"],
            "raw_output": state["raw_output"],
        }
        comparison = _coverage_comparison(
            state["raw_output"]["observed_value"],
            expected_value,
            projection_ref=projection_ref,
            projection_sha256=projection_sha256,
        )
        observations[field] = comparison["matches_expected"]
        observation_provenance[field] = observation
        comparison_provenance[field] = comparison
    contradictions = [key for key, matches in observations.items() if not matches]
    promotional_fields = [field] if state["status"] == "valid_source_mappable" else []
    eligible = (
        state["status"] == "valid_source_mappable"
        and bool(promotional_fields)
        and not state["limitations"]
        and not contradictions
    )
    record = {
        "backend": state["backend"],
        "capability_status": state["status"],
        "comparison_provenance": comparison_provenance,
        "contradictions": contradictions,
        "diagnostic_observations": observations,
        "eligible_for_selection": eligible,
        "invocation_receipt_ref": state["receipt_ref"],
        "invocation_receipt_sha256": state["receipt_sha256"],
        "limitation_codes": state["limitations"],
        "observation_provenance": observation_provenance,
        "promotional_fields": promotional_fields,
        "source_ref": state["source_ref"],
    }
    validate_parser_specialist_record(
        root,
        record,
        round_ref=round_ref,
        state=state,
        pure=pure,
        projection_ref=projection_ref,
        projection_sha256=projection_sha256,
        expected_value=expected_value,
    )
    return record


def validate_parser_specialist_record(
    root: str | os.PathLike[str],
    value: Any,
    *,
    round_ref: str,
    state: Mapping[str, Any],
    pure: Mapping[str, Any],
    projection_ref: str,
    projection_sha256: str,
    expected_value: Sequence[str],
) -> dict[str, Any]:
    root_path = Path(root)
    contract = load_profile(root_path)[0]["parser_capability_contract"]
    record = _require_keys(value, PARSER_SPECIALIST_KEYS, "parser specialist capability record")
    if (
        record["backend"] != state["backend"]
        or record["source_ref"] != state["source_ref"]
        or record["invocation_receipt_ref"] != state["receipt_ref"]
        or record["invocation_receipt_sha256"] != state["receipt_sha256"]
        or record["capability_status"] != state["status"]
        or record["limitation_codes"] != state["limitations"]
    ):
        raise EvidenceValidationError("parser specialist capability binding/status mismatch")
    status = record["capability_status"]
    if status not in contract["capability_status_enum"]:
        raise EvidenceValidationError("parser specialist capability status is not registered")
    limitations = record["limitation_codes"]
    if type(limitations) is not list or len(limitations) != len(set(limitations)) or any(
        item not in contract["limitation_codes"] for item in limitations
    ):
        raise EvidenceValidationError("parser specialist limitations are not registered unique codes")
    observed = record["diagnostic_observations"]
    observation = record["observation_provenance"]
    comparison = record["comparison_provenance"]
    if (
        type(observed) is not dict
        or type(observation) is not dict
        or type(comparison) is not dict
        or list(observed) != list(observation)
        or list(observed) != list(comparison)
        or any(key not in contract["observable_fields"] or type(item) is not bool for key, item in observed.items())
    ):
        raise EvidenceValidationError("parser specialist observation/provenance field registry mismatch")
    for field in observed:
        _validate_observation_provenance(root_path, observation[field], round_ref=round_ref, state=state, pure=pure)
        _validate_comparison_provenance(
            comparison[field],
            state=state,
            projection_ref=projection_ref,
            projection_sha256=projection_sha256,
            expected_value=expected_value,
        )
        if observed[field] != comparison[field]["matches_expected"]:
            raise EvidenceValidationError("parser specialist observation value differs from comparison provenance")
    contradictions = record["contradictions"]
    expected_contradictions = [key for key, matches in observed.items() if not matches]
    if contradictions != expected_contradictions:
        raise EvidenceValidationError("parser specialist contradiction registry mismatch")
    promotional = record["promotional_fields"]
    observable_fields = contract["observable_fields"]
    if type(promotional) is not list or promotional != observable_fields[: len(promotional)]:
        raise EvidenceValidationError("parser specialist promotional fields are not a leading prefix")
    if any(field not in observed for field in promotional):
        raise EvidenceValidationError("parser specialist promotes a field without independent provenance")
    if status == "valid_source_mappable":
        if limitations or not promotional:
            raise EvidenceValidationError("source-mappable specialist has limitations or no promotion prefix")
    elif promotional or record["eligible_for_selection"]:
        raise EvidenceValidationError("non-source-mappable/error specialist is promotional or eligible")
    if status == "malformed_output" and observed:
        raise EvidenceValidationError("malformed specialist output carries observations")
    if status not in {"valid_source_mappable", "valid_not_source_mappable"} and not limitations:
        raise EvidenceValidationError("parser error capability status has no limitation")
    expected_eligible = status == "valid_source_mappable" and bool(promotional) and not limitations and not contradictions
    if _require_bool(record["eligible_for_selection"], "parser specialist eligibility") != expected_eligible:
        raise EvidenceValidationError("parser specialist eligibility mismatch")
    return record


def _load_parser_projections(
    root: Path,
    round_ref: str,
    profile: Mapping[str, Any],
    expected: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    directory_ref = f"{round_ref}/parser/expected-values"
    _ensure_safe_directory(root, directory_ref, "parser projection directory")
    expected_refs = {_parser_projection_ref(round_ref, source_ref) for source_ref in profile["source_allowlist"]}
    actual_refs: set[str] = set()
    for item in (root / directory_ref).glob("*.json"):
        info = item.lstat()
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
            raise EvidenceValidationError("parser expected-value projection is not a no-follow regular file")
        actual_refs.add(item.relative_to(root).as_posix())
    if actual_refs != expected_refs:
        raise EvidenceValidationError("parser expected-value projections do not exactly cover all source cases")
    result: dict[str, dict[str, Any]] = {}
    for source_ref in profile["source_allowlist"]:
        ref = _parser_projection_ref(round_ref, source_ref)
        raw = _read(root, ref)
        record = validate_expected_value_projection(
            _strict_json(raw, "parser expected-value projection"),
            source_ref=source_ref,
            source_sha256=expected[source_ref]["source_sha256"],
            expected_value=expected[source_ref]["labels"],
        )
        result[source_ref] = {"ref": ref, "sha256": content_digest(raw), "record": record}
    return result


def _parser_veto(specialists: Sequence[Mapping[str, Any]]) -> bool:
    evidence_failure = {
        "source_mutated",
        "invocation_mismatch",
        "missing_artifact",
        "version_mismatch",
    }
    return any(
        item["capability_status"] in evidence_failure
        or bool(item["contradictions"])
        for item in specialists
    )


def build_parser_comparison(
    root: str | os.PathLike[str],
    round_ref: str,
    implementation_manifest_ref: str,
) -> dict[str, Any]:
    root_path = Path(root)
    effective, _ = load_profile(root_path)
    profile = effective["parser_fidelity_profile"]
    contract = effective["parser_capability_contract"]
    versions, expected, states, pure = _collect_parser_states(
        root_path, round_ref, implementation_manifest_ref, require_observations=True
    )
    projections = _load_parser_projections(root_path, round_ref, profile, expected)
    cases: list[dict[str, Any]] = []
    all_specialists: list[dict[str, Any]] = []
    state_by_key = {(state["source_ref"], state["backend"]): state for state in states}
    for source_ref in profile["source_allowlist"]:
        projection = projections[source_ref]
        specialists = [
            _specialist_record(
                root_path,
                round_ref,
                state_by_key[(source_ref, backend)],
                pure,
                projection["ref"],
                projection["sha256"],
                projection["record"]["expected_value"],
            )
            for backend in profile["executables"]
        ]
        all_specialists.extend(specialists)
        current_fidelity = {field: True for field in contract["observable_fields"]}
        case = {
            "case_token": _parser_case_token(source_ref),
            "current_fidelity": current_fidelity,
            "expected_value_ref": projection["ref"],
            "expected_value_sha256": projection["sha256"],
            "schema_version": "p02r2_parser_case_comparison@1",
            "selected_backend": contract["primary_backend"],
            "selected_version": contract["primary_version"],
            "selection_reason": "current_exact_reconstruction_retained; specialists_are_diagnostic_only",
            "source_ref": source_ref,
            "source_sha256": expected[source_ref]["source_sha256"],
            "specialists": specialists,
        }
        cases.append(case)
    version_bindings = [
        {
            "backend": backend,
            "receipt_ref": versions[backend]["ref"],
            "receipt_sha256": versions[backend]["sha256"],
            "version_matches": versions[backend]["version_matches"],
        }
        for backend in profile["executables"]
    ]
    selected_counts = {contract["primary_backend"]: len(cases), **{backend: 0 for backend in profile["executables"]}}
    record = {
        "case_count": len(cases),
        "cases": cases,
        "current_reconstruction_exact": True,
        "implementation_manifest_ref": implementation_manifest_ref,
        "implementation_manifest_sha256": pure["implementation_manifest_sha256"],
        "invocation_count": len(versions) + len(states),
        "materially_better_specialist_count": 0,
        "non_claims": PARSER_NON_CLAIMS,
        "parser_veto": _parser_veto(all_specialists),
        "phase": P02_PHASE,
        "profile_schema_version": profile["schema_version"],
        "pure_extractor_module_ref": pure["module_ref"],
        "pure_extractor_module_sha256": pure["module_sha256"],
        "result_round": PurePosixPath(round_ref).name,
        "revision": P02_REVISION,
        "schema_version": "p02r2_parser_comparison@1",
        "selected_backend_counts": selected_counts,
        "source_invocation_count": len(states),
        "version_invocation_count": len(versions),
        "version_receipts": version_bindings,
    }
    return validate_parser_comparison(record, profile=profile, contract=contract)


def validate_parser_comparison(
    value: Any,
    *,
    profile: Mapping[str, Any],
    contract: Mapping[str, Any],
) -> dict[str, Any]:
    record = _require_keys(value, PARSER_COMPARISON_KEYS, "parser comparison")
    if (
        record["schema_version"] != "p02r2_parser_comparison@1"
        or record["phase"] != P02_PHASE
        or record["revision"] != P02_REVISION
        or P02_ROUND_RE.fullmatch(_require_string(record["result_round"], "parser comparison result round")) is None
        or record["profile_schema_version"] != profile["schema_version"]
    ):
        raise EvidenceValidationError("parser comparison metadata mismatch")
    if record["case_count"] != len(profile["source_allowlist"]) or record["case_count"] != len(record["cases"]):
        raise EvidenceValidationError("parser comparison case count mismatch")
    if (
        record["version_invocation_count"] != contract["required_version_invocation_count"]
        or record["source_invocation_count"] != contract["required_source_invocation_count"]
        or record["invocation_count"] != contract["required_invocation_count"]
    ):
        raise EvidenceValidationError("parser comparison invocation counts do not close")
    if type(record["cases"]) is not list or type(record["version_receipts"]) is not list:
        raise EvidenceValidationError("parser comparison cases/version receipts are not arrays")
    for case in record["cases"]:
        _require_keys(case, PARSER_CASE_KEYS, "parser comparison case")
    specialists = [specialist for case in record["cases"] for specialist in case["specialists"]]
    if record["parser_veto"] != _parser_veto(specialists):
        raise EvidenceValidationError("parser comparison veto differs from capability reconstruction")
    for version in record["version_receipts"]:
        _require_keys(version, PARSER_VERSION_BINDING_KEYS, "parser version binding")
        _logical_ref(version["receipt_ref"], "parser version binding ref")
        _require_sha(version["receipt_sha256"], "parser version binding digest")
        _require_bool(version["version_matches"], "parser version match")
    _logical_ref(record["implementation_manifest_ref"], "parser implementation manifest ref")
    _require_sha(record["implementation_manifest_sha256"], "parser implementation manifest digest")
    _logical_ref(record["pure_extractor_module_ref"], "pure extractor module ref")
    _require_sha(record["pure_extractor_module_sha256"], "pure extractor module digest")
    _require_int(record["materially_better_specialist_count"], "materially better specialist count", nonnegative=True)
    _require_bool(record["current_reconstruction_exact"], "current parser reconstruction exact")
    _require_bool(record["parser_veto"], "parser comparison veto")
    if record["non_claims"] != PARSER_NON_CLAIMS:
        raise EvidenceValidationError("parser comparison non-claims mismatch")
    expected_counts = {contract["primary_backend"]: len(profile["source_allowlist"]), **{backend: 0 for backend in profile["executables"]}}
    if record["selected_backend_counts"] != expected_counts:
        raise EvidenceValidationError("parser comparison selected-backend counts mismatch")
    return record


def verify_parser_comparison(
    root: str | os.PathLike[str],
    ref: str,
    implementation_manifest_ref: str | None = None,
) -> dict[str, Any]:
    root_path = Path(root)
    raw = _read(root_path, ref)
    value = _strict_json(raw, "parser comparison")
    effective, _ = load_profile(root_path)
    record = validate_parser_comparison(
        value,
        profile=effective["parser_fidelity_profile"],
        contract=effective["parser_capability_contract"],
    )
    round_ref = _round_ref(record["result_round"])
    if ref != f"{round_ref}/parser/parser-comparison.json":
        raise EvidenceValidationError("parser comparison ref is not fixed and round-local")
    expected_manifest_ref = f"{round_ref}/implementation-round-sha256.txt"
    if implementation_manifest_ref is None:
        implementation_manifest_ref = record["implementation_manifest_ref"]
    if implementation_manifest_ref != expected_manifest_ref or record["implementation_manifest_ref"] != expected_manifest_ref:
        raise EvidenceValidationError("parser comparison implementation manifest ref mismatch")
    expected = build_parser_comparison(root_path, round_ref, implementation_manifest_ref)
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("parser comparison differs from independent raw-evidence reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record, "reconstruction": expected}


def parse_sha256_manifest(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("SHA-256 manifest is not strict UTF-8") from exc
    if text and not text.endswith("\n"):
        raise EvidenceValidationError("SHA-256 manifest is not LF terminated")
    records: dict[str, str] = {}
    for line in text.splitlines():
        digest, separator, ref = line.partition("  ")
        if separator != "  " or P02_SHA_RE.fullmatch(digest) is None or ref in records:
            raise EvidenceValidationError("SHA-256 manifest line is invalid")
        _logical_ref(ref, "manifest ref")
        records[ref] = digest
    if list(records) != sorted(records, key=lambda item: item.encode("utf-8")):
        raise EvidenceValidationError("SHA-256 manifest is not sorted")
    return records


def manifest_bytes(root: Path, refs: Iterable[str]) -> bytes:
    unique = sorted(set(refs), key=lambda item: item.encode("utf-8"))
    if not unique:
        raise EvidenceValidationError("manifest scope cannot be empty")
    return b"".join(f"{content_digest(_read(root, ref))}  {ref}\n".encode("utf-8") for ref in unique)


def implementation_refs(root: Path) -> list[str]:
    refs: list[str] = []
    for top_name in ("src", "tests", "scripts"):
        for path in (root / top_name).rglob("*"):
            if path.is_symlink():
                raise EvidenceValidationError(f"symlink in implementation tree: {path}")
            if path.is_file() and "__pycache__" not in path.parts and path.suffix not in {".pyc", ".pyo"}:
                refs.append(path.relative_to(root).as_posix())
    return sorted(refs, key=lambda item: item.encode("utf-8"))


def verify_manifest(root: Path, ref: str, *, require_current_bytes: bool = True) -> dict[str, str]:
    raw = _read(root, ref)
    records = parse_sha256_manifest(raw)
    if require_current_bytes:
        for item_ref, digest in records.items():
            if content_digest(_read(root, item_ref)) != digest:
                raise EvidenceValidationError(f"manifest input drifted: {item_ref}")
    return records


def reconstruct_reviewed_obligations(root: str | os.PathLike[str] = ".") -> dict[str, dict[str, Any]]:
    root_path = Path(root)
    compact, _materialized = load_profile(root_path)
    records: dict[str, dict[str, Any]] = {}
    for case_index, case in enumerate(compact["fixtures"]):
        if "source_ref" in case:
            by_label = {
                item["label"]: item
                for item in extract_label_scoped_obligations(
                    root_path / case["source_ref"],
                    source_ref=case["source_ref"],
                    corpus_version=FIXTURE_CORPUS_VERSION,
                )
            }
            for item_index, expected in enumerate(case["expected"]):
                records[f"/fixtures/{case_index}/expected/{item_index}"] = by_label[expected["label"]]
        else:
            for item_index, expected in enumerate(case["expected_lookup"]["file_scoped_obligations"]):
                records[f"/fixtures/{case_index}/expected_lookup/file_scoped_obligations/{item_index}"] = next(
                    item
                    for item in extract_label_scoped_obligations(
                        root_path / expected["source_ref"],
                        source_ref=expected["source_ref"],
                        corpus_version=FIXTURE_CORPUS_VERSION,
                    )
                    if item["label"] == expected["label"]
                )
    for item_index, expected in enumerate(compact["frozen_sources"]):
        records[f"/frozen_sources/{item_index}"] = next(
            item
            for item in extract_label_scoped_obligations(
                root_path / expected["source_ref"],
                source_ref=expected["source_ref"],
                corpus_version=FROZEN_CORPUS_VERSION,
            )
            if item["label"] == expected["label"]
        )
    return records


def verify_materialized_obligations(root: str | os.PathLike[str] = ".") -> dict[str, Any]:
    root_path = Path(root)
    compact, materialized = load_profile(root_path)
    actual = reconstruct_reviewed_obligations(root_path)
    expected = {item["oracle_path"]: item for item in materialized["obligations"]}
    if set(actual) != set(expected) or len(actual) != materialized["obligation_count"]:
        raise EvidenceValidationError("materialized/source obligation path closure mismatch")
    canonical_counts: dict[str, int] = {}
    for path, record in actual.items():
        item = expected[path]
        source = _read(root_path, record["document"]["file"])
        validate_label_scoped_obligation(record, source_bytes=source)
        if identity_payload(record) != item["identity_payload"]:
            raise EvidenceValidationError(f"materialized/source identity mismatch: {path}")
        canonical_count = len(canonical_json_bytes(identity_payload(record)))
        if (
            canonical_count != item["canonical_byte_count"]
            or record["obligation_digest"] != item["obligation_digest"]
            or record["obligation_id"] != item["obligation_id"]
        ):
            raise EvidenceValidationError(f"materialized/source derived identity mismatch: {path}")
        canonical_counts[path] = canonical_count
    ids = {item["obligation_id"] for item in actual.values()}
    if len(ids) != len(actual):
        raise EvidenceValidationError("reviewed obligation ids are not unique")
    return {
        "records": actual,
        "canonical_counts": canonical_counts,
        "obligation_count": len(actual),
        "unique_obligation_count": len(ids),
        "compact_oracle_sha256": content_digest(_read(root_path, P02_ORACLE_REF)),
        "materialized_oracle_sha256": content_digest(_read(root_path, P02_MATERIALIZED_REF)),
    }


def validate_obligation_bundle(value: Any) -> dict[str, Any]:
    record = _require_keys(value, OBLIGATION_BUNDLE_KEYS, "obligation bundle")
    if record["schema_version"] != "p02_obligation_bundle@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("obligation bundle metadata mismatch")
    if P02_ROUND_RE.fullmatch(_require_string(record["result_round"], "obligation bundle round")) is None:
        raise EvidenceValidationError("obligation bundle round mismatch")
    obligations = record["obligations"]
    if not isinstance(obligations, list) or len(obligations) != 17 or record["obligation_count"] != 17:
        raise EvidenceValidationError("obligation bundle must contain exactly 17 records")
    paths: list[str] = []
    ids: list[str] = []
    for index, item in enumerate(obligations):
        _require_keys(item, OBLIGATION_BUNDLE_ENTRY_KEYS, f"obligation bundle entry {index}")
        path = _require_string(item["oracle_path"], f"obligation bundle path {index}")
        if not path.startswith("/") or path in paths:
            raise EvidenceValidationError("obligation bundle oracle paths must be absolute unique pointers")
        validate_label_scoped_obligation(item["obligation"])
        paths.append(path)
        ids.append(item["obligation"]["obligation_id"])
    if paths != sorted(paths, key=lambda item: item.encode("utf-8")) or len(set(ids)) != 17:
        raise EvidenceValidationError("obligation bundle order or identity uniqueness mismatch")
    return record


def build_obligation_bundle(root: str | os.PathLike[str], result_round: str) -> dict[str, Any]:
    if P02_ROUND_RE.fullmatch(result_round) is None:
        raise EvidenceValidationError("invalid obligation-bundle result round")
    verified = verify_materialized_obligations(root)
    record = {
        "schema_version": "p02_obligation_bundle@1",
        "phase": P02_PHASE,
        "result_round": result_round,
        "obligation_count": verified["obligation_count"],
        "obligations": [
            {"oracle_path": path, "obligation": obligation}
            for path, obligation in sorted(verified["records"].items(), key=lambda item: item[0].encode("utf-8"))
        ],
    }
    return validate_obligation_bundle(record)


def verify_obligation_bundle(root: str | os.PathLike[str], ref: str) -> dict[str, Any]:
    root_path = Path(root)
    raw = _read(root_path, ref)
    record = validate_obligation_bundle(_strict_json(raw, "obligation bundle"))
    round_ref = _round_ref(record["result_round"])
    if ref != extraction_artifact_refs(round_ref)["obligations"]:
        raise EvidenceValidationError("obligation bundle ref is not fixed and round-local")
    expected = build_obligation_bundle(root_path, record["result_round"])
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("obligation bundle differs from independent source reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record}


def validate_reconstruction_summary(value: Any, *, profile: dict[str, Any] | None = None) -> dict[str, Any]:
    record = _require_keys(value, RECONSTRUCTION_SUMMARY_KEYS, "extraction reconstruction summary")
    if record["schema_version"] != "p02_extraction_reconstruction_summary@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("extraction summary metadata mismatch")
    if P02_ROUND_RE.fullmatch(_require_string(record["result_round"], "extraction summary round")) is None:
        raise EvidenceValidationError("extraction summary round mismatch")
    for key in ("compact_oracle_sha256", "materialized_oracle_sha256"):
        _require_sha(record[key], f"extraction summary {key}")
    for key in ("obligation_count", "unique_obligation_count", "backend_request_count", "source_edit_count"):
        _require_int(record[key], f"extraction summary {key}", nonnegative=True)
    if record["obligation_count"] != 17 or record["unique_obligation_count"] != 17:
        raise EvidenceValidationError("extraction summary obligation counts mismatch")
    for key in ("all_materialized_records_exact", "all_source_reconstructions_exact"):
        if _require_bool(record[key], f"extraction summary {key}") is not True:
            raise EvidenceValidationError("extraction summary reconstruction did not pass")
    for key, expected_count in (("source_digests", 13), ("obligation_digests", 17), ("frozen_positive_obligation_digests", 4)):
        mapping = record[key]
        if type(mapping) is not dict or len(mapping) != expected_count:
            raise EvidenceValidationError(f"extraction summary {key} count mismatch")
        for ref, digest in mapping.items():
            _require_string(ref, f"extraction summary {key} ref")
            _require_sha(digest, f"extraction summary {key} digest")
    if record["backend_request_count"] != 0 or record["source_edit_count"] != 0:
        raise EvidenceValidationError("extraction summary records forbidden work")
    profile = profile or governance_profile()
    if record["publication_mode"] != "disabled" or record["non_claims"] != profile["round_close_schema"]["non_claims"]:
        raise EvidenceValidationError("extraction summary boundary mismatch")
    return record


def build_reconstruction_summary(root: str | os.PathLike[str], result_round: str) -> dict[str, Any]:
    root_path = Path(root)
    compact, _ = load_profile(root_path)
    verified = verify_materialized_obligations(root_path)
    records = verified["records"]
    source_refs = compact["parser_fidelity_profile"]["source_allowlist"]
    frozen_by_label = {item["label"]: item for item in compact["frozen_sources"]}
    record = {
        "schema_version": "p02_extraction_reconstruction_summary@1",
        "phase": P02_PHASE,
        "result_round": result_round,
        "compact_oracle_sha256": verified["compact_oracle_sha256"],
        "materialized_oracle_sha256": verified["materialized_oracle_sha256"],
        "obligation_count": verified["obligation_count"],
        "unique_obligation_count": verified["unique_obligation_count"],
        "all_materialized_records_exact": True,
        "all_source_reconstructions_exact": True,
        "source_digests": {ref: content_digest(_read(root_path, ref)) for ref in source_refs},
        "obligation_digests": {path: item["obligation_digest"] for path, item in records.items()},
        "frozen_positive_obligation_digests": {
            label: frozen_by_label[label]["expected_obligation_digest"]
            for label in sorted(frozen_by_label, key=lambda item: item.encode("utf-8"))
        },
        "backend_request_count": 0,
        "source_edit_count": 0,
        "publication_mode": "disabled",
        "non_claims": governance_profile(root_path)["round_close_schema"]["non_claims"],
    }
    return validate_reconstruction_summary(record, profile=governance_profile(root_path))


def verify_reconstruction_summary(root: str | os.PathLike[str], ref: str) -> dict[str, Any]:
    root_path = Path(root)
    raw = _read(root_path, ref)
    profile = governance_profile(root_path)
    record = validate_reconstruction_summary(
        _strict_json(raw, "extraction reconstruction summary"), profile=profile
    )
    round_ref = _round_ref(record["result_round"])
    if ref != extraction_artifact_refs(round_ref)["reconstruction_summary"]:
        raise EvidenceValidationError("reconstruction summary ref is not fixed and round-local")
    expected = build_reconstruction_summary(root_path, record["result_round"])
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("reconstruction summary differs from independent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record}


def _json_pointer(root: Any, pointer: str) -> tuple[Any, str | int]:
    if not pointer.startswith("/"):
        raise EvidenceValidationError("mutation pointer is not RFC 6901 absolute")
    parts = [part.replace("~1", "/").replace("~0", "~") for part in pointer[1:].split("/")]
    parent = root
    for raw in parts[:-1]:
        key: str | int = int(raw) if isinstance(parent, list) else raw
        parent = parent[key]
    final: str | int = int(parts[-1]) if isinstance(parent, list) else parts[-1]
    return parent, final


def _mutated(value: Any) -> Any:
    if value is None:
        return "#p02-identity-mutation"
    if type(value) is bool:
        return not value
    if type(value) is int:
        return value + 1
    if isinstance(value, str):
        return value + "#p02-identity-mutation"
    if isinstance(value, list):
        return [*value, "#p02-identity-mutation"]
    if isinstance(value, dict):
        return {**value, "#p02-identity-mutation": True}
    raise EvidenceValidationError("unsupported mutation value type")


def _project_identity_from_envelope(
    identity: Mapping[str, Any],
    envelope: Mapping[str, Any],
    excluded_keys: Sequence[str],
) -> dict[str, Any]:
    if type(identity) is not dict or type(envelope) is not dict:
        raise EvidenceValidationError("identity/envelope projection requires objects")
    if set(identity) & set(envelope):
        raise EvidenceValidationError("non-identity envelope collides with an identity field")
    if set(envelope) != set(excluded_keys) or len(excluded_keys) != len(set(excluded_keys)):
        raise EvidenceValidationError("non-identity envelope does not equal the reviewed exclusion registry")
    combined = {**deepcopy(identity), **deepcopy(envelope)}
    return {key: value for key, value in combined.items() if key not in excluded_keys}


def build_mutation_matrix(root: str | os.PathLike[str], result_round: str) -> dict[str, Any]:
    root_path = Path(root)
    compact, _ = load_profile(root_path)
    verified = verify_materialized_obligations(root_path)
    golden = compact["golden_identity_vector"]
    original = golden["identity_payload"]
    original_digest = content_digest(original)
    if len(canonical_json_bytes(original)) != golden["canonical_byte_count"] or original_digest != golden["obligation_digest"]:
        raise EvidenceValidationError("golden identity vector mismatch")
    changed = 0
    for pointer in golden["mutations_that_must_change_digest"]:
        candidate = deepcopy(original)
        parent, key = _json_pointer(candidate, pointer)
        parent[key] = _mutated(parent[key])
        if content_digest(candidate) == original_digest:
            raise EvidenceValidationError(f"identity mutation did not change digest: {pointer}")
        changed += 1
    unchanged = 0
    envelope = golden["non_identity_test_envelope"]
    excluded_keys = golden["exclude_from_identity_payload"]
    if _project_identity_from_envelope(original, envelope, excluded_keys) != original:
        raise EvidenceValidationError("golden non-identity envelope changes the identity projection")
    for pointer in golden["mutations_that_must_not_change_digest"]:
        candidate = deepcopy(envelope)
        parent, key = _json_pointer(candidate, pointer)
        parent[key] = _mutated(parent[key])
        projected = _project_identity_from_envelope(original, candidate, excluded_keys)
        if projected != original or content_digest(projected) != original_digest:
            raise EvidenceValidationError(f"non-identity mutation changed identity digest: {pointer}")
        unchanged += 1
    ambiguity_count = sum(1 for item in verified["records"].values() if item["extraction_state"] != "valid_complete")
    record = {
        "schema_version": "p02_mutation_ambiguity_matrix@1",
        "phase": P02_PHASE,
        "result_round": result_round,
        "golden_canonical_byte_count": len(canonical_json_bytes(original)),
        "golden_digest": original_digest,
        "must_change_count": len(golden["mutations_that_must_change_digest"]),
        "must_change_pass_count": changed,
        "must_not_change_count": len(golden["mutations_that_must_not_change_digest"]),
        "must_not_change_pass_count": unchanged,
        "materialized_obligation_count": verified["obligation_count"],
        "unique_obligation_count": verified["unique_obligation_count"],
        "ambiguity_case_count": ambiguity_count,
        "all_pass": True,
    }
    return validate_mutation_matrix(record)


def validate_mutation_matrix(value: Any) -> dict[str, Any]:
    record = _require_keys(value, MUTATION_KEYS, "mutation matrix")
    if record["schema_version"] != "p02_mutation_ambiguity_matrix@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("mutation matrix metadata mismatch")
    if P02_ROUND_RE.fullmatch(record["result_round"]) is None:
        raise EvidenceValidationError("mutation matrix result round mismatch")
    for key in MUTATION_KEYS - {"schema_version", "phase", "result_round", "golden_digest", "all_pass"}:
        _require_int(record[key], f"mutation matrix {key}", nonnegative=True)
    _require_sha(record["golden_digest"], "mutation matrix golden digest")
    if _require_bool(record["all_pass"], "mutation matrix all_pass") is not True:
        raise EvidenceValidationError("mutation matrix did not pass")
    if (
        record["must_change_count"] != record["must_change_pass_count"]
        or record["must_not_change_count"] != record["must_not_change_pass_count"]
        or record["materialized_obligation_count"] != record["unique_obligation_count"]
    ):
        raise EvidenceValidationError("mutation matrix counts do not close")
    return record


def verify_mutation_matrix(root: str | os.PathLike[str], ref: str) -> dict[str, Any]:
    root_path = Path(root)
    raw = _read(root_path, ref)
    record = validate_mutation_matrix(_strict_json(raw, "mutation ambiguity matrix"))
    round_ref = _round_ref(record["result_round"])
    if ref != extraction_artifact_refs(round_ref)["mutation_matrix"]:
        raise EvidenceValidationError("mutation matrix ref is not fixed and round-local")
    expected = build_mutation_matrix(root_path, record["result_round"])
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("mutation matrix differs from independent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record}


def validate_bundle_index(value: Any, *, profile: dict[str, Any] | None = None) -> dict[str, Any]:
    record = _require_keys(value, BUNDLE_INDEX_KEYS, "extraction bundle index")
    if record["schema_version"] != "p02_extraction_bundle_index@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("extraction bundle metadata mismatch")
    if P02_ROUND_RE.fullmatch(record["result_round"]) is None:
        raise EvidenceValidationError("extraction bundle result round mismatch")
    inventory = record["artifact_inventory"]
    if not isinstance(inventory, list) or not inventory:
        raise EvidenceValidationError("extraction bundle inventory is empty")
    refs: list[str] = []
    for index, item in enumerate(inventory):
        _require_keys(item, BUNDLE_ARTIFACT_KEYS, f"bundle artifact {index}")
        refs.append(_logical_ref(item["logical_ref"], "bundle artifact ref"))
        _require_sha(item["sha256"], "bundle artifact sha256")
        _require_int(item["byte_count"], "bundle artifact byte count", nonnegative=True)
        _require_string(item["role"], "bundle artifact role")
    if refs != sorted(set(refs), key=lambda item: item.encode("utf-8")):
        raise EvidenceValidationError("bundle inventory refs are not sorted unique")
    for key in ("obligation_count", "unique_obligation_count", "backend_request_count", "source_edit_count"):
        _require_int(record[key], key, nonnegative=True)
    if record["obligation_count"] != 17 or record["unique_obligation_count"] != 17:
        raise EvidenceValidationError("extraction bundle does not contain 17 unique obligations")
    _require_sha(record["semantic_digest"], "bundle semantic digest")
    if record["publication_mode"] != "disabled" or _require_bool(
        record["all_source_reconstructions_exact"], "bundle source reconstruction"
    ) is not True:
        raise EvidenceValidationError("extraction bundle boundary mismatch")
    if record["backend_request_count"] != 0 or record["source_edit_count"] != 0:
        raise EvidenceValidationError("extraction bundle records forbidden work")
    profile = profile or governance_profile()
    if record["non_claims"] != profile["round_close_schema"]["non_claims"]:
        raise EvidenceValidationError("extraction bundle non-claims mismatch")
    return record


def validate_backend_ledger_index(value: Any) -> dict[str, Any]:
    record = _require_keys(value, LEDGER_INDEX_KEYS, "backend ledger index")
    if record["schema_version"] != "p02_backend_ledger_index@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("backend ledger-index metadata mismatch")
    if P02_ROUND_RE.fullmatch(_require_string(record["result_round"], "backend ledger-index round")) is None:
        raise EvidenceValidationError("backend ledger-index round mismatch")
    ledgers = record["ledgers"]
    attestations = record["attestations"]
    if not isinstance(ledgers, list) or not isinstance(attestations, list):
        raise EvidenceValidationError("backend ledger index inventories must be arrays")
    if len(ledgers) != len(P02_GUARDED_ACTIONS) or len(attestations) != len(P02_GUARDED_ACTIONS):
        raise EvidenceValidationError("backend ledger index action coverage mismatch")
    ledger_actions: list[str] = []
    total_attempts = 0
    for index, item in enumerate(ledgers):
        _require_keys(item, GUARD_LEDGER_ENTRY_KEYS, f"backend ledger {index}")
        action = _require_string(item["action"], f"backend ledger {index} action")
        ledger_actions.append(action)
        _logical_ref(item["ledger_ref"], f"backend ledger {index} ref")
        _require_sha(item["ledger_sha256"], f"backend ledger {index} digest")
        _require_int(item["ledger_byte_count"], f"backend ledger {index} byte count", nonnegative=True)
        total_attempts += _require_int(
            item["forbidden_attempt_count"], f"backend ledger {index} forbidden attempts", nonnegative=True
        )
    attestation_actions: list[str] = []
    for index, item in enumerate(attestations):
        _require_keys(item, LEDGER_INDEX_ATTESTATION_KEYS, f"backend guard attestation {index}")
        if item["schema_version"] != "p02_backend_guard_attestation@1":
            raise EvidenceValidationError("backend guard attestation schema mismatch")
        action = _require_string(item["action"], f"backend attestation {index} action")
        attestation_actions.append(action)
        _logical_ref(item["ledger_ref"], f"backend attestation {index} ledger ref")
        _require_sha(item["ledger_sha256"], f"backend attestation {index} ledger digest")
        _logical_ref(item["attestation_ref"], f"backend attestation {index} ref")
        _require_sha(item["attestation_sha256"], f"backend attestation {index} digest")
        attempts = _require_int(
            item["forbidden_attempt_count"], f"backend attestation {index} forbidden attempts", nonnegative=True
        )
        if attempts != 0 or item["guard_replacement_errors"] != []:
            raise EvidenceValidationError("backend guard attestation is not clean")
        if _require_bool(item["parser_exception_enabled"], f"backend attestation {index} parser exception") != (
            action == "parser_fidelity_tests"
        ):
            raise EvidenceValidationError("backend guard parser exception boundary mismatch")
        if P02_UTC_RE.fullmatch(_require_string(item["closed_at_utc"], f"backend attestation {index} close time")) is None:
            raise EvidenceValidationError("backend guard attestation close time mismatch")
    if ledger_actions != list(P02_GUARDED_ACTIONS) or attestation_actions != list(P02_GUARDED_ACTIONS):
        raise EvidenceValidationError("backend ledger index actions are not exact and ordered")
    if record["forbidden_attempt_count"] != total_attempts or total_attempts != 0:
        raise EvidenceValidationError("backend ledger index forbidden-attempt total mismatch")
    if _require_bool(record["all_guards_intact"], "backend ledger all_guards_intact") is not True:
        raise EvidenceValidationError("backend ledger guard integrity failed")
    return record


def build_backend_ledger_index(root: str | os.PathLike[str], round_ref: str) -> dict[str, Any]:
    root_path = Path(root)
    result_round = PurePosixPath(round_ref).name
    if round_ref != _round_ref(result_round):
        raise EvidenceValidationError("backend ledger index round root mismatch")
    ledgers: list[dict[str, Any]] = []
    attestations: list[dict[str, Any]] = []
    for action in P02_GUARDED_ACTIONS:
        ledger_ref = f"{round_ref}/ledgers/backend-invocations-{action}.jsonl"
        ledger_raw = _read(root_path, ledger_ref)
        lines = [line for line in ledger_raw.splitlines() if line]
        ledger = {
            "action": action,
            "ledger_ref": ledger_ref,
            "ledger_sha256": content_digest(ledger_raw),
            "ledger_byte_count": len(ledger_raw),
            "forbidden_attempt_count": len(lines),
        }
        attestation_ref = f"{round_ref}/ledgers/backend-guard-attestation-{action}.json"
        attestation_raw = _read(root_path, attestation_ref)
        attestation = _strict_json(attestation_raw, f"backend guard attestation {action}")
        if (
            attestation.get("action") != action
            or attestation.get("ledger_ref") != ledger_ref
            or attestation.get("ledger_sha256") != ledger["ledger_sha256"]
            or attestation.get("forbidden_attempt_count") != ledger["forbidden_attempt_count"]
        ):
            raise EvidenceValidationError(f"backend guard attestation binding mismatch: {action}")
        ledgers.append(ledger)
        attestations.append(
            {
                **attestation,
                "attestation_ref": attestation_ref,
                "attestation_sha256": content_digest(attestation_raw),
            }
        )
    record = {
        "schema_version": "p02_backend_ledger_index@1",
        "phase": P02_PHASE,
        "result_round": result_round,
        "ledgers": ledgers,
        "attestations": attestations,
        "forbidden_attempt_count": sum(item["forbidden_attempt_count"] for item in ledgers),
        "all_guards_intact": all(
            not item["guard_replacement_errors"] and item["forbidden_attempt_count"] == 0
            for item in attestations
        ),
    }
    return validate_backend_ledger_index(record)


def verify_backend_ledger_index(root: str | os.PathLike[str], ref: str) -> dict[str, Any]:
    root_path = Path(root)
    raw = _read(root_path, ref)
    record = validate_backend_ledger_index(_strict_json(raw, "backend ledger index"))
    round_ref = _round_ref(record["result_round"])
    expected = build_backend_ledger_index(root_path, round_ref)
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("backend ledger index differs from independent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record}


def verify_bundle_index(root: str | os.PathLike[str], ref: str) -> dict[str, Any]:
    root_path = Path(root)
    raw = _read(root_path, ref)
    profile = governance_profile(root_path)
    record = validate_bundle_index(_strict_json(raw, "extraction bundle index"), profile=profile)
    round_ref = _round_ref(record["result_round"])
    refs = extraction_artifact_refs(round_ref)
    if ref != refs["bundle_index"]:
        raise EvidenceValidationError("bundle index ref is not fixed and round-local")
    verify_obligation_bundle(root_path, refs["obligations"])
    verify_reconstruction_summary(root_path, refs["reconstruction_summary"])
    verify_parser_comparison(root_path, refs["parser_comparison"])
    verify_mutation_matrix(root_path, refs["mutation_matrix"])
    verify_backend_ledger_index(root_path, refs["backend_ledger_index"])
    expected_roles = {refs[key]: role for key, role in PARSER_BUNDLE_ROLES.items()}
    expected = build_bundle_index(root_path, round_ref, artifact_roles=expected_roles)
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("bundle index differs from independent constituent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record}


def build_bundle_index(
    root: str | os.PathLike[str],
    round_ref: str,
    *,
    artifact_roles: Mapping[str, str],
) -> dict[str, Any]:
    root_path = Path(root)
    refs = extraction_artifact_refs(round_ref)
    expected_refs = {
        refs["obligations"],
        refs["reconstruction_summary"],
        refs["parser_comparison"],
        refs["mutation_matrix"],
        refs["backend_ledger_index"],
    }
    if set(artifact_roles) != expected_refs:
        raise EvidenceValidationError("bundle artifact roles do not cover the exact P02 extraction artifacts")
    expected_roles = {refs[key]: role for key, role in PARSER_BUNDLE_ROLES.items()}
    if dict(artifact_roles) != expected_roles:
        raise EvidenceValidationError("bundle artifact roles differ from the closed P02 role registry")
    inventory = []
    for ref in sorted(expected_refs, key=lambda item: item.encode("utf-8")):
        raw = _read(root_path, ref)
        inventory.append(
            {"logical_ref": ref, "sha256": content_digest(raw), "byte_count": len(raw), "role": artifact_roles[ref]}
        )
    semantic_digest = content_digest(
        [{key: item[key] for key in ("logical_ref", "sha256", "byte_count", "role")} for item in inventory]
    )
    record = {
        "schema_version": "p02_extraction_bundle_index@1",
        "phase": P02_PHASE,
        "result_round": PurePosixPath(round_ref).name,
        "artifact_inventory": inventory,
        "obligation_count": 17,
        "unique_obligation_count": 17,
        "semantic_digest": semantic_digest,
        "backend_request_count": 0,
        "source_edit_count": 0,
        "publication_mode": "disabled",
        "all_source_reconstructions_exact": True,
        "non_claims": governance_profile(root_path)["round_close_schema"]["non_claims"],
    }
    return validate_bundle_index(record, profile=governance_profile(root_path))


def validate_command_receipt(value: Any, *, profile: dict[str, Any] | None = None) -> dict[str, Any]:
    record = _require_keys(value, RECEIPT_KEYS, "P02 receipt")
    if record["schema_version"] != "p02_command_receipt@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("P02 receipt metadata mismatch")
    result_round = record["result_round"]
    if P02_ROUND_RE.fullmatch(result_round) is None:
        raise EvidenceValidationError("P02 receipt result round mismatch")
    sequence = _require_int(record["sequence"], "P02 receipt sequence")
    if sequence < 1:
        raise EvidenceValidationError("P02 receipt sequence must be positive")
    action = _require_string(record["check_id"], "P02 receipt check id")
    profile = profile or governance_profile()
    if action not in profile["actions"]:
        raise EvidenceValidationError("P02 receipt action is not registered")
    action_profile = profile["actions"][action]
    if record["execution_class"] != action_profile["execution_class"]:
        raise EvidenceValidationError("P02 receipt execution class mismatch")
    round_ref = _round_ref(result_round)
    expected_artifact_ref = None
    if action_profile["artifact_ref_template"] is not None:
        expected_artifact_ref = action_profile["artifact_ref_template"].replace("RESULT_ROUND", result_round)
    if record["external_argv"] != external_argv(round_ref, action, artifact_ref=expected_artifact_ref):
        raise EvidenceValidationError("P02 receipt external argv mismatch")
    if record["execution_class"] == "governance_native":
        if record["handler_id"] != action_profile["handler_id"] or record["child_argv"] is not None or record["child_environment_sha256"] is not None:
            raise EvidenceValidationError("P02 native receipt nullability/handler mismatch")
    elif record["execution_class"] == "subprocess":
        if record["handler_id"] is not None or not isinstance(record["child_argv"], list) or record["child_environment_sha256"] is None:
            raise EvidenceValidationError("P02 subprocess receipt nullability mismatch")
        _require_sha(record["child_environment_sha256"], "child environment digest")
        if record["child_argv"] != child_argv(round_ref, action):
            raise EvidenceValidationError("P02 receipt child argv mismatch")
        if record["child_environment_sha256"] != content_digest(child_environment(round_ref, action)):
            raise EvidenceValidationError("P02 receipt child environment mismatch")
        if record["child_argv"] == record["external_argv"]:
            raise EvidenceValidationError("P02 child argv must differ from external argv")
    else:
        raise EvidenceValidationError("unknown P02 receipt execution class")
    if not isinstance(record["external_argv"], list) or not all(isinstance(item, str) for item in record["external_argv"]):
        raise EvidenceValidationError("P02 receipt external argv is invalid")
    for key in ("started_at_utc", "ended_at_utc"):
        if P02_UTC_RE.fullmatch(_require_string(record[key], key)) is None:
            raise EvidenceValidationError("P02 receipt time is invalid")
    _require_int(record["wall_time_ns"], "wall_time_ns", nonnegative=True)
    _require_int(record["exit_code"], "exit_code")
    for stream in ("stdout", "stderr"):
        ref = _logical_ref(record[f"{stream}_ref"], f"{stream}_ref")
        if not ref.startswith(f"{round_ref}/logs/"):
            raise EvidenceValidationError("P02 receipt log is not round-local")
        _require_sha(record[f"{stream}_sha256"], f"{stream}_sha256")
        _require_int(record[f"{stream}_byte_count"], f"{stream}_byte_count", nonnegative=True)
    if record["prior_receipt_sha256"] is not None:
        _require_sha(record["prior_receipt_sha256"], "prior receipt sha256")
    expected_binding_keys = profile["receipt_binding_keys"][action]
    if type(record["bindings"]) is not dict or set(record["bindings"]) != set(expected_binding_keys):
        raise EvidenceValidationError("P02 receipt bindings differ from action profile")
    if record["exit_code"] != 0 and any(value is not None for value in record["bindings"].values()):
        raise EvidenceValidationError("failed P02 action must have null bindings")
    if record["exit_code"] == 0:
        nullable: frozenset[str] = frozenset()
        if action == "init_round":
            predecessor_values = [record["bindings"][key] for key in INIT_PREDECESSOR_BINDING_KEYS]
            if result_round == "rr01":
                if any(value is not None for value in predecessor_values):
                    raise EvidenceValidationError("rr01 initializer has a predecessor binding")
                nullable = INIT_PREDECESSOR_BINDING_KEYS
            elif any(value is None for value in predecessor_values):
                raise EvidenceValidationError("successor initializer has a null predecessor binding")
        if any(
            value is None
            for key, value in record["bindings"].items()
            if key not in nullable
        ):
            raise EvidenceValidationError("successful P02 action has null binding")
    return record


def validate_receipt_index(value: Any) -> dict[str, Any]:
    record = _require_keys(value, RECEIPT_INDEX_KEYS, "P02 receipt index")
    if record["schema_version"] != "p02_receipt_index@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("P02 receipt-index metadata mismatch")
    if P02_ROUND_RE.fullmatch(record["result_round"]) is None:
        raise EvidenceValidationError("P02 receipt-index result round mismatch")
    entries = record["receipts"]
    if not isinstance(entries, list) or not entries:
        raise EvidenceValidationError("P02 receipt-index entries are empty")
    seen: set[str] = set()
    for expected_sequence, entry in enumerate(entries, start=1):
        _require_keys(entry, RECEIPT_INDEX_ENTRY_KEYS, "P02 receipt-index entry")
        if entry["sequence"] != expected_sequence:
            raise EvidenceValidationError("P02 receipt-index sequence is not contiguous")
        action = _require_string(entry["check_id"], "receipt-index check id")
        if action in seen:
            raise EvidenceValidationError("P02 receipt-index repeats an action")
        seen.add(action)
        _logical_ref(entry["receipt_ref"], "receipt-index receipt ref")
        _require_sha(entry["receipt_sha256"], "receipt-index receipt sha256")
    if record["head_sequence"] != len(entries) or record["head_sha256"] != entries[-1]["receipt_sha256"]:
        raise EvidenceValidationError("P02 receipt-index head mismatch")
    return record


def verify_receipt_index(root: str | os.PathLike[str], index_ref: str) -> dict[str, Any]:
    root_path = Path(root)
    raw = _read(root_path, index_ref)
    index = validate_receipt_index(_strict_json(raw, "P02 receipt index"))
    profile = governance_profile(root_path)
    prior: str | None = None
    receipts: list[dict[str, Any]] = []
    round_ref = _round_ref(index["result_round"])
    if PurePosixPath(index_ref).parent.as_posix() != f"{round_ref}/receipts":
        raise EvidenceValidationError("P02 receipt-index path is not round-local")
    for entry in index["receipts"]:
        receipt_raw = _read(root_path, entry["receipt_ref"])
        digest = content_digest(receipt_raw)
        if digest != entry["receipt_sha256"]:
            raise EvidenceValidationError("P02 receipt digest mismatch")
        receipt = validate_command_receipt(_strict_json(receipt_raw, "P02 receipt"), profile=profile)
        if (
            receipt["sequence"] != entry["sequence"]
            or receipt["check_id"] != entry["check_id"]
            or receipt["result_round"] != index["result_round"]
            or receipt["prior_receipt_sha256"] != prior
        ):
            raise EvidenceValidationError("P02 receipt/index chain mismatch")
        for stream in ("stdout", "stderr"):
            stream_raw = _read(root_path, receipt[f"{stream}_ref"])
            if len(stream_raw) != receipt[f"{stream}_byte_count"] or content_digest(stream_raw) != receipt[f"{stream}_sha256"]:
                raise EvidenceValidationError("P02 receipt stream digest/count mismatch")
        receipts.append({"entry": entry, "record": receipt, "sha256": digest})
        prior = digest
    return {"index_ref": index_ref, "index_sha256": content_digest(raw), "record": index, "receipts": receipts}


def latest_receipt_index(root: str | os.PathLike[str], round_ref: str) -> dict[str, Any] | None:
    root_path = Path(root)
    directory = root_path / round_ref / "receipts"
    if not directory.exists():
        return None
    if directory.is_symlink() or not directory.is_dir():
        raise EvidenceValidationError("P02 receipt directory is unsafe")
    numbered: list[tuple[int, Path]] = []
    for item in directory.glob("receipt-index-*.json"):
        match = re.fullmatch(r"receipt-index-([0-9]{2})\.json", item.name)
        if match is None:
            raise EvidenceValidationError("P02 receipt-index filename is not canonical")
        sequence = int(match.group(1))
        if sequence < 1 or item.name != f"receipt-index-{sequence:02d}.json":
            raise EvidenceValidationError("P02 receipt-index filename has a noncanonical sequence")
        numbered.append((sequence, item))
    numbered.sort(key=lambda item: item[0])
    if len({sequence for sequence, _item in numbered}) != len(numbered):
        raise EvidenceValidationError("P02 receipt-index filenames repeat a numeric sequence")
    candidates = [item for _sequence, item in numbered]
    if not candidates:
        return None
    verified = [verify_receipt_index(root_path, item.relative_to(root_path).as_posix()) for item in candidates]
    for sequence, item in enumerate(verified, start=1):
        if item["record"]["head_sequence"] != sequence:
            raise EvidenceValidationError("P02 receipt-index snapshots are not contiguous")
        if item["record"]["receipts"] != verified[-1]["record"]["receipts"][:sequence]:
            raise EvidenceValidationError("P02 receipt-index snapshot is not a terminal prefix")
    return verified[-1]


def external_argv(round_ref: str, action: str, *, artifact_ref: str | None = None) -> list[str]:
    profile = governance_profile()
    operation = profile["actions"][action]["external_operation"]
    template = profile["external_argv_templates"][operation]
    result = [item.replace("RR", round_ref).replace("ACTION", action) for item in template]
    if artifact_ref is not None:
        result = [item.replace("ARTIFACT_REF", artifact_ref) for item in result]
    return result


def child_environment(round_ref: str, action: str) -> dict[str, str]:
    template = governance_profile()["child_environment"]["template"]
    return {key: value.replace("RR", round_ref).replace("ACTION", action) for key, value in template.items()}


def child_argv(round_ref: str, action: str) -> list[str] | None:
    template = governance_profile()["actions"][action]["child_argv_template"]
    return None if template is None else [item.replace("RR", round_ref) for item in template]


def expected_next_action(
    chain: Mapping[str, Any] | None,
    *,
    stable_path_exists: bool = False,
) -> str:
    if chain is None:
        raise EvidenceValidationError("P02 round has no init receipt")
    receipts = chain["receipts"]
    if not receipts or receipts[0]["record"]["check_id"] != "init_round":
        raise EvidenceValidationError("P02 round does not start with init_round")
    profile = governance_profile()
    actions = [item["record"]["check_id"] for item in receipts]
    exits = [item["record"]["exit_code"] for item in receipts]
    latest = receipts[-1]["record"]
    latest_action = latest["check_id"]
    latest_exit = latest["exit_code"]

    # These outcomes have precedence over the earlier failure that led to them.
    if latest_action == "close_round":
        if latest_exit == 0:
            raise EvidenceValidationError("P02 result round is terminal")
        raise EvidenceValidationError("failed close_round requires human recovery")
    if latest_action == "bind_scoped_repair":
        if latest_exit == 0:
            return "close_round"
        raise EvidenceValidationError("failed bind_scoped_repair requires human recovery")
    if latest_action == "stable_publication":
        if stable_path_exists:
            raise EvidenceValidationError("post-link publication failure requires human recovery")
        if latest_exit == 0:
            if latest["bindings"].get("same_inode") is not True or latest["bindings"].get("same_digest") is not True:
                raise EvidenceValidationError("successful stable publication lacks link equality")
            raise EvidenceValidationError("P02 result round is terminal")
        return "bind_scoped_repair"

    failed = [action for action, code in zip(actions, exits, strict=True) if code != 0]
    local_checks = profile["failure_state_machine"]["local_check_action_ids"]
    if failed:
        first_failed = failed[0]
        if first_failed in local_checks:
            if "bind_result" not in actions:
                return "bind_result"
            bind = next(item["record"] for item in receipts if item["record"]["check_id"] == "bind_result")
            if bind["exit_code"] != 0 or "build_run_manifest" in actions:
                return "bind_scoped_repair"
            return "build_run_manifest"
        return "bind_scoped_repair"
    if latest["check_id"] in {"result_review_binding", "final_seal_audit_binding"}:
        verdict_key = "review_verdict" if latest["check_id"] == "result_review_binding" else "audit_verdict"
        if latest["bindings"][verdict_key] == "REVISE":
            return "bind_scoped_repair"
    successor = profile["failure_state_machine"]["success_successor"].get(latest_action)
    if successor is None:
        raise EvidenceValidationError("P02 receipt chain has no accepted successor")
    return successor


def parse_human_result(raw: bytes, *, result_round: str, pre_result_index_sha256: str) -> str:
    if len(raw) > 262144 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError("P02 human result violates bounded byte grammar")
    try:
        lines = raw.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("P02 human result is not strict UTF-8") from exc
    profile = governance_profile()["human_result_profile"]
    for section in profile["required_sections"]:
        if lines.count(f"## {section}") != 1:
            raise EvidenceValidationError(f"P02 human result section count mismatch: {section}")
    nonempty = [line for line in lines if line]
    if len(nonempty) < 4:
        raise EvidenceValidationError("P02 human result footer is missing")
    decision_line = nonempty[-3]
    prefix = "Claimed decision: `"
    if not decision_line.startswith(prefix) or not decision_line.endswith("`"):
        raise EvidenceValidationError("P02 human result decision footer is invalid")
    decision = decision_line[len(prefix) : -1]
    expected = [
        f"Result round: `{result_round}`",
        f"Claimed decision: `{decision}`",
        f"Pre-result receipt-index SHA-256: `{pre_result_index_sha256}`",
        "Publication mode: `disabled`",
    ]
    if nonempty[-4:] != expected or decision not in profile["decision_enum"]:
        raise EvidenceValidationError("P02 human result footer mismatch")
    if any(lines.count(item) != 1 for item in expected):
        raise EvidenceValidationError("P02 human result footer line is repeated")
    return decision


def parse_review(raw: bytes, *, expected_bindings: Mapping[str, str], kind: str) -> str:
    if len(raw) > 131072 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"P02 {kind} violates bounded byte grammar")
    try:
        lines = raw.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError(f"P02 {kind} is not strict UTF-8") from exc
    for label, digest in expected_bindings.items():
        line = f"{label}: `{digest}`"
        if lines.count(line) != 1:
            raise EvidenceValidationError(f"P02 {kind} binding line mismatch: {label}")
    verdicts = [line for line in lines if line.startswith("VERDICT:")]
    nonempty = [line for line in lines if line]
    if len(verdicts) != 1 or verdicts[0] not in {"VERDICT: AGREE", "VERDICT: REVISE"} or nonempty[-1] != verdicts[0]:
        raise EvidenceValidationError(f"P02 {kind} verdict is not unique and final")
    return verdicts[0].split(": ", 1)[1]


def _validate_pass_maps(value: Mapping[str, Any], *, profile: dict[str, Any], name: str) -> None:
    primary = value["primary_criterion"]
    primary_keys = set(profile["phase_result_schema"]["primary_criterion_keys"])
    if type(primary) is not dict or set(primary) != primary_keys or len(primary) != len(primary_keys):
        raise EvidenceValidationError(f"{name} primary criterion keys mismatch")
    if any(type(item) is not bool for item in primary.values()):
        raise EvidenceValidationError(f"{name} primary criterion values are not booleans")
    if primary["all_pass"] != all(primary[key] for key in primary_keys - {"all_pass"}):
        raise EvidenceValidationError(f"{name} all_pass is not the criterion conjunction")

    veto_keys = set(profile["round_close_schema"]["veto_keys"])
    vetoes = value["vetoes"]
    if type(vetoes) is not dict or set(vetoes) != veto_keys or len(vetoes) != len(veto_keys):
        raise EvidenceValidationError(f"{name} veto keys mismatch")
    if any(type(item) is not bool for item in vetoes.values()):
        raise EvidenceValidationError(f"{name} veto values are not booleans")
    if value["non_claims"] != profile["round_close_schema"]["non_claims"]:
        raise EvidenceValidationError(f"{name} non-claims mismatch")


def validate_phase_result(value: Any, *, profile: dict[str, Any] | None = None) -> dict[str, Any]:
    profile = profile or governance_profile()
    schema = profile["phase_result_schema"]
    record = _require_keys(value, frozenset(schema["exact_keys"]), "P02 phase result")
    if record["schema_version"] != schema["schema_version"] or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("P02 phase-result metadata mismatch")
    if record["decision"] not in {
        "candidate_pass_pending_independent_result_review",
        "blocked",
    }:
        raise EvidenceValidationError("P02 phase-result decision mismatch")
    if record["publication_mode"] != "disabled" or record["claim_eligibility"] != "ineligible":
        raise EvidenceValidationError("P02 phase-result claim boundary mismatch")
    _validate_pass_maps(record, profile=profile, name="P02 phase result")
    primary = record["primary_criterion"]
    if record["decision"] == "candidate_pass_pending_independent_result_review" and (
        not primary["all_pass"] or any(record["vetoes"].values())
    ):
        raise EvidenceValidationError("P02 candidate pass contradicts criteria/vetoes")
    return record


def validate_run_manifest(
    value: Any,
    *,
    parser_profile: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    record = _require_keys(value, RUN_MANIFEST_KEYS, "P02 run manifest")
    if record["schema_version"] != "p02_extraction_run_manifest@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("P02 run-manifest metadata mismatch")
    if P02_ROUND_RE.fullmatch(record["result_round"]) is None:
        raise EvidenceValidationError("P02 run-manifest result round mismatch")
    git_commit = _require_string(record["git_commit"], "P02 run-manifest git commit")
    if P02_GIT_OID_RE.fullmatch(git_commit) is None:
        raise EvidenceValidationError("P02 run-manifest git commit must be a lower-case Git object id")
    for key in ("started_at_utc", "ended_at_utc"):
        if P02_UTC_RE.fullmatch(_require_string(record[key], key)) is None:
            raise EvidenceValidationError("P02 run-manifest time mismatch")
    _require_int(record["wall_time_ns"], "P02 run-manifest wall time", nonnegative=True)
    for key in ("environment", "device_execution", "random_seed_policy"):
        if type(record[key]) is not dict:
            raise EvidenceValidationError(f"P02 run-manifest {key} must be an object")
    if record["device_execution"].get("gpu_requested") is not False or record["device_execution"].get("gpu_initialized") is not False:
        raise EvidenceValidationError("P02 run manifest records GPU execution")
    if not isinstance(record["external_tool_considerations"], list) or not isinstance(record["artifact_inventory"], list):
        raise EvidenceValidationError("P02 run-manifest ledgers must be lists")
    inventory: dict[str, dict[str, Any]] = {}
    for item in record["artifact_inventory"]:
        if type(item) is not dict or set(item) != {"logical_ref", "sha256", "byte_count", "role"}:
            raise EvidenceValidationError("P02 run-manifest artifact inventory entry mismatch")
        ref = _logical_ref(item["logical_ref"], "P02 run-manifest artifact ref")
        if ref in inventory:
            raise EvidenceValidationError("P02 run-manifest artifact inventory repeats a ref")
        _require_sha(item["sha256"], "P02 run-manifest artifact digest")
        _require_int(item["byte_count"], "P02 run-manifest artifact byte count", nonnegative=True)
        _require_string(item["role"], "P02 run-manifest artifact role")
        inventory[ref] = item

    tools = record["external_tool_considerations"]
    if len(tools) != 4 or any(type(item) is not dict or set(item) != RUN_MANIFEST_TOOL_KEYS for item in tools):
        raise EvidenceValidationError("P02 run-manifest external-tool schema mismatch")
    by_tool = {item.get("tool"): item for item in tools}
    if len(by_tool) != 4 or set(by_tool) != {
        "current_byte_preserving_scanner",
        "LaTeXML",
        "Pandoc",
        "SymPy_Sage_Lean_and_proof_search_backends",
    }:
        raise EvidenceValidationError("P02 run-manifest external-tool registry mismatch")
    expected_static = {
        "current_byte_preserving_scanner": {
            "role": "primary exact source reconstruction",
            "availability_version_evidence": {
                "evidence_type": "embedded_version",
                "measured_version": "p02_lightweight_locator@1",
            },
            "selected": True,
            "certifying_status": "noncertifying_extraction",
        },
        "SymPy_Sage_Lean_and_proof_search_backends": {
            "role": "later semantic or mathematical checking",
            "availability_version_evidence": {
                "evidence_type": "not_invoked",
                "measured_version": None,
            },
            "selected": False,
            "certifying_status": "forbidden_by_phase02_boundary",
        },
    }
    for tool, expected in expected_static.items():
        if {key: by_tool[tool][key] for key in expected} != expected:
            raise EvidenceValidationError(f"P02 run-manifest {tool} evidence mismatch")

    parser_profile = parser_profile or load_profile()[0]["parser_fidelity_profile"]
    round_ref = _round_ref(record["result_round"])
    parser_evidence_roles = {
        "parser_fidelity_tests_receipt",
        "parser_fidelity_tests_stdout",
        "parser_fidelity_tests_stderr",
        "differential_parser_fidelity_comparison",
        "latexml_parser_version_receipt",
        "pandoc_parser_version_receipt",
    }
    observed_parser_evidence_roles = {
        item["role"] for item in inventory.values() if item["role"] in parser_evidence_roles
    }
    parser_comparison_bound = "differential_parser_fidelity_comparison" in observed_parser_evidence_roles
    if observed_parser_evidence_roles and not parser_comparison_bound:
        raise EvidenceValidationError("P02 run-manifest parser evidence is incomplete")
    for backend, tool in (("latexml", "LaTeXML"), ("pandoc", "Pandoc")):
        item = by_tool[tool]
        if (
            item["role"] != "diagnostic structural parser"
            or item["selected"] is not False
            or item["certifying_status"] != "diagnostic_only_unless_source_mappable"
        ):
            raise EvidenceValidationError(f"P02 run-manifest {tool} boundary mismatch")
        evidence = item["availability_version_evidence"]
        expected_ref = _parser_version_ref(round_ref, backend)
        if not parser_comparison_bound:
            if evidence != {
                "evidence_type": "not_measured_in_blocked_round",
                "measured_version": None,
                "version_matches": None,
                "version_receipt_ref": None,
                "version_receipt_sha256": None,
            }:
                raise EvidenceValidationError(f"P02 run-manifest {tool} blocked-round evidence mismatch")
            continue
        if (
            type(evidence) is not dict
            or set(evidence) != RUN_MANIFEST_PARSER_VERSION_EVIDENCE_KEYS
            or evidence["evidence_type"] != "measured_parser_version_receipt"
            or evidence["measured_version"] != parser_profile["executables"][backend]["measured_version"]
            or evidence["version_matches"] is not True
            or evidence["version_receipt_ref"] != expected_ref
        ):
            raise EvidenceValidationError(f"P02 run-manifest {tool} version evidence mismatch")
        digest = _require_sha(evidence["version_receipt_sha256"], f"P02 run-manifest {tool} receipt digest")
        bound = inventory.get(expected_ref)
        if bound is None or bound["sha256"] != digest or bound["role"] != f"{backend}_parser_version_receipt":
            raise EvidenceValidationError(f"P02 run-manifest {tool} version receipt is unbound")
    if not isinstance(record["non_claims"], list) or not record["non_claims"]:
        raise EvidenceValidationError("P02 run-manifest non-claims are empty")
    return record


def validate_candidate(value: Any) -> dict[str, Any]:
    record = _require_keys(value, CANDIDATE_KEYS, "P02 candidate")
    if record["schema_version"] != "p02_candidate_decision@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("P02 candidate metadata mismatch")
    if record["decision"] != "candidate_pass_pending_independent_result_review":
        raise EvidenceValidationError("P02 candidate decision mismatch")
    if record["publication_mode"] != "disabled" or record["claim_eligibility"] != "ineligible":
        raise EvidenceValidationError("P02 candidate boundary mismatch")
    if P02_ROUND_RE.fullmatch(_require_string(record["result_round"], "candidate result round")) is None:
        raise EvidenceValidationError("P02 candidate result round mismatch")
    for ref_key, digest_key in (
        ("entry_record_ref", "entry_record_sha256"),
        ("p01_stable_decision_ref", "p01_stable_decision_sha256"),
        ("p01_terminal_receipt_index_ref", "p01_terminal_receipt_index_sha256"),
        ("reviewed_plan_ref", "reviewed_plan_sha256"),
        ("reviewed_compact_oracle_ref", "reviewed_compact_oracle_sha256"),
        ("reviewed_materialized_oracle_ref", "reviewed_materialized_oracle_sha256"),
        ("implementation_entry_manifest_ref", "implementation_entry_manifest_sha256"),
        ("implementation_round_manifest_ref", "implementation_round_manifest_sha256"),
        ("protected_manifest_ref", "protected_manifest_sha256"),
        ("immutable_input_manifest_ref", "immutable_input_manifest_sha256"),
        ("run_manifest_ref", "run_manifest_sha256"),
        ("result_ref", "result_sha256"),
        ("pre_candidate_receipt_index_ref", "pre_candidate_receipt_index_sha256"),
        ("extraction_bundle_index_ref", "extraction_bundle_index_sha256"),
        ("parser_comparison_ref", "parser_comparison_sha256"),
        ("mutation_ambiguity_matrix_ref", "mutation_ambiguity_matrix_sha256"),
        ("backend_ledger_index_ref", "backend_ledger_index_sha256"),
    ):
        _logical_ref(record[ref_key], ref_key)
        _require_sha(record[digest_key], digest_key)
    _require_sha(record["extraction_bundle_semantic_digest"], "candidate bundle semantic digest")
    for key in ("backend_request_count", "source_edit_count"):
        if _require_int(record[key], f"candidate {key}", nonnegative=True) != 0:
            raise EvidenceValidationError(f"P02 candidate {key} must be zero")
    frozen = record["frozen_source_digests"]
    if type(frozen) is not dict or len(frozen) != 2:
        raise EvidenceValidationError("P02 candidate frozen-source digest map mismatch")
    for ref, digest in frozen.items():
        _logical_ref(ref, "candidate frozen-source ref")
        _require_sha(digest, "candidate frozen-source digest")
    profile = governance_profile()
    _validate_pass_maps(record, profile=profile, name="P02 candidate")
    if not record["primary_criterion"]["all_pass"] or any(record["vetoes"].values()):
        raise EvidenceValidationError("P02 candidate criteria/vetoes do not pass")
    return record


def validate_final(value: Any) -> dict[str, Any]:
    record = _require_keys(value, FINAL_KEYS, "P02 final decision")
    if record["schema_version"] != "p02_final_decision@1" or record["phase"] != P02_PHASE:
        raise EvidenceValidationError("P02 final metadata mismatch")
    if record["decision"] != "pass" or record["publication_mode"] != "disabled":
        raise EvidenceValidationError("P02 final decision/boundary mismatch")
    if P02_ROUND_RE.fullmatch(_require_string(record["result_round"], "final result round")) is None:
        raise EvidenceValidationError("P02 final result round mismatch")
    for ref_key, digest_key in (
        ("candidate_decision_ref", "candidate_decision_sha256"),
        ("result_review_ref", "result_review_sha256"),
        ("reviewed_receipt_index_ref", "reviewed_receipt_index_sha256"),
        ("p01_stable_decision_ref", "p01_stable_decision_sha256"),
    ):
        _logical_ref(record[ref_key], ref_key)
        _require_sha(record[digest_key], digest_key)
    _require_sha(record["extraction_bundle_semantic_digest"], "final bundle semantic digest")
    _validate_pass_maps(record, profile=governance_profile(), name="P02 final decision")
    if not record["primary_criterion"].get("all_pass") or any(record["vetoes"].values()):
        raise EvidenceValidationError("P02 final criteria/vetoes do not pass")
    return record


def downstream_reviewed_bindings(entry: Mapping[str, Any]) -> dict[str, str]:
    return {
        "reviewed_plan_ref": entry["recovery_plan_ref"],
        "reviewed_plan_sha256": entry["recovery_plan_sha256"],
        "reviewed_compact_oracle_ref": entry["recovery_oracle_ref"],
        "reviewed_compact_oracle_sha256": entry["recovery_oracle_sha256"],
        "reviewed_materialized_oracle_ref": entry["base_materialized_oracle_ref"],
        "reviewed_materialized_oracle_sha256": entry["base_materialized_oracle_sha256"],
    }


def _verify_entry_tree(root: Path, entry_ref: str) -> None:
    entry_root = root / PurePosixPath(entry_ref).parent
    if entry_root.is_symlink() or not entry_root.is_dir():
        raise EvidenceValidationError("P02 entry root is unsafe")
    items = list(entry_root.iterdir())
    expected = {
        "entry-record.json",
        "implementation-entry-sha256.txt",
        "protected-entry-sha256.txt",
        "immutable-input-sha256.txt",
    }
    if {item.name for item in items} != expected or any(item.is_symlink() or not item.is_file() for item in items):
        raise EvidenceValidationError("P02 entry tree differs from the sealed four-file shape")


def verify_entry(root: str | os.PathLike[str] = ".") -> dict[str, Any]:
    root_path = Path(root)
    raw = _read(root_path, P02_ENTRY_RECORD_REF)
    record = _strict_json(raw, "P02 entry record")
    recovery = load_recovery_oracle(root_path)
    schema = recovery["entry_schema"]
    _require_keys(record, frozenset(schema["exact_keys"]), "P02 entry record")
    if (
        record["schema_version"] != schema["schema_version"]
        or record["phase"] != P02_PHASE
        or record["revision"] != P02_REVISION
    ):
        raise EvidenceValidationError("P02 entry metadata mismatch")
    for key, value in record.items():
        if key.endswith("_ref"):
            _logical_ref(value, key)
        elif key.endswith("_sha256"):
            _require_sha(value, key)
    for ref_key, digest_key in (
        ("recovery_plan_ref", "recovery_plan_sha256"),
        ("recovery_oracle_ref", "recovery_oracle_sha256"),
        ("agreeing_plan_review_ref", "agreeing_plan_review_sha256"),
        ("entry_bootstrap_ref", "entry_bootstrap_sha256"),
        ("base_plan_ref", "base_plan_sha256"),
        ("base_compact_oracle_ref", "base_compact_oracle_sha256"),
        ("base_materialized_oracle_ref", "base_materialized_oracle_sha256"),
        ("prior_entry_ref", "prior_entry_sha256"),
        ("runtime_contract_review_ref", "runtime_contract_review_sha256"),
        ("pre_round_blocker_ref", "pre_round_blocker_sha256"),
        ("p01_stable_decision_ref", "p01_stable_decision_sha256"),
        ("p01_terminal_receipt_index_ref", "p01_terminal_receipt_index_sha256"),
        ("implementation_entry_manifest_ref", "implementation_entry_manifest_sha256"),
        ("protected_entry_manifest_ref", "protected_entry_manifest_sha256"),
        ("immutable_input_manifest_ref", "immutable_input_manifest_sha256"),
    ):
        if content_digest(_read(root_path, record[ref_key])) != record[digest_key]:
            raise EvidenceValidationError(f"P02 entry binding drift: {ref_key}")
    expected_refs = recovery["recovery_refs"]
    bindings = recovery["base_bindings"]
    if (
        record["recovery_plan_ref"] != expected_refs["recovery_plan_ref"]
        or record["recovery_oracle_ref"] != expected_refs["recovery_oracle_ref"]
        or record["entry_bootstrap_ref"] != expected_refs["entry_bootstrap_ref"]
        or record["base_plan_ref"] != bindings["p02r2_plan_ref"]
        or record["base_compact_oracle_ref"] != bindings["p02r2_oracle_ref"]
        or record["base_materialized_oracle_ref"] != bindings["materialized_oracle_ref"]
        or record["prior_entry_ref"] != bindings["p02r2_entry_ref"]
        or record["runtime_contract_review_ref"] != bindings["timeout_adjudication_ref"]
        or record["pre_round_blocker_ref"] != bindings["timeout_blocker_ref"]
    ):
        raise EvidenceValidationError("P02R3 entry refs differ from the recovery contract")
    _verify_entry_tree(root_path, P02_ENTRY_RECORD_REF)
    _verify_entry_tree(root_path, record["prior_entry_ref"])
    parse_sha256_manifest(_read(root_path, record["implementation_entry_manifest_ref"]))
    # The broad protected-tree snapshot is historical governance evidence. The
    # immutable manifest below remains the live gate for P02 scientific inputs.
    verify_manifest(
        root_path,
        record["protected_entry_manifest_ref"],
        require_current_bytes=False,
    )
    verify_manifest(root_path, record["immutable_input_manifest_ref"])
    prior = _strict_json(_read(root_path, record["prior_entry_ref"]), "prior P02 entry record")
    for ref_key, digest_key in (
        ("implementation_entry_manifest_ref", "implementation_entry_manifest_sha256"),
        ("protected_entry_manifest_ref", "protected_entry_manifest_sha256"),
        ("immutable_input_manifest_ref", "immutable_input_manifest_sha256"),
    ):
        if content_digest(_read(root_path, prior[ref_key])) != prior[digest_key]:
            raise EvidenceValidationError(f"prior P02 entry binding drift: {ref_key}")
    p01 = verify_p01_receipt_index(root_path, record["p01_terminal_receipt_index_ref"])
    if p01["index_sha256"] != record["p01_terminal_receipt_index_sha256"]:
        raise EvidenceValidationError("P01 terminal receipt-index binding mismatch")
    return {
        "ref": P02_ENTRY_RECORD_REF,
        "sha256": content_digest(raw),
        "record": record,
        "reviewed_bindings": downstream_reviewed_bindings(record),
    }


def fixed_ref(profile: Mapping[str, Any], key: str, result_round: str, round_ref: str) -> str:
    return profile["fixed_artifact_refs"][key].replace("RESULT_ROUND", result_round).replace("RR", round_ref)


def current_git_commit(root: Path) -> str:
    head = (root / ".git/HEAD").read_text(encoding="ascii").strip()
    if P02_GIT_OID_RE.fullmatch(head):
        return head
    if not head.startswith("ref: "):
        raise EvidenceValidationError("Git HEAD has an unsupported format")
    ref = head[5:]
    ref_path = root / ".git" / ref
    if ref_path.is_file():
        value = ref_path.read_text(encoding="ascii").strip()
        if P02_GIT_OID_RE.fullmatch(value) is None:
            raise EvidenceValidationError("Git ref is not a lower-case Git object id")
        return value
    packed = root / ".git/packed-refs"
    if packed.is_file():
        for line in packed.read_text(encoding="ascii").splitlines():
            if line and not line.startswith(("#", "^")):
                digest, name = line.split(" ", 1)
                if name == ref:
                    if P02_GIT_OID_RE.fullmatch(digest) is None:
                        raise EvidenceValidationError("packed Git ref is not a lower-case Git object id")
                    return digest
    raise EvidenceValidationError("Git HEAD ref cannot be resolved without a subprocess")
