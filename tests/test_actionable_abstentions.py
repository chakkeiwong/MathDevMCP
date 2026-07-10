from mathdevmcp.actionable_abstentions import build_actionable_abstention_payload


def test_actionable_abstention_for_expectation_reports_missing_math() -> None:
    result = build_actionable_abstention_payload(
        text=r"\Delta \NPV_i = \E[\NPV_i(a)-\NPV_i(a_0)\mid \mathcal I]",
        problem="Expectation equality is not yet formalized.",
        why_not_concrete="No exact replacement text.",
        location="paper.tex > line 10",
        kind="concretize_before_fix",
    )

    obligation_ids = {item["id"] for item in result["missing_obligations"]}
    set_ids = {item["id"] for item in result["possible_assumption_sets"]}
    route_text = " ".join(step["detail"] for step in result["how_derivation_can_work"])

    assert result["metadata"] == {"schema_version": "1.0", "contract": "actionable_abstention_payload"}
    assert {"conditional_law_defined", "measurable_integrable_payoff_terms"}.issubset(obligation_ids)
    assert "kernel_integrability_condition" in set_ids
    assert "finite weighted sum" in " ".join(item["closes"] for item in result["possible_assumption_sets"])
    assert "finite conditional expectation" in route_text
    assert "not proof certificates" in result["non_claim"]


def test_actionable_abstention_for_bellman_reports_dynamic_programming_obligations() -> None:
    result = build_actionable_abstention_payload(
        text=r"V_t^\star(b,O;s)=\max_{a\in\mathcal A_t(O,b)}\{\bar r_t+\E[V_{t+1}^\star]\}",
        problem="Bellman recursion not formalized.",
        why_not_concrete="Manual formalization required.",
        location="paper.tex > Bellman > line 20",
        kind="add_review_boundary",
    )

    kinds = {item["kind"] for item in result["missing_obligations"]}

    assert "bellman_value_recursion" in result["domains"]
    assert {"dynamic_programming_condition", "probability_condition", "recursion_boundary_condition"}.issubset(kinds)
    assert result["next_audit"]["tool"] == "audit_and_propose_assumptions"


def test_actionable_abstention_for_malformed_replacement_demands_source_span() -> None:
    result = build_actionable_abstention_payload(
        text=r"\begin{equation} x = \left[ y \end{equation}",
        problem="Replacement LaTeX is malformed.",
        why_not_concrete="The reconstructed replacement LaTeX failed conservative structure checks.",
        location="paper.tex > line 30",
        kind="split_derivation_step",
    )

    obligation_ids = {item["id"] for item in result["missing_obligations"]}

    assert "malformed_replacement_latex" in result["domains"]
    assert {"balanced_replacement_latex", "source_span_reconstruction"}.issubset(obligation_ids)
    assert result["next_audit"]["tool"] == "audit_derivation_v2_label"
