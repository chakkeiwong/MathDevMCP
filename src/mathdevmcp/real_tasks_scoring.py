from __future__ import annotations

"""Deterministic structural scoring for real-task benchmark candidate answers."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract


@dataclass(frozen=True)
class RealTaskCandidateAnswer:
    case_id: str
    status: str | None
    substatus: str | None
    labels: list[str]
    evidence_class: str | None
    summary_text: str
    claims: list[str]
    next_actions: list[str]


@dataclass(frozen=True)
class RealTaskStructuralScore:
    case_id: str
    status: str
    reason: str
    quality_checks: dict[str, bool]
    details: dict[str, Any]


def _normalize_text(value: str) -> str:
    return " ".join(value.lower().replace("_", " ").split())


def _list_of_strings(value: object) -> list[str]:
    return value if isinstance(value, list) and all(isinstance(item, str) for item in value) else []


def _build_candidate(value: dict[str, Any]) -> RealTaskCandidateAnswer | None:
    required_strings = ["case_id", "summary_text"]
    for field in required_strings:
        field_value = value.get(field)
        if not isinstance(field_value, str) or not field_value.strip():
            return None
    optional_string_fields = ["status", "substatus", "evidence_class"]
    for field in optional_string_fields:
        field_value = value.get(field)
        if field_value is not None and not isinstance(field_value, str):
            return None
    labels = value.get("labels")
    claims = value.get("claims")
    next_actions = value.get("next_actions")
    if not isinstance(labels, list) or not all(isinstance(item, str) for item in labels):
        return None
    if not isinstance(claims, list) or not all(isinstance(item, str) for item in claims):
        return None
    if not isinstance(next_actions, list) or not all(isinstance(item, str) for item in next_actions):
        return None
    return RealTaskCandidateAnswer(
        case_id=value["case_id"],
        status=value.get("status"),
        substatus=value.get("substatus"),
        labels=labels,
        evidence_class=value.get("evidence_class"),
        summary_text=value["summary_text"],
        claims=claims,
        next_actions=next_actions,
    )


def _contains_all(required: list[str], haystack: list[str] | str) -> tuple[bool, list[str]]:
    if isinstance(haystack, str):
        normalized_haystack = _normalize_text(haystack)
        missing = [item for item in required if _normalize_text(item) not in normalized_haystack]
    else:
        normalized_values = {_normalize_text(item) for item in haystack}
        missing = [item for item in required if _normalize_text(item) not in normalized_values]
    return not missing, missing


def _find_present(required: list[str], haystack: list[str] | str) -> list[str]:
    if isinstance(haystack, str):
        normalized_haystack = _normalize_text(haystack)
        return [item for item in required if _normalize_text(item) in normalized_haystack]
    normalized_values = {_normalize_text(item) for item in haystack}
    return [item for item in required if _normalize_text(item) in normalized_values]


def score_real_task_case(case: dict[str, Any], candidate: dict[str, Any]) -> dict:
    built = _build_candidate(candidate)
    case_id = case.get("id", "<unknown>")
    if built is None:
        return attach_contract(
            asdict(
                RealTaskStructuralScore(
                    case_id=case_id,
                    status="inconclusive",
                    reason="Candidate answer is malformed or missing required normalized fields.",
                    quality_checks={
                        "expected_status_match": False,
                        "expected_substatus_match": False,
                        "expected_labels_present": False,
                        "required_terms_present": False,
                        "forbidden_claims_absent": False,
                        "required_next_actions_present": False,
                        "evidence_class_match": False,
                        "false_confidence_veto_clear": False,
                    },
                    details={"candidate": candidate},
                )
            ),
            "real_task_case_structural_score",
        )

    gold = case.get("gold", {}) if isinstance(case.get("gold", {}), dict) else {}
    expected_status = gold.get("expected_status")
    expected_substatus = gold.get("expected_substatus")
    expected_labels = _list_of_strings(gold.get("expected_labels"))
    required_terms = _list_of_strings(gold.get("required_terms"))
    forbidden_claims = _list_of_strings(gold.get("forbidden_claims"))
    required_next_actions = _list_of_strings(gold.get("required_next_actions"))
    expected_evidence_class = gold.get("evidence_class")
    false_confidence_veto = gold.get("false_confidence_veto") is True

    status_match = built.status == expected_status
    substatus_match = expected_substatus is None or built.substatus == expected_substatus
    labels_present, missing_labels = _contains_all(expected_labels, built.labels)
    required_terms_present, missing_terms = _contains_all(required_terms, built.summary_text)
    present_forbidden_claims = _find_present(forbidden_claims, built.claims)
    forbidden_claims_absent = len(present_forbidden_claims) == 0
    next_actions_present, missing_next_actions = _contains_all(required_next_actions, built.next_actions)
    evidence_class_match = built.evidence_class == expected_evidence_class
    false_confidence_veto_clear = not (false_confidence_veto and present_forbidden_claims)

    quality_checks = {
        "expected_status_match": status_match,
        "expected_substatus_match": substatus_match,
        "expected_labels_present": labels_present,
        "required_terms_present": required_terms_present,
        "forbidden_claims_absent": forbidden_claims_absent,
        "required_next_actions_present": next_actions_present,
        "evidence_class_match": evidence_class_match,
        "false_confidence_veto_clear": false_confidence_veto_clear,
    }

    passed = all(quality_checks.values())
    status = "consistent" if passed else "mismatch"
    reason = "Candidate answer satisfies the real-task structural scoring contract." if passed else "Candidate answer violates the real-task structural scoring contract."

    return attach_contract(
        asdict(
            RealTaskStructuralScore(
                case_id=case_id,
                status=status,
                reason=reason,
                quality_checks=quality_checks,
                details={
                    "missing_expected_labels": missing_labels,
                    "missing_required_terms": missing_terms,
                    "present_forbidden_claims": present_forbidden_claims,
                    "missing_required_next_actions": missing_next_actions,
                    "observed_status": built.status,
                    "observed_substatus": built.substatus,
                    "observed_evidence_class": built.evidence_class,
                },
            )
        ),
        "real_task_case_structural_score",
    )
