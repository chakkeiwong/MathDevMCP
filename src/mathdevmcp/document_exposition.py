"""Context-aware mathematical-exposition roles and issue projection."""

from __future__ import annotations

import re
from typing import Any, Iterable

from .contracts import attach_contract
from .evidence_manifest import content_digest


EXPOSITION_CONTRACT = "document_exposition_issue_projection"
ACTIONABLE_STATUSES = frozenset({"actionable_patch", "actionable_assumption_text"})


def _context_paragraphs(target: dict[str, Any]) -> list[dict[str, Any]]:
    context = target.get("exposition_context")
    if not isinstance(context, dict):
        return []
    paragraphs = context.get("paragraphs")
    return [item for item in paragraphs if isinstance(item, dict)] if isinstance(paragraphs, list) else []


def _context_text(target: dict[str, Any]) -> str:
    return "\n".join(str(item.get("text", "")) for item in _context_paragraphs(target))


def _contains_inverse(text: str) -> bool:
    compact = re.sub(r"\s+", "", text)
    return "^{-1}" in compact or "\\inv" in compact


def _contains_power_series(text: str) -> bool:
    compact = re.sub(r"\s+", "", text)
    return any(token in compact for token in ("\\Omega^2", "\\Omega^{2}", "\\cdots", "\\sum"))


def _role_evidence(
    role: str,
    source: str,
    cue: str,
    target: dict[str, Any],
    *,
    source_spans: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    evidence = {
        "role": role,
        "authority": "source_evidenced_role" if source == "source_context" else "inferred_structural_role",
        "source": source,
        "cue": cue,
        "location": target.get("location"),
        "non_claim": "Equation role controls exposition routing only; it does not establish truth or proof.",
    }
    if source_spans:
        evidence["source_spans"] = source_spans
    return evidence


def _cue_spans(target: dict[str, Any], cues: tuple[str, ...]) -> list[dict[str, Any]]:
    return _supporting_paragraphs(
        target,
        lambda value: any(cue in value.lower() for cue in cues),
    )


def classify_exposition_roles(target: dict[str, Any]) -> list[dict[str, Any]]:
    """Classify one display using exact source context and bounded structure."""
    text = str(target.get("text") or "")
    context = _context_text(target)
    lowered = context.lower()
    roles: list[dict[str, Any]] = []

    routing = target.get("routing_role")
    if isinstance(routing, dict) and routing.get("role") not in {None, "unsupported_or_ambiguous"}:
        roles.append(
            _role_evidence(
                str(routing["role"]),
                "existing_routing_role",
                str(routing.get("source", {}).get("cue_text", "")),
                target,
            )
        )

    definition_cues = (
        " is defined",
        " are defined",
        "defined by",
        "define the",
        "we define",
        "is the leontief",
        "leontief object",
        "leontief inverse",
    )
    if any(cue in lowered for cue in definition_cues) or (
        "leontief" in lowered and _contains_inverse(text) and text.lstrip().startswith("\\mathcal{L}")
    ):
        roles.append(
            _role_evidence(
                "definition",
                "source_context",
                "definition cue",
                target,
                source_spans=_cue_spans(target, definition_cues + ("leontief",)),
            )
        )

    if _contains_inverse(text) and _contains_power_series(text):
        roles.append(
            _role_evidence(
                "conditional_identity",
                "inferred_structure",
                "inverse equals matrix-power series",
                target,
            )
        )

    assumption_cues = (
        "maintained assumption",
        "maintains constant returns",
        "source-stated maintained",
        "suppose that",
        "we assume",
        "assume that",
    )
    if any(cue in lowered for cue in assumption_cues):
        roles.append(
            _role_evidence(
                "maintained_assumption",
                "source_context",
                "maintained-assumption cue",
                target,
                source_spans=_cue_spans(target, assumption_cues),
            )
        )

    if "accounting identity" in lowered or "is an identity" in lowered:
        roles.append(
            _role_evidence(
                "accounting_identity",
                "source_context",
                "accounting-identity cue",
                target,
                source_spans=_cue_spans(target, ("accounting identity", "is an identity")),
            )
        )

    deduped: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in roles:
        if item["role"] not in seen:
            deduped.append(item)
            seen.add(item["role"])
    if not deduped:
        deduped.append(_role_evidence("unknown", "no_decisive_cue", "", target))
    return deduped


def enrich_targets_with_exposition_roles(targets: list[dict[str, Any]]) -> list[dict[str, Any]]:
    enriched: list[dict[str, Any]] = []
    for target in targets:
        roles = classify_exposition_roles(target)
        enriched.append(
            {
                **target,
                "equation_roles": [item["role"] for item in roles],
                "equation_role_evidence": roles,
                "role_nonclaim": "Role classification is source/structure evidence, not mathematical certification.",
            }
        )
    return enriched


def _supporting_paragraphs(target: dict[str, Any], predicate) -> list[dict[str, Any]]:
    support: list[dict[str, Any]] = []
    for paragraph in _context_paragraphs(target):
        text = str(paragraph.get("text", ""))
        if predicate(text):
            support.append(
                {
                    "file": target.get("exposition_context", {}).get("file"),
                    "line_start": paragraph.get("line_start"),
                    "line_end": paragraph.get("line_end"),
                    "text": text,
                }
            )
    return support


def _unique_spans(items: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[tuple[Any, ...]] = set()
    for item in items:
        key = (item.get("file"), item.get("line_start"), item.get("line_end"), item.get("text"))
        if key not in seen:
            result.append(item)
            seen.add(key)
    return result


def _raw_refs(raw_gaps: list[dict[str, Any]], label: str) -> list[str]:
    marker = f":{label}:"
    refs = [
        str(ref)
        for gap in raw_gaps
        for ref in gap.get("evidence_refs", [])
        if marker in str(ref)
    ]
    return list(dict.fromkeys(refs)) or [f"document_exposition:{label}"]


def _raw_subevidence(raw_gaps: list[dict[str, Any]], label: str) -> list[dict[str, Any]]:
    marker = f":{label}:"
    result: list[dict[str, Any]] = []
    for gap in raw_gaps:
        if any(marker in str(ref) for ref in gap.get("evidence_refs", [])):
            result.append(
                {
                    "kind": gap.get("kind"),
                    "name": gap.get("label"),
                    "problem": gap.get("problem"),
                    "evidence_refs": gap.get("evidence_refs", []),
                }
            )
    return result


def _inverse_issue(target: dict[str, Any], raw_gaps: list[dict[str, Any]]) -> dict[str, Any]:
    label = str(target["label"])
    text = str(target.get("text") or "")
    has_series = _contains_power_series(text)
    dimensions = _supporting_paragraphs(
        target,
        lambda value: bool(
            re.search(r"\\Omega\s*\\in\s*\\mathbb\{R\}\^\{J\\times J\}", value)
            or ("matrix" in value.lower() and "j\\times j" in re.sub(r"\s+", "", value.lower()))
        ),
    )
    invertibility = _supporting_paragraphs(
        target,
        lambda value: "is invertible" in value.lower() or "nonsingular" in value.lower(),
    )
    convergence = _supporting_paragraphs(
        target,
        lambda value: "neumann" in value.lower()
        and any(token in value.lower() for token in ("converges", "convergence", "requires"))
        and bool(re.search(r"\\rho\s*\(\s*\\Omega\s*\)\s*<\s*1", value)),
    ) if has_series else []
    obligation_support = {
        "dimension_contract": dimensions,
        "invertibility": invertibility,
    }
    if has_series:
        obligation_support["neumann_convergence"] = convergence
    unresolved = [name for name, support in obligation_support.items() if not support]
    all_support = _unique_spans(item for values in obligation_support.values() for item in values)
    status = "resolved_by_existing_context" if not unresolved else (
        "partially_resolved" if all_support else "unresolved"
    )
    family = "matrix-domain-and-neumann-convergence" if has_series else "matrix-domain-and-invertibility"
    issue_id = f"{label}/{family}"
    candidate_patch = None
    if unresolved:
        candidate_patch = (
            r"Let $\Omega\in\mathbb{R}^{J\times J}$ and suppose $\rho(\Omega)<1$. "
            r"Then $I-\Omega$ is invertible and the Neumann series converges, so "
            r"$(I-\Omega)^{-1}=\sum_{n=0}^{\infty}\Omega^n$."
            if has_series
            else r"State a condition ensuring that the displayed inverse operand is invertible."
        )
    issue = {
        "issue_id": issue_id,
        "id": issue_id,
        "label": label,
        "family": family,
        "status": status,
        "roles": list(target.get("equation_roles", [])),
        "location": target.get("location"),
        "subevidence": list(obligation_support),
        "obligation_support": obligation_support,
        "existing_context_support": all_support,
        "unresolved_obligations": unresolved,
        "route_evidence": _raw_subevidence(raw_gaps, label),
        "evidence_refs": _raw_refs(raw_gaps, label),
        "candidate_patch": candidate_patch,
        "patch_class": "candidate_exposition_patch_not_certificate" if candidate_patch else None,
        "math_nonclaim": (
            "This status reports whether the document states the scoped exposition conditions. "
            "It does not certify the matrix theorem or source-specific validity."
        ),
    }
    issue["issue_digest"] = content_digest(issue)
    return issue


def _fallback_issue(target: dict[str, Any], raw_gaps: list[dict[str, Any]]) -> dict[str, Any] | None:
    label = str(target.get("label") or "")
    raw = _raw_subevidence(raw_gaps, label)
    if not raw:
        return None
    roles = set(target.get("equation_roles", []))
    if roles <= {"definition", "maintained_assumption", "accounting_identity"}:
        status = "resolved_by_existing_context"
        unresolved: list[str] = []
    elif "maintained_assumption" in roles and all(item.get("name") in {"obligation_1", "obligation_2"} for item in raw):
        status = "resolved_by_existing_context"
        unresolved = []
    else:
        status = "needs_formalization"
        unresolved = sorted({str(item.get("name") or item.get("kind")) for item in raw})
    issue_id = f"{label}/formalization-and-source-role"
    issue = {
        "issue_id": issue_id,
        "id": issue_id,
        "label": label,
        "family": "formalization-and-source-role",
        "status": status,
        "roles": list(target.get("equation_roles", [])),
        "location": target.get("location"),
        "subevidence": raw,
        "existing_context_support": [],
        "unresolved_obligations": unresolved,
        "route_evidence": raw,
        "evidence_refs": _raw_refs(raw_gaps, label),
        "candidate_patch": None,
        "patch_class": None,
        "math_nonclaim": "Formalization status is diagnostic and does not establish truth or falsehood.",
    }
    issue["issue_digest"] = content_digest(issue)
    return issue


def build_exposition_projection(
    targets: list[dict[str, Any]],
    raw_gaps: list[dict[str, Any]],
) -> dict[str, Any]:
    """Aggregate proof routes into one source-aware human issue per family."""
    enriched = enrich_targets_with_exposition_roles(targets)
    issues: list[dict[str, Any]] = []
    for target in enriched:
        label = str(target.get("label") or "")
        text = str(target.get("text") or "")
        if _contains_inverse(text):
            issues.append(_inverse_issue(target, raw_gaps))
        else:
            if not _raw_subevidence(raw_gaps, label):
                continue
            issue = _fallback_issue(target, raw_gaps)
            if issue is not None:
                issues.append(issue)

    gaps: list[dict[str, Any]] = []
    proposals: list[dict[str, Any]] = []
    for issue in issues:
        if issue["status"] == "resolved_by_existing_context":
            continue
        label = str(issue["label"])
        gap = {
            "id": issue["issue_id"],
            "issue_id": issue["issue_id"],
            "label": "invertibility_required" if issue["family"].startswith("matrix-domain") else label,
            "target_label": label,
            "kind": "exposition_obligation",
            "status": issue["status"],
            "substantive_classification": "concrete_repair" if issue.get("candidate_patch") else "diagnostic_abstention",
            "location": issue.get("location"),
            "problem": "The displayed inverse/series lacks required local exposition conditions."
            if issue["family"].startswith("matrix-domain")
            else "The equation role or derivation remains unresolved.",
            "why_mathematically_problematic": (
                "Inverse notation requires an invertible operand. The displayed Neumann series additionally "
                "requires a convergence condition; positive definiteness is only one structured sufficient condition."
                if issue["family"].startswith("matrix-domain")
                else "The source does not yet distinguish a definition, assumption, identity, or derived claim clearly enough for routing."
            ),
            "unresolved_obligations": issue["unresolved_obligations"],
            "existing_context_support": issue["existing_context_support"],
            "evidence_refs": issue["evidence_refs"],
        }
        gaps.append(gap)
        if issue.get("candidate_patch"):
            proposals.append(
                {
                    "id": f"proposal:{issue['issue_id']}",
                    "issue_id": issue["issue_id"],
                    "gap_ids": [issue["issue_id"]],
                    "label": label,
                    "status": "actionable_assumption_text",
                    "substantive_classification": "concrete_repair",
                    "patch_class": issue["patch_class"],
                    "candidate_patch": issue["candidate_patch"],
                    "assumption_statement": issue["candidate_patch"],
                    "replacement_latex": "",
                    "proposed_fix": issue["candidate_patch"],
                    "requires_human_review": True,
                    "backend_evidence": {
                        "status": "not_requested_for_exposition_patch",
                        "reason": "The patch states a standard sufficient condition; it is not a proof certificate.",
                    },
                    "evidence_refs": issue["evidence_refs"],
                }
            )
    result = {
        "targets": enriched,
        "issues": issues,
        "gaps": gaps,
        "proposals": proposals,
        "status_counts": {
            status: sum(1 for issue in issues if issue["status"] == status)
            for status in sorted({str(issue["status"]) for issue in issues})
        },
        "non_claims": [
            "Context closure is a source-exposition observation, not mathematical proof.",
            "Candidate exposition patches require human review and do not certify source-specific validity.",
        ],
    }
    return attach_contract(result, EXPOSITION_CONTRACT)
