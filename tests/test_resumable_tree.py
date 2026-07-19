from __future__ import annotations

import hashlib
import base64
from copy import deepcopy
import json
from pathlib import Path

import pytest

from mathdevmcp.cli import main as cli_main
from mathdevmcp.document_derivation_tree import audit_document_derivation_tree
from mathdevmcp.evidence_manifest import canonical_json_bytes
from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.mcp_server import (
    page_resumable_tree_records as fastmcp_page_resumable_tree_records,
)
from mathdevmcp.mcp_server import (
    resolve_resumable_tree_record as fastmcp_resolve_resumable_tree_record,
)
from mathdevmcp.resumable_tree import (
    assemble_resumable_tree_result,
    create_resumable_tree_session,
    persist_resumable_tree_session,
    page_resumable_tree_records,
    resolve_resumable_tree_record,
    run_resumable_tree_targets,
)


LABELS = ["eq:first", "eq:second"]


def _redigest_page_token(token: str, **changes: object) -> str:
    padded = token + "=" * (-len(token) % 4)
    envelope = json.loads(base64.urlsafe_b64decode(padded).decode("utf-8"))
    envelope["payload"].update(changes)
    payload = canonical_json_bytes(envelope["payload"])
    envelope["sha256"] = hashlib.sha256(payload).hexdigest()
    return base64.urlsafe_b64encode(canonical_json_bytes(envelope)).decode("ascii").rstrip("=")


def _fixture(tmp_path: Path) -> tuple[Path, str]:
    source = tmp_path / "tree.tex"
    source.write_text(
        r"""\section{Tree fixture}
\begin{equation}x=x\label{eq:first}\end{equation}
\begin{equation}y=y\label{eq:second}\end{equation}
""",
        encoding="utf-8",
    )
    return source, hashlib.sha256(source.read_bytes()).hexdigest()


def _semantic_projection(result: dict) -> dict:
    return {
        "coverage": result["coverage"],
        "target_extraction": result["target_extraction"],
        "targets": result["targets"],
        "context_targets": result["context_targets"],
        "publication_mode": result["publication_mode"],
        "publication_veto_ids": result["publication_veto_ids"],
        "non_claims": result["non_claims"],
    }


def test_tree_targets_resume_and_preserve_document_assembly(tmp_path: Path) -> None:
    source, digest = _fixture(tmp_path)
    uninterrupted = audit_document_derivation_tree(
        source,
        focus_labels=LABELS,
        max_labels=2,
        max_attempts=1,
    )
    session, context = create_resumable_tree_session(
        source,
        LABELS,
        source_digest=digest,
        max_attempts=1,
    )
    persisted = persist_resumable_tree_session(session, tmp_path / "artifacts")
    assert persist_resumable_tree_session(session, tmp_path / "artifacts") == persisted
    first = run_resumable_tree_targets(session, context, tmp_path / "artifacts", max_new_records=1)
    second = run_resumable_tree_targets(session, context, tmp_path / "artifacts", max_new_records=1)
    third = run_resumable_tree_targets(session, context, tmp_path / "artifacts")
    resumed = assemble_resumable_tree_result(session, third)

    assert first["completed_count"] == 1 and first["pending_count"] == 1
    assert second["complete"] is True and second["reused_count"] == 1
    assert third["complete"] is True and third["reused_count"] == 2
    assert canonical_json_bytes(_semantic_projection(resumed)) == canonical_json_bytes(
        _semantic_projection(uninterrupted)
    )
    assert resumed["resumable_evidence"]["record_ids"] == [
        item["record"]["record_id"] for item in third["records"]
    ]


def _completed_tree(tmp_path: Path) -> tuple[dict, Path]:
    source, digest = _fixture(tmp_path)
    session, context = create_resumable_tree_session(
        source, LABELS, source_digest=digest, max_attempts=1
    )
    artifacts = tmp_path / "artifacts"
    persist_resumable_tree_session(session, artifacts)
    batch = run_resumable_tree_targets(session, context, artifacts)
    assert batch["complete"] is True
    return session, artifacts


def test_resumable_tree_pages_and_chunked_resolver_reconstruct_exact_record(tmp_path: Path) -> None:
    session, artifacts = _completed_tree(tmp_path)
    first = page_resumable_tree_records(artifacts, session["session_id"], limit=1)
    second = page_resumable_tree_records(
        artifacts, session["session_id"], page_token=first["continuation_token"]
    )

    assert first["returned_count"] == second["returned_count"] == 1
    assert [first["records"][0]["label"], second["records"][0]["label"]] == LABELS
    assert first["payload_guardrail"]["status"] == "met"
    assert first["publication_enabled"] is False

    meta = first["records"][0]
    chunks: list[bytes] = []
    offset = 0
    while True:
        resolved = resolve_resumable_tree_record(
            artifacts, first["page_token"], meta["index"],
            record_sha256=meta["record_sha256"], byte_offset=offset, byte_limit=127,
        )
        chunks.append(base64.b64decode(resolved["canonical_record_base64"]))
        if resolved["next_byte_offset"] is None:
            break
        offset = resolved["next_byte_offset"]
    payload = b"".join(chunks)
    assert hashlib.sha256(payload).hexdigest() == meta["record_sha256"]


def test_resumable_tree_page_and_resolver_fail_closed(tmp_path: Path) -> None:
    session, artifacts = _completed_tree(tmp_path)
    first = page_resumable_tree_records(artifacts, session["session_id"], limit=1)
    meta = first["records"][0]

    with pytest.raises(ValueError, match="invalid|digest"):
        page_resumable_tree_records(
            artifacts, session["session_id"], page_token=first["continuation_token"][:-1] + "A"
        )
    forged = _redigest_page_token(first["page_token"], next_offset=2)
    with pytest.raises(ValueError, match="not issued"):
        resolve_resumable_tree_record(
            artifacts, forged, 0, record_sha256=meta["record_sha256"]
        )
    with pytest.raises(ValueError, match="not issued"):
        page_resumable_tree_records(
            artifacts, session["session_id"], page_token=forged
        )
    with pytest.raises(ValueError, match="outside the page token scope"):
        resolve_resumable_tree_record(
            artifacts, first["page_token"], 1, record_sha256=meta["record_sha256"]
        )
    with pytest.raises(ValueError, match="record digest mismatch"):
        resolve_resumable_tree_record(
            artifacts, first["page_token"], 0, record_sha256="0" * 64
        )

    target_directory = (
        artifacts / "resumable-trees" / session["session_id"] / "targets"
    )
    extra = target_directory / "unexpected.json"
    extra.write_text("{}", encoding="utf-8")
    with pytest.raises(ValueError, match="record inventory mismatch"):
        page_resumable_tree_records(artifacts, session["session_id"])
    extra.unlink()

    session_path = artifacts / "resumable-trees" / session["session_id"] / "session.json"
    original = session_path.read_bytes()
    mutated = deepcopy(session)
    mutated["source_digest"] = "0" * 64
    session_path.write_bytes(canonical_json_bytes(mutated))
    with pytest.raises(ValueError, match="identity mismatch|source drift"):
        page_resumable_tree_records(artifacts, session["session_id"])
    session_path.write_bytes(original)


def test_resumable_tree_page_facade_and_fastmcp_parity(tmp_path: Path) -> None:
    session, artifacts = _completed_tree(tmp_path)
    arguments = {
        "artifact_root": str(artifacts),
        "session_id": session["session_id"],
        "limit": 1,
    }
    library = page_resumable_tree_records(
        artifacts, session["session_id"], limit=1
    )
    facade = call_mcp_tool("page_resumable_tree_records", arguments)
    fastmcp = fastmcp_page_resumable_tree_records(**arguments).structuredContent

    assert {key: value for key, value in facade.items() if key != "ok"} == library
    assert {key: value for key, value in fastmcp.items() if key != "ok"} == library

    item = library["records"][0]
    resolver_arguments = {
        "artifact_root": str(artifacts),
        "page_token": library["page_token"],
        "index": item["index"],
        "record_sha256": item["record_sha256"],
        "byte_limit": 127,
    }
    resolved = resolve_resumable_tree_record(
        artifacts,
        library["page_token"],
        item["index"],
        record_sha256=item["record_sha256"],
        byte_limit=127,
    )
    resolved_facade = call_mcp_tool(
        "resolve_resumable_tree_record", resolver_arguments
    )
    resolved_fastmcp = fastmcp_resolve_resumable_tree_record(
        **resolver_arguments
    ).structuredContent

    assert {key: value for key, value in resolved_facade.items() if key != "ok"} == resolved
    assert {key: value for key, value in resolved_fastmcp.items() if key != "ok"} == resolved


def test_resumable_tree_page_and_resolver_cli_parity(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    session, artifacts = _completed_tree(tmp_path)
    assert cli_main([
        "page-resumable-tree-records",
        session["session_id"],
        "--artifact-root", str(artifacts),
        "--limit", "1",
    ]) == 0
    page = json.loads(capsys.readouterr().out)
    expected_page = page_resumable_tree_records(
        artifacts, session["session_id"], limit=1
    )
    assert page == expected_page

    item = page["records"][0]
    assert cli_main([
        "resolve-resumable-tree-record",
        page["page_token"],
        str(item["index"]),
        item["record_sha256"],
        "--artifact-root", str(artifacts),
        "--byte-limit", "127",
    ]) == 0
    resolved = json.loads(capsys.readouterr().out)
    expected = resolve_resumable_tree_record(
        artifacts,
        page["page_token"],
        item["index"],
        record_sha256=item["record_sha256"],
        byte_limit=127,
    )
    assert resolved == expected
