from __future__ import annotations

from copy import deepcopy
import hashlib

from mathdevmcp.evidence_manifest import (
    P01_NON_CLAIMS,
    build_evidence_manifest,
    build_evidence_request,
    canonical_json_bytes,
    content_digest,
)
from mathdevmcp.promotion_policy import evaluate_promotion, verify_exact_binding


SOURCE_BYTES = b"x + 1 = 1 + x"
NATIVE_BYTES = b"check(x + 1 = 1 + x)"
EDIT_BYTES = b"x + 1 = 1 + x"


def _fixture():
    assumptions = [{"id": "scalar", "kind": "domain", "statement": "x is a real scalar."}]
    tool = {"name": "fake", "adapter_version": "1", "backend_version": "test", "executable_id": "fake_runner"}
    request = build_evidence_request(
        source={
            "logical_id": "synthetic/source.tex",
            "file": "synthetic/source.tex",
            "digest": hashlib.sha256(SOURCE_BYTES).hexdigest(),
            "spans": [{"start_byte": 0, "end_byte": len(SOURCE_BYTES)}],
            "label": "eq:test",
            "parser_version": "synthetic-1",
        },
        obligation={"digest": hashlib.sha256(SOURCE_BYTES).hexdigest(), "target": "x + 1 = 1 + x"},
        branch={"id": "branch_test", "lineage": ["root", "branch_test"]},
        typed_assumptions=assumptions,
        assumption_digest=content_digest(assumptions),
        native_input={"digest": hashlib.sha256(NATIVE_BYTES).hexdigest(), "media_type": "text/plain"},
        tool=tool,
        resource_limits={"timeout_ms": 1000, "max_output_bytes": 4096},
        expected_result_class="synthetic_fixture",
        backend_role="test_only_noncertifying",
        unsupported_conclusions=list(P01_NON_CLAIMS),
        policy_version="p01-test",
    )
    request_bytes = canonical_json_bytes(request, schema="evidence_request@1")

    def artifact(ref, data, role, media_type="application/octet-stream"):
        return {
            "logical_ref": ref,
            "media_type": media_type,
            "sha256": hashlib.sha256(data).hexdigest(),
            "byte_count": len(data),
            "role": role,
        }

    request_artifact = artifact("attempt/request.json", request_bytes, "request", "application/json")
    native = artifact("attempt/native-input.txt", NATIVE_BYTES, "native_input", "text/plain")
    stdout = artifact("attempt/stdout.txt", b"ok\n", "stdout", "text/plain")
    stderr = artifact("attempt/stderr.txt", b"", "stderr", "text/plain")
    structured = artifact("attempt/result.json", b'{"status":"synthetic_ok"}', "structured_result", "application/json")
    manifest = build_evidence_manifest(
        request=request,
        request_digest=content_digest(request, schema="evidence_request@1"),
        attempt_id=f"att_{content_digest(request, schema='evidence_request@1')}",
        execution_id="exe_00000000000000000000000000000000",
        run_id="run_test",
        execution={
            "started_at_utc": "2026-07-11T00:00:00Z",
            "ended_at_utc": "2026-07-11T00:00:01Z",
            "wall_time_ns": 1,
            "exit_classification": "completed",
            "exit_code": 0,
            "signal": None,
            "timeout": False,
            "device_execution": {"mode": "cpu_test_double", "gpu_requested": False, "gpu_initialized": False},
            "environment": {
                "python_implementation": "CPython",
                "python_version": "3.11.15",
                "platform_system": "Linux",
                "test_runner_version": "pytest-test",
            },
            "runner_version": "fake-1",
        },
        result={
            "outcome": "certified",
            "stdout": stdout,
            "stderr": stderr,
            "structured_result": structured,
            "stdout_truncated": False,
            "stderr_truncated": False,
            "redaction": {"applied": False, "fields": []},
            "certificate": None,
        },
        integrity={
            "request_artifact": request_artifact,
            "artifact_inventory": [request_artifact, native, stdout, stderr, structured],
            "atomic_write_state": "manifest_published_last_no_overwrite",
            "integrity_state": "sealed_pending_reader_verification",
        },
        interpretation={
            "certified_scope": "synthetic fixture only",
            "refuted_scope": None,
            "unresolved_assumption_ids": [],
            "blocker_ids": [],
            "veto_ids": [],
            "non_claims": list(P01_NON_CLAIMS),
        },
    )
    manifest_sha256 = hashlib.sha256(canonical_json_bytes(manifest, schema="evidence_manifest@1")).hexdigest()
    verified = [{"integrity_state": "verified", "manifest_sha256": manifest_sha256, "manifest": manifest}]
    source = {"bytes": SOURCE_BYTES, "spans": request["source"]["spans"], "label": "eq:test", "edit_span": {"start_byte": 0, "end_byte": len(SOURCE_BYTES)}}
    branch = {"id": "branch_test", "lineage": ["root", "branch_test"], "obligation_digest": request["obligation"]["digest"], "normalized_target": request["obligation"]["target"], "typed_assumptions": assumptions}
    edit = {"bytes": EDIT_BYTES, "digest": hashlib.sha256(EDIT_BYTES).hexdigest(), "source_digest": hashlib.sha256(SOURCE_BYTES).hexdigest(), "label": "eq:test", "span": source["edit_span"]}
    policy = {"native_input_bytes": NATIVE_BYTES, "tool": tool, "backend_role": "test_only_noncertifying", "allowed_outcomes": ["certified"], "evidence_vetoes": [], "engineering_vetoes": [], "conflict_detected": False, "publication_enabled": False}
    return verified, source, branch, edit, policy


def test_complete_synthetic_fixture_verifies_integrity_but_is_never_claim_eligible() -> None:
    result = verify_exact_binding(*_fixture())
    assert result["integrity_binding_verified"] is True
    assert result["integrity_binding_status"] == "verified_for_synthetic_fixture"
    assert result["claim_eligibility"] == "ineligible"
    assert result["publication_enabled"] is False
    assert result["decision"] == "publish_evidence_report"


def test_verified_manifests_are_required_for_integrity_binding() -> None:
    verified, source, branch, edit, policy = _fixture()
    verified[0]["integrity_state"] = "sealed_pending_reader_verification"
    result = evaluate_promotion(verified, source, branch, edit, policy)
    assert result["integrity_binding_verified"] is False
    assert "verified_manifest" in result["failed_invariant_ids"]
    assert result["claim_eligibility"] == "ineligible"


def test_mutation_matrix_vetoes_every_material_binding_group_without_mutation() -> None:
    base = _fixture()
    before = deepcopy(base)
    mutations = []

    def mutate(index, path, value):
        case = deepcopy(base)
        target = case[index]
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        mutations.append(case)

    mutate(1, ("bytes",), b"changed")
    mutate(1, ("spans",), [{"start_byte": 1, "end_byte": 2}])
    mutate(1, ("label",), "eq:other")
    mutate(2, ("obligation_digest",), "0" * 64)
    mutate(2, ("normalized_target",), "x=x")
    mutate(2, ("id",), "other")
    mutate(2, ("lineage",), ["root", "other"])
    mutate(2, ("typed_assumptions",), [])
    mutate(3, ("bytes",), b"changed edit")
    mutate(4, ("native_input_bytes",), b"changed native")
    mutate(4, ("tool",), {"name": "other"})
    mutate(4, ("backend_role",), "other")
    mutate(4, ("conflict_detected",), True)
    mutate(4, ("evidence_vetoes",), ["veto"])
    mutate(4, ("engineering_vetoes",), ["error"])
    mutate(4, ("publication_enabled",), True)
    manifest_case = deepcopy(base)
    manifest_case[0][0]["manifest"]["result"]["stdout_truncated"] = True
    mutations.append(manifest_case)

    for case in mutations:
        result = evaluate_promotion(*case)
        assert result["integrity_binding_verified"] is False
        assert result["claim_eligibility"] == "ineligible"
        assert result["publication_enabled"] is False
    assert base == before


def test_cached_legacy_promotion_fields_have_no_authority() -> None:
    verified, source, branch, edit, policy = _fixture()
    branch["can_promote"] = True
    branch["status"] = "proved"
    branch["output_ref"] = "mathdevmcp://legacy/success"
    result = evaluate_promotion(verified, source, branch, edit, policy)
    assert result["integrity_binding_verified"] is True
    assert result["claim_eligibility"] == "ineligible"
    assert result["publication_enabled"] is False
