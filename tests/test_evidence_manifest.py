from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import threading
from typing import Any, Callable

import pytest

from mathdevmcp.evidence_manifest import (
    EvidenceConflictError,
    EvidenceValidationError,
    P01_ENTRY_ROOT_REF,
    P01_EVIDENCE_ROOT_REF,
    P01_NON_CLAIMS,
    P01_PASS_ACTION_SEQUENCE,
    P01_PLAN_REF,
    P01_PYTHON,
    P01_REQUIRED_INVARIANT_IDS,
    P01_REQUIRED_LEGACY_CASES,
    P01_REQUIRED_MUTATION_CASES,
    P01_VETO_KEYS,
    allocate_execution,
    atomic_write_artifact,
    atomic_write_canonical_record,
    build_evidence_manifest,
    build_evidence_request,
    canonical_json_bytes,
    content_digest,
    create_run_bundle,
    normalize_legacy_evidence,
    p01_fixed_action_argv,
    p01_governance_action_argv,
    publish_stable_phase_decision,
    reconstruct_p01_candidate,
    reconstruct_p01_final_decision,
    reconstruct_p01_run_manifest,
    seal_attempt_manifest,
    seal_bundle_index,
    strict_load_canonical_json,
    validate_logical_path,
    verify_attempt_manifest,
    verify_bootstrap_close,
    verify_bundle_index,
    verify_final_seal_audit_bindings,
    verify_p01_candidate,
    verify_p01_final_decision_candidate,
    verify_p01_run_manifest,
    verify_receipt_index,
    verify_result_review_bindings,
)


def _request(*, label: str = "eq:synthetic", target: str = "x + 1 = 1 + x") -> dict:
    assumptions = [
        {"id": "a_scalar", "kind": "domain", "statement": "x is a real scalar."},
        {"id": "a_defined", "kind": "definedness", "statement": "All terms are defined."},
    ]
    return build_evidence_request(
        source={
            "logical_id": "synthetic/source.tex",
            "file": "synthetic/source.tex",
            "label": label,
            "digest": hashlib.sha256(b"x + 1 = 1 + x").hexdigest(),
            "spans": [{"start_byte": 0, "end_byte": 13}],
            "parser_version": "synthetic-1",
        },
        obligation={"digest": hashlib.sha256(target.encode()).hexdigest(), "target": target},
        branch={"id": "branch_assumptions", "lineage": ["root", "branch_assumptions"]},
        typed_assumptions=assumptions,
        assumption_digest=content_digest(assumptions),
        native_input={"digest": hashlib.sha256(target.encode()).hexdigest(), "media_type": "text/plain"},
        tool={"name": "fake", "adapter_version": "1", "backend_version": "test", "executable_id": "fake_runner"},
        resource_limits={"timeout_ms": 1000, "max_output_bytes": 4096},
        expected_result_class="synthetic_integrity_fixture",
        backend_role="test_only_noncertifying",
        unsupported_conclusions=["mathematical proof", "publication eligibility"],
        policy_version="p01-test-1",
    )


def _execution_record() -> dict:
    return {
        "started_at_utc": "2026-07-11T00:00:00Z",
        "ended_at_utc": "2026-07-11T00:00:01Z",
        "wall_time_ns": 1_000_000_000,
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
        "runner_version": "fake-runner-1",
    }


def _result_record(stdout: dict, stderr: dict, structured: dict) -> dict:
    return {
        "outcome": "certified",
        "stdout": stdout,
        "stderr": stderr,
        "structured_result": structured,
        "stdout_truncated": False,
        "stderr_truncated": False,
        "redaction": {"applied": False, "fields": []},
        "certificate": None,
    }


def _interpretation() -> dict:
    return {
        "certified_scope": "synthetic fixture only",
        "refuted_scope": None,
        "unresolved_assumption_ids": [],
        "blocker_ids": [],
        "veto_ids": [],
        "non_claims": list(P01_NON_CLAIMS),
    }


def _sealed_bundle(tmp_path: Path):
    bundle = create_run_bundle(tmp_path / "evidence", run_id="run_test")
    request = _request()
    execution = allocate_execution(bundle, request)
    stdout = atomic_write_artifact(bundle, f"{execution.logical_root}/stdout.txt", b"ok\n", media_type="text/plain", role="stdout")
    stderr = atomic_write_artifact(bundle, f"{execution.logical_root}/stderr.txt", b"", media_type="text/plain", role="stderr")
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
        [stdout, stderr, structured],
        execution_record=_execution_record(),
        result_record=_result_record(stdout, stderr, structured),
        interpretation=_interpretation(),
    )
    return bundle, execution, sealed


def test_canonical_json_golden_order_unicode_and_set_semantics() -> None:
    first = {"z": 1, "typed_assumptions": [{"id": "b"}, {"id": "a"}], "name": "e\u0301"}
    second = {"name": "é", "typed_assumptions": [{"id": "a"}, {"id": "b"}], "z": 1}
    assert canonical_json_bytes(first) == canonical_json_bytes(second)
    assert canonical_json_bytes({"steps": ["b", "a"]}) != canonical_json_bytes({"steps": ["a", "b"]})


def test_canonical_json_rejects_float_surrogate_nonstring_and_nfc_collision() -> None:
    for value in ({"x": 1.0}, {"x": "\ud800"}, {1: "x"}, {"é": 1, "e\u0301": 2}):
        with pytest.raises(EvidenceValidationError):
            canonical_json_bytes(value)


def test_strict_canonical_loader_rejects_duplicates_and_noncanonical_bytes() -> None:
    with pytest.raises(EvidenceValidationError, match="duplicate"):
        strict_load_canonical_json(b'{"schema_version":"1.0","schema_version":"1.0"}', schema="evidence_request@1")
    request = _request()
    noncanonical = json.dumps(request, ensure_ascii=False, indent=2).encode()
    with pytest.raises(EvidenceValidationError, match="not canonical"):
        strict_load_canonical_json(noncanonical, schema="evidence_request@1")


def test_request_identity_changes_for_every_material_identity_group() -> None:
    base = _request()
    variants = []
    for path, value in (
        (("source", "label"), "eq:changed"),
        (("source", "digest"), "1" * 64),
        (("obligation", "target"), "x=x"),
        (("branch", "id"), "branch_changed"),
        (("native_input", "digest"), "2" * 64),
        (("tool", "backend_version"), "other"),
        (("backend_role",), "other_test_role"),
    ):
        variant = deepcopy(base)
        target = variant
        for key in path[:-1]:
            target = target[key]
        target[path[-1]] = value
        if path == ("obligation", "target"):
            variant["obligation"]["digest"] = hashlib.sha256(value.encode()).hexdigest()
        variants.append(variant)
    base_digest = content_digest(base, schema="evidence_request@1")
    assert all(content_digest(value, schema="evidence_request@1") != base_digest for value in variants)


@pytest.mark.parametrize("value", ["../x", "/x", "a//b", "a/./b", "a\\b", "C:/x", "a/"])
def test_logical_path_attacks_are_rejected(value: str) -> None:
    with pytest.raises(EvidenceValidationError):
        validate_logical_path(value)


def test_governance_records_require_strict_canonical_bytes(tmp_path: Path) -> None:
    vetoes = {key: False for key in P01_VETO_KEYS}
    record = {
        "schema_version": "p01_final_decision@1",
        "phase": "P01",
        "result_round": "rr01",
        "decision": "pass",
        "publication_mode": "disabled",
        "payload_bundle_index_digest": "1" * 64,
        "payload_bundle_index_file_sha256": "2" * 64,
        "candidate_decision_ref": "result-rounds/rr01/P01-candidate-decision.json",
        "candidate_decision_sha256": "3" * 64,
        "result_review_ref": "reviews/result.md",
        "result_review_sha256": "4" * 64,
        "reviewed_receipt_index_ref": "result-rounds/rr01/receipts/receipt-index-1.json",
        "reviewed_receipt_index_sha256": "5" * 64,
        "vetoes": vetoes,
        "non_claims": list(P01_NON_CLAIMS),
    }
    root = tmp_path / "root"
    root.mkdir()
    atomic_write_canonical_record(root, "decision.json", record, schema="p01_final_decision@1")
    loaded = strict_load_canonical_json(root / "decision.json", schema="p01_final_decision@1")
    assert loaded == json.loads(canonical_json_bytes(record, schema="p01_final_decision@1"))
    malformed = dict(record)
    malformed["extra"] = True
    with pytest.raises(EvidenceValidationError):
        canonical_json_bytes(malformed, schema="p01_final_decision@1")


def test_governance_store_is_no_overwrite_regular_file(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    record = {"schema_version": "p01_summary@1", "phase": "P01", "result_round": "rr01", "cases": [], "all_pass": True}
    atomic_write_canonical_record(root, "summary.json", record, schema="p01_summary@1")
    before = (root / "summary.json").read_bytes()
    with pytest.raises(EvidenceConflictError):
        atomic_write_canonical_record(root, "summary.json", record, schema="p01_summary@1")
    assert (root / "summary.json").read_bytes() == before
    assert (root / "summary.json").stat().st_mode & 0o777 == 0o600


def test_atomic_store_rejects_symlinked_intermediate_and_final(tmp_path: Path) -> None:
    bundle = create_run_bundle(tmp_path / "root", run_id="run_safe")
    outside = tmp_path / "outside"
    outside.mkdir()
    (bundle.root / "linked").symlink_to(outside, target_is_directory=True)
    with pytest.raises((EvidenceValidationError, OSError)):
        atomic_write_artifact(bundle, "linked/escape.bin", b"x")
    target = bundle.root / "final.bin"
    target.symlink_to(outside / "x")
    with pytest.raises((EvidenceConflictError, OSError)):
        atomic_write_artifact(bundle, "final.bin", b"x")


def test_attempt_manifest_verifies_and_tamper_fails(tmp_path: Path) -> None:
    bundle, execution, sealed = _sealed_bundle(tmp_path)
    verified = verify_attempt_manifest(bundle.root, sealed["manifest_ref"])
    assert verified["integrity_state"] == "verified"
    stdout = bundle.root / execution.logical_root / "stdout.txt"
    stdout.write_bytes(b"tampered")
    with pytest.raises(EvidenceValidationError, match="mismatch"):
        verify_attempt_manifest(bundle.root, sealed["manifest_ref"])


def test_parallel_identical_request_allocations_share_attempt_not_execution(tmp_path: Path) -> None:
    bundle = create_run_bundle(tmp_path / "root", run_id="run_parallel")
    request = _request()
    allocations = []
    lock = threading.Lock()

    def allocate() -> None:
        value = allocate_execution(bundle, request)
        with lock:
            allocations.append(value)

    threads = [threading.Thread(target=allocate) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    assert len({item.request_digest for item in allocations}) == 1
    assert len({item.attempt_id for item in allocations}) == 1
    assert len({item.execution_id for item in allocations}) == 4


def test_bundle_index_is_deterministic_and_excludes_governance(tmp_path: Path) -> None:
    bundle, _, _ = _sealed_bundle(tmp_path)
    result = seal_bundle_index(bundle)
    record = result["record"]
    refs = [item["logical_ref"] for item in record["artifacts"]]
    assert refs == sorted(refs)
    assert "bundle-index.json" not in refs
    assert result["payload_bundle_index_digest"] == content_digest(record, schema="payload_bundle_index@1")
    verified = verify_bundle_index(bundle.root)
    assert verified["disk_verification_state"] == "verified"
    assert verified["payload_bundle_index_file_sha256"] == result["payload_bundle_index_file_sha256"]
    with pytest.raises(EvidenceConflictError):
        atomic_write_artifact(bundle, "late.bin", b"late")
    with pytest.raises(EvidenceConflictError):
        allocate_execution(bundle, _request())


def test_round_close_schema_enforces_stage_nullability_and_both_entry_bindings() -> None:
    repair = {
        "finding_id": "finding-1",
        "source_stage": "local_check",
        "severity": "high",
        "affected_paths": ["src/mathdevmcp/evidence_manifest.py"],
        "required_change": "Repair the exact failed boundary.",
        "required_check_ids": ["canonical"],
        "non_claim": "This repair does not establish mathematical correctness.",
    }
    base = {
        "schema_version": "p01_round_close@1",
        "phase": "P01",
        "result_round": "rr01",
        "close_reason": "local_check_failure",
        "failed_action": "canonical",
        "entry_implementation_manifest_sha256": "1" * 64,
        "entry_protected_manifest_sha256": "2" * 64,
        "bootstrap_close_ref": "bootstrap-attempts/b01/bootstrap-close.txt",
        "bootstrap_close_sha256": "3" * 64,
        "predecessor_close_ref": None,
        "predecessor_close_sha256": None,
        "predecessor_terminal_receipt_index_ref": None,
        "predecessor_terminal_receipt_index_sha256": None,
        "implementation_exit_manifest_sha256": "4" * 64,
        "receipt_index_before_close_ref": "result-rounds/rr01/receipts/receipt-index-14.json",
        "receipt_index_before_close_sha256": "5" * 64,
        "log_inventory": [
            {
                "logical_ref": "result-rounds/rr01/logs/canonical-tests.log",
                "sha256": "6" * 64,
                "byte_count": 10,
                "role": "formal_check_log",
                "exit_code": 1,
            }
        ],
        "run_manifest_ref": None,
        "run_manifest_sha256": None,
        "result_ref": None,
        "result_sha256": None,
        "candidate_ref": None,
        "candidate_sha256": None,
        "result_review_ref": None,
        "result_review_sha256": None,
        "result_review_verdict": None,
        "final_decision_candidate_ref": None,
        "final_decision_candidate_sha256": None,
        "final_seal_audit_ref": None,
        "final_seal_audit_sha256": None,
        "scoped_repairs": [repair],
        "vetoes": {key: key == "canonical_identity_failure" for key in P01_VETO_KEYS},
        "non_claims": list(P01_NON_CLAIMS),
    }
    assert canonical_json_bytes(base, schema="p01_round_close@1")
    assert base["entry_implementation_manifest_sha256"] != base["entry_protected_manifest_sha256"]

    stages = {
        "candidate_gate_failure": {
            "failed_action": "candidate_gate",
            "run_manifest_ref": "result-rounds/rr01/run-manifest.json",
            "run_manifest_sha256": "7" * 64,
            "result_ref": "docs/plans/p01-result.md",
            "result_sha256": "8" * 64,
            "candidate_ref": "result-rounds/rr01/P01-candidate-decision.json",
            "candidate_sha256": "9" * 64,
        },
        "result_review_revise": {
            "failed_action": None,
            "run_manifest_ref": "result-rounds/rr01/run-manifest.json",
            "run_manifest_sha256": "7" * 64,
            "result_ref": "docs/plans/p01-result.md",
            "result_sha256": "8" * 64,
            "candidate_ref": "result-rounds/rr01/P01-candidate-decision.json",
            "candidate_sha256": "9" * 64,
            "result_review_ref": "docs/reviews/p01-review.md",
            "result_review_sha256": "a" * 64,
            "result_review_verdict": "REVISE",
        },
        "final_seal_audit_revise": {
            "failed_action": None,
            "run_manifest_ref": "result-rounds/rr01/run-manifest.json",
            "run_manifest_sha256": "7" * 64,
            "result_ref": "docs/plans/p01-result.md",
            "result_sha256": "8" * 64,
            "candidate_ref": "result-rounds/rr01/P01-candidate-decision.json",
            "candidate_sha256": "9" * 64,
            "result_review_ref": "docs/reviews/p01-review.md",
            "result_review_sha256": "a" * 64,
            "result_review_verdict": "AGREE",
            "final_decision_candidate_ref": "result-rounds/rr01/P01-final-decision-candidate.json",
            "final_decision_candidate_sha256": "b" * 64,
            "final_seal_audit_ref": "docs/reviews/p01-audit.md",
            "final_seal_audit_sha256": "c" * 64,
        },
    }
    for reason, changes in stages.items():
        record = deepcopy(base)
        record["close_reason"] = reason
        record.update(changes)
        record["scoped_repairs"][0]["source_stage"] = {
            "candidate_gate_failure": "candidate_gate",
            "result_review_revise": "result_review",
            "final_seal_audit_revise": "final_seal_audit",
        }[reason]
        assert canonical_json_bytes(record, schema="p01_round_close@1")
        invalid = deepcopy(record)
        invalid["candidate_ref"] = None
        with pytest.raises(EvidenceValidationError):
            canonical_json_bytes(invalid, schema="p01_round_close@1")

    successor = deepcopy(base)
    successor["result_round"] = "rr02"
    with pytest.raises(EvidenceValidationError, match="predecessor"):
        canonical_json_bytes(successor, schema="p01_round_close@1")


def _bootstrap_close() -> bytes:
    return (
        "MATHDEVMCP_P01_BOOTSTRAP_CLOSE_V1\n"
        "bootstrap_attempt=b01\n"
        "status=PASS\n"
        f"entry_implementation_manifest_sha256={'1' * 64}\n"
        f"entry_protected_manifest_sha256={'2' * 64}\n"
        "prior_result_round_close_ref=NONE\n"
        "prior_result_round_close_sha256=NONE\n"
        f"implementation_exit_manifest_sha256={'3' * 64}\n"
        f"bootstrap_command_ledger_sha256={'4' * 64}\n"
        f"bootstrap_log_sha256={'5' * 64}\n"
        "bootstrap_log_byte_count=42\n"
        "bootstrap_exit_code=0\n"
        "bootstrap_result_note_ref=docs/plans/mathdevmcp-real-document-remediation-phase-01-bootstrap-b01-result-2026-07-11.md\n"
        f"bootstrap_result_note_sha256={'6' * 64}\n"
        "END\n"
    ).encode()


def test_bootstrap_close_parser_matches_independent_ascii_grammar() -> None:
    assert verify_bootstrap_close(_bootstrap_close(), {})["status"] == "PASS"
    for replacement in (b"status=FAIL", b"bootstrap_exit_code=1", b"END\r"):
        with pytest.raises(EvidenceValidationError):
            verify_bootstrap_close(_bootstrap_close().replace(b"status=PASS" if b"status" in replacement else b"bootstrap_exit_code=0" if b"exit" in replacement else b"END", replacement), {})


def _review_bytes(verdict: str = "AGREE") -> tuple[bytes, dict[str, str]]:
    bindings = {
        "result_round": "rr01",
        "candidate_sha256": "1" * 64,
        "run_manifest_sha256": "2" * 64,
        "result_sha256": "3" * 64,
        "payload_bundle_index_digest": "4" * 64,
        "payload_bundle_index_file_sha256": "5" * 64,
        "receipt_index_sha256": "6" * 64,
    }
    text = (
        f"Reviewed result round: `{bindings['result_round']}`\n"
        f"Reviewed candidate SHA-256: `{bindings['candidate_sha256']}`\n"
        f"Reviewed run manifest SHA-256: `{bindings['run_manifest_sha256']}`\n"
        f"Reviewed result SHA-256: `{bindings['result_sha256']}`\n"
        f"Reviewed payload bundle-index digest: `{bindings['payload_bundle_index_digest']}`\n"
        f"Reviewed payload bundle-index file SHA-256: `{bindings['payload_bundle_index_file_sha256']}`\n"
        f"Reviewed governance receipt-index SHA-256: `{bindings['receipt_index_sha256']}`\n"
        f"VERDICT: {verdict}\n"
    )
    return text.encode(), bindings


def test_review_and_audit_grammars_are_closed_unique_and_final() -> None:
    review, bindings = _review_bytes()
    assert verify_result_review_bindings(review, bindings)["verdict"] == "AGREE"
    for bad in (review + review.splitlines(keepends=True)[1], review.replace(b"VERDICT: AGREE\n", b"VERDICT: AGREE\nextra\n"), b"\xef\xbb\xbf" + review, review.replace(b"\n", b"\r\n")):
        with pytest.raises(EvidenceValidationError):
            verify_result_review_bindings(bad, bindings)

    audit_bindings = {
        "result_round": "rr01",
        "final_candidate_sha256": "1" * 64,
        "candidate_sha256": "2" * 64,
        "result_review_sha256": "3" * 64,
        "validation_log_sha256": "4" * 64,
        "receipt_index_sha256": "5" * 64,
    }
    audit = (
        f"Audited result round: `{audit_bindings['result_round']}`\n"
        f"Audited final-decision candidate SHA-256: `{audit_bindings['final_candidate_sha256']}`\n"
        f"Audited candidate SHA-256: `{audit_bindings['candidate_sha256']}`\n"
        f"Audited result-review SHA-256: `{audit_bindings['result_review_sha256']}`\n"
        f"Audited final-candidate validation-log SHA-256: `{audit_bindings['validation_log_sha256']}`\n"
        f"Audited governance receipt-index SHA-256: `{audit_bindings['receipt_index_sha256']}`\n"
        "VERDICT: AGREE\n"
    ).encode()
    assert verify_final_seal_audit_bindings(audit, audit_bindings)["verdict"] == "AGREE"


def test_governance_receipt_chain_and_action_bindings_are_closed() -> None:
    init_bindings = {
        "bootstrap_close_ref": "bootstrap-attempts/b01/bootstrap-close.txt",
        "bootstrap_close_sha256": "1" * 64,
        "bootstrap_shell_verification_ref": "bootstrap-attempts/b01/bootstrap-shell-verification.log",
        "bootstrap_shell_verification_sha256": "2" * 64,
        "entry_implementation_manifest_sha256": "3" * 64,
        "entry_protected_manifest_sha256": "4" * 64,
        "implementation_exit_manifest_ref": "result-rounds/rr01/implementation-exit-sha256.txt",
        "implementation_exit_manifest_sha256": "5" * 64,
        "prior_round_close_ref": None,
        "prior_round_close_sha256": None,
        "prior_terminal_receipt_index_ref": None,
        "prior_terminal_receipt_index_sha256": None,
    }
    first = {
        "schema_version": "p01_command_receipt@1",
        "phase": "P01",
        "result_round": "rr01",
        "sequence": 1,
        "check_id": "init_round",
        "command_argv": ["p01_governance.py", "init-round"],
        "started_at_utc": "2026-07-11T00:00:00Z",
        "ended_at_utc": "2026-07-11T00:00:01Z",
        "wall_time_ns": 1,
        "exit_code": 0,
        "stdout_ref": "logs/init.stdout",
        "stdout_sha256": hashlib.sha256(b"").hexdigest(),
        "stdout_byte_count": 0,
        "stderr_ref": "logs/init.stderr",
        "stderr_sha256": hashlib.sha256(b"").hexdigest(),
        "stderr_byte_count": 0,
        "prior_receipt_sha256": None,
        "bindings": init_bindings,
    }
    payload = canonical_json_bytes(first, schema="p01_command_receipt@1")
    entry = {"sequence": 1, "check_id": "init_round", "receipt_ref": "receipts/receipt-1.json", "receipt_sha256": content_digest(payload)}
    index = {"schema_version": "p01_receipt_index@1", "phase": "P01", "result_round": "rr01", "receipts": [entry], "head_sequence": 1, "head_sha256": entry["receipt_sha256"]}
    assert canonical_json_bytes(index, schema="p01_receipt_index@1")
    bad = deepcopy(index)
    bad["head_sha256"] = "0" * 64
    with pytest.raises(EvidenceValidationError):
        canonical_json_bytes(bad, schema="p01_receipt_index@1")
    bad_receipt = deepcopy(first)
    bad_receipt["bindings"]["unexpected"] = "6" * 64
    with pytest.raises(EvidenceValidationError, match="keys mismatch"):
        canonical_json_bytes(bad_receipt, schema="p01_command_receipt@1")
    bad_receipt = deepcopy(first)
    bad_receipt["check_id"] = "canonical"
    with pytest.raises(EvidenceValidationError, match="keys mismatch"):
        canonical_json_bytes(bad_receipt, schema="p01_command_receipt@1")


def test_stable_publication_revalidates_bindings_without_injected_authority() -> None:
    assert "authorization" not in publish_stable_phase_decision.__annotations__
    with pytest.raises(TypeError):
        publish_stable_phase_decision(Path("."), candidate_ref="x", review_ref="y", audit_ref="z", validation_log_ref="v", governance_receipt_index_ref="i", stable_ref="s", authorization=True)


def _stable_publication_fixture(
    root: Path,
    *,
    candidate_gate_stdout_override: bytes | None = None,
    candidate_validation_override: bytes | None = None,
    init_measurement_overrides: dict[str, str] | None = None,
    command_argv_tamper_action: str | None = None,
) -> dict[str, Any]:
    root.mkdir()
    round_ref = f"{P01_EVIDENCE_ROOT_REF}/result-rounds/rr01"
    entries: list[dict[str, Any]] = []
    prior_sha256: str | None = None

    def write_bytes(ref: str, data: bytes) -> None:
        path = root / ref
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def append_receipt(
        check_id: str,
        bindings: dict[str, Any],
        *,
        stdout: bytes = b"",
        stderr: bytes = b"",
    ) -> tuple[str, str]:
        nonlocal prior_sha256
        sequence = len(entries) + 1
        stdout_ref = f"{round_ref}/logs/receipt-{sequence:02d}.stdout"
        stderr_ref = f"{round_ref}/logs/receipt-{sequence:02d}.stderr"
        write_bytes(stdout_ref, stdout)
        write_bytes(stderr_ref, stderr)
        if check_id == "init_round":
            command_argv = [
                "env",
                "PYTHONPATH=src",
                P01_PYTHON,
                "scripts/p01_governance.py",
                "init-round",
                "--round",
                "rr01",
                "--entry-root",
                P01_ENTRY_ROOT_REF,
                "--bootstrap-close",
                bindings["bootstrap_close_ref"],
                "--bootstrap-shell-verification",
                bindings["bootstrap_shell_verification_ref"],
                "--round-root",
                round_ref,
                "--prior-round-close",
                "NONE",
                "--prior-terminal-receipt-index",
                "NONE",
            ]
        else:
            command_argv = p01_fixed_action_argv(round_ref, check_id)
            if command_argv is None:
                artifact_ref = None
                if check_id == "result_review_binding":
                    artifact_ref = bindings["review_ref"]
                elif check_id == "final_seal_audit_binding":
                    artifact_ref = bindings["audit_ref"]
                command_argv = p01_governance_action_argv(round_ref, check_id, artifact_ref=artifact_ref)
        if check_id == command_argv_tamper_action:
            command_argv = [*command_argv, "--tampered"]
        receipt = {
            "schema_version": "p01_command_receipt@1",
            "phase": "P01",
            "result_round": "rr01",
            "sequence": sequence,
            "check_id": check_id,
            "command_argv": command_argv,
            "started_at_utc": "2026-07-11T00:00:00Z",
            "ended_at_utc": "2026-07-11T00:00:01Z",
            "wall_time_ns": sequence,
            "exit_code": 0,
            "stdout_ref": stdout_ref,
            "stdout_sha256": hashlib.sha256(stdout).hexdigest(),
            "stdout_byte_count": len(stdout),
            "stderr_ref": stderr_ref,
            "stderr_sha256": hashlib.sha256(stderr).hexdigest(),
            "stderr_byte_count": len(stderr),
            "prior_receipt_sha256": prior_sha256,
            "bindings": bindings,
        }
        receipt_ref = f"{round_ref}/receipts/receipt-{sequence:02d}.json"
        receipt_write = atomic_write_canonical_record(
            root,
            receipt_ref,
            receipt,
            schema="p01_command_receipt@1",
        )
        prior_sha256 = receipt_write["sha256"]
        entries.append(
            {
                "sequence": sequence,
                "check_id": check_id,
                "receipt_ref": receipt_ref,
                "receipt_sha256": prior_sha256,
            }
        )
        index = {
            "schema_version": "p01_receipt_index@1",
            "phase": "P01",
            "result_round": "rr01",
            "receipts": deepcopy(entries),
            "head_sequence": sequence,
            "head_sha256": prior_sha256,
        }
        index_ref = f"{round_ref}/receipts/receipt-index-{sequence:02d}.json"
        index_write = atomic_write_canonical_record(root, index_ref, index, schema="p01_receipt_index@1")
        return index_ref, index_write["sha256"]

    result_ref = "docs/plans/mathdevmcp-real-document-remediation-phase-01-evidence-integrity-result-rr01-2026-07-11.md"
    review_ref = "docs/reviews/mathdevmcp-real-document-remediation-phase-01-result-review-rr01-result-2026-07-11.md"
    audit_ref = "docs/reviews/p01-audit.md"
    bundle_root_ref = f"{round_ref}/synthetic-bundle/run"
    bundle_ref = f"{bundle_root_ref}/bundle-index.json"
    run_ref = f"{round_ref}/run-manifest.json"
    original_ref = f"{round_ref}/P01-candidate-decision.json"
    final_ref = f"{round_ref}/P01-final-decision-candidate.json"
    candidate_validation_ref = f"{round_ref}/logs/candidate-validation.log"
    validation_ref = f"{round_ref}/logs/final-decision-candidate-validation.log"
    stable_ref = f"{P01_EVIDENCE_ROOT_REF}/phase-results/P01-decision.json"
    write_bytes(P01_PLAN_REF, b"synthetic P01 plan fixture\n")
    write_bytes(result_ref, b"synthetic result fixture\n")
    result_sha256 = hashlib.sha256((root / result_ref).read_bytes()).hexdigest()

    entry_manifest = f"{'1' * 64}  src/mathdevmcp/base.py\n".encode()
    exit_manifest = f"{'2' * 64}  src/mathdevmcp/base.py\n".encode()
    protected_manifest = b"".join(
        f"{value:064x}  docs/protected-{value:02d}.md\n".encode()
        for value in range(1, 12)
    )
    entry_sha256 = content_digest(entry_manifest)
    exit_sha256 = content_digest(exit_manifest)
    protected_sha256 = content_digest(protected_manifest)
    implementation_ref = f"{round_ref}/implementation-exit-sha256.txt"
    write_bytes(f"{P01_ENTRY_ROOT_REF}/implementation-entry-sha256.txt", entry_manifest)
    write_bytes(f"{P01_ENTRY_ROOT_REF}/protected-dirty-sha256.txt", protected_manifest)
    write_bytes(implementation_ref, exit_manifest)

    bootstrap_ref = f"{P01_EVIDENCE_ROOT_REF}/bootstrap-attempts/b01/bootstrap-close.txt"
    bootstrap_result_ref = "docs/plans/mathdevmcp-real-document-remediation-phase-01-bootstrap-b01-result-2026-07-11.md"
    bootstrap_result = b"synthetic bootstrap result\n"
    ledger_ref = f"{P01_EVIDENCE_ROOT_REF}/bootstrap-attempts/b01/bootstrap-command-ledger.txt"
    ledger = b"synthetic bootstrap ledger\n"
    run_log_ref = f"{P01_EVIDENCE_ROOT_REF}/bootstrap-attempts/b01/bootstrap-run.log"
    run_log = b"status=PASS\n"
    write_bytes(bootstrap_result_ref, bootstrap_result)
    write_bytes(ledger_ref, ledger)
    write_bytes(run_log_ref, run_log)
    bootstrap_result_sha256 = content_digest(bootstrap_result)
    ledger_sha256 = content_digest(ledger)
    run_log_sha256 = content_digest(run_log)
    bootstrap = (
        "MATHDEVMCP_P01_BOOTSTRAP_CLOSE_V1\n"
        "bootstrap_attempt=b01\n"
        "status=PASS\n"
        f"entry_implementation_manifest_sha256={entry_sha256}\n"
        f"entry_protected_manifest_sha256={protected_sha256}\n"
        "prior_result_round_close_ref=NONE\n"
        "prior_result_round_close_sha256=NONE\n"
        f"implementation_exit_manifest_sha256={exit_sha256}\n"
        f"bootstrap_command_ledger_sha256={ledger_sha256}\n"
        f"bootstrap_log_sha256={run_log_sha256}\n"
        f"bootstrap_log_byte_count={len(run_log)}\n"
        "bootstrap_exit_code=0\n"
        f"bootstrap_result_note_ref={bootstrap_result_ref}\n"
        f"bootstrap_result_note_sha256={bootstrap_result_sha256}\n"
        "END\n"
    ).encode("ascii")
    write_bytes(bootstrap_ref, bootstrap)
    bootstrap_sha256 = content_digest(bootstrap)
    shell_ref = f"{P01_EVIDENCE_ROOT_REF}/bootstrap-attempts/b01/bootstrap-shell-verification.log"
    shell = (
        "MATHDEVMCP_P01_BOOTSTRAP_SHELL_VERIFICATION_V1\n"
        f"bootstrap_close_ref={bootstrap_ref}\n"
        f"bootstrap_close_sha256={bootstrap_sha256}\n"
        f"bootstrap_command_ledger_ref={ledger_ref}\n"
        f"bootstrap_command_ledger_sha256={ledger_sha256}\n"
        f"bootstrap_run_log_ref={run_log_ref}\n"
        f"bootstrap_run_log_sha256={run_log_sha256}\n"
        f"bootstrap_result_note_ref={bootstrap_result_ref}\n"
        f"bootstrap_result_note_sha256={bootstrap_result_sha256}\n"
        "status=PASS\n"
    ).encode("ascii")
    write_bytes(shell_ref, shell)

    bundle = {
        "schema_version": "1.0",
        "index_kind": "payload_bundle_index",
        "exclusions": ["bundle-index.json", "phase-results/", "review-governance/"],
        "artifacts": [],
    }
    bundle_write = atomic_write_canonical_record(root, bundle_ref, bundle, schema="payload_bundle_index@1")
    bundle_digest = content_digest(bundle, schema="payload_bundle_index@1")

    mutation = {
        "schema_version": "p01_mutation_summary@1",
        "phase": "P01",
        "result_round": "rr01",
        "cases": [
            {
                "case_id": case_id,
                "mutated_field": case_id,
                "expected_veto_id": veto_id,
                "observed_veto_ids": [veto_id],
                "passed": True,
            }
            for case_id, veto_id in P01_REQUIRED_MUTATION_CASES
        ],
        "all_pass": True,
    }
    parallel = {
        "schema_version": "p01_parallel_summary@1",
        "phase": "P01",
        "result_round": "rr01",
        "cases": [
            {
                "case_id": "identical_request_thread_and_run_identity",
                "request_equal": True,
                "attempt_equal": True,
                "execution_distinct": True,
                "run_distinct": True,
                "deterministic_index": True,
                "passed": True,
            }
        ],
        "all_pass": True,
    }
    legacy = {
        "schema_version": "p01_legacy_summary@1",
        "phase": "P01",
        "result_round": "rr01",
        "cases": [
            {
                "case_id": case_id,
                "input_schema_class": schema_class,
                "expected_certification_state": state,
                "observed_certification_state": state,
                "passed": True,
            }
            for case_id, schema_class, state in P01_REQUIRED_LEGACY_CASES
        ],
        "all_pass": True,
    }
    generator = {
        "schema_version": "p01_generator_result@1",
        "phase": "P01",
        "result_round": "rr01",
        "bundle_ref": bundle_root_ref,
        "payload_bundle_index_digest": bundle_digest,
        "payload_bundle_index_file_sha256": bundle_write["sha256"],
        "disk_verification_state": "verified",
        "invariant_ids": list(P01_REQUIRED_INVARIANT_IDS),
        "all_pass": True,
    }
    summary_specs = (
        ("mutation", "summaries/mutation-matrix.json", mutation, "p01_mutation_summary@1"),
        ("parallel", "summaries/serial-parallel-identity.json", parallel, "p01_parallel_summary@1"),
        ("legacy", "summaries/legacy-matrix.json", legacy, "p01_legacy_summary@1"),
        ("generator", "summaries/generator-result.json", generator, "p01_generator_result@1"),
    )
    summary_refs: dict[str, str] = {}
    for name, relative, record, schema in summary_specs:
        ref = f"{round_ref}/{relative}"
        atomic_write_canonical_record(root, ref, record, schema=schema)
        summary_refs[name] = ref

    init_bindings = {
        "bootstrap_close_ref": bootstrap_ref,
        "bootstrap_close_sha256": bootstrap_sha256,
        "bootstrap_shell_verification_ref": shell_ref,
        "bootstrap_shell_verification_sha256": content_digest(shell),
        "entry_implementation_manifest_sha256": entry_sha256,
        "entry_protected_manifest_sha256": protected_sha256,
        "implementation_exit_manifest_ref": implementation_ref,
        "implementation_exit_manifest_sha256": exit_sha256,
        "prior_round_close_ref": None,
        "prior_round_close_sha256": None,
        "prior_terminal_receipt_index_ref": None,
        "prior_terminal_receipt_index_sha256": None,
    }
    init_measurement_record = {
        "bootstrap": "b01",
        "git_commit": "a" * 40,
        "implementation_exit_manifest_sha256": exit_sha256,
        "platform_system": "Linux",
        "pytest_version": "9.0.2",
        "python_executable": P01_PYTHON,
        "python_implementation": "CPython",
        "python_version": "3.11.15",
        "pythonpath": "src",
    }
    init_measurement_record.update(init_measurement_overrides or {})
    init_measurement = canonical_json_bytes(init_measurement_record) + b"\n"
    for action in P01_PASS_ACTION_SEQUENCE[:14]:
        bindings = init_bindings if action == "init_round" else (
            {
                "manifest_ref": implementation_ref,
                "manifest_sha256": exit_sha256,
            }
            if action == "implementation_exit"
            else {}
        )
        append_receipt(action, bindings, stdout=init_measurement if action == "init_round" else b"")
    bind_result_index_ref, bind_result_index_sha256 = append_receipt(
        "bind_result",
        {"result_ref": result_ref, "result_sha256": result_sha256},
    )
    run_manifest = reconstruct_p01_run_manifest(root, bind_result_index_ref)
    run_write = atomic_write_canonical_record(root, run_ref, run_manifest, schema="p01_run_manifest@1")
    build_run_index_ref, build_run_index_sha256 = append_receipt(
        "build_run_manifest",
        {
            "run_manifest_ref": run_ref,
            "run_manifest_sha256": run_write["sha256"],
            "bound_receipt_index_ref": bind_result_index_ref,
            "bound_receipt_index_sha256": bind_result_index_sha256,
        },
    )
    original, _ = reconstruct_p01_candidate(root, build_run_index_ref)
    original_write = atomic_write_canonical_record(root, original_ref, original, schema="p01_candidate_decision@1")
    build_candidate_index_ref, build_candidate_index_sha256 = append_receipt(
        "build_candidate",
        {
            "run_manifest_ref": run_ref,
            "run_manifest_sha256": run_write["sha256"],
            "candidate_ref": original_ref,
            "candidate_sha256": original_write["sha256"],
            "bound_receipt_index_ref": build_run_index_ref,
            "bound_receipt_index_sha256": build_run_index_sha256,
        },
    )
    verified = verify_p01_candidate(
        root,
        candidate_ref=original_ref,
        build_run_receipt_index_ref=build_run_index_ref,
    )
    write_bytes(candidate_validation_ref, candidate_validation_override or verified["report_bytes"])
    candidate_gate_index_ref, candidate_gate_index_sha256 = append_receipt(
        "candidate_gate",
        {
            "run_manifest_ref": run_ref,
            "run_manifest_sha256": run_write["sha256"],
            "candidate_ref": original_ref,
            "candidate_sha256": original_write["sha256"],
            "validated_receipt_index_ref": build_candidate_index_ref,
            "validated_receipt_index_sha256": build_candidate_index_sha256,
            "payload_bundle_index_ref": bundle_ref,
            "payload_bundle_index_digest": bundle_digest,
            "payload_bundle_index_file_sha256": bundle_write["sha256"],
        },
        stdout=candidate_gate_stdout_override or verified["report_bytes"],
    )
    review = (
        "Phase 01 synthetic publication fixture review.\n"
        f"Reviewed result round: `rr01`\n"
        f"Reviewed candidate SHA-256: `{original_write['sha256']}`\n"
        f"Reviewed run manifest SHA-256: `{run_write['sha256']}`\n"
        f"Reviewed result SHA-256: `{result_sha256}`\n"
        f"Reviewed payload bundle-index digest: `{bundle_digest}`\n"
        f"Reviewed payload bundle-index file SHA-256: `{bundle_write['sha256']}`\n"
        f"Reviewed governance receipt-index SHA-256: `{candidate_gate_index_sha256}`\n"
        "VERDICT: AGREE\n"
    ).encode()
    write_bytes(review_ref, review)
    review_sha256 = hashlib.sha256(review).hexdigest()
    review_binding_index_ref, review_binding_index_sha256 = append_receipt(
        "result_review_binding",
        {
            "review_ref": review_ref,
            "review_sha256": review_sha256,
            "candidate_ref": original_ref,
            "candidate_sha256": original_write["sha256"],
            "reviewed_receipt_index_ref": candidate_gate_index_ref,
            "reviewed_receipt_index_sha256": candidate_gate_index_sha256,
        },
        stdout=b"VERDICT=AGREE\n",
    )
    final = reconstruct_p01_final_decision(root, review_binding_index_ref)
    final_write = atomic_write_canonical_record(root, final_ref, final, schema="p01_final_decision@1")
    build_final_index_ref, build_final_index_sha256 = append_receipt(
        "build_final_candidate",
        {
            "final_candidate_ref": final_ref,
            "final_candidate_sha256": final_write["sha256"],
            "result_review_ref": review_ref,
            "result_review_sha256": review_sha256,
            "reviewed_receipt_index_ref": review_binding_index_ref,
            "reviewed_receipt_index_sha256": review_binding_index_sha256,
        },
    )
    validation = b"P01_FINAL_CANDIDATE_VALIDATION_V1\nstatus=PASS\n"
    write_bytes(validation_ref, validation)
    validation_sha256 = hashlib.sha256(validation).hexdigest()
    final_gate_index_ref, final_gate_index_sha256 = append_receipt(
        "final_candidate_gate",
        {
            "final_candidate_ref": final_ref,
            "final_candidate_sha256": final_write["sha256"],
            "validation_log_ref": validation_ref,
            "validation_log_sha256": validation_sha256,
            "validated_receipt_index_ref": build_final_index_ref,
            "validated_receipt_index_sha256": build_final_index_sha256,
        },
    )
    audit = (
        "Phase 01 synthetic publication fixture audit.\n"
        "Audited result round: `rr01`\n"
        f"Audited final-decision candidate SHA-256: `{final_write['sha256']}`\n"
        f"Audited candidate SHA-256: `{original_write['sha256']}`\n"
        f"Audited result-review SHA-256: `{review_sha256}`\n"
        f"Audited final-candidate validation-log SHA-256: `{validation_sha256}`\n"
        f"Audited governance receipt-index SHA-256: `{final_gate_index_sha256}`\n"
        "VERDICT: AGREE\n"
    ).encode()
    write_bytes(audit_ref, audit)
    audit_sha256 = hashlib.sha256(audit).hexdigest()
    terminal_index_ref, terminal_index_sha256 = append_receipt(
        "final_seal_audit_binding",
        {
            "audit_ref": audit_ref,
            "audit_sha256": audit_sha256,
            "final_candidate_ref": final_ref,
            "final_candidate_sha256": final_write["sha256"],
            "candidate_ref": original_ref,
            "candidate_sha256": original_write["sha256"],
            "result_review_ref": review_ref,
            "result_review_sha256": review_sha256,
            "validation_log_ref": validation_ref,
            "validation_log_sha256": validation_sha256,
            "audited_receipt_index_ref": final_gate_index_ref,
            "audited_receipt_index_sha256": final_gate_index_sha256,
        },
    )
    return {
        "append_receipt": append_receipt,
        "audit_ref": audit_ref,
        "audit_sha256": audit_sha256,
        "build_final_index_ref": build_final_index_ref,
        "build_run_index_ref": build_run_index_ref,
        "candidate_ref": original_ref,
        "candidate_validation_ref": candidate_validation_ref,
        "final_ref": final_ref,
        "final_sha256": final_write["sha256"],
        "review_ref": review_ref,
        "review_binding_index_ref": review_binding_index_ref,
        "run_ref": run_ref,
        "stable_ref": stable_ref,
        "summary_refs": summary_refs,
        "terminal_index_ref": terminal_index_ref,
        "terminal_index_sha256": terminal_index_sha256,
        "final_gate_index_ref": final_gate_index_ref,
        "validation_ref": validation_ref,
        "validation_sha256": validation_sha256,
    }


def test_stable_publication_is_no_overwrite_hard_link_with_terminal_receipt(tmp_path: Path) -> None:
    root = tmp_path / "root"
    fixture = _stable_publication_fixture(root)
    published = publish_stable_phase_decision(
        root,
        candidate_ref=fixture["final_ref"],
        review_ref=fixture["review_ref"],
        audit_ref=fixture["audit_ref"],
        validation_log_ref=fixture["validation_ref"],
        governance_receipt_index_ref=fixture["terminal_index_ref"],
        stable_ref=fixture["stable_ref"],
    )
    assert published["same_inode"] is True
    assert published["same_digest"] is True
    assert published["stable_sha256"] == fixture["final_sha256"]
    final = root / fixture["final_ref"]
    stable = root / fixture["stable_ref"]
    assert final.stat().st_ino == stable.stat().st_ino
    assert stable.read_bytes() == final.read_bytes()
    publication_index_ref, publication_index_sha256 = fixture["append_receipt"](
        "stable_publication",
        {
            "stable_ref": fixture["stable_ref"],
            "stable_sha256": published["stable_sha256"],
            "final_candidate_ref": fixture["final_ref"],
            "final_candidate_sha256": fixture["final_sha256"],
            "audit_ref": fixture["audit_ref"],
            "audit_sha256": fixture["audit_sha256"],
            "validation_log_ref": fixture["validation_ref"],
            "validation_log_sha256": fixture["validation_sha256"],
            "same_inode": True,
            "same_digest": True,
        },
    )
    terminal = verify_receipt_index(root, publication_index_ref)
    assert terminal["index_sha256"] == publication_index_sha256
    assert terminal["receipts"][-1]["record"]["check_id"] == "stable_publication"
    with pytest.raises(EvidenceConflictError):
        publish_stable_phase_decision(
            root,
            candidate_ref=fixture["final_ref"],
            review_ref=fixture["review_ref"],
            audit_ref=fixture["audit_ref"],
            validation_log_ref=fixture["validation_ref"],
            governance_receipt_index_ref=fixture["terminal_index_ref"],
            stable_ref=fixture["stable_ref"],
        )


def _replace_canonical_record(root: Path, ref: str, record: dict[str, Any], schema: str) -> None:
    (root / ref).write_bytes(canonical_json_bytes(record, schema=schema))


def _mutate_final_field(final: dict[str, Any], field: str) -> None:
    replacements: dict[str, Any] = {
        "schema_version": "p01_final_decision@2",
        "phase": "P02",
        "result_round": "rr02",
        "decision": "fail",
        "publication_mode": "enabled",
        "payload_bundle_index_digest": "0" * 64,
        "payload_bundle_index_file_sha256": "1" * 64,
        "candidate_decision_ref": "alternate/candidate.json",
        "candidate_decision_sha256": "2" * 64,
        "result_review_ref": "alternate/review.md",
        "result_review_sha256": "3" * 64,
        "reviewed_receipt_index_ref": "alternate/receipt-index.json",
        "reviewed_receipt_index_sha256": "4" * 64,
    }
    if field == "vetoes":
        final[field]["governance_chain_failure"] = True
    elif field == "non_claims":
        final[field].remove("no_release_readiness")
    else:
        final[field] = replacements[field]


@pytest.mark.parametrize(
    "field",
    (
        "schema_version",
        "phase",
        "result_round",
        "decision",
        "publication_mode",
        "payload_bundle_index_digest",
        "payload_bundle_index_file_sha256",
        "candidate_decision_ref",
        "candidate_decision_sha256",
        "result_review_ref",
        "result_review_sha256",
        "reviewed_receipt_index_ref",
        "reviewed_receipt_index_sha256",
        "vetoes",
        "non_claims",
    ),
)
def test_each_final_decision_field_tamper_is_rejected(tmp_path: Path, field: str) -> None:
    root = tmp_path / field
    fixture = _stable_publication_fixture(root)
    final = strict_load_canonical_json(root / fixture["final_ref"], schema="p01_final_decision@1")
    _mutate_final_field(final, field)
    try:
        _replace_canonical_record(root, fixture["final_ref"], final, "p01_final_decision@1")
    except EvidenceValidationError:
        return
    with pytest.raises(EvidenceValidationError, match="does not equal independent reconstruction"):
        verify_p01_final_decision_candidate(
            root,
            final_candidate_ref=fixture["final_ref"],
            build_final_receipt_index_ref=fixture["build_final_index_ref"],
        )


def test_hash_consistent_result_review_command_tamper_is_rejected(tmp_path: Path) -> None:
    with pytest.raises(EvidenceValidationError, match="result_review_binding receipt argv"):
        _stable_publication_fixture(
            tmp_path / "result_review_binding",
            command_argv_tamper_action="result_review_binding",
        )


@pytest.mark.parametrize(
    "action",
    ("build_final_candidate", "final_candidate_gate", "final_seal_audit_binding"),
)
def test_hash_consistent_suffix_command_tamper_blocks_publication(tmp_path: Path, action: str) -> None:
    root = tmp_path / action
    fixture = _stable_publication_fixture(root, command_argv_tamper_action=action)
    with pytest.raises(EvidenceValidationError, match=rf"{action} receipt argv"):
        publish_stable_phase_decision(
            root,
            candidate_ref=fixture["final_ref"],
            review_ref=fixture["review_ref"],
            audit_ref=fixture["audit_ref"],
            validation_log_ref=fixture["validation_ref"],
            governance_receipt_index_ref=fixture["terminal_index_ref"],
            stable_ref=fixture["stable_ref"],
        )


@pytest.mark.parametrize(
    "case_id,mutate",
    (
        (
            "criterion",
            lambda candidate: candidate["primary_criterion"].update(
                canonical_vectors_pass=False,
                all_pass=False,
            ),
        ),
        (
            "veto",
            lambda candidate: candidate["vetoes"].update(canonical_identity_failure=True),
        ),
        (
            "non_claim",
            lambda candidate: candidate["non_claims"].remove("no_release_readiness"),
        ),
        (
            "predecessor",
            lambda candidate: candidate["predecessor"].update(
                entry_protected_manifest_sha256="0" * 64,
            ),
        ),
    ),
)
def test_candidate_semantic_field_tamper_is_rejected(
    tmp_path: Path,
    case_id: str,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    root = tmp_path / case_id
    fixture = _stable_publication_fixture(root)
    candidate = strict_load_canonical_json(root / fixture["candidate_ref"], schema="p01_candidate_decision@1")
    mutate(candidate)
    try:
        _replace_canonical_record(root, fixture["candidate_ref"], candidate, "p01_candidate_decision@1")
    except EvidenceValidationError:
        return
    with pytest.raises(EvidenceValidationError):
        verify_p01_candidate(
            root,
            candidate_ref=fixture["candidate_ref"],
            build_run_receipt_index_ref=fixture["build_run_index_ref"],
        )


@pytest.mark.parametrize(
    "case_id,mutate",
    (
        ("git_commit", lambda run: run.update(git_commit="b" * 40)),
        ("implementation_delta", lambda run: run.update(implementation_diff_digest="c" * 64)),
        (
            "test_runner",
            lambda run: run["environment"].update(test_runner_version="pytest-0.0.0"),
        ),
        ("wall_time", lambda run: run.update(wall_time_ns=run["wall_time_ns"] + 1)),
        ("receipt_inventory", lambda run: run["artifact_inventory"].pop()),
    ),
)
def test_run_manifest_semantic_provenance_tamper_is_rejected(
    tmp_path: Path,
    case_id: str,
    mutate: Callable[[dict[str, Any]], None],
) -> None:
    root = tmp_path / case_id
    fixture = _stable_publication_fixture(root)
    run = strict_load_canonical_json(root / fixture["run_ref"], schema="p01_run_manifest@1")
    mutate(run)
    _replace_canonical_record(root, fixture["run_ref"], run, "p01_run_manifest@1")
    with pytest.raises(EvidenceValidationError, match="independent reconstruction"):
        verify_p01_run_manifest(
            root,
            run_manifest_ref=fixture["run_ref"],
            bind_result_receipt_index_ref=run["pre_candidate_receipt_index_ref"],
        )


@pytest.mark.parametrize(
    "case_id,overrides",
    (
        ("python_executable", {"python_executable": "/tmp/alternate-python"}),
        ("pythonpath", {"pythonpath": "tests"}),
        ("git_commit_shape", {"git_commit": "not-a-commit"}),
    ),
)
def test_init_environment_provenance_mismatch_is_rejected(
    tmp_path: Path,
    case_id: str,
    overrides: dict[str, str],
) -> None:
    with pytest.raises(EvidenceValidationError):
        _stable_publication_fixture(tmp_path / case_id, init_measurement_overrides=overrides)


@pytest.mark.parametrize("summary_name", ("mutation", "parallel", "legacy", "generator"))
def test_each_source_summary_semantic_tamper_is_rejected(tmp_path: Path, summary_name: str) -> None:
    root = tmp_path / summary_name
    fixture = _stable_publication_fixture(root)
    schemas = {
        "mutation": "p01_mutation_summary@1",
        "parallel": "p01_parallel_summary@1",
        "legacy": "p01_legacy_summary@1",
        "generator": "p01_generator_result@1",
    }
    ref = fixture["summary_refs"][summary_name]
    record = strict_load_canonical_json(root / ref, schema=schemas[summary_name])
    if summary_name == "mutation":
        record["cases"][0]["case_id"] = "wrong_case"
    elif summary_name == "parallel":
        record["cases"][0]["case_id"] = "wrong_case"
    elif summary_name == "legacy":
        record["cases"][0]["expected_certification_state"] = "wrong_state"
    else:
        record["invariant_ids"][0] = "wrong_invariant"
    _replace_canonical_record(root, ref, record, schemas[summary_name])
    with pytest.raises(EvidenceValidationError):
        reconstruct_p01_candidate(root, fixture["build_run_index_ref"])


@pytest.mark.parametrize(
    "case_id,kwargs",
    (
        ("receipt_stdout", {"candidate_gate_stdout_override": b'{"status":"STALE"}\n'}),
        ("validation_log", {"candidate_validation_override": b'{"status":"STALE"}\n'}),
    ),
)
def test_stable_publication_rejects_candidate_report_mismatch(
    tmp_path: Path,
    case_id: str,
    kwargs: dict[str, bytes],
) -> None:
    root = tmp_path / case_id
    with pytest.raises(EvidenceValidationError, match="candidate validation report"):
        fixture = _stable_publication_fixture(root, **kwargs)
        publish_stable_phase_decision(
            root,
            candidate_ref=fixture["final_ref"],
            review_ref=fixture["review_ref"],
            audit_ref=fixture["audit_ref"],
            validation_log_ref=fixture["validation_ref"],
            governance_receipt_index_ref=fixture["terminal_index_ref"],
            stable_ref=fixture["stable_ref"],
        )


def test_required_mutation_contract_includes_result_truncation() -> None:
    assert P01_REQUIRED_MUTATION_CASES[16] == ("result_truncation", "result_not_truncated")
    assert len(P01_REQUIRED_MUTATION_CASES) == 21


def test_legacy_normalization_never_manufactures_v1_authority() -> None:
    cases = (
        ({"status": "proved", "can_promote": True, "output_ref": "mathdevmcp://legacy/success"}, "unbound_legacy_evidence"),
        ({"schema_version": "1.0", "status": "proved"}, "invalid_or_partial_v1"),
        ({"schema_version": "1.1", "status": "proved"}, "invalid_or_partial_v1"),
        ({"schema_version": "2.0", "status": "proved"}, "unknown_major_schema"),
    )
    for value, expected in cases:
        normalized = normalize_legacy_evidence(value)
        assert normalized["publication_enabled"] is False
        assert normalized["claim_eligibility"] == "ineligible"
        assert normalized["certification_state"] == expected
        assert normalized["certification_state"] != "verified"


def test_additive_minor_manifest_is_renderable_only_after_base_validation(tmp_path: Path) -> None:
    _, _, sealed = _sealed_bundle(tmp_path)
    extended = deepcopy(sealed["manifest"])
    extended["schema_version"] = "1.1"
    extended["additive_note"] = "diagnostic metadata"
    without_digest = dict(extended)
    without_digest.pop("evidence_manifest_digest")
    extended["evidence_manifest_digest"] = content_digest(without_digest)

    normalized = normalize_legacy_evidence(extended)
    assert normalized["schema_version"] == "1.1"
    assert normalized["certification_state"] == "sealed_pending_reader_verification"
    assert normalized["ignored_additive_metadata"] == ["additive_note"]
    assert normalized["claim_eligibility"] == "ineligible"
    assert normalized["publication_enabled"] is False

    extended["request"]["source"]["digest"] = "0" * 64
    normalized = normalize_legacy_evidence(extended)
    assert normalized["certification_state"] == "invalid_or_partial_v1"
