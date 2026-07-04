from __future__ import annotations

"""Reusable local standard for agent handoff review packets."""

from copy import deepcopy
from typing import Any

from .contracts import attach_contract


AGENT_HANDOFF_PACKET_CONTRACT = "agent_handoff_packet"

REQUIRED_PACKET_FIELDS: tuple[str, ...] = (
    "question",
    "human_framing",
    "source_anchors",
    "assumptions",
    "route_availability",
    "derivation_proof_steps",
    "backend_checks",
    "counterexamples",
    "gaps",
    "actions",
    "evidence_classes",
    "non_claims",
    "reasoning",
)

REQUIRED_HUMAN_FRAMING_FIELDS: tuple[str, ...] = (
    "case_purpose",
    "local_background",
    "minimal_formula_scaffold",
    "source_context_summary",
    "decision_target",
    "decision_criteria",
    "alternative_explanations",
    "what_would_change_conclusion",
)

REQUIRED_REASONING_FIELDS: tuple[str, ...] = (
    "conclusion",
    "why",
    "human_framing",
    "source_context",
    "formalization",
    "decisive_evidence",
    "why_conclusion_follows",
    "limits",
    "answer_text",
    "status",
)

BOUNDARY_TERM_GROUPS: dict[str, tuple[str, ...]] = (
    {
        "proof_certificate": ("not a proof", "proof certificate"),
        "release_readiness": ("release readiness", "release-readiness"),
        "public_benchmark_validity": ("public benchmark",),
        "scientific_validation": ("scientific validation", "scientific-validity"),
        "general_theorem_proving": ("general theorem", "broad theorem", "theorem-proving"),
        "downstream_agent_reliability": ("downstream-agent reliability", "downstream agent reliability"),
    }
)

CERTIFYING_EVIDENCE_CLASSES: set[str] = {"backend_certificate", "backend_counterexample", "scoped_contradiction"}


def _is_non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _list_of_strings(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str) and item.strip()]


def _texts(items: Any) -> list[str]:
    if not isinstance(items, list):
        return []
    texts: list[str] = []
    for item in items:
        if isinstance(item, str):
            texts.append(item)
        elif isinstance(item, dict):
            for key in ("text", "description", "reason", "summary", "code"):
                value = item.get(key)
                if isinstance(value, str):
                    texts.append(value)
    return texts


def _missing_boundary_groups(packet: dict[str, Any]) -> list[str]:
    non_claim_text = " ".join(_texts(packet.get("non_claims"))).lower()
    reasoning = packet.get("reasoning")
    limits_text = ""
    if isinstance(reasoning, dict):
        limits_text = " ".join(_texts(reasoning.get("limits"))).lower()
    combined = f"{non_claim_text} {limits_text}"
    return [label for label, terms in BOUNDARY_TERM_GROUPS.items() if not any(term in combined for term in terms)]


def _validate_required_lists(packet: dict[str, Any], errors: list[str]) -> None:
    list_fields = (
        "assumptions",
        "derivation_proof_steps",
        "backend_checks",
        "counterexamples",
        "gaps",
        "actions",
        "evidence_classes",
        "non_claims",
        "source_anchors",
    )
    for field in list_fields:
        if field in packet and not isinstance(packet.get(field), list):
            errors.append(f"{field} must be a list")

    if isinstance(packet.get("source_anchors"), list) and not packet["source_anchors"]:
        errors.append("source_anchors must be non-empty")
    if isinstance(packet.get("evidence_classes"), list):
        if not packet["evidence_classes"]:
            errors.append("evidence_classes must be non-empty")
        for index, item in enumerate(packet["evidence_classes"]):
            if not _is_non_empty_string(item):
                errors.append(f"evidence_classes[{index}] must be a non-empty string")
    if isinstance(packet.get("non_claims"), list) and not packet["non_claims"]:
        errors.append("non_claims must be non-empty")


def _validate_human_framing(prefix: str, framing: Any, errors: list[str]) -> None:
    if not isinstance(framing, dict):
        errors.append(f"{prefix} must be an object")
        return

    string_fields = (
        "case_purpose",
        "local_background",
        "minimal_formula_scaffold",
        "source_context_summary",
        "decision_target",
    )
    list_fields = (
        "decision_criteria",
        "alternative_explanations",
        "what_would_change_conclusion",
    )
    for field in REQUIRED_HUMAN_FRAMING_FIELDS:
        if field not in framing:
            errors.append(f"{prefix}.{field} is required")
    for field in string_fields:
        if field in framing and not _is_non_empty_string(framing.get(field)):
            errors.append(f"{prefix}.{field} must be a non-empty string")
    for field in list_fields:
        if field in framing and not isinstance(framing.get(field), list):
            errors.append(f"{prefix}.{field} must be a list")
    for field in ("decision_criteria", "what_would_change_conclusion"):
        if isinstance(framing.get(field), list) and not _list_of_strings(framing.get(field)):
            errors.append(f"{prefix}.{field} must contain at least one non-empty string")


def _validate_reasoning(reasoning: Any, errors: list[str]) -> None:
    if not isinstance(reasoning, dict):
        errors.append("reasoning must be an object")
        return

    for field in REQUIRED_REASONING_FIELDS:
        if field not in reasoning:
            errors.append(f"reasoning.{field} is required")

    for field in ("conclusion", "answer_text", "status"):
        if field in reasoning and not _is_non_empty_string(reasoning.get(field)):
            errors.append(f"reasoning.{field} must be a non-empty string")

    list_fields = (
        "why",
        "source_context",
        "formalization",
        "decisive_evidence",
        "why_conclusion_follows",
        "limits",
    )
    for field in list_fields:
        if field in reasoning and not isinstance(reasoning.get(field), list):
            errors.append(f"reasoning.{field} must be a list")
        elif field in reasoning and not _list_of_strings(reasoning.get(field)):
            errors.append(f"reasoning.{field} must contain at least one non-empty string")

    if isinstance(reasoning.get("why"), list) and len(_list_of_strings(reasoning["why"])) < 4:
        errors.append("reasoning.why must contain at least four non-empty strings")

    if "human_framing" in reasoning:
        _validate_human_framing("reasoning.human_framing", reasoning.get("human_framing"), errors)


def validate_agent_handoff_packet(packet: dict[str, Any]) -> list[str]:
    """Return deterministic validation errors for a local handoff packet."""
    errors: list[str] = []
    if not isinstance(packet, dict):
        return ["packet must be an object"]

    metadata = packet.get("metadata")
    if metadata is not None:
        if not isinstance(metadata, dict):
            errors.append("metadata must be an object")
        else:
            if metadata.get("schema_version") != "1.0":
                errors.append("metadata.schema_version must be 1.0")
            if metadata.get("contract") != AGENT_HANDOFF_PACKET_CONTRACT:
                errors.append(f"metadata.contract must be {AGENT_HANDOFF_PACKET_CONTRACT}")

    for field in REQUIRED_PACKET_FIELDS:
        if field not in packet:
            errors.append(f"{field} is required")

    if "question" in packet and not _is_non_empty_string(packet.get("question")):
        errors.append("question must be a non-empty string")
    if "human_framing" in packet:
        _validate_human_framing("human_framing", packet.get("human_framing"), errors)
    if "route_availability" in packet and not isinstance(packet.get("route_availability"), dict):
        errors.append("route_availability must be an object")
    if "reasoning" in packet:
        _validate_reasoning(packet.get("reasoning"), errors)

    _validate_required_lists(packet, errors)

    missing_boundaries = _missing_boundary_groups(packet)
    boundary_present = not missing_boundaries
    if "non_claims" in packet and isinstance(packet.get("non_claims"), list):
        for label in missing_boundaries:
            errors.append(f"non_claims missing required boundary: {label}")

    certification_source = packet.get("certification_source")
    evidence_classes = set(_list_of_strings(packet.get("evidence_classes")))
    proof_like = certification_source in {"backend", "scoped_contradiction"} or bool(evidence_classes & CERTIFYING_EVIDENCE_CLASSES)
    if proof_like and not boundary_present:
        errors.append("proof-like evidence requires explicit packet boundary non-claim")
    if proof_like and not packet.get("backend_checks") and not packet.get("derivation_proof_steps"):
        errors.append("proof-like evidence requires backend_checks or derivation_proof_steps")

    return errors


def build_agent_handoff_packet(
    *,
    question: str,
    human_framing: dict[str, Any],
    source_anchors: list[Any],
    assumptions: list[Any] | None = None,
    route_availability: dict[str, Any] | None = None,
    derivation_proof_steps: list[Any] | None = None,
    backend_checks: list[Any] | None = None,
    counterexamples: list[Any] | None = None,
    gaps: list[Any] | None = None,
    actions: list[Any] | None = None,
    evidence_classes: list[str] | None = None,
    non_claims: list[Any] | None = None,
    reasoning: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a contract-attached packet without mutating caller inputs."""
    packet: dict[str, Any] = {
        "question": question,
        "human_framing": deepcopy(human_framing),
        "source_anchors": deepcopy(source_anchors),
        "assumptions": deepcopy(assumptions or []),
        "route_availability": deepcopy(route_availability or {}),
        "derivation_proof_steps": deepcopy(derivation_proof_steps or []),
        "backend_checks": deepcopy(backend_checks or []),
        "counterexamples": deepcopy(counterexamples or []),
        "gaps": deepcopy(gaps or []),
        "actions": deepcopy(actions or []),
        "evidence_classes": deepcopy(evidence_classes or []),
        "non_claims": deepcopy(non_claims or []),
        "reasoning": deepcopy(reasoning),
    }
    if extra:
        packet.update(deepcopy(extra))
    packet = attach_contract(packet, AGENT_HANDOFF_PACKET_CONTRACT)
    errors = validate_agent_handoff_packet(packet)
    if errors:
        raise ValueError(f"invalid agent handoff packet: {errors}")
    return packet
