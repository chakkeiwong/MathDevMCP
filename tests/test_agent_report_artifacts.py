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
    assert compact["payload_guardrail"]["canonical_byte_count"] == len(
        json.dumps(compact, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )
    assert len(compact["repair_ledger"]) == 20
    assert resolved["report"] == report


def test_compact_audit_fix_truncates_preview_but_resolves_full_report(tmp_path: Path) -> None:
    report = _audit_fix_fixture()
    details = report["evidence"][0]["low_level"]["proposal_details"]
    report["evidence"][0]["low_level"]["proposal_details"] = [
        {**details[index % len(details)], "problem": "long diagnostic " + "x" * 1000 + str(index)}
        for index in range(200)
    ]
    artifact = persist_agent_report(report, tmp_path)

    compact = compact_audit_fix_report(report, artifact)

    assert compact["repair_ledger_truncated"] is True
    assert compact["repair_ledger_total_count"] == 200
    assert len(compact["repair_ledger"]) < 200
    assert compact["payload_guardrail"]["status"] == "met"
    assert resolve_agent_report(tmp_path, artifact["sha256"])["report"] == report


def test_compact_audit_fix_summarizes_large_coverage_ledger(tmp_path: Path) -> None:
    report = _audit_fix_fixture()
    report["evidence"][0]["low_level"]["coverage"] = {
        "mode": "explicit_labels",
        "target_file": "source.tex",
        "audited_label_count": 200,
        "skipped_label_count": 0,
        "audit_complete": True,
        "audited_labels": [
            {"label": f"eq:{index}", "canonical_target": {"payload": "x" * 1000}}
            for index in range(200)
        ],
    }
    artifact = persist_agent_report(report, tmp_path)

    compact = compact_audit_fix_report(report, artifact)

    assert compact["coverage"]["audited_label_count"] == 200
    assert len(compact["coverage"]["audited_label_preview"]) == 20
    assert compact["coverage"]["audited_label_preview_truncated"] is True
    assert compact["payload_guardrail"]["status"] == "met"


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


def test_compact_rigor_preserves_semantic_issues_and_actionable_proposals(tmp_path: Path) -> None:
    issue = {
        "issue_id": "eq:test/matrix-domain-and-neumann-convergence",
        "label": "eq:test",
        "family": "matrix-domain-and-neumann-convergence",
        "status": "unresolved",
        "roles": ["definition", "conditional_identity"],
        "unresolved_obligations": ["neumann_convergence"],
        "candidate_patch": "Assume rho(Omega) < 1.",
        "patch_class": "candidate_exposition_patch_not_certificate",
        "math_nonclaim": "This is not a proof certificate.",
    }
    proposal = {
        "id": "proposal:1",
        "issue_id": issue["issue_id"],
        "status": "actionable_assumption_text",
        "candidate_patch": issue["candidate_patch"],
    }
    report = {
        "tex_path": "/private/source.tex",
        "coverage": {"status": "selected_scope_complete", "gap_count": 1},
        "target_selection": {"selected_count": 1, "targets": []},
        "issues": [issue],
        "proposals": [proposal, {"id": "diagnostic:1", "status": "diagnostic_only"}],
        "gaps": [],
        "non_claims": ["Not proof."],
    }
    artifact = persist_agent_report(report, tmp_path)

    compact = compact_rigor_report(report, artifact)

    assert compact["issue_ledger"] == [issue]
    assert compact["issue_ledger_total_count"] == 1
    assert compact["issue_ledger_truncated"] is False
    assert compact["actionable_proposals"] == [proposal]
    assert compact["actionable_proposal_total_count"] == 1
    assert compact["actionable_proposals_truncated"] is False
    assert resolve_agent_report(tmp_path, artifact["sha256"])["report"] == report


def test_compact_rigor_bounds_large_semantic_ledgers(tmp_path: Path) -> None:
    reports = [
        {
            "issue_id": f"eq:{index}/formalization",
            "label": f"eq:{index}",
            "family": "formalization-and-source-role",
            "status": "needs_formalization",
            "candidate_patch": "x" * 2000,
        }
        for index in range(200)
    ]
    report = {
        "tex_path": "/private/source.tex",
        "coverage": {"status": "selected_scope_complete", "gap_count": 200},
        "target_selection": {"selected_count": 200, "targets": []},
        "issues": reports,
        "proposals": [
            {
                "id": f"proposal:{index}",
                "status": "actionable_assumption_text",
                "candidate_patch": "y" * 2000,
            }
            for index in range(200)
        ],
        "gaps": [],
        "non_claims": ["Not proof."],
    }
    artifact = persist_agent_report(report, tmp_path)

    compact = compact_rigor_report(report, artifact)

    assert compact["payload_guardrail"]["status"] == "met"
    assert compact["issue_ledger_total_count"] == 200
    assert compact["actionable_proposal_total_count"] == 200
    assert compact["issue_ledger_truncated"] or compact["actionable_proposals_truncated"]


def test_compact_rigor_truncates_large_target_and_gap_previews(tmp_path: Path) -> None:
    report = {
        "tex_path": "/private/source.tex",
        "coverage": {"status": "selected_scope_complete", "gap_count": 200},
        "target_selection": {
            "selected_count": 200,
            "available_labeled_equation_count": 200,
            "partial_coverage": False,
            "targets": [
                {
                    "label": f"eq:{index}",
                    "line_start": index + 1,
                    "line_end": index + 1,
                    "normalized_target": {"kind": "equality"},
                    "routing_role": {"role": "definition", "authority": "source_evidenced_role"},
                    "obligation_id": f"obl_{index}",
                    "obligation_digest": "d" * 64,
                    "local_obligations": [{"id": f"local_{index}_{j}"} for j in range(10)],
                    "downstream_integration_obligations": [{"id": f"downstream_{index}_{j}"} for j in range(10)],
                }
                for index in range(200)
            ],
        },
        "gaps": [
            {
                "id": f"gap:{index}",
                "kind": "review",
                "label": f"eq:{index}",
                "location": "source.tex > " + "x" * 500,
                "problem": "Unverified " + "y" * 500,
            }
            for index in range(200)
        ],
        "non_claims": [{"code": "not_proof", "text": "Not proof."}],
    }
    artifact = persist_agent_report(report, tmp_path)

    compact = compact_rigor_report(report, artifact)

    assert compact["target_selection"]["target_total_count"] == 200
    assert compact["gap_ledger_total_count"] == 200
    assert compact["target_selection"]["target_preview_truncated"] or compact["gap_ledger_truncated"]
    assert compact["payload_guardrail"]["status"] == "met"
    assert compact["payload_guardrail"]["canonical_byte_count"] == len(
        json.dumps(compact, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    )
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
