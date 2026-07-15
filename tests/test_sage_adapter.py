import hashlib
import json
import os
from pathlib import Path

import pytest

import mathdevmcp.sage_adapter as sage_adapter
from mathdevmcp.external_adapter_contract import p04_injected_result_from_adapter
from mathdevmcp.evidence_manifest import content_digest
from mathdevmcp.sage_adapter import (
    SAGE_ADAPTER_VERSION,
    SAGE_MAX_MANIFEST_BYTES,
    SAGE_MANIFEST_SCHEMA,
    SAGE_RESULT_SENTINEL,
    SageAdapterError,
    SagePolynomialObligation,
    _canonical_bytes,
    _execution_environment,
    _seal_manifest,
    generate_sage_polynomial_script,
    run_sage_polynomial_obligation,
    verify_sage_execution_manifest,
)


def _obligation(lhs="(x + 1)**2", rhs="x**2 + 2*x + 1", *, domain="QQ"):
    target = f"{lhs} = {rhs}"
    return SagePolynomialObligation(
        branch_id="branch_sage",
        branch_lineage=("root", "branch_sage"),
        obligation_digest=hashlib.sha256(target.encode()).hexdigest(),
        target=target,
        lhs=lhs,
        rhs=rhs,
        variable="x",
        domain=domain,
    )


def _stdout(
    status="certified",
    *,
    witness=None,
    difference="0",
    version="9.5",
    input_lhs="(x + 1)**2",
    input_rhs="x**2 + 2*x + 1",
):
    payload = {
        "schema_version": "p05_sage_polynomial_result@1",
        "status": status,
        "reason": "Synthetic Sage result.",
        "sage_version": version,
        "domain": "QQ",
        "variable": "x",
        "input_lhs": input_lhs,
        "input_rhs": input_rhs,
        "lhs": "x^2 + 2*x + 1",
        "rhs": "x^2 + 2*x + 1" if status == "certified" else "x^2",
        "difference": difference,
        "witness": witness,
    }
    return (SAGE_RESULT_SENTINEL + json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _runner(stdout=None, **updates):
    value = {
        "stdout": _stdout() if stdout is None else stdout,
        "stderr": b"",
        "exit_code": 0,
        "timed_out": False,
        "truncated": False,
        "runner_error": None,
    }
    value.update(updates)
    return lambda **kwargs: value


def test_generated_script_constructs_polynomial_ring_over_qq() -> None:
    script = generate_sage_polynomial_script(_obligation()).decode("ascii")
    compile(script, "input.py", "exec")
    assert "PolynomialRing(QQ" in script
    assert "lhs = R(" in script and "rhs = R(" in script
    assert "eval(" not in script and "sage_eval" not in script
    assert SAGE_RESULT_SENTINEL in script


def test_script_and_request_identity_are_deterministic() -> None:
    obligation = _obligation()
    assert generate_sage_polynomial_script(obligation) == generate_sage_polynomial_script(obligation)
    left = run_sage_polynomial_obligation(obligation, executable="/usr/bin/sage", runner=_runner())
    right = run_sage_polynomial_obligation(obligation, executable="/usr/bin/sage", runner=_runner())
    assert left["request"]["request_digest"] == right["request"]["request_digest"]


def test_fake_positive_is_not_live_or_promotable() -> None:
    result = run_sage_polynomial_obligation(
        _obligation(), executable="/usr/bin/sage", runner=_runner()
    )
    assert result["status"] == "certified"
    assert result["execution"]["kind"] == "fake_runner"
    assert result["live_tool_executed"] is False
    assert result["can_promote"] is False
    assert result["evidence"]["manifest_verified"] is False


def test_fake_refutation_requires_concrete_unequal_evaluation() -> None:
    witness = {"assignment": {"x": "1"}, "lhs": "2", "rhs": "1"}
    result = run_sage_polynomial_obligation(
        _obligation("x + 1", "x"),
        executable="/usr/bin/sage",
        runner=_runner(
            _stdout(
                "refuted",
                witness=witness,
                difference="1",
                input_lhs="x + 1",
                input_rhs="x",
            )
        ),
    )
    assert result["status"] == "refuted"
    assert result["evidence"]["refutation_witness"] == witness
    assert result["can_promote"] is False


@pytest.mark.parametrize(
    ("stdout", "expected"),
    [
        (b"", "malformed_output"),
        (b"extra\n" + _stdout(), "malformed_output"),
        (SAGE_RESULT_SENTINEL.encode() + b"{bad}\n", "malformed_output"),
        (_stdout(version="10.0"), "malformed_output"),
        (_stdout("refuted", witness=None, difference="x"), "malformed_output"),
        (
            _stdout(
                "refuted",
                witness={"assignment": {"x": "0"}, "lhs": "1", "rhs": "1"},
                difference="1",
            ),
            "malformed_output",
        ),
    ],
)
def test_malformed_or_unexpected_output_is_rejected(stdout, expected) -> None:
    result = run_sage_polynomial_obligation(
        _obligation(), executable="/usr/bin/sage", runner=_runner(stdout)
    )
    assert result["status"] == expected
    assert result["can_promote"] is False


@pytest.mark.parametrize(
    ("runner", "status"),
    [
        (_runner(timed_out=True), "timeout"),
        (_runner(exit_code=2), "execution_error"),
        (_runner(runner_error="OSError: failed"), "execution_error"),
        (_runner(stdout=b"x" * 65, truncated=True), "truncated_output"),
        (lambda **kwargs: ["not", "a", "mapping"], "malformed_output"),
    ],
)
def test_fake_process_failures_are_closed_nonmathematical_statuses(runner, status) -> None:
    result = run_sage_polynomial_obligation(
        _obligation(),
        executable="/usr/bin/sage",
        max_output_bytes=4096,
        runner=runner,
    )
    assert result["status"] == status
    assert result["can_promote"] is False


def test_live_launch_failure_is_not_labeled_as_executed(tmp_path, monkeypatch) -> None:
    executable = tmp_path / "sage"
    executable.write_bytes(b"#!/bin/sh\nexit 0\n")
    executable.chmod(0o700)

    monkeypatch.setattr(
        sage_adapter,
        "_default_runner",
        lambda **kwargs: {
            "runner_error": "OSError: exec failed",
            "timed_out": False,
            "stdout": b"",
            "stderr": b"exec failed",
            "exit_code": None,
        },
    )
    result = run_sage_polynomial_obligation(
        _obligation(),
        executable=str(executable),
        artifact_root=tmp_path / "artifacts",
    )

    assert result["status"] == "execution_error"
    assert result["execution"]["kind"] == "not_run"
    assert result["live_tool_executed"] is False
    assert result["can_promote"] is False


@pytest.mark.parametrize(
    "obligation",
    [
        _obligation(domain="ZZ"),
        _obligation("x/(x + 1)", "1"),
        _obligation("x**-1", "1"),
        _obligation("x**65", "x"),
        _obligation(str(2**300), "1"),
        _obligation("sin(x)", "x"),
    ],
)
def test_out_of_scope_polynomial_inputs_do_not_execute(obligation) -> None:
    called = False

    def runner(**kwargs):
        nonlocal called
        called = True
        return _runner()(**kwargs)

    result = run_sage_polynomial_obligation(
        obligation, executable="/usr/bin/sage", runner=runner
    )
    assert result["status"] == "unsupported"
    assert result["live_tool_executed"] is False
    assert called is False


def test_sage_target_must_exactly_match_encoded_sides() -> None:
    obligation = _obligation()
    changed = SagePolynomialObligation(
        **{**obligation.__dict__, "target": "x = x"}
    )
    called = False

    def runner(**kwargs):
        nonlocal called
        called = True
        return _runner()(**kwargs)

    result = run_sage_polynomial_obligation(
        changed, executable="/usr/bin/sage", runner=runner
    )
    assert result["status"] == "unsupported"
    assert called is False


def test_unavailable_path_is_diagnostic_and_not_executed(tmp_path) -> None:
    result = run_sage_polynomial_obligation(
        _obligation(), executable=str(tmp_path / "missing-sage"), runner=_runner()
    )
    assert result["status"] == "unavailable"
    assert result["live_tool_executed"] is False


def test_runner_observes_exact_script_command_and_limits() -> None:
    observed = {}

    def runner(**kwargs):
        observed.update(kwargs)
        return _runner()(**kwargs)

    result = run_sage_polynomial_obligation(
        _obligation(),
        executable="/usr/bin/sage",
        timeout_seconds=2.5,
        max_output_bytes=1234,
        runner=runner,
    )
    assert result["status"] == "certified"
    assert observed["command"] == ["/usr/bin/sage", "--python", "<script.py>"]
    assert observed["timeout_seconds"] == 2.5
    assert observed["max_output_bytes"] == 1234
    assert hashlib.sha256(observed["script_bytes"]).hexdigest() == result["request"]["native_input_digest"]
    assert result["request"]["native_input_media_type"] == "text/x-python"
    assert result["request"]["tool"]["adapter_version"] == SAGE_ADAPTER_VERSION


def test_generated_script_stops_before_polynomial_action_on_version_drift() -> None:
    script = generate_sage_polynomial_script(
        _obligation(), expected_version_prefix="expected-family"
    ).decode("ascii")
    version_guard = script.index("if not str(sage_version).startswith")
    algebra_import = script.index("from sage.all import PolynomialRing, QQ")
    ring_construction = script.index("R = PolynomialRing")
    assert version_guard < algebra_import < ring_construction
    assert "polynomial action was not run" in script


def test_fake_result_maps_only_to_exact_p04_request() -> None:
    result = run_sage_polynomial_obligation(
        _obligation(), executable="/usr/bin/sage", runner=_runner()
    )
    exact = {
        "branch_id": "branch_sage",
        "branch_lineage": result["request"]["branch_lineage"],
        "obligation_digest": result["request"]["obligation_digest"],
        "target": result["request"]["normalized_target"],
        "request_digest": hashlib.sha256(b"p04").hexdigest(),
        "native_input_digest": result["request"]["native_input_digest"],
        "typed_assumption_digests": [
            content_digest(item) for item in result["request"]["typed_assumptions"]
        ],
        "timeout_ms": result["request"]["resource_limits"]["timeout_ms"],
        "max_output_bytes": result["request"]["resource_limits"]["max_output_bytes"],
        "max_artifact_bytes": result["request"]["resource_limits"]["max_artifact_bytes"],
    }
    mapped = p04_injected_result_from_adapter(result, exact)
    assert mapped["branch_id"] == "branch_sage"
    assert mapped["status"] == "proved"
    assert mapped["test_only"] is True


def test_fake_process_provenance_cannot_make_result_live() -> None:
    def deceptive(**kwargs):
        return {
            **_runner()(**kwargs),
            "command": ["/usr/bin/sage", "input.py"],
            "run_root": "/tmp/fake",
        }

    result = run_sage_polynomial_obligation(
        _obligation(), executable="/usr/bin/sage", runner=deceptive
    )
    assert result["status"] == "certified"
    assert result["live_tool_executed"] is False
    assert result["evidence"]["manifest_verified"] is False


def _synthetic_sealed_manifest(tmp_path: Path, *, with_scratch: bool = False) -> Path:
    obligation = _obligation()
    script = generate_sage_polynomial_script(obligation)
    request = run_sage_polynomial_obligation(
        obligation, executable="/usr/bin/sage", runner=_runner()
    )["request"]
    run_root = tmp_path / "sage-run-fixture"
    run_root.mkdir(parents=True)
    (run_root / "input.py").write_bytes(script)
    environment = _execution_environment(run_root, "/usr/bin/sage")
    if with_scratch:
        cache = run_root / "dot-sage" / "cache"
        cache.mkdir()
        (cache / "lazy-import.pickle").write_bytes(b"cache")
        r_config = run_root / "dot-sage" / "R"
        r_config.mkdir()
        (r_config / "Makevars.user").write_bytes(b"CFLAGS=-O2\n")
        (run_root / "dot-sage" / "db").mkdir()
        (run_root / "dot-sage" / "matplotlib-1.5.1").mkdir()
        (run_root / "dot-sage" / "temp" / "test-host").mkdir(parents=True)
    stdout = _stdout()
    payload = json.loads(stdout.decode().removeprefix(SAGE_RESULT_SENTINEL))
    _seal_manifest(
        request=request,
        raw={
            "run_root": str(run_root),
            "stdout": stdout,
            "stderr": b"",
            "command": ["/usr/bin/sage", "--python", str(run_root / "input.py")],
            "environment": environment,
            "started_at_utc": "2026-07-13T00:00:00Z",
            "ended_at_utc": "2026-07-13T00:00:01Z",
            "wall_time_ns": 1_000_000_000,
            "exit_code": 0,
            "timed_out": False,
            "truncated": False,
        },
        script_bytes=script,
        payload=payload,
        status="certified",
        non_claims=list(request["unsupported_conclusions"]),
    )
    return run_root / "manifest.json"


def _rewrite_manifest(path: Path, mutation) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    mutation(value)
    value.pop("manifest_digest")
    value["manifest_digest"] = hashlib.sha256(_canonical_bytes(value)).hexdigest()
    path.write_bytes(_canonical_bytes(value))


def _rewrite_payload_and_refresh_manifest(path: Path, mutation) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    result_path = path.parent / "result.json"
    payload = json.loads(result_path.read_text(encoding="utf-8"))
    mutation(payload)
    result_bytes = _canonical_bytes(payload)
    stdout_bytes = (
        SAGE_RESULT_SENTINEL.encode("ascii") + result_bytes + b"\n"
    )
    result_path.write_bytes(result_bytes)
    (path.parent / "stdout.bin").write_bytes(stdout_bytes)
    rewritten = {"result.json": result_bytes, "stdout.bin": stdout_bytes}
    for artifact in value["artifacts"]:
        if artifact["path"] in rewritten:
            data = rewritten[artifact["path"]]
            artifact["byte_count"] = len(data)
            artifact["sha256"] = hashlib.sha256(data).hexdigest()
    value["result"]["payload_sha256"] = hashlib.sha256(result_bytes).hexdigest()
    value.pop("manifest_digest")
    value["manifest_digest"] = hashlib.sha256(_canonical_bytes(value)).hexdigest()
    path.write_bytes(_canonical_bytes(value))


def _rewrite_script_request_and_refresh_manifest(path: Path, script: bytes) -> None:
    value = json.loads(path.read_text(encoding="utf-8"))
    (path.parent / "input.py").write_bytes(script)
    for artifact in value["artifacts"]:
        if artifact["path"] == "input.py":
            artifact["byte_count"] = len(script)
            artifact["sha256"] = hashlib.sha256(script).hexdigest()
    request = value["request"]
    request["native_input_digest"] = hashlib.sha256(script).hexdigest()
    request.pop("request_digest")
    request["request_digest"] = content_digest(request)
    value["request_digest"] = request["request_digest"]
    value.pop("manifest_digest")
    value["manifest_digest"] = hashlib.sha256(_canonical_bytes(value)).hexdigest()
    path.write_bytes(_canonical_bytes(value))


def test_synthetic_sealed_manifest_passes_full_semantic_verification(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    verified = verify_sage_execution_manifest(path)
    assert verified["integrity_state"] == "verified"
    assert verified["payload"]["status"] == "certified"
    assert verified["manifest"]["schema_version"] == SAGE_MANIFEST_SCHEMA
    assert verified["manifest"]["command"][1] == "--python"
    assert set(verified["artifact_digests"]) == {
        "input.py",
        "stdout.bin",
        "stderr.bin",
        "result.json",
    }
    assert [item["path"] for item in verified["scratch_inventory"]] == [
        "dot-sage",
        "home",
        "tmp",
    ]
    assert verified["encoded_assumption_digests"] == [
        content_digest(verified["manifest"]["request"]["typed_assumptions"][0])
    ]
    assert verified["assumption_encoding_evidence_refs"]


def test_manifest_rejects_redigested_noncanonical_sage_script(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    _rewrite_script_request_and_refresh_manifest(
        path,
        b"# caller-authored script with refreshed outer hashes\n",
    )

    with pytest.raises(SageAdapterError, match="deterministic encoding"):
        verify_sage_execution_manifest(path)


def test_manifest_records_and_verifies_bounded_runtime_scratch(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path, with_scratch=True)
    verified = verify_sage_execution_manifest(path)

    inventory = {item["path"]: item for item in verified["scratch_inventory"]}
    assert set(inventory) == {
        "dot-sage",
        "dot-sage/R",
        "dot-sage/R/Makevars.user",
        "dot-sage/cache",
        "dot-sage/cache/lazy-import.pickle",
        "dot-sage/db",
        "dot-sage/matplotlib-1.5.1",
        "dot-sage/temp",
        "dot-sage/temp/test-host",
        "home",
        "tmp",
    }
    assert inventory["dot-sage/cache/lazy-import.pickle"] == {
        "path": "dot-sage/cache/lazy-import.pickle",
        "kind": "file",
        "mode": 0o644,
        "byte_count": 5,
        "sha256": hashlib.sha256(b"cache").hexdigest(),
    }
    assert inventory["dot-sage/R/Makevars.user"]["sha256"] == hashlib.sha256(
        b"CFLAGS=-O2\n"
    ).hexdigest()
    assert verified["manifest"]["scratch"]["file_bytes"] == 16


def test_live_artifact_budget_and_aggregate_output_are_bound_before_execution() -> None:
    aggregate = run_sage_polynomial_obligation(
        _obligation(),
        executable="/usr/bin/sage",
        max_output_bytes=10,
        runner=_runner(stdout=b"123456", stderr=b"123456"),
    )
    assert aggregate["status"] == "truncated_output"
    assert aggregate["can_promote"] is False


def test_live_manifest_sealing_failure_preserves_process_provenance(
    tmp_path, monkeypatch
) -> None:
    executable = tmp_path / "sage"
    executable.write_bytes(b"#!/bin/sh\nexit 0\n")
    executable.chmod(0o700)

    def completed_runner(
        *, executable, script_bytes, timeout_seconds, max_output_bytes, artifact_root
    ):
        del timeout_seconds, max_output_bytes
        artifact_root.mkdir(parents=True)
        run_root = artifact_root / "sage-run-fixture"
        run_root.mkdir()
        script_path = run_root / "input.py"
        script_path.write_bytes(script_bytes)
        environment = _execution_environment(run_root, executable)
        (run_root / "unexpected.bin").write_bytes(b"invalid closed inventory")
        return {
            "started_at_utc": "2026-07-13T00:00:00Z",
            "ended_at_utc": "2026-07-13T00:00:01Z",
            "wall_time_ns": 1_000_000_000,
            "exit_code": 0,
            "timed_out": False,
            "truncated": False,
            "stdout": _stdout(),
            "stderr": b"",
            "runner_error": None,
            "command": [executable, "--python", str(script_path)],
            "environment": environment,
            "run_root": str(run_root),
        }

    monkeypatch.setattr(sage_adapter, "_default_runner", completed_runner)
    result = run_sage_polynomial_obligation(
        _obligation(),
        executable=str(executable),
        artifact_root=tmp_path / "artifacts",
    )

    assert result["status"] == "execution_error"
    assert result["execution"]["kind"] == "subprocess"
    assert result["execution"]["exit_code"] == 0
    assert result["live_tool_executed"] is True
    assert result["evidence"]["manifest_verified"] is False
    assert result["can_promote"] is False
    assert "manifest could not be sealed and verified" in result["reason"]


def test_manifest_rejects_unexpected_run_root_file_and_tiny_artifact_budget(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    (path.parent / "unexpected.bin").write_bytes(b"x")
    with pytest.raises(SageAdapterError, match="layout"):
        verify_sage_execution_manifest(path)

    obligation = _obligation()
    script = generate_sage_polynomial_script(obligation)
    request = run_sage_polynomial_obligation(
        obligation,
        executable="/usr/bin/sage",
        max_artifact_bytes=1,
        runner=_runner(),
    )["request"]
    run_root = tmp_path / "tiny" / "sage-run-fixture"
    run_root.mkdir(parents=True)
    (run_root / "input.py").write_bytes(script)
    environment = _execution_environment(run_root, "/usr/bin/sage")
    stdout = _stdout()
    payload = json.loads(stdout.decode().removeprefix(SAGE_RESULT_SENTINEL))
    with pytest.raises(SageAdapterError, match="evidence file exceeds its bound"):
        _seal_manifest(
            request=request,
            raw={
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
            },
            script_bytes=script,
            payload=payload,
            status="certified",
            non_claims=list(request["unsupported_conclusions"]),
        )


def test_manifest_rejects_sage_preparser_byproduct(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    (path.parent / "input.sage.py").write_bytes(b"# unbound Sage pre-parser output\n")

    with pytest.raises(SageAdapterError, match="layout"):
        verify_sage_execution_manifest(path)


def test_manifest_rejects_scratch_mutation_after_sealing(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path, with_scratch=True)
    (path.parent / "dot-sage" / "cache" / "lazy-import.pickle").write_bytes(
        b"changed"
    )

    with pytest.raises(SageAdapterError, match="scratch inventory mismatch"):
        verify_sage_execution_manifest(path)


@pytest.mark.parametrize("kind", ["symlink", "hardlink", "special"])
def test_manifest_rejects_unsafe_scratch_entries(tmp_path, kind) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    scratch = path.parent / "dot-sage"
    if kind == "symlink":
        (scratch / "unsafe").symlink_to(path.parent / "input.py")
        message = "symlink"
    elif kind == "hardlink":
        (scratch / "source").write_bytes(b"x")
        (scratch / "unsafe").hardlink_to(scratch / "source")
        message = "hard links"
    else:
        (scratch / "unsafe").mkdir()
        os.mkfifo(scratch / "unsafe" / "pipe")
        message = "special file"

    with pytest.raises(SageAdapterError, match=message):
        verify_sage_execution_manifest(path)


def test_manifest_rejects_scratch_entry_count_overflow(tmp_path, monkeypatch) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    scratch = path.parent / "dot-sage"
    (scratch / "one").write_bytes(b"1")
    (scratch / "two").write_bytes(b"2")
    monkeypatch.setattr(sage_adapter, "SAGE_MAX_SCRATCH_ENTRIES", 1)

    with pytest.raises(SageAdapterError, match="entry count"):
        verify_sage_execution_manifest(path)


def test_manifest_rejects_scratch_byte_overflow_before_reading(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    oversized = path.parent / "dot-sage" / "oversized"
    with oversized.open("wb") as handle:
        handle.truncate(10_485_761)

    with pytest.raises(SageAdapterError, match="scratch file bytes"):
        verify_sage_execution_manifest(path)


def test_manifest_rejects_unexpected_root_directory(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    (path.parent / "unregistered-scratch").mkdir()

    with pytest.raises(SageAdapterError, match="unexpected directory"):
        verify_sage_execution_manifest(path)


def test_manifest_rejects_oversized_manifest_before_json_parsing(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    with path.open("wb") as handle:
        handle.truncate(SAGE_MAX_MANIFEST_BYTES + 1)

    with pytest.raises(SageAdapterError, match="read bound"):
        verify_sage_execution_manifest(path)


def test_manifest_rejects_hard_linked_manifest(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    (tmp_path / "manifest-hardlink.json").hardlink_to(path)

    with pytest.raises(SageAdapterError, match="multiple hard links"):
        verify_sage_execution_manifest(path)


def test_manifest_scratch_record_mutation_fails_after_digest_refresh(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path, with_scratch=True)
    _rewrite_manifest(
        path,
        lambda value: value["scratch"].__setitem__("file_bytes", 4),
    )

    with pytest.raises(SageAdapterError, match="scratch inventory mismatch"):
        verify_sage_execution_manifest(path)


def test_manifest_rejects_boolean_scratch_count_after_digest_refresh(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path, with_scratch=True)
    _rewrite_manifest(
        path,
        lambda value: value["scratch"].__setitem__("file_bytes", False),
    )

    with pytest.raises(SageAdapterError, match="scratch inventory mismatch"):
        verify_sage_execution_manifest(path)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        (lambda value: value["command"].__setitem__(1, "--wrong"), "command/executable"),
        (lambda value: value["environment"].__setitem__("CUDA_VISIBLE_DEVICES", "0"), "environment"),
        (lambda value: value["tool"].__setitem__("reported_version", "10.0"), "version"),
        (lambda value: value.__setitem__("non_claims", ["weakened"]), "non-claims"),
        (lambda value: value["result"].__setitem__("status", "refuted"), "result status"),
        (lambda value: value["artifacts"][0].__setitem__("role", "stdout"), "role mismatch"),
    ],
)
def test_manifest_cross_field_mutations_fail_after_outer_digest_is_refreshed(
    tmp_path, mutation, message
) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    _rewrite_manifest(path, mutation)
    with pytest.raises(SageAdapterError, match=message):
        verify_sage_execution_manifest(path)


@pytest.mark.parametrize(("field", "replacement"), [("domain", "ZZ"), ("variable", "y")])
def test_manifest_rejects_redigested_payload_typed_domain_mismatch(
    tmp_path, field, replacement
) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    _rewrite_payload_and_refresh_manifest(
        path, lambda payload: payload.__setitem__(field, replacement)
    )

    with pytest.raises(SageAdapterError, match="request typed domain assumption"):
        verify_sage_execution_manifest(path)


def test_manifest_rejects_swapped_script_and_stdout_payload(tmp_path) -> None:
    path = _synthetic_sealed_manifest(tmp_path)
    run_root = path.parent
    (run_root / "input.py").write_bytes(b"# swapped script\n")
    with pytest.raises(SageAdapterError, match="artifact digest mismatch"):
        verify_sage_execution_manifest(path)

    path = _synthetic_sealed_manifest(tmp_path / "second")
    run_root = path.parent
    different = _stdout("refuted", witness={"assignment": {"x": "0"}, "lhs": "1", "rhs": "0"}, difference="1")
    (run_root / "stdout.bin").write_bytes(different)
    with pytest.raises(SageAdapterError, match="artifact digest mismatch"):
        verify_sage_execution_manifest(path)
