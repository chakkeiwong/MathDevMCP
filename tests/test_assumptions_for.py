from pathlib import Path

from mathdevmcp.assumptions_for import audit_and_propose_assumptions, assumptions_for, score_assumption_set
from mathdevmcp.high_level_contracts import validate_high_level_result


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"


def test_assumptions_for_logdet_reports_route_required_domain() -> None:
    result = assumptions_for("logdet(A)")

    assert result["status"] == "missing_assumptions"
    assert result["workflow"] == "assumptions_for"
    assert result["claim_class"] == "assumption_discovery"
    assert "route_assumptions_not_global_minimality" in {item["code"] for item in result["non_claims"]}
    assert result["assumptions"][0]["route_categories"] == ["covariance_condition", "domain_condition"]
    assert result["evidence_ledger"]["assumption_items"][0]["route_categories"] == [
        "covariance_condition",
        "domain_condition",
    ]
    assert result["coverage"]["gap_count"] == 1
    assert result["tool_uses"][0]["tool"] == "assumptions_required"
    assert result["gaps"][0]["location"] == "logdet(A)"
    assert "logdet" in result["gaps"][0]["why"].lower()
    assert result["proposals"][0]["gap_ids"] == [result["gaps"][0]["id"]]
    assert "positive definite" in result["proposals"][0]["proposal_text"]
    assert result["proposals"][0]["validation"]["status"] == "validated_by_rule"
    assert result["validation"]["certifying"] is False
    assert result["agent_handoff"]["assumption_gap_ledger"] == result["gaps"]
    rubric = score_assumption_set(result, {"determinant domain"})
    assert rubric["status"] == "passed"
    assert validate_high_level_result(result) == []


def test_assumptions_for_inverse_and_division_scores_by_set_terms() -> None:
    result = assumptions_for("x / y + inv(A)")

    rubric = score_assumption_set(result, {"denominator is nonzero", "invertible"})
    categories_by_text = {item["text"]: item["route_categories"] for item in result["assumptions"]}

    assert result["status"] == "missing_assumptions"
    assert categories_by_text["denominator is nonzero"] == ["domain_condition"]
    assert categories_by_text["matrix operand is square and invertible"] == ["domain_condition", "shape_condition"]
    assert rubric["status"] == "passed"
    assert validate_high_level_result(result) == []


def test_assumptions_for_latex_jacobian_logdet_reports_domain_shape_and_smoothness() -> None:
    result = assumptions_for(r"For an invertible map $T$, use $\log |\det J_T|$.")

    categories = set(result["assumptions"][0]["route_categories"])
    assert result["status"] == "missing_assumptions"
    assert {"domain_condition", "shape_condition", "smoothness_condition"}.issubset(categories)
    assert "Jacobian" in result["proposals"][0]["proposal_text"]
    assert result["proposals"][0]["validation"]["status"] == "validated_by_rule"


def test_assumptions_for_conditional_expectation_reports_integrability() -> None:
    result = assumptions_for(r"\E[X(z') \mid z]")

    assert result["status"] == "missing_assumptions"
    assert "integrable" in result["proposals"][0]["proposal_text"]
    assert "integrability_condition" in result["gaps"][0]["route_categories"]
    assert result["proposals"][0]["validation"]["status"] == "validated_by_rule"
    assert result["proposals"][0]["missing_assumptions"]
    assert result["proposals"][0]["possible_assumption_sets"]
    assert result["proposals"][0]["derivation_route"]


def test_assumptions_for_interior_foc_reports_interchange_route() -> None:
    result = assumptions_for(
        r"Interior first-order conditions: 0 = m(\bar e)d\bar e/dk' + \beta \E[V^\star_k(k',b',z')\mid z]."
    )

    proposal_texts = " ".join(proposal["proposal_text"] for proposal in result["proposals"])
    routes = " ".join(
        step["detail"]
        for proposal in result["proposals"]
        for step in proposal.get("derivation_route", [])
        if isinstance(step, dict)
    )
    assert result["status"] == "missing_assumptions"
    assert "interchanged" in proposal_texts or "interchange" in routes
    assert "transition" in routes


def test_assumptions_for_risky_pricing_reports_math_packet() -> None:
    result = assumptions_for(
        r"For \(b'>0\), the zero-profit condition is "
        r"b'(1+r)=\E[D(k',b',z')R(k',z')+(1-D(k',b',z'))b'(1+\widetilde r(z,k',b'))\mid z]."
    )

    route_kinds = {proposal.get("route_kind") for proposal in result["proposals"]}
    packet_text = " ".join(
        " ".join(proposal.get("missing_assumptions", []))
        + " "
        + " ".join(
            str(assumption_set.get("closes", ""))
            for assumption_set in proposal.get("possible_assumption_sets", [])
            if isinstance(assumption_set, dict)
        )
        + " "
        + " ".join(step.get("detail", "") for step in proposal.get("derivation_route", []) if isinstance(step, dict))
        for proposal in result["proposals"]
    )

    assert {"risky_pricing_expectation", "zero_profit_pricing_convention"}.issubset(route_kinds)
    assert "conditional probability law" in packet_text
    assert "zero-profit pricing measure" in packet_text
    assert "finite weighted sum" in packet_text
    assert "proof certificate" in result["validation"]["boundary"]


def test_assumptions_for_interior_foc_reports_missing_math_and_derivation() -> None:
    result = assumptions_for(
        r"Interior first-order conditions: "
        r"0=m(\bar e)d\bar e/dk' + \beta \E[V^\star_k(k',b',z')\mid z]."
    )

    proposals = [proposal for proposal in result["proposals"] if proposal.get("route_kind") == "interior_foc_expectation"]
    assert proposals
    proposal = proposals[0]
    missing_text = " ".join(proposal["missing_assumptions"])
    route_text = " ".join(step["detail"] for step in proposal["derivation_route"])
    set_ids = {item["id"] for item in proposal["possible_assumption_sets"]}

    assert "differentiability of \\(V^\\star" in missing_text
    assert "choice-independence" in missing_text
    assert {"finite_state_interior_foc", "dominated_interchange_interior_foc"} == set_ids
    assert "\\(\\partial_x\\E[V^\\star" in route_text
    assert "transition law" in route_text


def test_assumptions_for_provided_assumption_does_not_claim_minimality() -> None:
    result = assumptions_for("x / y", provided_assumptions=["denominator is nonzero"])

    assert result["status"] == "inconclusive"
    assert "general_theorem_proving_not_claimed" in {item["code"] for item in result["non_claims"]}
    assert not any("minimal" in item["text"].lower() for item in result["non_claims"])
    assert result["gaps"] == []
    assert result["proposals"] == []
    assert validate_high_level_result(result) == []


def test_assumptions_for_unknown_route_is_inconclusive_not_proof() -> None:
    result = assumptions_for("x + y")

    assert result["status"] == "inconclusive"
    assert result["certification_source"] == "none"
    assert result["veto_reasons"]
    assert result["gaps"][0]["id"] == "assumption_gap_direct_target_unknown_route"
    assert result["proposals"][0]["type"] == "formalize_assumption"
    assert result["proposals"][0]["validation"]["status"] == "not_encodable"
    assert validate_high_level_result(result) == []


def test_assumption_set_rubric_reports_missing_terms() -> None:
    result = assumptions_for("logdet(A)")
    rubric = score_assumption_set(result, {"stationarity"})

    assert rubric["status"] == "failed"
    assert rubric["missing_terms"] == ["stationarity"]


def test_audit_and_propose_assumptions_writes_gap_proposal_markdown(tmp_path: Path) -> None:
    output = tmp_path / "assumptions.md"
    result = audit_and_propose_assumptions(
        "Audit assumptions for the transport logdet label",
        root=str(FIXTURES),
        labels=["prop:transport-logdet"],
        output_path=output,
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "audit_assumption_report_result"}
    assert result["status"] == "proposal_ready"
    assert result["coverage"]["gap_count"] >= 1
    assert "prop:transport-logdet" in result["gaps"][0]["location"]
    assert result["proposals"][0]["gap_ids"] == [result["gaps"][0]["id"]]
    assert result["proposals"][0]["validation"]["status"] == "validated_by_rule"
    assert "Jacobian" in result["proposals"][0]["proposal_text"]
    assert result["agent_handoff"]["proposal_count"] == len(result["proposals"])
    markdown = output.read_text(encoding="utf-8")
    assert "Problem:" in markdown
    assert "Proposed assumption:" in markdown
    assert "Possible sufficient assumption sets:" in markdown
    assert "How the derivation works under the assumptions:" in markdown
    assert "not a proof certificate" in markdown


def test_audit_and_propose_assumptions_uses_source_stable_gap_ids(tmp_path: Path) -> None:
    result = audit_and_propose_assumptions(
        "Audit two labels",
        root=str(FIXTURES),
        labels=["prop:transport-logdet", "prop:transport-mismatch"],
        output_path=tmp_path / "two-labels.md",
    )

    gap_ids = [gap["id"] for gap in result["gaps"]]
    proposal_ids = [proposal["id"] for proposal in result["proposals"]]
    assert len(gap_ids) == len(set(gap_ids))
    assert len(proposal_ids) == len(set(proposal_ids))


def test_audit_and_propose_assumptions_markdown_preserves_math_packet(tmp_path: Path) -> None:
    output = tmp_path / "risky.md"
    result = audit_and_propose_assumptions(
        "Audit risky assumptions",
        root=str(Path(__file__).resolve().parent.parent / "docs"),
        labels=["prop:risky-pricing", "prop:interior-foc"],
        output_path=output,
    )

    markdown = output.read_text(encoding="utf-8")
    route_kinds = {proposal.get("route_kind") for proposal in result["proposals"]}

    assert result["coverage"]["proposal_count"] >= 4
    assert {"risky_pricing_expectation", "zero_profit_pricing_convention", "interior_foc_expectation", "foc_expectation_differentiation"}.issubset(route_kinds)
    assert "Mathematically missing: a conditional probability law" in markdown
    assert "Possible sufficient assumption sets:" in markdown
    assert "How the derivation works under the assumptions:" in markdown
    assert "Under a choice-independent transition law" in markdown
