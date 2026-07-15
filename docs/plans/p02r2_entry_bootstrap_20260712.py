from __future__ import annotations

"""Create the reviewed Phase 02R2 recovery entry snapshot exactly once."""

import json
import os
from pathlib import Path
import re
import runpy
import stat
import sys
from typing import Any, Iterable

from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
    strict_load_canonical_json,
    validate_logical_path,
    verify_receipt_index,
)


PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
BASE_BOOTSTRAP_REF = "docs/plans/p02_entry_bootstrap_20260711.py"
BOOTSTRAP_REF = "docs/plans/p02r2_entry_bootstrap_20260712.py"
RECOVERY_PLAN_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-02r2-"
    "capability-scoped-parser-recovery-subplan-2026-07-12.md"
)
RECOVERY_ORACLE_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-02r2-recovery-oracle-2026-07-12.json"
)
EVIDENCE_ROOT_REF = ".local/mathdevmcp/evidence/p02r2-20260712"
ENTRY_ROOT_REF = f"{EVIDENCE_ROOT_REF}/entry"
ENTRY_RECORD_REF = f"{ENTRY_ROOT_REF}/entry-record.json"
IMPLEMENTATION_MANIFEST_REF = f"{ENTRY_ROOT_REF}/implementation-entry-sha256.txt"
PROTECTED_MANIFEST_REF = f"{ENTRY_ROOT_REF}/protected-entry-sha256.txt"
IMMUTABLE_MANIFEST_REF = f"{ENTRY_ROOT_REF}/immutable-input-sha256.txt"
PURE_EXTRACTOR_MODULE_REF = "src/mathdevmcp/parser_capability_extractors.py"
COMPILE_PATCH_PATH = "/governance_action_profile/actions/compile/child_argv_template"
EXPECTED_ENVIRONMENT = {
    "HOME": "/tmp/mathdevmcp-p02r2-entry-home",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": "/usr/bin:/bin",
    "PYTHONHASHSEED": "0",
    "PYTHONPATH": "src",
}
REVIEW_RE = re.compile(
    r"docs/reviews/mathdevmcp-real-document-remediation-phase-02r2-"
    r"plan-review-r(11|12|13|14)-result-2026-07-12\.md"
)
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


def _read(root: Path, ref: str) -> bytes:
    validate_logical_path(ref)
    raw, info = read_bytes_no_follow(root, ref)
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError(f"artifact is not regular: {ref}")
    return raw


def _sha(root: Path, ref: str) -> str:
    return content_digest(_read(root, ref))


def _strict_reviewed_json(raw: bytes, name: str) -> dict[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"{name} violates strict JSON bytes")

    def reject_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise EvidenceValidationError(f"{name} contains duplicate key: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=reject_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"{name} is not strict JSON") from exc
    if type(value) is not dict:
        raise EvidenceValidationError(f"{name} must be an object")
    return value


def _validate_invocation(argv: list[str]) -> None:
    expected = [PYTHON, "-B", "-S", BOOTSTRAP_REF, *argv]
    if sys.orig_argv != expected:
        raise EvidenceValidationError("P02R2 entry bootstrap process argv is not exact")
    if dict(os.environ) != EXPECTED_ENVIRONMENT:
        raise EvidenceValidationError("P02R2 entry bootstrap environment is not exact")
    if sys.executable != PYTHON or not sys.flags.dont_write_bytecode or not sys.flags.no_site:
        raise EvidenceValidationError("P02R2 entry bootstrap runtime flags are not exact")


def _load_base_library(root: Path) -> dict[str, Any]:
    if _sha(root, BASE_BOOTSTRAP_REF) != "6fe84454491fe76e52daf789292ea4a44d695acb244fcdcf78838356bf2b55ec":
        raise EvidenceValidationError("frozen R9 bootstrap source drifted")
    return runpy.run_path(str(root / BASE_BOOTSTRAP_REF), run_name="p02_r9_bootstrap_library")


def _resolve_pointer(value: Any, pointer: str) -> Any:
    if not pointer.startswith("/"):
        raise EvidenceValidationError("profile patch path is not absolute")
    current = value
    for token in pointer[1:].split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        if not isinstance(current, dict) or token not in current:
            raise EvidenceValidationError(f"profile patch path does not resolve: {pointer}")
        current = current[token]
    return current


def _validate_recovery_oracle(root: Path, oracle: dict[str, Any]) -> dict[str, Any]:
    if (
        oracle.get("schema_version") != "p02r2_recovery_oracle@1"
        or oracle.get("phase") != "P02"
        or oracle.get("revision") != "P02R2"
    ):
        raise EvidenceValidationError("P02R2 recovery oracle metadata mismatch")
    bindings = oracle["base_bindings"]
    for key, value in bindings.items():
        if key.endswith("_ref"):
            validate_logical_path(value, name=key)
            digest_key = key[:-4] + "_sha256"
            if digest_key not in bindings or _sha(root, value) != bindings[digest_key]:
                raise EvidenceValidationError(f"P02R2 frozen binding mismatch: {key}")
        elif key.endswith("_sha256") and SHA_RE.fullmatch(value) is None:
            raise EvidenceValidationError(f"P02R2 frozen digest is invalid: {key}")

    refs = oracle["recovery_refs"]
    expected_refs = {
        "recovery_plan_ref": RECOVERY_PLAN_REF,
        "recovery_oracle_ref": RECOVERY_ORACLE_REF,
        "entry_bootstrap_ref": BOOTSTRAP_REF,
        "evidence_root_ref": EVIDENCE_ROOT_REF,
        "entry_root_ref": ENTRY_ROOT_REF,
        "entry_record_ref": ENTRY_RECORD_REF,
        "implementation_entry_manifest_ref": IMPLEMENTATION_MANIFEST_REF,
        "protected_entry_manifest_ref": PROTECTED_MANIFEST_REF,
        "immutable_input_manifest_ref": IMMUTABLE_MANIFEST_REF,
        "stable_decision_ref": f"{EVIDENCE_ROOT_REF}/phase-results/P02-decision.json",
    }
    if refs != expected_refs:
        raise EvidenceValidationError("P02R2 recovery refs differ from bootstrap constants")
    entry = oracle["entry_schema"]
    if entry.get("schema_version") != "p02r2_entry_record@1" or entry.get("write_order") != [
        IMPLEMENTATION_MANIFEST_REF,
        PROTECTED_MANIFEST_REF,
        IMMUTABLE_MANIFEST_REF,
        ENTRY_RECORD_REF,
    ]:
        raise EvidenceValidationError("P02R2 entry profile mismatch")
    keys = entry.get("exact_keys")
    if not isinstance(keys, list) or len(keys) != len(set(keys)) or len(keys) != 33:
        raise EvidenceValidationError("P02R2 entry key registry mismatch")
    bootstrap_profile = oracle["entry_bootstrap_profile"]
    expected_argv = [
        "/usr/bin/env",
        "-i",
        *(f"{key}={value}" for key, value in EXPECTED_ENVIRONMENT.items()),
        PYTHON,
        "-B",
        "-S",
        BOOTSTRAP_REF,
        "--agreeing-plan-review-ref",
        "AGREEING_REVIEW_REF",
    ]
    if (
        bootstrap_profile.get("source_ref") != BOOTSTRAP_REF
        or bootstrap_profile.get("python") != PYTHON
        or bootstrap_profile.get("environment") != EXPECTED_ENVIRONMENT
        or bootstrap_profile.get("external_argv_template") != expected_argv
        or bootstrap_profile.get("review_path_regex") != REVIEW_RE.pattern
        or bootstrap_profile.get("base_validator_binding")
        != {
            "ref": BASE_BOOTSTRAP_REF,
            "sha256": "6fe84454491fe76e52daf789292ea4a44d695acb244fcdcf78838356bf2b55ec",
            "permitted_reuse": [
                "strict source/environment/materialized validation",
                "implementation/source manifest construction",
                "fixed read-only git status parser",
                "manifest grammar and implementation allowlist",
            ],
        }
    ):
        raise EvidenceValidationError("P02R2 entry bootstrap profile mismatch")
    budget = oracle["review_budget"]
    if budget.get("permitted_recovery_plan_rounds") != [11, 12, 13, 14] or budget.get("forbidden_first_round") != 15:
        raise EvidenceValidationError("P02R2 review budget mismatch")
    history = budget.get("review_history")
    if not isinstance(history, list):
        raise EvidenceValidationError("P02R2 review history must be ordered")
    history_keys = {
        "round",
        "result_ref",
        "result_sha256",
        "verdict",
        "reviewed_recovery_plan_sha256",
        "reviewed_recovery_oracle_sha256",
        "reviewed_recovery_bootstrap_sha256",
        "reviewed_base_plan_sha256",
        "reviewed_base_compact_oracle_sha256",
        "reviewed_materialized_oracle_sha256",
        "reviewed_prior_entry_sha256",
    }
    if [item.get("round") for item in history if isinstance(item, dict)] != list(
        range(11, 11 + len(history))
    ):
        raise EvidenceValidationError("P02R2 review history rounds are not contiguous from R11")
    for item in history:
        if type(item) is not dict or set(item) != history_keys or item["verdict"] != "REVISE":
            raise EvidenceValidationError("P02R2 review history record mismatch")
        expected_ref = (
            "docs/reviews/mathdevmcp-real-document-remediation-phase-02r2-"
            f"plan-review-r{item['round']}-result-2026-07-12.md"
        )
        if item["result_ref"] != expected_ref or _sha(root, expected_ref) != item["result_sha256"]:
            raise EvidenceValidationError("P02R2 review history result binding mismatch")
        for key, value in item.items():
            if key.endswith("_sha256") and SHA_RE.fullmatch(value) is None:
                raise EvidenceValidationError(f"P02R2 review history digest mismatch: {key}")
    contract = oracle["parser_capability_contract"]
    contract_keys = {
        "schema_version",
        "primary_backend",
        "primary_version",
        "primary_current_rule",
        "capability_status_enum",
        "limitation_codes",
        "observable_fields",
        "independence_rule",
        "pure_extractor_module_contract",
        "extractor_registry",
        "extractor_execution_rule",
        "raw_artifact_binding_schema",
        "source_invocation_receipt_schema",
        "raw_input_entry_schema",
        "raw_extractor_output_schema",
        "expected_value_projection_schema",
        "comparison_rule",
        "real_document_label_scope_audit",
        "record_contract",
        "status_precedence",
        "status_field_rules",
        "malformed_rule",
        "non_source_mappable_rule",
        "limitation_boundary",
        "contradiction_rule",
        "selection_rule",
        "required_invocation_count",
        "required_version_invocation_count",
        "required_source_invocation_count",
        "proxy_metrics",
        "veto_id",
    }
    if (
        type(contract) is not dict
        or set(contract) != contract_keys
        or contract.get("schema_version") != "p02r2_parser_capability_contract@1"
        or contract.get("required_invocation_count") != 28
        or contract.get("required_version_invocation_count") != 2
        or contract.get("required_source_invocation_count") != 26
        or len(contract.get("capability_status_enum", [])) != 9
        or len(contract.get("observable_fields", [])) != 7
    ):
        raise EvidenceValidationError("P02R2 parser capability registry mismatch")
    pure = contract.get("pure_extractor_module_contract")
    pure_keys = {
        "schema_version",
        "module_ref",
        "creation_boundary",
        "top_level_statement_order",
        "allowed_imports",
        "module_body_rule",
        "function_shape_rule",
        "store_target_rule",
        "module_global_rule",
        "forbidden_ast_nodes",
        "forbidden_capability_roots",
        "static_name_and_call_rule",
        "runtime_function_rule",
        "function_contracts",
    }
    expected_function_contracts = {
        "_p02r2_extract_latexml_structural_label_set": {
            "positional_parameters": ["specialist_output_xml", "specialist_log"],
            "referenced_globals": ["ET"],
            "referenced_builtins": [
                "UnicodeDecodeError",
                "ValueError",
                "bytes",
                "sorted",
                "str",
                "type",
            ],
            "builtin_callable_allowlist": ["ValueError", "sorted", "type"],
            "imported_attribute_allowlist": ["ET.ParseError", "ET.fromstring"],
            "imported_callable_allowlist": ["ET.fromstring"],
            "value_attribute_read_allowlist": ["attrib", "tag"],
            "value_method_call_allowlist": [
                "append",
                "decode",
                "items",
                "iter",
                "rsplit",
                "split",
                "startswith",
            ],
            "callable_dependency_allowlist": [],
        },
        "_p02r2_extract_pandoc_math_label_set": {
            "positional_parameters": ["specialist_stdout_json"],
            "referenced_globals": ["json", "re"],
            "referenced_builtins": [
                "UnicodeDecodeError",
                "ValueError",
                "bytes",
                "dict",
                "len",
                "list",
                "set",
                "sorted",
                "str",
                "type",
            ],
            "builtin_callable_allowlist": ["ValueError", "len", "list", "set", "sorted", "type"],
            "imported_attribute_allowlist": ["json.loads", "re.finditer"],
            "imported_callable_allowlist": ["json.loads", "re.finditer"],
            "value_attribute_read_allowlist": [],
            "value_method_call_allowlist": [
                "add",
                "append",
                "decode",
                "extend",
                "group",
                "items",
                "pop",
            ],
            "callable_dependency_allowlist": [],
        },
    }
    if (
        type(pure) is not dict
        or set(pure) != pure_keys
        or pure["schema_version"] != "p02r2_pure_extractor_module_contract@1"
        or pure["module_ref"] != PURE_EXTRACTOR_MODULE_REF
        or pure["top_level_statement_order"]
        != [
            "import json",
            "import re",
            "import xml.etree.ElementTree as ET",
            "def _p02r2_extract_latexml_structural_label_set",
            "def _p02r2_extract_pandoc_math_label_set",
        ]
        or pure["allowed_imports"]
        != [
            {"form": "import", "module": "json", "alias": None},
            {"form": "import", "module": "re", "alias": None},
            {"form": "import", "module": "xml.etree.ElementTree", "alias": "ET"},
        ]
        or pure["function_contracts"] != expected_function_contracts
        or len(pure["forbidden_ast_nodes"]) != len(set(pure["forbidden_ast_nodes"]))
        or len(pure["forbidden_capability_roots"])
        != len(set(pure["forbidden_capability_roots"]))
    ):
        raise EvidenceValidationError("P02R2 pure extractor module contract mismatch")
    extractors = contract.get("extractor_registry")
    expected_extractors = {
        "p02r2_latexml_structural_label_set_v1": (
            "latexml",
            "_p02r2_extract_latexml_structural_label_set",
            ["specialist_output_xml", "specialist_log"],
        ),
        "p02r2_pandoc_math_label_set_v1": (
            "pandoc",
            "_p02r2_extract_pandoc_math_label_set",
            ["specialist_stdout_json"],
        ),
    }
    extractor_keys = {
        "backend",
        "function_name",
        "module_ref",
        "input_roles",
        "input_value_types",
        "input_receipt_artifact_fields",
        "output_exact_keys",
        "raw_observable_field",
        "observed_value_schema",
        "promotion_capable",
        "forbidden_inputs",
    }
    if type(extractors) is not dict or set(extractors) != set(expected_extractors):
        raise EvidenceValidationError("P02R2 extractor id registry mismatch")
    expected_receipt_fields = {
        "p02r2_latexml_structural_label_set_v1": ["output", "log"],
        "p02r2_pandoc_math_label_set_v1": ["stdout"],
    }
    for extractor_id, (backend, function_name, input_roles) in expected_extractors.items():
        item = extractors[extractor_id]
        if (
            type(item) is not dict
            or set(item) != extractor_keys
            or item["backend"] != backend
            or item["function_name"] != function_name
            or item["module_ref"] != PURE_EXTRACTOR_MODULE_REF
            or item["input_roles"] != input_roles
            or item["input_value_types"] != ["bytes"] * len(input_roles)
            or item["input_receipt_artifact_fields"] != expected_receipt_fields[extractor_id]
            or item["output_exact_keys"] != ["raw_observable_field", "observed_value"]
            or item["raw_observable_field"] != "document_structural_label_set"
            or item["promotion_capable"] is not False
        ):
            raise EvidenceValidationError(f"P02R2 extractor registry mismatch: {extractor_id}")
        required_forbidden = {
            "source_bytes",
            "source_ref_contents",
            "expected_labels",
            "expected_spans",
            "current_parser_record",
            "compact_oracle",
            "materialized_oracle",
            "filesystem_path",
            "subprocess",
            "network",
        }
        if set(item["forbidden_inputs"]) != required_forbidden or len(item["forbidden_inputs"]) != len(
            required_forbidden
        ):
            raise EvidenceValidationError(f"P02R2 extractor forbidden-input closure mismatch: {extractor_id}")
    raw_artifact = contract.get("raw_artifact_binding_schema")
    if (
        type(raw_artifact) is not dict
        or set(raw_artifact)
        != {"schema_version", "exact_keys_in_canonical_order", "exact_types", "binding_rule"}
        or raw_artifact["schema_version"] != "p02r2_raw_artifact_binding@1"
        or raw_artifact["exact_keys_in_canonical_order"]
        != ["byte_count", "present", "ref", "sha256"]
        or raw_artifact["exact_types"]
        != {
            "ref": "workspace_relative_str",
            "present": "bool",
            "sha256": "lowercase_sha256_str_or_null",
            "byte_count": "nonnegative_int_not_bool_or_null",
        }
    ):
        raise EvidenceValidationError("P02R2 raw artifact binding schema mismatch")
    source_receipt = contract.get("source_invocation_receipt_schema")
    if (
        type(source_receipt) is not dict
        or set(source_receipt)
        != {
            "schema_version",
            "fixed_ref_template",
            "exact_keys_in_canonical_order",
            "exact_types",
            "binding_rule",
        }
        or source_receipt["schema_version"] != "p02r2_parser_source_invocation_receipt@1"
        or source_receipt["fixed_ref_template"] != "RR/parser/receipts/BACKEND-CASE-raw.json"
        or source_receipt["exact_keys_in_canonical_order"]
        != [
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
        ]
        or source_receipt["exact_types"]
        != {
            "schema_version": "str_exact_p02r2_parser_source_invocation_receipt@1",
            "backend": "str_enum_latexml_pandoc",
            "source_ref": "workspace_relative_str",
            "source_sha256_before": "lowercase_sha256_str",
            "source_sha256_after": "lowercase_sha256_str",
            "case_token": "lowercase_sha256_str",
            "argv": "list[str]",
            "environment": "object[str,str]",
            "timeout_seconds": "positive_int_not_bool",
            "exit_code": "int_or_null_not_bool",
            "timed_out": "bool",
            "wall_time_ns": "nonnegative_int_not_bool",
            "stdout": "p02r2_raw_artifact_binding@1",
            "stderr": "p02r2_raw_artifact_binding@1",
            "output": "p02r2_raw_artifact_binding@1",
            "log": "p02r2_raw_artifact_binding@1_or_null",
            "version_receipt_ref": "workspace_relative_str",
            "version_receipt_sha256": "lowercase_sha256_str",
        }
    ):
        raise EvidenceValidationError("P02R2 source invocation receipt schema mismatch")
    raw_input = contract.get("raw_input_entry_schema")
    if (
        type(raw_input) is not dict
        or set(raw_input)
        != {
            "schema_version",
            "exact_keys_in_canonical_order",
            "exact_types",
            "array_rule",
            "artifact_rule",
            "invocation_receipt_rule",
        }
        or raw_input["schema_version"] != "p02r2_raw_input_entry@1"
        or raw_input["exact_keys_in_canonical_order"]
        != [
            "artifact_byte_count",
            "artifact_ref",
            "artifact_sha256",
            "invocation_receipt_ref",
            "invocation_receipt_sha256",
            "role",
            "value_type",
        ]
        or raw_input["exact_types"]
        != {
            "role": "str",
            "value_type": "str_exact_bytes",
            "artifact_ref": "workspace_relative_str",
            "artifact_sha256": "lowercase_sha256_str",
            "artifact_byte_count": "nonnegative_int_not_bool",
            "invocation_receipt_ref": "workspace_relative_str",
            "invocation_receipt_sha256": "lowercase_sha256_str",
        }
    ):
        raise EvidenceValidationError("P02R2 raw input schema mismatch")
    raw_output = contract.get("raw_extractor_output_schema")
    if (
        type(raw_output) is not dict
        or set(raw_output)
        != {"schema_version", "exact_keys_in_canonical_order", "exact_types", "value_rule"}
        or raw_output["schema_version"] != "p02r2_raw_extractor_output@1"
        or raw_output["exact_keys_in_canonical_order"]
        != ["observed_value", "raw_observable_field"]
        or raw_output["exact_types"]
        != {
            "observed_value": "list[str]",
            "raw_observable_field": "str_exact_document_structural_label_set",
        }
    ):
        raise EvidenceValidationError("P02R2 raw extractor output schema mismatch")
    expected_projection = contract.get("expected_value_projection_schema")
    if (
        type(expected_projection) is not dict
        or set(expected_projection)
        != {
            "schema_version",
            "fixed_ref_template",
            "exact_keys_in_canonical_order",
            "exact_types",
            "projection_rule",
        }
        or expected_projection["schema_version"] != "p02r2_expected_label_value_projection@1"
        or expected_projection["fixed_ref_template"]
        != "RR/parser/expected-values/CASE-exact-requested-label-set.json"
        or expected_projection["exact_keys_in_canonical_order"]
        != ["expected_value", "observable_field", "schema_version", "source_ref", "source_sha256"]
        or expected_projection["exact_types"]
        != {
            "schema_version": "str_exact_p02r2_expected_label_value_projection@1",
            "source_ref": "workspace_relative_str",
            "source_sha256": "lowercase_sha256_str",
            "observable_field": "str_exact_exact_requested_label_set",
            "expected_value": "list[str]",
        }
    ):
        raise EvidenceValidationError("P02R2 expected-value projection schema mismatch")
    scope_audit = contract.get("real_document_label_scope_audit")
    expected_scope_entries = [
        {
            "source_ref": (
                "docs/credit-card-npv-component-proposal/"
                "credit_card_npv_component_proposal_final_submission.tex"
            ),
            "source_distinct_label_token_count": 298,
            "requested_label_count": 2,
            "unscoped_extra_label_token_count": 296,
        },
        {
            "source_ref": "docs/risky-debt-maliar-deep-learning-lecture-note.tex",
            "source_distinct_label_token_count": 116,
            "requested_label_count": 2,
            "unscoped_extra_label_token_count": 114,
        },
    ]
    if (
        type(scope_audit) is not dict
        or set(scope_audit)
        != {"schema_version", "distinct_label_token_regex", "entries", "audit_rule"}
        or scope_audit["schema_version"] != "p02r2_real_document_label_scope_audit@1"
        or scope_audit["distinct_label_token_regex"] != r"\\label\s*\{([^{}]+)\}"
        or scope_audit["entries"] != expected_scope_entries
    ):
        raise EvidenceValidationError("P02R2 real-document label-scope audit mismatch")
    records = contract.get("record_contract")
    if (
        type(records) is not dict
        or set(records)
        != {
            "required_fields",
            "diagnostic_observations",
            "observation_provenance_schema",
            "comparison_provenance_schema",
            "promotional_fields",
            "contradictions",
            "eligible_for_selection",
        }
        or records["required_fields"]
        != [
            "capability_status",
            "limitation_codes",
            "diagnostic_observations",
            "observation_provenance",
            "comparison_provenance",
            "promotional_fields",
            "contradictions",
            "eligible_for_selection",
        ]
    ):
        raise EvidenceValidationError("P02R2 parser record contract mismatch")
    observation = records["observation_provenance_schema"]
    if (
        type(observation) is not dict
        or set(observation) != {"exact_keys_in_canonical_order", "exact_types", "binding_rule"}
        or observation["exact_keys_in_canonical_order"]
        != [
            "extractor_id",
            "extractor_module_ref",
            "extractor_module_sha256",
            "forbidden_lineage",
            "raw_inputs",
            "raw_output",
        ]
        or observation["exact_types"]
        != {
            "extractor_id": "str",
            "extractor_module_ref": "workspace_relative_str",
            "extractor_module_sha256": "lowercase_sha256_str",
            "raw_inputs": "list[p02r2_raw_input_entry@1]",
            "raw_output": "p02r2_raw_extractor_output@1",
            "forbidden_lineage": "list[str]_exact_empty",
        }
    ):
        raise EvidenceValidationError("P02R2 observation provenance schema mismatch")
    comparison = records["comparison_provenance_schema"]
    if (
        type(comparison) is not dict
        or set(comparison) != {"exact_keys_in_canonical_order", "exact_types", "binding_rule"}
        or comparison["exact_keys_in_canonical_order"]
        != [
            "comparison_id",
            "expected_value",
            "expected_value_ref",
            "expected_value_sha256",
            "matched_requested_value",
            "matches_expected",
            "missing_requested_value",
            "raw_observed_value",
            "unscoped_extra_value",
        ]
        or comparison["exact_types"]
        != {
            "comparison_id": "str_exact_p02r2_requested_label_coverage_comparison_v1",
            "expected_value_ref": "workspace_relative_str",
            "expected_value_sha256": "lowercase_sha256_str",
            "expected_value": "list[str]",
            "matched_requested_value": "list[str]",
            "matches_expected": "bool",
            "missing_requested_value": "list[str]",
            "raw_observed_value": "list[str]",
            "unscoped_extra_value": "list[str]",
        }
    ):
        raise EvidenceValidationError("P02R2 comparison provenance schema mismatch")
    downstream = oracle.get("downstream_binding_contract")
    downstream_keys = {
        "schema_version",
        "inherited_reviewed_plan_fields",
        "inherited_reviewed_compact_oracle_fields",
        "inherited_reviewed_materialized_oracle_fields",
        "transitive_base_rule",
        "forbidden_aliases",
        "result_schema_rule",
        "run_manifest_rule",
        "candidate_rule",
        "final_rule",
    }
    if (
        type(downstream) is not dict
        or set(downstream) != downstream_keys
        or downstream["schema_version"] != "p02r2_downstream_binding_contract@1"
    ):
        raise EvidenceValidationError("P02R2 downstream binding contract mismatch")

    base = _strict_reviewed_json(
        _read(root, bindings["base_compact_oracle_ref"]), "base compact oracle"
    )
    label_pattern = re.compile(scope_audit["distinct_label_token_regex"])
    for expected in expected_scope_entries:
        source_ref = expected["source_ref"]
        try:
            source_text = _read(root, source_ref).decode("utf-8", "strict")
        except UnicodeDecodeError as exc:
            raise EvidenceValidationError("P02R2 scope-audit source is not strict UTF-8") from exc
        source_labels = set(label_pattern.findall(source_text))
        requested_labels = {
            item["label"] for item in base["frozen_sources"] if item["source_ref"] == source_ref
        }
        if (
            len(source_labels) != expected["source_distinct_label_token_count"]
            or len(requested_labels) != expected["requested_label_count"]
            or not requested_labels <= source_labels
            or len(source_labels - requested_labels) != expected["unscoped_extra_label_token_count"]
        ):
            raise EvidenceValidationError("P02R2 real-document label-scope evidence drifted")
    patches = oracle["profile_patch"]
    paths = [item.get("path") for item in patches]
    if len(patches) != 12 or len(paths) != len(set(paths)):
        raise EvidenceValidationError("P02R2 profile patch registry mismatch")
    for item in patches:
        if set(item) != {"path", "expected_base_value", "replacement"}:
            raise EvidenceValidationError("P02R2 profile patch schema mismatch")
        if _resolve_pointer(base, item["path"]) != item["expected_base_value"]:
            raise EvidenceValidationError(f"P02R2 profile patch baseline drift: {item['path']}")
    compile_patch = next((item for item in patches if item["path"] == COMPILE_PATCH_PATH), None)
    if compile_patch is None:
        raise EvidenceValidationError("P02R2 compile allowlist patch is missing")
    old_argv = compile_patch["expected_base_value"]
    new_argv = compile_patch["replacement"]
    if (
        type(old_argv) is not list
        or type(new_argv) is not list
        or old_argv[:3] != [PYTHON, "-m", "py_compile"]
        or new_argv[:3] != [PYTHON, "-m", "py_compile"]
        or len(old_argv[3:]) != 22
        or len(new_argv[3:]) != 23
        or old_argv[3:] != sorted(old_argv[3:], key=lambda value: value.encode("utf-8"))
        or new_argv[3:] != sorted(new_argv[3:], key=lambda value: value.encode("utf-8"))
        or len(set(new_argv[3:])) != 23
        or set(new_argv[3:]) != set(old_argv[3:]) | {PURE_EXTRACTOR_MODULE_REF}
    ):
        raise EvidenceValidationError("P02R2 effective implementation allowlist mismatch")
    return base


def _verify_old_entry(root: Path, base: dict[str, Any], bindings: dict[str, Any]) -> dict[str, Any]:
    entry_ref = bindings["prior_entry_ref"]
    raw = _read(root, entry_ref)
    if content_digest(raw) != bindings["prior_entry_sha256"]:
        raise EvidenceValidationError("old Phase 02 entry record digest mismatch")
    value = _strict_reviewed_json(raw, "old Phase 02 entry record")
    if canonical_json_bytes(value) != raw:
        raise EvidenceValidationError("old Phase 02 entry record is not canonical")
    schema = base["governance_action_profile"]["entry_snapshot_schema"]
    if set(value) != set(schema["exact_keys"]) or len(value) != len(schema["exact_keys"]):
        raise EvidenceValidationError("old Phase 02 entry schema mismatch")
    entry_root = root / Path(entry_ref).parent
    if entry_root.is_symlink() or not entry_root.is_dir():
        raise EvidenceValidationError("old Phase 02 entry root is unsafe")
    files = list(entry_root.iterdir())
    expected_names = {
        "entry-record.json",
        "implementation-entry-sha256.txt",
        "protected-entry-sha256.txt",
        "immutable-input-sha256.txt",
    }
    if {item.name for item in files} != expected_names or any(item.is_symlink() or not item.is_file() for item in files):
        raise EvidenceValidationError("old Phase 02 entry tree differs from its sealed four-file shape")
    for ref_key, digest_key in (
        ("implementation_entry_manifest_ref", "implementation_entry_manifest_sha256"),
        ("protected_entry_manifest_ref", "protected_entry_manifest_sha256"),
        ("immutable_input_manifest_ref", "immutable_input_manifest_sha256"),
    ):
        if _sha(root, value[ref_key]) != value[digest_key]:
            raise EvidenceValidationError(f"old Phase 02 entry artifact drift: {ref_key}")
    return value


def _verify_manifest_current(root: Path, raw: bytes, base_library: dict[str, Any]) -> None:
    refs = base_library["_manifest_refs_from_bytes"](raw)
    for line, ref in zip(raw.splitlines(), refs, strict=True):
        digest = line[:64].decode("ascii")
        if _sha(root, ref) != digest:
            raise EvidenceValidationError(f"old protected/immutable input drifted: {ref}")


def _review_verdict(raw: bytes, *, expected: str | None = None) -> str:
    if len(raw) > 131072 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError("P02R2 review violates bounded byte grammar")
    try:
        lines = raw.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("P02R2 review is not strict UTF-8") from exc
    verdicts = [line for line in lines if line.startswith("VERDICT:")]
    nonempty = [line for line in lines if line]
    if len(verdicts) != 1 or verdicts[0] not in {"VERDICT: AGREE", "VERDICT: REVISE"} or not nonempty or nonempty[-1] != verdicts[0]:
        raise EvidenceValidationError("P02R2 review verdict is not unique and final")
    verdict = verdicts[0].split(": ", 1)[1]
    if expected is not None and verdict != expected:
        raise EvidenceValidationError(f"P02R2 review verdict must be {expected}")
    return verdict


def _review_binding_lines(binding: dict[str, Any]) -> dict[str, str]:
    return {
        "Reviewed recovery plan SHA-256": binding["reviewed_recovery_plan_sha256"],
        "Reviewed recovery oracle SHA-256": binding["reviewed_recovery_oracle_sha256"],
        "Reviewed recovery bootstrap SHA-256": binding["reviewed_recovery_bootstrap_sha256"],
        "Reviewed base plan SHA-256": binding["reviewed_base_plan_sha256"],
        "Reviewed base compact oracle SHA-256": binding["reviewed_base_compact_oracle_sha256"],
        "Reviewed materialized oracle SHA-256": binding["reviewed_materialized_oracle_sha256"],
        "Reviewed prior entry SHA-256": binding["reviewed_prior_entry_sha256"],
    }


def _verify_review_lines(raw: bytes, required: dict[str, str]) -> None:
    lines = raw.decode("utf-8", "strict").splitlines()
    for label, digest in required.items():
        if SHA_RE.fullmatch(digest) is None or lines.count(f"{label}: `{digest}`") != 1:
            raise EvidenceValidationError(f"P02R2 review binding mismatch: {label}")


def _verify_agreeing_review(
    root: Path,
    review_ref: str,
    *,
    recovery_oracle: dict[str, Any],
) -> str:
    match = REVIEW_RE.fullmatch(review_ref)
    if match is None:
        raise EvidenceValidationError("P02R2 agreeing review path is outside R11-R14")
    selected_round = int(match.group(1))
    review_dir = root / "docs/reviews"
    history = {item["round"]: item for item in recovery_oracle["review_budget"]["review_history"]}
    for round_number in range(11, 15):
        ref = (
            "docs/reviews/mathdevmcp-real-document-remediation-phase-02r2-"
            f"plan-review-r{round_number}-result-2026-07-12.md"
        )
        exists = (root / ref).exists() or (root / ref).is_symlink()
        if round_number < selected_round:
            if not exists or round_number not in history:
                raise EvidenceValidationError("P02R2 review sequence has a skipped or unregistered round")
            historical = history[round_number]
            historical_raw = _read(root, ref)
            if content_digest(historical_raw) != historical["result_sha256"]:
                raise EvidenceValidationError("P02R2 historical review digest mismatch")
            _review_verdict(historical_raw, expected="REVISE")
            _verify_review_lines(historical_raw, _review_binding_lines(historical))
        elif round_number > selected_round and exists:
            raise EvidenceValidationError("P02R2 later review result already exists")
    for path in review_dir.glob(
        "mathdevmcp-real-document-remediation-phase-02r2-plan-review-r*-result-*.md"
    ):
        parsed = REVIEW_RE.fullmatch(path.relative_to(root).as_posix())
        if parsed is None or int(parsed.group(1)) not in range(11, 15):
            raise EvidenceValidationError("P02R2 review result escapes the authorized budget")

    raw = _read(root, review_ref)
    _review_verdict(raw, expected="AGREE")
    bindings = recovery_oracle["base_bindings"]
    required = {
        "Reviewed recovery plan SHA-256": _sha(root, RECOVERY_PLAN_REF),
        "Reviewed recovery oracle SHA-256": _sha(root, RECOVERY_ORACLE_REF),
        "Reviewed recovery bootstrap SHA-256": _sha(root, BOOTSTRAP_REF),
        "Reviewed base plan SHA-256": bindings["base_plan_sha256"],
        "Reviewed base compact oracle SHA-256": bindings["base_compact_oracle_sha256"],
        "Reviewed materialized oracle SHA-256": bindings["base_materialized_oracle_sha256"],
        "Reviewed prior entry SHA-256": bindings["prior_entry_sha256"],
    }
    _verify_review_lines(raw, required)
    return content_digest(raw)


def _tree_refs(root: Path, ref: str) -> set[str]:
    top = root / ref
    if top.is_symlink() or not top.is_dir():
        raise EvidenceValidationError(f"protected evidence tree is unsafe: {ref}")
    result: set[str] = set()
    for path in top.rglob("*"):
        if path.is_symlink():
            raise EvidenceValidationError(f"symlink in protected evidence tree: {path}")
        if path.is_file():
            result.add(path.relative_to(root).as_posix())
        elif not path.is_dir():
            raise EvidenceValidationError(f"special path in protected evidence tree: {path}")
    return result


def _control_refs(root: Path) -> set[str]:
    result = {
        "AGENTS.md",
        RECOVERY_PLAN_REF,
        RECOVERY_ORACLE_REF,
        BOOTSTRAP_REF,
        BASE_BOOTSTRAP_REF,
    }
    for directory_ref in ("docs/plans", "docs/reviews"):
        directory = root / directory_ref
        for path in directory.iterdir():
            if path.is_symlink():
                raise EvidenceValidationError(f"symlink in protected control directory: {path}")
            if path.is_file() and path.name.startswith("mathdevmcp-"):
                result.add(path.relative_to(root).as_posix())
    return result


def _protected_refs(
    root: Path,
    base_library: dict[str, Any],
    base: dict[str, Any],
    *,
    output_refs: set[str],
) -> set[str]:
    allowlist = base_library["_implementation_allowlist"](base)
    dirty = set(base_library["_dirty_refs"](root)) - allowlist - output_refs
    protected = dirty | _control_refs(root)
    for tree in (
        ".local/mathdevmcp/evidence/p00-20260711",
        ".local/mathdevmcp/evidence/p01-20260711",
        ".local/mathdevmcp/evidence/p02-20260711",
    ):
        protected.update(_tree_refs(root, tree))
    return protected


def _mkdir_entry_tree(root: Path) -> None:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    directory_fd = os.open(root, flags)
    try:
        for component in (".local", "mathdevmcp", "evidence"):
            next_fd = os.open(component, flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        os.mkdir("p02r2-20260712", mode=0o700, dir_fd=directory_fd)
        phase_fd = os.open("p02r2-20260712", flags, dir_fd=directory_fd)
        try:
            os.mkdir("entry", mode=0o700, dir_fd=phase_fd)
        finally:
            os.close(phase_fd)
    finally:
        os.close(directory_fd)


def _verify_new_tree(root: Path, expected_refs: Iterable[str]) -> None:
    phase = root / EVIDENCE_ROOT_REF
    if phase.is_symlink() or not phase.is_dir() or [item.name for item in phase.iterdir()] != ["entry"]:
        raise EvidenceValidationError("P02R2 evidence root shape mismatch")
    entry = phase / "entry"
    files = list(entry.iterdir())
    expected_names = {Path(ref).name for ref in expected_refs}
    if {item.name for item in files} != expected_names or len(files) != len(expected_names):
        raise EvidenceValidationError("P02R2 entry root shape mismatch")
    if any(item.is_symlink() or not item.is_file() for item in files):
        raise EvidenceValidationError("P02R2 entry output is not regular")


def _write_snapshot(root: Path, review_ref: str) -> dict[str, str]:
    if (root / EVIDENCE_ROOT_REF).exists() or (root / EVIDENCE_ROOT_REF).is_symlink():
        raise EvidenceValidationError("P02R2 evidence root must be absent")
    if (root / PURE_EXTRACTOR_MODULE_REF).exists() or (root / PURE_EXTRACTOR_MODULE_REF).is_symlink():
        raise EvidenceValidationError("P02R2 pure extractor module must be absent before entry")

    base_library = _load_base_library(root)
    recovery_oracle = _strict_reviewed_json(_read(root, RECOVERY_ORACLE_REF), "P02R2 recovery oracle")
    base = _validate_recovery_oracle(root, recovery_oracle)
    bindings = recovery_oracle["base_bindings"]
    old_entry = _verify_old_entry(root, base, bindings)
    for manifest_key in ("protected_entry_manifest_ref", "immutable_input_manifest_ref"):
        _verify_manifest_current(root, _read(root, old_entry[manifest_key]), base_library)
    review_sha = _verify_agreeing_review(root, review_ref, recovery_oracle=recovery_oracle)

    p01_stable_ref = old_entry["p01_stable_decision_ref"]
    p01_index_ref = old_entry["p01_terminal_receipt_index_ref"]
    strict_load_canonical_json(_read(root, p01_stable_ref), schema="p01_final_decision@1")
    p01_index = verify_receipt_index(root, p01_index_ref)
    if (
        _sha(root, p01_stable_ref) != old_entry["p01_stable_decision_sha256"]
        or p01_index["index_sha256"] != old_entry["p01_terminal_receipt_index_sha256"]
    ):
        raise EvidenceValidationError("P02R2 P01 predecessor binding mismatch")

    immutable_refs = set(base_library["_verified_immutable_refs"](root, base))
    immutable_refs.update(
        {
            RECOVERY_PLAN_REF,
            RECOVERY_ORACLE_REF,
            BOOTSTRAP_REF,
            review_ref,
            *bindings.values(),
            *(
                old_entry[key]
                for key in (
                    "implementation_entry_manifest_ref",
                    "protected_entry_manifest_ref",
                    "immutable_input_manifest_ref",
                )
            ),
        }
    )
    immutable_refs = {ref for ref in immutable_refs if isinstance(ref, str) and not SHA_RE.fullmatch(ref)}
    implementation_manifest = base_library["_manifest"](
        root, base_library["_implementation_refs"](root)
    )
    output_refs = set(recovery_oracle["entry_schema"]["write_order"])
    protected_refs = _protected_refs(root, base_library, base, output_refs=output_refs)
    protected_manifest = base_library["_manifest"](root, protected_refs)
    immutable_manifest = base_library["_manifest"](root, immutable_refs)

    record = {
        "schema_version": "p02r2_entry_record@1",
        "phase": "P02",
        "revision": "P02R2",
        "recovery_plan_ref": RECOVERY_PLAN_REF,
        "recovery_plan_sha256": _sha(root, RECOVERY_PLAN_REF),
        "recovery_oracle_ref": RECOVERY_ORACLE_REF,
        "recovery_oracle_sha256": _sha(root, RECOVERY_ORACLE_REF),
        "agreeing_plan_review_ref": review_ref,
        "agreeing_plan_review_sha256": review_sha,
        "entry_bootstrap_ref": BOOTSTRAP_REF,
        "entry_bootstrap_sha256": _sha(root, BOOTSTRAP_REF),
        "base_plan_ref": bindings["base_plan_ref"],
        "base_plan_sha256": bindings["base_plan_sha256"],
        "base_compact_oracle_ref": bindings["base_compact_oracle_ref"],
        "base_compact_oracle_sha256": bindings["base_compact_oracle_sha256"],
        "base_materialized_oracle_ref": bindings["base_materialized_oracle_ref"],
        "base_materialized_oracle_sha256": bindings["base_materialized_oracle_sha256"],
        "prior_entry_ref": bindings["prior_entry_ref"],
        "prior_entry_sha256": bindings["prior_entry_sha256"],
        "runtime_contract_review_ref": bindings["runtime_contract_review_ref"],
        "runtime_contract_review_sha256": bindings["runtime_contract_review_sha256"],
        "pre_round_blocker_ref": bindings["pre_round_blocker_ref"],
        "pre_round_blocker_sha256": bindings["pre_round_blocker_sha256"],
        "p01_stable_decision_ref": p01_stable_ref,
        "p01_stable_decision_sha256": old_entry["p01_stable_decision_sha256"],
        "p01_terminal_receipt_index_ref": p01_index_ref,
        "p01_terminal_receipt_index_sha256": old_entry["p01_terminal_receipt_index_sha256"],
        "implementation_entry_manifest_ref": IMPLEMENTATION_MANIFEST_REF,
        "implementation_entry_manifest_sha256": content_digest(implementation_manifest),
        "protected_entry_manifest_ref": PROTECTED_MANIFEST_REF,
        "protected_entry_manifest_sha256": content_digest(protected_manifest),
        "immutable_input_manifest_ref": IMMUTABLE_MANIFEST_REF,
        "immutable_input_manifest_sha256": content_digest(immutable_manifest),
    }
    exact_keys = recovery_oracle["entry_schema"]["exact_keys"]
    if set(record) != set(exact_keys) or len(record) != len(exact_keys):
        raise EvidenceValidationError("P02R2 entry record differs from exact schema")

    payloads = {
        IMPLEMENTATION_MANIFEST_REF: implementation_manifest,
        PROTECTED_MANIFEST_REF: protected_manifest,
        IMMUTABLE_MANIFEST_REF: immutable_manifest,
        ENTRY_RECORD_REF: canonical_json_bytes(record),
    }
    _mkdir_entry_tree(root)
    for ref in recovery_oracle["entry_schema"]["write_order"]:
        atomic_write_bytes_no_replace(root, ref, payloads[ref])
    _verify_new_tree(root, payloads)
    reopened = {ref: _read(root, ref) for ref in payloads}
    if reopened != payloads:
        raise EvidenceValidationError("P02R2 entry reopen mismatch")

    current_manifests = {
        IMPLEMENTATION_MANIFEST_REF: base_library["_manifest"](
            root, base_library["_implementation_refs"](root)
        ),
        PROTECTED_MANIFEST_REF: base_library["_manifest"](
            root,
            _protected_refs(root, base_library, base, output_refs=output_refs),
        ),
        IMMUTABLE_MANIFEST_REF: base_library["_manifest"](root, immutable_refs),
    }
    for ref, current in current_manifests.items():
        if current != reopened[ref]:
            raise EvidenceValidationError(f"P02R2 entry manifest scope changed: {ref}")
    return {
        "entry_record_ref": ENTRY_RECORD_REF,
        "entry_record_sha256": content_digest(reopened[ENTRY_RECORD_REF]),
    }


def main() -> int:
    argv = sys.argv[1:]
    if len(argv) != 2 or argv[0] != "--agreeing-plan-review-ref" or "=" in argv[0]:
        raise EvidenceValidationError(
            "P02R2 entry bootstrap accepts exactly --agreeing-plan-review-ref VALUE"
        )
    _validate_invocation(argv)
    if REVIEW_RE.fullmatch(argv[1]) is None:
        raise EvidenceValidationError("P02R2 agreeing review ref is outside R11-R14")
    root = Path.cwd().absolute()
    if not (root / ".git").is_dir() or not (root / "src/mathdevmcp").is_dir():
        raise EvidenceValidationError("P02R2 entry bootstrap must run at workspace root")
    result = _write_snapshot(root, argv[1])
    sys.stdout.buffer.write(canonical_json_bytes(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
