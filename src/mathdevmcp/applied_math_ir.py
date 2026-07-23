"""Source-bound evidence packets and a small, discipline-neutral claim IR.

The IR deliberately preserves uncertainty.  It is an audit transport and
relationship substrate, not a theorem prover or an OCR-to-LaTeX converter.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
import hashlib
import re
from typing import Any, Iterable


APPLIED_MATH_IR_SCHEMA = "applied_math_claim_ir"
APPLIED_MATH_IR_VERSION = "1.1"
AUTHENTICATION_STATES = frozenset(
    {
        "source_authenticated",
        "page_region_located",
        "independently_verified_transcription",
        "parser_candidate_only",
    }
)


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SourceAnchor:
    source_id: str
    path: str
    sha256: str
    page: int | None = None
    line_start: int | None = None
    line_end: int | None = None
    char_start: int | None = None
    char_end: int | None = None
    label: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _anchor(
    *,
    source_id: str,
    path: str,
    sha256: str,
    page: int | None = None,
    line_start: int | None = None,
    line_end: int | None = None,
    char_start: int | None = None,
    char_end: int | None = None,
    label: str | None = None,
) -> dict[str, Any]:
    return SourceAnchor(
        source_id=source_id,
        path=path,
        sha256=sha256,
        page=page,
        line_start=line_start,
        line_end=line_end,
        char_start=char_start,
        char_end=char_end,
        label=label,
    ).to_dict()


def _packet_id(source_id: str, kind: str, anchor: dict[str, Any], raw: str) -> str:
    key = "|".join(
        [
            source_id,
            kind,
            str(anchor.get("page")),
            str(anchor.get("line_start")),
            str(anchor.get("char_start")),
            raw,
        ]
    )
    return f"packet:{_digest(key)[:20]}"


def _candidate_kind(text: str) -> str | None:
    folded = text.casefold()
    if "=" in text or "≡" in text or re.search(r"\([A-Za-z][A-Za-z0-9_.:-]*\)", text):
        return "equation_candidate"
    if any(term in folded for term in ("assumption", "suppose", "we require")):
        return "assumption_candidate"
    if any(term in folded for term in ("estimate", "result", "we find", "shows")):
        return "claim_candidate"
    return None


def _lines_with_offsets(text: str) -> Iterable[tuple[int, int, int, str]]:
    offset = 0
    for number, line in enumerate(text.splitlines(keepends=True), start=1):
        raw = line.rstrip("\r\n")
        start = offset
        offset += len(line)
        yield number, start, offset, raw


def build_pdf_evidence_packets(
    *,
    source_id: str,
    path: str,
    sha256: str,
    body_text: str,
    parser_name: str,
    parser_version: str,
) -> list[dict[str, Any]]:
    """Build page and display-math candidates from parser text.

    Form-feed boundaries are retained as page identity.  A missing crop/image
    reference is explicit so consumers cannot mistake this for visual
    equation recovery.
    """

    packets: list[dict[str, Any]] = []
    page_offset = 0
    for page_number, page_text in enumerate(body_text.split("\f"), start=1):
        page_start = page_offset
        page_offset += len(page_text) + 1
        lines = list(_lines_with_offsets(page_text))
        for line_index, (line_number, start, end, line) in enumerate(lines):
            kind = _candidate_kind(line)
            if kind is None:
                continue
            label_match = re.search(r"\((C\.\d+)\)", line)
            if label_match:
                context_start = max(0, line_index - 6)
                context_end = min(len(lines), line_index + 3)
                context_lines = lines[context_start:context_end]
                raw_text = "\n".join(item[3] for item in context_lines)
                line_start = context_lines[0][0]
                line_end = context_lines[-1][0]
                char_start = page_start + context_lines[0][1]
                char_end = page_start + context_lines[-1][2]
            else:
                raw_text = line
                line_start = line_number
                line_end = line_number
                char_start = page_start + start
                char_end = page_start + end
            anchor = _anchor(
                source_id=source_id,
                path=path,
                sha256=sha256,
                page=page_number,
                line_start=line_start,
                line_end=line_end,
                char_start=char_start,
                char_end=char_end,
            )
            packets.append(
                {
                    "id": _packet_id(source_id, kind, anchor, raw_text),
                    "kind": kind,
                    "raw_text": raw_text,
                    "anchor": anchor,
                    "extraction": {
                        "tier": "pdf_parser_noncertifying",
                        "parser_name": parser_name,
                        "parser_version": parser_version,
                        "confidence": "candidate",
                        "visual_crop": None,
                        "manual_visual_review_required": True,
                    },
                    # A parser name is not a visual region. A caller must
                    # supply and validate a crop before this state can change.
                    "authentication_state": "parser_candidate_only",
                    "role_candidate": (
                        "linearized_equation" if "lineariz" in raw_text.casefold() else
                        "return_or_pricing" if any(term in raw_text.casefold() for term in ("return", "discount", "sdf")) else
                        "equation_candidate"
                    ),
                    "label": label_match.group(1) if label_match else None,
                }
            )
        # Every page is itself an evidence object, including pages with no
        # candidate equation. This prevents silent page loss in reports.
        page_anchor = _anchor(
            source_id=source_id,
            path=path,
            sha256=sha256,
            page=page_number,
            char_start=page_start,
            char_end=page_start + len(page_text),
        )
        packets.append(
            {
                "id": _packet_id(source_id, "page", page_anchor, page_text),
                "kind": "page",
                "raw_text": page_text,
                "anchor": page_anchor,
                "extraction": {
                    "tier": "pdf_parser_noncertifying",
                    "parser_name": parser_name,
                    "parser_version": parser_version,
                    "confidence": "page_boundary",
                    "visual_crop": None,
                    "manual_visual_review_required": False,
                },
                "authentication_state": "parser_candidate_only",
            }
        )
    return packets


def build_latex_evidence_packets(
    *, source_id: str, path: str, sha256: str, text: str, equations: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    for equation in equations:
        raw = str(equation.get("text", ""))
        line_start = int(equation.get("line_start", 1))
        start = sum(len(line) + 1 for line in text.splitlines()[: line_start - 1])
        anchor = _anchor(
            source_id=source_id,
            path=path,
            sha256=sha256,
            line_start=line_start,
            line_end=line_start + raw.count("\n"),
            char_start=start,
            char_end=start + len(raw),
            label=str(equation.get("id")) if equation.get("id") else None,
        )
        packets.append(
            {
                "id": _packet_id(source_id, "equation", anchor, raw),
                "kind": "equation",
                "raw_text": raw,
                "anchor": anchor,
                "extraction": {
                    "tier": "source_text",
                    "parser_name": "mathdevmcp_latex_structure",
                    "parser_version": APPLIED_MATH_IR_VERSION,
                    "confidence": "source",
                    "visual_crop": None,
                    "manual_visual_review_required": False,
                },
                "authentication_state": "source_authenticated",
                "label": equation.get("id"),
                "environment": equation.get("environment"),
            }
        )
    return packets


def build_claim_ir(
    *, source_records: list[dict[str, Any]], packets: list[dict[str, Any]]
) -> dict[str, Any]:
    """Build nodes and conservative edges from explicit source references."""

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    labels: dict[str, str] = {}
    for packet in packets:
        node_id = f"object:{packet['id'].split(':', 1)[1]}"
        node_kind = {
            "equation": "equation",
            "equation_candidate": "equation_candidate",
            "assumption_candidate": "assumption_candidate",
            "claim_candidate": "claim_candidate",
            "page": "page",
        }.get(str(packet.get("kind")), "evidence_object")
        nodes.append(
            {
                "id": node_id,
                "kind": node_kind,
                "packet_id": packet["id"],
                "label": packet.get("label"),
                "authentication_state": packet.get("authentication_state", "parser_candidate_only"),
                "anchor": packet["anchor"],
                "status": "extracted" if node_kind != "equation_candidate" else "candidate",
                "raw_text": packet.get("raw_text", ""),
            }
        )
        if packet.get("label"):
            labels[str(packet["label"])] = node_id
    # Pair source equations generically when one context explicitly describes
    # a linearization and another source equation shares distinctive concept
    # terms. This nominates a relationship for checking; it does not establish
    # that the equations are mathematically related.
    stopwords = {
        "about", "above", "after", "also", "been", "before", "being", "below",
        "between", "can", "equation", "equations", "from", "have", "into", "linearized",
        "linearize", "model", "that", "their", "then", "these", "this", "where", "which",
        "with", "yields", "the", "and", "for", "are", "its", "we", "of", "to", "in",
    }

    def concept_terms(raw: str) -> set[str]:
        return {
            term
            for term in re.findall(r"[a-z][a-z0-9]+", raw.casefold())
            if len(term) >= 4 and term not in stopwords
        }

    labeled_packets = [packet for packet in packets if packet.get("label")]
    level_packets = [packet for packet in labeled_packets if packet.get("role_candidate") != "linearized_equation"]
    linear_packets = [packet for packet in labeled_packets if packet.get("role_candidate") == "linearized_equation"]
    for linear in linear_packets:
        linear_terms = concept_terms(str(linear.get("raw_text", "")))
        candidates: list[tuple[int, dict[str, Any], set[str]]] = []
        for level in level_packets:
            shared = linear_terms & concept_terms(str(level.get("raw_text", "")))
            # Require both a role match and at least two shared concepts. A
            # proximity window prevents unrelated equations elsewhere in a
            # long PDF from pairing merely because they mention "capital".
            page_gap = abs(int(linear.get("anchor", {}).get("page") or 0) - int(level.get("anchor", {}).get("page") or 0))
            if len(shared) >= 2 and page_gap <= 2:
                candidates.append((len(shared), level, shared))
        if not candidates:
            continue
        score, level, shared = max(candidates, key=lambda item: (item[0], str(item[1].get("label"))))
        source_node = labels[str(level["label"])]
        target_node = labels[str(linear["label"])]
        edge_id = f"edge:{_digest(source_node + target_node + 'linearizes_to')[:20]}"
        if any(edge.get("id") == edge_id for edge in edges):
            continue
        edges.append(
            {
                "id": edge_id,
                "source": source_node,
                "target": target_node,
                "relation": "candidate_linearizes_to",
                "status": "inferred",
                "evidence_refs": [level["id"], linear["id"]],
                "check": "generic_level_linearization_consistency",
                "confidence": "candidate",
                "shared_terms": sorted(shared),
                "similarity_score": score,
                "source_label": level.get("label"),
                "target_label": linear.get("label"),
            }
        )
    for packet in packets:
        label = packet.get("label")
        if not label:
            continue
        raw = str(packet.get("raw_text", ""))
        for referenced in re.findall(r"(?:eq:|eqn:|equation[:._-]?)([A-Za-z0-9_.-]+)", raw, re.IGNORECASE):
            target = labels.get(referenced) or labels.get(f"eq:{referenced}")
            if target:
                source = f"object:{packet['id'].split(':', 1)[1]}"
                edges.append(
                    {
                        "id": f"edge:{_digest(source + target + 'references')[:20]}",
                        "source": source,
                        "target": target,
                        "relation": "references",
                        "status": "explicit",
                        "evidence_refs": [packet["id"]],
                    }
                )
    return {
        "schema": APPLIED_MATH_IR_SCHEMA,
        "version": APPLIED_MATH_IR_VERSION,
        "source_ids": [str(item.get("sha256", "")) for item in source_records],
        "nodes": nodes,
        "edges": edges,
        "limitations": [
            "PDF candidates are parser text and require visual/source review.",
            "Unlabeled adjacency is not treated as dependency.",
            "Edges inferred by a future validator must retain status='inferred'.",
        ],
    }


def validate_claim_ir(
    ir: dict[str, Any],
    *,
    packets: list[dict[str, Any]] | None = None,
    source_records: list[dict[str, Any]] | None = None,
) -> list[str]:
    errors: list[str] = []
    if ir.get("schema") != APPLIED_MATH_IR_SCHEMA:
        errors.append("schema mismatch")
    if ir.get("version") != APPLIED_MATH_IR_VERSION:
        errors.append("version mismatch")
    nodes = ir.get("nodes")
    edges = ir.get("edges")
    if not isinstance(nodes, list) or not isinstance(edges, list):
        return ["nodes and edges must be lists"]
    node_ids = [node.get("id") for node in nodes if isinstance(node, dict)]
    if len(node_ids) != len(set(node_ids)):
        errors.append("duplicate node ids")
    known = set(node_ids)
    packet_ids = {str(item.get("id")) for item in (packets or [])}
    source_digests = {str(item.get("sha256")) for item in (source_records or [])}
    for index, edge in enumerate(edges):
        if not isinstance(edge, dict):
            errors.append(f"edge {index} is not an object")
            continue
        if edge.get("source") not in known or edge.get("target") not in known:
            errors.append(f"edge {index} references unknown node")
        if edge.get("status") not in {"explicit", "inferred", "unresolved"}:
            errors.append(f"edge {index} has invalid status")
        if not isinstance(edge.get("evidence_refs"), list):
            errors.append(f"edge {index} lacks evidence_refs")
        elif packets is not None:
            errors.extend(
                f"edge {index} references unknown evidence packet {ref}"
                for ref in edge["evidence_refs"]
                if ref not in packet_ids
            )
    for index, node in enumerate(nodes):
        if not isinstance(node, dict):
            continue
        state = node.get("authentication_state")
        if state is not None and state not in AUTHENTICATION_STATES:
            errors.append(f"node {index} has invalid authentication_state")
        if packets is not None and node.get("packet_id") not in packet_ids:
            errors.append(f"node {index} references unknown packet")
        anchor = node.get("anchor")
        if isinstance(anchor, dict):
            digest = str(anchor.get("sha256", ""))
            if not re.fullmatch(r"[0-9a-f]{64}", digest):
                errors.append(f"node {index} has invalid source digest")
            elif source_records is not None and digest not in source_digests:
                errors.append(f"node {index} source digest is not bound to a source record")
    return errors


def evidence_chain(
    *, finding_id: str, packet_ids: list[str], check_id: str, result: dict[str, Any]
) -> dict[str, Any]:
    return {
        "finding_id": finding_id,
        "source_packets": list(packet_ids),
        "objects": [f"object:{packet_id.split(':', 1)[1]}" for packet_id in packet_ids],
        "edges": [],
        "check": check_id,
        "result": result,
        "claim_boundary": "diagnostic_evidence_only",
    }


def verify_independent_transcription(
    *,
    reviewer_id: str,
    extractor_id: str,
    source_anchor: dict[str, Any],
    transcription: str,
    transcription_sha256: str,
    decision: str,
    conflict_notes: str = "",
    review_record: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return an authentication record; only a bound independent decision can pass."""

    actual = _digest(transcription)
    anchor_digest = str(source_anchor.get("sha256", "")) if isinstance(source_anchor, dict) else ""
    region_digest = ""
    if isinstance(source_anchor, dict):
        region_digest = str(source_anchor.get("region_sha256") or source_anchor.get("crop_sha256") or "")
    record = review_record if isinstance(review_record, dict) else {}
    valid = (
        bool(reviewer_id)
        and bool(extractor_id)
        and reviewer_id != extractor_id
        and decision in {"agree", "disagree", "abstain"}
        and actual == transcription_sha256
        and isinstance(source_anchor, dict)
        and bool(re.fullmatch(r"[0-9a-f]{64}", anchor_digest))
        and bool(re.fullmatch(r"[0-9a-f]{64}", region_digest))
        and isinstance(source_anchor.get("page"), int)
        and source_anchor.get("page", 0) > 0
        and record.get("reviewer_id") == reviewer_id
        and record.get("extractor_id") == extractor_id
        and record.get("source_anchor") == source_anchor
        and record.get("transcription_sha256") == transcription_sha256
        and record.get("decision") == decision
        and isinstance(record.get("record_id"), str)
        and bool(record.get("record_id"))
    )
    state = "independently_verified_transcription" if valid and decision == "agree" else "parser_candidate_only"
    return {
        "state": state,
        "reviewer_id": reviewer_id,
        "extractor_id": extractor_id,
        "reviewer_independent": bool(reviewer_id and extractor_id and reviewer_id != extractor_id),
        "source_anchor": source_anchor,
        "transcription_sha256": transcription_sha256,
        "actual_transcription_sha256": actual,
        "decision": decision,
        "conflict_notes": conflict_notes,
        "review_record": record,
        "non_claim": "Independent transcription review authenticates the supplied transcription only; it does not prove the source equation's mathematical claim.",
    }
