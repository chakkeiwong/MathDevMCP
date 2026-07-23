"""Bounded, source-only relationship validators for the applied-math IR.

These checks intentionally return tensions unless a closed numerical target is
available. They never execute user code and never infer a scientific meaning
from a keyword alone.
"""

from __future__ import annotations

import re
from typing import Any

from .applied_math_ir import evidence_chain


def _packet_refs(text: str, packets: list[dict[str, Any]], excerpt: str) -> list[str]:
    folded = excerpt.casefold()
    refs = [
        str(packet["id"])
        for packet in packets
        if folded and folded[:80] in str(packet.get("raw_text", "")).casefold()
    ]
    if refs:
        return refs
    return [str(packet["id"]) for packet in packets if packet.get("kind") in {"equation", "equation_candidate"}][:2]


def _finding(
    *,
    finding_id: str,
    family: str,
    summary: str,
    excerpt: str,
    packets: list[dict[str, Any]],
    disposition: str = "supported_tension",
    severity: str = "medium",
    check_id: str,
) -> dict[str, Any]:
    packet_ids = _packet_refs(excerpt, packets, excerpt)
    return {
        "id": f"finding:{finding_id}",
        "family": family,
        "disposition": disposition,
        "severity": severity,
        "summary": summary,
        "source_anchor": {
            "evidence_tier": "source_text_relationship_check",
            "excerpt": re.sub(r"\s+", " ", excerpt)[:500],
        },
        "evidence": {"excerpt": re.sub(r"\s+", " ", excerpt)[:500]},
        "evidence_chain": evidence_chain(
            finding_id=f"finding:{finding_id}",
            packet_ids=packet_ids,
            check_id=check_id,
            result={"disposition": disposition, "severity": severity},
        ),
    }


def run_generic_relationship_validators(
    source_text: str,
    packets: list[dict[str, Any]],
    claim_ir: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Return only source-supported relationship tensions.

    Patterns identify a relationship candidate; the report remains explicit
    that source/code semantic equivalence and author intent are not checked.
    """

    findings: list[dict[str, Any]] = []
    patterns = (
        (
            "level-linearization-boundary",
            "approximation_linearization",
            r"(?:steady[- ]state|equilibrium).{0,220}(?:zero|0).{0,220}(?:log[- ]deviation|log deviation|relative deviation)",
            "The level statement and log-deviation statement require an explicit positive-level or absolute-deviation convention.",
            "relationship:level_to_linearized_domain",
        ),
        (
            "ownership-domain-transition",
            "accounting_aggregation",
            r"(?:entrant|new participant|new cohort).{0,260}(?:share|starting capital|initial wealth).{0,260}(?:prior[- ]period holdings|held assets|total assets)",
            "The entrant-capital relation names an ownership domain; comparison with total stocks must preserve bank-held versus aggregate holdings.",
            "relationship:ownership_domain",
        ),
        (
            "level-return-linearization",
            "algebra_calculus",
            r"(?:long[- ]maturity|bond)\s+(?:return|price).{0,180}(?:price|quotient).{0,180}(?:negative|=|coefficient).{0,180}(?:deviation|return)",
            "The level return relation and its linearized movement require a checked differentiation and coefficient identity; the source text alone leaves a sign/parameter branch to resolve.",
            "relationship:level_to_linearized_return",
        ),
        (
            "sdf-normalization-sign",
            "probability_statistics",
            r"(?:stochastic discount factor|pricing kernel).{0,120}(?:return|payoff).{0,180}=\s*1.{0,260}(?:linearized|deviation).{0,160}(?:return|discount)",
            "A stated stochastic-discount-factor normalization is paired with a linearized return term; its sign and date require a checked derivation under the source timing convention.",
            "relationship:sdf_normalization_to_linearization",
        ),
        (
            "entrant-asset-domain",
            "accounting_aggregation",
            r"(?:entrant|new cohort).{0,180}(?:capital|loan|bond holdings).{0,180}(?:government bond|security).{0,220}(?:total|aggregate|asset holdings)",
            "The entrant-stock relation uses an asset ownership domain that must not be silently replaced by aggregate household or central-bank holdings.",
            "relationship:entrant_asset_domain",
        ),
        (
            "external-model-closure",
            "document_completeness",
            r"(?:full set of|additional)\s+(?:equilibrium\s+)?equations.{0,260}(?:github|yaml|external)",
            "The model boundary depends on an external equation package; standalone reconstruction is incomplete until that package is inspected.",
            "relationship:claim_to_external_source",
        ),
    )
    for identifier, family, pattern, summary, check_id in patterns:
        match = re.search(pattern, source_text, re.IGNORECASE | re.DOTALL)
        if not match:
            continue
        excerpt = match.group(0)
        findings.append(
            _finding(
                finding_id=identifier,
                family=family,
                summary=summary,
                excerpt=excerpt,
                packets=packets,
                check_id=check_id,
            )
        )
    candidate_edges = (claim_ir or {}).get("edges", [])
    edge_specs = {
        "generic_level_linearization_consistency": (
            "level-linearization-pair-candidate",
            "approximation_linearization",
            "The source contains a candidate level/linearized equation pair. Expansion point, retained order, signs, coefficients, timing, and object domains require explicit comparison before consistency can be claimed.",
        ),
    }
    packet_by_id = {str(packet.get("id")): packet for packet in packets}
    for edge in candidate_edges:
        check_id = str(edge.get("check", ""))
        if edge.get("status") != "inferred" or check_id not in edge_specs:
            continue
        identifier, family, summary = edge_specs[check_id]
        refs = [packet_by_id[item] for item in edge.get("evidence_refs", []) if item in packet_by_id]
        excerpt = "\n".join(str(packet.get("raw_text", "")) for packet in refs)
        finding = _finding(
            finding_id=f"{identifier}:{str(edge.get('id', 'edge:unknown')).split(':', 1)[-1]}",
            family=family,
            summary=summary,
            excerpt=excerpt,
            packets=refs or packets,
            check_id=f"relationship:{check_id}",
        )
        finding["evidence_chain"]["edges"] = [edge["id"]]
        findings.append(finding)
    return findings
