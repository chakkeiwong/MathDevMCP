from copy import deepcopy
import hashlib

import pytest

from mathdevmcp.external_adapter_contract import (
    P05_ADAPTER_STATUSES,
    ExternalAdapterContractError,
    build_external_adapter_request,
    build_external_adapter_result,
    p04_injected_result_from_adapter,
    validate_external_adapter_request,
    validate_external_adapter_result,
)


def _request(*, native: bytes = b"x + 1 == 1 + x", assumptions=None, tool="sympy"):
    executable = "/usr/bin/sage" if tool == "sage" else None
    return build_external_adapter_request(
        branch_id="branch_x",
        branch_lineage=("root", "branch_x"),
        obligation_digest=hashlib.sha256(b"x + 1 = 1 + x").hexdigest(),
        normalized_target="x + 1 = 1 + x",
        typed_assumptions=assumptions
        if assumptions is not None
        else [{"id": "x_domain", "kind": "domain", "symbol": "x", "domain": "rational"}],
        native_input_bytes=native,
        native_input_media_type="text/plain",
        tool_name=tool,
        adapter_version="p05-test",
        backend_version="fake-1",
        requested_executable=executable,
        resolved_executable=executable,
        timeout_ms=1_000,
        max_output_bytes=4_096,
        max_artifact_bytes=16_384,
        expected_result_class="synthetic_contract_fixture",
        backend_role="test_only_noncertifying",
        unsupported_conclusions=(
            "no_general_cas_soundness",
            "no_real_document_repair_capability",
            "no_publication",
        ),
    )


def _execution(kind="fake_runner", *, tool="sympy"):
    executable = "/usr/bin/sage" if kind == "subprocess" and tool == "sage" else None
    return {
        "kind": kind,
        "runner_id": "p05-conformance-double",
        "command": [executable, "--nodotsage", "fixture.sage"] if executable else [],
        "executable_path": executable,
        "resolved_executable_path": executable,
        "exit_code": 0 if executable else None,
        "timed_out": False,
        "stdout_bytes": 2,
        "stderr_bytes": 0,
        "stdout_sha256": hashlib.sha256(b"ok").hexdigest(),
        "stderr_sha256": hashlib.sha256(b"").hexdigest(),
    }


def _result(status="diagnostic", *, request=None, execution=None, witness=None):
    request = request or _request()
    return build_external_adapter_result(
        request=request,
        status=status,
        reason=f"Synthetic {status} result.",
        execution=execution or _execution(),
        evidence_kind="counterexample" if status == "refuted" else "diagnostic",
        evidence_details=None,
        output_ref="artifact://fixture/output" if status in {"certified", "refuted"} else None,
        manifest_ref=None,
        manifest_sha256=None,
        manifest_verified=False,
        refutation_witness=witness,
        next_discriminator="Run the exact supported adapter with a verified manifest.",
        non_claims=list(request["unsupported_conclusions"]),
    )


@pytest.mark.parametrize("status", sorted(P05_ADAPTER_STATUSES))
def test_closed_status_matrix_accepts_every_declared_status(status: str) -> None:
    witness = {"assignment": {"x": 0}, "lhs": 1, "rhs": 2} if status == "refuted" else None
    result = _result(status, witness=witness)
    assert result["status"] == status
    assert result["publication_enabled"] is False


def test_unknown_status_is_rejected() -> None:
    with pytest.raises(ExternalAdapterContractError, match="unknown adapter status"):
        _result("mysteriously_good")


def test_request_digest_rejects_assumption_and_native_input_mutation() -> None:
    request = _request()
    assumption_mutation = deepcopy(request)
    assumption_mutation["typed_assumptions"][0]["domain"] = "real"
    native_mutation = deepcopy(request)
    native_mutation["native_input_digest"] = hashlib.sha256(b"x - x").hexdigest()

    with pytest.raises(ExternalAdapterContractError, match="request digest mismatch"):
        validate_external_adapter_request(assumption_mutation)
    with pytest.raises(ExternalAdapterContractError, match="request digest mismatch"):
        validate_external_adapter_request(native_mutation)


def test_result_digest_rejects_status_and_manifest_mutation() -> None:
    result = _result()
    status_mutation = deepcopy(result)
    status_mutation["status"] = "certified"
    manifest_mutation = deepcopy(result)
    manifest_mutation["evidence"]["manifest_verified"] = True
    detail_mutation = deepcopy(result)
    detail_mutation["evidence"]["details"] = {"forged": True}

    with pytest.raises(ExternalAdapterContractError, match="digest mismatch|can_promote"):
        validate_external_adapter_result(status_mutation)
    with pytest.raises(ExternalAdapterContractError, match="requires its reference"):
        validate_external_adapter_result(manifest_mutation)
    with pytest.raises(ExternalAdapterContractError, match="digest mismatch"):
        validate_external_adapter_result(detail_mutation)


def test_fake_runner_cannot_claim_live_execution_or_promotion() -> None:
    result = _result("certified")
    assert result["live_tool_executed"] is False
    assert result["can_promote"] is False

    mutation = deepcopy(result)
    mutation["live_tool_executed"] = True
    mutation["result_digest"] = hashlib.sha256(b"not-authoritative").hexdigest()
    with pytest.raises(ExternalAdapterContractError, match="live_tool_executed"):
        validate_external_adapter_result(mutation)


def test_diagnostic_subprocess_result_never_promotes() -> None:
    request = _request(tool="sage")
    result = _result(
        "diagnostic", request=request, execution=_execution("subprocess", tool="sage")
    )
    assert result["live_tool_executed"] is True
    assert result["can_promote"] is False


def test_subprocess_executable_identity_mismatch_is_rejected() -> None:
    request = _request(tool="sage")
    execution = _execution("subprocess", tool="sage")
    execution["command"][0] = "/bin/false"
    with pytest.raises(ExternalAdapterContractError, match="command executable mismatch"):
        _result("diagnostic", request=request, execution=execution)


def test_unavailable_request_retains_requested_path_without_claiming_resolution(tmp_path) -> None:
    missing = str(tmp_path / "missing-specialist")
    request = build_external_adapter_request(
        branch_id="branch_x",
        branch_lineage=("root", "branch_x"),
        obligation_digest=hashlib.sha256(b"x = x").hexdigest(),
        normalized_target="x = x",
        typed_assumptions=[{"id": "domain_x", "kind": "domain", "symbol": "x", "domain": "rational"}],
        native_input_bytes=b"x == x",
        native_input_media_type="text/plain",
        tool_name="specialist",
        adapter_version="p05-test",
        backend_version="unavailable",
        requested_executable=missing,
        resolved_executable=None,
        timeout_ms=1_000,
        max_output_bytes=4_096,
        max_artifact_bytes=16_384,
        expected_result_class="synthetic_contract_fixture",
        backend_role="test_only_noncertifying",
        unsupported_conclusions=("no_capability_claim", "no_publication"),
    )
    result = _result("unavailable", request=request)
    assert result["request"]["tool"]["requested_executable"] == missing
    assert result["request"]["tool"]["resolved_executable"] is None
    assert result["live_tool_executed"] is False


def test_repeatable_request_and_result_identity() -> None:
    left_request = _request()
    right_request = _request()
    left = _result(request=left_request)
    right = _result(request=right_request)
    assert left_request["request_digest"] == right_request["request_digest"]
    assert left["result_digest"] == right["result_digest"]


def test_negative_outcome_preserves_discriminator_and_nonclaims() -> None:
    for status in sorted(P05_ADAPTER_STATUSES - {"certified", "refuted"}):
        result = _result(status)
        assert result["next_discriminator"]
        assert set(result["request"]["unsupported_conclusions"]) <= set(result["non_claims"])
        assert result["can_promote"] is False


def test_p04_mapping_rejects_parent_sibling_and_native_input_mismatch() -> None:
    request = _request()
    result = _result("certified", request=request)
    exact = {
        "branch_id": "branch_x",
        "branch_lineage": request["branch_lineage"],
        "obligation_digest": request["obligation_digest"],
        "target": request["normalized_target"],
        "request_digest": hashlib.sha256(b"p04-request").hexdigest(),
        "native_input_digest": request["native_input_digest"],
        "typed_assumption_digests": [
            hashlib.sha256(
                b'{"domain":"rational","id":"x_domain","kind":"domain","symbol":"x"}'
            ).hexdigest()
        ],
        "timeout_ms": request["resource_limits"]["timeout_ms"],
        "max_output_bytes": request["resource_limits"]["max_output_bytes"],
        "max_artifact_bytes": request["resource_limits"]["max_artifact_bytes"],
    }
    mapped = p04_injected_result_from_adapter(result, exact)
    assert mapped["branch_id"] == "branch_x"
    assert mapped["status"] == "proved"
    assert mapped["test_only"] is True

    sibling = {**exact, "branch_id": "branch_y"}
    parent = {**exact, "branch_id": "root"}
    wrong_native = {
        **exact,
        "native_input_digest": hashlib.sha256(b"different").hexdigest(),
    }
    wrong_assumptions = {**exact, "typed_assumption_digests": []}
    wrong_target = {**exact, "target": "different target"}
    wrong_limits = {**exact, "max_output_bytes": 1}
    with pytest.raises(ExternalAdapterContractError, match="branch binding"):
        p04_injected_result_from_adapter(result, sibling)
    with pytest.raises(ExternalAdapterContractError, match="branch binding"):
        p04_injected_result_from_adapter(result, parent)
    with pytest.raises(ExternalAdapterContractError, match="native-input binding"):
        p04_injected_result_from_adapter(result, wrong_native)
    with pytest.raises(ExternalAdapterContractError, match="typed-assumption binding"):
        p04_injected_result_from_adapter(result, wrong_assumptions)
    with pytest.raises(ExternalAdapterContractError, match="target binding"):
        p04_injected_result_from_adapter(result, wrong_target)
    with pytest.raises(ExternalAdapterContractError, match="output-limit binding"):
        p04_injected_result_from_adapter(result, wrong_limits)
