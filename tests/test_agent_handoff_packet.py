from copy import deepcopy

import pytest

from mathdevmcp.agent_handoff_packet import build_agent_handoff_packet, validate_agent_handoff_packet


def _framing() -> dict:
    return {
        "case_purpose": "Check a bounded derivation handoff.",
        "local_background": "The claim concerns a scoped symbolic equality.",
        "minimal_formula_scaffold": "Need to compare lhs - rhs under stated assumptions.",
        "source_context_summary": "The source asks for local review of one displayed step.",
        "decision_target": "Decide whether the encoded obligation is proved, refuted, or blocked.",
        "decision_criteria": ["A backend certificate proves only the encoded obligation."],
        "alternative_explanations": ["A mismatch may reflect missing assumptions."],
        "what_would_change_conclusion": ["A concrete counterexample or missing assumption record."],
    }


def _reasoning(framing: dict | None = None) -> dict:
    human_framing = framing or _framing()
    return {
        "conclusion": "The packet is diagnostic and bounded to the encoded obligation.",
        "why": [
            "Question and scope are recorded.",
            "Source context is bounded.",
            "Machine evidence is preserved separately.",
            "Boundary non-claims are explicit.",
        ],
        "human_framing": deepcopy(human_framing),
        "source_context": ["source.md:1-3 supplies the local claim."],
        "formalization": ["Encoded obligation: lhs should equal rhs."],
        "decisive_evidence": ["Sympy simplified lhs - rhs to zero."],
        "why_conclusion_follows": ["A zero simplification certifies only this encoded equality."],
        "limits": ["This packet is not a proof certificate or release readiness claim."],
        "answer_text": "Conclusion: diagnostic bounded packet, not a proof certificate.",
        "status": "diagnostic_only",
    }


def _packet_kwargs() -> dict:
    framing = _framing()
    return {
        "question": "Can we derive lhs = rhs from the recorded assumptions?",
        "human_framing": framing,
        "source_anchors": [{"path": "source.md", "line_range": "1-3", "role": "claim"}],
        "assumptions": [{"text": "x is real", "status": "used"}],
        "route_availability": {"symbolic_backend_state": "available"},
        "derivation_proof_steps": [{"lhs": "x + 1", "rhs": "1 + x", "status": "proved"}],
        "backend_checks": [{"backend": "sympy", "status": "proved"}],
        "counterexamples": [],
        "gaps": [],
        "actions": [{"code": "human_review", "description": "Inspect the bounded packet."}],
        "evidence_classes": ["backend_certificate"],
        "non_claims": [
            "This packet is not a proof certificate, release readiness, public benchmark validity, "
            "scientific validation, general theorem proving, or downstream-agent reliability claim."
        ],
        "reasoning": _reasoning(framing),
    }


def test_build_agent_handoff_packet_attaches_contract_and_validates() -> None:
    packet = build_agent_handoff_packet(**_packet_kwargs())

    assert packet["metadata"] == {"schema_version": "1.0", "contract": "agent_handoff_packet"}
    assert validate_agent_handoff_packet(packet) == []


def test_validator_catches_missing_required_top_level_field() -> None:
    packet = build_agent_handoff_packet(**_packet_kwargs())
    del packet["source_anchors"]

    assert "source_anchors is required" in validate_agent_handoff_packet(packet)


def test_validator_catches_missing_human_framing_background() -> None:
    packet = build_agent_handoff_packet(**_packet_kwargs())
    packet["human_framing"]["local_background"] = ""

    assert "human_framing.local_background must be a non-empty string" in validate_agent_handoff_packet(packet)


def test_validator_catches_missing_reasoning_explanation() -> None:
    packet = build_agent_handoff_packet(**_packet_kwargs())
    packet["reasoning"]["why_conclusion_follows"] = []

    assert "reasoning.why_conclusion_follows must contain at least one non-empty string" in validate_agent_handoff_packet(packet)


def test_validator_catches_missing_source_anchors() -> None:
    packet = build_agent_handoff_packet(**_packet_kwargs())
    packet["source_anchors"] = []

    assert "source_anchors must be non-empty" in validate_agent_handoff_packet(packet)


def test_validator_catches_missing_non_claims() -> None:
    packet = build_agent_handoff_packet(**_packet_kwargs())
    packet["non_claims"] = []
    packet["reasoning"]["limits"] = []

    errors = validate_agent_handoff_packet(packet)
    assert "non_claims must be non-empty" in errors
    assert "reasoning.limits must contain at least one non-empty string" in errors
    assert "non_claims missing required boundary: proof_certificate" in errors


def test_builder_does_not_mutate_inputs() -> None:
    kwargs = _packet_kwargs()
    original = deepcopy(kwargs)

    packet = build_agent_handoff_packet(**kwargs)
    packet["human_framing"]["local_background"] = "mutated"
    packet["backend_checks"].append({"backend": "other"})

    assert kwargs == original


def test_diagnostic_packet_with_boundary_passes() -> None:
    kwargs = _packet_kwargs()
    kwargs["evidence_classes"] = ["review_packet"]
    kwargs["backend_checks"] = [{"backend": "none", "status": "diagnostic_only"}]
    kwargs["derivation_proof_steps"] = []
    kwargs["gaps"] = [{"kind": "needs_human_review"}]

    packet = build_agent_handoff_packet(**kwargs)

    assert validate_agent_handoff_packet(packet) == []


def test_proof_like_overclaim_without_boundary_fails() -> None:
    packet = build_agent_handoff_packet(**_packet_kwargs())
    packet["non_claims"] = ["Backend certificate present."]
    packet["reasoning"]["limits"] = ["Backend certificate present."]

    assert "proof-like evidence requires explicit packet boundary non-claim" in validate_agent_handoff_packet(packet)


def test_validator_requires_all_global_boundary_categories() -> None:
    packet = build_agent_handoff_packet(**_packet_kwargs())
    packet["non_claims"] = ["This packet is not a proof certificate or release readiness claim."]
    packet["reasoning"]["limits"] = ["This packet is not a proof certificate or release readiness claim."]

    errors = validate_agent_handoff_packet(packet)

    assert "non_claims missing required boundary: public_benchmark_validity" in errors
    assert "non_claims missing required boundary: scientific_validation" in errors
    assert "non_claims missing required boundary: general_theorem_proving" in errors
    assert "non_claims missing required boundary: downstream_agent_reliability" in errors
