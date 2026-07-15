#!/usr/bin/env python3
"""Create and independently verify the immutable Phase 08C continuation."""

from __future__ import annotations

import argparse
import builtins
from contextlib import contextmanager
from copy import deepcopy
import hashlib
import importlib.abc
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import socket
import stat
import subprocess
import sys
import time
from typing import Any, Iterator, Mapping, Sequence
import uuid


class Phase08CError(RuntimeError):
    """Raised when the continuation cannot preserve its reviewed boundary."""


WORKSPACE = Path("/home/chakwong/python/MathDevMCP")
SOURCE_ROOT = WORKSPACE / "src"
RUNNER_REF = "scripts/run_p08c_frozen_workflow.py"
P08_PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
PARENT_REF = ".local/mathdevmcp/evidence/p08-20260714/runs/20260714T045222Z-a0e295b097c0"
CONTINUATION_PARENT_REF = ".local/mathdevmcp/evidence/p08-20260714/continuations"
PARENT_RUN_ID = "20260714T045222Z-a0e295b097c0"
PARENT_RUN_BINDING = "14a49479769439925a6e3f9ad293b1b0fcea5a61f81ec454fbaea5ea80da8fb0"
PARENT_CODE_IDENTITY = "4ff3eb7d75707ee355ea093830e6b829736284b16b807ea6a0e82a18231e878c"
P08A_DECISION_DIGEST = "9ca9db79c1911dc4e72bca2fd13a13aebea4eb5c23994d0b6607c5137f88bf3f"
P08A_SOURCE_MANIFEST_DIGEST = "f0cbf55b6bc8eb7ca5c2a45eb49f9a86555dadc5821cf66ad8aaf6585d8899d2"
P08A_EXTRACTION_DIGEST = "5b33819c3df0d1380d62c8fbe9c0042f326340dc0b2b398224285a202652c576"
P08A_CONTEXT_DIGEST = "eaa96197dc0607aeb430455e9fdc0989ce7f00ff374404371206c00887f45eab"
P08A_DECISION_SHA256 = "25923d1ad62acba91521fccca73a732b375610e9331e20ad33d289fa29f10421"
P08B_DECISION_SHA256 = "ffe2769cb1516bf3ccbcdf563152b3f87ed3e63081e4012bf746587570301d84"
P08B_DECISION_DIGEST = "8548c8d8e26bf404392fb4a51e7ea483ac7773961bd8897251bf5ec7240ab08c"
P08B_REQUEST_DIGEST = "648d59267c180361027f7f07fa91d514db90584b0c70db3729ee7c7bd2a66dcb"
P08B_RESULT_DIGEST = "1dfaace0ef1b244f0b2ce4b2b1d00e822a281bb8d70ce6783e4ed4979b6641e6"
PARENT_TREE_DIGEST = "1718b1e72a0dbb56a3b0ea9cee052db2b0ea793327e0d8d92f507ecab3cd5f77"
PARENT_TREE_FILE_COUNT = 166
PARENT_TREE_BYTE_COUNT = 11_412_915
COMPACT_LIMIT = 25_600
PROBE_TIMEOUT_SECONDS = 10
PROBE_OUTPUT_LIMIT = 65_536
LOCAL_ABSOLUTE_PATH_FRAGMENT = re.compile(
    r"(?<![A-Za-z0-9_.-])/(?:home|tmp|usr|opt|var|run|mnt|srv)"
    r"(?:/[^/\s'\"`<>|,;?&#=]+)*"
)

SOURCE_BINDINGS = {
    "card": {
        "ref": "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
        "sha256": "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8",
        "comparator_ref": "docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json",
        "comparator_sha256": "d5f6705c2d5ed8779086aa38cddc380b31045801dddfd26c784e30123f96f3d6",
        "focus_labels": [
            "eq:panel-npv-functional",
            "eq:incremental-cash-flow",
            "eq:incremental-npv",
        ],
        "target_labels": [
            "eq:panel-npv-functional",
            "eq:incremental-cash-flow",
            "eq:incremental-npv",
        ],
        "context_labels": [],
    },
    "risky": {
        "ref": "docs/risky-debt-maliar-deep-learning-lecture-note.tex",
        "sha256": "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1",
        "comparator_ref": "docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json",
        "comparator_sha256": "6c3928f098262c801d9a94d23030f37df173fd873e232b8d49366fa89491e2aa",
        "focus_labels": ["prop:interior-foc", "eq:foc-k", "eq:foc-b"],
        "target_labels": ["eq:foc-k", "eq:foc-b"],
        "context_labels": ["prop:interior-foc"],
    },
}

EXPECTED_ENVIRONMENT = {
    "CUDA_VISIBLE_DEVICES": "-1",
    "HOME": "/home/chakwong",
    "LANG": "C",
    "LC_ALL": "C",
    "MATHDEVMCP_BACKEND_CONDA_ENV": "mathdevmcp-backends",
    "MATHDEVMCP_LEAN_TOOLCHAIN": "leanprover/lean4:v4.20.0",
    "PATH": "/usr/bin:/bin:/home/chakwong/.elan/bin:/home/chakwong/miniconda3/condabin",
    "PWD": str(WORKSPACE),
    "PYTHONHASHSEED": "0",
    "PYTHONUNBUFFERED": "1",
}

CONDA = "/home/chakwong/miniconda3/condabin/conda"
BACKEND_PYTHON = "/home/chakwong/miniconda3/envs/mathdevmcp-backends/bin/python"
VERSION_COMMANDS = {
    ("/usr/bin/latexml", "--VERSION"),
    ("/usr/bin/pandoc", "--version"),
    ("/home/chakwong/.elan/bin/lean", "--version"),
    ("/usr/bin/sage", "--version"),
}
REGISTERED_MODULE_PACKAGES = {
    ("sympy", "sympy"),
    ("mcp", "mcp"),
    ("lean_dojo", "lean-dojo"),
    ("lean_explore", "lean-explore"),
    ("pantograph", "pantograph"),
    ("leansearchv2", "leansearchv2"),
}
EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT = {
    "conda_env_list": 21,
    "executable_version": 4,
    "backend_python_package_version": 8,
}


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
        raise Phase08CError("record is not canonical-JSON serializable") from exc


def _digest(value: Any) -> str:
    raw = bytes(value) if isinstance(value, (bytes, bytearray, memoryview)) else _canonical(value)
    return hashlib.sha256(raw).hexdigest()


def _utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _require_runtime() -> None:
    expected_stdlib = [
        "/home/chakwong/miniconda3/envs/tfgpu/lib/python311.zip",
        "/home/chakwong/miniconda3/envs/tfgpu/lib/python3.11",
        "/home/chakwong/miniconda3/envs/tfgpu/lib/python3.11/lib-dynload",
    ]
    if (
        sys.executable != P08_PYTHON
        or sys.flags.isolated != 1
        or sys.flags.no_site != 1
        or sys.flags.no_user_site != 1
        or sys.flags.ignore_environment != 1
        or sys.flags.safe_path is not True
        or sys.flags.dont_write_bytecode != 1
        or sys.pycache_prefix != "/dev/null"
        or sys.path != expected_stdlib
        or not Path("/dev/null").is_char_device()
    ):
        raise Phase08CError("P08C runtime is not isolated and source-only")
    actual_env = {key: value for key, value in os.environ.items() if key != "_"}
    if actual_env != EXPECTED_ENVIRONMENT:
        raise Phase08CError("P08C process environment differs from the reviewed exact envelope")
    if Path.cwd().absolute() != WORKSPACE or WORKSPACE.is_symlink():
        raise Phase08CError("P08C must run from the literal non-symlinked workspace")


def _activate_repo_source() -> None:
    source = str(SOURCE_ROOT)
    if source in sys.path:
        raise Phase08CError("repository source entered sys.path before P08C attestation")
    sys.path.insert(0, source)


def _assert_no_symlink(path: Path, *, root: Path = WORKSPACE) -> None:
    absolute = path.absolute()
    try:
        relative = absolute.relative_to(root)
    except ValueError as exc:
        raise Phase08CError(f"path escapes registered root: {path}") from exc
    cursor = root
    if cursor.is_symlink():
        raise Phase08CError("registered root must not be a symlink")
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise Phase08CError(f"symlink is forbidden in P08C paths: {cursor}")


def _regular_bytes(path: Path, *, root: Path = WORKSPACE) -> bytes:
    _assert_no_symlink(path, root=root)
    info = path.stat()
    if not stat.S_ISREG(info.st_mode):
        raise Phase08CError(f"required file is not regular: {path}")
    return path.read_bytes()


def _safe_ref(raw_ref: Any, label: str) -> str:
    if not isinstance(raw_ref, str) or not raw_ref:
        raise Phase08CError(f"{label} must be a non-empty string")
    value = PurePosixPath(raw_ref)
    if (
        value.is_absolute()
        or value.as_posix() != raw_ref
        or any(part in {"", ".", ".."} for part in value.parts)
    ):
        raise Phase08CError(f"{label} is not a normalized relative reference")
    return raw_ref


def _decode_canonical(raw: bytes, label: str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Phase08CError(f"invalid JSON: {label}") from exc
    if not isinstance(value, dict) or _canonical(value) != raw:
        raise Phase08CError(f"artifact is not a canonical JSON object: {label}")
    return value


def _load_canonical(path: Path, *, root: Path = WORKSPACE) -> dict[str, Any]:
    return _decode_canonical(_regular_bytes(path, root=root), str(path))


def _write_new(path: Path, raw: bytes, *, root: Path = WORKSPACE) -> None:
    _assert_no_symlink(path.parent, root=root)
    if path.exists() or path.is_symlink():
        raise Phase08CError(f"P08C never overwrites artifacts: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0),
        0o600,
    )
    try:
        view = memoryview(raw)
        while view:
            count = os.write(descriptor, view)
            if count <= 0:
                raise OSError("short P08C write")
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    if _regular_bytes(path, root=root) != raw:
        raise Phase08CError(f"P08C reopen mismatch: {path}")


def _write_json_new(path: Path, value: Mapping[str, Any]) -> None:
    _write_new(path, _canonical(dict(value)))


def _verify_semantic_digest(record: Mapping[str, Any], field: str, expected: str) -> None:
    actual = record.get(field)
    reconstructed = _digest({key: value for key, value in record.items() if key != field})
    if actual != expected or actual != reconstructed:
        raise Phase08CError(f"parent semantic digest mismatch: {field}")


def _verify_parent_code_identity(parent: Path) -> dict[str, Any]:
    identity = _load_canonical(parent / "code-identity.json")
    _verify_semantic_digest(identity, "code_identity_digest", PARENT_CODE_IDENTITY)
    if identity.get("run_id") != PARENT_RUN_ID or identity.get("run_binding_digest") != PARENT_RUN_BINDING:
        raise Phase08CError("parent code identity cross-binding mismatch")
    refs: set[str] = set()
    for item in identity.get("files", []):
        if not isinstance(item, dict) or set(item) != {"ref", "sha256", "byte_count", "dirty"}:
            raise Phase08CError("parent code identity file record is malformed")
        ref = _safe_ref(item["ref"], "parent code ref")
        if ref in refs:
            raise Phase08CError("parent code identity has duplicate refs")
        refs.add(ref)
        snapshot = _regular_bytes(parent / "code-snapshot" / ref)
        if _digest(snapshot) != item["sha256"] or len(snapshot) != item["byte_count"]:
            raise Phase08CError(f"parent code snapshot mismatch: {ref}")
    return identity


def _tree_identity(root: Path) -> tuple[int, int, str]:
    records: list[tuple[str, str, bytes | None]] = []
    file_count = 0
    byte_count = 0
    for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix().encode("utf-8")):
        status = path.lstat()
        relative = path.relative_to(root).as_posix()
        if stat.S_ISLNK(status.st_mode):
            raise Phase08CError(f"immutable tree contains a symlink: {relative}")
        if stat.S_ISDIR(status.st_mode):
            records.append(("directory", relative, None))
            continue
        if not stat.S_ISREG(status.st_mode):
            raise Phase08CError(f"immutable tree contains a special entry: {relative}")
        raw = path.read_bytes()
        records.append(("file", relative, raw))
        file_count += 1
        byte_count += len(raw)
    tree_hash = hashlib.sha256()
    for kind, relative, raw in records:
        if kind == "directory":
            tree_hash.update(b"D\0" + relative.encode("utf-8") + b"\0")
        else:
            assert raw is not None
            tree_hash.update(
                b"F\0"
                + relative.encode("utf-8")
                + b"\0"
                + len(raw).to_bytes(8, "big")
                + hashlib.sha256(raw).digest()
            )
    return file_count, byte_count, tree_hash.hexdigest()


def _verify_parent_bundle(parent: Path) -> dict[str, Any]:
    candidate = parent / "p08b/backend/eq_cashflow_rate_derivative"
    expected_names = {"native-input.json", "stdout.bin", "stderr.bin", "result.json", "manifest.json"}
    _assert_no_symlink(candidate)
    entries = list(candidate.iterdir())
    if {entry.name for entry in entries} != expected_names or any(
        entry.is_symlink() or not entry.is_file() for entry in entries
    ):
        raise Phase08CError("parent P08B candidate file set mismatch")
    manifest_raw = _regular_bytes(candidate / "manifest.json")
    manifest = _decode_canonical(manifest_raw, "parent P08B bundle manifest")
    if (
        manifest.get("run_id") != PARENT_RUN_ID
        or manifest.get("run_binding_digest") != PARENT_RUN_BINDING
        or manifest.get("code_identity_digest") != PARENT_CODE_IDENTITY
        or manifest.get("candidate_id") != "eq:cashflow-rate-derivative"
        or manifest.get("request_digest") != P08B_REQUEST_DIGEST
        or manifest.get("publication_enabled") is not False
    ):
        raise Phase08CError("parent P08B bundle binding mismatch")
    expected_files = []
    for name in ("native-input.json", "stdout.bin", "stderr.bin", "result.json"):
        raw = _regular_bytes(candidate / name)
        expected_files.append({"name": name, "sha256": _digest(raw), "byte_count": len(raw)})
    if manifest.get("files") != expected_files:
        raise Phase08CError("parent P08B bundle file records mismatch")
    native = _decode_canonical(_regular_bytes(candidate / "native-input.json"), "parent native input")
    result = _decode_canonical(_regular_bytes(candidate / "result.json"), "parent result")
    _verify_semantic_digest(native, "request_digest", P08B_REQUEST_DIGEST)
    _verify_semantic_digest(result, "result_digest", P08B_RESULT_DIGEST)
    if (
        result.get("request") != native
        or result.get("status") != "backend_checked"
        or result.get("claim_class") != "backend_checked_computational_support"
        or result.get("can_promote") is not False
        or result.get("formal_proof_certified") is not False
        or result.get("publication_enabled") is not False
        or result.get("worker_record", {}).get("difference_srepr") != "Integer(0)"
    ):
        raise Phase08CError("parent P08B result boundary mismatch")
    return {
        "manifest_sha256": _digest(manifest_raw),
        "request_digest": native["request_digest"],
        "result_digest": result["result_digest"],
    }


def _verify_parent() -> dict[str, Any]:
    parent = WORKSPACE / PARENT_REF
    _assert_no_symlink(parent)
    if not parent.is_dir():
        raise Phase08CError("literal parent run is missing")
    if _tree_identity(parent) != (
        PARENT_TREE_FILE_COUNT,
        PARENT_TREE_BYTE_COUNT,
        PARENT_TREE_DIGEST,
    ):
        raise Phase08CError("immutable parent tree identity mismatch")
    run_manifest = _load_canonical(parent / "run-manifest.json")
    if (
        run_manifest.get("run_id") != PARENT_RUN_ID
        or run_manifest.get("run_root") != PARENT_REF
        or run_manifest.get("run_binding_digest") != PARENT_RUN_BINDING
        or run_manifest.get("code_identity_digest") != PARENT_CODE_IDENTITY
        or run_manifest.get("publication_enabled") is not False
    ):
        raise Phase08CError("parent run manifest binding mismatch")
    _verify_parent_code_identity(parent)
    source = _load_canonical(parent / "source-manifest.json")
    extraction = _load_canonical(parent / "p08a/extraction.json")
    context = _load_canonical(parent / "p08a/context.json")
    p08a = _load_canonical(parent / "p08a/decision.json")
    p08b_raw = _regular_bytes(parent / "p08b/capability-decision.json")
    p08b = _decode_canonical(p08b_raw, "parent P08B decision")
    if _digest(_regular_bytes(parent / "p08a/decision.json")) != P08A_DECISION_SHA256:
        raise Phase08CError("parent P08A decision file SHA-256 mismatch")
    if _digest(p08b_raw) != P08B_DECISION_SHA256:
        raise Phase08CError("parent P08B decision file SHA-256 mismatch")
    _verify_semantic_digest(source, "source_manifest_digest", P08A_SOURCE_MANIFEST_DIGEST)
    _verify_semantic_digest(extraction, "extraction_digest", P08A_EXTRACTION_DIGEST)
    _verify_semantic_digest(context, "context_digest", P08A_CONTEXT_DIGEST)
    _verify_semantic_digest(p08a, "decision_digest", P08A_DECISION_DIGEST)
    _verify_semantic_digest(p08b, "decision_digest", P08B_DECISION_DIGEST)
    if (
        p08a.get("status") != "PASS_P08A_FROZEN_EXTRACTION_CONTEXT"
        or p08a.get("vetoes") != []
        or p08a.get("backend_request_count") != 0
        or p08a.get("publication_enabled") is not False
        or p08b.get("status") != "backend_checked"
        or p08b.get("request_digest") != P08B_REQUEST_DIGEST
        or p08b.get("result_digest") != P08B_RESULT_DIGEST
        or p08b.get("vetoes") != []
        or p08b.get("can_promote") is not False
        or p08b.get("formal_proof_certified") is not False
        or p08b.get("publication_enabled") is not False
    ):
        raise Phase08CError("parent P08A/P08B decision boundary mismatch")
    for item in source.get("artifacts", []):
        raw = _regular_bytes(WORKSPACE / str(item.get("ref")))
        if _digest(raw) != item.get("sha256") or len(raw) != item.get("byte_count"):
            raise Phase08CError(f"frozen source/comparator drift: {item.get('ref')}")
    for binding in SOURCE_BINDINGS.values():
        if _digest(_regular_bytes(WORKSPACE / binding["ref"])) != binding["sha256"]:
            raise Phase08CError("frozen source digest differs from P08C registration")
        if _digest(_regular_bytes(WORKSPACE / binding["comparator_ref"])) != binding["comparator_sha256"]:
            raise Phase08CError("frozen comparator digest differs from P08C registration")
    bundle = _verify_parent_bundle(parent)
    return {
        "schema_version": "p08c_parent_binding@1",
        "parent_run_id": PARENT_RUN_ID,
        "parent_run_root": PARENT_REF,
        "parent_run_binding_digest": PARENT_RUN_BINDING,
        "parent_code_identity_digest": PARENT_CODE_IDENTITY,
        "parent_tree_digest": PARENT_TREE_DIGEST,
        "parent_tree_file_count": PARENT_TREE_FILE_COUNT,
        "parent_tree_byte_count": PARENT_TREE_BYTE_COUNT,
        "p08a_decision_digest": P08A_DECISION_DIGEST,
        "p08a_decision_sha256": P08A_DECISION_SHA256,
        "p08a_source_manifest_digest": P08A_SOURCE_MANIFEST_DIGEST,
        "p08a_extraction_digest": P08A_EXTRACTION_DIGEST,
        "p08a_context_digest": P08A_CONTEXT_DIGEST,
        "p08b_decision_digest": P08B_DECISION_DIGEST,
        "p08b_decision_sha256": P08B_DECISION_SHA256,
        "p08b_request_digest": bundle["request_digest"],
        "p08b_result_digest": bundle["result_digest"],
        "p08b_bundle_manifest_sha256": bundle["manifest_sha256"],
        "publication_enabled": False,
    }


def _loaded_repo_sources() -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for name, module in sorted(sys.modules.items()):
        raw_file = getattr(module, "__file__", None)
        if not isinstance(raw_file, str) or not raw_file:
            continue
        path = Path(raw_file)
        try:
            ref = path.absolute().relative_to(WORKSPACE).as_posix()
        except ValueError:
            continue
        if not ref.startswith("src/mathdevmcp/"):
            continue
        if path.suffix != ".py" or "__pycache__" in path.parts:
            raise Phase08CError(f"repository module loaded from bytecode: {name}:{ref}")
        raw = _regular_bytes(path)
        records[ref] = {"ref": ref, "sha256": _digest(raw), "byte_count": len(raw)}
    if not records:
        raise Phase08CError("P08C loaded no repository source modules")
    return [records[key] for key in sorted(records)]


def _snapshot_code(continuation: Path, continuation_id: str, binding: str) -> dict[str, Any]:
    records = []
    for path in sorted(SOURCE_ROOT.joinpath("mathdevmcp").glob("*.py"), key=lambda item: item.name.encode("utf-8")):
        raw = _regular_bytes(path)
        records.append(
            {
                "ref": path.relative_to(WORKSPACE).as_posix(),
                "sha256": _digest(raw),
                "byte_count": len(raw),
            }
        )
    runner_raw = _regular_bytes(WORKSPACE / RUNNER_REF)
    records.insert(0, {"ref": RUNNER_REF, "sha256": _digest(runner_raw), "byte_count": len(runner_raw)})
    for item in records:
        raw = _regular_bytes(WORKSPACE / item["ref"])
        _write_new(continuation / "code-snapshot" / item["ref"], raw)
    identity = {
        "schema_version": "p08c_code_identity@1",
        "continuation_id": continuation_id,
        "continuation_binding_digest": binding,
        "files": records,
        "runtime": {
            "python": P08_PYTHON,
            "flags": ["-I", "-S", "-B", "-X", "pycache_prefix=/dev/null"],
            "source_root": str(SOURCE_ROOT),
            "module_origin_policy": "source_only_no_bytecode",
        },
        "boundary": "P08C source identity has no proof, promotion, publication, or parent-rewrite authority.",
    }
    identity["code_identity_digest"] = _digest(identity)
    _write_json_new(continuation / "code-identity.json", identity)
    return identity


def _verify_code_identity(
    continuation: Path,
    *,
    require_loaded_modules: bool = True,
) -> dict[str, Any]:
    identity = _load_canonical(continuation / "code-identity.json")
    _verify_semantic_digest(identity, "code_identity_digest", str(identity.get("code_identity_digest")))
    if set(identity) != {
        "schema_version",
        "continuation_id",
        "continuation_binding_digest",
        "files",
        "runtime",
        "boundary",
        "code_identity_digest",
    } or not isinstance(identity.get("files"), list):
        raise Phase08CError("P08C code identity schema mismatch")
    refs: set[str] = set()
    for item in identity.get("files", []):
        if not isinstance(item, Mapping) or set(item) != {"ref", "sha256", "byte_count"}:
            raise Phase08CError("P08C code identity file record is malformed")
        ref = _safe_ref(item.get("ref"), "P08C code ref")
        value = PurePosixPath(ref)
        is_module = len(value.parts) == 3 and value.parts[:2] == ("src", "mathdevmcp") and value.suffix == ".py"
        if ref in refs or not (ref == RUNNER_REF or is_module):
            raise Phase08CError("P08C code identity contains duplicate or foreign ref")
        refs.add(ref)
        live = _regular_bytes(WORKSPACE / ref)
        snapshot = _regular_bytes(continuation / "code-snapshot" / ref)
        if live != snapshot or _digest(live) != item.get("sha256") or len(live) != item.get("byte_count"):
            raise Phase08CError(f"P08C code drift veto: {ref}")
    snapshot_root = continuation / "code-snapshot"
    snapshot_refs = {
        path.relative_to(snapshot_root).as_posix()
        for path in snapshot_root.rglob("*")
        if path.is_file() and not path.is_symlink()
    }
    if snapshot_refs != refs:
        raise Phase08CError("P08C code snapshot file set differs from code identity")
    if any(path.is_symlink() or (not path.is_dir() and not path.is_file()) for path in snapshot_root.rglob("*")):
        raise Phase08CError("P08C code snapshot contains an unsafe entry")
    if require_loaded_modules:
        loaded = {item["ref"] for item in _loaded_repo_sources()}
        if loaded - refs:
            raise Phase08CError(f"loaded repository source lacks snapshot: {sorted(loaded - refs)}")
    return identity


class _BlockedImportFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname: str, path: Any = None, target: Any = None) -> None:
        # Isolated sys.path makes these unavailable; returning None also lets
        # doctor perform non-importing find_spec availability checks.
        return None


def _verify_source_tree_cache_policy() -> None:
    for path in SOURCE_ROOT.joinpath("mathdevmcp").rglob("*"):
        status = path.lstat()
        relative = path.relative_to(SOURCE_ROOT).as_posix()
        in_cache = "__pycache__" in path.relative_to(SOURCE_ROOT).parts
        if stat.S_ISLNK(status.st_mode):
            raise Phase08CError(f"repository source tree contains a symlink: {relative}")
        if stat.S_ISDIR(status.st_mode):
            if in_cache and path.name != "__pycache__":
                raise Phase08CError(f"repository cache contains a directory: {relative}")
            continue
        if not stat.S_ISREG(status.st_mode):
            raise Phase08CError(f"repository source tree contains a special entry: {relative}")
        if in_cache:
            if path.suffix != ".pyc" or status.st_mode & 0o111:
                raise Phase08CError(f"repository cache contains an unexpected file: {relative}")
            continue
        if path.suffix in {".pyc", ".pyo"}:
            raise Phase08CError(f"repository source tree contains legacy bytecode: {relative}")


def _probe_python_code(module: str, package: str) -> str:
    return (
        "import importlib.metadata, importlib.util, sys; "
        f"module={module!r}; package={package!r}; "
        "spec=importlib.util.find_spec(module); "
        "sys.exit(2) if spec is None else None; "
        "print(importlib.metadata.version(package))"
    )


def _classify_probe(argv: Sequence[str]) -> str | None:
    command = tuple(str(item) for item in argv)
    if command == (CONDA, "env", "list"):
        return "conda_env_list"
    if command in VERSION_COMMANDS:
        return "executable_version"
    if len(command) == 3 and command[0] == BACKEND_PYTHON and command[1] == "-c":
        matches = [
            (module, package)
            for module, package in REGISTERED_MODULE_PACKAGES
            if command[2] == _probe_python_code(module, package)
        ]
        if len(matches) == 1:
            return "backend_python_package_version"
    return None


def _probe_counts_by_document(
    probes: Sequence[Mapping[str, Any]],
) -> dict[str, dict[str, int]]:
    counts = {
        document: {classification: 0 for classification in EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT}
        for document in SOURCE_BINDINGS
    }
    for item in probes:
        document = item.get("document")
        classification = item.get("classification")
        if document not in counts or classification not in EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT:
            raise Phase08CError("persisted doctor probe lacks a registered document/classification binding")
        counts[str(document)][str(classification)] += 1
    return counts


def _bounded_probe(
    original_popen: Any,
    argv: list[str],
    *,
    env: Mapping[str, str] | None,
    timeout: int,
) -> tuple[int, bytes, bytes, int]:
    started = time.monotonic()
    process = original_popen(
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=None if env is None else dict(env),
        bufsize=0,
    )
    assert process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    streams = {process.stdout: "stdout", process.stderr: "stderr"}
    for stream in streams:
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ)
    chunks = {"stdout": bytearray(), "stderr": bytearray()}
    overflow = False
    timed_out = False
    while selector.get_map():
        remaining = timeout - (time.monotonic() - started)
        if remaining <= 0:
            timed_out = True
            break
        for key, _mask in selector.select(min(remaining, 0.1)):
            stream = key.fileobj
            try:
                chunk = os.read(stream.fileno(), 65_536)
            except BlockingIOError:
                continue
            if not chunk:
                selector.unregister(stream)
                stream.close()
                continue
            name = streams[stream]
            available = max(0, PROBE_OUTPUT_LIMIT + 1 - len(chunks[name]))
            chunks[name].extend(chunk[:available])
            if len(chunks[name]) > PROBE_OUTPUT_LIMIT or len(chunk) > available:
                overflow = True
                break
        if overflow:
            break
    if not timed_out and not overflow:
        remaining = timeout - (time.monotonic() - started)
        if remaining <= 0:
            timed_out = True
        else:
            try:
                process.wait(timeout=remaining)
            except subprocess.TimeoutExpired:
                timed_out = True
    if (timed_out or overflow) and process.poll() is None:
        process.terminate()
    if process.poll() is None:
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=2)
    for registered in list(selector.get_map().values()):
        selector.unregister(registered.fileobj)
        registered.fileobj.close()
    selector.close()
    if timed_out:
        raise Phase08CError(f"doctor probe timed out: {argv!r}")
    if overflow:
        raise Phase08CError(f"doctor probe output exceeded the reviewed byte limit: {argv!r}")
    return (
        int(process.returncode),
        bytes(chunks["stdout"]),
        bytes(chunks["stderr"]),
        int((time.monotonic() - started) * 1_000),
    )


@contextmanager
def _guarded_probes() -> Iterator[list[dict[str, Any]]]:
    ledger: list[dict[str, Any]] = []
    originals = {
        "run": subprocess.run,
        "Popen": subprocess.Popen,
        "call": subprocess.call,
        "check_call": subprocess.check_call,
        "check_output": subprocess.check_output,
        "os_system": os.system,
        "os_popen": os.popen,
        "socket": socket.create_connection,
        "socket_class": socket.socket,
        "import": builtins.__import__,
        "import_module": importlib.import_module,
    }
    blocked_import_roots = {
        "anthropic",
        "lean_dojo",
        "leandojo",
        "openai",
        "pantograph",
        "sage",
        "sageall",
        "sympy",
    }

    def guarded_run(*args: Any, **kwargs: Any) -> subprocess.CompletedProcess[str]:
        if len(args) != 1 or "args" in kwargs:
            ledger.append(
                {
                    "sequence": len(ledger) + 1,
                    "classification": "rejected_unregistered_process",
                    "argv": [repr(args), repr(kwargs.get("args"))],
                    "allowed": False,
                }
            )
            raise Phase08CError("P08C subprocess call shape is not registered")
        raw_argv = args[0] if args else kwargs.get("args")
        if not isinstance(raw_argv, (list, tuple)) or not all(isinstance(item, str) for item in raw_argv):
            ledger.append(
                {
                    "sequence": len(ledger) + 1,
                    "classification": "rejected_unregistered_process",
                    "argv": [repr(raw_argv)],
                    "allowed": False,
                }
            )
            raise Phase08CError("P08C subprocess argv must be a string list")
        argv = list(raw_argv)
        classification = _classify_probe(argv)
        input_value = kwargs.get("input")
        timeout = kwargs.get("timeout")
        invalid = (
            classification is None
            or input_value not in (None, b"", "")
            or timeout != PROBE_TIMEOUT_SECONDS
            or kwargs.get("shell", False)
            or kwargs.get("cwd") is not None
            or kwargs.get("stdin") not in {None, subprocess.DEVNULL}
        )
        expected_probe_env = dict(EXPECTED_ENVIRONMENT)
        expected_probe_env["PATH"] = (
            "/home/chakwong/miniconda3/envs/mathdevmcp-backends/bin:"
            + EXPECTED_ENVIRONMENT["PATH"]
        )
        expected_probe_env["ELAN_TOOLCHAIN"] = EXPECTED_ENVIRONMENT[
            "MATHDEVMCP_LEAN_TOOLCHAIN"
        ]
        supplied_env = kwargs.get("env")
        if classification == "executable_version":
            invalid = invalid or supplied_env != expected_probe_env
        else:
            invalid = invalid or supplied_env is not None
        allowed_keys = {"check", "capture_output", "text", "timeout", "env", "stdin"}
        invalid = (
            invalid
            or bool(set(kwargs) - allowed_keys)
            or kwargs.get("check") is not False
            or kwargs.get("capture_output") is not True
            or kwargs.get("text") is not True
        )
        if invalid:
            ledger.append(
                {
                    "sequence": len(ledger) + 1,
                    "classification": "rejected_unregistered_process",
                    "argv": argv,
                    "allowed": False,
                }
            )
            raise Phase08CError(f"unregistered P08C subprocess rejected before launch: {argv!r}")
        text_mode = True
        returncode, stdout_raw, stderr_raw, wall_time_ms = _bounded_probe(
            originals["Popen"],
            argv,
            env=kwargs.get("env"),
            timeout=timeout,
        )
        stdout: str | bytes = stdout_raw.decode("utf-8", "replace") if text_mode else stdout_raw
        stderr: str | bytes = stderr_raw.decode("utf-8", "replace") if text_mode else stderr_raw
        completed = subprocess.CompletedProcess(argv, returncode, stdout, stderr)
        ledger.append(
            {
                "sequence": len(ledger) + 1,
                "classification": classification,
                "argv": argv,
                "input_byte_count": 0,
                "timeout_seconds": timeout,
                "returncode": returncode,
                "stdout_byte_count": len(stdout_raw),
                "stdout_sha256": _digest(stdout_raw),
                "stderr_byte_count": len(stderr_raw),
                "stderr_sha256": _digest(stderr_raw),
                "wall_time_ms": wall_time_ms,
                "mathematical_input": False,
                "evidence_authority": "operational_provenance_only",
                "allowed": True,
            }
        )
        return completed

    def reject(*args: Any, **kwargs: Any) -> None:
        ledger.append(
            {
                "sequence": len(ledger) + 1,
                "classification": "rejected_unregistered_process_or_network",
                "argv": [repr(args[0] if args else kwargs)],
                "allowed": False,
            }
        )
        raise Phase08CError("unregistered process or network API rejected before launch")

    def guarded_import(
        name: str,
        globals: Mapping[str, Any] | None = None,
        locals: Mapping[str, Any] | None = None,
        fromlist: Sequence[str] = (),
        level: int = 0,
    ) -> Any:
        if level == 0 and name.split(".", 1)[0] in blocked_import_roots:
            raise Phase08CError(f"mathematical/model package import rejected: {name}")
        return originals["import"](name, globals, locals, fromlist, level)

    def guarded_import_module(name: str, package: str | None = None) -> Any:
        if name.split(".", 1)[0] in blocked_import_roots:
            raise Phase08CError(f"mathematical/model package import rejected: {name}")
        return originals["import_module"](name, package)

    finder = _BlockedImportFinder()
    sys.meta_path.insert(0, finder)
    subprocess.run = guarded_run  # type: ignore[assignment]
    subprocess.Popen = reject  # type: ignore[assignment]
    subprocess.call = reject  # type: ignore[assignment]
    subprocess.check_call = reject  # type: ignore[assignment]
    subprocess.check_output = reject  # type: ignore[assignment]
    os.system = reject  # type: ignore[assignment]
    os.popen = reject  # type: ignore[assignment]
    socket.create_connection = reject  # type: ignore[assignment]
    socket.socket = reject  # type: ignore[assignment]
    builtins.__import__ = guarded_import  # type: ignore[assignment]
    importlib.import_module = guarded_import_module  # type: ignore[assignment]
    try:
        yield ledger
    finally:
        subprocess.run = originals["run"]  # type: ignore[assignment]
        subprocess.Popen = originals["Popen"]  # type: ignore[assignment]
        subprocess.call = originals["call"]  # type: ignore[assignment]
        subprocess.check_call = originals["check_call"]  # type: ignore[assignment]
        subprocess.check_output = originals["check_output"]  # type: ignore[assignment]
        os.system = originals["os_system"]  # type: ignore[assignment]
        os.popen = originals["os_popen"]  # type: ignore[assignment]
        socket.create_connection = originals["socket"]  # type: ignore[assignment]
        socket.socket = originals["socket_class"]  # type: ignore[assignment]
        builtins.__import__ = originals["import"]  # type: ignore[assignment]
        importlib.import_module = originals["import_module"]  # type: ignore[assignment]
        if finder in sys.meta_path:
            sys.meta_path.remove(finder)


def _all_backend_attempts(value: Any) -> list[Any]:
    attempts: list[Any] = []
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key == "backend_attempts":
                if not isinstance(child, list):
                    raise Phase08CError("backend_attempts field is not a list")
                attempts.extend(child)
            attempts.extend(_all_backend_attempts(child))
    elif isinstance(value, list):
        for child in value:
            attempts.extend(_all_backend_attempts(child))
    return attempts


def _blocked_target_actionable(target: Mapping[str, Any]) -> bool:
    ranking = target.get("tree", {}).get("branch_ranking", {})
    selected = ranking.get("selected_action") if isinstance(ranking, Mapping) else None
    if isinstance(selected, Mapping) and selected.get("action_id") and selected.get("expected_artifact"):
        return True
    blockers = target.get("tree", {}).get("blockers", [])
    return isinstance(blockers, list) and any(isinstance(item, Mapping) for item in blockers)


def _verify_recursive_authority_boundary(value: Any, label: str) -> None:
    for path, key, child in _walk(value):
        dotted = ".".join(path)
        if key in {
            "publication_enabled",
            "can_promote",
            "publishable_as_repair",
            "applicable_to_document_branch",
        } and child is not False:
            raise Phase08CError(f"{label} crossed authority boundary at {dotted}")
        if key == "publication_mode" and child != "disabled":
            raise Phase08CError(f"{label} changed publication mode at {dotted}")
        if key in {"document_ready_repair_proposals", "ready_repair_proposals"} and child != []:
            raise Phase08CError(f"{label} contains a ready/applicable repair at {dotted}")
        if key == "repair_proposal_count" and child != 0:
            raise Phase08CError(f"{label} contains a nonzero repair count at {dotted}")
        if key == "formal_proof_certified" and child is not False:
            raise Phase08CError(f"{label} claims formal proof at {dotted}")


def _walk(value: Any, path: tuple[str, ...] = ()) -> Iterator[tuple[tuple[str, ...], str, Any]]:
    if isinstance(value, Mapping):
        for raw_key, child in value.items():
            key = str(raw_key)
            child_path = (*path, key)
            yield child_path, key, child
            yield from _walk(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            child_path = (*path, str(index))
            yield child_path, str(index), child
            yield from _walk(child, child_path)


def _string_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [str(item) for item in value if isinstance(item, (str, int)) and str(item)]
    return []


def _target_id(target: Mapping[str, Any], index: int) -> str:
    for key in ("id", "row_id", "label"):
        value = target.get(key)
        if isinstance(value, str) and value:
            suffix = f":{target.get('row_index')}" if key == "label" and target.get("row_index") is not None else ""
            return f"target:{value}{suffix}"
    return "target_" + _digest({"index": index, "target": dict(target)})


def _collect_veto_ids(value: Any) -> list[str]:
    values: set[str] = set()
    for _, key, child in _walk(value):
        if (("veto" in key and key.endswith("_ids")) or key in {"launch_vetoes", "vetoes"}):
            values.update(_string_values(child))
    return sorted(values)


def _assumption_record(value: Mapping[str, Any]) -> dict[str, Any]:
    record = {
        key: deepcopy(value.get(key))
        for key in (
            "id",
            "status",
            "text",
            "statement",
            "assumptions",
            "role",
            "branch_id",
            "source",
            "evidence_refs",
            "source_refs",
        )
        if key in value
    }
    if not isinstance(record.get("id"), str) or not record["id"]:
        record["id"] = "assumption_" + _digest(dict(value))
        record["id_authority"] = "synthetic_presentation_identity"
    return record


def _unresolved_assumptions(value: Any) -> list[dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for path, key, child in _walk(value):
        if key.endswith("unresolved_assumption_ids") or key.endswith("missing_assumption_ids") or key.endswith("blocked_by_assumption_ids"):
            for item in _string_values(child):
                records.setdefault(item, {"id": item, "status": "unresolved"})
        if key in {"missing_route_assumptions", "missing_or_unresolved_assumptions", "unresolved_assumptions"}:
            for item in _string_values(child):
                item_id = "assumption_" + _digest({"field": key, "text": item})
                records.setdefault(
                    item_id,
                    {
                        "id": item_id,
                        "status": "unresolved",
                        "text": item,
                        "id_authority": "synthetic_presentation_identity",
                    },
                )
        if not isinstance(child, Mapping):
            continue
        status = str(child.get("status", ""))
        if status not in {"missing", "unresolved"} or not any("assumption" in part for part in path):
            continue
        record = _assumption_record(child)
        records.setdefault(str(record["id"]), record)
    return [records[key] for key in sorted(records)]


def _candidate_assumptions(value: Any) -> list[dict[str, Any]]:
    records: dict[bytes, dict[str, Any]] = {}
    for path, key, child in _walk(value):
        if key == "proposed_assumptions":
            for item in _string_values(child):
                record = {
                    "id": "candidate_assumption_" + _digest(item),
                    "status": "candidate",
                    "text": item,
                    "id_authority": "synthetic_presentation_identity",
                }
                records.setdefault(_canonical(record), record)
        if not isinstance(child, Mapping):
            continue
        status = str(child.get("status", ""))
        context = len(path) >= 2 and path[-2] in {"possible_assumption_sets", "typed_assumptions"}
        if status not in {"candidate", "proposed_sufficient"} and not context:
            continue
        record = _assumption_record(child)
        if not any(record.get(field) for field in ("id", "text", "statement", "assumptions")):
            continue
        record.setdefault("status", "candidate")
        records.setdefault(_canonical(record), record)
    return [records[key] for key in sorted(records)]


def _blocker_records(value: Any) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for _, key, child in _walk(value):
        if "blocker" not in key or key.endswith("_ids") or key.endswith("_count"):
            continue
        if isinstance(child, Mapping):
            records.append(deepcopy(dict(child)))
        elif isinstance(child, list):
            records.extend(deepcopy(dict(item)) for item in child if isinstance(item, Mapping))
    unique: dict[str, dict[str, Any]] = {}
    for record in records:
        record_id = str(record.get("id", "")) or "blocker_" + _digest(record)
        normalized = deepcopy(record)
        normalized["id"] = record_id
        unique.setdefault(_digest(normalized), normalized)
    return [unique[key] for key in sorted(unique)]


def _selected_action(value: Any) -> dict[str, Any] | None:
    if isinstance(value, Mapping):
        tree = value.get("tree") if isinstance(value.get("tree"), Mapping) else value
        ranking = tree.get("branch_ranking") if isinstance(tree.get("branch_ranking"), Mapping) else {}
        action = ranking.get("selected_action")
        if isinstance(action, Mapping) and action:
            return deepcopy(dict(action))
    for _, key, child in _walk(value):
        if key == "selected_action" and isinstance(child, Mapping) and child:
            return deepcopy(dict(child))
    return None


def _fallback_action(target_id: str, blockers: list[dict[str, Any]]) -> dict[str, Any]:
    blocker_ids = sorted(str(item["id"]) for item in blockers)
    next_evidence = next(
        (
            str(item.get("required_next_evidence"))
            for item in blockers
            if isinstance(item.get("required_next_evidence"), str) and item.get("required_next_evidence")
        ),
        "Inspect the target's exact blocker and evidence references before choosing a mathematical route.",
    )
    payload = {
        "action_kind": "inspect_blocker_evidence",
        "target_ids": [target_id],
        "blocker_ids": blocker_ids,
        "required_next_evidence": next_evidence,
        "expected_artifact": {
            "kind": "scoped_diagnostic_followup",
            "binding_fields": ["target_id", "blocker_ids"],
        },
        "authority": "presentation_only",
        "non_claim": "This fallback is not a ranked mathematical action or publication authority.",
    }
    payload["action_id"] = "fallback_action_" + _digest(payload)
    return payload


def _source_ref_entries(value: Any) -> list[dict[str, Any]]:
    refs: list[Any] = []
    for _, key, child in _walk(value):
        if "source_ref" not in key:
            continue
        if isinstance(child, Mapping):
            refs.append(deepcopy(dict(child)))
        elif isinstance(child, list):
            refs.extend(
                deepcopy(dict(item)) if isinstance(item, Mapping) else str(item)
                for item in child
                if isinstance(item, (Mapping, str)) and item
            )
        elif isinstance(child, str) and child:
            refs.append(child)
    unique: dict[str, Any] = {}
    for ref in refs:
        unique.setdefault("source_ref_" + _digest(ref), ref)
    result = []
    for ref_id in sorted(unique):
        record = unique[ref_id]
        result.append(
            {**deepcopy(dict(record)), "source_ref_id": ref_id}
            if isinstance(record, Mapping)
            else {"source_ref_id": ref_id, "ref": str(record)}
        )
    return result


def _evidence_ref_entries(value: Any) -> list[dict[str, str]]:
    refs: set[str] = set()
    for _, key, child in _walk(value):
        is_ref = (
            "evidence_ref" in key
            or key in {"manifest_ref", "request_ref", "result_ref", "output_ref", "artifact_ref"}
            or key.endswith(("_manifest_ref", "_request_ref", "_result_ref", "_output_ref", "_artifact_ref"))
            or key in {"attempt_refs", "request_refs", "result_refs", "output_refs", "artifact_refs", "manifest_refs"}
        )
        if is_ref:
            refs.update(_string_values(child))
    return [
        {"evidence_ref_id": "evidence_ref_" + _digest(ref), "ref": ref}
        for ref in sorted(refs)
    ]


def _independent_compact_target(target: Mapping[str, Any], index: int) -> dict[str, Any]:
    target_id = _target_id(target, index)
    blockers = _blocker_records(target)
    return {
        "target_id": target_id,
        "label": target.get("label"),
        "row_id": target.get("row_id"),
        "row_index": target.get("row_index"),
        "location": target.get("location"),
        "status": target.get("status"),
        "publication_mode": target.get("publication_mode", "disabled"),
        "promotion": deepcopy(target.get("promotion", {})),
        "failure_classifications": sorted(set(_string_values(target.get("failure_classifications", [])))),
        "veto_ids": _collect_veto_ids(target),
        "unresolved_assumptions": _unresolved_assumptions(target),
        "candidate_assumptions": _candidate_assumptions(target),
        "blocker_ids": sorted({str(item["id"]) for item in blockers}),
        "selected_action": _selected_action(target) or _fallback_action(target_id, blockers),
        "evidence_refs": _evidence_ref_entries(target),
        "source_refs": _source_ref_entries(target),
        "reference_resolution": "exact_current_page_records",
    }


def _verify_raw_audit(document: str, audit: Mapping[str, Any]) -> None:
    binding = SOURCE_BINDINGS[document]
    execution = audit.get("execution") if isinstance(audit.get("execution"), Mapping) else {}
    coverage = audit.get("coverage") if isinstance(audit.get("coverage"), Mapping) else {}
    targets = [item for item in audit.get("targets", []) if isinstance(item, Mapping)]
    context_targets = [item for item in audit.get("context_targets", []) if isinstance(item, Mapping)]
    if (
        audit.get("tex_path") != binding["ref"]
        or audit.get("backend_env") != "mathdevmcp-backends"
        or audit.get("search_mode") != "agent_guided"
        or audit.get("grounding_policy") != "strict"
        or audit.get("publication_mode") != "disabled"
        or audit.get("promotion", {}).get("can_promote") is not False
        or execution.get("mode") != "serial"
        or execution.get("workers_requested") != 1
        or execution.get("workers_used") != 1
        or execution.get("failure_count") != 0
        or execution.get("failures") != []
        or coverage.get("missing_focus_labels") != []
        or coverage.get("tool_grounded_compiler_validation_error_count") != 0
        or coverage.get("document_ready_repair_proposal_count") != 0
        or coverage.get("promoted_count") != 0
        or coverage.get("raw_promoted_count") != 0
        or [item.get("label") for item in targets] != binding["target_labels"]
        or [item.get("label") for item in context_targets] != binding["context_labels"]
        or coverage.get("context_target_labels") != binding["context_labels"]
    ):
        raise Phase08CError(f"{document} raw audit boundary mismatch")
    if _all_backend_attempts(audit):
        raise Phase08CError(f"{document} raw audit contains mathematical backend attempts")
    _verify_recursive_authority_boundary(audit, f"{document} raw audit")
    for target in targets:
        classifications = set(str(item) for item in target.get("failure_classifications", []))
        compiler = target.get("tree", {}).get("tool_grounded_proposal_compiler", {})
        if (
            target.get("claim_type") == "worker_failure"
            or "engineering_error" in classifications
            or not isinstance(compiler, Mapping)
            or compiler.get("validation_errors") != []
            or compiler.get("repair_proposal_count") != 0
            or compiler.get("document_ready_repair_proposals") != []
            or any(
                isinstance(item, Mapping) and item.get("publishable_as_repair") is not False
                for item in compiler.get("compiled_items", [])
            )
            or not _blocked_target_actionable(target)
        ):
            raise Phase08CError(f"{document} target failed actionability/engineering boundary")


def _verify_views(
    document: str,
    audit: Mapping[str, Any],
    request: Mapping[str, Any],
    compact: Mapping[str, Any],
    detailed: Mapping[str, Any],
    artifact_root: Path,
    response_module: Any,
) -> dict[str, Any]:
    for response in (compact, detailed):
        errors = response_module.validate_document_derivation_response(audit, response)
        if errors:
            raise Phase08CError(f"{document} response validation failed: {errors}")
        if (
            response.get("audit_request_id") != request.get("audit_request_id")
            or response.get("publication_mode") != "disabled"
            or response.get("promotion", {}).get("can_promote") is not False
        ):
            raise Phase08CError(f"{document} response authority mismatch")
        _verify_recursive_authority_boundary(
            response,
            f"{document} {response.get('response_mode')} response",
        )
    global_fields = [
        "audit_result_id",
        "audit_request_id",
        "audit_status",
        "status",
        "source_ref",
        "publication_mode",
        "promotion",
        "coverage",
        "failure_classifications",
        "veto_ids",
        "unresolved_assumption_ids",
        "candidate_assumption_ids",
        "action_decision_ids",
        "reference_inventory",
        "non_claims",
        "execution_summary",
        "completeness",
    ]
    for field in global_fields:
        if compact.get(field) != detailed.get(field):
            raise Phase08CError(f"{document} compact/detailed global parity mismatch: {field}")
    raw_targets = [item for item in audit.get("targets", []) if isinstance(item, Mapping)]
    compact_targets = [item for item in compact.get("targets", []) if isinstance(item, Mapping)]
    detailed_targets = [item for item in detailed.get("targets", []) if isinstance(item, Mapping)]
    if len(compact_targets) != len(raw_targets) or detailed_targets != raw_targets:
        raise Phase08CError(f"{document} compact/detailed target count or raw parity mismatch")
    for index, (raw_target, compact_target) in enumerate(zip(raw_targets, compact_targets, strict=True)):
        expected = _independent_compact_target(raw_target, index)
        ranking = raw_target.get("tree", {}).get("branch_ranking", {})
        selected = ranking.get("selected_action") if isinstance(ranking, Mapping) else None
        action = compact_target.get("selected_action")
        if (
            compact_target != expected
            or
            not isinstance(action, Mapping)
            or not action.get("action_id")
            or not action.get("expected_artifact")
            or (isinstance(selected, Mapping) and selected and action != selected)
            or not compact_target.get("reference_resolution")
            or compact_target.get("publication_mode") != "disabled"
            or compact_target.get("promotion", {}).get("can_promote") is not False
        ):
            raise Phase08CError(f"{document} compact action is unusable")
    compact_raw = response_module.canonical_document_derivation_response_bytes(compact)
    detailed_raw = response_module.canonical_document_derivation_response_bytes(detailed)
    for raw in (compact_raw, detailed_raw):
        text = raw.decode("utf-8")
        if str(WORKSPACE) in text or LOCAL_ABSOLUTE_PATH_FRAGMENT.search(text):
            raise Phase08CError(f"{document} response leaked a private/local path")
    return {
        "document": document,
        "audit_result_id": compact["audit_result_id"],
        "audit_request_id": compact["audit_request_id"],
        "target_labels": [item.get("label") for item in compact_targets],
        "context_target_labels": SOURCE_BINDINGS[document]["context_labels"],
        "compact_canonical_bytes": len(compact_raw),
        "compact_pretty_bytes": len(json.dumps(compact, ensure_ascii=False, indent=2).encode("utf-8")),
        "detailed_canonical_bytes": len(detailed_raw),
        "compact_size_status": "met" if len(compact_raw) <= COMPACT_LIMIT else "exceeded_complete_boundary_preserved",
        "semantic_parity": True,
        "actionability": True,
        "private_path_free": True,
        "publication_enabled": False,
    }


def _artifact_inventory(continuation: Path, refs: Sequence[str]) -> list[dict[str, Any]]:
    if not isinstance(refs, Sequence) or isinstance(refs, (str, bytes, bytearray)):
        raise Phase08CError("artifact inventory refs must be a sequence")
    normalized = [_safe_ref(ref, "artifact inventory ref") for ref in refs]
    if len(normalized) != len(set(normalized)):
        raise Phase08CError("artifact inventory contains duplicate refs")
    records = []
    for ref in sorted(normalized):
        raw = _regular_bytes(continuation / ref, root=continuation)
        records.append({"ref": ref, "sha256": _digest(raw), "byte_count": len(raw)})
    return records


def _persisted_artifact_refs(continuation: Path) -> list[str]:
    root = continuation / "detailed-artifacts"
    refs: list[str] = []
    if root.exists():
        for path in sorted(root.rglob("*"), key=lambda item: item.relative_to(root).as_posix()):
            if path.is_symlink() or (not path.is_dir() and not path.is_file()):
                raise Phase08CError("detailed artifact tree contains an unsafe entry")
            if path.is_file():
                refs.append(path.relative_to(continuation).as_posix())
    return refs


def _verify_persisted_detailed_artifact(
    continuation: Path,
    document: str,
    audit: Mapping[str, Any],
    request: Mapping[str, Any],
    compact: Mapping[str, Any],
    detailed: Mapping[str, Any],
) -> None:
    artifact = compact.get("artifact")
    if not isinstance(artifact, Mapping) or artifact != detailed.get("artifact"):
        raise Phase08CError(f"{document} persisted artifact metadata parity mismatch")
    expected_ref = (
        f"detailed-artifacts/{document}/document-derivation/"
        f"{compact.get('audit_result_id')}/{compact.get('audit_request_id')}/detailed.json"
    )
    raw = _regular_bytes(continuation / expected_ref, root=continuation)
    record = _decode_canonical(raw, f"{document} persisted detailed artifact")
    stripped = deepcopy(dict(audit))
    for key in ("markdown", "output_md", "output_json"):
        stripped.pop(key, None)
    expected = {
        "schema_version": "p07_document_derivation_artifact@1",
        "audit_result_id": compact.get("audit_result_id"),
        "audit_request_id": compact.get("audit_request_id"),
        "audit_request": dict(request),
        "audit": stripped,
        "authority": "local_byte_identity_only",
        "non_claim": "This artifact is a diagnostic audit record, not a mathematical certificate or publication authority.",
    }
    if (
        record != expected
        or artifact.get("state") != "verified"
        or artifact.get("sha256") != _digest(raw)
        or artifact.get("byte_count") != len(raw)
        or artifact.get("schema_version") != "p07_document_derivation_artifact@1"
        or artifact.get("authority") != "local_byte_identity_only"
    ):
        raise Phase08CError(f"{document} persisted detailed artifact reconstruction mismatch")


def _verify_exact_continuation_files(
    continuation: Path,
    identity: Mapping[str, Any],
    decision: Mapping[str, Any],
) -> None:
    expected = {
        "code-identity.json",
        "decision.json",
        *(
            "code-snapshot/" + str(item.get("ref"))
            for item in identity.get("files", [])
            if isinstance(item, Mapping)
        ),
        *(
            str(item.get("ref"))
            for item in decision.get("artifact_inventory", [])
            if isinstance(item, Mapping)
        ),
    }
    actual: set[str] = set()
    actual_directories: set[str] = set()
    for path in continuation.rglob("*"):
        if path.is_symlink() or (not path.is_dir() and not path.is_file()):
            raise Phase08CError("P08C continuation contains an unsafe entry")
        if path.is_file():
            actual.add(path.relative_to(continuation).as_posix())
        elif path.is_dir():
            actual_directories.add(path.relative_to(continuation).as_posix())
    expected_directories: set[str] = set()
    for ref in expected:
        parent = PurePosixPath(ref).parent
        while parent != PurePosixPath("."):
            expected_directories.add(parent.as_posix())
            parent = parent.parent
    if actual != expected or actual_directories != expected_directories:
        raise Phase08CError("P08C continuation file set differs from registered identities")


def _create(args: argparse.Namespace) -> dict[str, Any]:
    if Path(__file__).resolve() != (WORKSPACE / RUNNER_REF).resolve():
        raise Phase08CError("create must execute the reviewed live P08C runner path")
    if args.parent_run_root != PARENT_REF or args.continuation_root != CONTINUATION_PARENT_REF:
        raise Phase08CError("create requires the literal reviewed parent and continuation roots")
    if (args.budget_profile, args.max_attempts, args.workers, args.target_limit) != ("smoke", 0, 1, 20):
        raise Phase08CError("P08C request controls differ from the reviewed exact values")
    parent_binding = _verify_parent()

    parent = WORKSPACE / CONTINUATION_PARENT_REF
    _assert_no_symlink(parent)
    parent.mkdir(parents=True, exist_ok=True)
    continuation_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + uuid.uuid4().hex[:12]
    continuation = parent / continuation_id
    continuation.mkdir(mode=0o700)
    continuation_ref = continuation.relative_to(WORKSPACE).as_posix()
    binding = _digest(
        {
            "continuation_id": continuation_id,
            "continuation_root": continuation_ref,
            "parent_run_binding_digest": PARENT_RUN_BINDING,
            "phase": "P08C",
        }
    )
    try:
        identity = _snapshot_code(continuation, continuation_id, binding)
        manifest = {
            "schema_version": "p08c_continuation_manifest@1",
            "continuation_id": continuation_id,
            "continuation_root": continuation_ref,
            "continuation_binding_digest": binding,
            "parent_run_root": PARENT_REF,
            "parent_run_binding_digest": PARENT_RUN_BINDING,
            "code_identity_digest": identity["code_identity_digest"],
            "created_at_utc": _utc_now(),
            "python_executable": sys.executable,
            "python_version": sys.version.split()[0],
            "cpu_gpu_status": "CPU-only; GPU devices intentionally hidden with CUDA_VISIBLE_DEVICES=-1",
            "request_controls": {
                "max_labels": 30,
                "budget_profile": args.budget_profile,
                "max_attempts": args.max_attempts,
                "backend_env": "mathdevmcp-backends",
                "search_mode": "agent_guided",
                "grounding_policy": "strict",
                "workers": args.workers,
                "target_limit": args.target_limit,
            },
            "raw_audit_invocations": {"card": 1, "risky": 1},
            "publication_enabled": False,
        }
        _write_json_new(continuation / "manifest.json", manifest)
        _write_json_new(continuation / "parent-binding.json", parent_binding)

        document_records: dict[str, Any] = {}
        all_probes: list[dict[str, Any]] = []
        invocation_counts = {"card": 0, "risky": 0}
        probe_class_counts: dict[str, dict[str, int]] = {}
        with _guarded_probes() as probe_ledger:
            from mathdevmcp.document_derivation_response import (
                build_document_derivation_audit_request,
                compile_document_derivation_response,
            )
            import mathdevmcp.document_derivation_response as response_module
            from mathdevmcp.document_derivation_tree import audit_document_derivation_tree

            for document, binding_record in SOURCE_BINDINGS.items():
                probe_start = len(probe_ledger)
                request = build_document_derivation_audit_request(
                    binding_record["ref"],
                    focus_labels=binding_record["focus_labels"],
                    max_labels=30,
                    budget_profile=args.budget_profile,
                    max_attempts=args.max_attempts,
                    backend_env="mathdevmcp-backends",
                    search_mode="agent_guided",
                    grounding_policy="strict",
                    workers=args.workers,
                )
                audit = audit_document_derivation_tree(
                    binding_record["ref"],
                    focus_labels=binding_record["focus_labels"],
                    max_labels=30,
                    budget_profile=args.budget_profile,
                    max_attempts=args.max_attempts,
                    backend_env="mathdevmcp-backends",
                    search_mode="agent_guided",
                    grounding_policy="strict",
                    workers=args.workers,
                )
                invocation_counts[document] += 1
                document_probes = probe_ledger[probe_start:]
                counts = {
                    classification: sum(
                        item.get("classification") == classification
                        for item in document_probes
                    )
                    for classification in EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT
                }
                if counts != EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT:
                    raise Phase08CError(
                        f"{document} doctor probe coverage differs from the reviewed call graph: {counts}"
                    )
                for item in document_probes:
                    if "document" in item:
                        raise Phase08CError("doctor probe already has an untrusted document binding")
                    item["document"] = document
                probe_class_counts[document] = counts
                _verify_raw_audit(document, audit)
                artifact_root = continuation / "detailed-artifacts" / document
                compact = compile_document_derivation_response(
                    audit,
                    request,
                    response_mode="compact",
                    artifact_root=artifact_root,
                    target_limit=args.target_limit,
                )
                detailed = compile_document_derivation_response(
                    audit,
                    request,
                    response_mode="detailed",
                    artifact_root=artifact_root,
                    target_limit=args.target_limit,
                )
                comparison = _verify_views(
                    document,
                    audit,
                    request,
                    compact,
                    detailed,
                    artifact_root,
                    response_module,
                )
                _verify_persisted_detailed_artifact(
                    continuation,
                    document,
                    audit,
                    request,
                    compact,
                    detailed,
                )
                for name, value in (
                    ("request", request),
                    ("audit", audit),
                    ("compact", compact),
                    ("detailed", detailed),
                ):
                    _write_json_new(continuation / "p08c" / f"{document}-{name}.json", value)
                document_records[document] = comparison
            all_probes.extend(deepcopy(probe_ledger))
        if invocation_counts != {"card": 1, "risky": 1}:
            raise Phase08CError("raw document workflow invocation count mismatch")
        _write_json_new(
            continuation / "p08c/probe-ledger.json",
            {
                "schema_version": "p08c_probe_ledger@1",
                "probes": all_probes,
                "per_document_classification_counts": probe_class_counts,
                "mathematical_backend_attempt_count": 0,
                "publication_enabled": False,
            },
        )
        parity = {
            "schema_version": "p08c_parity_and_size@1",
            "documents": [document_records[key] for key in SOURCE_BINDINGS],
            "primary_criterion_met": all(
                record["semantic_parity"]
                and record["actionability"]
                and record["private_path_free"]
                and record["compact_size_status"] == "met"
                for record in document_records.values()
            ),
            "publication_enabled": False,
            "non_claims": [
                "P08C does not prove either document.",
                "P08C does not establish a best or applicable repair.",
                "Payload size and response parity are product evidence only.",
            ],
        }
        _write_json_new(continuation / "p08c/parity-and-size.json", parity)
        refs = [
            "manifest.json",
            "parent-binding.json",
            "p08c/card-request.json",
            "p08c/card-audit.json",
            "p08c/card-compact.json",
            "p08c/card-detailed.json",
            "p08c/risky-request.json",
            "p08c/risky-audit.json",
            "p08c/risky-compact.json",
            "p08c/risky-detailed.json",
            "p08c/probe-ledger.json",
            "p08c/parity-and-size.json",
        ] + _persisted_artifact_refs(continuation)
        inventory = _artifact_inventory(continuation, refs)
        decision = {
            "schema_version": "p08c_decision@1",
            "status": (
                "PASS_P08C_FROZEN_AGENT_FACING_WORKFLOW"
                if parity["primary_criterion_met"]
                else "INCOMPLETE_P08C_PRODUCT_CRITERION"
            ),
            "continuation_id": continuation_id,
            "continuation_binding_digest": binding,
            "parent_run_binding_digest": PARENT_RUN_BINDING,
            "code_identity_digest": identity["code_identity_digest"],
            "artifact_inventory": inventory,
            "artifact_inventory_digest": _digest(inventory),
            "raw_audit_invocations": {"card": 1, "risky": 1},
            "mathematical_backend_attempt_count": 0,
            "formal_proof_certified": False,
            "can_promote": False,
            "publication_enabled": False,
            "vetoes": [] if parity["primary_criterion_met"] else ["compact_product_criterion_not_met"],
            "non_claims": parity["non_claims"],
        }
        decision["decision_digest"] = _digest(decision)
        _write_json_new(continuation / "decision.json", decision)
        _verify_code_identity(continuation)
        _verify_exact_continuation_files(continuation, identity, decision)
        return {
            "status": decision["status"],
            "continuation_id": continuation_id,
            "continuation_root": continuation_ref,
            "decision_digest": decision["decision_digest"],
            "publication_enabled": False,
        }
    except Exception:
        marker = continuation / "FAILED_DURING_CREATE.txt"
        if not marker.exists():
            _write_new(marker, b"P08C create failed; preserve this continuation for diagnosis.\n")
        raise


def _open_continuation(raw_ref: str) -> Path:
    value = PurePosixPath(raw_ref)
    if value.parent != PurePosixPath(CONTINUATION_PARENT_REF) or not value.name:
        raise Phase08CError("verify requires a literal continuations/<continuation-id> root")
    if value.name in {"current", "latest"} or any(char in raw_ref for char in "*?[]"):
        raise Phase08CError("implicit/latest/glob continuation selection is forbidden")
    continuation = WORKSPACE / value.as_posix()
    _assert_no_symlink(continuation)
    if not continuation.is_dir():
        raise Phase08CError("P08C continuation root is missing")
    return continuation


def _verify(args: argparse.Namespace) -> dict[str, Any]:
    continuation = _open_continuation(args.continuation_root)
    expected_runner = continuation / "code-snapshot" / RUNNER_REF
    if Path(__file__).resolve() != expected_runner.resolve():
        raise Phase08CError("verify must execute the continuation's snapshotted runner")
    parent_binding = _verify_parent()
    manifest = _load_canonical(continuation / "manifest.json")
    identity = _load_canonical(continuation / "code-identity.json")
    decision = _load_canonical(continuation / "decision.json")
    _verify_semantic_digest(decision, "decision_digest", str(decision.get("decision_digest")))
    if args.expected_decision_digest != decision.get("decision_digest"):
        raise Phase08CError("P08C decision digest differs from the literal create handoff")
    _verify_code_identity(continuation, require_loaded_modules=False)
    expected_binding = _digest(
        {
            "continuation_id": manifest.get("continuation_id"),
            "continuation_root": args.continuation_root,
            "parent_run_binding_digest": PARENT_RUN_BINDING,
            "phase": "P08C",
        }
    )
    if (
        manifest.get("schema_version") != "p08c_continuation_manifest@1"
        or set(manifest)
        != {
            "schema_version",
            "continuation_id",
            "continuation_root",
            "continuation_binding_digest",
            "parent_run_root",
            "parent_run_binding_digest",
            "code_identity_digest",
            "created_at_utc",
            "python_executable",
            "python_version",
            "cpu_gpu_status",
            "request_controls",
            "raw_audit_invocations",
            "publication_enabled",
        }
        or
        manifest.get("continuation_root") != args.continuation_root
        or manifest.get("continuation_binding_digest") != expected_binding
        or manifest.get("parent_run_root") != PARENT_REF
        or manifest.get("parent_run_binding_digest") != PARENT_RUN_BINDING
        or manifest.get("code_identity_digest") != identity.get("code_identity_digest")
        or manifest.get("raw_audit_invocations") != {"card": 1, "risky": 1}
        or manifest.get("python_executable") != P08_PYTHON
        or manifest.get("python_version") != sys.version.split()[0]
        or manifest.get("cpu_gpu_status")
        != "CPU-only; GPU devices intentionally hidden with CUDA_VISIBLE_DEVICES=-1"
        or manifest.get("request_controls")
        != {
            "max_labels": 30,
            "budget_profile": "smoke",
            "max_attempts": 0,
            "backend_env": "mathdevmcp-backends",
            "search_mode": "agent_guided",
            "grounding_policy": "strict",
            "workers": 1,
            "target_limit": 20,
        }
        or manifest.get("publication_enabled") is not False
        or identity.get("continuation_binding_digest") != expected_binding
        or identity.get("continuation_id") != manifest.get("continuation_id")
        or identity.get("schema_version") != "p08c_code_identity@1"
        or identity.get("runtime")
        != {
            "python": P08_PYTHON,
            "flags": ["-I", "-S", "-B", "-X", "pycache_prefix=/dev/null"],
            "source_root": str(SOURCE_ROOT),
            "module_origin_policy": "source_only_no_bytecode",
        }
        or identity.get("boundary")
        != "P08C source identity has no proof, promotion, publication, or parent-rewrite authority."
        or decision.get("code_identity_digest") != identity.get("code_identity_digest")
        or decision.get("continuation_binding_digest") != expected_binding
        or decision.get("parent_run_binding_digest") != PARENT_RUN_BINDING
    ):
        raise Phase08CError("P08C continuation manifest/identity binding mismatch")
    stored_parent = _load_canonical(continuation / "parent-binding.json")
    if stored_parent != parent_binding:
        raise Phase08CError("P08C parent binding differs from independent reconstruction")

    from mathdevmcp.document_derivation_response import canonical_document_derivation_response_bytes
    import mathdevmcp.document_derivation_response as response_module

    identity = _verify_code_identity(continuation)

    reconstructed: dict[str, Any] = {}
    for document in SOURCE_BINDINGS:
        request = _load_canonical(continuation / "p08c" / f"{document}-request.json")
        audit = _load_canonical(continuation / "p08c" / f"{document}-audit.json")
        compact = _load_canonical(continuation / "p08c" / f"{document}-compact.json")
        detailed = _load_canonical(continuation / "p08c" / f"{document}-detailed.json")
        _verify_raw_audit(document, audit)
        artifact_root = continuation / "detailed-artifacts" / document
        reconstructed[document] = _verify_views(
            document,
            audit,
            request,
            compact,
            detailed,
            artifact_root,
            response_module,
        )
        _verify_persisted_detailed_artifact(
            continuation,
            document,
            audit,
            request,
            compact,
            detailed,
        )
        if len(canonical_document_derivation_response_bytes(compact)) != compact["canonical_byte_count"]:
            raise Phase08CError("compact byte count differs from independent serialization")
    stored_parity = _load_canonical(continuation / "p08c/parity-and-size.json")
    expected_parity = {
        "schema_version": "p08c_parity_and_size@1",
        "documents": [reconstructed[key] for key in SOURCE_BINDINGS],
        "primary_criterion_met": all(
            record["semantic_parity"]
            and record["actionability"]
            and record["private_path_free"]
            and record["compact_size_status"] == "met"
            for record in reconstructed.values()
        ),
        "publication_enabled": False,
        "non_claims": [
            "P08C does not prove either document.",
            "P08C does not establish a best or applicable repair.",
            "Payload size and response parity are product evidence only.",
        ],
    }
    if stored_parity != expected_parity:
        raise Phase08CError("P08C parity/size artifact differs from independent reconstruction")
    probe = _load_canonical(continuation / "p08c/probe-ledger.json")
    probes = probe.get("probes")
    reconstructed_probe_counts = (
        _probe_counts_by_document(probes)
        if isinstance(probes, list) and all(isinstance(item, Mapping) for item in probes)
        else None
    )
    if (
        probe.get("schema_version") != "p08c_probe_ledger@1"
        or set(probe)
        != {
            "schema_version",
            "probes",
            "per_document_classification_counts",
            "mathematical_backend_attempt_count",
            "publication_enabled",
        }
        or not isinstance(probes, list)
        or not probes
        or probe.get("per_document_classification_counts")
        != {
            document: dict(EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT)
            for document in SOURCE_BINDINGS
        }
        or reconstructed_probe_counts != probe.get("per_document_classification_counts")
        or probe.get("mathematical_backend_attempt_count") != 0
        or probe.get("publication_enabled") is not False
        or any(not isinstance(item, Mapping) for item in probes)
        or any(
            _classify_probe(item.get("argv", [])) != item.get("classification")
            or item.get("allowed") is not True
            or set(item)
            != {
                "sequence",
                "document",
                "classification",
                "argv",
                "input_byte_count",
                "timeout_seconds",
                "returncode",
                "stdout_byte_count",
                "stdout_sha256",
                "stderr_byte_count",
                "stderr_sha256",
                "wall_time_ms",
                "mathematical_input",
                "evidence_authority",
                "allowed",
            }
            or item.get("sequence") != index
            or item.get("document") not in SOURCE_BINDINGS
            or item.get("input_byte_count") != 0
            or item.get("timeout_seconds") != PROBE_TIMEOUT_SECONDS
            or item.get("stdout_byte_count", PROBE_OUTPUT_LIMIT + 1) > PROBE_OUTPUT_LIMIT
            or item.get("stderr_byte_count", PROBE_OUTPUT_LIMIT + 1) > PROBE_OUTPUT_LIMIT
            or item.get("mathematical_input") is not False
            or item.get("evidence_authority") != "operational_provenance_only"
            or not isinstance(item.get("returncode"), int)
            or not isinstance(item.get("wall_time_ms"), int)
            or item.get("wall_time_ms", -1) < 0
            or not isinstance(item.get("stdout_sha256"), str)
            or len(item.get("stdout_sha256", "")) != 64
            or not isinstance(item.get("stderr_sha256"), str)
            or len(item.get("stderr_sha256", "")) != 64
            for index, item in enumerate(probes, start=1)
            if isinstance(item, Mapping)
        )
    ):
        raise Phase08CError("P08C probe ledger boundary mismatch")
    refs = [item.get("ref") for item in decision.get("artifact_inventory", [])]
    inventory = _artifact_inventory(continuation, refs)
    expected_status = (
        "PASS_P08C_FROZEN_AGENT_FACING_WORKFLOW"
        if expected_parity["primary_criterion_met"]
        else "INCOMPLETE_P08C_PRODUCT_CRITERION"
    )
    expected_vetoes = [] if expected_parity["primary_criterion_met"] else [
        "compact_product_criterion_not_met"
    ]
    expected_non_claims = expected_parity["non_claims"]
    if (
        decision.get("schema_version") != "p08c_decision@1"
        or set(decision)
        != {
            "schema_version",
            "status",
            "continuation_id",
            "continuation_binding_digest",
            "parent_run_binding_digest",
            "code_identity_digest",
            "artifact_inventory",
            "artifact_inventory_digest",
            "raw_audit_invocations",
            "mathematical_backend_attempt_count",
            "formal_proof_certified",
            "can_promote",
            "publication_enabled",
            "vetoes",
            "non_claims",
            "decision_digest",
        }
        or
        decision.get("status") != expected_status
        or decision.get("continuation_id") != manifest.get("continuation_id")
        or decision.get("continuation_binding_digest") != expected_binding
        or decision.get("parent_run_binding_digest") != PARENT_RUN_BINDING
        or decision.get("code_identity_digest") != identity.get("code_identity_digest")
        or decision.get("artifact_inventory") != inventory
        or decision.get("artifact_inventory_digest") != _digest(inventory)
        or decision.get("raw_audit_invocations") != {"card": 1, "risky": 1}
        or decision.get("mathematical_backend_attempt_count") != 0
        or decision.get("formal_proof_certified") is not False
        or decision.get("can_promote") is not False
        or decision.get("publication_enabled") is not False
        or decision.get("vetoes") != expected_vetoes
        or decision.get("non_claims") != expected_non_claims
    ):
        raise Phase08CError("P08C decision differs from independent reconstruction")
    _verify_code_identity(continuation)
    _verify_exact_continuation_files(continuation, identity, decision)
    return {
        "status": decision["status"],
        "continuation_id": manifest["continuation_id"],
        "continuation_root": args.continuation_root,
        "decision_digest": decision["decision_digest"],
        "verified": True,
        "publication_enabled": False,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create")
    create.add_argument("--parent-run-root", required=True)
    create.add_argument("--continuation-root", required=True)
    create.add_argument("--budget-profile", required=True)
    create.add_argument("--max-attempts", required=True, type=int)
    create.add_argument("--workers", required=True, type=int)
    create.add_argument("--target-limit", required=True, type=int)
    create.set_defaults(handler=_create)
    verify = subparsers.add_parser("verify")
    verify.add_argument("--continuation-root", required=True)
    verify.add_argument("--expected-decision-digest", required=True)
    verify.set_defaults(handler=_verify)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    try:
        _require_runtime()
        _activate_repo_source()
        _verify_source_tree_cache_policy()
        args = build_parser().parse_args(argv)
        result = args.handler(args)
        sys.stdout.buffer.write(_canonical(result) + b"\n")
        return 0
    except (Phase08CError, OSError, ValueError) as exc:
        sys.stderr.write(f"P08C_ERROR: {type(exc).__name__}: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
