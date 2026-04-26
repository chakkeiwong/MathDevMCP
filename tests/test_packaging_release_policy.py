from pathlib import Path
import tomllib

from mathdevmcp.release_policy import release_readiness_report


ROOT = Path(__file__).resolve().parent.parent


def test_optional_dependency_groups_keep_base_package_small():
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    optional = data["project"]["optional-dependencies"]

    assert data["project"]["dependencies"] == []
    assert optional["dev"] == ["pytest"]
    assert "sympy" in optional["symbolic"]
    assert "mcp" in optional["mcp"]
    assert "lean-dojo" in optional["leandojo"]
    assert {"sympy", "mcp", "lean-dojo"}.issubset(set(optional["all"]))


def test_release_readiness_report_records_policy_fields():
    report = release_readiness_report(ROOT)

    assert report["metadata"] == {"schema_version": "1.0", "contract": "release_readiness_report"}
    assert report["package_version"]
    assert report["git_commit"]
    assert report["benchmark_gate"]["summary"]["expected_abstentions"] >= 1
    assert report["schema_version"] == "1.0"
    assert report["status"] in {"ready", "ready_with_caveats", "not_ready"}
