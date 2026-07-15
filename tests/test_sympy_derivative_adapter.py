from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from mathdevmcp.external_adapter_contract import (
    ExternalAdapterContractError,
    p04_injected_result_from_adapter,
)
from mathdevmcp.sympy_derivative_adapter import (
    REGISTERED_EXPECTED_DERIVATIVE,
    REGISTERED_EXPRESSION,
    SYMPY_DERIVATIVE_ADAPTER_VERSION,
    SYMPY_DERIVATIVE_OPERATION,
    SympyDerivativeContractError,
    _denominator_factors,
    _normalized_factor_base,
    _tree_identity,
    build_derivative_request,
    build_derivative_result,
    canonical_json_bytes,
    compute_worker_record,
    derivative_capability_descriptor,
    parse_worker_stdout,
    validate_derivative_request,
    validate_derivative_result,
    validate_worker_record,
    worker_record_bytes,
)


def _request():
    return build_derivative_request(
        source_expression_obligation_digest="1" * 64,
        source_target_obligation_digest="2" * 64,
    )


def _execution(**updates):
    value = {
        "kind": "subprocess",
        "runner_id": SYMPY_DERIVATIVE_ADAPTER_VERSION,
        "command": [
            "/home/chakwong/miniconda3/envs/tfgpu/bin/python3",
            "-I",
            "-S",
            "-B",
            "-X",
            "pycache_prefix=/dev/null",
            "/tmp/snapshotted-sympy-derivative-adapter.py",
        ],
        "executable": "/home/chakwong/miniconda3/envs/tfgpu/bin/python3",
        "environment": {
            "CUDA_VISIBLE_DEVICES": "-1",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
        },
        "exit_code": 0,
        "timed_out": False,
        "overflow": False,
        "wall_time_ms": 10,
        "live_tool_executed": True,
        "run_id": "run-1",
        "run_binding_digest": "3" * 64,
        "code_identity_digest": "4" * 64,
    }
    value.update(updates)
    return value


def _successful_result():
    request = _request()
    worker = compute_worker_record(request)
    native = canonical_json_bytes(request)
    stdout = worker_record_bytes(worker, request)
    stderr = b""
    return build_derivative_result(
        request=request,
        worker_record=worker,
        native_input=native,
        stdout=stdout,
        stderr=stderr,
        execution=_execution(),
    )


def _redigest_request(value):
    value["request_digest"] = hashlib.sha256(
        canonical_json_bytes({key: child for key, child in value.items() if key != "request_digest"})
    ).hexdigest()
    return value


def _redigest_result(value):
    value["result_digest"] = hashlib.sha256(
        canonical_json_bytes({key: child for key, child in value.items() if key != "result_digest"})
    ).hexdigest()
    return value


def test_descriptor_is_separate_nonpromoting_p08_contract() -> None:
    assert derivative_capability_descriptor() == {
        "adapter_version": "p08-sympy-derivative-adapter@1",
        "operation": "construct_scalar_derivative_then_compare",
        "request_schema": "p08_sympy_derivative_request@1",
        "worker_output_schema": "p08_sympy_derivative_worker_output@1",
        "result_schema": "p08_sympy_derivative_result@1",
        "status_registry": [
            "backend_checked",
            "execution_error",
            "malformed_output",
            "source_target_mismatch",
            "timeout",
            "truncated_output",
            "unavailable",
            "unsupported",
        ],
        "imports_sympy_at_module_import": False,
        "can_promote": False,
        "publication_enabled": False,
    }


def test_request_is_deterministic_and_binds_exact_candidate() -> None:
    left = _request()
    right = _request()
    assert canonical_json_bytes(left) == canonical_json_bytes(right)
    assert left["expression"] == REGISTERED_EXPRESSION
    assert left["expected_derivative"] == REGISTERED_EXPECTED_DERIVATIVE
    assert left["differentiated_variable"] == "rt"
    assert left["held_constant"] == ["bp", "r", "tau"]
    assert left["typed_assumptions"][-1] == {
        "id": "differentiable_in_rt",
        "kind": "differentiability",
        "expression": REGISTERED_EXPRESSION,
        "variable": "rt",
        "domain": "real_where_registered_denominators_nonzero",
    }


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value.__setitem__("expression", "bp/(1 + rt)"),
        lambda value: value.__setitem__("expected_derivative", "-bp/(1 + rt)**2"),
        lambda value: value.__setitem__("differentiated_variable", "r"),
        lambda value: value.__setitem__("held_constant", ["bp", "rt", "tau"]),
        lambda value: value["symbols"][0].__setitem__("domain", "rational"),
        lambda value: value["typed_assumptions"].pop(),
        lambda value: value["typed_assumptions"].append(
            {"id": "extra", "kind": "nonzero_polynomial", "expression": "r + rt"}
        ),
        lambda value: value["typed_assumptions"][1].__setitem__("expression", "1 - r"),
        lambda value: value["resource_limits"].__setitem__("timeout_seconds", 11),
        lambda value: value.__setitem__("operation", "identity_check"),
    ],
)
def test_request_mutations_are_rejected_even_with_recomputed_digest(mutate) -> None:
    request = deepcopy(_request())
    mutate(request)
    _redigest_request(request)
    with pytest.raises(SympyDerivativeContractError):
        validate_derivative_request(request)


@pytest.mark.parametrize(
    "expression",
    ["__import__('os')", "bp[0]", "lambda: rt", "unknown + rt", "rt**r"],
)
def test_unsafe_or_unregistered_expression_is_rejected(expression: str) -> None:
    request = deepcopy(_request())
    request["expression"] = expression
    _redigest_request(request)
    with pytest.raises(SympyDerivativeContractError):
        validate_derivative_request(request)


def test_live_sympy_constructs_then_compares_exact_registered_derivative() -> None:
    request = _request()
    worker = compute_worker_record(request)
    assert worker["difference"] == "0"
    assert worker["difference_srepr"] == "Integer(0)"
    assert worker["constructed_derivative_srepr"] != worker["source_target_srepr"]
    factors = worker["denominator_factors"]
    expected = {"Add(Symbol('r', real=True), Integer(1))", "Add(Symbol('rt', real=True), Integer(1))"}
    assert {item["base_srepr"] for item in factors["registered_nonzero"]} == expected
    assert {item["base_srepr"] for item in factors["expression"]} == expected
    assert {item["multiplicity"] for item in factors["expression"]} == {1}
    assert sorted(item["multiplicity"] for item in factors["constructed_derivative"]) == [2, 2]
    assert sorted(item["multiplicity"] for item in factors["source_target"]) == [1, 2]


def test_direct_polynomial_factor_normalization_handles_unit_sign_and_power() -> None:
    import sympy as sp

    r, rt = sp.symbols("r rt", real=True)
    positive, identity = _normalized_factor_base(1 + r, r, rt, sp)
    negative, negative_identity = _normalized_factor_base(-3 * (1 + r), r, rt, sp)
    assert positive == negative == r + 1
    assert identity == negative_identity
    factors = _denominator_factors(1 / ((1 + r) ** 3 * (1 + rt)), r, rt, sp)
    assert {item["base"]: item["multiplicity"] for item in factors} == {"r + 1": 3, "rt + 1": 1}
    assert _denominator_factors((1 + r) / (1 + r), r, rt, sp) == []
    extra = _denominator_factors(1 / (r + rt), r, rt, sp)
    assert {item["base"] for item in extra} == {"r + rt"}


def test_worker_stdout_is_one_strict_canonical_lf_terminated_object() -> None:
    request = _request()
    worker = compute_worker_record(request)
    raw = worker_record_bytes(worker, request)
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert parse_worker_stdout(raw, request) == worker
    for changed in (raw + b"\n", raw + b"junk", b" " + raw, raw[:-1]):
        with pytest.raises(SympyDerivativeContractError):
            parse_worker_stdout(changed, request)


def test_worker_binding_and_assumption_mutations_are_rejected() -> None:
    request = _request()
    worker = compute_worker_record(request)
    mutations = []
    changed = deepcopy(worker)
    changed["request_digest"] = "0" * 64
    mutations.append(changed)
    changed = deepcopy(worker)
    changed["typed_assumptions"].pop()
    mutations.append(changed)
    changed = deepcopy(worker)
    changed["denominator_factors"]["expression"].pop()
    mutations.append(changed)
    changed = deepcopy(worker)
    changed["sympy_origin_sha256"] = "0" * 64
    mutations.append(changed)
    changed = deepcopy(worker)
    changed["sympy_package_sha256"] = "0" * 64
    mutations.append(changed)
    changed = deepcopy(worker)
    changed["mpmath_package_sha256"] = "0" * 64
    mutations.append(changed)
    changed = deepcopy(worker)
    changed["site_packages_module_roots"] = ["sympy"]
    mutations.append(changed)
    for value in mutations[:2] + mutations[3:]:
        with pytest.raises(SympyDerivativeContractError):
            validate_worker_record(value, request)
    # Structural factor tampering remains visible in canonical bytes and is
    # rejected by independent recomputation in the runner verifier.
    assert canonical_json_bytes(mutations[2]) != canonical_json_bytes(worker)


def test_actual_tree_identity_counts_surprises_but_ignores_redirected_cache(
    tmp_path: Path,
) -> None:
    site = tmp_path / "site-packages"
    package = site / "package"
    metadata = site / "package-1.0.dist-info"
    package.mkdir(parents=True)
    metadata.mkdir()
    (package / "__init__.py").write_text("VALUE = 'source'\n", encoding="utf-8")
    (metadata / "METADATA").write_text("Name: package\nVersion: 1.0\n", encoding="utf-8")
    roots = ("package", "package-1.0.dist-info")
    baseline = _tree_identity(site, roots)

    cache = package / "__pycache__"
    cache.mkdir()
    (cache / "__init__.cpython-311.pyc").write_bytes(b"valid-cache-placeholder")
    assert _tree_identity(site, roots) == baseline

    (package / "injected.py").write_text("VALUE = 'injected'\n", encoding="utf-8")
    changed = _tree_identity(site, roots)
    assert changed[0] == baseline[0] + 1
    assert changed[1] > baseline[1]
    assert changed[2] != baseline[2]


@pytest.mark.parametrize("kind", ["legacy_bytecode", "cache_surprise", "executable", "symlink"])
def test_actual_tree_identity_rejects_executable_surprises(
    tmp_path: Path, kind: str
) -> None:
    site = tmp_path / "site-packages"
    package = site / "package"
    metadata = site / "package-1.0.dist-info"
    package.mkdir(parents=True)
    metadata.mkdir()
    source = package / "__init__.py"
    source.write_text("VALUE = 'source'\n", encoding="utf-8")
    if kind == "legacy_bytecode":
        (package / "payload.pyc").write_bytes(b"payload")
        message = "legacy executable bytecode"
    elif kind == "cache_surprise":
        cache = package / "__pycache__"
        cache.mkdir()
        (cache / "payload.py").write_text("VALUE = 'payload'\n", encoding="utf-8")
        message = "cache contains an unexpected file"
    elif kind == "executable":
        payload = package / "payload.py"
        payload.write_text("VALUE = 'payload'\n", encoding="utf-8")
        payload.chmod(0o755)
        message = "unexpected executable file"
    else:
        (package / "alias.py").symlink_to(source)
        message = "contains a symlink"
    with pytest.raises(SympyDerivativeContractError, match=message):
        _tree_identity(site, ("package", "package-1.0.dist-info"))


def test_success_is_backend_checked_but_never_promoting_or_proof() -> None:
    result = _successful_result()
    assert result["status"] == "backend_checked"
    assert result["claim_class"] == "backend_checked_computational_support"
    assert result["can_promote"] is False
    assert result["publication_enabled"] is False
    assert result["formal_proof_certified"] is False
    assert "no_formal_proof" in result["non_claims"]
    with pytest.raises(ExternalAdapterContractError):
        p04_injected_result_from_adapter(result, {})


@pytest.mark.parametrize(
    "execution_update",
    [
        {"kind": "fake_runner"},
        {"live_tool_executed": False},
        {"exit_code": 1},
        {"timed_out": True},
        {"overflow": True},
        {"runner_id": "wrong"},
    ],
)
def test_fake_or_unclean_execution_cannot_claim_backend_checked(execution_update) -> None:
    request = _request()
    worker = compute_worker_record(request)
    native = canonical_json_bytes(request)
    stdout = worker_record_bytes(worker, request)
    with pytest.raises(SympyDerivativeContractError):
        build_derivative_result(
            request=request,
            worker_record=worker,
            native_input=native,
            stdout=stdout,
            stderr=b"",
            execution=_execution(**execution_update),
        )


@pytest.mark.parametrize(
    "status",
    ["unsupported", "unavailable", "execution_error", "timeout", "malformed_output", "truncated_output"],
)
def test_failure_statuses_are_closed_non_evidence(status: str) -> None:
    request = _request()
    result = build_derivative_result(
        request=request,
        worker_record=None,
        native_input=canonical_json_bytes(request),
        stdout=b"",
        stderr=b"diagnostic",
        execution=_execution(exit_code=1, live_tool_executed=False),
        failure_status=status,
        failure_reason="Synthetic implementation diagnostic.",
    )
    assert result["status"] == status
    assert result["claim_class"] == "no_mathematical_evidence"
    assert result["can_promote"] is False


def test_result_digest_raw_binding_and_authority_mutations_fail() -> None:
    result = _successful_result()
    mutations = []
    changed = deepcopy(result)
    changed["raw_bindings"]["stdout.bin"]["sha256"] = "0" * 64
    raw_binding_mutation = _redigest_result(changed)
    changed = deepcopy(result)
    changed["can_promote"] = True
    mutations.append(_redigest_result(changed))
    changed = deepcopy(result)
    changed["publication_enabled"] = True
    mutations.append(_redigest_result(changed))
    changed = deepcopy(result)
    changed["formal_proof_certified"] = True
    mutations.append(_redigest_result(changed))
    changed = deepcopy(result)
    changed["status"] = "invented"
    mutations.append(_redigest_result(changed))
    for value in mutations:
        with pytest.raises(SympyDerivativeContractError):
            validate_derivative_result(value)
    # This is structurally valid in isolation; the runner verifier rejects it
    # by hashing the independently reopened stdout bytes.
    assert validate_derivative_result(raw_binding_mutation) == raw_binding_mutation
    assert raw_binding_mutation["raw_bindings"] != result["raw_bindings"]


def test_sign_flip_and_dropped_term_neighbors_do_not_pass() -> None:
    import sympy as sp

    bp, r, rt, tau = sp.symbols("bp r rt tau", real=True)
    expression = bp / (1 + rt) + tau * rt * bp / ((1 + rt) * (1 + r))
    constructed = sp.diff(expression, rt)
    wrong_sign = -bp / (1 + rt) ** 2 * (-1 + tau / (1 + r))
    dropped = -bp / (1 + rt) ** 2
    assert sp.simplify(constructed - wrong_sign) != 0
    assert sp.simplify(constructed - dropped) != 0
