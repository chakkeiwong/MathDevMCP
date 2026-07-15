#!/usr/bin/env python3
"""Append-only measured governance for the Phase 02R3 extraction gate."""

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

from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
)
from mathdevmcp import extraction_evidence as extraction


PHASE = "P02"
REVISION = "P02R3"
EVIDENCE_ROOT_REF = ".local/mathdevmcp/evidence/p02r3-20260712"
ENTRY_RECORD_REF = f"{EVIDENCE_ROOT_REF}/entry/entry-record.json"
BASE_ORACLE_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-02-extraction-oracle-2026-07-11.json"
RECOVERY_ORACLE_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-02r3-timeout-policy-recovery-oracle-2026-07-12.json"
MATERIALIZED_ORACLE_REF = "docs/plans/mathdevmcp-real-document-remediation-phase-02-materialized-obligations-oracle-2026-07-11.json"
PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
ROUND_RE = re.compile(r"^rr0[1-5]$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
CALLER_FORBIDDEN_ENV = (
    "MATHDEVMCP_P02_ACTION",
    "MATHDEVMCP_P02_DISPATCH_DEPTH",
    "MATHDEVMCP_P02_ROUND_ROOT",
)


def _repo_root() -> Path:
    root = Path.cwd().absolute()
    for ref in (".git", "src", "tests", "scripts", BASE_ORACLE_REF, RECOVERY_ORACLE_REF):
        path = root / ref
        if path.is_symlink() or not path.exists():
            raise EvidenceValidationError("p02_governance.py must run from the MathDevMCP workspace root")
    return root


def _guard_caller_environment() -> None:
    present = [key for key in CALLER_FORBIDDEN_ENV if key in os.environ]
    if present:
        raise EvidenceValidationError(f"caller supplied reserved Phase 02 environment: {present}")


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _logical_ref(root: Path, value: str | os.PathLike[str]) -> str:
    path = Path(value)
    if path.is_absolute():
        try:
            path = path.relative_to(root)
        except ValueError as exc:
            raise EvidenceValidationError("path is outside the workspace trust root") from exc
    ref = path.as_posix()
    pure = PurePosixPath(ref)
    if not ref or pure.is_absolute() or pure.as_posix() != ref or any(part in {"", ".", ".."} for part in pure.parts):
        raise EvidenceValidationError("path is not a normalized workspace-relative ref")
    return ref


def _read(root: Path, ref: str) -> bytes:
    raw, info = read_bytes_no_follow(root, _logical_ref(root, ref))
    if not stat.S_ISREG(info.st_mode):
        raise EvidenceValidationError(f"artifact is not a regular file: {ref}")
    return raw


def _digest(root: Path, ref: str) -> str:
    return content_digest(_read(root, ref))


def _strict_json_bytes(raw: bytes, name: str, *, canonical: bool = True) -> dict[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"{name} violates strict JSON byte rules")

    def no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
        value: dict[str, Any] = {}
        for key, item in pairs:
            if key in value:
                raise EvidenceValidationError(f"{name} has duplicate key {key}")
            value[key] = item
        return value

    try:
        value = json.loads(
            raw.decode("utf-8", "strict"),
            object_pairs_hook=no_duplicates,
            parse_float=lambda token: (_ for _ in ()).throw(EvidenceValidationError(f"float forbidden in {name}: {token}")),
            parse_constant=lambda token: (_ for _ in ()).throw(EvidenceValidationError(f"nonfinite forbidden in {name}: {token}")),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise EvidenceValidationError(f"{name} is not strict JSON") from exc
    if type(value) is not dict:
        raise EvidenceValidationError(f"{name} must be a JSON object")
    if canonical and canonical_json_bytes(value) != raw:
        raise EvidenceValidationError(f"{name} is not canonical JSON")
    return value


def _strict_json(root: Path, ref: str, name: str, *, canonical: bool = True) -> dict[str, Any]:
    return _strict_json_bytes(_read(root, ref), name, canonical=canonical)


def _load_effective_profile(root: Path) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    effective, materialized = extraction.load_profile(root)
    recovery = extraction.load_recovery_oracle(root)
    if (
        recovery.get("revision") != REVISION
        or recovery["recovery_refs"]["recovery_oracle_ref"] != RECOVERY_ORACLE_REF
        or recovery["base_bindings"]["materialized_oracle_ref"] != MATERIALIZED_ORACLE_REF
        or materialized.get("obligation_count") != 17
    ):
        raise EvidenceValidationError("P02R3 effective profile binding mismatch")
    profile = effective["governance_action_profile"]
    action_ids = [*profile["action_order"], *profile["failure_suffix_order"]]
    if list(profile["actions"]) != action_ids or set(profile["receipt_binding_keys"]) != set(action_ids):
        raise EvidenceValidationError("effective governance action registry mismatch")
    if profile["actions"]["compile"]["child_argv_template"][3:] != sorted(
        profile["actions"]["compile"]["child_argv_template"][3:], key=lambda item: item.encode("utf-8")
    ):
        raise EvidenceValidationError("effective compile allowlist is not sorted")
    profile["round_close_schema"]["non_claims"] = extraction.canonical_non_claims(
        profile["round_close_schema"]["non_claims"]
    )
    return effective, recovery, profile


def _round_context(root: Path, value: str | os.PathLike[str], *, must_exist: bool) -> tuple[str, str, Path]:
    ref = _logical_ref(root, value)
    pure = PurePosixPath(ref)
    if pure.parent.as_posix() != f"{EVIDENCE_ROOT_REF}/result-rounds" or ROUND_RE.fullmatch(pure.name) is None:
        raise EvidenceValidationError("round root is outside the fixed Phase 02R3 result-round namespace")
    path = root / ref
    current = root
    for part in pure.parts:
        current = current / part
        if current.exists() or current.is_symlink():
            info = current.lstat()
            if stat.S_ISLNK(info.st_mode) or (current != path and not stat.S_ISDIR(info.st_mode)):
                raise EvidenceValidationError(f"unsafe round path component: {current}")
    if must_exist and (path.is_symlink() or not path.is_dir()):
        raise EvidenceValidationError("round root is absent or unsafe")
    if not must_exist and (path.exists() or path.is_symlink()):
        raise EvidenceValidationError("round root must be absent")
    return ref, pure.name, path


def _safe_mkdir(path: Path, *, parents: bool = False) -> None:
    if path.exists() or path.is_symlink():
        if path.is_symlink() or not path.is_dir():
            raise EvidenceValidationError(f"directory path is unsafe: {path}")
        return
    path.mkdir(mode=0o700, parents=parents, exist_ok=False)


def _write(root: Path, ref: str, raw: bytes) -> dict[str, Any]:
    result = atomic_write_bytes_no_replace(root, ref, raw)
    reopened = _read(root, ref)
    if reopened != raw or content_digest(reopened) != result["sha256"]:
        raise EvidenceValidationError(f"no-overwrite artifact failed immediate verification: {ref}")
    return result


def _write_json(root: Path, ref: str, value: Any) -> dict[str, Any]:
    return _write(root, ref, canonical_json_bytes(value))


def _implementation_manifest_bytes(root: Path) -> bytes:
    return extraction.manifest_bytes(root, extraction.implementation_refs(root))


def _parse_manifest(raw: bytes) -> dict[str, str]:
    return extraction.parse_sha256_manifest(raw)


def _verify_manifest(root: Path, ref: str, *, current: bool = True) -> dict[str, str]:
    return extraction.verify_manifest(root, ref, require_current_bytes=current)


def _verify_entry(root: Path, recovery: Mapping[str, Any]) -> dict[str, Any]:
    verified = extraction.verify_entry(root)
    record = verified["record"]
    if record["recovery_oracle_ref"] != RECOVERY_ORACLE_REF:
        raise EvidenceValidationError("entry does not bind the P02R3 recovery oracle")
    review = _read(root, record["agreeing_plan_review_ref"])
    history = recovery["review_contract"]["review_history"]
    if len(history) != 1 or history[0]["round"] != 14:
        raise EvidenceValidationError("P02R3 review history is not exact")
    required = {
        "Reviewed P02R3 plan SHA-256": record["recovery_plan_sha256"],
        "Reviewed P02R3 oracle SHA-256": record["recovery_oracle_sha256"],
        "Reviewed P02R3 bootstrap SHA-256": record["entry_bootstrap_sha256"],
        "Reviewed P02R3 R14 result SHA-256": history[0]["result_sha256"],
        "Reviewed P02R2 plan SHA-256": record["base_plan_sha256"],
        "Reviewed P02R2 oracle SHA-256": record["base_compact_oracle_sha256"],
        "Reviewed P02R2 entry SHA-256": record["prior_entry_sha256"],
        "Reviewed timeout blocker SHA-256": record["pre_round_blocker_sha256"],
        "Reviewed timeout adjudication SHA-256": record["runtime_contract_review_sha256"],
    }
    _parse_review_bytes(review, required, "plan review", expected_verdict="AGREE")
    return verified


def _parse_review_bytes(
    raw: bytes,
    bindings: Mapping[str, str],
    kind: str,
    *,
    expected_verdict: str | None = None,
) -> str:
    if len(raw) > 131072 or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw or b"\r" in raw:
        raise EvidenceValidationError(f"{kind} violates bounded UTF-8 grammar")
    try:
        lines = raw.decode("utf-8", "strict").splitlines()
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError(f"{kind} is not strict UTF-8") from exc
    for label, value in bindings.items():
        line = f"{label}: `{value}`"
        if lines.count(line) != 1 or sum(label in item for item in lines) != 1:
            raise EvidenceValidationError(f"{kind} binding is not unique: {label}")
    verdicts = [line for line in lines if line.startswith("VERDICT:")]
    nonempty = [line for line in lines if line]
    if len(verdicts) != 1 or verdicts[0] not in {"VERDICT: AGREE", "VERDICT: REVISE"} or not nonempty or nonempty[-1] != verdicts[0]:
        raise EvidenceValidationError(f"{kind} verdict is not unique and final")
    verdict = verdicts[0].split(": ", 1)[1]
    if expected_verdict is not None and verdict != expected_verdict:
        raise EvidenceValidationError(f"{kind} verdict is not {expected_verdict}")
    return verdict


def _effective_external_argv(profile: Mapping[str, Any], round_ref: str, action: str, artifact_ref: str | None = None) -> list[str]:
    operation = profile["actions"][action]["external_operation"]
    result = [item.replace("RR", round_ref).replace("ACTION", action) for item in profile["external_argv_templates"][operation]]
    if artifact_ref is not None:
        result = [item.replace("ARTIFACT_REF", artifact_ref) for item in result]
    if any("ARTIFACT_REF" in item for item in result):
        raise EvidenceValidationError("external argv has an unbound artifact ref")
    return result


def _effective_child_argv(profile: Mapping[str, Any], round_ref: str, action: str) -> list[str] | None:
    template = profile["actions"][action]["child_argv_template"]
    return None if template is None else [item.replace("RR", round_ref) for item in template]


def _effective_child_environment(profile: Mapping[str, Any], round_ref: str, action: str) -> dict[str, str]:
    return {
        key: value.replace("RR", round_ref).replace("ACTION", action)
        for key, value in profile["child_environment"]["template"].items()
    }


def _receipt_ref(round_ref: str, sequence: int) -> str:
    return f"{round_ref}/receipts/receipt-{sequence:02d}.json"


def _index_ref(round_ref: str, sequence: int) -> str:
    return f"{round_ref}/receipts/receipt-index-{sequence:02d}.json"


def _verify_receipt_index(root: Path, ref: str, profile: Mapping[str, Any]) -> dict[str, Any]:
    raw = _read(root, ref)
    index = extraction.validate_receipt_index(_strict_json_bytes(raw, "P02 receipt index"))
    round_ref = f"{EVIDENCE_ROOT_REF}/result-rounds/{index['result_round']}"
    if PurePosixPath(ref).parent.as_posix() != f"{round_ref}/receipts":
        raise EvidenceValidationError("receipt index is not round-local")
    prior: str | None = None
    receipts: list[dict[str, Any]] = []
    for entry in index["receipts"]:
        if entry["receipt_ref"] != _receipt_ref(round_ref, entry["sequence"]):
            raise EvidenceValidationError("receipt ref is not canonical for its sequence")
        receipt_raw = _read(root, entry["receipt_ref"])
        digest = content_digest(receipt_raw)
        if digest != entry["receipt_sha256"]:
            raise EvidenceValidationError("receipt digest mismatch")
        receipt = extraction.validate_command_receipt(
            _strict_json_bytes(receipt_raw, "P02 command receipt"), profile=dict(profile)
        )
        if receipt["sequence"] != entry["sequence"] or receipt["check_id"] != entry["check_id"] or receipt["prior_receipt_sha256"] != prior:
            raise EvidenceValidationError("receipt/index chain mismatch")
        for stream in ("stdout", "stderr"):
            stream_raw = _read(root, receipt[f"{stream}_ref"])
            if content_digest(stream_raw) != receipt[f"{stream}_sha256"] or len(stream_raw) != receipt[f"{stream}_byte_count"]:
                raise EvidenceValidationError("receipt stream binding mismatch")
        receipts.append({"entry": entry, "record": receipt, "sha256": digest})
        prior = digest
    return {"index_ref": ref, "index_sha256": content_digest(raw), "record": index, "receipts": receipts}


def _latest_chain(root: Path, round_ref: str, profile: Mapping[str, Any]) -> dict[str, Any] | None:
    directory = root / round_ref / "receipts"
    if not directory.exists():
        return None
    if directory.is_symlink() or not directory.is_dir():
        raise EvidenceValidationError("receipt directory is unsafe")
    candidates = sorted(directory.glob("receipt-index-*.json"), key=lambda item: item.name)
    if not candidates:
        return None
    verified = [_verify_receipt_index(root, path.relative_to(root).as_posix(), profile) for path in candidates]
    for sequence, item in enumerate(verified, start=1):
        if item["record"]["head_sequence"] != sequence or item["record"]["receipts"] != verified[-1]["record"]["receipts"][:sequence]:
            raise EvidenceValidationError("receipt-index snapshots are not contiguous immutable prefixes")
    return verified[-1]


def _append_receipt(
    root: Path,
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
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
    chain = _latest_chain(root, round_ref, profile)
    entries = [] if chain is None else list(chain["record"]["receipts"])
    sequence = len(entries) + 1
    stdout = _read(root, stdout_ref)
    stderr = _read(root, stderr_ref)
    action_profile = profile["actions"][action]
    child_argv = _effective_child_argv(profile, round_ref, action)
    child_environment = _effective_child_environment(profile, round_ref, action) if child_argv is not None else None
    receipt = {
        "schema_version": "p02_command_receipt@1",
        "phase": PHASE,
        "result_round": result_round,
        "sequence": sequence,
        "check_id": action,
        "execution_class": action_profile["execution_class"],
        "handler_id": action_profile["handler_id"],
        "external_argv": _effective_external_argv(profile, round_ref, action, artifact_ref),
        "child_argv": child_argv,
        "child_environment_sha256": content_digest(child_environment) if child_environment is not None else None,
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
    extraction.validate_command_receipt(receipt, profile=dict(profile))
    written = _write_json(root, _receipt_ref(round_ref, sequence), receipt)
    entry = {
        "sequence": sequence,
        "check_id": action,
        "receipt_ref": _receipt_ref(round_ref, sequence),
        "receipt_sha256": written["sha256"],
    }
    index = {
        "schema_version": "p02_receipt_index@1",
        "phase": PHASE,
        "result_round": result_round,
        "receipts": [*entries, entry],
        "head_sequence": sequence,
        "head_sha256": written["sha256"],
    }
    _write_json(root, _index_ref(round_ref, sequence), index)
    verified = _verify_receipt_index(root, _index_ref(round_ref, sequence), profile)
    return {"ref": entry["receipt_ref"], "sha256": written["sha256"], "record": receipt}, verified


def _fixed_ref(profile: Mapping[str, Any], key: str, result_round: str, round_ref: str) -> str:
    return profile["fixed_artifact_refs"][key].replace("RESULT_ROUND", result_round).replace("RR", round_ref)


def _receipt_for(chain: Mapping[str, Any], action: str) -> dict[str, Any] | None:
    matches = [item["record"] for item in chain["receipts"] if item["record"]["check_id"] == action]
    if len(matches) > 1:
        raise EvidenceValidationError(f"receipt chain repeats action: {action}")
    return matches[0] if matches else None


def _receipt_pair(
    chain: Mapping[str, Any],
    action: str,
    ref_key: str,
    digest_key: str,
) -> tuple[str | None, str | None]:
    receipt = _receipt_for(chain, action)
    if receipt is None or receipt["exit_code"] != 0:
        return None, None
    return receipt["bindings"][ref_key], receipt["bindings"][digest_key]


def _null_bindings(profile: Mapping[str, Any], action: str) -> dict[str, None]:
    return {key: None for key in profile["receipt_binding_keys"][action]}


def _ensure_runtime_directories(root: Path, round_ref: str) -> None:
    for suffix in (
        "governance",
        "governance/home",
        "governance/tmp",
        "logs",
        "receipts",
        "inputs",
    ):
        path = root / round_ref / suffix
        _safe_mkdir(path, parents=False)


def _verify_runtime_directories(root: Path, round_ref: str) -> None:
    for suffix in ("governance/home", "governance/tmp", "logs", "receipts", "inputs"):
        path = root / round_ref / suffix
        if path.is_symlink() or not path.is_dir():
            raise EvidenceValidationError(f"round runtime directory is absent or unsafe: {suffix}")


def _validate_round_close(root: Path, ref: str, profile: Mapping[str, Any]) -> dict[str, Any]:
    record = _strict_json(root, ref, "P02 round close")
    schema = profile["round_close_schema"]
    if set(record) != set(schema["exact_keys"]) or record["schema_version"] != schema["schema_version"]:
        raise EvidenceValidationError("P02 round-close schema mismatch")
    if record["phase"] != PHASE or record["decision"] != "blocked" or record["publication_mode"] != "disabled":
        raise EvidenceValidationError("P02 round-close boundary mismatch")
    if ROUND_RE.fullmatch(record["result_round"]) is None:
        raise EvidenceValidationError("P02 round-close result round mismatch")
    if record["close_reason"] not in profile["scoped_repair_schema"]["close_reasons"]:
        raise EvidenceValidationError("P02 round-close reason mismatch")
    if type(record["failed_actions"]) is not list or type(record["log_inventory"]) is not list:
        raise EvidenceValidationError("P02 round-close ordered fields mismatch")
    if record["non_claims"] != schema["non_claims"] or type(record["repairs"]) is not list or not record["repairs"]:
        raise EvidenceValidationError("P02 round-close non-claims or repairs mismatch")
    if (
        type(record["vetoes"]) is not dict
        or set(record["vetoes"]) != set(schema["veto_keys"])
        or len(record["vetoes"]) != len(schema["veto_keys"])
    ):
        raise EvidenceValidationError("P02 round-close veto map mismatch")
    if not any(record["vetoes"].values()) or record["vetoes"]["governance_chain_failure"]:
        raise EvidenceValidationError("P02 round-close veto outcome mismatch")
    if any(type(value) is not bool for value in record["vetoes"].values()):
        raise EvidenceValidationError("P02 round-close veto values are not booleans")
    seen_null_stage = False
    for ref_key, digest_key in schema["nullable_stage_pairs_in_order"]:
        pair = (record[ref_key], record[digest_key])
        if (pair[0] is None) != (pair[1] is None):
            raise EvidenceValidationError("P02 round-close stage pair has mixed nullability")
        if pair[0] is None:
            seen_null_stage = True
        elif seen_null_stage:
            raise EvidenceValidationError("P02 round-close has a reached stage after an unreached stage")
    if (record["result_review_ref"] is None) != (record["result_review_verdict"] is None):
        raise EvidenceValidationError("P02 round-close result-review verdict nullability mismatch")
    if (record["final_seal_audit_ref"] is None) != (record["final_seal_audit_verdict"] is None):
        raise EvidenceValidationError("P02 round-close final-audit verdict nullability mismatch")
    for key in ("result_review_verdict", "final_seal_audit_verdict"):
        if record[key] is not None and record[key] not in {"AGREE", "REVISE"}:
            raise EvidenceValidationError("P02 round-close verdict is outside the reviewed enum")
    predecessor = (
        record["predecessor_round_close_ref"],
        record["predecessor_round_close_sha256"],
        record["predecessor_terminal_receipt_index_ref"],
        record["predecessor_terminal_receipt_index_sha256"],
    )
    if record["result_round"] == "rr01":
        if any(value is not None for value in predecessor):
            raise EvidenceValidationError("rr01 close has non-null predecessor fields")
    elif any(value is None for value in predecessor):
        raise EvidenceValidationError("successor close has null predecessor fields")
    for key, value in record.items():
        if key.endswith("_ref") and value is not None:
            _logical_ref(root, value)
        elif key.endswith("_sha256") and value is not None and SHA_RE.fullmatch(value) is None:
            raise EvidenceValidationError(f"P02 round-close digest is invalid: {key}")
    direct_pairs = [
        (key.removesuffix("_sha256") + "_ref", key)
        for key in record
        if key.endswith("_sha256") and key.removesuffix("_sha256") + "_ref" in record
    ]
    for ref_key, digest_key in direct_pairs:
        if record[ref_key] is not None and _digest(root, record[ref_key]) != record[digest_key]:
            raise EvidenceValidationError(f"P02 round-close artifact binding drift: {ref_key}")
    for item in record["log_inventory"]:
        if set(item) != {"logical_ref", "sha256", "byte_count", "role", "exit_code"}:
            raise EvidenceValidationError("P02 round-close log entry schema mismatch")
        raw = _read(root, item["logical_ref"])
        if content_digest(raw) != item["sha256"] or len(raw) != item["byte_count"]:
            raise EvidenceValidationError("P02 round-close log binding mismatch")
    return record


def _predecessor_bindings(
    root: Path,
    profile: Mapping[str, Any],
    result_round: str,
) -> dict[str, str | None]:
    number = int(result_round[2:])
    phase_root = root / EVIDENCE_ROOT_REF
    if phase_root.is_symlink() or not phase_root.is_dir():
        raise EvidenceValidationError("P02R3 phase root is unsafe")
    rounds_parent = root / EVIDENCE_ROOT_REF / "result-rounds"
    existing = []
    if rounds_parent.exists():
        if rounds_parent.is_symlink() or not rounds_parent.is_dir():
            raise EvidenceValidationError("result-rounds parent is unsafe")
        existing = sorted(
            item.name
            for item in rounds_parent.iterdir()
            if item.name != result_round and ROUND_RE.fullmatch(item.name)
        )
    expected_phase_children = {"entry", "result-rounds"} if rounds_parent.exists() else {"entry"}
    if {item.name for item in phase_root.iterdir()} != expected_phase_children:
        raise EvidenceValidationError("P02R3 phase root contains an unexpected pre-round child")
    expected_existing = [f"rr{index:02d}" for index in range(1, number)]
    if existing != expected_existing:
        raise EvidenceValidationError("result-round namespace does not contain exactly the predecessor prefix")
    nulls = {
        "predecessor_round_close_ref": None,
        "predecessor_round_close_sha256": None,
        "predecessor_terminal_receipt_index_ref": None,
        "predecessor_terminal_receipt_index_sha256": None,
    }
    if number == 1:
        return nulls
    prior_round = f"rr{number - 1:02d}"
    prior_ref = f"{EVIDENCE_ROOT_REF}/result-rounds/{prior_round}"
    close_ref = f"{prior_ref}/round-close.json"
    close = _validate_round_close(root, close_ref, profile)
    if close["result_round"] != prior_round:
        raise EvidenceValidationError("predecessor close is not the immediately preceding result round")
    chain = _latest_chain(root, prior_ref, profile)
    if chain is None:
        raise EvidenceValidationError("predecessor terminal receipt index is absent")
    terminal = chain["receipts"][-1]["record"]
    if (
        terminal["check_id"] != "close_round"
        or terminal["exit_code"] != 0
        or terminal["bindings"]["round_close_ref"] != close_ref
        or terminal["bindings"]["round_close_sha256"] != _digest(root, close_ref)
        or terminal["bindings"]["receipt_index_before_close_ref"] != close["receipt_index_before_close_ref"]
        or terminal["bindings"]["receipt_index_before_close_sha256"] != close["receipt_index_before_close_sha256"]
    ):
        raise EvidenceValidationError("predecessor terminal receipt does not seal its close")
    return {
        "predecessor_round_close_ref": close_ref,
        "predecessor_round_close_sha256": _digest(root, close_ref),
        "predecessor_terminal_receipt_index_ref": chain["index_ref"],
        "predecessor_terminal_receipt_index_sha256": chain["index_sha256"],
    }


def _init_round(
    root: Path,
    effective: Mapping[str, Any],
    recovery: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_root: str,
) -> dict[str, Any]:
    started = _utc_now()
    start_ns = time.monotonic_ns()
    round_ref, result_round, round_path = _round_context(root, round_root, must_exist=False)
    if sys.executable != PYTHON or os.environ.get("PYTHONPATH") != "src":
        raise EvidenceValidationError("init-round requires the pinned Python and PYTHONPATH=src")
    entry = _verify_entry(root, recovery)
    entry_record = entry["record"]
    predecessor = _predecessor_bindings(root, profile, result_round)
    current_manifest = _implementation_manifest_bytes(root)
    manifest_ref = _fixed_ref(profile, "round_implementation_manifest", result_round, round_ref)

    _safe_mkdir(round_path.parent, parents=False)
    round_path.mkdir(mode=0o700, parents=False, exist_ok=False)
    _ensure_runtime_directories(root, round_ref)
    written_manifest = _write(root, manifest_ref, current_manifest)
    if _verify_manifest(root, manifest_ref) != _parse_manifest(current_manifest):
        raise EvidenceValidationError("round implementation manifest failed immediate verification")

    reviewed = extraction.downstream_reviewed_bindings(entry_record)
    bindings: dict[str, Any] = {
        "entry_record_ref": entry["ref"],
        "entry_record_sha256": entry["sha256"],
        "entry_implementation_manifest_ref": entry_record["implementation_entry_manifest_ref"],
        "entry_implementation_manifest_sha256": entry_record["implementation_entry_manifest_sha256"],
        "round_implementation_manifest_ref": manifest_ref,
        "round_implementation_manifest_sha256": written_manifest["sha256"],
        "entry_protected_manifest_ref": entry_record["protected_entry_manifest_ref"],
        "entry_protected_manifest_sha256": entry_record["protected_entry_manifest_sha256"],
        "entry_immutable_input_manifest_ref": entry_record["immutable_input_manifest_ref"],
        "entry_immutable_input_manifest_sha256": entry_record["immutable_input_manifest_sha256"],
        "p01_stable_decision_ref": entry_record["p01_stable_decision_ref"],
        "p01_stable_decision_sha256": entry_record["p01_stable_decision_sha256"],
        "p01_terminal_receipt_index_ref": entry_record["p01_terminal_receipt_index_ref"],
        "p01_terminal_receipt_index_sha256": entry_record["p01_terminal_receipt_index_sha256"],
        **reviewed,
        "agreeing_plan_review_ref": entry_record["agreeing_plan_review_ref"],
        "agreeing_plan_review_sha256": entry_record["agreeing_plan_review_sha256"],
        **predecessor,
    }
    if set(bindings) != set(profile["receipt_binding_keys"]["init_round"]):
        raise EvidenceValidationError("init-round binding map differs from the effective profile")
    measurement = {
        "git_commit": extraction.current_git_commit(root),
        "implementation_manifest_sha256": written_manifest["sha256"],
        "python_executable": sys.executable,
        "python_version": sys.version.split()[0],
        "result_round": result_round,
        "revision": REVISION,
    }
    stdout_ref = f"{round_ref}/logs/init-round.stdout"
    stderr_ref = f"{round_ref}/logs/init-round.stderr"
    _write(root, stdout_ref, canonical_json_bytes(measurement) + b"\n")
    _write(root, stderr_ref, b"")
    ended = _utc_now()
    receipt, chain = _append_receipt(
        root,
        profile,
        round_ref,
        result_round,
        "init_round",
        artifact_ref=None,
        started_at=started,
        ended_at=ended,
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


def _run_subprocess(
    root: Path,
    profile: Mapping[str, Any],
    round_ref: str,
    action: str,
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    argv = _effective_child_argv(profile, round_ref, action)
    if argv is None:
        raise EvidenceValidationError(f"subprocess action has no child argv: {action}")
    environment = _effective_child_environment(profile, round_ref, action)
    completed = subprocess.run(
        argv,
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
        shell=False,
    )
    bindings: dict[str, Any] = _null_bindings(profile, action) if completed.returncode != 0 else {}
    if action == "generate_extraction_bundle" and completed.returncode == 0:
        try:
            parsed = _strict_json_bytes(completed.stdout.rstrip(b"\n"), "generator stdout")
            if completed.stdout != canonical_json_bytes(parsed) + b"\n" or set(parsed) != {
                "bundle_index_ref",
                "bundle_index_sha256",
            }:
                raise EvidenceValidationError("generator stdout contract mismatch")
            verified = extraction.verify_bundle_index(root, parsed["bundle_index_ref"])
            if verified["sha256"] != parsed["bundle_index_sha256"]:
                raise EvidenceValidationError("generator bundle binding mismatch")
            bindings = dict(parsed)
        except Exception as exc:
            return 1, completed.stdout, completed.stderr + f"{type(exc).__name__}: {exc}\n".encode(), _null_bindings(profile, action)
    return completed.returncode, completed.stdout, completed.stderr, bindings


def _manifest_exit(
    root: Path,
    entry_manifest_ref: str,
    output_ref: str,
) -> tuple[bytes, bool]:
    entry_raw = _read(root, entry_manifest_ref)
    entry = _parse_manifest(entry_raw)
    current = extraction.manifest_bytes(root, list(entry))
    _write(root, output_ref, current)
    return current, current == entry_raw


def _native_evidence_gate(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    action: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    refs = extraction.extraction_artifact_refs(round_ref)
    init = chain["receipts"][0]["record"]["bindings"]
    if action == "mutation_ambiguity_gate":
        verifier = getattr(extraction, "verify_mutation_matrix", None)
        if verifier is not None:
            verified = verifier(root, refs["mutation_matrix"])
        else:
            raw = _read(root, refs["mutation_matrix"])
            record = extraction.validate_mutation_matrix(_strict_json_bytes(raw, "mutation matrix"))
            verified = {"sha256": content_digest(raw), "record": record}
        bindings = {"mutation_matrix_ref": refs["mutation_matrix"], "mutation_matrix_sha256": verified["sha256"]}
        return 0, canonical_json_bytes(bindings), b"", bindings
    if action == "zero_backend_source_edit_gate":
        ledger = extraction.verify_backend_ledger_index(root, refs["backend_ledger_index"])
        output_ref = f"{round_ref}/immutable-input-exit-sha256.txt"
        current, equal = _manifest_exit(root, init["entry_immutable_input_manifest_ref"], output_ref)
        if ledger["record"]["forbidden_attempt_count"] != 0 or not equal:
            raise EvidenceValidationError("backend ledger or immutable-input comparison failed")
        bindings = {
            "backend_ledger_index_ref": refs["backend_ledger_index"],
            "backend_ledger_index_sha256": ledger["sha256"],
            "immutable_input_exit_manifest_ref": output_ref,
            "immutable_input_exit_manifest_sha256": content_digest(current),
        }
        return 0, canonical_json_bytes(bindings), b"", bindings
    if action == "protected_check":
        extraction.verify_entry(root)
        output_ref = f"{round_ref}/protected-exit-sha256.txt"
        current, equal = _manifest_exit(root, init["entry_protected_manifest_ref"], output_ref)
        if not equal:
            raise EvidenceValidationError("protected entry baseline drifted")
        bindings = {
            "protected_exit_manifest_ref": output_ref,
            "protected_exit_manifest_sha256": content_digest(current),
        }
        return 0, canonical_json_bytes(bindings), b"", bindings
    if action == "implementation_exit":
        current = _implementation_manifest_bytes(root)
        initialized = _read(root, init["round_implementation_manifest_ref"])
        if current != initialized:
            raise EvidenceValidationError("implementation bytes drifted after init-round")
        bindings = {
            "round_implementation_manifest_ref": init["round_implementation_manifest_ref"],
            "round_implementation_manifest_sha256": content_digest(initialized),
        }
        return 0, canonical_json_bytes(bindings), b"", bindings
    if action == "allowlist":
        before = _parse_manifest(_read(root, init["entry_implementation_manifest_ref"]))
        after = _parse_manifest(_read(root, init["round_implementation_manifest_ref"]))
        touched = sorted(
            (ref for ref in set(before) | set(after) if before.get(ref) != after.get(ref)),
            key=lambda item: item.encode("utf-8"),
        )
        allowed = set(extraction.implementation_allowlist(root))
        unexpected = [ref for ref in touched if ref not in allowed]
        touched_ref = f"{round_ref}/touched-paths.txt"
        unexpected_ref = f"{round_ref}/unexpected-paths.txt"
        touched_raw = "".join(f"{ref}\n" for ref in touched).encode()
        unexpected_raw = "".join(f"{ref}\n" for ref in unexpected).encode()
        _write(root, touched_ref, touched_raw)
        _write(root, unexpected_ref, unexpected_raw)
        bindings = {
            "touched_paths_ref": touched_ref,
            "touched_paths_sha256": content_digest(touched_raw),
            "unexpected_paths_ref": unexpected_ref,
            "unexpected_paths_sha256": content_digest(unexpected_raw),
        }
        if unexpected:
            return 1, canonical_json_bytes({"touched": touched, "unexpected": unexpected}), unexpected_raw, _null_bindings(profile, action)
        return 0, canonical_json_bytes({"touched": touched, "unexpected": unexpected}), b"", bindings
    raise EvidenceValidationError(f"unsupported evidence-gate action: {action}")


def _action_success(chain: Mapping[str, Any], action: str) -> bool:
    receipt = _receipt_for(chain, action)
    return receipt is not None and receipt["exit_code"] == 0


def _phase_measurements(
    root: Path,
    profile: Mapping[str, Any],
    round_ref: str,
    chain: Mapping[str, Any],
) -> dict[str, Any]:
    refs = extraction.extraction_artifact_refs(round_ref)
    failed = [item["record"]["check_id"] for item in chain["receipts"] if item["record"]["exit_code"] != 0]
    bundle: dict[str, Any] | None = None
    mutation: dict[str, Any] | None = None
    parser: dict[str, Any] | None = None
    timeout_gate: dict[str, Any] | None = None
    ledger: dict[str, Any] | None = None
    if _action_success(chain, "generate_extraction_bundle"):
        bundle = extraction.verify_bundle_index(root, refs["bundle_index"])
        mutation_raw = _read(root, refs["mutation_matrix"])
        mutation = extraction.validate_mutation_matrix(_strict_json_bytes(mutation_raw, "mutation matrix"))
        ledger = extraction.verify_backend_ledger_index(root, refs["backend_ledger_index"])
        parser_verifier = getattr(extraction, "verify_parser_comparison", None)
        if parser_verifier is None:
            parser_raw = _read(root, refs["parser_comparison"])
            parser_record = _strict_json_bytes(parser_raw, "parser comparison")
            parser = {"sha256": content_digest(parser_raw), "record": parser_record}
        else:
            init = chain["receipts"][0]["record"]["bindings"]
            parser = parser_verifier(
                root,
                refs["parser_comparison"],
                implementation_manifest_ref=init["round_implementation_manifest_ref"],
            )
        timeout_gate = extraction.verify_parser_timeout_gate(
            root,
            round_ref,
            init["round_implementation_manifest_ref"],
        )
    backend_count = ledger["record"]["forbidden_attempt_count"] if ledger is not None else 0
    if ledger is None:
        for action in extraction.P02_GUARDED_ACTIONS:
            receipt = _receipt_for(chain, action)
            if receipt is None:
                continue
            ledger_ref = f"{round_ref}/ledgers/backend-invocations-{action}.jsonl"
            try:
                backend_count += len([line for line in _read(root, ledger_ref).splitlines() if line])
            except Exception:
                backend_count += 1
    init = chain["receipts"][0]["record"]["bindings"]
    immutable = _parse_manifest(_read(root, init["entry_immutable_input_manifest_ref"]))
    source_edit_count = 0
    for ref, expected_digest in immutable.items():
        try:
            if _digest(root, ref) != expected_digest:
                source_edit_count += 1
        except Exception:
            source_edit_count += 1
    source_gate = _receipt_for(chain, "zero_backend_source_edit_gate")
    if source_gate is not None and source_gate["exit_code"] == 0:
        source_edit_count = 0
    all_checks = not failed
    mutation_pass = mutation is not None and mutation["all_pass"] is True
    bundle_pass = bundle is not None and bundle["record"]["all_source_reconstructions_exact"] is True
    parser_pass = (
        parser is not None
        and parser["record"].get("current_reconstruction_exact") is True
        and parser["record"].get("parser_veto") is False
        and parser["record"].get("materially_better_specialist_count") == 0
        and timeout_gate is not None
        and timeout_gate["all_invocations_completed_within_ceiling"] is True
    )
    criteria = {
        "all_17_materialized_obligations_exact": bundle_pass and bundle["record"]["obligation_count"] == 17,
        "all_reviewed_source_spans_exact": bundle_pass,
        "all_grouping_and_ambiguity_outcomes_exact": mutation_pass and _action_success(chain, "localizer_tests"),
        "all_normalized_targets_and_inventories_exact": bundle_pass and _action_success(chain, "obligation_tests"),
        "all_identity_and_mutation_checks_pass": mutation_pass and _action_success(chain, "mutation_ambiguity_gate"),
        "frozen_positive_obligations_exact": bundle_pass and _action_success(chain, "frozen_regressions"),
        "proposition_container_exact": _action_success(chain, "frozen_regressions") and _action_success(chain, "target_integration_tests"),
        "parser_fidelity_contract_pass": parser_pass and _action_success(chain, "parser_fidelity_tests"),
        "zero_backend_requests": backend_count == 0 and _action_success(chain, "zero_backend_source_edit_gate"),
        "zero_source_edits": source_edit_count == 0 and _action_success(chain, "zero_backend_source_edit_gate"),
        "publication_quarantine_pass": _action_success(chain, "p00_quarantine"),
        "allowlist_and_protected_state_pass": all(
            _action_success(chain, item) for item in ("protected_check", "implementation_exit", "allowlist", "diff")
        ),
    }
    criteria["all_pass"] = all(criteria.values()) and all_checks
    vetoes = {key: False for key in profile["round_close_schema"]["veto_keys"]}
    if failed:
        vetoes["artifact_or_bundle_integrity_failure"] = True
    if backend_count != 0:
        vetoes["backend_execution_detected"] = True
    if source_edit_count != 0:
        vetoes["source_edit_detected"] = True
    if parser is not None and not parser_pass:
        vetoes["parser_fidelity_or_provenance_failure"] = True
    return {
        "bundle": bundle,
        "mutation": mutation,
        "parser": parser,
        "timeout_gate": timeout_gate,
        "backend_request_count": backend_count,
        "source_edit_count": source_edit_count,
        "primary_criterion": criteria,
        "vetoes": vetoes,
    }


def _build_phase_result(
    root: Path,
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    human_ref: str,
    human_raw: bytes,
) -> dict[str, Any]:
    measurements = _phase_measurements(root, profile, round_ref, chain)
    init = chain["receipts"][0]["record"]["bindings"]
    refs = extraction.extraction_artifact_refs(round_ref)
    bundle = measurements["bundle"]
    parser = measurements["parser"]
    mutation_ref = refs["mutation_matrix"] if measurements["mutation"] is not None else None
    decision = (
        "candidate_pass_pending_independent_result_review"
        if measurements["primary_criterion"]["all_pass"] and not any(measurements["vetoes"].values())
        else "blocked"
    )
    claimed = extraction.parse_human_result(
        human_raw,
        result_round=result_round,
        pre_result_index_sha256=chain["index_sha256"],
    )
    if claimed != decision:
        raise EvidenceValidationError("human result claimed decision differs from independent reconstruction")
    record = {
        "schema_version": profile["phase_result_schema"]["schema_version"],
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
        "p01_stable_decision_ref": init["p01_stable_decision_ref"],
        "p01_stable_decision_sha256": init["p01_stable_decision_sha256"],
        "p01_terminal_receipt_index_ref": init["p01_terminal_receipt_index_ref"],
        "p01_terminal_receipt_index_sha256": init["p01_terminal_receipt_index_sha256"],
        "reviewed_plan_ref": init["reviewed_plan_ref"],
        "reviewed_plan_sha256": init["reviewed_plan_sha256"],
        "reviewed_compact_oracle_ref": init["reviewed_compact_oracle_ref"],
        "reviewed_compact_oracle_sha256": init["reviewed_compact_oracle_sha256"],
        "reviewed_materialized_oracle_ref": init["reviewed_materialized_oracle_ref"],
        "reviewed_materialized_oracle_sha256": init["reviewed_materialized_oracle_sha256"],
        "extraction_bundle_index_ref": refs["bundle_index"] if bundle is not None else None,
        "extraction_bundle_index_sha256": bundle["sha256"] if bundle is not None else None,
        "parser_comparison_ref": refs["parser_comparison"] if parser is not None else None,
        "parser_comparison_sha256": parser["sha256"] if parser is not None else None,
        "mutation_ambiguity_matrix_ref": mutation_ref,
        "mutation_ambiguity_matrix_sha256": _digest(root, mutation_ref) if mutation_ref is not None else None,
        "backend_request_count": measurements["backend_request_count"],
        "source_edit_count": measurements["source_edit_count"],
        "primary_criterion": measurements["primary_criterion"],
        "vetoes": measurements["vetoes"],
        "non_claims": profile["round_close_schema"]["non_claims"],
    }
    return extraction.validate_phase_result(record, profile=dict(profile))


def _bind_result(
    root: Path,
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    human_ref = _fixed_ref(profile, "human_result", result_round, round_ref)
    human_raw = _read(root, human_ref)
    record = _build_phase_result(root, profile, round_ref, result_round, chain, human_ref, human_raw)
    result_ref = _fixed_ref(profile, "machine_result", result_round, round_ref)
    written = _write_json(root, result_ref, record)
    bindings = {
        "human_result_ref": human_ref,
        "human_result_sha256": content_digest(human_raw),
        "result_ref": result_ref,
        "result_sha256": written["sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


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


def _verify_phase_result(
    root: Path,
    profile: Mapping[str, Any],
    result_ref: str,
) -> dict[str, Any]:
    raw = _read(root, result_ref)
    record = extraction.validate_phase_result(_strict_json_bytes(raw, "P02 phase result"), profile=dict(profile))
    pre_chain = _verify_receipt_index(root, record["pre_result_receipt_index_ref"], profile)
    if pre_chain["index_sha256"] != record["pre_result_receipt_index_sha256"]:
        raise EvidenceValidationError("phase result pre-result receipt-index binding mismatch")
    human_raw = _read(root, record["human_result_ref"])
    if content_digest(human_raw) != record["human_result_sha256"]:
        raise EvidenceValidationError("phase result human-result binding mismatch")
    round_ref = f"{EVIDENCE_ROOT_REF}/result-rounds/{record['result_round']}"
    expected = _build_phase_result(
        root,
        profile,
        round_ref,
        record["result_round"],
        pre_chain,
        record["human_result_ref"],
        human_raw,
    )
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("phase result differs from independent reconstruction")
    return {"ref": result_ref, "sha256": content_digest(raw), "record": record, "pre_chain": pre_chain}


def _implementation_delta(
    root: Path,
    entry_ref: str,
    round_ref: str,
) -> tuple[list[dict[str, Any]], str]:
    before = _parse_manifest(_read(root, entry_ref))
    after = _parse_manifest(_read(root, round_ref))
    delta = [
        {"logical_ref": ref, "entry_sha256": before.get(ref), "round_sha256": after.get(ref)}
        for ref in sorted(set(before) | set(after), key=lambda item: item.encode("utf-8"))
        if before.get(ref) != after.get(ref)
    ]
    return delta, content_digest(delta)


def _frozen_source_digests(root: Path, effective: Mapping[str, Any]) -> dict[str, str]:
    declared: dict[str, str] = {}
    for item in effective["frozen_sources"]:
        ref = item["source_ref"]
        digest = _digest(root, ref)
        if digest != item["source_sha256"]:
            raise EvidenceValidationError(f"frozen source drift: {ref}")
        if ref in declared and declared[ref] != digest:
            raise EvidenceValidationError("frozen source has inconsistent reviewed digests")
        declared[ref] = digest
    if len(declared) != 2:
        raise EvidenceValidationError("frozen source digest map must contain exactly two documents")
    return declared


def _measured_parser_version_evidence(
    root: Path,
    effective: Mapping[str, Any],
    round_ref: str,
    parser: Mapping[str, Any],
) -> tuple[dict[str, dict[str, Any]], list[tuple[str, str]]]:
    profile = effective["parser_fidelity_profile"]
    bindings = parser["version_receipts"]
    if type(bindings) is not list or len(bindings) != len(profile["executables"]):
        raise EvidenceValidationError("parser comparison version receipt closure mismatch")
    by_backend = {item.get("backend"): item for item in bindings if type(item) is dict}
    if len(by_backend) != len(bindings) or set(by_backend) != set(profile["executables"]):
        raise EvidenceValidationError("parser comparison version receipt registry mismatch")

    evidence: dict[str, dict[str, Any]] = {}
    inventory_refs: list[tuple[str, str]] = []
    for backend, executable in profile["executables"].items():
        verified = extraction.verify_parser_version_receipt(
            root,
            round_ref,
            backend,
            profile=profile,
        )
        binding = by_backend[backend]
        expected_binding = {
            "backend": backend,
            "receipt_ref": verified["ref"],
            "receipt_sha256": verified["sha256"],
            "version_matches": verified["version_matches"],
        }
        if binding != expected_binding or verified["version_matches"] is not True:
            raise EvidenceValidationError(f"{backend} version evidence does not match its raw receipt")
        evidence[backend] = {
            "evidence_type": "measured_parser_version_receipt",
            "measured_version": executable["measured_version"],
            "version_matches": True,
            "version_receipt_ref": verified["ref"],
            "version_receipt_sha256": verified["sha256"],
        }
        inventory_refs.append((verified["ref"], f"{backend}_parser_version_receipt"))
    return evidence, inventory_refs


def _build_run_manifest_record(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> dict[str, Any]:
    bind = _receipt_for(chain, "bind_result")
    if bind is None or bind["exit_code"] != 0:
        raise EvidenceValidationError("run manifest requires a successful bind_result receipt")
    result = _verify_phase_result(root, profile, bind["bindings"]["result_ref"])
    init_receipt = chain["receipts"][0]["record"]
    init = init_receipt["bindings"]
    delta, delta_digest = _implementation_delta(
        root,
        init["entry_implementation_manifest_ref"],
        init["round_implementation_manifest_ref"],
    )
    artifact_refs: list[tuple[str, str]] = []
    for item in chain["receipts"]:
        receipt = item["record"]
        artifact_refs.extend(
            (
                (item["entry"]["receipt_ref"], f"{receipt['check_id']}_receipt"),
                (receipt["stdout_ref"], f"{receipt['check_id']}_stdout"),
                (receipt["stderr_ref"], f"{receipt['check_id']}_stderr"),
            )
        )
    artifact_refs.extend(
        [
            (chain["index_ref"], "pre_candidate_receipt_index"),
            (result["ref"], "machine_phase_result"),
            (result["record"]["human_result_ref"], "human_phase_result"),
            (init["entry_record_ref"], "entry_record"),
            (init["round_implementation_manifest_ref"], "round_implementation_manifest"),
        ]
    )
    bundle_ref = result["record"]["extraction_bundle_index_ref"]
    if bundle_ref is not None:
        bundle = extraction.verify_bundle_index(root, bundle_ref)
        artifact_refs.append((bundle_ref, "extraction_bundle_index"))
        artifact_refs.extend(
            (item["logical_ref"], item["role"])
            for item in bundle["record"]["artifact_inventory"]
        )
    parser_versions: dict[str, dict[str, Any]] = {
        backend: {
            "evidence_type": "not_measured_in_blocked_round",
            "measured_version": None,
            "version_matches": None,
            "version_receipt_ref": None,
            "version_receipt_sha256": None,
        }
        for backend in effective["parser_fidelity_profile"]["executables"]
    }
    parser_ref = result["record"]["parser_comparison_ref"]
    if parser_ref is not None:
        parser = extraction.verify_parser_comparison(
            root,
            parser_ref,
            implementation_manifest_ref=init["round_implementation_manifest_ref"],
        )["record"]
        parser_versions, version_inventory = _measured_parser_version_evidence(
            root,
            effective,
            round_ref,
            parser,
        )
        artifact_refs.extend(version_inventory)
    record = {
        "schema_version": "p02_extraction_run_manifest@1",
        "phase": PHASE,
        "result_round": result_round,
        "git_commit": extraction.current_git_commit(root),
        "started_at_utc": init_receipt["started_at_utc"],
        "ended_at_utc": chain["receipts"][-1]["record"]["ended_at_utc"],
        "wall_time_ns": sum(item["record"]["wall_time_ns"] for item in chain["receipts"]),
        "environment": {
            "python_executable": PYTHON,
            "python_version": sys.version.split()[0],
            "pythonpath": "src",
            "locale": "C.UTF-8",
        },
        "device_execution": {
            "mode": "cpu_only_parser_and_test_execution",
            "gpu_requested": False,
            "gpu_initialized": False,
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
        "implementation_delta_digest": delta_digest,
        "source_data_version": "p02r2-reviewed-fixture-and-frozen-source-corpus-20260712",
        "frozen_source_digests": _frozen_source_digests(root, effective),
        "external_tool_considerations": [
            {
                "tool": "current_byte_preserving_scanner",
                "role": "primary exact source reconstruction",
                "availability_version_evidence": {
                    "evidence_type": "embedded_version",
                    "measured_version": "p02_lightweight_locator@1",
                },
                "selected": True,
                "certifying_status": "noncertifying_extraction",
            },
            {
                "tool": "LaTeXML",
                "role": "diagnostic structural parser",
                "availability_version_evidence": parser_versions["latexml"],
                "selected": False,
                "certifying_status": "diagnostic_only_unless_source_mappable",
            },
            {
                "tool": "Pandoc",
                "role": "diagnostic structural parser",
                "availability_version_evidence": parser_versions["pandoc"],
                "selected": False,
                "certifying_status": "diagnostic_only_unless_source_mappable",
            },
            {
                "tool": "SymPy_Sage_Lean_and_proof_search_backends",
                "role": "later semantic or mathematical checking",
                "availability_version_evidence": {
                    "evidence_type": "not_invoked",
                    "measured_version": None,
                },
                "selected": False,
                "certifying_status": "forbidden_by_phase02_boundary",
            },
        ],
        "artifact_inventory": _artifact_inventory(root, artifact_refs),
        "non_claims": profile["round_close_schema"]["non_claims"],
    }
    _ = delta
    return extraction.validate_run_manifest(
        record,
        parser_profile=effective["parser_fidelity_profile"],
    )


def _verify_run_manifest(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    ref: str,
) -> dict[str, Any]:
    raw = _read(root, ref)
    record = extraction.validate_run_manifest(
        _strict_json_bytes(raw, "P02 run manifest"),
        parser_profile=effective["parser_fidelity_profile"],
    )
    chain = _verify_receipt_index(root, record["pre_candidate_receipt_index_ref"], profile)
    if chain["index_sha256"] != record["pre_candidate_receipt_index_sha256"]:
        raise EvidenceValidationError("run manifest receipt-index binding mismatch")
    round_ref = f"{EVIDENCE_ROOT_REF}/result-rounds/{record['result_round']}"
    expected = _build_run_manifest_record(root, effective, profile, round_ref, record["result_round"], chain)
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("run manifest differs from independent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record, "chain": chain}


def _build_run_manifest(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    record = _build_run_manifest_record(root, effective, profile, round_ref, result_round, chain)
    ref = _fixed_ref(profile, "run_manifest", result_round, round_ref)
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
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> dict[str, Any]:
    run_receipt = _receipt_for(chain, "build_run_manifest")
    if run_receipt is None or run_receipt["exit_code"] != 0:
        raise EvidenceValidationError("candidate construction requires a successful run-manifest receipt")
    run = _verify_run_manifest(root, effective, profile, run_receipt["bindings"]["run_manifest_ref"])
    result = _verify_phase_result(root, profile, run["record"]["result_ref"])
    if result["record"]["decision"] != "candidate_pass_pending_independent_result_review":
        raise EvidenceValidationError("blocked phase result cannot produce a candidate pass")
    init = chain["receipts"][0]["record"]["bindings"]
    bundle = extraction.verify_bundle_index(root, result["record"]["extraction_bundle_index_ref"])
    refs = extraction.extraction_artifact_refs(round_ref)
    record = {
        "schema_version": "p02_candidate_decision@1",
        "phase": PHASE,
        "result_round": result_round,
        "decision": "candidate_pass_pending_independent_result_review",
        "publication_mode": "disabled",
        "claim_eligibility": "ineligible",
        "entry_record_ref": init["entry_record_ref"],
        "entry_record_sha256": init["entry_record_sha256"],
        "p01_stable_decision_ref": init["p01_stable_decision_ref"],
        "p01_stable_decision_sha256": init["p01_stable_decision_sha256"],
        "p01_terminal_receipt_index_ref": init["p01_terminal_receipt_index_ref"],
        "p01_terminal_receipt_index_sha256": init["p01_terminal_receipt_index_sha256"],
        "reviewed_plan_ref": init["reviewed_plan_ref"],
        "reviewed_plan_sha256": init["reviewed_plan_sha256"],
        "reviewed_compact_oracle_ref": init["reviewed_compact_oracle_ref"],
        "reviewed_compact_oracle_sha256": init["reviewed_compact_oracle_sha256"],
        "reviewed_materialized_oracle_ref": init["reviewed_materialized_oracle_ref"],
        "reviewed_materialized_oracle_sha256": init["reviewed_materialized_oracle_sha256"],
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
        "extraction_bundle_index_ref": bundle["ref"],
        "extraction_bundle_index_sha256": bundle["sha256"],
        "extraction_bundle_semantic_digest": bundle["record"]["semantic_digest"],
        "parser_comparison_ref": refs["parser_comparison"],
        "parser_comparison_sha256": _digest(root, refs["parser_comparison"]),
        "mutation_ambiguity_matrix_ref": refs["mutation_matrix"],
        "mutation_ambiguity_matrix_sha256": _digest(root, refs["mutation_matrix"]),
        "backend_ledger_index_ref": refs["backend_ledger_index"],
        "backend_ledger_index_sha256": _digest(root, refs["backend_ledger_index"]),
        "frozen_source_digests": _frozen_source_digests(root, effective),
        "backend_request_count": result["record"]["backend_request_count"],
        "source_edit_count": result["record"]["source_edit_count"],
        "primary_criterion": result["record"]["primary_criterion"],
        "vetoes": result["record"]["vetoes"],
        "non_claims": profile["round_close_schema"]["non_claims"],
    }
    return extraction.validate_candidate(record)


def _verify_candidate(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    ref: str,
) -> dict[str, Any]:
    raw = _read(root, ref)
    record = extraction.validate_candidate(_strict_json_bytes(raw, "P02 candidate"))
    chain = _verify_receipt_index(root, record["pre_candidate_receipt_index_ref"], profile)
    if chain["index_sha256"] != record["pre_candidate_receipt_index_sha256"]:
        raise EvidenceValidationError("candidate receipt-index binding mismatch")
    round_ref = f"{EVIDENCE_ROOT_REF}/result-rounds/{record['result_round']}"
    expected = _build_candidate_record(root, effective, profile, round_ref, record["result_round"], chain)
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("candidate differs from independent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record, "chain": chain}


def _build_candidate(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    record = _build_candidate_record(root, effective, profile, round_ref, result_round, chain)
    ref = _fixed_ref(profile, "candidate", result_round, round_ref)
    written = _write_json(root, ref, record)
    bindings = {
        "candidate_ref": ref,
        "candidate_sha256": written["sha256"],
        "run_manifest_ref": record["run_manifest_ref"],
        "run_manifest_sha256": record["run_manifest_sha256"],
        "bound_receipt_index_ref": chain["index_ref"],
        "bound_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _candidate_gate(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    build = chain["receipts"][-1]["record"]
    if build["check_id"] != "build_candidate" or build["exit_code"] != 0:
        raise EvidenceValidationError("candidate gate requires a successful build-candidate head")
    candidate = _verify_candidate(root, effective, profile, build["bindings"]["candidate_ref"])
    if candidate["sha256"] != build["bindings"]["candidate_sha256"]:
        raise EvidenceValidationError("candidate build receipt binding mismatch")
    log = {
        "schema_version": "p02_candidate_validation@1",
        "result_round": result_round,
        "candidate_ref": candidate["ref"],
        "candidate_sha256": candidate["sha256"],
        "validated_receipt_index_ref": chain["index_ref"],
        "validated_receipt_index_sha256": chain["index_sha256"],
        "status": "PASS",
    }
    log_ref = _fixed_ref(profile, "candidate_validation_log", result_round, round_ref)
    written = _write_json(root, log_ref, log)
    bindings = {
        "candidate_ref": candidate["ref"],
        "candidate_sha256": candidate["sha256"],
        "validation_log_ref": log_ref,
        "validation_log_sha256": written["sha256"],
        "validated_receipt_index_ref": chain["index_ref"],
        "validated_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(log), b"", bindings


def _result_review_binding(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
    artifact_ref: str,
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    expected_ref = profile["actions"]["result_review_binding"]["artifact_ref_template"].replace(
        "RESULT_ROUND", result_round
    )
    if artifact_ref != expected_ref:
        raise EvidenceValidationError("result-review artifact ref is not the exact round-specific ref")
    gate = chain["receipts"][-1]["record"]
    if gate["check_id"] != "candidate_gate" or gate["exit_code"] != 0:
        raise EvidenceValidationError("result review requires a successful candidate-gate head")
    candidate = _verify_candidate(root, effective, profile, gate["bindings"]["candidate_ref"])
    gate_log = _strict_json(root, gate["bindings"]["validation_log_ref"], "candidate validation log")
    if (
        _digest(root, gate["bindings"]["validation_log_ref"]) != gate["bindings"]["validation_log_sha256"]
        or gate_log.get("status") != "PASS"
        or gate_log.get("candidate_sha256") != candidate["sha256"]
        or gate_log.get("validated_receipt_index_sha256") != gate["bindings"]["validated_receipt_index_sha256"]
    ):
        raise EvidenceValidationError("result review candidate-gate log binding mismatch")
    review_raw = _read(root, expected_ref)
    expected_bindings = {
        "Reviewed result round": result_round,
        "Reviewed candidate SHA-256": candidate["sha256"],
        "Reviewed run manifest SHA-256": candidate["record"]["run_manifest_sha256"],
        "Reviewed result SHA-256": candidate["record"]["result_sha256"],
        "Reviewed extraction bundle semantic digest": candidate["record"]["extraction_bundle_semantic_digest"],
        "Reviewed extraction bundle-index SHA-256": candidate["record"]["extraction_bundle_index_sha256"],
        "Reviewed parser comparison SHA-256": candidate["record"]["parser_comparison_sha256"],
        "Reviewed mutation/ambiguity matrix SHA-256": candidate["record"]["mutation_ambiguity_matrix_sha256"],
        "Reviewed governance receipt-index SHA-256": chain["index_sha256"],
    }
    verdict = extraction.parse_review(review_raw, expected_bindings=expected_bindings, kind="result review")
    bindings = {
        "review_ref": expected_ref,
        "review_sha256": content_digest(review_raw),
        "review_verdict": verdict,
        "candidate_ref": candidate["ref"],
        "candidate_sha256": candidate["sha256"],
        "reviewed_receipt_index_ref": chain["index_ref"],
        "reviewed_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, f"VERDICT={verdict}\n".encode(), b"", bindings


def _build_final_record(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    chain: Mapping[str, Any],
) -> dict[str, Any]:
    review_receipt = chain["receipts"][-1]["record"]
    if (
        review_receipt["check_id"] != "result_review_binding"
        or review_receipt["exit_code"] != 0
        or review_receipt["bindings"]["review_verdict"] != "AGREE"
    ):
        raise EvidenceValidationError("final candidate requires an agreeing result-review head")
    candidate = _verify_candidate(root, effective, profile, review_receipt["bindings"]["candidate_ref"])
    review_raw = _read(root, review_receipt["bindings"]["review_ref"])
    if content_digest(review_raw) != review_receipt["bindings"]["review_sha256"]:
        raise EvidenceValidationError("final candidate result-review binding drift")
    reviewed_chain = _verify_receipt_index(root, review_receipt["bindings"]["reviewed_receipt_index_ref"], profile)
    if reviewed_chain["index_sha256"] != review_receipt["bindings"]["reviewed_receipt_index_sha256"]:
        raise EvidenceValidationError("final candidate reviewed receipt-index binding drift")
    gate = reviewed_chain["receipts"][-1]["record"]
    if gate["check_id"] != "candidate_gate" or gate["exit_code"] != 0:
        raise EvidenceValidationError("final candidate review did not bind a candidate-gate head")
    expected_review_bindings = {
        "Reviewed result round": candidate["record"]["result_round"],
        "Reviewed candidate SHA-256": candidate["sha256"],
        "Reviewed run manifest SHA-256": candidate["record"]["run_manifest_sha256"],
        "Reviewed result SHA-256": candidate["record"]["result_sha256"],
        "Reviewed extraction bundle semantic digest": candidate["record"]["extraction_bundle_semantic_digest"],
        "Reviewed extraction bundle-index SHA-256": candidate["record"]["extraction_bundle_index_sha256"],
        "Reviewed parser comparison SHA-256": candidate["record"]["parser_comparison_sha256"],
        "Reviewed mutation/ambiguity matrix SHA-256": candidate["record"]["mutation_ambiguity_matrix_sha256"],
        "Reviewed governance receipt-index SHA-256": reviewed_chain["index_sha256"],
    }
    if (
        extraction.parse_review(review_raw, expected_bindings=expected_review_bindings, kind="result review")
        != "AGREE"
    ):
        raise EvidenceValidationError("final candidate result review is not independently agreeing")
    init = chain["receipts"][0]["record"]["bindings"]
    record = {
        "schema_version": "p02_final_decision@1",
        "phase": PHASE,
        "result_round": candidate["record"]["result_round"],
        "decision": "pass",
        "publication_mode": "disabled",
        "candidate_decision_ref": candidate["ref"],
        "candidate_decision_sha256": candidate["sha256"],
        "result_review_ref": review_receipt["bindings"]["review_ref"],
        "result_review_sha256": review_receipt["bindings"]["review_sha256"],
        "reviewed_receipt_index_ref": chain["index_ref"],
        "reviewed_receipt_index_sha256": chain["index_sha256"],
        "p01_stable_decision_ref": init["p01_stable_decision_ref"],
        "p01_stable_decision_sha256": init["p01_stable_decision_sha256"],
        "extraction_bundle_semantic_digest": candidate["record"]["extraction_bundle_semantic_digest"],
        "primary_criterion": candidate["record"]["primary_criterion"],
        "vetoes": candidate["record"]["vetoes"],
        "non_claims": profile["round_close_schema"]["non_claims"],
    }
    return extraction.validate_final(record)


def _verify_final(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    ref: str,
) -> dict[str, Any]:
    raw = _read(root, ref)
    record = extraction.validate_final(_strict_json_bytes(raw, "P02 final decision"))
    chain = _verify_receipt_index(root, record["reviewed_receipt_index_ref"], profile)
    if chain["index_sha256"] != record["reviewed_receipt_index_sha256"]:
        raise EvidenceValidationError("final candidate receipt-index binding mismatch")
    expected = _build_final_record(root, effective, profile, chain)
    if canonical_json_bytes(record) != canonical_json_bytes(expected):
        raise EvidenceValidationError("final candidate differs from independent reconstruction")
    return {"ref": ref, "sha256": content_digest(raw), "record": record, "chain": chain}


def _build_final_candidate(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    record = _build_final_record(root, effective, profile, chain)
    ref = _fixed_ref(profile, "final_candidate", result_round, round_ref)
    written = _write_json(root, ref, record)
    bindings = {
        "final_candidate_ref": ref,
        "final_candidate_sha256": written["sha256"],
        "review_ref": record["result_review_ref"],
        "review_sha256": record["result_review_sha256"],
        "reviewed_receipt_index_ref": chain["index_ref"],
        "reviewed_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _final_candidate_gate(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    build = chain["receipts"][-1]["record"]
    if build["check_id"] != "build_final_candidate" or build["exit_code"] != 0:
        raise EvidenceValidationError("final gate requires a successful build-final-candidate head")
    final = _verify_final(root, effective, profile, build["bindings"]["final_candidate_ref"])
    if final["sha256"] != build["bindings"]["final_candidate_sha256"]:
        raise EvidenceValidationError("final build receipt binding mismatch")
    log = {
        "schema_version": "p02_final_candidate_validation@1",
        "result_round": result_round,
        "final_candidate_ref": final["ref"],
        "final_candidate_sha256": final["sha256"],
        "validated_receipt_index_ref": chain["index_ref"],
        "validated_receipt_index_sha256": chain["index_sha256"],
        "status": "PASS",
    }
    log_ref = _fixed_ref(profile, "final_validation_log", result_round, round_ref)
    written = _write_json(root, log_ref, log)
    bindings = {
        "final_candidate_ref": final["ref"],
        "final_candidate_sha256": final["sha256"],
        "validation_log_ref": log_ref,
        "validation_log_sha256": written["sha256"],
        "validated_receipt_index_ref": chain["index_ref"],
        "validated_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(log), b"", bindings


def _final_seal_audit_binding(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    result_round: str,
    chain: Mapping[str, Any],
    artifact_ref: str,
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    expected_ref = profile["actions"]["final_seal_audit_binding"]["artifact_ref_template"].replace(
        "RESULT_ROUND", result_round
    )
    if artifact_ref != expected_ref:
        raise EvidenceValidationError("final-seal artifact ref is not the exact round-specific ref")
    gate = chain["receipts"][-1]["record"]
    if gate["check_id"] != "final_candidate_gate" or gate["exit_code"] != 0:
        raise EvidenceValidationError("final-seal audit requires a successful final-candidate gate")
    final = _verify_final(root, effective, profile, gate["bindings"]["final_candidate_ref"])
    candidate_ref = final["record"]["candidate_decision_ref"]
    gate_log = _strict_json(root, gate["bindings"]["validation_log_ref"], "final validation log")
    if (
        _digest(root, gate["bindings"]["validation_log_ref"]) != gate["bindings"]["validation_log_sha256"]
        or gate_log.get("status") != "PASS"
        or gate_log.get("final_candidate_sha256") != final["sha256"]
        or gate_log.get("validated_receipt_index_sha256") != gate["bindings"]["validated_receipt_index_sha256"]
    ):
        raise EvidenceValidationError("final-seal audit validation-log binding mismatch")
    audit_raw = _read(root, expected_ref)
    expected_bindings = {
        "Audited result round": result_round,
        "Audited final-decision candidate SHA-256": final["sha256"],
        "Audited candidate SHA-256": final["record"]["candidate_decision_sha256"],
        "Audited result-review SHA-256": final["record"]["result_review_sha256"],
        "Audited final-candidate validation-log SHA-256": gate["bindings"]["validation_log_sha256"],
        "Audited governance receipt-index SHA-256": chain["index_sha256"],
    }
    verdict = extraction.parse_review(audit_raw, expected_bindings=expected_bindings, kind="final-seal audit")
    bindings = {
        "audit_ref": expected_ref,
        "audit_sha256": content_digest(audit_raw),
        "audit_verdict": verdict,
        "final_candidate_ref": final["ref"],
        "final_candidate_sha256": final["sha256"],
        "candidate_ref": candidate_ref,
        "candidate_sha256": final["record"]["candidate_decision_sha256"],
        "review_ref": final["record"]["result_review_ref"],
        "review_sha256": final["record"]["result_review_sha256"],
        "validation_log_ref": gate["bindings"]["validation_log_ref"],
        "validation_log_sha256": gate["bindings"]["validation_log_sha256"],
        "audited_receipt_index_ref": chain["index_ref"],
        "audited_receipt_index_sha256": chain["index_sha256"],
    }
    return 0, f"VERDICT={verdict}\n".encode(), b"", bindings


def _validate_scoped_repair(
    root: Path,
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> dict[str, Any]:
    ref = _fixed_ref(profile, "scoped_repair", result_round, round_ref)
    record = _strict_json(root, ref, "P02 scoped repair")
    schema = profile["scoped_repair_schema"]
    if set(record) != set(schema["exact_keys"]) or record["schema_version"] != schema["schema_version"]:
        raise EvidenceValidationError("P02 scoped-repair schema mismatch")
    if record["phase"] != PHASE or record["result_round"] != result_round or record["close_reason"] not in schema["close_reasons"]:
        raise EvidenceValidationError("P02 scoped-repair metadata mismatch")
    failed = [item["record"]["check_id"] for item in chain["receipts"] if item["record"]["exit_code"] != 0]
    latest = chain["receipts"][-1]["record"]
    if record["close_reason"] == "measured_action_failure":
        if not failed or record["failed_actions"] != failed:
            raise EvidenceValidationError("measured-failure scoped repair has wrong failed actions")
        trigger = next(item for item in chain["receipts"] if item["record"]["exit_code"] != 0)
        expected_artifact = trigger["entry"]["receipt_ref"]
        expected_index = _index_ref(round_ref, trigger["record"]["sequence"])
    elif record["close_reason"] == "result_review_revise":
        if failed or latest["check_id"] != "result_review_binding" or latest["bindings"]["review_verdict"] != "REVISE":
            raise EvidenceValidationError("result-review repair does not follow measured REVISE")
        if record["failed_actions"] != []:
            raise EvidenceValidationError("review REVISE repair must have no failed actions")
        expected_artifact = latest["bindings"]["review_ref"]
        expected_index = chain["index_ref"]
    else:
        if failed or latest["check_id"] != "final_seal_audit_binding" or latest["bindings"]["audit_verdict"] != "REVISE":
            raise EvidenceValidationError("final-seal repair does not follow measured REVISE")
        if record["failed_actions"] != []:
            raise EvidenceValidationError("audit REVISE repair must have no failed actions")
        expected_artifact = latest["bindings"]["audit_ref"]
        expected_index = chain["index_ref"]
    source_index = _verify_receipt_index(root, record["source_receipt_index_ref"], profile)
    if (
        record["source_artifact_ref"] != expected_artifact
        or record["source_artifact_sha256"] != _digest(root, expected_artifact)
        or record["source_receipt_index_ref"] != expected_index
        or record["source_receipt_index_sha256"] != source_index["index_sha256"]
    ):
        raise EvidenceValidationError("scoped-repair trigger binding mismatch")
    repairs = record["repairs"]
    if type(repairs) is not list or not repairs:
        raise EvidenceValidationError("scoped-repair repairs must be a nonempty list")
    allowed_paths = set(extraction.implementation_allowlist(root))
    check_order = profile["action_order"][1:23]
    finding_ids: set[str] = set()
    for repair in repairs:
        if set(repair) != set(schema["repair_entry_exact_keys"]):
            raise EvidenceValidationError("scoped-repair entry keys mismatch")
        if not isinstance(repair["finding_id"], str) or not repair["finding_id"] or repair["finding_id"] in finding_ids:
            raise EvidenceValidationError("scoped-repair finding id is invalid or duplicated")
        finding_ids.add(repair["finding_id"])
        if repair["source_stage"] not in schema["repair_source_stage_enum"] or repair["severity"] not in schema["repair_severity_enum"]:
            raise EvidenceValidationError("scoped-repair source stage or severity mismatch")
        paths = repair["affected_paths"]
        if paths != sorted(set(paths), key=lambda item: item.encode("utf-8")) or not paths or not set(paths) <= allowed_paths:
            raise EvidenceValidationError("scoped-repair affected paths are outside the reviewed allowlist")
        required = repair["required_check_ids"]
        if not required or len(required) != len(set(required)) or any(item not in check_order for item in required):
            raise EvidenceValidationError("scoped-repair required checks mismatch")
        if [check_order.index(item) for item in required] != sorted(check_order.index(item) for item in required):
            raise EvidenceValidationError("scoped-repair required checks are not in action order")
        if repair["non_claim"] != schema["non_claim_literal"] or not repair["required_change"]:
            raise EvidenceValidationError("scoped-repair text contract mismatch")
    return {"ref": ref, "sha256": _digest(root, ref), "record": record}


def _bind_scoped_repair(
    root: Path,
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    repair = _validate_scoped_repair(root, profile, round_ref, result_round, chain)
    record = repair["record"]
    bindings = {
        "scoped_repair_ref": repair["ref"],
        "scoped_repair_sha256": repair["sha256"],
        "source_artifact_ref": record["source_artifact_ref"],
        "source_artifact_sha256": record["source_artifact_sha256"],
        "source_receipt_index_ref": record["source_receipt_index_ref"],
        "source_receipt_index_sha256": record["source_receipt_index_sha256"],
        "receipt_index_before_repair_ref": chain["index_ref"],
        "receipt_index_before_repair_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _close_round(
    root: Path,
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    binding = chain["receipts"][-1]["record"]
    if binding["check_id"] != "bind_scoped_repair" or binding["exit_code"] != 0:
        raise EvidenceValidationError("close-round requires a successful bind-scoped-repair head")
    repair = _validate_scoped_repair(
        root,
        profile,
        round_ref,
        result_round,
        _verify_receipt_index(root, binding["bindings"]["receipt_index_before_repair_ref"], profile),
    )
    init = chain["receipts"][0]["record"]["bindings"]
    stage_specs = (
        ("bind_result", "human_result_ref", "human_result_sha256"),
        ("bind_result", "result_ref", "result_sha256"),
        ("build_run_manifest", "run_manifest_ref", "run_manifest_sha256"),
        ("build_candidate", "candidate_ref", "candidate_sha256"),
        ("candidate_gate", "validation_log_ref", "validation_log_sha256"),
        ("result_review_binding", "review_ref", "review_sha256"),
        ("build_final_candidate", "final_candidate_ref", "final_candidate_sha256"),
        ("final_candidate_gate", "validation_log_ref", "validation_log_sha256"),
        ("final_seal_audit_binding", "audit_ref", "audit_sha256"),
    )
    pairs = [_receipt_pair(chain, *spec) for spec in stage_specs]
    review_receipt = _receipt_for(chain, "result_review_binding")
    audit_receipt = _receipt_for(chain, "final_seal_audit_binding")
    log_inventory = []
    for item in chain["receipts"]:
        receipt = item["record"]
        for stream in ("stdout", "stderr"):
            raw = _read(root, receipt[f"{stream}_ref"])
            log_inventory.append(
                {
                    "logical_ref": receipt[f"{stream}_ref"],
                    "sha256": content_digest(raw),
                    "byte_count": len(raw),
                    "role": f"{receipt['check_id']}_{stream}",
                    "exit_code": receipt["exit_code"],
                }
            )
    vetoes = {key: False for key in profile["round_close_schema"]["veto_keys"]}
    vetoes["artifact_or_bundle_integrity_failure"] = repair["record"]["close_reason"] == "measured_action_failure"
    vetoes["independent_review_not_agreed"] = repair["record"]["close_reason"] in {
        "result_review_revise",
        "final_seal_audit_revise",
    }
    backend_ref = extraction.extraction_artifact_refs(round_ref)["backend_ledger_index"]
    if (root / backend_ref).is_file() and not (root / backend_ref).is_symlink():
        try:
            if extraction.verify_backend_ledger_index(root, backend_ref)["record"]["forbidden_attempt_count"] != 0:
                vetoes["backend_execution_detected"] = True
        except Exception:
            pass
    entry_immutable = _parse_manifest(_read(root, init["entry_immutable_input_manifest_ref"]))
    effective_profile = extraction.load_profile(root)[0]
    changed_immutable = []
    for ref, expected_digest in entry_immutable.items():
        try:
            if _digest(root, ref) != expected_digest:
                changed_immutable.append(ref)
        except Exception:
            changed_immutable.append(ref)
    if changed_immutable:
        vetoes["source_edit_detected"] = True
        frozen_refs = {item["source_ref"] for item in effective_profile["frozen_sources"]}
        if set(changed_immutable) & frozen_refs:
            vetoes["frozen_source_digest_failure"] = True
    allowlist_receipt = _receipt_for(chain, "allowlist")
    if allowlist_receipt is not None and allowlist_receipt["exit_code"] != 0:
        unexpected_ref = f"{round_ref}/unexpected-paths.txt"
        try:
            if _read(root, unexpected_ref):
                vetoes["unexpected_implementation_path"] = True
        except Exception:
            pass
    parser_ref = extraction.extraction_artifact_refs(round_ref)["parser_comparison"]
    if (root / parser_ref).is_file() and not (root / parser_ref).is_symlink():
        try:
            parser = extraction.verify_parser_comparison(
                root,
                parser_ref,
                implementation_manifest_ref=init["round_implementation_manifest_ref"],
            )["record"]
            if parser["parser_veto"] or not parser["current_reconstruction_exact"]:
                vetoes["parser_fidelity_or_provenance_failure"] = True
        except Exception:
            pass
    record = {
        "schema_version": profile["round_close_schema"]["schema_version"],
        "phase": PHASE,
        "result_round": result_round,
        "decision": "blocked",
        "publication_mode": "disabled",
        "close_reason": repair["record"]["close_reason"],
        "failed_actions": repair["record"]["failed_actions"],
        "human_result_ref": pairs[0][0],
        "human_result_sha256": pairs[0][1],
        "entry_implementation_manifest_ref": init["entry_implementation_manifest_ref"],
        "entry_implementation_manifest_sha256": init["entry_implementation_manifest_sha256"],
        "round_implementation_manifest_ref": init["round_implementation_manifest_ref"],
        "round_implementation_manifest_sha256": init["round_implementation_manifest_sha256"],
        "entry_protected_manifest_ref": init["entry_protected_manifest_ref"],
        "entry_protected_manifest_sha256": init["entry_protected_manifest_sha256"],
        "entry_immutable_input_manifest_ref": init["entry_immutable_input_manifest_ref"],
        "entry_immutable_input_manifest_sha256": init["entry_immutable_input_manifest_sha256"],
        "p01_stable_decision_ref": init["p01_stable_decision_ref"],
        "p01_stable_decision_sha256": init["p01_stable_decision_sha256"],
        "p01_terminal_receipt_index_ref": init["p01_terminal_receipt_index_ref"],
        "p01_terminal_receipt_index_sha256": init["p01_terminal_receipt_index_sha256"],
        "predecessor_round_close_ref": init["predecessor_round_close_ref"],
        "predecessor_round_close_sha256": init["predecessor_round_close_sha256"],
        "predecessor_terminal_receipt_index_ref": init["predecessor_terminal_receipt_index_ref"],
        "predecessor_terminal_receipt_index_sha256": init["predecessor_terminal_receipt_index_sha256"],
        "scoped_repair_ref": repair["ref"],
        "scoped_repair_sha256": repair["sha256"],
        "source_artifact_ref": repair["record"]["source_artifact_ref"],
        "source_artifact_sha256": repair["record"]["source_artifact_sha256"],
        "source_receipt_index_ref": repair["record"]["source_receipt_index_ref"],
        "source_receipt_index_sha256": repair["record"]["source_receipt_index_sha256"],
        "receipt_index_before_repair_ref": binding["bindings"]["receipt_index_before_repair_ref"],
        "receipt_index_before_repair_sha256": binding["bindings"]["receipt_index_before_repair_sha256"],
        "receipt_index_before_close_ref": chain["index_ref"],
        "receipt_index_before_close_sha256": chain["index_sha256"],
        "result_ref": pairs[1][0],
        "result_sha256": pairs[1][1],
        "run_manifest_ref": pairs[2][0],
        "run_manifest_sha256": pairs[2][1],
        "candidate_ref": pairs[3][0],
        "candidate_sha256": pairs[3][1],
        "candidate_validation_log_ref": pairs[4][0],
        "candidate_validation_log_sha256": pairs[4][1],
        "result_review_ref": pairs[5][0],
        "result_review_sha256": pairs[5][1],
        "result_review_verdict": review_receipt["bindings"]["review_verdict"] if review_receipt and review_receipt["exit_code"] == 0 else None,
        "final_candidate_ref": pairs[6][0],
        "final_candidate_sha256": pairs[6][1],
        "final_validation_log_ref": pairs[7][0],
        "final_validation_log_sha256": pairs[7][1],
        "final_seal_audit_ref": pairs[8][0],
        "final_seal_audit_sha256": pairs[8][1],
        "final_seal_audit_verdict": audit_receipt["bindings"]["audit_verdict"] if audit_receipt and audit_receipt["exit_code"] == 0 else None,
        "log_inventory": log_inventory,
        "vetoes": vetoes,
        "non_claims": profile["round_close_schema"]["non_claims"],
        "repairs": repair["record"]["repairs"],
    }
    close_ref = _fixed_ref(profile, "round_close", result_round, round_ref)
    written = _write_json(root, close_ref, record)
    _validate_round_close(root, close_ref, profile)
    bindings = {
        "scoped_repair_ref": repair["ref"],
        "scoped_repair_sha256": repair["sha256"],
        "round_close_ref": close_ref,
        "round_close_sha256": written["sha256"],
        "receipt_index_before_close_ref": chain["index_ref"],
        "receipt_index_before_close_sha256": chain["index_sha256"],
    }
    return 0, canonical_json_bytes(bindings), b"", bindings


def _stable_publication(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    chain: Mapping[str, Any],
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    audit = chain["receipts"][-1]["record"]
    if (
        audit["check_id"] != "final_seal_audit_binding"
        or audit["exit_code"] != 0
        or audit["bindings"]["audit_verdict"] != "AGREE"
    ):
        raise EvidenceValidationError("stable publication requires an agreeing final-seal head")
    final = _verify_final(root, effective, profile, audit["bindings"]["final_candidate_ref"])
    if final["sha256"] != audit["bindings"]["final_candidate_sha256"]:
        raise EvidenceValidationError("stable publication final-candidate binding mismatch")
    audit_raw = _read(root, audit["bindings"]["audit_ref"])
    if content_digest(audit_raw) != audit["bindings"]["audit_sha256"]:
        raise EvidenceValidationError("stable publication audit binding drift")
    audited_chain = _verify_receipt_index(root, audit["bindings"]["audited_receipt_index_ref"], profile)
    if audited_chain["index_sha256"] != audit["bindings"]["audited_receipt_index_sha256"]:
        raise EvidenceValidationError("stable publication audited receipt-index binding drift")
    gate = audited_chain["receipts"][-1]["record"]
    if gate["check_id"] != "final_candidate_gate" or gate["exit_code"] != 0:
        raise EvidenceValidationError("stable publication audit did not bind a final-candidate gate")
    expected_audit_bindings = {
        "Audited result round": result_round,
        "Audited final-decision candidate SHA-256": final["sha256"],
        "Audited candidate SHA-256": final["record"]["candidate_decision_sha256"],
        "Audited result-review SHA-256": final["record"]["result_review_sha256"],
        "Audited final-candidate validation-log SHA-256": audit["bindings"]["validation_log_sha256"],
        "Audited governance receipt-index SHA-256": audited_chain["index_sha256"],
    }
    if extraction.parse_review(
        audit_raw,
        expected_bindings=expected_audit_bindings,
        kind="final-seal audit",
    ) != "AGREE":
        raise EvidenceValidationError("stable publication final-seal audit is not independently agreeing")
    stable_ref = _fixed_ref(profile, "stable_decision", result_round, round_ref)
    stable_path = root / stable_ref
    if stable_path.exists() or stable_path.is_symlink():
        raise EvidenceValidationError("stable decision path already exists")
    phase_root = root / EVIDENCE_ROOT_REF
    if phase_root.is_symlink() or not phase_root.is_dir():
        raise EvidenceValidationError("stable publication phase root is unsafe")
    _safe_mkdir(stable_path.parent, parents=False)
    os.link(root / final["ref"], stable_path, follow_symlinks=False)
    source_info = os.stat(root / final["ref"], follow_symlinks=False)
    stable_info = os.stat(stable_path, follow_symlinks=False)
    same_inode = source_info.st_dev == stable_info.st_dev and source_info.st_ino == stable_info.st_ino
    same_digest = _digest(root, stable_ref) == final["sha256"]
    if not same_inode or not same_digest:
        raise EvidenceValidationError("stable hard link failed inode/digest verification")
    bindings = {
        "stable_ref": stable_ref,
        "stable_sha256": _digest(root, stable_ref),
        "final_candidate_ref": final["ref"],
        "final_candidate_sha256": final["sha256"],
        "audit_ref": audit["bindings"]["audit_ref"],
        "audit_sha256": audit["bindings"]["audit_sha256"],
        "validation_log_ref": audit["bindings"]["validation_log_ref"],
        "validation_log_sha256": audit["bindings"]["validation_log_sha256"],
        "same_inode": same_inode,
        "same_digest": same_digest,
    }
    log = {
        "schema_version": "p02_stable_decision_validation@1",
        "result_round": result_round,
        **bindings,
        "publication_mode": "disabled",
        "status": "PASS",
    }
    return 0, canonical_json_bytes(log), b"", bindings


def _native_action(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    action: str,
    chain: Mapping[str, Any],
    artifact_ref: str | None,
) -> tuple[int, bytes, bytes, dict[str, Any]]:
    if action in {
        "mutation_ambiguity_gate",
        "zero_backend_source_edit_gate",
        "protected_check",
        "implementation_exit",
        "allowlist",
    }:
        return _native_evidence_gate(root, effective, profile, round_ref, result_round, action, chain)
    if action == "bind_result":
        return _bind_result(root, profile, round_ref, result_round, chain)
    if action == "build_run_manifest":
        return _build_run_manifest(root, effective, profile, round_ref, result_round, chain)
    if action == "build_candidate":
        return _build_candidate(root, effective, profile, round_ref, result_round, chain)
    if action == "candidate_gate":
        return _candidate_gate(root, effective, profile, round_ref, result_round, chain)
    if action == "result_review_binding" and artifact_ref is not None:
        return _result_review_binding(root, effective, profile, round_ref, result_round, chain, artifact_ref)
    if action == "build_final_candidate":
        return _build_final_candidate(root, effective, profile, round_ref, result_round, chain)
    if action == "final_candidate_gate":
        return _final_candidate_gate(root, effective, profile, round_ref, result_round, chain)
    if action == "final_seal_audit_binding" and artifact_ref is not None:
        return _final_seal_audit_binding(root, effective, profile, result_round, chain, artifact_ref)
    if action == "bind_scoped_repair":
        return _bind_scoped_repair(root, profile, round_ref, result_round, chain)
    if action == "close_round":
        return _close_round(root, profile, round_ref, result_round, chain)
    if action == "stable_publication":
        return _stable_publication(root, effective, profile, round_ref, result_round, chain)
    raise EvidenceValidationError(f"native action implementation is unavailable: {action}")


def _log_stem(action: str) -> str:
    return action.replace("_", "-")


def _run_action(
    root: Path,
    effective: Mapping[str, Any],
    profile: Mapping[str, Any],
    round_ref: str,
    result_round: str,
    action: str,
    artifact_ref: str | None,
) -> dict[str, Any]:
    _verify_runtime_directories(root, round_ref)
    chain = _latest_chain(root, round_ref, profile)
    stable_ref = _fixed_ref(profile, "stable_decision", result_round, round_ref)
    stable_exists = (root / stable_ref).exists() or (root / stable_ref).is_symlink()
    if stable_exists and (chain is None or chain["receipts"][-1]["record"]["check_id"] != "stable_publication"):
        raise EvidenceValidationError("stable path exists without a trusted terminal publication receipt; human recovery required")
    expected = extraction.expected_next_action(chain, stable_path_exists=stable_exists)
    if action != expected:
        raise EvidenceValidationError(f"action {action} is not allowed; expected {expected}")
    action_profile = profile["actions"][action]
    if action_profile["artifact_ref_template"] is None:
        if artifact_ref is not None:
            raise EvidenceValidationError("--artifact-ref is accepted only for review/audit binding")
    else:
        if artifact_ref is None:
            raise EvidenceValidationError(f"{action} requires --artifact-ref")
        artifact_ref = _logical_ref(root, artifact_ref)
        expected_artifact = action_profile["artifact_ref_template"].replace("RESULT_ROUND", result_round)
        if artifact_ref != expected_artifact:
            raise EvidenceValidationError("artifact ref differs from the effective action profile")
    stdout_ref = f"{round_ref}/logs/{_log_stem(action)}.stdout"
    stderr_ref = f"{round_ref}/logs/{_log_stem(action)}.stderr"
    started = _utc_now()
    start_ns = time.monotonic_ns()
    try:
        if action_profile["execution_class"] == "subprocess":
            exit_code, stdout, stderr, bindings = _run_subprocess(root, profile, round_ref, action)
        elif action_profile["execution_class"] == "governance_native":
            exit_code, stdout, stderr, bindings = _native_action(
                root,
                effective,
                profile,
                round_ref,
                result_round,
                action,
                chain,
                artifact_ref,
            )
        else:
            raise EvidenceValidationError("action has an unknown execution class")
        if set(bindings) != set(profile["receipt_binding_keys"][action]):
            raise EvidenceValidationError("action returned a binding map outside the effective profile")
    except Exception as exc:
        exit_code = 1
        stdout = b""
        stderr = f"{type(exc).__name__}: {exc}\n".encode("utf-8")
        bindings = _null_bindings(profile, action)
    ended = _utc_now()
    wall_time_ns = time.monotonic_ns() - start_ns
    _write(root, stdout_ref, stdout)
    _write(root, stderr_ref, stderr)
    receipt, new_chain = _append_receipt(
        root,
        profile,
        round_ref,
        result_round,
        action,
        artifact_ref=artifact_ref,
        started_at=started,
        ended_at=ended,
        wall_time_ns=wall_time_ns,
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


def _strict_cli(argv: list[str], action_ids: set[str]) -> tuple[str, str, str | None]:
    if any("=" in token for token in argv):
        raise EvidenceValidationError("equal-sign arguments are forbidden")
    if argv[:1] == ["init-round"]:
        if len(argv) != 3 or argv[1] != "--round-root":
            raise EvidenceValidationError("usage: p02_governance.py init-round --round-root RR")
        return "init-round", argv[2], None
    if argv[:1] != ["run"]:
        raise EvidenceValidationError("operation must be exactly init-round or run")
    if len(argv) not in {5, 7} or argv[1] != "--round-root" or argv[3] != "--action":
        raise EvidenceValidationError("usage: p02_governance.py run --round-root RR --action ACTION [--artifact-ref REF]")
    action = argv[4]
    if action not in action_ids or action == "init_round":
        raise EvidenceValidationError("run action is not registered or is initializer-only")
    artifact_ref = None
    if len(argv) == 7:
        if argv[5] != "--artifact-ref":
            raise EvidenceValidationError("only --artifact-ref may follow the action")
        artifact_ref = argv[6]
    return action, argv[2], artifact_ref


def main(argv: list[str] | None = None) -> int:
    _guard_caller_environment()
    args = sys.argv[1:] if argv is None else argv
    root = _repo_root()
    effective, recovery, profile = _load_effective_profile(root)
    action, round_root, artifact_ref = _strict_cli(args, set(profile["actions"]))
    os.environ["MATHDEVMCP_P02_DISPATCH_DEPTH"] = "1"
    if action == "init-round":
        status = _init_round(root, effective, recovery, profile, round_root)
    else:
        round_ref, result_round, _ = _round_context(root, round_root, must_exist=True)
        status = _run_action(
            root,
            effective,
            profile,
            round_ref,
            result_round,
            action,
            artifact_ref,
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
