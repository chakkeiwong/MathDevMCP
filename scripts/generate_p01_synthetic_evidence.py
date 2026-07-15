#!/usr/bin/env python3
from __future__ import annotations

"""Generate durable fake-only Phase 01 evidence below one result round."""

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import stat
import threading
from typing import Any

from mathdevmcp.evidence_manifest import (
    P01_NON_CLAIMS,
    allocate_execution,
    atomic_write_artifact,
    atomic_write_canonical_record,
    build_evidence_request,
    canonical_json_bytes,
    content_digest,
    create_run_bundle,
    normalize_legacy_evidence,
    seal_attempt_manifest,
    seal_bundle_index,
    verify_attempt_manifest,
    verify_bundle_index,
)
from mathdevmcp.promotion_policy import INVARIANT_IDS, evaluate_promotion


ROUND_RE = re.compile(r"^rr0[1-5]$")
SOURCE_BYTES = b"x + 1 = 1 + x"
NATIVE_BYTES = b"check(x + 1 = 1 + x)"
EDIT_BYTES = b"x + 1 = 1 + x"
TARGET = "x + 1 = 1 + x"


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _safe_round_root(value: str) -> tuple[Path, Path, str]:
    if not value or "\x00" in value or "\\" in value or ".." in Path(value).parts:
        raise ValueError("round root must be a normalized local path")
    repo = Path.cwd().absolute()
    round_root = Path(value)
    if not round_root.is_absolute():
        round_root = repo / round_root
    round_root = round_root.absolute()
    expected_parent = repo / ".local" / "mathdevmcp" / "evidence" / "p01-20260711" / "result-rounds"
    if round_root.parent != expected_parent or not ROUND_RE.fullmatch(round_root.name):
        raise ValueError("round root is outside the fixed Phase 01 result-rounds root")
    current = repo
    for part in round_root.relative_to(repo).parts:
        current = current / part
        if current.exists() or current.is_symlink():
            info = current.lstat()
            if stat.S_ISLNK(info.st_mode) or (current != round_root and not stat.S_ISDIR(info.st_mode)):
                raise ValueError(f"unsafe round-root component: {current}")
    if not round_root.is_dir() or round_root.is_symlink():
        raise ValueError("round root must be an existing no-follow directory")
    return round_root, expected_parent.parent, round_root.name


def _request() -> dict[str, Any]:
    assumptions = [{"id": "scalar", "kind": "domain", "statement": "x is a real scalar."}]
    return build_evidence_request(
        source={
            "logical_id": "synthetic/source.tex",
            "file": "synthetic/source.tex",
            "label": "eq:synthetic",
            "digest": _digest(SOURCE_BYTES),
            "spans": [{"start_byte": 0, "end_byte": len(SOURCE_BYTES)}],
            "parser_version": "p01-synthetic-1",
        },
        obligation={"digest": _digest(TARGET.encode("utf-8")), "target": TARGET},
        branch={"id": "branch_synthetic", "lineage": ["root", "branch_synthetic"]},
        typed_assumptions=assumptions,
        assumption_digest=content_digest(assumptions),
        native_input={"digest": _digest(NATIVE_BYTES), "media_type": "text/plain"},
        tool={
            "name": "fake",
            "adapter_version": "p01-generator-1",
            "backend_version": "synthetic",
            "executable_id": "embedded_fake_runner",
        },
        resource_limits={"timeout_ms": 1000, "max_output_bytes": 4096},
        expected_result_class="synthetic_integrity_fixture",
        backend_role="test_only_noncertifying",
        unsupported_conclusions=list(P01_NON_CLAIMS),
        policy_version="p01_integrity_binding@1",
    )


def _execution_record() -> dict[str, Any]:
    return {
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
            "test_runner_version": "p01-generator",
        },
        "runner_version": "embedded-fake-runner-1",
    }


def _seal_execution(bundle, request, allocation) -> dict[str, Any]:
    native = atomic_write_artifact(
        bundle,
        f"{allocation.logical_root}/native-input.txt",
        NATIVE_BYTES,
        media_type="text/plain",
        role="native_input",
    )
    stdout = atomic_write_artifact(
        bundle,
        f"{allocation.logical_root}/stdout.txt",
        b"synthetic fixture only\n",
        media_type="text/plain",
        role="stdout",
    )
    stderr = atomic_write_artifact(
        bundle,
        f"{allocation.logical_root}/stderr.txt",
        b"",
        media_type="text/plain",
        role="stderr",
    )
    structured_bytes = canonical_json_bytes({"status": "synthetic_certified_fixture"})
    structured = atomic_write_artifact(
        bundle,
        f"{allocation.logical_root}/result.json",
        structured_bytes,
        media_type="application/json",
        role="structured_result",
    )
    sealed = seal_attempt_manifest(
        bundle,
        request,
        allocation,
        [native, stdout, stderr, structured],
        execution_record=_execution_record(),
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
    return verify_attempt_manifest(bundle.root, sealed["manifest_ref"])


def _policy_fixture(verified: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    request = verified["manifest"]["request"]
    source = {
        "bytes": SOURCE_BYTES,
        "spans": request["source"]["spans"],
        "label": request["source"]["label"],
        "edit_span": {"start_byte": 0, "end_byte": len(SOURCE_BYTES)},
    }
    branch = {
        "id": request["branch"]["id"],
        "lineage": request["branch"]["lineage"],
        "obligation_digest": request["obligation"]["digest"],
        "normalized_target": request["obligation"]["target"],
        "typed_assumptions": request["typed_assumptions"],
    }
    edit = {
        "bytes": EDIT_BYTES,
        "digest": _digest(EDIT_BYTES),
        "source_digest": _digest(SOURCE_BYTES),
        "label": request["source"]["label"],
        "span": source["edit_span"],
    }
    policy = {
        "native_input_bytes": NATIVE_BYTES,
        "tool": request["tool"],
        "backend_role": request["backend_role"],
        "allowed_outcomes": ["certified"],
        "evidence_vetoes": [],
        "engineering_vetoes": [],
        "conflict_detected": False,
        "publication_enabled": False,
    }
    return [verified], source, branch, edit, policy


def _reseal_verified(case: list[Any]) -> None:
    verified = case[0][0]
    manifest = verified["manifest"]
    without_digest = dict(manifest)
    without_digest.pop("evidence_manifest_digest")
    manifest["evidence_manifest_digest"] = content_digest(without_digest)
    verified["manifest_sha256"] = content_digest(canonical_json_bytes(manifest, schema="evidence_manifest@1"))


def _mutation_cases(base: tuple[Any, ...]) -> list[dict[str, Any]]:
    mutations: list[tuple[str, str, Any]] = []

    def add(case_id: str, expected: str, mutate) -> None:
        case = deepcopy(base)
        mutate(case)
        result = evaluate_promotion(*case)
        observed = list(result["failed_invariant_ids"])
        mutations.append((case_id, expected, observed))

    add("source_bytes", "source_digest", lambda case: case[1].update(bytes=b"changed source"))
    add("source_span", "source_span", lambda case: case[1].update(spans=[{"start_byte": 1, "end_byte": 2}]))
    add("source_label", "source_label", lambda case: case[1].update(label="eq:other"))
    add("target", "normalized_target", lambda case: case[2].update(normalized_target="x = x"))
    add("obligation", "obligation_digest", lambda case: case[2].update(obligation_digest="0" * 64))
    add("assumptions", "typed_assumptions", lambda case: case[2].update(typed_assumptions=[]))
    add("branch", "branch_id", lambda case: case[2].update(id="branch_other"))
    add("lineage", "branch_lineage", lambda case: case[2].update(lineage=["root", "branch_other"]))
    add("native_input", "native_input_digest", lambda case: case[4].update(native_input_bytes=b"changed native"))
    add("tool_version", "tool_identity", lambda case: case[4]["tool"].update(backend_version="other"))
    add("backend_role", "backend_role", lambda case: case[4].update(backend_role="other"))
    add("conflict", "no_conflict", lambda case: case[4].update(conflict_detected=True))
    add("edit_bytes", "candidate_edit_binding", lambda case: case[3].update(bytes=b"changed edit"))
    add("edit_span", "candidate_edit_binding", lambda case: case[3].update(span={"start_byte": 1, "end_byte": 2}))
    add("publication_flag", "publication_quarantine", lambda case: case[4].update(publication_enabled=True))

    def mutate_outcome(case) -> None:
        manifest = case[0][0]["manifest"]
        manifest["result"]["outcome"] = "unknown"
        manifest["interpretation"]["certified_scope"] = None
        _reseal_verified(case)

    add("result_outcome", "result_outcome", mutate_outcome)

    def mutate_truncation(case) -> None:
        case[0][0]["manifest"]["result"]["stdout_truncated"] = True
        _reseal_verified(case)

    add("result_truncation", "result_not_truncated", mutate_truncation)

    def mutate_role(case) -> None:
        manifest = case[0][0]["manifest"]
        ref = manifest["result"]["structured_result"]["logical_ref"]
        manifest["result"]["structured_result"]["role"] = "wrong_role"
        for entry in manifest["integrity"]["artifact_inventory"]:
            if entry["logical_ref"] == ref:
                entry["role"] = "wrong_role"
        _reseal_verified(case)

    add("artifact_role", "sealed_inventory", mutate_role)

    def mutate_inventory(case) -> None:
        manifest = case[0][0]["manifest"]
        manifest["integrity"]["artifact_inventory"].append(
            {
                "logical_ref": "unexpected.bin",
                "media_type": "application/octet-stream",
                "sha256": _digest(b"unexpected"),
                "byte_count": len(b"unexpected"),
                "role": "unexpected",
            }
        )
        _reseal_verified(case)

    add("artifact_inventory", "sealed_inventory", mutate_inventory)
    add("evidence_veto", "no_evidence_vetoes", lambda case: case[4].update(evidence_vetoes=["synthetic_veto"]))
    add("engineering_veto", "no_engineering_vetoes", lambda case: case[4].update(engineering_vetoes=["synthetic_error"]))

    return [
        {
            "case_id": case_id,
            "mutated_field": case_id,
            "expected_veto_id": expected,
            "observed_veto_ids": observed,
            "passed": expected in observed,
        }
        for case_id, expected, observed in mutations
    ]


def _legacy_cases() -> list[dict[str, Any]]:
    fixtures = (
        ("current_v0", {"status": "proved", "can_promote": True}, "unbound_legacy_evidence"),
        ("legacy_uri", {"status": "proved", "output_ref": "mathdevmcp://legacy/success"}, "unbound_legacy_evidence"),
        ("partial_v1", {"schema_version": "1.0", "status": "proved"}, "invalid_or_partial_v1"),
        ("unknown_major", {"schema_version": "2.0", "status": "proved"}, "unknown_major_schema"),
    )
    cases = []
    for case_id, value, expected in fixtures:
        normalized = normalize_legacy_evidence(value)
        observed = normalized["certification_state"]
        cases.append(
            {
                "case_id": case_id,
                "input_schema_class": str(value.get("schema_version", "0-legacy")),
                "expected_certification_state": expected,
                "observed_certification_state": observed,
                "passed": observed == expected
                and normalized["claim_eligibility"] == "ineligible"
                and normalized["publication_enabled"] is False,
            }
        )
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("--round-root", required=True)
    args = parser.parse_args()
    round_root, _, result_round = _safe_round_root(args.round_root)
    bundle_parent = round_root / "synthetic-bundle"
    summaries = round_root / "summaries"
    if bundle_parent.exists() or bundle_parent.is_symlink() or summaries.exists() or summaries.is_symlink():
        raise RuntimeError("generator outputs must all be absent")

    request = _request()
    primary = create_run_bundle(bundle_parent)
    allocations = []
    allocation_lock = threading.Lock()

    def allocate() -> None:
        allocation = allocate_execution(primary, request)
        with allocation_lock:
            allocations.append(allocation)

    threads = [threading.Thread(target=allocate) for _ in range(4)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    allocations.sort(key=lambda item: item.execution_id)
    verified_attempts = [_seal_execution(primary, request, allocation) for allocation in allocations]
    primary_index = seal_bundle_index(primary)
    primary_disk = verify_bundle_index(primary.root)

    comparison = create_run_bundle(bundle_parent)
    comparison_allocation = allocate_execution(comparison, request)
    _seal_execution(comparison, request, comparison_allocation)
    seal_bundle_index(comparison)
    comparison_disk = verify_bundle_index(comparison.root)

    request_equal = len({allocation.request_digest for allocation in allocations}) == 1
    attempt_equal = len({allocation.attempt_id for allocation in allocations}) == 1
    execution_distinct = len({allocation.execution_id for allocation in allocations}) == len(allocations)
    run_distinct = primary.run_id != comparison.run_id
    deterministic_index = [
        item["logical_ref"] for item in primary_disk["record"]["artifacts"]
    ] == sorted(item["logical_ref"] for item in primary_disk["record"]["artifacts"])
    parallel_cases = [
        {
            "case_id": "identical_request_thread_and_run_identity",
            "request_equal": request_equal,
            "attempt_equal": attempt_equal,
            "execution_distinct": execution_distinct,
            "run_distinct": run_distinct,
            "deterministic_index": deterministic_index,
            "passed": request_equal and attempt_equal and execution_distinct and run_distinct and deterministic_index,
        }
    ]

    base = _policy_fixture(verified_attempts[0])
    baseline_policy = evaluate_promotion(*base)
    mutation_cases = _mutation_cases(base)
    legacy_cases = _legacy_cases()
    prefix = round_root.relative_to(Path.cwd().absolute()).as_posix()
    mutation_record = {
        "schema_version": "p01_mutation_summary@1",
        "phase": "P01",
        "result_round": result_round,
        "cases": mutation_cases,
        "all_pass": all(item["passed"] for item in mutation_cases),
    }
    parallel_record = {
        "schema_version": "p01_parallel_summary@1",
        "phase": "P01",
        "result_round": result_round,
        "cases": parallel_cases,
        "all_pass": all(item["passed"] for item in parallel_cases),
    }
    legacy_record = {
        "schema_version": "p01_legacy_summary@1",
        "phase": "P01",
        "result_round": result_round,
        "cases": legacy_cases,
        "all_pass": all(item["passed"] for item in legacy_cases),
    }
    generator_pass = (
        baseline_policy["integrity_binding_verified"] is True
        and baseline_policy["claim_eligibility"] == "ineligible"
        and baseline_policy["publication_enabled"] is False
        and mutation_record["all_pass"]
        and parallel_record["all_pass"]
        and legacy_record["all_pass"]
        and primary_disk["disk_verification_state"] == "verified"
        and comparison_disk["disk_verification_state"] == "verified"
    )
    generator_record = {
        "schema_version": "p01_generator_result@1",
        "phase": "P01",
        "result_round": result_round,
        "bundle_ref": f"{prefix}/synthetic-bundle/{primary.run_id}",
        "payload_bundle_index_digest": primary_index["payload_bundle_index_digest"],
        "payload_bundle_index_file_sha256": primary_index["payload_bundle_index_file_sha256"],
        "disk_verification_state": primary_disk["disk_verification_state"],
        "invariant_ids": list(INVARIANT_IDS),
        "all_pass": generator_pass,
    }
    records = (
        ("summaries/mutation-matrix.json", mutation_record, "p01_mutation_summary@1"),
        ("summaries/serial-parallel-identity.json", parallel_record, "p01_parallel_summary@1"),
        ("summaries/legacy-matrix.json", legacy_record, "p01_legacy_summary@1"),
        ("summaries/generator-result.json", generator_record, "p01_generator_result@1"),
    )
    for logical_ref, record, schema in records:
        atomic_write_canonical_record(round_root, logical_ref, record, schema=schema)

    status = {
        "all_pass": generator_pass,
        "bundle_ref": generator_record["bundle_ref"],
        "mutation_case_count": len(mutation_cases),
        "result_round": result_round,
        "status": "PASS" if generator_pass else "FAIL",
    }
    print(json.dumps(status, sort_keys=True, separators=(",", ":")))
    return 0 if generator_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
