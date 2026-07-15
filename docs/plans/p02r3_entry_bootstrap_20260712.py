from __future__ import annotations

"""Create the reviewed Phase 02R3 timeout-recovery entry snapshot once."""

from copy import deepcopy
import json
import os
from pathlib import Path
import re
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
    strict_load_canonical_json,
    validate_logical_path,
    verify_receipt_index,
)


PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
BOOTSTRAP_REF = "docs/plans/p02r3_entry_bootstrap_20260712.py"
PLAN_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-02r3-timeout-policy-recovery-subplan-2026-07-12.md"
)
ORACLE_REF = (
    "docs/plans/"
    "mathdevmcp-real-document-remediation-phase-02r3-timeout-policy-recovery-oracle-2026-07-12.json"
)
R2_BOOTSTRAP_REF = "docs/plans/p02r2_entry_bootstrap_20260712.py"
R2_EVIDENCE_ROOT_REF = ".local/mathdevmcp/evidence/p02r2-20260712"
EVIDENCE_ROOT_REF = ".local/mathdevmcp/evidence/p02r3-20260712"
ENTRY_ROOT_REF = f"{EVIDENCE_ROOT_REF}/entry"
ENTRY_RECORD_REF = f"{ENTRY_ROOT_REF}/entry-record.json"
IMPLEMENTATION_MANIFEST_REF = f"{ENTRY_ROOT_REF}/implementation-entry-sha256.txt"
PROTECTED_MANIFEST_REF = f"{ENTRY_ROOT_REF}/protected-entry-sha256.txt"
IMMUTABLE_MANIFEST_REF = f"{ENTRY_ROOT_REF}/immutable-input-sha256.txt"
R14_REVIEW_REF = (
    "docs/reviews/"
    "mathdevmcp-real-document-remediation-phase-02r3-plan-review-r14-result-2026-07-12.md"
)
R14_BUNDLE_REF = (
    "docs/reviews/"
    "mathdevmcp-real-document-remediation-phase-02r3-plan-review-r14-bundle-2026-07-12.md"
)
R14_REVIEW_SHA256 = "604f0aae23065b2257a71eb7291770f69bb7cd9ed7486dccb97e8430fd7579d0"
REVIEW_REF = (
    "docs/reviews/"
    "mathdevmcp-real-document-remediation-phase-02r3-plan-review-r15-result-2026-07-12.md"
)
REVIEW_BUNDLE_REF = (
    "docs/reviews/"
    "mathdevmcp-real-document-remediation-phase-02r3-plan-review-r15-bundle-2026-07-12.md"
)
EXPECTED_ENVIRONMENT = {
    "HOME": "/tmp/mathdevmcp-p02r3-entry-home",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
    "PATH": "/usr/bin:/bin",
    "PYTHONHASHSEED": "0",
    "PYTHONPATH": "src",
}
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
P02R3_REVIEW_ARTIFACT_RE = re.compile(
    r"mathdevmcp-real-document-remediation-phase-02r3-plan-review-r\d+-(?:bundle|result)-2026-07-12\.md"
)
R2_ENTRY_FILENAMES = {
    "entry-record.json",
    "implementation-entry-sha256.txt",
    "protected-entry-sha256.txt",
    "immutable-input-sha256.txt",
}


def _read(root: Path, ref: str) -> bytes:
    validate_logical_path(ref)
    raw, info = read_bytes_no_follow(root, ref)
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError(f"artifact is not regular: {ref}")
    return raw


def _sha(root: Path, ref: str) -> str:
    return content_digest(_read(root, ref))


def _open_directory_chain(root: Path, ref: str) -> int:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    directory_fd = os.open(root, flags)
    try:
        for component in Path(ref).parts:
            next_fd = os.open(component, flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        return directory_fd
    except Exception:
        os.close(directory_fd)
        raise


def _verify_r2_phase_root(root: Path) -> None:
    try:
        phase_fd = _open_directory_chain(root, R2_EVIDENCE_ROOT_REF)
        try:
            if set(os.listdir(phase_fd)) != {"entry"}:
                raise EvidenceValidationError("P02R2 phase root is not exactly entry-only")
            entry_info = os.stat("entry", dir_fd=phase_fd, follow_symlinks=False)
            if not stat.S_ISDIR(entry_info.st_mode):
                raise EvidenceValidationError("P02R2 entry child is not a no-follow directory")
            entry_fd = os.open(
                "entry",
                os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW,
                dir_fd=phase_fd,
            )
            try:
                if set(os.listdir(entry_fd)) != R2_ENTRY_FILENAMES:
                    raise EvidenceValidationError("P02R2 entry tree is not the exact four-file tree")
                for name in R2_ENTRY_FILENAMES:
                    info = os.stat(name, dir_fd=entry_fd, follow_symlinks=False)
                    if not stat.S_ISREG(info.st_mode):
                        raise EvidenceValidationError(f"P02R2 entry artifact is not regular: {name}")
            finally:
                os.close(entry_fd)
        finally:
            os.close(phase_fd)
    except OSError as exc:
        raise EvidenceValidationError("P02R2 phase root failed no-follow validation") from exc


def _strict_json(raw: bytes, name: str) -> dict[str, Any]:
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
    if type(value) is not dict:
        raise EvidenceValidationError(f"{name} must be an object")
    return value


def _validate_invocation(argv: list[str]) -> None:
    expected = [PYTHON, "-B", "-S", BOOTSTRAP_REF, *argv]
    if sys.orig_argv != expected:
        raise EvidenceValidationError("P02R3 bootstrap process argv is not exact")
    if dict(os.environ) != EXPECTED_ENVIRONMENT:
        raise EvidenceValidationError("P02R3 bootstrap environment is not exact")
    if sys.executable != PYTHON or not sys.flags.dont_write_bytecode or not sys.flags.no_site:
        raise EvidenceValidationError("P02R3 bootstrap runtime flags are not exact")


def _pointer_parent(value: Any, pointer: str) -> tuple[dict[str, Any], str]:
    if not pointer.startswith("/"):
        raise EvidenceValidationError("P02R3 patch path is not absolute")
    parts = [item.replace("~1", "/").replace("~0", "~") for item in pointer[1:].split("/")]
    current = value
    for part in parts[:-1]:
        if type(current) is not dict or part not in current:
            raise EvidenceValidationError(f"P02R3 patch path does not resolve: {pointer}")
        current = current[part]
    if type(current) is not dict or parts[-1] not in current:
        raise EvidenceValidationError(f"P02R3 patch path does not resolve: {pointer}")
    return current, parts[-1]


def _verify_bindings(root: Path, bindings: dict[str, Any]) -> None:
    if type(bindings) is not dict or not bindings:
        raise EvidenceValidationError("P02R3 base bindings are absent")
    for key, value in bindings.items():
        if key.endswith("_ref"):
            validate_logical_path(value, name=key)
            digest_key = key.removesuffix("_ref") + "_sha256"
            if bindings.get(digest_key) != _sha(root, value):
                raise EvidenceValidationError(f"P02R3 frozen binding drift: {key}")
        elif key.endswith("_sha256") and (type(value) is not str or SHA_RE.fullmatch(value) is None):
            raise EvidenceValidationError(f"P02R3 digest is invalid: {key}")


def _load_r2_effective(root: Path, bindings: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    r2_raw = _read(root, bindings["p02r2_oracle_ref"])
    r2_oracle = _strict_json(r2_raw, "P02R2 recovery oracle")
    r2_library = runpy.run_path(str(root / R2_BOOTSTRAP_REF), run_name="p02r2_bootstrap_library")
    base = r2_library["_validate_recovery_oracle"](root, r2_oracle)
    effective = deepcopy(base)
    for patch in r2_oracle["profile_patch"]:
        parent, key = _pointer_parent(effective, patch["path"])
        if parent[key] != patch["expected_base_value"]:
            raise EvidenceValidationError(f"P02R2 baseline reconstruction drift: {patch['path']}")
        parent[key] = deepcopy(patch["replacement"])
    effective["governance_action_profile"]["entry_snapshot_schema"] = deepcopy(r2_oracle["entry_schema"])
    effective["governance_action_profile"]["entry_bootstrap_profile"] = deepcopy(
        r2_oracle["entry_bootstrap_profile"]
    )
    effective["parser_capability_contract"] = deepcopy(r2_oracle["parser_capability_contract"])
    return effective, r2_oracle


def _validate_oracle(root: Path, oracle: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    exact_top = {
        "schema_version",
        "phase",
        "revision",
        "date",
        "base_bindings",
        "recovery_refs",
        "review_contract",
        "entry_schema",
        "entry_bootstrap_profile",
        "profile_patch",
        "timeout_default_audit",
        "parser_veto_partition",
        "downstream_binding_contract",
        "namespace_rule",
        "effective_profile_rule",
        "unchanged_contract",
    }
    if (
        set(oracle) != exact_top
        or oracle["schema_version"] != "p02r3_timeout_recovery_oracle@1"
        or oracle["phase"] != "P02"
        or oracle["revision"] != "P02R3"
    ):
        raise EvidenceValidationError("P02R3 oracle metadata/schema mismatch")
    bindings = oracle["base_bindings"]
    _verify_bindings(root, bindings)
    expected_binding_refs = {
        "p02r2_plan_ref",
        "p02r2_oracle_ref",
        "p02r2_bootstrap_ref",
        "p02r2_agreeing_review_ref",
        "p02r2_entry_ref",
        "timeout_blocker_ref",
        "timeout_adjudication_ref",
        "materialized_oracle_ref",
        "timeout_diagnostic_log_ref",
        "timeout_diagnostic_xml_ref",
    }
    if {key for key in bindings if key.endswith("_ref")} != expected_binding_refs:
        raise EvidenceValidationError("P02R3 base binding registry mismatch")

    refs = oracle["recovery_refs"]
    expected_refs = {
        "recovery_plan_ref": PLAN_REF,
        "recovery_oracle_ref": ORACLE_REF,
        "entry_bootstrap_ref": BOOTSTRAP_REF,
        "evidence_root_ref": EVIDENCE_ROOT_REF,
        "entry_root_ref": ENTRY_ROOT_REF,
        "entry_record_ref": ENTRY_RECORD_REF,
        "implementation_entry_manifest_ref": IMPLEMENTATION_MANIFEST_REF,
        "protected_entry_manifest_ref": PROTECTED_MANIFEST_REF,
        "immutable_input_manifest_ref": IMMUTABLE_MANIFEST_REF,
        "stable_decision_ref": f"{EVIDENCE_ROOT_REF}/phase-results/P02-decision.json",
    }
    if refs != expected_refs:
        raise EvidenceValidationError("P02R3 recovery refs mismatch")
    entry = oracle["entry_schema"]
    if (
        entry.get("schema_version") != "p02r3_entry_record@1"
        or len(entry.get("exact_keys", [])) != 33
        or len(set(entry["exact_keys"])) != 33
        or entry.get("write_order")
        != [IMPLEMENTATION_MANIFEST_REF, PROTECTED_MANIFEST_REF, IMMUTABLE_MANIFEST_REF, ENTRY_RECORD_REF]
    ):
        raise EvidenceValidationError("P02R3 entry schema mismatch")
    bootstrap = oracle["entry_bootstrap_profile"]
    expected_argv = [
        "/usr/bin/env",
        "-i",
        *(f"{key}={value}" for key, value in EXPECTED_ENVIRONMENT.items()),
        PYTHON,
        "-B",
        "-S",
        BOOTSTRAP_REF,
        "--agreeing-plan-review-ref",
        REVIEW_REF,
    ]
    if (
        bootstrap.get("source_ref") != BOOTSTRAP_REF
        or bootstrap.get("python") != PYTHON
        or bootstrap.get("environment") != EXPECTED_ENVIRONMENT
        or bootstrap.get("external_argv_template") != expected_argv
    ):
        raise EvidenceValidationError("P02R3 bootstrap profile mismatch")
    review = oracle["review_contract"]
    if type(review) is not dict:
        raise EvidenceValidationError("P02R3 review contract must be an object")
    history = review.get("review_history")
    history_keys = {
        "round",
        "result_ref",
        "result_sha256",
        "verdict",
        "reviewed_p02r3_plan_sha256",
        "reviewed_p02r3_oracle_sha256",
        "reviewed_p02r3_bootstrap_sha256",
        "reviewed_p02r2_plan_sha256",
        "reviewed_p02r2_oracle_sha256",
        "reviewed_p02r2_entry_sha256",
        "reviewed_timeout_blocker_sha256",
        "reviewed_timeout_adjudication_sha256",
    }
    if (
        set(review)
        != {
            "review_round",
            "result_ref",
            "bundle_ref",
            "review_history",
            "required_binding_labels",
            "verdict_enum",
            "sequence_rule",
            "budget_boundary",
        }
        or review.get("review_round") != 15
        or review.get("result_ref") != REVIEW_REF
        or review.get("bundle_ref") != REVIEW_BUNDLE_REF
        or review.get("verdict_enum") != ["AGREE", "REVISE"]
        or len(review.get("required_binding_labels", [])) != 9
        or type(history) is not list
        or len(history) != 1
        or type(history[0]) is not dict
        or set(history[0]) != history_keys
        or history[0]["round"] != 14
        or history[0]["result_ref"] != R14_REVIEW_REF
        or history[0]["result_sha256"] != R14_REVIEW_SHA256
        or history[0]["verdict"] != "REVISE"
    ):
        raise EvidenceValidationError("P02R3 review contract mismatch")
    r14 = history[0]
    if _sha(root, R14_REVIEW_REF) != R14_REVIEW_SHA256:
        raise EvidenceValidationError("P02R3 R14 review history drift")
    expected_r14_bindings = {
        "reviewed_p02r3_plan_sha256": "3867c8f93ee4c9f62009944c2c5f9147af99972bf5f6bdfa08f2ad1c70ed4b79",
        "reviewed_p02r3_oracle_sha256": "8ac9e7b2a0f561545f5ab3b7aeacdd66faae3bf07f4024e7d2358e6e891ef3de",
        "reviewed_p02r3_bootstrap_sha256": "8e1f9d126a758601027af69f64d7568f68f09572930514063cb47e15b926bee4",
        "reviewed_p02r2_plan_sha256": bindings["p02r2_plan_sha256"],
        "reviewed_p02r2_oracle_sha256": bindings["p02r2_oracle_sha256"],
        "reviewed_p02r2_entry_sha256": bindings["p02r2_entry_sha256"],
        "reviewed_timeout_blocker_sha256": bindings["timeout_blocker_sha256"],
        "reviewed_timeout_adjudication_sha256": bindings["timeout_adjudication_sha256"],
    }
    if any(r14[key] != value for key, value in expected_r14_bindings.items()):
        raise EvidenceValidationError("P02R3 R14 reviewed binding history mismatch")

    effective, r2_oracle = _load_r2_effective(root, bindings)
    patches = oracle["profile_patch"]
    paths = [item.get("path") for item in patches]
    if len(patches) != 11 or len(paths) != len(set(paths)):
        raise EvidenceValidationError("P02R3 patch registry mismatch")
    for item in patches:
        if type(item) is not dict or set(item) != {"path", "expected_base_value", "replacement"}:
            raise EvidenceValidationError("P02R3 patch schema mismatch")
        parent, key = _pointer_parent(effective, item["path"])
        if parent[key] != item["expected_base_value"]:
            raise EvidenceValidationError(f"P02R3 patch baseline drift: {item['path']}")
        parent[key] = deepcopy(item["replacement"])
    executables = effective["parser_fidelity_profile"]["executables"]
    if (
        set(executables) != {"latexml", "pandoc"}
        or set(executables["latexml"])
        != {"path", "measured_version", "version_argv", "fidelity_argv_template", "version_timeout_seconds", "source_timeout_seconds"}
        or set(executables["pandoc"])
        != {"path", "measured_version", "version_argv", "fidelity_argv_template", "version_timeout_seconds", "source_timeout_seconds"}
        or executables["latexml"]["version_timeout_seconds"] != 60
        or executables["latexml"]["source_timeout_seconds"] != 180
        or executables["pandoc"]["version_timeout_seconds"] != 30
        or executables["pandoc"]["source_timeout_seconds"] != 30
    ):
        raise EvidenceValidationError("P02R3 timeout patch did not close")
    partition = oracle["parser_veto_partition"]
    statuses = set(r2_oracle["parser_capability_contract"]["capability_status_enum"])
    evidence = partition.get("evidence_integrity_statuses")
    limitations = partition.get("limitation_only_statuses")
    if (
        evidence != ["source_mutated", "invocation_mismatch", "missing_artifact", "version_mismatch"]
        or limitations != ["timed_out", "nonzero_exit", "malformed_output", "valid_not_source_mappable"]
        or set(evidence) & set(limitations)
        or set(evidence) | set(limitations) | {partition.get("candidate_status")} != statuses
    ):
        raise EvidenceValidationError("P02R3 parser-veto partition mismatch")
    audit = oracle["timeout_default_audit"]
    if (
        audit.get("rejected_source_baseline_seconds") != 60
        or audit.get("latexml_version_timeout_seconds") != 60
        or audit.get("latexml_source_timeout_seconds") != 180
        or audit.get("pandoc_version_timeout_seconds") != 30
        or audit.get("pandoc_source_timeout_seconds") != 30
        or audit.get("formal_observed_wall_time_ns") != 60084494781
        or audit.get("diagnostic_time_is_independent_wall_clock") is not False
        or audit.get("reported_margin_milliseconds") != 81760
    ):
        raise EvidenceValidationError("P02R3 timeout default audit mismatch")
    return effective, r2_oracle


def _verify_r2_entry(root: Path, oracle: dict[str, Any], r2_effective: dict[str, Any]) -> dict[str, Any]:
    _verify_r2_phase_root(root)
    bindings = oracle["base_bindings"]
    ref = bindings["p02r2_entry_ref"]
    raw = _read(root, ref)
    if content_digest(raw) != bindings["p02r2_entry_sha256"]:
        raise EvidenceValidationError("P02R2 entry digest drift")
    record = _strict_json(raw, "P02R2 entry record")
    schema = r2_effective["governance_action_profile"]["entry_snapshot_schema"]
    if set(record) != set(schema["exact_keys"]) or record["schema_version"] != schema["schema_version"]:
        raise EvidenceValidationError("P02R2 entry schema drift")
    entry_root = root / Path(ref).parent
    items = list(entry_root.iterdir())
    if {item.name for item in items} != R2_ENTRY_FILENAMES or any(
        item.is_symlink() or not item.is_file() for item in items
    ):
        raise EvidenceValidationError("P02R2 entry tree drift")
    for ref_key, sha_key in (
        ("implementation_entry_manifest_ref", "implementation_entry_manifest_sha256"),
        ("protected_entry_manifest_ref", "protected_entry_manifest_sha256"),
        ("immutable_input_manifest_ref", "immutable_input_manifest_sha256"),
    ):
        if _sha(root, record[ref_key]) != record[sha_key]:
            raise EvidenceValidationError(f"P02R2 entry artifact drift: {ref_key}")
    return record


def _verify_manifest_current(root: Path, raw: bytes, base_library: dict[str, Any]) -> None:
    for line, ref in zip(raw.splitlines(), base_library["_manifest_refs_from_bytes"](raw), strict=True):
        if _sha(root, ref) != line[:64].decode("ascii"):
            raise EvidenceValidationError(f"protected predecessor drift: {ref}")


def _verify_review(root: Path, oracle: dict[str, Any], review_ref: str) -> str:
    if review_ref != REVIEW_REF:
        raise EvidenceValidationError("P02R3 agreeing review ref is not R15")
    review_artifacts = {
        path.name
        for path in (root / "docs/reviews").iterdir()
        if path.is_file() and P02R3_REVIEW_ARTIFACT_RE.fullmatch(path.name)
    }
    if review_artifacts != {
        Path(R14_BUNDLE_REF).name,
        Path(R14_REVIEW_REF).name,
        Path(REVIEW_BUNDLE_REF).name,
        Path(REVIEW_REF).name,
    }:
        raise EvidenceValidationError("P02R3 plan-review artifact sequence is not exactly R14 then R15")
    raw = _read(root, review_ref)
    if len(raw) > 131072 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError("P02R3 review violates bounded byte grammar")
    lines = raw.decode("utf-8", "strict").splitlines()
    bindings = oracle["base_bindings"]
    required = {
        "Reviewed P02R3 plan SHA-256": _sha(root, PLAN_REF),
        "Reviewed P02R3 oracle SHA-256": _sha(root, ORACLE_REF),
        "Reviewed P02R3 bootstrap SHA-256": _sha(root, BOOTSTRAP_REF),
        "Reviewed P02R3 R14 result SHA-256": R14_REVIEW_SHA256,
        "Reviewed P02R2 plan SHA-256": bindings["p02r2_plan_sha256"],
        "Reviewed P02R2 oracle SHA-256": bindings["p02r2_oracle_sha256"],
        "Reviewed P02R2 entry SHA-256": bindings["p02r2_entry_sha256"],
        "Reviewed timeout blocker SHA-256": bindings["timeout_blocker_sha256"],
        "Reviewed timeout adjudication SHA-256": bindings["timeout_adjudication_sha256"],
    }
    if list(required) != oracle["review_contract"]["required_binding_labels"]:
        raise EvidenceValidationError("P02R3 review binding registry mismatch")
    for label, digest in required.items():
        if lines.count(f"{label}: `{digest}`") != 1:
            raise EvidenceValidationError(f"P02R3 review binding mismatch: {label}")
    verdicts = [line for line in lines if line.startswith("VERDICT:")]
    nonempty = [line for line in lines if line]
    if verdicts != ["VERDICT: AGREE"] or not nonempty or nonempty[-1] != "VERDICT: AGREE":
        raise EvidenceValidationError("P02R3 review is not uniquely agreeing")
    return content_digest(raw)


def _tree_refs(root: Path, ref: str) -> set[str]:
    top = root / ref
    if top.is_symlink() or not top.is_dir():
        raise EvidenceValidationError(f"protected tree is unsafe: {ref}")
    result: set[str] = set()
    for path in top.rglob("*"):
        if path.is_symlink():
            raise EvidenceValidationError(f"symlink in protected tree: {path}")
        if path.is_file():
            result.add(path.relative_to(root).as_posix())
        elif not path.is_dir():
            raise EvidenceValidationError(f"special path in protected tree: {path}")
    return result


def _control_refs(root: Path) -> set[str]:
    result = {"AGENTS.md", PLAN_REF, ORACLE_REF, BOOTSTRAP_REF, R2_BOOTSTRAP_REF}
    for directory_ref in ("docs/plans", "docs/reviews"):
        for path in (root / directory_ref).iterdir():
            if path.is_symlink():
                raise EvidenceValidationError(f"symlink in control directory: {path}")
            if path.is_file() and path.name.startswith("mathdevmcp-"):
                result.add(path.relative_to(root).as_posix())
    return result


def _protected_refs(
    root: Path,
    base_library: dict[str, Any],
    effective: dict[str, Any],
    *,
    output_refs: set[str],
) -> set[str]:
    allowlist = base_library["_implementation_allowlist"](effective)
    protected = set(base_library["_dirty_refs"](root)) - allowlist - output_refs
    protected.update(_control_refs(root))
    for tree in (
        ".local/mathdevmcp/evidence/p00-20260711",
        ".local/mathdevmcp/evidence/p01-20260711",
        ".local/mathdevmcp/evidence/p02-20260711",
        ".local/mathdevmcp/evidence/p02r2-20260712",
    ):
        protected.update(_tree_refs(root, tree))
    return protected


def _mkdir_tree(root: Path) -> None:
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    directory_fd = os.open(root, flags)
    try:
        for component in (".local", "mathdevmcp", "evidence"):
            next_fd = os.open(component, flags, dir_fd=directory_fd)
            os.close(directory_fd)
            directory_fd = next_fd
        os.mkdir("p02r3-20260712", mode=0o700, dir_fd=directory_fd)
        phase_fd = os.open("p02r3-20260712", flags, dir_fd=directory_fd)
        try:
            os.mkdir("entry", mode=0o700, dir_fd=phase_fd)
        finally:
            os.close(phase_fd)
    finally:
        os.close(directory_fd)


def _verify_new_tree(root: Path, refs: Iterable[str]) -> None:
    phase = root / EVIDENCE_ROOT_REF
    if phase.is_symlink() or not phase.is_dir() or {item.name for item in phase.iterdir()} != {"entry"}:
        raise EvidenceValidationError("P02R3 phase-root shape mismatch")
    entry = phase / "entry"
    items = list(entry.iterdir())
    names = {Path(ref).name for ref in refs}
    if {item.name for item in items} != names or any(item.is_symlink() or not item.is_file() for item in items):
        raise EvidenceValidationError("P02R3 entry-root shape mismatch")


def _write_snapshot(root: Path, review_ref: str) -> dict[str, str]:
    if (root / EVIDENCE_ROOT_REF).exists() or (root / EVIDENCE_ROOT_REF).is_symlink():
        raise EvidenceValidationError("P02R3 evidence root must be absent")
    oracle = _strict_json(_read(root, ORACLE_REF), "P02R3 recovery oracle")
    effective, _r2_oracle = _validate_oracle(root, oracle)
    bindings = oracle["base_bindings"]
    r2_entry = _verify_r2_entry(root, oracle, effective)
    base_library = runpy.run_path(
        str(root / "docs/plans/p02_entry_bootstrap_20260711.py"),
        run_name="p02_base_bootstrap_library",
    )
    for manifest_key in ("protected_entry_manifest_ref", "immutable_input_manifest_ref"):
        _verify_manifest_current(root, _read(root, r2_entry[manifest_key]), base_library)
    review_sha = _verify_review(root, oracle, review_ref)

    p01_stable_ref = r2_entry["p01_stable_decision_ref"]
    p01_index_ref = r2_entry["p01_terminal_receipt_index_ref"]
    strict_load_canonical_json(_read(root, p01_stable_ref), schema="p01_final_decision@1")
    p01_index = verify_receipt_index(root, p01_index_ref)
    if (
        _sha(root, p01_stable_ref) != r2_entry["p01_stable_decision_sha256"]
        or p01_index["index_sha256"] != r2_entry["p01_terminal_receipt_index_sha256"]
    ):
        raise EvidenceValidationError("P02R3 P01 predecessor binding mismatch")

    immutable_refs = set(base_library["_verified_immutable_refs"](root, effective))
    immutable_refs.update(
        {
            PLAN_REF,
            ORACLE_REF,
            BOOTSTRAP_REF,
            R14_REVIEW_REF,
            review_ref,
            *(value for key, value in bindings.items() if key.endswith("_ref")),
            r2_entry["implementation_entry_manifest_ref"],
            r2_entry["protected_entry_manifest_ref"],
            r2_entry["immutable_input_manifest_ref"],
        }
    )
    implementation = base_library["_manifest"](root, base_library["_implementation_refs"](root))
    output_refs = set(oracle["entry_schema"]["write_order"])
    protected = base_library["_manifest"](
        root, _protected_refs(root, base_library, effective, output_refs=output_refs)
    )
    immutable = base_library["_manifest"](root, immutable_refs)
    record = {
        "schema_version": "p02r3_entry_record@1",
        "phase": "P02",
        "revision": "P02R3",
        "recovery_plan_ref": PLAN_REF,
        "recovery_plan_sha256": _sha(root, PLAN_REF),
        "recovery_oracle_ref": ORACLE_REF,
        "recovery_oracle_sha256": _sha(root, ORACLE_REF),
        "agreeing_plan_review_ref": review_ref,
        "agreeing_plan_review_sha256": review_sha,
        "entry_bootstrap_ref": BOOTSTRAP_REF,
        "entry_bootstrap_sha256": _sha(root, BOOTSTRAP_REF),
        "base_plan_ref": bindings["p02r2_plan_ref"],
        "base_plan_sha256": bindings["p02r2_plan_sha256"],
        "base_compact_oracle_ref": bindings["p02r2_oracle_ref"],
        "base_compact_oracle_sha256": bindings["p02r2_oracle_sha256"],
        "base_materialized_oracle_ref": bindings["materialized_oracle_ref"],
        "base_materialized_oracle_sha256": bindings["materialized_oracle_sha256"],
        "prior_entry_ref": bindings["p02r2_entry_ref"],
        "prior_entry_sha256": bindings["p02r2_entry_sha256"],
        "runtime_contract_review_ref": bindings["timeout_adjudication_ref"],
        "runtime_contract_review_sha256": bindings["timeout_adjudication_sha256"],
        "pre_round_blocker_ref": bindings["timeout_blocker_ref"],
        "pre_round_blocker_sha256": bindings["timeout_blocker_sha256"],
        "p01_stable_decision_ref": p01_stable_ref,
        "p01_stable_decision_sha256": r2_entry["p01_stable_decision_sha256"],
        "p01_terminal_receipt_index_ref": p01_index_ref,
        "p01_terminal_receipt_index_sha256": r2_entry["p01_terminal_receipt_index_sha256"],
        "implementation_entry_manifest_ref": IMPLEMENTATION_MANIFEST_REF,
        "implementation_entry_manifest_sha256": content_digest(implementation),
        "protected_entry_manifest_ref": PROTECTED_MANIFEST_REF,
        "protected_entry_manifest_sha256": content_digest(protected),
        "immutable_input_manifest_ref": IMMUTABLE_MANIFEST_REF,
        "immutable_input_manifest_sha256": content_digest(immutable),
    }
    if set(record) != set(oracle["entry_schema"]["exact_keys"]):
        raise EvidenceValidationError("P02R3 entry record differs from exact schema")
    payloads = {
        IMPLEMENTATION_MANIFEST_REF: implementation,
        PROTECTED_MANIFEST_REF: protected,
        IMMUTABLE_MANIFEST_REF: immutable,
        ENTRY_RECORD_REF: canonical_json_bytes(record),
    }
    _mkdir_tree(root)
    for ref in oracle["entry_schema"]["write_order"]:
        atomic_write_bytes_no_replace(root, ref, payloads[ref])
    _verify_new_tree(root, payloads)
    reopened = {ref: _read(root, ref) for ref in payloads}
    if reopened != payloads:
        raise EvidenceValidationError("P02R3 entry reopen mismatch")
    current = {
        IMPLEMENTATION_MANIFEST_REF: base_library["_manifest"](
            root, base_library["_implementation_refs"](root)
        ),
        PROTECTED_MANIFEST_REF: base_library["_manifest"](
            root, _protected_refs(root, base_library, effective, output_refs=output_refs)
        ),
        IMMUTABLE_MANIFEST_REF: base_library["_manifest"](root, immutable_refs),
    }
    if any(current[ref] != reopened[ref] for ref in current):
        raise EvidenceValidationError("P02R3 entry manifest scope changed during creation")
    return {"entry_record_ref": ENTRY_RECORD_REF, "entry_record_sha256": content_digest(reopened[ENTRY_RECORD_REF])}


def main() -> int:
    argv = sys.argv[1:]
    if len(argv) != 2 or argv[0] != "--agreeing-plan-review-ref" or any("=" in item for item in argv):
        raise EvidenceValidationError(
            "P02R3 bootstrap accepts exactly --agreeing-plan-review-ref VALUE"
        )
    _validate_invocation(argv)
    if argv[1] != REVIEW_REF:
        raise EvidenceValidationError("P02R3 agreeing review ref is not the exact R15 result")
    root = Path.cwd().absolute()
    if not (root / ".git").is_dir() or not (root / "src/mathdevmcp").is_dir():
        raise EvidenceValidationError("P02R3 bootstrap must run at workspace root")
    result = _write_snapshot(root, argv[1])
    sys.stdout.buffer.write(canonical_json_bytes(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
