#!/usr/bin/env python3
"""Append-only governance for Phase 03 context-only evidence."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import time
from typing import Any, Mapping

from mathdevmcp.context_evidence import (
    P03_GUARDED_ACTIONS,
    P03_NON_CLAIMS,
    P03_PRIMARY_CRITERIA,
    P03_VETO_KEYS,
    context_artifact_refs,
    expected_p03_next_action,
    parse_p03_human_result,
    parse_p03_review,
    reconstruct_context_bundle,
    validate_p03_candidate,
    validate_p03_final,
    validate_p03_mutation_matrix,
    validate_p03_phase_result,
    validate_p03_receipt,
    validate_p03_receipt_index,
    validate_p03_run_manifest,
    verify_p03_entry,
)
from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
    validate_logical_path,
)


PHASE = "P03"
REVISION = "P03R1"
PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
GOVERNANCE_REF = "scripts/p03_governance.py"
EVIDENCE_ROOT_REF = ".local/mathdevmcp/evidence/p03-20260712"
ROUND_PARENT_REF = f"{EVIDENCE_ROOT_REF}/result-rounds"
ENTRY_RECORD_REF = f"{EVIDENCE_ROOT_REF}/entry/entry-record.json"
P02_FINAL_REF = (
    ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/"
    "P02-final-decision-candidate.json"
)
P00_DECISION_REF = ".local/mathdevmcp/evidence/p00-20260711/phase-results/P00-decision.json"
P00_DECISION_SHA256 = "2b44b9ae8fe3f8fcce4f7903fd206a5279326212374b73dba9af59bb476592ea"
ROUND_RE = re.compile(r"^rr0[1-5]$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

P02_PASS_ACTIONS = (
    "init_round",
    "localizer_tests",
    "obligation_tests",
    "target_integration_tests",
    "parser_fidelity_tests",
    "frozen_regressions",
    "p00_quarantine",
    "generate_extraction_bundle",
    "mutation_ambiguity_gate",
    "zero_backend_source_edit_gate",
    "compile",
    "protected_check",
    "implementation_exit",
    "allowlist",
    "diff",
    "bind_result",
    "build_run_manifest",
    "build_candidate",
    "candidate_gate",
    "result_review_binding",
    "build_final_candidate",
    "final_candidate_gate",
    "final_seal_audit_binding",
    "stable_publication",
)

FORMAL_TESTS = {
    "context_graph_tests": ["tests/test_document_context_graph.py"],
    "resolver_tests": ["tests/test_document_context_resolver.py"],
    "symbol_assumption_tests": [
        "tests/test_context_evidence.py::test_formal_symbol_resolution_preserves_scope_and_lexical_uncertainty",
        "tests/test_context_evidence.py::test_formal_typed_assumption_identity_and_binding_are_orthogonal",
        "tests/test_context_evidence.py::test_formal_duplicate_notation_aliases_remain_ambiguous",
        "tests/test_context_evidence.py::test_frozen_card_pi_is_policy_or_ambiguous_never_posterior_by_spelling",
    ],
    "report_boundary_tests": [
        "tests/test_context_evidence.py::test_compiler_preserves_context_state_distinctions",
        "tests/test_context_evidence.py::test_engineering_context_error_vetoes_target_before_math_or_backend",
        "tests/test_context_evidence.py::test_not_searched_is_rendered_as_unsearched_not_missing",
        "tests/test_context_evidence.py::test_parser_ambiguity_is_not_rendered_as_math_gap",
        "tests/test_context_evidence.py::test_candidate_assumption_is_not_rendered_as_source_fact",
        "tests/test_context_evidence.py::test_context_only_module_has_no_backend_or_doctor_import_path",
        "tests/test_context_evidence.py::test_generator_reopens_manifest_bound_guard_before_production_import",
        "tests/test_context_evidence.py::test_guard_classifies_backend_imports_and_frozen_sources_without_attempts",
    ],
    "frozen_context_regressions": ["tests/test_context_real_regressions.py"],
    "p00_quarantine": [
        "tests/test_context_evidence.py::test_p00_disabled_decision_and_context_only_publication_boundary_are_preserved"
    ],
}

COMPILE_REFS = (
    "scripts/generate_p03_context_evidence.py",
    "scripts/p03_governance.py",
    "src/mathdevmcp/context_evidence.py",
    "src/mathdevmcp/document_context_graph.py",
    "src/mathdevmcp/document_derivation_tree.py",
    "src/mathdevmcp/latex_index.py",
    "src/mathdevmcp/math_ir.py",
    "src/mathdevmcp/notation_reconciliation.py",
    "tests/p03_no_backend_guard.py",
    "tests/test_context_evidence.py",
    "tests/test_context_real_regressions.py",
    "tests/test_document_context_graph.py",
    "tests/test_document_context_resolver.py",
    "tests/test_document_derivation_real_regressions.py",
    "tests/test_document_derivation_tree.py",
    "tests/test_latex_index.py",
    "tests/test_math_ir.py",
    "tests/test_notation_reconciliation.py",
)

NATIVE_ACTIONS = frozenset(
    {
        "init_round",
        "mutation_gate",
        "zero_backend_source_edit_gate",
        "protected_check",
        "implementation_exit",
        "allowlist",
        "bind_result",
        "build_run_manifest",
        "build_candidate",
        "candidate_gate",
        "result_review_binding",
        "build_final_candidate",
        "final_candidate_gate",
        "final_seal_audit_binding",
        "stable_publication",
        "bind_scoped_repair",
        "close_round",
    }
)

BINDING_KEYS: dict[str, tuple[str, ...]] = {
    "init_round": (
        "entry_record_ref",
        "entry_record_sha256",
        "entry_implementation_manifest_ref",
        "entry_implementation_manifest_sha256",
        "round_implementation_manifest_ref",
        "round_implementation_manifest_sha256",
        "entry_protected_manifest_ref",
        "entry_protected_manifest_sha256",
        "entry_immutable_input_manifest_ref",
        "entry_immutable_input_manifest_sha256",
        "pre_round_worktree_ref",
        "pre_round_worktree_sha256",
        "reviewed_plan_ref",
        "reviewed_plan_sha256",
        "reviewed_recovery_plan_ref",
        "reviewed_recovery_plan_sha256",
        "agreeing_recovery_review_ref",
        "agreeing_recovery_review_sha256",
        "p02_stable_decision_ref",
        "p02_stable_decision_sha256",
        "p02_terminal_receipt_index_ref",
        "p02_terminal_receipt_index_sha256",
        "p02_extraction_bundle_index_ref",
        "p02_extraction_bundle_index_sha256",
        "p02_obligations_ref",
        "p02_obligations_sha256",
        "p02_close_ref",
        "p02_close_sha256",
        "predecessor_round_close_ref",
        "predecessor_round_close_sha256",
        "predecessor_terminal_receipt_index_ref",
        "predecessor_terminal_receipt_index_sha256",
    ),
    "generate_context_bundle": (
        "bundle_index_ref",
        "bundle_index_sha256",
        "bundle_semantic_digest",
    ),
    "mutation_gate": ("mutation_matrix_ref", "mutation_matrix_sha256", "all_pass"),
    "zero_backend_source_edit_gate": (
        "guard_index_ref",
        "guard_index_sha256",
        "backend_request_count",
        "source_edit_count",
        "publication_count",
    ),
    "protected_check": ("protected_manifest_ref", "protected_manifest_sha256", "verified_target_count"),
    "implementation_exit": ("implementation_exit_manifest_ref", "implementation_exit_manifest_sha256"),
    "allowlist": ("touched_paths_ref", "touched_paths_sha256", "unexpected_paths_ref", "unexpected_paths_sha256"),
    "bind_result": ("human_result_ref", "human_result_sha256", "result_ref", "result_sha256"),
    "build_run_manifest": (
        "run_manifest_ref",
        "run_manifest_sha256",
        "bound_receipt_index_ref",
        "bound_receipt_index_sha256",
    ),
    "build_candidate": ("candidate_ref", "candidate_sha256"),
    "candidate_gate": (
        "candidate_ref",
        "candidate_sha256",
        "validation_log_ref",
        "validation_log_sha256",
        "validated_receipt_index_ref",
        "validated_receipt_index_sha256",
    ),
    "result_review_binding": (
        "review_ref",
        "review_sha256",
        "review_verdict",
        "reviewed_receipt_index_ref",
        "reviewed_receipt_index_sha256",
    ),
    "build_final_candidate": ("final_candidate_ref", "final_candidate_sha256"),
    "final_candidate_gate": (
        "final_candidate_ref",
        "final_candidate_sha256",
        "validation_log_ref",
        "validation_log_sha256",
        "validated_receipt_index_ref",
        "validated_receipt_index_sha256",
    ),
    "final_seal_audit_binding": (
        "audit_ref",
        "audit_sha256",
        "audit_verdict",
        "audited_receipt_index_ref",
        "audited_receipt_index_sha256",
        "validation_log_ref",
        "validation_log_sha256",
    ),
    "stable_publication": (
        "stable_ref",
        "stable_sha256",
        "final_candidate_ref",
        "final_candidate_sha256",
        "audit_ref",
        "audit_sha256",
        "same_inode",
        "same_digest",
    ),
    "bind_scoped_repair": ("scoped_repair_ref", "scoped_repair_sha256"),
    "close_round": (
        "round_close_ref",
        "round_close_sha256",
        "receipt_index_before_close_ref",
        "receipt_index_before_close_sha256",
    ),
}
for _action in (*FORMAL_TESTS, "compile", "diff"):
    BINDING_KEYS[_action] = ()


def _repo_root() -> Path:
    root = Path.cwd().absolute()
    if not (root / ".git").is_dir() or not (root / "src/mathdevmcp").is_dir():
        raise EvidenceValidationError("Phase 03 governance must run from the workspace root")
    return root


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _read(root: Path, ref: str) -> bytes:
    raw, info = read_bytes_no_follow(root, ref)
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError(f"Phase 03 artifact is not regular: {ref}")
    return raw


def _digest(root: Path, ref: str) -> str:
    return content_digest(_read(root, ref))


def _json(raw: bytes, name: str, *, canonical: bool = True) -> dict[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"{name} violates strict JSON byte rules")
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"{name} is not strict UTF-8 JSON") from exc
    if not isinstance(value, dict) or (canonical and canonical_json_bytes(value) != raw):
        raise EvidenceValidationError(f"{name} is not a canonical JSON object")
    return value


def _write(root: Path, ref: str, raw: bytes) -> dict[str, Any]:
    result = atomic_write_bytes_no_replace(root, ref, raw)
    reopened = _read(root, ref)
    if reopened != raw or content_digest(reopened) != result["sha256"]:
        raise EvidenceValidationError(f"Phase 03 artifact reopen mismatch: {ref}")
    return result


def _write_json(root: Path, ref: str, value: Any) -> dict[str, Any]:
    return _write(root, ref, canonical_json_bytes(value))


def _round_context(root: Path, value: str, *, must_exist: bool) -> tuple[str, str, Path]:
    path = PurePosixPath(value)
    if path.parent.as_posix() != ROUND_PARENT_REF or ROUND_RE.fullmatch(path.name) is None:
        raise EvidenceValidationError("Phase 03 round root is outside the reviewed namespace")
    target = root / path
    exists = target.exists() or target.is_symlink()
    if must_exist:
        if not exists or target.is_symlink() or not target.is_dir():
            raise EvidenceValidationError("Phase 03 round root is unavailable or unsafe")
    elif exists:
        raise EvidenceValidationError("Phase 03 round root already exists")
    return path.as_posix(), path.name, target


def _manifest_records(raw: bytes) -> dict[str, str]:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("Phase 03 implementation manifest is not UTF-8") from exc
    if not text.endswith("\n") or "\r" in text or "\x00" in text:
        raise EvidenceValidationError("Phase 03 implementation manifest bytes are invalid")
    result: dict[str, str] = {}
    for line in text.splitlines():
        digest, separator, ref = line.partition("  ")
        if separator != "  " or SHA_RE.fullmatch(digest) is None or ref in result:
            raise EvidenceValidationError("Phase 03 implementation manifest line is invalid")
        validate_logical_path(ref, name="implementation manifest ref")
        result[ref] = digest
    if list(result) != sorted(result, key=lambda item: item.encode("utf-8")):
        raise EvidenceValidationError("Phase 03 implementation manifest is not ordered")
    return result


def _implementation_refs(root: Path) -> list[str]:
    refs: list[str] = []
    for top_name in ("scripts", "src", "tests"):
        top = root / top_name
        for directory, names, files in os.walk(top, topdown=True, followlinks=False):
            names[:] = sorted(name for name in names if name != "__pycache__")
            current = Path(directory)
            for name in [*names, *files]:
                path = current / name
                if path.is_symlink():
                    raise EvidenceValidationError(f"symlink in implementation tree: {path.relative_to(root)}")
            for name in sorted(files):
                path = current / name
                if path.suffix in {".pyc", ".pyo"}:
                    continue
                refs.append(path.relative_to(root).as_posix())
    return sorted(refs, key=lambda item: item.encode("utf-8"))


def _implementation_manifest(root: Path) -> bytes:
    return b"".join(f"{_digest(root, ref)}  {ref}\n".encode("utf-8") for ref in _implementation_refs(root))


def _verify_manifest_live(root: Path, ref: str) -> dict[str, str]:
    records = _manifest_records(_read(root, ref))
    for logical_ref, digest in records.items():
        if _digest(root, logical_ref) != digest:
            raise EvidenceValidationError(f"Phase 03 manifest target drift: {logical_ref}")
    return records


def _mkdir_exact(path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise EvidenceValidationError(f"Phase 03 directory already exists: {path}")
    if path.parent.is_symlink() or not path.parent.is_dir():
        raise EvidenceValidationError(f"Phase 03 directory parent is unsafe: {path.parent}")
    path.mkdir(mode=0o700, parents=False, exist_ok=False)


def _fixed_refs(round_ref: str, result_round: str) -> dict[str, str]:
    return {
        "round_implementation_manifest": f"{round_ref}/implementation-round-sha256.txt",
        "pre_round_worktree": f"{round_ref}/pre-round-worktree.json",
        "implementation_exit_manifest": f"{round_ref}/implementation-exit-sha256.txt",
        "touched_paths": f"{round_ref}/touched-paths.txt",
        "unexpected_paths": f"{round_ref}/unexpected-paths.txt",
        "human_result": (
            "docs/plans/mathdevmcp-real-document-remediation-phase-03-semantic-resolution-"
            f"and-corpus-context-result-{result_round}-2026-07-12.md"
        ),
        "machine_result": f"{round_ref}/P03-result.json",
        "run_manifest": f"{round_ref}/run-manifest.json",
        "candidate": f"{round_ref}/P03-candidate-decision.json",
        "candidate_validation": f"{round_ref}/candidate-validation.json",
        "result_review": (
            "docs/reviews/mathdevmcp-real-document-remediation-phase-03-result-review-"
            f"{result_round}-result-2026-07-12.md"
        ),
        "final_candidate": f"{round_ref}/P03-final-decision-candidate.json",
        "final_validation": f"{round_ref}/final-candidate-validation.json",
        "final_audit": (
            "docs/reviews/mathdevmcp-real-document-remediation-phase-03-final-seal-audit-"
            f"{result_round}-result-2026-07-12.md"
        ),
        "stable": f"{EVIDENCE_ROOT_REF}/phase-results/P03-decision.json",
        "scoped_repair": f"{round_ref}/scoped-repair.json",
        "round_close": f"{round_ref}/round-close.json",
    }


def _child_environment(root: Path, round_ref: str, action: str) -> dict[str, str]:
    environment = {
        "CUDA_VISIBLE_DEVICES": "-1",
        "HOME": str(root / round_ref / "governance/home"),
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "MATHDEVMCP_P03_ACTION": action,
        "MATHDEVMCP_P03_DISPATCH_DEPTH": "1",
        "MATHDEVMCP_P03_ROUND_ROOT": round_ref,
        "PATH": "/usr/bin:/bin",
        "PYTHONHASHSEED": "0",
        "PYTHONPATH": "src",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "TMPDIR": str(root / round_ref / "governance/tmp"),
    }
    # ``py_compile`` ignores ``-B`` for its explicit targets.  Keep all
    # resulting bytecode inside the reviewed round-local write boundary.
    if action == "compile":
        environment["PYTHONPYCACHEPREFIX"] = str(root / round_ref / "governance/pycache")
    return environment


def _child_argv(round_ref: str, action: str) -> list[str] | None:
    if action in FORMAL_TESTS:
        return [
            PYTHON,
            "-B",
            "-m",
            "pytest",
            "-q",
            "-p",
            "tests.p03_no_backend_guard",
            "-p",
            "no:cacheprovider",
            "-p",
            "no:logging",
            *FORMAL_TESTS[action],
        ]
    if action == "generate_context_bundle":
        return [PYTHON, "-B", "scripts/generate_p03_context_evidence.py", "--round-root", round_ref]
    if action == "compile":
        return [PYTHON, "-B", "-m", "py_compile", *COMPILE_REFS]
    if action == "diff":
        return ["/usr/bin/git", "diff", "--check"]
    return None


def _execution_class(action: str) -> str:
    return "governance_native" if action in NATIVE_ACTIONS else "subprocess"


def _handler_id(action: str) -> str:
    return f"p03_{'native' if action in NATIVE_ACTIONS else 'subprocess'}_{action}_v1"


def _external_argv(round_ref: str, action: str, artifact_ref: str | None) -> list[str]:
    if action == "init_round":
        result = ["/usr/bin/env", "PYTHONPATH=src", PYTHON, GOVERNANCE_REF, "init-round", "--round-root", round_ref]
    else:
        result = [
            "/usr/bin/env",
            "PYTHONPATH=src",
            PYTHON,
            GOVERNANCE_REF,
            "run",
            "--round-root",
            round_ref,
            "--action",
            action,
        ]
    if artifact_ref is not None:
        result.extend(["--artifact-ref", artifact_ref])
    return result


def _fixed_action_artifact_ref(round_ref: str, result_round: str, action: str) -> str | None:
    refs = _fixed_refs(round_ref, result_round)
    if action == "result_review_binding":
        return refs["result_review"]
    if action == "final_seal_audit_binding":
        return refs["final_audit"]
    return None


def _receipt_ref(round_ref: str, sequence: int) -> str:
    return f"{round_ref}/receipts/receipt-{sequence:02d}.json"


def _index_ref(round_ref: str, sequence: int) -> str:
    return f"{round_ref}/receipts/receipt-index-{sequence:02d}.json"


def _null_bindings(action: str) -> dict[str, None]:
    return {key: None for key in BINDING_KEYS[action]}


def _verify_receipt_index(root: Path, ref: str, pass_actions: tuple[str, ...], failure_actions: tuple[str, ...]) -> dict[str, Any]:
    raw = _read(root, ref)
    actions = (*pass_actions, *failure_actions)
    index = validate_p03_receipt_index(_json(raw, "Phase 03 receipt index"), expected_actions=actions)
    round_ref = f"{ROUND_PARENT_REF}/{index['result_round']}"
    if (
        PurePosixPath(ref).parent.as_posix() != f"{round_ref}/receipts"
        or ref != _index_ref(round_ref, index["head_sequence"])
    ):
        raise EvidenceValidationError("Phase 03 receipt index is not round-local")
    prior: str | None = None
    receipts: list[dict[str, Any]] = []
    for entry in index["receipts"]:
        expected_ref = _receipt_ref(round_ref, entry["sequence"])
        if entry["receipt_ref"] != expected_ref:
            raise EvidenceValidationError("Phase 03 receipt ref is not canonical")
        receipt_raw = _read(root, entry["receipt_ref"])
        digest = content_digest(receipt_raw)
        if digest != entry["receipt_sha256"]:
            raise EvidenceValidationError("Phase 03 receipt digest mismatch")
        receipt = validate_p03_receipt(_json(receipt_raw, "Phase 03 receipt"), expected_actions=actions)
        action_artifact_ref = _fixed_action_artifact_ref(
            round_ref,
            index["result_round"],
            receipt["action"],
        )
        if (
            receipt["sequence"] != entry["sequence"]
            or receipt["action"] != entry["action"]
            or receipt["result_round"] != index["result_round"]
            or receipt["prior_receipt_sha256"] != prior
            or receipt["execution_class"] != _execution_class(receipt["action"])
            or receipt["handler_id"] != _handler_id(receipt["action"])
            or receipt["external_argv"]
            != _external_argv(
                round_ref,
                receipt["action"],
                action_artifact_ref,
            )
        ):
            raise EvidenceValidationError("Phase 03 receipt/index/action binding mismatch")
        child = _child_argv(round_ref, receipt["action"])
        environment = _child_environment(root, round_ref, receipt["action"]) if child is not None else {}
        if (
            receipt["child_argv"] != ([] if child is None else child)
            or receipt["child_environment_sha256"] != content_digest(environment)
            or set(receipt["bindings"]) != set(BINDING_KEYS[receipt["action"]])
        ):
            raise EvidenceValidationError("Phase 03 receipt child/binding registry mismatch")
        for stream in ("stdout", "stderr"):
            expected_stream_ref = (
                f"{round_ref}/logs/{receipt['action'].replace('_', '-')}.{stream}"
            )
            if receipt[f"{stream}_ref"] != expected_stream_ref:
                raise EvidenceValidationError("Phase 03 receipt stream ref is not canonical")
            stream_raw = _read(root, receipt[f"{stream}_ref"])
            if (
                content_digest(stream_raw) != receipt[f"{stream}_sha256"]
                or len(stream_raw) != receipt[f"{stream}_byte_count"]
            ):
                raise EvidenceValidationError("Phase 03 receipt stream binding mismatch")
        receipts.append({"entry": entry, "record": receipt, "sha256": digest})
        prior = digest
    return {
        "index_ref": ref,
        "index_sha256": content_digest(raw),
        "record": index,
        "receipts": receipts,
    }


def _latest_chain(
    root: Path,
    round_ref: str,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any] | None:
    directory = root / round_ref / "receipts"
    if not directory.exists():
        return None
    if directory.is_symlink() or not directory.is_dir():
        raise EvidenceValidationError("Phase 03 receipt directory is unsafe")
    candidates = sorted(directory.glob("receipt-index-*.json"), key=lambda path: path.name)
    if not candidates:
        return None
    verified = [
        _verify_receipt_index(root, path.relative_to(root).as_posix(), pass_actions, failure_actions)
        for path in candidates
    ]
    terminal = verified[-1]["record"]["receipts"]
    for sequence, item in enumerate(verified, start=1):
        if item["record"]["head_sequence"] != sequence or item["record"]["receipts"] != terminal[:sequence]:
            raise EvidenceValidationError("Phase 03 receipt indexes are not immutable contiguous prefixes")
    return verified[-1]


def _append_receipt(
    root: Path,
    round_ref: str,
    result_round: str,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
    action: str,
    *,
    artifact_ref: str | None,
    started_at: str,
    ended_at: str,
    wall_time_ns: int,
    exit_code: int,
    stdout_ref: str,
    stderr_ref: str,
    bindings: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    chain = _latest_chain(root, round_ref, pass_actions, failure_actions)
    entries = [] if chain is None else list(chain["record"]["receipts"])
    sequence = len(entries) + 1
    child = _child_argv(round_ref, action)
    environment = _child_environment(root, round_ref, action) if child is not None else {}
    stdout = _read(root, stdout_ref)
    stderr = _read(root, stderr_ref)
    receipt = {
        "schema_version": "p03_command_receipt@1",
        "phase": PHASE,
        "result_round": result_round,
        "sequence": sequence,
        "action": action,
        "execution_class": _execution_class(action),
        "handler_id": _handler_id(action),
        "external_argv": _external_argv(round_ref, action, artifact_ref),
        "child_argv": [] if child is None else child,
        "child_environment_sha256": content_digest(environment),
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
        "prior_receipt_sha256": None if chain is None else chain["record"]["head_sha256"],
        "bindings": dict(bindings),
    }
    validate_p03_receipt(receipt, expected_actions=(*pass_actions, *failure_actions))
    written = _write_json(root, _receipt_ref(round_ref, sequence), receipt)
    entry = {
        "sequence": sequence,
        "action": action,
        "receipt_ref": _receipt_ref(round_ref, sequence),
        "receipt_sha256": written["sha256"],
    }
    index = {
        "schema_version": "p03_receipt_index@1",
        "phase": PHASE,
        "result_round": result_round,
        "receipts": [*entries, entry],
        "head_sequence": sequence,
        "head_sha256": written["sha256"],
    }
    _write_json(root, _index_ref(round_ref, sequence), index)
    verified = _verify_receipt_index(root, _index_ref(round_ref, sequence), pass_actions, failure_actions)
    return {"ref": entry["receipt_ref"], "sha256": written["sha256"], "record": receipt}, verified


def _receipt_for(chain: Mapping[str, Any], action: str) -> dict[str, Any] | None:
    matches = [item["record"] for item in chain["receipts"] if item["record"]["action"] == action]
    if len(matches) > 1:
        raise EvidenceValidationError(f"Phase 03 receipt chain repeats action: {action}")
    return matches[0] if matches else None


def _load_registry(root: Path) -> tuple[dict[str, Any], tuple[str, ...], tuple[str, ...]]:
    entry = verify_p03_entry(root)
    record = entry["record"]
    pass_actions = tuple(record["p03_pass_actions"])
    failure_actions = tuple(record["p03_failure_suffix_actions"])
    if (
        len(pass_actions) != 24
        or len(set(pass_actions)) != 24
        or failure_actions != ("bind_scoped_repair", "close_round")
        or set(pass_actions) & set(failure_actions)
        or set(BINDING_KEYS) != set(pass_actions) | set(failure_actions)
        or tuple(FORMAL_TESTS) != P03_GUARDED_ACTIONS[:-1]
    ):
        raise EvidenceValidationError("Phase 03 effective action registry mismatch")
    if tuple(sorted(COMPILE_REFS, key=lambda item: item.encode("utf-8"))) != COMPILE_REFS:
        raise EvidenceValidationError("Phase 03 compile registry must be sorted by UTF-8 bytes")
    if set(COMPILE_REFS) != set(record["implementation_allowlist_exact"]):
        raise EvidenceValidationError("Phase 03 compile registry differs from the frozen exact allowlist")
    return entry, pass_actions, failure_actions


def _verify_p02_entry_boundary(root: Path, entry_record: Mapping[str, Any]) -> None:
    stable_ref = entry_record["p02_stable_decision_ref"]
    stable_raw = _read(root, stable_ref)
    final_raw = _read(root, P02_FINAL_REF)
    if content_digest(stable_raw) != entry_record["p02_stable_decision_sha256"] or stable_raw != final_raw:
        raise EvidenceValidationError("Phase 03 P02 stable/final binding drift")
    stable_info = os.stat(root / stable_ref, follow_symlinks=False)
    final_info = os.stat(root / P02_FINAL_REF, follow_symlinks=False)
    if (
        not stat.S_ISREG(stable_info.st_mode)
        or not stat.S_ISREG(final_info.st_mode)
        or stable_info.st_dev != final_info.st_dev
        or stable_info.st_ino != final_info.st_ino
        or stable_info.st_nlink < 2
    ):
        raise EvidenceValidationError("Phase 03 P02 stable decision is not the sealed hard link")
    decision = _json(stable_raw, "P02 stable decision", canonical=True)
    if (
        decision.get("schema_version") != "p02_final_decision@1"
        or decision.get("phase") != "P02"
        or decision.get("decision") != "pass"
        or decision.get("publication_mode") != "disabled"
        or decision.get("extraction_bundle_semantic_digest")
        != entry_record["p02_extraction_bundle_semantic_digest"]
        or decision.get("primary_criterion", {}).get("all_pass") is not True
        or any(decision.get("vetoes", {}).values())
        or len(decision.get("non_claims", [])) != 8
    ):
        raise EvidenceValidationError("Phase 03 P02 stable decision boundary mismatch")
    terminal_ref = entry_record["p02_terminal_receipt_index_ref"]
    terminal_raw = _read(root, terminal_ref)
    terminal = _json(terminal_raw, "P02 terminal receipt index", canonical=True)
    if (
        content_digest(terminal_raw) != entry_record["p02_terminal_receipt_index_sha256"]
        or terminal.get("schema_version") != "p02_receipt_index@1"
        or [item.get("check_id") for item in terminal.get("receipts", [])] != list(P02_PASS_ACTIONS)
        or terminal.get("head_sequence") != 24
    ):
        raise EvidenceValidationError("Phase 03 P02 terminal receipt index mismatch")
    prior: str | None = None
    for sequence, item in enumerate(terminal["receipts"], start=1):
        receipt_raw = _read(root, item["receipt_ref"])
        if content_digest(receipt_raw) != item["receipt_sha256"]:
            raise EvidenceValidationError("Phase 03 P02 terminal receipt digest mismatch")
        receipt = _json(receipt_raw, "P02 terminal receipt", canonical=True)
        if (
            receipt.get("sequence") != sequence
            or receipt.get("check_id") != P02_PASS_ACTIONS[sequence - 1]
            or receipt.get("exit_code") != 0
            or receipt.get("prior_receipt_sha256") != prior
        ):
            raise EvidenceValidationError("Phase 03 P02 terminal receipt chain mismatch")
        prior = item["receipt_sha256"]
    final_receipt = _json(_read(root, terminal["receipts"][-1]["receipt_ref"]), "P02 publication receipt")
    if final_receipt.get("bindings", {}).get("same_inode") is not True or final_receipt.get("bindings", {}).get("same_digest") is not True:
        raise EvidenceValidationError("Phase 03 P02 terminal receipt lacks link equality")


def _verify_review_authority(root: Path, entry_record: Mapping[str, Any]) -> None:
    ref = entry_record["review_budget_carry_forward_ref"]
    raw = _read(root, ref)
    if content_digest(raw) != entry_record["review_budget_carry_forward_sha256"]:
        raise EvidenceValidationError("Phase 03 review authority binding drift")
    record = _json(raw, "Phase 03 review-budget carry-forward")
    expected_keys = {
        "authority",
        "date",
        "entry_recovery_plan_ref",
        "entry_recovery_plan_sha256",
        "entry_recovery_review_ref",
        "entry_recovery_review_sha256",
        "final_seal_audit_rounds_reserved",
        "non_claim",
        "phase",
        "recovery",
        "result_review_rounds_reserved",
        "schema_version",
        "source_budget_ref",
        "source_budget_sha256",
        "source_plan_review_ref",
        "source_plan_review_sha256",
    }
    if (
        set(record) != expected_keys
        or record["schema_version"] != "p03r1_review_budget_carry_forward@1"
        or record["phase"] != PHASE
        or record["recovery"] != REVISION
        or record["authority"] != "human_user"
        or record["result_review_rounds_reserved"] != 1
        or record["final_seal_audit_rounds_reserved"] != 1
        or record["entry_recovery_plan_ref"] != entry_record["entry_recovery_plan_ref"]
        or record["entry_recovery_plan_sha256"] != entry_record["entry_recovery_plan_sha256"]
        or record["entry_recovery_review_ref"] != entry_record["agreeing_entry_recovery_review_ref"]
        or record["entry_recovery_review_sha256"] != entry_record["agreeing_entry_recovery_review_sha256"]
    ):
        raise EvidenceValidationError("Phase 03 review authority contract mismatch")
    for ref_key, digest_key in (
        ("entry_recovery_plan_ref", "entry_recovery_plan_sha256"),
        ("entry_recovery_review_ref", "entry_recovery_review_sha256"),
        ("source_budget_ref", "source_budget_sha256"),
        ("source_plan_review_ref", "source_plan_review_sha256"),
    ):
        if _digest(root, record[ref_key]) != record[digest_key]:
            raise EvidenceValidationError("Phase 03 review authority artifact drift")
    review_raw = _read(root, record["entry_recovery_review_ref"])
    if not review_raw.decode("utf-8", "strict").rstrip().endswith("VERDICT: AGREE"):
        raise EvidenceValidationError("Phase 03 recovery review is not agreeing")


def _predecessor_bindings(
    root: Path,
    result_round: str,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any]:
    number = int(result_round[2:])
    parent = root / ROUND_PARENT_REF
    existing: list[str] = []
    if parent.exists():
        if parent.is_symlink() or not parent.is_dir():
            raise EvidenceValidationError("Phase 03 result-rounds parent is unsafe")
        existing = sorted(path.name for path in parent.iterdir() if ROUND_RE.fullmatch(path.name))
    expected = [f"rr{index:02d}" for index in range(1, number)]
    if existing != expected:
        raise EvidenceValidationError("Phase 03 result-round namespace is not the exact predecessor prefix")
    nulls = {
        "predecessor_round_close_ref": None,
        "predecessor_round_close_sha256": None,
        "predecessor_terminal_receipt_index_ref": None,
        "predecessor_terminal_receipt_index_sha256": None,
    }
    if number == 1:
        return nulls
    prior_round = f"rr{number - 1:02d}"
    prior_ref = f"{ROUND_PARENT_REF}/{prior_round}"
    close_ref = f"{prior_ref}/round-close.json"
    close_raw = _read(root, close_ref)
    close = _json(close_raw, "Phase 03 predecessor close")
    chain = _latest_chain(root, prior_ref, pass_actions, failure_actions)
    if (
        chain is None
        or chain["receipts"][-1]["record"]["action"] != "close_round"
        or chain["receipts"][-1]["record"]["exit_code"] != 0
        or close.get("schema_version") != "p03_round_close@1"
        or close.get("result_round") != prior_round
        or close.get("decision") != "blocked"
    ):
        raise EvidenceValidationError("Phase 03 predecessor round is not safely closed")
    return {
        "predecessor_round_close_ref": close_ref,
        "predecessor_round_close_sha256": content_digest(close_raw),
        "predecessor_terminal_receipt_index_ref": chain["index_ref"],
        "predecessor_terminal_receipt_index_sha256": chain["index_sha256"],
    }


def _init_round(
    root: Path,
    entry: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
    round_root: str,
) -> dict[str, Any]:
    started = _utc_now()
    start_ns = time.monotonic_ns()
    round_ref, result_round, round_path = _round_context(root, round_root, must_exist=False)
    if sys.executable != PYTHON or os.environ.get("PYTHONPATH") != "src":
        raise EvidenceValidationError("Phase 03 init-round requires the pinned Python and PYTHONPATH=src")
    record = entry["record"]
    _verify_p02_entry_boundary(root, record)
    _verify_review_authority(root, record)
    predecessor = _predecessor_bindings(root, result_round, pass_actions, failure_actions)
    parent = round_path.parent
    if not parent.exists():
        if parent.parent.is_symlink() or not parent.parent.is_dir():
            raise EvidenceValidationError("Phase 03 result-rounds parent cannot be created safely")
        parent.mkdir(mode=0o700, parents=False, exist_ok=False)
    _mkdir_exact(round_path)
    for suffix in ("governance", "logs", "receipts", "inputs"):
        _mkdir_exact(round_path / suffix)
    for suffix in ("home", "tmp"):
        _mkdir_exact(round_path / "governance" / suffix)
    manifest_ref = _fixed_refs(round_ref, result_round)["round_implementation_manifest"]
    manifest_raw = _implementation_manifest(root)
    manifest_write = _write(root, manifest_ref, manifest_raw)
    if _manifest_records(manifest_raw) != _verify_manifest_live(root, manifest_ref):
        raise EvidenceValidationError("Phase 03 round implementation manifest failed reopen verification")
    pre_round_ref = _fixed_refs(round_ref, result_round)["pre_round_worktree"]
    pre_round_write = _write_json(root, pre_round_ref, _build_pre_round_worktree(root, result_round))
    runtime = record["runtime_measurement"]
    if (
        runtime["python_executable"] != PYTHON
        or runtime["python_version"] != sys.version.split()[0]
        or runtime["pytest_version"] != "9.0.2"
    ):
        raise EvidenceValidationError("Phase 03 runtime differs from the entry measurement")
    bindings = {
        "entry_record_ref": ENTRY_RECORD_REF,
        "entry_record_sha256": entry["sha256"],
        "entry_implementation_manifest_ref": record["implementation_entry_manifest_ref"],
        "entry_implementation_manifest_sha256": record["implementation_entry_manifest_sha256"],
        "round_implementation_manifest_ref": manifest_ref,
        "round_implementation_manifest_sha256": manifest_write["sha256"],
        "entry_protected_manifest_ref": record["protected_entry_manifest_ref"],
        "entry_protected_manifest_sha256": record["protected_entry_manifest_sha256"],
        "entry_immutable_input_manifest_ref": record["immutable_input_manifest_ref"],
        "entry_immutable_input_manifest_sha256": record["immutable_input_manifest_sha256"],
        "pre_round_worktree_ref": pre_round_ref,
        "pre_round_worktree_sha256": pre_round_write["sha256"],
        "reviewed_plan_ref": record["reviewed_plan_ref"],
        "reviewed_plan_sha256": record["reviewed_plan_sha256"],
        "reviewed_recovery_plan_ref": record["entry_recovery_plan_ref"],
        "reviewed_recovery_plan_sha256": record["entry_recovery_plan_sha256"],
        "agreeing_recovery_review_ref": record["agreeing_entry_recovery_review_ref"],
        "agreeing_recovery_review_sha256": record["agreeing_entry_recovery_review_sha256"],
        "p02_stable_decision_ref": record["p02_stable_decision_ref"],
        "p02_stable_decision_sha256": record["p02_stable_decision_sha256"],
        "p02_terminal_receipt_index_ref": record["p02_terminal_receipt_index_ref"],
        "p02_terminal_receipt_index_sha256": record["p02_terminal_receipt_index_sha256"],
        "p02_extraction_bundle_index_ref": record["p02_extraction_bundle_index_ref"],
        "p02_extraction_bundle_index_sha256": record["p02_extraction_bundle_index_sha256"],
        "p02_obligations_ref": record["p02_obligations_ref"],
        "p02_obligations_sha256": record["p02_obligations_sha256"],
        "p02_close_ref": record["p02_close_ref"],
        "p02_close_sha256": record["p02_close_sha256"],
        **predecessor,
    }
    if set(bindings) != set(BINDING_KEYS["init_round"]):
        raise EvidenceValidationError("Phase 03 init-round bindings differ from the fixed registry")
    measurement = {
        "schema_version": "p03_round_initialization@1",
        "phase": PHASE,
        "revision": REVISION,
        "result_round": result_round,
        "git_commit": _git_commit(root),
        "implementation_manifest_sha256": manifest_write["sha256"],
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
        "pytest_version": runtime["pytest_version"],
        "device_mode": "cpu_only_no_gpu_requested",
    }
    stdout_ref = f"{round_ref}/logs/init-round.stdout"
    stderr_ref = f"{round_ref}/logs/init-round.stderr"
    _write(root, stdout_ref, canonical_json_bytes(measurement) + b"\n")
    _write(root, stderr_ref, b"")
    receipt, chain = _append_receipt(
        root,
        round_ref,
        result_round,
        pass_actions,
        failure_actions,
        "init_round",
        artifact_ref=None,
        started_at=started,
        ended_at=_utc_now(),
        wall_time_ns=time.monotonic_ns() - start_ns,
        exit_code=0,
        stdout_ref=stdout_ref,
        stderr_ref=stderr_ref,
        bindings=bindings,
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


def _git_commit(root: Path) -> str:
    completed = subprocess.run(
        ["/usr/bin/git", "rev-parse", "HEAD"],
        cwd=root,
        env={"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PATH": "/usr/bin:/bin"},
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    value = completed.stdout.decode("ascii", "strict").strip()
    if completed.returncode != 0 or re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value) is None:
        raise EvidenceValidationError("Phase 03 cannot measure the git commit")
    return value


def _run_subprocess(
    root: Path,
    round_ref: str,
    action: str,
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    argv = _child_argv(round_ref, action)
    if argv is None:
        raise EvidenceValidationError(f"Phase 03 subprocess action has no child argv: {action}")
    completed = subprocess.run(
        argv,
        cwd=root,
        env=_child_environment(root, round_ref, action),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        return completed.returncode, completed.stdout, completed.stderr, _null_bindings(action)
    bindings: dict[str, Any] = {}
    if action == "generate_context_bundle":
        try:
            line = completed.stdout.rstrip(b"\n")
            parsed = _json(line, "Phase 03 generator stdout")
            expected = {"bundle_index_ref", "bundle_index_sha256", "bundle_semantic_digest"}
            if set(parsed) != expected:
                raise EvidenceValidationError("Phase 03 generator stdout keys mismatch")
            reconstructed = reconstruct_context_bundle(root, parsed["bundle_index_ref"])
            if (
                _digest(root, parsed["bundle_index_ref"]) != parsed["bundle_index_sha256"]
                or reconstructed["bundle_semantic_digest"] != parsed["bundle_semantic_digest"]
            ):
                raise EvidenceValidationError("Phase 03 generator stdout binding mismatch")
            bindings = parsed
        except Exception as exc:
            return 1, completed.stdout, completed.stderr + f"{type(exc).__name__}: {exc}\n".encode(), _null_bindings(action)
    return 0, completed.stdout, completed.stderr, bindings


def _mutation_gate(root: Path, round_ref: str) -> tuple[int, bytes, bytes, dict[str, Any]]:
    refs = context_artifact_refs(round_ref)
    raw = _read(root, refs["mutation_matrix"])
    matrix = validate_p03_mutation_matrix(_json(raw, "Phase 03 mutation matrix"))
    bindings = {
        "mutation_matrix_ref": refs["mutation_matrix"],
        "mutation_matrix_sha256": content_digest(raw),
        "all_pass": matrix["all_pass"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _zero_gate(root: Path, round_ref: str) -> tuple[int, bytes, bytes, dict[str, Any]]:
    refs = context_artifact_refs(round_ref)
    reconstructed = reconstruct_context_bundle(root, refs["bundle_index"])
    bindings = {
        "guard_index_ref": refs["guard_index"],
        "guard_index_sha256": _digest(root, refs["guard_index"]),
        "backend_request_count": reconstructed["backend_request_count"],
        "source_edit_count": reconstructed["source_edit_count"],
        "publication_count": reconstructed["publication_count"],
    }
    if any(bindings[key] != 0 for key in ("backend_request_count", "source_edit_count", "publication_count")):
        raise EvidenceValidationError("Phase 03 zero-backend/source-edit/publication gate is nonzero")
    return 0, canonical_json_bytes(bindings), b"", bindings


def _protected_gate(root: Path, entry_record: Mapping[str, Any]) -> tuple[int, bytes, bytes, dict[str, Any]]:
    ref = entry_record["protected_entry_manifest_ref"]
    if _digest(root, ref) != entry_record["protected_entry_manifest_sha256"]:
        raise EvidenceValidationError("Phase 03 protected manifest drift")
    records = _verify_manifest_live(root, ref)
    bindings = {
        "protected_manifest_ref": ref,
        "protected_manifest_sha256": entry_record["protected_entry_manifest_sha256"],
        "verified_target_count": len(records),
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _implementation_exit(root: Path, round_ref: str, result_round: str) -> tuple[int, bytes, bytes, dict[str, Any]]:
    refs = _fixed_refs(round_ref, result_round)
    raw = _implementation_manifest(root)
    written = _write(root, refs["implementation_exit_manifest"], raw)
    bindings = {
        "implementation_exit_manifest_ref": refs["implementation_exit_manifest"],
        "implementation_exit_manifest_sha256": written["sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _git_status_paths(root: Path) -> set[str]:
    completed = subprocess.run(
        ["/usr/bin/git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=root,
        env={"LANG": "C.UTF-8", "LC_ALL": "C.UTF-8", "PATH": "/usr/bin:/bin"},
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise EvidenceValidationError("Phase 03 cannot measure git status")
    entries = completed.stdout.split(b"\x00")
    paths: set[str] = set()
    index = 0
    while index < len(entries):
        raw = entries[index]
        index += 1
        if not raw:
            continue
        text = raw.decode("utf-8", "surrogateescape")
        if len(text) < 4 or text[2] != " ":
            raise EvidenceValidationError("Phase 03 git status record is malformed")
        status = text[:2]
        path = text[3:]
        if status[0] in {"R", "C"}:
            if index >= len(entries) or not entries[index]:
                raise EvidenceValidationError("Phase 03 git status rename record is incomplete")
            path = entries[index].decode("utf-8", "surrogateescape")
            index += 1
        validate_logical_path(path, name="Phase 03 git status path")
        paths.add(path)
    return paths


def _build_pre_round_worktree(root: Path, result_round: str) -> dict[str, Any]:
    entries: list[dict[str, Any]] = []
    for ref in sorted(_git_status_paths(root), key=lambda item: item.encode("utf-8")):
        path = root / ref
        if path.is_symlink():
            raise EvidenceValidationError("Phase 03 pre-round dirty path may not be a symlink")
        if path.exists():
            raw = _read(root, ref)
            entry = {
                "ref": ref,
                "state": "regular",
                "sha256": content_digest(raw),
                "byte_count": len(raw),
            }
        else:
            entry = {"ref": ref, "state": "absent", "sha256": None, "byte_count": None}
        entries.append(entry)
    return {
        "schema_version": "p03_pre_round_worktree@1",
        "phase": PHASE,
        "result_round": result_round,
        "entries": entries,
    }


def _verify_pre_round_worktree(
    root: Path,
    ref: str,
    expected_sha256: str,
    result_round: str,
) -> dict[str, Any]:
    raw = _read(root, ref)
    if content_digest(raw) != expected_sha256:
        raise EvidenceValidationError("Phase 03 pre-round worktree binding drift")
    record = _json(raw, "Phase 03 pre-round worktree")
    if (
        set(record) != {"schema_version", "phase", "result_round", "entries"}
        or record["schema_version"] != "p03_pre_round_worktree@1"
        or record["phase"] != PHASE
        or record["result_round"] != result_round
        or not isinstance(record["entries"], list)
    ):
        raise EvidenceValidationError("Phase 03 pre-round worktree schema mismatch")
    refs: list[str] = []
    for entry in record["entries"]:
        if not isinstance(entry, dict) or set(entry) != {"ref", "state", "sha256", "byte_count"}:
            raise EvidenceValidationError("Phase 03 pre-round worktree entry mismatch")
        logical_ref = validate_logical_path(entry["ref"], name="pre-round worktree ref")
        refs.append(logical_ref)
        if entry["state"] == "regular":
            if SHA_RE.fullmatch(entry["sha256"] or "") is None or type(entry["byte_count"]) is not int:
                raise EvidenceValidationError("Phase 03 pre-round regular-file binding is invalid")
        elif entry["state"] == "absent":
            if entry["sha256"] is not None or entry["byte_count"] is not None:
                raise EvidenceValidationError("Phase 03 pre-round absent-file binding is invalid")
        else:
            raise EvidenceValidationError("Phase 03 pre-round worktree state is invalid")
    if refs != sorted(set(refs), key=lambda item: item.encode("utf-8")):
        raise EvidenceValidationError("Phase 03 pre-round worktree refs are not ordered and unique")
    return record


def _allowlist_gate(
    root: Path,
    entry_record: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    refs = _fixed_refs(round_ref, result_round)
    before = _manifest_records(_read(root, entry_record["implementation_entry_manifest_ref"]))
    after_ref = refs["implementation_exit_manifest"]
    after = _manifest_records(_read(root, after_ref))
    touched = {
        ref
        for ref in set(before) | set(after)
        if before.get(ref) != after.get(ref)
    }
    # New governance/source files are captured by the exit manifest; status is
    # included to retain deletions and any path outside src/tests/scripts.
    touched |= _git_status_paths(root)
    exact = set(entry_record["implementation_allowlist_exact"])
    prefixes = tuple(entry_record["implementation_allowlist_prefixes"])
    allowed = sorted(
        (ref for ref in touched if ref in exact or any(ref.startswith(prefix) for prefix in prefixes)),
        key=lambda item: item.encode("utf-8"),
    )
    unexpected = sorted(
        (ref for ref in touched if ref not in exact and not any(ref.startswith(prefix) for prefix in prefixes)),
        key=lambda item: item.encode("utf-8"),
    )
    # Paths dirty before P03 are preserved by the entry manifest and are not a
    # P03 delta unless their entry/current digests differ.
    protected = _manifest_records(_read(root, entry_record["protected_entry_manifest_ref"]))
    init = chain["receipts"][0]["record"]
    if init["action"] != "init_round" or init["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 allowlist lacks a trusted initializer")
    pre_round = _verify_pre_round_worktree(
        root,
        init["bindings"]["pre_round_worktree_ref"],
        init["bindings"]["pre_round_worktree_sha256"],
        result_round,
    )
    pre_round_unchanged: set[str] = set()
    for item in pre_round["entries"]:
        ref = item["ref"]
        path = root / ref
        if (
            item["state"] == "regular"
            and path.exists()
            and not path.is_symlink()
            and path.is_file()
            and _digest(root, ref) == item["sha256"]
        ):
            pre_round_unchanged.add(ref)
    entry_dirty = {
        ref
        for ref in _git_status_paths(root)
        if (ref in before and before.get(ref) == after.get(ref))
        or (ref in protected and _digest(root, ref) == protected[ref])
        or ref in pre_round_unchanged
    }
    unexpected = [ref for ref in unexpected if ref not in entry_dirty]
    touched = sorted(set(allowed) | set(unexpected), key=lambda item: item.encode("utf-8"))
    touched_raw = b"".join(f"{ref}\n".encode("utf-8") for ref in touched)
    unexpected_raw = b"".join(f"{ref}\n".encode("utf-8") for ref in unexpected)
    touched_written = _write(root, refs["touched_paths"], touched_raw)
    unexpected_written = _write(root, refs["unexpected_paths"], unexpected_raw)
    bindings = {
        "touched_paths_ref": refs["touched_paths"],
        "touched_paths_sha256": touched_written["sha256"],
        "unexpected_paths_ref": refs["unexpected_paths"],
        "unexpected_paths_sha256": unexpected_written["sha256"],
    }
    if unexpected:
        return 1, canonical_json_bytes({"touched": touched, "unexpected": unexpected}), unexpected_raw, bindings
    return 0, canonical_json_bytes({"touched": touched, "unexpected": []}), b"", bindings


def _artifact_inventory(root: Path, refs: list[tuple[str, str]]) -> list[dict[str, Any]]:
    inventory: list[dict[str, Any]] = []
    seen: set[str] = set()
    for ref, role in refs:
        if ref in seen:
            continue
        seen.add(ref)
        raw = _read(root, ref)
        inventory.append(
            {
                "logical_ref": ref,
                "sha256": content_digest(raw),
                "byte_count": len(raw),
                "role": role,
            }
        )
    return inventory


def _action_success(chain: Mapping[str, Any], action: str) -> bool:
    receipt = _receipt_for(chain, action)
    return receipt is not None and receipt["exit_code"] == 0


def _phase_measurements(root: Path, round_ref: str, chain: Mapping[str, Any]) -> dict[str, Any]:
    refs = context_artifact_refs(round_ref)
    reconstructed = reconstruct_context_bundle(root, refs["bundle_index"])
    manifests_value = _json(_read(root, refs["manifests"]), "Phase 03 manifest collection")
    manifests = manifests_value["manifests"]
    symbol_value = _json(_read(root, refs["symbol_ledger"]), "Phase 03 symbol ledger")
    typed_value = _json(_read(root, refs["typed_assumptions"]), "Phase 03 typed assumptions")
    context_value = _json(_read(root, refs["context_ledger"]), "Phase 03 context ledger")
    math_value = _json(_read(root, refs["mathematical_ledger"]), "Phase 03 mathematical ledger")
    mutation_value = validate_p03_mutation_matrix(_json(_read(root, refs["mutation_matrix"]), "Phase 03 mutation matrix"))
    source_support_exact = True
    for manifest in manifests:
        if manifest["entry_state"] != "context_search":
            continue
        if manifest["terminal_state"] in {"stated", "source_supported"}:
            source_support_exact &= any(
                item.get("applicability_state") == "explicit"
                and item.get("source_ref", {}).get("dependency_path")
                for item in manifest["candidates"]
            )
    card_digests = {
        "7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0",
        "d9f072ac09016b17d5630556329bc871e79386a442c8c26587ef39a0134eeaac",
    }
    card_ok = True
    for entry in symbol_value["entries"]:
        if entry["obligation_digest"] not in card_digests:
            continue
        pi = next(item for item in entry["resolutions"] if item["symbol"] == r"\pi")
        card_ok &= pi["state"] in {"resolved", "ambiguous"} and pi["role"] in {"policy_candidate", None}
    primary = {
        "all_17_obligations_partitioned_exactly": reconstructed["obligation_count"] == 17
        and reconstructed["context_search_count"] == 14
        and reconstructed["extraction_veto_count"] == 3,
        "all_context_manifests_validate": len(manifests) == 17,
        "all_source_support_has_exact_applicable_provenance": source_support_exact,
        "search_boundaries_and_states_preserved": all(
            item["entry_state"] == "extraction_veto"
            or item["terminal_state"] != "not_found_after_search"
            or (
                not item["budget_exhausted"]
                and not item["unsearched_files"]
                and not item["engineering_diagnostics"]
            )
            for item in manifests
        ),
        "symbol_and_notation_ambiguity_preserved": reconstructed["notation_ledger_entry_count"] == 14,
        "typed_assumption_states_orthogonal": len(typed_value["assumptions"]) == 14
        and len({item["binding_digest"] for item in typed_value["assumptions"]}) == 14,
        "report_state_ledgers_separated": len(context_value["entries"]) == 17
        and math_value["entries"] == [],
        "frozen_card_pi_not_posterior_by_spelling": card_ok,
        "zero_backend_source_edit_publication": reconstructed["backend_request_count"] == 0
        and reconstructed["source_edit_count"] == 0
        and reconstructed["publication_count"] == 0,
        "governance_allowlist_and_protected_state_pass": all(
            _action_success(chain, action)
            for action in ("protected_check", "implementation_exit", "allowlist", "diff")
        ),
    }
    primary["all_pass"] = all(primary.values()) and mutation_value["all_pass"]
    vetoes = {key: False for key in P03_VETO_KEYS}
    vetoes["p02_or_source_binding_drift"] = False
    vetoes["sibling_context_leakage"] = not reconstructed["all_frozen_entries_single_reachable_file"]
    vetoes["invented_or_incomplete_provenance"] = not source_support_exact
    vetoes["integrity_or_symlink_failure"] = any(
        bool(item.get("integrity_vetoes")) for item in manifests
    )
    vetoes["local_absence_promoted_to_corpus_absence"] = not primary["search_boundaries_and_states_preserved"]
    vetoes["not_searched_promoted_to_missing"] = False
    vetoes["lexical_candidate_promoted_to_support"] = not mutation_value["all_pass"]
    vetoes["unconditional_symbol_role"] = not card_ok
    vetoes["candidate_assumption_promoted_to_stated"] = not mutation_value["all_pass"]
    vetoes["context_error_promoted_to_mathematics"] = bool(math_value["entries"])
    vetoes["backend_execution_detected"] = reconstructed["backend_request_count"] != 0
    vetoes["source_edit_detected"] = reconstructed["source_edit_count"] != 0
    vetoes["publication_leak_detected"] = reconstructed["publication_count"] != 0
    vetoes["unexpected_implementation_path"] = not _action_success(chain, "allowlist")
    vetoes["protected_baseline_drift"] = not _action_success(chain, "protected_check")
    vetoes["governance_chain_failure"] = False
    return {
        "reconstructed": reconstructed,
        "primary_criterion": primary,
        "vetoes": vetoes,
    }


def _build_phase_result_record(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    human_ref: str,
    human_raw: bytes,
) -> dict[str, Any]:
    measurements = _phase_measurements(root, round_ref, chain)
    init = chain["receipts"][0]["record"]["bindings"]
    refs = context_artifact_refs(round_ref)
    decision = (
        "candidate_pass_pending_independent_result_review"
        if measurements["primary_criterion"]["all_pass"] and not any(measurements["vetoes"].values())
        else "blocked"
    )
    if parse_p03_human_result(
        human_raw,
        result_round=result_round,
        pre_result_index_sha256=chain["index_sha256"],
    ) != decision:
        raise EvidenceValidationError("Phase 03 human result contradicts reconstructed gates")
    record = {
        "schema_version": "p03_phase_result@1",
        "phase": PHASE,
        "result_round": result_round,
        "decision": decision,
        "publication_mode": "disabled",
        "claim_eligibility": "ineligible",
        "human_result_ref": human_ref,
        "human_result_sha256": content_digest(human_raw),
        "pre_result_receipt_index_ref": chain["index_ref"],
        "pre_result_receipt_index_sha256": chain["index_sha256"],
        "entry_record_ref": init["entry_record_ref"],
        "entry_record_sha256": init["entry_record_sha256"],
        "p02_stable_decision_ref": init["p02_stable_decision_ref"],
        "p02_stable_decision_sha256": init["p02_stable_decision_sha256"],
        "p02_terminal_receipt_index_ref": init["p02_terminal_receipt_index_ref"],
        "p02_terminal_receipt_index_sha256": init["p02_terminal_receipt_index_sha256"],
        "p02_extraction_bundle_index_ref": init["p02_extraction_bundle_index_ref"],
        "p02_extraction_bundle_index_sha256": init["p02_extraction_bundle_index_sha256"],
        "p02_obligations_ref": init["p02_obligations_ref"],
        "p02_obligations_sha256": init["p02_obligations_sha256"],
        "p02_close_ref": init["p02_close_ref"],
        "p02_close_sha256": init["p02_close_sha256"],
        "context_bundle_index_ref": refs["bundle_index"],
        "context_bundle_index_sha256": _digest(root, refs["bundle_index"]),
        "mutation_matrix_ref": refs["mutation_matrix"],
        "mutation_matrix_sha256": _digest(root, refs["mutation_matrix"]),
        "guard_index_ref": refs["guard_index"],
        "guard_index_sha256": _digest(root, refs["guard_index"]),
        "p02_extraction_bundle_semantic_digest": verify_p03_entry(root)["record"][
            "p02_extraction_bundle_semantic_digest"
        ],
        "context_bundle_semantic_digest": measurements["reconstructed"]["bundle_semantic_digest"],
        "backend_request_count": measurements["reconstructed"]["backend_request_count"],
        "source_edit_count": measurements["reconstructed"]["source_edit_count"],
        "publication_count": measurements["reconstructed"]["publication_count"],
        "primary_criterion": measurements["primary_criterion"],
        "vetoes": measurements["vetoes"],
        "non_claims": list(P03_NON_CLAIMS),
    }
    return validate_p03_phase_result(record)


def _verify_phase_result(
    root: Path,
    ref: str,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any]:
    raw = _read(root, ref)
    record = validate_p03_phase_result(_json(raw, "Phase 03 phase result"))
    chain = _verify_receipt_index(root, record["pre_result_receipt_index_ref"], pass_actions, failure_actions)
    if chain["index_sha256"] != record["pre_result_receipt_index_sha256"]:
        raise EvidenceValidationError("Phase 03 result receipt-index binding mismatch")
    human_raw = _read(root, record["human_result_ref"])
    if content_digest(human_raw) != record["human_result_sha256"]:
        raise EvidenceValidationError("Phase 03 human result binding drift")
    round_ref = f"{ROUND_PARENT_REF}/{record['result_round']}"
    expected = _build_phase_result_record(
        root,
        round_ref,
        record["result_round"],
        chain,
        record["human_result_ref"],
        human_raw,
    )
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("Phase 03 result differs from independent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record, "chain": chain}


def _bind_result(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    refs = _fixed_refs(round_ref, result_round)
    human_raw = _read(root, refs["human_result"])
    record = _build_phase_result_record(root, round_ref, result_round, chain, refs["human_result"], human_raw)
    written = _write_json(root, refs["machine_result"], record)
    bindings = {
        "human_result_ref": refs["human_result"],
        "human_result_sha256": content_digest(human_raw),
        "result_ref": refs["machine_result"],
        "result_sha256": written["sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _implementation_delta(root: Path, entry_ref: str, exit_ref: str) -> tuple[list[dict[str, Any]], str]:
    before = _manifest_records(_read(root, entry_ref))
    after = _manifest_records(_read(root, exit_ref))
    delta = [
        {"logical_ref": ref, "entry_sha256": before.get(ref), "exit_sha256": after.get(ref)}
        for ref in sorted(set(before) | set(after), key=lambda item: item.encode("utf-8"))
        if before.get(ref) != after.get(ref)
    ]
    return delta, content_digest(delta)


def _build_run_manifest_record(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any]:
    bind = _receipt_for(chain, "bind_result")
    if bind is None or bind["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 run manifest requires successful result binding")
    result = _verify_phase_result(root, bind["bindings"]["result_ref"], pass_actions, failure_actions)
    init_receipt = chain["receipts"][0]["record"]
    init = init_receipt["bindings"]
    exit_receipt = _receipt_for(chain, "implementation_exit")
    if exit_receipt is None or exit_receipt["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 run manifest requires implementation exit")
    exit_ref = exit_receipt["bindings"]["implementation_exit_manifest_ref"]
    delta, delta_digest = _implementation_delta(root, init["entry_implementation_manifest_ref"], exit_ref)
    artifact_refs: list[tuple[str, str]] = []
    for item in chain["receipts"]:
        receipt = item["record"]
        artifact_refs.extend(
            [
                (item["entry"]["receipt_ref"], f"{receipt['action']}_receipt"),
                (receipt["stdout_ref"], f"{receipt['action']}_stdout"),
                (receipt["stderr_ref"], f"{receipt['action']}_stderr"),
            ]
        )
    artifact_refs.extend(
        [
            (chain["index_ref"], "pre_candidate_receipt_index"),
            (result["ref"], "machine_phase_result"),
            (result["record"]["human_result_ref"], "human_phase_result"),
            (init["entry_record_ref"], "entry_record"),
            (init["round_implementation_manifest_ref"], "round_implementation_manifest"),
            (init["pre_round_worktree_ref"], "pre_round_worktree"),
            (exit_ref, "implementation_exit_manifest"),
        ]
    )
    bundle_index = _json(_read(root, result["record"]["context_bundle_index_ref"]), "Phase 03 bundle index")
    artifact_refs.append((result["record"]["context_bundle_index_ref"], "context_bundle_index"))
    artifact_refs.extend((item["ref"], "context_bundle_constituent") for item in bundle_index["artifacts"])
    guard = _json(_read(root, result["record"]["guard_index_ref"]), "Phase 03 guard index")
    artifact_refs.extend(
        (entry[key], f"guard_{key}")
        for entry in guard["entries"]
        for key in ("attestation_ref", "ledger_ref")
    )
    record = {
        "schema_version": "p03_run_manifest@1",
        "phase": PHASE,
        "result_round": result_round,
        "git_commit": _git_commit(root),
        "started_at_utc": init_receipt["started_at_utc"],
        "ended_at_utc": chain["receipts"][-1]["record"]["ended_at_utc"],
        "wall_time_ns": sum(item["record"]["wall_time_ns"] for item in chain["receipts"]),
        "environment": {
            "python_executable": PYTHON,
            "python_version": sys.version.split()[0],
            "pytest_version": verify_p03_entry(root)["record"]["runtime_measurement"]["pytest_version"],
            "pythonpath": "src",
            "locale": "C.UTF-8",
        },
        "device_execution": {
            "mode": "cpu_only_context_parsing_and_tests",
            "gpu_requested": False,
            "gpu_initialized": False,
            "cuda_visible_devices": "-1",
        },
        "random_seed_policy": {
            "randomized_scientific_computation": False,
            "python_hash_seed": "0",
            "seeds": [],
        },
        "plan_ref": init["reviewed_plan_ref"],
        "plan_sha256": init["reviewed_plan_sha256"],
        "result_ref": result["ref"],
        "result_sha256": result["sha256"],
        "governance_receipt_family_ref": f"{round_ref}/receipts",
        "pre_candidate_receipt_index_ref": chain["index_ref"],
        "pre_candidate_receipt_index_sha256": chain["index_sha256"],
        "entry_record_ref": init["entry_record_ref"],
        "entry_record_sha256": init["entry_record_sha256"],
        "implementation_entry_manifest_sha256": init["entry_implementation_manifest_sha256"],
        "implementation_round_manifest_sha256": init["round_implementation_manifest_sha256"],
        "implementation_exit_manifest_sha256": exit_receipt["bindings"]["implementation_exit_manifest_sha256"],
        "implementation_delta_digest": delta_digest,
        "source_data_version": "p02r3-sealed-17-obligation-corpus+p03-entry-rooted-context@1",
        "frozen_source_digests": {
            ref: _digest(root, ref)
            for ref in (
                "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
                "docs/risky-debt-maliar-deep-learning-lecture-note.tex",
            )
        },
        "external_tool_considerations": [
            {
                "tool": "repository_native_context_scanner",
                "role": "entry-rooted dependency and exact source provenance",
                "availability_version_evidence": "p03_context_dependency_graph@1 from bound source bytes",
                "selected": True,
                "certifying_status": "noncertifying_context_evidence",
            },
            {
                "tool": "P02_byte_preserving_locator",
                "role": "sealed target ownership and extraction input",
                "availability_version_evidence": "p02_lightweight_locator@1 via stable P02 bundle",
                "selected": True,
                "certifying_status": "noncertifying_extraction_input",
            },
            {
                "tool": "SymPy_and_SageMath",
                "role": "later algebra or domain checking",
                "availability_version_evidence": "not invoked in P03",
                "selected": False,
                "certifying_status": "forbidden_by_phase03_boundary",
            },
            {
                "tool": "Lean_and_specialist_premise_or_proof_search",
                "role": "later formal certification or premise search",
                "availability_version_evidence": "not invoked in P03",
                "selected": False,
                "certifying_status": "forbidden_by_phase03_boundary",
            },
        ],
        "artifact_inventory": _artifact_inventory(root, artifact_refs),
        "non_claims": list(P03_NON_CLAIMS),
    }
    _ = delta
    return validate_p03_run_manifest(record)


def _verify_run_manifest(
    root: Path,
    ref: str,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any]:
    raw = _read(root, ref)
    record = validate_p03_run_manifest(_json(raw, "Phase 03 run manifest"))
    chain = _verify_receipt_index(root, record["pre_candidate_receipt_index_ref"], pass_actions, failure_actions)
    if chain["index_sha256"] != record["pre_candidate_receipt_index_sha256"]:
        raise EvidenceValidationError("Phase 03 run-manifest receipt-index binding mismatch")
    expected = _build_run_manifest_record(root, f"{ROUND_PARENT_REF}/{record['result_round']}", record["result_round"], chain, pass_actions, failure_actions)
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("Phase 03 run manifest differs from independent reconstruction")
    for item in record["artifact_inventory"]:
        raw_item = _read(root, item["logical_ref"])
        if content_digest(raw_item) != item["sha256"] or len(raw_item) != item["byte_count"]:
            raise EvidenceValidationError("Phase 03 run-manifest inventory artifact drift")
    return {"ref": ref, "sha256": content_digest(raw), "record": record, "chain": chain}


def _build_run_manifest(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    record = _build_run_manifest_record(root, round_ref, result_round, chain, pass_actions, failure_actions)
    ref = _fixed_refs(round_ref, result_round)["run_manifest"]
    written = _write_json(root, ref, record)
    bindings = {
        "run_manifest_ref": ref,
        "run_manifest_sha256": written["sha256"],
        "bound_receipt_index_ref": chain["index_ref"],
        "bound_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _build_candidate_record(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any]:
    run_receipt = _receipt_for(chain, "build_run_manifest")
    if run_receipt is None or run_receipt["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 candidate requires a successful run manifest")
    run = _verify_run_manifest(root, run_receipt["bindings"]["run_manifest_ref"], pass_actions, failure_actions)
    result = _verify_phase_result(root, run["record"]["result_ref"], pass_actions, failure_actions)
    if result["record"]["decision"] != "candidate_pass_pending_independent_result_review":
        raise EvidenceValidationError("Phase 03 blocked result cannot produce a pass candidate")
    init = chain["receipts"][0]["record"]["bindings"]
    refs = context_artifact_refs(round_ref)
    reconstructed = reconstruct_context_bundle(root, refs["bundle_index"])
    record = {
        "schema_version": "p03_candidate_decision@1",
        "phase": PHASE,
        "result_round": result_round,
        "decision": "candidate_pass_pending_independent_result_review",
        "publication_mode": "disabled",
        "claim_eligibility": "ineligible",
        "entry_record_ref": init["entry_record_ref"],
        "entry_record_sha256": init["entry_record_sha256"],
        "p02_stable_decision_ref": init["p02_stable_decision_ref"],
        "p02_stable_decision_sha256": init["p02_stable_decision_sha256"],
        "p02_terminal_receipt_index_ref": init["p02_terminal_receipt_index_ref"],
        "p02_terminal_receipt_index_sha256": init["p02_terminal_receipt_index_sha256"],
        "reviewed_plan_ref": init["reviewed_plan_ref"],
        "reviewed_plan_sha256": init["reviewed_plan_sha256"],
        "reviewed_recovery_plan_ref": init["reviewed_recovery_plan_ref"],
        "reviewed_recovery_plan_sha256": init["reviewed_recovery_plan_sha256"],
        "agreeing_recovery_review_ref": init["agreeing_recovery_review_ref"],
        "agreeing_recovery_review_sha256": init["agreeing_recovery_review_sha256"],
        "implementation_entry_manifest_ref": init["entry_implementation_manifest_ref"],
        "implementation_entry_manifest_sha256": init["entry_implementation_manifest_sha256"],
        "implementation_round_manifest_ref": init["round_implementation_manifest_ref"],
        "implementation_round_manifest_sha256": init["round_implementation_manifest_sha256"],
        "protected_manifest_ref": init["entry_protected_manifest_ref"],
        "protected_manifest_sha256": init["entry_protected_manifest_sha256"],
        "immutable_input_manifest_ref": init["entry_immutable_input_manifest_ref"],
        "immutable_input_manifest_sha256": init["entry_immutable_input_manifest_sha256"],
        "run_manifest_ref": run["ref"],
        "run_manifest_sha256": run["sha256"],
        "result_ref": result["ref"],
        "result_sha256": result["sha256"],
        "pre_candidate_receipt_index_ref": chain["index_ref"],
        "pre_candidate_receipt_index_sha256": chain["index_sha256"],
        "context_bundle_index_ref": refs["bundle_index"],
        "context_bundle_index_sha256": _digest(root, refs["bundle_index"]),
        "context_bundle_semantic_digest": reconstructed["bundle_semantic_digest"],
        "mutation_matrix_ref": refs["mutation_matrix"],
        "mutation_matrix_sha256": _digest(root, refs["mutation_matrix"]),
        "guard_index_ref": refs["guard_index"],
        "guard_index_sha256": _digest(root, refs["guard_index"]),
        "frozen_source_digests": dict(run["record"]["frozen_source_digests"]),
        "backend_request_count": result["record"]["backend_request_count"],
        "source_edit_count": result["record"]["source_edit_count"],
        "publication_count": result["record"]["publication_count"],
        "primary_criterion": result["record"]["primary_criterion"],
        "vetoes": result["record"]["vetoes"],
        "non_claims": list(P03_NON_CLAIMS),
    }
    return validate_p03_candidate(record)


def _verify_candidate(
    root: Path,
    ref: str,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any]:
    raw = _read(root, ref)
    record = validate_p03_candidate(_json(raw, "Phase 03 candidate"))
    chain = _verify_receipt_index(root, record["pre_candidate_receipt_index_ref"], pass_actions, failure_actions)
    if chain["index_sha256"] != record["pre_candidate_receipt_index_sha256"]:
        raise EvidenceValidationError("Phase 03 candidate receipt-index binding mismatch")
    expected = _build_candidate_record(
        root,
        f"{ROUND_PARENT_REF}/{record['result_round']}",
        record["result_round"],
        chain,
        pass_actions,
        failure_actions,
    )
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("Phase 03 candidate differs from independent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record, "chain": chain}


def _build_candidate(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    record = _build_candidate_record(root, round_ref, result_round, chain, pass_actions, failure_actions)
    ref = _fixed_refs(round_ref, result_round)["candidate"]
    written = _write_json(root, ref, record)
    bindings = {"candidate_ref": ref, "candidate_sha256": written["sha256"]}
    return 0, canonical_json_bytes(bindings), b"", bindings


def _candidate_gate(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    build = chain["receipts"][-1]["record"]
    if build["action"] != "build_candidate" or build["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 candidate gate requires a successful build head")
    candidate = _verify_candidate(root, build["bindings"]["candidate_ref"], pass_actions, failure_actions)
    if candidate["sha256"] != build["bindings"]["candidate_sha256"]:
        raise EvidenceValidationError("Phase 03 candidate build binding mismatch")
    log = {
        "schema_version": "p03_candidate_validation@1",
        "result_round": result_round,
        "candidate_ref": candidate["ref"],
        "candidate_sha256": candidate["sha256"],
        "validated_receipt_index_ref": chain["index_ref"],
        "validated_receipt_index_sha256": chain["index_sha256"],
        "status": "PASS",
    }
    ref = _fixed_refs(round_ref, result_round)["candidate_validation"]
    written = _write_json(root, ref, log)
    bindings = {
        "candidate_ref": candidate["ref"],
        "candidate_sha256": candidate["sha256"],
        "validation_log_ref": ref,
        "validation_log_sha256": written["sha256"],
        "validated_receipt_index_ref": chain["index_ref"],
        "validated_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(log), b"", bindings


def _result_review_binding(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    artifact_ref: str,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    expected_ref = _fixed_refs(round_ref, result_round)["result_review"]
    if artifact_ref != expected_ref:
        raise EvidenceValidationError("Phase 03 result-review ref is not exact")
    gate = chain["receipts"][-1]["record"]
    if gate["action"] != "candidate_gate" or gate["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 result review requires a successful candidate gate")
    candidate = _verify_candidate(root, gate["bindings"]["candidate_ref"], pass_actions, failure_actions)
    log_raw = _read(root, gate["bindings"]["validation_log_ref"])
    log = _json(log_raw, "Phase 03 candidate validation log")
    if (
        content_digest(log_raw) != gate["bindings"]["validation_log_sha256"]
        or log.get("status") != "PASS"
        or log.get("candidate_sha256") != candidate["sha256"]
    ):
        raise EvidenceValidationError("Phase 03 candidate validation-log binding mismatch")
    review_raw = _read(root, expected_ref)
    expected_bindings = {
        "Reviewed result round": result_round,
        "Reviewed candidate SHA-256": candidate["sha256"],
        "Reviewed run manifest SHA-256": candidate["record"]["run_manifest_sha256"],
        "Reviewed result SHA-256": candidate["record"]["result_sha256"],
        "Reviewed context bundle semantic digest": candidate["record"]["context_bundle_semantic_digest"],
        "Reviewed context bundle-index SHA-256": candidate["record"]["context_bundle_index_sha256"],
        "Reviewed mutation matrix SHA-256": candidate["record"]["mutation_matrix_sha256"],
        "Reviewed guard-index SHA-256": candidate["record"]["guard_index_sha256"],
        "Reviewed governance receipt-index SHA-256": chain["index_sha256"],
    }
    verdict = parse_p03_review(review_raw, expected_bindings=expected_bindings, kind="result review")
    bindings = {
        "review_ref": expected_ref,
        "review_sha256": content_digest(review_raw),
        "review_verdict": verdict,
        "reviewed_receipt_index_ref": chain["index_ref"],
        "reviewed_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, f"VERDICT={verdict}\n".encode(), b"", bindings


def _build_final_record(
    root: Path,
    chain: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any]:
    review = chain["receipts"][-1]["record"]
    if (
        review["action"] != "result_review_binding"
        or review["exit_code"] != 0
        or review["bindings"]["review_verdict"] != "AGREE"
    ):
        raise EvidenceValidationError("Phase 03 final candidate requires an agreeing review head")
    reviewed_chain = _verify_receipt_index(
        root,
        review["bindings"]["reviewed_receipt_index_ref"],
        pass_actions,
        failure_actions,
    )
    if reviewed_chain["index_sha256"] != review["bindings"]["reviewed_receipt_index_sha256"]:
        raise EvidenceValidationError("Phase 03 reviewed receipt-index binding drift")
    gate = reviewed_chain["receipts"][-1]["record"]
    if gate["action"] != "candidate_gate" or gate["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 result review did not bind a candidate gate")
    candidate = _verify_candidate(root, gate["bindings"]["candidate_ref"], pass_actions, failure_actions)
    review_raw = _read(root, review["bindings"]["review_ref"])
    expected_review_bindings = {
        "Reviewed result round": candidate["record"]["result_round"],
        "Reviewed candidate SHA-256": candidate["sha256"],
        "Reviewed run manifest SHA-256": candidate["record"]["run_manifest_sha256"],
        "Reviewed result SHA-256": candidate["record"]["result_sha256"],
        "Reviewed context bundle semantic digest": candidate["record"]["context_bundle_semantic_digest"],
        "Reviewed context bundle-index SHA-256": candidate["record"]["context_bundle_index_sha256"],
        "Reviewed mutation matrix SHA-256": candidate["record"]["mutation_matrix_sha256"],
        "Reviewed guard-index SHA-256": candidate["record"]["guard_index_sha256"],
        "Reviewed governance receipt-index SHA-256": reviewed_chain["index_sha256"],
    }
    if (
        content_digest(review_raw) != review["bindings"]["review_sha256"]
        or parse_p03_review(review_raw, expected_bindings=expected_review_bindings, kind="result review") != "AGREE"
    ):
        raise EvidenceValidationError("Phase 03 result review is not independently agreeing")
    init = chain["receipts"][0]["record"]["bindings"]
    record = {
        "schema_version": "p03_final_decision@1",
        "phase": PHASE,
        "result_round": candidate["record"]["result_round"],
        "decision": "pass",
        "publication_mode": "disabled",
        "candidate_decision_ref": candidate["ref"],
        "candidate_decision_sha256": candidate["sha256"],
        "result_review_ref": review["bindings"]["review_ref"],
        "result_review_sha256": review["bindings"]["review_sha256"],
        "reviewed_receipt_index_ref": chain["index_ref"],
        "reviewed_receipt_index_sha256": chain["index_sha256"],
        "p02_stable_decision_ref": init["p02_stable_decision_ref"],
        "p02_stable_decision_sha256": init["p02_stable_decision_sha256"],
        "context_bundle_semantic_digest": candidate["record"]["context_bundle_semantic_digest"],
        "primary_criterion": candidate["record"]["primary_criterion"],
        "vetoes": candidate["record"]["vetoes"],
        "non_claims": list(P03_NON_CLAIMS),
    }
    return validate_p03_final(record)


def _verify_final(
    root: Path,
    ref: str,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any]:
    raw = _read(root, ref)
    record = validate_p03_final(_json(raw, "Phase 03 final decision"))
    chain = _verify_receipt_index(root, record["reviewed_receipt_index_ref"], pass_actions, failure_actions)
    if chain["index_sha256"] != record["reviewed_receipt_index_sha256"]:
        raise EvidenceValidationError("Phase 03 final receipt-index binding mismatch")
    expected = _build_final_record(root, chain, pass_actions, failure_actions)
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("Phase 03 final candidate differs from independent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record, "chain": chain}


def _build_final_candidate(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    record = _build_final_record(root, chain, pass_actions, failure_actions)
    ref = _fixed_refs(round_ref, result_round)["final_candidate"]
    written = _write_json(root, ref, record)
    bindings = {"final_candidate_ref": ref, "final_candidate_sha256": written["sha256"]}
    return 0, canonical_json_bytes(bindings), b"", bindings


def _final_candidate_gate(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    build = chain["receipts"][-1]["record"]
    if build["action"] != "build_final_candidate" or build["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 final gate requires a successful build head")
    final = _verify_final(root, build["bindings"]["final_candidate_ref"], pass_actions, failure_actions)
    if final["sha256"] != build["bindings"]["final_candidate_sha256"]:
        raise EvidenceValidationError("Phase 03 final build binding mismatch")
    log = {
        "schema_version": "p03_final_candidate_validation@1",
        "result_round": result_round,
        "final_candidate_ref": final["ref"],
        "final_candidate_sha256": final["sha256"],
        "validated_receipt_index_ref": chain["index_ref"],
        "validated_receipt_index_sha256": chain["index_sha256"],
        "status": "PASS",
    }
    ref = _fixed_refs(round_ref, result_round)["final_validation"]
    written = _write_json(root, ref, log)
    bindings = {
        "final_candidate_ref": final["ref"],
        "final_candidate_sha256": final["sha256"],
        "validation_log_ref": ref,
        "validation_log_sha256": written["sha256"],
        "validated_receipt_index_ref": chain["index_ref"],
        "validated_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(log), b"", bindings


def _final_seal_audit_binding(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    artifact_ref: str,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    expected_ref = _fixed_refs(round_ref, result_round)["final_audit"]
    if artifact_ref != expected_ref:
        raise EvidenceValidationError("Phase 03 final-seal audit ref is not exact")
    gate = chain["receipts"][-1]["record"]
    if gate["action"] != "final_candidate_gate" or gate["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 final-seal audit requires a successful final gate")
    final = _verify_final(root, gate["bindings"]["final_candidate_ref"], pass_actions, failure_actions)
    log_raw = _read(root, gate["bindings"]["validation_log_ref"])
    log = _json(log_raw, "Phase 03 final validation log")
    if (
        content_digest(log_raw) != gate["bindings"]["validation_log_sha256"]
        or log.get("status") != "PASS"
        or log.get("final_candidate_sha256") != final["sha256"]
    ):
        raise EvidenceValidationError("Phase 03 final validation-log binding mismatch")
    audit_raw = _read(root, expected_ref)
    expected_bindings = {
        "Audited result round": result_round,
        "Audited final-decision candidate SHA-256": final["sha256"],
        "Audited candidate SHA-256": final["record"]["candidate_decision_sha256"],
        "Audited result-review SHA-256": final["record"]["result_review_sha256"],
        "Audited final-candidate validation-log SHA-256": gate["bindings"]["validation_log_sha256"],
        "Audited governance receipt-index SHA-256": chain["index_sha256"],
    }
    verdict = parse_p03_review(audit_raw, expected_bindings=expected_bindings, kind="final-seal audit")
    bindings = {
        "audit_ref": expected_ref,
        "audit_sha256": content_digest(audit_raw),
        "audit_verdict": verdict,
        "audited_receipt_index_ref": chain["index_ref"],
        "audited_receipt_index_sha256": chain["index_sha256"],
        "validation_log_ref": gate["bindings"]["validation_log_ref"],
        "validation_log_sha256": gate["bindings"]["validation_log_sha256"],
    }
    return 0, f"VERDICT={verdict}\n".encode(), b"", bindings


def _stable_publication(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    audit = chain["receipts"][-1]["record"]
    if (
        audit["action"] != "final_seal_audit_binding"
        or audit["exit_code"] != 0
        or audit["bindings"]["audit_verdict"] != "AGREE"
    ):
        raise EvidenceValidationError("Phase 03 stable publication requires an agreeing final audit head")
    audited_chain = _verify_receipt_index(
        root,
        audit["bindings"]["audited_receipt_index_ref"],
        pass_actions,
        failure_actions,
    )
    if audited_chain["index_sha256"] != audit["bindings"]["audited_receipt_index_sha256"]:
        raise EvidenceValidationError("Phase 03 audited receipt-index binding drift")
    gate = audited_chain["receipts"][-1]["record"]
    if gate["action"] != "final_candidate_gate" or gate["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 final audit did not bind a final-candidate gate")
    final = _verify_final(root, gate["bindings"]["final_candidate_ref"], pass_actions, failure_actions)
    audit_raw = _read(root, audit["bindings"]["audit_ref"])
    expected_audit_bindings = {
        "Audited result round": result_round,
        "Audited final-decision candidate SHA-256": final["sha256"],
        "Audited candidate SHA-256": final["record"]["candidate_decision_sha256"],
        "Audited result-review SHA-256": final["record"]["result_review_sha256"],
        "Audited final-candidate validation-log SHA-256": audit["bindings"]["validation_log_sha256"],
        "Audited governance receipt-index SHA-256": audited_chain["index_sha256"],
    }
    if (
        content_digest(audit_raw) != audit["bindings"]["audit_sha256"]
        or parse_p03_review(audit_raw, expected_bindings=expected_audit_bindings, kind="final-seal audit")
        != "AGREE"
    ):
        raise EvidenceValidationError("Phase 03 final-seal audit is not independently agreeing")
    refs = _fixed_refs(round_ref, result_round)
    stable_path = root / refs["stable"]
    if stable_path.exists() or stable_path.is_symlink():
        raise EvidenceValidationError("Phase 03 stable decision path already exists")
    if stable_path.parent.exists():
        if stable_path.parent.is_symlink() or not stable_path.parent.is_dir():
            raise EvidenceValidationError("Phase 03 phase-results directory is unsafe")
    else:
        _mkdir_exact(stable_path.parent)
    os.link(root / final["ref"], stable_path, follow_symlinks=False)
    source_info = os.stat(root / final["ref"], follow_symlinks=False)
    stable_info = os.stat(stable_path, follow_symlinks=False)
    same_inode = source_info.st_dev == stable_info.st_dev and source_info.st_ino == stable_info.st_ino
    same_digest = _digest(root, refs["stable"]) == final["sha256"]
    if not same_inode or not same_digest:
        raise EvidenceValidationError("Phase 03 stable hard-link identity failed; human recovery required")
    bindings = {
        "stable_ref": refs["stable"],
        "stable_sha256": _digest(root, refs["stable"]),
        "final_candidate_ref": final["ref"],
        "final_candidate_sha256": final["sha256"],
        "audit_ref": audit["bindings"]["audit_ref"],
        "audit_sha256": audit["bindings"]["audit_sha256"],
        "same_inode": same_inode,
        "same_digest": same_digest,
    }
    log = {
        "schema_version": "p03_stable_decision_validation@1",
        "phase": PHASE,
        "result_round": result_round,
        "publication_mode": "disabled",
        "status": "PASS",
        **bindings,
    }
    return 0, canonical_json_bytes(log), b"", bindings


def _validate_scoped_repair(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    entry_record: Mapping[str, Any],
) -> dict[str, Any]:
    ref = _fixed_refs(round_ref, result_round)["scoped_repair"]
    raw = _read(root, ref)
    record = _json(raw, "Phase 03 scoped repair")
    keys = {
        "schema_version",
        "phase",
        "result_round",
        "close_reason",
        "failed_actions",
        "source_artifact_ref",
        "source_artifact_sha256",
        "source_receipt_index_ref",
        "source_receipt_index_sha256",
        "repairs",
        "non_claim",
    }
    if not isinstance(record, dict) or set(record) != keys or record["schema_version"] != "p03_scoped_repair@1":
        raise EvidenceValidationError("Phase 03 scoped-repair schema mismatch")
    if record["phase"] != PHASE or record["result_round"] != result_round:
        raise EvidenceValidationError("Phase 03 scoped-repair metadata mismatch")
    latest = chain["receipts"][-1]["record"]
    failed = [item["record"]["action"] for item in chain["receipts"] if item["record"]["exit_code"] != 0]
    if failed:
        close_reason = "measured_action_failure"
        trigger = next(item for item in chain["receipts"] if item["record"]["exit_code"] != 0)
        source_ref = trigger["entry"]["receipt_ref"]
        source_index_ref = _index_ref(round_ref, trigger["record"]["sequence"])
    elif latest["action"] == "result_review_binding" and latest["bindings"]["review_verdict"] == "REVISE":
        close_reason = "result_review_revise"
        source_ref = latest["bindings"]["review_ref"]
        source_index_ref = chain["index_ref"]
    elif latest["action"] == "final_seal_audit_binding" and latest["bindings"]["audit_verdict"] == "REVISE":
        close_reason = "final_seal_audit_revise"
        source_ref = latest["bindings"]["audit_ref"]
        source_index_ref = chain["index_ref"]
    else:
        raise EvidenceValidationError("Phase 03 scoped repair lacks a measured trigger")
    if (
        record["close_reason"] != close_reason
        or record["failed_actions"] != failed
        or record["source_artifact_ref"] != source_ref
        or record["source_artifact_sha256"] != _digest(root, source_ref)
        or record["source_receipt_index_ref"] != source_index_ref
        or record["source_receipt_index_sha256"] != _digest(root, source_index_ref)
        or record["non_claim"] != "Repair scope is a next-round instruction, not a current-round pass or scientific claim."
    ):
        raise EvidenceValidationError("Phase 03 scoped-repair trigger binding mismatch")
    allowed_exact = set(entry_record["implementation_allowlist_exact"])
    allowed_prefixes = tuple(entry_record["implementation_allowlist_prefixes"])
    if not isinstance(record["repairs"], list) or not record["repairs"]:
        raise EvidenceValidationError("Phase 03 scoped repair requires repair entries")
    finding_ids: set[str] = set()
    for repair in record["repairs"]:
        expected = {
            "finding_id",
            "source_stage",
            "severity",
            "affected_paths",
            "required_change",
            "required_check_ids",
            "non_claim",
        }
        if not isinstance(repair, dict) or set(repair) != expected:
            raise EvidenceValidationError("Phase 03 scoped-repair entry keys mismatch")
        finding_id = repair["finding_id"]
        if not isinstance(finding_id, str) or not finding_id or finding_id in finding_ids:
            raise EvidenceValidationError("Phase 03 scoped-repair finding id is invalid")
        finding_ids.add(finding_id)
        paths = repair["affected_paths"]
        if (
            not isinstance(paths, list)
            or not paths
            or paths != sorted(set(paths), key=lambda item: item.encode("utf-8"))
            or any(path not in allowed_exact and not any(path.startswith(prefix) for prefix in allowed_prefixes) for path in paths)
        ):
            raise EvidenceValidationError("Phase 03 scoped-repair path is outside the frozen allowlist")
        checks = repair["required_check_ids"]
        if not isinstance(checks, list) or not checks or any(check not in P03_GUARDED_ACTIONS for check in checks):
            raise EvidenceValidationError("Phase 03 scoped-repair check registry mismatch")
        if repair["non_claim"] != "The requested repair does not establish a current-round pass.":
            raise EvidenceValidationError("Phase 03 scoped-repair non-claim mismatch")
    return {"ref": ref, "sha256": content_digest(raw), "record": record}


def _bind_scoped_repair(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    entry_record: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    repair = _validate_scoped_repair(root, round_ref, result_round, chain, entry_record)
    bindings = {"scoped_repair_ref": repair["ref"], "scoped_repair_sha256": repair["sha256"]}
    return 0, canonical_json_bytes(bindings), b"", bindings


def _close_round(
    root: Path,
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    entry_record: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    binding = chain["receipts"][-1]["record"]
    if binding["action"] != "bind_scoped_repair" or binding["exit_code"] != 0:
        raise EvidenceValidationError("Phase 03 close requires a successful scoped-repair binding")
    source_chain = {**chain, "receipts": chain["receipts"][:-1]}
    source_chain["record"] = {**chain["record"], "receipts": chain["record"]["receipts"][:-1]}
    repair = _validate_scoped_repair(root, round_ref, result_round, source_chain, entry_record)
    failed = [item["record"]["action"] for item in source_chain["receipts"] if item["record"]["exit_code"] != 0]
    latest = source_chain["receipts"][-1]["record"]
    close = {
        "schema_version": "p03_round_close@1",
        "phase": PHASE,
        "result_round": result_round,
        "decision": "blocked",
        "publication_mode": "disabled",
        "close_reason": repair["record"]["close_reason"],
        "failed_actions": failed,
        "scoped_repair_ref": repair["ref"],
        "scoped_repair_sha256": repair["sha256"],
        "source_artifact_ref": repair["record"]["source_artifact_ref"],
        "source_artifact_sha256": repair["record"]["source_artifact_sha256"],
        "receipt_index_before_close_ref": chain["index_ref"],
        "receipt_index_before_close_sha256": chain["index_sha256"],
        "result_review_verdict": (
            latest["bindings"]["review_verdict"] if latest["action"] == "result_review_binding" else None
        ),
        "final_seal_audit_verdict": (
            latest["bindings"]["audit_verdict"] if latest["action"] == "final_seal_audit_binding" else None
        ),
        "non_claims": list(P03_NON_CLAIMS),
    }
    ref = _fixed_refs(round_ref, result_round)["round_close"]
    written = _write_json(root, ref, close)
    bindings = {
        "round_close_ref": ref,
        "round_close_sha256": written["sha256"],
        "receipt_index_before_close_ref": chain["index_ref"],
        "receipt_index_before_close_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _native_action(
    root: Path,
    entry_record: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    action: str,
    chain: Mapping[str, Any],
    artifact_ref: str | None,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    if action == "mutation_gate":
        return _mutation_gate(root, round_ref)
    if action == "zero_backend_source_edit_gate":
        return _zero_gate(root, round_ref)
    if action == "protected_check":
        return _protected_gate(root, entry_record)
    if action == "implementation_exit":
        return _implementation_exit(root, round_ref, result_round)
    if action == "allowlist":
        return _allowlist_gate(root, entry_record, round_ref, result_round, chain)
    if action == "bind_result":
        return _bind_result(root, round_ref, result_round, chain)
    if action == "build_run_manifest":
        return _build_run_manifest(root, round_ref, result_round, chain, pass_actions, failure_actions)
    if action == "build_candidate":
        return _build_candidate(root, round_ref, result_round, chain, pass_actions, failure_actions)
    if action == "candidate_gate":
        return _candidate_gate(root, round_ref, result_round, chain, pass_actions, failure_actions)
    if action == "result_review_binding" and artifact_ref is not None:
        return _result_review_binding(
            root,
            round_ref,
            result_round,
            chain,
            artifact_ref,
            pass_actions,
            failure_actions,
        )
    if action == "build_final_candidate":
        return _build_final_candidate(root, round_ref, result_round, chain, pass_actions, failure_actions)
    if action == "final_candidate_gate":
        return _final_candidate_gate(root, round_ref, result_round, chain, pass_actions, failure_actions)
    if action == "final_seal_audit_binding" and artifact_ref is not None:
        return _final_seal_audit_binding(
            root,
            round_ref,
            result_round,
            chain,
            artifact_ref,
            pass_actions,
            failure_actions,
        )
    if action == "stable_publication":
        return _stable_publication(root, round_ref, result_round, chain, pass_actions, failure_actions)
    if action == "bind_scoped_repair":
        return _bind_scoped_repair(root, round_ref, result_round, chain, entry_record)
    if action == "close_round":
        return _close_round(root, round_ref, result_round, chain, entry_record)
    raise EvidenceValidationError(f"Phase 03 native action is unavailable: {action}")


def _run_action(
    root: Path,
    entry_record: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    action: str,
    artifact_ref: str | None,
    pass_actions: tuple[str, ...],
    failure_actions: tuple[str, ...],
) -> dict[str, Any]:
    chain = _latest_chain(root, round_ref, pass_actions, failure_actions)
    if chain is None:
        raise EvidenceValidationError("Phase 03 initialized receipt chain is absent")
    stable_ref = _fixed_refs(round_ref, result_round)["stable"]
    stable_exists = (root / stable_ref).exists() or (root / stable_ref).is_symlink()
    if stable_exists and chain["receipts"][-1]["record"]["action"] != "stable_publication":
        raise EvidenceValidationError("Phase 03 stable path exists without trusted terminal receipt; human recovery required")
    expected = expected_p03_next_action(
        [item["record"] for item in chain["receipts"]],
        pass_actions=pass_actions,
        failure_actions=failure_actions,
        stable_path_exists=stable_exists,
    )
    if action != expected:
        raise EvidenceValidationError(f"Phase 03 action {action} is not allowed; expected {expected}")
    refs = _fixed_refs(round_ref, result_round)
    if action == "result_review_binding":
        expected_artifact = refs["result_review"]
    elif action == "final_seal_audit_binding":
        expected_artifact = refs["final_audit"]
    else:
        expected_artifact = None
    if artifact_ref != expected_artifact:
        if expected_artifact is None:
            raise EvidenceValidationError("--artifact-ref is accepted only for review/audit actions")
        raise EvidenceValidationError("Phase 03 review/audit action requires its exact artifact ref")
    stdout_ref = f"{round_ref}/logs/{action.replace('_', '-')}.stdout"
    stderr_ref = f"{round_ref}/logs/{action.replace('_', '-')}.stderr"
    started = _utc_now()
    start_ns = time.monotonic_ns()
    try:
        if _execution_class(action) == "subprocess":
            exit_code, stdout, stderr, bindings = _run_subprocess(root, round_ref, action)
        else:
            exit_code, stdout, stderr, bindings = _native_action(
                root,
                entry_record,
                round_ref,
                result_round,
                action,
                chain,
                artifact_ref,
                pass_actions,
                failure_actions,
            )
        if set(bindings) != set(BINDING_KEYS[action]):
            raise EvidenceValidationError("Phase 03 action returned an unregistered binding map")
    except Exception as exc:
        exit_code = 1
        stdout = b""
        stderr = f"{type(exc).__name__}: {exc}\n".encode("utf-8")
        bindings = _null_bindings(action)
    _write(root, stdout_ref, stdout)
    _write(root, stderr_ref, stderr)
    receipt, new_chain = _append_receipt(
        root,
        round_ref,
        result_round,
        pass_actions,
        failure_actions,
        action,
        artifact_ref=artifact_ref,
        started_at=started,
        ended_at=_utc_now(),
        wall_time_ns=time.monotonic_ns() - start_ns,
        exit_code=exit_code,
        stdout_ref=stdout_ref,
        stderr_ref=stderr_ref,
        bindings=bindings,
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


def _guard_caller_environment() -> None:
    if os.environ.get("MATHDEVMCP_P03_DISPATCH_DEPTH") is not None or os.environ.get("MATHDEVMCP_P03_ACTION") is not None or os.environ.get("MATHDEVMCP_P03_ROUND_ROOT") is not None:
        raise EvidenceValidationError("Phase 03 dispatch variables may not be supplied by the caller")
    if os.environ.get("PYTHONPATH") != "src" or sys.executable != PYTHON:
        raise EvidenceValidationError("Phase 03 governance requires PYTHONPATH=src and the pinned Python")


def _strict_cli(argv: list[str], actions: set[str]) -> tuple[str, str, str | None]:
    if any("=" in token for token in argv):
        raise EvidenceValidationError("Phase 03 equal-sign arguments are forbidden")
    if argv[:1] == ["init-round"]:
        if len(argv) != 3 or argv[1] != "--round-root":
            raise EvidenceValidationError("usage: p03_governance.py init-round --round-root RR")
        return "init-round", argv[2], None
    if argv[:1] != ["run"]:
        raise EvidenceValidationError("Phase 03 operation must be exactly init-round or run")
    if len(argv) not in {5, 7} or argv[1] != "--round-root" or argv[3] != "--action":
        raise EvidenceValidationError(
            "usage: p03_governance.py run --round-root RR --action ACTION [--artifact-ref REF]"
        )
    action = argv[4]
    if action not in actions or action == "init_round":
        raise EvidenceValidationError("Phase 03 run action is unregistered or initializer-only")
    artifact_ref = None
    if len(argv) == 7:
        if argv[5] != "--artifact-ref":
            raise EvidenceValidationError("Phase 03 only --artifact-ref may follow the action")
        artifact_ref = validate_logical_path(argv[6], name="Phase 03 review artifact ref")
    return action, argv[2], artifact_ref


def main(argv: list[str] | None = None) -> int:
    _guard_caller_environment()
    args = sys.argv[1:] if argv is None else argv
    root = _repo_root()
    entry, pass_actions, failure_actions = _load_registry(root)
    action, round_root, artifact_ref = _strict_cli(args, set(pass_actions) | set(failure_actions))
    if action == "init-round":
        status = _init_round(root, entry, pass_actions, failure_actions, round_root)
    else:
        round_ref, result_round, _ = _round_context(root, round_root, must_exist=True)
        status = _run_action(
            root,
            entry["record"],
            round_ref,
            result_round,
            action,
            artifact_ref,
            pass_actions,
            failure_actions,
        )
    sys.stdout.buffer.write(canonical_json_bytes(status) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        sys.stderr.buffer.write(
            canonical_json_bytes(
                {
                    "measurement_recorded": False,
                    "status": "governance_error",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
            + b"\n"
        )
        raise SystemExit(2)
