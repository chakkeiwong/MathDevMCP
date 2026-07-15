#!/usr/bin/env python3
from __future__ import annotations

"""Append-only measured governance for the Phase 01 evidence-integrity gate."""

import argparse
import ast
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import platform
import re
import stat
import subprocess
import sys
import time
from typing import Any, Callable

from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    P01_ENTRY_ROOT_REF,
    P01_EVIDENCE_ROOT_REF,
    P01_NON_CLAIMS,
    P01_PASS_ACTION_SEQUENCE,
    P01_PLAN_REF,
    P01_PYTHON,
    P01_RECEIPT_BINDING_KEYS,
    P01_VETO_KEYS,
    atomic_write_bytes_no_replace,
    atomic_write_canonical_record,
    canonical_json_bytes,
    content_digest,
    p01_fixed_action_argv,
    p01_governance_action_argv,
    publish_stable_phase_decision,
    read_bytes_no_follow,
    reconstruct_p01_candidate,
    reconstruct_p01_final_decision,
    reconstruct_p01_run_manifest,
    strict_load_canonical_json,
    verify_bootstrap_close,
    verify_bundle_index,
    verify_final_seal_audit_bindings,
    verify_receipt_index,
    verify_result_review_bindings,
    verify_p01_candidate,
    verify_p01_final_decision_candidate,
)


PYTHON = P01_PYTHON
PLAN_REF = P01_PLAN_REF
ENTRY_ROOT_REF = P01_ENTRY_ROOT_REF
EVIDENCE_ROOT_REF = P01_EVIDENCE_ROOT_REF
ROUND_RE = re.compile(r"^rr0[1-5]$")
UTC_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

CHECK_ACTIONS = P01_PASS_ACTION_SEQUENCE[1:14]
RUN_ACTIONS = (
    *CHECK_ACTIONS,
    "bind_result",
    "build_run_manifest",
    "build_candidate",
    "candidate_gate",
    "result_review_binding",
    "build_final_candidate",
    "final_candidate_gate",
    "final_seal_audit_binding",
    "bind_scoped_repair",
    "close_round",
    "stable_publication",
)

IMPLEMENTATION_ALLOWLIST = frozenset(
    {
        "src/mathdevmcp/evidence_manifest.py",
        "src/mathdevmcp/promotion_policy.py",
        "src/mathdevmcp/external_tool_adapters.py",
        "src/mathdevmcp/derivation_search_tree.py",
        "src/mathdevmcp/derivation_branch_controller.py",
        "src/mathdevmcp/document_derivation_tree.py",
        "tests/test_evidence_manifest.py",
        "tests/test_promotion_policy.py",
        "tests/test_external_tool_adapters.py",
        "tests/test_derivation_search_tree.py",
        "tests/test_derivation_branch_controller.py",
        "tests/test_document_derivation_tree.py",
        "tests/test_document_publication_quarantine.py",
        "scripts/generate_p01_synthetic_evidence.py",
        "scripts/p01_bootstrap_gate.sh",
        "scripts/p01_governance.py",
    }
)

P00_NODES = (
    "test_simple_algebra_is_partial_evidence_not_repair",
    "test_x_over_x_preserves_nonzero_requirement_after_raw_backend_success",
    "test_latex_sqrt_preserves_real_domain_requirement",
    "test_siblings_collision_and_edit_mismatch_remain_legacy_unbound",
    "test_edit_target_mismatch_cannot_bypass_compiler_quarantine",
    "test_adapter_exception_is_engineering_error_not_only_math_gap",
    "test_serial_and_parallel_worker_exceptions_are_engineering_errors",
    "test_library_facade_server_and_cli_have_quarantine_parity",
    "test_emergency_kill_switch_returns_before_source_access_on_all_surfaces",
    "test_lower_level_controller_contract_remains_raw_and_unchanged",
    "test_phase01_document_surfaces_remain_ineligible_and_publication_false",
)


def _repo_root() -> Path:
    root = Path.cwd().absolute()
    if not (root / ".git").is_dir() or not (root / "src" / "mathdevmcp").is_dir():
        raise EvidenceValidationError("p01_governance.py must run from the MathDevMCP repository root")
    return root


def _logical_ref(root: Path, value: str | os.PathLike[str]) -> str:
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    path = path.absolute()
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise EvidenceValidationError("path is outside the repository trust root") from exc
    ref = relative.as_posix()
    if ".." in relative.parts or not ref:
        raise EvidenceValidationError("path is not a normalized workspace-relative ref")
    return ref


def _round_context(root: Path, value: str | os.PathLike[str], *, must_exist: bool) -> tuple[str, str, Path]:
    ref = _logical_ref(root, value)
    pure = PurePosixPath(ref)
    expected = PurePosixPath(EVIDENCE_ROOT_REF) / "result-rounds"
    if pure.parent != expected or not ROUND_RE.fullmatch(pure.name):
        raise EvidenceValidationError("round root is outside the fixed P01 result-rounds root")
    path = root / ref
    current = root
    for part in pure.parts:
        current = current / part
        if current.exists() or current.is_symlink():
            info = current.lstat()
            if stat.S_ISLNK(info.st_mode) or (current != path and not stat.S_ISDIR(info.st_mode)):
                raise EvidenceValidationError(f"unsafe round path component: {current}")
    if must_exist and (not path.is_dir() or path.is_symlink()):
        raise EvidenceValidationError("round root must be an existing no-follow directory")
    if not must_exist and (path.exists() or path.is_symlink()):
        raise EvidenceValidationError("round root must be absent")
    return ref, pure.name, path


def _digest_ref(root: Path, ref: str) -> str:
    data, _ = read_bytes_no_follow(root, ref)
    return content_digest(data)


def _manifest_bytes(root: Path) -> bytes:
    paths = sorted(
        (
            path
            for top in (root / "src", root / "tests", root / "scripts")
            for path in top.rglob("*")
            if path.is_file()
            and not path.is_symlink()
            and "__pycache__" not in path.parts
            and path.suffix not in {".pyc", ".pyo"}
        ),
        key=lambda path: path.relative_to(root).as_posix().encode("utf-8"),
    )
    return b"".join(
        f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.relative_to(root).as_posix()}\n".encode("utf-8")
        for path in paths
    )


def _entry_protected_digest(root: Path) -> str:
    data, _ = read_bytes_no_follow(root, f"{ENTRY_ROOT_REF}/protected-dirty-sha256.txt")
    lines = data.splitlines(keepends=True)
    if len(lines) < 11:
        raise EvidenceValidationError("entry protected manifest has fewer than the frozen 11 records")
    return content_digest(b"".join(lines[:11]))


def _parse_sha256_manifest(data: bytes) -> dict[str, str]:
    try:
        text = data.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("implementation manifest is not strict UTF-8") from exc
    result: dict[str, str] = {}
    for line in text.splitlines():
        digest, separator, ref = line.partition("  ")
        if separator != "  " or not re.fullmatch(r"[0-9a-f]{64}", digest) or not ref or ref in result:
            raise EvidenceValidationError("implementation manifest has invalid sha256sum grammar")
        result[ref] = digest
    return result


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _receipt_chain(root: Path, round_ref: str) -> dict[str, Any] | None:
    receipts_dir = root / round_ref / "receipts"
    if not receipts_dir.exists():
        return None
    if receipts_dir.is_symlink() or not receipts_dir.is_dir():
        raise EvidenceValidationError("receipt directory is unsafe")
    candidates = sorted(receipts_dir.glob("receipt-index-*.json"), key=lambda path: path.name)
    if not candidates:
        return None
    refs = [_logical_ref(root, path) for path in candidates]
    verified = [verify_receipt_index(root, ref) for ref in refs]
    for expected, item in enumerate(verified, start=1):
        if item["record"]["head_sequence"] != expected:
            raise EvidenceValidationError("receipt-index snapshots are not contiguous")
        if item["record"]["receipts"] != verified[-1]["record"]["receipts"][:expected]:
            raise EvidenceValidationError("receipt-index snapshots are not immutable prefixes")
    return verified[-1]


def _write_receipt(
    root: Path,
    round_ref: str,
    result_round: str,
    check_id: str,
    command_argv: list[str],
    started_at: str,
    ended_at: str,
    wall_time_ns: int,
    exit_code: int,
    stdout_ref: str,
    stderr_ref: str,
    bindings: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    chain = _receipt_chain(root, round_ref)
    previous_entries = [] if chain is None else chain["record"]["receipts"]
    sequence = len(previous_entries) + 1
    prior = None if chain is None else chain["record"]["head_sha256"]
    stdout, _ = read_bytes_no_follow(root, stdout_ref)
    stderr, _ = read_bytes_no_follow(root, stderr_ref)
    receipt = {
        "schema_version": "p01_command_receipt@1",
        "phase": "P01",
        "result_round": result_round,
        "sequence": sequence,
        "check_id": check_id,
        "command_argv": command_argv,
        "started_at_utc": started_at,
        "ended_at_utc": ended_at,
        "wall_time_ns": wall_time_ns,
        "exit_code": exit_code,
        "stdout_ref": stdout_ref,
        "stdout_sha256": content_digest(stdout),
        "stdout_byte_count": len(stdout),
        "stderr_ref": stderr_ref,
        "stderr_sha256": content_digest(stderr),
        "stderr_byte_count": len(stderr),
        "prior_receipt_sha256": prior,
        "bindings": bindings,
    }
    receipt_ref = f"{round_ref}/receipts/receipt-{sequence:02d}.json"
    written = atomic_write_canonical_record(root, receipt_ref, receipt, schema="p01_command_receipt@1")
    entry = {
        "sequence": sequence,
        "check_id": check_id,
        "receipt_ref": receipt_ref,
        "receipt_sha256": written["sha256"],
    }
    entries = [*previous_entries, entry]
    index = {
        "schema_version": "p01_receipt_index@1",
        "phase": "P01",
        "result_round": result_round,
        "receipts": entries,
        "head_sequence": sequence,
        "head_sha256": written["sha256"],
    }
    index_ref = f"{round_ref}/receipts/receipt-index-{sequence:02d}.json"
    index_written = atomic_write_canonical_record(root, index_ref, index, schema="p01_receipt_index@1")
    verified = verify_receipt_index(root, index_ref)
    if verified["index_sha256"] != index_written["sha256"]:
        raise EvidenceValidationError("new receipt index failed immediate verification")
    return {"record": receipt, "ref": receipt_ref, "sha256": written["sha256"]}, verified


def _run_command(root: Path, argv: list[str]) -> tuple[int, bytes, bytes]:
    environment = {**os.environ, "PYTHONPATH": "src"}
    completed = subprocess.run(argv, cwd=root, env=environment, check=False, capture_output=True)
    return completed.returncode, completed.stdout, completed.stderr


def _fixed_argv(root: Path, round_ref: str, result_round: str, action: str) -> list[str] | None:
    _ = root, result_round
    return p01_fixed_action_argv(round_ref, action)


def _changed_paths(root: Path, round_ref: str) -> tuple[list[str], bytes, bytes]:
    entry, _ = read_bytes_no_follow(root, f"{ENTRY_ROOT_REF}/implementation-entry-sha256.txt")
    current, _ = read_bytes_no_follow(root, f"{round_ref}/implementation-exit-sha256.txt")
    before = _parse_sha256_manifest(entry)
    after = _parse_sha256_manifest(current)
    changed = sorted(
        {ref for ref in set(before) | set(after) if before.get(ref) != after.get(ref)},
        key=lambda ref: ref.encode("utf-8"),
    )
    unexpected = sorted(set(changed) - IMPLEMENTATION_ALLOWLIST, key=lambda ref: ref.encode("utf-8"))
    return changed, "".join(f"{ref}\n" for ref in changed).encode(), "".join(f"{ref}\n" for ref in unexpected).encode()


def _internal_check(root: Path, round_ref: str, result_round: str, action: str) -> tuple[int, bytes, bytes, dict[str, Any]]:
    if action == "implementation_exit":
        manifest = _manifest_bytes(root)
        ref = f"{round_ref}/implementation-exit-check-sha256.txt"
        atomic_write_bytes_no_replace(root, ref, manifest)
        initialized, _ = read_bytes_no_follow(root, f"{round_ref}/implementation-exit-sha256.txt")
        passed = manifest == initialized
        return (
            0 if passed else 1,
            json.dumps({"manifest_equal": passed, "manifest_sha256": content_digest(manifest)}, sort_keys=True).encode() + b"\n",
            b"" if passed else b"implementation manifest drifted after init-round\n",
            {"manifest_ref": f"{round_ref}/implementation-exit-sha256.txt", "manifest_sha256": content_digest(initialized)},
        )
    if action == "allowlist":
        changed, touched, unexpected = _changed_paths(root, round_ref)
        atomic_write_bytes_no_replace(root, f"{round_ref}/touched-files.txt", touched)
        atomic_write_bytes_no_replace(root, f"{round_ref}/unexpected-touched-files.txt", unexpected)
        return (
            0 if not unexpected else 1,
            json.dumps({"changed_paths": changed, "unexpected_count": len(unexpected)}, sort_keys=True).encode() + b"\n",
            unexpected,
            {},
        )
    if action == "assignment_audit":
        audit_terms = (
            "publishable_as_repair",
            "publication_enabled",
            "claim_eligibility",
            "exact_manifest_eligible",
            "evidence_schema_version",
            "integrity_binding_status",
        )
        forbidden_generator = (
            "derive_or_refute",
            "find_counterexample",
            "check_lean_source",
            "subprocess",
            "socket",
            "requests",
            "urllib",
        )
        generator = (root / "scripts/generate_p01_synthetic_evidence.py").read_text(encoding="utf-8")
        violations = [term for term in forbidden_generator if term in generator]
        governance = (root / "scripts/p01_governance.py").read_text(encoding="utf-8")
        tree = ast.parse(governance)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
                violations.append("unsafe_governance_evaluation")
            if isinstance(node, ast.Call) and any(
                keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True
                for keyword in node.keywords
            ):
                violations.append("unsafe_governance_shell")
        bootstrap = (root / "scripts/p01_bootstrap_gate.sh").read_text(encoding="utf-8")
        forbidden_shell_tokens = ("e" + "val ", "sour" + "ce ")
        if any(token in bootstrap for token in forbidden_shell_tokens):
            violations.append("unsafe_bootstrap_evaluation")
        matched = []
        for ref in (
            "src/mathdevmcp/document_derivation_tree.py",
            "src/mathdevmcp/evidence_manifest.py",
            "src/mathdevmcp/promotion_policy.py",
            "tests/test_document_publication_quarantine.py",
        ):
            text = (root / ref).read_text(encoding="utf-8")
            matched.extend(f"{ref}:{line_no}:{line}" for line_no, line in enumerate(text.splitlines(), 1) if any(term in line for term in audit_terms))
        output = ("\n".join(matched) + "\n").encode("utf-8")
        error = ("\n".join(violations) + ("\n" if violations else "")).encode("utf-8")
        return 0 if not violations else 1, output, error, {}
    raise EvidenceValidationError(f"no internal check implementation for {action}")


def _current_state(chain: dict[str, Any] | None) -> tuple[list[str], list[int]]:
    if chain is None:
        return [], []
    return (
        [item["record"]["check_id"] for item in chain["receipts"]],
        [item["record"]["exit_code"] for item in chain["receipts"]],
    )


def _expected_action(root: Path, chain: dict[str, Any] | None) -> str:
    actions, exits = _current_state(chain)
    if not actions or actions[0] != "init_round":
        raise EvidenceValidationError("round does not have a valid init_round receipt")
    if actions[-1] in {"stable_publication", "close_round"}:
        raise EvidenceValidationError("round is terminal")
    if any(code != 0 for code in exits):
        failed_actions = [action for action, code in zip(actions, exits, strict=True) if code != 0]
        if any(action not in CHECK_ACTIONS for action in failed_actions):
            return "bind_scoped_repair" if "bind_scoped_repair" not in actions else "close_round"
        if "bind_result" not in actions:
            return "bind_result"
        bind_result_receipt = _receipt_for(chain, "bind_result")
        if bind_result_receipt is not None and bind_result_receipt["exit_code"] != 0:
            return "bind_scoped_repair"
        if "build_run_manifest" not in actions:
            return "build_run_manifest"
        run_receipt = _receipt_for(chain, "build_run_manifest")
        if run_receipt is not None and run_receipt["exit_code"] != 0:
            return "bind_scoped_repair"
        if "bind_scoped_repair" not in actions:
            return "bind_scoped_repair"
        return "close_round"
    if actions[-1] in {"result_review_binding", "final_seal_audit_binding"}:
        latest = chain["receipts"][-1]["record"]
        measured, _ = read_bytes_no_follow(root, latest["stdout_ref"])
        if measured == b"VERDICT=REVISE\n":
            return "bind_scoped_repair"
        if measured != b"VERDICT=AGREE\n":
            raise EvidenceValidationError("review/audit receipt has no exact measured verdict")
    pass_prefix = list(P01_PASS_ACTION_SEQUENCE)
    if actions == pass_prefix[: len(actions)]:
        return pass_prefix[len(actions)] if len(actions) < len(pass_prefix) else "stable_publication"
    if actions[-1] == "bind_scoped_repair":
        return "close_round"
    raise EvidenceValidationError("receipt chain does not match an allowed P01 state")


def _artifact_entry(root: Path, ref: str, role: str, media_type: str = "application/octet-stream") -> dict[str, Any]:
    data, _ = read_bytes_no_follow(root, ref)
    return {"logical_ref": ref, "media_type": media_type, "sha256": content_digest(data), "byte_count": len(data), "role": role}


def _summary_records(root: Path, round_ref: str) -> dict[str, dict[str, Any]]:
    specs = {
        "mutation": ("summaries/mutation-matrix.json", "p01_mutation_summary@1"),
        "parallel": ("summaries/serial-parallel-identity.json", "p01_parallel_summary@1"),
        "legacy": ("summaries/legacy-matrix.json", "p01_legacy_summary@1"),
        "generator": ("summaries/generator-result.json", "p01_generator_result@1"),
    }
    return {
        name: strict_load_canonical_json(root / round_ref / ref, schema=schema)
        for name, (ref, schema) in specs.items()
    }


def _result_ref(result_round: str) -> str:
    return f"docs/plans/mathdevmcp-real-document-remediation-phase-01-evidence-integrity-result-{result_round}-2026-07-11.md"


def _review_ref(result_round: str) -> str:
    return f"docs/reviews/mathdevmcp-real-document-remediation-phase-01-result-review-{result_round}-result-2026-07-11.md"


def _audit_ref(result_round: str) -> str:
    return f"docs/reviews/mathdevmcp-real-document-remediation-phase-01-final-seal-audit-{result_round}-result-2026-07-11.md"


def _build_run_manifest(root: Path, round_ref: str, result_round: str, chain: dict[str, Any]) -> dict[str, Any]:
    _ = round_ref, result_round
    return reconstruct_p01_run_manifest(root, chain["index_ref"])


def _candidate_record(root: Path, round_ref: str, result_round: str, chain: dict[str, Any]) -> dict[str, Any]:
    _ = round_ref, result_round
    return reconstruct_p01_candidate(root, chain["index_ref"])[0]


def _construction_action(root: Path, round_ref: str, result_round: str, action: str, chain: dict[str, Any]) -> tuple[int, bytes, bytes, dict[str, Any]]:
    if action == "bind_result":
        ref = _result_ref(result_round)
        data, _ = read_bytes_no_follow(root, ref)
        if len(data) > 1024 * 1024:
            raise EvidenceValidationError("result note exceeds the bounded governance limit")
        return 0, json.dumps({"result_ref": ref, "result_sha256": content_digest(data)}, sort_keys=True).encode() + b"\n", b"", {"result_ref": ref, "result_sha256": content_digest(data)}
    if action == "build_run_manifest":
        record = _build_run_manifest(root, round_ref, result_round, chain)
        ref = f"{round_ref}/run-manifest.json"
        written = atomic_write_canonical_record(root, ref, record, schema="p01_run_manifest@1")
        bindings = {
            "run_manifest_ref": ref,
            "run_manifest_sha256": written["sha256"],
            "bound_receipt_index_ref": chain["index_ref"],
            "bound_receipt_index_sha256": chain["index_sha256"],
        }
        return 0, canonical_json_bytes(bindings), b"", bindings
    if action == "build_candidate":
        record = _candidate_record(root, round_ref, result_round, chain)
        ref = f"{round_ref}/P01-candidate-decision.json"
        written = atomic_write_canonical_record(root, ref, record, schema="p01_candidate_decision@1")
        bindings = {
            "run_manifest_ref": record["run_manifest_ref"],
            "run_manifest_sha256": record["run_manifest_sha256"],
            "candidate_ref": ref,
            "candidate_sha256": written["sha256"],
            "bound_receipt_index_ref": chain["index_ref"],
            "bound_receipt_index_sha256": chain["index_sha256"],
        }
        return 0, canonical_json_bytes(bindings), b"", bindings
    if action == "candidate_gate":
        candidate_ref = f"{round_ref}/P01-candidate-decision.json"
        candidate = strict_load_canonical_json(root / candidate_ref, schema="p01_candidate_decision@1")
        build_receipt = chain["receipts"][-1]["record"]
        if build_receipt["check_id"] != "build_candidate" or build_receipt["exit_code"] != 0:
            raise EvidenceValidationError("candidate gate requires a successful build_candidate head")
        if (
            candidate["pre_candidate_receipt_index_ref"] != build_receipt["bindings"]["bound_receipt_index_ref"]
            or candidate["pre_candidate_receipt_index_sha256"]
            != build_receipt["bindings"]["bound_receipt_index_sha256"]
            or build_receipt["bindings"]["candidate_ref"] != candidate_ref
            or build_receipt["bindings"]["candidate_sha256"] != _digest_ref(root, candidate_ref)
        ):
            raise EvidenceValidationError("candidate/build receipt binding mismatch")
        verified = verify_p01_candidate(
            root,
            candidate_ref=candidate_ref,
            build_run_receipt_index_ref=candidate["pre_candidate_receipt_index_ref"],
        )
        log_ref = f"{round_ref}/logs/candidate-validation.log"
        payload = verified["report_bytes"]
        atomic_write_bytes_no_replace(root, log_ref, payload)
        bindings = {
            "run_manifest_ref": candidate["run_manifest_ref"],
            "run_manifest_sha256": candidate["run_manifest_sha256"],
            "candidate_ref": candidate_ref,
            "candidate_sha256": _digest_ref(root, candidate_ref),
            "validated_receipt_index_ref": chain["index_ref"],
            "validated_receipt_index_sha256": chain["index_sha256"],
            "payload_bundle_index_ref": candidate["payload_bundle_index_ref"],
            "payload_bundle_index_digest": candidate["payload_bundle_index_digest"],
            "payload_bundle_index_file_sha256": candidate["payload_bundle_index_file_sha256"],
        }
        return 0, payload, b"", bindings
    raise EvidenceValidationError(f"unsupported construction action: {action}")


def _review_action(root: Path, round_ref: str, result_round: str, action: str, chain: dict[str, Any], artifact_ref: str | None) -> tuple[int, bytes, bytes, dict[str, Any]]:
    candidate_ref = f"{round_ref}/P01-candidate-decision.json"
    candidate = strict_load_canonical_json(root / candidate_ref, schema="p01_candidate_decision@1")
    if action == "result_review_binding":
        expected_ref = _review_ref(result_round)
        if artifact_ref != expected_ref:
            raise EvidenceValidationError("result-review artifact ref is not the exact round-specific path")
        review, _ = read_bytes_no_follow(root, expected_ref)
        parsed = verify_result_review_bindings(
            review,
            {
                "result_round": result_round,
                "candidate_sha256": _digest_ref(root, candidate_ref),
                "run_manifest_sha256": candidate["run_manifest_sha256"],
                "result_sha256": candidate["result_sha256"],
                "payload_bundle_index_digest": candidate["payload_bundle_index_digest"],
                "payload_bundle_index_file_sha256": candidate["payload_bundle_index_file_sha256"],
                "receipt_index_sha256": chain["index_sha256"],
            },
        )
        bindings = {
            "review_ref": expected_ref,
            "review_sha256": content_digest(review),
            "candidate_ref": candidate_ref,
            "candidate_sha256": _digest_ref(root, candidate_ref),
            "reviewed_receipt_index_ref": chain["index_ref"],
            "reviewed_receipt_index_sha256": chain["index_sha256"],
        }
        return 0, f"VERDICT={parsed['verdict']}\n".encode(), b"", bindings
    if action == "build_final_candidate":
        record = reconstruct_p01_final_decision(root, chain["index_ref"])
        ref = f"{round_ref}/P01-final-decision-candidate.json"
        written = atomic_write_canonical_record(root, ref, record, schema="p01_final_decision@1")
        bindings = {
            "final_candidate_ref": ref,
            "final_candidate_sha256": written["sha256"],
            "result_review_ref": record["result_review_ref"],
            "result_review_sha256": record["result_review_sha256"],
            "reviewed_receipt_index_ref": chain["index_ref"],
            "reviewed_receipt_index_sha256": chain["index_sha256"],
        }
        return 0, canonical_json_bytes(bindings), b"", bindings
    if action == "final_candidate_gate":
        final_ref = f"{round_ref}/P01-final-decision-candidate.json"
        build_receipt = chain["receipts"][-1]["record"]
        if build_receipt["check_id"] != "build_final_candidate" or build_receipt["exit_code"] != 0:
            raise EvidenceValidationError("final candidate gate requires a successful build_final_candidate head")
        verified = verify_p01_final_decision_candidate(
            root,
            final_candidate_ref=final_ref,
            build_final_receipt_index_ref=chain["index_ref"],
        )
        log_ref = f"{round_ref}/logs/final-decision-candidate-validation.log"
        payload = b"P01_FINAL_CANDIDATE_VALIDATION_V1\nstatus=PASS\n"
        atomic_write_bytes_no_replace(root, log_ref, payload)
        bindings = {
            "final_candidate_ref": final_ref,
            "final_candidate_sha256": verified["final_candidate_sha256"],
            "validation_log_ref": log_ref,
            "validation_log_sha256": content_digest(payload),
            "validated_receipt_index_ref": chain["index_ref"],
            "validated_receipt_index_sha256": chain["index_sha256"],
        }
        return 0, payload, b"", bindings
    if action == "final_seal_audit_binding":
        expected_ref = _audit_ref(result_round)
        if artifact_ref != expected_ref:
            raise EvidenceValidationError("final-seal audit ref is not the exact round-specific path")
        final_ref = f"{round_ref}/P01-final-decision-candidate.json"
        final = strict_load_canonical_json(root / final_ref, schema="p01_final_decision@1")
        gate = chain["receipts"][-1]["record"]
        audit, _ = read_bytes_no_follow(root, expected_ref)
        parsed = verify_final_seal_audit_bindings(
            audit,
            {
                "result_round": result_round,
                "final_candidate_sha256": _digest_ref(root, final_ref),
                "candidate_sha256": final["candidate_decision_sha256"],
                "result_review_sha256": final["result_review_sha256"],
                "validation_log_sha256": gate["bindings"]["validation_log_sha256"],
                "receipt_index_sha256": chain["index_sha256"],
            },
        )
        bindings = {
            "audit_ref": expected_ref,
            "audit_sha256": content_digest(audit),
            "final_candidate_ref": final_ref,
            "final_candidate_sha256": _digest_ref(root, final_ref),
            "candidate_ref": candidate_ref,
            "candidate_sha256": final["candidate_decision_sha256"],
            "result_review_ref": final["result_review_ref"],
            "result_review_sha256": final["result_review_sha256"],
            "validation_log_ref": gate["bindings"]["validation_log_ref"],
            "validation_log_sha256": gate["bindings"]["validation_log_sha256"],
            "audited_receipt_index_ref": chain["index_ref"],
            "audited_receipt_index_sha256": chain["index_sha256"],
        }
        return 0, f"VERDICT={parsed['verdict']}\n".encode(), b"", bindings
    raise EvidenceValidationError(f"unsupported review action: {action}")


def _stable_action(root: Path, round_ref: str, chain: dict[str, Any]) -> tuple[int, bytes, bytes, dict[str, Any]]:
    final_ref = f"{round_ref}/P01-final-decision-candidate.json"
    final = strict_load_canonical_json(root / final_ref, schema="p01_final_decision@1")
    audit_receipt = chain["receipts"][-1]["record"]
    if not audit_receipt["stdout_ref"]:
        raise EvidenceValidationError("missing final-seal audit receipt")
    published = publish_stable_phase_decision(
        root,
        candidate_ref=final_ref,
        review_ref=final["result_review_ref"],
        audit_ref=audit_receipt["bindings"]["audit_ref"],
        validation_log_ref=audit_receipt["bindings"]["validation_log_ref"],
        governance_receipt_index_ref=chain["index_ref"],
        stable_ref=f"{EVIDENCE_ROOT_REF}/phase-results/P01-decision.json",
    )
    log_ref = f"{round_ref}/logs/stable-decision-validation.log"
    log = (
        "P01_STABLE_DECISION_VALIDATION_V1\n"
        f"stable_ref={published['stable_ref']}\n"
        f"stable_sha256={published['stable_sha256']}\n"
        f"same_inode={str(published['same_inode']).lower()}\n"
        f"same_digest={str(published['same_digest']).lower()}\n"
        "status=PASS\n"
    ).encode("ascii")
    atomic_write_bytes_no_replace(root, log_ref, log)
    bindings = {
        "stable_ref": published["stable_ref"],
        "stable_sha256": published["stable_sha256"],
        "final_candidate_ref": final_ref,
        "final_candidate_sha256": _digest_ref(root, final_ref),
        "audit_ref": audit_receipt["bindings"]["audit_ref"],
        "audit_sha256": audit_receipt["bindings"]["audit_sha256"],
        "validation_log_ref": audit_receipt["bindings"]["validation_log_ref"],
        "validation_log_sha256": audit_receipt["bindings"]["validation_log_sha256"],
        "same_inode": published["same_inode"],
        "same_digest": published["same_digest"],
    }
    return 0, log, b"", bindings


def _receipt_for(chain: dict[str, Any], check_id: str) -> dict[str, Any] | None:
    matches = [item["record"] for item in chain["receipts"] if item["record"]["check_id"] == check_id]
    if len(matches) > 1:
        raise EvidenceValidationError(f"receipt chain repeats {check_id}")
    return matches[0] if matches else None


def _pair_from_receipt(chain: dict[str, Any], check_id: str, ref_key: str, digest_key: str) -> tuple[str | None, str | None]:
    receipt = _receipt_for(chain, check_id)
    if receipt is None or receipt["exit_code"] != 0:
        return None, None
    return receipt["bindings"][ref_key], receipt["bindings"][digest_key]


def _repair_action(root: Path, round_ref: str, result_round: str, action: str, chain: dict[str, Any]) -> tuple[int, bytes, bytes, dict[str, Any]]:
    repair_ref = f"{round_ref}/inputs/scoped-repair.json"
    repair = strict_load_canonical_json(root / repair_ref, schema="p01_scoped_repair@1")
    if repair["result_round"] != result_round:
        raise EvidenceValidationError("scoped-repair input round mismatch")
    source, _ = read_bytes_no_follow(root, repair["source_artifact_ref"])
    source_index = verify_receipt_index(root, repair["source_receipt_index_ref"])
    if content_digest(source) != repair["source_artifact_sha256"] or source_index["index_sha256"] != repair["source_receipt_index_sha256"]:
        raise EvidenceValidationError("scoped-repair source bindings do not recompute")
    if action == "bind_scoped_repair":
        bindings = {
            "scoped_repair_input_ref": repair_ref,
            "scoped_repair_input_sha256": _digest_ref(root, repair_ref),
            "source_artifact_ref": repair["source_artifact_ref"],
            "source_artifact_sha256": repair["source_artifact_sha256"],
            "source_receipt_index_ref": repair["source_receipt_index_ref"],
            "source_receipt_index_sha256": repair["source_receipt_index_sha256"],
        }
        return 0, canonical_json_bytes(bindings), b"", bindings
    if action != "close_round":
        raise EvidenceValidationError(f"unsupported repair action: {action}")
    binding_receipt = chain["receipts"][-1]["record"]
    if binding_receipt["check_id"] != "bind_scoped_repair" or binding_receipt["exit_code"] != 0:
        raise EvidenceValidationError("close_round requires a successful bind_scoped_repair head")
    init = chain["receipts"][0]["record"]["bindings"]
    result_ref, result_sha256 = _pair_from_receipt(chain, "bind_result", "result_ref", "result_sha256")
    run_ref, run_sha256 = _pair_from_receipt(chain, "build_run_manifest", "run_manifest_ref", "run_manifest_sha256")
    candidate_ref, candidate_sha256 = _pair_from_receipt(chain, "build_candidate", "candidate_ref", "candidate_sha256")
    review_ref, review_sha256 = _pair_from_receipt(chain, "result_review_binding", "review_ref", "review_sha256")
    final_ref, final_sha256 = _pair_from_receipt(chain, "build_final_candidate", "final_candidate_ref", "final_candidate_sha256")
    audit_ref, audit_sha256 = _pair_from_receipt(chain, "final_seal_audit_binding", "audit_ref", "audit_sha256")
    review_verdict = None
    review_receipt = _receipt_for(chain, "result_review_binding")
    if review_receipt is not None and review_receipt["exit_code"] == 0:
        measured, _ = read_bytes_no_follow(root, review_receipt["stdout_ref"])
        if measured in {b"VERDICT=AGREE\n", b"VERDICT=REVISE\n"}:
            review_verdict = measured.decode("ascii").strip().split("=", 1)[1]
    if repair["close_reason"] == "result_review_revise" and review_verdict != "REVISE":
        raise EvidenceValidationError("result-review close requires measured REVISE")
    if repair["close_reason"] == "final_seal_audit_revise" and review_verdict != "AGREE":
        raise EvidenceValidationError("final-seal close requires agreeing result review")
    failed_action = None
    if repair["close_reason"] in {"local_check_failure", "candidate_gate_failure"}:
        failed = [item["record"] for item in chain["receipts"] if item["record"]["exit_code"] != 0]
        if not failed:
            raise EvidenceValidationError("failure close has no failed receipt")
        failed_action = failed[0]["check_id"]
    log_inventory = []
    for item in chain["receipts"]:
        receipt = item["record"]
        for stem in ("stdout", "stderr"):
            ref = receipt[f"{stem}_ref"]
            data, _ = read_bytes_no_follow(root, ref)
            log_inventory.append(
                {
                    "logical_ref": ref,
                    "sha256": content_digest(data),
                    "byte_count": len(data),
                    "role": f"{receipt['check_id']}_{stem}",
                    "exit_code": receipt["exit_code"],
                }
            )
    close = {
        "schema_version": "p01_round_close@1",
        "phase": "P01",
        "result_round": result_round,
        "close_reason": repair["close_reason"],
        "failed_action": failed_action,
        "entry_implementation_manifest_sha256": init["entry_implementation_manifest_sha256"],
        "entry_protected_manifest_sha256": init["entry_protected_manifest_sha256"],
        "bootstrap_close_ref": init["bootstrap_close_ref"],
        "bootstrap_close_sha256": init["bootstrap_close_sha256"],
        "predecessor_close_ref": init["prior_round_close_ref"],
        "predecessor_close_sha256": init["prior_round_close_sha256"],
        "predecessor_terminal_receipt_index_ref": init["prior_terminal_receipt_index_ref"],
        "predecessor_terminal_receipt_index_sha256": init["prior_terminal_receipt_index_sha256"],
        "implementation_exit_manifest_sha256": init["implementation_exit_manifest_sha256"],
        "receipt_index_before_close_ref": chain["index_ref"],
        "receipt_index_before_close_sha256": chain["index_sha256"],
        "log_inventory": log_inventory,
        "run_manifest_ref": run_ref,
        "run_manifest_sha256": run_sha256,
        "result_ref": result_ref,
        "result_sha256": result_sha256,
        "candidate_ref": candidate_ref,
        "candidate_sha256": candidate_sha256,
        "result_review_ref": review_ref,
        "result_review_sha256": review_sha256,
        "result_review_verdict": review_verdict,
        "final_decision_candidate_ref": final_ref,
        "final_decision_candidate_sha256": final_sha256,
        "final_seal_audit_ref": audit_ref,
        "final_seal_audit_sha256": audit_sha256,
        "scoped_repairs": repair["repairs"],
        "vetoes": {key: key == "governance_chain_failure" for key in P01_VETO_KEYS},
        "non_claims": list(P01_NON_CLAIMS),
    }
    close_ref = f"{round_ref}/round-close.json"
    written = atomic_write_canonical_record(root, close_ref, close, schema="p01_round_close@1")
    bindings = {
        "scoped_repair_input_ref": repair_ref,
        "scoped_repair_input_sha256": _digest_ref(root, repair_ref),
        "round_close_ref": close_ref,
        "round_close_sha256": written["sha256"],
        "preceding_receipt_index_ref": chain["index_ref"],
        "preceding_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _run_action(root: Path, round_ref: str, result_round: str, action: str, artifact_ref: str | None) -> dict[str, Any]:
    chain = _receipt_chain(root, round_ref)
    expected = _expected_action(root, chain)
    if action != expected:
        raise EvidenceValidationError(f"action {action} is not allowed; expected {expected}")
    if action in {"result_review_binding", "final_seal_audit_binding"}:
        if artifact_ref is None:
            raise EvidenceValidationError(f"{action} requires --artifact-ref")
        artifact_ref = _logical_ref(root, artifact_ref)
    elif artifact_ref is not None:
        raise EvidenceValidationError("--artifact-ref is accepted only for review/audit binding")

    log_names = {
        "canonical": "canonical-tests",
        "store": "store-tests",
        "promotion": "promotion-tests",
        "compatibility": "compatibility-tests",
        "integration": "integration-tests",
        "p00_quarantine": "p00-quarantine-regression",
        "generator": "synthetic-generator",
        "compile": "compile-check",
        "protected_check": "protected-dirty-check",
        "implementation_exit": "implementation-exit-check",
        "allowlist": "allowlist-check",
        "assignment_audit": "assignment-audit",
        "diff": "diff-check",
        "bind_result": "bind-result",
        "build_run_manifest": "build-run-manifest",
        "build_candidate": "build-candidate",
        "candidate_gate": "candidate-validation",
        "result_review_binding": "result-review-binding",
        "build_final_candidate": "build-final-candidate",
        "final_candidate_gate": "final-decision-candidate-validation",
        "final_seal_audit_binding": "final-seal-audit-binding",
        "bind_scoped_repair": "bind-scoped-repair",
        "close_round": "close-round",
        "stable_publication": "stable-decision-validation",
    }
    stem = log_names[action]
    stdout_ref = f"{round_ref}/logs/{stem}.stdout"
    stderr_ref = f"{round_ref}/logs/{stem}.stderr"
    started = _utc_now()
    start_ns = time.monotonic_ns()
    argv = p01_governance_action_argv(round_ref, action, artifact_ref=artifact_ref)
    fixed = _fixed_argv(root, round_ref, result_round, action)
    try:
        if fixed is not None:
            exit_code, stdout, stderr = _run_command(root, fixed)
            bindings: dict[str, Any] = {}
            receipt_argv = fixed
        elif action in {"implementation_exit", "allowlist", "assignment_audit"}:
            exit_code, stdout, stderr, bindings = _internal_check(root, round_ref, result_round, action)
            receipt_argv = argv
        elif action in {"bind_result", "build_run_manifest", "build_candidate", "candidate_gate"}:
            exit_code, stdout, stderr, bindings = _construction_action(root, round_ref, result_round, action, chain)
            receipt_argv = argv
        elif action in {"result_review_binding", "build_final_candidate", "final_candidate_gate", "final_seal_audit_binding"}:
            exit_code, stdout, stderr, bindings = _review_action(root, round_ref, result_round, action, chain, artifact_ref)
            receipt_argv = argv
        elif action in {"bind_scoped_repair", "close_round"}:
            exit_code, stdout, stderr, bindings = _repair_action(root, round_ref, result_round, action, chain)
            receipt_argv = argv
        elif action == "stable_publication":
            exit_code, stdout, stderr, bindings = _stable_action(root, round_ref, chain)
            receipt_argv = argv
        else:
            raise EvidenceValidationError(f"action implementation is unavailable: {action}")
    except Exception as exc:
        exit_code = 1
        stdout = b""
        stderr = f"{type(exc).__name__}: {exc}\n".encode("utf-8")
        bindings = {key: None for key in P01_RECEIPT_BINDING_KEYS[action]}
        receipt_argv = fixed or argv
    ended = _utc_now()
    wall_time_ns = time.monotonic_ns() - start_ns
    atomic_write_bytes_no_replace(root, stdout_ref, stdout)
    atomic_write_bytes_no_replace(root, stderr_ref, stderr)
    receipt, new_chain = _write_receipt(
        root,
        round_ref,
        result_round,
        action,
        receipt_argv,
        started,
        ended,
        wall_time_ns,
        exit_code,
        stdout_ref,
        stderr_ref,
        bindings,
    )
    return {
        "action": action,
        "measurement_recorded": True,
        "receipt_index_ref": new_chain["index_ref"],
        "receipt_index_sha256": new_chain["index_sha256"],
        "receipt_ref": receipt["ref"],
        "receipt_sha256": receipt["sha256"],
        "state": "recorded_pass" if exit_code == 0 else "recorded_failure",
        "underlying_exit_code": exit_code,
    }


def _init_round(root: Path, args: argparse.Namespace) -> dict[str, Any]:
    started = _utc_now()
    start_ns = time.monotonic_ns()
    round_ref, result_round, round_path = _round_context(root, args.round_root, must_exist=False)
    if args.round != result_round:
        raise EvidenceValidationError("--round does not match --round-root")
    entry_ref = _logical_ref(root, args.entry_root)
    if entry_ref != ENTRY_ROOT_REF:
        raise EvidenceValidationError("entry root is not the fixed P01 entry root")
    bootstrap_ref = _logical_ref(root, args.bootstrap_close)
    shell_ref = _logical_ref(root, args.bootstrap_shell_verification)
    bootstrap, _ = read_bytes_no_follow(root, bootstrap_ref)
    shell, _ = read_bytes_no_follow(root, shell_ref)
    parsed = verify_bootstrap_close(
        bootstrap,
        {
            "entry_implementation_manifest_sha256": content_digest(read_bytes_no_follow(root, f"{ENTRY_ROOT_REF}/implementation-entry-sha256.txt")[0]),
            "entry_protected_manifest_sha256": _entry_protected_digest(root),
        },
    )
    if b"status=PASS\n" not in shell or f"bootstrap_close_sha256={content_digest(bootstrap)}\n".encode() not in shell:
        raise EvidenceValidationError("bootstrap shell verification does not bind the close")
    current_manifest = _manifest_bytes(root)
    current_digest = content_digest(current_manifest)
    if current_digest != parsed["implementation_exit_manifest_sha256"]:
        raise EvidenceValidationError("current implementation does not match bootstrap close")

    prior_close_ref = None if args.prior_round_close == "NONE" else _logical_ref(root, args.prior_round_close)
    prior_index_ref = None if args.prior_terminal_receipt_index == "NONE" else _logical_ref(root, args.prior_terminal_receipt_index)
    if result_round == "rr01":
        if prior_close_ref is not None or prior_index_ref is not None:
            raise EvidenceValidationError("rr01 prior bindings must be NONE")
    else:
        if prior_close_ref is None or prior_index_ref is None:
            raise EvidenceValidationError("successor round requires prior close and terminal index")
        prior_close = strict_load_canonical_json(root / prior_close_ref, schema="p01_round_close@1")
        prior_chain = verify_receipt_index(root, prior_index_ref)
        last = prior_chain["receipts"][-1]["record"]
        prior_close_sha256 = _digest_ref(root, prior_close_ref)
        if (
            last["check_id"] != "close_round"
            or last["exit_code"] != 0
            or last["bindings"]["round_close_ref"] != prior_close_ref
            or last["bindings"]["round_close_sha256"] != prior_close_sha256
        ):
            raise EvidenceValidationError("prior terminal index does not close the supplied predecessor")
        if prior_close["result_round"] != f"rr{int(result_round[2:]) - 1:02d}":
            raise EvidenceValidationError("prior close is not the immediately preceding round")
        if (
            parsed["prior_result_round_close_ref"] != prior_close_ref
            or parsed["prior_result_round_close_sha256"] != prior_close_sha256
        ):
            raise EvidenceValidationError("bootstrap close does not bind the supplied predecessor")

    if result_round == "rr01" and (
        parsed["prior_result_round_close_ref"] != "NONE"
        or parsed["prior_result_round_close_sha256"] != "NONE"
    ):
        raise EvidenceValidationError("rr01 bootstrap predecessor must be NONE")
    if sys.executable != PYTHON or os.environ.get("PYTHONPATH") != "src":
        raise EvidenceValidationError("init-round requires the pinned Python and PYTHONPATH=src")
    git_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if not re.fullmatch(r"[0-9a-f]{40}", git_commit):
        raise EvidenceValidationError("git rev-parse did not return a canonical commit id")

    if not round_path.parent.exists():
        round_path.parent.mkdir(mode=0o700, parents=False)
    if round_path.parent.is_symlink() or not round_path.parent.is_dir():
        raise EvidenceValidationError("result-rounds parent is unsafe")
    round_path.mkdir(mode=0o700, parents=False)
    manifest_ref = f"{round_ref}/implementation-exit-sha256.txt"
    atomic_write_bytes_no_replace(root, manifest_ref, current_manifest)
    stdout_ref = f"{round_ref}/logs/init-round.stdout"
    stderr_ref = f"{round_ref}/logs/init-round.stderr"
    measurement = {
        "bootstrap": parsed["bootstrap_attempt"],
        "git_commit": git_commit,
        "implementation_exit_manifest_sha256": current_digest,
        "platform_system": platform.system(),
        "pytest_version": importlib.metadata.version("pytest"),
        "python_executable": sys.executable,
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "pythonpath": os.environ["PYTHONPATH"],
    }
    stdout = canonical_json_bytes(measurement) + b"\n"
    atomic_write_bytes_no_replace(root, stdout_ref, stdout)
    atomic_write_bytes_no_replace(root, stderr_ref, b"")
    ended = _utc_now()
    wall_time_ns = time.monotonic_ns() - start_ns
    bindings = {
        "bootstrap_close_ref": bootstrap_ref,
        "bootstrap_close_sha256": content_digest(bootstrap),
        "bootstrap_shell_verification_ref": shell_ref,
        "bootstrap_shell_verification_sha256": content_digest(shell),
        "entry_implementation_manifest_sha256": content_digest(read_bytes_no_follow(root, f"{ENTRY_ROOT_REF}/implementation-entry-sha256.txt")[0]),
        "entry_protected_manifest_sha256": _entry_protected_digest(root),
        "implementation_exit_manifest_ref": manifest_ref,
        "implementation_exit_manifest_sha256": current_digest,
        "prior_round_close_ref": prior_close_ref,
        "prior_round_close_sha256": _digest_ref(root, prior_close_ref) if prior_close_ref else None,
        "prior_terminal_receipt_index_ref": prior_index_ref,
        "prior_terminal_receipt_index_sha256": _digest_ref(root, prior_index_ref) if prior_index_ref else None,
    }
    receipt, chain = _write_receipt(
        root,
        round_ref,
        result_round,
        "init_round",
        [
            "env",
            "PYTHONPATH=src",
            PYTHON,
            "scripts/p01_governance.py",
            "init-round",
            "--round",
            result_round,
            "--entry-root",
            entry_ref,
            "--bootstrap-close",
            bootstrap_ref,
            "--bootstrap-shell-verification",
            shell_ref,
            "--round-root",
            round_ref,
            "--prior-round-close",
            prior_close_ref or "NONE",
            "--prior-terminal-receipt-index",
            prior_index_ref or "NONE",
        ],
        started,
        ended,
        wall_time_ns,
        0,
        stdout_ref,
        stderr_ref,
        bindings,
    )
    return {
        "action": "init_round",
        "measurement_recorded": True,
        "receipt_index_ref": chain["index_ref"],
        "receipt_index_sha256": chain["index_sha256"],
        "receipt_ref": receipt["ref"],
        "receipt_sha256": receipt["sha256"],
        "state": "round_initialized",
        "underlying_exit_code": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(allow_abbrev=False)
    subparsers = parser.add_subparsers(dest="operation", required=True)
    init = subparsers.add_parser("init-round", allow_abbrev=False)
    init.add_argument("--round", required=True)
    init.add_argument("--entry-root", required=True)
    init.add_argument("--bootstrap-close", required=True)
    init.add_argument("--bootstrap-shell-verification", required=True)
    init.add_argument("--round-root", required=True)
    init.add_argument("--prior-round-close", required=True)
    init.add_argument("--prior-terminal-receipt-index", required=True)
    run = subparsers.add_parser("run", allow_abbrev=False)
    run.add_argument("--round-root", required=True)
    run.add_argument("--action", choices=RUN_ACTIONS, required=True)
    run.add_argument("--artifact-ref")
    args = parser.parse_args()
    root = _repo_root()
    if args.operation == "init-round":
        status = _init_round(root, args)
    else:
        round_ref, result_round, _ = _round_context(root, args.round_root, must_exist=True)
        status = _run_action(root, round_ref, result_round, args.action, args.artifact_ref)
    print(json.dumps(status, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"measurement_recorded": False, "status": "governance_error", "error": f"{type(exc).__name__}: {exc}"}, sort_keys=True, separators=(",", ":")), file=sys.stderr)
        raise SystemExit(2)
