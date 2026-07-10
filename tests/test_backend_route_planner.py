from mathdevmcp.backend_route_planner import BACKEND_ROUTE_PLAN_BOUNDARY, plan_backend_routes


CAPABILITIES = {
    "sympy": {"available": True, "status": "available", "path": "/python", "version": "test"},
    "sage": {"available": False, "status": "unavailable", "path": None, "version": None},
    "lean": {"available": False, "status": "unavailable", "path": None, "version": None},
}


def test_route_planner_scalar_identity_prefers_symbolic_without_certifying() -> None:
    result = plan_backend_routes("a + b = b + a", capabilities=CAPABILITIES)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "backend_route_plan_result"}
    assert result["status"] == "planned"
    assert result["selected_route"]["backend"] == "sympy"
    assert result["selected_route"]["status"] == "ready_to_attempt"
    assert result["selected_route"]["tool"] == "derive_or_refute"
    assert result["selected_route"]["evidence_contract"] == "derive_or_refute_result"
    assert result["candidates"][1]["backend"] == "bounded_counterexample"
    assert result["external_tool_first_plan"]["metadata"]["contract"] == "external_tool_first_plan_result"
    assert result["external_tool_first_plan"]["selected_external_tools"][0]["tool"] == "sympy"
    assert result["boundary"] == BACKEND_ROUTE_PLAN_BOUNDARY
    assert "route_plan_not_certificate" in {item["code"] for item in result["non_claims"]}


def test_route_planner_matrix_counterexample_and_sage_diagnostic() -> None:
    result = plan_backend_routes("A*B = B*A", capabilities=CAPABILITIES)

    by_backend = {candidate["backend"]: candidate for candidate in result["candidates"]}
    assert result["selected_route"]["backend"] == "bounded_counterexample"
    assert by_backend["sympy"]["status"] == "not_applicable"
    assert by_backend["bounded_counterexample"]["status"] == "ready_to_attempt"
    assert by_backend["bounded_counterexample"]["tool"] == "find_counterexample"
    assert by_backend["sage"]["status"] == "unavailable"
    assert "Sage could help" in by_backend["sage"]["reason"]
    assert result["diagnostics"]["unavailable_count"] >= 1


def test_route_planner_risky_debt_target_requires_formalization() -> None:
    target = {
        "target": "0 = m(\\bar e)\\frac{d\\bar e}{dk'} +\\beta \\E[V^\\star_k(k',b',z')\\mid z]",
        "lhs": "0",
        "rhs": "m(\\bar e)\\frac{d\\bar e}{dk'} +\\beta \\E[V^\\star_k(k',b',z')\\mid z]",
    }

    result = plan_backend_routes(target, capabilities=CAPABILITIES)

    by_backend = {candidate["backend"]: candidate for candidate in result["candidates"]}
    assert by_backend["sympy"]["status"] == "not_applicable"
    assert by_backend["bounded_counterexample"]["status"] == "requires_formalization"
    assert by_backend["sage"]["status"] == "unavailable"
    assert by_backend["lean"]["status"] == "requires_formalization"
    assert by_backend["lean"]["tool"] == "lean_check"
    assert "explicit Lean source" in by_backend["lean"]["reason"]
    assert result["diagnostics"]["requires_formalization_count"] == 2


def test_route_planner_records_backend_unavailability_without_refutation() -> None:
    capabilities = {
        "sympy": {"available": False, "status": "unavailable"},
        "sage": {"available": False, "status": "unavailable"},
        "lean": {"available": False, "status": "unavailable"},
    }

    result = plan_backend_routes("x + 1 = 1 + x", capabilities=capabilities)

    by_backend = {candidate["backend"]: candidate for candidate in result["candidates"]}
    assert by_backend["sympy"]["status"] == "unavailable"
    assert by_backend["bounded_counterexample"]["status"] == "unavailable"
    assert result["selected_route"]["status"] == "unavailable"
    assert "proof" not in result["selected_route"]["status"]
    assert "refutation" in result["boundary"]
