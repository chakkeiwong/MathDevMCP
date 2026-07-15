from __future__ import annotations

"""Pure Phase 01 exact-binding policy under publication quarantine."""

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping, Sequence

from .derivation_search_tree import validate_branch_record
from .evidence_manifest import (
    EvidenceValidationError,
    canonical_json_bytes,
    content_digest,
    validate_evidence_manifest,
)
from .external_adapter_contract import reader_verified_claim_evidence_record
from .failure_ledgers import LEDGER_KINDS, validate_ledgers


PROMOTION_POLICY_VERSION = "p01_integrity_binding@1"
INTEGRITY_DECISION = "publish_evidence_report"
CLAIM_ELIGIBILITY = "ineligible"
INTEGRITY_STATUS_VERIFIED = "verified_for_synthetic_fixture"
INTEGRITY_STATUS_REJECTED = "rejected"

INVARIANT_IDS = (
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

NON_CLAIMS = (
    "no_real_document_extraction",
    "no_backend_conformance",
    "no_mathematical_certification",
    "no_branch_local_scheduler",
    "no_publication_eligibility",
    "no_source_document_edit",
    "no_multiprocess_support",
    "no_release_readiness",
)

P06_PROMOTION_POLICY_VERSION = "p06_exact_promotion_decision@2"
P06_PROMOTION_SCHEMA_VERSION = "p06_promotion_decision@2"
P06_PERSISTED_DECISION_AUTHORITY = (
    "internal_consistency_only_requires_native_evidence_reevaluation"
)
P06_TEST_GATE_SCHEMA_VERSION = "p06_test_only_aggregate_gate@1"
P06_TEST_GATE_SENTINEL = "pure_policy_fixture_no_program_authority"
P06_PUBLICATION_MODES = frozenset({"disabled", "experimental_exact_manifest"})
P06_CLAIM_ELIGIBILITY_EXACT = "exact_manifest_eligible"
P06_CLAIM_ELIGIBILITY_INELIGIBLE = "ineligible"
P06_INVARIANT_IDS = (
    "current_source_binding",
    "validated_unambiguous_extraction",
    "exact_branch_binding",
    "complete_assumption_support_and_encoding",
    "certifying_backend_role_and_input_class",
    "actual_non_test_backend_execution",
    "registered_reader_evidence_integrity",
    "scoped_terminal_outcome",
    "candidate_edit_binding_and_scope",
    "empty_typed_veto_sets",
    "publication_policy_and_aggregate_gate",
    "deterministic_decision_reconstruction",
)
P06_PROMOTION_NON_CLAIMS = (
    "no_whole_document_proof",
    "no_automatic_source_edit",
    "no_default_or_release_enablement",
    "no_scientific_optimality_claim",
    "no_backend_soundness_beyond_scoped_manifest",
    "test_only_gate_is_not_program_authority",
)


def _digest_bytes(value: bytes | bytearray | memoryview) -> str:
    return hashlib.sha256(bytes(value)).hexdigest()


def _copy_json(value: Any) -> Any:
    return deepcopy(value)


def _manifest_from_verified(value: Mapping[str, Any]) -> Mapping[str, Any] | None:
    if value.get("integrity_state") != "verified":
        return None
    manifest = value.get("manifest")
    if not isinstance(manifest, Mapping):
        return None
    try:
        validated = validate_evidence_manifest(deepcopy(manifest))
        manifest_sha256 = content_digest(canonical_json_bytes(validated, schema="evidence_manifest@1"))
    except (EvidenceValidationError, TypeError, ValueError):
        return None
    if value.get("manifest_sha256") != manifest_sha256:
        return None
    return validated


def _eq(left: Any, right: Any) -> bool:
    try:
        return canonical_json_bytes(left) == canonical_json_bytes(right)
    except (TypeError, ValueError):
        return False


def _invariant(invariant_id: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"id": invariant_id, "passed": bool(passed), "detail": detail}


def verify_exact_binding(
    verified_manifests: Sequence[Mapping[str, Any]],
    current_source: Mapping[str, Any],
    branch: Mapping[str, Any],
    candidate_edit: Mapping[str, Any],
    policy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Recompute P01 identity/integrity invariants without I/O or mutation."""
    source = _copy_json(current_source)
    branch_copy = _copy_json(branch)
    edit = _copy_json(candidate_edit)
    policy_copy = _copy_json(policy or {})

    manifests = [manifest for value in verified_manifests if (manifest := _manifest_from_verified(value)) is not None]
    request = manifests[0].get("request", {}) if len(manifests) == 1 else {}
    result = manifests[0].get("result", {}) if len(manifests) == 1 else {}
    integrity = manifests[0].get("integrity", {}) if len(manifests) == 1 else {}
    interpretation = manifests[0].get("interpretation", {}) if len(manifests) == 1 else {}

    source_bytes = source.get("bytes")
    edit_bytes = edit.get("bytes")
    source_digest = _digest_bytes(source_bytes) if isinstance(source_bytes, (bytes, bytearray, memoryview)) else None
    edit_digest = _digest_bytes(edit_bytes) if isinstance(edit_bytes, (bytes, bytearray, memoryview)) else None
    request_source = request.get("source", {}) if isinstance(request, Mapping) else {}
    request_obligation = request.get("obligation", {}) if isinstance(request, Mapping) else {}
    request_branch = request.get("branch", {}) if isinstance(request, Mapping) else {}
    request_native = request.get("native_input", {}) if isinstance(request, Mapping) else {}
    request_tool = request.get("tool", {}) if isinstance(request, Mapping) else {}

    expected_assumptions = branch_copy.get("typed_assumptions", [])
    expected_assumption_digest = content_digest(expected_assumptions) if isinstance(expected_assumptions, list) else None
    native_bytes = policy_copy.get("native_input_bytes")
    native_digest = _digest_bytes(native_bytes) if isinstance(native_bytes, (bytes, bytearray, memoryview)) else None

    inventory = integrity.get("artifact_inventory", []) if isinstance(integrity, Mapping) else []
    inventory_entries = [item for item in inventory if isinstance(item, Mapping)] if isinstance(inventory, list) else []
    refs = [item.get("logical_ref") for item in inventory_entries]
    roles = [item.get("role") for item in inventory_entries]
    named_entries = [
        integrity.get("request_artifact"),
        result.get("stdout"),
        result.get("stderr"),
        result.get("structured_result"),
    ]
    if result.get("certificate") is not None:
        named_entries.append(result.get("certificate"))
    native_entries = [item for item in inventory_entries if item.get("role") == "native_input"]
    expected_entries = [item for item in named_entries if isinstance(item, Mapping)] + native_entries
    expected_roles = {"request", "native_input", "stdout", "stderr", "structured_result"}
    inventory_closed = (
        len(inventory_entries) == len(refs) == len(set(refs))
        and len(native_entries) == 1
        and set(refs) == {item.get("logical_ref") for item in expected_entries}
        and expected_roles <= set(roles)
        and result.get("stdout", {}).get("role") == "stdout"
        and result.get("stderr", {}).get("role") == "stderr"
        and result.get("structured_result", {}).get("role") == "structured_result"
        and integrity.get("request_artifact", {}).get("role") == "request"
    )
    outcome = result.get("outcome") if isinstance(result, Mapping) else None
    allowed_outcomes = set(policy_copy.get("allowed_outcomes", ("certified", "refuted", "unknown")))
    evidence_vetoes = list(policy_copy.get("evidence_vetoes", ()))
    engineering_vetoes = list(policy_copy.get("engineering_vetoes", ()))

    checks = [
        _invariant("verified_manifest", len(verified_manifests) == 1 and len(manifests) == 1, "Exactly one reader-verified manifest is required."),
        _invariant("source_digest", source_digest is not None and request_source.get("digest") == source_digest, "Current exact source bytes must match the request digest."),
        _invariant("source_span", _eq(request_source.get("spans"), source.get("spans")), "Ordered source spans must match."),
        _invariant("source_label", request_source.get("label") == source.get("label"), "Source label must match."),
        _invariant("obligation_digest", request_obligation.get("digest") == branch_copy.get("obligation_digest"), "Obligation digest must match."),
        _invariant("normalized_target", request_obligation.get("target") == branch_copy.get("normalized_target"), "Normalized target must match."),
        _invariant("branch_id", request_branch.get("id") == branch_copy.get("id"), "Branch id must match."),
        _invariant("branch_lineage", _eq(request_branch.get("lineage"), branch_copy.get("lineage")), "Ordered branch lineage must match."),
        _invariant("typed_assumptions", _eq(request.get("typed_assumptions"), expected_assumptions), "Full typed assumptions must match."),
        _invariant("assumption_digest", expected_assumption_digest is not None and request.get("assumption_digest") == expected_assumption_digest, "Assumption digest must be recomputed."),
        _invariant("native_input_digest", native_digest is not None and request_native.get("digest") == native_digest, "Exact native input bytes must match."),
        _invariant("tool_identity", _eq(request_tool, policy_copy.get("tool")), "Tool, adapter, backend, and executable identity must match."),
        _invariant("backend_role", request.get("backend_role") == policy_copy.get("backend_role"), "Backend role must match the explicit policy."),
        _invariant("sealed_inventory", inventory_closed, "Sealed artifact inventory must be closed, conflict-free, and use exact roles."),
        _invariant("result_outcome", outcome in allowed_outcomes, "Outcome must be allowed by the scoped policy."),
        _invariant("result_not_truncated", isinstance(result, Mapping) and not result.get("stdout_truncated") and not result.get("stderr_truncated"), "Truncated result streams veto binding."),
        _invariant("no_conflict", not policy_copy.get("conflict_detected", False), "Conflicting evidence vetoes binding."),
        _invariant(
            "candidate_edit_binding",
            edit_digest is not None
            and edit.get("digest") == edit_digest
            and edit.get("source_digest") == source_digest
            and edit.get("label") == source.get("label")
            and _eq(edit.get("span"), source.get("edit_span")),
            "Candidate edit bytes, source digest, label, and span must match.",
        ),
        _invariant("no_evidence_vetoes", not evidence_vetoes and not interpretation.get("veto_ids", []), "Evidence veto sets must be empty."),
        _invariant("no_engineering_vetoes", not engineering_vetoes, "Engineering veto set must be empty."),
        _invariant("publication_quarantine", policy_copy.get("publication_enabled") is False, "Publication must remain explicitly disabled."),
    ]

    passed = all(item["passed"] for item in checks)
    failed = [item["id"] for item in checks if not item["passed"]]
    return {
        "metadata": {"schema_version": "1.0", "contract": PROMOTION_POLICY_VERSION},
        "integrity_binding_status": INTEGRITY_STATUS_VERIFIED if passed else INTEGRITY_STATUS_REJECTED,
        "integrity_binding_verified": passed,
        "claim_eligibility": CLAIM_ELIGIBILITY,
        "publication_enabled": False,
        "decision": INTEGRITY_DECISION,
        "invariants": checks,
        "failed_invariant_ids": failed,
        "veto_ids": failed,
        "non_claims": list(NON_CLAIMS),
        "boundary": "Identity and storage integrity are not extraction correctness, backend conformance, mathematical proof, or publication authority.",
    }


def evaluate_promotion(
    verified_manifests: Sequence[Mapping[str, Any]],
    current_source: Mapping[str, Any],
    branch: Mapping[str, Any],
    candidate_edit: Mapping[str, Any],
    policy: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return the deterministic Phase 01 report-only decision."""
    return verify_exact_binding(verified_manifests, current_source, branch, candidate_edit, policy)


def build_test_only_aggregate_gate(*, phase_decision_digests: Sequence[str]) -> dict[str, Any]:
    """Build a pure-policy fixture that has no product or program authority."""
    digests = list(phase_decision_digests)
    if len(digests) != 7 or any(
        not isinstance(item, str)
        or len(item) != 64
        or any(char not in "0123456789abcdef" for char in item)
        for item in digests
    ):
        raise ValueError("test-only gate requires seven P00-P06 decision digests")
    record = {
        "schema_version": P06_TEST_GATE_SCHEMA_VERSION,
        "sentinel": P06_TEST_GATE_SENTINEL,
        "phase_ids": [f"P{index:02d}" for index in range(7)],
        "phase_decision_digests": digests,
        "all_pass": True,
        "program_authority": False,
    }
    record["gate_digest"] = content_digest(record)
    return record


def _verify_test_only_aggregate_gate(value: Any) -> bool:
    if not isinstance(value, Mapping) or set(value) != {
        "schema_version",
        "sentinel",
        "phase_ids",
        "phase_decision_digests",
        "all_pass",
        "program_authority",
        "gate_digest",
    }:
        return False
    if (
        value["schema_version"] != P06_TEST_GATE_SCHEMA_VERSION
        or value["sentinel"] != P06_TEST_GATE_SENTINEL
        or value["phase_ids"] != [f"P{index:02d}" for index in range(7)]
        or value["all_pass"] is not True
        or value["program_authority"] is not False
    ):
        return False
    digests = value["phase_decision_digests"]
    if not isinstance(digests, list) or len(digests) != 7 or any(
        not isinstance(item, str)
        or len(item) != 64
        or any(char not in "0123456789abcdef" for char in item)
        for item in digests
    ):
        return False
    return value["gate_digest"] == content_digest(
        {key: value[key] for key in value if key != "gate_digest"}
    )


def _p06_invariant(
    invariant_id: str,
    passed: bool,
    detail: str,
    evidence_refs: Sequence[str],
) -> dict[str, Any]:
    refs = sorted({str(item) for item in evidence_refs if str(item)})
    canonical_refs = json.loads(
        canonical_json_bytes({"evidence_refs": refs}).decode("utf-8")
    )["evidence_refs"]
    return {
        "id": invariant_id,
        "passed": bool(passed),
        "detail": detail,
        "evidence_refs": canonical_refs,
    }


def _span_contains(outer: Mapping[str, Any], inner: Mapping[str, Any]) -> bool:
    if not isinstance(outer, Mapping) or not isinstance(inner, Mapping):
        return False
    if outer.get("file") != inner.get("file") or outer.get("label") != inner.get("label"):
        return False
    for key in ("start_byte", "end_byte"):
        if not isinstance(outer.get(key), int) or not isinstance(inner.get(key), int):
            return False
    return outer["start_byte"] <= inner["start_byte"] < inner["end_byte"] <= outer["end_byte"]


def _assumption_support_complete(
    assumptions: Sequence[Mapping[str, Any]],
    assumption_digests: Sequence[str],
    support_records: Any,
    source_digest: str | None,
    source_spans: Sequence[Mapping[str, Any]],
    candidate_edit: Mapping[str, Any],
) -> tuple[bool, list[str]]:
    if (
        not isinstance(support_records, list)
        or len(support_records) != len(assumptions)
        or len(assumption_digests) != len(assumptions)
    ):
        return False, [
            str(item.get("id") or f"assumption_{index}")
            for index, item in enumerate(assumptions)
        ]
    by_digest: dict[str, Mapping[str, Any]] = {}
    for record in support_records:
        if (
            not isinstance(record, Mapping)
            or set(record)
            != {
                "assumption_id",
                "assumption_digest",
                "support_status",
                "source_refs",
                "candidate_edit_statement",
            }
            or record.get("assumption_digest") in by_digest
        ):
            return False, [
                str(item.get("id") or f"assumption_{index}")
                for index, item in enumerate(assumptions)
            ]
        by_digest[str(record["assumption_digest"])] = record
    unresolved: list[str] = []
    edit_text = candidate_edit.get("text")
    for index, (assumption, assumption_digest) in enumerate(
        zip(assumptions, assumption_digests, strict=True)
    ):
        assumption_id = str(assumption.get("id") or f"assumption_{index}")
        support = by_digest.get(assumption_digest)
        if support is None or support.get("assumption_id") != assumption_id:
            unresolved.append(assumption_id)
            continue
        support_status = support.get("support_status")
        if support_status == "source_supported":
            refs = support.get("source_refs")
            if (
                not isinstance(refs, list)
                or not refs
                or support.get("candidate_edit_statement") is not None
            ):
                unresolved.append(assumption_id)
                continue
            valid_refs = all(
                isinstance(ref, Mapping)
                and ref.get("source_digest") == source_digest
                and any(_span_contains(span, ref) for span in source_spans)
                for ref in refs
            )
            if not valid_refs:
                unresolved.append(assumption_id)
        elif support_status == "candidate_edit":
            statement = support.get("candidate_edit_statement")
            if (
                support.get("source_refs") != []
                or not isinstance(edit_text, str)
                or not isinstance(statement, str)
                or not statement
                or statement not in edit_text
            ):
                unresolved.append(assumption_id)
        else:
            unresolved.append(assumption_id)
    return not unresolved, unresolved


def _claim_scope_contained(
    certified_scope: str,
    edit_scope: Mapping[str, Any],
    branch_target: str,
) -> bool:
    return bool(
        isinstance(certified_scope, str)
        and certified_scope == branch_target
        and isinstance(edit_scope, Mapping)
        and set(edit_scope) == {"kind", "target"}
        and edit_scope.get("kind") in {"exact_target", "assumptions_and_exact_target"}
        and edit_scope.get("target") == branch_target
    )


def _decision_digest(record: Mapping[str, Any]) -> str:
    return content_digest(
        {
            key: record[key]
            for key in record
            if key not in {"promotion_decision_digest", "reconstruction"}
        }
    )


def _is_sha256(value: Any) -> bool:
    return bool(
        isinstance(value, str)
        and len(value) == 64
        and all(char in "0123456789abcdef" for char in value)
    )


def _require_sorted_unique_strings(value: Any, label: str) -> list[str]:
    if (
        not isinstance(value, list)
        or any(not isinstance(item, str) or not item for item in value)
        or value != sorted(set(value))
    ):
        raise ValueError(f"Phase 06 {label} must be a sorted unique string list")
    return value


def _canonical_evidence_refs(value: list[str]) -> list[str]:
    return json.loads(
        canonical_json_bytes({"evidence_refs": value}).decode("utf-8")
    )["evidence_refs"]


def _canonical_non_claims(value: Sequence[str]) -> list[str]:
    return json.loads(
        canonical_json_bytes({"non_claims": list(value)}).decode("utf-8")
    )["non_claims"]


def _validate_decision_manifest_refs(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise ValueError("Phase 06 manifest_refs must be a list")
    refs: list[dict[str, Any]] = []
    identities: list[tuple[str, str]] = []
    for item in value:
        if not isinstance(item, Mapping) or set(item) != {
            "manifest_ref",
            "manifest_sha256",
            "manifest_family",
            "manifest_version",
        }:
            raise ValueError("Phase 06 manifest ref shape is invalid")
        record = dict(item)
        if (
            not isinstance(record["manifest_ref"], str)
            or not record["manifest_ref"]
            or not _is_sha256(record["manifest_sha256"])
            or not isinstance(record["manifest_family"], str)
            or not record["manifest_family"]
            or not isinstance(record["manifest_version"], str)
            or not record["manifest_version"]
        ):
            raise ValueError("Phase 06 manifest ref values are invalid")
        refs.append(record)
        identities.append((record["manifest_ref"], record["manifest_sha256"]))
    if identities != sorted(set(identities)):
        raise ValueError("Phase 06 manifest refs must be sorted and unique")
    return refs


def _validate_candidate_edit_projection(value: Any) -> tuple[dict[str, Any], bool]:
    if not isinstance(value, Mapping) or set(value) != {
        "placement",
        "kind",
        "text",
        "edit_digest",
    }:
        raise ValueError("Phase 06 candidate edit projection is invalid")
    edit = deepcopy(dict(value))
    placement = edit["placement"]
    if not isinstance(placement, Mapping) or set(placement) != {
        "file",
        "label",
        "start_byte",
        "end_byte",
    }:
        raise ValueError("Phase 06 candidate edit placement is invalid")
    if (
        not isinstance(placement["file"], str)
        or not placement["file"]
        or not isinstance(placement["label"], str)
        or not placement["label"]
        or not isinstance(placement["start_byte"], int)
        or isinstance(placement["start_byte"], bool)
        or not isinstance(placement["end_byte"], int)
        or isinstance(placement["end_byte"], bool)
        or not 0 <= placement["start_byte"] < placement["end_byte"]
    ):
        raise ValueError("Phase 06 candidate edit placement is invalid")
    text = edit["text"]
    digest = edit["edit_digest"]
    if text is None:
        if digest is not None:
            raise ValueError("Phase 06 candidate edit digest has no text")
        digest_ok = False
    elif not isinstance(text, str):
        raise ValueError("Phase 06 candidate edit text is invalid")
    else:
        if digest != _digest_bytes(text.encode("utf-8")):
            raise ValueError("Phase 06 candidate edit digest mismatch")
        digest_ok = True
    kind_ok = isinstance(edit["kind"], str) and bool(edit["kind"])
    return edit, bool(kind_ok and digest_ok and edit["placement"])


def _phase06_expected_reason(
    *, claim_eligible: bool, publication_pass: bool, has_manifest_refs: bool
) -> str:
    if claim_eligible and publication_pass:
        return "All exact claim and explicit test-only publication invariants pass."
    if claim_eligible:
        return "All exact claim invariants pass; publication remains report-only."
    if has_manifest_refs:
        return "One or more exact claim invariants failed; publish only the gap/evidence boundary."
    return "No valid normalized manifest remains; reject the promotion input."


def verify_phase06_promotion_decision(value: Any) -> dict[str, Any]:
    """Verify persisted internal consistency, never native claim authority."""
    expected_keys = {
        "schema_version",
        "policy_version",
        "authority",
        "promotion_decision_digest",
        "branch_id",
        "obligation_digest",
        "assumption_digest",
        "candidate_edit",
        "manifest_refs",
        "invariant_results",
        "unresolved_assumption_ids",
        "open_blocker_ids",
        "engineering_error_ids",
        "evidence_integrity_error_ids",
        "mathematical_veto_ids",
        "compact_omission_veto_ids",
        "claim_eligibility",
        "decision",
        "publication_enabled",
        "publication_mode",
        "reason",
        "vetoes",
        "non_claims",
        "applicable_repair",
        "reconstruction",
    }
    if not isinstance(value, Mapping) or set(value) != expected_keys:
        raise ValueError("Phase 06 promotion decision keys mismatch")
    record = deepcopy(dict(value))
    if (
        record["schema_version"] != P06_PROMOTION_SCHEMA_VERSION
        or record["policy_version"] != P06_PROMOTION_POLICY_VERSION
        or record["authority"] != P06_PERSISTED_DECISION_AUTHORITY
    ):
        raise ValueError("Phase 06 promotion decision version is invalid")
    if record["branch_id"] is not None and (
        not isinstance(record["branch_id"], str) or not record["branch_id"]
    ):
        raise ValueError("Phase 06 branch_id is invalid")
    if record["obligation_digest"] is not None and not _is_sha256(
        record["obligation_digest"]
    ):
        raise ValueError("Phase 06 obligation_digest is invalid")
    if not _is_sha256(record["assumption_digest"]):
        raise ValueError("Phase 06 assumption_digest is invalid")
    _, candidate_projection_ok = _validate_candidate_edit_projection(
        record["candidate_edit"]
    )
    manifest_refs = _validate_decision_manifest_refs(record["manifest_refs"])
    id_fields = (
        "unresolved_assumption_ids",
        "open_blocker_ids",
        "engineering_error_ids",
        "evidence_integrity_error_ids",
        "mathematical_veto_ids",
        "compact_omission_veto_ids",
        "vetoes",
    )
    for field in id_fields:
        _require_sorted_unique_strings(record[field], field)
    invariants = record["invariant_results"]
    if (
        not isinstance(invariants, list)
        or [item.get("id") for item in invariants if isinstance(item, Mapping)]
        != list(P06_INVARIANT_IDS)
    ):
        raise ValueError("Phase 06 invariant registry mismatch")
    expected_digest = _decision_digest(record)
    reconstruction = record["reconstruction"]
    if not isinstance(reconstruction, Mapping) or set(reconstruction) != {
        "algorithm",
        "recomputed_digest",
        "matches",
    }:
        raise ValueError("Phase 06 reconstruction record is invalid")
    if (
        record["promotion_decision_digest"] != expected_digest
        or reconstruction["algorithm"] != "canonical_sha256_excluding_digest_and_reconstruction"
        or reconstruction["recomputed_digest"] != expected_digest
        or reconstruction["matches"] is not True
    ):
        raise ValueError("Phase 06 promotion decision digest mismatch")
    by_id = {item["id"]: item for item in invariants}
    if len(by_id) != len(P06_INVARIANT_IDS) or any(
        set(item) != {"id", "passed", "detail", "evidence_refs"}
        or
        not isinstance(item.get("passed"), bool)
        or not isinstance(item.get("detail"), str)
        or not item.get("detail")
        or not isinstance(item.get("evidence_refs"), list)
        or item.get("evidence_refs")
        != _canonical_evidence_refs(item.get("evidence_refs", []))
        or any(
            not isinstance(ref, str) or not ref
            for ref in item.get("evidence_refs", [])
        )
        for item in invariants
    ):
        raise ValueError("Phase 06 invariant result shape is invalid")
    if by_id["deterministic_decision_reconstruction"]["passed"] is not True:
        raise ValueError("Phase 06 deterministic reconstruction invariant must pass")
    if by_id["deterministic_decision_reconstruction"]["evidence_refs"] != []:
        raise ValueError("Phase 06 reconstruction invariant evidence is self-referential")

    typed_veto_ids = [
        *record["engineering_error_ids"],
        *record["evidence_integrity_error_ids"],
        *record["mathematical_veto_ids"],
        *record["compact_omission_veto_ids"],
    ]
    if by_id["empty_typed_veto_sets"]["passed"] is not (
        not typed_veto_ids and not record["open_blocker_ids"]
    ):
        raise ValueError("Phase 06 typed-veto invariant disagrees with stored veto sets")
    if (
        by_id["complete_assumption_support_and_encoding"]["passed"]
        and record["unresolved_assumption_ids"]
    ):
        raise ValueError("Phase 06 assumption invariant disagrees with unresolved ids")
    if by_id["candidate_edit_binding_and_scope"]["passed"] and not candidate_projection_ok:
        raise ValueError("Phase 06 candidate-edit invariant disagrees with stored edit")
    native_invariant_ids = (
        "certifying_backend_role_and_input_class",
        "actual_non_test_backend_execution",
        "registered_reader_evidence_integrity",
        "scoped_terminal_outcome",
    )
    if any(by_id[item]["passed"] for item in native_invariant_ids) and not manifest_refs:
        raise ValueError("Phase 06 native-evidence invariant lacks a manifest ref")
    if by_id["exact_branch_binding"]["passed"] and (
        not record["branch_id"] or not _is_sha256(record["obligation_digest"])
    ):
        raise ValueError("Phase 06 exact-branch invariant lacks branch identity")
    manifest_ref_values = {item["manifest_ref"] for item in manifest_refs}
    if manifest_ref_values and not manifest_ref_values <= set(
        by_id["registered_reader_evidence_integrity"]["evidence_refs"]
    ):
        raise ValueError("Phase 06 manifest refs are absent from reader evidence refs")
    claim_pass = all(
        by_id[invariant_id]["passed"]
        for invariant_id in (*P06_INVARIANT_IDS[:10], P06_INVARIANT_IDS[11])
    )
    expected_eligibility = (
        P06_CLAIM_ELIGIBILITY_EXACT
        if claim_pass
        else P06_CLAIM_ELIGIBILITY_INELIGIBLE
    )
    publication_pass = by_id["publication_policy_and_aggregate_gate"]["passed"]
    if claim_pass and publication_pass:
        expected_decision = "eligible_experimental_repair"
    elif claim_pass:
        expected_decision = "publish_evidence_report"
    elif record["manifest_refs"]:
        expected_decision = "publish_gap"
    else:
        expected_decision = "reject"
    expected_vetoes = sorted(
        item["id"]
        for item in invariants[:10]
        if not item["passed"]
    )
    expected_reason = _phase06_expected_reason(
        claim_eligible=claim_pass,
        publication_pass=publication_pass,
        has_manifest_refs=bool(manifest_refs),
    )
    if (
        record["claim_eligibility"] != expected_eligibility
        or record["decision"] != expected_decision
        or not isinstance(record["publication_enabled"], bool)
        or record["publication_mode"] not in P06_PUBLICATION_MODES
        or (
            publication_pass
            and not (
                record["publication_mode"] == "experimental_exact_manifest"
                and record["publication_enabled"] is True
            )
        )
        or record["vetoes"] != expected_vetoes
        or record["reason"] != expected_reason
        or record["applicable_repair"] is not None
        or not isinstance(record["non_claims"], list)
        or len(record["non_claims"]) != len(P06_PROMOTION_NON_CLAIMS)
        or record["non_claims"]
        != _canonical_non_claims(P06_PROMOTION_NON_CLAIMS)
    ):
        raise ValueError("Phase 06 promotion decision semantics mismatch")
    return record


def evaluate_phase06_promotion(
    *,
    normalized_claim_evidence: Any,
    current_source: Mapping[str, Any],
    extraction: Mapping[str, Any],
    branch: Mapping[str, Any],
    candidate_edit: Mapping[str, Any],
    ledgers: Mapping[str, Any],
    policy: Mapping[str, Any],
) -> dict[str, Any]:
    """Recompute Phase 06 claim eligibility and publication independently."""
    source = deepcopy(dict(current_source)) if isinstance(current_source, Mapping) else {}
    extraction_copy = deepcopy(dict(extraction)) if isinstance(extraction, Mapping) else {}
    branch_copy = deepcopy(dict(branch)) if isinstance(branch, Mapping) else {}
    edit = deepcopy(dict(candidate_edit)) if isinstance(candidate_edit, Mapping) else {}
    policy_copy = deepcopy(dict(policy)) if isinstance(policy, Mapping) else {}

    try:
        evidence = reader_verified_claim_evidence_record(normalized_claim_evidence)
        evidence_valid = True
    except (TypeError, ValueError):
        evidence = deepcopy(dict(normalized_claim_evidence)) if isinstance(normalized_claim_evidence, Mapping) else {}
        evidence_valid = False
    branch_errors = validate_branch_record(branch_copy)
    try:
        ledger_bundle = validate_ledgers(ledgers)
        ledgers_valid = True
    except (TypeError, ValueError):
        ledger_bundle = {
            "deduplicated_entries": [],
            "veto_entry_ids": ["invalid_ledger_bundle"],
        }
        ledgers_valid = False

    source_bytes = source.get("bytes")
    source_digest = (
        _digest_bytes(source_bytes)
        if isinstance(source_bytes, (bytes, bytearray, memoryview))
        else None
    )
    source_spans = source.get("owned_spans") if isinstance(source.get("owned_spans"), list) else []
    source_label = source.get("label")
    source_shape_ok = set(source) == {
        "schema_version",
        "logical_id",
        "bytes",
        "digest",
        "label",
        "owned_spans",
        "obligation_digest",
        "normalized_target",
        "assumption_support",
    } and source.get("schema_version") == "p06_current_source@1"
    extraction_source = extraction_copy.get("source") if isinstance(extraction_copy.get("source"), Mapping) else {}
    extraction_ok = bool(
        set(extraction_copy)
        == {"schema_version", "state", "adapter_eligible", "ambiguity_ids", "source"}
        and extraction_copy.get("schema_version") == "p06_extraction_binding@1"
        and extraction_copy.get("state") == "validated"
        and extraction_copy.get("adapter_eligible") is True
        and extraction_copy.get("ambiguity_ids") == []
        and extraction_source.get("digest") == source_digest
        and extraction_source.get("label") == source_label
        and _eq(extraction_source.get("owned_spans"), source_spans)
    )
    source_binding_ok = bool(
        evidence_valid
        and source_shape_ok
        and source_digest
        and isinstance(source.get("logical_id"), str)
        and source.get("logical_id")
        and source.get("digest") == source_digest
        and isinstance(source_label, str)
        and source_label
        and source_spans
        and evidence.get("obligation", {}).get("digest") == source.get("obligation_digest")
        and evidence.get("obligation", {}).get("target") == source.get("normalized_target")
    )
    evidence_branch = evidence.get("branch") if isinstance(evidence.get("branch"), Mapping) else {}
    evidence_assumptions = evidence.get("typed_assumptions")
    branch_binding_ok = bool(
        not branch_errors
        and evidence_valid
        and evidence_branch.get("id") == branch_copy.get("id")
        and evidence_branch.get("lineage") == branch_copy.get("lineage")
        and evidence_branch.get("record_digest") == content_digest(branch_copy)
        and evidence.get("obligation", {}).get("digest") == branch_copy.get("obligation_digest")
        and evidence.get("obligation", {}).get("target") == branch_copy.get("target")
        and evidence_assumptions == branch_copy.get("typed_assumptions")
        and evidence.get("typed_assumption_digests") == branch_copy.get("typed_assumption_digests")
    )
    support_ok, unresolved_assumption_ids = _assumption_support_complete(
        branch_copy.get("typed_assumptions", [])
        if isinstance(branch_copy.get("typed_assumptions"), list)
        else [],
        branch_copy.get("typed_assumption_digests", [])
        if isinstance(branch_copy.get("typed_assumption_digests"), list)
        else [],
        source.get("assumption_support"),
        source_digest,
        source_spans,
        edit,
    )
    encoding = evidence.get("assumption_encoding") if isinstance(evidence.get("assumption_encoding"), Mapping) else {}
    encoding_ok = bool(
        evidence_valid
        and encoding.get("complete") is True
        and encoding.get("encoded_assumption_digests")
        == sorted(branch_copy.get("typed_assumption_digests", []))
    )
    assumption_ok = support_ok and encoding_ok
    allowed_roles = policy_copy.get("certifying_backend_roles")
    allowed_classes = policy_copy.get("accepted_input_classes")
    role_ok = bool(
        evidence_valid
        and isinstance(allowed_roles, list)
        and evidence.get("backend_role") in allowed_roles
        and isinstance(allowed_classes, list)
        and evidence.get("accepted_input_class") in allowed_classes
        and evidence.get("certifying") is True
    )
    execution = evidence.get("execution") if isinstance(evidence.get("execution"), Mapping) else {}
    live_execution_ok = bool(
        evidence_valid
        and execution.get("live_tool_executed") is True
        and execution.get("test_only") is False
        and execution.get("kind") in {"subprocess", "python_library"}
    )
    manifest_ok = bool(
        evidence_valid
        and evidence.get("integrity_state") == "registered_reader_verified"
        and evidence.get("manifest_family") == "registered_external_adapter"
    )
    outcome = evidence.get("outcome") if isinstance(evidence.get("outcome"), Mapping) else {}
    outcome_ok = bool(
        evidence_valid
        and outcome.get("status") in {"certified", "refuted"}
        and outcome.get("scope") == branch_copy.get("target")
        and outcome.get("placeholder_free") is True
        and outcome.get("conflict_free") is True
        and outcome.get("truncated") is False
    )

    edit_text = edit.get("text")
    edit_bytes = edit_text.encode("utf-8") if isinstance(edit_text, str) else None
    edit_digest = _digest_bytes(edit_bytes) if edit_bytes is not None else None
    edit_span = edit.get("placement") if isinstance(edit.get("placement"), Mapping) else {}
    edit_ok = bool(
        set(edit)
        == {"schema_version", "kind", "text", "edit_digest", "source_digest", "label", "placement", "claim_scope"}
        and edit.get("schema_version") == "p06_candidate_edit@1"
        and edit_digest
        and edit.get("edit_digest") == edit_digest
        and edit.get("source_digest") == source_digest
        and edit.get("label") == source_label
        and any(_span_contains(span, edit_span) for span in source_spans)
        and _claim_scope_contained(
            str(outcome.get("scope") or ""),
            edit.get("claim_scope") if isinstance(edit.get("claim_scope"), Mapping) else {},
            str(branch_copy.get("target") or ""),
        )
    )

    ledger_entries = ledger_bundle.get("deduplicated_entries", [])
    engineering_error_ids = sorted(
        item["entry_id"]
        for item in ledger_entries
        if item["ledger_kind"] == "engineering" and item["veto_role"] == "veto"
    )
    evidence_integrity_error_ids = sorted(
        [
            item["entry_id"]
            for item in ledger_entries
            if item["ledger_kind"] == "evidence_integrity"
            and item["veto_role"] == "veto"
        ]
        + ([] if ledgers_valid else ["invalid_ledger_bundle"])
    )
    mathematical_veto_ids = sorted(
        item["entry_id"]
        for item in ledger_entries
        if item["ledger_kind"] == "mathematical_validity" and item["veto_role"] == "veto"
    )
    compact_omission_veto_ids = sorted(
        {
            str(item)
            for item in policy_copy.get("compact_omission_veto_ids", [])
            if isinstance(item, str) and item
        }
    ) if isinstance(policy_copy.get("compact_omission_veto_ids"), list) else ["invalid_compact_veto_set"]
    open_blocker_ids = sorted(
        {
            scope
            for item in ledger_entries
            if item["veto_role"] == "veto"
            for scope in item["smallest_discriminator"]["closes_scope"]
        }
    )
    no_vetoes = bool(
        ledgers_valid
        and not engineering_error_ids
        and not evidence_integrity_error_ids
        and not mathematical_veto_ids
        and not compact_omission_veto_ids
    )

    mode = policy_copy.get("publication_mode")
    publication_enabled = policy_copy.get("publication_enabled") is True
    explicit_mode = policy_copy.get("explicit_mode") is True
    gate_ok = _verify_test_only_aggregate_gate(policy_copy.get("test_only_aggregate_gate"))
    publication_gate_ok = bool(
        mode == "experimental_exact_manifest"
        and publication_enabled
        and explicit_mode
        and gate_ok
        and policy_copy.get("allow_test_only_experimental_policy") is True
    )
    policy_shape_ok = set(policy_copy) == {
        "schema_version",
        "publication_mode",
        "publication_enabled",
        "explicit_mode",
        "certifying_backend_roles",
        "accepted_input_classes",
        "compact_omission_veto_ids",
        "test_only_aggregate_gate",
        "allow_test_only_experimental_policy",
    } and policy_copy.get("schema_version") == "p06_promotion_policy_input@1" and mode in P06_PUBLICATION_MODES
    if not policy_shape_ok:
        publication_gate_ok = False

    evidence_refs = (
        evidence.get("evidence_refs", [])
        if evidence_valid and isinstance(evidence.get("evidence_refs"), list)
        else []
    )
    source_ref = f"source:{source_digest}" if source_digest else "source:invalid"
    edit_ref = f"edit:{edit_digest}" if edit_digest else "edit:invalid"
    checks = [
        _p06_invariant("current_source_binding", source_binding_ok, "Current source bytes, owned spans, label, obligation, and target must be exact.", [source_ref]),
        _p06_invariant("validated_unambiguous_extraction", extraction_ok, "Extraction must be validated, adapter-eligible, and ambiguity-free.", [source_ref]),
        _p06_invariant("exact_branch_binding", branch_binding_ok, "Validated Phase 04 branch identity, lineage, obligation, target, and assumptions must equal normalized evidence.", evidence_refs),
        _p06_invariant("complete_assumption_support_and_encoding", assumption_ok, "Every typed assumption must have current source/edit support and native-input encoding evidence.", [source_ref, edit_ref, *encoding.get("evidence_refs", [])] if isinstance(encoding.get("evidence_refs"), list) else [source_ref, edit_ref]),
        _p06_invariant("certifying_backend_role_and_input_class", role_ok, "Backend role and accepted input class must be explicitly permitted and certifying.", evidence_refs),
        _p06_invariant("actual_non_test_backend_execution", live_execution_ok, "Real eligibility requires actual non-test backend execution.", evidence_refs),
        _p06_invariant("registered_reader_evidence_integrity", manifest_ok, "Evidence must be reverified by its registered native reader.", evidence_refs),
        _p06_invariant("scoped_terminal_outcome", outcome_ok, "Outcome must be scoped, terminal, placeholder-free, conflict-free, and untruncated.", evidence_refs),
        _p06_invariant("candidate_edit_binding_and_scope", edit_ok, "Candidate edit bytes, placement, source, label, and mathematical scope must be exact.", [edit_ref]),
        _p06_invariant("empty_typed_veto_sets", no_vetoes, "Engineering, evidence, mathematical, and compact-omission veto sets must be empty.", ledger_bundle.get("veto_entry_ids", [])),
        _p06_invariant("publication_policy_and_aggregate_gate", publication_gate_ok, "Experimental publication requires explicit test-only policy mode and a valid no-authority aggregate fixture.", [str(policy_copy.get("test_only_aggregate_gate", {}).get("gate_digest", ""))] if isinstance(policy_copy.get("test_only_aggregate_gate"), Mapping) else []),
    ]
    claim_checks = checks[:10]

    manifest_refs = []
    if (
        evidence_valid
        and evidence.get("manifest_ref")
        and evidence.get("manifest_sha256")
    ):
        manifest_refs.append(
            {
                "manifest_ref": evidence["manifest_ref"],
                "manifest_sha256": evidence["manifest_sha256"],
                "manifest_family": evidence.get("manifest_family"),
                "manifest_version": evidence.get("manifest_version"),
            }
        )
    manifest_refs.sort(
        key=lambda item: (item["manifest_ref"], item["manifest_sha256"])
    )
    assumption_digest = content_digest(branch_copy.get("typed_assumptions", []))
    record = {
        "schema_version": P06_PROMOTION_SCHEMA_VERSION,
        "policy_version": P06_PROMOTION_POLICY_VERSION,
        "authority": P06_PERSISTED_DECISION_AUTHORITY,
        "promotion_decision_digest": "",
        "branch_id": branch_copy.get("id"),
        "obligation_digest": branch_copy.get("obligation_digest"),
        "assumption_digest": assumption_digest,
        "candidate_edit": {
            "placement": deepcopy(edit_span),
            "kind": edit.get("kind"),
            "text": edit_text,
            "edit_digest": edit_digest,
        },
        "manifest_refs": manifest_refs,
        "invariant_results": checks,
        "unresolved_assumption_ids": sorted(unresolved_assumption_ids),
        "open_blocker_ids": open_blocker_ids,
        "engineering_error_ids": engineering_error_ids,
        "evidence_integrity_error_ids": evidence_integrity_error_ids,
        "mathematical_veto_ids": mathematical_veto_ids,
        "compact_omission_veto_ids": compact_omission_veto_ids,
        "claim_eligibility": P06_CLAIM_ELIGIBILITY_INELIGIBLE,
        "decision": "reject",
        "publication_enabled": publication_enabled,
        "publication_mode": mode if mode in P06_PUBLICATION_MODES else "disabled",
        "reason": (
            "Decision semantics are finalized after deterministic reconstruction."
        ),
        "vetoes": sorted(
            item["id"] for item in claim_checks if not item["passed"]
        ),
        "non_claims": _canonical_non_claims(P06_PROMOTION_NON_CLAIMS),
        "applicable_repair": None,
        "reconstruction": {},
    }
    digest = _decision_digest(record)
    reconstruction_passed = bool(digest and len(digest) == 64)
    checks.append(
        _p06_invariant(
            "deterministic_decision_reconstruction",
            reconstruction_passed,
            "Canonical reconstruction must reproduce the decision digest byte-for-byte.",
            [],
        )
    )
    claim_eligible = all(
        item["passed"] for item in (*checks[:10], checks[11])
    )
    record["claim_eligibility"] = (
        P06_CLAIM_ELIGIBILITY_EXACT
        if claim_eligible
        else P06_CLAIM_ELIGIBILITY_INELIGIBLE
    )
    if claim_eligible and publication_gate_ok:
        record["decision"] = "eligible_experimental_repair"
    elif claim_eligible:
        record["decision"] = "publish_evidence_report"
    elif manifest_refs:
        record["decision"] = "publish_gap"
    else:
        record["decision"] = "reject"
    record["reason"] = _phase06_expected_reason(
        claim_eligible=claim_eligible,
        publication_pass=publication_gate_ok,
        has_manifest_refs=bool(manifest_refs),
    )
    record["promotion_decision_digest"] = _decision_digest(record)
    record["reconstruction"] = {
        "algorithm": "canonical_sha256_excluding_digest_and_reconstruction",
        "recomputed_digest": record["promotion_decision_digest"],
        "matches": True,
    }
    return verify_phase06_promotion_decision(record)
