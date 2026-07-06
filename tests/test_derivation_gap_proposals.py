from mathdevmcp.derivation_gap_proposals import (
    build_derivation_gap_proposal_packet,
    build_derivation_gaps,
    build_derivation_proposals,
    build_derivation_tool_uses,
    summarize_derivation_validation,
)
from mathdevmcp.derive_or_refute import derive_or_refute


def _packet(target: str, **kwargs):
    low_level = derive_or_refute(target, **kwargs)
    gaps = build_derivation_gaps(low_level)
    proposals = build_derivation_proposals(gaps)
    return low_level, gaps, proposals


def test_derivation_builder_accepts_backend_certificate_for_proved_target() -> None:
    low_level, gaps, proposals = _packet("a + b = b + a")

    assert low_level["status"] == "proved"
    assert gaps[0]["status"] == "proved"
    assert gaps[0]["severity"] == "closed"
    assert proposals[0]["type"] == "accept_backend_certificate"
    assert proposals[0]["validation"]["status"] == "certified_by_backend"
    assert proposals[0]["validation"]["certifying"] is True
    assert any(ref.startswith("backend_evidence:backend_verified") for ref in proposals[0]["evidence_refs"])
    assert "scoped" in proposals[0]["proposal_text"].lower()


def test_derivation_builder_accepts_counterexample_for_refuted_target() -> None:
    _, gaps, proposals = _packet("A*B = B*A")

    assert gaps[0]["status"] == "refuted"
    assert gaps[0]["counterexamples"]
    assert "lhs_value" in gaps[0]["counterexamples"][0]
    assert proposals[0]["type"] == "accept_counterexample"
    assert proposals[0]["validation"]["status"] == "refuted_by_counterexample"
    assert proposals[0]["validation"]["certifying"] is True
    route_text = " ".join(step["detail"] for step in proposals[0]["derivation_route"])
    assert "assignments" in route_text


def test_derivation_builder_links_missing_assumption_repairs() -> None:
    _, gaps, proposals = _packet("logdet(A) = trace(A)")

    gap = gaps[0]
    proposal = proposals[0]
    assert gap["status"] == "missing_assumptions"
    assert gap["assumption_gaps"]
    assert proposal["type"] == "add_assumptions"
    assert proposal["validation"]["status"] == "blocked_by_missing_assumptions"
    assert proposal["validation"]["certifying"] is False
    assert proposal["assumption_repairs"]
    assert all(item["gap_ids"] for item in proposal["assumption_repairs"])
    repair_text = " ".join(item["proposal_text"] for item in proposal["assumption_repairs"])
    assert "positive definite" in repair_text
    assert "conformable" in repair_text
    assert "collect more evidence" not in proposal["proposal_text"].lower()


def test_derivation_builder_abstains_with_typed_formalization_for_unknown_route() -> None:
    _, gaps, proposals = _packet("A = A")

    proposal = proposals[0]
    assert gaps[0]["status"] == "unknown"
    assert proposal["type"] == "formalize_target"
    assert proposal["validation"]["status"] == "abstained_no_certifying_route"
    assert proposal["validation"]["certifying"] is False
    assert proposal["formalization_target"]["needed_before_claim"] is True
    assert "typed_obligation" in {item["expected_artifact"] for item in proposal["backend_plan"]}


def test_derivation_builder_reports_not_encodable_without_false_claim() -> None:
    _, gaps, proposals = _packet("[x] = [x]")

    proposal = proposals[0]
    assert gaps[0]["status"] == "not_encodable"
    assert proposal["type"] == "formalize_target"
    assert proposal["validation"]["status"] == "blocked_by_not_encodable"
    assert proposal["validation"]["certifying"] is False
    assert "domains" in " ".join(proposal["formalization_target"]["required_fields"])


def test_derivation_builder_reports_backend_unavailable(monkeypatch) -> None:
    import mathdevmcp.math_debugging_router as router

    monkeypatch.setattr(router, "find_spec", lambda name: None)
    low_level = derive_or_refute("x + y = y + x", backend="sage")
    gaps = build_derivation_gaps(low_level)
    proposals = build_derivation_proposals(gaps)

    assert low_level["status"] == "backend_unavailable"
    assert gaps[0]["status"] == "backend_unavailable"
    assert proposals[0]["type"] == "try_backend_proof"
    assert proposals[0]["validation"]["status"] == "blocked_by_backend_unavailable"
    assert proposals[0]["backend_plan"][0]["tool"] == "configure_backend"


def test_derivation_packet_and_tool_uses_are_agent_consumable() -> None:
    low_level = derive_or_refute("logdet(A) = trace(A)", givens=["A is a covariance matrix"])
    packet = build_derivation_gap_proposal_packet(low_level)
    tool_uses = build_derivation_tool_uses(
        low_level["target"],
        givens=low_level["givens"],
        assumptions=["A is positive definite"],
        backend="auto",
    )

    assert packet["metadata"] == {"schema_version": "1.0", "contract": "derivation_gap_proposal_packet"}
    assert packet["agent_handoff"]["derivation_gap_ledger"] == packet["gaps"]
    assert packet["validation"]["proposal_count"] == len(packet["proposals"])
    assert tool_uses[0]["tool"] == "derive_or_refute"
    assert tool_uses[0]["arguments"]["givens"] == ["A is a covariance matrix"]
    assert tool_uses[0]["arguments"]["assumptions"] == ["A is positive definite"]
    assert tool_uses[1]["tool"] == "build_derivation_gaps"
    assert tool_uses[2]["tool"] == "build_derivation_proposals"


def test_every_derivation_proposal_links_to_gap_and_has_validation() -> None:
    statuses = [
        _packet("a + b = b + a"),
        _packet("A*B = B*A"),
        _packet("logdet(A) = trace(A)"),
        _packet("A = A"),
        _packet("[x] = [x]"),
    ]
    proposals = [proposal for _, _, status_proposals in statuses for proposal in status_proposals]
    gap_ids = {gap["id"] for _, status_gaps, _ in statuses for gap in status_gaps}
    validation = summarize_derivation_validation(proposals)

    assert proposals
    assert all(proposal["gap_ids"] for proposal in proposals)
    assert all(proposal["gap_ids"][0] in gap_ids for proposal in proposals)
    assert all(isinstance(proposal.get("validation"), dict) for proposal in proposals)
    assert validation["proposal_count"] == len(proposals)
    assert validation["certifying_proposal_count"] == 2
