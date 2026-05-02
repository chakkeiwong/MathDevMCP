from pathlib import Path
import tomllib

from mathdevmcp.release_policy import release_readiness_report


ROOT = Path(__file__).resolve().parent.parent


def test_optional_dependency_groups_keep_base_package_small():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    optional = data["project"]["optional-dependencies"]

    assert data["project"]["dependencies"] == []
    assert "pytest" in optional["dev"]
    assert "build" in optional["dev"]
    assert "twine" in optional["dev"]
    assert optional["quality"] == ["build", "twine"]
    assert "sympy" in optional["symbolic"]
    assert "mcp" in optional["mcp"]
    assert "lean-dojo" in optional["leandojo"]
    assert {"sympy", "mcp", "lean-dojo", "build", "twine"}.issubset(set(optional["all"]))


def test_docs_explain_optional_mcp_runtime_policy():
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "README.md",
            ROOT / "mcp" / "README.md",
            ROOT / "docs" / "mathdevmcp-deployment-guide.md",
            ROOT / "docs" / "mathdevmcp-support-matrix.md",
        ]
    )

    assert "base package intentionally has no required runtime dependencies" in combined
    assert "[mcp]" in combined
    assert "mathdevmcp-mcp" in combined


def test_support_matrix_documents_backend_profile_boundary():
    text = (ROOT / "docs" / "mathdevmcp-support-matrix.md").read_text(encoding="utf-8")

    assert "base and public profiles must stay usable" in text
    assert "MCP-facing installs use the optional `[mcp]` extra" in text
    assert "toolchain download failures" in text


def test_release_readiness_report_records_policy_fields():
    report = release_readiness_report(ROOT)

    assert report["metadata"] == {"schema_version": "1.0", "contract": "release_readiness_report"}
    assert report["package_version"]
    assert report["git_commit"]
    assert report["benchmark_gate"]["summary"]["expected_abstentions"] >= 1
    assert report["schema_version"] == "1.0"
    assert report["status"] in {"ready", "ready_with_caveats", "not_ready"}


def test_public_profile_is_available_and_distinct_from_full():
    report = release_readiness_report(ROOT, profile="public")

    assert report["profile"] == "public"
    assert "ci_release_gate" in report["required_capabilities"]
    assert "private_corpus_manifest" in report["optional_capabilities"]
