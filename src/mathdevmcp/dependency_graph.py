"""Lightweight dependency graph for labels, assumptions, conventions, and packets."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from .contracts import attach_contract


@dataclass(frozen=True)
class GraphNode:
    id: str
    kind: str
    label: str | None = None
    metadata: dict | None = None


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relation: str


def build_dependency_graph(
    *,
    index: dict | None = None,
    manifest: dict | None = None,
    conventions: dict | None = None,
    packets: list[dict] | None = None,
) -> dict:
    nodes: dict[str, dict] = {}
    edges: list[dict] = []
    if index is not None:
        for label, block in index.get("labels", {}).items():
            nodes[f"label:{label}"] = asdict(GraphNode(f"label:{label}", "label", label=str(label), metadata={"file": block.get("file"), "line_start": block.get("line_start")}))
    if manifest is not None:
        for obj in manifest.get("objects", []):
            node_id = f"assumption:{obj.get('name')}"
            nodes[node_id] = asdict(GraphNode(node_id, "assumption", metadata=obj))
            for label in (index or {}).get("labels", {}):
                block_text = str((index or {}).get("labels", {}).get(label, {}).get("text", ""))
                if obj.get("name") and str(obj.get("name")) in block_text:
                    edges.append(asdict(GraphEdge(f"label:{label}", node_id, "uses_assumption_symbol")))
    if conventions is not None:
        for convention in conventions.get("conventions", []):
            node_id = f"convention:{convention.get('id')}"
            nodes[node_id] = asdict(GraphNode(node_id, "convention", metadata=convention))
            for label in convention.get("applies_to", []):
                if label != "*":
                    edges.append(asdict(GraphEdge(f"label:{label}", node_id, "uses_convention")))
    for packet in packets or []:
        packet_id = str(packet.get("packet_id") or packet.get("label") or "packet")
        node_id = f"packet:{packet_id}"
        nodes[node_id] = asdict(GraphNode(node_id, "packet", label=packet.get("label"), metadata={"status": packet.get("status")}))
        if packet.get("label"):
            edges.append(asdict(GraphEdge(node_id, f"label:{packet['label']}", "audits_label")))
    return attach_contract(
        {
            "status": "consistent",
            "reason": "Dependency graph was built from supplied diagnostic artifacts.",
            "nodes": sorted(nodes.values(), key=lambda node: node["id"]),
            "edges": edges,
        },
        "dependency_graph",
    )


def convention_impact_report(graph: dict, convention_id: str) -> dict:
    convention_node = f"convention:{convention_id}"
    labels = sorted(
        edge["source"].removeprefix("label:")
        for edge in graph.get("edges", [])
        if edge.get("target") == convention_node and str(edge.get("source", "")).startswith("label:")
    )
    return attach_contract(
        {
            "status": "consistent" if labels else "inconclusive",
            "reason": "Convention impact report built." if labels else "No labels depend on the convention in the supplied graph.",
            "convention_id": convention_id,
            "labels_to_reaudit": labels,
            "actions": [
                {"kind": "reaudit_label_after_convention_change", "target": label, "severity": "medium"}
                for label in labels
            ],
        },
        "convention_impact_report",
    )
