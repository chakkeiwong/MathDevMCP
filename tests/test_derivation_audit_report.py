from pathlib import Path
import subprocess
import sys

from mathdevmcp.derivation_audit_report import audit_and_propose_derivations


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"
ROOT = Path(__file__).resolve().parent.parent


def test_audit_and_propose_derivations_writes_direct_markdown(tmp_path: Path) -> None:
    output = tmp_path / "derivations.md"
    result = audit_and_propose_derivations(
        "Audit a direct matrix derivation",
        target="logdet(A) = trace(A)",
        output_path=output,
    )

    markdown = output.read_text(encoding="utf-8")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "derivation_audit_report_result"}
    assert result["status"] == "proposal_ready"
    assert result["coverage"]["gap_count"] == 1
    assert result["tool_uses"][0]["tool"] == "plan_backend_routes"
    assert result["tool_uses"][1]["tool"] == "derive_or_refute"
    assert result["route_plans"][0]["metadata"]["contract"] == "backend_route_plan_result"
    assert result["proposals"][0]["type"] == "add_assumptions"
    assert result["proposals"][0]["assumption_repairs"]
    assert "Location:" in markdown
    assert "Problem:" in markdown
    assert "Why:" in markdown
    assert "Proposed fix:" in markdown
    assert "Derivation route:" in markdown
    assert "Backend plan:" in markdown
    assert "Linked assumption repairs:" in markdown
    assert "Possible sufficient assumption sets:" in markdown
    assert "How the derivation works under the assumptions:" in markdown
    assert "collect more evidence" not in markdown.lower()


def test_audit_and_propose_derivations_uses_label_location(tmp_path: Path) -> None:
    output = tmp_path / "label-report.md"
    result = audit_and_propose_derivations(
        "Audit fixture label",
        root=str(FIXTURES),
        labels=["prop:transport-logdet"],
        output_path=output,
    )

    markdown = output.read_text(encoding="utf-8")

    assert result["status"] == "proposal_ready"
    assert result["tool_uses"][0]["tool"] == "build_index"
    assert result["tool_uses"][1]["tool"] == "extract_derivation_targets_for_label"
    assert result["tool_uses"][2]["tool"] == "plan_backend_routes"
    assert result["coverage"]["fallback_target_count"] == 1
    assert result["target_extraction"]["label_results"][0]["status"] == "fallback_used"
    assert result["gaps"][0]["location"].startswith("doc_consistency_good.tex > prop:transport-logdet > line")
    assert "prop:transport-logdet" in markdown
    assert "Extraction status: `fallback_full_block`" in markdown
    assert "Backend Route Plans" in markdown
    assert "Evidence refs:" in markdown


def test_audit_and_propose_derivations_uses_extracted_risky_debt_obligations(tmp_path: Path) -> None:
    output = tmp_path / "risky-debt-extracted.md"
    result = audit_and_propose_derivations(
        "Audit risky-debt extracted obligations",
        root=str(ROOT / "docs"),
        labels=["prop:risky-pricing", "prop:interior-foc"],
        output_path=output,
    )

    markdown = output.read_text(encoding="utf-8")

    assert result["status"] == "proposal_ready"
    assert result["coverage"]["target_count"] == 3
    assert result["coverage"]["label_count"] == 2
    assert result["coverage"]["extracted_target_count"] == 3
    assert result["coverage"]["fallback_target_count"] == 0
    assert [target["label"] for item in result["target_extraction"]["label_results"] for target in item["targets"]] == [
        "eq:risky-pricing",
        "eq:foc-k",
        "eq:foc-b",
    ]
    assert [target_result["source"]["parent_label"] for target_result in result["target_results"]] == [
        "prop:risky-pricing",
        "prop:interior-foc",
        "prop:interior-foc",
    ]
    assert [target_result["source"]["label"] for target_result in result["target_results"]] == [
        "eq:risky-pricing",
        "eq:foc-k",
        "eq:foc-b",
    ]
    assert result["route_plans"][0]["source"]["label"] == "eq:risky-pricing"
    assert result["route_plans"][1]["source"]["label"] == "eq:foc-k"
    assert all(plan["metadata"]["contract"] == "backend_route_plan_result" for plan in result["route_plans"])
    assert "Parent Label: `prop:risky-pricing`" in markdown
    assert "Target: `eq:foc-k`" in markdown
    assert "risky-debt-maliar-deep-learning-lecture-note.tex > prop:interior-foc > eq:foc-b > line 781" in markdown
    assert "Backend Route Plans" in markdown
    assert "`lean`" in markdown
    assert "Route planning is diagnostic only" in markdown


def test_audit_and_propose_derivations_reports_missing_label_coverage_gap() -> None:
    result = audit_and_propose_derivations(
        "Audit missing label",
        root=str(FIXTURES),
        labels=["prop:not-present"],
    )

    assert result["status"] == "needs_evidence"
    assert result["coverage"]["target_count"] == 0
    assert result["coverage"]["coverage_gaps"] == [
        f"Label `prop:not-present` was not found under `{FIXTURES}`."
    ]
    assert result["proposals"] == []


def test_audit_and_propose_derivations_preserves_certifying_boundary(tmp_path: Path) -> None:
    output = tmp_path / "proved.md"
    result = audit_and_propose_derivations(
        "Audit proved target",
        target="a + b = b + a",
        output_path=output,
    )

    markdown = output.read_text(encoding="utf-8")

    assert result["proposals"][0]["type"] == "accept_backend_certificate"
    assert result["validation"]["certifying_proposal_count"] == 1
    assert "certifying backend" in markdown
    assert "does not apply edits" in markdown


def test_cli_audit_and_propose_derivations_writes_markdown(tmp_path: Path) -> None:
    output = tmp_path / "cli-derivations.md"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-and-propose-derivations",
            "Audit direct derivation",
            "--target",
            "logdet(A) = trace(A)",
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "derivation_audit_report_result"' in result.stdout
    assert '"status": "proposal_ready"' in result.stdout
    assert output.exists()
    assert "Linked assumption repairs:" in output.read_text(encoding="utf-8")
