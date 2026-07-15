from __future__ import annotations

"""Entry-rooted, backend-free LaTeX context graph and bounded resolver."""

from collections import defaultdict, deque
from collections.abc import Mapping
import re
from pathlib import Path
from typing import Any

from .evidence_manifest import EvidenceValidationError, content_digest
from .latex_index import EntryRootedDiscovery, discover_entry_rooted_tex_files


GRAPH_SCHEMA_VERSION = "p03_context_dependency_graph@1"
SEARCH_SCHEMA_VERSION = "p03_context_manifest@1"
CONTEXT_STATES = frozenset(
    {
        "stated",
        "source_supported",
        "ambiguous",
        "not_found_after_search",
        "not_searched",
        "candidate_assumption",
    }
)
_BUDGET_KEYS = frozenset(
    {"max_files", "max_bytes", "max_nodes", "max_edges", "max_dependency_expansions"}
)
_ENV_RE = re.compile(
    rb"\\begin\{(?P<kind>definition|assumption|proposition|theorem|lemma|corollary|equation|align|alignat|gather|multline)\*?\}"
    rb"(?P<body>.*?)"
    rb"\\end\{(?P=kind)\*?\}",
    re.DOTALL,
)
_SECTION_RE = re.compile(
    rb"\\(?P<kind>part|chapter|section|subsection|subsubsection)\*?\{(?P<title>[^{}]+)\}"
)
_LABEL_RE = re.compile(rb"\\label\{(?P<label>[^{}]+)\}")
_REFERENCE_RE = re.compile(rb"\\(?:ref|eqref|autoref)\{(?P<label>[^{}]+)\}")
_DECLARATION_RE = re.compile(
    rb"(?:The\s+symbol\s+)?\$?(?P<symbol>\\[A-Za-z]+|[A-Za-z][A-Za-z0-9_]*)\$?"
    rb"\s+(?:is|denotes|represents|means|:=)\s+(?P<meaning>[^.;\n]+)",
    re.IGNORECASE,
)


def _positive_budget(value: Mapping[str, Any]) -> dict[str, int]:
    if not isinstance(value, Mapping) or set(value) != _BUDGET_KEYS:
        raise EvidenceValidationError(f"context budget keys must be exactly {sorted(_BUDGET_KEYS)}")
    result: dict[str, int] = {}
    for key in sorted(_BUDGET_KEYS):
        item = value[key]
        if type(item) is not int or item <= 0:
            raise EvidenceValidationError(f"context budget {key} must be a positive integer")
        result[key] = item
    return result


def _line_span(raw: bytes, start: int, end: int) -> dict[str, int]:
    return {
        "start": raw[:start].count(b"\n") + 1,
        "end": raw[:end].count(b"\n") + 1,
    }


def _node_id(
    entry_source_digest: str,
    kind: str,
    source_file: str,
    byte_span: Mapping[str, int],
    declaration_key: str,
) -> str:
    return "ctx_" + content_digest(
        [entry_source_digest, kind, source_file, dict(byte_span), declaration_key]
    )


def _edge_id(kind: str, from_node_id: str, to_node_id: str, source_span: Mapping[str, Any]) -> str:
    return "edge_" + content_digest([kind, from_node_id, to_node_id, dict(source_span)])


def _source_node(
    *,
    entry_source_digest: str,
    kind: str,
    source_file: str,
    source_digest: str,
    raw: bytes,
    start: int,
    end: int,
    declaration_key: str,
    parse_state: str = "parsed",
) -> dict[str, Any]:
    span = {"start": start, "end": end}
    try:
        source_text = raw[start:end].decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise EvidenceValidationError("context node does not contain strict UTF-8 bytes") from exc
    return {
        "id": _node_id(entry_source_digest, kind, source_file, span, declaration_key),
        "kind": kind,
        "source_file": source_file,
        "source_digest": source_digest,
        "byte_span": span,
        "line_span": _line_span(raw, start, end),
        "declaration_key": declaration_key,
        "parse_state": parse_state,
        "source_text": source_text,
    }


def _contains_offset(node: Mapping[str, Any], offset: int) -> bool:
    span = node["byte_span"]
    return int(span["start"]) <= offset < int(span["end"])


def _parent_node(nodes: list[dict[str, Any]], source_file: str, offset: int, file_id: str) -> str:
    candidates = [
        node
        for node in nodes
        if node["source_file"] == source_file
        and node["kind"] in {"definition", "assumption", "proposition", "theorem", "lemma", "corollary", "equation"}
        and _contains_offset(node, offset)
    ]
    if not candidates:
        return file_id
    candidates.sort(
        key=lambda node: (
            int(node["byte_span"]["end"]) - int(node["byte_span"]["start"]),
            node["id"],
        )
    )
    return candidates[0]["id"]


def _graph_edge(
    *,
    kind: str,
    from_node_id: str,
    to_node_id: str,
    source_file: str,
    target_file: str,
    byte_span: Mapping[str, int],
    line_span: Mapping[str, int],
    source_digest: str,
) -> dict[str, Any]:
    source_span = {
        "source_file": source_file,
        "source_digest": source_digest,
        "byte_span": dict(byte_span),
        "line_span": dict(line_span),
    }
    return {
        "id": _edge_id(kind, from_node_id, to_node_id, source_span),
        "kind": kind,
        "from_node_id": from_node_id,
        "to_node_id": to_node_id,
        "source_file": source_file,
        "target_file": target_file,
        "source_span": source_span,
    }


def _syntax_nodes(discovery: EntryRootedDiscovery, entry_digest: str) -> tuple[list[dict], list[dict]]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    file_ids: dict[str, str] = {}

    for logical_ref in discovery.reachable_files:
        snapshot = discovery.snapshots[logical_ref]
        file_node = _source_node(
            entry_source_digest=entry_digest,
            kind="file",
            source_file=logical_ref,
            source_digest=snapshot.source_digest,
            raw=snapshot.raw_bytes,
            start=0,
            end=len(snapshot.raw_bytes),
            declaration_key=logical_ref,
            parse_state=snapshot.parse_state,
        )
        file_node["entry_reachable"] = True
        file_node["byte_count"] = snapshot.byte_count
        file_ids[logical_ref] = file_node["id"]
        nodes.append(file_node)

    for logical_ref in discovery.reachable_files:
        snapshot = discovery.snapshots[logical_ref]
        if snapshot.parse_state != "parsed":
            continue
        raw = snapshot.raw_bytes
        local_nodes: list[dict[str, Any]] = []
        for match in _SECTION_RE.finditer(raw):
            title = match.group("title").decode("utf-8", "strict").strip()
            local_nodes.append(
                _source_node(
                    entry_source_digest=entry_digest,
                    kind="section",
                    source_file=logical_ref,
                    source_digest=snapshot.source_digest,
                    raw=raw,
                    start=match.start(),
                    end=match.end(),
                    declaration_key=f"{match.group('kind').decode('ascii')}:{title}",
                )
            )
        for match in _ENV_RE.finditer(raw):
            kind = match.group("kind").decode("ascii")
            normalized_kind = "equation" if kind in {"align", "alignat", "gather", "multline"} else kind
            labels = [item.group("label").decode("utf-8", "strict") for item in _LABEL_RE.finditer(match.group(0))]
            declaration_key = labels[0] if labels else f"{normalized_kind}:{match.start()}"
            local_nodes.append(
                _source_node(
                    entry_source_digest=entry_digest,
                    kind=normalized_kind,
                    source_file=logical_ref,
                    source_digest=snapshot.source_digest,
                    raw=raw,
                    start=match.start(),
                    end=match.end(),
                    declaration_key=declaration_key,
                )
            )
        for match in _LABEL_RE.finditer(raw):
            label = match.group("label").decode("utf-8", "strict")
            local_nodes.append(
                _source_node(
                    entry_source_digest=entry_digest,
                    kind="label",
                    source_file=logical_ref,
                    source_digest=snapshot.source_digest,
                    raw=raw,
                    start=match.start(),
                    end=match.end(),
                    declaration_key=label,
                )
            )
        for match in _REFERENCE_RE.finditer(raw):
            label = match.group("label").decode("utf-8", "strict")
            local_nodes.append(
                _source_node(
                    entry_source_digest=entry_digest,
                    kind="reference",
                    source_file=logical_ref,
                    source_digest=snapshot.source_digest,
                    raw=raw,
                    start=match.start(),
                    end=match.end(),
                    declaration_key=label,
                )
            )
        for match in _DECLARATION_RE.finditer(raw):
            symbol = match.group("symbol").decode("utf-8", "strict")
            meaning = match.group("meaning").decode("utf-8", "strict").strip()
            local_nodes.append(
                _source_node(
                    entry_source_digest=entry_digest,
                    kind="notation_declaration",
                    source_file=logical_ref,
                    source_digest=snapshot.source_digest,
                    raw=raw,
                    start=match.start(),
                    end=match.end(),
                    declaration_key=f"{symbol}:{meaning}",
                )
            )
        nodes.extend(local_nodes)

        for node in local_nodes:
            parent_id = file_ids[logical_ref]
            if node["kind"] in {"label", "reference", "notation_declaration"}:
                parent_id = _parent_node(local_nodes, logical_ref, node["byte_span"]["start"], parent_id)
            edges.append(
                _graph_edge(
                    kind="contains",
                    from_node_id=parent_id,
                    to_node_id=node["id"],
                    source_file=logical_ref,
                    target_file=logical_ref,
                    byte_span=node["byte_span"],
                    line_span=node["line_span"],
                    source_digest=snapshot.source_digest,
                )
            )

    label_nodes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        if node["kind"] == "label":
            label_nodes[node["declaration_key"]].append(node)

    for node in nodes:
        if node["kind"] != "reference":
            continue
        matches = label_nodes.get(node["declaration_key"], [])
        if len(matches) != 1:
            continue
        target = matches[0]
        snapshot = discovery.snapshots[node["source_file"]]
        parent_id = _parent_node(nodes, node["source_file"], node["byte_span"]["start"], file_ids[node["source_file"]])
        edges.append(
            _graph_edge(
                kind="references",
                from_node_id=parent_id,
                to_node_id=target["id"],
                source_file=node["source_file"],
                target_file=target["source_file"],
                byte_span=node["byte_span"],
                line_span=node["line_span"],
                source_digest=snapshot.source_digest,
            )
        )

    for source_ref in discovery.reachable_files:
        snapshot = discovery.snapshots[source_ref]
        for directive in snapshot.directives:
            target_ref = directive["target_file"]
            if target_ref not in file_ids:
                continue
            edges.append(
                _graph_edge(
                    kind=directive["kind"],
                    from_node_id=file_ids[source_ref],
                    to_node_id=file_ids[target_ref],
                    source_file=source_ref,
                    target_file=target_ref,
                    byte_span=directive["byte_span"],
                    line_span=directive["line_span"],
                    source_digest=snapshot.source_digest,
                )
            )

    nodes.sort(
        key=lambda node: (
            node["source_file"].encode("utf-8"),
            int(node["byte_span"]["start"]),
            node["kind"],
            node["id"],
        )
    )
    edges.sort(
        key=lambda edge: (
            edge["source_file"].encode("utf-8"),
            int(edge["source_span"]["byte_span"]["start"]),
            edge["kind"],
            edge["id"],
        )
    )
    return nodes, edges


def build_context_dependency_graph(
    root: Path,
    entry_ref: str,
    *,
    expected_entry_source_digest: str,
    budget: Mapping[str, Any],
) -> dict[str, Any]:
    limits = _positive_budget(budget)
    if not re.fullmatch(r"[0-9a-f]{64}", expected_entry_source_digest):
        raise EvidenceValidationError("expected_entry_source_digest must be a lowercase SHA-256")
    discovery = discover_entry_rooted_tex_files(root, entry_ref, budget=limits)
    entry_snapshot = discovery.snapshots[discovery.entry_ref]
    if entry_snapshot.source_digest != expected_entry_source_digest:
        raise EvidenceValidationError("entry source digest drift")
    nodes, edges = _syntax_nodes(discovery, expected_entry_source_digest)
    diagnostics = [dict(item) for item in discovery.diagnostics]
    labels: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for node in nodes:
        if node["kind"] == "label":
            labels[node["declaration_key"]].append(node)
    for label, occurrences in labels.items():
        if len(occurrences) > 1:
            diagnostics.append(
                {
                    "kind": "duplicate_label",
                    "classification": "context",
                    "source_file": occurrences[0]["source_file"],
                    "target_file": label,
                    "byte_span": occurrences[0]["byte_span"],
                    "occurrence_ids": [item["id"] for item in occurrences],
                }
            )
    diagnostics.sort(
        key=lambda item: (
            str(item.get("source_file", "")).encode("utf-8"),
            int((item.get("byte_span") or {}).get("start", -1)),
            item["kind"],
        )
    )
    files = [
        {
            "logical_ref": ref,
            "source_digest": discovery.snapshots[ref].source_digest,
            "byte_count": discovery.snapshots[ref].byte_count,
            "full_byte_span": {"start": 0, "end": discovery.snapshots[ref].byte_count},
            "full_line_span": {"start": 1, "end": discovery.snapshots[ref].line_count},
            "parse_state": discovery.snapshots[ref].parse_state,
            "entry_reachable": True,
        }
        for ref in discovery.reachable_files
    ]
    graph_digest = content_digest(
        [discovery.entry_ref, expected_entry_source_digest, nodes, edges, diagnostics]
    )
    return {
        "schema_version": GRAPH_SCHEMA_VERSION,
        "entry_ref": discovery.entry_ref,
        "entry_source_digest": expected_entry_source_digest,
        "graph_digest": graph_digest,
        "budget": limits,
        "files": files,
        "nodes": nodes,
        "edges": edges,
        "diagnostics": diagnostics,
        "integrity_vetoes": list(discovery.integrity_vetoes),
        "considered_files": list(discovery.considered_files),
        "reachable_files": list(discovery.reachable_files),
        "excluded_sibling_files": list(discovery.excluded_sibling_files),
        "unsearched_files": [dict(item) for item in discovery.unsearched_files],
        "traversal_counts": dict(discovery.traversal_counts),
        "non_claims": [
            "Entry reachability does not establish semantic applicability.",
            "The graph is source-context evidence, not mathematical proof.",
        ],
    }


def _closed_string_list(value: Any, name: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise EvidenceValidationError(f"{name} must be a list of non-empty strings")
    if len(value) != len(set(value)):
        raise EvidenceValidationError(f"{name} must not contain duplicates")
    return list(value)


def _request(value: Mapping[str, Any], graph: Mapping[str, Any], obligation: Mapping[str, Any]) -> dict[str, Any]:
    keys = {
        "obligation_digest",
        "entry_source_digest",
        "requirement_id",
        "requirement_predicate",
        "requirement_subjects",
        "required_node_kinds",
        "required_edge_kinds",
        "required_files",
        "budget",
    }
    if not isinstance(value, Mapping) or set(value) != keys:
        raise EvidenceValidationError(f"context request keys must be exactly {sorted(keys)}")
    request = dict(value)
    if request["obligation_digest"] != obligation.get("obligation_digest"):
        raise EvidenceValidationError("context request obligation digest mismatch")
    if request["entry_source_digest"] != graph.get("entry_source_digest"):
        raise EvidenceValidationError("context request entry source digest mismatch")
    for key in ("obligation_digest", "entry_source_digest"):
        if not isinstance(request[key], str) or not re.fullmatch(r"[0-9a-f]{64}", request[key]):
            raise EvidenceValidationError(f"{key} must be a lowercase SHA-256")
    for key in ("requirement_id", "requirement_predicate"):
        if not isinstance(request[key], str) or not request[key]:
            raise EvidenceValidationError(f"{key} must be a non-empty string")
    request["requirement_subjects"] = _closed_string_list(request["requirement_subjects"], "requirement_subjects")
    request["required_node_kinds"] = _closed_string_list(request["required_node_kinds"], "required_node_kinds")
    request["required_edge_kinds"] = _closed_string_list(request["required_edge_kinds"], "required_edge_kinds")
    request["required_files"] = _closed_string_list(request["required_files"], "required_files")
    request["budget"] = _positive_budget(request["budget"])
    return request


def _words(value: str) -> set[str]:
    value = re.sub(r"\\(?:ref|eqref|autoref)\{([^{}]+)\}", r" \1 ", value)
    value = re.sub(r"\\([A-Za-z]+)", r" \1 ", value)
    return {
        word
        for word in re.findall(r"[A-Za-z0-9_:-]+", value.lower())
        if word not in {"the", "a", "an", "is", "for", "by", "of", "to", "used"}
    }


def _file_dependency_paths(graph: Mapping[str, Any]) -> dict[str, list[str]]:
    file_nodes = {node["source_file"]: node["id"] for node in graph["nodes"] if node["kind"] == "file"}
    adjacency: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for edge in graph["edges"]:
        if edge["kind"] in {"input", "include"}:
            adjacency[edge["source_file"]].append((edge["target_file"], edge["id"]))
    for values in adjacency.values():
        values.sort(key=lambda item: (item[0].encode("utf-8"), item[1]))
    result: dict[str, list[str]] = {graph["entry_ref"]: [file_nodes[graph["entry_ref"]]]}
    queue: deque[str] = deque([graph["entry_ref"]])
    while queue:
        source = queue.popleft()
        for target, edge_id in adjacency.get(source, []):
            if target in result or target not in file_nodes:
                continue
            result[target] = [*result[source], edge_id, file_nodes[target]]
            queue.append(target)
    return result


def _source_ref(node: Mapping[str, Any], dependency_path: list[str], applicability_reason: str) -> dict[str, Any]:
    return {
        "file": node["source_file"],
        "source_digest": node["source_digest"],
        "byte_span": dict(node["byte_span"]),
        "line_span": dict(node["line_span"]),
        "enclosing_node_id": node["id"],
        "dependency_path": dependency_path,
        "applicability_reason": applicability_reason,
    }


def _diagnostic_blocks(
    diagnostic: Mapping[str, Any], request: Mapping[str, Any], *, found_support: bool
) -> bool:
    if diagnostic.get("classification") == "integrity":
        return True
    if diagnostic.get("kind") == "duplicate_label":
        return False
    required_files = set(request["required_files"])
    if required_files:
        return diagnostic.get("target_file") in required_files or diagnostic.get("source_file") in required_files
    return not found_support and diagnostic.get("kind") in {
        "missing_include",
        "unsupported_include_form",
        "decode_failure",
        "include_cycle",
    }


def resolve_context_requirement(
    graph: Mapping[str, Any],
    obligation: Mapping[str, Any],
    request: Mapping[str, Any],
) -> dict[str, Any]:
    if graph.get("schema_version") != GRAPH_SCHEMA_VERSION:
        raise EvidenceValidationError("context resolver requires a P03 context graph")
    bound = _request(request, graph, obligation)
    if obligation.get("adapter_eligible") is not True or obligation.get("extraction_state") != "valid_complete":
        raise EvidenceValidationError("ineligible extraction records require an extraction-veto manifest")

    limits = bound["budget"]
    files = list(graph["reachable_files"])
    searched_files = files[:limits["max_files"]]
    unsearched_files = [
        {"file": item, "reason": "max_files"} for item in files[limits["max_files"]:]
    ] + [dict(item) for item in graph.get("unsearched_files", [])]
    file_bytes = {item["logical_ref"]: item["byte_count"] for item in graph["files"]}
    bytes_used = 0
    byte_searched_files: list[str] = []
    for item in searched_files:
        if bytes_used + file_bytes[item] > limits["max_bytes"]:
            unsearched_files.append({"file": item, "reason": "max_bytes"})
            continue
        bytes_used += file_bytes[item]
        byte_searched_files.append(item)
    searched_files = byte_searched_files
    eligible_nodes = [node for node in graph["nodes"] if node["source_file"] in searched_files]
    searched_nodes = eligible_nodes[:limits["max_nodes"]]
    node_exhausted = len(eligible_nodes) > len(searched_nodes)
    eligible_edges = [
        edge for edge in graph["edges"]
        if edge["source_file"] in searched_files and edge["target_file"] in searched_files
    ]
    searched_edges = eligible_edges[:limits["max_edges"]]
    edge_exhausted = len(eligible_edges) > len(searched_edges)
    file_paths = _file_dependency_paths(graph)

    predicate_words = _words(bound["requirement_predicate"])
    subject_words = set().union(*(_words(item) for item in bound["requirement_subjects"]))
    required_kinds = set(bound["required_node_kinds"])
    target_spans = obligation.get("owned_spans", []) if obligation.get("document", {}).get("file") == graph["entry_ref"] else []
    candidates: list[dict[str, Any]] = []
    for node in searched_nodes:
        if node["kind"] not in required_kinds:
            continue
        dependency_path = file_paths.get(node["source_file"])
        if not dependency_path:
            continue
        words = _words(node["source_text"])
        lexical_overlap = sorted(predicate_words & words)
        subject_overlap = sorted(subject_words & words)
        if not lexical_overlap and not subject_overlap:
            continue
        exact_subjects = bool(subject_words) and subject_words <= words
        in_target = any(
            int(span.get("start_byte", -1)) <= int(node["byte_span"]["start"])
            and int(span.get("end_byte", -1)) >= int(node["byte_span"]["end"])
            for span in target_spans
            if isinstance(span, Mapping)
        )
        explicit_applicability = exact_subjects or any(
            subject in node["source_text"] for subject in bound["requirement_subjects"] if ":" in subject
        )
        applicability_reason = (
            "The typed declaration explicitly names every requirement subject."
            if exact_subjects
            else "The reachable source has lexical overlap but lacks an explicit complete applicability relation."
        )
        priority = (
            "exact_declaration"
            if node["kind"] in {"definition", "assumption", "notation_declaration"}
            else "dependency_linked_use"
        )
        path = [*dependency_path]
        contains = next(
            (
                edge["id"]
                for edge in searched_edges
                if edge["kind"] == "contains" and edge["to_node_id"] == node["id"]
            ),
            None,
        )
        if contains:
            path.extend([contains, node["id"]])
        candidates.append(
            {
                "node_id": node["id"],
                "priority_class": priority,
                "lexical_evidence": lexical_overlap,
                "subject_evidence": subject_overlap,
                "applicability_state": "explicit" if explicit_applicability else "candidate",
                "applicability_reason": applicability_reason,
                "dependency_path": path,
                "source_ref": _source_ref(node, path, applicability_reason),
                "target_span_match": in_target,
            }
        )
    for candidate in candidates:
        if candidate["applicability_state"] != "explicit":
            continue
        span = candidate["source_ref"]["byte_span"]
        nested = [
            other
            for other in candidates
            if other is not candidate
            and other["applicability_state"] == "explicit"
            and other["source_ref"]["file"] == candidate["source_ref"]["file"]
            and span["start"] <= other["source_ref"]["byte_span"]["start"]
            and span["end"] >= other["source_ref"]["byte_span"]["end"]
            and (
                span["start"] < other["source_ref"]["byte_span"]["start"]
                or span["end"] > other["source_ref"]["byte_span"]["end"]
            )
        ]
        if nested:
            candidate["applicability_state"] = "candidate"
            candidate["applicability_reason"] = (
                "This enclosing source node is retained as context; a nested exact declaration carries applicability."
            )
            candidate["source_ref"]["applicability_reason"] = candidate["applicability_reason"]
    priority_order = {"exact_declaration": 0, "dependency_linked_use": 1}
    candidates.sort(
        key=lambda item: (
            priority_order[item["priority_class"]],
            0 if item["applicability_state"] == "explicit" else 1,
            len(item["dependency_path"]),
            -len(item["lexical_evidence"]),
            item["source_ref"]["file"].encode("utf-8"),
            item["source_ref"]["byte_span"]["start"],
            item["node_id"],
        )
    )

    explicit = [item for item in candidates if item["applicability_state"] == "explicit"]
    stated = [item for item in explicit if item["target_span_match"]]
    ambiguous = False
    if len(explicit) > 1:
        meanings = {
            " ".join(sorted(_words(next(node["source_text"] for node in searched_nodes if node["id"] == item["node_id"]))))
            for item in explicit
        }
        ambiguous = len(meanings) > 1 and len({item["priority_class"] for item in explicit}) == 1
    found_support = bool(explicit) and not ambiguous
    blocking_diagnostics = [
        dict(item)
        for item in graph["diagnostics"]
        if _diagnostic_blocks(item, bound, found_support=found_support)
    ]
    budget_exhausted = bool(unsearched_files or node_exhausted or edge_exhausted)
    if graph.get("integrity_vetoes"):
        terminal_state = "not_searched"
    elif ambiguous:
        terminal_state = "ambiguous"
    elif stated:
        terminal_state = "stated"
    elif explicit:
        terminal_state = "source_supported"
    elif budget_exhausted or blocking_diagnostics:
        terminal_state = "not_searched"
    elif candidates:
        terminal_state = "candidate_assumption"
    else:
        terminal_state = "not_found_after_search"
    assert terminal_state in CONTEXT_STATES

    legacy = {
        "stated": "stated",
        "source_supported": "nearby_stated",
        "candidate_assumption": "inferred_candidate",
        "ambiguous": "unresolved",
        "not_found_after_search": "missing",
        "not_searched": "not_searched",
    }[terminal_state]
    request_digest = content_digest(
        [
            bound["obligation_digest"],
            graph["graph_digest"],
            bound["requirement_predicate"],
            bound["required_edge_kinds"],
            bound["budget"],
        ]
    )
    manifest = {
        "schema_version": SEARCH_SCHEMA_VERSION,
        "phase": "P03",
        "entry_state": "context_search",
        "obligation_digest": bound["obligation_digest"],
        "p02_extraction_state": obligation["extraction_state"],
        "p02_adapter_eligible": obligation["adapter_eligible"],
        "p02_label": obligation.get("label"),
        "entry_source_digest": graph["entry_source_digest"],
        "corpus_graph_digest": graph["graph_digest"],
        "context_request": bound,
        "context_request_digest": request_digest,
        "searched_files": searched_files,
        "searched_nodes": [item["id"] for item in searched_nodes],
        "searched_edges": [item["id"] for item in searched_edges],
        "searched_counts": {
            "files": len(searched_files),
            "nodes": len(searched_nodes),
            "edges": len(searched_edges),
            "bytes": bytes_used,
        },
        "unsearched_files": sorted(
            unsearched_files,
            key=lambda item: (item["file"].encode("utf-8"), item["reason"]),
        ),
        "unsearched_node_count": max(0, len(eligible_nodes) - len(searched_nodes)),
        "unsearched_edge_count": max(0, len(eligible_edges) - len(searched_edges)),
        "budget_exhausted": budget_exhausted,
        "candidates": candidates,
        "semantic_candidates": candidates,
        "typed_assumptions": [],
        "symbol_resolutions": [],
        "terminal_state": terminal_state,
        "engineering_diagnostics": blocking_diagnostics,
        "integrity_vetoes": list(graph["integrity_vetoes"]),
        "legacy_context_status": {
            "value": legacy,
            "diagnostic": True,
            "deprecated": True,
        },
        "non_claims": [
            "Lexical evidence is explanatory and cannot establish support.",
            "Source support is not mathematical sufficiency or proof.",
            "Search completeness is limited to the recorded budget and dependency closure.",
        ],
    }
    manifest["manifest_digest"] = content_digest(manifest)
    return manifest
