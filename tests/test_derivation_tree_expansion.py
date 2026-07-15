from mathdevmcp.derivation_search_tree import (
    BlockerNode,
    SourceSpan,
    build_initial_search_tree,
    validate_search_tree,
)
from mathdevmcp.derivation_tree_expansion import expand_tree_with_hypotheses


CAPABILITIES = {
    "sympy": {"available": True, "status": "available", "version": "1.14.0"},
    "sage": {"available": False, "status": "unavailable"},
    "lean": {"available": False, "status": "unavailable"},
}

INTEGRATIONS = {
    "leansearchv2": {"resolved_available": False},
    "lean_explore": {"resolved_available": False},
    "jixia": {"resolved_available": False},
    "pantograph": {"resolved_available": False},
    "lean_dojo": {"resolved_available": False},
}


def _tree_with_blocker() -> dict:
    tree = build_initial_search_tree(
        r"\E[X \mid z]",
        source_span=SourceSpan(file="paper.tex", line_start=10, line_end=12, label="eq:test"),
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
    )
    tree["root"]["blockers"].append(
        {
            "id": "blocker_conditional_law",
            "kind": "conditional_law_translation_required",
            "problem": "Conditional law is not encoded.",
            "why": "The expectation needs a conditional law.",
            "required_next_evidence": "State the law.",
            "source": "test",
            "evidence_refs": ["typed:test"],
        }
    )
    return tree


def test_expand_tree_with_hypotheses_creates_child_nodes_with_parent_provenance() -> None:
    result = expand_tree_with_hypotheses(_tree_with_blocker(), budget={"max_nodes": 2, "max_agent_expansions_per_blocker": 2})

    assert result["metadata"]["contract"] == "derivation_tree_expansion_result"
    assert result["status"] == "expanded"
    assert result["expanded_node_count"] == 2
    assert result["validation_errors"] == []
    children = result["tree"]["root"]["children"]
    assert len(children) == 2
    for child in children:
        assert child["status"] == "expanded_by_rule"
        assert child["generator"]["kind"] == "rule_generated"
        assert child["parent_node_id"] == "root"
        assert child["parent_blocker_id"] == "blocker_conditional_law"
        assert child["agent_hypothesis"]["status"] == "candidate_pending_tree_verification"
        assert child["backend_attempts"] == []
        assert child["backend_formalization_targets"]
        assert child["backend_formalization_targets"][0]["metadata"]["contract"] == "backend_formalization_target"
        assert child["blockers"][0]["kind"] == "backend_evidence_required"
    assert result["summary"]["node_count"] == 3
    assert validate_search_tree(result["tree"]) == []


def test_expand_tree_budget_exhaustion_is_explicit() -> None:
    result = expand_tree_with_hypotheses(_tree_with_blocker(), budget={"max_nodes": 1, "max_agent_expansions_per_blocker": 2})

    assert result["expanded_node_count"] == 1
    assert result["budget_exhausted"] is True
    assert result["skipped"]
    assert result["skipped"][0]["reason"] == "max_nodes_exhausted"


def test_expand_tree_invalid_tree_returns_bounded_failure() -> None:
    result = expand_tree_with_hypotheses({"root": None})

    assert result["status"] == "invalid_tree"
    assert result["validation_errors"] == ["root must be a dict"]
