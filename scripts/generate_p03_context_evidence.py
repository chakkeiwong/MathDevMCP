#!/usr/bin/env python3
"""Generate the Phase 03 context-only evidence bundle once."""

from __future__ import annotations

import os
from pathlib import Path, PurePosixPath
import stat
import sys
from types import ModuleType
from typing import Callable, ContextManager

from mathdevmcp.evidence_manifest import (
    EvidenceValidationError,
    atomic_write_bytes_no_replace,
    canonical_json_bytes,
    content_digest,
    read_bytes_no_follow,
)


ROUND_PARENT = PurePosixPath(".local/mathdevmcp/evidence/p03-20260712/result-rounds")
GUARD_REF = "tests/p03_no_backend_guard.py"


def _parse_argv(argv: list[str]) -> str:
    if len(argv) != 2 or argv[0] != "--round-root" or any("=" in item for item in argv):
        raise EvidenceValidationError("usage: generate_p03_context_evidence.py --round-root RR")
    value = PurePosixPath(argv[1])
    if value.parent != ROUND_PARENT or value.name not in {f"rr0{index}" for index in range(1, 6)}:
        raise EvidenceValidationError("Phase 03 generator round root is outside the reviewed scope")
    return value.as_posix()


def _root() -> Path:
    root = Path.cwd().absolute()
    if not (root / ".git").exists() or not (root / "src/mathdevmcp").is_dir():
        raise EvidenceValidationError("Phase 03 generator must run from the MathDevMCP workspace root")
    return root


def _require_formal_environment(round_ref: str) -> None:
    expected = {
        "MATHDEVMCP_P03_ACTION": "generate_context_bundle",
        "MATHDEVMCP_P03_DISPATCH_DEPTH": "1",
        "MATHDEVMCP_P03_ROUND_ROOT": round_ref,
        "CUDA_VISIBLE_DEVICES": "-1",
        "TMPDIR": f"{Path.cwd().absolute() / round_ref / 'governance/tmp'}",
    }
    if any(os.environ.get(key) != value for key, value in expected.items()):
        raise EvidenceValidationError("Phase 03 generator formal environment mismatch")


def _manifest_digest(raw: bytes, ref: str) -> str:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("Phase 03 implementation manifest is not strict UTF-8") from exc
    if not text.endswith("\n") or "\r" in text or "\x00" in text:
        raise EvidenceValidationError("Phase 03 implementation manifest has invalid bytes")
    records: dict[str, str] = {}
    for line in text.splitlines():
        digest, separator, logical_ref = line.partition("  ")
        if (
            separator != "  "
            or len(digest) != 64
            or any(char not in "0123456789abcdef" for char in digest)
            or not logical_ref
            or logical_ref in records
        ):
            raise EvidenceValidationError("Phase 03 implementation manifest line is invalid")
        records[logical_ref] = digest
    if list(records) != sorted(records, key=lambda item: item.encode("utf-8")) or ref not in records:
        raise EvidenceValidationError("Phase 03 implementation manifest does not bind the guard")
    return records[ref]


def _load_install_guard(root: Path, round_ref: str) -> Callable[..., ContextManager[object]]:
    manifest_ref = f"{round_ref}/implementation-round-sha256.txt"
    manifest_raw, manifest_info = read_bytes_no_follow(root, manifest_ref)
    guard_raw, guard_info = read_bytes_no_follow(root, GUARD_REF)
    if not stat.S_ISREG(manifest_info.st_mode) or not stat.S_ISREG(guard_info.st_mode):
        raise EvidenceValidationError("Phase 03 guard or round manifest is not a regular file")
    if content_digest(guard_raw) != _manifest_digest(manifest_raw, GUARD_REF):
        raise EvidenceValidationError("Phase 03 guard differs from the initialized round manifest")
    module = ModuleType("_mathdevmcp_p03_no_backend_guard")
    module.__file__ = str(root / GUARD_REF)
    exec(compile(guard_raw, module.__file__, "exec"), module.__dict__)
    install_guard = module.__dict__.get("install_guard")
    if not callable(install_guard):
        raise EvidenceValidationError("Phase 03 guard does not expose install_guard")
    return install_guard


def _require_absent(root: Path, refs: list[str]) -> None:
    for ref in refs:
        path = root / ref
        if path.exists() or path.is_symlink():
            raise EvidenceValidationError(f"Phase 03 generator output already exists: {ref}")


def _write(root: Path, ref: str, value: object) -> dict[str, object]:
    raw = canonical_json_bytes(value)
    result = atomic_write_bytes_no_replace(root, ref, raw)
    reopened, info = read_bytes_no_follow(root, ref)
    if not stat.S_ISREG(info.st_mode) or reopened != raw or content_digest(reopened) != result["sha256"]:
        raise EvidenceValidationError(f"Phase 03 generator reopen mismatch: {ref}")
    return result


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    round_ref = _parse_argv(args)
    root = _root()
    _require_formal_environment(round_ref)
    install_guard = _load_install_guard(root, round_ref)

    with install_guard(round_root=round_ref, action="generate_context_bundle", formal=True):
        from mathdevmcp.context_evidence import (
            build_context_evidence_payload,
            context_artifact_refs,
            validate_context_manifest,
        )

        refs = context_artifact_refs(round_ref)
        _require_absent(root, list(refs.values()))
        payload = build_context_evidence_payload(root)
        for manifest in payload["manifests"]:
            validate_context_manifest(manifest)
        values = {
            refs["corpus_graphs"]: payload["corpus_graphs"],
            refs["manifests"]: {
                "schema_version": "p03_context_manifest_collection@1",
                "manifests": payload["manifests"],
            },
            refs["symbol_ledger"]: payload["symbol_resolution_ledger"],
            refs["notation_ledger"]: payload["notation_conflict_ledger"],
            refs["typed_assumptions"]: payload["typed_assumptions"],
            refs["parser_ledger"]: payload["ledgers"]["parser"],
            refs["context_ledger"]: payload["ledgers"]["context"],
            refs["mathematical_ledger"]: payload["ledgers"]["mathematical"],
            refs["engineering_ledger"]: payload["ledgers"]["engineering"],
            refs["interpretation_ledger"]: payload["ledgers"]["interpretation"],
            refs["mutation_matrix"]: payload["mutation_matrix"],
            refs["frozen_regressions"]: payload["frozen_regressions"],
        }
        for ref in sorted(values, key=lambda item: item.encode("utf-8")):
            _write(root, ref, values[ref])

    from mathdevmcp.context_evidence import (
        build_context_bundle_index,
        build_guard_index,
        context_artifact_refs,
        reconstruct_context_bundle,
    )

    refs = context_artifact_refs(round_ref)
    guard_index = build_guard_index(root, round_ref)
    _write(root, refs["guard_index"], guard_index)
    values[refs["guard_index"]] = guard_index
    bundle_index = build_context_bundle_index(root, refs, values)
    written = _write(root, refs["bundle_index"], bundle_index)
    reconstructed = reconstruct_context_bundle(root, refs["bundle_index"])
    if reconstructed["bundle_semantic_digest"] != bundle_index["bundle_semantic_digest"]:
        raise EvidenceValidationError("Phase 03 generator bundle reconstruction mismatch")
    sys.stdout.buffer.write(
        canonical_json_bytes(
            {
                "bundle_index_ref": refs["bundle_index"],
                "bundle_index_sha256": written["sha256"],
                "bundle_semantic_digest": bundle_index["bundle_semantic_digest"],
            }
        )
        + b"\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
