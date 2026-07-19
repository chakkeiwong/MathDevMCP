from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

from mathdevmcp.audit_and_propose_fix import audit_and_propose_fix
from mathdevmcp.cli import main as cli_main
from mathdevmcp.evidence_manifest import canonical_json_bytes
from mathdevmcp.proof_audit_v2 import audit_derivation_v2_for_label
from mathdevmcp.proof_packet import build_proof_packet_label
from mathdevmcp.resumable_audit import (
    build_resumable_audit_fix_result,
    create_resumable_audit_session,
    load_resumable_audit_session,
    load_resumable_audit_label_record,
    ordered_results_from_batch,
    persist_resumable_audit_session,
    run_resumable_label_audits,
    run_session_label_audits,
    validate_resumable_audit_fix_result,
    validate_resumable_audit_session,
)


LABELS = ["eq:first", "eq:second"]


def _fixture(tmp_path: Path) -> tuple[Path, str]:
    source = tmp_path / "document.tex"
    source.write_text(
        r"""
\section{Fixture}
\begin{equation}x = x\label{eq:first}\end{equation}
\begin{equation}y = y\label{eq:second}\end{equation}
""",
        encoding="utf-8",
    )
    return source, hashlib.sha256(source.read_bytes()).hexdigest()


def _session(tmp_path: Path):
    source, digest = _fixture(tmp_path)
    session, index, parser = create_resumable_audit_session(
        tmp_path,
        source.name,
        LABELS,
        source_digest=digest,
    )
    return source, digest, session, index, parser


def _packet_session(tmp_path: Path):
    source, digest = _fixture(tmp_path)
    session, index, parser = create_resumable_audit_session(
        tmp_path,
        source.name,
        LABELS,
        source_digest=digest,
        backend="sympy",
        paragraph_context=False,
        context_before=0,
        context_after=0,
        task_context="general_math_audit",
        summary_only=True,
    )
    return source, digest, session, index, parser


def _producer(tmp_path: Path, digest: str, index: dict, parser: dict):
    return lambda label: audit_derivation_v2_for_label(
        str(tmp_path),
        label,
        paragraph_context=True,
        before=4,
        after=1,
        summary_only=True,
        backend="sympy",
        task_context="symbolic_exposition",
        file="document.tex",
        source_digest=digest,
        index=index,
        parser_policy=parser,
    )


def test_session_identity_is_deterministic_and_persisted(tmp_path: Path) -> None:
    _, digest, session, _, _ = _session(tmp_path)
    second, _, _ = create_resumable_audit_session(
        tmp_path,
        "document.tex",
        LABELS,
        source_digest=digest,
    )
    artifacts = tmp_path / "artifacts"

    persisted = persist_resumable_audit_session(session, artifacts)
    repeated = persist_resumable_audit_session(session, artifacts)
    loaded = load_resumable_audit_session(artifacts, session["session_id"])

    assert second["session_id"] == session["session_id"]
    assert loaded == session
    assert persisted["sha256"] == hashlib.sha256(
        (artifacts / persisted["ref"]).read_bytes()
    ).hexdigest()
    assert repeated == persisted


def test_session_identity_binds_each_projected_parser_policy(tmp_path: Path) -> None:
    _, _, session, _, _ = _session(tmp_path)
    tampered = deepcopy(session)
    tampered["label_parser_policies"][0]["policy"]["status"] = "selected_for_context_only"

    with pytest.raises(ValueError, match="identity mismatch"):
        validate_resumable_audit_session(tampered)


def test_session_options_change_identity_and_mismatched_result_is_rejected(tmp_path: Path) -> None:
    _, digest, session, index, parser = _session(tmp_path)
    changed, _, _ = create_resumable_audit_session(
        tmp_path,
        "document.tex",
        LABELS,
        source_digest=digest,
        paragraph_context=False,
    )
    assert changed["session_id"] != session["session_id"]

    wrong = lambda label: audit_derivation_v2_for_label(
        str(tmp_path),
        label,
        paragraph_context=False,
        summary_only=True,
        backend="sympy",
        file="document.tex",
        source_digest=digest,
        index=index,
        parser_policy=parser,
    )
    with pytest.raises(ValueError, match="audit configuration mismatch"):
        run_resumable_label_audits(session, tmp_path / "wrong-artifacts", wrong, max_new_records=1)


def test_bound_session_runner_uses_exact_configuration(tmp_path: Path) -> None:
    _, _, session, index, parser = _session(tmp_path)
    batch = run_session_label_audits(
        session,
        tmp_path / "artifacts",
        index=index,
        parser_policy=parser,
    )

    assert batch["complete"] is True
    assert all(item["audit_configuration"] == {
        "backend": "sympy",
        "paragraph_context": True,
        "before": 4,
        "after": 1,
        "task_context": "symbolic_exposition",
        "summary_only": True,
        "file": "document.tex",
        "source_digest": session["source_digest"],
        "parser_backends": ["current"],
    } for item in ordered_results_from_batch(batch))


def test_session_identity_binds_context_window(tmp_path: Path) -> None:
    source, digest = _fixture(tmp_path)
    default, _, _ = create_resumable_audit_session(
        tmp_path,
        source.name,
        LABELS,
        source_digest=digest,
    )
    display_only, _, _ = create_resumable_audit_session(
        tmp_path,
        source.name,
        LABELS,
        source_digest=digest,
        context_before=0,
        context_after=0,
    )

    assert default["options"]["before"] == 4
    assert default["options"]["after"] == 1
    assert display_only["options"]["before"] == display_only["options"]["after"] == 0
    assert default["session_id"] != display_only["session_id"]


def test_record_production_failure_does_not_discard_other_labels(tmp_path: Path) -> None:
    _, digest, session, index, parser = _session(tmp_path)
    base = _producer(tmp_path, digest, index, parser)

    def producer(label: str):
        if label == LABELS[0]:
            raise RuntimeError("localized failure")
        return base(label)

    batch = run_resumable_label_audits(session, tmp_path / "artifacts", producer)

    assert batch["failed_count"] == 1
    assert batch["failures"][0]["failure_classification"] == "record_production_failure"
    assert batch["completed_count"] == 1
    assert batch["pending_count"] == 1


def test_quarantined_relation_shape_is_preserved_as_typed_abstention(tmp_path: Path) -> None:
    source = tmp_path / "relation.tex"
    source.write_text(
        r"""\begin{equation}
\{\hbox{printed rows}\}\quad\subset\quad\{\hbox{full system}\}.
\label{eq:subset}
\end{equation}
""",
        encoding="utf-8",
    )
    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    session, index, parser = create_resumable_audit_session(
        tmp_path,
        source.name,
        ["eq:subset"],
        source_digest=digest,
    )
    batch = run_session_label_audits(
        session,
        tmp_path / "artifacts",
        index=index,
        parser_policy=parser,
    )

    assert session["bindings"][0]["binding_type"] == "typed_abstention"
    assert batch["complete"] is True
    assert ordered_results_from_batch(batch)[0]["source_binding_status"] == "source_bound_typed_abstention"


def test_interrupted_batch_resumes_without_recomputing_completed_record(tmp_path: Path) -> None:
    _, digest, session, index, parser = _session(tmp_path)
    artifacts = tmp_path / "artifacts"
    calls: list[str] = []
    base = _producer(tmp_path, digest, index, parser)

    def counted(label: str):
        calls.append(label)
        return base(label)

    first = run_resumable_label_audits(session, artifacts, counted, max_new_records=1)
    second = run_resumable_label_audits(session, artifacts, counted, max_new_records=1)
    third = run_resumable_label_audits(
        session,
        artifacts,
        lambda label: (_ for _ in ()).throw(AssertionError(label)),
    )

    assert first["completed_count"] == 1 and first["pending_count"] == 1
    assert second["complete"] is True and second["produced_count"] == 1 and second["reused_count"] == 1
    assert third["complete"] is True and third["reused_count"] == 2
    assert calls == LABELS
    assert [item["label"] for item in ordered_results_from_batch(third)] == LABELS
    assert canonical_json_bytes(ordered_results_from_batch(third)[0])


def test_source_drift_and_record_tamper_fail_closed(tmp_path: Path) -> None:
    source, digest, session, index, parser = _session(tmp_path)
    artifacts = tmp_path / "artifacts"
    run_resumable_label_audits(
        session,
        artifacts,
        _producer(tmp_path, digest, index, parser),
        max_new_records=1,
    )
    record_path = next((artifacts / "resumable-audits").rglob("000000-*.json"))
    record = json.loads(record_path.read_text(encoding="utf-8"))
    record["label"] = "eq:tampered"
    record_path.write_text(json.dumps(record, sort_keys=True, separators=(",", ":")), encoding="utf-8")

    with pytest.raises(ValueError, match="label mismatch"):
        run_resumable_label_audits(session, artifacts, _producer(tmp_path, digest, index, parser))

    source.write_text(source.read_text(encoding="utf-8") + "\n% drift\n", encoding="utf-8")
    with pytest.raises(ValueError, match="source drift"):
        run_resumable_label_audits(session, artifacts, _producer(tmp_path, digest, index, parser))


def test_precomputed_audits_preserve_audit_fix_semantics(tmp_path: Path) -> None:
    _, digest, session, index, parser = _session(tmp_path)
    uninterrupted = audit_and_propose_fix(
        "Audit fixture",
        root=str(tmp_path),
        labels=LABELS,
        target_file="document.tex",
        source_digest=digest,
        backend="sympy",
        task_context="symbolic_exposition",
        validate_proposed_fixes=False,
    )
    batch = run_resumable_label_audits(
        session,
        tmp_path / "artifacts",
        _producer(tmp_path, digest, index, parser),
    )
    resumed = audit_and_propose_fix(
        "Audit fixture",
        root=str(tmp_path),
        labels=LABELS,
        target_file="document.tex",
        source_digest=digest,
        backend="sympy",
        validate_proposed_fixes=False,
        precomputed_label_audits=ordered_results_from_batch(batch),
    )
    left = uninterrupted["evidence"][0]["low_level"]
    right = resumed["evidence"][0]["low_level"]

    assert right["status"] == left["status"]
    assert right["coverage"]["label_ledger"] == left["coverage"]["label_ledger"]
    assert right["proposal_changes"] == left["proposal_changes"]
    assert right["proposal_details"] == left["proposal_details"]
    assert right["non_claims"] == left["non_claims"]


def test_resumable_aggregate_and_packet_reuse_are_bound_and_tamper_evident(tmp_path: Path) -> None:
    _, _, session, index, parser = _session(tmp_path)
    batch = run_session_label_audits(
        session,
        tmp_path / "artifacts",
        index=index,
        parser_policy=parser,
    )
    aggregate = build_resumable_audit_fix_result(session, batch, "Audit fixture")
    assert validate_resumable_audit_fix_result(aggregate) is aggregate
    provenance = aggregate["evidence"][0]["low_level"]["resumable_evidence"]
    assert provenance["session_id"] == session["session_id"]
    assert len(provenance["record_ids"]) == len(LABELS)

    first = batch["records"][0]
    packet = build_proof_packet_label(
        str(tmp_path),
        LABELS[0],
        file="document.tex",
        source_digest=session["source_digest"],
        summary_only=True,
        index=index,
        resumable_session=session,
        resumable_record=first["record"],
        resumable_record_index=0,
    )
    assert packet["audit_provenance"] == {
        "mode": "reused_validated_checkpoint",
        "record_id": first["record"]["record_id"],
    }

    aggregate["evidence"][0]["low_level"]["proposal_details"].append({"tampered": True})
    with pytest.raises(ValueError, match="semantic result drift"):
        validate_resumable_audit_fix_result(aggregate)


def test_public_packet_checkpoint_selector_reuses_exact_record_without_rebuild(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, _, session, index, parser = _packet_session(tmp_path)
    artifacts = tmp_path / "artifacts"
    persist_resumable_audit_session(session, artifacts)
    batch = run_session_label_audits(session, artifacts, index=index, parser_policy=parser)
    item = batch["records"][0]
    loaded = load_resumable_audit_label_record(
        artifacts, session, 0, item["record"]["record_id"]
    )
    assert loaded == item["record"]

    def forbidden(*args, **kwargs):
        raise AssertionError("checkpoint packet must not rebuild the index or audit")

    monkeypatch.setattr("mathdevmcp.proof_packet.build_index", forbidden)
    monkeypatch.setattr("mathdevmcp.proof_packet.audit_derivation_v2_for_label", forbidden)
    packet = build_proof_packet_label(
        str(tmp_path),
        LABELS[0],
        file="document.tex",
        source_digest=session["source_digest"],
        summary_only=True,
        checkpoint_root=artifacts,
        checkpoint_session_id=session["session_id"],
        checkpoint_record_index=0,
        checkpoint_record_id=item["record"]["record_id"],
    )

    assert packet["proof_audit_v2"] == item["record"]["result"]
    assert packet["audit_provenance"] == {
        "mode": "reused_validated_checkpoint",
        "record_id": item["record"]["record_id"],
    }
    assert packet["dependency_graph"]["nodes"]


def test_public_packet_checkpoint_selector_fails_closed_on_partial_or_wrong_identity(tmp_path: Path) -> None:
    _, _, session, index, parser = _packet_session(tmp_path)
    artifacts = tmp_path / "artifacts"
    persist_resumable_audit_session(session, artifacts)
    batch = run_session_label_audits(session, artifacts, index=index, parser_policy=parser)
    record_id = batch["records"][0]["record"]["record_id"]

    with pytest.raises(ValueError, match="requires root, session, record index, and record ID"):
        build_proof_packet_label(
            str(tmp_path), LABELS[0], checkpoint_root=artifacts
        )
    with pytest.raises(ValueError, match="record identity mismatch"):
        build_proof_packet_label(
            str(tmp_path), LABELS[0], file="document.tex",
            source_digest=session["source_digest"], summary_only=True,
            checkpoint_root=artifacts, checkpoint_session_id=session["session_id"],
            checkpoint_record_index=0, checkpoint_record_id="record_" + "0" * 64,
        )
    with pytest.raises(ValueError, match="checkpoint label"):
        build_proof_packet_label(
            str(tmp_path), LABELS[1], file="document.tex",
            source_digest=session["source_digest"], summary_only=True,
            checkpoint_root=artifacts, checkpoint_session_id=session["session_id"],
            checkpoint_record_index=0, checkpoint_record_id=record_id,
        )

    _, _, legacy_session, legacy_index, legacy_parser = _session(tmp_path)
    legacy_artifacts = tmp_path / "legacy-artifacts"
    persist_resumable_audit_session(legacy_session, legacy_artifacts)
    legacy_batch = run_session_label_audits(
        legacy_session,
        legacy_artifacts,
        index=legacy_index,
        parser_policy=legacy_parser,
    )
    legacy_record_id = legacy_batch["records"][0]["record"]["record_id"]
    with pytest.raises(ValueError, match="audit configuration"):
        build_proof_packet_label(
            str(tmp_path), LABELS[0], file="document.tex",
            source_digest=legacy_session["source_digest"], summary_only=True,
            checkpoint_root=legacy_artifacts,
            checkpoint_session_id=legacy_session["session_id"],
            checkpoint_record_index=0, checkpoint_record_id=legacy_record_id,
        )


def test_current_packet_configuration_checkpoint_has_exact_semantic_parity(tmp_path: Path) -> None:
    source, digest = _fixture(tmp_path)
    session, index, parser = create_resumable_audit_session(
        tmp_path,
        source.name,
        [LABELS[0]],
        source_digest=digest,
        backend="sympy",
        paragraph_context=False,
        context_before=0,
        context_after=0,
        task_context="general_math_audit",
        summary_only=True,
    )
    artifacts = tmp_path / "packet-artifacts"
    persist_resumable_audit_session(session, artifacts)
    batch = run_session_label_audits(
        session, artifacts, index=index, parser_policy=parser
    )
    record = batch["records"][0]["record"]
    arguments = {
        "file": source.name,
        "source_digest": digest,
        "summary_only": True,
    }

    computed = build_proof_packet_label(str(tmp_path), LABELS[0], **arguments)
    reused = build_proof_packet_label(
        str(tmp_path), LABELS[0], **arguments,
        checkpoint_root=artifacts,
        checkpoint_session_id=session["session_id"],
        checkpoint_record_index=0,
        checkpoint_record_id=record["record_id"],
    )

    assert reused["proof_audit_v2"] == computed["proof_audit_v2"]
    assert reused["source"] == computed["source"]
    assert reused["dependency_graph"] == computed["dependency_graph"]
    assert reused["status"] == computed["status"]
    assert reused["actions"] == computed["actions"]
    assert reused["audit_provenance"] == {
        "mode": "reused_validated_checkpoint",
        "record_id": record["record_id"],
    }


def test_cached_proof_and_negative_packet_cli_routes_reuse_exact_record(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source, digest, session, index, parser = _packet_session(tmp_path)
    artifacts = tmp_path / "packet-artifacts"
    persist_resumable_audit_session(session, artifacts)
    batch = run_session_label_audits(
        session, artifacts, index=index, parser_policy=parser
    )
    record = batch["records"][0]["record"]
    selector = [
        "--root", str(tmp_path),
        "--file", source.name,
        "--source-digest", digest,
        "--checkpoint-root", str(artifacts),
        "--checkpoint-session-id", session["session_id"],
        "--checkpoint-record-index", "0",
        "--checkpoint-record-id", record["record_id"],
    ]

    assert cli_main([
        "proof-packet-label", LABELS[0], "--summary-only", *selector
    ]) == 0
    proof = json.loads(capsys.readouterr().out)
    assert proof["audit_provenance"] == {
        "mode": "reused_validated_checkpoint",
        "record_id": record["record_id"],
    }

    assert cli_main(["negative-evidence-label", LABELS[0], *selector]) == 0
    negative = json.loads(capsys.readouterr().out)
    assert negative["audit_provenance"] == proof["audit_provenance"]
    assert negative["evidence"] == proof["proof_audit_v2"]


def test_precomputed_audit_order_mismatch_is_rejected(tmp_path: Path) -> None:
    _, digest, session, index, parser = _session(tmp_path)
    batch = run_resumable_label_audits(
        session,
        tmp_path / "artifacts",
        _producer(tmp_path, digest, index, parser),
    )
    with pytest.raises(ValueError, match="exactly match requested label order"):
        audit_and_propose_fix(
            "Audit fixture",
            root=str(tmp_path),
            labels=LABELS,
            target_file="document.tex",
            source_digest=digest,
            precomputed_label_audits=list(reversed(ordered_results_from_batch(batch))),
        )
