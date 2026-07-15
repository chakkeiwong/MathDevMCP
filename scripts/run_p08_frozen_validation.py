#!/usr/bin/env python3
"""Run the immutable, publication-disabled Phase 08 validation gates."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import hashlib
import importlib
import importlib.abc
import json
import os
from pathlib import Path, PurePosixPath
import selectors
import socket
import stat
import subprocess
import sys
import time
import uuid
from typing import Any, Mapping, Sequence


PHASE_ROOT = PurePosixPath(".local/mathdevmcp/evidence/p08-20260714")
P08_PYTHON = "/home/chakwong/miniconda3/envs/tfgpu/bin/python3"
P08_RAW_STREAM_LIMIT = 262_144
P08_BUNDLE_LIMIT = 1_048_576
P08_BUNDLE_OVERHEAD = 16_384
P08_WORKER_ENVIRONMENT = {
    "CUDA_VISIBLE_DEVICES": "-1",
    "LANG": "C.UTF-8",
    "LC_ALL": "C.UTF-8",
}
P08_WORKER_PYTHON_FLAGS = [
    "-I",
    "-S",
    "-B",
    "-X",
    "pycache_prefix=/dev/null",
]
RUN_SCHEMA = "p08_run_manifest@1"
CODE_SCHEMA = "p08_code_identity@1"
SOURCE_SCHEMA = "p08_source_manifest@1"
EXTRACTION_SCHEMA = "p08_extraction@1"
CONTEXT_SCHEMA = "p08_context@1"
DECISION_SCHEMA = "p08a_decision@1"
CAPABILITY_SCHEMA = "p08_capability_preflight@1"
FORMALIZATION_SCHEMA = "p08_source_bound_formalization@1"
TOOL_LEDGER_SCHEMA = "p08_external_tool_ledger@1"
CAPABILITY_LADDER_SCHEMA = "p08_capability_ladder@1"
CAPABILITY_MANIFEST_SCHEMA = "p08_capability_bundle_manifest@1"
CAPABILITY_DECISION_SCHEMA = "p08_capability_decision@1"
DERIVATIVE_ADAPTER_REF = "src/mathdevmcp/sympy_derivative_adapter.py"
DERIVATIVE_ADAPTER_VERSION = "p08-sympy-derivative-adapter@1"
DERIVATIVE_OPERATION = "construct_scalar_derivative_then_compare"
DERIVATIVE_STATUSES = [
    "backend_checked",
    "execution_error",
    "malformed_output",
    "source_target_mismatch",
    "timeout",
    "truncated_output",
    "unavailable",
    "unsupported",
]

SOURCE_BINDINGS = {
    "card": {
        "ref": "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex",
        "sha256": "dada009a7bdc08c8bb14fd8be5bb2ac737fc0d02f82b25638677e7535845cbf8",
        "budget": {
            "max_files": 1,
            "max_bytes": 469_323,
            "max_nodes": 4_096,
            "max_edges": 8_192,
            "max_dependency_expansions": 1,
        },
    },
    "risky": {
        "ref": "docs/risky-debt-maliar-deep-learning-lecture-note.tex",
        "sha256": "d66501516115493b9ffe6d0cc9b2eb85964dc352aba6539768b81fd6ad6923c1",
        "budget": {
            "max_files": 1,
            "max_bytes": 117_506,
            "max_nodes": 4_096,
            "max_edges": 8_192,
            "max_dependency_expansions": 1,
        },
    },
}

COMPARATOR_BINDINGS = {
    "card_old_report": {
        "ref": "docs/reviews/credit-card-npv-agent-guided-tool-verified-repair-phase09-2026-07-10.json",
        "sha256": "d5f6705c2d5ed8779086aa38cddc380b31045801dddfd26c784e30123f96f3d6",
    },
    "risky_old_report": {
        "ref": "docs/reviews/risky-debt-agent-guided-tool-verified-repair-phase09-2026-07-10.json",
        "sha256": "6c3928f098262c801d9a94d23030f37df173fd873e232b8d49366fa89491e2aa",
    },
}

EXTRACTION_GROUPS = (
    ("card_capability", "card", ("eq:panel-cf-primitive", "eq:incremental-cash-flow")),
    (
        "card_focus",
        "card",
        ("eq:panel-npv-functional", "eq:incremental-cash-flow", "eq:incremental-npv"),
    ),
    (
        "risky_capability",
        "risky",
        (
            "eq:risky-cash-flow",
            "eq:cashflow-rate-derivative",
            "eq:cashflow-total-k",
            "eq:cashflow-total-b",
        ),
    ),
    ("risky_focus", "risky", ("prop:interior-foc",)),
)

RETAINED_OBLIGATION_DIGESTS = {
    "eq:incremental-cash-flow": "7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0",
    "eq:incremental-npv": "d9f072ac09016b17d5630556329bc871e79386a442c8c26587ef39a0134eeaac",
    "eq:foc-k": "d987e605da2d4e509d0d65289a56e9b7f5d121273543bdf74276b9fb4c23bba5",
    "eq:foc-b": "8d04797cf7e394624890ab2e0b0688f22d86d9194de94af3aa1407fb1a45edca",
}

P08B_SOURCE_PROJECTIONS = {
    "eq:risky-cash-flow": {
        "obligation_digest": "7daeeae3555cbda56cdeca91a3982c159696b20e4e31b8102bdffd69122e557c",
        "document_ref": SOURCE_BINDINGS["risky"]["ref"],
        "document_sha256": SOURCE_BINDINGS["risky"]["sha256"],
        "source_math_sha256": "acfd823aaa242f17f13f2962f22b781ef4d773862e9a9e62aafc87c50135b6ff",
        "normalized_target_sha256": "c55ee319cf306ae7185c22b2801438d705dacc68a9ded0a0f222b2716d63bd18",
        "selected_terms": [
            "\\frac{b'}{1+\\widetilde r(z,k',b')}",
            "\\frac{\\tau \\widetilde r(z,k',b')b'} {(1+\\widetilde r(z,k',b'))(1+r)}",
        ],
        "registered_scalar": "bp/(1 + rt) + tau*rt*bp/((1 + rt)*(1 + r))",
    },
    "eq:cashflow-rate-derivative": {
        "obligation_digest": "60e19a4bb366cc067b8d6fcb12804fe1cd98e8c2ccf9c6425236d7dfe910800b",
        "document_ref": SOURCE_BINDINGS["risky"]["ref"],
        "document_sha256": SOURCE_BINDINGS["risky"]["sha256"],
        "source_math_sha256": "d26671d734eddbebe7349929a5d49c60d12745d40c123bf4cfca930c96aea595",
        "normalized_target_sha256": "1fbd4aaba111ae5a999dd6dc694f0b4c43d9aee83b6d7ae694767f09a5e43207",
        "selected_terms": [
            "e_{\\widetilde r}",
            "\\frac{b'}{(1+\\widetilde r)^2} \\left(-1+\\frac{\\tau}{1+r}\\right)",
        ],
        "registered_scalar": "bp/(1 + rt)**2 * (-1 + tau/(1 + r))",
    },
}

CONTEXT_SPECS = {
    "eq:panel-cf-primitive": (
        "Source declarations applicable to the one-period incremental cash-flow components, baseline contrast, scenario, and downstream policy are available.",
        ("Delta CF", "Delta PPNR", "Delta EL", "Delta Kchg", "Delta Tax", "Delta RelValue", "a", "pi", "s"),
    ),
    "eq:incremental-cash-flow": (
        "Source declarations applicable to the one-period incremental cash-flow components, baseline contrast, scenario, and downstream policy are available.",
        ("Delta CF", "Delta PPNR", "Delta EL", "Delta Kchg", "Delta Tax", "Delta RelValue", "a", "pi", "s"),
    ),
    "eq:panel-npv-functional": (
        "Source declarations applicable to acquisition cost, discounted cash flow, terminal value, conditioning information, scenario, and downstream policy are available.",
        ("Delta NPV", "C acq", "Delta CF", "Delta TV", "delta", "H", "X d", "pi", "s"),
    ),
    "eq:incremental-npv": (
        "Source declarations applicable to acquisition cost, discounted cash flow, terminal value, conditioning information, scenario, and downstream policy are available.",
        ("Delta NPV", "C acq", "Delta CF", "Delta TV", "delta", "H", "I id", "pi", "s"),
    ),
    "eq:risky-cash-flow": (
        "Source declarations applicable to risky-rate cash flow, tax, adjustment cost, capital, debt, and state variables are available.",
        ("e", "widetilde r", "tau", "psi", "pi", "k", "k prime", "b", "b prime", "z"),
    ),
    "eq:cashflow-rate-derivative": (
        "The source definition and declarations needed to interpret the partial derivative of cash flow with respect to the risky-rate argument are available.",
        ("eq:risky-cash-flow", "e", "widetilde r", "tau", "b prime", "r"),
    ),
    "eq:cashflow-total-k": (
        "The source declarations needed for the total derivative with respect to next-period capital, including investment and risky-rate dependence, are available.",
        ("eq:risky-cash-flow", "I", "psi I", "e widetilde r", "widetilde r", "k prime", "b prime", "z"),
    ),
    "eq:cashflow-total-b": (
        "The source declarations needed for the total derivative with respect to next-period debt, including risky-rate dependence, are available.",
        ("eq:risky-cash-flow", "e widetilde r", "widetilde r", "tau", "r", "k prime", "b prime", "z"),
    ),
    "eq:foc-k": (
        "The proposition assumptions and source declarations needed for the interior capital first-order condition and conditional continuation derivative are available.",
        ("prop:interior-foc", "m", "bar e", "beta", "V star k", "k prime", "b prime", "z", "z prime"),
    ),
    "eq:foc-b": (
        "The proposition assumptions and source declarations needed for the interior debt first-order condition and conditional continuation derivative are available.",
        ("prop:interior-foc", "m", "bar e", "beta", "V star b", "k prime", "b prime", "z", "z prime"),
    ),
}

REQUIRED_CODE_REFS = frozenset(
    {
        "scripts/run_p08_frozen_validation.py",
        "src/mathdevmcp/document_derivation_tree.py",
        "src/mathdevmcp/derivation_target_extraction.py",
        "src/mathdevmcp/latex_index.py",
        "src/mathdevmcp/document_context_graph.py",
        "src/mathdevmcp/context_evidence.py",
        "src/mathdevmcp/document_derivation_response.py",
        "src/mathdevmcp/mcp_facade.py",
        "src/mathdevmcp/external_tool_adapters.py",
        "src/mathdevmcp/external_adapter_contract.py",
        DERIVATIVE_ADAPTER_REF,
    }
)

_BLOCKED_BACKEND_IMPORT_ROOTS = frozenset(
    {
        "anthropic",
        "lean_dojo",
        "leandojo",
        "openai",
        "pantograph",
        "sage",
        "sageall",
        "sympy",
    }
)


class Phase08Error(RuntimeError):
    """Raised when a Phase 08 gate must fail closed."""


class _BlockedBackendImportFinder(importlib.abc.MetaPathFinder):
    def __init__(self, reject: Any) -> None:
        self._reject = reject

    def find_spec(self, fullname: str, path: Any = None, target: Any = None) -> None:
        if fullname.split(".", 1)[0] in _BLOCKED_BACKEND_IMPORT_ROOTS:
            self._reject("python_import", fullname)
        return None


@contextmanager
def _no_math_backend_scope(action: str):
    attempts: list[dict[str, str]] = []

    def reject(kind: str, target: str) -> None:
        attempts.append({"kind": kind, "target": target})
        raise Phase08Error(f"P08A forbids backend/network access: {kind}:{target}")

    finder = _BlockedBackendImportFinder(reject)
    patches = [
        (subprocess, "run", subprocess.run),
        (subprocess, "Popen", subprocess.Popen),
        (subprocess, "call", subprocess.call),
        (subprocess, "check_call", subprocess.check_call),
        (subprocess, "check_output", subprocess.check_output),
        (os, "system", os.system),
        (os, "popen", os.popen),
        (socket, "create_connection", socket.create_connection),
    ]

    def blocked_process(*args: Any, **kwargs: Any) -> None:
        target = repr(args[0] if args else kwargs.get("args", "unknown"))[:512]
        reject("process", target)

    def blocked_network(*args: Any, **kwargs: Any) -> None:
        target = repr(args[0] if args else kwargs.get("address", "unknown"))[:512]
        reject("network", target)

    sys.meta_path.insert(0, finder)
    for owner, name, _original in patches:
        setattr(owner, name, blocked_network if owner is socket else blocked_process)
    try:
        yield attempts
    finally:
        for owner, name, original in reversed(patches):
            setattr(owner, name, original)
        if finder in sys.meta_path:
            sys.meta_path.remove(finder)


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _digest(value: Any) -> str:
    raw = bytes(value) if isinstance(value, (bytes, bytearray, memoryview)) else _canonical(value)
    return hashlib.sha256(raw).hexdigest()


def _utc_now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _workspace() -> Path:
    root = Path.cwd().absolute()
    if root.is_symlink() or not (root / ".git").exists() or not (root / "src/mathdevmcp").is_dir():
        raise Phase08Error("Phase 08 must run from the non-symlinked MathDevMCP workspace root")
    return root


def _logical_ref(root: Path, path: Path) -> str:
    try:
        ref = path.absolute().relative_to(root).as_posix()
    except ValueError as exc:
        raise Phase08Error("path escapes the MathDevMCP workspace") from exc
    if any(part in {"", ".", ".."} for part in PurePosixPath(ref).parts):
        raise Phase08Error("path is not a normalized workspace-relative reference")
    return ref


def _assert_no_symlink(root: Path, path: Path) -> None:
    absolute = path.absolute()
    try:
        relative = absolute.relative_to(root)
    except ValueError as exc:
        raise Phase08Error("path escapes the workspace") from exc
    cursor = root
    if cursor.is_symlink():
        raise Phase08Error("workspace root must not be a symlink")
    for part in relative.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise Phase08Error(f"symlink is forbidden in Phase 08 paths: {cursor}")


def _regular_bytes(root: Path, ref: str) -> bytes:
    path = root / ref
    _assert_no_symlink(root, path)
    info = path.stat()
    if not stat.S_ISREG(info.st_mode):
        raise Phase08Error(f"required artifact is not a regular file: {ref}")
    return path.read_bytes()


def _write_new(path: Path, raw: bytes) -> None:
    if path.exists() or path.is_symlink():
        raise Phase08Error(f"Phase 08 never overwrites artifacts: {path}")
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
                raise OSError("short Phase 08 artifact write")
            view = view[count:]
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _write_json_new(path: Path, value: Mapping[str, Any]) -> dict[str, Any]:
    raw = _canonical(dict(value))
    _write_new(path, raw)
    reopened = path.read_bytes()
    if reopened != raw:
        raise Phase08Error(f"artifact reopen mismatch: {path}")
    return {"sha256": _digest(raw), "byte_count": len(raw)}


def _load_canonical(path: Path) -> dict[str, Any]:
    return _load_canonical_bounded(path)


def _load_canonical_bounded(path: Path, max_bytes: int | None = None) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise Phase08Error(f"missing or unsafe Phase 08 artifact: {path}")
    if max_bytes is not None:
        size = path.stat().st_size
        if size > max_bytes:
            raise Phase08Error(f"canonical artifact exceeds its registered byte limit: {path}")
    raw = path.read_bytes()
    if max_bytes is not None and len(raw) > max_bytes:
        raise Phase08Error(f"canonical artifact changed past its registered byte limit: {path}")
    return _decode_canonical(raw, path)


def _decode_canonical(raw: bytes, source: Path | str) -> dict[str, Any]:
    try:
        value = json.loads(raw.decode("utf-8", "strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise Phase08Error(f"invalid JSON artifact: {source}") from exc
    if not isinstance(value, dict) or _canonical(value) != raw:
        raise Phase08Error(f"artifact is not canonical JSON: {source}")
    return value


def _read_regular_bounded(root: Path, path: Path, max_bytes: int, label: str) -> bytes:
    _assert_no_symlink(root, path)
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise Phase08Error(f"required candidate artifact is not a regular file: {label}")
        if before.st_size > max_bytes:
            raise Phase08Error(f"candidate artifact exceeds its registered byte limit: {label}")
        chunks = bytearray()
        while len(chunks) <= max_bytes:
            chunk = os.read(descriptor, min(65_536, max_bytes + 1 - len(chunks)))
            if not chunk:
                break
            chunks.extend(chunk)
        after = os.fstat(descriptor)
        if len(chunks) > max_bytes:
            raise Phase08Error(f"candidate artifact exceeds its registered byte limit: {label}")
        if before.st_ino != after.st_ino or before.st_dev != after.st_dev or len(chunks) != after.st_size:
            raise Phase08Error(f"candidate artifact changed during bounded read: {label}")
        return bytes(chunks)
    finally:
        os.close(descriptor)


def _candidate_file_limits(max_artifact_bytes: int) -> dict[str, int]:
    if max_artifact_bytes != P08_BUNDLE_LIMIT:
        raise Phase08Error("candidate bundle limit differs from the reviewed exact value")
    return {
        "native-input.json": P08_RAW_STREAM_LIMIT,
        "stdout.bin": P08_RAW_STREAM_LIMIT,
        "stderr.bin": P08_RAW_STREAM_LIMIT,
        "result.json": max_artifact_bytes,
        "manifest.json": max_artifact_bytes,
    }


def _candidate_aggregate(
    predecessor_byte_counts: Sequence[int],
    manifest_byte_count: int,
    fixed_overhead_bytes: int,
    max_artifact_bytes: int,
) -> tuple[int, int]:
    values = [*predecessor_byte_counts, manifest_byte_count, fixed_overhead_bytes]
    if any(type(value) is not int or value < 0 for value in values):
        raise Phase08Error("candidate bundle byte accounting is invalid")
    if fixed_overhead_bytes != P08_BUNDLE_OVERHEAD or max_artifact_bytes != P08_BUNDLE_LIMIT:
        raise Phase08Error("candidate bundle accounting limits differ from reviewed values")
    exact_sum = sum(predecessor_byte_counts) + manifest_byte_count
    final_aggregate = exact_sum + fixed_overhead_bytes
    if final_aggregate > max_artifact_bytes:
        raise Phase08Error("capability bundle aggregate limit exceeded")
    return exact_sum, final_aggregate


def _require_exact_candidate_entries(candidate_root: Path, expected_names: set[str]) -> None:
    if not candidate_root.is_dir() or candidate_root.is_symlink():
        raise Phase08Error("capability candidate bundle directory is missing or unsafe")
    entries = list(candidate_root.iterdir())
    if any(entry.is_symlink() or not entry.is_file() for entry in entries):
        raise Phase08Error("capability candidate bundle contains a non-regular entry")
    if {entry.name for entry in entries} != expected_names:
        raise Phase08Error("capability candidate bundle file set mismatch")


def _git(args: Sequence[str]) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=_workspace(),
        stdin=subprocess.DEVNULL,
        capture_output=True,
        check=False,
        text=True,
        timeout=10,
    )
    if completed.returncode != 0:
        raise Phase08Error(f"git {' '.join(args)} failed: {completed.stderr.strip()}")
    return completed.stdout


def _code_refs(root: Path) -> list[str]:
    refs = ["scripts/run_p08_frozen_validation.py"]
    for path in sorted((root / "src/mathdevmcp").glob("*.py"), key=lambda item: item.name.encode("utf-8")):
        _assert_no_symlink(root, path)
        if path.is_file():
            refs.append(path.relative_to(root).as_posix())
    if not REQUIRED_CODE_REFS <= set(refs):
        raise Phase08Error(f"required code refs are absent: {sorted(REQUIRED_CODE_REFS - set(refs))}")
    return refs


def _snapshot_code(root: Path, run_root: Path, run_id: str, run_binding_digest: str) -> dict[str, Any]:
    dirty = sorted(
        {
            line[3:]
            for line in _git(["status", "--porcelain=v1", "--untracked-files=all"]).splitlines()
            if len(line) >= 4
        },
        key=lambda item: item.encode("utf-8"),
    )
    files = []
    for ref in _code_refs(root):
        raw = _regular_bytes(root, ref)
        destination = run_root / "code-snapshot" / ref
        _write_new(destination, raw)
        files.append(
            {
                "ref": ref,
                "sha256": _digest(raw),
                "byte_count": len(raw),
                "dirty": ref in dirty,
            }
        )
    identity = {
        "schema_version": CODE_SCHEMA,
        "run_id": run_id,
        "run_binding_digest": run_binding_digest,
        "head": _git(["rev-parse", "HEAD"]).strip(),
        "dirty_paths": dirty,
        "required_refs": sorted(REQUIRED_CODE_REFS),
        "files": files,
        "boundary": "Exact scoped execution and verification code bytes; no publication or claim authority.",
    }
    identity["code_identity_digest"] = _digest(identity)
    _write_json_new(run_root / "code-identity.json", identity)
    return identity


def _verify_code_identity(root: Path, run_root: Path) -> dict[str, Any]:
    identity = _load_canonical(run_root / "code-identity.json")
    if identity.get("schema_version") != CODE_SCHEMA:
        raise Phase08Error("unsupported Phase 08 code identity")
    expected = _digest({key: value for key, value in identity.items() if key != "code_identity_digest"})
    if identity.get("code_identity_digest") != expected:
        raise Phase08Error("code identity digest mismatch")
    refs = [item.get("ref") for item in identity.get("files", []) if isinstance(item, dict)]
    if len(refs) != len(set(refs)) or not REQUIRED_CODE_REFS <= set(refs):
        raise Phase08Error("code identity has duplicate or missing required refs")
    for item in identity["files"]:
        ref = item["ref"]
        live = _regular_bytes(root, ref)
        snapshot = _regular_bytes(root, _logical_ref(root, run_root / "code-snapshot" / ref))
        if live != snapshot or _digest(live) != item["sha256"] or len(live) != item["byte_count"]:
            raise Phase08Error(f"code drift veto: {ref}")
    return identity


def _loaded_repo_modules(root: Path, identity: Mapping[str, Any]) -> list[dict[str, Any]]:
    known = {item["ref"]: item for item in identity["files"]}
    loaded: dict[str, dict[str, Any]] = {}
    for name, module in sorted(sys.modules.items()):
        raw_path = getattr(module, "__file__", None)
        if not isinstance(raw_path, str) or not raw_path:
            continue
        path = Path(raw_path)
        if path.suffix in {".pyc", ".pyo"}:
            try:
                import importlib.util

                source = importlib.util.source_from_cache(str(path))
                path = Path(source)
            except (ValueError, NotImplementedError):
                continue
        try:
            ref = path.absolute().relative_to(root).as_posix()
        except ValueError:
            continue
        if ref != "scripts/run_p08_frozen_validation.py" and not ref.startswith("src/mathdevmcp/"):
            continue
        if ref not in known:
            raise Phase08Error(f"loaded repo module has no code snapshot entry: {name}:{ref}")
        raw = _regular_bytes(root, ref)
        if _digest(raw) != known[ref]["sha256"]:
            raise Phase08Error(f"loaded repo module drift veto: {name}:{ref}")
        loaded[ref] = {"ref": ref, "sha256": known[ref]["sha256"]}
    return [loaded[key] for key in sorted(loaded)]


def _new_run(root: Path, artifact_root: str) -> tuple[Path, str, str]:
    if PurePosixPath(artifact_root) != PHASE_ROOT:
        raise Phase08Error(f"artifact root must be exactly {PHASE_ROOT}")
    parent = root / artifact_root / "runs"
    _assert_no_symlink(root, parent)
    parent.mkdir(parents=True, exist_ok=True)
    run_id = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + uuid.uuid4().hex[:12]
    run_root = parent / run_id
    run_root.mkdir(mode=0o700)
    run_ref = run_root.relative_to(root).as_posix()
    binding = _digest({"run_id": run_id, "run_root": run_ref, "phase": "P08"})
    return run_root, run_id, binding


def _open_run(root: Path, raw_run_root: str) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    value = PurePosixPath(raw_run_root)
    if value.parent != PurePosixPath(PHASE_ROOT) / "runs" or not value.name:
        raise Phase08Error("later Phase 08 commands require the exact immutable runs/<run-id> root")
    if value.name in {"current", "latest"} or any(char in raw_run_root for char in "*?[]"):
        raise Phase08Error("implicit/latest/glob Phase 08 run selection is forbidden")
    run_root = root / value.as_posix()
    _assert_no_symlink(root, run_root)
    if not run_root.is_dir():
        raise Phase08Error("Phase 08 run root does not exist")
    manifest = _load_canonical(run_root / "run-manifest.json")
    if manifest.get("schema_version") != RUN_SCHEMA or manifest.get("run_id") != value.name:
        raise Phase08Error("run id/root mismatch")
    expected_binding = _digest(
        {"run_id": value.name, "run_root": value.as_posix(), "phase": "P08"}
    )
    if manifest.get("run_binding_digest") != expected_binding:
        raise Phase08Error("run binding digest mismatch")
    if manifest.get("python_executable") != P08_PYTHON or sys.executable != P08_PYTHON:
        raise Phase08Error("Phase 08 interpreter differs from the reviewed exact executable")
    identity = _verify_code_identity(root, run_root)
    if identity.get("run_id") != value.name or identity.get("run_binding_digest") != expected_binding:
        raise Phase08Error("cross-run code identity rejected")
    if manifest.get("code_identity_digest") != identity.get("code_identity_digest"):
        raise Phase08Error("run manifest/code identity cross-binding mismatch")
    return run_root, manifest, identity


def _bound_record(
    schema: str,
    manifest: Mapping[str, Any],
    identity: Mapping[str, Any],
    fields: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "schema_version": schema,
        "run_id": manifest["run_id"],
        "run_binding_digest": manifest["run_binding_digest"],
        "code_identity_digest": identity["code_identity_digest"],
        **dict(fields),
    }


def _require_record_binding(
    record: Mapping[str, Any], manifest: Mapping[str, Any], identity: Mapping[str, Any]
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
        raise Phase08Error("cross-run artifact or code identity rejected")


def _source_manifest(root: Path, manifest: Mapping[str, Any], identity: Mapping[str, Any]) -> dict[str, Any]:
    artifacts = []
    for role, binding in {**SOURCE_BINDINGS, **COMPARATOR_BINDINGS}.items():
        raw = _regular_bytes(root, binding["ref"])
        measured = _digest(raw)
        if measured != binding["sha256"]:
            raise Phase08Error(f"frozen digest drift veto: {binding['ref']}")
        artifacts.append(
            {
                "role": role,
                "ref": binding["ref"],
                "sha256": measured,
                "byte_count": len(raw),
            }
        )
    result = _bound_record(
        SOURCE_SCHEMA,
        manifest,
        identity,
        {"artifacts": artifacts, "all_digests_match": True},
    )
    result["source_manifest_digest"] = _digest(result)
    return result


def _validate_obligation_source(root: Path, obligation: Mapping[str, Any]) -> None:
    document = obligation.get("document")
    if not isinstance(document, Mapping):
        raise Phase08Error("obligation document binding is missing")
    raw = _regular_bytes(root, str(document["file"]))
    if _digest(raw) != document.get("source_digest"):
        raise Phase08Error("obligation source digest mismatch")
    owned = obligation.get("owned_spans")
    excluded = obligation.get("excluded_spans")
    if not isinstance(owned, list) or not owned or not isinstance(excluded, list):
        raise Phase08Error("obligation lacks exact owned/excluded spans")
    pairs = [(int(item["start_byte"]), int(item["end_byte"])) for item in owned]
    for start, end in pairs:
        if not 0 <= start < end <= len(raw):
            raise Phase08Error("owned span escapes frozen source")
    envelope = raw[pairs[0][0] : pairs[-1][1]].decode("utf-8", "strict")
    if envelope != obligation.get("source_math"):
        raise Phase08Error("owned source envelope reconstruction mismatch")
    for item in obligation.get("owned_rows", []):
        start, end = int(item["start_byte"]), int(item["end_byte"])
        if _digest(raw[start:end]) != item.get("raw_source_sha256"):
            raise Phase08Error("owned row source reconstruction mismatch")
    for item in excluded:
        start, end = int(item["start_byte"]), int(item["end_byte"])
        if any(a < end and start < b for a, b in pairs):
            raise Phase08Error("excluded sibling span overlaps owned span")
    if obligation.get("extraction_state") != "valid_complete" or obligation.get("adapter_eligible") is not True:
        raise Phase08Error("P08A requires complete adapter-eligible obligations")
    if obligation.get("normalized_target", {}).get("complete_lhs_rhs") is not True:
        raise Phase08Error("P08A obligation lacks complete lhs/rhs")


def _extract(root: Path) -> dict[str, Any]:
    with _no_math_backend_scope("p08a_extraction") as attempts:
        from mathdevmcp.document_derivation_tree import extract_document_derivation_obligations

        groups = []
        for group_id, source_id, labels in EXTRACTION_GROUPS:
            binding = SOURCE_BINDINGS[source_id]
            result = extract_document_derivation_obligations(
                root / binding["ref"],
                focus_labels=list(labels),
            )
            if result.get("status") != "extracted" or result.get("requested_labels") != list(labels):
                raise Phase08Error(f"extraction group failed or reordered: {group_id}")
            if result.get("backend_request_count") != 0:
                raise Phase08Error("backend request detected during P08A extraction")
            if result.get("publication_enabled") is not False or result.get("publication_mode") != "disabled":
                raise Phase08Error("publication boundary failed during P08A extraction")
            obligations = result.get("obligations")
            if not isinstance(obligations, list) or not obligations:
                raise Phase08Error(f"extraction group has no obligations: {group_id}")
            expected_labels = (
                ["eq:foc-k", "eq:foc-b"] if group_id == "risky_focus" else list(labels)
            )
            actual_labels = [item.get("label") for item in obligations]
            if actual_labels != expected_labels or len(set(actual_labels)) != len(actual_labels):
                raise Phase08Error(f"obligation label ownership/order mismatch: {group_id}")
            if len({item.get("obligation_digest") for item in obligations}) != len(obligations):
                raise Phase08Error(f"duplicate obligation identity: {group_id}")
            for obligation in obligations:
                _validate_obligation_source(root, obligation)
                retained = RETAINED_OBLIGATION_DIGESTS.get(str(obligation.get("label")))
                if retained is not None and obligation.get("obligation_digest") != retained:
                    raise Phase08Error(f"retained obligation digest drift: {obligation.get('label')}")
            if group_id == "card_capability" and any(
                {"conditional_expectation", "summation"} & set(item.get("operator_inventory", []))
                for item in obligations
            ):
                raise Phase08Error("card capability extraction owns forbidden NPV operators")
            if group_id == "risky_focus":
                targets = result.get("targets", [])
                if [item.get("label") for item in targets] != ["eq:foc-k", "eq:foc-b"]:
                    raise Phase08Error("proposition child-target partition mismatch")
                if any(item.get("parent_label") != "prop:interior-foc" for item in targets):
                    raise Phase08Error("risky focus child lost proposition ownership")
            groups.append(
                {
                    "group_id": group_id,
                    "source_id": source_id,
                    "requested_labels": list(labels),
                    "result": result,
                }
            )
    return {
        "groups": groups,
        "backend_request_count": 0,
        "guard": {
            "action": "p08a_extraction",
            "forbidden_attempt_count": len(attempts),
            "forbidden_attempts": attempts,
        },
        "publication_enabled": False,
    }


def _obligations_by_label(extraction: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for group in extraction.get("groups", []):
        for obligation in group.get("result", {}).get("obligations", []):
            label = str(obligation.get("label"))
            existing = records.get(label)
            if existing is not None and existing.get("obligation_digest") != obligation.get("obligation_digest"):
                raise Phase08Error(f"same label has cross-group obligation drift: {label}")
            records.setdefault(label, dict(obligation))
    if set(records) != set(CONTEXT_SPECS):
        raise Phase08Error(
            f"context obligation coverage mismatch: missing={sorted(set(CONTEXT_SPECS)-set(records))}"
        )
    return records


def _context_request(label: str, obligation: Mapping[str, Any], source_id: str) -> dict[str, Any]:
    predicate, subjects = CONTEXT_SPECS[label]
    document = obligation["document"]
    if label in subjects:
        raise Phase08Error("context request contains its own target label")
    return {
        "obligation_digest": obligation["obligation_digest"],
        "entry_source_digest": document["source_digest"],
        "requirement_id": "p08_context_" + "".join(
            char if char.isalnum() else "_" for char in label
        ),
        "requirement_predicate": predicate,
        "requirement_subjects": list(subjects),
        "required_node_kinds": ["definition", "assumption", "notation_declaration", "proposition"],
        "required_edge_kinds": ["input", "include", "contains", "references"],
        "required_files": [SOURCE_BINDINGS[source_id]["ref"]],
        "budget": dict(SOURCE_BINDINGS[source_id]["budget"]),
    }


def _resolve_context(root: Path, extraction: Mapping[str, Any]) -> dict[str, Any]:
    with _no_math_backend_scope("p08a_context") as attempts:
        from mathdevmcp.context_evidence import validate_context_manifest
        from mathdevmcp.document_context_graph import (
            build_context_dependency_graph,
            resolve_context_requirement,
        )

        obligations = _obligations_by_label(extraction)
        graphs: dict[str, dict[str, Any]] = {}
        for source_id, binding in SOURCE_BINDINGS.items():
            graph = build_context_dependency_graph(
                root,
                binding["ref"],
                expected_entry_source_digest=binding["sha256"],
                budget=binding["budget"],
            )
            if graph.get("entry_ref") != binding["ref"] or graph.get("integrity_vetoes"):
                raise Phase08Error(f"unsafe context graph: {source_id}")
            if graph.get("reachable_files") != [binding["ref"]]:
                raise Phase08Error(f"unexpected context dependency closure: {source_id}")
            graphs[source_id] = graph
        manifests = []
        for label, obligation in obligations.items():
            source_id = next(
                key
                for key, binding in SOURCE_BINDINGS.items()
                if obligation["document"]["file"] == binding["ref"]
            )
            request = _context_request(label, obligation, source_id)
            manifest = resolve_context_requirement(graphs[source_id], obligation, request)
            for candidate in manifest.get("candidates", []):
                if candidate.get("target_span_match") is True and candidate.get("applicability_state") == "explicit":
                    raise Phase08Error(f"target span promoted to context support: {label}")
                if candidate.get("applicability_state") == "explicit":
                    if candidate.get("source_ref", {}).get("file") != SOURCE_BINDINGS[source_id]["ref"]:
                        raise Phase08Error(f"context support escapes required file: {label}")
            if manifest.get("terminal_state") == "stated":
                raise Phase08Error(f"target self-evidence produced stated context: {label}")
            validate_context_manifest(manifest)
            manifests.append({"label": label, "source_id": source_id, "manifest": manifest})
    return {
        "graphs": [graphs[key] for key in sorted(graphs)],
        "manifests": manifests,
        "terminal_state_counts": {
            state: sum(item["manifest"]["terminal_state"] == state for item in manifests)
            for state in sorted({item["manifest"]["terminal_state"] for item in manifests})
        },
        "backend_request_count": 0,
        "guard": {
            "action": "p08a_context",
            "forbidden_attempt_count": len(attempts),
            "forbidden_attempts": attempts,
        },
        "publication_enabled": False,
    }


def _record_command(
    run_root: Path,
    command: str,
    manifest: Mapping[str, Any],
    identity: Mapping[str, Any],
    loaded: list[dict[str, Any]],
) -> None:
    record = _bound_record(
        "p08_command_code_identity@1",
        manifest,
        identity,
        {
            "command": command,
            "loaded_repo_modules": loaded,
            "recorded_at_utc": _utc_now(),
        },
    )
    _write_json_new(run_root / "code-usage" / f"{command}.json", record)


def command_freeze_extract(args: argparse.Namespace) -> dict[str, Any]:
    root = _workspace()
    if not args.new_run:
        raise Phase08Error("freeze-extract requires --new-run")
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        raise Phase08Error("Phase 08 requires CUDA_VISIBLE_DEVICES=-1 before Python import")
    if sys.executable != P08_PYTHON:
        raise Phase08Error("Phase 08 requires the reviewed exact Python executable")
    run_root, run_id, binding = _new_run(root, args.artifact_root)
    try:
        identity = _snapshot_code(root, run_root, run_id, binding)
        manifest = {
            "schema_version": RUN_SCHEMA,
            "run_id": run_id,
            "run_root": run_root.relative_to(root).as_posix(),
            "run_binding_digest": binding,
            "created_at_utc": _utc_now(),
            "head": identity["head"],
            "dirty_paths": identity["dirty_paths"],
            "code_identity_digest": identity["code_identity_digest"],
            "python_executable": sys.executable,
            "python_version": sys.version.split()[0],
            "cpu_gpu_status": "CPU-only; GPU devices intentionally hidden with CUDA_VISIBLE_DEVICES=-1",
            "seeds": "N/A; deterministic extraction/context route",
            "plan_ref": "docs/plans/mathdevmcp-real-document-remediation-phase-08-frozen-real-document-validation-subplan-2026-07-14.md",
            "publication_enabled": False,
        }
        _write_json_new(run_root / "run-manifest.json", manifest)
        _verify_code_identity(root, run_root)
        source = _source_manifest(root, manifest, identity)
        _write_json_new(run_root / "source-manifest.json", source)
        extraction_fields = _extract(root)
        extraction = _bound_record(EXTRACTION_SCHEMA, manifest, identity, extraction_fields)
        extraction["extraction_digest"] = _digest(extraction)
        _verify_code_identity(root, run_root)
        _write_json_new(run_root / "p08a/extraction.json", extraction)
        loaded = _loaded_repo_modules(root, identity)
        _record_command(run_root, "freeze-extract", manifest, identity, loaded)
        _verify_code_identity(root, run_root)
        return {
            "status": "P08_W1_EXTRACTED",
            "run_id": run_id,
            "run_root": manifest["run_root"],
            "run_binding_digest": binding,
            "code_identity_digest": identity["code_identity_digest"],
            "extraction_digest": extraction["extraction_digest"],
        }
    except Exception:
        marker = run_root / "FAILED_DURING_FREEZE_EXTRACT.txt"
        if not marker.exists():
            _write_new(marker, b"Fresh run creation failed; preserve for diagnosis.\n")
        raise


def command_resolve_context(args: argparse.Namespace) -> dict[str, Any]:
    root = _workspace()
    run_root, manifest, identity = _open_run(root, args.run_root)
    extraction = _load_canonical(run_root / "p08a/extraction.json")
    _require_record_binding(extraction, manifest, identity)
    context_fields = _resolve_context(root, extraction)
    context = _bound_record(CONTEXT_SCHEMA, manifest, identity, context_fields)
    context["context_digest"] = _digest(context)
    _verify_code_identity(root, run_root)
    _write_json_new(run_root / "p08a/context.json", context)
    loaded = _loaded_repo_modules(root, identity)
    _record_command(run_root, "resolve-context", manifest, identity, loaded)
    _verify_code_identity(root, run_root)
    return {
        "status": "P08_W2_CONTEXT_RESOLVED",
        "run_id": manifest["run_id"],
        "run_root": manifest["run_root"],
        "context_digest": context["context_digest"],
        "terminal_state_counts": context["terminal_state_counts"],
    }


def _verify_source_manifest(root: Path, record: Mapping[str, Any]) -> None:
    if record.get("schema_version") != SOURCE_SCHEMA or record.get("all_digests_match") is not True:
        raise Phase08Error("source manifest status mismatch")
    expected = _digest({key: value for key, value in record.items() if key != "source_manifest_digest"})
    if record.get("source_manifest_digest") != expected:
        raise Phase08Error("source manifest digest mismatch")
    for item in record.get("artifacts", []):
        raw = _regular_bytes(root, item["ref"])
        if _digest(raw) != item["sha256"] or len(raw) != item["byte_count"]:
            raise Phase08Error(f"source manifest reopen drift: {item['ref']}")


def _verify_extraction(root: Path, extraction: Mapping[str, Any]) -> None:
    expected = _digest({key: value for key, value in extraction.items() if key != "extraction_digest"})
    if extraction.get("schema_version") != EXTRACTION_SCHEMA or extraction.get("extraction_digest") != expected:
        raise Phase08Error("extraction artifact digest/schema mismatch")
    if extraction.get("backend_request_count") != 0 or extraction.get("publication_enabled") is not False:
        raise Phase08Error("extraction backend/publication boundary mismatch")
    if extraction.get("guard") != {
        "action": "p08a_extraction",
        "forbidden_attempt_count": 0,
        "forbidden_attempts": [],
    }:
        raise Phase08Error("extraction guard attestation mismatch")
    group_ids = [item.get("group_id") for item in extraction.get("groups", [])]
    if group_ids != [item[0] for item in EXTRACTION_GROUPS]:
        raise Phase08Error("extraction group order mismatch")
    _obligations_by_label(extraction)
    for group in extraction["groups"]:
        for obligation in group["result"]["obligations"]:
            _validate_obligation_source(root, obligation)


def _verify_context(context: Mapping[str, Any]) -> None:
    from mathdevmcp.context_evidence import validate_context_manifest

    expected = _digest({key: value for key, value in context.items() if key != "context_digest"})
    if context.get("schema_version") != CONTEXT_SCHEMA or context.get("context_digest") != expected:
        raise Phase08Error("context artifact digest/schema mismatch")
    if context.get("backend_request_count") != 0 or context.get("publication_enabled") is not False:
        raise Phase08Error("context backend/publication boundary mismatch")
    if context.get("guard") != {
        "action": "p08a_context",
        "forbidden_attempt_count": 0,
        "forbidden_attempts": [],
    }:
        raise Phase08Error("context guard attestation mismatch")
    labels = [item.get("label") for item in context.get("manifests", [])]
    if labels != list(CONTEXT_SPECS):
        raise Phase08Error("context request order/coverage mismatch")
    for item in context["manifests"]:
        manifest = item["manifest"]
        validate_context_manifest(manifest)
        required_file = SOURCE_BINDINGS[item["source_id"]]["ref"]
        request = manifest["context_request"]
        if request["required_files"] != [required_file] or item["label"] in request["requirement_subjects"]:
            raise Phase08Error("context pre-registration binding mismatch")
        for candidate in manifest["candidates"]:
            if candidate.get("applicability_state") == "explicit":
                if candidate.get("target_span_match") is True:
                    raise Phase08Error("target-span context support rejected")
                if candidate.get("source_ref", {}).get("file") != required_file:
                    raise Phase08Error("explicit context support file mismatch")


def command_verify_p08a(args: argparse.Namespace) -> dict[str, Any]:
    root = _workspace()
    run_root, manifest, identity = _open_run(root, args.run_root)
    source = _load_canonical(run_root / "source-manifest.json")
    extraction = _load_canonical(run_root / "p08a/extraction.json")
    context = _load_canonical(run_root / "p08a/context.json")
    for record in (source, extraction, context):
        _require_record_binding(record, manifest, identity)
    _verify_source_manifest(root, source)
    _verify_extraction(root, extraction)
    _verify_context(context)
    prior_usage = []
    for command in ("freeze-extract", "resolve-context"):
        record = _load_canonical(run_root / "code-usage" / f"{command}.json")
        _require_record_binding(record, manifest, identity)
        prior_usage.append(record)
    if any(item.get("code_identity_digest") != identity["code_identity_digest"] for item in prior_usage):
        raise Phase08Error("P08A producer code identity mismatch")
    decision = _bound_record(
        DECISION_SCHEMA,
        manifest,
        identity,
        {
            "status": "PASS_P08A_FROZEN_EXTRACTION_CONTEXT",
            "source_manifest_digest": source["source_manifest_digest"],
            "extraction_digest": extraction["extraction_digest"],
            "context_digest": context["context_digest"],
            "producer_code_identity_digests": sorted(
                {item["code_identity_digest"] for item in prior_usage}
            ),
            "backend_request_count": 0,
            "publication_enabled": False,
            "vetoes": [],
            "non_claims": [
                "P08A validates source, extraction, and context boundaries only.",
                "P08A is not mathematical proof or substantive backend capability evidence.",
            ],
        },
    )
    decision["decision_digest"] = _digest(decision)
    _verify_code_identity(root, run_root)
    _write_json_new(run_root / "p08a/decision.json", decision)
    loaded = _loaded_repo_modules(root, identity)
    _record_command(run_root, "verify-p08a", manifest, identity, loaded)
    _verify_code_identity(root, run_root)
    return {
        "status": decision["status"],
        "run_id": manifest["run_id"],
        "run_root": manifest["run_root"],
        "decision_digest": decision["decision_digest"],
        "code_identity_digest": identity["code_identity_digest"],
    }


def _require_p08a_pass(
    root: Path,
    run_root: Path,
    manifest: Mapping[str, Any],
    identity: Mapping[str, Any],
) -> dict[str, Any]:
    source = _load_canonical(run_root / "source-manifest.json")
    extraction = _load_canonical(run_root / "p08a/extraction.json")
    context = _load_canonical(run_root / "p08a/context.json")
    for record in (source, extraction, context):
        _require_record_binding(record, manifest, identity)
    _verify_source_manifest(root, source)
    _verify_extraction(root, extraction)
    _verify_context(context)
    decision = _load_canonical(run_root / "p08a/decision.json")
    _require_record_binding(decision, manifest, identity)
    expected = _digest({key: value for key, value in decision.items() if key != "decision_digest"})
    if decision.get("decision_digest") != expected or decision.get("status") != "PASS_P08A_FROZEN_EXTRACTION_CONTEXT":
        raise Phase08Error("P08A has not passed exactly")
    if decision.get("backend_request_count") != 0 or decision.get("publication_enabled") is not False:
        raise Phase08Error("P08A decision boundary mismatch")
    return decision


def _capability_obligations(extraction: Mapping[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    by_label: dict[str, list[dict[str, Any]]] = {}
    for group in extraction.get("groups", []):
        for obligation in group.get("result", {}).get("obligations", []):
            by_label.setdefault(str(obligation.get("label")), []).append(dict(obligation))
    selected = {}
    for label in ("eq:risky-cash-flow", "eq:cashflow-rate-derivative"):
        matches = by_label.get(label, [])
        if len(matches) != 1:
            raise Phase08Error(f"capability source obligation is absent or inconsistent: {label}")
        selected[label] = matches[0]
    expression = selected["eq:risky-cash-flow"]
    target = selected["eq:cashflow-rate-derivative"]
    for obligation in (expression, target):
        expected = P08B_SOURCE_PROJECTIONS[obligation["label"]]
        document = obligation.get("document")
        normalized = obligation.get("normalized_target")
        if (
            obligation.get("obligation_digest") != expected["obligation_digest"]
            or not isinstance(document, Mapping)
            or document.get("file") != expected["document_ref"]
            or document.get("source_digest") != expected["document_sha256"]
            or _digest(str(obligation.get("source_math", "")).encode("utf-8"))
            != expected["source_math_sha256"]
            or not isinstance(normalized, Mapping)
            or _digest(normalized) != expected["normalized_target_sha256"]
            or any(term not in normalized.get("display_text", "") for term in expected["selected_terms"])
        ):
            raise Phase08Error(
                f"P08B source-to-scalar projection binding mismatch: {obligation['label']}"
            )
    return expression, target


def _adapter_readiness(
    expression_obligation: Mapping[str, Any],
    target_obligation: Mapping[str, Any],
    identity: Mapping[str, Any],
) -> tuple[str, dict[str, Any] | None, dict[str, Any] | None, str | None]:
    refs = {item["ref"] for item in identity["files"]}
    if DERIVATIVE_ADAPTER_REF not in refs:
        return "BLOCKED_ADAPTER_REPAIR_REQUIRED", None, None, "adapter code is absent from the exact code identity"
    before_sympy = "sympy" in sys.modules
    if before_sympy:
        return "BLOCKED_ADAPTER_REPAIR_REQUIRED", None, None, "SymPy was already imported before the readiness handshake"
    try:
        adapter = importlib.import_module("mathdevmcp.sympy_derivative_adapter")
        expected_exports = {
            "SYMPY_DERIVATIVE_ADAPTER_VERSION": DERIVATIVE_ADAPTER_VERSION,
            "SYMPY_DERIVATIVE_OPERATION": DERIVATIVE_OPERATION,
            "SYMPY_DERIVATIVE_REQUEST_SCHEMA": "p08_sympy_derivative_request@1",
            "SYMPY_DERIVATIVE_WORKER_SCHEMA": "p08_sympy_derivative_worker_output@1",
            "SYMPY_DERIVATIVE_RESULT_SCHEMA": "p08_sympy_derivative_result@1",
        }
        if any(getattr(adapter, name, None) != value for name, value in expected_exports.items()):
            raise ValueError("adapter exported version/schema/operation mismatch")
        for name in (
            "derivative_capability_descriptor",
            "build_derivative_request",
            "validate_derivative_request",
            "canonical_json_bytes",
        ):
            if not callable(getattr(adapter, name, None)):
                raise ValueError(f"adapter readiness API is absent or non-callable: {name}")
        descriptor = adapter.derivative_capability_descriptor()
        expected_descriptor = {
            "adapter_version": DERIVATIVE_ADAPTER_VERSION,
            "operation": DERIVATIVE_OPERATION,
            "request_schema": "p08_sympy_derivative_request@1",
            "worker_output_schema": "p08_sympy_derivative_worker_output@1",
            "result_schema": "p08_sympy_derivative_result@1",
            "status_registry": DERIVATIVE_STATUSES,
            "imports_sympy_at_module_import": False,
            "can_promote": False,
            "publication_enabled": False,
        }
        if descriptor != expected_descriptor:
            raise ValueError("adapter capability descriptor mismatch")
        request = adapter.build_derivative_request(
            source_expression_obligation_digest=expression_obligation["obligation_digest"],
            source_target_obligation_digest=target_obligation["obligation_digest"],
        )
        adapter.validate_derivative_request(request)
        second = adapter.build_derivative_request(
            source_expression_obligation_digest=expression_obligation["obligation_digest"],
            source_target_obligation_digest=target_obligation["obligation_digest"],
        )
        if adapter.canonical_json_bytes(request) != adapter.canonical_json_bytes(second):
            raise ValueError("adapter dry request is nondeterministic")
        if request["adapter_version"] != DERIVATIVE_ADAPTER_VERSION or request["operation"] != DERIVATIVE_OPERATION:
            raise ValueError("adapter dry request binding mismatch")
        if (
            request.get("expression")
            != P08B_SOURCE_PROJECTIONS["eq:risky-cash-flow"]["registered_scalar"]
            or request.get("expected_derivative")
            != P08B_SOURCE_PROJECTIONS["eq:cashflow-rate-derivative"]["registered_scalar"]
        ):
            raise ValueError("adapter request differs from the source-bound scalar projection")
        if "sympy" in sys.modules and not before_sympy:
            raise ValueError("adapter readiness imported SymPy")
        return "READY_EXACT_REGISTERED_ROUTE", descriptor, request, None
    except Exception as exc:
        return "BLOCKED_ADAPTER_REPAIR_REQUIRED", None, None, f"{type(exc).__name__}: {exc}"


def _formalization_record(
    manifest: Mapping[str, Any],
    identity: Mapping[str, Any],
    expression_obligation: Mapping[str, Any],
    target_obligation: Mapping[str, Any],
    request: Mapping[str, Any] | None,
) -> dict[str, Any]:
    result = _bound_record(
        FORMALIZATION_SCHEMA,
        manifest,
        identity,
        {
            "candidate_id": "eq:cashflow-rate-derivative",
            "source_bindings": {
                "expression": {
                    key: expression_obligation[key]
                    for key in ("label", "obligation_digest", "document", "owned_spans", "source_math")
                },
                "target": {
                    key: target_obligation[key]
                    for key in ("label", "obligation_digest", "document", "owned_spans", "source_math")
                },
            },
            "symbol_map": {
                "rt": {"source": "\\widetilde r", "role": "differentiated", "domain": "real"},
                "bp": {"source": "b'", "role": "held_constant", "domain": "real"},
                "tau": {"source": "\\tau", "role": "held_constant", "domain": "real"},
                "r": {"source": "r", "role": "held_constant", "domain": "real"},
            },
            "source_projection": {
                "expression_selected_terms": P08B_SOURCE_PROJECTIONS[
                    "eq:risky-cash-flow"
                ]["selected_terms"],
                "target_equality_members": P08B_SOURCE_PROJECTIONS[
                    "eq:cashflow-rate-derivative"
                ]["selected_terms"],
                "registered_expression": P08B_SOURCE_PROJECTIONS[
                    "eq:risky-cash-flow"
                ]["registered_scalar"],
                "registered_expected_derivative": P08B_SOURCE_PROJECTIONS[
                    "eq:cashflow-rate-derivative"
                ]["registered_scalar"],
                "boundary": "Human-reviewed source-to-scalar projection; computational input binding, not proof.",
            },
            "expression": None if request is None else request["expression"],
            "expected_derivative": None if request is None else request["expected_derivative"],
            "typed_assumptions": [] if request is None else request["typed_assumptions"],
            "request_digest": None if request is None else request["request_digest"],
            "construction_input_excludes_expected_derivative": True,
            "publication_enabled": False,
            "non_claims": [
                "This formalization is a source-bound backend request, not proof.",
                "The expected derivative is unavailable to the construction stage and enters only comparison.",
            ],
        },
    )
    result["formalization_digest"] = _digest(result)
    return result


def _tool_ledger_record(
    manifest: Mapping[str, Any],
    identity: Mapping[str, Any],
    status: str,
    readiness_error: str | None,
) -> dict[str, Any]:
    result = _bound_record(
        TOOL_LEDGER_SCHEMA,
        manifest,
        identity,
        {
            "candidate_id": "eq:cashflow-rate-derivative",
            "tools": [
                {
                    "tool": "SymPy",
                    "role": "construct exact scalar derivative and independently simplify the difference",
                    "availability": "selected_pending_live_execution" if status == "READY_EXACT_REGISTERED_ROUTE" else "route_not_ready",
                    "selected": status == "READY_EXACT_REGISTERED_ROUTE",
                    "reason": readiness_error,
                },
                {
                    "tool": "SageMath",
                    "role": "exact algebra/calculus",
                    "availability": "installed_scope_known",
                    "selected": False,
                    "reason": "The reviewed Phase 05 route is polynomial-only and is not transferred to rational differentiation.",
                },
                {
                    "tool": "Lean",
                    "role": "proof-kernel certification",
                    "availability": "not_selected_without_exact_lean_theorem",
                    "selected": False,
                    "reason": "No reviewed source-bound Lean theorem is available for this candidate.",
                },
                {
                    "tool": "LeanSearch-v2/LeanExplore/jixia/Pantograph/LeanDojo",
                    "role": "retrieval, extraction, or proof-state interaction",
                    "availability": "not_applicable_before_lean_formalization",
                    "selected": False,
                    "reason": "These routes cannot certify the unformalized scalar candidate.",
                },
                {
                    "tool": "MathDevMCP native orchestration",
                    "role": "source binding, routing, ledgers, limits, and report generation",
                    "availability": "selected_for_orchestration_only",
                    "selected": True,
                    "reason": "It does not construct the derivative or replace the specialist backend.",
                },
            ],
            "selected_route": (
                "SymPy exact derivative construction through the separate P08 adapter"
                if status == "READY_EXACT_REGISTERED_ROUTE"
                else None
            ),
            "backend_request_count": 0,
            "publication_enabled": False,
        },
    )
    result["tool_ledger_digest"] = _digest(result)
    return result


def _capability_ladder_record(
    manifest: Mapping[str, Any], identity: Mapping[str, Any], status: str
) -> dict[str, Any]:
    candidate_ids = [
        "eq:cashflow-rate-derivative",
        "eq:cashflow-total-k",
        "eq:cashflow-total-b",
        "eq:panel-cf-primitive",
        "eq:incremental-cash-flow",
        "eq:panel-npv-functional",
        "eq:foc-k",
        "eq:foc-b",
    ]
    first_state = "ready" if status == "READY_EXACT_REGISTERED_ROUTE" else "blocked_adapter_repair"
    result = _bound_record(
        CAPABILITY_LADDER_SCHEMA,
        manifest,
        identity,
        {
            "candidate_order": candidate_ids,
            "candidates": [
                {
                    "candidate_id": candidate_id,
                    "state": first_state if index == 0 else "not_reached",
                    "backend_execution_count": 0,
                }
                for index, candidate_id in enumerate(candidate_ids)
            ],
            "current_candidate_id": "eq:cashflow-rate-derivative",
            "target_shopping_allowed": False,
            "publication_enabled": False,
        },
    )
    result["ladder_digest"] = _digest(result)
    return result


def command_capability_preflight(args: argparse.Namespace) -> dict[str, Any]:
    root = _workspace()
    run_root, manifest, identity = _open_run(root, args.run_root)
    _require_p08a_pass(root, run_root, manifest, identity)
    extraction = _load_canonical(run_root / "p08a/extraction.json")
    expression_obligation, obligation = _capability_obligations(extraction)
    with _no_math_backend_scope("p08b_capability_preflight") as attempts:
        status, descriptor, request, readiness_error = _adapter_readiness(
            expression_obligation, obligation, identity
        )
    if attempts:
        status = "BLOCKED_ADAPTER_REPAIR_REQUIRED"
        descriptor = None
        request = None
        readiness_error = "adapter readiness attempted a forbidden backend, process, or network action"
    formalization = _formalization_record(
        manifest, identity, expression_obligation, obligation, request
    )
    tool_ledger = _tool_ledger_record(manifest, identity, status, readiness_error)
    ladder = _capability_ladder_record(manifest, identity, status)
    _write_json_new(run_root / "p08b/formalization.json", formalization)
    _write_json_new(run_root / "p08b/external-tool-ledger.json", tool_ledger)
    _write_json_new(run_root / "p08b/capability-ladder.json", ladder)
    result = _bound_record(
        CAPABILITY_SCHEMA,
        manifest,
        identity,
        {
            "status": status,
            "candidate_id": "eq:cashflow-rate-derivative",
            "candidate_obligation_digest": obligation["obligation_digest"],
            "formalization": {
                "source_expression": "g(rt) = bp/(1 + rt) + tau*rt*bp/((1 + rt)*(1 + r))",
                "source_target": "d g(rt)/d rt = bp/(1 + rt)^2 * (-1 + tau/(1 + r))",
                "differentiated_variable": "rt",
                "held_constant": ["bp", "tau", "r"],
                "domains": {"rt": "real", "bp": "real", "tau": "real", "r": "real"},
                "domain_assumptions": [
                    "1 + rt != 0",
                    "1 + r != 0",
                    "g is differentiable with respect to rt on the nonsingular real domain",
                ],
            },
            "adapter_descriptor": descriptor,
            "dry_request": request,
            "formalization_digest": formalization["formalization_digest"],
            "tool_ledger_digest": tool_ledger["tool_ledger_digest"],
            "ladder_digest": ladder["ladder_digest"],
            "selected_route": "SymPy deterministic derivative construction plus independent exact-zero difference check",
            "route_gap": (
                None
                if status == "READY_EXACT_REGISTERED_ROUTE"
                else readiness_error or "The exact derivative adapter readiness handshake failed."
            ),
            "required_repair": (
                None
                if status == "READY_EXACT_REGISTERED_ROUTE"
                else {
                    "adapter_ref": DERIVATIVE_ADAPTER_REF,
                    "test_ref": "tests/test_sympy_derivative_adapter.py",
                    "review_required": True,
                    "fresh_p08a_run_required": True,
                }
            ),
            "backend_request_count": 0,
            "readiness_guard": {
                "action": "p08b_capability_preflight",
                "forbidden_attempt_count": len(attempts),
                "forbidden_attempts": attempts,
            },
            "publication_enabled": False,
            "non_claims": [
                "Preflight does not import or execute SymPy.",
                "A generated formalization is not proof or backend evidence.",
            ],
        },
    )
    result["preflight_digest"] = _digest(result)
    _verify_code_identity(root, run_root)
    _write_json_new(run_root / "p08b/capability-preflight.json", result)
    loaded = _loaded_repo_modules(root, identity)
    _record_command(run_root, "capability-preflight", manifest, identity, loaded)
    return {
        "status": status,
        "run_id": manifest["run_id"],
        "run_root": manifest["run_root"],
        "preflight_digest": result["preflight_digest"],
        "backend_request_count": 0,
    }


def _verify_preflight(
    run_root: Path,
    manifest: Mapping[str, Any],
    identity: Mapping[str, Any],
) -> dict[str, Any]:
    preflight = _load_canonical(run_root / "p08b/capability-preflight.json")
    _require_record_binding(preflight, manifest, identity)
    if preflight.get("schema_version") != CAPABILITY_SCHEMA or set(preflight) != {
        "schema_version",
        "run_id",
        "run_binding_digest",
        "code_identity_digest",
        "status",
        "candidate_id",
        "candidate_obligation_digest",
        "formalization",
        "adapter_descriptor",
        "dry_request",
        "formalization_digest",
        "tool_ledger_digest",
        "ladder_digest",
        "selected_route",
        "route_gap",
        "required_repair",
        "backend_request_count",
        "readiness_guard",
        "publication_enabled",
        "non_claims",
        "preflight_digest",
    }:
        raise Phase08Error("capability preflight schema/keys mismatch")
    expected = _digest({key: value for key, value in preflight.items() if key != "preflight_digest"})
    if preflight.get("preflight_digest") != expected:
        raise Phase08Error("capability preflight digest mismatch")
    if preflight.get("status") != "READY_EXACT_REGISTERED_ROUTE":
        raise Phase08Error("capability execution is blocked pending the exact registered route")
    if preflight.get("backend_request_count") != 0 or preflight.get("publication_enabled") is not False:
        raise Phase08Error("capability preflight authority boundary mismatch")
    if preflight.get("readiness_guard") != {
        "action": "p08b_capability_preflight",
        "forbidden_attempt_count": 0,
        "forbidden_attempts": [],
    }:
        raise Phase08Error("capability preflight guard attestation mismatch")
    extraction = _load_canonical(run_root / "p08a/extraction.json")
    expression_obligation, target_obligation = _capability_obligations(extraction)
    adapter = importlib.import_module("mathdevmcp.sympy_derivative_adapter")
    expected_request = adapter.build_derivative_request(
        source_expression_obligation_digest=expression_obligation["obligation_digest"],
        source_target_obligation_digest=target_obligation["obligation_digest"],
    )
    adapter.validate_derivative_request(preflight.get("dry_request"))
    if preflight.get("dry_request") != expected_request:
        raise Phase08Error("capability preflight dry request differs from P08A obligations")
    if preflight.get("adapter_descriptor") != adapter.derivative_capability_descriptor():
        raise Phase08Error("capability preflight descriptor drift")
    formalization = _load_canonical(run_root / "p08b/formalization.json")
    tool_ledger = _load_canonical(run_root / "p08b/external-tool-ledger.json")
    ladder = _load_canonical(run_root / "p08b/capability-ladder.json")
    for record in (formalization, tool_ledger, ladder):
        _require_record_binding(record, manifest, identity)
    expected_formalization_record = _formalization_record(
        manifest, identity, expression_obligation, target_obligation, expected_request
    )
    expected_tool_ledger = _tool_ledger_record(
        manifest, identity, "READY_EXACT_REGISTERED_ROUTE", None
    )
    expected_ladder = _capability_ladder_record(
        manifest, identity, "READY_EXACT_REGISTERED_ROUTE"
    )
    if formalization != expected_formalization_record:
        raise Phase08Error("capability formalization artifact reconstruction mismatch")
    if tool_ledger != expected_tool_ledger:
        raise Phase08Error("external-tool ledger reconstruction mismatch")
    if ladder != expected_ladder:
        raise Phase08Error("capability ladder reconstruction mismatch")
    if (
        preflight.get("formalization_digest") != formalization["formalization_digest"]
        or preflight.get("tool_ledger_digest") != tool_ledger["tool_ledger_digest"]
        or preflight.get("ladder_digest") != ladder["ladder_digest"]
    ):
        raise Phase08Error("capability preflight artifact digest binding mismatch")
    expected_formalization = {
        "source_expression": "g(rt) = bp/(1 + rt) + tau*rt*bp/((1 + rt)*(1 + r))",
        "source_target": "d g(rt)/d rt = bp/(1 + rt)^2 * (-1 + tau/(1 + r))",
        "differentiated_variable": "rt",
        "held_constant": ["bp", "tau", "r"],
        "domains": {"rt": "real", "bp": "real", "tau": "real", "r": "real"},
        "domain_assumptions": [
            "1 + rt != 0",
            "1 + r != 0",
            "g is differentiable with respect to rt on the nonsingular real domain",
        ],
    }
    if (
        preflight.get("candidate_id") != "eq:cashflow-rate-derivative"
        or preflight.get("candidate_obligation_digest") != target_obligation["obligation_digest"]
        or preflight.get("formalization") != expected_formalization
        or preflight.get("selected_route")
        != "SymPy deterministic derivative construction plus independent exact-zero difference check"
        or preflight.get("route_gap") is not None
        or preflight.get("required_repair") is not None
        or preflight.get("non_claims")
        != [
            "Preflight does not import or execute SymPy.",
            "A generated formalization is not proof or backend evidence.",
        ]
    ):
        raise Phase08Error("capability preflight scientific binding mismatch")
    return preflight


def _bounded_worker(
    command: list[str],
    native: bytes,
    *,
    timeout_seconds: int,
    max_stdout_bytes: int,
    max_stderr_bytes: int,
) -> dict[str, Any]:
    if len(native) > P08_RAW_STREAM_LIMIT:
        raise Phase08Error("worker native input exceeds the registered byte limit")
    if (
        type(timeout_seconds) is not int
        or timeout_seconds <= 0
        or type(max_stdout_bytes) is not int
        or max_stdout_bytes < 0
        or type(max_stderr_bytes) is not int
        or max_stderr_bytes < 0
    ):
        raise Phase08Error("worker resource limits are invalid")
    started = time.monotonic()
    process = subprocess.Popen(
        command,
        cwd=_workspace(),
        env=dict(P08_WORKER_ENVIRONMENT),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0,
    )
    assert process.stdin is not None and process.stdout is not None and process.stderr is not None
    selector = selectors.DefaultSelector()
    streams = {process.stdout: ("stdout", max_stdout_bytes), process.stderr: ("stderr", max_stderr_bytes)}
    for stream in streams:
        os.set_blocking(stream.fileno(), False)
        selector.register(stream, selectors.EVENT_READ)
    os.set_blocking(process.stdin.fileno(), False)
    selector.register(process.stdin, selectors.EVENT_WRITE)
    input_offset = 0
    chunks: dict[str, bytearray] = {"stdout": bytearray(), "stderr": bytearray()}
    overflow = False
    timed_out = False
    while selector.get_map():
        remaining = timeout_seconds - (time.monotonic() - started)
        if remaining <= 0:
            timed_out = True
            break
        for key, _mask in selector.select(min(remaining, 0.1)):
            stream = key.fileobj
            if stream is process.stdin:
                try:
                    written = os.write(stream.fileno(), native[input_offset : input_offset + 65_536])
                except BlockingIOError:
                    continue
                except BrokenPipeError:
                    written = 0
                input_offset += written
                if written == 0 or input_offset == len(native):
                    selector.unregister(stream)
                    stream.close()
                continue
            name, limit = streams[stream]
            try:
                chunk = os.read(stream.fileno(), 65_536)
            except BlockingIOError:
                continue
            if not chunk:
                selector.unregister(stream)
                stream.close()
                continue
            available = max(0, limit + 1 - len(chunks[name]))
            chunks[name].extend(chunk[:available])
            if len(chunks[name]) > limit or len(chunk) > available:
                overflow = True
                break
        if overflow:
            break
    if not timed_out and not overflow:
        remaining = timeout_seconds - (time.monotonic() - started)
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
    return {
        "stdout": bytes(chunks["stdout"]),
        "stderr": bytes(chunks["stderr"]),
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "overflow": overflow,
        "wall_time_ms": int((time.monotonic() - started) * 1_000),
    }


def _execution_record(
    manifest: Mapping[str, Any],
    identity: Mapping[str, Any],
    command: list[str],
    worker: Mapping[str, Any],
) -> dict[str, Any]:
    return {
        "kind": "subprocess",
        "runner_id": DERIVATIVE_ADAPTER_VERSION,
        "command": command,
        "executable": command[0],
        "environment": dict(P08_WORKER_ENVIRONMENT),
        "exit_code": worker["exit_code"],
        "timed_out": worker["timed_out"],
        "overflow": worker["overflow"],
        "wall_time_ms": worker["wall_time_ms"],
        "live_tool_executed": worker["exit_code"] is not None,
        "run_id": manifest["run_id"],
        "run_binding_digest": manifest["run_binding_digest"],
        "code_identity_digest": identity["code_identity_digest"],
    }


def _worker_failure(worker: Mapping[str, Any]) -> tuple[str, str] | None:
    if worker["timed_out"]:
        return "timeout", "The derivative worker exceeded the registered timeout."
    if worker["overflow"]:
        return "truncated_output", "The derivative worker exceeded a registered stream limit."
    if worker["exit_code"] != 0:
        return "execution_error", "The derivative worker exited unsuccessfully."
    return None


def _derive_result_from_raw(
    adapter: Any,
    request: Mapping[str, Any],
    native: bytes,
    stdout: bytes,
    stderr: bytes,
    execution: Mapping[str, Any],
    worker_failure: tuple[str, str] | None,
) -> dict[str, Any]:
    if worker_failure is not None:
        return adapter.build_derivative_result(
            request=request,
            worker_record=None,
            native_input=native,
            stdout=stdout,
            stderr=stderr,
            execution=execution,
            failure_status=worker_failure[0],
            failure_reason=worker_failure[1],
        )
    try:
        worker_record = adapter.parse_worker_stdout(stdout, request)
    except Exception as exc:
        return adapter.build_derivative_result(
            request=request,
            worker_record=None,
            native_input=native,
            stdout=stdout,
            stderr=stderr,
            execution=execution,
            failure_status="malformed_output",
            failure_reason=f"Worker evidence failed revalidation: {type(exc).__name__}: {exc}",
        )
    return adapter.build_derivative_result(
        request=request,
        worker_record=worker_record,
        native_input=native,
        stdout=stdout,
        stderr=stderr,
        execution=execution,
    )


def command_capability_run(args: argparse.Namespace) -> dict[str, Any]:
    root = _workspace()
    run_root, manifest, identity = _open_run(root, args.run_root)
    _require_p08a_pass(root, run_root, manifest, identity)
    preflight = _verify_preflight(run_root, manifest, identity)
    if args.candidate != "eq:cashflow-rate-derivative":
        raise Phase08Error("candidate argument violates the fixed capability ladder")
    if (args.timeout_seconds, args.max_output_bytes, args.max_artifact_bytes) != (
        10,
        P08_RAW_STREAM_LIMIT,
        P08_BUNDLE_LIMIT,
    ):
        raise Phase08Error("capability limits differ from the reviewed exact values")
    adapter = importlib.import_module("mathdevmcp.sympy_derivative_adapter")
    request = adapter.validate_derivative_request(preflight["dry_request"])
    native = adapter.canonical_json_bytes(request)
    if len(native) > P08_RAW_STREAM_LIMIT:
        raise Phase08Error("capability native input exceeds the reviewed exact limit")
    candidate_root = run_root / "p08b/backend/eq_cashflow_rate_derivative"
    if candidate_root.exists() or candidate_root.is_symlink():
        raise Phase08Error("capability candidate bundle already exists; no overwrite or duplicate execution")
    _assert_no_symlink(root, candidate_root.parent)
    candidate_root.mkdir(parents=True)
    worker_snapshot = run_root / "code-snapshot" / DERIVATIVE_ADAPTER_REF
    _assert_no_symlink(root, worker_snapshot)
    command = [P08_PYTHON, *P08_WORKER_PYTHON_FLAGS, str(worker_snapshot)]
    worker = _bounded_worker(
        command,
        native,
        timeout_seconds=args.timeout_seconds,
        max_stdout_bytes=args.max_output_bytes,
        max_stderr_bytes=args.max_output_bytes,
    )
    stdout = worker["stdout"]
    stderr = worker["stderr"]
    execution = _execution_record(manifest, identity, command, worker)
    _write_new(candidate_root / "native-input.json", native)
    _write_new(candidate_root / "stdout.bin", stdout)
    _write_new(candidate_root / "stderr.bin", stderr)
    result = _derive_result_from_raw(
        adapter,
        request,
        native,
        stdout,
        stderr,
        execution,
        _worker_failure(worker),
    )
    result_raw = adapter.canonical_json_bytes(result)
    if len(result_raw) > args.max_artifact_bytes:
        raise Phase08Error("capability structured result exceeds the bundle limit")
    _write_new(candidate_root / "result.json", result_raw)
    file_records = []
    candidate_limits = _candidate_file_limits(args.max_artifact_bytes)
    for name in ("native-input.json", "stdout.bin", "stderr.bin", "result.json"):
        raw = _read_regular_bounded(
            root, candidate_root / name, candidate_limits[name], name
        )
        file_records.append({"name": name, "sha256": _digest(raw), "byte_count": len(raw)})
    bundle_manifest = _bound_record(
        CAPABILITY_MANIFEST_SCHEMA,
        manifest,
        identity,
        {
            "candidate_id": args.candidate,
            "request_digest": request["request_digest"],
            "files": file_records,
            "fixed_overhead_bytes": P08_BUNDLE_OVERHEAD,
            "max_artifact_bytes": args.max_artifact_bytes,
            "publication_enabled": False,
        },
    )
    manifest_raw = _canonical(bundle_manifest)
    if len(manifest_raw) > args.max_artifact_bytes:
        raise Phase08Error("capability manifest exceeds the bundle limit")
    _candidate_aggregate(
        [item["byte_count"] for item in file_records],
        len(manifest_raw),
        P08_BUNDLE_OVERHEAD,
        args.max_artifact_bytes,
    )
    _write_new(candidate_root / "manifest.json", manifest_raw)
    _record_command(run_root, "capability-run", manifest, identity, _loaded_repo_modules(root, identity))
    _verify_code_identity(root, run_root)
    return {
        "status": result["status"],
        "run_id": manifest["run_id"],
        "run_root": manifest["run_root"],
        "result_digest": result["result_digest"],
        "manifest_sha256": _digest(manifest_raw),
        "can_promote": False,
        "publication_enabled": False,
    }


def command_verify_capability(args: argparse.Namespace) -> dict[str, Any]:
    root = _workspace()
    run_root, manifest, identity = _open_run(root, args.run_root)
    _require_p08a_pass(root, run_root, manifest, identity)
    preflight = _verify_preflight(run_root, manifest, identity)
    adapter = importlib.import_module("mathdevmcp.sympy_derivative_adapter")
    request = adapter.validate_derivative_request(preflight["dry_request"])
    candidate_root = run_root / "p08b/backend/eq_cashflow_rate_derivative"
    _assert_no_symlink(root, candidate_root)
    expected_names = {"native-input.json", "stdout.bin", "stderr.bin", "result.json", "manifest.json"}
    _require_exact_candidate_entries(candidate_root, expected_names)
    limits = _candidate_file_limits(P08_BUNDLE_LIMIT)
    raw_files = {
        name: _read_regular_bounded(root, candidate_root / name, limit, name)
        for name, limit in limits.items()
    }
    native = raw_files["native-input.json"]
    stdout = raw_files["stdout.bin"]
    stderr = raw_files["stderr.bin"]
    if native != adapter.canonical_json_bytes(request):
        raise Phase08Error("capability native input differs from preflight request")
    result_stored = _decode_canonical(raw_files["result.json"], "result.json")
    try:
        adapter.validate_derivative_result(result_stored)
    except Exception as exc:
        raise Phase08Error(
            f"capability structured result failed contract validation: {type(exc).__name__}: {exc}"
        ) from exc
    execution = result_stored["execution"]
    expected_worker = run_root / "code-snapshot" / DERIVATIVE_ADAPTER_REF
    if (
        execution.get("kind") != "subprocess"
        or execution.get("runner_id") != DERIVATIVE_ADAPTER_VERSION
        or execution.get("command")
        != [P08_PYTHON, *P08_WORKER_PYTHON_FLAGS, str(expected_worker)]
        or execution.get("executable") != P08_PYTHON
        or execution.get("environment") != P08_WORKER_ENVIRONMENT
        or execution.get("run_id") != manifest["run_id"]
        or execution.get("run_binding_digest") != manifest["run_binding_digest"]
        or execution.get("code_identity_digest") != identity["code_identity_digest"]
    ):
        raise Phase08Error("capability execution envelope binding mismatch")
    failure = _worker_failure(
        {
            "exit_code": execution["exit_code"],
            "timed_out": execution["timed_out"],
            "overflow": execution["overflow"],
        }
    )
    try:
        result_derived = _derive_result_from_raw(
            adapter, request, native, stdout, stderr, execution, failure
        )
    except Exception as exc:
        raise Phase08Error(
            f"capability raw-byte reconstruction failed: {type(exc).__name__}: {exc}"
        ) from exc
    if adapter.canonical_json_bytes(result_stored) != adapter.canonical_json_bytes(result_derived):
        raise Phase08Error("capability structured result differs from independent raw-byte derivation")
    bundle_manifest = _decode_canonical(raw_files["manifest.json"], "manifest.json")
    _require_record_binding(bundle_manifest, manifest, identity)
    if bundle_manifest.get("schema_version") != CAPABILITY_MANIFEST_SCHEMA:
        raise Phase08Error("capability bundle manifest schema mismatch")
    if set(bundle_manifest) != {
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
    }:
        raise Phase08Error("capability bundle manifest keys mismatch")
    if bundle_manifest.get("request_digest") != request["request_digest"]:
        raise Phase08Error("capability manifest request mismatch")
    if (
        bundle_manifest.get("candidate_id") != "eq:cashflow-rate-derivative"
        or bundle_manifest.get("fixed_overhead_bytes") != P08_BUNDLE_OVERHEAD
        or bundle_manifest.get("max_artifact_bytes") != P08_BUNDLE_LIMIT
        or bundle_manifest.get("publication_enabled") is not False
    ):
        raise Phase08Error("capability manifest scientific/budget boundary mismatch")
    expected_file_records = []
    for name in ("native-input.json", "stdout.bin", "stderr.bin", "result.json"):
        raw = raw_files[name]
        expected_file_records.append({"name": name, "sha256": _digest(raw), "byte_count": len(raw)})
    if bundle_manifest.get("files") != expected_file_records:
        raise Phase08Error("capability manifest predecessor binding mismatch")
    manifest_raw = raw_files["manifest.json"]
    exact_sum, final_aggregate = _candidate_aggregate(
        [item["byte_count"] for item in expected_file_records],
        len(manifest_raw),
        bundle_manifest["fixed_overhead_bytes"],
        bundle_manifest["max_artifact_bytes"],
    )
    _require_exact_candidate_entries(candidate_root, expected_names)
    if result_stored["status"] not in {"backend_checked", "source_target_mismatch"}:
        raise Phase08Error("capability execution ended in an engineering/non-evidence status")
    decision = _bound_record(
        CAPABILITY_DECISION_SCHEMA,
        manifest,
        identity,
        {
            "status": result_stored["status"],
            "candidate_id": "eq:cashflow-rate-derivative",
            "request_digest": request["request_digest"],
            "result_digest": result_stored["result_digest"],
            "manifest_sha256": _digest(manifest_raw),
            "manifest_byte_count": len(manifest_raw),
            "counted_file_byte_sum": exact_sum,
            "fixed_overhead_bytes": bundle_manifest["fixed_overhead_bytes"],
            "final_aggregate_bytes": final_aggregate,
            "max_artifact_bytes": bundle_manifest["max_artifact_bytes"],
            "claim_class": result_stored["claim_class"],
            "can_promote": False,
            "publication_enabled": False,
            "formal_proof_certified": False,
            "vetoes": [],
            "non_claims": result_stored["non_claims"],
        },
    )
    decision["decision_digest"] = _digest(decision)
    _write_json_new(run_root / "p08b/capability-decision.json", decision)
    _record_command(run_root, "verify-capability", manifest, identity, _loaded_repo_modules(root, identity))
    _verify_code_identity(root, run_root)
    return {
        "status": decision["status"],
        "run_id": manifest["run_id"],
        "run_root": manifest["run_root"],
        "decision_digest": decision["decision_digest"],
        "can_promote": False,
        "publication_enabled": False,
        "formal_proof_certified": False,
    }


def command_not_implemented(args: argparse.Namespace) -> dict[str, Any]:
    raise Phase08Error(f"{args.command} is not implemented until the verified capability handoff")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    fresh = subparsers.add_parser("freeze-extract")
    fresh.add_argument("--artifact-root", required=True)
    fresh.add_argument("--new-run", action="store_true")
    fresh.set_defaults(handler=command_freeze_extract)
    for name, handler in (
        ("resolve-context", command_resolve_context),
        ("verify-p08a", command_verify_p08a),
        ("capability-preflight", command_capability_preflight),
        ("capability-run", command_capability_run),
        ("verify-capability", command_verify_capability),
        ("frozen-workflow", command_not_implemented),
        ("verify-final", command_not_implemented),
    ):
        child = subparsers.add_parser(name)
        child.add_argument("--run-root", required=True)
        if name == "capability-run":
            child.add_argument("--candidate", required=True)
            child.add_argument("--timeout-seconds", required=True, type=int)
            child.add_argument("--max-output-bytes", required=True, type=int)
            child.add_argument("--max-artifact-bytes", required=True, type=int)
        if name == "frozen-workflow":
            child.add_argument("--budget-profile", required=True)
            child.add_argument("--max-attempts", required=True, type=int)
            child.add_argument("--workers", required=True, type=int)
            child.add_argument("--target-limit", required=True, type=int)
        child.set_defaults(handler=handler)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if sys.executable != P08_PYTHON:
            raise Phase08Error(f"Phase 08 requires the pinned interpreter {P08_PYTHON}")
        if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
            raise Phase08Error("Phase 08 requires CUDA_VISIBLE_DEVICES=-1 before import")
        result = args.handler(args)
    except Phase08Error as exc:
        sys.stderr.write(f"P08_VETO: {exc}\n")
        return 2
    sys.stdout.buffer.write(_canonical(result) + b"\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
