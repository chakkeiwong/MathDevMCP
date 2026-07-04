import pytest
import subprocess
import sys
from pathlib import Path

from mathdevmcp.derive_or_refute import derive_or_refute
from mathdevmcp.math_debugging import validate_workbench_result
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools


ROOT = Path(__file__).resolve().parent.parent


def test_derive_or_refute_proves_direct_scalar_identity() -> None:
    result = derive_or_refute("a + b = b + a")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "derive_or_refute_result"}
    assert result["status"] == "proved"
    assert result["route_decision"]["status"] == "proved"
    assert validate_workbench_result(result["workbench_result"]) == []


def test_derive_or_refute_refutes_false_target_with_backend() -> None:
    result = derive_or_refute("1 + 1 = 3")

    assert result["status"] == "refuted"
    assert result["route_decision"]["status"] == "refuted"
    assert result["workbench_result"]["status"] == "refuted"


def test_derive_or_refute_reports_missing_assumptions_before_unknown() -> None:
    result = derive_or_refute("logdet(A) = trace(A)")

    assert result["status"] == "missing_assumptions"
    assert result["assumption_diagnostic"]["missing_assumptions"]
    assert result["route_decision"]["route"] == "human_review"


def test_derive_or_refute_uses_counterexample_fallback_for_matrix_commutativity() -> None:
    result = derive_or_refute("A*B = B*A")

    assert result["status"] == "refuted"
    assert result["counterexample_search"]["status"] == "refuted"
    assert result["workbench_result"]["counterexamples"]


def test_derive_or_refute_does_not_refute_opaque_semantic_placeholders() -> None:
    result = derive_or_refute(
        "affine_recovery_text = uniform_neural_solver_bound",
        givens=["affine recovery text"],
    )

    assert result["status"] == "missing_assumptions"
    assert result["counterexample_search"] is None
    assert not result["workbench_result"]["counterexamples"]
    assert any(action["kind"] == "supply_source_backed_assumptions" for action in result["workbench_result"]["actions"])


def test_derive_or_refute_reports_unknown_without_proof_language_for_no_hit() -> None:
    result = derive_or_refute("A = A")

    assert result["status"] == "unknown"
    assert "proof" not in result["reason"].lower()
    assert result["counterexample_search"]["status"] == "unknown"


def test_derive_or_refute_requires_parseable_target() -> None:
    with pytest.raises(ValueError):
        derive_or_refute("x + y")


def test_derive_or_refute_mcp_facade_exposes_workflow() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool("derive_or_refute", {"target": "a + b = b + a"})

    assert "derive_or_refute" in names
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "derive_or_refute_result"
    assert result["status"] == "proved"


def test_cli_derive_or_refute_reports_contract() -> None:
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "derive-or-refute",
            "1 + 1 = 3",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert '"contract": "derive_or_refute_result"' in result.stdout
    assert '"status": "refuted"' in result.stdout
