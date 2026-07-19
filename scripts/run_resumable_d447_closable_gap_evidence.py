from __future__ import annotations

"""Run the bounded real-D447 evidence gates for the closable-gap program."""

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import Any

from mathdevmcp.evidence_manifest import canonical_json_bytes
from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.mcp_server import negative_evidence_label, proof_packet_label
from mathdevmcp.negative_evidence import build_negative_evidence_label
from mathdevmcp.proof_packet import build_proof_packet_label
from mathdevmcp.resumable_audit import (
    create_resumable_audit_session,
    persist_resumable_audit_session,
    run_session_label_audits,
)
from mathdevmcp.resumable_tree import (
    page_resumable_tree_records,
    resolve_resumable_tree_record,
)


SOURCE = Path("/home/chakwong/python/DynareMCP/docs/AIpostdoc/finalBGS/bgs_final_committee_report_d447.tex")
SOURCE_DIGEST = "c5cfc66061ce90b053cf7e1df6eb770bababfcda85aa54c26546437037da0690"
LABELS = [
    "eq:author-counterfactual-window",
    "eq:bgs-paper-c71-restated",
    "eq:sw-wage-phillips",
]


def _write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _without_provenance(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _without_provenance(item)
            for key, item in value.items()
            if key not in {"audit_provenance", "artifact", "detail_resolution", "payload_guardrail"}
        }
    if isinstance(value, list):
        return [_without_provenance(item) for item in value]
    return value


def _unwrap(result: Any) -> dict[str, Any]:
    if hasattr(result, "structuredContent"):
        value = result.structuredContent
    else:
        value = result
    if isinstance(value, dict) and value.get("ok") is True and isinstance(value.get("result"), dict):
        return value["result"]
    if isinstance(value, dict) and value.get("ok") is True:
        return {key: item for key, item in value.items() if key != "ok"}
    if not isinstance(value, dict):
        raise RuntimeError(f"unexpected public result: {type(value).__name__}")
    return value


def _run_cli(command: str, args: list[str]) -> dict[str, Any]:
    env = {**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"), "CUDA_VISIBLE_DEVICES": "-1"}
    completed = subprocess.run(
        [sys.executable, "-m", "mathdevmcp.cli", command, *args],
        cwd=Path(__file__).resolve().parents[1],
        env=env,
        capture_output=True,
        text=True,
        check=False,
        timeout=240,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr)
    return json.loads(completed.stdout)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1":
        raise RuntimeError("set CUDA_VISIBLE_DEVICES=-1 before the D447 evidence run")
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest() != SOURCE_DIGEST:
        raise RuntimeError("D447 source digest drift")

    started = time.perf_counter()
    session, index, parser_policy = create_resumable_audit_session(
        SOURCE.parent,
        SOURCE.name,
        LABELS,
        source_digest=SOURCE_DIGEST,
        backend="sympy",
        paragraph_context=False,
        context_before=0,
        context_after=0,
        task_context="general_math_audit",
        summary_only=True,
    )
    persist_resumable_audit_session(session, args.artifact_root)
    batch = run_session_label_audits(
        session,
        args.artifact_root,
        index=index,
        parser_policy=parser_policy,
    )
    if not batch.get("complete"):
        raise RuntimeError("current-schema packet sample is incomplete")
    records = {
        item["label"]: item["record"]
        for item in batch["records"]
    }

    parity: list[dict[str, Any]] = []
    for index_value, label in enumerate(LABELS):
        record_id = records[label]["record_id"]
        packet_args = {
            "file": SOURCE.name,
            "source_digest": SOURCE_DIGEST,
            "summary_only": True,
            "checkpoint_root": str(args.artifact_root),
            "checkpoint_session_id": session["session_id"],
            "checkpoint_record_index": index_value,
            "checkpoint_record_id": record_id,
        }
        negative_checkpoint_args = {
            key: packet_args[key]
            for key in (
                "checkpoint_root",
                "checkpoint_session_id",
                "checkpoint_record_index",
                "checkpoint_record_id",
            )
        }
        uncached_started = time.perf_counter()
        uncached = build_proof_packet_label(str(SOURCE.parent), label, file=SOURCE.name, source_digest=SOURCE_DIGEST, summary_only=True)
        uncached_seconds = time.perf_counter() - uncached_started
        cached_started = time.perf_counter()
        cached = build_proof_packet_label(str(SOURCE.parent), label, **packet_args)
        cached_seconds = time.perf_counter() - cached_started
        negative_uncached = build_negative_evidence_label(str(SOURCE.parent), label, file=SOURCE.name, source_digest=SOURCE_DIGEST)
        negative_cached = build_negative_evidence_label(
            str(SOURCE.parent),
            label,
            file=SOURCE.name,
            source_digest=SOURCE_DIGEST,
            **negative_checkpoint_args,
        )
        facade = _unwrap(call_mcp_tool("proof_packet_label", {"root": str(SOURCE.parent), "label": label, **packet_args, "response_mode": "detailed"}))
        server = _unwrap(proof_packet_label(root=str(SOURCE.parent), label=label, response_mode="detailed", **packet_args))
        cli = _run_cli(
            "proof-packet-label",
            [label, "--root", str(SOURCE.parent), "--file", SOURCE.name, "--source-digest", SOURCE_DIGEST, "--summary-only", "--checkpoint-root", str(args.artifact_root), "--checkpoint-session-id", session["session_id"], "--checkpoint-record-index", str(index_value), "--checkpoint-record-id", record_id],
        )
        negative_facade = _unwrap(call_mcp_tool("negative_evidence_label", {"root": str(SOURCE.parent), "label": label, "file": SOURCE.name, "source_digest": SOURCE_DIGEST, **{key: packet_args[key] for key in ("checkpoint_root", "checkpoint_session_id", "checkpoint_record_index", "checkpoint_record_id")}, "response_mode": "detailed"}))
        negative_server = _unwrap(negative_evidence_label(root=str(SOURCE.parent), label=label, file=SOURCE.name, source_digest=SOURCE_DIGEST, response_mode="detailed", **{key: packet_args[key] for key in ("checkpoint_root", "checkpoint_session_id", "checkpoint_record_index", "checkpoint_record_id")}))
        negative_cli = _run_cli(
            "negative-evidence-label",
            [label, "--root", str(SOURCE.parent), "--file", SOURCE.name, "--source-digest", SOURCE_DIGEST, "--checkpoint-root", str(args.artifact_root), "--checkpoint-session-id", session["session_id"], "--checkpoint-record-index", str(index_value), "--checkpoint-record-id", record_id],
        )
        packet_projection = _without_provenance(cached)
        negative_projection = _without_provenance(negative_cached)
        if any(_without_provenance(item) != packet_projection for item in (uncached, facade, server, cli)):
            raise RuntimeError(f"proof packet semantic parity failed for {label}")
        if any(_without_provenance(item) != negative_projection for item in (negative_uncached, negative_facade, negative_server, negative_cli)):
            raise RuntimeError(f"negative packet semantic parity failed for {label}")
        parity.append({
            "label": label,
            "record_id": record_id,
            "proof_reused": cached["audit_provenance"],
            "negative_reused": negative_cached["audit_provenance"],
            "proof_semantic_sha256": hashlib.sha256(canonical_json_bytes(packet_projection)).hexdigest(),
            "negative_semantic_sha256": hashlib.sha256(canonical_json_bytes(negative_projection)).hexdigest(),
            "uncached_seconds": uncached_seconds,
            "cached_seconds": cached_seconds,
            "timing_classification": "descriptive_only",
            "public_routes": ["library", "facade", "fastmcp", "cli"],
        })

    tree_root = Path("/home/chakwong/python/MathDevMCP/.local/mathdevmcp/evidence/resumable-d447-remediation-20260718/full/tree")
    tree_session_id = "tree_session_9e949d6d64b7b8ba9eda0cec954f7a47ed200dbfcfb3557ca95d410e76f42c11"
    page_count = 0
    record_count = 0
    seen: set[int] = set()
    resolved_bytes = 0
    max_page_bytes = 0
    token: str | None = None
    while True:
        page = page_resumable_tree_records(tree_root, tree_session_id, limit=20, page_token=token)
        page_count += 1
        page_bytes = len(canonical_json_bytes(page))
        max_page_bytes = max(max_page_bytes, page_bytes)
        if page_bytes > 30_720:
            raise RuntimeError("tree page exceeded public payload budget")
        for item in page["records"]:
            index_value = int(item["index"])
            if index_value in seen:
                raise RuntimeError("duplicate tree record index")
            seen.add(index_value)
            record_count += 1
            payload = bytearray()
            byte_offset = 0
            while True:
                resolved = resolve_resumable_tree_record(
                    tree_root,
                    page["page_token"],
                    index_value,
                    record_sha256=item["record_sha256"],
                    byte_offset=byte_offset,
                    byte_limit=16_384,
                )
                payload.extend(base64.b64decode(resolved["canonical_record_base64"]))
                if resolved["next_byte_offset"] is None:
                    break
                byte_offset = int(resolved["next_byte_offset"])
            if hashlib.sha256(payload).hexdigest() != item["record_sha256"]:
                raise RuntimeError("resolved tree record digest mismatch")
            resolved_bytes += len(payload)
        token = page.get("continuation_token")
        if token is None:
            break
    if record_count != 434 or len(seen) != 434:
        raise RuntimeError("D447 tree page coverage mismatch")

    result = {
        "schema_version": "d447_closable_gap_evidence@1",
        "status": "passed",
        "source": {"path": str(SOURCE), "sha256": SOURCE_DIGEST},
        "environment": {"cuda_visible_devices": os.environ.get("CUDA_VISIBLE_DEVICES"), "execution_mode": "cpu_only"},
        "packet_session": {"session_id": session["session_id"], "options": session["options"], "record_count": len(records)},
        "packet_parity": parity,
        "tree_page_walk": {"session_id": tree_session_id, "page_count": page_count, "record_count": record_count, "unique_indices": len(seen), "resolved_record_bytes": resolved_bytes, "max_page_bytes": max_page_bytes, "public_page_budget_bytes": 30_720, "publication_enabled": False},
        "elapsed_seconds": time.perf_counter() - started,
        "non_claim": "These gates establish source-bound engineering reuse and bounded transport only; they do not prove D447 mathematics, scientific validity, publication readiness, or independent generalization.",
    }
    _write(args.output, result)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
