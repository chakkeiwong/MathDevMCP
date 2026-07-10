from mathdevmcp.report_claim_boundary import audit_report_claim_boundary


def test_report_claim_boundary_classifies_report_status_not_theorem() -> None:
    result = audit_report_claim_boundary(
        "The audit report passed Phase 3 but is not a proof of the document.",
        evidence_snippets=["Phase 3 result: 20 focused tests passed; generated report has actionable abstentions."],
        source={"path": "docs/plans/phase-03-result.md"},
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "report_claim_boundary_audit"}
    assert result["boundary_class"] == "report_status_or_nonclaim"
    assert result["mathematical_claim"] is False
    assert result["document_evidence_needed"]
    assert result["missing_evidence"]
    assert result["overclaim_risks"][0]["kind"] == "report_status_as_theorem"
    assert "not phrase it as a mathematical theorem" in result["safe_wording"]
    assert result["agent_handoff"]["missing_evidence"] == result["missing_evidence"]


def test_report_claim_boundary_classifies_math_claim_as_needing_math_evidence() -> None:
    result = audit_report_claim_boundary("For all x, f(x)=g(x).")

    assert result["boundary_class"] == "mathematical_or_scientific_claim"
    assert result["mathematical_claim"] is True
    assert any(item["kind"] == "math_or_empirical_evidence" for item in result["document_evidence_needed"])
    assert "supply the appropriate mathematical" in result["safe_wording"]


def test_report_claim_boundary_ambiguous_claim_requests_rewrite() -> None:
    result = audit_report_claim_boundary("This is better now.")

    assert result["boundary_class"] == "ambiguous_claim_boundary"
    assert result["status"] == "needs_boundary_clarification"
    assert "Rewrite the claim" in result["safe_wording"]
