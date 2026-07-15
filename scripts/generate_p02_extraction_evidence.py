#!/usr/bin/env python3
"""Generate source-reconstructed Phase 02 extraction evidence once."""

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


ROUND_PARENT = PurePosixPath(".local/mathdevmcp/evidence/p02r3-20260712/result-rounds")
GUARD_REF = "tests/p02_no_backend_guard.py"


def _parse_argv(argv: list[str]) -> str:
    if len(argv) != 2 or argv[0] != "--round-root" or "=" in argv[0]:
        raise EvidenceValidationError("usage: generate_p02_extraction_evidence.py --round-root RR")
    value = PurePosixPath(argv[1])
    if value.parent != ROUND_PARENT or value.name not in {f"rr0{index}" for index in range(1, 6)}:
        raise EvidenceValidationError("Phase 02 generator round root is outside the reviewed scope")
    return value.as_posix()


def _root() -> Path:
    root = Path.cwd().absolute()
    if not (root / ".git").exists() or not (root / "src/mathdevmcp").is_dir():
        raise EvidenceValidationError("Phase 02 generator must run from the MathDevMCP workspace root")
    return root


def _require_formal_environment(round_ref: str) -> None:
    expected = {
        "MATHDEVMCP_P02_ACTION": "generate_extraction_bundle",
        "MATHDEVMCP_P02_DISPATCH_DEPTH": "1",
        "MATHDEVMCP_P02_ROUND_ROOT": round_ref,
    }
    if any(os.environ.get(key) != value for key, value in expected.items()):
        raise EvidenceValidationError("Phase 02 generator formal environment mismatch")


def _manifest_digest(raw: bytes, ref: str) -> str:
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("Phase 02 round manifest is not strict UTF-8") from exc
    if not text or not text.endswith("\n") or "\r" in text or "\x00" in text:
        raise EvidenceValidationError("Phase 02 round manifest has invalid bytes")
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
            raise EvidenceValidationError("Phase 02 round manifest line is invalid")
        records[logical_ref] = digest
    if list(records) != sorted(records, key=lambda item: item.encode("utf-8")) or ref not in records:
        raise EvidenceValidationError("Phase 02 round manifest does not bind the guard")
    return records[ref]


def _load_install_guard(root: Path, round_ref: str) -> Callable[..., ContextManager[object]]:
    manifest_ref = f"{round_ref}/implementation-round-sha256.txt"
    manifest_raw, manifest_info = read_bytes_no_follow(root, manifest_ref)
    guard_raw, guard_info = read_bytes_no_follow(root, GUARD_REF)
    if not stat.S_ISREG(manifest_info.st_mode) or not stat.S_ISREG(guard_info.st_mode):
        raise EvidenceValidationError("Phase 02 guard or round manifest is not a regular file")
    if content_digest(guard_raw) != _manifest_digest(manifest_raw, GUARD_REF):
        raise EvidenceValidationError("Phase 02 guard differs from the initialized round manifest")

    module = ModuleType("_mathdevmcp_p02_no_backend_guard")
    module.__file__ = str(root / GUARD_REF)
    exec(compile(guard_raw, module.__file__, "exec"), module.__dict__)
    install_guard = module.__dict__.get("install_guard")
    if not callable(install_guard):
        raise EvidenceValidationError("Phase 02 guard does not expose install_guard")
    return install_guard


def _require_absent(root: Path, refs: list[str]) -> None:
    for ref in refs:
        path = root / ref
        if path.exists() or path.is_symlink():
            raise EvidenceValidationError(f"Phase 02 generator output already exists: {ref}")


def _write(root: Path, ref: str, value: object) -> dict[str, object]:
    raw = canonical_json_bytes(value)
    result = atomic_write_bytes_no_replace(root, ref, raw)
    reopened, _ = read_bytes_no_follow(root, ref)
    if reopened != raw or content_digest(reopened) != result["sha256"]:
        raise EvidenceValidationError(f"Phase 02 generator reopen mismatch: {ref}")
    return result


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    round_ref = _parse_argv(args)
    root = _root()
    _require_formal_environment(round_ref)
    install_guard = _load_install_guard(root, round_ref)

    # Import source reconstruction only after the guard has patched every
    # backend-capable module reachable in this process.
    with install_guard(round_root=round_ref, action="generate_extraction_bundle", formal=True):
        from mathdevmcp.extraction_evidence import (
            build_mutation_matrix,
            build_obligation_bundle,
            build_reconstruction_summary,
            extraction_artifact_refs,
            verify_parser_comparison,
        )

        refs = extraction_artifact_refs(round_ref)
        _require_absent(
            root,
            [
                refs["bundle_index"],
                refs["obligations"],
                refs["reconstruction_summary"],
                refs["mutation_matrix"],
                refs["backend_ledger_index"],
            ],
        )
        implementation_manifest_ref = f"{round_ref}/implementation-round-sha256.txt"
        verified_parser = verify_parser_comparison(
            root,
            refs["parser_comparison"],
            implementation_manifest_ref,
        )
        if verified_parser["ref"] != refs["parser_comparison"]:
            raise EvidenceValidationError("Phase 02R2 parser comparison ref differs after verification")
        result_round = PurePosixPath(round_ref).name
        obligations = build_obligation_bundle(root, result_round)
        reconstruction = build_reconstruction_summary(root, result_round)
        mutation = build_mutation_matrix(root, result_round)
        _write(root, refs["obligations"], obligations)
        _write(root, refs["reconstruction_summary"], reconstruction)
        _write(root, refs["mutation_matrix"], mutation)

    # Guard closure seals this action's own ledger and attestation. Packaging
    # below only reopens already reconstructed bytes and launches no process.
    from mathdevmcp.extraction_evidence import (
        build_backend_ledger_index,
        build_bundle_index,
        extraction_artifact_refs,
        verify_backend_ledger_index,
        verify_bundle_index,
    )

    refs = extraction_artifact_refs(round_ref)
    ledger_index = build_backend_ledger_index(root, round_ref)
    _write(root, refs["backend_ledger_index"], ledger_index)
    verify_backend_ledger_index(root, refs["backend_ledger_index"])

    bundle = build_bundle_index(
        root,
        round_ref,
        artifact_roles={
            refs["obligations"]: "source_reconstructed_label_scoped_obligations",
            refs["reconstruction_summary"]: "source_oracle_reconstruction_summary",
            refs["parser_comparison"]: "differential_parser_fidelity_comparison",
            refs["mutation_matrix"]: "identity_mutation_and_ambiguity_matrix",
            refs["backend_ledger_index"]: "zero_backend_guard_ledger_index",
        },
    )
    written = _write(root, refs["bundle_index"], bundle)
    verified = verify_bundle_index(root, refs["bundle_index"])
    if verified["sha256"] != written["sha256"]:
        raise EvidenceValidationError("Phase 02 bundle verification digest mismatch")
    sys.stdout.buffer.write(
        canonical_json_bytes(
            {
                "bundle_index_ref": refs["bundle_index"],
                "bundle_index_sha256": verified["sha256"],
            }
        )
        + b"\n"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
