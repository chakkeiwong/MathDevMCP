from __future__ import annotations

from copy import deepcopy
from pathlib import Path

from mathdevmcp.document_context_graph import (
    build_context_dependency_graph,
    resolve_context_requirement,
)
from mathdevmcp.evidence_manifest import content_digest


ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = ROOT / "tests/fixtures/document_context_graph"
GRAPH_BUDGET = {
    "max_files": 8,
    "max_bytes": 1_048_576,
    "max_nodes": 256,
    "max_edges": 512,
    "max_dependency_expansions": 64,
}
OBLIGATION = {
    "obligation_digest": "1" * 64,
    "adapter_eligible": True,
    "extraction_state": "valid_complete",
    "label": "eq:target",
    "owned_spans": [{"start_byte": 91, "end_byte": 145, "line_start": 5, "line_end": 7}],
    "document": {"file": "entry.tex"},
    "source_math": "x = y",
}


def _graph() -> dict:
    raw = (FIXTURE_ROOT / "entry.tex").read_bytes()
    return build_context_dependency_graph(
        FIXTURE_ROOT,
        "entry.tex",
        expected_entry_source_digest=content_digest(raw),
        budget=GRAPH_BUDGET,
    )


def _request(**updates: object) -> dict:
    request = {
        "obligation_digest": OBLIGATION["obligation_digest"],
        "entry_source_digest": content_digest((FIXTURE_ROOT / "entry.tex").read_bytes()),
        "requirement_id": "requirement_policy_pi",
        "requirement_predicate": "The symbol pi is the downstream policy for eq:target.",
        "requirement_subjects": ["pi", "eq:target"],
        "required_node_kinds": ["definition", "notation_declaration"],
        "required_edge_kinds": ["input", "contains", "references"],
        "required_files": [],
        "budget": dict(GRAPH_BUDGET),
    }
    request.update(updates)
    return request


def test_cross_file_declaration_is_source_supported_with_dependency_path() -> None:
    result = resolve_context_requirement(_graph(), OBLIGATION, _request())

    assert result["terminal_state"] == "source_supported"
    assert result["candidates"][0]["dependency_path"]
    assert result["candidates"][0]["source_ref"]["source_digest"]
    assert result["candidates"][0]["applicability_reason"]


def test_not_searched_never_becomes_missing() -> None:
    budget = {**GRAPH_BUDGET, "max_nodes": 1}
    result = resolve_context_requirement(_graph(), OBLIGATION, _request(budget=budget))

    assert result["terminal_state"] == "not_searched"
    assert result["legacy_context_status"]["value"] == "not_searched"
    assert result["budget_exhausted"] is True


def test_not_found_requires_completed_search() -> None:
    request = _request(
        requirement_id="requirement_absent",
        requirement_predicate="A globally Lipschitz constant is declared.",
        requirement_subjects=["globally_lipschitz_constant"],
    )
    complete = resolve_context_requirement(_graph(), OBLIGATION, request)
    assert complete["terminal_state"] == "not_searched"  # missing include prevents closure-wide absence

    clean = deepcopy(_graph())
    clean["diagnostics"] = [
        item for item in clean["diagnostics"]
        if item["kind"] not in {"missing_include", "include_cycle"}
    ]
    clean["unsearched_files"] = []
    clean["graph_digest"] = content_digest({
        key: value for key, value in clean.items() if key != "graph_digest"
    })
    request["entry_source_digest"] = clean["entry_source_digest"]
    complete = resolve_context_requirement(clean, OBLIGATION, request)
    assert complete["terminal_state"] == "not_found_after_search"


def test_context_budget_records_unsearched_files() -> None:
    budget = {**GRAPH_BUDGET, "max_files": 1}
    result = resolve_context_requirement(_graph(), OBLIGATION, _request(budget=budget))

    assert result["terminal_state"] == "not_searched"
    assert result["unsearched_files"]


def test_keyword_match_without_dependency_does_not_source_support() -> None:
    graph = _graph()
    graph["nodes"].append({
        **next(node for node in graph["nodes"] if node["kind"] == "definition"),
        "id": "ctx_unreachable_decoy",
        "source_file": "sibling-decoy.tex",
        "kind": "notation_declaration",
    })
    result = resolve_context_requirement(graph, OBLIGATION, _request())

    assert all(candidate["source_ref"]["file"] != "sibling-decoy.tex" for candidate in result["candidates"])


def test_irrelevant_same_section_text_does_not_close_requirement() -> None:
    request = _request(
        requirement_id="requirement_convexity",
        requirement_predicate="The objective is strictly convex.",
        requirement_subjects=["objective", "strictly_convex"],
    )
    result = resolve_context_requirement(_graph(), OBLIGATION, request)

    assert result["terminal_state"] != "source_supported"


def test_missing_include_blocks_only_dependent_context_claims() -> None:
    local = resolve_context_requirement(_graph(), OBLIGATION, _request())
    dependent = resolve_context_requirement(
        _graph(),
        OBLIGATION,
        _request(
            requirement_id="requirement_missing",
            requirement_predicate="The missing appendix states regularity.",
            requirement_subjects=["regularity"],
            required_files=["shared/missing.tex"],
        ),
    )

    assert local["terminal_state"] == "source_supported"
    assert dependent["terminal_state"] == "not_searched"


def test_resolver_is_deterministic_under_file_creation_order(tmp_path: Path) -> None:
    entries = {
        "entry.tex": "\\input{b}\\input{a}\\n\\label{eq:t} x=y\\n",
        "a.tex": "\\begin{definition}alpha is parameter a for eq:t.\\end{definition}\n",
        "b.tex": "\\begin{definition}beta is parameter b for eq:t.\\end{definition}\n",
    }
    outputs = []
    for order in (list(entries), list(reversed(entries))):
        root = tmp_path / str(len(outputs))
        root.mkdir()
        for name in order:
            (root / name).write_text(entries[name], encoding="utf-8")
        raw = (root / "entry.tex").read_bytes()
        graph = build_context_dependency_graph(
            root,
            "entry.tex",
            expected_entry_source_digest=content_digest(raw),
            budget=GRAPH_BUDGET,
        )
        outputs.append(graph["graph_digest"])

    assert outputs[0] == outputs[1]
