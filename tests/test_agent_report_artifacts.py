from __future__ import annotations

import json
from pathlib import Path

import pytest

from mathdevmcp.agent_report_artifacts import (
    AGENT_REPORT_TRANSPORT_BYTES,
    compact_audit_fix_report,
    compact_review_packet,
    compact_rigor_report,
    persist_agent_report,
    resolve_agent_report,
)


def _audit_fix_fixture() -> dict:
    low = {
        "source": {"file": "source.tex", "source_digest": "1" * 64},
        "coverage": {"audited_label_count": 2, "audit_complete": True},
        "proposal_details": [
            {
                "kind": "prove_reconstructed_obligation",
                "target": f"obligation_{index}",
                "label": "eq:test",
                "location": f"source.tex > line {index}",
                "problem": "A scoped proof target remains unverified.",
                "proof_target": f"x_{index} = x_{index}",
                "evidence_ref": f"proof_audit_v2:eq:test:obligation_{index}",
                "evidence_only": True,
            }
            for index in range(20)
        ],
        "validation": {"enabled": False},
    }
    return {
        "status": "diagnostic_only",
        "answer": "A bounded report is available.",
        "evidence": [{"low_level": low}],
        "veto_reasons": [{"code": "unverified"}],
        "assumptions": [],
        "actions": [{"code": "review"}],
        "non_claims": [{"code": "not_proof", "text": "The report is not proof."}],
    }


def test_compact_audit_fix_round_trip_is_bounded_and_lossless(tmp_path: Path) -> None:
    report = _audit_fix_fixture()
    artifact = persist_agent_report(report, tmp_path)
    compact = compact_audit_fix_report(report, artifact)
    resolved = resolve_agent_report(tmp_path, artifact["sha256"])

    assert compact["payload_guardrail"]["status"] == "met"
    assert compact["payload_guardrail"]["canonical_byte_count"] <= AGENT_REPORT_TRANSPORT_BYTES
    assert len(compact["repair_ledger"]) == 20
    assert resolved["report"] == report


def test_compact_rigor_preserves_gap_ledger_and_round_trip(tmp_path: Path) -> None:
    report = {
        "tex_path": "/private/source.tex",
        "coverage": {"status": "partial_coverage", "gap_count": 1},
        "target_selection": {"selected_count": 1, "available_labeled_equation_count": 10, "partial_coverage": True, "targets": [{"label": "eq:test", "line_start": 3, "classification": "identity"}]},
        "gaps": [{"id": "gap:1", "kind": "review", "label": "eq:test", "location": "source.tex > line 3", "problem": "Unverified.", "evidence_ref": "proof:1"}],
        "non_claims": [{"code": "not_proof", "text": "Not proof."}],
    }
    artifact = persist_agent_report(report, tmp_path)
    compact = compact_rigor_report(report, artifact)

    assert compact["source"] == {"file": "source.tex"}
    assert compact["gap_ledger"][0]["id"] == "gap:1"
    assert compact["payload_guardrail"]["status"] == "met"
    assert resolve_agent_report(tmp_path, artifact["sha256"])["report"] == report


def test_agent_report_resolver_rejects_digest_tamper(tmp_path: Path) -> None:
    report = _audit_fix_fixture()
    artifact = persist_agent_report(report, tmp_path)
    path = tmp_path / "agent-reports" / f"{artifact['sha256']}.json"
    path.write_bytes(path.read_bytes() + b" ")

    with pytest.raises(ValueError, match="digest mismatch"):
        resolve_agent_report(tmp_path, artifact["sha256"])


def test_compact_review_packet_preserves_handoff_and_round_trip(tmp_path: Path) -> None:
    report = {
        "status": "diagnostic_only",
        "question": "Review?",
        "answer": "Review evidence.",
        "agent_handoff": {"evidence_ledger": [{"id": "e1"}], "veto_risks": [{"code": "v1"}], "certification_boundary": "Not proof."},
        "veto_reasons": [{"code": "v1"}],
        "assumptions": [],
        "actions": [{"code": "review"}],
        "non_claims": [{"code": "not_proof"}],
    }
    artifact = persist_agent_report(report, tmp_path)
    compact = compact_review_packet(report, artifact)

    assert compact["handoff"] == report["agent_handoff"]
    assert compact["payload_guardrail"]["status"] == "met"
    assert resolve_agent_report(tmp_path, artifact["sha256"])["report"] == report
