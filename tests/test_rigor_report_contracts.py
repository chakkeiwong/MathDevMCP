from __future__ import annotations

from copy import deepcopy

import pytest

from mathdevmcp.rigor_report_contracts import (
    build_editorial_integration_records,
    compare_rigor_reports,
    semantic_issue_digest,
    validate_obligation_metadata,
    page_rigor_report_records,
)
from mathdevmcp.agent_report_artifacts import persist_agent_report


def _issue(issue_id: str, status: str, obligations: list[str]) -> dict:
    return {
        "issue_id": issue_id,
        "label": issue_id.split("/", 1)[0],
        "family": "test-family",
        "status": status,
        "roles": ["definition"],
        "location": "document.tex:1-3",
        "unresolved_obligations": obligations,
        "route_evidence": [{"runtime_seconds": 3.2}],
        "math_nonclaim": "Diagnostic evidence is not proof.",
    }


def _report(issues: list[dict], *, digest: str = "a" * 64) -> dict:
    return {
        "source": {"file": "document.tex", "canonical_path": "/tmp/document.tex", "source_digest": digest},
        "target_selection": {"targets": [{"label": "eq:a"}, {"label": "eq:b"}, {"label": "eq:c"}]},
        "issues": issues,
        "metadata": {"schema_version": "1.0", "contract": "math_document_rigor_audit"},
        "backend_provenance": {"runtime": "ignored"},
    }


def test_lifecycle_comparison_reports_all_transition_classes() -> None:
    prior = _report(
        [
            _issue("eq:a/a", "unresolved", ["x", "y"]),
            _issue("eq:b/b", "unresolved", ["x"]),
            _issue("eq:c/c", "partially_resolved", ["x"]),
            _issue("eq:d/d", "unresolved", ["x"]),
        ]
    )
    current = _report(
        [
            _issue("eq:a/a", "partially_resolved", ["x"]),
            _issue("eq:b/b", "resolved_by_existing_context", []),
            _issue("eq:c/c", "unresolved", ["x", "y"]),
            _issue("eq:e/e", "unresolved", ["x"]),
        ]
    )

    comparison = compare_rigor_reports(current, prior)
    by_id = {item["issue_id"]: item["status"] for item in comparison["transitions"]}

    assert comparison["status"] == "compared"
    assert by_id == {
        "eq:a/a": "improved_but_open",
        "eq:b/b": "closed",
        "eq:c/c": "regressed",
        "eq:d/d": "closed",
        "eq:e/e": "new",
    }


def test_runtime_only_changes_do_not_change_issue_identity_or_lifecycle() -> None:
    prior_issue = _issue("eq:a/a", "unresolved", ["x"])
    current_issue = deepcopy(prior_issue)
    current_issue["route_evidence"] = [{"runtime_seconds": 99, "backend": "other"}]
    current_issue["backend_environment"] = {"python": "/different/runtime"}

    comparison = compare_rigor_reports(_report([current_issue]), _report([prior_issue]))

    assert semantic_issue_digest(current_issue) == semantic_issue_digest(prior_issue)
    assert comparison["transitions"][0]["status"] == "unchanged"


def test_cross_source_comparison_fails_closed_without_controlled_revision() -> None:
    comparison = compare_rigor_reports(
        _report([_issue("eq:a/a", "resolved_by_existing_context", [])], digest="b" * 64),
        _report([_issue("eq:a/a", "unresolved", ["x"])], digest="a" * 64),
    )

    assert comparison["status"] == "inconclusive"
    assert "unbound_source_revision" in comparison["reasons"]
    assert comparison["transitions"] == []


def test_same_basename_different_canonical_path_fails_closed() -> None:
    current = _report([_issue("eq:a/a", "resolved_by_existing_context", [])])
    prior = _report([_issue("eq:a/a", "unresolved", ["x"])])
    current["source"]["canonical_path"] = "/tmp/current/document.tex"
    prior["source"]["canonical_path"] = "/tmp/prior/document.tex"

    comparison = compare_rigor_reports(current, prior)

    assert comparison["status"] == "inconclusive"
    assert "mismatched_canonical_path" in comparison["reasons"]


def test_controlled_revision_manifest_allows_source_bound_closure() -> None:
    manifest = {
        "schema_version": "rigor_report_revision@1",
        "prior_source_digest": "a" * 64,
        "current_source_digest": "b" * 64,
        "source_file": "document.tex",
        "canonical_path": "/tmp/document.tex",
        "labels": ["eq:a", "eq:b", "eq:c"],
        "relation": "controlled_revision",
    }
    comparison = compare_rigor_reports(
        _report([_issue("eq:a/a", "resolved_by_existing_context", [])], digest="b" * 64),
        _report([_issue("eq:a/a", "unresolved", ["x"])], digest="a" * 64),
        revision_manifest=manifest,
    )

    assert comparison["status"] == "compared"
    assert comparison["source_relation"] == "controlled_revision"
    assert comparison["transitions"][0]["status"] == "closed"


def test_obligation_metadata_is_source_bound_and_advisory() -> None:
    source = {"file": "document.tex", "source_digest": "a" * 64}
    metadata = {
        "schema_version": "obligation_metadata@1",
        "source": source,
        "entries": [
            {
                "label": "eq:a",
                "obligations": [
                    {"id": "timing", "statement": "State the information set.", "provenance": "author_supplied"}
                ],
            }
        ],
    }

    validated = validate_obligation_metadata(metadata, source=source, selected_labels=["eq:a"])
    record = build_editorial_integration_records(
        [_issue("eq:a/a", "unresolved", ["dimension"])],
        source=source,
        obligation_metadata=validated,
    )[0]

    assert record["schema_version"] == "exposition_surface_diagnostics@1"
    assert record["author_metadata"][0]["provenance"] == "author_supplied"
    assert record["author_metadata"][0]["authority"] == "advisory_not_source_truth"
    assert record["unresolved_obligations"][0]["provenance"] == "inferred"
    assert record["requires_human_review"] is False


@pytest.mark.parametrize(
    "mutation",
    [
        lambda value: value["source"].update(source_digest="b" * 64),
        lambda value: value["entries"][0].update(label="eq:unknown"),
        lambda value: value["entries"][0]["obligations"][0].update(provenance="source_evidenced"),
    ],
)
def test_invalid_obligation_metadata_fails_closed(mutation) -> None:
    source = {"file": "document.tex", "source_digest": "a" * 64}
    metadata = {
        "schema_version": "obligation_metadata@1",
        "source": dict(source),
        "entries": [
            {
                "label": "eq:a",
                "obligations": [
                    {"id": "timing", "statement": "State timing.", "provenance": "author_supplied"}
                ],
            }
        ],
    }
    mutation(metadata)

    with pytest.raises(ValueError):
        validate_obligation_metadata(metadata, source=source, selected_labels=["eq:a"])


def test_forensic_collection_paging_is_digest_bound_and_allowlisted(tmp_path):
    report = _report([_issue("eq:a/a", "unresolved", ["x"])])
    report["metadata"] = {"schema_version": "1.0", "contract": "math_document_rigor_audit"}
    report["tool_uses"] = [{"tool": "sympy"}, {"tool": "lean"}]
    artifact = persist_agent_report(report, tmp_path)

    page = page_rigor_report_records(str(tmp_path), artifact["sha256"], "tool_uses", limit=1)
    assert page["metadata"]["contract"] == "math_document_rigor_record_page"
    assert page["total_count"] == 2
    assert page["next_offset"] == 1
    assert page["records"][0]["record"]["tool"] == "sympy"
    with pytest.raises(ValueError):
        page_rigor_report_records(str(tmp_path), artifact["sha256"], "backend_provenance")
