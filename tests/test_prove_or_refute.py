import subprocess
import sys
from pathlib import Path

from mathdevmcp.math_debugging import validate_workbench_result
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.prove_or_refute import prove_or_refute


ROOT = Path(__file__).resolve().parent.parent


def test_prove_or_refute_proves_scalar_identity() -> None:
    result = prove_or_refute("a + b = b + a")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "prove_or_refute_result"}
    assert result["status"] == "proved"
    assert result["route_decision"]["status"] == "proved"
    assert validate_workbench_result(result["workbench_result"]) == []


def test_prove_or_refute_refutes_false_identity() -> None:
    result = prove_or_refute("1 + 1 = 3")

    assert result["status"] == "refuted"
    assert result["route_decision"]["status"] == "refuted"


def test_prove_or_refute_refutes_matrix_commutativity_with_counterexample() -> None:
    result = prove_or_refute("A*B = B*A")

    assert result["status"] == "refuted"
    assert result["counterexample_search"]["status"] == "refuted"


def test_prove_or_refute_does_not_refute_opaque_semantic_placeholders() -> None:
    result = prove_or_refute(
        "value_only_filtering_likelihood_proves_hmc_readiness",
        lhs="value_only_likelihood",
        rhs="hmc_production_readiness",
    )

    assert result["status"] == "unknown"
    assert result["counterexample_search"] is None
    assert not result["workbench_result"]["counterexamples"]
    assert result["workbench_result"]["actions"][0]["kind"] == "supply_source_backed_semantic_route"


def test_prove_or_refute_preserves_backend_unavailable_for_lean_without_source() -> None:
    result = prove_or_refute("True = True", backend="lean")

    assert result["status"] == "not_encodable"
    assert result["route_decision"]["route"] == "lean"
    assert result["counterexample_search"]["status"] in {"unknown", "not_encodable"}
    assert result["status"] != "refuted"


def test_prove_or_refute_unknown_is_not_false() -> None:
    result = prove_or_refute("A = A")

    assert result["status"] == "unknown"
    assert "No bounded proof or refutation" in result["reason"]


def test_prove_or_refute_mcp_and_cli_exposure() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    mcp_result = call_mcp_tool("prove_or_refute", {"claim": "1 + 1 = 3"})

    assert "prove_or_refute" in names
    assert mcp_result["ok"] is True
    assert mcp_result["status"] == "refuted"

    cli = subprocess.run(
        [sys.executable, "-m", "mathdevmcp.cli", "prove-or-refute", "a + b = b + a"],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert cli.returncode == 0, cli.stderr
    assert '"contract": "prove_or_refute_result"' in cli.stdout
    assert '"status": "proved"' in cli.stdout
