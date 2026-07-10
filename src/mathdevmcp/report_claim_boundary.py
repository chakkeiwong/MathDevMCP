from __future__ import annotations

"""Classify report-status prose without treating it as a theorem claim."""

import re
from typing import Any

from .contracts import attach_contract


REPORT_CLAIM_BOUNDARY_CONTRACT = "report_claim_boundary_audit"

REPORT_STATUS_PATTERNS: tuple[tuple[str, str], ...] = (
    ("draft_or_report_status", r"\b(report|draft|submission|appendix|section|result note|audit)\b"),
    ("evaluation_status", r"\b(pass(?:ed)?|fail(?:ed)?|ready|blocked|complete|incomplete|validated|reviewed)\b"),
    ("evidence_status", r"\b(evidence|artifact|manifest|ledger|review|diagnostic|benchmark|test|check)\b"),
    ("nonclaim_boundary", r"\b(not a proof|not proof|non-claim|does not claim|diagnostic only|not certified)\b"),
)

THEOREM_PATTERNS: tuple[tuple[str, str], ...] = (
    ("universal_math_claim", r"\b(for all|forall|always|never|unique|converges|equivalent|theorem|lemma|proof)\b"),
    ("formula_claim", r"(=|\\le|\\ge|\\forall|\\exists|\\sum|\\int)"),
)


def _matches(text: str, patterns: tuple[tuple[str, str], ...]) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    for kind, pattern in patterns:
        if re.search(pattern, text, flags=re.IGNORECASE):
            found.append({"kind": kind, "pattern": pattern})
    return found


def _document_evidence_needed(boundary_class: str) -> list[dict[str, str]]:
    common = [
        {
            "kind": "source_locator",
            "description": "A pointer to the report section, result note, run manifest, or review artifact that supports the status claim.",
        },
        {
            "kind": "scope_statement",
            "description": "The exact scope of the claim, including target document, labels, tests, or report slice.",
        },
        {
            "kind": "nonclaim_boundary",
            "description": "Explicit wording that the report-status claim is not a theorem proof or scientific truth claim.",
        },
    ]
    if boundary_class == "report_status_or_nonclaim":
        return [
            *common,
            {
                "kind": "status_evidence",
                "description": "The local checklist, test result, review verdict, or ledger entry that justifies the reported status.",
            },
            {
                "kind": "remaining_gap_statement",
                "description": "Any remaining limitations, missing evidence, or next audit required before stronger claims.",
            },
        ]
    return [
        *common,
        {
            "kind": "math_or_empirical_evidence",
            "description": "A derivation, backend certificate, data artifact, or citation appropriate to the mathematical or scientific claim.",
        },
    ]


def audit_report_claim_boundary(
    claim: str,
    *,
    evidence_snippets: list[str] | None = None,
    source: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a gap/evidence report for report-status or nonclaim prose."""
    snippets = [str(item) for item in (evidence_snippets or []) if str(item).strip()]
    source = dict(source or {})
    text = "\n".join([claim, *snippets])
    report_matches = _matches(text, REPORT_STATUS_PATTERNS)
    theorem_matches = _matches(claim, THEOREM_PATTERNS)
    reportish = bool(report_matches)
    theoremish = bool(theorem_matches) and not reportish
    if reportish:
        boundary_class = "report_status_or_nonclaim"
        mathematical_claim = False
        status = "evidence_requirements"
        reason = "The claim is report-status or nonclaim prose; it needs document evidence, not theorem proof."
        safe_wording = (
            "State this as a scoped report-status claim and cite the supporting artifact; "
            "do not phrase it as a mathematical theorem or scientific truth."
        )
    elif theoremish:
        boundary_class = "mathematical_or_scientific_claim"
        mathematical_claim = True
        status = "needs_math_or_empirical_evidence"
        reason = "The claim appears mathematical or scientific and needs derivation, backend, empirical, or citation support."
        safe_wording = "Do not downgrade this to report-status prose; supply the appropriate mathematical or empirical evidence."
    else:
        boundary_class = "ambiguous_claim_boundary"
        mathematical_claim = False
        status = "needs_boundary_clarification"
        reason = "The claim boundary is ambiguous; classify it before asking for proof or report evidence."
        safe_wording = "Rewrite the claim to say whether it is a report-status assertion, model assumption, empirical statement, or mathematical claim."
    evidence_needed = _document_evidence_needed(boundary_class)
    supplied_evidence_count = len(snippets)
    missing_evidence = [item for item in evidence_needed if supplied_evidence_count == 0 or item["kind"] != "source_locator"]
    overclaim_risks: list[dict[str, str]] = []
    if reportish:
        overclaim_risks.append(
            {
                "kind": "report_status_as_theorem",
                "description": "Asking for proof of report-status prose can hallucinate theorem obligations that the document never claimed.",
            }
        )
    if theoremish and snippets:
        overclaim_risks.append(
            {
                "kind": "evidence_snippet_as_proof",
                "description": "Document snippets can support provenance, but they do not certify a mathematical theorem by themselves.",
            }
        )
    result = {
        "status": status,
        "claim": claim,
        "boundary_class": boundary_class,
        "mathematical_claim": mathematical_claim,
        "reason": reason,
        "matched_boundary_phrases": report_matches,
        "matched_theorem_phrases": theorem_matches,
        "evidence_snippets": snippets,
        "source": source,
        "document_evidence_needed": evidence_needed,
        "missing_evidence": missing_evidence,
        "overclaim_risks": overclaim_risks,
        "safe_wording": safe_wording,
        "next_actions": [
            {
                "code": "attach_document_evidence",
                "description": "Attach the cited report artifact, result note, test output, or review verdict before reusing the claim.",
            },
            {
                "code": "preserve_nonclaim_boundary",
                "description": "Keep theorem/proof language out of report-status claims unless a proof artifact is supplied.",
            },
        ],
        "non_claims": [
            {
                "code": "report_boundary_not_truth_validation",
                "text": "This audit classifies the evidence boundary; it does not validate the truth of the underlying report.",
            },
            {
                "code": "document_evidence_not_proof",
                "text": "Document evidence can support a report-status claim but is not a mathematical proof certificate.",
            },
        ],
        "agent_handoff": {
            "status": status,
            "boundary_class": boundary_class,
            "mathematical_claim": mathematical_claim,
            "evidence_needed": evidence_needed,
            "missing_evidence": missing_evidence,
            "safe_wording": safe_wording,
            "next_action": "Attach document evidence or rewrite claim boundary before requesting proof.",
        },
    }
    return attach_contract(result, REPORT_CLAIM_BOUNDARY_CONTRACT)
