from __future__ import annotations

import hashlib
from pathlib import Path

from mathdevmcp.document_derivation_tree import audit_document_derivation_tree
from mathdevmcp.evidence_manifest import canonical_json_bytes
from mathdevmcp.resumable_tree import (
    assemble_resumable_tree_result,
    create_resumable_tree_session,
    persist_resumable_tree_session,
    run_resumable_tree_targets,
)


LABELS = ["eq:first", "eq:second"]


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
