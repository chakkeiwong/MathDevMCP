from __future__ import annotations

from copy import deepcopy
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

import mathdevmcp.mcp_facade as mcp_facade
import mathdevmcp.mcp_server as mcp_server
from mathdevmcp.document_derivation_response import (
    DOCUMENT_DERIVATION_ARTIFACT_SCHEMA,
    DOCUMENT_DERIVATION_RESPONSE_CONTRACT,
    DOCUMENT_DERIVATION_RESPONSE_SCHEMA,
    audit_result_id,
    build_document_derivation_audit_request,
    canonical_document_derivation_response_bytes,
    compile_document_derivation_response,
    decode_document_derivation_cursor,
    document_derivation_public_surface_sizes,
    load_document_derivation_continuation,
    resolve_document_derivation_records,
    validate_document_derivation_response,
)
from mathdevmcp.failure_ledgers import (
    build_status_entry,
    rank_repair_branches_partial_order,
    select_next_discriminating_action,
    validate_discriminating_action,
)
from mathdevmcp.mcp_facade import call_mcp_tool


PRIVATE_ROOT = "/home/private-user/projects/private-paper"


def _refresh_canonical_byte_count(response: dict) -> None:
    response["canonical_byte_count"] = 0
    while True:
        measured = len(
            json.dumps(
                response,
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
                sort_keys=True,
            ).encode("utf-8")
        )
        if response["canonical_byte_count"] == measured:
            return
        response["canonical_byte_count"] = measured


def _forge_checksummed_token(token: str, field: str) -> str:
    raw = bytearray(base64.urlsafe_b64decode(token + "=" * (-len(token) % 4)))
    digest_offsets = {
        "audit_result_id": 12,
        "audit_request_id": 44,
        "artifact_sha256": 76,
        "filter_id": 108,
        "page_boundary_digest": 140,
        "resolver_scope_digest": 172,
    }
    if field == "requested_target_limit":
        raw[5] = 2 if raw[5] != 2 else 3
    elif field == "next_offset":
        next_offset = int.from_bytes(raw[10:12], "big")
        raw[10:12] = (next_offset + 1).to_bytes(2, "big")
    else:
        raw[digest_offsets[field]] ^= 1
    raw[-32:] = hashlib.sha256(raw[:-32]).digest()
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def _raw_audit(*, target_count: int = 3) -> dict:
    shared_blocker = {
        "id": "blocker-shared",
        "kind": "missing_assumption",
        "problem": f"Missing assumption; inspect {PRIVATE_ROOT}/notes.txt",
        "why": "The denominator may vanish.",
        "required_next_evidence": "Produce a source-bound nonzero-domain record.",
        "evidence_refs": ["evidence://shared"],
        "source_refs": [
            {
                "file": f"{PRIVATE_ROOT}/paper.tex",
                "label": "eq:shared",
                "line_start": 10,
                "line_end": 12,
                "evidence_ref": "source://shared",
                "snippet": "x / x = 1",
            }
        ],
    }
    targets = []
    for index in range(target_count):
        target_id = f"target-{index}"
        assumption_id = f"assumption-{index}"
        action_id = f"action-{index}"
        target = {
            "id": target_id,
            "row_id": f"row-{index}",
            "row_index": index,
            "label": f"eq:{index}",
            "location": f"paper.tex > eq:{index} > line {10 + index}",
            "status": "blocked",
            "publication_mode": "disabled",
            "promotion": {"can_promote": False, "reason": "publication disabled"},
            "failure_classifications": ["mathematical_gap"],
            "veto_ids": [f"target-veto-{index}"],
            "semantic_work_packet": {
                "id": f"packet-{index}",
                "label_scoped_obligation": {
                    "obligation_id": f"obl_{index:064x}",
                    "obligation_digest": f"{index:064x}",
                },
                "typed_repair_obligation": {
                    "id": f"typed-obligation-{index}",
                    "math_obligation": {"id": f"math-obligation-{index}"},
                },
                "source_span": {
                    "file": "paper.tex",
                    "start_byte": index * 10,
                    "end_byte": index * 10 + 9,
                },
                "target": f"x_{index} = x_{index}",
            },
            "tree": {
                "assumptions": [
                    {
                        "id": assumption_id,
                        "status": "missing" if index % 2 == 0 else "unresolved",
                        "text": f"x_{index} != 0",
                        "role": "domain_condition",
                        "evidence_refs": [f"evidence://assumption/{index}"],
                        "source_refs": [
                            {
                                "file": "paper.tex",
                                "label": f"eq:{index}",
                                "line_start": 10 + index,
                                "line_end": 10 + index,
                                "evidence_ref": f"source://assumption/{index}",
                                "snippet": f"x_{index}",
                            }
                        ],
                    }
                ],
                "blockers": [
                    {**deepcopy(shared_blocker), "id": f"blocker-shared-{index}"},
                    {
                        "id": f"blocker-local-{index}",
                        "kind": "backend_input_missing",
                        "problem": "No exact backend input exists.",
                        "why": "The target has not been formalized.",
                        "required_next_evidence": "Generate an assumption-bound formalization.",
                        "evidence_refs": [f"evidence://blocker/{index}"],
                    },
                ],
                "branch_ranking": {
                    "selected_action": _closed_phase06_action(index)
                },
            },
        }
        targets.append(target)
    return {
        "metadata": {"schema_version": "1.0", "contract": "document_derivation_tree_audit"},
        "status": "diagnostic_complete",
        "tex_path": f"{PRIVATE_ROOT}/paper.tex",
        "backend_env": "mathdevmcp-backends",
        "search_mode": "agent_guided",
        "grounding_policy": "strict",
        "publication_mode": "disabled",
        "publication_veto_ids": ["document_repair_publication_disabled"],
        "veto_ids": ["document_repair_publication_disabled"],
        "failure_classifications": ["mathematical_gap"],
        "promotion": {"can_promote": False, "reason": "publication disabled"},
        "execution": {
            "mode": "serial",
            "target_count": target_count,
            "failure_count": 0,
            "private_detail": f"runner cache at {PRIVATE_ROOT}/cache",
        },
        "coverage": {
            "status": "partial_coverage",
            "semantic_packet_count": target_count,
            "selected_rows": target_count,
            "promoted_count": 0,
        },
        "backend_provenance": {
            "doctor": {
                "python": {
                    "executable": "/usr/bin/python3",
                    "prefix": "/usr",
                    "path_head": ["/usr/bin", f"{PRIVATE_ROOT}/bin"],
                },
                "capabilities": {
                    "sympy": {
                        "available": True,
                        "version": "1.14.0",
                        "path": f"{PRIVATE_ROOT}/env/sympy",
                    }
                },
            }
        },
        "tool_uses": [
            {
                "tool": "locate_equations_in_file",
                "arguments": {"tex_path": f"{PRIVATE_ROOT}/paper.tex", "root": PRIVATE_ROOT},
                "status": "completed",
            }
        ],
        "targets": targets,
        "context_targets": [],
        "non_claims": [
            {"code": "not_document_proof", "text": "This diagnostic is not a document proof."},
            {"code": "publication_disabled", "text": "No returned item is an applicable edit."},
        ],
        "markdown": f"# Private report\n\nLoaded from {PRIVATE_ROOT}/paper.tex",
        "output_md": f"{PRIVATE_ROOT}/out/report.md",
        "output_json": f"{PRIVATE_ROOT}/out/report.json",
    }


def _request(**overrides) -> dict:
    values = {
        "tex_path": f"{PRIVATE_ROOT}/paper.tex",
        "focus_labels": ["eq:0", "eq:1", "eq:2"],
        "max_labels": 30,
        "budget_profile": "standard",
        "max_attempts": 3,
        "backend_env": "mathdevmcp-backends",
        "search_mode": "agent_guided",
        "grounding_policy": "strict",
        "workers": 1,
    }
    values.update(overrides)
    return build_document_derivation_audit_request(**values)


def _closed_phase06_action(index: int = 0) -> dict:
    scope = {
        "obligation_id": f"obligation-{index}",
        "target": f"x_{index} / x_{index} = 1",
        "candidate_conclusion": f"x_{index} / x_{index} = 1",
        "branch_ids": [f"branch-{index}"],
        "source_spans": [
            {
                "file": "paper.tex",
                "start_byte": 0,
                "end_byte": 9,
                "label": f"eq:{index}",
            }
        ],
        "closed_blocker_scope": ["missing_assumption"],
    }
    entry = build_status_entry(
        status="missing_assumption",
        origin_id=f"attempt-{index}",
        target_id=f"target-{index}",
        scope=scope,
        problem="The nonzero-domain assumption is missing.",
        why="Division by x is not valid when x is zero.",
        source_refs=[f"source://eq:{index}"],
        evidence_refs=[f"evidence://attempt-{index}"],
    )
    branch = {
        "id": f"branch-{index}",
        "obligation_id": f"obligation-{index}",
        "target": f"x_{index} / x_{index} = 1",
        "candidate_conclusion": f"x_{index} / x_{index} = 1",
        "exact_verified_evidence": False,
        "ledgers": [entry],
        "typed_assumptions": [],
        "covered_obligation_ids": [f"obligation-{index}"],
        "execution_cost": None,
    }
    ranking = rank_repair_branches_partial_order([branch])
    return select_next_discriminating_action(ranking, [entry])


def test_all_modes_preserve_complete_global_boundary_and_contract(tmp_path: Path) -> None:
    audit = _raw_audit()
    request = _request()
    responses = {
        mode: compile_document_derivation_response(
            audit,
            request,
            response_mode=mode,
            artifact_root=tmp_path if mode == "artifact_only" else None,
            target_limit=1,
        )
        for mode in ("compact", "detailed", "artifact_only")
    }

    for mode, response in responses.items():
        assert response["metadata"] == {
            "schema_version": "1.0",
            "contract": DOCUMENT_DERIVATION_RESPONSE_CONTRACT,
        }
        assert response["response_schema_version"] == DOCUMENT_DERIVATION_RESPONSE_SCHEMA
        assert response["response_mode"] == mode
        assert response["audit_result_id"] == audit_result_id(audit)
        assert response["audit_request_id"] == request["audit_request_id"]
        assert response["audit_status"] == audit["status"]
        assert response["publication_mode"] == "disabled"
        assert response["promotion"] == audit["promotion"]
        assert response["coverage"] == audit["coverage"]
        assert response["veto_ids"] == [
            "document_repair_publication_disabled",
            "target-veto-0",
            "target-veto-1",
            "target-veto-2",
        ]
        assert response["unresolved_assumption_ids"] == [
            "assumption-0",
            "assumption-1",
            "assumption-2",
        ]
        assert isinstance(response["candidate_assumption_ids"], list)
        assert response["action_decision_ids"] == sorted(
            _closed_phase06_action(index)["action_id"] for index in range(3)
        )
        assert response["reference_inventory"]["evidence_ref_count"] > 0
        assert response["reference_inventory"]["source_ref_count"] > 0
        assert response["non_claims"]
        assert response["completeness"]["global_veto_ids"] == "complete"
        assert validate_document_derivation_response(audit, response) == []
        assert response["canonical_byte_count"] == len(canonical_document_derivation_response_bytes(response))

    assert responses["detailed"]["audit_metadata"] == audit["metadata"]
    assert "markdown" not in responses["detailed"]
    assert "audit_metadata" not in responses["compact"]
    assert "targets" not in responses["artifact_only"]
    assert responses["artifact_only"]["artifact"]["state"] == "verified"


@pytest.mark.parametrize(
    "field",
    [
        "metadata",
        "response_schema_version",
        "response_mode",
        "audit_status",
        "status",
        "audit_result_id",
        "audit_request_id",
        "publication_mode",
        "promotion",
        "coverage",
        "failure_classifications",
        "execution_summary",
        "veto_ids",
        "unresolved_assumption_ids",
        "candidate_assumption_ids",
        "action_decision_ids",
        "reference_inventory",
        "non_claims",
        "artifact",
        "page",
        "completeness",
        "payload_guardrail",
        "canonical_byte_count",
    ],
)
def test_common_boundary_field_deletion_fails_validation(field: str) -> None:
    audit = _raw_audit()
    response = compile_document_derivation_response(audit, _request())
    del response[field]

    errors = validate_document_derivation_response(audit, response)

    assert errors
    assert any(field in error or field in {"metadata", "response_schema_version", "response_mode"} for error in errors)


def test_response_mode_cannot_change_status_promotion_or_coverage() -> None:
    audit = _raw_audit()
    response = compile_document_derivation_response(audit, _request())

    response["audit_status"] = "proved"
    response["status"] = "proved"
    response["promotion"]["reason"] = "changed"
    response["coverage"]["promoted_count"] = 1

    errors = validate_document_derivation_response(audit, response)

    assert "audit status differs from completed audit" in errors
    assert "status alias differs from completed audit" in errors
    assert "promotion differs from completed audit" in errors
    assert "coverage differs from completed audit" in errors
    assert "canonical_byte_count does not match response bytes" in errors


def test_compact_page_publishes_closed_resolver_catalog(tmp_path: Path) -> None:
    response = compile_document_derivation_response(
        _raw_audit(),
        _request(),
        artifact_root=tmp_path,
    )

    catalog = response["page"]["resolver_catalog"]
    assert catalog["global_collections"] == [
        "global_blocker_records",
        "global_evidence_ref_records",
        "global_source_ref_records",
    ]
    assert "label_scoped_obligation" in catalog["target_collections"]


def test_compile_rejects_completed_audit_from_another_source() -> None:
    audit = _raw_audit()

    with pytest.raises(ValueError, match="completed audit source"):
        compile_document_derivation_response(
            audit,
            _request(tex_path=f"{PRIVATE_ROOT}/other.tex"),
        )


def test_compact_paginates_targets_but_never_global_boundary(tmp_path: Path) -> None:
    audit = _raw_audit(target_count=3)
    request = _request()
    first = compile_document_derivation_response(
        audit,
        request,
        artifact_root=tmp_path,
        target_limit=1,
    )
    cursor = first["page"]["page_token"]
    assert cursor
    second = compile_document_derivation_response(
        audit,
        request,
        artifact_root=tmp_path,
        target_limit=1,
        target_cursor=cursor,
    )

    third = compile_document_derivation_response(
        audit,
        request,
        artifact_root=tmp_path,
        target_cursor=second["page"]["page_token"],
    )

    assert first["page"]["target_ids"] + second["page"]["target_ids"] + third["page"]["target_ids"] == [
        "target:target-0",
        "target:target-1",
        "target:target-2",
    ]
    for key in (
        "veto_ids",
        "unresolved_assumption_ids",
        "candidate_assumption_ids",
        "action_decision_ids",
        "non_claims",
        "coverage",
    ):
        assert first[key] == second[key]
    assert first["page"]["continuation_available"] is True
    assert third["page"]["continuation_available"] is False

    with pytest.raises(ValueError, match="target_limit must equal"):
        compile_document_derivation_response(
            audit,
            request,
            artifact_root=tmp_path,
            target_limit=2,
            target_cursor=cursor,
        )


def test_pure_compiler_is_inline_complete_without_persisting_artifact() -> None:
    audit = _raw_audit()
    request = _request()
    first = compile_document_derivation_response(audit, request, target_limit=1)
    assert first["artifact"]["state"] == "not_persisted"
    assert first["compact_representation"] == "inline_complete"
    assert first["page"]["continuation_available"] is False
    assert first["page"]["page_token"] is None
    assert first["page"]["target_ids"] == [
        "target:target-0",
        "target:target-1",
        "target:target-2",
    ]


def test_duplicate_blocker_prose_is_grouped_with_all_targets() -> None:
    response = compile_document_derivation_response(_raw_audit(), _request(), target_limit=1)
    shared = [item for item in response["blocker_catalog"] if item["kind"] == "missing_assumption"]

    assert len(shared) == 1
    assert shared[0]["blocker_ids"] == [
        "blocker-shared-0",
        "blocker-shared-1",
        "blocker-shared-2",
    ]
    assert shared[0]["affected_target_ids"] == [
        "target:target-0",
        "target:target-1",
        "target:target-2",
    ]


def test_persisted_continuation_loads_exact_audit_and_rejects_request_mutations(tmp_path: Path) -> None:
    audit = _raw_audit()
    request = _request()
    first = compile_document_derivation_response(
        audit,
        request,
        artifact_root=tmp_path,
        target_limit=1,
    )
    cursor = first["page"]["page_token"]
    loaded = load_document_derivation_continuation(tmp_path, cursor, request)

    assert loaded == {key: value for key, value in audit.items() if key not in {"markdown", "output_md", "output_json"}}

    mutations = [
        {"tex_path": f"{PRIVATE_ROOT}/other.tex"},
        {"focus_labels": ["eq:1"]},
        {"max_labels": 2},
        {"budget_profile": "smoke"},
        {"max_attempts": 1},
        {"backend_env": "other-env"},
        {"search_mode": "other"},
        {"grounding_policy": "other"},
        {"workers": 2},
    ]
    for mutation in mutations:
        with pytest.raises(ValueError, match="continuation audit request"):
            load_document_derivation_continuation(tmp_path, cursor, _request(**mutation))


def test_cursor_rejects_tamper_other_audit_filter_and_missing_artifact(tmp_path: Path) -> None:
    audit = _raw_audit()
    request = _request()
    response = compile_document_derivation_response(audit, request, artifact_root=tmp_path, target_limit=1)
    cursor = response["page"]["page_token"]

    with pytest.raises(ValueError):
        decode_document_derivation_cursor(cursor[:-1] + ("A" if cursor[-1] != "A" else "B"))
    with pytest.raises(ValueError, match="audit_result_id mismatch"):
        compile_document_derivation_response(
            _raw_audit(target_count=2),
            request,
            artifact_root=tmp_path,
            target_cursor=cursor,
        )
    with pytest.raises(ValueError, match="artifact_root is required"):
        load_document_derivation_continuation(None, cursor, request)


def test_cursor_rejects_noncanonical_and_junk_base64_spellings(tmp_path: Path) -> None:
    response = compile_document_derivation_response(
        _raw_audit(),
        _request(),
        artifact_root=tmp_path,
        target_limit=1,
    )
    cursor = response["page"]["page_token"]

    invalid_spellings = [
        cursor[:8] + "!" + cursor[8:],
        cursor + "AA",
        cursor + "=",
    ]
    for spelling in invalid_spellings:
        with pytest.raises(ValueError, match="page token"):
            decode_document_derivation_cursor(spelling)


def test_artifact_bytes_digest_collision_and_symlink_guards(tmp_path: Path) -> None:
    audit = _raw_audit()
    request = _request()
    response = compile_document_derivation_response(
        audit,
        request,
        response_mode="artifact_only",
        artifact_root=tmp_path,
    )
    artifact = response["artifact"]
    destination = (
        tmp_path
        / "document-derivation"
        / response["audit_result_id"]
        / response["audit_request_id"]
        / "detailed.json"
    )
    payload = destination.read_bytes()
    record = json.loads(payload)

    assert record["schema_version"] == DOCUMENT_DERIVATION_ARTIFACT_SCHEMA
    assert artifact["sha256"] == hashlib.sha256(payload).hexdigest()
    assert artifact["byte_count"] == len(payload)
    second_request = compile_document_derivation_response(
        audit,
        _request(max_attempts=1),
        response_mode="artifact_only",
        artifact_root=tmp_path,
    )
    assert second_request["audit_result_id"] == response["audit_result_id"]
    assert second_request["audit_request_id"] != response["audit_request_id"]
    destination.write_bytes(b"different bytes")
    with pytest.raises(ValueError, match="collision"):
        compile_document_derivation_response(
            audit,
            request,
            response_mode="artifact_only",
            artifact_root=tmp_path,
        )

    symlink_root = tmp_path / "symlink-root"
    symlink_root.symlink_to(tmp_path, target_is_directory=True)
    with pytest.raises(ValueError, match="symlink"):
        compile_document_derivation_response(
            audit,
            request,
            response_mode="artifact_only",
            artifact_root=symlink_root,
        )


def test_transport_redacts_source_backend_output_error_and_artifact_paths(tmp_path: Path) -> None:
    audit = _raw_audit()
    audit["targets"][0]["tree"]["attempt_refs"] = [
        "mathdevmcp://external-tool-adapter/sympy/attempt-1"
    ]
    response = compile_document_derivation_response(
        audit,
        _request(),
        response_mode="detailed",
        artifact_root=tmp_path / "private-artifacts",
    )
    serialized = json.dumps(response, sort_keys=True)

    assert PRIVATE_ROOT not in serialized
    assert str(tmp_path) not in serialized
    assert "/usr/bin/python3" not in serialized
    assert response["tex_path"].startswith("mathdevmcp-source://")
    assert response["tool_uses"][0]["arguments"]["tex_path"].startswith("mathdevmcp-source://")
    assert response["backend_provenance"]["doctor"]["python"]["executable"] == "<redacted-local-path>"
    assert response["backend_provenance"]["doctor"]["capabilities"]["sympy"]["version"] == "1.14.0"
    assert response["targets"][0]["tree"]["assumptions"][0]["source_refs"][0]["label"] == "eq:0"
    assert response["output_references"][0]["logical_uri"].startswith("mathdevmcp-output://")
    assert response["artifact"]["logical_uri"].startswith("mathdevmcp-artifact://")
    assert "mathdevmcp://external-tool-adapter/sympy/attempt-1" in serialized


def test_transport_redacts_private_paths_embedded_in_uris_without_redacting_logical_uris() -> None:
    audit = _raw_audit()
    audit["targets"][0]["tree"]["attempt_refs"] = [
        f"file://{PRIVATE_ROOT}/attempt.json",
        f"evidence://attempt-0?output={PRIVATE_ROOT}/result.json",
        "mathdevmcp://external-tool-adapter/sympy/attempt-0",
    ]
    audit["targets"][0]["tree"]["non_claims"] = [
        f"The diagnostic at file://{PRIVATE_ROOT}/attempt.json is not proof."
    ]
    response = compile_document_derivation_response(audit, _request(), target_limit=1)
    serialized = json.dumps(response, sort_keys=True)

    assert PRIVATE_ROOT not in serialized
    assert "file:///home/" not in serialized
    assert "output=/home/" not in serialized
    assert "<redacted-local-root>" in serialized
    assert "mathdevmcp://external-tool-adapter/sympy/attempt-0" in serialized


def test_compact_preserves_complete_validated_phase06_action_contract() -> None:
    audit = _raw_audit()
    action = _closed_phase06_action()
    audit["targets"][0]["tree"]["branch_ranking"]["selected_action"] = action

    response = compile_document_derivation_response(audit, _request(), target_limit=1)
    transported = response["targets"][0]["selected_action"]

    assert transported == action
    assert validate_discriminating_action(transported) == action
    assert transported["prerequisites"]
    assert set(transported["budget"]) == {
        "profile",
        "max_attempts",
        "timeout_ms",
        "max_output_bytes",
        "provenance",
    }
    assert set(transported["outcomes"]) == {
        "unavailable",
        "unsupported",
        "timeout",
        "execution_error",
        "malformed",
        "certified",
        "refuted",
        "unknown",
    }


def test_nested_promotion_decision_vetoes_are_complete_and_mutation_detected() -> None:
    audit = _raw_audit()
    audit["targets"][0]["promotion_decision"] = {
        "vetoes": ["exact_branch_binding", "publication_policy_and_aggregate_gate"]
    }
    response = compile_document_derivation_response(audit, _request(), target_limit=1)

    assert "exact_branch_binding" in response["veto_ids"]
    assert "publication_policy_and_aggregate_gate" in response["veto_ids"]
    assert "exact_branch_binding" in response["targets"][0]["veto_ids"]
    mutated = deepcopy(response)
    mutated["veto_ids"].remove("exact_branch_binding")
    assert "veto_ids differs from completed audit" in validate_document_derivation_response(
        audit,
        mutated,
    )


def test_current_global_ledgers_do_not_inflate_legacy_nested_history() -> None:
    audit = _raw_audit()
    audit["integrity_binding_verified"] = True
    audit["veto_ids"] = ["document_repair_publication_disabled"]
    audit["failure_classifications"] = ["mathematical_gap"]
    audit["targets"][0]["tree"]["historical_backend_evidence"] = {
        "failure_classification": "evidence_binding_error",
        "veto_ids": ["legacy_unbound_document_evidence"],
    }

    response = compile_document_derivation_response(audit, _request(), target_limit=1)

    assert response["failure_classifications"] == ["mathematical_gap"]
    assert "legacy_unbound_document_evidence" not in response["veto_ids"]
    assert "document_repair_publication_disabled" in response["veto_ids"]


def test_request_identity_binds_exact_worker_argument() -> None:
    zero = _request(workers=0)
    one = _request(workers=1)

    assert zero["workers"] == 0
    assert zero["audit_request_id"] != one["audit_request_id"]


def test_artifact_only_requires_root_and_response_rejects_publication() -> None:
    with pytest.raises(ValueError, match="artifact_root"):
        compile_document_derivation_response(_raw_audit(), _request(), response_mode="artifact_only")

    enabled = _raw_audit()
    enabled["publication_mode"] = "experimental"
    with pytest.raises(ValueError, match="publication_mode=disabled"):
        compile_document_derivation_response(enabled, _request())

    promoted = _raw_audit()
    promoted["promotion"]["can_promote"] = True
    with pytest.raises(ValueError, match="promotion authority"):
        compile_document_derivation_response(promoted, _request())


def test_duplicate_target_identity_is_rejected() -> None:
    audit = _raw_audit(target_count=2)
    audit["targets"][1]["id"] = audit["targets"][0]["id"]

    with pytest.raises(ValueError, match="duplicate target identities"):
        compile_document_derivation_response(audit, _request())


def test_disabled_audit_compiles_without_targets_or_source_access() -> None:
    audit = {
        "metadata": {"contract": "document_derivation_tree_audit", "schema_version": "1.0"},
        "status": "document_derivation_tree_disabled_pending_publication_safety",
        "publication_mode": "disabled",
        "promotion": {"can_promote": False},
        "coverage": {"status": "not_run_tool_disabled", "promoted_count": 0},
        "veto_ids": ["tool_disabled", "publication_disabled"],
        "targets": [],
        "non_claims": [{"code": "tool_disabled_not_audit", "text": "The source was not read."}],
    }
    response = compile_document_derivation_response(audit, _request(tex_path="/missing/private.tex"))

    assert response["targets"] == []
    assert response["page"]["total_target_count"] == 0
    assert response["veto_ids"] == ["publication_disabled", "tool_disabled"]


def test_compact_consumer_has_action_source_evidence_and_boundary_under_guardrail() -> None:
    response = compile_document_derivation_response(_raw_audit(), _request(), target_limit=1)
    target = response["targets"][0]

    assert target["target_id"]
    assert target["blocker_ids"]
    assert target["selected_action"]["action_id"]
    assert target["selected_action"]["expected_artifact"]
    assert "candidate_assumptions" in target
    assert target["evidence_refs"]
    assert target["source_refs"]
    assert target["source_evidence"]["target"]
    assert "normalized_target" in target["source_evidence"]
    assert "routing_role" in target["source_evidence"]
    assert target["source_evidence"]["boundary"] == {
        "claim_eligibility": "ineligible",
        "publication_enabled": False,
        "promotion_allowed": False,
    }
    assert "document_repair_publication_disabled" in response["veto_ids"]
    assert response["non_claims"]
    assert response["compact_representation"] == "inline_complete"
    assert len(response["targets"]) == 3
    assert response["canonical_byte_count"] > 25_600
    assert response["payload_guardrail"]["status"] == "exceeded_complete_boundary_preserved"


def test_payload_guardrail_never_omits_complete_boundary() -> None:
    audit = _raw_audit()
    audit["non_claims"].append(
        {"code": "large_required_boundary", "text": "required " + "x" * 30_000}
    )
    response = compile_document_derivation_response(audit, _request(), target_limit=1)

    assert response["canonical_byte_count"] > 25_600
    assert response["payload_guardrail"]["status"] == "exceeded_complete_boundary_preserved"
    assert any(
        isinstance(item, dict) and item.get("code") == "large_required_boundary"
        for item in response["non_claims"]
    )
    assert validate_document_derivation_response(audit, response) == []


def test_facade_initial_request_calls_raw_audit_once_and_continuation_zero_times(
    tmp_path: Path, monkeypatch
) -> None:
    calls: list[dict] = []

    def captured_audit(tex_path, **kwargs):
        calls.append({"tex_path": tex_path, **kwargs})
        audit = _raw_audit()
        audit["tex_path"] = str(tex_path)
        return audit

    monkeypatch.setattr(mcp_facade, "high_level_audit_document_derivation_tree", captured_audit)
    arguments = {
        "tex_path": str(tmp_path / "paper.tex"),
        "focus_labels": ["eq:0", "eq:1", "eq:2"],
        "max_labels": 30,
        "budget_profile": "standard",
        "max_attempts": 3,
        "backend_env": "mathdevmcp-backends",
        "search_mode": "agent_guided",
        "grounding_policy": "strict",
        "workers": 1,
        "artifact_root": str(tmp_path / "artifacts"),
        "target_limit": 1,
    }

    first = call_mcp_tool("audit_document_derivation_tree", arguments)
    second = call_mcp_tool(
        "audit_document_derivation_tree",
        {**arguments, "target_cursor": first["page"]["page_token"]},
    )

    assert first["ok"] is second["ok"] is True
    assert len(calls) == 1
    assert first["page"]["target_ids"] == ["target:target-0"]
    assert second["page"]["target_ids"] == ["target:target-1"]
    assert second["audit_result_id"] == first["audit_result_id"]


def test_facade_rejects_changed_continuation_before_raw_audit(tmp_path: Path, monkeypatch) -> None:
    calls = 0

    def captured_audit(_tex_path, **_kwargs):
        nonlocal calls
        calls += 1
        audit = _raw_audit()
        audit["tex_path"] = str(_tex_path)
        return audit

    monkeypatch.setattr(mcp_facade, "high_level_audit_document_derivation_tree", captured_audit)
    arguments = {
        "tex_path": str(tmp_path / "paper.tex"),
        "focus_labels": ["eq:0"],
        "artifact_root": str(tmp_path / "artifacts"),
        "target_limit": 1,
    }
    first = call_mcp_tool("audit_document_derivation_tree", arguments)
    changed = call_mcp_tool(
        "audit_document_derivation_tree",
        {
            **arguments,
            "max_attempts": 1,
            "target_cursor": first["page"]["page_token"],
        },
    )

    assert calls == 1
    assert changed["ok"] is False
    assert changed["error"]["type"] == "invalid_arguments"
    assert "continuation audit request" in changed["error"]["message"]


@pytest.mark.parametrize(
    "arguments",
    [
        {"response_mode": "invalid"},
        {"target_limit": 0},
        {"target_limit": 101},
        {"response_mode": "artifact_only"},
        {"response_mode": "detailed", "target_cursor": "invalid"},
        {"target_cursor": "invalid"},
    ],
)
def test_facade_invalid_response_options_fail_before_raw_audit(arguments, monkeypatch) -> None:
    def forbidden_audit(*_args, **_kwargs):
        raise AssertionError("raw audit must not run for invalid response options")

    monkeypatch.setattr(mcp_facade, "high_level_audit_document_derivation_tree", forbidden_audit)
    result = call_mcp_tool(
        "audit_document_derivation_tree",
        {"tex_path": "/missing/private.tex", **arguments},
    )

    assert result["ok"] is False
    assert result["error"]["type"] == "invalid_arguments"


def test_cli_continuation_uses_persisted_audit_after_source_is_removed(tmp_path: Path) -> None:
    tex = tmp_path / "two-targets.tex"
    tex.write_text(
        """\\begin{equation}
\\label{eq:first}
x + 1 = 1 + x
\\end{equation}
\\begin{equation}
\\label{eq:second}
y + 1 = 1 + y
\\end{equation}
""",
        encoding="utf-8",
    )
    artifact_root = tmp_path / "artifacts"
    command = [
        sys.executable,
        "-m",
        "mathdevmcp.cli",
        "audit-document-derivation-tree",
        str(tex),
        "--focus-label",
        "eq:first",
        "--focus-label",
        "eq:second",
        "--budget-profile",
        "smoke",
        "--max-attempts",
        "1",
        "--artifact-root",
        str(artifact_root),
        "--target-limit",
        "1",
    ]
    first_run = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
    )
    assert first_run.returncode == 0, first_run.stderr
    first = json.loads(first_run.stdout)
    cursor = first["page"]["page_token"]
    assert cursor
    tex.unlink()

    second_run = subprocess.run(
        [*command, "--target-cursor", cursor],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src")},
    )
    assert second_run.returncode == 0, second_run.stderr
    second = json.loads(second_run.stdout)

    assert [target["label"] for target in first["targets"]] == ["eq:first"]
    assert [target["label"] for target in second["targets"]] == ["eq:second"]
    assert first["page"]["target_ids"] != second["page"]["target_ids"]
    assert second["audit_result_id"] == first["audit_result_id"]
    assert second["artifact"] == first["artifact"]


def test_v2_page_token_is_fixed_width_canonical_and_rejects_alternate_spellings(
    tmp_path: Path,
) -> None:
    response = compile_document_derivation_response(
        _raw_audit(), _request(), artifact_root=tmp_path, target_limit=1
    )
    token = response["page"]["page_token"]
    raw = base64.urlsafe_b64decode(token + "=" * (-len(token) % 4))

    assert len(raw) == 236
    assert len(token) == 315
    assert base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=") == token
    assert decode_document_derivation_cursor(token)["requested_target_limit"] == 1

    invalid = [
        token + "=",
        token + "\n",
        token[:-1],
        token + "A",
        base64.b64encode(raw).decode("ascii").rstrip("="),
    ]
    for value in invalid:
        if value == token:
            continue
        with pytest.raises(ValueError):
            decode_document_derivation_cursor(value)

    for index in range(len(raw)):
        mutated = bytearray(raw)
        mutated[index] ^= 1
        candidate = base64.urlsafe_b64encode(mutated).decode("ascii").rstrip("=")
        with pytest.raises(ValueError):
            decode_document_derivation_cursor(candidate)


@pytest.mark.parametrize(
    ("mutation_id", "mutate", "expected_error"),
    [
        (
            "identity_table",
            lambda response: response["page_identity_tables"]["blocker_ids"].__setitem__(
                0, "changed-blocker"
            ),
            "page identity tables mismatch",
        ),
        (
            "index_membership",
            lambda response: response["targets"][0]["blocker_indices"].__setitem__(
                0, response["targets"][0]["blocker_indices"][1]
            ),
            "target 0 reconstruction failed",
        ),
        (
            "content_identity",
            lambda response: response["targets"][0]["content_identity"].__setitem__(
                "target_text_sha256", "0" * 64
            ),
            "content identity mismatch",
        ),
        (
            "selected_action",
            lambda response: response["targets"][0]["selected_action"]["action"].__setitem__(
                "action_id", "action_" + "0" * 64
            ),
            "action semantic id mismatch",
        ),
        (
            "record_count",
            lambda response: response["targets"][0].__setitem__(
                "blocker_record_count",
                response["targets"][0]["blocker_record_count"] + 1,
            ),
            "blocker_record_count mismatch",
        ),
        (
            "record_inventory",
            lambda response: response["record_inventory"].__setitem__(
                "global_source_ref_count",
                response["record_inventory"]["global_source_ref_count"] + 1,
            ),
            "record inventory mismatch",
        ),
        (
            "page_token_semantics",
            lambda response: response["page"].__setitem__(
                "page_token",
                _forge_checksummed_token(
                    response["page"]["page_token"], "resolver_scope_digest"
                ),
            ),
            "page token semantic binding mismatch",
        ),
    ],
)
def test_artifact_indexed_validator_rejects_postconstruction_semantic_mutations(
    tmp_path: Path,
    mutation_id: str,
    mutate,
    expected_error: str,
) -> None:
    audit = _raw_audit()
    response = compile_document_derivation_response(
        audit, _request(), artifact_root=tmp_path, target_limit=1
    )
    mutated = deepcopy(response)

    mutate(mutated)
    _refresh_canonical_byte_count(mutated)
    errors = validate_document_derivation_response(audit, mutated)

    assert any(expected_error in error for error in errors), (
        mutation_id,
        errors,
    )


@pytest.mark.parametrize(
    ("mutation_id", "field", "replacement"),
    [
        ("negative", "blocker_indices", [-1]),
        ("out_of_range", "blocker_indices", [10_000]),
        ("duplicate", "blocker_indices", [0, 0]),
        ("repeated_assumption", "unresolved_assumption_indices", [0, 0]),
    ],
)
def test_artifact_indexed_validator_rejects_invalid_index_shapes(
    tmp_path: Path,
    mutation_id: str,
    field: str,
    replacement: list[int],
) -> None:
    audit = _raw_audit()
    response = compile_document_derivation_response(
        audit, _request(), artifact_root=tmp_path, target_limit=1
    )
    mutated = deepcopy(response)
    mutated["targets"][0][field] = replacement
    _refresh_canonical_byte_count(mutated)

    errors = validate_document_derivation_response(audit, mutated)

    assert errors, mutation_id
    assert any(
        "reconstruction failed" in error or "membership mismatch" in error
        for error in errors
    ), (mutation_id, errors)


@pytest.mark.parametrize(
    "field",
    [
        "audit_result_id",
        "audit_request_id",
        "artifact_sha256",
        "filter_id",
        "requested_target_limit",
        "next_offset",
        "page_boundary_digest",
        "resolver_scope_digest",
    ],
)
def test_checksummed_forged_tokens_fail_semantic_binding(
    tmp_path: Path,
    field: str,
) -> None:
    audit = _raw_audit()
    request = _request()
    response = compile_document_derivation_response(
        audit, request, artifact_root=tmp_path, target_limit=1
    )
    forged = _forge_checksummed_token(response["page"]["page_token"], field)

    assert decode_document_derivation_cursor(forged)["checksum"]
    with pytest.raises(ValueError):
        compile_document_derivation_response(
            audit,
            request,
            artifact_root=tmp_path,
            target_cursor=forged,
        )


def test_continuation_reuses_token_limit_and_rejects_explicit_mismatch(
    tmp_path: Path,
) -> None:
    audit = _raw_audit()
    request = _request()
    first = compile_document_derivation_response(
        audit, request, artifact_root=tmp_path, target_limit=1
    )
    token = first["page"]["page_token"]

    second = compile_document_derivation_response(
        audit, request, artifact_root=tmp_path, target_cursor=token
    )
    assert second["page"]["requested_limit"] == 1
    with pytest.raises(ValueError, match="target_limit must equal"):
        compile_document_derivation_response(
            audit,
            request,
            artifact_root=tmp_path,
            target_limit=2,
            target_cursor=token,
        )


def test_resolver_enforces_exact_scope_and_reconstructs_ordered_bindings(
    tmp_path: Path,
) -> None:
    audit = _raw_audit()
    request = _request()
    page = compile_document_derivation_response(
        audit, request, artifact_root=tmp_path, target_limit=1
    )
    token = page["page"]["page_token"]
    target_id = page["page"]["target_ids"][0]

    global_records = resolve_document_derivation_records(
        token,
        "global_evidence_ref_records",
        artifact_root=tmp_path,
        limit=1,
    )
    assert global_records["target_id"] is None
    assert global_records["returned_record_count"] == 1
    assert global_records["next_offset"] == 1

    all_bindings: list[tuple[str, str]] = []
    offset = 0
    while True:
        resolved = resolve_document_derivation_records(
            token,
            "global_evidence_ref_records",
            artifact_root=tmp_path,
            offset=offset,
            limit=2,
        )
        all_bindings.extend(
            (item["identity"], item["raw_record_sha256"])
            for item in resolved["records"]
        )
        if resolved["next_offset"] is None:
            break
        offset = resolved["next_offset"]
    assert len(all_bindings) == len(set(all_bindings))

    target_record = resolve_document_derivation_records(
        token,
        "label_scoped_obligation",
        artifact_root=tmp_path,
        target_id=target_id,
    )
    assert target_record["records"][0]["identity"].startswith("obl_")
    assert document_derivation_public_surface_sizes(target_record)[
        "stdio_jsonrpc_line"
    ] <= 30_720

    invalid_pairs = [
        (target_id, "global_evidence_ref_records"),
        (None, "label_scoped_obligation"),
        ("target:other", "label_scoped_obligation"),
    ]
    for invalid_target, collection in invalid_pairs:
        with pytest.raises(ValueError, match="outside the page token scope"):
            resolve_document_derivation_records(
                token,
                collection,
                artifact_root=tmp_path,
                target_id=invalid_target,
            )

    with pytest.raises(ValueError, match="collection must be one of: .*global_evidence_ref_records"):
        resolve_document_derivation_records(
            token,
            "unknown_collection",
            artifact_root=tmp_path,
            target_id=target_id,
        )


def test_resolver_empty_collection_accepts_only_offset_zero(tmp_path: Path) -> None:
    audit = _raw_audit(target_count=2)
    audit["targets"][1]["tree"]["assumptions"] = []
    request = _request()
    first = compile_document_derivation_response(
        audit, request, artifact_root=tmp_path, target_limit=1
    )
    second = compile_document_derivation_response(
        audit,
        request,
        artifact_root=tmp_path,
        target_cursor=first["page"]["page_token"],
    )
    token = second["page"]["page_token"]
    target_id = second["page"]["target_ids"][0]

    empty = resolve_document_derivation_records(
        token,
        "unresolved_assumption_records",
        artifact_root=tmp_path,
        target_id=target_id,
        offset=0,
    )
    assert empty["records"] == []
    assert empty["next_offset"] is None
    with pytest.raises(ValueError, match="empty collection"):
        resolve_document_derivation_records(
            token,
            "unresolved_assumption_records",
            artifact_root=tmp_path,
            target_id=target_id,
            offset=1,
        )


def test_artifact_mutation_is_rejected_without_leaking_private_paths(
    tmp_path: Path,
) -> None:
    audit = _raw_audit()
    request = _request()
    response = compile_document_derivation_response(
        audit, request, artifact_root=tmp_path, target_limit=1
    )
    token = response["page"]["page_token"]
    destination = (
        tmp_path
        / "document-derivation"
        / response["audit_result_id"]
        / response["audit_request_id"]
        / "detailed.json"
    )
    payload = bytearray(destination.read_bytes())
    payload[-1] ^= 1
    destination.write_bytes(payload)

    with pytest.raises(ValueError, match="artifact digest mismatch") as direct:
        resolve_document_derivation_records(
            token,
            "global_evidence_ref_records",
            artifact_root=tmp_path,
        )
    assert PRIVATE_ROOT not in str(direct.value)
    assert str(tmp_path) not in str(direct.value)

    facade = call_mcp_tool(
        "resolve_document_derivation_records",
        {
            "page_token": token,
            "collection": "global_evidence_ref_records",
            "artifact_root": str(tmp_path),
        },
    )
    serialized = json.dumps(facade, sort_keys=True)
    assert facade["ok"] is False
    assert facade["error"]["type"] == "invalid_arguments"
    assert PRIVATE_ROOT not in serialized
    assert str(tmp_path) not in serialized
    assert token not in serialized

    call_result = mcp_server.resolve_document_derivation_records(
        token,
        "global_evidence_ref_records",
        str(tmp_path),
    )
    public = call_result.model_dump(by_alias=True, exclude_none=True)
    serialized_public = json.dumps(public, sort_keys=True)
    assert public["isError"] is True
    assert PRIVATE_ROOT not in serialized_public
    assert str(tmp_path) not in serialized_public
    assert token not in serialized_public

    cli = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "resolve-document-derivation-records",
            token,
            "global_evidence_ref_records",
            "--artifact-root",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert cli.returncode == 2
    assert cli.stdout == ""
    cli_error = json.loads(cli.stderr)
    assert cli_error == {
        "error": {
            "message": (
                "Document derivation request or persisted artifact failed "
                "validation."
            ),
            "type": "invalid_arguments",
        },
        "metadata": {"contract": "error", "schema_version": "1.0"},
        "ok": False,
    }
    assert "Traceback" not in cli.stderr
    assert PRIVATE_ROOT not in cli.stderr
    assert str(tmp_path) not in cli.stderr
    assert token not in cli.stderr


def test_cli_rejects_bad_continuation_token_without_echoing_inputs(
    tmp_path: Path,
) -> None:
    token = "not-a-valid-page-token"
    source = f"{PRIVATE_ROOT}/paper.tex"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-document-derivation-tree",
            source,
            "--artifact-root",
            str(tmp_path),
            "--target-cursor",
            token,
        ],
        check=False,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert completed.returncode == 2
    assert completed.stdout == ""
    assert json.loads(completed.stderr)["error"]["type"] == "invalid_arguments"
    assert "Traceback" not in completed.stderr
    assert source not in completed.stderr
    assert str(tmp_path) not in completed.stderr
    assert token not in completed.stderr
