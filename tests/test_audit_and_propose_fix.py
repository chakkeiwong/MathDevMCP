from pathlib import Path
import json
import subprocess
import sys

from mathdevmcp.audit_and_propose_fix import (
    audit_and_propose_fix,
    render_audit_fix_markdown,
    write_audit_fix_report_markdown,
)
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import audit_and_propose_fix as mcp_server_audit_and_propose_fix
from mathdevmcp.propose_fix import propose_fix


ROOT = Path(__file__).resolve().parent.parent
DOC_ROOT = ROOT / "docs"
RISKY_DEBT_DOC = DOC_ROOT / "risky-debt-maliar-deep-learning-lecture-note.tex"


def _audit_labels() -> list[str]:
    return ["prop:risky-pricing", "prop:interior-foc"]


def test_audit_and_propose_fix_returns_report_with_markdown_and_tool_uses(tmp_path: Path) -> None:
    output = tmp_path / "risky-debt-audit-fix.md"
    result = audit_and_propose_fix(
        "Audit the risky-debt lecture note and propose repairs",
        root=str(DOC_ROOT),
        labels=_audit_labels(),
        output_path=output,
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_result"}
    assert result["workflow"] == "audit_and_propose_fix"
    assert result["claim_class"] == "fix_report"
    assert result["status"] == "diagnostic_only"
    assert result["evidence"][0]["class"] == "fix_report"
    low_level = result["evidence"][0]["low_level"]
    assert low_level["tool_uses"][0]["tool"] == "audit_derivation_v2_label"
    assert any(item["tool"] == "propose_fix" for item in low_level["tool_uses"])
    assert low_level["markdown"] == output.read_text(encoding="utf-8")
    assert "MathDevMCP Audit And Fix Proposal" in low_level["markdown"]
    assert "## Audit Coverage" in low_level["markdown"]
    assert "Mode: `explicit_labels`" in low_level["markdown"]
    assert "Audited labels: 2 / 2" in low_level["markdown"]
    assert "prop:risky-pricing" in low_level["markdown"]
    assert "### Proposed Fixes" in low_level["markdown"]
    assert "Location:" in low_level["markdown"]
    assert "Problem:" in low_level["markdown"]
    assert "Why:" in low_level["markdown"]
    assert "Proposed fix:" in low_level["markdown"]
    assert "The derivation row is not split into a safe proof obligation." in low_level["markdown"]
    assert "Split the ambiguous derivation row into smaller labeled obligations." in low_level["markdown"]
    assert "Replacement LaTeX:" in low_level["markdown"]
    assert "m(\\bar e)\\frac{d\\bar e}{db'}" in low_level["markdown"]
    assert "Derivation obligation:" in low_level["markdown"]
    assert "Proof target:" in low_level["markdown"]
    assert "Derivation plan:" in low_level["markdown"]
    assert "prove_reconstructed_obligation" in low_level["markdown"]
    assert "Location: `proof_audit_v2_result`" not in low_level["markdown"]
    assert "Formalize the claim or configure a backend before asking for stronger evidence." not in low_level["markdown"]
    assert result["agent_handoff"]["proposal_details"]
    assert "proposed_changes" in result["agent_handoff"]
    assert "audit_fix_report_not_applied_or_certified" in {item["code"] for item in result["non_claims"]}
    assert propose_fix(
        "Propose a repair plan for the risky-debt lecture note",
        evidence=[],
        source={"context_summary": "baseline"},
    )["workflow"] == "propose_fix"


def test_audit_and_propose_fix_mcp_facade_and_server_surface_is_listed(tmp_path: Path) -> None:
    tools = {tool["name"]: tool for tool in list_mcp_tools()}
    output = tmp_path / "risky-debt-audit-fix.md"
    result = call_mcp_tool(
        "audit_and_propose_fix",
        {
            "question": "Audit the risky-debt lecture note and propose repairs",
            "root": str(DOC_ROOT),
            "labels": _audit_labels(),
            "validate_proposed_fixes": True,
            "backend_order": ["lean", "sage", "sympy"],
            "workers": 1,
            "output": str(output),
        },
    )

    assert "audit_and_propose_fix" in tools
    assert tools["audit_and_propose_fix"]["output_contract"] == "high_level_workflow_result"
    assert result["ok"] is True
    assert result["workflow"] == "audit_and_propose_fix"
    assert result["agent_handoff"]["validation"]["enabled"] is True
    assert output.exists()
    assert mcp_server_audit_and_propose_fix(
        "Audit the risky-debt lecture note and propose repairs",
        root=str(DOC_ROOT),
        labels=_audit_labels(),
        validate_proposed_fixes=True,
        backend_order=["lean", "sage", "sympy"],
    )["workflow"] == "audit_and_propose_fix"


def test_audit_and_propose_fix_whole_document_mode_reports_partial_coverage() -> None:
    result = audit_and_propose_fix(
        "Audit the risky-debt lecture note broadly and propose repairs",
        root=str(DOC_ROOT),
        whole_document=True,
        target_file=RISKY_DEBT_DOC.name,
        label_limit=2,
    )
    low_level = result["evidence"][0]["low_level"]
    coverage = low_level["coverage"]

    assert coverage["mode"] == "whole_document"
    assert coverage["target_file"] == RISKY_DEBT_DOC.name
    assert coverage["audited_label_count"] == 2
    assert coverage["discovered_label_count"] > coverage["audited_label_count"]
    assert coverage["skipped_label_count"] == coverage["discovered_label_count"] - 2
    assert coverage["audit_complete"] is False
    assert [item["label"] for item in coverage["audited_labels"]] == ["eq:ar1-shock", "eq:investment-law"]
    assert "Audited labels: 2 /" in low_level["markdown"]
    assert "Complete for selected scope: False" in low_level["markdown"]
    assert f"Target file: `{RISKY_DEBT_DOC.name}`" in low_level["markdown"]


def test_audit_and_propose_fix_whole_document_demotes_non_concrete_actions() -> None:
    result = audit_and_propose_fix(
        "Audit the risky-debt lecture note broadly and propose repairs",
        root=str(DOC_ROOT),
        whole_document=True,
        target_file=RISKY_DEBT_DOC.name,
        label_limit=2,
    )
    markdown = result["evidence"][0]["low_level"]["markdown"]
    proposed_changes = markdown.split("## Proposed Changes", 1)[1].split("### Proposed Fixes", 1)[0]
    proposed_fixes = markdown.split("### Proposed Fixes", 1)[1].split("## Evidence Gaps", 1)[0]
    evidence_gaps = markdown.split("## Evidence Gaps", 1)[1].split("## Next Actions", 1)[0]

    assert "`add_or_verify_assumption`" not in proposed_changes
    assert "`add_review_boundary`" not in proposed_changes
    assert "`add_or_verify_assumption`" not in proposed_fixes
    assert "`add_review_boundary`" not in proposed_fixes
    assert "State or verify the missing constraint" not in proposed_fixes
    assert "Add a local review boundary" not in proposed_fixes
    assert "`split_derivation_step`" in proposed_fixes
    assert "`concretize_before_fix`" in evidence_gaps
    assert "Do not edit the document from this item alone." in evidence_gaps


def test_audit_and_propose_fix_cli_writes_markdown_report(tmp_path: Path) -> None:
    output = tmp_path / "audit-fix.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-and-propose-fix",
            "Audit the risky-debt lecture note and propose repairs",
            "--root",
            str(DOC_ROOT),
            "--label",
            "prop:risky-pricing",
            "--label",
            "prop:interior-foc",
            "--whole-document",
            "--file",
            RISKY_DEBT_DOC.name,
            "--label-limit",
            "1",
            "--validate-proposed-fixes",
            "--validation-backend",
            "lean",
            "--validation-backend",
            "sage",
            "--validation-backend",
            "sympy",
            "--workers",
            "2",
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["workflow"] == "audit_and_propose_fix"
    assert payload["agent_handoff"]["coverage"]["mode"] == "whole_document_plus_explicit_labels"
    assert payload["agent_handoff"]["validation"]["enabled"] is True
    assert output.exists()
    markdown = output.read_text(encoding="utf-8")
    assert "MathDevMCP Audit And Fix Proposal" in markdown
    assert "## Audit Coverage" in markdown
    assert "## Proposed Fix Validation" in markdown


def test_render_audit_fix_markdown_contains_tool_use_table() -> None:
    report = audit_and_propose_fix(
        "Audit the risky-debt lecture note and propose repairs",
        root=str(DOC_ROOT),
        labels=_audit_labels(),
    )
    markdown = render_audit_fix_markdown(report["evidence"][0]["low_level"])

    assert "| Tool | Purpose | Status | Output contract | Arguments |" in markdown
    assert "propose_fix" in markdown
    assert "### Proposed Fixes" in markdown
    assert "## Evidence Gaps" in markdown
    assert "Problem:" in markdown
    assert "Proposed fix:" in markdown
    assert "Proof target:" in markdown
    assert "Derivation plan:" in markdown


def test_audit_and_propose_fix_reconstructs_concrete_foc_math_for_split_row() -> None:
    result = audit_and_propose_fix(
        "Audit the risky-debt lecture note and propose repairs",
        root=str(DOC_ROOT),
        labels=["prop:interior-foc"],
    )
    details = result["agent_handoff"]["proposal_details"]
    foc_b = next(item for item in details if item["target"] == "obligation_5")

    assert foc_b["location"].endswith("line 782")
    assert foc_b["math_fix"]["equation"] == "0 = m(\\bar e)\\frac{d\\bar e}{db'}\n  +\\beta \\E[V^\\star_b(k',b',z')\\mid z]"
    assert "\\begin{equation}" in foc_b["math_fix"]["replacement_latex"]
    assert "Differentiate the local objective" in foc_b["math_fix"]["derivation_obligation"]


def test_audit_and_propose_fix_replaces_generic_evidence_gap_with_concrete_obligations() -> None:
    result = audit_and_propose_fix(
        "Audit the risky-debt lecture note and propose repairs",
        root=str(DOC_ROOT),
        labels=_audit_labels(),
    )
    details = result["agent_handoff"]["proposal_details"]
    gaps = [item for item in details if item.get("kind") == "prove_reconstructed_obligation"]

    assert len(gaps) == 3
    assert {item["target"] for item in gaps} == {"obligation_2", "obligation_3", "obligation_5"}
    assert all("proof_audit_v2_result" not in item["location"] for item in gaps)
    assert all(item["proof_target"] for item in gaps)
    assert any("zero-profit condition" in item["derivation_plan"] for item in gaps)
    assert any("\\partial J/\\partial b'=0" in item["derivation_plan"] for item in gaps)
    assert all(item["evidence_ref"].startswith("proof_audit_v2:") for item in gaps)


def test_audit_and_propose_fix_validates_concrete_fixes_with_backend_attempts() -> None:
    result = audit_and_propose_fix(
        "Audit the risky-debt lecture note and propose repairs",
        root=str(DOC_ROOT),
        labels=_audit_labels(),
        validate_proposed_fixes=True,
        backend_order=["lean", "sage", "sympy"],
    )
    low_level = result["evidence"][0]["low_level"]
    concrete = [item for item in result["agent_handoff"]["proposal_details"] if not item.get("evidence_only") and item.get("math_fix")]

    assert low_level["validation"]["enabled"] is True
    assert low_level["validation"]["validated_detail_count"] >= len(concrete)
    assert "## Proposed Fix Validation" in low_level["markdown"]
    assert concrete
    for item in concrete:
        validation = item["validation"]
        assert validation["policy"] == "require_attempt_when_encodable"
        assert validation["backend_order"] == ["lean", "sage", "sympy"]
        assert validation["status"] in {"attempted_not_certified", "not_encodable", "verified", "refuted"}
        assert validation["reason"]
        attempts = validation["backend_attempts"]
        assert [attempt["backend"] for attempt in attempts] == ["lean", "sage", "sympy"]
        lean_attempt = attempts[0]
        sage_attempt = attempts[1]
        assert lean_attempt["status"] == "not_encodable"
        assert "does not synthesize Lean proof scripts" in lean_attempt["reason"]
        assert sage_attempt["severity"] == "diagnostic"
        assert "attempted only" in sage_attempt["reason"]
    assert "Validation:" in low_level["markdown"]
    assert "Backend attempts:" in low_level["markdown"]


def test_audit_and_propose_fix_parallel_workers_preserve_label_order() -> None:
    sequential = audit_and_propose_fix(
        "Audit the risky-debt lecture note and propose repairs",
        root=str(DOC_ROOT),
        labels=_audit_labels(),
        validate_proposed_fixes=True,
        workers=1,
    )
    parallel = audit_and_propose_fix(
        "Audit the risky-debt lecture note and propose repairs",
        root=str(DOC_ROOT),
        labels=_audit_labels(),
        validate_proposed_fixes=True,
        workers=2,
    )

    seq_low = sequential["evidence"][0]["low_level"]
    par_low = parallel["evidence"][0]["low_level"]
    assert [item["label"] for item in seq_low["coverage"]["audited_labels"]] == [item["label"] for item in par_low["coverage"]["audited_labels"]]
    assert [item["label"] for item in seq_low["audited_evidence"]] == [item["label"] for item in par_low["audited_evidence"]]
    assert [item["tool"] for item in seq_low["tool_uses"]] == [item["tool"] for item in par_low["tool_uses"]]
    assert [item["target"] for item in sequential["agent_handoff"]["proposal_details"]] == [item["target"] for item in parallel["agent_handoff"]["proposal_details"]]


def test_write_audit_fix_report_markdown_returns_written_path(tmp_path: Path) -> None:
    output = tmp_path / "fix-report.md"
    result = write_audit_fix_report_markdown(
        "Audit the risky-debt lecture note and propose repairs",
        output,
        root=str(DOC_ROOT),
        labels=_audit_labels(),
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "audit_fix_report_markdown"}
    assert Path(result["output"]).read_text(encoding="utf-8").startswith("# MathDevMCP Audit And Fix Proposal")


def test_build_audit_fix_report_prefers_evidence_ref_label_when_obligation_ids_collide() -> None:
    evidence = [
        {
            "label": "label:a",
            "status": "inconclusive",
            "reason": "label a reason",
            "obligations": [
                {
                    "id": "obligation_2",
                    "label": "label:a",
                    "reason": "wrong obligation chosen",
                    "source_text": "wrong source text",
                    "provenance": {
                        "file": "doc-a.tex",
                        "line_start": 10,
                        "section_path": ["Section A"],
                    },
                }
            ],
            "metadata": {"contract": "proof_audit_v2_result"},
        },
        {
            "label": "label:b",
            "status": "inconclusive",
            "reason": "label b reason",
            "obligations": [
                {
                    "id": "obligation_2",
                    "label": "label:b",
                    "reason": "right obligation chosen",
                    "source_text": "right source text",
                    "provenance": {
                        "file": "doc-b.tex",
                        "line_start": 42,
                        "section_path": ["Section B"],
                    },
                }
            ],
            "metadata": {"contract": "proof_audit_v2_result"},
        },
    ]
    report = {
        "question": "Synthetic collision regression",
        "status": "proposal_ready",
        "certification_boundary": "diagnostic only",
        "tool_uses": [],
        "audited_evidence": evidence,
        "proposal_changes": [
            {
                "kind": "split_derivation_step",
                "target": "obligation_2",
                    "summary": "Split the ambiguous derivation row into smaller labeled obligations.",
                    "rationale": "The derivation row was not split into a safe proof obligation.",
                    "evidence_refs": ["proof_audit_v2:label:b:obligation_2"],
                    "math_fix": {
                        "equation": "x = y",
                        "replacement_latex": "\\begin{equation}\n  x = y\n\\end{equation}",
                    },
                }
            ],
        "non_claims": [],
        "next_actions": [],
    }
    markdown = render_audit_fix_markdown(report)

    assert "doc-b.tex > Section B > line 42" in markdown
    assert "doc-a.tex > Section A > line 10" not in markdown
