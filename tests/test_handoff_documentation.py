from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
MAINTAINED_DOCS = (
    ROOT / "README.md",
    ROOT / "docs" / "README.md",
    ROOT / "docs" / "mathdevmcp-colleague-quick-start.md",
    ROOT / "docs" / "mathdevmcp-maintainer-guide.md",
    ROOT / "docs" / "mathdevmcp-deployment-guide.md",
    ROOT / "docs" / "mathdevmcp-security-governance.md",
    ROOT / "docs" / "mathdevmcp-support-matrix.md",
    ROOT / "docs" / "mathdevmcp-versioning-policy.md",
)


def test_maintained_document_links_resolve() -> None:
    missing: list[str] = []
    for path in MAINTAINED_DOCS:
        text = path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^]]+\]\(([^)]+)\)", text):
            relative = target.split("#", 1)[0]
            if not relative or "://" in relative or relative.startswith("mailto:"):
                continue
            if not (path.parent / relative).resolve().exists():
                missing.append(f"{path.relative_to(ROOT)} -> {relative}")

    assert missing == []


def test_maintainer_guide_has_executable_handoff_contract() -> None:
    text = (ROOT / "docs" / "mathdevmcp-maintainer-guide.md").read_text(encoding="utf-8")

    for marker in (
        "First 30 Minutes",
        "Architecture And Dependency Direction",
        "Change Recipes",
        "Test Ladder",
        "Release And Rollback",
        "Failure Triage",
        "Known Debt And Escalation",
        "scripts/maintainer_check.sh",
        "scripts/handoff_gate.sh",
        "trusted local",
        "not a sandbox",
    ):
        assert marker in text


def test_fast_and_final_gate_roles_are_not_conflated() -> None:
    fast = (ROOT / "scripts" / "maintainer_check.sh").read_text(encoding="utf-8")
    final = (ROOT / "scripts" / "handoff_gate.sh").read_text(encoding="utf-8")

    assert "This is not the complete regression suite" in fast
    assert 'python -m pytest -q "$ROOT/tests"' not in fast
    assert 'bash "$ROOT/scripts/test_lanes.sh" full' in final
    assert '"$ROOT/scripts/maintainer_check.sh"' in final
    assert "release_claim_ready" in final
    assert "ready_with_caveats" not in final


def test_docs_separate_maintained_guides_from_history() -> None:
    text = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")

    assert "historical programs" in text
    assert "not current" in text
    assert "mathdevmcp-maintainer-guide.md" in text
