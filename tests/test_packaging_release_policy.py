from pathlib import Path
import importlib
import tomllib

from mathdevmcp.release_policy import release_readiness_report


ROOT = Path(__file__).resolve().parent.parent


def test_optional_dependency_groups_keep_base_package_small():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    optional = data["project"]["optional-dependencies"]

    assert data["project"]["dependencies"] == []
    names = lambda values: {value.split("=")[0].split("<")[0].split(">")[0] for value in values}
    assert "pytest" in names(optional["dev"])
    assert "build" in names(optional["dev"])
    assert "twine" in names(optional["dev"])
    assert optional["quality"] == ["build", "twine"]
    assert "sympy" in names(optional["symbolic"])
    assert "mcp" in names(optional["mcp"])
    assert "lean-dojo" in names(optional["leandojo"])
    assert {"sympy", "mcp", "lean-dojo", "build", "twine"}.issubset(names(optional["all"]))


def test_declared_python_floor_matches_standard_library_usage_and_ci():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert data["project"]["requires-python"] == ">=3.11"
    assert "Programming Language :: Python :: 3.10" not in data["project"]["classifiers"]
    assert 'python-version: ["3.11", "3.12"]' in workflow


def test_mcp_entrypoint_uses_dependency_aware_launcher():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert data["project"]["scripts"]["mathdevmcp-mcp"] == "mathdevmcp.mcp_entrypoint:main"


def test_release_entrypoints_and_policy_modules_are_present():
    for relative in (
        "src/mathdevmcp/mcp_entrypoint.py",
        "src/mathdevmcp/release_profiles.py",
        "src/mathdevmcp/release_report_audit.py",
        "src/mathdevmcp/backend_protocol.py",
        "src/mathdevmcp/maintainability.py",
        "scripts/handoff_gate.sh",
        "scripts/maintainer_check.sh",
        "scripts/mcp_stdio_smoke.py",
        "LICENSE",
        "CHANGELOG.md",
    ):
        assert (ROOT / relative).is_file(), relative


def test_test_lanes_script_is_executable():
    assert (ROOT / "scripts" / "test_lanes.sh").stat().st_mode & 0o111


def test_mcp_launcher_reports_missing_extra_without_traceback(monkeypatch, capsys):
    launcher = importlib.import_module("mathdevmcp.mcp_entrypoint")

    def missing_mcp(name: str):
        error = ModuleNotFoundError("No module named 'mcp'", name="mcp")
        raise error

    monkeypatch.setattr(launcher.importlib, "import_module", missing_mcp)

    assert launcher.main([]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert "mathdevmcp[mcp]" in captured.err
    assert "ModuleNotFoundError" not in captured.err


def test_mcp_launcher_preflights_named_extra_before_server(monkeypatch):
    launcher = importlib.import_module("mathdevmcp.mcp_entrypoint")
    imports: list[str] = []

    def record_import(name: str):
        imports.append(name)
        if name == "mcp":
            error = ModuleNotFoundError("No module named 'mcp'", name="mcp")
            raise error
        raise AssertionError("server import must not run when the MCP extra is absent")

    monkeypatch.setattr(launcher.importlib, "import_module", record_import)

    assert launcher.main([]) == 2
    assert imports == ["mcp"]


def test_internal_license_and_version_policy_are_present():
    license_text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    policy = (ROOT / "docs" / "mathdevmcp-versioning-policy.md").read_text(encoding="utf-8")

    assert "controlled internal use" in license_text.lower()
    assert "redistribution" in license_text.lower()
    assert "Stable tools" in policy
    assert "Experimental tools" in policy
    assert "Deprecated tools" in policy
    assert "CHANGELOG.md" in policy


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

    assert "release-profile-analysis" in text
    assert "cross-profile release review" in text
    assert "base and public profiles must stay usable" in text
    assert "MCP-facing installs use the optional `[mcp]` extra" in text
    assert "toolchain download failures" in text
    assert "Profile-Scoped Caveats" in text
    assert "does not downgrade a public/base recommendation" in text


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


def test_docs_recommend_release_profile_analysis_for_gap_review():
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "README.md",
            ROOT / "docs" / "mathdevmcp-release-policy.md",
            ROOT / "docs" / "mathdevmcp-maintainer-guide.md",
        ]
    )

    assert "release-profile-analysis" in combined
    assert "what gaps remain" in combined
    assert "strict profile hypotheses" in combined
