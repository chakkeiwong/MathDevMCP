from pathlib import Path
import json
import subprocess
import sys

from mathdevmcp.high_level_contracts import validate_high_level_result
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import propose_fix as mcp_server_propose_fix
from mathdevmcp.propose_fix import propose_fix


ROOT = Path(__file__).resolve().parent.parent
DOC_ROOT = ROOT / "docs"
RISKY_DEBT_DOC = DOC_ROOT / "risky-debt-maliar-deep-learning-lecture-note.tex"


def _risky_debt_evidence() -> list[dict]:
    derived = call_mcp_tool(
        "audit_derivation_v2_label",
        {"root": str(DOC_ROOT), "label": "prop:risky-pricing", "paragraph_context": True, "summary_only": True},
    )
    foc = call_mcp_tool(
        "audit_derivation_v2_label",
        {"root": str(DOC_ROOT), "label": "prop:interior-foc", "paragraph_context": True, "summary_only": True},
    )
    return [derived, foc]


def test_propose_fix_returns_actionable_repair_plan_from_risky_debt_evidence() -> None:
    result = propose_fix(
        "Propose a repair plan for the risky-debt lecture note",
        evidence=_risky_debt_evidence(),
        source={"context_summary": "Risky-debt note repair guidance."},
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_result"}
    assert result["workflow"] == "propose_fix"
    assert result["status"] == "diagnostic_only"
    assert result["certification_source"] == "none"
    assert validate_high_level_result(result) == []
    kinds = {item["kind"] for item in result["evidence"][0]["low_level"]["proposed_changes"]}
    assert "split_derivation_step" in kinds
    assert "add_or_verify_assumption" not in kinds
    assert "fix_proposal_not_applied_or_verified" in {item["code"] for item in result["non_claims"]}
    assert "proposed_changes" in result["agent_handoff"]
    assert result["agent_handoff"]["proposed_changes"]


def test_propose_fix_mcp_facade_and_server_surface_is_listed() -> None:
    tools = {tool["name"]: tool for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "propose_fix",
        {
            "question": "Propose a repair plan for the risky-debt lecture note",
            "evidence": _risky_debt_evidence(),
            "source": {"context_summary": "Risky-debt note repair guidance."},
        },
    )

    assert "propose_fix" in tools
    assert tools["propose_fix"]["output_contract"] == "high_level_workflow_result"
    assert tools["propose_fix"]["certifying_capable"] is False
    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_result"}
    assert result["workflow"] == "propose_fix"
    assert mcp_server_propose_fix(
        "Propose a repair plan for the risky-debt lecture note",
        evidence=_risky_debt_evidence(),
        source={"context_summary": "Risky-debt note repair guidance."},
    )["workflow"] == "propose_fix"


def test_propose_fix_cli_returns_compact_handoff(tmp_path: Path) -> None:
    evidence_path = tmp_path / "propose_fix_evidence.json"
    evidence_path.write_text(json.dumps(_risky_debt_evidence()), encoding="utf-8")

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "propose-fix",
            "Propose a repair plan for the risky-debt lecture note",
            "--evidence",
            str(evidence_path),
            "--source",
            '{"context_summary":"Risky-debt note repair guidance."}',
            "--handoff",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["scoped_question"] == "Propose a repair plan for the risky-debt lecture note"
    assert payload["proposed_changes"]
    assert "not applied edits" in payload["certification_boundary"]
