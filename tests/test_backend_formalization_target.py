from mathdevmcp.backend_formalization_target import build_backend_formalization_target


def _node(target: str = "x + 1 = 1 + x", backend: str = "sympy") -> dict:
    return {
        "id": "node_agent_hypothesis_test",
        "target": target,
        "assumptions": [
            {
                "id": "assumption_1",
                "assumptions": ["x is a scalar backend symbol."],
                "status": "agent_hypothesis_pending_verification",
            }
        ],
        "agent_hypothesis": {
            "id": "agent_hypothesis_test",
            "expected_backend": backend,
        },
    }


def test_sympy_formalization_target_is_backend_ready_for_safe_scalar_equality() -> None:
    target = build_backend_formalization_target(_node())

    assert target["metadata"]["contract"] == "backend_formalization_target"
    assert target["backend"] == "sympy"
    assert target["status"] == "backend_ready"
    assert target["generated_source_or_expr"] == "x + 1 = 1 + x"
    assert target["blockers"] == []
    assert target["expected_certificate"] == "sympy equality simplification or counterexample attempt"
    assert target["symbol_map"]["x"] == "x"
    assert "not a certificate" in target["non_claims"][0]


def test_sympy_formalization_blocks_conditional_expectation() -> None:
    target = build_backend_formalization_target(_node(r"\E[X \mid z] = y", "sympy"))

    assert target["status"] == "blocked_not_encodable"
    assert "backend_not_encodable" in {blocker["kind"] for blocker in target["blockers"]}
    assert r"\E" in target["unsupported_constructs"]


def test_leandojo_route_is_diagnostic_only_not_certificate() -> None:
    target = build_backend_formalization_target(_node("True", "leandojo"))

    assert target["status"] == "diagnostic_only_route"
    assert target["expected_certificate"] == "direct Lean check still required for certification"
    assert target["blockers"][0]["kind"] == "diagnostic_search_not_certificate"


def test_lean_skeleton_has_placeholder_blocker_boundary() -> None:
    target = build_backend_formalization_target(_node("True", "lean"))

    assert target["status"] == "lean_skeleton_only"
    assert target["expected_certificate"] == "direct Lean check without sorry/placeholders"
    assert any(blocker["kind"] == "lean_placeholder_not_certificate" for blocker in target["blockers"])
    assert "sorry" in target["generated_source_or_expr"]
