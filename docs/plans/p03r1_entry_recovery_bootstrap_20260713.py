from __future__ import annotations

"""Audit, preflight, or create the recovered Phase 03 entry exactly once."""

from dataclasses import dataclass
import json
import os
from pathlib import Path, PurePosixPath
import runpy
import stat
import sys
from typing import Any, Iterable

from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
    validate_logical_path,
)


PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
BOOTSTRAP_REF = "docs/plans/p03r1_entry_recovery_bootstrap_20260713.py"
PLAN_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-03r1-entry-bootstrap-recovery-subplan-2026-07-13.md"
)
REVIEW_REF = (
    "docs/reviews/"
    "mathdevmcp-real-document-remediation-phase-03r1-entry-recovery-plan-review-r3-result-2026-07-13.md"
)
BUDGET_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-03r1-review-budget-carry-forward-2026-07-13.json"
)
BASE_BOOTSTRAP_REF = "docs/plans/p03_entry_bootstrap_20260712.py"
BASE_PLAN_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-03-semantic-resolution-and-corpus-context-subplan-2026-07-12.md"
)
R1_REVIEW_REF = (
    "docs/reviews/"
    "mathdevmcp-real-document-remediation-phase-03-plan-review-r1-result-2026-07-12.md"
)
R1_BLOCKER_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-03-plan-review-r1-blocker-result-2026-07-12.md"
)
R2_REVIEW_REF = (
    "docs/reviews/"
    "mathdevmcp-real-document-remediation-phase-03-plan-review-r2-result-2026-07-12.md"
)
BASE_BUDGET_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-03-review-budget-authorization-2026-07-12.json"
)
CREATE_BLOCKER_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-03-entry-bootstrap-create-blocker-result-2026-07-12.md"
)

EVIDENCE_ROOT_REF = ".local/mathdevmcp/evidence/p03-20260712"
ENTRY_ROOT_REF = f"{EVIDENCE_ROOT_REF}/entry"
ENTRY_RECORD_REF = f"{ENTRY_ROOT_REF}/entry-record.json"
IMPLEMENTATION_MANIFEST_REF = f"{ENTRY_ROOT_REF}/implementation-entry-sha256.txt"
PROTECTED_MANIFEST_REF = f"{ENTRY_ROOT_REF}/protected-entry-sha256.txt"
IMMUTABLE_MANIFEST_REF = f"{ENTRY_ROOT_REF}/immutable-input-sha256.txt"
EXCLUSION_LEDGER_REF = f"{ENTRY_ROOT_REF}/scratch-exclusion-ledger.json"

EXPECTED_ENVIRONMENT = {
    "HOME": "/tmp/mathdevmcp-p03r1-entry-home",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": "/usr/bin:/bin",
    "PYTHONHASHSEED": "0",
    "PYTHONPATH": "src",
}

HISTORY_DIGESTS = {
    BASE_PLAN_REF: "b0172a6122205d9378c4393bee270116ca501616da0a939b960f2ac16213c4f4",
    BASE_BOOTSTRAP_REF: "abb04fbff5cfbf97b0b41ce28d34c1cf93dbb45243558e0df3064c39f1e9ac8b",
    R1_REVIEW_REF: "4e4c2c235f53b035ec4a5780f02165a4662630782e3f5862a524edbd4ab9cd03",
    R1_BLOCKER_REF: "0b76111e955eb6e555b9bb711ad4c876ed487ad878cbe53f62a63021d7eedf90",
    R2_REVIEW_REF: "74eecc8cca08d26a9bb35d66f3e30e3796c888c84b4cb93ea3e3b4602ed851a2",
    BASE_BUDGET_REF: "f3e0910e670e31a4d6106fdc3f69c879e7312fe9bd710611a40e6c45875ba5b0",
    CREATE_BLOCKER_REF: "30542fb098c853b8cdc5c35b9d0b60220ee3dfd2d5c78e41537624c7db3e41cd",
}

PROTECTED_EVIDENCE_TREES = (
    ".local/mathdevmcp/evidence/p00-20260711",
    ".local/mathdevmcp/evidence/p01-20260711",
    ".local/mathdevmcp/evidence/p02-20260711",
    ".local/mathdevmcp/evidence/p02r2-20260712",
    ".local/mathdevmcp/evidence/p02r3-20260712",
)
SCRATCH_ROOTS = (
    ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr01/governance/tmp",
    ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr02/governance/tmp",
    ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds/rr03/governance/tmp",
)
P02R3_RESULT_ROUNDS_REF = ".local/mathdevmcp/evidence/p02r3-20260712/result-rounds"
EXPECTED_SCRATCH_COUNTS = {
    ref: {"directory_count": 69, "regular_file_count": 151, "symlink_count": 12}
    for ref in SCRATCH_ROOTS
}
EXPECTED_SCRATCH_REGULAR_BYTES = {ref: 74331 for ref in SCRATCH_ROOTS}
EXPECTED_SCRATCH_INVENTORY_DIGESTS = {
    SCRATCH_ROOTS[0]: "b65f35e87c692b6815fe473df70737d6929c540121820bf651611fff4884b488",
    SCRATCH_ROOTS[1]: "d7c5c9c29334517be5b15ddf7b9b477a2218815daa670640b4edb4e6026f9181",
    SCRATCH_ROOTS[2]: "765bfb63f35fa06b42ba3a77af6d52884b1c2e3462895fb7d452fe857a6d3ff1",
}

ALLOWLIST_EXACT = {
    "src/mathdevmcp/document_context_graph.py",
    "src/mathdevmcp/context_evidence.py",
    "src/mathdevmcp/latex_index.py",
    "src/mathdevmcp/document_derivation_tree.py",
    "src/mathdevmcp/math_ir.py",
    "src/mathdevmcp/notation_reconciliation.py",
    "scripts/generate_p03_context_evidence.py",
    "scripts/p03_governance.py",
    "tests/p03_no_backend_guard.py",
    "tests/test_context_evidence.py",
    "tests/test_context_real_regressions.py",
    "tests/test_document_context_graph.py",
    "tests/test_document_context_resolver.py",
    "tests/test_latex_index.py",
    "tests/test_document_derivation_tree.py",
    "tests/test_document_derivation_real_regressions.py",
    "tests/test_math_ir.py",
    "tests/test_notation_reconciliation.py",
}
ALLOWLIST_PREFIXES = ("tests/fixtures/document_context_graph/",)


@dataclass(frozen=True)
class PreparedEntry:
    summary: dict[str, Any]
    payloads: dict[str, bytes]


def _base() -> dict[str, Any]:
    return runpy.run_path(BASE_BOOTSTRAP_REF, run_name="p03r1_recovery_base")


def _read(root: Path, ref: str) -> bytes:
    validate_logical_path(ref)
    raw, info = read_bytes_no_follow(root, ref)
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError(f"P03R1 artifact is not regular: {ref}")
    return raw


def _sha(root: Path, ref: str) -> str:
    return content_digest(_read(root, ref))


def _strict_object(raw: bytes, name: str) -> dict[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"{name} violates strict JSON bytes")

    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in pairs:
            if key in result:
                raise EvidenceValidationError(f"{name} contains duplicate key {key}")
            result[key] = value
        return result

    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=no_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"{name} is not strict JSON") from exc
    if type(value) is not dict or canonical_json_bytes(value) != raw:
        raise EvidenceValidationError(f"{name} is not one canonical JSON object")
    return value


def _validate_invocation(argv: list[str]) -> tuple[str, str | None]:
    if argv == ["--mode", "audit"]:
        mode, readiness = "audit", None
    elif argv == ["--mode", "preflight"]:
        mode, readiness = "preflight", None
    elif (
        len(argv) == 4
        and argv[:2] == ["--mode", "create"]
        and argv[2] == "--readiness-digest"
        and len(argv[3]) == 64
        and all(char in "0123456789abcdef" for char in argv[3])
    ):
        mode, readiness = "create", argv[3]
    else:
        raise EvidenceValidationError(
            "P03R1 bootstrap accepts exactly --mode audit|preflight or "
            "--mode create --readiness-digest <lowercase sha256>"
        )
    expected = [PYTHON, "-B", "-S", BOOTSTRAP_REF, *argv]
    if sys.orig_argv != expected:
        raise EvidenceValidationError("P03R1 bootstrap process argv is not exact")
    if dict(os.environ) != EXPECTED_ENVIRONMENT:
        raise EvidenceValidationError("P03R1 bootstrap environment is not exact")
    if sys.executable != PYTHON or not sys.flags.dont_write_bytecode or not sys.flags.no_site:
        raise EvidenceValidationError("P03R1 bootstrap runtime flags are not exact")
    return mode, readiness


def _manifest(root: Path, refs: Iterable[str]) -> bytes:
    unique = sorted(set(refs), key=lambda item: item.encode("utf-8"))
    if not unique:
        raise EvidenceValidationError("P03R1 manifest cannot be empty")
    return b"".join(f"{_sha(root, ref)}  {ref}\n".encode("utf-8") for ref in unique)


def _classify_ref(ref: str) -> str | None:
    for scratch in SCRATCH_ROOTS:
        if ref == scratch or ref.startswith(f"{scratch}/"):
            return scratch
    return None


def _is_p02r3_scratch_namespace(ref: str) -> bool:
    prefix_parts = PurePosixPath(P02R3_RESULT_ROUNDS_REF).parts
    parts = PurePosixPath(ref).parts
    return (
        len(parts) == len(prefix_parts) + 3
        and parts[: len(prefix_parts)] == prefix_parts
        and parts[-2:] == ("governance", "tmp")
    )


def _open_dir_chain(root: Path, logical_ref: str) -> int:
    validate_logical_path(logical_ref)
    current_fd = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    try:
        for part in PurePosixPath(logical_ref).parts:
            next_fd = os.open(
                part,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=current_fd,
            )
            os.close(current_fd)
            current_fd = next_fd
        return current_fd
    except Exception:
        os.close(current_fd)
        raise


def _walk_no_follow(root: Path, top_ref: str, *, skip_scratch: bool) -> tuple[set[str], list[str]]:
    files: set[str] = set()
    symlinks: list[str] = []

    def visit(directory_fd: int, directory_ref: str) -> None:
        for name in sorted(os.listdir(directory_fd), key=os.fsencode):
            ref = f"{directory_ref}/{name}"
            scratch = _classify_ref(ref)
            if skip_scratch and _is_p02r3_scratch_namespace(ref) and scratch is None:
                raise EvidenceValidationError(f"P03R1 unregistered scratch root: {ref}")
            if skip_scratch and scratch is not None:
                if ref == scratch:
                    scratch_info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
                    if not stat.S_ISDIR(scratch_info.st_mode):
                        raise EvidenceValidationError(f"P03R1 scratch root is unsafe: {ref}")
                    scratch_fd = os.open(
                        name,
                        os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                        dir_fd=directory_fd,
                    )
                    os.close(scratch_fd)
                    continue
                raise EvidenceValidationError(f"P03R1 scratch traversal escaped skip boundary: {ref}")
            info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            if stat.S_ISLNK(info.st_mode):
                symlinks.append(ref)
            elif stat.S_ISDIR(info.st_mode):
                child_fd = os.open(
                    name,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=directory_fd,
                )
                try:
                    reopened = os.fstat(child_fd)
                    if reopened.st_dev != info.st_dev or reopened.st_ino != info.st_ino:
                        raise EvidenceValidationError(f"P03R1 directory changed during scan: {ref}")
                    visit(child_fd, ref)
                finally:
                    os.close(child_fd)
            elif stat.S_ISREG(info.st_mode):
                files.add(ref)
            else:
                raise EvidenceValidationError(f"P03R1 special path in protected tree: {ref}")

    top_fd = _open_dir_chain(root, top_ref)
    try:
        visit(top_fd, top_ref)
    finally:
        os.close(top_fd)
    return files, symlinks


def _verify_scratch_registry(root: Path) -> None:
    discovered: set[str] = set()
    rounds_fd = _open_dir_chain(root, P02R3_RESULT_ROUNDS_REF)
    try:
        for round_name in sorted(os.listdir(rounds_fd), key=os.fsencode):
            round_info = os.stat(round_name, dir_fd=rounds_fd, follow_symlinks=False)
            if not stat.S_ISDIR(round_info.st_mode):
                continue
            round_fd = os.open(
                round_name,
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=rounds_fd,
            )
            try:
                if "governance" not in os.listdir(round_fd):
                    continue
                governance_info = os.stat("governance", dir_fd=round_fd, follow_symlinks=False)
                if not stat.S_ISDIR(governance_info.st_mode):
                    continue
                governance_fd = os.open(
                    "governance",
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=round_fd,
                )
                try:
                    if "tmp" in os.listdir(governance_fd):
                        discovered.add(
                            f"{P02R3_RESULT_ROUNDS_REF}/{round_name}/governance/tmp"
                        )
                finally:
                    os.close(governance_fd)
            finally:
                os.close(round_fd)
    finally:
        os.close(rounds_fd)
    if discovered != set(SCRATCH_ROOTS):
        raise EvidenceValidationError(
            "P03R1 scratch registry drift: "
            f"expected {sorted(SCRATCH_ROOTS)}, found {sorted(discovered)}"
        )


def _scratch_inventory(root: Path, scratch_ref: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    inventory: list[dict[str, Any]] = []
    types: dict[str, str] = {"": "directory"}
    directory_count = 1
    regular_file_count = 0
    symlink_count = 0
    regular_byte_count = 0

    def visit(directory_fd: int, relative_parent: str) -> None:
        nonlocal directory_count, regular_file_count, symlink_count, regular_byte_count
        for name in sorted(os.listdir(directory_fd), key=os.fsencode):
            relative = f"{relative_parent}/{name}" if relative_parent else name
            entry_info = os.stat(name, dir_fd=directory_fd, follow_symlinks=False)
            if stat.S_ISLNK(entry_info.st_mode):
                target = os.readlink(name, dir_fd=directory_fd)
                inventory.append({"path": relative, "type": "symlink", "target": target})
                types[relative] = "symlink"
                symlink_count += 1
            elif stat.S_ISDIR(entry_info.st_mode):
                inventory.append({"path": relative, "type": "directory"})
                types[relative] = "directory"
                directory_count += 1
                child_fd = os.open(
                    name,
                    os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                    dir_fd=directory_fd,
                )
                try:
                    reopened = os.fstat(child_fd)
                    if reopened.st_dev != entry_info.st_dev or reopened.st_ino != entry_info.st_ino:
                        raise EvidenceValidationError(f"P03R1 scratch directory changed: {relative}")
                    visit(child_fd, relative)
                finally:
                    os.close(child_fd)
            elif stat.S_ISREG(entry_info.st_mode):
                file_fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory_fd)
                try:
                    reopened = os.fstat(file_fd)
                    if (
                        not stat.S_ISREG(reopened.st_mode)
                        or reopened.st_dev != entry_info.st_dev
                        or reopened.st_ino != entry_info.st_ino
                    ):
                        raise EvidenceValidationError(f"P03R1 scratch file changed: {relative}")
                    chunks: list[bytes] = []
                    while True:
                        chunk = os.read(file_fd, 65536)
                        if not chunk:
                            break
                        chunks.append(chunk)
                    raw = b"".join(chunks)
                finally:
                    os.close(file_fd)
                inventory.append(
                    {
                        "path": relative,
                        "type": "regular_file",
                        "byte_count": len(raw),
                        "sha256": content_digest(raw),
                    }
                )
                types[relative] = "regular_file"
                regular_file_count += 1
                regular_byte_count += len(raw)
            else:
                raise EvidenceValidationError(f"P03R1 special path in scratch tree: {relative}")

    scratch_fd = _open_dir_chain(root, scratch_ref)
    try:
        visit(scratch_fd, "")
    finally:
        os.close(scratch_fd)
    symlink_records: list[dict[str, Any]] = []
    scratch_absolute = (root / scratch_ref).absolute()
    for item in inventory:
        if item["type"] != "symlink":
            continue
        target = Path(item["target"])
        if not target.is_absolute():
            raise EvidenceValidationError(f"P03R1 scratch symlink target is not absolute: {item['path']}")
        try:
            target_relative = target.relative_to(scratch_absolute).as_posix()
        except ValueError as exc:
            raise EvidenceValidationError(f"P03R1 scratch symlink escapes its root: {item['path']}") from exc
        if types.get(target_relative) not in {"directory", "regular_file"}:
            raise EvidenceValidationError(f"P03R1 scratch symlink target is unsafe: {item['path']}")
        symlink_records.append(
            {
                "path": item["path"],
                "target": item["target"],
                "target_relative": target_relative,
                "target_type": types[target_relative],
            }
        )
    counts = {
        "directory_count": directory_count,
        "regular_file_count": regular_file_count,
        "symlink_count": symlink_count,
    }
    if counts != EXPECTED_SCRATCH_COUNTS[scratch_ref]:
        raise EvidenceValidationError(f"P03R1 scratch count drift: {scratch_ref}")
    inventory_digest = content_digest(canonical_json_bytes(inventory))
    if (
        regular_byte_count != EXPECTED_SCRATCH_REGULAR_BYTES[scratch_ref]
        or inventory_digest != EXPECTED_SCRATCH_INVENTORY_DIGESTS[scratch_ref]
    ):
        raise EvidenceValidationError(f"P03R1 scratch byte/inventory drift: {scratch_ref}")
    item = {
        "scratch_root": scratch_ref,
        "result_round": PurePosixPath(scratch_ref).parts[-3],
        **counts,
        "regular_byte_count": regular_byte_count,
        "inventory_digest": inventory_digest,
        "symlink_records": symlink_records,
        "reason": "pytest_owned_round_local_runtime_scratch_not_formal_evidence",
        "excluded_from_protected_manifest": True,
        "non_claim": "Exclusion does not validate scratch contents or make scratch formal evidence.",
    }
    return item, inventory


def _verify_no_formal_scratch_reference(root: Path, formal_refs: Iterable[str]) -> None:
    markers: list[bytes] = []
    for scratch in SCRATCH_ROOTS:
        markers.extend(
            [
                scratch.encode("utf-8"),
                f"{scratch}/".encode("utf-8"),
                f"{(root / scratch).absolute()}".encode("utf-8"),
                f"{(root / scratch).absolute()}/".encode("utf-8"),
            ]
        )
    for ref in formal_refs:
        raw = _read(root, ref)
        if any(marker in raw for marker in markers):
            raise EvidenceValidationError(f"P03R1 formal artifact references excluded scratch: {ref}")


def _verify_history(root: Path) -> None:
    for ref, expected in HISTORY_DIGESTS.items():
        if _sha(root, ref) != expected:
            raise EvidenceValidationError(f"P03R1 history drift: {ref}")


def _verify_review(root: Path) -> str:
    raw = _read(root, REVIEW_REF)
    if len(raw) > 131072 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError("P03R1 review violates bounded UTF-8 grammar")
    lines = raw.decode("utf-8", "strict").splitlines()
    base = _base()
    required = {
        "Reviewed Phase 03R1 recovery plan SHA-256": _sha(root, PLAN_REF),
        "Reviewed Phase 03R1 recovery bootstrap SHA-256": _sha(root, BOOTSTRAP_REF),
        "Reviewed Phase 03 create blocker SHA-256": HISTORY_DIGESTS[CREATE_BLOCKER_REF],
        "Reviewed Phase 03 base plan SHA-256": HISTORY_DIGESTS[BASE_PLAN_REF],
        "Reviewed Phase 03 base bootstrap SHA-256": HISTORY_DIGESTS[BASE_BOOTSTRAP_REF],
        "Reviewed Phase 03 R2 review SHA-256": HISTORY_DIGESTS[R2_REVIEW_REF],
        "Reviewed Phase 03 base budget SHA-256": HISTORY_DIGESTS[BASE_BUDGET_REF],
        "Reviewed P02 stable decision SHA-256": base["EXPECTED_DIGESTS"][base["P02_STABLE_REF"]],
        "Reviewed P02 terminal receipt-index SHA-256": base["EXPECTED_DIGESTS"][base["P02_TERMINAL_INDEX_REF"]],
    }
    for label, digest in required.items():
        line = f"{label}: `{digest}`"
        if lines.count(line) != 1 or sum(label in item for item in lines) != 1:
            raise EvidenceValidationError(f"P03R1 review binding is not unique: {label}")
    verdicts = [line for line in lines if line.startswith("VERDICT:")]
    nonempty = [line for line in lines if line]
    if verdicts != ["VERDICT: AGREE"] or not nonempty or nonempty[-1] != "VERDICT: AGREE":
        raise EvidenceValidationError("P03R1 review is not uniquely agreeing")
    return content_digest(raw)


def _verify_budget(root: Path, review_sha256: str) -> tuple[str, dict[str, Any]]:
    raw = _read(root, BUDGET_REF)
    value = _strict_object(raw, "P03R1 review-budget carry-forward")
    expected_keys = {
        "schema_version",
        "phase",
        "recovery",
        "date",
        "authority",
        "source_budget_ref",
        "source_budget_sha256",
        "source_plan_review_ref",
        "source_plan_review_sha256",
        "entry_recovery_plan_ref",
        "entry_recovery_plan_sha256",
        "entry_recovery_review_ref",
        "entry_recovery_review_sha256",
        "result_review_rounds_reserved",
        "final_seal_audit_rounds_reserved",
        "non_claim",
    }
    if (
        set(value) != expected_keys
        or value["schema_version"] != "p03r1_review_budget_carry_forward@1"
        or value["phase"] != "P03"
        or value["recovery"] != "P03R1"
        or value["date"] != "2026-07-13"
        or value["authority"] != "human_user"
        or value["source_budget_ref"] != BASE_BUDGET_REF
        or value["source_budget_sha256"] != HISTORY_DIGESTS[BASE_BUDGET_REF]
        or value["source_plan_review_ref"] != R2_REVIEW_REF
        or value["source_plan_review_sha256"] != HISTORY_DIGESTS[R2_REVIEW_REF]
        or value["entry_recovery_plan_ref"] != PLAN_REF
        or value["entry_recovery_plan_sha256"] != _sha(root, PLAN_REF)
        or value["entry_recovery_review_ref"] != REVIEW_REF
        or value["entry_recovery_review_sha256"] != review_sha256
        or value["result_review_rounds_reserved"] != 1
        or value["final_seal_audit_rounds_reserved"] != 1
        or value["non_claim"]
        != "Carry-forward preserves unused review authority only; it is not a technical verdict or signature."
    ):
        raise EvidenceValidationError("P03R1 review-budget carry-forward mismatch")
    return content_digest(raw), value


def _implementation_refs(root: Path) -> set[str]:
    refs: set[str] = set()
    for top_name in ("src", "tests", "scripts"):
        found, symlinks = _walk_no_follow(root, top_name, skip_scratch=False)
        if symlinks:
            raise EvidenceValidationError(f"P03R1 symlink in implementation tree: {symlinks[0]}")
        refs.update(
            ref
            for ref in found
            if "__pycache__" not in PurePosixPath(ref).parts
            and PurePosixPath(ref).suffix not in {".pyc", ".pyo"}
        )
    return refs


def _dirty_refs(root: Path) -> set[str]:
    return set(_base()["_dirty_refs"](root))


def _prepare(root: Path, *, require_authority: bool) -> PreparedEntry:
    if (root / EVIDENCE_ROOT_REF).exists() or (root / EVIDENCE_ROOT_REF).is_symlink():
        raise EvidenceValidationError("P03R1 requires the original Phase 03 evidence root to remain absent")
    _verify_history(root)
    base = _base()
    base_preflight = base["_preflight"](root)
    predecessor = base["_verify_p02"](root)
    runtime = base_preflight["runtime_measurement"]
    if (
        tuple(base_preflight["p03_pass_actions"]) != base["P03_PASS_ACTIONS"]
        or tuple(base_preflight["p03_failure_suffix_actions"]) != base["P03_FAILURE_SUFFIX_ACTIONS"]
        or set(base["ALLOWLIST_EXACT"]) != ALLOWLIST_EXACT
        or tuple(base["ALLOWLIST_PREFIXES"]) != ALLOWLIST_PREFIXES
    ):
        raise EvidenceValidationError("P03R1 base Phase 03 registry drift")

    _verify_scratch_registry(root)
    scratch_items: list[dict[str, Any]] = []
    scratch_inventory_digests: dict[str, str] = {}
    for scratch in SCRATCH_ROOTS:
        item, inventory = _scratch_inventory(root, scratch)
        scratch_items.append(item)
        scratch_inventory_digests[scratch] = content_digest(canonical_json_bytes(inventory))

    protected_evidence_refs: set[str] = set()
    for tree in PROTECTED_EVIDENCE_TREES:
        refs, symlinks = _walk_no_follow(root, tree, skip_scratch=tree.endswith("p02r3-20260712"))
        if symlinks:
            raise EvidenceValidationError(f"P03R1 symlink outside exact scratch roots: {symlinks[0]}")
        protected_evidence_refs.update(refs)
    _verify_no_formal_scratch_reference(root, protected_evidence_refs)

    implementation_refs = _implementation_refs(root)
    implementation = _manifest(root, implementation_refs)
    output_refs = {
        IMPLEMENTATION_MANIFEST_REF,
        PROTECTED_MANIFEST_REF,
        IMMUTABLE_MANIFEST_REF,
        EXCLUSION_LEDGER_REF,
        ENTRY_RECORD_REF,
    }
    protected_refs = {
        ref
        for ref in _dirty_refs(root) - ALLOWLIST_EXACT - output_refs
        if not any(ref.startswith(prefix) for prefix in ALLOWLIST_PREFIXES)
    }
    protected_refs.update(protected_evidence_refs)
    protected_refs.update(set(HISTORY_DIGESTS) | {PLAN_REF, BOOTSTRAP_REF})

    review_sha256: str | None = None
    budget_sha256: str | None = None
    if require_authority:
        review_sha256 = _verify_review(root)
        budget_sha256, _budget = _verify_budget(root, review_sha256)
        protected_refs.update({REVIEW_REF, BUDGET_REF})

    protected = _manifest(root, protected_refs)
    immutable_refs = set(base["EXPECTED_DIGESTS"]) | set(HISTORY_DIGESTS) | {PLAN_REF, BOOTSTRAP_REF}
    if require_authority:
        immutable_refs.update({REVIEW_REF, BUDGET_REF})
    immutable = _manifest(root, immutable_refs)
    exclusion_record = {
        "schema_version": "p03r1_scratch_exclusion_ledger@1",
        "phase": "P03",
        "recovery": "P03R1",
        "date": "2026-07-13",
        "policy": "exclude_only_exact_p02r3_round_local_governance_tmp_roots",
        "scratch_roots": scratch_items,
        "scratch_root_count": 3,
        "total_regular_file_count": sum(item["regular_file_count"] for item in scratch_items),
        "total_directory_count": sum(item["directory_count"] for item in scratch_items),
        "total_symlink_count": sum(item["symlink_count"] for item in scratch_items),
        "formal_reference_count": 0,
        "formal_protected_file_count": len(protected_evidence_refs),
        "non_claims": [
            "excluded_scratch_is_not_formal_evidence",
            "scratch_exclusion_does_not_validate_test_outputs",
            "scratch_exclusion_does_not_weaken_symlink_veto_outside_exact_roots",
        ],
    }
    exclusion = canonical_json_bytes(exclusion_record)

    preparation_projection = {
        "schema_version": "p03r1_entry_preparation@1",
        "phase": "P03",
        "recovery": "P03R1",
        "date": "2026-07-13",
        "authority_bound": require_authority,
        "review_sha256": review_sha256,
        "budget_sha256": budget_sha256,
        "implementation_manifest_sha256": content_digest(implementation),
        "protected_manifest_sha256": content_digest(protected),
        "immutable_manifest_sha256": content_digest(immutable),
        "scratch_exclusion_ledger_sha256": content_digest(exclusion),
        "scratch_inventory_digests": scratch_inventory_digests,
        "implementation_ref_count": len(implementation_refs),
        "protected_ref_count": len(protected_refs),
        "immutable_ref_count": len(immutable_refs),
        "runtime_measurement": runtime,
        "p02_ordered_obligation_bindings": predecessor["obligation_bindings"],
        "p02_obligation_state_counts": predecessor["state_counts"],
        "p02_adapter_eligible_count": predecessor["eligible_count"],
        "entry_root_absent": True,
    }
    preparation_digest = content_digest(canonical_json_bytes(preparation_projection))
    record = {
        "schema_version": "p03_entry_record@2",
        "phase": "P03",
        "recovery": "P03R1",
        "date": "2026-07-13",
        "reviewed_plan_ref": BASE_PLAN_REF,
        "reviewed_plan_sha256": HISTORY_DIGESTS[BASE_PLAN_REF],
        "entry_recovery_plan_ref": PLAN_REF,
        "entry_recovery_plan_sha256": _sha(root, PLAN_REF),
        "entry_recovery_bootstrap_ref": BOOTSTRAP_REF,
        "entry_recovery_bootstrap_sha256": _sha(root, BOOTSTRAP_REF),
        "agreeing_entry_recovery_review_ref": REVIEW_REF if require_authority else None,
        "agreeing_entry_recovery_review_sha256": review_sha256,
        "review_budget_carry_forward_ref": BUDGET_REF if require_authority else None,
        "review_budget_carry_forward_sha256": budget_sha256,
        "failed_entry_bootstrap_ref": BASE_BOOTSTRAP_REF,
        "failed_entry_bootstrap_sha256": HISTORY_DIGESTS[BASE_BOOTSTRAP_REF],
        "failed_create_blocker_ref": CREATE_BLOCKER_REF,
        "failed_create_blocker_sha256": HISTORY_DIGESTS[CREATE_BLOCKER_REF],
        "master_plan_ref": base["MASTER_REF"],
        "master_plan_sha256": base["EXPECTED_DIGESTS"][base["MASTER_REF"]],
        "p02_close_ref": base["P02_CLOSE_REF"],
        "p02_close_sha256": base["EXPECTED_DIGESTS"][base["P02_CLOSE_REF"]],
        "p02_stable_decision_ref": base["P02_STABLE_REF"],
        "p02_stable_decision_sha256": base["EXPECTED_DIGESTS"][base["P02_STABLE_REF"]],
        "p02_extraction_bundle_index_ref": base["P02_BUNDLE_INDEX_REF"],
        "p02_extraction_bundle_index_sha256": base["EXPECTED_DIGESTS"][base["P02_BUNDLE_INDEX_REF"]],
        "p02_obligations_ref": base["P02_OBLIGATIONS_REF"],
        "p02_obligations_sha256": base["EXPECTED_DIGESTS"][base["P02_OBLIGATIONS_REF"]],
        "p02_terminal_receipt_index_ref": base["P02_TERMINAL_INDEX_REF"],
        "p02_terminal_receipt_index_sha256": base["EXPECTED_DIGESTS"][base["P02_TERMINAL_INDEX_REF"]],
        "p02_extraction_bundle_semantic_digest": "98dfaf84155723500dd2065cad4837ddea93a688273bb427b946a68172498395",
        "p02_ordered_obligation_bindings": predecessor["obligation_bindings"],
        "p02_obligation_state_counts": predecessor["state_counts"],
        "p02_adapter_eligible_count": predecessor["eligible_count"],
        "p03_pass_actions": list(base["P03_PASS_ACTIONS"]),
        "p03_failure_suffix_actions": list(base["P03_FAILURE_SUFFIX_ACTIONS"]),
        "runtime_measurement": runtime,
        "implementation_entry_manifest_ref": IMPLEMENTATION_MANIFEST_REF,
        "implementation_entry_manifest_sha256": content_digest(implementation),
        "protected_entry_manifest_ref": PROTECTED_MANIFEST_REF,
        "protected_entry_manifest_sha256": content_digest(protected),
        "immutable_input_manifest_ref": IMMUTABLE_MANIFEST_REF,
        "immutable_input_manifest_sha256": content_digest(immutable),
        "scratch_exclusion_ledger_ref": EXCLUSION_LEDGER_REF,
        "scratch_exclusion_ledger_sha256": content_digest(exclusion),
        "entry_preparation_digest": preparation_digest,
        "create_readiness_schema_version": "p03r1_entry_readiness@2",
        "implementation_allowlist_exact": sorted(ALLOWLIST_EXACT, key=lambda item: item.encode("utf-8")),
        "implementation_allowlist_prefixes": list(ALLOWLIST_PREFIXES),
        "device_mode": "cpu_only_no_gpu_requested",
        "publication_mode": "disabled",
    }
    payloads = {
        IMPLEMENTATION_MANIFEST_REF: implementation,
        PROTECTED_MANIFEST_REF: protected,
        IMMUTABLE_MANIFEST_REF: immutable,
        EXCLUSION_LEDGER_REF: exclusion,
        ENTRY_RECORD_REF: canonical_json_bytes(record),
    }
    readiness_projection = {
        **preparation_projection,
        "schema_version": "p03r1_entry_readiness@2",
        "entry_preparation_digest": preparation_digest,
        "entry_record_sha256": content_digest(payloads[ENTRY_RECORD_REF]),
    }
    readiness_digest = content_digest(canonical_json_bytes(readiness_projection))
    summary = {
        **readiness_projection,
        "status": "READY_NO_WRITE" if require_authority else "AUDIT_PASS_NO_WRITE",
        "readiness_digest": readiness_digest,
        "output_refs": sorted(payloads, key=lambda item: item.encode("utf-8")),
    }
    return PreparedEntry(summary=summary, payloads=payloads)


def _mkdir_entry(root: Path) -> None:
    parent_ref = ".local/mathdevmcp/evidence"
    parent_fd = _open_dir_chain(root, parent_ref)
    try:
        os.mkdir("p03-20260712", mode=0o700, dir_fd=parent_fd)
        phase_fd = os.open(
            "p03-20260712",
            os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
            dir_fd=parent_fd,
        )
        try:
            os.mkdir("entry", mode=0o700, dir_fd=phase_fd)
        finally:
            os.close(phase_fd)
    finally:
        os.close(parent_fd)


def _allocate(root: Path, prepared: PreparedEntry, expected_readiness: str) -> dict[str, Any]:
    if prepared.summary["readiness_digest"] != expected_readiness:
        raise EvidenceValidationError("P03R1 readiness digest mismatch")
    if prepared.summary["status"] != "READY_NO_WRITE":
        raise EvidenceValidationError("P03R1 create lacks authority-bound readiness")
    order = (
        IMPLEMENTATION_MANIFEST_REF,
        PROTECTED_MANIFEST_REF,
        IMMUTABLE_MANIFEST_REF,
        EXCLUSION_LEDGER_REF,
        ENTRY_RECORD_REF,
    )
    if set(prepared.payloads) != set(order):
        raise EvidenceValidationError("P03R1 prepared payload set mismatch")
    payload_digest_fields = {
        IMPLEMENTATION_MANIFEST_REF: "implementation_manifest_sha256",
        PROTECTED_MANIFEST_REF: "protected_manifest_sha256",
        IMMUTABLE_MANIFEST_REF: "immutable_manifest_sha256",
        EXCLUSION_LEDGER_REF: "scratch_exclusion_ledger_sha256",
        ENTRY_RECORD_REF: "entry_record_sha256",
    }
    for ref, field in payload_digest_fields.items():
        if content_digest(prepared.payloads[ref]) != prepared.summary.get(field):
            raise EvidenceValidationError(f"P03R1 prepared payload digest mismatch: {ref}")
    readiness_projection = {
        key: value
        for key, value in prepared.summary.items()
        if key not in {"status", "readiness_digest", "output_refs"}
    }
    if content_digest(canonical_json_bytes(readiness_projection)) != expected_readiness:
        raise EvidenceValidationError("P03R1 prepared readiness projection mismatch")
    _mkdir_entry(root)
    for ref in order:
        atomic_write_bytes_no_replace(root, ref, prepared.payloads[ref])
    reopened = {ref: _read(root, ref) for ref in order}
    if reopened != prepared.payloads:
        raise EvidenceValidationError("P03R1 entry reopen mismatch")
    phase = root / EVIDENCE_ROOT_REF
    entry = root / ENTRY_ROOT_REF
    if (
        phase.is_symlink()
        or entry.is_symlink()
        or {item.name for item in phase.iterdir()} != {"entry"}
        or {item.name for item in entry.iterdir()} != {PurePosixPath(ref).name for ref in order}
        or any(item.is_symlink() or not item.is_file() for item in entry.iterdir())
    ):
        raise EvidenceValidationError("P03R1 entry tree shape mismatch")
    return {
        **prepared.summary,
        "status": "ENTRY_CREATED",
        "entry_record_ref": ENTRY_RECORD_REF,
        "entry_record_sha256": content_digest(reopened[ENTRY_RECORD_REF]),
    }


def main() -> int:
    mode, expected_readiness = _validate_invocation(sys.argv[1:])
    root = Path.cwd().absolute()
    if not (root / ".git").is_dir() or not (root / "src/mathdevmcp").is_dir():
        raise EvidenceValidationError("P03R1 bootstrap must run from the workspace root")
    prepared = _prepare(root, require_authority=mode in {"preflight", "create"})
    result = (
        _allocate(root, prepared, expected_readiness or "")
        if mode == "create"
        else prepared.summary
    )
    sys.stdout.buffer.write(canonical_json_bytes(result) + b"\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        sys.stderr.buffer.write(
            canonical_json_bytes({"status": "ERROR", "error": f"{type(exc).__name__}: {exc}"}) + b"\n"
        )
        raise SystemExit(2)
