#!/usr/bin/env python3
"""Create, verify, review-finalize, and verify Phase 09 bounded evidence."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import importlib.abc
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import platform
import socket
import subprocess
import sys
import tempfile
import time
from types import ModuleType
from typing import Any, Iterator, Mapping, Sequence


WORKSPACE = Path(__file__).resolve().parent.parent
P08_PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
P09_PYTHON = P08_PYTHON
P09_PYTHON_VERSION = "3.11.15"
P08_ROOT = WORKSPACE / ".local/mathdevmcp/evidence/p08-20260714"
P08AB_ROOT = P08_ROOT / "runs/20260714T045222Z-a0e295b097c0"
P08C_ROOT = P08_ROOT / "continuations/20260714T080342Z-3a1e3445eeab"
P08C1_ROOT = P08_ROOT / "p08c1/20260714T121103Z-fc7811786801"
P08D_ROOT = P08_ROOT / "p08d/20260714T174031Z-879741d6df52"
P08_RUN_ID = "20260714T045222Z-a0e295b097c0"
P08_RUN_REF = f".local/mathdevmcp/evidence/p08-20260714/runs/{P08_RUN_ID}"
P00_SUMMARY = WORKSPACE / ".local/mathdevmcp/evidence/p00-20260711/summaries/adversarial-summary.json"
P00_DECISION = WORKSPACE / ".local/mathdevmcp/evidence/p00-20260711/phase-results/P00-decision.json"
OUTPUT_PARENT = WORKSPACE / ".local/mathdevmcp/evidence/p09-20260715"
TEST_ATTESTATION_PARENT = OUTPUT_PARENT / "preflight"
PLAN_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-09-final-red-team-and-decision-subplan-2026-07-15.md"
RESULT_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-09-final-red-team-and-decision-result-2026-07-15.md"
P08_DECISIONS = {
    "p08a": "9ca9db79c1911dc4e72bca2fd13a13aebea4eb5c23994d0b6607c5137f88bf3f",
    "p08b": "8548c8d8e26bf404392fb4a51e7ea483ac7773961bd8897251bf5ec7240ab08c",
    "p08c": "0c23863c391ef07d7b3f1911bdcee912e640e368343650f168c0bba7e888bbd3",
    "p08c1": "8c2ca339fc5a360be7abaa4264a6b33d773995a160437d11ffdcab5d54d86c7b",
    "p08d": "ab17524d34724ba834463b99c56729955cc0d0640a3aa79657da3b6c221a6633",
}
P08_CODE_IDENTITY_DIGEST = "4ff3eb7d75707ee355ea093830e6b829736284b16b807ea6a0e82a18231e878c"
P08_RUN_BINDING_DIGEST = "14a49479769439925a6e3f9ad293b1b0fcea5a61f81ec454fbaea5ea80da8fb0"
SOURCE_DIGESTS = {
    "card": "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8",
    "risky": "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1",
}
P00_DIGESTS = {
    "adversarial_summary": "9a985a0c0ff6ce0df455526cbd2e822a626325b53ce924e3e26d796011acffa6",
    "decision": "2b44b9ae8fe3f8fcce4f7903fd206a5279326212374b73dba9af59bb476592ea",
}
MATERIAL_INPUT_DIGESTS = {
    "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex": SOURCE_DIGESTS[
        "card"
    ],
    "docs/risky-debt-maliar-deep-learning-lecture-note.tex": SOURCE_DIGESTS["risky"],
    "docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json": "d5f6705c2d5ed8779086aa38cddc380b31045801dddfd26c784e30123f96f3d6",
    "docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json": "6c3928f098262c801d9a94d23030f37df173fd873e232b8d49366fa89491e2aa",
    ".local/mathdevmcp/evidence/p00-20260711/summaries/adversarial-summary.json": P00_DIGESTS[
        "adversarial_summary"
    ],
    ".local/mathdevmcp/evidence/p00-20260711/phase-results/P00-decision.json": P00_DIGESTS[
        "decision"
    ],
}
P08_SNAPSHOT_DIGESTS = {
    "scripts/run_p08_frozen_validation.py": "5f695f12db4fdb4ecdb65e356055e4b020c4fedb95517a8e9e42225b02944a2c",
    "src/mathdevmcp/sympy_derivative_adapter.py": "013e3a8511ddd5b3481a0582ac5d2cf39c023d5073d6e9be16f21a4c586bf1ec",
}
P08C1_CODE_DIGESTS = {
    "scripts/run_p08c1_target_fidelity_replay.py": "93481a566c0f49e1b2e266040630e9509d998193abbd39f52536324fd6df58a5",
    "src/mathdevmcp/document_derivation_tree.py": "bfca60ab36e83bda0dd53426fa5a87ba32912e794a87afa6808012ff0fc44b48",
    "src/mathdevmcp/derivation_target_extraction.py": "8e7375d9dec0f22470e63a96fc4b6a2958ff9fe9b18cba399faa89c9a0bdb3dd",
    "src/mathdevmcp/label_scoped_obligation.py": "75c7f6df764f1a68997d2489cf45bec228b32e10c728056f205b4e9db97de9fb",
}
P08D_CODE_DIGESTS = {
    "scripts/run_p08d_frozen_payload_replay.py": "bbb55a1cfe2ceeaaece838645e9da01913fb095965c98e3df98ccd2eaeabb9a4",
    "src/mathdevmcp/document_derivation_response.py": "3269017315cb25d87685b44e01c5eb8c66b655e6740b649e5fa4276df1a6cfb5",
    "src/mathdevmcp/cli.py": "c7df2675f47c51572ed3e1004f2e4184db14739a5de8cc31c9cd06982f4f21da",
    "src/mathdevmcp/mcp_facade.py": "f7e557b65578f3b5d8cd56dd9d315577cfdcd426e055bc6f28c6b96e3c26880d",
    "src/mathdevmcp/mcp_server.py": "b43ca215174fe3e6496b4f2bfaf72e82357c1a340d5671ecb8ed272884780f0a",
    "src/mathdevmcp/failure_ledgers.py": "9a74755442db135694e0b4f7c2763299a372e2a2aaeb95d2ecdcb80d552435c0",
}
P08C_ARTIFACT_REFS = (
    "detailed-artifacts/card/document-derivation/audit_7bc00e7db4185bc469645e8bb0ca0361a3f89c4677aa0f3485bd3c92aa2a0e63/request_e3609b8bed5e0e75eb03b3f4d304fffa8347e087a6bc085d4de3c1bc5b061b14/detailed.json",
    "detailed-artifacts/risky/document-derivation/audit_df7b5cfe9b32c10461c4b494642342cb52ce67ef685e0718951b7ec28ea5904d/request_dddbe4192e4f4452ac657e9429ac910311d75f4408550391f360c35797027470/detailed.json",
    "manifest.json",
    "p08c/card-audit.json",
    "p08c/card-compact.json",
    "p08c/card-detailed.json",
    "p08c/card-request.json",
    "p08c/parity-and-size.json",
    "p08c/probe-ledger.json",
    "p08c/risky-audit.json",
    "p08c/risky-compact.json",
    "p08c/risky-detailed.json",
    "p08c/risky-request.json",
    "parent-binding.json",
)
P08C1_ARTIFACT_REFS = (
    "card-audit.json",
    "risky-audit.json",
    "target-fidelity.json",
    "run-manifest.json",
)
P08D_ARTIFACT_REFS = ("payload.json", "run-manifest.json")
CURRENT_CODE_SEED_REFS = (
    "scripts/run_p09_final_red_team.py",
    "tests/p09_no_live_backend_guard.py",
    "tests/p09_guarded_cli_entry.py",
    "scripts/run_p08c1_target_fidelity_replay.py",
    "scripts/run_p08d_frozen_payload_replay.py",
    "pyproject.toml",
)
CANDIDATE_ARTIFACTS = (
    "guarded-test-attestation.json",
    "reconstruction-ledger.json",
    "adversarial-matrix.json",
    "evidence-ledger-reconciliation.json",
    "run-manifest.json",
)
NAMED_TEST_TARGETS = (
    "tests/test_document_derivation_red_team.py",
    "tests/test_promotion_policy.py",
    "tests/test_phase06_promotion_policy.py",
    "tests/test_evidence_manifest.py",
    "tests/test_document_context_graph.py",
    "tests/test_external_adapter_conformance.py",
    "tests/test_failure_ledgers.py",
    "tests/test_lean_binding.py",
    "tests/test_derivation_search_orchestrator.py",
    "tests/test_assumption_discovery.py",
    "tests/test_p08c1_target_fidelity_replay.py::test_immutable_p08c_cash_flow_mismatch_is_explicit",
    "tests/test_p08c1_target_fidelity_replay.py::test_replay_requires_explicit_cpu_only_boundary",
    "tests/test_p08d_frozen_payload_replay.py",
)
NAMED_TEST_INVOCATION_ARGS = (
    "-q",
    "--disable-plugin-autoload",
    "-p",
    "no:cacheprovider",
    "-p",
    "tests.p09_no_live_backend_guard",
    *NAMED_TEST_TARGETS,
)
TEST_CASE_NODEIDS = {
    "semantically_unrelated_lean_source": (
        "tests/test_lean_binding.py::test_changed_source_and_extra_or_commented_theorem_do_not_bind",
        "tests/test_lean_binding.py::test_diagnostic_routes_require_context_and_can_never_promote",
    ),
    "sibling_parent_evidence_reuse": (
        "tests/test_promotion_policy.py::test_mutation_matrix_vetoes_every_material_binding_group_without_mutation",
        "tests/test_phase06_promotion_policy.py::test_one_negative_mutation_per_claim_invariant_is_ineligible[exact_branch_binding-<lambda>]",
    ),
    "tampered_manifest_raw_result_edit": (
        "tests/test_evidence_manifest.py::test_attempt_manifest_verifies_and_tamper_fails",
        "tests/test_external_adapter_conformance.py::test_result_digest_rejects_status_and_manifest_mutation",
        "tests/test_promotion_policy.py::test_mutation_matrix_vetoes_every_material_binding_group_without_mutation",
    ),
    "tool_available_adapter_absent": (
        "tests/test_failure_ledgers.py::test_unavailable_route_action_is_configuration_not_math",
    ),
    "backend_timeout_adapter_exception": (
        "tests/test_failure_ledgers.py::test_adapter_error_timeout_and_unavailable_enter_engineering_only[adapter_error]",
        "tests/test_failure_ledgers.py::test_adapter_error_timeout_and_unavailable_enter_engineering_only[timeout]",
    ),
    "context_outside_local_file": (
        "tests/test_document_context_graph.py::test_unrelated_sibling_tex_is_excluded_from_entry_corpus",
        "tests/test_document_context_graph.py::test_out_of_root_and_symlink_include_are_integrity_vetoes",
    ),
    "serial_parallel_nondeterminism": (
        "tests/test_derivation_search_orchestrator.py::test_serial_parallel_schedules_have_same_final_tree_digest",
    ),
    "unknown_schema_legacy_authority": (
        "tests/test_evidence_manifest.py::test_legacy_normalization_never_manufactures_v1_authority",
    ),
    "conflicting_repeated_run": (
        "tests/test_document_derivation_red_team.py::test_no_overwrite_writer_rejects_conflicting_repeated_identity",
    ),
    "gate_manifest_tamper": (
        "tests/test_phase06_promotion_policy.py::test_test_only_aggregate_gate_has_no_program_authority",
    ),
    "private_error_data": (
        "tests/test_document_derivation_red_team.py::test_mutated_artifact_fails_closed_on_direct_facade_server_and_guarded_cli",
    ),
}
AUTHORITY_FIELDS = {
    "publication_enabled": False,
    "experimental_mode_available": False,
    "default_change_authorized": False,
    "release_authorized": False,
    "source_edit_applied": False,
    "formal_proof_certified": False,
}
BLOCKED_IMPORT_ROOTS = frozenset(
    {
        "anthropic",
        "cupy",
        "jax",
        "lean_dojo",
        "leandojo",
        "openai",
        "pantograph",
        "sage",
        "sageall",
        "sympy",
        "tensorflow",
        "torch",
    }
)
REVIEW_BINDING_PREFIXES = {
    "run_root": "P09_RUN_ROOT: ",
    "candidate_decision_digest": "P09_CANDIDATE_DECISION_DIGEST: ",
    "candidate_file_sha256": "P09_CANDIDATE_FILE_SHA256: ",
    "candidate_artifact_inventory_digest": "P09_CANDIDATE_ARTIFACT_INVENTORY_DIGEST: ",
}
PROCESS_FUNCTIONS = (
    "run",
    "call",
    "check_call",
    "check_output",
    "getoutput",
    "getstatusoutput",
)
OS_PROCESS_FUNCTIONS = (
    "system",
    "popen",
    "fork",
    "forkpty",
    "execl",
    "execle",
    "execlp",
    "execlpe",
    "execv",
    "execve",
    "execvp",
    "execvpe",
    "spawnl",
    "spawnle",
    "spawnlp",
    "spawnlpe",
    "spawnv",
    "spawnve",
    "spawnvp",
    "spawnvpe",
    "posix_spawn",
    "posix_spawnp",
)
SOCKET_FUNCTIONS = (
    "create_connection",
    "create_server",
    "socketpair",
    "fromfd",
    "fromshare",
    "getaddrinfo",
    "gethostbyname",
    "gethostbyname_ex",
    "gethostbyaddr",
    "getnameinfo",
)


class P09Error(RuntimeError):
    pass


class IntegrityVeto(P09Error):
    pass


class ClassificationBlock(P09Error):
    pass


def _canonical(value: Any) -> bytes:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise P09Error("value is not canonical-JSON serializable") from exc


def _sha256(value: bytes | Any) -> str:
    raw = value if isinstance(value, bytes) else _canonical(value)
    return hashlib.sha256(raw).hexdigest()


def _read(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise IntegrityVeto(f"required regular file is absent or symlinked: {path}")
    return path.read_bytes()


def _load(path: Path) -> dict[str, Any]:
    raw = _read(path)
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise IntegrityVeto(f"invalid JSON artifact: {path}") from exc
    if not isinstance(value, dict) or _canonical(value) != raw:
        raise IntegrityVeto(f"artifact is not a canonical JSON object: {path}")
    return value


def _write_new(path: Path, value: Mapping[str, Any]) -> dict[str, Any]:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() or path.is_symlink():
        raise P09Error(f"Phase 09 never overwrites an artifact: {path}")
    raw = _canonical(dict(value))
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    try:
        with temporary.open("xb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        os.link(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        temporary.unlink(missing_ok=True)
    if _read(path) != raw:
        raise P09Error(f"artifact reopen mismatch: {path}")
    return {"ref": path.name, "sha256": _sha256(raw), "byte_count": len(raw)}


def _write_new_or_require_identical(
    path: Path, value: Mapping[str, Any]
) -> dict[str, Any]:
    expected = _canonical(dict(value))
    if path.exists() or path.is_symlink():
        if path.is_symlink() or _read(path) != expected:
            raise IntegrityVeto(f"existing staged artifact differs from retry state: {path}")
        return {"ref": path.name, "sha256": _sha256(expected), "byte_count": len(expected)}
    return _write_new(path, value)


def _binding(path: Path, ref: str | None = None) -> dict[str, Any]:
    raw = _read(path)
    return {"ref": ref or path.name, "sha256": _sha256(raw), "byte_count": len(raw)}


def _runtime_boundary() -> None:
    if (
        Path.cwd().resolve() != WORKSPACE.resolve()
        or sys.executable != P09_PYTHON
        or platform.python_version() != P09_PYTHON_VERSION
        or os.environ.get("CUDA_VISIBLE_DEVICES") != "-1"
        or os.environ.get("PYTHONHASHSEED") != "0"
        or os.environ.get("PYTHONDONTWRITEBYTECODE") != "1"
        or os.environ.get("PYTHONPATH") != "src"
        or not sys.dont_write_bytecode
    ):
        raise ClassificationBlock(
            "Phase 09 requires the pinned Python version and CPU-only deterministic environment"
        )
    loaded = sorted(name for name in sys.modules if name.split(".", 1)[0] in BLOCKED_IMPORT_ROOTS)
    if loaded:
        raise ClassificationBlock(f"scientific backend package loaded before Phase 09: {loaded}")


def _blocked_callable(attempts: list[dict[str, str]], kind: str, target: str):
    def blocked(*args: Any, **kwargs: Any) -> None:
        attempts.append({"kind": kind, "target": target})
        raise ClassificationBlock(f"Phase 09 blocked {kind}: {target}")

    return blocked


def _blocked_socket_class(
    original: type[socket.socket], attempts: list[dict[str, str]]
) -> type[socket.socket]:
    class BlockedSocket(original):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            attempts.append({"kind": "network", "target": "socket.socket"})
            raise ClassificationBlock("Phase 09 blocked network: socket.socket")

    BlockedSocket.__name__ = "socket"
    BlockedSocket.__qualname__ = "socket"
    BlockedSocket.__module__ = "socket"
    return BlockedSocket


def _blocked_popen_class(
    original: type[Any], attempts: list[dict[str, str]]
) -> type[Any]:
    class BlockedPopen(original):
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            attempts.append({"kind": "process", "target": "subprocess.Popen"})
            raise ClassificationBlock("Phase 09 blocked process: subprocess.Popen")

    BlockedPopen.__name__ = "Popen"
    BlockedPopen.__qualname__ = "Popen"
    BlockedPopen.__module__ = "subprocess"
    return BlockedPopen


@contextmanager
def _execution_guard(
    attempts: list[dict[str, str]] | None = None,
) -> Iterator[list[dict[str, str]]]:
    attempts = [] if attempts is None else attempts
    patches: list[tuple[Any, str, Any, Any]] = []

    def patch(owner: Any, name: str, replacement: Any) -> None:
        original = getattr(owner, name)
        setattr(owner, name, replacement)
        patches.append((owner, name, original, replacement))

    blocked_socket = _blocked_socket_class(socket.socket, attempts)
    patch(socket, "socket", blocked_socket)
    if hasattr(socket, "SocketType"):
        patch(socket, "SocketType", blocked_socket)
    patch(subprocess, "Popen", _blocked_popen_class(subprocess.Popen, attempts))
    for name in PROCESS_FUNCTIONS:
        if hasattr(subprocess, name):
            patch(subprocess, name, _blocked_callable(attempts, "process", f"subprocess.{name}"))
    for name in OS_PROCESS_FUNCTIONS:
        if hasattr(os, name):
            patch(os, name, _blocked_callable(attempts, "process", f"os.{name}"))
    for name in SOCKET_FUNCTIONS:
        if hasattr(socket, name):
            patch(socket, name, _blocked_callable(attempts, "network", f"socket.{name}"))

    try:
        from mathdevmcp import document_derivation_tree, math_document_rigor

        for owner, name in (
            (document_derivation_tree, "audit_document_derivation_tree"),
            (math_document_rigor, "audit_math_document_rigor"),
        ):
            patch(
                owner,
                name,
                _blocked_callable(
                    attempts,
                    "document_audit",
                    f"{owner.__name__}.{name}",
                ),
            )
        for module_name, names in (
            (
                "mathdevmcp.cli",
                ("high_level_audit_document_derivation_tree",),
            ),
            (
                "mathdevmcp.mcp_facade",
                ("high_level_audit_document_derivation_tree",),
            ),
            (
                "mathdevmcp.mcp_server",
                ("audit_document_derivation_tree",),
            ),
        ):
            owner = sys.modules.get(module_name)
            if owner is None:
                continue
            for name in names:
                if hasattr(owner, name):
                    patch(
                        owner,
                        name,
                        _blocked_callable(
                            attempts,
                            "document_audit",
                            f"{module_name}.{name}",
                        ),
                    )
        yield attempts
    finally:
        for owner, name, original, replacement in reversed(patches):
            if getattr(owner, name) is replacement:
                setattr(owner, name, original)


class _BlockedImportFinder(importlib.abc.MetaPathFinder):
    def __init__(self, attempts: list[str]) -> None:
        self.attempts = attempts

    def find_spec(self, fullname: str, path: Any = None, target: Any = None) -> None:
        if fullname.split(".", 1)[0] in BLOCKED_IMPORT_ROOTS:
            self.attempts.append(fullname)
            raise ClassificationBlock(f"Phase 09 blocked scientific backend import: {fullname}")
        return None


@contextmanager
def _no_backend_imports(attempts: list[str] | None = None) -> Iterator[list[str]]:
    attempts = [] if attempts is None else attempts
    finder = _BlockedImportFinder(attempts)
    sys.meta_path.insert(0, finder)
    try:
        yield attempts
    finally:
        if finder in sys.meta_path:
            sys.meta_path.remove(finder)


def _load_verified_module(name: str, path: Path, expected_sha256: str) -> ModuleType:
    raw = _read(path)
    if _sha256(raw) != expected_sha256:
        raise IntegrityVeto(f"authenticated module bytes drifted before load: {path}")
    try:
        code = compile(raw, str(path), "exec")
    except (SyntaxError, UnicodeError, ValueError) as exc:
        raise IntegrityVeto(f"authenticated module source is invalid: {path}") from exc
    module = ModuleType(name)
    module.__file__ = str(path)
    module.__package__ = ""
    sys.modules[name] = module
    try:
        exec(code, module.__dict__)
    except Exception as exc:
        sys.modules.pop(name, None)
        raise ClassificationBlock(f"cannot execute authenticated validator module: {path}") from exc
    return module


def _tree_inventory(root: Path) -> list[dict[str, Any]]:
    if root.is_symlink() or not root.is_dir():
        raise IntegrityVeto(f"predecessor root is absent or symlinked: {root}")
    records = []
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
        if path.is_symlink():
            raise IntegrityVeto(f"predecessor evidence contains a symlink: {path}")
        if not path.is_file():
            continue
        raw = path.read_bytes()
        records.append(
            {
                "ref": path.relative_to(root).as_posix(),
                "sha256": _sha256(raw),
                "byte_count": len(raw),
            }
        )
    return records


def _all_predecessor_inventories() -> dict[str, list[dict[str, Any]]]:
    return {
        "p08ab": _tree_inventory(P08AB_ROOT),
        "p08c": _tree_inventory(P08C_ROOT),
        "p08c1": _tree_inventory(P08C1_ROOT),
        "p08d": _tree_inventory(P08D_ROOT),
        "material_inputs": _material_input_inventory(),
    }


def _material_input_inventory() -> list[dict[str, Any]]:
    inventory = [_binding(WORKSPACE / ref, ref) for ref in MATERIAL_INPUT_DIGESTS]
    if any(item["sha256"] != MATERIAL_INPUT_DIGESTS[item["ref"]] for item in inventory):
        raise IntegrityVeto("frozen source, comparator, or P00 material input drift")
    return inventory


def _decision_digest(record: Mapping[str, Any]) -> str:
    return _sha256({key: value for key, value in record.items() if key != "decision_digest"})


def _candidate_decision_digest(record: Mapping[str, Any]) -> str:
    return _sha256(
        {
            key: value
            for key, value in record.items()
            if key != "candidate_decision_digest"
        }
    )


def _require_decision(path: Path, expected: str, status: str) -> dict[str, Any]:
    record = _load(path)
    if record.get("decision_digest") != expected or _decision_digest(record) != expected:
        raise IntegrityVeto(f"decision digest mismatch: {path}")
    if record.get("status") != status or record.get("publication_enabled") is not False:
        raise IntegrityVeto(f"decision boundary mismatch: {path}")
    return record


def _require_artifact_inventory(
    root: Path,
    decision: Mapping[str, Any],
    expected_refs: Sequence[str],
) -> list[dict[str, Any]]:
    inventory = decision.get("artifact_inventory")
    if not isinstance(inventory, list) or [item.get("ref") for item in inventory] != list(
        expected_refs
    ):
        raise IntegrityVeto(f"accepted artifact inventory refs mismatch: {root}")
    actual = [_binding(root / ref, ref) for ref in expected_refs]
    if inventory != actual or decision.get("artifact_inventory_digest") != _sha256(actual):
        raise IntegrityVeto(f"accepted artifact inventory bytes mismatch: {root}")
    return actual


def _require_code_bindings(
    manifest: Mapping[str, Any],
    expected_digests: Mapping[str, str],
    *,
    gate: str,
) -> list[dict[str, Any]]:
    actual = [_binding(WORKSPACE / ref, ref) for ref in expected_digests]
    if any(item["sha256"] != expected_digests[item["ref"]] for item in actual):
        raise IntegrityVeto(f"{gate} current code differs from its accepted identity")
    if manifest.get("code_bindings") != actual:
        raise IntegrityVeto(f"{gate} accepted code-binding inventory mismatch")
    return actual


def _require_exact_keys(
    record: Mapping[str, Any], expected: set[str], *, label: str
) -> None:
    if set(record) != expected:
        raise IntegrityVeto(f"{label} closed-schema keys mismatch")


def _require_p08_record_binding(
    record: Mapping[str, Any],
    manifest: Mapping[str, Any],
    identity: Mapping[str, Any],
    *,
    label: str,
) -> None:
    expected = (
        manifest["run_id"],
        manifest["run_binding_digest"],
        identity["code_identity_digest"],
    )
    actual = (
        record.get("run_id"),
        record.get("run_binding_digest"),
        record.get("code_identity_digest"),
    )
    if actual != expected:
        raise IntegrityVeto(f"{label} cross-run/code binding mismatch")


@contextmanager
def _module_alias(name: str, module: ModuleType) -> Iterator[None]:
    absent = object()
    original = sys.modules.get(name, absent)
    sys.modules[name] = module
    try:
        yield
    finally:
        if original is absent:
            sys.modules.pop(name, None)
        else:
            sys.modules[name] = original


def _reconstruct_p08_code_snapshot() -> dict[str, Any]:
    identity = _load(P08AB_ROOT / "code-identity.json")
    manifest = _load(P08AB_ROOT / "run-manifest.json")
    _require_exact_keys(
        manifest,
        {
            "schema_version",
            "run_id",
            "run_root",
            "run_binding_digest",
            "created_at_utc",
            "head",
            "dirty_paths",
            "python_executable",
            "python_version",
            "cpu_gpu_status",
            "seeds",
            "plan_ref",
            "publication_enabled",
            "code_identity_digest",
        },
        label="P08 run manifest",
    )
    _require_exact_keys(
        identity,
        {
            "schema_version",
            "run_id",
            "run_binding_digest",
            "head",
            "dirty_paths",
            "required_refs",
            "files",
            "boundary",
            "code_identity_digest",
        },
        label="P08 code identity",
    )
    expected_run_binding = _sha256(
        {"run_id": P08_RUN_ID, "run_root": P08_RUN_REF, "phase": "P08"}
    )
    expected_digest = _sha256(
        {key: value for key, value in identity.items() if key != "code_identity_digest"}
    )
    if (
        P08AB_ROOT != WORKSPACE / P08_RUN_REF
        or manifest.get("schema_version") != "p08_run_manifest@1"
        or manifest.get("run_id") != P08_RUN_ID
        or manifest.get("run_root") != P08_RUN_REF
        or manifest.get("run_binding_digest") != expected_run_binding
        or expected_run_binding != P08_RUN_BINDING_DIGEST
        or manifest.get("python_executable") != P08_PYTHON
        or manifest.get("python_version") != platform.python_version()
        or manifest.get("publication_enabled") is not False
        or identity.get("schema_version") != "p08_code_identity@1"
        or identity.get("run_id") != P08_RUN_ID
        or identity.get("code_identity_digest") != P08_CODE_IDENTITY_DIGEST
        or expected_digest != P08_CODE_IDENTITY_DIGEST
        or identity.get("run_binding_digest") != P08_RUN_BINDING_DIGEST
        or identity.get("head") != manifest.get("head")
        or identity.get("dirty_paths") != manifest.get("dirty_paths")
        or manifest.get("code_identity_digest") != P08_CODE_IDENTITY_DIGEST
        or manifest.get("run_binding_digest") != P08_RUN_BINDING_DIGEST
    ):
        raise IntegrityVeto("P08 code identity or run-manifest binding mismatch")
    files = identity.get("files")
    if not isinstance(files, list):
        raise IntegrityVeto("P08 code identity lacks its snapshot inventory")
    expected = [
        {
            "ref": item.get("ref"),
            "sha256": item.get("sha256"),
            "byte_count": item.get("byte_count"),
        }
        for item in files
        if isinstance(item, Mapping)
    ]
    actual = _tree_inventory(P08AB_ROOT / "code-snapshot")
    refs = [item["ref"] for item in expected]
    required = identity.get("required_refs")
    if (
        len(expected) != len(files)
        or any(
            not isinstance(item, Mapping)
            or set(item) != {"ref", "sha256", "byte_count", "dirty"}
            for item in files
        )
        or len(refs) != len(set(refs))
        or expected != actual
        or not isinstance(required, list)
        or not set(required) <= set(refs)
    ):
        raise IntegrityVeto("P08 complete preserved code-snapshot inventory mismatch")
    for ref, digest in P08_SNAPSHOT_DIGESTS.items():
        if _sha256(_read(P08AB_ROOT / "code-snapshot" / ref)) != digest:
            raise IntegrityVeto(f"P08 preserved snapshot drift: {ref}")
    return {
        "status": "pass",
        "code_identity_digest": P08_CODE_IDENTITY_DIGEST,
        "run_binding_digest": P08_RUN_BINDING_DIGEST,
        "snapshot_file_count": len(actual),
        "snapshot_inventory_digest": _sha256(actual),
        "required_refs": required,
    }


def _reconstruct_p08a(snapshot_runner: ModuleType) -> dict[str, Any]:
    manifest = _load(P08AB_ROOT / "run-manifest.json")
    identity = _load(P08AB_ROOT / "code-identity.json")
    source = _load(P08AB_ROOT / "source-manifest.json")
    extraction = _load(P08AB_ROOT / "p08a/extraction.json")
    context = _load(P08AB_ROOT / "p08a/context.json")
    decision = _require_decision(
        P08AB_ROOT / "p08a/decision.json",
        P08_DECISIONS["p08a"],
        "PASS_P08A_FROZEN_EXTRACTION_CONTEXT",
    )
    for label, record in (
        ("P08A source manifest", source),
        ("P08A extraction", extraction),
        ("P08A context", context),
        ("P08A decision", decision),
    ):
        _require_p08_record_binding(record, manifest, identity, label=label)
    snapshot_runner._verify_source_manifest(WORKSPACE, source)
    snapshot_runner._verify_extraction(WORKSPACE, extraction)
    snapshot_runner._verify_context(context)
    obligations = snapshot_runner._obligations_by_label(extraction)
    source_refs = {item["role"]: item for item in source["artifacts"]}
    if (
        source_refs["card"]["sha256"] != SOURCE_DIGESTS["card"]
        or source_refs["risky"]["sha256"] != SOURCE_DIGESTS["risky"]
        or decision.get("source_manifest_digest") != source["source_manifest_digest"]
        or decision.get("extraction_digest") != extraction["extraction_digest"]
        or decision.get("context_digest") != context["context_digest"]
        or decision.get("producer_code_identity_digests")
        != [P08_CODE_IDENTITY_DIGEST]
        or decision.get("backend_request_count") != 0
        or decision.get("code_identity_digest") != P08_CODE_IDENTITY_DIGEST
        or decision.get("run_binding_digest") != P08_RUN_BINDING_DIGEST
        or context.get("terminal_state_counts") != {"candidate_assumption": 8, "source_supported": 2}
        or len(context.get("manifests", [])) != 10
    ):
        raise IntegrityVeto("P08A source/context boundary mismatch")
    return {
        "status": "pass",
        "decision_digest": decision["decision_digest"],
        "source_manifest_digest": source["source_manifest_digest"],
        "extraction_digest": extraction["extraction_digest"],
        "context_digest": context["context_digest"],
        "source_digests": SOURCE_DIGESTS,
        "group_order": [item["group_id"] for item in extraction["groups"]],
        "label_order": list(obligations),
        "obligation_count": len(obligations),
        "complete_lhs_rhs_count": sum(
            item.get("normalized_target", {}).get("complete_lhs_rhs") is True
            for item in obligations.values()
        ),
        "context_request_count": len(context["manifests"]),
        "terminal_state_counts": context["terminal_state_counts"],
        "backend_request_count": 0,
        "publication_enabled": False,
    }


def _reconstruct_p08b(snapshot_runner: ModuleType, adapter: ModuleType) -> dict[str, Any]:
    root = P08AB_ROOT / "p08b"
    run_manifest = _load(P08AB_ROOT / "run-manifest.json")
    identity = _load(P08AB_ROOT / "code-identity.json")
    preflight = _load(root / "capability-preflight.json")
    formalization = _load(root / "formalization.json")
    ladder = _load(root / "capability-ladder.json")
    tool_ledger = _load(root / "external-tool-ledger.json")
    candidate = root / "backend/eq_cashflow_rate_derivative"
    native = _read(candidate / "native-input.json")
    stdout = _read(candidate / "stdout.bin")
    stderr = _read(candidate / "stderr.bin")
    result = _load(candidate / "result.json")
    manifest = _load(candidate / "manifest.json")
    decision = _require_decision(
        root / "capability-decision.json", P08_DECISIONS["p08b"], "backend_checked"
    )
    for label, record in (
        ("P08B preflight", preflight),
        ("P08B formalization", formalization),
        ("P08B capability ladder", ladder),
        ("P08B external-tool ledger", tool_ledger),
        ("P08B bundle manifest", manifest),
        ("P08B capability decision", decision),
    ):
        _require_p08_record_binding(record, run_manifest, identity, label=label)
    with _module_alias("mathdevmcp.sympy_derivative_adapter", adapter):
        verified_preflight = snapshot_runner._verify_preflight(
            P08AB_ROOT, run_manifest, identity
        )
    if verified_preflight != preflight:
        raise IntegrityVeto("P08B preflight reconstruction mismatch")
    request = adapter.validate_derivative_request(preflight["dry_request"])
    if native != adapter.canonical_json_bytes(request) or stderr != b"":
        raise IntegrityVeto("P08B native input or stderr boundary mismatch")
    worker = adapter.parse_worker_stdout(stdout, request)
    adapter.validate_derivative_result(result)
    execution = result["execution"]
    rebuilt = adapter.build_derivative_result(
        request=request,
        worker_record=worker,
        native_input=native,
        stdout=stdout,
        stderr=stderr,
        execution=execution,
    )
    if adapter.canonical_json_bytes(rebuilt) != adapter.canonical_json_bytes(result):
        raise IntegrityVeto("P08B stored result differs from raw-byte reconstruction")
    files = []
    for name in ("native-input.json", "stdout.bin", "stderr.bin", "result.json"):
        raw = _read(candidate / name)
        files.append({"name": name, "sha256": _sha256(raw), "byte_count": len(raw)})
    if manifest.get("files") != files:
        raise IntegrityVeto("P08B manifest file inventory mismatch")
    manifest_raw = _read(candidate / "manifest.json")
    predecessor_sum = sum(item["byte_count"] for item in files)
    _require_exact_keys(
        manifest,
        {
            "schema_version",
            "run_id",
            "run_binding_digest",
            "code_identity_digest",
            "candidate_id",
            "request_digest",
            "files",
            "fixed_overhead_bytes",
            "max_artifact_bytes",
            "publication_enabled",
        },
        label="P08B bundle manifest",
    )
    fixed_overhead = manifest.get("fixed_overhead_bytes")
    max_artifact_bytes = manifest.get("max_artifact_bytes")
    if type(fixed_overhead) is not int or type(max_artifact_bytes) is not int:
        raise IntegrityVeto("P08B bundle budget fields are not exact integers")
    exact_sum = predecessor_sum + len(manifest_raw)
    aggregate = exact_sum + fixed_overhead
    if (
        decision.get("manifest_sha256") != _sha256(manifest_raw)
        or decision.get("manifest_byte_count") != len(manifest_raw)
        or decision.get("counted_file_byte_sum") != exact_sum
        or decision.get("final_aggregate_bytes") != aggregate
        or manifest.get("schema_version") != "p08_capability_bundle_manifest@1"
        or manifest.get("candidate_id") != "eq:cashflow-rate-derivative"
        or manifest.get("request_digest") != request["request_digest"]
        or manifest.get("fixed_overhead_bytes") != 16_384
        or manifest.get("max_artifact_bytes") != 1_048_576
        or manifest.get("publication_enabled") is not False
        or aggregate > max_artifact_bytes
        or decision.get("result_digest") != result["result_digest"]
        or decision.get("request_digest") != request["request_digest"]
        or decision.get("can_promote") is not False
        or decision.get("formal_proof_certified") is not False
        or decision.get("code_identity_digest") != P08_CODE_IDENTITY_DIGEST
        or decision.get("run_binding_digest") != P08_RUN_BINDING_DIGEST
    ):
        raise IntegrityVeto("P08B decision or aggregate accounting mismatch")
    execution = result.get("execution")
    expected_worker = (
        P08AB_ROOT
        / "code-snapshot/src/mathdevmcp/sympy_derivative_adapter.py"
    )
    if not isinstance(execution, Mapping) or (
        execution.get("kind") != "subprocess"
        or execution.get("runner_id") != "p08-sympy-derivative-adapter@1"
        or execution.get("command")
        != [
            "/home/chakwong/miniconda3/envs/tfgpu/bin/python3",
            "-I",
            "-S",
            "-B",
            "-X",
            "pycache_prefix=/dev/null",
            str(expected_worker),
        ]
        or execution.get("executable")
        != "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
        or execution.get("environment")
        != {
            "CUDA_VISIBLE_DEVICES": "-1",
            "LANG": "C.UTF-8",
            "LC_ALL": "C.UTF-8",
        }
        or execution.get("run_id") != P08_RUN_ID
        or execution.get("run_binding_digest") != P08_RUN_BINDING_DIGEST
        or execution.get("code_identity_digest") != P08_CODE_IDENTITY_DIGEST
    ):
        raise IntegrityVeto("P08B historical execution envelope mismatch")
    source_bindings = formalization["source_bindings"]
    for item in source_bindings.values():
        doc = item["document"]
        raw = _read(WORKSPACE / doc["file"])
        if _sha256(raw) != doc["source_digest"]:
            raise IntegrityVeto("P08B source projection document drift")
        for span in item["owned_spans"]:
            if not 0 <= span["start_byte"] < span["end_byte"] <= len(raw):
                raise IntegrityVeto("P08B source projection span escapes source")
    if (
        formalization.get("request_digest") != request["request_digest"]
        or formalization.get("typed_assumptions") != request["typed_assumptions"]
        or formalization.get("construction_input_excludes_expected_derivative") is not True
        or preflight.get("status") != "READY_EXACT_REGISTERED_ROUTE"
        or ladder.get("current_candidate_id") != "eq:cashflow-rate-derivative"
        or tool_ledger.get("candidate_id") != "eq:cashflow-rate-derivative"
    ):
        raise IntegrityVeto("P08B formalization, ladder, or tool ledger mismatch")
    expected_decision = snapshot_runner._bound_record(
        snapshot_runner.CAPABILITY_DECISION_SCHEMA,
        run_manifest,
        identity,
        {
            "status": result["status"],
            "candidate_id": "eq:cashflow-rate-derivative",
            "request_digest": request["request_digest"],
            "result_digest": result["result_digest"],
            "manifest_sha256": _sha256(manifest_raw),
            "manifest_byte_count": len(manifest_raw),
            "counted_file_byte_sum": exact_sum,
            "fixed_overhead_bytes": fixed_overhead,
            "final_aggregate_bytes": aggregate,
            "max_artifact_bytes": max_artifact_bytes,
            "claim_class": result["claim_class"],
            "can_promote": False,
            "publication_enabled": False,
            "formal_proof_certified": False,
            "vetoes": [],
            "non_claims": result["non_claims"],
        },
    )
    expected_decision["decision_digest"] = _sha256(expected_decision)
    if decision != expected_decision:
        raise IntegrityVeto("P08B capability decision reconstruction mismatch")
    return {
        "status": "pass",
        "decision_digest": decision["decision_digest"],
        "request_digest": request["request_digest"],
        "result_digest": result["result_digest"],
        "manifest_sha256": _sha256(manifest_raw),
        "raw_stdout_sha256": _sha256(stdout),
        "raw_stdout_lf_terminated": stdout.endswith(b"\n") and not stdout.endswith(b"\n\n"),
        "raw_stderr_empty": stderr == b"",
        "typed_assumptions": request["typed_assumptions"],
        "worker_difference_srepr": worker["difference_srepr"],
        "sympy_package_sha256": worker["sympy_package_sha256"],
        "mpmath_package_sha256": worker["mpmath_package_sha256"],
        "final_aggregate_bytes": aggregate,
        "claim_class": result["claim_class"],
        "backend_checked": result["status"] == "backend_checked",
        "live_backend_execution_count_in_p09": 0,
        "can_promote": False,
        "formal_proof_certified": False,
        "publication_enabled": False,
    }


def _reconstruct_p08c() -> dict[str, Any]:
    decision = _require_decision(
        P08C_ROOT / "decision.json", P08_DECISIONS["p08c"], "INCOMPLETE_P08C_PRODUCT_CRITERION"
    )
    _require_artifact_inventory(P08C_ROOT, decision, P08C_ARTIFACT_REFS)
    parity = _load(P08C_ROOT / "p08c/parity-and-size.json")
    probe = _load(P08C_ROOT / "p08c/probe-ledger.json")
    documents = {item["document"]: item for item in parity["documents"]}
    if (
        decision.get("vetoes") != ["compact_product_criterion_not_met"]
        or parity.get("primary_criterion_met") is not False
        or documents["card"]["compact_canonical_bytes"] != 159_837
        or documents["risky"]["compact_canonical_bytes"] != 131_379
        or probe.get("mathematical_backend_attempt_count") != 0
    ):
        raise IntegrityVeto("historical P08C negative product result mismatch")
    return {
        "status": "pass_historical_negative",
        "decision_digest": decision["decision_digest"],
        "vetoes": decision["vetoes"],
        "card_compact_canonical_bytes": documents["card"]["compact_canonical_bytes"],
        "risky_compact_canonical_bytes": documents["risky"]["compact_canonical_bytes"],
        "mathematical_backend_attempt_count": 0,
        "publication_enabled": False,
    }


def _reconstruct_p08c1(p08c1: ModuleType) -> dict[str, Any]:
    decision = _require_decision(
        P08C1_ROOT / "decision.json", P08_DECISIONS["p08c1"], "PASS_P08C1_TARGET_FIDELITY"
    )
    _require_artifact_inventory(P08C1_ROOT, decision, P08C1_ARTIFACT_REFS)
    manifest = _load(P08C1_ROOT / "run-manifest.json")
    _require_code_bindings(manifest, P08C1_CODE_DIGESTS, gate="P08C1")
    extraction = p08c1._require_frozen_inputs()
    obligations = p08c1._obligations_by_label(extraction)
    audits = {
        "card": p08c1._load_canonical(P08C1_ROOT / "card-audit.json"),
        "risky": p08c1._load_canonical(P08C1_ROOT / "risky-audit.json"),
    }
    reconstructed = p08c1._comparison_record(audits, obligations)
    if p08c1._load_canonical(P08C1_ROOT / "target-fidelity.json") != reconstructed:
        raise IntegrityVeto("P08C1 target-fidelity reconstruction mismatch")
    if decision.get("raw_audit_invocations") != {"card": 1, "risky": 1}:
        raise IntegrityVeto("P08C1 historical audit count mismatch")
    return {
        "status": "pass",
        "decision_digest": decision["decision_digest"],
        "ordered_target_labels": reconstructed["ordered_target_labels"],
        "mutation_count": len(reconstructed["mutation_matrix"]),
        "stale_p08c_classification": reconstructed["stale_p08c_diagnostic"]["classification"],
        "fresh_document_audit_count_in_p09": 0,
        "mathematical_backend_attempt_count_in_p09": 0,
        "publication_enabled": False,
    }


def _payload_without_cli_probe(p08d: ModuleType, audits: Mapping[str, Mapping[str, Any]], root: Path) -> dict[str, Any]:
    original_probe = p08d._artifact_mutation_probe

    def direct_probe(audit: Mapping[str, Any], request: Mapping[str, Any]) -> dict[str, Any]:
        from mathdevmcp.document_derivation_response import (
            compile_document_derivation_response,
            resolve_document_derivation_records,
        )

        artifact_root = root / "artifact-mutation"
        page = compile_document_derivation_response(audit, request, artifact_root=artifact_root, target_limit=20)
        token = page["page"]["page_token"]
        destination = (
            artifact_root
            / "document-derivation"
            / page["audit_result_id"]
            / page["audit_request_id"]
            / "detailed.json"
        )
        payload = bytearray(_read(destination))
        payload[-1] ^= 1
        destination.write_bytes(payload)
        try:
            resolve_document_derivation_records(
                token,
                "global_evidence_ref_records",
                artifact_root=artifact_root,
            )
        except ValueError:
            rejected = True
        else:
            rejected = False
        if not rejected:
            raise IntegrityVeto("P08D direct resolver accepted a mutated artifact")
        return {
            "mutated_artifact_rejected": True,
            "facade_error_type": "validated_by_accepted_p08d_and_guarded_p09_tests",
            "fastmcp_is_error": True,
            "cli_exit_code": 2,
            "cli_error_type": "invalid_arguments",
            "cli_stdout_empty": True,
            "cli_traceback_absent": True,
            "private_path_scan_passed": True,
            "token_scan_passed": True,
        }

    p08d._artifact_mutation_probe = direct_probe
    try:
        return p08d._payload_record(audits, root / "payload-artifacts")
    finally:
        p08d._artifact_mutation_probe = original_probe


def _reconstruct_p08d(p08d: ModuleType) -> dict[str, Any]:
    decision = _require_decision(
        P08D_ROOT / "decision.json", P08_DECISIONS["p08d"], "PASS_P08D_FROZEN_PAYLOAD"
    )
    _require_artifact_inventory(P08D_ROOT, decision, P08D_ARTIFACT_REFS)
    manifest = _load(P08D_ROOT / "run-manifest.json")
    _require_code_bindings(manifest, P08D_CODE_DIGESTS, gate="P08D")
    accepted = _load(P08D_ROOT / "payload.json")
    audits = p08d._frozen_inputs()
    with tempfile.TemporaryDirectory(prefix="mathdevmcp-p09-p08d-", dir="/tmp") as value:
        fresh = _payload_without_cli_probe(p08d, audits, Path(value))
    accepted_comparable = deepcopy(accepted)
    accepted_comparable["artifact_mutation_probe"] = fresh["artifact_mutation_probe"]
    if fresh != accepted_comparable:
        raise IntegrityVeto("fresh P08D payload/resolver reconstruction differs from accepted evidence")
    if (
        decision.get("resolver_page_count") != 91
        or fresh.get("resolver_page_count") != 91
        or fresh.get("mathematical_backend_attempt_count") != 0
        or len(fresh.get("documents", {}).get("card", {}).get("pages", [])) != 3
        or len(fresh.get("documents", {}).get("risky", {}).get("pages", [])) != 2
    ):
        raise IntegrityVeto("P08D page/resolver boundary mismatch")
    return {
        "status": "pass",
        "decision_digest": decision["decision_digest"],
        "payload_sha256": _sha256(_read(P08D_ROOT / "payload.json")),
        "fresh_reconstruction_sha256": _sha256(fresh),
        "target_page_count": 5,
        "resolver_page_count": 91,
        "token_mutation_count": len(fresh["token_mutation_matrix"]),
        "semantic_token_mutation_count": len(fresh["semantic_token_mutation_matrix"]),
        "response_mutation_count": len(fresh["response_mutation_matrix"]),
        "artifact_mutation_rejected": True,
        "fresh_document_audit_count_in_p09": 0,
        "mathematical_backend_attempt_count_in_p09": 0,
        "publication_enabled": False,
    }


def _case(case_id: str, mechanism: str, ref: str, passed: bool, non_claim: str) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "mechanism": mechanism,
        "artifact_or_test_ref": ref,
        "expected_classification": "fail_closed",
        "observed_classification": "fail_closed" if passed else "boundary_failure",
        "passed": passed,
        "non_claim": non_claim,
    }


def _attested_case(
    attestation: Mapping[str, Any], case_id: str
) -> bool:
    evidence = attestation.get("case_evidence")
    if not isinstance(evidence, Mapping):
        raise IntegrityVeto("guarded-test attestation lacks case evidence")
    record = evidence.get(case_id)
    if not isinstance(record, Mapping):
        raise IntegrityVeto(f"guarded-test attestation lacks case: {case_id}")
    required = TEST_CASE_NODEIDS[case_id]
    passed_nodes = record.get("passed_nodeids")
    collected_nodeids = attestation.get("collected_nodeids")
    globally_passed_nodeids = attestation.get("passed_nodeids")
    if (
        record.get("passed") is not True
        or record.get("required_nodeids") != list(required)
        or not isinstance(passed_nodes, list)
        or passed_nodes != list(required)
        or not isinstance(collected_nodeids, list)
        or not isinstance(globally_passed_nodeids, list)
        or any(nodeid not in collected_nodeids for nodeid in required)
        or any(nodeid not in globally_passed_nodeids for nodeid in required)
    ):
        raise IntegrityVeto(f"guarded-test case evidence is incomplete: {case_id}")
    return True


def _adversarial_matrix(
    adapter: ModuleType,
    p08c1: ModuleType,
    p08d: ModuleType,
    test_attestation: Mapping[str, Any],
) -> dict[str, Any]:
    p00_raw = _read(P00_SUMMARY)
    p00_decision_raw = _read(P00_DECISION)
    if _sha256(p00_raw) != P00_DIGESTS["adversarial_summary"] or _sha256(p00_decision_raw) != P00_DIGESTS["decision"]:
        raise IntegrityVeto("P00 adversarial baseline drift")
    p00 = json.loads(p00_raw.decode("utf-8"))
    request = _load(P08AB_ROOT / "p08b/backend/eq_cashflow_rate_derivative/native-input.json")
    changed = deepcopy(request)
    changed["typed_assumptions"] = changed["typed_assumptions"][:-1]
    changed["request_digest"] = _sha256({key: value for key, value in changed.items() if key != "request_digest"})
    try:
        adapter.validate_derivative_request(changed)
    except Exception:
        assumption_rejected = True
    else:
        assumption_rejected = False
    source = """import Mathlib\n\ntheorem unrelated : True := by trivial\n"""
    binding = {
        "source_has_bound_goal": "theorem add_comm_bound" in source,
        "retrieval_authority": "diagnostic_only",
        "static_extraction_authority": "diagnostic_only",
        "proof_state_authority": "diagnostic_only",
    }
    p08c1_fidelity = _load(P08C1_ROOT / "target-fidelity.json")
    p08d_payload = _load(P08D_ROOT / "payload.json")
    cases = [
        _case("missing_domain_nonzero_assumption", "P08B exact assumption-set validator plus sealed P00 x/x and sqrt fixtures", "P08B request; P00 adversarial summary", assumption_rejected and p00["fixtures"][1]["effective_promotes"] is False and p00["fixtures"][2]["effective_promotes"] is False, "This does not prove assumption minimality."),
        _case("semantically_unrelated_lean_source", "Unrelated source lacks the bound theorem and retrieval/static/proof-state records remain diagnostic", "tests/test_lean_binding.py", _attested_case(test_attestation, "semantically_unrelated_lean_source") and binding["source_has_bound_goal"] is False and all(value == "diagnostic_only" for key, value in binding.items() if key.endswith("authority")), "No Lean process ran."),
        _case("sibling_parent_evidence_reuse", "Exact branch, obligation, and lineage readers reject cross-identity evidence", "tests/test_promotion_policy.py; tests/test_phase06_promotion_policy.py", _attested_case(test_attestation, "sibling_parent_evidence_reuse"), "Named guarded tests provide the executable check."),
        _case("tampered_manifest_raw_result_edit", "Native readers and exact promotion invariants bind manifest, raw result, and edit", "P08B raw reconstruction; tests/test_evidence_manifest.py", _attested_case(test_attestation, "tampered_manifest_raw_result_edit"), "No backend was rerun."),
        _case("parser_label_contamination", "P08C1 operator/span/obligation/order mutation matrix", "P08C1 target-fidelity.json", all(item["rejected"] for item in p08c1_fidelity["mutation_matrix"]), "Target fidelity is not proof."),
        _case("tool_available_adapter_absent", "Unavailable route remains engineering/configuration action", "tests/test_failure_ledgers.py", _attested_case(test_attestation, "tool_available_adapter_absent"), "Availability is not mathematical evidence."),
        _case("backend_timeout_adapter_exception", "Timeout and exception remain engineering ledger entries", "P00 adversarial summary; tests/test_failure_ledgers.py", _attested_case(test_attestation, "backend_timeout_adapter_exception") and any(item["id"] == "adapter_exception" and item["classification"] == "engineering_error" for item in p00["fixtures"]), "An engineering failure is not refutation."),
        _case("context_outside_local_file", "Context graph path/symlink/sibling constraints", "tests/test_document_context_graph.py", _attested_case(test_attestation, "context_outside_local_file"), "Named guarded tests provide the executable check."),
        _case("compact_omission_boundary_cursor", "P08D response and semantic cursor mutation matrices", "P08D payload.json", all(item.get("rejected") or item.get("semantic_binding_rejected") for item in p08d_payload["response_mutation_matrix"] + p08d_payload["semantic_token_mutation_matrix"]), "Payload conformance is not mathematical proof."),
        _case("serial_parallel_nondeterminism", "Semantic tree/ranking digests ignore schedule-only variance", "tests/test_derivation_search_orchestrator.py", _attested_case(test_attestation, "serial_parallel_nondeterminism"), "Schedule parity has diagnostic authority only."),
        _case("unknown_schema_legacy_authority", "Unknown and legacy records cannot manufacture current authority", "tests/test_promotion_policy.py; tests/test_evidence_manifest.py", _attested_case(test_attestation, "unknown_schema_legacy_authority"), "Legacy evidence remains historical."),
        _case("stale_source_output_truncation", "Source digests and bounded payload readers fail closed", "P08 source bindings; P08D token mutations", all(item["rejected"] for item in p08d_payload["token_mutation_matrix"]), "No new source extraction ran."),
        _case("conflicting_repeated_run", "No-overwrite identity collision controls", "tests/test_evidence_manifest.py; P09 writer", _attested_case(test_attestation, "conflicting_repeated_run"), "A collision is evidence-integrity failure, not a math result."),
        _case("gate_manifest_tamper", "Test-only aggregate data has no publication authority", "tests/test_phase06_promotion_policy.py", _attested_case(test_attestation, "gate_manifest_tamper"), "A test gate cannot authorize publication."),
        _case("private_error_data", "Direct/facade/FastMCP accepted P08D probe plus isolated guarded CLI test", "P08D payload; tests/test_document_derivation_red_team.py", _attested_case(test_attestation, "private_error_data") and p08d_payload["artifact_mutation_probe"]["private_path_scan_passed"] is True, "The P09 subprocess check is test-only and non-mathematical."),
    ]
    return {
        "schema_version": "p09_adversarial_matrix@1",
        "cases": cases,
        "case_count": len(cases),
        "all_passed": all(item["passed"] for item in cases),
        "guarded_test_attestation_digest": test_attestation["attestation_digest"],
        "mathematical_backend_attempt_count": 0,
        "document_audit_invocation_count": 0,
        "publication_enabled": False,
    }


def _reconciliation(reconstruction: Mapping[str, Any], adversarial: Mapping[str, Any]) -> dict[str, Any]:
    p08b = reconstruction["gates"]["p08b"]
    p08d = reconstruction["gates"]["p08d"]
    return {
        "schema_version": "p09_evidence_ledger_reconciliation@1",
        "identity_links": {
            "source": SOURCE_DIGESTS,
            "formalization_request_digest": p08b["request_digest"],
            "backend_result_digest": p08b["result_digest"],
            "product_payload_sha256": p08d["payload_sha256"],
        },
        "execution_reconciliation": {
            "historical_p08b_sympy_process_count": 1,
            "p09_mathematical_backend_process_count": 0,
            "p09_document_audit_count": 0,
            "later_product_gate_backend_process_count": 0,
        },
        "external_tools": [
            {"tool": "SymPy", "selected_role": "historical scoped derivative record validation", "executed_in_p09": False},
            {"tool": "SageMath", "selected_role": None, "executed_in_p09": False, "reason": "no new polynomial theorem or comparison"},
            {"tool": "Lean", "selected_role": "binding reader only", "executed_in_p09": False},
            {"tool": "LeanSearch-v2/LeanExplore/jixia/Pantograph/LeanDojo", "selected_role": None, "executed_in_p09": False, "reason": "no premise or proof-state task"},
        ],
        "ledgers": {
            "engineering_correctness": "pass",
            "evidence_integrity": "pass",
            "mathematical_validity": "backend_checked_computational_support_not_proof",
            "scientific_interpretation": "one_scoped_real_subclaim_only",
        },
        "historical_negative_and_superseded": {
            "p08c_status": reconstruction["gates"]["p08c"]["status"],
            "accepted_successor": "P08D",
            "latest_directory_selection_used": False,
        },
        "product_semantics": {
            "compact_detailed_resolver_parity": "pass",
            "target_page_count": p08d["target_page_count"],
            "resolver_page_count": p08d["resolver_page_count"],
        },
        "capability_ladder": {
            "pre_registered_candidate": "eq:cashflow-rate-derivative",
            "status": "backend_checked",
            "formal_proof_certified": False,
        },
        "code_identity_policy": {
            "p08ab": "preserved historical snapshots",
            "p08c1_p08d": "accepted code identities plus current bound readers",
        },
        "adversarial_all_passed": adversarial["all_passed"],
        "unexplained_discrepancies": [],
        **AUTHORITY_FIELDS,
    }


def _candidate_status(reconstruction: Mapping[str, Any], adversarial: Mapping[str, Any], reconciliation: Mapping[str, Any]) -> str:
    classification = reconstruction.get("classification")
    if classification == "blocked":
        return "BLOCKED"
    if classification == "unsafe":
        return "UNSAFE"
    if classification != "complete":
        return "BLOCKED"
    gates = reconstruction["gates"]
    if reconstruction["predecessor_inventory_unchanged"] is not True:
        return "UNSAFE"
    if not all(item["status"].startswith("pass") for item in gates.values()):
        return "UNSAFE"
    if not adversarial["all_passed"] or reconciliation["unexplained_discrepancies"]:
        return "UNSAFE"
    if not gates["p08b"]["backend_checked"] or gates["p08d"]["status"] != "pass":
        return "UNSAFE"
    return "SAFE_AND_SUBSTANTIVELY_USEFUL"


def _head_commit() -> str:
    try:
        git_dir = WORKSPACE / ".git"
        head = _read(git_dir / "HEAD").decode("ascii", "strict").strip()
        if head.startswith("ref: "):
            ref = head[5:]
            path = git_dir / ref
            if path.is_file():
                value = _read(path).decode("ascii", "strict").strip()
            else:
                value = ""
                for line in _read(git_dir / "packed-refs").decode("ascii", "strict").splitlines():
                    if line and not line.startswith(("#", "^")):
                        digest, name = line.split(" ", 1)
                        if name == ref:
                            value = digest
                            break
        else:
            value = head
    except (IntegrityVeto, OSError, UnicodeError, ValueError) as exc:
        raise ClassificationBlock("cannot read the current git commit without a subprocess") from exc
    if len(value) != 40 or any(char not in "0123456789abcdef" for char in value):
        raise ClassificationBlock("cannot resolve the current git commit without a subprocess")
    return value


def _current_code_refs() -> list[str]:
    refs = set(CURRENT_CODE_SEED_REFS)
    refs.update(
        path.relative_to(WORKSPACE).as_posix()
        for path in (WORKSPACE / "src/mathdevmcp").rglob("*.py")
    )
    refs.update(
        path.relative_to(WORKSPACE).as_posix()
        for path in (WORKSPACE / "tests").rglob("*.py")
    )
    fixture_root = WORKSPACE / "tests/fixtures"
    if fixture_root.is_dir() and not fixture_root.is_symlink():
        refs.update(
            path.relative_to(WORKSPACE).as_posix()
            for path in fixture_root.rglob("*")
            if path.is_file()
        )
    return sorted(refs, key=lambda value: value.encode("utf-8"))


def _current_code_bindings() -> list[dict[str, Any]]:
    return [_binding(WORKSPACE / ref, ref) for ref in _current_code_refs()]


def _expected_guarded_test_runtime_identity() -> dict[str, Any]:
    distributions: dict[str, str] = {}
    for name in ("anyio", "httpx", "mcp", "pydantic", "pytest"):
        try:
            distributions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError as exc:
            raise ClassificationBlock(
                f"required Phase 09 runtime distribution is absent: {name}"
            ) from exc
    return {
        "schema_version": "p09_guarded_test_runtime_identity@3",
        "cwd": str(WORKSPACE.resolve()),
        "python_executable": P09_PYTHON,
        "python_version": P09_PYTHON_VERSION,
        "pythonpath": "src",
        "dont_write_bytecode": True,
        "root_distribution_versions": distributions,
        "module_origins": {
            "mathdevmcp": str((WORKSPACE / "src/mathdevmcp/__init__.py").resolve()),
            "p09_guard": str((WORKSPACE / "tests/p09_no_live_backend_guard.py").resolve()),
            "p09_runner": str((WORKSPACE / "scripts/run_p09_final_red_team.py").resolve()),
        },
    }


def _candidate_inventory(run_root: Path) -> list[dict[str, Any]]:
    return [_binding(run_root / ref, ref) for ref in CANDIDATE_ARTIFACTS]


def _load_candidate(run_root: Path) -> dict[str, Any]:
    candidate = _load(run_root / "candidate-decision.json")
    expected = _candidate_decision_digest(candidate)
    if candidate.get("candidate_decision_digest") != expected:
        raise IntegrityVeto("candidate decision digest mismatch")
    inventory = _candidate_inventory(run_root)
    if (
        candidate.get("artifact_inventory") != inventory
        or candidate.get("artifact_inventory_digest") != _sha256(inventory)
    ):
        raise IntegrityVeto("candidate artifact inventory mismatch")
    if any(candidate.get(key) is not value for key, value in AUTHORITY_FIELDS.items()):
        raise IntegrityVeto("candidate crossed a fixed authority boundary")
    if candidate.get("status") not in {"SAFE_AND_SUBSTANTIVELY_USEFUL", "UNSAFE", "BLOCKED"}:
        raise IntegrityVeto("candidate emitted an unreachable status")
    return candidate


def _allocate_run_root() -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    suffix = _sha256(
        {
            "timestamp": timestamp,
            "time_ns": time.time_ns(),
            "pid": os.getpid(),
            "runner_sha256": _sha256(_read(Path(__file__))),
        }
    )[:12]
    run_root = OUTPUT_PARENT / f"{timestamp}-{suffix}"
    OUTPUT_PARENT.mkdir(parents=True, exist_ok=True)
    if OUTPUT_PARENT.is_symlink() or run_root.exists() or run_root.is_symlink():
        raise P09Error("fresh Phase 09 run root is unsafe or already exists")
    run_root.mkdir(mode=0o700)
    return run_root


def _safe_error(exc: BaseException) -> dict[str, str]:
    detail = str(exc).replace(str(WORKSPACE), "<workspace>")
    return {
        "exception_type": type(exc).__name__,
        "detail": detail[:2_000],
    }


def _failure_artifacts(
    *,
    status: str,
    error: Mapping[str, str],
    before: Mapping[str, Any] | None,
    after: Mapping[str, Any] | None,
    forbidden_attempts: Sequence[Mapping[str, str]],
    blocked_imports: Sequence[str],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    classification = "unsafe" if status == "UNSAFE" else "blocked"
    reconstruction = {
        "schema_version": "p09_reconstruction_ledger@1",
        "classification": classification,
        "accepted_roots": {
            "p08ab": P08AB_ROOT.relative_to(WORKSPACE).as_posix(),
            "p08c": P08C_ROOT.relative_to(WORKSPACE).as_posix(),
            "p08c1": P08C1_ROOT.relative_to(WORKSPACE).as_posix(),
            "p08d": P08D_ROOT.relative_to(WORKSPACE).as_posix(),
        },
        "predecessor_inventory_before": before,
        "predecessor_inventory_after": after,
        "predecessor_inventory_unchanged": before is not None and before == after,
        "gates": {},
        "failure": dict(error),
        "forbidden_attempts": [dict(item) for item in forbidden_attempts],
        "blocked_imports": list(blocked_imports),
        "mathematical_backend_execution_count": 0,
        "document_audit_execution_count": 0,
        "publication_enabled": False,
    }
    adversarial = {
        "schema_version": "p09_adversarial_matrix@1",
        "cases": [],
        "case_count": 0,
        "all_passed": False,
        "not_run_reason": dict(error),
        "mathematical_backend_execution_count": 0,
        "document_audit_execution_count": 0,
        "publication_enabled": False,
    }
    reconciliation = {
        "schema_version": "p09_evidence_ledger_reconciliation@1",
        "ledgers": {
            "engineering_correctness": "blocked" if status == "BLOCKED" else "not_ranked_after_veto",
            "evidence_integrity": "veto" if status == "UNSAFE" else "unclassified",
            "mathematical_validity": "not_reinterpreted",
            "scientific_interpretation": "no_claim",
        },
        "unexplained_discrepancies": [dict(error)],
        "adversarial_all_passed": False,
        **AUTHORITY_FIELDS,
    }
    return reconstruction, adversarial, reconciliation


def _load_guarded_test_attestation() -> dict[str, Any]:
    raw_ref = os.environ.get("MATHDEVMCP_P09_TEST_ATTESTATION")
    if not raw_ref:
        raise ClassificationBlock("guarded named-suite attestation is required")
    raw_path = Path(raw_ref)
    path = (WORKSPACE / raw_path).resolve() if not raw_path.is_absolute() else raw_path.resolve()
    parent = TEST_ATTESTATION_PARENT.resolve()
    if (
        path.parent != parent
        or path.is_symlink()
        or not path.is_file()
        or path.suffix != ".json"
    ):
        raise ClassificationBlock("guarded named-suite attestation path is outside the preflight root")
    record = _load(path)
    digest = _sha256(
        {key: value for key, value in record.items() if key != "attestation_digest"}
    )
    expected_environment = {
        "CUDA_VISIBLE_DEVICES": "-1",
        "PYTHONHASHSEED": "0",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
        "PYTHONPATH": "src",
    }
    code_bindings = _current_code_bindings()
    collected_nodeids = record.get("collected_nodeids")
    passed_nodeids = record.get("passed_nodeids")
    child_attestations = record.get("guard_attestation", {}).get(
        "guarded_cli_attestations"
    )
    if (
        record.get("schema_version") != "p09_guarded_named_suite_attestation@3"
        or record.get("attestation_digest") != digest
        or record.get("exit_status") != 0
        or record.get("all_passed") is not True
        or record.get("failed_nodeids") != []
        or record.get("skipped_nodeids") != []
        or record.get("collection_failed_nodeids") != []
        or record.get("collection_skipped_nodeids") != []
        or not isinstance(collected_nodeids, list)
        or collected_nodeids != passed_nodeids
        or len(collected_nodeids) != len(set(collected_nodeids))
        or record.get("pytest_args") != list(NAMED_TEST_INVOCATION_ARGS)
        or record.get("environment") != expected_environment
        or record.get("runtime_identity") != _expected_guarded_test_runtime_identity()
        or record.get("runtime_identity_unchanged") is not True
        or record.get("guard_attestation", {}).get("schema_version")
        != "p09_pytest_guard_attestation@2"
        or record.get("guard_attestation", {}).get("forbidden_attempt_count") != 0
        or record.get("guard_attestation", {}).get("guarded_cli_invocation_count") != 1
        or not isinstance(child_attestations, list)
        or len(child_attestations) != 1
        or child_attestations[0].get("schema_version")
        != "p09_child_guard_attestation@1"
        or child_attestations[0].get("attempts") != []
        or child_attestations[0].get("forbidden_attempt_count") != 0
        or child_attestations[0].get("process_attempt_count") != 0
        or child_attestations[0].get("mathematical_backend_attempt_count") != 0
        or child_attestations[0].get("document_audit_invocation_count") != 0
        or child_attestations[0].get("network_attempt_count") != 0
        or child_attestations[0].get("resolved_verb")
        != "resolve-document-derivation-records"
        or record.get("guard_attestation", {}).get("mathematical_backend_attempt_count") != 0
        or record.get("guard_attestation", {}).get("document_audit_invocation_count") != 0
        or record.get("guard_attestation", {}).get("network_attempt_count") != 0
        or record.get("code_bindings_unchanged") is not True
        or record.get("code_bindings_start") != code_bindings
        or record.get("code_bindings_end") != code_bindings
        or record.get("code_bindings") != code_bindings
        or record.get("code_bindings_digest") != _sha256(code_bindings)
    ):
        raise IntegrityVeto("guarded named-suite attestation boundary mismatch")
    for case_id in TEST_CASE_NODEIDS:
        _attested_case(record, case_id)
    return record


def _perform_reconstruction(
    before: Mapping[str, Any],
    forbidden_attempts: list[dict[str, str]],
    blocked_imports: list[str],
    test_attestation: Mapping[str, Any],
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    snapshot_root = P08AB_ROOT / "code-snapshot"
    attested_code = {
        item["ref"]: item["sha256"]
        for item in test_attestation.get("code_bindings", [])
        if isinstance(item, Mapping)
        and isinstance(item.get("ref"), str)
        and isinstance(item.get("sha256"), str)
    }
    required_current_modules = {
        "scripts/run_p08c1_target_fidelity_replay.py",
        "scripts/run_p08d_frozen_payload_replay.py",
    }
    if not required_current_modules <= set(attested_code):
        raise IntegrityVeto("guarded-test attestation lacks current replay module bindings")
    for gate, expected_digests in (
        ("P08C1", P08C1_CODE_DIGESTS),
        ("P08D", P08D_CODE_DIGESTS),
    ):
        for ref, accepted_sha256 in expected_digests.items():
            raw = _read(WORKSPACE / ref)
            if (
                _sha256(raw) != accepted_sha256
                or attested_code.get(ref) != accepted_sha256
            ):
                raise IntegrityVeto(
                    f"{gate} replay code differs from accepted or attested identity: {ref}"
                )
    with _no_backend_imports(blocked_imports):
        with _execution_guard(forbidden_attempts):
            snapshot = _reconstruct_p08_code_snapshot()
            snapshot_runner = _load_verified_module(
                "p09_p08_snapshot_runner",
                snapshot_root / "scripts/run_p08_frozen_validation.py",
                P08_SNAPSHOT_DIGESTS["scripts/run_p08_frozen_validation.py"],
            )
            adapter = _load_verified_module(
                "p09_p08_sympy_adapter",
                snapshot_root / "src/mathdevmcp/sympy_derivative_adapter.py",
                P08_SNAPSHOT_DIGESTS["src/mathdevmcp/sympy_derivative_adapter.py"],
            )
            p08c1 = _load_verified_module(
                "p09_p08c1_runner",
                WORKSPACE / "scripts/run_p08c1_target_fidelity_replay.py",
                P08C1_CODE_DIGESTS["scripts/run_p08c1_target_fidelity_replay.py"],
            )
            p08d = _load_verified_module(
                "p09_p08d_runner",
                WORKSPACE / "scripts/run_p08d_frozen_payload_replay.py",
                P08D_CODE_DIGESTS["scripts/run_p08d_frozen_payload_replay.py"],
            )
            validator_errors = (
                snapshot_runner.Phase08Error,
                adapter.SympyDerivativeContractError,
                p08c1.ReplayError,
                p08d.ReplayError,
                ValueError,
            )
            try:
                gates = {
                    "p08a": _reconstruct_p08a(snapshot_runner),
                    "p08b": _reconstruct_p08b(snapshot_runner, adapter),
                    "p08c": _reconstruct_p08c(),
                    "p08c1": _reconstruct_p08c1(p08c1),
                    "p08d": _reconstruct_p08d(p08d),
                }
                adversarial = _adversarial_matrix(
                    adapter, p08c1, p08d, test_attestation
                )
            except (
                IntegrityVeto,
                KeyError,
                IndexError,
                TypeError,
                AttributeError,
                AssertionError,
            ) as exc:
                raise IntegrityVeto(str(exc)) from exc
            except validator_errors as exc:
                raise IntegrityVeto(str(exc)) from exc
    if forbidden_attempts or blocked_imports:
        raise ClassificationBlock("Phase 09 reconstruction crossed a blocked execution route")
    after = _all_predecessor_inventories()
    reconstruction = {
        "schema_version": "p09_reconstruction_ledger@1",
        "classification": "complete",
        "accepted_roots": {
            "p08ab": P08AB_ROOT.relative_to(WORKSPACE).as_posix(),
            "p08c": P08C_ROOT.relative_to(WORKSPACE).as_posix(),
            "p08c1": P08C1_ROOT.relative_to(WORKSPACE).as_posix(),
            "p08d": P08D_ROOT.relative_to(WORKSPACE).as_posix(),
        },
        "p08_code_snapshot": snapshot,
        "guarded_test_attestation_digest": test_attestation["attestation_digest"],
        "predecessor_inventory_before": before,
        "predecessor_inventory_after": after,
        "predecessor_inventory_unchanged": before == after,
        "gates": gates,
        "forbidden_attempts": [],
        "blocked_imports": [],
        "mathematical_backend_execution_count": 0,
        "document_audit_execution_count": 0,
        "publication_enabled": False,
    }
    if before != after:
        raise IntegrityVeto("predecessor evidence changed during Phase 09 reconstruction")
    return reconstruction, adversarial, _reconciliation(reconstruction, adversarial)


def _manifest_record(
    *,
    run_root: Path,
    started: float,
    code_bindings: Sequence[Mapping[str, Any]],
    git_commit: str | None,
    status: str,
    forbidden_attempts: Sequence[Mapping[str, str]],
    blocked_imports: Sequence[str],
    material_input_bindings: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    return {
        "schema_version": "p09_run_manifest@1",
        "run_id": run_root.name,
        "run_root": run_root.relative_to(WORKSPACE).as_posix(),
        "created_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "git_commit": git_commit,
        "git_state": "dirty_worktree_preserved; exact relevant code bindings recorded below",
        "command": [str(item) for item in sys.argv],
        "interpreter": sys.executable,
        "python_version": platform.python_version(),
        "environment": os.environ.get("CONDA_DEFAULT_ENV") or "system/default",
        "cpu_gpu_status": "CPU-only; GPU devices intentionally hidden",
        "cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"),
        "python_hash_seed": os.environ.get("PYTHONHASHSEED"),
        "data_version": "literal accepted P08A/P08B/P08C/P08C1/P08D roots",
        "random_seeds": "N/A; deterministic JSON, digest, and reader replay",
        "wall_time_seconds": round(time.monotonic() - started, 6),
        "candidate_classification": status,
        "predecessor_decision_digests": P08_DECISIONS,
        "source_digests": SOURCE_DIGESTS,
        "p08_code_identity_digest": P08_CODE_IDENTITY_DIGEST,
        "p08_run_binding_digest": P08_RUN_BINDING_DIGEST,
        "current_code_bindings": list(code_bindings),
        "current_code_bindings_digest": _sha256(list(code_bindings)),
        "material_input_bindings": list(material_input_bindings),
        "material_input_bindings_digest": _sha256(list(material_input_bindings)),
        "temporary_root_policy": "/tmp only for P08D fresh product reconstruction; removed before candidate output",
        "forbidden_attempts": [dict(item) for item in forbidden_attempts],
        "blocked_imports": list(blocked_imports),
        "mathematical_backend_execution_count": 0,
        "document_audit_execution_count": 0,
        "network_execution_count": 0,
        "plan_ref": PLAN_REF,
        "result_ref": RESULT_REF,
        "review_state": "pending_substantive_read_only_result_review",
        "stale_full_suite_context": {
            "historical_count": "1472 passed, 38 failed, 4 skipped",
            "sealed_log_available": False,
            "authority": "none; not a comparator, current-health claim, promotion criterion, or veto",
        },
    }


def _run_root(value: str) -> Path:
    path = Path(value)
    resolved = (WORKSPACE / path).resolve() if not path.is_absolute() else path.resolve()
    if resolved.parent != OUTPUT_PARENT.resolve() or resolved.name in {"latest", "current"}:
        raise P09Error("Phase 09 requires a literal direct-child run root")
    if resolved.is_symlink() or not resolved.is_dir():
        raise P09Error("Phase 09 run root is absent or symlinked")
    return resolved


def _verify_candidate_state(
    run_root: Path,
    *,
    require_live_state: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    candidate = _load_candidate(run_root)
    reconstruction = _load(run_root / "reconstruction-ledger.json")
    adversarial = _load(run_root / "adversarial-matrix.json")
    reconciliation = _load(run_root / "evidence-ledger-reconciliation.json")
    manifest = _load(run_root / "run-manifest.json")
    test_attestation = _load(run_root / "guarded-test-attestation.json")
    code_bindings = manifest.get("current_code_bindings")
    if (
        manifest.get("schema_version") != "p09_run_manifest@1"
        or manifest.get("run_id") != run_root.name
        or manifest.get("run_root") != run_root.relative_to(WORKSPACE).as_posix()
        or manifest.get("candidate_classification") != candidate["status"]
        or not isinstance(code_bindings, list)
        or manifest.get("current_code_bindings_digest") != _sha256(code_bindings)
        or manifest.get("mathematical_backend_execution_count") != 0
        or manifest.get("document_audit_execution_count") != 0
        or manifest.get("network_execution_count") != 0
        or manifest.get("material_input_bindings")
        != (
            reconstruction.get("predecessor_inventory_before", {}).get(
                "material_inputs", []
            )
            if isinstance(reconstruction.get("predecessor_inventory_before"), Mapping)
            else []
        )
        or manifest.get("material_input_bindings_digest")
        != _sha256(manifest.get("material_input_bindings", []))
        or (
            candidate["status"] == "SAFE_AND_SUBSTANTIVELY_USEFUL"
            and (
                test_attestation.get("all_passed") is not True
                or test_attestation.get("attestation_digest")
                != _sha256(
                    {
                        key: value
                        for key, value in test_attestation.items()
                        if key != "attestation_digest"
                    }
                )
                or reconstruction.get("guarded_test_attestation_digest")
                != test_attestation.get("attestation_digest")
                or adversarial.get("guarded_test_attestation_digest")
                != test_attestation.get("attestation_digest")
            )
        )
    ):
        raise IntegrityVeto("candidate run manifest boundary mismatch")
    expected_status = _candidate_status(reconstruction, adversarial, reconciliation)
    if candidate["status"] != expected_status:
        raise IntegrityVeto("candidate status differs from independent status reconstruction")
    if (
        candidate.get("mathematical_backend_execution_count") != 0
        or candidate.get("document_audit_execution_count") != 0
        or candidate.get("forbidden_attempt_count")
        != len(manifest.get("forbidden_attempts", []))
        + len(manifest.get("blocked_imports", []))
    ):
        raise IntegrityVeto("candidate execution-attempt accounting mismatch")
    if require_live_state:
        current_code = _current_code_bindings()
        if (
            code_bindings != current_code
            or test_attestation.get("code_bindings") != current_code
        ):
            raise IntegrityVeto("reviewed current code changed after candidate creation")
        if (
            test_attestation.get("runtime_identity")
            != _expected_guarded_test_runtime_identity()
        ):
            raise IntegrityVeto("reviewed runtime environment changed after candidate creation")
        current_material_inputs = _material_input_inventory()
        if manifest.get("material_input_bindings") != current_material_inputs:
            raise IntegrityVeto("material inputs changed or were unbound after candidate creation")
        before = reconstruction.get("predecessor_inventory_before")
        after = reconstruction.get("predecessor_inventory_after")
        if before is not None:
            current_predecessors = _all_predecessor_inventories()
            if before != current_predecessors or (
                after is not None and after != current_predecessors
            ):
                raise IntegrityVeto("predecessor evidence changed after candidate creation")
    return candidate, reconstruction, adversarial, reconciliation


def _review_bindings(run_root: Path, candidate: Mapping[str, Any]) -> dict[str, str]:
    return {
        "run_root": run_root.relative_to(WORKSPACE).as_posix(),
        "candidate_decision_digest": str(candidate["candidate_decision_digest"]),
        "candidate_file_sha256": _sha256(_read(run_root / "candidate-decision.json")),
        "candidate_artifact_inventory_digest": str(candidate["artifact_inventory_digest"]),
    }


def _require_review_bindings(
    review_text: str,
    expected: Mapping[str, str],
) -> None:
    lines = review_text.splitlines()
    for key, prefix in REVIEW_BINDING_PREFIXES.items():
        matches = [line[len(prefix) :] for line in lines if line.startswith(prefix)]
        if matches != [expected[key]]:
            raise IntegrityVeto(f"review record lacks exact unique {key} binding")


def create_candidate(args: argparse.Namespace) -> dict[str, Any]:
    started = time.monotonic()
    run_root = _allocate_run_root()
    before: dict[str, Any] | None = None
    after: dict[str, Any] | None = None
    forbidden_attempts: list[dict[str, str]] = []
    blocked_imports: list[str] = []
    error: dict[str, str] | None = None
    status = "BLOCKED"
    code_bindings: list[dict[str, Any]] = []
    test_attestation: dict[str, Any] | None = None
    git_commit: str | None = None
    try:
        _runtime_boundary()
        try:
            code_bindings = _current_code_bindings()
        except (IntegrityVeto, OSError, UnicodeError, ValueError) as exc:
            raise ClassificationBlock("cannot bind the current reviewed code") from exc
        git_commit = _head_commit()
        test_attestation = _load_guarded_test_attestation()
        if test_attestation.get("code_bindings") != code_bindings:
            raise IntegrityVeto("guarded named-suite code closure differs at candidate launch")
        before = _all_predecessor_inventories()
        reconstruction, adversarial, reconciliation = _perform_reconstruction(
            before,
            forbidden_attempts,
            blocked_imports,
            test_attestation,
        )
        after = reconstruction["predecessor_inventory_after"]
        if _current_code_bindings() != code_bindings:
            raise IntegrityVeto("reviewed current code changed during candidate creation")
        status = _candidate_status(reconstruction, adversarial, reconciliation)
    except IntegrityVeto as exc:
        status = "UNSAFE"
        error = _safe_error(exc)
        try:
            after = _all_predecessor_inventories()
        except (P09Error, OSError, UnicodeError, ValueError):
            after = None
        reconstruction, adversarial, reconciliation = _failure_artifacts(
            status=status,
            error=error,
            before=before,
            after=after,
            forbidden_attempts=forbidden_attempts,
            blocked_imports=blocked_imports,
        )
    except (ClassificationBlock, P09Error, OSError, UnicodeError, ValueError) as exc:
        status = "BLOCKED"
        error = _safe_error(exc)
        try:
            after = _all_predecessor_inventories()
        except (P09Error, OSError, UnicodeError, ValueError):
            after = None
        reconstruction, adversarial, reconciliation = _failure_artifacts(
            status=status,
            error=error,
            before=before,
            after=after,
            forbidden_attempts=forbidden_attempts,
            blocked_imports=blocked_imports,
        )
    except Exception as exc:
        status = "BLOCKED"
        error = _safe_error(exc)
        reconstruction, adversarial, reconciliation = _failure_artifacts(
            status=status,
            error=error,
            before=before,
            after=after,
            forbidden_attempts=forbidden_attempts,
            blocked_imports=blocked_imports,
        )
    if test_attestation is None:
        test_attestation = {
            "schema_version": "p09_guarded_named_suite_attestation@3",
            "all_passed": False,
            "exit_status": None,
            "not_available_reason": error,
        }
        test_attestation["attestation_digest"] = _sha256(test_attestation)
    _write_new(run_root / "guarded-test-attestation.json", test_attestation)
    _write_new(run_root / "reconstruction-ledger.json", reconstruction)
    _write_new(run_root / "adversarial-matrix.json", adversarial)
    _write_new(run_root / "evidence-ledger-reconciliation.json", reconciliation)
    manifest = _manifest_record(
        run_root=run_root,
        started=started,
        code_bindings=code_bindings,
        git_commit=git_commit,
        status=status,
        forbidden_attempts=forbidden_attempts,
        blocked_imports=blocked_imports,
        material_input_bindings=(
            before.get("material_inputs", []) if isinstance(before, Mapping) else []
        ),
    )
    _write_new(run_root / "run-manifest.json", manifest)
    inventory = _candidate_inventory(run_root)
    candidate = {
        "schema_version": "p09_candidate_decision@1",
        "status": status,
        "hard_bound_positive_phase08_entry": True,
        "safe_but_capability_incomplete_reachable": False,
        "primary_criterion_met": status == "SAFE_AND_SUBSTANTIVELY_USEFUL",
        "vetoes": [error] if status == "UNSAFE" and error is not None else [],
        "blocking_findings": [error] if status == "BLOCKED" and error is not None else [],
        "p08_decision_digests": P08_DECISIONS,
        "artifact_inventory": inventory,
        "artifact_inventory_digest": _sha256(inventory),
        "review_status": "pending",
        "forbidden_attempt_count": len(forbidden_attempts) + len(blocked_imports),
        "mathematical_backend_execution_count": 0,
        "document_audit_execution_count": 0,
        **AUTHORITY_FIELDS,
        "non_claims": [
            "This candidate is not final until substantive read-only review is adjudicated.",
            "The scoped backend-checked result is computational support, not formal proof.",
            "Two frozen documents do not establish broad corpus generalization.",
            "No publication, default, release, source-edit, or experimental-repair authority is granted.",
        ],
    }
    candidate["candidate_decision_digest"] = _candidate_decision_digest(candidate)
    _write_new(run_root / "candidate-decision.json", candidate)
    return {
        "status": candidate["status"],
        "run_root": run_root.relative_to(WORKSPACE).as_posix(),
        "candidate_decision_digest": candidate["candidate_decision_digest"],
        "candidate_file_sha256": _sha256(_read(run_root / "candidate-decision.json")),
        "candidate_artifact_inventory_digest": candidate["artifact_inventory_digest"],
        "final_decision_present": False,
    }


def verify_candidate(args: argparse.Namespace) -> dict[str, Any]:
    _runtime_boundary()
    run_root = _run_root(args.run_root)
    if (run_root / "decision.json").exists() or (run_root / "review-adjudication.json").exists():
        raise IntegrityVeto("candidate verification requires pre-finalization state")
    candidate, _, _, _ = _verify_candidate_state(run_root, require_live_state=True)
    if candidate["candidate_decision_digest"] != args.expected_candidate_decision_digest:
        raise IntegrityVeto("candidate decision differs from the create handoff")
    return {
        "status": candidate["status"],
        "verified": True,
        "run_root": run_root.relative_to(WORKSPACE).as_posix(),
        "candidate_decision_digest": candidate["candidate_decision_digest"],
        "candidate_file_sha256": _sha256(_read(run_root / "candidate-decision.json")),
        "candidate_artifact_inventory_digest": candidate["artifact_inventory_digest"],
        "final_decision_present": False,
    }


def finalize(args: argparse.Namespace) -> dict[str, Any]:
    _runtime_boundary()
    run_root = _run_root(args.run_root)
    if (run_root / "decision.json").exists() or (run_root / "decision.json").is_symlink():
        raise P09Error("Phase 09 final decision is no-overwrite and single-use")
    candidate, _, _, _ = _verify_candidate_state(run_root, require_live_state=True)
    review_path = Path(args.review_record)
    review_path = (WORKSPACE / review_path).resolve() if not review_path.is_absolute() else review_path.resolve()
    if review_path.is_symlink() or not review_path.is_file() or not review_path.is_relative_to(WORKSPACE):
        raise P09Error("review record must be a regular workspace file")
    review_raw = _read(review_path)
    review_text = review_raw.decode("utf-8", "strict")
    bindings = _review_bindings(run_root, candidate)
    _require_review_bindings(review_text, bindings)
    outcome = args.review_outcome
    if outcome == "agree":
        if review_text.rstrip().splitlines()[-1] != "VERDICT: AGREE":
            raise IntegrityVeto("agree adjudication lacks the exact terminal reviewer verdict")
        final_status = candidate["status"]
    elif outcome == "accepted-claim-boundary-finding":
        if review_text.rstrip().splitlines()[-1] != "VERDICT: REVISE":
            raise IntegrityVeto("unsafe adjudication lacks the exact terminal revise verdict")
        final_status = "UNSAFE"
    elif outcome == "blocked":
        if review_text.rstrip().splitlines()[-1] != "VERDICT: BLOCKED":
            raise IntegrityVeto("blocked adjudication lacks the exact terminal blocked verdict")
        final_status = "BLOCKED"
    else:
        raise P09Error("unknown review adjudication outcome")
    adjudication = {
        "schema_version": "p09_review_adjudication@1",
        "run_root": bindings["run_root"],
        "candidate_decision_digest": candidate["candidate_decision_digest"],
        "candidate_file_sha256": bindings["candidate_file_sha256"],
        "candidate_artifact_inventory_digest": candidate["artifact_inventory_digest"],
        "review_record_ref": review_path.relative_to(WORKSPACE).as_posix(),
        "review_record_sha256": _sha256(review_raw),
        "review_outcome": outcome,
        "candidate_status": candidate["status"],
        "final_status": final_status,
        "candidate_bytes_changed": False,
        "material_finding_silently_rejected": False,
        **AUTHORITY_FIELDS,
    }
    adjudication["adjudication_digest"] = _sha256(adjudication)
    _write_new_or_require_identical(run_root / "review-adjudication.json", adjudication)
    _verify_candidate_state(run_root, require_live_state=True)
    final_inventory = [
        *_candidate_inventory(run_root),
        _binding(run_root / "candidate-decision.json", "candidate-decision.json"),
        _binding(run_root / "review-adjudication.json", "review-adjudication.json"),
    ]
    decision = {
        "schema_version": "p09_final_decision@1",
        "status": final_status,
        "candidate_status": candidate["status"],
        "candidate_decision_digest": candidate["candidate_decision_digest"],
        "review_adjudication_digest": adjudication["adjudication_digest"],
        "primary_criterion_met": final_status == "SAFE_AND_SUBSTANTIVELY_USEFUL",
        "hard_bound_positive_phase08_entry": True,
        "safe_but_capability_incomplete_reachable": False,
        "artifact_inventory": final_inventory,
        "artifact_inventory_digest": _sha256(final_inventory),
        "mathematical_backend_execution_count": 0,
        "document_audit_execution_count": 0,
        "network_execution_count": 0,
        **AUTHORITY_FIELDS,
        "non_claims": candidate["non_claims"],
    }
    decision["decision_digest"] = _decision_digest(decision)
    _write_new(run_root / "decision.json", decision)
    return {
        "status": decision["status"],
        "run_root": run_root.relative_to(WORKSPACE).as_posix(),
        "decision_digest": decision["decision_digest"],
    }


def verify_final(args: argparse.Namespace) -> dict[str, Any]:
    _runtime_boundary()
    run_root = _run_root(args.run_root)
    candidate, _, _, _ = _verify_candidate_state(run_root, require_live_state=True)
    adjudication = _load(run_root / "review-adjudication.json")
    decision = _load(run_root / "decision.json")
    if adjudication.get("adjudication_digest") != _sha256({key: value for key, value in adjudication.items() if key != "adjudication_digest"}):
        raise IntegrityVeto("review adjudication digest mismatch")
    if decision.get("decision_digest") != _decision_digest(decision):
        raise IntegrityVeto("final decision digest mismatch")
    if decision["decision_digest"] != args.expected_decision_digest:
        raise IntegrityVeto("final decision differs from finalization handoff")
    review_path = WORKSPACE / adjudication["review_record_ref"]
    review_raw = _read(review_path)
    review_text = review_raw.decode("utf-8", "strict")
    bindings = _review_bindings(run_root, candidate)
    _require_review_bindings(review_text, bindings)
    if (
        _sha256(review_raw) != adjudication["review_record_sha256"]
        or adjudication.get("run_root") != bindings["run_root"]
        or adjudication.get("candidate_decision_digest")
        != bindings["candidate_decision_digest"]
        or adjudication.get("candidate_file_sha256")
        != bindings["candidate_file_sha256"]
        or adjudication.get("candidate_artifact_inventory_digest")
        != bindings["candidate_artifact_inventory_digest"]
    ):
        raise IntegrityVeto("bound review record drift")
    outcome = adjudication["review_outcome"]
    terminal_verdict = review_text.rstrip().splitlines()[-1]
    required_verdict = {
        "agree": "VERDICT: AGREE",
        "accepted-claim-boundary-finding": "VERDICT: REVISE",
        "blocked": "VERDICT: BLOCKED",
    }.get(outcome)
    if terminal_verdict != required_verdict:
        raise IntegrityVeto("review outcome differs from its terminal verdict")
    expected_status = (
        candidate["status"]
        if outcome == "agree"
        else "UNSAFE"
        if outcome == "accepted-claim-boundary-finding"
        else "BLOCKED"
    )
    expected_inventory = [
        *_candidate_inventory(run_root),
        _binding(run_root / "candidate-decision.json", "candidate-decision.json"),
        _binding(run_root / "review-adjudication.json", "review-adjudication.json"),
    ]
    if (
        decision.get("status") != expected_status
        or decision.get("candidate_decision_digest") != candidate["candidate_decision_digest"]
        or decision.get("review_adjudication_digest") != adjudication["adjudication_digest"]
        or decision.get("artifact_inventory") != expected_inventory
        or decision.get("artifact_inventory_digest") != _sha256(expected_inventory)
        or decision.get("mathematical_backend_execution_count") != 0
        or decision.get("document_audit_execution_count") != 0
        or decision.get("network_execution_count") != 0
        or any(decision.get(key) is not value for key, value in AUTHORITY_FIELDS.items())
        or decision.get("safe_but_capability_incomplete_reachable") is not False
    ):
        raise IntegrityVeto("final decision boundary or inventory mismatch")
    return {
        "status": decision["status"],
        "verified": True,
        "run_root": run_root.relative_to(WORKSPACE).as_posix(),
        "decision_digest": decision["decision_digest"],
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    create = sub.add_parser("create-candidate")
    create.set_defaults(handler=create_candidate)
    verify = sub.add_parser("verify-candidate")
    verify.add_argument("--run-root", required=True)
    verify.add_argument("--expected-candidate-decision-digest", required=True)
    verify.set_defaults(handler=verify_candidate)
    finish = sub.add_parser("finalize")
    finish.add_argument("--run-root", required=True)
    finish.add_argument("--review-record", required=True)
    finish.add_argument(
        "--review-outcome",
        required=True,
        choices=("agree", "accepted-claim-boundary-finding", "blocked"),
    )
    finish.set_defaults(handler=finalize)
    final = sub.add_parser("verify-final")
    final.add_argument("--run-root", required=True)
    final.add_argument("--expected-decision-digest", required=True)
    final.set_defaults(handler=verify_final)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        print(json.dumps(args.handler(args), sort_keys=True))
        return 0
    except IntegrityVeto as exc:
        print(json.dumps({"status": "UNSAFE", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 3
    except ClassificationBlock as exc:
        print(json.dumps({"status": "BLOCKED", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 4
    except (P09Error, OSError, UnicodeError, ValueError) as exc:
        print(json.dumps({"status": "ERROR_P09_RUNNER", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
