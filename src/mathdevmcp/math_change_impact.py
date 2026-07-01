from __future__ import annotations

"""Likely downstream impact analysis for changed math artifacts."""

from dataclasses import asdict, dataclass
from typing import Any

from .contracts import attach_contract


KNOWN_NODE_PREFIXES = ("label:", "assumption:", "packet:", "convention:", "code:", "test:", "claim:")


@dataclass(frozen=True)
class ImpactArtifact:
    artifact_id: str
    kind: str
    relation: str
    confidence: str
    provenance: dict[str, Any]
    reason: str


@dataclass(frozen=True)
class MathChangeImpactResult:
    status: str
    reason: str
    changed_id: str
    changed_kind: str
    affected_artifacts: list[dict[str, Any]]
    dependency_paths: list[list[str]]
    missing_link_warnings: list[dict[str, Any]]
    evidence_boundary: str


def _node_by_id(graph: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(node.get("id")): node for node in graph.get("nodes", []) if isinstance(node, dict)}


def _forward_edges(graph: dict[str, Any], node_id: str) -> list[dict[str, Any]]:
    return [edge for edge in graph.get("edges", []) if edge.get("source") == node_id or edge.get("target") == node_id]


def _artifact_from_node(node: dict[str, Any], relation: str, confidence: str, reason: str) -> ImpactArtifact:
    return ImpactArtifact(
        artifact_id=str(node.get("id")),
        kind=str(node.get("kind", "unknown")),
        relation=relation,
        confidence=confidence,
        provenance={"label": node.get("label"), "metadata": node.get("metadata", {})},
        reason=reason,
    )


def _artifact_matches_changed(artifact: dict[str, Any], changed_id: str) -> bool:
    haystack = " ".join(
        str(value)
        for key, value in artifact.items()
        if key not in {"metadata"} or isinstance(value, (str, int, float, bool))
    )
    return changed_id in haystack


def math_change_impact(
    changed_id: str,
    *,
    changed_kind: str = "label",
    graph: dict[str, Any] | None = None,
    packets: list[dict[str, Any]] | None = None,
    code_links: list[dict[str, Any]] | None = None,
    generated_tests: list[dict[str, Any]] | None = None,
    claims: list[dict[str, Any]] | None = None,
    assumptions: list[dict[str, Any]] | None = None,
) -> dict:
    graph = graph or {}
    changed_node_id = changed_id if changed_id.startswith(KNOWN_NODE_PREFIXES) else f"{changed_kind}:{changed_id}"
    nodes = _node_by_id(graph)
    affected: list[ImpactArtifact] = []
    paths: list[list[str]] = []
    warnings: list[dict[str, Any]] = []

    if changed_node_id in nodes:
        affected.append(
            _artifact_from_node(nodes[changed_node_id], "changed_artifact", "direct", "This is the changed graph node.")
        )
    else:
        warnings.append(
            {
                "kind": "missing_changed_node",
                "changed_id": changed_node_id,
                "reason": "The changed artifact was not present in the supplied dependency graph.",
            }
        )

    for edge in _forward_edges(graph, changed_node_id):
        neighbor_id = str(edge["target"] if edge.get("source") == changed_node_id else edge.get("source"))
        node = nodes.get(neighbor_id)
        if node is None:
            warnings.append({"kind": "missing_graph_node", "node_id": neighbor_id, "reason": "An edge referenced a missing graph node."})
            continue
        relation = str(edge.get("relation", "linked"))
        affected.append(_artifact_from_node(node, relation, "linked", "Graph edge links this artifact to the changed item."))
        paths.append([changed_node_id, relation, neighbor_id])

    artifact_groups = [
        ("review_packet", packets or []),
        ("code_link", code_links or []),
        ("generated_test", generated_tests or []),
        ("claim_packet", claims or []),
        ("assumption_entry", assumptions or []),
    ]
    for kind, artifacts in artifact_groups:
        for index, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                continue
            artifact_id = str(artifact.get("packet_id") or artifact.get("id") or artifact.get("claim_id") or f"{kind}:{index}")
            if _artifact_matches_changed(artifact, changed_id):
                affected.append(
                    ImpactArtifact(
                        artifact_id=artifact_id,
                        kind=kind,
                        relation="mentions_changed_artifact",
                        confidence="possible_unlinked",
                        provenance={"source_index": index},
                        reason="Artifact text or fields mention the changed id, but this is not a complete dependency proof.",
                    )
                )

    if not paths:
        warnings.append(
            {
                "kind": "missing_downstream_links",
                "reason": "No graph dependency paths were found; absence of links is not evidence of no impact.",
            }
        )

    if affected:
        status = "impacts_found"
        reason = "Likely affected artifacts were identified with bounded confidence levels."
    else:
        status = "inconclusive"
        reason = "No affected artifacts were found in supplied inputs, but impact coverage is incomplete."

    result = MathChangeImpactResult(
        status=status,
        reason=reason,
        changed_id=changed_id,
        changed_kind=changed_kind,
        affected_artifacts=[asdict(item) for item in affected],
        dependency_paths=paths,
        missing_link_warnings=warnings,
        evidence_boundary=(
            "Impact analysis is non-exhaustive. Missing links do not prove no impact, "
            "and this tool never auto-edits downstream math, code, tests, or claims."
        ),
    )
    return attach_contract(asdict(result), "math_change_impact_result")
