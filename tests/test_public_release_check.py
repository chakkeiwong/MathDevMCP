from pathlib import Path

import mathdevmcp.public_release as public_release
from mathdevmcp.public_release import public_release_check
from mathdevmcp.release_policy import release_readiness_report


ROOT = Path(__file__).resolve().parent.parent


def test_public_release_check_passes_product_surface():
    report = public_release_check(ROOT)

    assert report["metadata"] == {"schema_version": "1.0", "contract": "public_release_check"}
    assert report["status"] == "consistent"
    assert report["blockers"] == []
    assert {check["name"] for check in report["checks"]} == {
        "ci_workflow",
        "packaging_metadata",
        "mcp_surface",
        "support_matrix",
        "docs_release_boundary",
        "quality_gate",
        "private_path_leaks",
        "release_report_substance",
    }


def test_public_release_profile_uses_public_surface_gate():
    report = release_readiness_report(ROOT, profile="public")

    assert report["profile"] == "public"
    assert "mcp_surface_consistency" in report["required_capabilities"]
    assert "ci_release_gate" in report["required_capabilities"]
    assert not any(blocker["kind"] == "ci_release_gate_missing" for blocker in report["blockers"])


def test_public_release_check_requires_release_hypothesis_ci_gate():
    report = public_release_check(ROOT)
    ci = next(check for check in report["checks"] if check["name"] == "ci_workflow")

    assert ci["status"] == "consistent"
    assert not any(finding["detail"] == "release-hypothesis-check" for finding in ci["findings"])


def test_public_release_check_enforces_lightweight_base_package():
    report = public_release_check(ROOT)
    packaging = next(check for check in report["checks"] if check["name"] == "packaging_metadata")

    assert packaging["status"] == "consistent"
    assert not any(finding["kind"] == "base_dependencies_not_lightweight" for finding in packaging["findings"])
    assert not any(finding["kind"] == "mcp_extra_missing_runtime_dependency" for finding in packaging["findings"])


def test_public_release_check_rejects_generated_home_path_leaks():
    source = (ROOT / "src" / "mathdevmcp" / "public_release.py").read_text(encoding="utf-8")
    generated = "\n".join(path.read_text(encoding="utf-8") for path in (ROOT / "docs" / "generated" / "release_report").glob("*.txt"))

    assert '"/home/chakwong"' in source
    assert "/home/chakwong" not in generated


def test_public_release_check_propagates_release_report_failure(monkeypatch):
    monkeypatch.setattr(
        public_release,
        "audit_release_report_substance",
        lambda root: {
            "status": "mismatch",
            "findings": [
                {
                    "severity": "high",
                    "kind": "missing_chapter_role",
                    "detail": "Audit a Derivation",
                }
            ],
        },
    )

    report = public_release_check(ROOT)

    assert report["status"] == "mismatch"
    assert any(
        finding["check"] == "release_report_substance"
        and finding["kind"] == "missing_chapter_role"
        for finding in report["blockers"]
    )
