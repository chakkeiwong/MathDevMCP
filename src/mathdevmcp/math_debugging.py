from __future__ import annotations

"""Shared contracts for question-centered mathematical debugging workflows."""

from dataclasses import asdict, dataclass
from typing import Any, Literal

from .contracts import attach_contract


WorkbenchStatus = Literal[
    "proved",
    "refuted",
    "unknown",
    "missing_assumptions",
    "not_encodable",
    "backend_unavailable",
    "inconclusive",
]

EvidenceSeverity = Literal["certifying", "blocking", "diagnostic", "supporting"]

CERTIFICATION_BOUNDARY = (
    "Only deterministic backend certificates for scoped obligations can certify "
    "mathematical claims. Supporting, diagnostic, and numeric evidence must not "
    "be promoted to proof."
)

WORKBENCH_STATUSES: set[str] = {
    "proved",
    "refuted",
    "unknown",
    "missing_assumptions",
    "not_encodable",
    "backend_unavailable",
    "inconclusive",
}

EVIDENCE_SEVERITIES: set[str] = {"certifying", "blocking", "diagnostic", "supporting"}


@dataclass(frozen=True)
class MathQuestion:
    question_type: str
    target: str
    givens: list[str]
    assumptions: list[str]
    context: dict[str, Any]


@dataclass(frozen=True)
class AssumptionRecord:
    text: str
    status: str
    source: str
    necessity: str = "unknown"
    used_by: list[str] | None = None
    route_categories: list[str] | None = None
    route_category_sources: list[str] | None = None


@dataclass(frozen=True)
class BackendAttemptRecord:
    backend: str
    status: str
    reason: str
    evidence: list[dict[str, Any]]
    severity: EvidenceSeverity


@dataclass(frozen=True)
class CounterexampleRecord:
    status: str
    assignments: dict[str, Any]
    lhs_value: Any
    rhs_value: Any
    reason: str
    backend: str
    seed: int | None = None


@dataclass(frozen=True)
class WorkbenchObligation:
    id: str
    lhs: str
    rhs: str
    assumptions: list[str]
    status: WorkbenchStatus
    reason: str
    backend_attempts: list[dict[str, Any]]
    counterexample: dict[str, Any] | None
    missing_assumptions: list[dict[str, Any]]
    provenance: dict[str, Any]


@dataclass(frozen=True)
class WorkbenchResult:
    question: dict[str, Any]
    status: WorkbenchStatus
    reason: str
    obligations: list[dict[str, Any]]
    assumptions: list[dict[str, Any]]
    backend_attempts: list[dict[str, Any]]
    counterexamples: list[dict[str, Any]]
    actions: list[dict[str, Any]]
    certification_boundary: str


def math_question(
    question_type: str,
    target: str,
    *,
    givens: list[str] | None = None,
    assumptions: list[str] | None = None,
    context: dict[str, Any] | None = None,
) -> dict:
    return attach_contract(
        asdict(
            MathQuestion(
                question_type=question_type,
                target=target,
                givens=givens or [],
                assumptions=assumptions or [],
                context=context or {},
            )
        ),
        "math_debugging_question",
    )


def assumption_record(
    text: str,
    *,
    status: str,
    source: str,
    necessity: str = "unknown",
    used_by: list[str] | None = None,
    route_categories: list[str] | None = None,
    route_category_sources: list[str] | None = None,
) -> dict:
    return asdict(
        AssumptionRecord(
            text=text,
            status=status,
            source=source,
            necessity=necessity,
            used_by=used_by or [],
            route_categories=route_categories or [],
            route_category_sources=route_category_sources or [],
        )
    )


def backend_attempt_record(
    *,
    backend: str,
    status: str,
    reason: str,
    evidence: list[dict[str, Any]] | None = None,
    severity: EvidenceSeverity = "diagnostic",
) -> dict:
    if severity not in EVIDENCE_SEVERITIES:
        raise ValueError(f"Unsupported evidence severity: {severity}")
    return asdict(
        BackendAttemptRecord(
            backend=backend,
            status=status,
            reason=reason,
            evidence=evidence or [],
            severity=severity,
        )
    )


def counterexample_record(
    *,
    assignments: dict[str, Any],
    lhs_value: Any,
    rhs_value: Any,
    reason: str,
    backend: str,
    status: str = "found",
    seed: int | None = None,
) -> dict:
    return asdict(
        CounterexampleRecord(
            status=status,
            assignments=assignments,
            lhs_value=lhs_value,
            rhs_value=rhs_value,
            reason=reason,
            backend=backend,
            seed=seed,
        )
    )


def workbench_obligation(
    obligation_id: str,
    *,
    lhs: str,
    rhs: str,
    status: WorkbenchStatus,
    reason: str,
    assumptions: list[str] | None = None,
    backend_attempts: list[dict[str, Any]] | None = None,
    counterexample: dict[str, Any] | None = None,
    missing_assumptions: list[dict[str, Any]] | None = None,
    provenance: dict[str, Any] | None = None,
) -> dict:
    if status not in WORKBENCH_STATUSES:
        raise ValueError(f"Unsupported workbench status: {status}")
    return asdict(
        WorkbenchObligation(
            id=obligation_id,
            lhs=lhs,
            rhs=rhs,
            assumptions=assumptions or [],
            status=status,
            reason=reason,
            backend_attempts=backend_attempts or [],
            counterexample=counterexample,
            missing_assumptions=missing_assumptions or [],
            provenance=provenance or {},
        )
    )


def workbench_result(
    question: dict,
    *,
    status: WorkbenchStatus,
    reason: str,
    obligations: list[dict[str, Any]] | None = None,
    assumptions: list[dict[str, Any]] | None = None,
    backend_attempts: list[dict[str, Any]] | None = None,
    counterexamples: list[dict[str, Any]] | None = None,
    actions: list[dict[str, Any]] | None = None,
) -> dict:
    if status not in WORKBENCH_STATUSES:
        raise ValueError(f"Unsupported workbench status: {status}")
    return attach_contract(
        asdict(
            WorkbenchResult(
                question=question,
                status=status,
                reason=reason,
                obligations=obligations or [],
                assumptions=assumptions or [],
                backend_attempts=backend_attempts or [],
                counterexamples=counterexamples or [],
                actions=actions or [],
                certification_boundary=CERTIFICATION_BOUNDARY,
            )
        ),
        "math_debugging_workbench_result",
    )


def validate_workbench_result(result: dict) -> list[str]:
    errors: list[str] = []
    if result.get("status") not in WORKBENCH_STATUSES:
        errors.append("status is not a supported workbench status")
    if CERTIFICATION_BOUNDARY != result.get("certification_boundary"):
        errors.append("certification_boundary must preserve the MathDevMCP proof boundary")
    for index, attempt in enumerate(result.get("backend_attempts", [])):
        if attempt.get("severity") not in EVIDENCE_SEVERITIES:
            errors.append(f"backend_attempts[{index}].severity is invalid")
    for index, obligation in enumerate(result.get("obligations", [])):
        if obligation.get("status") not in WORKBENCH_STATUSES:
            errors.append(f"obligations[{index}].status is invalid")
        for attempt_index, attempt in enumerate(obligation.get("backend_attempts", [])):
            if attempt.get("severity") not in EVIDENCE_SEVERITIES:
                errors.append(f"obligations[{index}].backend_attempts[{attempt_index}].severity is invalid")
    return errors
