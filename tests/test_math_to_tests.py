import ast

from mathdevmcp.math_to_tests import generate_math_tests
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools


def _artifact_by_kind(result: dict, kind: str) -> dict:
    return next(artifact for artifact in result["artifacts"] if artifact["kind"] == kind)


def test_generate_math_tests_symbolic_identity_snippet_parses() -> None:
    result = generate_math_tests("a + b = b + a", assumptions=["a,b are scalars"], kinds=["symbolic_identity"])
    artifact = _artifact_by_kind(result, "symbolic_identity")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "math_test_generation_result"}
    assert artifact["mode"] == "pytest_snippet"
    ast.parse(artifact["code"])
    assert "do not prove" in artifact["diagnostic_boundary"]


def test_generate_math_tests_numeric_fixture_snippet_parses() -> None:
    result = generate_math_tests("x + 1 = 2", numeric_fixtures={"x": 1}, kinds=["numeric_fixture"])
    artifact = _artifact_by_kind(result, "numeric_fixture")

    assert artifact["mode"] == "pytest_snippet"
    assert "'x': 1" in artifact["code"]
    ast.parse(artifact["code"])


def test_generate_math_tests_shape_property_is_plan_only() -> None:
    result = generate_math_tests("A*x = y", kinds=["shape_property"], notation=[{"symbol": "x", "orientation": "column"}])
    artifact = _artifact_by_kind(result, "shape_property")

    assert artifact["mode"] == "plan_only"
    assert artifact["expected_failure_mode"] == "shape_or_orientation_mismatch"
    assert artifact["plan"]


def test_generate_math_tests_finite_difference_is_plan_only() -> None:
    result = generate_math_tests("d f(x) / d x = g(x)", kinds=["finite_difference"])
    artifact = _artifact_by_kind(result, "finite_difference")

    assert artifact["mode"] == "plan_only"
    assert "human review" in " ".join(artifact["plan"])


def test_generate_math_tests_expected_failure_records_mode() -> None:
    result = generate_math_tests("x = x + 1", kinds=["expected_failure"], expected_failure_mode="counterexample_expected")
    artifact = _artifact_by_kind(result, "expected_failure")

    assert artifact["mode"] == "plan_only"
    assert artifact["expected_failure_mode"] == "counterexample_expected"


def test_generate_math_tests_mcp_facade_exposes_workflow() -> None:
    names = {tool["name"] for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "generate_math_tests",
        {"target": "a + b = b + a", "kinds": ["symbolic_identity"]},
    )

    assert "generate_math_tests" in names
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "math_test_generation_result"
    assert result["artifacts"][0]["mode"] == "pytest_snippet"
