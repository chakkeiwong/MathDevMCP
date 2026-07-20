from pathlib import Path
import shutil

from mathdevmcp.release_report_audit import audit_release_report_substance


ROOT = Path(__file__).resolve().parent.parent


def _copy_report_inputs(destination: Path) -> None:
    (destination / "docs" / "generated").mkdir(parents=True)
    shutil.copy2(
        ROOT / "docs" / "mathdevmcp-release-report.tex",
        destination / "docs" / "mathdevmcp-release-report.tex",
    )
    shutil.copy2(
        ROOT / "docs" / "mathdevmcp-release-report.pdf",
        destination / "docs" / "mathdevmcp-release-report.pdf",
    )
    shutil.copytree(
        ROOT / "docs" / "generated" / "release_report",
        destination / "docs" / "generated" / "release_report",
    )


def test_release_report_audit_matches_workflow_roles_not_numbers() -> None:
    report = audit_release_report_substance(ROOT)

    assert report["status"] == "consistent"
    assert report["findings"] == []
    assert report["metadata"] == {
        "schema_version": "1.0",
        "contract": "release_report_substance_audit",
    }


def test_release_report_audit_rejects_missing_semantic_workflow(tmp_path: Path) -> None:
    _copy_report_inputs(tmp_path)
    path = tmp_path / "docs" / "mathdevmcp-release-report.tex"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        r"\chapter{Workflow 5: Audit a Derivation}",
        r"\chapter{Workflow 5: Unrelated Material}",
    )
    path.write_text(text, encoding="utf-8")

    report = audit_release_report_substance(tmp_path)

    assert report["status"] == "mismatch"
    assert any(
        finding["kind"] == "missing_chapter_role"
        and finding["detail"] == "Audit a Derivation"
        for finding in report["findings"]
    )
