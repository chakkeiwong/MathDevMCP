from pathlib import Path
import tomllib


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
