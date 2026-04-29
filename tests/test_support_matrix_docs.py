from pathlib import Path

from mathdevmcp.release_policy import RELEASE_PROFILES


ROOT = Path(__file__).resolve().parent.parent


def test_support_matrix_covers_release_profiles():
    text = (ROOT / "docs" / "mathdevmcp-support-matrix.md").read_text(encoding="utf-8")

    for profile in RELEASE_PROFILES:
        assert profile in text
    for topic in ["MCP", "symbolic", "LeanDojo", "LaTeXML", "private corpus", "public industrial release"]:
        assert topic in text


def test_release_policy_documents_public_boundary():
    text = (ROOT / "docs" / "mathdevmcp-release-policy.md").read_text(encoding="utf-8")

    assert "public industrial release" in text
    assert "`full` profile means every internal optional evidence source" in text
    assert "--profile public" in text

