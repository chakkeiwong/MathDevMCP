from __future__ import annotations

from pathlib import Path

import pytest

from mathdevmcp.document_context_graph import build_context_dependency_graph
from mathdevmcp.evidence_manifest import EvidenceValidationError, content_digest
from mathdevmcp.latex_index import discover_entry_rooted_tex_files


ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = ROOT / "tests/fixtures/document_context_graph"
DEFAULT_BUDGET = {
    "max_files": 8,
    "max_bytes": 1_048_576,
    "max_nodes": 256,
    "max_edges": 512,
    "max_dependency_expansions": 64,
}


def _graph(entry: str = "entry.tex") -> dict:
    raw = (FIXTURE_ROOT / entry).read_bytes()
    return build_context_dependency_graph(
        FIXTURE_ROOT,
        entry,
        expected_entry_source_digest=content_digest(raw),
        budget=DEFAULT_BUDGET,
    )


def test_cross_file_definition_is_retrieved_by_dependency() -> None:
    graph = _graph()

    definitions = [node for node in graph["nodes"] if node["kind"] == "definition"]
    assert any(node["source_file"] == "shared/definitions.tex" for node in definitions)
    assert any(
        edge["kind"] == "input"
        and edge["source_file"] == "entry.tex"
        and edge["target_file"] == "shared/definitions.tex"
        for edge in graph["edges"]
    )


def test_duplicate_labels_remain_file_scoped() -> None:
    graph = _graph()
    duplicates = [
        node for node in graph["nodes"]
        if node["kind"] == "label" and node["declaration_key"] == "eq:duplicate"
    ]

    assert {node["source_file"] for node in duplicates} == {
        "shared/cycle-a.tex",
        "shared/definitions.tex",
    }
    assert any(item["kind"] == "duplicate_label" for item in graph["diagnostics"])


def test_missing_include_is_engineering_diagnostic() -> None:
    graph = _graph()
    missing = [item for item in graph["diagnostics"] if item["kind"] == "missing_include"]

    assert len(missing) == 1
    assert missing[0]["target_file"] == "shared/missing.tex"
    assert missing[0]["classification"] == "engineering"


def test_unrelated_sibling_tex_is_excluded_from_entry_corpus() -> None:
    graph = _graph()

    assert "sibling-decoy.tex" in graph["excluded_sibling_files"]
    assert "sibling-decoy.tex" not in graph["reachable_files"]
    assert all(node["source_file"] != "sibling-decoy.tex" for node in graph["nodes"])


def test_include_cycle_is_bounded_and_recorded() -> None:
    graph = _graph()

    assert graph["reachable_files"].count("shared/cycle-a.tex") == 1
    assert any(item["kind"] == "include_cycle" for item in graph["diagnostics"])


def test_out_of_root_and_symlink_include_are_integrity_vetoes(tmp_path: Path) -> None:
    (tmp_path / "entry.tex").write_text("\\input{../outside}\n", encoding="utf-8")
    discovery = discover_entry_rooted_tex_files(tmp_path, "entry.tex", budget=DEFAULT_BUDGET)
    assert "path_traversal" in {item["kind"] for item in discovery.diagnostics}
    assert discovery.integrity_vetoes

    (tmp_path / "real.tex").write_text("x", encoding="utf-8")
    (tmp_path / "link.tex").symlink_to(tmp_path / "real.tex")
    (tmp_path / "entry2.tex").write_text("\\input{link}\n", encoding="utf-8")
    discovery = discover_entry_rooted_tex_files(tmp_path, "entry2.tex", budget=DEFAULT_BUDGET)
    assert "symlink_include" in {item["kind"] for item in discovery.diagnostics}
    assert discovery.integrity_vetoes


def test_every_context_node_has_digest_and_exact_span() -> None:
    graph = _graph()
    snapshots = {item["logical_ref"]: (FIXTURE_ROOT / item["logical_ref"]).read_bytes() for item in graph["files"]}

    for node in graph["nodes"]:
        assert len(node["source_digest"]) == 64
        assert node["byte_span"]["start"] < node["byte_span"]["end"] or node["kind"] == "file"
        assert node["line_span"]["start"] >= 1
        raw = snapshots[node["source_file"]]
        start, end = node["byte_span"]["start"], node["byte_span"]["end"]
        assert raw[start:end].decode("utf-8") == node["source_text"]


def test_comment_scanner_preserves_only_live_include_span() -> None:
    discovery = discover_entry_rooted_tex_files(FIXTURE_ROOT, "commented.tex", budget=DEFAULT_BUDGET)
    directives = discovery.snapshots["commented.tex"].directives

    assert len(directives) == 1
    directive = directives[0]
    raw = (FIXTURE_ROOT / "commented.tex").read_bytes()
    assert raw[directive["byte_span"]["start"]:directive["byte_span"]["end"]] == b"\\input{shared/definitions}"


def test_missing_entry_ref_fails_closed() -> None:
    with pytest.raises(EvidenceValidationError):
        discover_entry_rooted_tex_files(FIXTURE_ROOT, "absent.tex", budget=DEFAULT_BUDGET)
