from __future__ import annotations

"""Gap and proposal builders for agent-consumable derivation workflows."""

import re
from typing import Any

from .assumption_gap_proposals import build_assumption_gaps, build_assumption_proposals
from .contracts import attach_contract


DERIVATION_VALIDATION_POLICY = "derivation_evidence_boundary_v1"
DERIVATION_VALIDATION_BOUNDARY = (
    "Only certifying backend attempts or concrete counterexample artifacts can "
    "close a scoped derivation obligation. Diagnostic routes, missing "
    "assumption proposals, and formalization plans are not proof certificates."
)


def _slug(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.lower()).strip("_")
    return slug or "derivation"


def _source_prefix(source: dict[str, Any] | None = None) -> str:
    source = source or {}
    for key in ("label", "block_id", "file", "path"):
        value = source.get(key)
        if isinstance(value, str) and value:
            return _slug(value)
    return "direct_target"


def _location(target: str, source: dict[str, Any] | None = None) -> str:
    source = source or {}
    file = source.get("file") or source.get("path")
    label = source.get("label")
    parent_label = source.get("parent_label")
    line = source.get("line_start")
    if file and parent_label and label and parent_label != label and line:
        return f"{file} > {parent_label} > {label} > line {line}"
    if file and parent_label and label and parent_label != label:
        return f"{file} > {parent_label} > {label}"
    if file and label and line:
        return f"{file} > {label} > line {line}"
    if file and label:
        return f"{file} > {label}"
    if file and line:
        return f"{file} > line {line}"
    if label:
        return str(label)
    return target or "direct target"


def _route_decision(low_level: dict[str, Any]) -> dict[str, Any]:
    route = low_level.get("route_decision")
    return route if isinstance(route, dict) else {}


def _workbench(low_level: dict[str, Any]) -> dict[str, Any]:
    workbench = low_level.get("workbench_result")
    return workbench if isinstance(workbench, dict) else {}


def _obligations(low_level: dict[str, Any]) -> list[dict[str, Any]]:
    obligations = _workbench(low_level).get("obligations")
    return [item for item in obligations if isinstance(item, dict)] if isinstance(obligations, list) else []


def _first_obligation(low_level: dict[str, Any]) -> dict[str, Any]:
    obligations = _obligations(low_level)
    return obligations[0] if obligations else {}


def _backend_attempts(low_level: dict[str, Any]) -> list[dict[str, Any]]:
    attempts: list[dict[str, Any]] = []
    route = _route_decision(low_level)
    if isinstance(route.get("backend_attempt"), dict):
        attempts.append(route["backend_attempt"])
    workbench_attempts = _workbench(low_level).get("backend_attempts")
    if isinstance(workbench_attempts, list):
        attempts.extend(item for item in workbench_attempts if isinstance(item, dict))
    for obligation in _obligations(low_level):
        nested = obligation.get("backend_attempts")
        if isinstance(nested, list):
            attempts.extend(item for item in nested if isinstance(item, dict))
    counterexample_search = low_level.get("counterexample_search")
    if isinstance(counterexample_search, dict):
        counter_workbench = counterexample_search.get("workbench_result")
        nested = counter_workbench.get("backend_attempts") if isinstance(counter_workbench, dict) else None
        if isinstance(nested, list):
            attempts.extend(item for item in nested if isinstance(item, dict))
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for attempt in attempts:
        marker = repr(sorted((str(key), repr(value)) for key, value in attempt.items()))
        if marker not in seen:
            deduped.append(attempt)
            seen.add(marker)
    return deduped


def _counterexamples(low_level: dict[str, Any]) -> list[dict[str, Any]]:
    counterexamples: list[dict[str, Any]] = []
    search = low_level.get("counterexample_search")
    if isinstance(search, dict) and isinstance(search.get("counterexample"), dict):
        counterexamples.append(search["counterexample"])
    workbench_items = _workbench(low_level).get("counterexamples")
    if isinstance(workbench_items, list):
        counterexamples.extend(item for item in workbench_items if isinstance(item, dict))
    for obligation in _obligations(low_level):
        if isinstance(obligation.get("counterexample"), dict):
            counterexamples.append(obligation["counterexample"])
    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for counterexample in counterexamples:
        marker = repr(sorted((str(key), repr(value)) for key, value in counterexample.items()))
        if marker not in seen:
            deduped.append(counterexample)
            seen.add(marker)
    return deduped


def _assumption_diagnostic(low_level: dict[str, Any]) -> dict[str, Any]:
    diagnostic = low_level.get("assumption_diagnostic")
    return diagnostic if isinstance(diagnostic, dict) else {}


def _missing_assumptions(low_level: dict[str, Any]) -> list[dict[str, Any]]:
    diagnostic = _assumption_diagnostic(low_level)
    raw = diagnostic.get("missing_assumptions")
    if not raw:
        raw = _workbench(low_level).get("assumptions")
    if not raw:
        obligation = _first_obligation(low_level)
        raw = obligation.get("missing_assumptions")
    return [item for item in raw if isinstance(item, dict)] if isinstance(raw, list) else []


def _target(low_level: dict[str, Any]) -> str:
    return str(low_level.get("target", ""))


def _lhs(low_level: dict[str, Any]) -> str:
    return str(low_level.get("lhs", ""))


def _rhs(low_level: dict[str, Any]) -> str:
    return str(low_level.get("rhs", ""))


def _evidence_refs_for_attempts(attempts: list[dict[str, Any]]) -> list[str]:
    refs: list[str] = []
    for attempt in attempts:
        backend = _slug(str(attempt.get("backend", "backend")))
        status = _slug(str(attempt.get("status", "unknown")))
        refs.append(f"backend_attempt:{backend}:{status}")
        evidence = attempt.get("evidence")
        if isinstance(evidence, list):
            for item in evidence:
                if isinstance(item, dict) and item.get("kind"):
                    refs.append(f"backend_evidence:{_slug(str(item['kind']))}")
    return refs


def _evidence_refs(low_level: dict[str, Any]) -> list[str]:
    refs = ["derive_or_refute_result"]
    route = _route_decision(low_level)
    if route.get("route"):
        refs.append(f"route:{_slug(str(route['route']))}")
    refs.extend(_evidence_refs_for_attempts(_backend_attempts(low_level)))
    for assumption in _missing_assumptions(low_level):
        sources = assumption.get("route_category_sources")
        if isinstance(sources, list):
            refs.extend(str(item) for item in sources if isinstance(item, str))
    counterexample_search = low_level.get("counterexample_search")
    if isinstance(counterexample_search, dict):
        refs.append(f"counterexample_search:{_slug(str(counterexample_search.get('status', 'unknown')))}")
    deduped: list[str] = []
    seen: set[str] = set()
    for ref in refs:
        if ref not in seen:
            deduped.append(ref)
            seen.add(ref)
    return deduped


def _problem_for_status(status: str, low_level: dict[str, Any]) -> str:
    if status == "proved":
        return "The scoped derivation obligation is closed by backend certificate evidence."
    if status == "refuted":
        if _counterexamples(low_level):
            return "The scoped derivation obligation is refuted by a concrete counterexample artifact."
        return "The low-level route reported refutation, but no concrete counterexample artifact is attached."
    if status == "missing_assumptions":
        return "The derivation route is blocked by missing route-required assumptions."
    if status == "not_encodable":
        return "The target is not encodable by the current bounded derivation route."
    if status == "backend_unavailable":
        return "The requested derivation backend is unavailable in this environment."
    return "No bounded derivation or refutation was found for the scoped target."


def _why_for_status(status: str, low_level: dict[str, Any]) -> str:
    route = _route_decision(low_level)
    route_reason = str(route.get("reason", "")).strip()
    if status == "proved":
        return "A backend attempt with certifying severity proved the normalized lhs/rhs obligation."
    if status == "refuted":
        if _counterexamples(low_level):
            return "The counterexample gives assignments for which lhs and rhs evaluate to different values."
        return "High-level derivation workflows require a concrete counterexample artifact before promoting a refutation."
    if status == "missing_assumptions":
        return "The route uses operations whose domain, shape, regularity, probability, or economic assumptions must be stated before the derivation is well posed."
    if status == "not_encodable":
        return route_reason or "The expression falls outside the conservative parser or backend grammar."
    if status == "backend_unavailable":
        return route_reason or "The selected deterministic backend could not be imported or run."
    if route_reason:
        return route_reason
    return "The bounded tools did not find a proof certificate, counterexample, or concrete missing-assumption route."


def _severity_for_status(status: str, low_level: dict[str, Any]) -> str:
    if status == "proved":
        return "closed"
    if status == "refuted":
        return "blocking" if _counterexamples(low_level) else "high"
    if status == "missing_assumptions":
        return "high"
    if status in {"not_encodable", "backend_unavailable"}:
        return "medium"
    return "medium"


def build_derivation_gaps(
    low_level: dict[str, Any],
    *,
    source: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Convert a derivation result into stable, agent-consumable gap records."""
    status = str(low_level.get("status", "unknown"))
    target = _target(low_level)
    source_context = dict(source or {})
    gap_id = f"derivation_gap_{_source_prefix(source)}_{_slug(status)}_1"
    base_gap = {
        "id": gap_id,
        "location": _location(target, source),
        "target": target,
        "lhs": _lhs(low_level),
        "rhs": _rhs(low_level),
        "status": status,
        "problem": _problem_for_status(status, low_level),
        "why": _why_for_status(status, low_level),
        "failed_route": {
            "route": _route_decision(low_level).get("route"),
            "status": _route_decision(low_level).get("status"),
            "reason": _route_decision(low_level).get("reason"),
        },
        "missing_assumptions": _missing_assumptions(low_level),
        "backend_attempts": _backend_attempts(low_level),
        "counterexamples": _counterexamples(low_level),
        "evidence_refs": _evidence_refs(low_level),
        "severity": _severity_for_status(status, low_level),
        "source_context": source_context,
    }
    if status == "missing_assumptions":
        assumption_gaps = build_assumption_gaps(target, _missing_assumptions(low_level), source=source)
        base_gap["assumption_gaps"] = assumption_gaps
        base_gap["problem"] = f"{base_gap['problem']} Missing assumption gaps: {len(assumption_gaps)}."
    return [base_gap]


def _backend_plan_for_status(status: str, gap: dict[str, Any]) -> list[dict[str, Any]]:
    if status == "proved":
        return [
            {
                "tool": "accept_backend_certificate",
                "reason": "Use the existing certifying backend attempt as the scoped derivation artifact.",
                "expected_artifact": "backend_certificate",
            }
        ]
    if status == "refuted":
        return [
            {
                "tool": "accept_counterexample",
                "reason": "Use the concrete counterexample artifact as the scoped refutation artifact.",
                "expected_artifact": "counterexample",
            }
        ]
    if status == "missing_assumptions":
        return [
            {
                "tool": "assumptions_required",
                "reason": "Recover route-required assumptions before retrying deterministic derivation.",
                "expected_artifact": "assumption_gap_proposals",
            },
            {
                "tool": "derive_or_refute",
                "reason": "Rerun the scoped derivation after assumptions are explicitly supplied.",
                "expected_artifact": "proof_certificate_or_counterexample_or_named_gap",
            },
        ]
    if status == "backend_unavailable":
        backend_names = sorted(
            {
                str(attempt.get("backend"))
                for attempt in gap.get("backend_attempts", [])
                if isinstance(attempt, dict) and attempt.get("backend")
            }
        )
        return [
            {
                "tool": "configure_backend",
                "reason": "Install or select the deterministic backend before retrying.",
                "expected_artifact": "backend_availability_check",
                "backend": ", ".join(backend_names) if backend_names else "selected backend",
            }
        ]
    return [
        {
            "tool": "formalize_claim",
            "reason": "Convert the target into a typed obligation with explicit domains and operators.",
            "expected_artifact": "typed_obligation",
        },
        {
            "tool": "derive_or_refute",
            "reason": "Retry with the strongest available deterministic backend after formalization.",
            "expected_artifact": "proof_certificate_or_counterexample_or_named_gap",
        },
    ]


def _formalization_target(status: str, gap: dict[str, Any]) -> dict[str, Any]:
    return {
        "target": gap.get("target", ""),
        "lhs": gap.get("lhs", ""),
        "rhs": gap.get("rhs", ""),
        "required_fields": [
            "typed lhs/rhs",
            "domains of each symbol",
            "operator semantics",
            "explicit assumptions used by backend route",
        ],
        "needed_before_claim": status not in {"proved", "refuted"},
    }


def _derivation_route_for_status(status: str, gap: dict[str, Any]) -> list[dict[str, str]]:
    if status == "proved":
        return [
            {
                "step": "Use certifying backend evidence",
                "detail": "The backend attempt has certifying severity and status `proved` for the scoped lhs/rhs obligation.",
            },
            {
                "step": "Preserve scope",
                "detail": "Treat the result as a scoped derivation certificate only for the encoded target and assumptions.",
            },
        ]
    if status == "refuted" and gap.get("counterexamples"):
        return [
            {
                "step": "Inspect counterexample",
                "detail": "Use the attached assignments and lhs/rhs values to show the equality fails.",
            },
            {
                "step": "Revise target or assumptions",
                "detail": "Either weaken the claim, add assumptions that exclude the counterexample, or replace the false equality.",
            },
        ]
    if status == "missing_assumptions":
        return [
            {
                "step": "State route assumptions",
                "detail": "Apply the linked assumption proposals before treating the derivation as well posed.",
            },
            {
                "step": "Rerun deterministic route",
                "detail": "Call derive_or_refute with the proposed assumptions as explicit assumptions, not free-form givens.",
            },
            {
                "step": "Accept only backend closure",
                "detail": "Promote the derivation only if a backend certificate or concrete counterexample is returned.",
            },
        ]
    if status == "backend_unavailable":
        return [
            {
                "step": "Make backend available",
                "detail": "Configure the requested deterministic backend or select an installed backend with an equivalent contract.",
            },
            {
                "step": "Rerun obligation",
                "detail": "Retry the same scoped lhs/rhs obligation and preserve backend attempt evidence.",
            },
        ]
    return [
        {
            "step": "Formalize source claim",
            "detail": "Make symbol types, domains, operator semantics, and assumptions explicit.",
        },
        {
            "step": "Choose deterministic route",
            "detail": "Route to SymPy, Lean, Sage, or another configured backend only after the target is encodable.",
        },
        {
            "step": "Return named residual gap",
            "detail": "If no backend closes the target, report the unresolved typed obligation instead of a generic review request.",
        },
    ]


def _proposal_type_for_status(status: str, gap: dict[str, Any]) -> str:
    if status == "proved":
        return "accept_backend_certificate"
    if status == "refuted":
        return "accept_counterexample" if gap.get("counterexamples") else "manual_review_with_named_gap"
    if status == "missing_assumptions":
        return "add_assumptions"
    if status == "backend_unavailable":
        return "try_backend_proof"
    if status == "not_encodable":
        return "formalize_target"
    return "formalize_target"


def _proposal_text_for_status(status: str, gap: dict[str, Any]) -> str:
    if status == "proved":
        return "Accept the scoped backend certificate as the derivation artifact for this encoded obligation."
    if status == "refuted":
        if gap.get("counterexamples"):
            return "Accept the attached counterexample as a refutation of the scoped equality, then revise the source claim or assumptions."
        return "Do not promote the refutation until a concrete counterexample artifact is attached."
    if status == "missing_assumptions":
        return "Add or verify the linked route-required assumptions, then rerun the deterministic derivation route."
    if status == "backend_unavailable":
        return "Configure the requested deterministic backend or reroute to an available backend before making a proof/refutation claim."
    if status == "not_encodable":
        return "Formalize the claim into typed lhs/rhs, domains, operators, and explicit assumptions before retrying a backend."
    return "Produce a typed obligation and retry deterministic proof or counterexample search; keep the current result as an unresolved named derivation gap."


def _validation_for_status(proposal: dict[str, Any], gap: dict[str, Any]) -> dict[str, Any]:
    status = str(gap.get("status", "unknown"))
    certifying_attempt = any(
        isinstance(attempt, dict)
        and attempt.get("status") == "proved"
        and attempt.get("severity") == "certifying"
        for attempt in gap.get("backend_attempts", [])
    )
    blocking_counterexample = bool(gap.get("counterexamples"))
    if status == "proved" and certifying_attempt:
        validation_status = "certified_by_backend"
        certifying = True
        reason = "The proposal is backed by a certifying backend attempt."
    elif status == "refuted" and blocking_counterexample:
        validation_status = "refuted_by_counterexample"
        certifying = True
        reason = "The proposal is backed by a concrete counterexample artifact."
    elif status == "missing_assumptions":
        validation_status = "blocked_by_missing_assumptions"
        certifying = False
        reason = "The proposal names route-required assumptions but does not prove the target."
    elif status == "backend_unavailable":
        validation_status = "blocked_by_backend_unavailable"
        certifying = False
        reason = "The required backend evidence was not available."
    elif status == "not_encodable":
        validation_status = "blocked_by_not_encodable"
        certifying = False
        reason = "The target is not yet encoded for deterministic proof or refutation."
    else:
        validation_status = "abstained_no_certifying_route"
        certifying = False
        reason = "No certifying proof, concrete counterexample, or concrete missing-assumption repair closed the target."
    return {
        "policy": DERIVATION_VALIDATION_POLICY,
        "status": validation_status,
        "certifying": certifying,
        "reason": reason,
        "backend_attempts": list(gap.get("backend_attempts", [])),
        "counterexample_count": len(gap.get("counterexamples", [])) if isinstance(gap.get("counterexamples"), list) else 0,
        "boundary": DERIVATION_VALIDATION_BOUNDARY,
        "gap_id": gap.get("id"),
        "proposal_id": proposal.get("id"),
    }


def _assumption_repairs_for_gap(gap: dict[str, Any]) -> list[dict[str, Any]]:
    assumption_gaps = gap.get("assumption_gaps")
    if not isinstance(assumption_gaps, list) or not assumption_gaps:
        return []
    return build_assumption_proposals([item for item in assumption_gaps if isinstance(item, dict)])


def build_derivation_proposals(gaps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build concrete derivation proposals linked to derivation gaps."""
    proposals: list[dict[str, Any]] = []
    for index, gap in enumerate(gaps, start=1):
        status = str(gap.get("status", "unknown"))
        proposal = {
            "id": f"derivation_proposal_{_slug(str(gap.get('id', index)))}",
            "gap_ids": [gap["id"]],
            "type": _proposal_type_for_status(status, gap),
            "location": gap.get("location", ""),
            "proposal_text": _proposal_text_for_status(status, gap),
            "derivation_route": _derivation_route_for_status(status, gap),
            "formalization_target": _formalization_target(status, gap),
            "backend_plan": _backend_plan_for_status(status, gap),
            "assumption_repairs": _assumption_repairs_for_gap(gap),
            "evidence_refs": list(gap.get("evidence_refs", [])),
            "application_status": "not_applied",
        }
        proposal["validation"] = _validation_for_status(proposal, gap)
        proposals.append(proposal)
    return proposals


def summarize_derivation_validation(proposals: list[dict[str, Any]]) -> dict[str, Any]:
    statuses: dict[str, int] = {}
    certifying_count = 0
    attempts = 0
    counterexamples = 0
    for proposal in proposals:
        validation = proposal.get("validation") if isinstance(proposal.get("validation"), dict) else {}
        status = str(validation.get("status", "missing"))
        statuses[status] = statuses.get(status, 0) + 1
        if validation.get("certifying") is True:
            certifying_count += 1
        backend_attempts = validation.get("backend_attempts")
        if isinstance(backend_attempts, list):
            attempts += len(backend_attempts)
        if isinstance(validation.get("counterexample_count"), int):
            counterexamples += validation["counterexample_count"]
    return {
        "policy": DERIVATION_VALIDATION_POLICY,
        "status_counts": statuses,
        "proposal_count": len(proposals),
        "certifying_proposal_count": certifying_count,
        "backend_attempt_count": attempts,
        "counterexample_count": counterexamples,
        "boundary": DERIVATION_VALIDATION_BOUNDARY,
    }


def build_derivation_tool_uses(
    target: str,
    *,
    givens: list[str] | None = None,
    assumptions: list[str] | None = None,
    backend: str = "auto",
    source_tool: str = "derive_or_refute",
) -> list[dict[str, Any]]:
    return [
        {
            "tool": source_tool,
            "arguments": {
                "target": target,
                "givens": list(givens or []),
                "assumptions": list(assumptions or []),
                "backend": backend,
            },
            "purpose": "Run deterministic proof/refutation routing and bounded counterexample search for the scoped derivation target.",
            "status": "completed",
            "output_contract": "derive_or_refute_result",
        },
        {
            "tool": "build_derivation_gaps",
            "arguments": {"target": target},
            "purpose": "Convert low-level derivation evidence into named gap records with proof/refutation boundaries.",
            "status": "completed",
            "output_contract": "derivation_gap_list",
        },
        {
            "tool": "build_derivation_proposals",
            "arguments": {"gap_count": "derived"},
            "purpose": "Create concrete derivation proposals linked to each gap.",
            "status": "completed",
            "output_contract": "derivation_proposal_list",
        },
    ]


def build_derivation_gap_proposal_packet(
    low_level: dict[str, Any],
    *,
    source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a complete internal packet for later high-level workflow wiring."""
    gaps = build_derivation_gaps(low_level, source=source)
    proposals = build_derivation_proposals(gaps)
    return attach_contract(
        {
            "status": str(low_level.get("status", "unknown")),
            "target": _target(low_level),
            "gaps": gaps,
            "proposals": proposals,
            "validation": summarize_derivation_validation(proposals),
            "tool_uses": build_derivation_tool_uses(
                _target(low_level),
                givens=low_level.get("givens") if isinstance(low_level.get("givens"), list) else [],
            ),
            "agent_handoff": {
                "scoped_target": _target(low_level),
                "status": str(low_level.get("status", "unknown")),
                "gap_count": len(gaps),
                "proposal_count": len(proposals),
                "derivation_gap_ledger": gaps,
                "proposals": proposals,
                "validation_boundary": DERIVATION_VALIDATION_BOUNDARY,
                "next_artifact": "Use proposal backend plans and linked assumption repairs before editing source text or claiming closure.",
            },
        },
        "derivation_gap_proposal_packet",
    )
