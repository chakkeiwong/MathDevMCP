from pathlib import Path

from mathdevmcp.workflow import build_implementation_brief


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"


def test_build_implementation_brief_reports_consistent_case():
    result = build_implementation_brief(
        str(FIXTURES),
        "transport log-determinant identity",
        str(FIXTURES / "doc_consistency_good.py"),
        required_terms=["logdet"],
    )

    assert result["selected_label"] == "prop:transport-logdet"
    assert result["status"] == "consistent"
    assert result["checks"]["consistency"]["status"] == "consistent"
    assert result["doc_context"]["file"] == "doc_consistency_good.tex"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "implementation_brief"}
    assert result["provenance"]["label"] == "prop:transport-logdet"
    assert result["ok"] is True



def test_build_implementation_brief_reports_unverified_derivation():
    result = build_implementation_brief(
        str(FIXTURES),
        "transport log-determinant identity",
        str(FIXTURES / "doc_consistency_good.py"),
        required_terms=["logdet"],
        lhs="log_pi + logdet",
        rhs="logdet + log_pi",
    )

    assert result["status"] == "unverified"
    assert result["checks"]["derivation"]["status"] == "unverified"
    assert result["checks"]["derivation"]["metadata"] == {"schema_version": "1.0", "contract": "label_derivation_result"}
    assert result["checks"]["derivation"]["step_chain"] == [{"label": "prop:transport-logdet", "supported_by_context": False, "cited_labels": []}]


def test_build_implementation_brief_reuses_cache(tmp_path):
    cache = tmp_path / "workflow_index_cache.json"

    cold = build_implementation_brief(
        str(FIXTURES),
        "transport log-determinant identity",
        str(FIXTURES / "doc_consistency_good.py"),
        required_terms=["logdet"],
        cache_path=cache,
    )
    warm = build_implementation_brief(
        str(FIXTURES),
        "transport log-determinant identity",
        str(FIXTURES / "doc_consistency_good.py"),
        required_terms=["logdet"],
        cache_path=cache,
    )

    assert cold["cache"] == {"path": str(cache), "hit": False}
    assert warm["cache"] == {"path": str(cache), "hit": True}
    assert warm["status"] == "consistent"
    assert warm["checks"]["consistency"]["doc_context"]["file"] == "doc_consistency_good.tex"
