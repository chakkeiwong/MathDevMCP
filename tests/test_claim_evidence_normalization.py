from __future__ import annotations

from copy import deepcopy
import hashlib
import json

import pytest

from mathdevmcp.derivation_search_orchestrator import (
    P04_REQUEST_SCHEMA,
    P04_RESULT_SCHEMA,
)
from mathdevmcp.derivation_branch_controller import rank_repair_branches
from mathdevmcp.derivation_search_tree import (
    build_branch_record,
    transition_branch,
    validate_branch_record,
)
from mathdevmcp.evidence_manifest import (
    P01_NON_CLAIMS,
    allocate_execution,
    atomic_write_artifact,
    build_evidence_request,
    canonical_json_bytes,
    content_digest,
    create_run_bundle,
    seal_attempt_manifest,
)
from mathdevmcp.external_adapter_contract import (
    ExternalAdapterContractError,
    P06_REGISTERED_REVALIDATION_READER,
    RevalidatingClaimEvidence,
    build_external_adapter_request,
    build_external_adapter_result,
    normalize_generic_v1_claim_evidence,
    normalize_registered_adapter_claim_evidence,
    reader_verified_claim_evidence_record,
    reverify_registered_adapter_claim_evidence,
    validate_normalized_claim_evidence,
    verify_live_adapter_manifest,
)
from mathdevmcp.sage_adapter import (
    SAGE_ADAPTER_VERSION,
    SAGE_RESULT_SENTINEL,
    SagePolynomialObligation,
    _execution_environment,
    _seal_manifest,
    generate_sage_polynomial_script,
)


def _p04_request(branch: dict, *, native_input: str, backend: str, timeout_ms: int = 1_000) -> dict:
    request = {
        "schema_version": P04_REQUEST_SCHEMA,
        "branch_id": branch["id"],
        "branch_lineage": list(branch["lineage"]),
        "obligation_digest": branch["obligation_digest"],
        "target": branch["target"],
        "typed_assumption_digests": list(branch["typed_assumption_digests"]),
        "action_kind": "backend",
        "backend": backend,
        "native_input": native_input,
        "native_input_digest": content_digest(native_input.encode("utf-8")),
        "timeout_ms": timeout_ms,
        "max_output_bytes": 4_096,
        "max_artifact_bytes": 1_048_576,
        "formalization_plan_digest": content_digest(branch["formalization_plan"]),
    }
    request["request_digest"] = content_digest(request)
    request["request_ref"] = f"artifact://p04/request/{request['request_digest']}"
    return request


def _p04_result(
    request: dict,
    *,
    test_only: bool,
    live_tool_executed: bool,
    manifest_verified: bool,
    adapter_result_digest: str | None,
    live_manifest_verification: dict | None,
    output_ref: str,
) -> dict:
    result = {
        "schema_version": P04_RESULT_SCHEMA,
        "branch_id": request["branch_id"],
        "request_digest": request["request_digest"],
        "status": "proved",
        "evidence_kind": "certifying_backend",
        "certification_status": "certified",
        "closed_blocker_ids": [],
        "reason": "Synthetic current-schema result for normalization tests.",
        "output_ref": output_ref,
        "raw_result_digest": content_digest({"fixture": output_ref}),
        "test_only": test_only,
        "live_tool_executed": live_tool_executed,
        "manifest_verified": manifest_verified,
        "adapter_result_digest": adapter_result_digest,
        "live_manifest_verification": live_manifest_verification,
    }
    result["result_digest"] = content_digest(result)
    result["result_ref"] = f"artifact://p04/result/{result['result_digest']}"
    return result


def _final_branch(initial: dict, request: dict, result: dict) -> dict:
    running = transition_branch(
        initial,
        "running",
        reason="Execute the exact synthetic request.",
        request_ref=request["request_ref"],
    )
    final = transition_branch(
        running,
        "proved",
        reason="Record the exact synthetic result.",
        request_ref=request["request_ref"],
        result_ref=result["result_ref"],
    )
    assert validate_branch_record(final) == []
    return final


def _redigest_request(value: dict) -> dict:
    request = deepcopy(value)
    request.pop("request_digest", None)
    request.pop("request_ref", None)
    request["request_digest"] = content_digest(request)
    request["request_ref"] = f"artifact://p04/request/{request['request_digest']}"
    return request


def _redigest_result(value: dict) -> dict:
    result = deepcopy(value)
    result.pop("result_digest", None)
    result.pop("result_ref", None)
    result["result_digest"] = content_digest(result)
    result["result_ref"] = f"artifact://p04/result/{result['result_digest']}"
    return result


def _generic_fixture(tmp_path) -> dict:
    source_bytes = b"x + 1 = 1 + x"
    target = source_bytes.decode("ascii")
    native_input = "check(x + 1 == 1 + x)"
    assumptions = [
        {
            "id": "scalar_x",
            "kind": "domain",
            "statement": "x is a real scalar.",
        }
    ]
    initial = build_branch_record(
        obligation_digest=hashlib.sha256(target.encode("utf-8")).hexdigest(),
        target=target,
        typed_assumptions=assumptions,
        generator={"kind": "root"},
        formalization_plan={
            "backend": "fake",
            "action_kind": "backend",
            "native_input": native_input,
            "timeout_seconds": 1,
        },
        state="ready",
    )
    p04_request = _p04_request(initial, native_input=native_input, backend="fake")
    p04_result = _p04_result(
        p04_request,
        test_only=True,
        live_tool_executed=False,
        manifest_verified=False,
        adapter_result_digest=None,
        live_manifest_verification=None,
        output_ref="artifact://synthetic/generic-v1",
    )
    branch = _final_branch(initial, p04_request, p04_result)

    request = build_evidence_request(
        source={
            "logical_id": "synthetic/source.tex",
            "file": "synthetic/source.tex",
            "digest": hashlib.sha256(source_bytes).hexdigest(),
            "spans": [{"start_byte": 0, "end_byte": len(source_bytes)}],
            "label": "eq:generic",
            "parser_version": "synthetic-1",
        },
        obligation={"digest": initial["obligation_digest"], "target": target},
        branch={"id": initial["id"], "lineage": initial["lineage"]},
        typed_assumptions=assumptions,
        assumption_digest=content_digest(assumptions),
        native_input={
            "digest": p04_request["native_input_digest"],
            "media_type": "text/plain",
        },
        tool={
            "name": "fake",
            "adapter_version": "p06-generic-test",
            "backend_version": "test",
            "executable_id": "fake_runner",
        },
        resource_limits={"timeout_ms": 1_000, "max_output_bytes": 4_096},
        expected_result_class="synthetic_normalization_fixture",
        backend_role="test_only_noncertifying",
        unsupported_conclusions=list(P01_NON_CLAIMS),
        policy_version="p06-generic-test",
    )
    bundle = create_run_bundle(tmp_path / "generic-evidence", run_id="run_p06_generic")
    execution = allocate_execution(bundle, request)
    native = atomic_write_artifact(
        bundle,
        f"{execution.logical_root}/native-input.txt",
        native_input.encode("utf-8"),
        media_type="text/plain",
        role="native_input",
    )
    stdout = atomic_write_artifact(
        bundle,
        f"{execution.logical_root}/stdout.txt",
        b"ok\n",
        media_type="text/plain",
        role="stdout",
    )
    stderr = atomic_write_artifact(
        bundle,
        f"{execution.logical_root}/stderr.txt",
        b"",
        media_type="text/plain",
        role="stderr",
    )
    structured = atomic_write_artifact(
        bundle,
        f"{execution.logical_root}/result.json",
        canonical_json_bytes({"status": "synthetic_ok"}),
        media_type="application/json",
        role="structured_result",
    )
    sealed = seal_attempt_manifest(
        bundle,
        request,
        execution,
        [native, stdout, stderr, structured],
        execution_record={
            "started_at_utc": "2026-07-13T00:00:00Z",
            "ended_at_utc": "2026-07-13T00:00:01Z",
            "wall_time_ns": 1,
            "exit_classification": "completed",
            "exit_code": 0,
            "signal": None,
            "timeout": False,
            "device_execution": {
                "mode": "cpu_test_double",
                "gpu_requested": False,
                "gpu_initialized": False,
            },
            "environment": {
                "python_implementation": "CPython",
                "python_version": "3.11.15",
                "platform_system": "Linux",
                "test_runner_version": "pytest-test",
            },
            "runner_version": "p06-generic-test",
        },
        result_record={
            "outcome": "certified",
            "stdout": stdout,
            "stderr": stderr,
            "structured_result": structured,
            "stdout_truncated": False,
            "stderr_truncated": False,
            "redaction": {"applied": False, "fields": []},
            "certificate": None,
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
    return {
        "artifact_root": bundle.root,
        "manifest_ref": sealed["manifest_ref"],
        "initial_branch": initial,
        "branch": branch,
        "p04_request": p04_request,
        "p04_result": p04_result,
    }


def _sage_payload() -> dict:
    return {
        "schema_version": "p05_sage_polynomial_result@1",
        "status": "certified",
        "reason": "Synthetic Sage result.",
        "sage_version": "9.5",
        "domain": "QQ",
        "variable": "x",
        "input_lhs": "(x + 1)**2",
        "input_rhs": "x**2 + 2*x + 1",
        "lhs": "x^2 + 2*x + 1",
        "rhs": "x^2 + 2*x + 1",
        "difference": "0",
        "witness": None,
    }


def _sage_fixture(tmp_path) -> dict:
    target = "(x + 1)**2 = x**2 + 2*x + 1"
    assumptions = [{"id": "domain_x", "kind": "domain", "symbol": "x", "domain": "QQ"}]
    placeholder = SagePolynomialObligation(
        branch_id="placeholder",
        branch_lineage=("placeholder",),
        obligation_digest=hashlib.sha256(target.encode("utf-8")).hexdigest(),
        target=target,
        lhs="(x + 1)**2",
        rhs="x**2 + 2*x + 1",
        variable="x",
        domain="QQ",
    )
    script = generate_sage_polynomial_script(placeholder).decode("ascii")
    initial = build_branch_record(
        obligation_digest=placeholder.obligation_digest,
        target=target,
        typed_assumptions=assumptions,
        generator={"kind": "root"},
        formalization_plan={
            "backend": "sage",
            "action_kind": "backend",
            "native_input": script,
            "timeout_seconds": 1,
        },
        state="ready",
    )
    p04_request = _p04_request(initial, native_input=script, backend="sage")
    adapter_request = build_external_adapter_request(
        branch_id=initial["id"],
        branch_lineage=initial["lineage"],
        obligation_digest=initial["obligation_digest"],
        normalized_target=initial["target"],
        typed_assumptions=assumptions,
        native_input_bytes=script.encode("ascii"),
        native_input_media_type="text/x-python",
        tool_name="sage",
        adapter_version=SAGE_ADAPTER_VERSION,
        backend_version="expected_prefix:9.5",
        requested_executable="/usr/bin/sage",
        resolved_executable="/usr/bin/sage",
        timeout_ms=p04_request["timeout_ms"],
        max_output_bytes=p04_request["max_output_bytes"],
        max_artifact_bytes=p04_request["max_artifact_bytes"],
        expected_result_class="exact_univariate_polynomial_identity_over_QQ",
        backend_role="scoped_specialist_certificate",
        unsupported_conclusions=(
            "no_multivariate_or_nonpolynomial_claim",
            "no_domain_beyond_QQ",
            "no_general_sage_soundness",
            "no_real_document_repair_capability",
            "no_publication",
        ),
    )
    run_root = tmp_path / "sage-run-fixture"
    run_root.mkdir()
    (run_root / "input.py").write_bytes(script.encode("ascii"))
    environment = _execution_environment(run_root, "/usr/bin/sage")
    payload = _sage_payload()
    stdout = (
        SAGE_RESULT_SENTINEL
        + json.dumps(payload, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    raw = {
        "run_root": str(run_root),
        "stdout": stdout,
        "stderr": b"",
        "command": ["/usr/bin/sage", "--python", str(run_root / "input.py")],
        "environment": environment,
        "started_at_utc": "2026-07-13T00:00:00Z",
        "ended_at_utc": "2026-07-13T00:00:01Z",
        "wall_time_ns": 1,
        "exit_code": 0,
        "timed_out": False,
        "truncated": False,
    }
    sealed = _seal_manifest(
        request=adapter_request,
        raw=raw,
        script_bytes=script.encode("ascii"),
        payload=payload,
        status="certified",
        non_claims=list(adapter_request["unsupported_conclusions"]),
    )
    adapter_result = build_external_adapter_result(
        request=adapter_request,
        status="certified",
        reason=payload["reason"],
        execution={
            "kind": "subprocess",
            "runner_id": SAGE_ADAPTER_VERSION,
            "command": raw["command"],
            "executable_path": "/usr/bin/sage",
            "resolved_executable_path": "/usr/bin/sage",
            "exit_code": 0,
            "timed_out": False,
            "stdout_bytes": len(stdout),
            "stderr_bytes": 0,
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stderr_sha256": hashlib.sha256(b"").hexdigest(),
        },
        evidence_kind="sage_polynomial_identity",
        evidence_details=payload,
        output_ref=sealed["manifest_ref"],
        manifest_ref=sealed["manifest_ref"],
        manifest_sha256=sealed["manifest_sha256"],
        manifest_verified=True,
        refutation_witness=None,
        next_discriminator="Inspect the exact registered Sage manifest.",
        non_claims=list(adapter_request["unsupported_conclusions"]),
    )
    receipt = verify_live_adapter_manifest(adapter_result)
    p04_result = _p04_result(
        p04_request,
        test_only=False,
        live_tool_executed=True,
        manifest_verified=True,
        adapter_result_digest=adapter_result["result_digest"],
        live_manifest_verification=receipt,
        output_ref=sealed["manifest_ref"],
    )
    branch = _final_branch(initial, p04_request, p04_result)
    return {
        "manifest_path": run_root / "manifest.json",
        "initial_branch": initial,
        "branch": branch,
        "p04_request": p04_request,
        "p04_result": p04_result,
        "adapter_result": adapter_result,
        "payload": payload,
        "stdout": stdout,
    }


def test_generic_v1_normalizes_only_through_native_reader_and_remains_noncertifying(tmp_path):
    fixture = _generic_fixture(tmp_path)
    normalized = normalize_generic_v1_claim_evidence(
        artifact_root=fixture["artifact_root"],
        manifest_ref=fixture["manifest_ref"],
        p04_branch=fixture["branch"],
        p04_request=fixture["p04_request"],
        p04_result=fixture["p04_result"],
    )
    assert normalized["manifest_version"] == "evidence_manifest@1"
    assert normalized["native_reader"] == "verify_attempt_manifest"
    assert normalized["certifying"] is False
    assert normalized["execution"] == {
        "kind": "cpu_test_double",
        "live_tool_executed": False,
        "test_only": True,
    }


def test_sage_v3_normalizes_only_after_registered_reverification(tmp_path):
    fixture = _sage_fixture(tmp_path)
    normalized = normalize_registered_adapter_claim_evidence(
        adapter_result=fixture["adapter_result"],
        p04_branch=fixture["branch"],
        p04_request=fixture["p04_request"],
        p04_result=fixture["p04_result"],
    )
    assert normalized["manifest_version"] == "p05_sage_execution_manifest@3"
    assert normalized["native_reader"] == "verify_live_adapter_manifest"
    assert normalized["certifying"] is True
    assert normalized["branch"]["id"] == fixture["branch"]["id"]

    fixture["manifest_path"].write_bytes(fixture["manifest_path"].read_bytes() + b"\n")
    with pytest.raises(ExternalAdapterContractError, match="verification failed"):
        normalize_registered_adapter_claim_evidence(
            adapter_result=fixture["adapter_result"],
            p04_branch=fixture["branch"],
            p04_request=fixture["p04_request"],
            p04_result=fixture["p04_result"],
        )


def test_revalidation_request_cannot_be_replaced_by_redigested_json(tmp_path):
    fixture = _sage_fixture(tmp_path)
    handle = reverify_registered_adapter_claim_evidence(
        adapter_result=fixture["adapter_result"],
        p04_branch=fixture["branch"],
        p04_request=fixture["p04_request"],
        p04_result=fixture["p04_result"],
    )
    record = reader_verified_claim_evidence_record(handle)
    forged = deepcopy(record)
    forged["outcome"]["scope"] = "caller-authored scope"
    forged["normalization_digest"] = content_digest(
        {key: forged[key] for key in forged if key != "normalization_digest"}
    )

    with pytest.raises(ExternalAdapterContractError, match="reader authority"):
        reader_verified_claim_evidence_record(forged)

    verified_branch = fixture["branch"]
    ranking = rank_repair_branches(
        [verified_branch],
        claim_evidence_by_branch_id={verified_branch["id"]: handle},
    )
    by_id = {item["branch_id"]: item for item in ranking["rankings"]}
    assert by_id[verified_branch["id"]]["decision_dimensions"]["exact_verified_evidence"] is True


def test_constructing_revalidation_request_does_not_confer_authority(tmp_path):
    fixture = _sage_fixture(tmp_path)
    forged = RevalidatingClaimEvidence(
        reader=P06_REGISTERED_REVALIDATION_READER,
        inputs={
            "adapter_result": fixture["adapter_result"],
            "p04_branch": {**fixture["branch"], "state": "failed"},
            "p04_request": fixture["p04_request"],
            "p04_result": fixture["p04_result"],
        },
    )

    with pytest.raises(ExternalAdapterContractError, match="validated Phase 04 branch"):
        reader_verified_claim_evidence_record(forged)


def test_manifest_mutation_after_request_creation_is_detected(tmp_path):
    fixture = _sage_fixture(tmp_path)
    request = reverify_registered_adapter_claim_evidence(
        adapter_result=fixture["adapter_result"],
        p04_branch=fixture["branch"],
        p04_request=fixture["p04_request"],
        p04_result=fixture["p04_result"],
    )
    fixture["manifest_path"].write_bytes(
        fixture["manifest_path"].read_bytes() + b"\n"
    )

    with pytest.raises(ExternalAdapterContractError, match="verification failed"):
        reader_verified_claim_evidence_record(request)


def test_ranking_rejects_evidence_replay_onto_mutated_same_id_branch(tmp_path):
    fixture = _sage_fixture(tmp_path)
    request = reverify_registered_adapter_claim_evidence(
        adapter_result=fixture["adapter_result"],
        p04_branch=fixture["branch"],
        p04_request=fixture["p04_request"],
        p04_result=fixture["p04_result"],
    )
    mutated = deepcopy(fixture["branch"])
    mutated["blockers"].append(
        {
            "id": "mutated_same_id_blocker",
            "kind": "caller_mutation",
        }
    )
    assert validate_branch_record(mutated) == []
    ranking = rank_repair_branches(
        [mutated],
        claim_evidence_by_branch_id={mutated["id"]: request},
    )

    assert ranking["rankings"][0]["decision_dimensions"]["exact_verified_evidence"] is False


def test_normalized_evidence_binds_exact_redigested_p04_request_and_result(tmp_path):
    fixture = _generic_fixture(tmp_path)
    request = deepcopy(fixture["p04_request"])
    request["target"] = "x = x"
    request = _redigest_request(request)
    result = _p04_result(
        request,
        test_only=True,
        live_tool_executed=False,
        manifest_verified=False,
        adapter_result_digest=None,
        live_manifest_verification=None,
        output_ref="artifact://synthetic/redigested-mutation",
    )
    branch = _final_branch(fixture["initial_branch"], request, result)
    with pytest.raises(ExternalAdapterContractError, match="branch/request identity"):
        normalize_generic_v1_claim_evidence(
            artifact_root=fixture["artifact_root"],
            manifest_ref=fixture["manifest_ref"],
            p04_branch=branch,
            p04_request=request,
            p04_result=result,
        )


def test_caller_authored_verified_receipt_is_rejected(tmp_path):
    fixture = _sage_fixture(tmp_path)
    forged = deepcopy(fixture["p04_result"])
    forged["live_manifest_verification"] = {
        **forged["live_manifest_verification"],
        "manifest_sha256": "0" * 64,
    }
    forged = _redigest_result(forged)
    branch = _final_branch(fixture["initial_branch"], fixture["p04_request"], forged)
    with pytest.raises(ExternalAdapterContractError, match="result evidence mismatch"):
        normalize_registered_adapter_claim_evidence(
            adapter_result=fixture["adapter_result"],
            p04_branch=branch,
            p04_request=fixture["p04_request"],
            p04_result=forged,
        )


def test_unknown_manifest_family_is_diagnostic_only(tmp_path):
    fixture = _generic_fixture(tmp_path)
    normalized = normalize_generic_v1_claim_evidence(
        artifact_root=fixture["artifact_root"],
        manifest_ref=fixture["manifest_ref"],
        p04_branch=fixture["branch"],
        p04_request=fixture["p04_request"],
        p04_result=fixture["p04_result"],
    )
    unknown = deepcopy(normalized)
    unknown["manifest_family"] = "caller_defined_family"
    unknown["normalization_digest"] = content_digest(
        {key: unknown[key] for key in unknown if key != "normalization_digest"}
    )
    with pytest.raises(ExternalAdapterContractError, match="unregistered"):
        validate_normalized_claim_evidence(unknown)


def test_fake_runner_and_legacy_uri_never_normalize_as_certifying(tmp_path):
    fixture = _sage_fixture(tmp_path)
    request = fixture["adapter_result"]["request"]
    fake = build_external_adapter_result(
        request=request,
        status="certified",
        reason="Synthetic fake runner.",
        execution={
            "kind": "fake_runner",
            "runner_id": "injected_sage_runner",
            "command": [],
            "executable_path": None,
            "resolved_executable_path": None,
            "exit_code": None,
            "timed_out": False,
            "stdout_bytes": len(fixture["stdout"]),
            "stderr_bytes": 0,
            "stdout_sha256": hashlib.sha256(fixture["stdout"]).hexdigest(),
            "stderr_sha256": hashlib.sha256(b"").hexdigest(),
        },
        evidence_kind="sage_polynomial_identity",
        evidence_details=fixture["payload"],
        output_ref="mathdevmcp://sage/fake/diagnostic",
        manifest_ref=None,
        manifest_sha256=None,
        manifest_verified=False,
        refutation_witness=None,
        next_discriminator="Run the registered live Sage adapter.",
        non_claims=list(request["unsupported_conclusions"]),
    )
    result = _p04_result(
        fixture["p04_request"],
        test_only=True,
        live_tool_executed=False,
        manifest_verified=False,
        adapter_result_digest=fake["result_digest"],
        live_manifest_verification=None,
        output_ref="mathdevmcp://sage/fake/diagnostic",
    )
    branch = _final_branch(fixture["initial_branch"], fixture["p04_request"], result)
    with pytest.raises(ExternalAdapterContractError, match="requires a promotable live"):
        normalize_registered_adapter_claim_evidence(
            adapter_result=fake,
            p04_branch=branch,
            p04_request=fixture["p04_request"],
            p04_result=result,
        )


def test_missing_p04_bundle_cannot_be_reconstructed_from_sage_manifest(tmp_path):
    fixture = _sage_fixture(tmp_path)
    with pytest.raises(ExternalAdapterContractError, match="validated Phase 04 branch"):
        normalize_registered_adapter_claim_evidence(
            adapter_result=fixture["adapter_result"],
            p04_branch={},
            p04_request={},
            p04_result={},
        )
