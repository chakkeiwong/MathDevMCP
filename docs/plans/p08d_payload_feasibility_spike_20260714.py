from __future__ import annotations

"""Read-only exact-byte feasibility check for the Phase 08D compact schema."""

import base64
from copy import deepcopy
import hashlib
import importlib.metadata
import json
from pathlib import Path
import struct
import sys
import tempfile
from typing import Any, Mapping


REPO_ROOT = Path(__file__).resolve().parents[2]
P08C_SNAPSHOT_SRC = (
    REPO_ROOT
    / ".local/mathdevmcp/evidence/p08-20260714/continuations"
    / "20260714T080342Z-3a1e3445eeab/code-snapshot/src"
)
sys.path.insert(0, str(P08C_SNAPSHOT_SRC))

from mathdevmcp.failure_ledgers import validate_discriminating_action  # noqa: E402
import mathdevmcp.document_derivation_response as response_module  # noqa: E402
from mcp.types import (  # noqa: E402
    CallToolResult,
    JSONRPCMessage,
    JSONRPCResponse,
    TextContent,
)


P08C1_RUN_ROOT = (
    REPO_ROOT
    / ".local/mathdevmcp/evidence/p08-20260714/p08c1"
    / "20260714T121103Z-fc7811786801"
)
P08A_EXTRACTION = (
    REPO_ROOT
    / ".local/mathdevmcp/evidence/p08-20260714/runs"
    / "20260714T045222Z-a0e295b097c0/p08a/extraction.json"
)

EXPECTED_INPUT_SHA256 = {
    "card-audit.json": "e74d738f651657cbb68498ebf51faf50c9a2589381d6477fa6910c2070f548e8",
    "risky-audit.json": "c6370c05d12dae1c2bee8f2e321da487f26115545943b9ee1874e56028228047",
    "target-fidelity.json": "4fd07445dd796fba570fe46c9fa6daf4362ba5f12a740b64ff942a0cea81872b",
    "decision.json": "9b98b29de3bf6b8237370e12e3c3776855619a373b8333c1207b064e197e5d17",
}
EXPECTED_P08A_EXTRACTION_SHA256 = "8a0386d360068ff3ee481ea88a170a41abeae6dce5716a55a7c75660859e4da0"
EXPECTED_REQUEST_SHA256 = {
    "card": "32a7793e5f1674edb2e9690429d2a4998316bd780385bce8867355c61fda3a45",
    "risky": "fee205368a9af4d2a399d43827352d14830a02ade2e0ba35b3ff7ec231a638be",
}
EXPECTED_V1_COMPACT_SHA256 = {
    "card": "118aa556f743e2cefb6ee8e26de08bd19c161ab66a3226b0d28da54386f8f11d",
    "risky": "e2a76b66a92e4ae77f03142b24e15fa89408b81a6f2112a0b8170e8472ba8427",
}
EXPECTED_ARTIFACT_SHA256 = {
    "card": "c5ac16312c9ec34dae87f8974ac5ccb800b13c198c6ffe28a320cfe46d35709f",
    "risky": "cb7a39b8acce5c4a91dbbc52ad2a6309304dbca88974ea42ae2417c44de89082",
}
EXPECTED_RESPONSE_MODULE_SHA256 = "127de9b1fcf313a8dbd7bd0e1bf24e531845e4b8a843d3a917d458fb160ede02"
EXPECTED_FAILURE_LEDGER_SHA256 = "9a74755442db135694e0b4f7c2763299a372e2a2aaeb95d2ecdcb80d552435c0"

SOURCE_SPECS = {
    "card": {
        "source": "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
        "focus_labels": [
            "eq:panel-npv-functional",
            "eq:incremental-cash-flow",
            "eq:incremental-npv",
        ],
    },
    "risky": {
        "source": "docs/risky-debt-maliar-deep-learning-lecture-note.tex",
        "focus_labels": ["prop:interior-foc", "eq:foc-k", "eq:foc-b"],
    },
}

RESPONSE_SCHEMA = "p08_document_derivation_response@2"
CURSOR_SCHEMA = "p08_document_derivation_cursor@2"
SELECTOR_SCHEMA = "p08d_document_derivation_selector@1"
RESOLVER_SCOPE_SCHEMA = "p08d_document_derivation_resolver_scope@1"
ARTIFACT_SCHEMA = "p07_document_derivation_artifact@1"
ACTION_POLICY = "p08d_unresolved_choice_action_policy@1"
BYTE_POLICY = "p08d_compact_byte_policy@1"
TOKEN_MAGIC = b"MDP2"
BYTE_POLICY_CODE = 1
TOKEN_DIGEST_COUNT = 7
TOKEN_SIZE = len(TOKEN_MAGIC) + 8 + TOKEN_DIGEST_COUNT * 32
CANONICAL_LIMIT = 25_600
TRANSPORT_LIMIT = 30_720
COMPATIBILITY_TEXT = "MathDevMCP structured result; read structuredContent."

OUTCOME_NAMES = (
    "unavailable",
    "unsupported",
    "timeout",
    "execution_error",
    "malformed",
    "certified",
    "refuted",
    "unknown",
)

GLOBAL_RESOLVER_COLLECTIONS = (
    "global_blocker_records",
    "global_evidence_ref_records",
    "global_source_ref_records",
)
TARGET_RESOLVER_COLLECTIONS = (
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


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_v1_comparator(
    document: str,
    artifact_parent: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], Path]:
    spec = SOURCE_SPECS[document]
    raw_audit = json.loads((P08C1_RUN_ROOT / f"{document}-audit.json").read_text())
    request = response_module.build_document_derivation_audit_request(
        spec["source"],
        focus_labels=spec["focus_labels"],
        max_labels=30,
        budget_profile="smoke",
        max_attempts=0,
        backend_env="mathdevmcp-backends",
        search_mode="agent_guided",
        grounding_policy="strict",
        workers=1,
    )
    if digest(request) != EXPECTED_REQUEST_SHA256[document]:
        raise RuntimeError(f"{document} P08C1 request binding drift")
    artifact_root = artifact_parent / document
    compact = response_module.compile_document_derivation_response(
        raw_audit,
        request,
        response_mode="compact",
        artifact_root=artifact_root,
        target_limit=20,
    )
    if digest(compact) != EXPECTED_V1_COMPACT_SHA256[document]:
        raise RuntimeError(f"{document} P08C1 v1 compact comparator drift")
    if compact.get("artifact", {}).get("sha256") != EXPECTED_ARTIFACT_SHA256[document]:
        raise RuntimeError(f"{document} P08C1 detailed artifact identity drift")
    return compact, request, raw_audit, artifact_root


def load_verified_artifact(
    document: str,
    compact: Mapping[str, Any],
    request: Mapping[str, Any],
    raw_audit: Mapping[str, Any],
    artifact_root: Path,
) -> tuple[Path, dict[str, Any]]:
    artifact_path = (
        artifact_root
        / "document-derivation"
        / str(compact["audit_result_id"])
        / str(compact["audit_request_id"])
        / "detailed.json"
    )
    payload = artifact_path.read_bytes()
    actual_sha256 = hashlib.sha256(payload).hexdigest()
    expected_sha256 = EXPECTED_ARTIFACT_SHA256[document]
    if actual_sha256 != expected_sha256:
        raise RuntimeError(f"immutable {document} artifact drift: {actual_sha256}")
    artifact_binding = compact.get("artifact")
    if not isinstance(artifact_binding, Mapping):
        raise RuntimeError(f"{document} compact comparator has no artifact binding")
    if (
        artifact_binding.get("state") != "verified"
        or artifact_binding.get("schema_version") != ARTIFACT_SCHEMA
        or artifact_binding.get("sha256") != actual_sha256
        or artifact_binding.get("byte_count") != len(payload)
    ):
        raise RuntimeError(f"{document} compact artifact binding mismatch")
    try:
        record = json.loads(payload.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"{document} artifact is not valid UTF-8 JSON") from exc
    if not isinstance(record, dict) or canonical_bytes(record) != payload:
        raise RuntimeError(f"{document} artifact is not canonical JSON")
    if set(record) != {
        "schema_version",
        "audit_result_id",
        "audit_request_id",
        "audit_request",
        "audit",
        "authority",
        "non_claim",
    }:
        raise RuntimeError(f"{document} artifact has an unexpected top-level schema")
    if (
        record.get("schema_version") != ARTIFACT_SCHEMA
        or record.get("audit_result_id") != compact["audit_result_id"]
        or record.get("audit_request_id") != compact["audit_request_id"]
        or canonical_bytes(record.get("audit_request")) != canonical_bytes(request)
    ):
        raise RuntimeError(f"{document} artifact identity/request mismatch")
    persisted_audit = record.get("audit")
    expected_audit = response_module._without_presentation_fields(raw_audit)
    if (
        not isinstance(persisted_audit, dict)
        or canonical_bytes(persisted_audit) != canonical_bytes(expected_audit)
        or response_module.audit_result_id(persisted_audit) != compact["audit_result_id"]
    ):
        raise RuntimeError(f"{document} artifact audit projection mismatch")
    expected_record = response_module._artifact_record(expected_audit, request)
    if canonical_bytes(record) != canonical_bytes(expected_record):
        raise RuntimeError(f"{document} artifact record does not reconstruct exactly")
    return artifact_root, persisted_audit


def verify_compact_comparator(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    request: Mapping[str, Any],
    artifact_root: Path,
) -> None:
    errors = response_module.validate_document_derivation_response(audit, compact)
    if errors:
        raise RuntimeError(f"frozen compact comparator is invalid: {errors}")
    expected_targets: list[dict[str, Any]] = []
    expected_blockers: list[tuple[str, list[dict[str, Any]]]] = []
    for index, raw_target in enumerate(audit["targets"]):
        projected, blockers = response_module._compact_target(
            raw_target,
            index=index,
            result_id=compact["audit_result_id"],
            source_identity=str(request["source_identity"]),
            artifact_root=artifact_root,
        )
        expected_targets.append(projected)
        expected_blockers.append((projected["target_id"], blockers))
    if canonical_bytes(expected_targets) != canonical_bytes(compact["targets"]):
        raise RuntimeError("frozen compact target comparator does not reconstruct from artifact")
    expected_catalog = response_module._blocker_catalog(
        expected_blockers,
        result_id=compact["audit_result_id"],
        source_identity=str(request["source_identity"]),
        artifact_root=artifact_root,
    )
    if canonical_bytes(expected_catalog) != canonical_bytes(compact["blocker_catalog"]):
        raise RuntimeError("frozen grouped blocker catalog does not reconstruct from artifact")


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
        for name in OUTCOME_NAMES
    }


REGISTERED_ACTION_POLICY: dict[str, Any] = {
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


def project_action(
    action: Mapping[str, Any],
    global_veto_ids: list[str],
) -> dict[str, Any]:
    validated = validate_discriminating_action(action)
    if canonical_bytes(validated) != canonical_bytes(action):
        raise ValueError("selected action changes under the Phase 06 validator")
    expected = {
        **deepcopy(REGISTERED_ACTION_POLICY),
        "action_id": action.get("action_id"),
        "target_ids": deepcopy(action.get("branch_ids")),
        "branch_ids": deepcopy(action.get("branch_ids")),
        "launch_vetoes": deepcopy(action.get("launch_vetoes")),
    }
    if canonical_bytes(expected) != canonical_bytes(action):
        return {
            "representation": "inline_validated",
            "action": deepcopy(dict(validated)),
        }
    return {
        "representation": "registered_policy",
        "policy_id": ACTION_POLICY,
        "action_id": action["action_id"],
        "action_kind": action["action_kind"],
        "branch_ids": deepcopy(action["branch_ids"]),
        "launch_veto_indices": [
            global_veto_ids.index(value) for value in action["launch_vetoes"]
        ],
        "prerequisite": "resolve_nondominated_branch_choice",
        "expected_artifact_kind": "formalization_choice_record",
    }


def expand_action(
    projection: Mapping[str, Any],
    global_veto_ids: list[str],
) -> dict[str, Any]:
    if projection.get("representation") == "inline_validated":
        action = projection.get("action")
        if not isinstance(action, Mapping):
            raise ValueError("inline action projection is invalid")
        validated = validate_discriminating_action(action)
        if canonical_bytes(validated) != canonical_bytes(action):
            raise ValueError("inline action changes under the Phase 06 validator")
        return validated
    if projection.get("policy_id") != ACTION_POLICY:
        raise ValueError("unknown action projection policy")
    launch_veto_indices = projection.get("launch_veto_indices")
    if not isinstance(launch_veto_indices, list):
        raise ValueError("projected launch veto indices are invalid")
    action = {
        **deepcopy(REGISTERED_ACTION_POLICY),
        "action_id": projection["action_id"],
        "target_ids": deepcopy(projection["branch_ids"]),
        "branch_ids": deepcopy(projection["branch_ids"]),
        "launch_vetoes": checked_indices(
            launch_veto_indices,
            global_veto_ids,
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


def record_binding(identity: str, record: Any) -> dict[str, str]:
    return {
        "identity": identity,
        "raw_record_sha256": digest(record),
    }


def record_bindings(
    records: list[Mapping[str, Any]],
    identity_key: str,
) -> list[dict[str, str]]:
    bindings = [record_binding(str(record[identity_key]), record) for record in records]
    identities = [item["identity"] for item in bindings]
    pairs = [canonical_bytes(item) for item in bindings]
    if len(pairs) != len(set(pairs)):
        raise ValueError(f"{identity_key} collection contains a duplicate record binding")
    if not identities:
        return []
    return bindings


def raw_blocker_records(value: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for _, key, child in response_module._walk(value):
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
        identity = str(record.get("id", "")) or "blocker_" + digest(record)
        binding = record_binding(identity, record)
        by_binding.setdefault(canonical_bytes(binding), record)
    return [by_binding[key] for key in sorted(by_binding)]


def blocker_bindings(value: Any) -> list[dict[str, str]]:
    bindings: list[dict[str, str]] = []
    for record in raw_blocker_records(value):
        identity = str(record.get("id", "")) or "blocker_" + digest(record)
        bindings.append(record_binding(identity, record))
    return bindings


def target_content_identity(raw_target: Mapping[str, Any]) -> dict[str, str]:
    packet = raw_target.get("semantic_work_packet")
    if not isinstance(packet, Mapping):
        raise ValueError("raw target has no semantic work packet")
    obligation = packet.get("typed_repair_obligation")
    source_span = packet.get("source_span")
    target_text = packet.get("target")
    label_scoped = packet.get("label_scoped_obligation")
    if not isinstance(obligation, Mapping):
        raise ValueError("semantic work packet has no typed repair obligation")
    math_obligation = obligation.get("math_obligation")
    if not isinstance(math_obligation, Mapping):
        raise ValueError("typed repair obligation has no math obligation")
    if not isinstance(source_span, Mapping):
        raise ValueError("semantic work packet has no source span")
    if not isinstance(target_text, str) or not target_text:
        raise ValueError("semantic work packet has no target text")
    if not isinstance(label_scoped, Mapping):
        raise ValueError("semantic work packet has no label-scoped obligation")
    packet_id = packet.get("id")
    obligation_id = obligation.get("id")
    math_obligation_id = math_obligation.get("id")
    if not isinstance(packet_id, str) or not packet_id:
        raise ValueError("semantic work packet identity is missing")
    if not isinstance(obligation_id, str) or not obligation_id:
        raise ValueError("typed repair obligation identity is missing")
    if not isinstance(math_obligation_id, str) or not math_obligation_id:
        raise ValueError("math obligation identity is missing")
    return {
        "semantic_work_packet_id": packet_id,
        "label_scoped_obligation_id": str(label_scoped["obligation_id"]),
        "label_scoped_obligation_digest": str(label_scoped["obligation_digest"]),
        "label_scoped_obligation_sha256": digest(label_scoped),
        "typed_repair_obligation_id": obligation_id,
        "typed_repair_obligation_sha256": digest(obligation),
        "math_obligation_id": math_obligation_id,
        "math_obligation_sha256": digest(math_obligation),
        "source_span_sha256": digest(source_span),
        "target_text_sha256": digest(target_text),
    }


def checked_indices(
    indices: list[Any],
    values: list[str],
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


def target_collections(
    target: Mapping[str, Any],
    raw_target: Mapping[str, Any],
) -> dict[str, list[dict[str, str]]]:
    blockers = raw_blocker_records(raw_target)
    evidence_refs = response_module._evidence_ref_entries(raw_target)
    source_refs = response_module._source_ref_entries(raw_target)
    unresolved = response_module._collect_unresolved_assumptions(raw_target)
    candidates = response_module._collect_candidate_assumptions(raw_target)
    selected_action = response_module._selected_action(raw_target)
    if not isinstance(selected_action, Mapping):
        raise ValueError("raw target has no selected action")
    expected = {
        "evidence_refs": target["evidence_refs"],
        "source_refs": target["source_refs"],
        "unresolved_assumptions": target["unresolved_assumptions"],
        "candidate_assumptions": target["candidate_assumptions"],
    }
    actual = {
        "evidence_refs": evidence_refs,
        "source_refs": source_refs,
        "unresolved_assumptions": unresolved,
        "candidate_assumptions": candidates,
    }
    if canonical_bytes(actual) != canonical_bytes(expected):
        raise ValueError("raw target collections differ from the frozen compact comparator")
    blocker_ids = sorted(
        {
            str(item.get("id", "")) or "blocker_" + digest(item)
            for item in blockers
        }
    )
    if blocker_ids != target["blocker_ids"]:
        raise ValueError("raw blocker identities differ from the frozen compact comparator")
    if canonical_bytes(selected_action) != canonical_bytes(target["selected_action"]):
        raise ValueError("raw selected action differs from the frozen compact comparator")
    packet = raw_target["semantic_work_packet"]
    obligation = packet["typed_repair_obligation"]
    math_obligation = obligation["math_obligation"]
    return {
        "content_identity": target_content_identity(raw_target),
        "blocker_records": blocker_bindings(raw_target),
        "evidence_ref_records": record_bindings(evidence_refs, "evidence_ref_id"),
        "source_ref_records": record_bindings(source_refs, "source_ref_id"),
        "unresolved_assumption_records": record_bindings(unresolved, "id"),
        "candidate_assumption_records": record_bindings(candidates, "id"),
        "selected_action": [
            record_binding(selected_action["action_id"], selected_action)
        ],
        "label_scoped_obligation": [
            record_binding(
                str(packet["label_scoped_obligation"]["obligation_id"]),
                packet["label_scoped_obligation"],
            )
        ],
        "typed_repair_obligation": [
            record_binding(obligation["id"], obligation)
        ],
        "math_obligation": [
            record_binding(math_obligation["id"], math_obligation)
        ],
        "source_span": [
            record_binding(f"{packet['id']}#source_span", packet["source_span"])
        ],
        "target_text": [
            record_binding(f"{packet['id']}#target", packet["target"])
        ],
    }


def collection_map(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    target_indices: list[int],
) -> dict[str, Any]:
    evidence_refs = response_module._evidence_ref_entries(audit)
    source_refs = response_module._source_ref_entries(audit)
    reference_inventory = compact["reference_inventory"]
    if [item["ref"] for item in evidence_refs] != reference_inventory["evidence_refs"]:
        raise ValueError("global evidence records differ from the frozen inventory")
    if [item["evidence_ref_id"] for item in evidence_refs] != reference_inventory[
        "evidence_ref_ids"
    ]:
        raise ValueError("global evidence identities differ from the frozen inventory")
    if [item["source_ref_id"] for item in source_refs] != reference_inventory[
        "source_ref_ids"
    ]:
        raise ValueError("global source identities differ from the frozen inventory")
    targets: dict[str, Any] = {}
    for target_index in target_indices:
        target = compact["targets"][target_index]
        raw_target = audit["targets"][target_index]
        targets[target["target_id"]] = target_collections(target, raw_target)
    return {
        "global": {
            "global_blocker_records": blocker_bindings(audit),
            "global_evidence_ref_records": record_bindings(
                evidence_refs, "evidence_ref_id"
            ),
            "global_source_ref_records": record_bindings(source_refs, "source_ref_id"),
        },
        "targets": targets,
    }


def resolver_scope_descriptor(collections: Mapping[str, Any]) -> dict[str, Any]:
    global_values = collections.get("global")
    target_values = collections.get("targets")
    if not isinstance(global_values, Mapping) or set(global_values) != set(
        GLOBAL_RESOLVER_COLLECTIONS
    ):
        raise ValueError("resolver global scope is not the closed collection set")
    if not isinstance(target_values, Mapping):
        raise ValueError("resolver target scope is not a mapping")

    scopes: list[dict[str, Any]] = []
    for collection in GLOBAL_RESOLVER_COLLECTIONS:
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
    expected_target_keys = {"content_identity", *TARGET_RESOLVER_COLLECTIONS}
    for target_id, per_target in target_values.items():
        if not isinstance(target_id, str) or not target_id:
            raise ValueError("resolver target scope has no target identity")
        if not isinstance(per_target, Mapping) or set(per_target) != expected_target_keys:
            raise ValueError("resolver target scope is not the closed collection set")
        for collection in TARGET_RESOLVER_COLLECTIONS:
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
        "schema_version": RESOLVER_SCOPE_SCHEMA,
        "global_target_sentinel": None,
        "scopes": scopes,
    }


def page_boundary(
    compact: Mapping[str, Any],
    target_indices: list[int],
    page_index: int,
    previous_offset: int,
    next_offset: int,
    requested_target_limit: int,
) -> dict[str, Any]:
    return {
        "response_schema_version": RESPONSE_SCHEMA,
        "artifact_schema_version": ARTIFACT_SCHEMA,
        "compact_representation": "artifact_indexed",
        "byte_policy_version": BYTE_POLICY,
        "canonical_limit": CANONICAL_LIMIT,
        "transport_limit": TRANSPORT_LIMIT,
        "requested_target_limit": requested_target_limit,
        "page_index": page_index,
        "previous_offset": previous_offset,
        "next_offset": next_offset,
        "target_ids": [compact["targets"][index]["target_id"] for index in target_indices],
        "filter_id": compact["page"]["filter_id"],
    }


def _identity_digest(value: Any, prefix: str, field: str) -> bytes:
    if not isinstance(value, str) or not value.startswith(prefix):
        raise ValueError(f"{field} is not a {prefix} identity")
    suffix = value[len(prefix) :]
    if len(suffix) != 64:
        raise ValueError(f"{field} digest length is invalid")
    try:
        return bytes.fromhex(suffix)
    except ValueError as exc:
        raise ValueError(f"{field} digest is not lowercase hexadecimal") from exc


def decode_page_token(token: str) -> dict[str, Any]:
    if not isinstance(token, str) or not token or "=" in token:
        raise ValueError("page token must be nonempty unpadded base64url")
    try:
        raw = base64.b64decode(
            token + "=" * (-len(token) % 4),
            altchars=b"-_",
            validate=True,
        )
    except (ValueError, TypeError) as exc:
        raise ValueError("page token is not strict base64url") from exc
    if len(raw) != TOKEN_SIZE or raw[: len(TOKEN_MAGIC)] != TOKEN_MAGIC:
        raise ValueError("page token version or length is invalid")
    if base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=") != token:
        raise ValueError("page token is not canonical base64url")
    cursor = len(TOKEN_MAGIC)
    policy, requested_limit, page_index, previous_offset, next_offset = struct.unpack(
        "!BBHHH", raw[cursor : cursor + 8]
    )
    cursor += 8
    chunks = [raw[cursor + index * 32 : cursor + (index + 1) * 32] for index in range(7)]
    payload = raw[:-32]
    if policy != BYTE_POLICY_CODE or hashlib.sha256(payload).digest() != chunks[-1]:
        raise ValueError("page token policy or checksum is invalid")
    if not 1 <= requested_limit <= 100:
        raise ValueError("page token requested limit is invalid")
    if not previous_offset < next_offset <= 65_535 or page_index > previous_offset:
        raise ValueError("page token offsets are invalid")
    return {
        "schema_version": CURSOR_SCHEMA,
        "selector_schema_version": SELECTOR_SCHEMA,
        "audit_result_id": "audit_" + chunks[0].hex(),
        "audit_request_id": "request_" + chunks[1].hex(),
        "artifact_sha256": chunks[2].hex(),
        "filter_id": "filter_" + chunks[3].hex(),
        "byte_policy_version": BYTE_POLICY,
        "requested_target_limit": requested_limit,
        "page_index": page_index,
        "previous_offset": previous_offset,
        "next_offset": next_offset,
        "page_boundary_digest": chunks[4].hex(),
        "resolver_scope_digest": chunks[5].hex(),
        "checksum": chunks[6].hex(),
    }


def encode_page_token(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    target_indices: list[int],
    page_index: int,
    previous_offset: int,
    next_offset: int,
    requested_limit: int,
) -> str:
    if not 1 <= requested_limit <= 100:
        raise ValueError("page token requested limit is invalid")
    if any(value > 65_535 for value in (page_index, previous_offset, next_offset)):
        raise ValueError("page token index exceeds the closed two-byte range")
    payload = b"".join(
        [
            TOKEN_MAGIC,
            struct.pack(
                "!BBHHH",
                BYTE_POLICY_CODE,
                requested_limit,
                page_index,
                previous_offset,
                next_offset,
            ),
            _identity_digest(compact["audit_result_id"], "audit_", "audit_result_id"),
            _identity_digest(compact["audit_request_id"], "request_", "audit_request_id"),
            bytes.fromhex(compact["artifact"]["sha256"]),
            _identity_digest(compact["page"]["filter_id"], "filter_", "filter_id"),
            bytes.fromhex(
                digest(
                    page_boundary(
                        compact,
                        target_indices,
                        page_index,
                        previous_offset,
                        next_offset,
                        requested_limit,
                    )
                )
            ),
            bytes.fromhex(
                digest(
                    resolver_scope_descriptor(
                        collection_map(compact, audit, target_indices)
                    )
                )
            ),
        ]
    )
    raw = payload + hashlib.sha256(payload).digest()
    token = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    decoded = decode_page_token(token)
    if decoded["artifact_sha256"] != compact["artifact"]["sha256"]:
        raise ValueError("page token failed artifact round trip")
    return token


def _page_tables(targets: list[Mapping[str, Any]]) -> dict[str, list[str]]:
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
                item["source_ref_id"] for target in targets for item in target["source_refs"]
            )
        ),
    }


def _project_target(
    compact: Mapping[str, Any],
    target: Mapping[str, Any],
    raw_target: Mapping[str, Any],
    tables: Mapping[str, list[str]],
    target_values: Mapping[str, Any],
) -> dict[str, Any]:
    raw_selected_action = response_module._selected_action(raw_target)
    if not isinstance(raw_selected_action, Mapping):
        raise ValueError("stored audit target has no selected action")
    return {
        "target_id": target["target_id"],
        "label": target["label"],
        "row_id": target["row_id"],
        "row_index": target["row_index"],
        "location": target["location"],
        "content_identity": target_content_identity(raw_target),
        "status": target["status"],
        "publication_mode": target["publication_mode"],
        "promotion_ref": "global",
        "failure_classification_indices": [
            compact["failure_classifications"].index(value)
            for value in target["failure_classifications"]
        ],
        "veto_indices": [compact["veto_ids"].index(value) for value in target["veto_ids"]],
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
        "blocker_indices": [tables["blocker_ids"].index(value) for value in target["blocker_ids"]],
        "evidence_ref_indices": [
            tables["evidence_refs"].index(item["ref"]) for item in target["evidence_refs"]
        ],
        "source_ref_indices": [
            tables["source_ref_ids"].index(item["source_ref_id"])
            for item in target["source_refs"]
        ],
        "selected_action": project_action(raw_selected_action, compact["veto_ids"]),
    }


def compile_projected_page(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    page_index: int,
    previous_offset: int,
    target_count: int,
    requested_limit: int = 20,
) -> dict[str, Any]:
    if target_count < 1:
        raise ValueError("projected page must contain at least one target")
    target_indices = list(range(previous_offset, previous_offset + target_count))
    targets = [compact["targets"][index] for index in target_indices]
    raw_targets = [audit["targets"][index] for index in target_indices]
    collections = collection_map(compact, audit, target_indices)
    tables = _page_tables(targets)
    target_projections = [
        _project_target(
            compact,
            target,
            raw_target,
            tables,
            collections["targets"][target["target_id"]],
        )
        for target, raw_target in zip(targets, raw_targets, strict=True)
    ]
    next_offset = previous_offset + target_count
    boundary = page_boundary(
        compact,
        target_indices,
        page_index,
        previous_offset,
        next_offset,
        requested_limit,
    )
    page_token = encode_page_token(
        compact,
        audit,
        target_indices,
        page_index,
        previous_offset,
        next_offset,
        requested_limit,
    )
    global_values = collections["global"]
    response = {
        "metadata": deepcopy(compact["metadata"]),
        "response_schema_version": RESPONSE_SCHEMA,
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
        "veto_ids": deepcopy(compact["veto_ids"]),
        "unresolved_assumption_ids": deepcopy(compact["unresolved_assumption_ids"]),
        "candidate_assumption_ids": deepcopy(compact["candidate_assumption_ids"]),
        "action_decision_ids": deepcopy(compact["action_decision_ids"]),
        "non_claims": deepcopy(compact["non_claims"]),
        "execution_summary": deepcopy(compact["execution_summary"]),
        "output_references": deepcopy(compact["output_references"]),
        "artifact": {
            "state": "verified",
            "schema_version": ARTIFACT_SCHEMA,
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
            "global_source_ref_count": len(global_values["global_source_ref_records"]),
            "resolution": "page_token",
        },
        "page_identity_tables": tables,
        "targets": target_projections,
        "page": {
            "page_index": page_index,
            "previous_offset": previous_offset,
            "next_offset": next_offset,
            "requested_limit": requested_limit,
            "effective_limit": target_count,
            "included_target_count": target_count,
            "total_target_count": len(compact["targets"]),
            "target_ids": [target["target_id"] for target in targets],
            "continuation_available": next_offset < len(compact["targets"]),
            "filter_id": compact["page"]["filter_id"],
            "byte_policy_version": BYTE_POLICY,
            "page_token": page_token,
        },
        "completeness": {
            "global_boundary": "complete",
            "current_target_identities": "literal_page_tables",
            "global_and_full_records": "verified_page_token",
        },
        "payload_guardrail": {
            "canonical_target_bytes": CANONICAL_LIMIT,
            "transport_target_bytes": TRANSPORT_LIMIT,
            "status": "pending",
            "authority": "product_usability_only",
        },
        "canonical_byte_count": 0,
    }
    while True:
        measured = len(canonical_bytes(response))
        status = (
            "met"
            if measured <= CANONICAL_LIMIT
            else "exceeded_complete_boundary_preserved"
        )
        if (
            response["canonical_byte_count"] == measured
            and response["payload_guardrail"]["status"] == status
        ):
            break
        response["canonical_byte_count"] = measured
        response["payload_guardrail"]["status"] = status

    for target, raw_target, projection in zip(
        targets, raw_targets, target_projections, strict=True
    ):
        raw_selected_action = response_module._selected_action(raw_target)
        expanded = expand_action(projection["selected_action"], compact["veto_ids"])
        if canonical_bytes(expanded) != canonical_bytes(raw_selected_action):
            raise ValueError("projected action does not expand to the exact frozen action")
        if checked_indices(
            projection["blocker_indices"], tables["blocker_ids"], field="blocker_indices", allow_duplicates=False
        ) != target["blocker_ids"]:
            raise ValueError("blocker indices do not expand to the frozen target identities")
        if checked_indices(
            projection["evidence_ref_indices"], tables["evidence_refs"], field="evidence_ref_indices", allow_duplicates=False
        ) != [item["ref"] for item in target["evidence_refs"]]:
            raise ValueError("evidence indices do not expand to the frozen target references")
        if checked_indices(
            projection["source_ref_indices"], tables["source_ref_ids"], field="source_ref_indices", allow_duplicates=False
        ) != [item["source_ref_id"] for item in target["source_refs"]]:
            raise ValueError("source indices do not expand to the frozen target identities")
        target_values = collections["targets"][target["target_id"]]
        if checked_indices(
            projection["unresolved_assumption_indices"], compact["unresolved_assumption_ids"], field="unresolved_assumption_indices", allow_duplicates=True
        ) != [item["identity"] for item in target_values["unresolved_assumption_records"]]:
            raise ValueError("unresolved assumption indices do not preserve record occurrences")
        if checked_indices(
            projection["candidate_assumption_indices"], compact["candidate_assumption_ids"], field="candidate_assumption_indices", allow_duplicates=True
        ) != [item["identity"] for item in target_values["candidate_assumption_records"]]:
            raise ValueError("candidate assumption indices do not preserve record occurrences")
    return response


def measure_page(response: Mapping[str, Any]) -> dict[str, int]:
    facade = {**deepcopy(dict(response)), "ok": True}
    result = CallToolResult(
        content=[TextContent(type="text", text=COMPATIBILITY_TEXT)],
        structuredContent=facade,
        isError=False,
    )
    result_json = result.model_dump_json(by_alias=True, exclude_none=True)
    stdio = (
        JSONRPCMessage(
            root=JSONRPCResponse(
                jsonrpc="2.0",
                id=1,
                result=result.model_dump(by_alias=True, exclude_none=True),
            )
        ).model_dump_json(by_alias=True, exclude_none=True).encode("utf-8")
        + b"\n"
    )
    return {
        "canonical_response": len(canonical_bytes(response)),
        "cli_stdout": len(canonical_bytes(response) + b"\n"),
        "facade": len(canonical_bytes(facade)),
        "call_tool_result": len(result_json.encode("utf-8") + b"\n"),
        "stdio_jsonrpc_line": len(stdio),
        "page_token": len(response["page"]["page_token"]),
    }


def resolver_surface_sizes(response: Mapping[str, Any]) -> dict[str, int]:
    facade = {**deepcopy(dict(response)), "ok": True}
    result = CallToolResult(
        content=[TextContent(type="text", text=COMPATIBILITY_TEXT)],
        structuredContent=facade,
        isError=False,
    )
    result_json = result.model_dump_json(by_alias=True, exclude_none=True)
    stdio = (
        JSONRPCMessage(
            root=JSONRPCResponse(
                jsonrpc="2.0",
                id=1,
                result=result.model_dump(by_alias=True, exclude_none=True),
            )
        ).model_dump_json(by_alias=True, exclude_none=True).encode("utf-8")
        + b"\n"
    )
    return {
        "canonical_response": len(canonical_bytes(response)),
        "cli_stdout": len(canonical_bytes(response) + b"\n"),
        "facade": len(canonical_bytes(facade)),
        "call_tool_result": len(result_json.encode("utf-8") + b"\n"),
        "stdio_jsonrpc_line": len(stdio),
    }


def resolver_record(
    identity: str,
    record: Any,
    *,
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    artifact_root: Path,
) -> dict[str, Any]:
    return {
        "identity": identity,
        "raw_record_sha256": digest(record),
        "record": response_module._redact_transport(
            record,
            result_id=compact["audit_result_id"],
            source_identity=str(audit["tex_path"]),
            artifact_root=artifact_root,
        ),
    }


def resolver_page(
    compact: Mapping[str, Any],
    *,
    page_index: int,
    target_id: str | None,
    collection: str,
    offset: int,
    limit: int,
    records: list[dict[str, Any]],
    scope_digest: str,
) -> tuple[dict[str, Any], dict[str, int]]:
    if not records:
        if offset != 0:
            raise ValueError("resolver offset is outside the empty collection")
        response = {
            "schema_version": "p08d_document_derivation_record_page@1",
            "authority": "diagnostic_presentation_only",
            "audit_result_id": compact["audit_result_id"],
            "audit_request_id": compact["audit_request_id"],
            "artifact": {
                "state": "verified",
                "schema_version": ARTIFACT_SCHEMA,
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
            "resolver_scope_digest": scope_digest,
            "payload_guardrail": {
                "transport_target_bytes": TRANSPORT_LIMIT,
                "status": "met",
                "authority": "product_usability_only",
            },
            "non_claim": (
                "Resolved records are evidence navigation, not proof or publication "
                "authority."
            ),
        }
        return response, resolver_surface_sizes(response)
    if offset < 0 or offset >= len(records):
        raise ValueError("resolver offset is outside the nonempty collection")
    selected: list[dict[str, Any]] = []
    response: dict[str, Any] = {}
    sizes: dict[str, int] = {}
    for record in records[offset : offset + limit]:
        candidate = [*selected, record]
        next_offset = offset + len(candidate)
        response = {
            "schema_version": "p08d_document_derivation_record_page@1",
            "authority": "diagnostic_presentation_only",
            "audit_result_id": compact["audit_result_id"],
            "audit_request_id": compact["audit_request_id"],
            "artifact": {
                "state": "verified",
                "schema_version": ARTIFACT_SCHEMA,
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
            "resolver_scope_digest": scope_digest,
            "payload_guardrail": {
                "transport_target_bytes": TRANSPORT_LIMIT,
                "status": "pending",
                "authority": "product_usability_only",
            },
            "non_claim": (
                "Resolved records are evidence navigation, not proof or publication "
                "authority."
            ),
        }
        response["payload_guardrail"]["status"] = "met"
        sizes = resolver_surface_sizes(response)
        if any(
            sizes[key] > TRANSPORT_LIMIT
            for key in ("cli_stdout", "facade", "call_tool_result", "stdio_jsonrpc_line")
        ):
            if not selected:
                response["payload_guardrail"]["status"] = (
                    "exceeded_complete_record_preserved"
                )
                return response, resolver_surface_sizes(response)
            break
        selected = candidate
    if not selected:
        raise ValueError("resolver did not select a complete record")
    if len(response["records"]) != len(selected):
        next_offset = offset + len(selected)
        response["records"] = selected
        response["returned_record_count"] = len(selected)
        response["next_offset"] = next_offset if next_offset < len(records) else None
        sizes = resolver_surface_sizes(response)
    return response, sizes


def resolver_collections(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    target_index: int,
    artifact_root: Path,
) -> dict[tuple[str | None, str], list[dict[str, Any]]]:
    target = audit["targets"][target_index]
    compact_target = compact["targets"][target_index]
    blocker_records = raw_blocker_records(target)
    selected_action = response_module._selected_action(target)
    if not isinstance(selected_action, Mapping):
        raise ValueError("stored audit target has no selected action")
    packet = target["semantic_work_packet"]
    label_scoped = packet["label_scoped_obligation"]
    obligation = packet["typed_repair_obligation"]
    math_obligation = obligation["math_obligation"]
    return {
        (None, "global_blocker_records"): [
            resolver_record(
                str(item.get("id", "")) or "blocker_" + digest(item),
                item,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
            for item in raw_blocker_records(audit)
        ],
        (None, "global_evidence_ref_records"): [
            resolver_record(
                item["evidence_ref_id"],
                item,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
            for item in response_module._evidence_ref_entries(audit)
        ],
        (None, "global_source_ref_records"): [
            resolver_record(
                item["source_ref_id"],
                item,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
            for item in response_module._source_ref_entries(audit)
        ],
        (compact_target["target_id"], "blocker_records"): [
            resolver_record(
                str(item.get("id", "")) or "blocker_" + digest(item),
                item,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
            for item in blocker_records
        ],
        (compact_target["target_id"], "evidence_ref_records"): [
            resolver_record(
                item["evidence_ref_id"],
                item,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
            for item in response_module._evidence_ref_entries(target)
        ],
        (compact_target["target_id"], "source_ref_records"): [
            resolver_record(
                item["source_ref_id"],
                item,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
            for item in response_module._source_ref_entries(target)
        ],
        (compact_target["target_id"], "unresolved_assumption_records"): [
            resolver_record(
                item["id"],
                item,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
            for item in response_module._collect_unresolved_assumptions(target)
        ],
        (compact_target["target_id"], "candidate_assumption_records"): [
            resolver_record(
                item["id"],
                item,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
            for item in response_module._collect_candidate_assumptions(target)
        ],
        (compact_target["target_id"], "selected_action"): [
            resolver_record(
                selected_action["action_id"],
                selected_action,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
        ],
        (compact_target["target_id"], "label_scoped_obligation"): [
            resolver_record(
                label_scoped["obligation_id"],
                label_scoped,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
        ],
        (compact_target["target_id"], "typed_repair_obligation"): [
            resolver_record(
                obligation["id"],
                obligation,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
        ],
        (compact_target["target_id"], "math_obligation"): [
            resolver_record(
                math_obligation["id"],
                math_obligation,
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
        ],
        (compact_target["target_id"], "source_span"): [
            resolver_record(
                f"{packet['id']}#source_span",
                packet["source_span"],
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
        ],
        (compact_target["target_id"], "target_text"): [
            resolver_record(
                f"{packet['id']}#target",
                packet["target"],
                compact=compact,
                audit=audit,
                artifact_root=artifact_root,
            )
        ],
    }


def page_fits(sizes: Mapping[str, int]) -> bool:
    return sizes["canonical_response"] <= CANONICAL_LIMIT and all(
        sizes[surface] <= TRANSPORT_LIMIT
        for surface in ("cli_stdout", "facade", "call_tool_result", "stdio_jsonrpc_line")
    )


def longest_prefix_page(
    compact: Mapping[str, Any],
    audit: Mapping[str, Any],
    *,
    page_index: int,
    previous_offset: int,
    requested_limit: int = 20,
) -> tuple[dict[str, Any], dict[str, int]]:
    remaining = len(compact["targets"]) - previous_offset
    maximum = min(requested_limit, remaining)
    selected: tuple[dict[str, Any], dict[str, int]] | None = None
    for target_count in range(1, maximum + 1):
        response = compile_projected_page(
            compact,
            audit,
            page_index,
            previous_offset,
            target_count,
            requested_limit,
        )
        sizes = measure_page(response)
        if not page_fits(sizes):
            break
        selected = response, sizes
    if selected is not None:
        return selected
    response = compile_projected_page(
        compact,
        audit,
        page_index,
        previous_offset,
        1,
        requested_limit,
    )
    return response, measure_page(response)


def main() -> int:
    if importlib.metadata.version("mcp") != "1.27.0":
        raise RuntimeError("feasibility check requires the pinned mcp==1.27.0")
    for name, expected in EXPECTED_INPUT_SHA256.items():
        actual = file_sha256(P08C1_RUN_ROOT / name)
        if actual != expected:
            raise RuntimeError(f"verified P08C1 input drift: {name}: {actual}")
    if file_sha256(P08A_EXTRACTION) != EXPECTED_P08A_EXTRACTION_SHA256:
        raise RuntimeError("immutable P08A extraction comparator drift")
    snapshot_response = P08C_SNAPSHOT_SRC / "mathdevmcp/document_derivation_response.py"
    snapshot_ledger = P08C_SNAPSHOT_SRC / "mathdevmcp/failure_ledgers.py"
    live_response = REPO_ROOT / "src/mathdevmcp/document_derivation_response.py"
    live_ledger = REPO_ROOT / "src/mathdevmcp/failure_ledgers.py"
    if {
        file_sha256(snapshot_response),
        file_sha256(live_response),
    } != {EXPECTED_RESPONSE_MODULE_SHA256}:
        raise RuntimeError("response compiler differs from the bound P08C1 projection code")
    if {
        file_sha256(snapshot_ledger),
        file_sha256(live_ledger),
    } != {EXPECTED_FAILURE_LEDGER_SHA256}:
        raise RuntimeError("action validator differs from the bound P08C1 projection code")
    decision = json.loads((P08C1_RUN_ROOT / "decision.json").read_text())
    fidelity = json.loads((P08C1_RUN_ROOT / "target-fidelity.json").read_text())
    if (
        decision.get("status") != "PASS_P08C1_TARGET_FIDELITY"
        or decision.get("primary_criterion_met") is not True
        or decision.get("vetoes") != []
        or fidelity.get("primary_criterion_met") is not True
        or fidelity.get("vetoes") != []
        or fidelity.get("ordered_target_labels")
        != [
            "eq:panel-npv-functional",
            "eq:incremental-cash-flow",
            "eq:incremental-npv",
            "eq:foc-k",
            "eq:foc-b",
        ]
    ):
        raise RuntimeError("P08C1 target-fidelity decision is not a passing baseline")

    measurements: dict[str, list[dict[str, Any]]] = {}
    resolver_measurements: dict[str, list[dict[str, Any]]] = {}
    with tempfile.TemporaryDirectory(prefix="p08d-p08c1-feasibility-") as temporary:
      artifact_parent = Path(temporary)
      for document in ("card", "risky"):
        compact, request, raw_audit, artifact_root = build_v1_comparator(
            document, artifact_parent
        )
        artifact_root, audit = load_verified_artifact(
            document,
            compact,
            request,
            raw_audit,
            artifact_root,
        )
        verify_compact_comparator(compact, audit, request, artifact_root)
        pages: list[dict[str, Any]] = []
        resolved_pages: list[dict[str, Any]] = []
        page_index = 0
        previous_offset = 0
        ordered_union: list[str] = []
        while previous_offset < len(compact["targets"]):
            response, sizes = longest_prefix_page(
                compact,
                audit,
                page_index=page_index,
                previous_offset=previous_offset,
                requested_limit=20,
            )
            if not page_fits(sizes):
                raise RuntimeError(
                    f"{document} page {page_index} has no complete target within limits"
                )
            pages.append(
                {
                    "page_index": page_index,
                    "previous_offset": previous_offset,
                    "next_offset": response["page"]["next_offset"],
                    "target_ids": response["page"]["target_ids"],
                    "sizes": sizes,
                }
            )
            ordered_union.extend(response["page"]["target_ids"])
            decoded_token = decode_page_token(response["page"]["page_token"])
            target_indices = list(
                range(previous_offset, int(response["page"]["next_offset"]))
            )
            boundary = page_boundary(
                compact,
                target_indices,
                page_index,
                previous_offset,
                int(response["page"]["next_offset"]),
                20,
            )
            collections_for_scope = collection_map(compact, audit, target_indices)
            expected_token = {
                "audit_result_id": compact["audit_result_id"],
                "audit_request_id": compact["audit_request_id"],
                "artifact_sha256": compact["artifact"]["sha256"],
                "filter_id": compact["page"]["filter_id"],
                "page_index": page_index,
                "previous_offset": previous_offset,
                "next_offset": response["page"]["next_offset"],
                "requested_target_limit": 20,
                "page_boundary_digest": digest(boundary),
                "resolver_scope_digest": digest(
                    resolver_scope_descriptor(collections_for_scope)
                ),
            }
            if any(decoded_token[key] != value for key, value in expected_token.items()):
                raise RuntimeError("page token does not reconstruct the exact page boundary")
            collections: dict[tuple[str | None, str], list[dict[str, Any]]] = {}
            for position, target_index in enumerate(target_indices):
                target_collections_for_index = resolver_collections(
                    compact,
                    audit,
                    target_index,
                    artifact_root,
                )
                for key, value in target_collections_for_index.items():
                    if key[0] is None and position > 0:
                        continue
                    collections[key] = value
            for (target_id, collection), records in collections.items():
                offset = 0
                resolved_bindings: list[dict[str, str]] = []
                first_page = True
                while first_page or offset < len(records):
                    first_page = False
                    resolved, resolved_sizes = resolver_page(
                        compact,
                        page_index=page_index,
                        target_id=target_id,
                        collection=collection,
                        offset=offset,
                        limit=100,
                        records=records,
                        scope_digest=decoded_token["resolver_scope_digest"],
                    )
                    if resolved["payload_guardrail"]["status"] != "met":
                        raise RuntimeError(
                            f"{document} page {page_index} {collection} has an "
                            "oversize complete resolver record"
                        )
                    serialized_resolver = canonical_bytes(resolved).decode("utf-8")
                    if response_module._ABSOLUTE_PATH_FRAGMENT.search(serialized_resolver):
                        raise RuntimeError("resolver projection leaked an absolute local path")
                    if any(
                        resolved_sizes[key] > TRANSPORT_LIMIT
                        for key in (
                            "cli_stdout",
                            "facade",
                            "call_tool_result",
                            "stdio_jsonrpc_line",
                        )
                    ):
                        raise RuntimeError(
                            f"{document} page {page_index} {collection} resolver "
                            "envelope exceeds transport limit"
                        )
                    resolved_pages.append(
                        {
                            "page_index": page_index,
                            "target_id": target_id,
                            "collection": collection,
                            "offset": offset,
                            "returned_record_count": resolved[
                                "returned_record_count"
                            ],
                            "sizes": resolved_sizes,
                        }
                    )
                    resolved_bindings.extend(
                        {
                            "identity": item["identity"],
                            "raw_record_sha256": item["raw_record_sha256"],
                        }
                        for item in resolved["records"]
                    )
                    next_offset = resolved["next_offset"]
                    if next_offset is None:
                        break
                    if not isinstance(next_offset, int) or next_offset <= offset:
                        raise RuntimeError("resolver pagination did not advance")
                    offset = next_offset
                expected_bindings = [
                    {
                        "identity": item["identity"],
                        "raw_record_sha256": item["raw_record_sha256"],
                    }
                    for item in records
                ]
                if canonical_bytes(resolved_bindings) != canonical_bytes(
                    expected_bindings
                ):
                    raise RuntimeError(
                        f"{document} page {page_index} {collection} resolver union drift"
                    )
            previous_offset = int(response["page"]["next_offset"])
            page_index += 1
        expected_order = [target["target_id"] for target in compact["targets"]]
        if ordered_union != expected_order or len(ordered_union) != len(set(ordered_union)):
            raise RuntimeError(f"{document} page union omitted, duplicated, or reordered a target")
        measurements[document] = pages
        resolver_measurements[document] = resolved_pages

    output = {
        "schema_version": "p08d_payload_feasibility@2",
        "baseline": "PASS_P08C1_TARGET_FIDELITY",
        "status": "PASS_P08C1_BOUND_P08D_FEASIBILITY",
        "mcp_version": importlib.metadata.version("mcp"),
        "canonical_limit": CANONICAL_LIMIT,
        "transport_limit": TRANSPORT_LIMIT,
        "measurements": measurements,
        "resolver_measurements": resolver_measurements,
        "non_claim": (
            "This read-only projection establishes implementation feasibility, not "
            "production payload conformance or mathematical correctness."
        ),
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
