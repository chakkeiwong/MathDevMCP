from __future__ import annotations

"""Strict Phase 03 context-only evidence schemas and reconstruction."""

from collections.abc import Mapping
from copy import deepcopy
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
from typing import Any

from .document_context_graph import (
    GRAPH_SCHEMA_VERSION,
    SEARCH_SCHEMA_VERSION,
    build_context_dependency_graph,
    resolve_context_requirement,
)
from .evidence_manifest import (
    EvidenceValidationError,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
    validate_logical_path,
)
from .math_ir import (
    build_typed_assumption,
    resolve_symbol_roles,
    validate_typed_assumption,
)


P03_ROOT_REF = ".local/mathdevmcp/evidence/p03-20260712"
P03_ENTRY_ROOT_REF = f"{P03_ROOT_REF}/entry"
P03_ENTRY_RECORD_REF = f"{P03_ENTRY_ROOT_REF}/entry-record.json"
P02_OBLIGATIONS_REF = (
    ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/"
    "extraction-bundle/obligations.json"
)
P02_OBLIGATIONS_SHA256 = "5aa6681e215d12f382e96f46f9f695cf80e1632affa0dd8bc39069eae78d85a0"
P02_STABLE_DECISION_REF = ".local/mathdevmcp/evidence/p02r3-20260712/phase-results/P02-decision.json"
P02_STABLE_DECISION_SHA256 = "f97b1a3a2faa02a661d69ee7b44620e1a8babb2669c7cafada89bf39c1c3db3d"
P02_EXTRACTION_BUNDLE_SEMANTIC_DIGEST = "98dfaf84155723500dd2065cad4837ddea93a688273bb427b946a68172498395"
ENTRY_FILE_NAMES = frozenset(
    {
        "entry-record.json",
        "implementation-entry-sha256.txt",
        "protected-entry-sha256.txt",
        "immutable-input-sha256.txt",
        "scratch-exclusion-ledger.json",
    }
)
CONTEXT_PACKET_LANES = (
    "parser_extraction",
    "context_search",
    "symbol_notation",
    "source_assumptions",
    "candidate_assumptions",
    "mathematical_requirements",
    "encoding_blockers",
    "backend_evidence",
    "engineering",
    "interpretation",
)
P03_PRIMARY_CRITERIA = (
    "all_17_obligations_partitioned_exactly",
    "all_context_manifests_validate",
    "all_source_support_has_exact_applicable_provenance",
    "search_boundaries_and_states_preserved",
    "symbol_and_notation_ambiguity_preserved",
    "typed_assumption_states_orthogonal",
    "report_state_ledgers_separated",
    "frozen_card_pi_not_posterior_by_spelling",
    "zero_backend_source_edit_publication",
    "governance_allowlist_and_protected_state_pass",
)
P03_VETO_KEYS = (
    "p02_or_source_binding_drift",
    "sibling_context_leakage",
    "invented_or_incomplete_provenance",
    "integrity_or_symlink_failure",
    "local_absence_promoted_to_corpus_absence",
    "not_searched_promoted_to_missing",
    "lexical_candidate_promoted_to_support",
    "unconditional_symbol_role",
    "candidate_assumption_promoted_to_stated",
    "context_error_promoted_to_mathematics",
    "backend_execution_detected",
    "source_edit_detected",
    "publication_leak_detected",
    "unexpected_implementation_path",
    "protected_baseline_drift",
    "governance_chain_failure",
)
P03_NON_CLAIMS = (
    "no_context_search_completeness_beyond_recorded_budgets",
    "no_semantic_equivalence",
    "no_sufficient_or_minimal_assumptions",
    "no_mathematical_closure_or_proof",
    "no_backend_fitness",
    "no_general_latex_coverage",
    "no_repair_publication",
    "no_phase04_or_release_readiness",
)
P03_HUMAN_RESULT_SECTIONS = (
    "Decision",
    "Master Decision Table",
    "Evidence Contract Result",
    "Bound State",
    "Actual Commands And Receipts",
    "Evidence Ledgers",
    "External-Tool Consideration Ledger",
    "Default And Assumption Audit",
    "Post-Run Red Team",
    "Veto Status",
    "Non-Claims",
    "Next Action",
)
P03_GUARDED_ACTIONS = (
    "context_graph_tests",
    "resolver_tests",
    "symbol_assumption_tests",
    "report_boundary_tests",
    "frozen_context_regressions",
    "p00_quarantine",
    "generate_context_bundle",
)
P03_MUTATION_IDS = (
    "source_digest",
    "source_span",
    "dependency_edge",
    "unsearched_boundary",
    "keyword_promotion",
    "candidate_assumption_promotion",
    "pi_role",
    "override_scope",
    "assumption_binding",
    "engineering_lane",
    "publication_backend_count",
)
_DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
_ROUND_ROOT = PurePosixPath(f"{P03_ROOT_REF}/result-rounds")
_DEFAULT_BUDGET = {
    "max_files": 8,
    "max_bytes": 1_048_576,
    "max_nodes": 256,
    "max_edges": 512,
    "max_dependency_expansions": 64,
}
_FROZEN_BUDGETS = {
    "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8": {
        "max_files": 1,
        "max_bytes": 469_323,
        "max_nodes": 4_096,
        "max_edges": 8_192,
        "max_dependency_expansions": 1,
    },
    "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1": {
        "max_files": 1,
        "max_bytes": 117_506,
        "max_nodes": 4_096,
        "max_edges": 8_192,
        "max_dependency_expansions": 1,
    },
}


def _require_digest(value: Any, name: str) -> str:
    if not isinstance(value, str) or not _DIGEST_RE.fullmatch(value):
        raise EvidenceValidationError(f"{name} must be a lowercase SHA-256")
    return value


def _strict_json(raw: bytes, name: str) -> dict[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise EvidenceValidationError(f"{name} has a UTF-8 BOM")
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"{name} is not strict UTF-8 JSON") from exc
    if not isinstance(value, dict) or canonical_json_bytes(value) != raw:
        raise EvidenceValidationError(f"{name} is not a canonical JSON object")
    return value


def _manifest_records(raw: bytes, name: str) -> dict[str, str]:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError(f"{name} is not strict UTF-8") from exc
    if not text.endswith("\n") or "\r" in text or "\x00" in text:
        raise EvidenceValidationError(f"{name} has invalid manifest bytes")
    records: dict[str, str] = {}
    for line in text.splitlines():
        digest, separator, ref = line.partition("  ")
        if separator != "  " or not _DIGEST_RE.fullmatch(digest) or ref in records:
            raise EvidenceValidationError(f"{name} contains an invalid manifest line")
        validate_logical_path(ref, name=f"{name} ref")
        records[ref] = digest
    if list(records) != sorted(records, key=lambda item: item.encode("utf-8")):
        raise EvidenceValidationError(f"{name} refs are not canonically ordered")
    return records


def _verify_manifest(
    root: Path,
    ref: str,
    expected_digest: str,
    *,
    verify_live_targets: bool,
) -> dict[str, str]:
    raw, info = read_bytes_no_follow(root, ref)
    if not stat.S_ISREG(info.st_mode) or content_digest(raw) != expected_digest:
        raise EvidenceValidationError(f"Phase 03 entry manifest drift: {ref}")
    records = _manifest_records(raw, ref)
    if verify_live_targets:
        for logical_ref, digest in records.items():
            target_raw, target_info = read_bytes_no_follow(root, logical_ref)
            if not stat.S_ISREG(target_info.st_mode) or content_digest(target_raw) != digest:
                raise EvidenceValidationError(f"Phase 03 entry target drift: {logical_ref}")
    return records


def _load_p02_obligations(root: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw, info = read_bytes_no_follow(root, P02_OBLIGATIONS_REF)
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError("P02 obligations are not a regular file")
    value = _strict_json(raw, "P02 obligations")
    expected = {"obligation_count", "obligations", "phase", "result_round", "schema_version"}
    if set(value) != expected:
        raise EvidenceValidationError("P02 obligations top-level schema drift")
    rows = value.get("obligations")
    if not isinstance(rows, list) or value.get("obligation_count") != len(rows):
        raise EvidenceValidationError("P02 obligation count mismatch")
    obligations: list[dict[str, Any]] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict) or set(row) != {"obligation", "oracle_path"}:
            raise EvidenceValidationError(f"P02 obligation row {index} schema drift")
        obligation = row["obligation"]
        if not isinstance(obligation, dict):
            raise EvidenceValidationError(f"P02 obligation row {index} is not an object")
        _require_digest(obligation.get("obligation_digest"), f"P02 obligation {index} digest")
        obligations.append(obligation)
    return value, obligations


def _verify_obligation_sources(
    root: Path,
    obligations: list[Mapping[str, Any]],
) -> dict[str, str]:
    """Verify the live source bytes that can affect Phase 03 classifications."""
    bindings: dict[str, str] = {}
    for index, obligation in enumerate(obligations):
        document = obligation.get("document")
        if not isinstance(document, Mapping):
            raise EvidenceValidationError(f"P02 obligation {index} document is missing")
        ref = document.get("file")
        digest = document.get("source_digest")
        if not isinstance(ref, str):
            raise EvidenceValidationError(f"P02 obligation {index} source ref is missing")
        validate_logical_path(ref, name=f"P02 obligation {index} source ref")
        expected_digest = _require_digest(digest, f"P02 obligation {index} source digest")
        previous = bindings.setdefault(ref, expected_digest)
        if previous != expected_digest:
            raise EvidenceValidationError(f"P02 obligations disagree on source digest: {ref}")
    for ref, expected_digest in bindings.items():
        raw, info = read_bytes_no_follow(root, ref)
        if not stat.S_ISREG(info.st_mode) or content_digest(raw) != expected_digest:
            raise EvidenceValidationError(f"Phase 03 obligation source drift: {ref}")
    return bindings


def load_p03_scientific_inputs(root: str | os.PathLike[str] = ".") -> dict[str, Any]:
    """Load only claim-relevant P02 inputs for prospective Phase 03 work."""
    workspace = Path(root).absolute()
    decision_raw, decision_info = read_bytes_no_follow(workspace, P02_STABLE_DECISION_REF)
    if (
        not stat.S_ISREG(decision_info.st_mode)
        or content_digest(decision_raw) != P02_STABLE_DECISION_SHA256
    ):
        raise EvidenceValidationError("Phase 03 P02 stable decision binding drift")
    decision = _strict_json(decision_raw, "P02 stable decision")
    if (
        decision.get("schema_version") != "p02_final_decision@1"
        or decision.get("phase") != "P02"
        or decision.get("decision") != "pass"
        or decision.get("publication_mode") != "disabled"
        or decision.get("extraction_bundle_semantic_digest")
        != P02_EXTRACTION_BUNDLE_SEMANTIC_DIGEST
        or decision.get("primary_criterion", {}).get("all_pass") is not True
        or any(decision.get("vetoes", {}).values())
    ):
        raise EvidenceValidationError("Phase 03 P02 stable decision does not authorize context input")

    obligations_raw, obligations_info = read_bytes_no_follow(workspace, P02_OBLIGATIONS_REF)
    if (
        not stat.S_ISREG(obligations_info.st_mode)
        or content_digest(obligations_raw) != P02_OBLIGATIONS_SHA256
    ):
        raise EvidenceValidationError("Phase 03 P02 obligations binding drift")
    _, obligations = _load_p02_obligations(workspace)
    bindings = [
        {
            "adapter_eligible": item.get("adapter_eligible"),
            "extraction_state": item.get("extraction_state"),
            "obligation_digest": item.get("obligation_digest"),
        }
        for item in obligations
    ]
    if (
        len(bindings) != 17
        or len({item["obligation_digest"] for item in bindings}) != 17
        or sum(item["adapter_eligible"] is True for item in bindings) != 14
        or {
            state: sum(item["extraction_state"] == state for item in bindings)
            for state in ("ambiguous", "orphaned", "valid_complete")
        }
        != {"ambiguous": 2, "orphaned": 1, "valid_complete": 14}
        or any(
            (item["extraction_state"] == "valid_complete")
            is not (item["adapter_eligible"] is True)
            for item in bindings
        )
    ):
        raise EvidenceValidationError("Phase 03 P02 obligation partition mismatch")
    return {
        "p02_decision": decision,
        "p02_decision_sha256": P02_STABLE_DECISION_SHA256,
        "p02_obligations_sha256": P02_OBLIGATIONS_SHA256,
        "obligations": obligations,
        "ordered_obligation_bindings": bindings,
        "scientific_source_bindings": _verify_obligation_sources(workspace, obligations),
    }


def verify_p03_entry(root: str | os.PathLike[str] = ".") -> dict[str, Any]:
    workspace = Path(root).absolute()
    entry_dir = workspace / P03_ENTRY_ROOT_REF
    if entry_dir.is_symlink() or not entry_dir.is_dir():
        raise EvidenceValidationError("Phase 03 recovery entry root is unavailable or unsafe")
    discovered = {path.name for path in entry_dir.iterdir()}
    if discovered != ENTRY_FILE_NAMES or any(path.is_symlink() or not path.is_file() for path in entry_dir.iterdir()):
        raise EvidenceValidationError("Phase 03 recovery entry must contain exactly five regular files")
    raw, info = read_bytes_no_follow(workspace, P03_ENTRY_RECORD_REF)
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError("Phase 03 entry record is not regular")
    record = _strict_json(raw, "Phase 03 entry record")
    required = {
        "schema_version": "p03_entry_record@2",
        "phase": "P03",
        "publication_mode": "disabled",
        "device_mode": "cpu_only_no_gpu_requested",
    }
    if any(record.get(key) != value for key, value in required.items()):
        raise EvidenceValidationError("Phase 03 entry record boundary mismatch")
    bindings = record.get("p02_ordered_obligation_bindings")
    if not isinstance(bindings, list) or len(bindings) != 17:
        raise EvidenceValidationError("Phase 03 entry does not bind 17 P02 obligations")
    if sum(item.get("adapter_eligible") is True for item in bindings if isinstance(item, dict)) != 14:
        raise EvidenceValidationError("Phase 03 entry adapter-eligible partition mismatch")
    if record.get("p02_obligation_state_counts") != {"ambiguous": 2, "orphaned": 1, "valid_complete": 14}:
        raise EvidenceValidationError("Phase 03 entry extraction-state partition mismatch")
    manifest_specs = (
        (
            record["implementation_entry_manifest_ref"],
            record["implementation_entry_manifest_sha256"],
            False,
        ),
        (record["protected_entry_manifest_ref"], record["protected_entry_manifest_sha256"], False),
        (record["immutable_input_manifest_ref"], record["immutable_input_manifest_sha256"], False),
    )
    manifests = {
        ref: _verify_manifest(
            workspace,
            ref,
            _require_digest(digest, f"{ref} digest"),
            verify_live_targets=verify_live_targets,
        )
        for ref, digest, verify_live_targets in manifest_specs
    }
    p02_raw, _ = read_bytes_no_follow(workspace, P02_OBLIGATIONS_REF)
    p02_digest = content_digest(p02_raw)
    if (
        p02_digest != P02_OBLIGATIONS_SHA256
        or p02_digest != record.get("p02_obligations_sha256")
    ):
        raise EvidenceValidationError("Phase 03 entry P02 obligations binding drift")
    _, obligations = _load_p02_obligations(workspace)
    scientific_source_bindings = _verify_obligation_sources(workspace, obligations)
    live_bindings = [
        {
            "adapter_eligible": item.get("adapter_eligible"),
            "extraction_state": item.get("extraction_state"),
            "obligation_digest": item.get("obligation_digest"),
        }
        for item in obligations
    ]
    if live_bindings != bindings:
        raise EvidenceValidationError("Phase 03 entry ordered P02 obligation binding drift")
    return {
        "record": record,
        "sha256": content_digest(raw),
        "manifests": manifests,
        "obligations": obligations,
        "scientific_source_bindings": scientific_source_bindings,
    }


def _exact_ref(value: Any, name: str) -> dict[str, Any]:
    keys = {
        "file",
        "source_digest",
        "byte_span",
        "line_span",
        "enclosing_node_id",
        "dependency_path",
        "applicability_reason",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise EvidenceValidationError(f"{name} keys mismatch")
    validate_logical_path(value["file"], name=f"{name}.file")
    _require_digest(value["source_digest"], f"{name}.source_digest")
    for span_name, minimum in (("byte_span", 0), ("line_span", 1)):
        span = value[span_name]
        if not isinstance(span, dict) or set(span) != {"start", "end"}:
            raise EvidenceValidationError(f"{name}.{span_name} keys mismatch")
        if type(span["start"]) is not int or type(span["end"]) is not int:
            raise EvidenceValidationError(f"{name}.{span_name} must contain integers")
        if span["start"] < minimum or span["end"] < span["start"]:
            raise EvidenceValidationError(f"{name}.{span_name} is invalid")
    if value["byte_span"]["end"] <= value["byte_span"]["start"]:
        raise EvidenceValidationError(f"{name}.byte_span must be non-empty")
    if not isinstance(value["dependency_path"], list) or not value["dependency_path"]:
        raise EvidenceValidationError(f"{name}.dependency_path must be non-empty")
    for key in ("enclosing_node_id", "applicability_reason"):
        if not isinstance(value[key], str) or not value[key]:
            raise EvidenceValidationError(f"{name}.{key} must be non-empty")
    return value


def _validate_search_manifest(value: dict[str, Any]) -> None:
    keys = {
        "schema_version",
        "phase",
        "entry_state",
        "obligation_digest",
        "p02_extraction_state",
        "p02_adapter_eligible",
        "p02_label",
        "entry_source_digest",
        "corpus_graph_digest",
        "context_request",
        "context_request_digest",
        "searched_files",
        "searched_nodes",
        "searched_edges",
        "searched_counts",
        "unsearched_files",
        "unsearched_node_count",
        "unsearched_edge_count",
        "budget_exhausted",
        "candidates",
        "semantic_candidates",
        "typed_assumptions",
        "symbol_resolutions",
        "terminal_state",
        "engineering_diagnostics",
        "integrity_vetoes",
        "legacy_context_status",
        "non_claims",
        "manifest_digest",
    }
    if set(value) != keys:
        raise EvidenceValidationError(
            f"context-search manifest keys mismatch: missing={sorted(keys - set(value))}, extra={sorted(set(value) - keys)}"
        )
    if value["p02_extraction_state"] != "valid_complete" or value["p02_adapter_eligible"] is not True:
        raise EvidenceValidationError("context search requires a valid, adapter-eligible P02 obligation")
    request = value["context_request"]
    if not isinstance(request, dict) or request.get("obligation_digest") != value["obligation_digest"]:
        raise EvidenceValidationError("context search request binding mismatch")
    if request.get("entry_source_digest") != value["entry_source_digest"]:
        raise EvidenceValidationError("context search source binding mismatch")
    expected_request_digest = content_digest(
        [
            request["obligation_digest"],
            value["corpus_graph_digest"],
            request["requirement_predicate"],
            request["required_edge_kinds"],
            request["budget"],
        ]
    )
    if value["context_request_digest"] != expected_request_digest:
        raise EvidenceValidationError("context request digest mismatch")
    if value["candidates"] != value["semantic_candidates"]:
        raise EvidenceValidationError("semantic candidate projection mismatch")
    if value["terminal_state"] not in {
        "stated",
        "source_supported",
        "ambiguous",
        "not_found_after_search",
        "not_searched",
        "candidate_assumption",
    }:
        raise EvidenceValidationError("context terminal state is invalid")
    if type(value["budget_exhausted"]) is not bool:
        raise EvidenceValidationError("context budget_exhausted must be boolean")
    if value["terminal_state"] == "not_found_after_search" and (
        value["budget_exhausted"]
        or value["unsearched_files"]
        or value["unsearched_node_count"]
        or value["unsearched_edge_count"]
        or value["engineering_diagnostics"]
        or value["integrity_vetoes"]
    ):
        raise EvidenceValidationError("not_found_after_search requires complete, unvetoed search")
    if value["terminal_state"] in {"stated", "source_supported"}:
        supported = [item for item in value["candidates"] if item.get("applicability_state") == "explicit"]
        if not supported:
            raise EvidenceValidationError("source-supported context requires an explicit candidate")
        for index, candidate in enumerate(supported):
            _exact_ref(candidate.get("source_ref"), f"candidate[{index}].source_ref")
    legacy = value["legacy_context_status"]
    if not isinstance(legacy, dict) or legacy.get("diagnostic") is not True or legacy.get("deprecated") is not True:
        raise EvidenceValidationError("legacy context status is not quarantined")


def _validate_extraction_veto(value: dict[str, Any]) -> None:
    keys = {
        "schema_version",
        "phase",
        "entry_state",
        "obligation_digest",
        "p02_extraction_state",
        "p02_adapter_eligible",
        "p02_label",
        "p02_source_digest",
        "p02_ambiguities",
        "searched_counts",
        "semantic_candidates",
        "typed_assumptions",
        "symbol_resolutions",
        "engineering_diagnostics",
        "integrity_vetoes",
        "non_claims",
        "manifest_digest",
    }
    if set(value) != keys:
        raise EvidenceValidationError("extraction-veto manifest keys mismatch")
    if value["p02_adapter_eligible"] is not False or value["p02_extraction_state"] not in {"ambiguous", "orphaned"}:
        raise EvidenceValidationError("extraction-veto manifest P02 state mismatch")
    if value["searched_counts"] != {"files": 0, "nodes": 0, "edges": 0, "bytes": 0}:
        raise EvidenceValidationError("extraction-veto manifest performed semantic traversal")
    if any(value[key] for key in ("semantic_candidates", "typed_assumptions", "symbol_resolutions")):
        raise EvidenceValidationError("extraction-veto manifest contains semantic output")


def validate_context_manifest(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise EvidenceValidationError("context manifest must be an object")
    if value.get("schema_version") != SEARCH_SCHEMA_VERSION or value.get("phase") != "P03":
        raise EvidenceValidationError("context manifest schema/phase mismatch")
    _require_digest(value.get("obligation_digest"), "context manifest obligation digest")
    if value.get("entry_state") == "context_search":
        _validate_search_manifest(value)
    elif value.get("entry_state") == "extraction_veto":
        _validate_extraction_veto(value)
    else:
        raise EvidenceValidationError("context manifest entry_state is invalid")
    expected = content_digest({key: child for key, child in value.items() if key != "manifest_digest"})
    if value.get("manifest_digest") != expected:
        raise EvidenceValidationError("context manifest digest mismatch")
    return value


def build_extraction_veto_manifest(obligation: Mapping[str, Any]) -> dict[str, Any]:
    if obligation.get("adapter_eligible") is not False or obligation.get("extraction_state") not in {"ambiguous", "orphaned"}:
        raise EvidenceValidationError("only ambiguous/orphaned obligations may produce extraction vetoes")
    document = obligation.get("document")
    if not isinstance(document, Mapping):
        raise EvidenceValidationError("P02 obligation document is missing")
    result = {
        "schema_version": SEARCH_SCHEMA_VERSION,
        "phase": "P03",
        "entry_state": "extraction_veto",
        "obligation_digest": obligation["obligation_digest"],
        "p02_extraction_state": obligation["extraction_state"],
        "p02_adapter_eligible": False,
        "p02_label": obligation.get("label"),
        "p02_source_digest": document.get("source_digest"),
        "p02_ambiguities": list(obligation.get("ambiguities", [])),
        "searched_counts": {"files": 0, "nodes": 0, "edges": 0, "bytes": 0},
        "semantic_candidates": [],
        "typed_assumptions": [],
        "symbol_resolutions": [],
        "engineering_diagnostics": [],
        "integrity_vetoes": [],
        "non_claims": [
            "Extraction ambiguity or orphaning is not a mathematical gap.",
            "No semantic traversal, symbol resolution, or assumption inference was performed.",
        ],
    }
    result["manifest_digest"] = content_digest(result)
    return validate_context_manifest(result)


def _obligation_budget(obligation: Mapping[str, Any]) -> dict[str, int]:
    source_digest = obligation.get("document", {}).get("source_digest")
    return dict(_FROZEN_BUDGETS.get(source_digest, _DEFAULT_BUDGET))


def _obligation_request(obligation: Mapping[str, Any], graph: Mapping[str, Any]) -> dict[str, Any]:
    inventory = obligation.get("symbol_inventory") if isinstance(obligation.get("symbol_inventory"), Mapping) else {}
    symbols = [
        str(item)
        for key in ("bare_identifiers", "latex_commands")
        for item in inventory.get(key, [])
        if isinstance(item, str) and item
    ]
    label = str(obligation.get("label") or obligation.get("obligation_id"))
    subjects = [label, *symbols[:8]]
    subjects = list(dict.fromkeys(subjects))
    return {
        "obligation_digest": obligation["obligation_digest"],
        "entry_source_digest": graph["entry_source_digest"],
        "requirement_id": f"context_for_{obligation['obligation_digest']}",
        "requirement_predicate": (
            f"Source declarations explicitly applicable to {label} and its scoped notation are available."
        ),
        "requirement_subjects": subjects,
        "required_node_kinds": ["definition", "assumption", "notation_declaration", "proposition"],
        "required_edge_kinds": ["input", "include", "contains", "references"],
        "required_files": [],
        "budget": _obligation_budget(obligation),
    }


def _symbol_ledger_entry(obligation: Mapping[str, Any], graph: Mapping[str, Any], manifest: Mapping[str, Any]) -> dict[str, Any]:
    inventory = obligation.get("symbol_inventory") if isinstance(obligation.get("symbol_inventory"), Mapping) else {}
    symbols = [
        str(item)
        for key in ("bare_identifiers", "latex_commands")
        for item in inventory.get(key, [])
        if isinstance(item, str) and item
    ]
    symbols = list(dict.fromkeys(symbols))
    document = obligation["document"]
    scope = {
        "entry_source_digest": document["source_digest"],
        "file": document["file"],
        "label": str(obligation.get("label") or obligation["obligation_id"]),
        "obligation_digest": obligation["obligation_digest"],
    }
    evidence: list[dict[str, Any]] = []
    file_ids = {
        node["source_file"]: node["id"]
        for node in graph["nodes"]
        if node["kind"] == "file"
    }
    paths: dict[str, list[str]] = {graph["entry_ref"]: [file_ids[graph["entry_ref"]]]}
    pending = [graph["entry_ref"]]
    while pending:
        source_file = pending.pop(0)
        for edge in graph["edges"]:
            if edge["kind"] not in {"input", "include"} or edge["source_file"] != source_file:
                continue
            target_file = edge["target_file"]
            if target_file in paths or target_file not in file_ids:
                continue
            paths[target_file] = [*paths[source_file], edge["id"], file_ids[target_file]]
            pending.append(target_file)
    for node in graph["nodes"]:
        if node["kind"] != "notation_declaration":
            continue
        source = node["source_text"]
        declared_symbol = str(node.get("declaration_key", "")).split(":", 1)[0]
        matched_symbol = next((symbol for symbol in symbols if symbol == declared_symbol), None)
        if matched_symbol is None:
            continue
        lowered = source.lower()
        role = "policy_candidate" if "policy" in lowered else "posterior_candidate" if "posterior" in lowered else "unknown"
        if role == "unknown":
            continue
        path = paths.get(node["source_file"], [])
        contains_edge = next(
            (
                edge["id"]
                for edge in graph["edges"]
                if edge["kind"] == "contains" and edge["to_node_id"] == node["id"]
            ),
            None,
        )
        full_path = [*path]
        if contains_edge:
            full_path.extend([contains_edge, node["id"]])
        source_ref = {
            "file": node["source_file"],
            "source_digest": node["source_digest"],
            "byte_span": dict(node["byte_span"]),
            "line_span": dict(node["line_span"]),
            "enclosing_node_id": node["id"],
            "dependency_path": full_path or [node["id"]],
            "applicability_reason": "The exact scoped declaration names the symbol and its role.",
        }
        evidence.append(
            {
                "symbol": matched_symbol,
                "proposed_role": role,
                "scope": scope,
                "evidence_kind": "exact_declaration",
                "source_refs": [source_ref],
                "applicability_reason": "The exact scoped declaration names the symbol and its role.",
            }
        )
    resolution = resolve_symbol_roles(
        symbols,
        scope=scope,
        evidence_records=evidence,
        search_state=manifest["terminal_state"],
    )
    return {"obligation_digest": obligation["obligation_digest"], **resolution}


def build_context_only_packet(
    *,
    obligation_digest: str,
    parser_extraction: list[dict[str, Any]],
    context_search: list[dict[str, Any]],
    symbol_notation: list[dict[str, Any]],
    source_assumptions: list[dict[str, Any]],
    candidate_assumptions: list[dict[str, Any]],
    mathematical_requirements: list[dict[str, Any]],
    encoding_blockers: list[dict[str, Any]],
    engineering: list[dict[str, Any]],
    interpretation: list[dict[str, Any]],
) -> dict[str, Any]:
    _require_digest(obligation_digest, "context-only packet obligation_digest")
    values = {
        "parser_extraction": parser_extraction,
        "context_search": context_search,
        "symbol_notation": symbol_notation,
        "source_assumptions": source_assumptions,
        "candidate_assumptions": candidate_assumptions,
        "mathematical_requirements": mathematical_requirements,
        "encoding_blockers": encoding_blockers,
        "backend_evidence": [],
        "engineering": engineering,
        "interpretation": interpretation,
    }
    for name, items in values.items():
        if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
            raise EvidenceValidationError(f"context-only lane {name} must be a list of objects")
    veto_ids = [
        str(item["id"])
        for item in engineering
        if item.get("affected") is True and isinstance(item.get("id"), str) and item["id"]
    ]
    packet = {
        "schema_version": "p03_context_only_packet@1",
        "obligation_digest": obligation_digest,
        "report_state_ledgers": values,
        "routing_eligible": not veto_ids,
        "routing_veto_ids": veto_ids,
        "legacy_context_status": {
            "diagnostic": True,
            "deprecated": True,
            "values": [],
        },
        "non_claims": [
            "The packet contains no backend evidence or mathematical certification.",
            "Engineering vetoes are not mathematical gaps or refutations.",
        ],
    }
    packet["packet_digest"] = content_digest(packet)
    return validate_context_only_packet(packet)


def validate_context_only_packet(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version",
        "obligation_digest",
        "report_state_ledgers",
        "routing_eligible",
        "routing_veto_ids",
        "legacy_context_status",
        "non_claims",
        "packet_digest",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise EvidenceValidationError("context-only packet keys mismatch")
    if value["schema_version"] != "p03_context_only_packet@1":
        raise EvidenceValidationError("context-only packet schema mismatch")
    _require_digest(value["obligation_digest"], "context-only packet obligation_digest")
    ledgers = value["report_state_ledgers"]
    if not isinstance(ledgers, dict) or tuple(ledgers) != CONTEXT_PACKET_LANES:
        raise EvidenceValidationError("context-only packet ledger order/schema mismatch")
    for lane, entries in ledgers.items():
        if not isinstance(entries, list) or any(not isinstance(item, dict) for item in entries):
            raise EvidenceValidationError(f"context-only packet lane {lane} is invalid")
    if ledgers["backend_evidence"]:
        raise EvidenceValidationError("P03 context-only backend evidence must be empty")
    if type(value["routing_eligible"]) is not bool:
        raise EvidenceValidationError("context-only routing_eligible must be boolean")
    affected = [
        str(item["id"])
        for item in ledgers["engineering"]
        if item.get("affected") is True and isinstance(item.get("id"), str) and item["id"]
    ]
    if value["routing_veto_ids"] != affected or value["routing_eligible"] != (not affected):
        raise EvidenceValidationError("context-only engineering veto projection mismatch")
    if value["legacy_context_status"] != {
        "diagnostic": True,
        "deprecated": True,
        "values": [],
    }:
        raise EvidenceValidationError("context-only legacy projection is not quarantined")
    expected = content_digest({key: child for key, child in value.items() if key != "packet_digest"})
    if value["packet_digest"] != expected:
        raise EvidenceValidationError("context-only packet digest mismatch")
    return value


def compact_context_only_packet(value: Any) -> dict[str, Any]:
    packet = validate_context_only_packet(value)
    ledgers = packet["report_state_ledgers"]
    return {
        "schema_version": "p03_context_only_compact@1",
        "obligation_digest": packet["obligation_digest"],
        "routing_eligible": packet["routing_eligible"],
        "routing_veto_ids": list(packet["routing_veto_ids"]),
        "lane_entries": {
            lane: [
                {
                    key: item[key]
                    for key in ("id", "state", "kind", "support_state", "encoding_state", "text")
                    if key in item
                }
                for item in entries
            ]
            for lane, entries in ledgers.items()
        },
        "non_claims": list(packet["non_claims"]),
        "source_packet_digest": packet["packet_digest"],
    }


def render_context_only_packet_markdown(value: Any) -> str:
    packet = validate_context_only_packet(value)
    headings = {
        "parser_extraction": "Extraction And Parser State",
        "context_search": "Context Search State",
        "symbol_notation": "Symbol And Notation State",
        "source_assumptions": "Source-Supported Assumptions",
        "candidate_assumptions": "Candidate Assumptions",
        "mathematical_requirements": "Mathematical Requirements",
        "encoding_blockers": "Encoding And Formalization Blockers",
        "backend_evidence": "Backend Evidence",
        "engineering": "Context Engineering Diagnostics",
        "interpretation": "Interpretation And Non-Claims",
    }
    lines = [
        "# Context-Only Evidence Packet",
        "",
        f"Obligation digest: `{packet['obligation_digest']}`",
        "",
        f"Routing eligible: `{str(packet['routing_eligible']).lower()}`",
        "",
    ]
    for lane, entries in packet["report_state_ledgers"].items():
        lines.extend([f"## {headings[lane]}", ""])
        if not entries:
            lines.extend(["- None recorded.", ""])
            continue
        for entry in entries:
            identifier = str(entry.get("id", "unidentified"))
            state = str(entry.get("state") or entry.get("support_state") or entry.get("kind") or "recorded")
            if state == "not_searched":
                description = "not searched; no absence or missing-assumption claim is made"
            elif lane == "candidate_assumptions":
                description = "candidate only; not stated or source-supported"
            elif lane == "engineering":
                description = "engineering diagnostic; not a mathematical gap or refutation"
            elif lane == "parser_extraction":
                description = "parser/extraction state; not a mathematical gap"
            else:
                description = str(entry.get("text") or entry.get("predicate") or entry.get("description") or "recorded")
            lines.append(f"- `{identifier}` state `{state}`: {description}")
        lines.append("")
    lines.extend(["## Routing Boundary", ""])
    if packet["routing_veto_ids"]:
        lines.append(f"- Context engineering vetoes apply before mathematical/backend routing: `{packet['routing_veto_ids']}`")
    else:
        lines.append("- No affected context engineering veto is recorded.")
    lines.extend(["", "## Non-Claims", ""])
    lines.extend(f"- {item}" for item in packet["non_claims"])
    lines.append("")
    return "\n".join(lines)


def build_context_evidence_payload(root: str | os.PathLike[str] = ".") -> dict[str, Any]:
    workspace = Path(root).absolute()
    inputs = load_p03_scientific_inputs(workspace)
    obligations = inputs["obligations"]
    manifests: list[dict[str, Any]] = []
    symbol_entries: list[dict[str, Any]] = []
    graph_summaries: list[dict[str, Any]] = []
    unique_graphs: dict[str, dict[str, Any]] = {}
    typed_assumption_records: list[dict[str, Any]] = []
    engineering_items: list[dict[str, Any]] = []
    for obligation in obligations:
        if obligation["adapter_eligible"] is not True:
            manifest = build_extraction_veto_manifest(obligation)
            manifests.append(manifest)
            continue
        document = obligation["document"]
        graph = build_context_dependency_graph(
            workspace,
            document["file"],
            expected_entry_source_digest=document["source_digest"],
            budget=_obligation_budget(obligation),
        )
        unique_graphs.setdefault(graph["graph_digest"], graph)
        manifest = resolve_context_requirement(graph, obligation, _obligation_request(obligation, graph))
        support_state = manifest["terminal_state"]
        exact_refs = [
            item["source_ref"]
            for item in manifest["candidates"]
            if item.get("applicability_state") == "explicit"
        ]
        assumption = build_typed_assumption(
            predicate=manifest["context_request"]["requirement_predicate"],
            formal_predicate=None,
            kind="context_requirement",
            subjects=manifest["context_request"]["requirement_subjects"],
            support_state=support_state,
            source_refs=exact_refs[:1] if support_state in {"stated", "source_supported"} else [],
            encoding_state="not_yet_encoded" if support_state in {"stated", "source_supported"} else "not_applicable",
            closes_blocker_ids=[manifest["context_request"]["requirement_id"]],
            search_completed=True if support_state == "not_found_after_search" else None,
        )
        manifest["typed_assumptions"] = [assumption]
        manifest["manifest_digest"] = content_digest(
            {key: child for key, child in manifest.items() if key != "manifest_digest"}
        )
        validate_context_manifest(manifest)
        manifests.append(manifest)
        typed_assumption_records.append(assumption)
        symbol_entries.append(_symbol_ledger_entry(obligation, graph, manifest))
        graph_summaries.append(
            {
                "entry_ref": graph["entry_ref"],
                "entry_source_digest": graph["entry_source_digest"],
                "graph_digest": graph["graph_digest"],
                "reachable_files": graph["reachable_files"],
                "excluded_sibling_file_count": len(graph["excluded_sibling_files"]),
                "diagnostic_kinds": [item["kind"] for item in graph["diagnostics"]],
            }
        )
        engineering_items.extend(
            {
                "id": f"eng_{content_digest([obligation['obligation_digest'], item])}",
                "obligation_digest": obligation["obligation_digest"],
                "affected": item in manifest["engineering_diagnostics"],
                **item,
            }
            for item in graph["diagnostics"]
        )
    ordered = [item["obligation_digest"] for item in manifests]
    expected = [item["obligation_digest"] for item in inputs["ordered_obligation_bindings"]]
    if ordered != expected:
        raise EvidenceValidationError("context evidence does not preserve P02 obligation order")
    if sum(item["entry_state"] == "context_search" for item in manifests) != 14:
        raise EvidenceValidationError("context evidence does not contain exactly 14 searches")
    if sum(item["entry_state"] == "extraction_veto" for item in manifests) != 3:
        raise EvidenceValidationError("context evidence does not contain exactly three extraction vetoes")
    frozen_entries = {
        "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8",
        "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1",
    }
    frozen_graphs = [item for item in graph_summaries if item["entry_source_digest"] in frozen_entries]
    parser_entries = [
        {
            "obligation_digest": obligation["obligation_digest"],
            "extraction_state": obligation["extraction_state"],
            "adapter_eligible": obligation["adapter_eligible"],
            "source_file": obligation["document"]["file"],
            "source_digest": obligation["document"]["source_digest"],
            "label": obligation.get("label"),
        }
        for obligation in obligations
    ]
    notation_entries = [
        {
            "obligation_digest": item["obligation_digest"],
            "candidate_ids": [candidate["candidate_id"] for candidate in item["candidates"]],
            "ambiguous_symbols": [
                resolution["symbol"]
                for resolution in item["resolutions"]
                if resolution["state"] == "ambiguous"
            ],
            "unresolved_symbols": [
                resolution["symbol"]
                for resolution in item["resolutions"]
                if resolution["state"] in {"candidate", "unknown", "not_searched"}
            ],
        }
        for item in symbol_entries
    ]
    payload = {
        "manifests": manifests,
        "corpus_graphs": {
            "schema_version": "p03_corpus_graph_collection@1",
            "graphs": [unique_graphs[key] for key in sorted(unique_graphs)],
        },
        "symbol_resolution_ledger": {
            "schema_version": "p03_symbol_resolution_ledger@1",
            "entries": symbol_entries,
        },
        "notation_conflict_ledger": {
            "schema_version": "p03_notation_conflict_ledger@1",
            "entries": notation_entries,
            "conflicts": [
                {
                    "obligation_digest": item["obligation_digest"],
                    "symbols": item["ambiguous_symbols"],
                }
                for item in notation_entries
                if item["ambiguous_symbols"]
            ],
            "non_claim": "No conflict count establishes semantic equivalence.",
        },
        "typed_assumptions": {
            "schema_version": "p03_typed_assumption_bundle@1",
            "assumptions": typed_assumption_records,
            "non_claim": "No assumption in this bundle is proved sufficient.",
        },
        "ledgers": {
            "parser": {"schema_version": "p03_parser_ledger@1", "entries": parser_entries},
            "context": {
                "schema_version": "p03_context_ledger@1",
                "entries": [
                    {
                        "obligation_digest": item["obligation_digest"],
                        "entry_state": item["entry_state"],
                        "terminal_state": item.get("terminal_state"),
                    }
                    for item in manifests
                ],
            },
            "mathematical": {"schema_version": "p03_mathematical_ledger@1", "entries": []},
            "engineering": {"schema_version": "p03_engineering_ledger@1", "entries": engineering_items},
            "interpretation": {
                "schema_version": "p03_interpretation_ledger@1",
                "entries": [
                    {"id": "no-proof", "text": "Context evidence is not mathematical proof."},
                    {"id": "no-completeness", "text": "Search completeness is budget scoped."},
                ],
            },
        },
        "frozen_regressions": {
            "schema_version": "p03_frozen_context_regressions@1",
            "entries": frozen_graphs,
            "all_entries_single_reachable_file": all(len(item["reachable_files"]) == 1 for item in frozen_graphs),
        },
    }
    payload["mutation_matrix"] = build_p03_mutation_matrix(payload)
    validate_context_evidence_payload(payload, expected_bindings=inputs["ordered_obligation_bindings"])
    return payload


def _mutation_result(mutation_id: str, *, detected: bool, mechanism: str) -> dict[str, Any]:
    return {
        "mutation_id": mutation_id,
        "single_field_or_fact": True,
        "expected_outcome": "rejected_or_downgraded",
        "observed_outcome": "rejected_or_downgraded" if detected else "silently_accepted",
        "detected": detected,
        "mechanism": mechanism,
    }


def build_p03_mutation_matrix(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Execute the reviewed one-fact mutations against phase-local validators."""
    manifests = payload["manifests"]
    search = next(item for item in manifests if item["entry_state"] == "context_search")
    assumption = payload["typed_assumptions"]["assumptions"][0]
    results: list[dict[str, Any]] = []

    mutated = deepcopy(search)
    mutated["entry_source_digest"] = "0" * 64
    mutated["manifest_digest"] = content_digest({key: value for key, value in mutated.items() if key != "manifest_digest"})
    results.append(
        _mutation_result(
            "source_digest",
            detected=_rejects(lambda: validate_context_manifest(mutated)),
            mechanism="request/entry source binding validator",
        )
    )

    graph = next(
        item
        for item in payload["corpus_graphs"]["graphs"]
        if item["graph_digest"] == search["corpus_graph_digest"]
    )
    node = graph["nodes"][0]
    exact_ref = {
        "file": node["source_file"],
        "source_digest": node["source_digest"],
        "byte_span": dict(node["byte_span"]),
        "line_span": dict(node["line_span"]),
        "enclosing_node_id": node["id"],
        "dependency_path": [node["id"]],
        "applicability_reason": "Synthetic validator probe bound to one graph node.",
    }
    mutated_ref = deepcopy(exact_ref)
    mutated_ref["byte_span"]["start"] = None
    results.append(
        _mutation_result(
            "source_span",
            detected=_rejects(lambda: _exact_ref(mutated_ref, "mutation source ref")),
            mechanism="exact source-ref span validator",
        )
    )
    mutated_ref = deepcopy(exact_ref)
    mutated_ref["dependency_path"] = []
    results.append(
        _mutation_result(
            "dependency_edge",
            detected=_rejects(lambda: _exact_ref(mutated_ref, "mutation source ref")),
            mechanism="non-empty dependency-path validator",
        )
    )

    mutated = deepcopy(search)
    mutated["context_request"]["budget"]["max_nodes"] = max(
        1, mutated["searched_counts"]["nodes"] - 1
    )
    mutated["context_request_digest"] = content_digest(
        [
            mutated["context_request"]["obligation_digest"],
            mutated["corpus_graph_digest"],
            mutated["context_request"]["requirement_predicate"],
            mutated["context_request"]["required_edge_kinds"],
            mutated["context_request"]["budget"],
        ]
    )
    mutated["manifest_digest"] = content_digest({key: value for key, value in mutated.items() if key != "manifest_digest"})
    results.append(
        _mutation_result(
            "unsearched_boundary",
            detected=_rejects(
                lambda: _validate_search_boundary_against_graph(mutated, graph)
            ),
            mechanism="graph-bound budget/count/closure projection validator",
        )
    )

    keyword_candidate = {
        "node_id": node["id"],
        "priority_class": "dependency_linked_use",
        "lexical_evidence": ["keyword"],
        "subject_evidence": [],
        "applicability_state": "explicit",
        "applicability_reason": "Keyword overlap only.",
        "dependency_path": [node["id"]],
        "source_ref": {**exact_ref, "applicability_reason": "Keyword overlap only."},
        "target_span_match": False,
    }
    results.append(
        _mutation_result(
            "keyword_promotion",
            detected=_rejects(
                lambda: _validate_candidate_against_graph(
                    keyword_candidate,
                    graph,
                    request=search["context_request"],
                )
            ),
            mechanism="manifest/graph applicability reconstruction",
        )
    )

    mutated = deepcopy(assumption)
    mutated["support_state"] = "stated"
    results.append(
        _mutation_result(
            "candidate_assumption_promotion",
            detected=_rejects(lambda: validate_typed_assumption(mutated)),
            mechanism="typed-assumption source-ref and binding validator",
        )
    )

    card = next(
        item
        for item in payload["symbol_resolution_ledger"]["entries"]
        if any(resolution["symbol"] == r"\pi" for resolution in item["resolutions"])
    )
    mutated = deepcopy(card)
    pi = next(item for item in mutated["resolutions"] if item["symbol"] == r"\pi")
    pi["state"] = "resolved"
    pi["role"] = "posterior_candidate"
    results.append(
        _mutation_result(
            "pi_role",
            detected=_rejects(lambda: validate_symbol_resolution_ledger({"schema_version": "p03_symbol_resolution_ledger@1", "entries": [mutated]})),
            mechanism="resolution/candidate consistency validator",
        )
    )

    mutated = deepcopy(card)
    candidate_entry = next(item for item in mutated["candidates"] if item["symbol"] == r"\pi")
    candidate_entry["scope"]["file"] += ".widened"
    results.append(
        _mutation_result(
            "override_scope",
            detected=_rejects(
                lambda: validate_symbol_resolution_ledger(
                    {"schema_version": "p03_symbol_resolution_ledger@1", "entries": [mutated]}
                )
            ),
            mechanism="symbol candidate identity binds exact scope",
        )
    )

    mutated = deepcopy(assumption)
    mutated["encoding_state"] = "not_encodable" if assumption["encoding_state"] != "not_encodable" else "not_applicable"
    results.append(
        _mutation_result(
            "assumption_binding",
            detected=_rejects(lambda: validate_typed_assumption(mutated)),
            mechanism="typed-assumption binding digest",
        )
    )

    synthetic = {"id": "eng_mutation", "kind": "missing_include", "affected": True}
    mutated_ledgers = deepcopy(payload["ledgers"])
    mutated_ledgers["mathematical"]["entries"].append(synthetic)
    results.append(
        _mutation_result(
            "engineering_lane",
            detected=_rejects(lambda: validate_evidence_ledgers(mutated_ledgers, manifests=manifests)),
            mechanism="closed report-lane validator",
        )
    )

    nonzero_guard = {
        "schema_version": "p03_guard_index@1",
        "actions": list(P03_GUARDED_ACTIONS),
        "entries": [
            {
                "action": action,
                "attestation_ref": f"synthetic/{action}.attestation.json",
                "attestation_sha256": "1" * 64,
                "ledger_ref": f"synthetic/{action}.ledger.jsonl",
                "ledger_sha256": "2" * 64,
            }
            for action in P03_GUARDED_ACTIONS
        ],
        "forbidden_attempt_count": 0,
        "guard_replacement_errors": [],
        "backend_request_count": 1,
        "source_edit_count": 0,
        "publication_count": 0,
    }
    results.append(
        _mutation_result(
            "publication_backend_count",
            detected=_rejects(lambda: validate_guard_index(nonzero_guard)),
            mechanism="zero-count guard-index validator",
        )
    )
    matrix = {
        "schema_version": "p03_mutation_matrix@2",
        "required_mutations": list(P03_MUTATION_IDS),
        "results": results,
        "all_pass": all(item["detected"] for item in results),
    }
    return validate_p03_mutation_matrix(matrix)


def _rejects(operation: Any) -> bool:
    try:
        operation()
    except (EvidenceValidationError, KeyError, TypeError, ValueError):
        return True
    return False


def validate_p03_mutation_matrix(value: Any) -> dict[str, Any]:
    keys = {"schema_version", "required_mutations", "results", "all_pass"}
    if not isinstance(value, dict) or set(value) != keys:
        raise EvidenceValidationError("Phase 03 mutation matrix keys mismatch")
    if value["schema_version"] != "p03_mutation_matrix@2":
        raise EvidenceValidationError("Phase 03 mutation matrix schema mismatch")
    if value["required_mutations"] != list(P03_MUTATION_IDS):
        raise EvidenceValidationError("Phase 03 mutation registry mismatch")
    results = value["results"]
    if not isinstance(results, list) or len(results) != len(P03_MUTATION_IDS):
        raise EvidenceValidationError("Phase 03 mutation result count mismatch")
    observed_ids: list[str] = []
    for result in results:
        expected_keys = {
            "mutation_id",
            "single_field_or_fact",
            "expected_outcome",
            "observed_outcome",
            "detected",
            "mechanism",
        }
        if not isinstance(result, dict) or set(result) != expected_keys:
            raise EvidenceValidationError("Phase 03 mutation result keys mismatch")
        observed_ids.append(result["mutation_id"])
        if (
            result["single_field_or_fact"] is not True
            or result["expected_outcome"] != "rejected_or_downgraded"
            or type(result["detected"]) is not bool
            or result["observed_outcome"]
            != ("rejected_or_downgraded" if result["detected"] else "silently_accepted")
            or not isinstance(result["mechanism"], str)
            or not result["mechanism"]
        ):
            raise EvidenceValidationError("Phase 03 mutation result is inconsistent")
    if observed_ids != list(P03_MUTATION_IDS):
        raise EvidenceValidationError("Phase 03 mutation result order mismatch")
    if value["all_pass"] != all(item["detected"] for item in results):
        raise EvidenceValidationError("Phase 03 mutation summary is not derived")
    if value["all_pass"] is not True:
        raise EvidenceValidationError("Phase 03 mutation matrix contains a surviving mutation")
    return value


def _validate_graph_collection(value: Any) -> dict[str, dict[str, Any]]:
    if not isinstance(value, dict) or set(value) != {"schema_version", "graphs"}:
        raise EvidenceValidationError("Phase 03 corpus graph collection keys mismatch")
    if value["schema_version"] != "p03_corpus_graph_collection@1" or not isinstance(value["graphs"], list):
        raise EvidenceValidationError("Phase 03 corpus graph collection schema mismatch")
    graphs: dict[str, dict[str, Any]] = {}
    for graph in value["graphs"]:
        expected_keys = {
            "schema_version",
            "entry_ref",
            "entry_source_digest",
            "graph_digest",
            "budget",
            "files",
            "nodes",
            "edges",
            "diagnostics",
            "integrity_vetoes",
            "considered_files",
            "reachable_files",
            "excluded_sibling_files",
            "unsearched_files",
            "traversal_counts",
            "non_claims",
        }
        if not isinstance(graph, dict) or set(graph) != expected_keys or graph["schema_version"] != GRAPH_SCHEMA_VERSION:
            raise EvidenceValidationError("Phase 03 corpus graph schema mismatch")
        expected_digest = content_digest(
            [
                graph["entry_ref"],
                graph["entry_source_digest"],
                graph["nodes"],
                graph["edges"],
                graph["diagnostics"],
            ]
        )
        if graph["graph_digest"] != expected_digest or graph["graph_digest"] in graphs:
            raise EvidenceValidationError("Phase 03 corpus graph digest mismatch or duplicate")
        budget = graph["budget"]
        if (
            not isinstance(budget, dict)
            or set(budget) != set(_DEFAULT_BUDGET)
            or any(type(item) is not int or item <= 0 for item in budget.values())
        ):
            raise EvidenceValidationError("Phase 03 graph budget is invalid")
        file_rows = {item["logical_ref"]: item for item in graph["files"]}
        node_rows = {item["id"]: item for item in graph["nodes"]}
        edge_rows = {item["id"]: item for item in graph["edges"]}
        if len(file_rows) != len(graph["files"]) or len(node_rows) != len(graph["nodes"]) or len(edge_rows) != len(graph["edges"]):
            raise EvidenceValidationError("Phase 03 graph contains duplicate file/node/edge identity")
        if graph["entry_ref"] not in file_rows or graph["reachable_files"] != [item["logical_ref"] for item in graph["files"]]:
            raise EvidenceValidationError("Phase 03 graph reachable-file projection mismatch")
        if file_rows[graph["entry_ref"]]["source_digest"] != graph["entry_source_digest"]:
            raise EvidenceValidationError("Phase 03 graph entry digest projection mismatch")
        traversal = graph["traversal_counts"]
        if not isinstance(traversal, dict) or set(traversal) != {
            "files",
            "bytes",
            "dependency_expansions",
        }:
            raise EvidenceValidationError("Phase 03 graph traversal-count schema mismatch")
        if traversal["files"] != len(graph["files"]) or traversal["bytes"] != sum(
            item["byte_count"] for item in graph["files"]
        ):
            raise EvidenceValidationError("Phase 03 graph traversal-count projection mismatch")
        expansions = traversal["dependency_expansions"]
        if type(expansions) is not int or not 0 <= expansions <= budget["max_dependency_expansions"]:
            raise EvidenceValidationError("Phase 03 graph dependency-expansion count is invalid")
        if traversal["files"] > budget["max_files"] or traversal["bytes"] > budget["max_bytes"]:
            raise EvidenceValidationError("Phase 03 graph traversal exceeds its construction budget")
        considered = graph["considered_files"]
        if (
            not isinstance(considered, list)
            or considered != sorted(set(considered), key=lambda item: item.encode("utf-8"))
            or graph["entry_ref"] not in considered
            or any(item not in considered for item in graph["reachable_files"])
        ):
            raise EvidenceValidationError("Phase 03 graph considered-file projection mismatch")
        unsearched = graph["unsearched_files"]
        if (
            not isinstance(unsearched, list)
            or any(
                not isinstance(item, dict)
                or set(item) != {"file", "reason"}
                or item["file"] not in considered
                or not isinstance(item["reason"], str)
                or not item["reason"]
                for item in unsearched
            )
            or unsearched
            != sorted(unsearched, key=lambda item: (item["file"].encode("utf-8"), item["reason"]))
        ):
            raise EvidenceValidationError("Phase 03 graph unsearched-file projection mismatch")
        diagnostic_files = {
            item.get("target_file")
            for item in graph["diagnostics"]
            if isinstance(item.get("target_file"), str)
        }
        accounted_unreached = {item["file"] for item in unsearched} | diagnostic_files
        if set(considered) - set(graph["reachable_files"]) - accounted_unreached:
            raise EvidenceValidationError("Phase 03 graph omits an unsearched boundary")
        for node in graph["nodes"]:
            file_row = file_rows.get(node["source_file"])
            if file_row is None or node["source_digest"] != file_row["source_digest"]:
                raise EvidenceValidationError("Phase 03 graph node source binding mismatch")
        for edge in graph["edges"]:
            if edge["from_node_id"] not in node_rows or edge["to_node_id"] not in node_rows:
                raise EvidenceValidationError("Phase 03 graph edge endpoint is absent")
            if edge["source_span"]["source_digest"] != file_rows[edge["source_file"]]["source_digest"]:
                raise EvidenceValidationError("Phase 03 graph edge source binding mismatch")
        graphs[graph["graph_digest"]] = graph
    if list(graphs) != sorted(graphs):
        raise EvidenceValidationError("Phase 03 corpus graph collection is not digest ordered")
    return graphs


def _validate_search_boundary_against_graph(
    manifest: Mapping[str, Any],
    graph: Mapping[str, Any],
) -> None:
    """Reconstruct the resolver's bounded graph projections exactly."""
    budget = manifest["context_request"]["budget"]
    if budget != graph["budget"]:
        raise EvidenceValidationError("Phase 03 context request/graph budget mismatch")
    reachable_files = list(graph["reachable_files"])
    admitted_files = reachable_files[: budget["max_files"]]
    expected_unsearched_files = [
        {"file": item, "reason": "max_files"}
        for item in reachable_files[budget["max_files"] :]
    ]
    expected_unsearched_files.extend(dict(item) for item in graph["unsearched_files"])

    file_bytes = {item["logical_ref"]: item["byte_count"] for item in graph["files"]}
    bytes_used = 0
    searched_files: list[str] = []
    for ref in admitted_files:
        if bytes_used + file_bytes[ref] > budget["max_bytes"]:
            expected_unsearched_files.append({"file": ref, "reason": "max_bytes"})
            continue
        bytes_used += file_bytes[ref]
        searched_files.append(ref)

    eligible_nodes = [item for item in graph["nodes"] if item["source_file"] in searched_files]
    searched_nodes = eligible_nodes[: budget["max_nodes"]]
    eligible_edges = [
        item
        for item in graph["edges"]
        if item["source_file"] in searched_files and item["target_file"] in searched_files
    ]
    searched_edges = eligible_edges[: budget["max_edges"]]
    unsearched_files = sorted(
        expected_unsearched_files,
        key=lambda item: (item["file"].encode("utf-8"), item["reason"]),
    )
    unsearched_node_count = len(eligible_nodes) - len(searched_nodes)
    unsearched_edge_count = len(eligible_edges) - len(searched_edges)
    expected = {
        "searched_files": searched_files,
        "searched_nodes": [item["id"] for item in searched_nodes],
        "searched_edges": [item["id"] for item in searched_edges],
        "searched_counts": {
            "files": len(searched_files),
            "nodes": len(searched_nodes),
            "edges": len(searched_edges),
            "bytes": bytes_used,
        },
        "unsearched_files": unsearched_files,
        "unsearched_node_count": unsearched_node_count,
        "unsearched_edge_count": unsearched_edge_count,
        "budget_exhausted": bool(
            unsearched_files or unsearched_node_count or unsearched_edge_count
        ),
    }
    for key, expected_value in expected.items():
        if manifest.get(key) != expected_value:
            raise EvidenceValidationError(
                f"Phase 03 search boundary projection mismatch: {key}"
            )


def _validate_candidate_against_graph(
    candidate: Mapping[str, Any],
    graph: Mapping[str, Any],
    *,
    request: Mapping[str, Any] | None = None,
) -> None:
    node = next((item for item in graph["nodes"] if item["id"] == candidate.get("node_id")), None)
    if node is None:
        raise EvidenceValidationError("context candidate graph node is absent")
    source_ref = _exact_ref(candidate.get("source_ref"), "context candidate source_ref")
    expected = {
        "file": node["source_file"],
        "source_digest": node["source_digest"],
        "byte_span": node["byte_span"],
        "line_span": node["line_span"],
        "enclosing_node_id": node["id"],
    }
    if any(source_ref[key] != value for key, value in expected.items()):
        raise EvidenceValidationError("context candidate source ref does not match its graph node")
    path = source_ref["dependency_path"]
    if candidate.get("dependency_path") != path or path[-1] != node["id"]:
        raise EvidenceValidationError("context candidate dependency path projection mismatch")
    known_ids = {item["id"] for item in graph["nodes"]} | {item["id"] for item in graph["edges"]}
    if any(item not in known_ids for item in path):
        raise EvidenceValidationError("context candidate dependency path contains an unknown graph identity")
    if candidate.get("applicability_state") == "explicit":
        subjects = candidate.get("subject_evidence")
        if not isinstance(subjects, list) or not subjects:
            raise EvidenceValidationError("explicit context candidate lacks subject applicability evidence")
        if request is not None:
            required_subjects = {
                word
                for subject in request["requirement_subjects"]
                for word in re.findall(r"[A-Za-z0-9_:-]+", subject.lower())
            }
            if required_subjects and not required_subjects <= set(subjects):
                raise EvidenceValidationError("explicit context candidate lacks complete subject applicability")
        if source_ref["applicability_reason"] != candidate.get("applicability_reason"):
            raise EvidenceValidationError("explicit context candidate applicability projection mismatch")


def validate_symbol_resolution_ledger(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != {"schema_version", "entries"}:
        raise EvidenceValidationError("Phase 03 symbol ledger keys mismatch")
    if value["schema_version"] != "p03_symbol_resolution_ledger@1" or not isinstance(value["entries"], list):
        raise EvidenceValidationError("Phase 03 symbol ledger schema mismatch")
    seen: set[str] = set()
    for entry in value["entries"]:
        expected = {
            "obligation_digest",
            "schema_version",
            "scope",
            "candidates",
            "resolutions",
            "diagnostics",
            "non_claim",
        }
        if not isinstance(entry, dict) or set(entry) != expected or entry["schema_version"] != "p03_symbol_resolution@1":
            raise EvidenceValidationError("Phase 03 symbol resolution entry schema mismatch")
        digest = _require_digest(entry["obligation_digest"], "symbol resolution obligation digest")
        if digest in seen or entry["scope"].get("obligation_digest") != digest:
            raise EvidenceValidationError("Phase 03 symbol resolution scope/identity mismatch")
        seen.add(digest)
        candidates = {item["candidate_id"]: item for item in entry["candidates"]}
        if len(candidates) != len(entry["candidates"]):
            raise EvidenceValidationError("Phase 03 symbol candidates contain duplicate identities")
        for candidate_id, candidate in candidates.items():
            expected_id = "sym_" + content_digest(
                [
                    candidate["symbol"],
                    candidate["proposed_role"],
                    candidate["scope"],
                    candidate["evidence_kind"],
                    candidate["source_refs"],
                ]
            )
            if candidate_id != expected_id or candidate["scope"] != entry["scope"]:
                raise EvidenceValidationError("Phase 03 symbol candidate identity/scope mismatch")
        for resolution in entry["resolutions"]:
            ids = resolution["candidate_ids"]
            if any(candidate_id not in candidates for candidate_id in ids):
                raise EvidenceValidationError("Phase 03 symbol resolution references an absent candidate")
            roles = {candidates[candidate_id]["proposed_role"] for candidate_id in ids}
            if resolution["state"] == "resolved" and (len(roles) != 1 or resolution["role"] not in roles):
                raise EvidenceValidationError("Phase 03 resolved role is not derived from its candidates")
            if resolution["state"] != "resolved" and resolution["role"] is not None:
                raise EvidenceValidationError("Phase 03 unresolved role must be null")
    return value


def validate_evidence_ledgers(value: Any, *, manifests: list[Mapping[str, Any]]) -> dict[str, Any]:
    expected_lanes = {"parser", "context", "mathematical", "engineering", "interpretation"}
    if not isinstance(value, dict) or set(value) != expected_lanes:
        raise EvidenceValidationError("Phase 03 evidence ledger lane mismatch")
    expected_schemas = {
        "parser": "p03_parser_ledger@1",
        "context": "p03_context_ledger@1",
        "mathematical": "p03_mathematical_ledger@1",
        "engineering": "p03_engineering_ledger@1",
        "interpretation": "p03_interpretation_ledger@1",
    }
    for lane, schema in expected_schemas.items():
        ledger = value[lane]
        if not isinstance(ledger, dict) or set(ledger) != {"schema_version", "entries"} or ledger["schema_version"] != schema:
            raise EvidenceValidationError(f"Phase 03 {lane} ledger schema mismatch")
        if not isinstance(ledger["entries"], list) or any(not isinstance(item, dict) for item in ledger["entries"]):
            raise EvidenceValidationError(f"Phase 03 {lane} ledger entries are invalid")
    ordered = [item["obligation_digest"] for item in manifests]
    parser = value["parser"]["entries"]
    context = value["context"]["entries"]
    if [item.get("obligation_digest") for item in parser] != ordered:
        raise EvidenceValidationError("Phase 03 parser ledger does not cover obligations in entry order")
    if [item.get("obligation_digest") for item in context] != ordered:
        raise EvidenceValidationError("Phase 03 context ledger does not cover obligations in entry order")
    for row, manifest in zip(context, manifests, strict=True):
        expected = {
            "obligation_digest": manifest["obligation_digest"],
            "entry_state": manifest["entry_state"],
            "terminal_state": manifest.get("terminal_state"),
        }
        if row != expected:
            raise EvidenceValidationError("Phase 03 context ledger projection mismatch")
    if value["mathematical"]["entries"]:
        raise EvidenceValidationError("Phase 03 mathematical ledger must remain empty")
    for item in value["engineering"]["entries"]:
        if "id" not in item or "kind" not in item or "affected" not in item:
            raise EvidenceValidationError("Phase 03 engineering ledger entry is incomplete")
    if not value["interpretation"]["entries"]:
        raise EvidenceValidationError("Phase 03 interpretation ledger cannot be empty")
    return value


def validate_context_evidence_payload(
    value: Any,
    *,
    expected_bindings: list[Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    required = {
        "manifests",
        "corpus_graphs",
        "symbol_resolution_ledger",
        "notation_conflict_ledger",
        "typed_assumptions",
        "ledgers",
        "mutation_matrix",
        "frozen_regressions",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise EvidenceValidationError("Phase 03 context evidence payload keys mismatch")
    manifests = value["manifests"]
    if not isinstance(manifests, list) or len(manifests) != 17:
        raise EvidenceValidationError("Phase 03 context evidence requires 17 manifests")
    for manifest in manifests:
        validate_context_manifest(manifest)
    if expected_bindings is not None:
        observed = [
            {
                "adapter_eligible": item["p02_adapter_eligible"],
                "extraction_state": item["p02_extraction_state"],
                "obligation_digest": item["obligation_digest"],
            }
            for item in manifests
        ]
        if observed != [dict(item) for item in expected_bindings]:
            raise EvidenceValidationError("Phase 03 manifest/P02 binding sequence mismatch")
    if sum(item["entry_state"] == "context_search" for item in manifests) != 14 or sum(
        item["entry_state"] == "extraction_veto" for item in manifests
    ) != 3:
        raise EvidenceValidationError("Phase 03 context evidence partition mismatch")
    graphs = _validate_graph_collection(value["corpus_graphs"])
    for manifest in manifests:
        if manifest["entry_state"] != "context_search":
            continue
        graph = graphs.get(manifest["corpus_graph_digest"])
        if graph is None or graph["entry_source_digest"] != manifest["entry_source_digest"]:
            raise EvidenceValidationError("Phase 03 manifest graph binding mismatch")
        _validate_search_boundary_against_graph(manifest, graph)
        for candidate in manifest["candidates"]:
            _validate_candidate_against_graph(candidate, graph, request=manifest["context_request"])
        for assumption in manifest["typed_assumptions"]:
            validate_typed_assumption(assumption)
    validate_symbol_resolution_ledger(value["symbol_resolution_ledger"])
    assumptions = value["typed_assumptions"]
    if not isinstance(assumptions, dict) or set(assumptions) != {"schema_version", "assumptions", "non_claim"}:
        raise EvidenceValidationError("Phase 03 typed-assumption bundle keys mismatch")
    if assumptions["schema_version"] != "p03_typed_assumption_bundle@1":
        raise EvidenceValidationError("Phase 03 typed-assumption bundle schema mismatch")
    for assumption in assumptions["assumptions"]:
        validate_typed_assumption(assumption)
    expected_assumptions = [item for manifest in manifests for item in manifest["typed_assumptions"]]
    if assumptions["assumptions"] != expected_assumptions:
        raise EvidenceValidationError("Phase 03 typed-assumption bundle projection mismatch")
    notation = value["notation_conflict_ledger"]
    if not isinstance(notation, dict) or set(notation) != {"schema_version", "entries", "conflicts", "non_claim"}:
        raise EvidenceValidationError("Phase 03 notation ledger keys mismatch")
    if notation["schema_version"] != "p03_notation_conflict_ledger@1":
        raise EvidenceValidationError("Phase 03 notation ledger schema mismatch")
    symbol_ids = {
        item["obligation_digest"]: {candidate["candidate_id"] for candidate in item["candidates"]}
        for item in value["symbol_resolution_ledger"]["entries"]
    }
    for entry in notation["entries"]:
        if set(entry) != {"obligation_digest", "candidate_ids", "ambiguous_symbols", "unresolved_symbols"}:
            raise EvidenceValidationError("Phase 03 notation ledger entry keys mismatch")
        if set(entry["candidate_ids"]) != symbol_ids.get(entry["obligation_digest"], set()):
            raise EvidenceValidationError("Phase 03 notation ledger candidate projection mismatch")
    validate_evidence_ledgers(value["ledgers"], manifests=manifests)
    validate_p03_mutation_matrix(value["mutation_matrix"])
    frozen = value["frozen_regressions"]
    if not isinstance(frozen, dict) or set(frozen) != {
        "schema_version",
        "entries",
        "all_entries_single_reachable_file",
    }:
        raise EvidenceValidationError("Phase 03 frozen-regression artifact keys mismatch")
    if frozen["schema_version"] != "p03_frozen_context_regressions@1" or not isinstance(
        frozen["entries"], list
    ):
        raise EvidenceValidationError("Phase 03 frozen-regression artifact schema mismatch")
    if len(frozen["entries"]) != 4:
        raise EvidenceValidationError("Phase 03 frozen-regression artifact must contain four obligations")
    derived_single = all(
        isinstance(item, dict)
        and len(item.get("reachable_files", [])) == 1
        and item.get("diagnostic_kinds") == []
        for item in frozen["entries"]
    )
    if frozen["all_entries_single_reachable_file"] != derived_single or derived_single is not True:
        raise EvidenceValidationError("Phase 03 frozen-regression closure mismatch")
    return value


def _round_ref(round_root: str) -> str:
    value = PurePosixPath(round_root)
    if value.parent != _ROUND_ROOT or value.name not in {f"rr0{index}" for index in range(1, 6)}:
        raise EvidenceValidationError("Phase 03 round root is outside the reviewed scope")
    return value.as_posix()


def context_artifact_refs(round_root: str) -> dict[str, str]:
    round_ref = _round_ref(round_root)
    base = f"{round_ref}/context-bundle"
    return {
        "bundle_index": f"{base}/bundle-index.json",
        "corpus_graphs": f"{base}/corpus-graphs.json",
        "manifests": f"{base}/manifests.json",
        "symbol_ledger": f"{base}/symbol-resolution-ledger.json",
        "notation_ledger": f"{base}/notation-conflict-ledger.json",
        "typed_assumptions": f"{base}/typed-assumptions.json",
        "parser_ledger": f"{base}/ledgers/parser.json",
        "context_ledger": f"{base}/ledgers/context.json",
        "mathematical_ledger": f"{base}/ledgers/mathematical.json",
        "engineering_ledger": f"{base}/ledgers/engineering.json",
        "interpretation_ledger": f"{base}/ledgers/interpretation.json",
        "guard_index": f"{base}/guard-index.json",
        "mutation_matrix": f"{base}/mutation-matrix.json",
        "frozen_regressions": f"{base}/frozen-regressions.json",
    }


def build_context_bundle_index(
    root: str | os.PathLike[str],
    refs: Mapping[str, str],
    artifact_values: Mapping[str, Any],
) -> dict[str, Any]:
    workspace = Path(root)
    expected_refs = set(refs.values()) - {refs["bundle_index"]}
    if set(artifact_values) != expected_refs:
        raise EvidenceValidationError("context bundle constituent refs mismatch")
    artifacts: list[dict[str, Any]] = []
    for ref in sorted(expected_refs, key=lambda item: item.encode("utf-8")):
        raw, info = read_bytes_no_follow(workspace, ref)
        expected_raw = canonical_json_bytes(artifact_values[ref])
        if not stat.S_ISREG(info.st_mode) or raw != expected_raw:
            raise EvidenceValidationError(f"context bundle constituent reopen mismatch: {ref}")
        artifacts.append({"ref": ref, "sha256": content_digest(raw), "byte_count": len(raw)})
    collection = artifact_values[refs["manifests"]]
    manifests = collection.get("manifests") if isinstance(collection, Mapping) else None
    if not isinstance(manifests, list):
        raise EvidenceValidationError("context manifest collection is invalid")
    payload = {
        "manifests": manifests,
        "corpus_graphs": artifact_values[refs["corpus_graphs"]],
        "symbol_resolution_ledger": artifact_values[refs["symbol_ledger"]],
        "notation_conflict_ledger": artifact_values[refs["notation_ledger"]],
        "typed_assumptions": artifact_values[refs["typed_assumptions"]],
        "ledgers": {
            "parser": artifact_values[refs["parser_ledger"]],
            "context": artifact_values[refs["context_ledger"]],
            "mathematical": artifact_values[refs["mathematical_ledger"]],
            "engineering": artifact_values[refs["engineering_ledger"]],
            "interpretation": artifact_values[refs["interpretation_ledger"]],
        },
        "mutation_matrix": artifact_values[refs["mutation_matrix"]],
        "frozen_regressions": artifact_values[refs["frozen_regressions"]],
    }
    validate_context_evidence_payload(payload)
    validate_guard_index(artifact_values[refs["guard_index"]])
    summary = {
        "context_search": sum(item["entry_state"] == "context_search" for item in manifests),
        "extraction_veto": sum(item["entry_state"] == "extraction_veto" for item in manifests),
        "total": len(manifests),
    }
    semantic_digest = content_digest([[item["ref"], item["sha256"], item["byte_count"]] for item in artifacts])
    return {
        "schema_version": "p03_context_bundle_index@1",
        "phase": "P03",
        "artifacts": artifacts,
        "summary_counts": summary,
        "bundle_semantic_digest": semantic_digest,
        "non_claims": [
            "Summary counts are explanatory and are not reconstruction authority.",
            "The bundle is context evidence, not mathematical certification.",
        ],
    }


def build_guard_index(
    root: str | os.PathLike[str],
    round_root: str,
    *,
    actions: tuple[str, ...] = P03_GUARDED_ACTIONS,
) -> dict[str, Any]:
    workspace = Path(root)
    round_ref = _round_ref(round_root)
    guard_root = f"{round_ref}/governance/guard"
    if not actions or len(actions) != len(set(actions)):
        raise EvidenceValidationError("Phase 03 guarded action registry is empty or duplicated")
    entries: list[dict[str, Any]] = []
    for action in actions:
        token = "".join(char if char.isalnum() or char in "_-" else "_" for char in action) or "unknown"
        attestation_ref = f"{guard_root}/guard-attestation-{token}.json"
        ledger_ref = f"{guard_root}/forbidden-attempts-{token}.jsonl"
        attestation_raw, attestation_info = read_bytes_no_follow(workspace, attestation_ref)
        ledger_raw, ledger_info = read_bytes_no_follow(workspace, ledger_ref)
        if not stat.S_ISREG(attestation_info.st_mode) or not stat.S_ISREG(ledger_info.st_mode):
            raise EvidenceValidationError("Phase 03 guard artifacts are not regular files")
        attestation = _strict_json(attestation_raw, "Phase 03 guard attestation")
        keys = {
            "schema_version",
            "action",
            "ledger_ref",
            "ledger_sha256",
            "forbidden_attempt_count",
            "guard_replacement_errors",
            "backend_request_count",
            "source_edit_count",
            "publication_count",
            "closed_at_utc",
        }
        if set(attestation) != keys or attestation["schema_version"] != "p03_context_only_guard_attestation@1":
            raise EvidenceValidationError("Phase 03 guard attestation schema mismatch")
        if (
            attestation["action"] != action
            or attestation["ledger_ref"] != ledger_ref
            or attestation["ledger_sha256"] != content_digest(ledger_raw)
            or attestation["forbidden_attempt_count"] != 0
            or attestation["guard_replacement_errors"] != []
            or attestation["backend_request_count"] != 0
            or attestation["source_edit_count"] != 0
            or attestation["publication_count"] != 0
            or ledger_raw != b""
        ):
            raise EvidenceValidationError("Phase 03 guard attestation is nonzero or inconsistent")
        entries.append(
            {
                "action": action,
                "attestation_ref": attestation_ref,
                "attestation_sha256": content_digest(attestation_raw),
                "ledger_ref": ledger_ref,
                "ledger_sha256": content_digest(ledger_raw),
            }
        )
    return {
        "schema_version": "p03_guard_index@1",
        "actions": list(actions),
        "entries": entries,
        "forbidden_attempt_count": 0,
        "guard_replacement_errors": [],
        "backend_request_count": 0,
        "source_edit_count": 0,
        "publication_count": 0,
    }


def validate_guard_index(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version",
        "actions",
        "entries",
        "forbidden_attempt_count",
        "guard_replacement_errors",
        "backend_request_count",
        "source_edit_count",
        "publication_count",
    }
    if not isinstance(value, dict) or set(value) != keys or value["schema_version"] != "p03_guard_index@1":
        raise EvidenceValidationError("Phase 03 guard index schema mismatch")
    if value["actions"] != list(P03_GUARDED_ACTIONS):
        raise EvidenceValidationError("Phase 03 guard index action registry mismatch")
    if not isinstance(value["entries"], list) or len(value["entries"]) != len(P03_GUARDED_ACTIONS):
        raise EvidenceValidationError("Phase 03 guard index entries mismatch")
    for index, entry in enumerate(value["entries"]):
        if not isinstance(entry, dict) or set(entry) != {
            "action",
            "attestation_ref",
            "attestation_sha256",
            "ledger_ref",
            "ledger_sha256",
        }:
            raise EvidenceValidationError("Phase 03 guard index entry schema mismatch")
        if entry["action"] != P03_GUARDED_ACTIONS[index]:
            raise EvidenceValidationError("Phase 03 guard index entry order mismatch")
        for key in ("attestation_ref", "ledger_ref"):
            validate_logical_path(entry[key], name=f"guard index entry {key}")
        for key in ("attestation_sha256", "ledger_sha256"):
            _require_digest(entry[key], f"guard index entry {key}")
    if (
        value["forbidden_attempt_count"] != 0
        or value["guard_replacement_errors"] != []
        or value["backend_request_count"] != 0
        or value["source_edit_count"] != 0
        or value["publication_count"] != 0
    ):
        raise EvidenceValidationError("Phase 03 guard index is nonzero")
    return value


def reconstruct_context_bundle(root: str | os.PathLike[str], index_ref: str) -> dict[str, Any]:
    workspace = Path(root)
    index_raw, info = read_bytes_no_follow(workspace, index_ref)
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError("context bundle index is not regular")
    index = _strict_json(index_raw, "context bundle index")
    keys = {"schema_version", "phase", "artifacts", "summary_counts", "bundle_semantic_digest", "non_claims"}
    if set(index) != keys or index["schema_version"] != "p03_context_bundle_index@1" or index["phase"] != "P03":
        raise EvidenceValidationError("context bundle index schema mismatch")
    artifacts = index["artifacts"]
    if not isinstance(artifacts, list):
        raise EvidenceValidationError("context bundle artifacts must be a list")
    reopened: dict[str, dict[str, Any]] = {}
    semantic_rows: list[list[Any]] = []
    for position, artifact in enumerate(artifacts):
        if not isinstance(artifact, dict) or set(artifact) != {"ref", "sha256", "byte_count"}:
            raise EvidenceValidationError(f"context bundle artifact {position} schema mismatch")
        ref = validate_logical_path(artifact["ref"], name=f"artifact[{position}].ref")
        raw, target_info = read_bytes_no_follow(workspace, ref)
        if (
            not stat.S_ISREG(target_info.st_mode)
            or content_digest(raw) != artifact["sha256"]
            or len(raw) != artifact["byte_count"]
        ):
            raise EvidenceValidationError(f"context bundle artifact drift: {ref}")
        reopened[ref] = _strict_json(raw, ref)
        semantic_rows.append([ref, artifact["sha256"], artifact["byte_count"]])
    if content_digest(semantic_rows) != index["bundle_semantic_digest"]:
        raise EvidenceValidationError("context bundle semantic digest mismatch")
    def unique(suffix: str) -> str:
        matches = [ref for ref in reopened if ref.endswith(suffix)]
        if len(matches) != 1:
            raise EvidenceValidationError(f"context bundle constituent is missing or ambiguous: {suffix}")
        return matches[0]

    manifest_ref = unique("/manifests.json")
    guard_ref = unique("/guard-index.json")
    collection = reopened[manifest_ref]
    if set(collection) != {"schema_version", "manifests"} or collection["schema_version"] != "p03_context_manifest_collection@1":
        raise EvidenceValidationError("context manifest collection schema mismatch")
    manifests = collection["manifests"]
    if not isinstance(manifests, list):
        raise EvidenceValidationError("context manifest collection is invalid")
    for item in manifests:
        validate_context_manifest(item)
    guard = validate_guard_index(reopened[guard_ref])
    for entry in guard["entries"]:
        for ref_key, digest_key in (("attestation_ref", "attestation_sha256"), ("ledger_ref", "ledger_sha256")):
            raw, target_info = read_bytes_no_follow(workspace, entry[ref_key])
            if not stat.S_ISREG(target_info.st_mode) or content_digest(raw) != entry[digest_key]:
                raise EvidenceValidationError(f"context guard artifact drift: {entry[ref_key]}")
    search_count = sum(item["entry_state"] == "context_search" for item in manifests)
    veto_count = sum(item["entry_state"] == "extraction_veto" for item in manifests)
    if len(manifests) != 17 or search_count != 14 or veto_count != 3:
        raise EvidenceValidationError("context bundle obligation partition mismatch")
    payload = {
        "manifests": manifests,
        "corpus_graphs": reopened[unique("/corpus-graphs.json")],
        "symbol_resolution_ledger": reopened[unique("/symbol-resolution-ledger.json")],
        "notation_conflict_ledger": reopened[unique("/notation-conflict-ledger.json")],
        "typed_assumptions": reopened[unique("/typed-assumptions.json")],
        "ledgers": {
            "parser": reopened[unique("/ledgers/parser.json")],
            "context": reopened[unique("/ledgers/context.json")],
            "mathematical": reopened[unique("/ledgers/mathematical.json")],
            "engineering": reopened[unique("/ledgers/engineering.json")],
            "interpretation": reopened[unique("/ledgers/interpretation.json")],
        },
        "mutation_matrix": reopened[unique("/mutation-matrix.json")],
        "frozen_regressions": reopened[unique("/frozen-regressions.json")],
    }
    inputs = load_p03_scientific_inputs(workspace)
    validate_context_evidence_payload(
        payload,
        expected_bindings=inputs["ordered_obligation_bindings"],
    )
    summary = index["summary_counts"]
    return {
        "context_search_count": search_count,
        "extraction_veto_count": veto_count,
        "obligation_count": len(manifests),
        "summary_count_mismatch": summary != {
            "context_search": search_count,
            "extraction_veto": veto_count,
            "total": len(manifests),
        },
        "backend_request_count": guard["backend_request_count"],
        "source_edit_count": guard["source_edit_count"],
        "publication_count": guard["publication_count"],
        "bundle_semantic_digest": index["bundle_semantic_digest"],
        "mutation_all_pass": payload["mutation_matrix"]["all_pass"],
        "mathematical_ledger_entry_count": len(payload["ledgers"]["mathematical"]["entries"]),
        "parser_ledger_entry_count": len(payload["ledgers"]["parser"]["entries"]),
        "notation_ledger_entry_count": len(payload["notation_conflict_ledger"]["entries"]),
        "frozen_regression_count": len(payload["frozen_regressions"]["entries"]),
        "all_frozen_entries_single_reachable_file": payload["frozen_regressions"][
            "all_entries_single_reachable_file"
        ],
    }


def validate_p03_receipt(value: Any, *, expected_actions: list[str] | tuple[str, ...]) -> dict[str, Any]:
    keys = {
        "schema_version",
        "phase",
        "result_round",
        "sequence",
        "action",
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
    if not isinstance(value, dict) or set(value) != keys:
        raise EvidenceValidationError("Phase 03 receipt keys mismatch")
    if value["schema_version"] != "p03_command_receipt@1" or value["phase"] != "P03":
        raise EvidenceValidationError("Phase 03 receipt schema/phase mismatch")
    if value["result_round"] not in {f"rr0{index}" for index in range(1, 6)}:
        raise EvidenceValidationError("Phase 03 receipt result round is invalid")
    if type(value["sequence"]) is not int or not 1 <= value["sequence"] <= 26:
        raise EvidenceValidationError("Phase 03 receipt sequence is invalid")
    if value["action"] not in set(expected_actions):
        raise EvidenceValidationError("Phase 03 receipt action is unregistered")
    if value["execution_class"] not in {"governance_native", "subprocess"}:
        raise EvidenceValidationError("Phase 03 receipt execution class is invalid")
    if not isinstance(value["handler_id"], str) or not value["handler_id"]:
        raise EvidenceValidationError("Phase 03 receipt handler id is invalid")
    for key in ("external_argv", "child_argv"):
        if not isinstance(value[key], list) or any(not isinstance(item, str) for item in value[key]):
            raise EvidenceValidationError(f"Phase 03 receipt {key} is invalid")
    _require_digest(value["child_environment_sha256"], "receipt child_environment_sha256")
    if type(value["wall_time_ns"]) is not int or value["wall_time_ns"] < 0:
        raise EvidenceValidationError("Phase 03 receipt wall time is invalid")
    if type(value["exit_code"]) is not int:
        raise EvidenceValidationError("Phase 03 receipt exit code is invalid")
    for prefix in ("stdout", "stderr"):
        validate_logical_path(value[f"{prefix}_ref"], name=f"receipt {prefix}_ref")
        _require_digest(value[f"{prefix}_sha256"], f"receipt {prefix}_sha256")
        if type(value[f"{prefix}_byte_count"]) is not int or value[f"{prefix}_byte_count"] < 0:
            raise EvidenceValidationError(f"receipt {prefix}_byte_count is invalid")
    prior = value["prior_receipt_sha256"]
    if value["sequence"] == 1:
        if prior is not None:
            raise EvidenceValidationError("first Phase 03 receipt must have null predecessor")
    else:
        _require_digest(prior, "receipt prior_receipt_sha256")
    if not isinstance(value["bindings"], dict):
        raise EvidenceValidationError("Phase 03 receipt bindings must be an object")
    return value


def validate_p03_receipt_index(value: Any, *, expected_actions: list[str] | tuple[str, ...]) -> dict[str, Any]:
    keys = {"schema_version", "phase", "result_round", "receipts", "head_sequence", "head_sha256"}
    if not isinstance(value, dict) or set(value) != keys:
        raise EvidenceValidationError("Phase 03 receipt index keys mismatch")
    if value["schema_version"] != "p03_receipt_index@1" or value["phase"] != "P03":
        raise EvidenceValidationError("Phase 03 receipt index schema/phase mismatch")
    if value["result_round"] not in {f"rr0{index}" for index in range(1, 6)}:
        raise EvidenceValidationError("Phase 03 receipt index round is invalid")
    receipts = value["receipts"]
    if not isinstance(receipts, list) or not receipts:
        raise EvidenceValidationError("Phase 03 receipt index must be a non-empty prefix")
    actions: list[str] = []
    for index, item in enumerate(receipts, start=1):
        if not isinstance(item, dict) or set(item) != {"sequence", "action", "receipt_ref", "receipt_sha256"}:
            raise EvidenceValidationError("Phase 03 receipt index entry keys mismatch")
        if item["sequence"] != index or item["action"] not in set(expected_actions):
            raise EvidenceValidationError("Phase 03 receipt index sequence/action mismatch")
        validate_logical_path(item["receipt_ref"], name="receipt index receipt_ref")
        _require_digest(item["receipt_sha256"], "receipt index receipt_sha256")
        actions.append(item["action"])
    if len(actions) != len(set(actions)):
        raise EvidenceValidationError("Phase 03 receipt index repeats an action")
    if value["head_sequence"] != len(receipts) or value["head_sha256"] != receipts[-1]["receipt_sha256"]:
        raise EvidenceValidationError("Phase 03 receipt index head mismatch")
    return value


def expected_p03_next_action(
    receipts: list[Mapping[str, Any]] | None,
    *,
    pass_actions: list[str] | tuple[str, ...],
    failure_actions: list[str] | tuple[str, ...],
    stable_path_exists: bool,
) -> str | None:
    if stable_path_exists:
        if receipts and receipts[-1].get("action") == "stable_publication" and receipts[-1].get("exit_code") == 0:
            return None
        raise EvidenceValidationError("Phase 03 stable path exists without a trusted terminal receipt")
    if not receipts:
        return pass_actions[0]
    actions = [str(item.get("action")) for item in receipts]
    if len(actions) != len(set(actions)):
        raise EvidenceValidationError("Phase 03 action history repeats an action")
    failures = [
        item
        for item in receipts
        if item.get("exit_code") != 0
        or (
            item.get("action") == "result_review_binding"
            and item.get("bindings", {}).get("review_verdict") == "REVISE"
        )
        or (
            item.get("action") == "final_seal_audit_binding"
            and item.get("bindings", {}).get("audit_verdict") == "REVISE"
        )
    ]
    if failures:
        if "bind_scoped_repair" not in actions:
            return failure_actions[0]
        if actions[-1] != "bind_scoped_repair" or receipts[-1].get("exit_code") != 0:
            raise EvidenceValidationError("Phase 03 failure suffix is not safely resumable")
        return failure_actions[1]
    if any(action in actions for action in failure_actions):
        raise EvidenceValidationError("Phase 03 failure suffix appears on a zero-failure path")
    expected_prefix = list(pass_actions[: len(actions)])
    if actions != expected_prefix:
        raise EvidenceValidationError("Phase 03 action history is not a pass-sequence prefix")
    return pass_actions[len(actions)] if len(actions) < len(pass_actions) else None


def _require_round(value: Any, name: str = "result round") -> str:
    if not isinstance(value, str) or value not in {f"rr0{index}" for index in range(1, 6)}:
        raise EvidenceValidationError(f"{name} is invalid")
    return value


def _require_ref_digest_pairs(value: Mapping[str, Any], pairs: tuple[tuple[str, str], ...], name: str) -> None:
    for ref_key, digest_key in pairs:
        validate_logical_path(value[ref_key], name=f"{name} {ref_key}")
        _require_digest(value[digest_key], f"{name} {digest_key}")


def _validate_pass_maps(value: Mapping[str, Any], name: str) -> None:
    primary = value.get("primary_criterion")
    expected_primary = {"all_pass", *P03_PRIMARY_CRITERIA}
    if not isinstance(primary, dict) or set(primary) != expected_primary:
        raise EvidenceValidationError(f"{name} primary criterion keys mismatch")
    if any(type(item) is not bool for item in primary.values()):
        raise EvidenceValidationError(f"{name} primary criterion values must be booleans")
    if primary["all_pass"] != all(primary[key] for key in P03_PRIMARY_CRITERIA):
        raise EvidenceValidationError(f"{name} all_pass is not derived")
    vetoes = value.get("vetoes")
    if not isinstance(vetoes, dict) or set(vetoes) != set(P03_VETO_KEYS):
        raise EvidenceValidationError(f"{name} veto keys mismatch")
    if any(type(item) is not bool for item in vetoes.values()):
        raise EvidenceValidationError(f"{name} veto values must be booleans")
    non_claims = value.get("non_claims")
    if (
        not isinstance(non_claims, list)
        or set(non_claims) != set(P03_NON_CLAIMS)
        or len(non_claims) != len(P03_NON_CLAIMS)
    ):
        raise EvidenceValidationError(f"{name} non-claims mismatch")


def parse_p03_human_result(raw: bytes, *, result_round: str, pre_result_index_sha256: str) -> str:
    _require_round(result_round)
    _require_digest(pre_result_index_sha256, "pre-result receipt-index digest")
    if len(raw) > 262_144 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError("Phase 03 human result violates bounded byte grammar")
    try:
        lines = raw.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("Phase 03 human result is not strict UTF-8") from exc
    for section in P03_HUMAN_RESULT_SECTIONS:
        if lines.count(f"## {section}") != 1:
            raise EvidenceValidationError(f"Phase 03 human result section mismatch: {section}")
    nonempty = [line for line in lines if line]
    if len(nonempty) < 4:
        raise EvidenceValidationError("Phase 03 human result footer is missing")
    prefix = "Claimed decision: `"
    if not nonempty[-3].startswith(prefix) or not nonempty[-3].endswith("`"):
        raise EvidenceValidationError("Phase 03 human result decision footer is invalid")
    decision = nonempty[-3][len(prefix) : -1]
    expected = [
        f"Result round: `{result_round}`",
        f"Claimed decision: `{decision}`",
        f"Pre-result receipt-index SHA-256: `{pre_result_index_sha256}`",
        "Publication mode: `disabled`",
    ]
    if nonempty[-4:] != expected or decision not in {
        "candidate_pass_pending_independent_result_review",
        "blocked",
    }:
        raise EvidenceValidationError("Phase 03 human result footer mismatch")
    if any(lines.count(item) != 1 for item in expected):
        raise EvidenceValidationError("Phase 03 human result footer is repeated")
    return decision


def parse_p03_review(raw: bytes, *, expected_bindings: Mapping[str, str], kind: str) -> str:
    if len(raw) > 131_072 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"Phase 03 {kind} violates bounded byte grammar")
    try:
        lines = raw.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError(f"Phase 03 {kind} is not strict UTF-8") from exc
    round_labels = {"Reviewed result round", "Audited result round"}
    for label, binding in expected_bindings.items():
        if not isinstance(label, str) or not label:
            raise EvidenceValidationError(f"Phase 03 {kind} has an invalid binding label")
        if label in round_labels:
            _require_round(binding, f"Phase 03 {kind} {label}")
        else:
            _require_digest(binding, f"Phase 03 {kind} {label}")
        if lines.count(f"{label}: `{binding}`") != 1:
            raise EvidenceValidationError(f"Phase 03 {kind} binding line mismatch: {label}")
    verdicts = [line for line in lines if line.startswith("VERDICT:")]
    nonempty = [line for line in lines if line]
    if (
        len(verdicts) != 1
        or verdicts[0] not in {"VERDICT: AGREE", "VERDICT: REVISE"}
        or not nonempty
        or nonempty[-1] != verdicts[0]
    ):
        raise EvidenceValidationError(f"Phase 03 {kind} verdict is not unique and final")
    return verdicts[0].split(": ", 1)[1]


_RESULT_PAIRS = (
    ("human_result_ref", "human_result_sha256"),
    ("pre_result_receipt_index_ref", "pre_result_receipt_index_sha256"),
    ("entry_record_ref", "entry_record_sha256"),
    ("p02_stable_decision_ref", "p02_stable_decision_sha256"),
    ("p02_terminal_receipt_index_ref", "p02_terminal_receipt_index_sha256"),
    ("p02_extraction_bundle_index_ref", "p02_extraction_bundle_index_sha256"),
    ("p02_obligations_ref", "p02_obligations_sha256"),
    ("p02_close_ref", "p02_close_sha256"),
    ("context_bundle_index_ref", "context_bundle_index_sha256"),
    ("mutation_matrix_ref", "mutation_matrix_sha256"),
    ("guard_index_ref", "guard_index_sha256"),
)


def validate_p03_phase_result(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version",
        "phase",
        "result_round",
        "decision",
        "publication_mode",
        "claim_eligibility",
        *{item for pair in _RESULT_PAIRS for item in pair},
        "p02_extraction_bundle_semantic_digest",
        "context_bundle_semantic_digest",
        "backend_request_count",
        "source_edit_count",
        "publication_count",
        "primary_criterion",
        "vetoes",
        "non_claims",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise EvidenceValidationError("Phase 03 phase-result keys mismatch")
    if value["schema_version"] != "p03_phase_result@1" or value["phase"] != "P03":
        raise EvidenceValidationError("Phase 03 phase-result metadata mismatch")
    _require_round(value["result_round"])
    if value["decision"] not in {"candidate_pass_pending_independent_result_review", "blocked"}:
        raise EvidenceValidationError("Phase 03 phase-result decision mismatch")
    if value["publication_mode"] != "disabled" or value["claim_eligibility"] != "ineligible":
        raise EvidenceValidationError("Phase 03 phase-result boundary mismatch")
    _require_ref_digest_pairs(value, _RESULT_PAIRS, "Phase 03 phase result")
    _require_digest(value["p02_extraction_bundle_semantic_digest"], "P02 bundle semantic digest")
    _require_digest(value["context_bundle_semantic_digest"], "P03 bundle semantic digest")
    for key in ("backend_request_count", "source_edit_count", "publication_count"):
        if type(value[key]) is not int or value[key] < 0:
            raise EvidenceValidationError(f"Phase 03 phase-result {key} is invalid")
    _validate_pass_maps(value, "Phase 03 phase result")
    passing = value["primary_criterion"]["all_pass"] and not any(value["vetoes"].values())
    if (value["decision"] == "candidate_pass_pending_independent_result_review") != passing:
        raise EvidenceValidationError("Phase 03 phase-result decision contradicts reconstructed gates")
    return value


def validate_p03_run_manifest(value: Any) -> dict[str, Any]:
    keys = {
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
        "implementation_exit_manifest_sha256",
        "implementation_delta_digest",
        "source_data_version",
        "frozen_source_digests",
        "external_tool_considerations",
        "artifact_inventory",
        "non_claims",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise EvidenceValidationError("Phase 03 run-manifest keys mismatch")
    if value["schema_version"] != "p03_run_manifest@1" or value["phase"] != "P03":
        raise EvidenceValidationError("Phase 03 run-manifest metadata mismatch")
    _require_round(value["result_round"])
    if not isinstance(value["git_commit"], str) or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value["git_commit"]) is None:
        raise EvidenceValidationError("Phase 03 run-manifest git commit is invalid")
    timestamp_re = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
    if any(not isinstance(value[key], str) or timestamp_re.fullmatch(value[key]) is None for key in ("started_at_utc", "ended_at_utc")):
        raise EvidenceValidationError("Phase 03 run-manifest timestamp is invalid")
    if type(value["wall_time_ns"]) is not int or value["wall_time_ns"] < 0:
        raise EvidenceValidationError("Phase 03 run-manifest wall time is invalid")
    for key in ("environment", "device_execution", "random_seed_policy"):
        if not isinstance(value[key], dict):
            raise EvidenceValidationError(f"Phase 03 run-manifest {key} must be an object")
    if value["device_execution"].get("gpu_requested") is not False or value["device_execution"].get("gpu_initialized") is not False:
        raise EvidenceValidationError("Phase 03 run-manifest records GPU execution")
    _require_ref_digest_pairs(
        value,
        (
            ("plan_ref", "plan_sha256"),
            ("result_ref", "result_sha256"),
            ("pre_candidate_receipt_index_ref", "pre_candidate_receipt_index_sha256"),
            ("entry_record_ref", "entry_record_sha256"),
        ),
        "Phase 03 run manifest",
    )
    validate_logical_path(value["governance_receipt_family_ref"], name="governance receipt family")
    for key in (
        "implementation_entry_manifest_sha256",
        "implementation_round_manifest_sha256",
        "implementation_exit_manifest_sha256",
        "implementation_delta_digest",
    ):
        _require_digest(value[key], f"Phase 03 run-manifest {key}")
    if not isinstance(value["source_data_version"], str) or not value["source_data_version"]:
        raise EvidenceValidationError("Phase 03 run-manifest source data version is invalid")
    frozen = value["frozen_source_digests"]
    if not isinstance(frozen, dict) or len(frozen) != 2:
        raise EvidenceValidationError("Phase 03 run-manifest frozen source map mismatch")
    for ref, digest in frozen.items():
        validate_logical_path(ref, name="Phase 03 frozen source ref")
        _require_digest(digest, "Phase 03 frozen source digest")
    tools = value["external_tool_considerations"]
    expected_tools = (
        "repository_native_context_scanner",
        "P02_byte_preserving_locator",
        "SymPy_and_SageMath",
        "Lean_and_specialist_premise_or_proof_search",
    )
    if not isinstance(tools, list) or tuple(item.get("tool") for item in tools if isinstance(item, dict)) != expected_tools:
        raise EvidenceValidationError("Phase 03 run-manifest external-tool registry mismatch")
    inventory = value["artifact_inventory"]
    if not isinstance(inventory, list):
        raise EvidenceValidationError("Phase 03 run-manifest inventory must be a list")
    seen: set[str] = set()
    for item in inventory:
        if not isinstance(item, dict) or set(item) != {"logical_ref", "sha256", "byte_count", "role"}:
            raise EvidenceValidationError("Phase 03 run-manifest inventory entry mismatch")
        ref = validate_logical_path(item["logical_ref"], name="Phase 03 inventory ref")
        if ref in seen:
            raise EvidenceValidationError("Phase 03 run-manifest inventory repeats a ref")
        seen.add(ref)
        _require_digest(item["sha256"], "Phase 03 inventory digest")
        if type(item["byte_count"]) is not int or item["byte_count"] < 0:
            raise EvidenceValidationError("Phase 03 inventory byte count is invalid")
        if not isinstance(item["role"], str) or not item["role"]:
            raise EvidenceValidationError("Phase 03 inventory role is invalid")
    if (
        not isinstance(value["non_claims"], list)
        or set(value["non_claims"]) != set(P03_NON_CLAIMS)
        or len(value["non_claims"]) != len(P03_NON_CLAIMS)
    ):
        raise EvidenceValidationError("Phase 03 run-manifest non-claims mismatch")
    return value


_CANDIDATE_PAIRS = (
    ("entry_record_ref", "entry_record_sha256"),
    ("p02_stable_decision_ref", "p02_stable_decision_sha256"),
    ("p02_terminal_receipt_index_ref", "p02_terminal_receipt_index_sha256"),
    ("reviewed_plan_ref", "reviewed_plan_sha256"),
    ("reviewed_recovery_plan_ref", "reviewed_recovery_plan_sha256"),
    ("agreeing_recovery_review_ref", "agreeing_recovery_review_sha256"),
    ("implementation_entry_manifest_ref", "implementation_entry_manifest_sha256"),
    ("implementation_round_manifest_ref", "implementation_round_manifest_sha256"),
    ("protected_manifest_ref", "protected_manifest_sha256"),
    ("immutable_input_manifest_ref", "immutable_input_manifest_sha256"),
    ("run_manifest_ref", "run_manifest_sha256"),
    ("result_ref", "result_sha256"),
    ("pre_candidate_receipt_index_ref", "pre_candidate_receipt_index_sha256"),
    ("context_bundle_index_ref", "context_bundle_index_sha256"),
    ("mutation_matrix_ref", "mutation_matrix_sha256"),
    ("guard_index_ref", "guard_index_sha256"),
)


def validate_p03_candidate(value: Any) -> dict[str, Any]:
    keys = {
        "schema_version",
        "phase",
        "result_round",
        "decision",
        "publication_mode",
        "claim_eligibility",
        *{item for pair in _CANDIDATE_PAIRS for item in pair},
        "context_bundle_semantic_digest",
        "frozen_source_digests",
        "backend_request_count",
        "source_edit_count",
        "publication_count",
        "primary_criterion",
        "vetoes",
        "non_claims",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise EvidenceValidationError("Phase 03 candidate keys mismatch")
    if value["schema_version"] != "p03_candidate_decision@1" or value["phase"] != "P03":
        raise EvidenceValidationError("Phase 03 candidate metadata mismatch")
    _require_round(value["result_round"])
    if value["decision"] != "candidate_pass_pending_independent_result_review":
        raise EvidenceValidationError("Phase 03 candidate decision mismatch")
    if value["publication_mode"] != "disabled" or value["claim_eligibility"] != "ineligible":
        raise EvidenceValidationError("Phase 03 candidate boundary mismatch")
    _require_ref_digest_pairs(value, _CANDIDATE_PAIRS, "Phase 03 candidate")
    _require_digest(value["context_bundle_semantic_digest"], "Phase 03 candidate bundle semantic digest")
    frozen = value["frozen_source_digests"]
    if not isinstance(frozen, dict) or len(frozen) != 2:
        raise EvidenceValidationError("Phase 03 candidate frozen-source map mismatch")
    for ref, digest in frozen.items():
        validate_logical_path(ref, name="Phase 03 candidate frozen source")
        _require_digest(digest, "Phase 03 candidate frozen source digest")
    for key in ("backend_request_count", "source_edit_count", "publication_count"):
        if value[key] != 0:
            raise EvidenceValidationError(f"Phase 03 candidate {key} must be zero")
    _validate_pass_maps(value, "Phase 03 candidate")
    if not value["primary_criterion"]["all_pass"] or any(value["vetoes"].values()):
        raise EvidenceValidationError("Phase 03 candidate gates do not pass")
    return value


def validate_p03_final(value: Any) -> dict[str, Any]:
    pairs = (
        ("candidate_decision_ref", "candidate_decision_sha256"),
        ("result_review_ref", "result_review_sha256"),
        ("reviewed_receipt_index_ref", "reviewed_receipt_index_sha256"),
        ("p02_stable_decision_ref", "p02_stable_decision_sha256"),
    )
    keys = {
        "schema_version",
        "phase",
        "result_round",
        "decision",
        "publication_mode",
        *{item for pair in pairs for item in pair},
        "context_bundle_semantic_digest",
        "primary_criterion",
        "vetoes",
        "non_claims",
    }
    if not isinstance(value, dict) or set(value) != keys:
        raise EvidenceValidationError("Phase 03 final-decision keys mismatch")
    if value["schema_version"] != "p03_final_decision@1" or value["phase"] != "P03":
        raise EvidenceValidationError("Phase 03 final-decision metadata mismatch")
    _require_round(value["result_round"])
    if value["decision"] != "pass" or value["publication_mode"] != "disabled":
        raise EvidenceValidationError("Phase 03 final decision/boundary mismatch")
    _require_ref_digest_pairs(value, pairs, "Phase 03 final decision")
    _require_digest(value["context_bundle_semantic_digest"], "Phase 03 final bundle semantic digest")
    _validate_pass_maps(value, "Phase 03 final decision")
    if not value["primary_criterion"]["all_pass"] or any(value["vetoes"].values()):
        raise EvidenceValidationError("Phase 03 final-decision gates do not pass")
    return value
