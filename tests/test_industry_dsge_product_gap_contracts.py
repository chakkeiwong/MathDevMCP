from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from mathdevmcp.agent_report_artifacts import persist_agent_report, resolve_agent_report
from mathdevmcp.math_document_rigor import audit_math_document_rigor
from mathdevmcp.math_document_rigor import plan_math_document_rigor_audit
from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.document_exposition import build_exposition_projection
from mathdevmcp.rigor_report_contracts import page_rigor_report_records


ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "tests/fixtures/industry_dsge_readability_pilot/missing_neumann_condition/document.tex"
PILOT_FIXTURES = ROOT / "tests/fixtures/industry_dsge_readability_pilot"


def test_compact_report_exposes_integration_and_lifecycle_pointer(tmp_path) -> None:
    result = audit_math_document_rigor(
        FIXTURE,
        focus_labels=["eq:leontief"],
        max_labels=1,
        validation_backends=["sympy"],
    )
    compact = call_mcp_tool(
        "audit_math_document_rigor",
        {
            "tex_path": str(FIXTURE),
            "focus_labels": ["eq:leontief"],
            "max_labels": 1,
            "validation_backends": ["sympy"],
            "response_mode": "compact",
            "artifact_root": str(tmp_path),
        },
    )

    assert compact["report_profile"] == "actionable"
    assert compact["editorial_integration"]["schema_version"] == "exposition_surface_diagnostics@1"
    resolved = resolve_agent_report(str(tmp_path), compact["artifact"]["sha256"])
    assert resolved["report"]["source"] == result["source"]
    assert resolved["artifact"]["sha256"] == compact["artifact"]["sha256"]
    assert compact["non_claims"]


def test_forensic_pages_reconstruct_exact_records_and_reject_invalid_requests(tmp_path) -> None:
    result = audit_math_document_rigor(
        FIXTURE,
        focus_labels=["eq:leontief"],
        max_labels=1,
        report_profile="forensic",
        validation_backends=["sympy"],
    )
    artifact = persist_agent_report(result, tmp_path)
    page = page_rigor_report_records(str(tmp_path), artifact["sha256"], "issues", limit=1)

    assert page["records"]
    record = page["records"][0]
    assert record["record_sha256"] == hashlib.sha256(
        json.dumps(record["record"], sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    assert page["artifact"]["sha256"] == artifact["sha256"]

    with pytest.raises(ValueError):
        page_rigor_report_records(str(tmp_path), artifact["sha256"], "not_allowlisted")
    with pytest.raises(ValueError):
        page_rigor_report_records(str(tmp_path), "0" * 64, "issues")
    (tmp_path / "agent-reports" / f"{artifact['sha256']}.json").write_bytes(b"tampered")
    with pytest.raises(ValueError, match="digest mismatch"):
        page_rigor_report_records(str(tmp_path), artifact["sha256"], "issues")


def test_unknown_role_is_human_classification_and_not_a_proof_route() -> None:
    from mathdevmcp.document_exposition import classify_exposition_roles, enrich_targets_with_exposition_roles

    target = {"label": "eq:unknown", "text": "x = y", "exposition_context": {"paragraphs": []}}
    roles = classify_exposition_roles(target)
    enriched = enrich_targets_with_exposition_roles([target])[0]

    assert [item["role"] for item in roles] == ["unknown"]
    assert enriched["primary_exposition_route"]["route"] == "human_classification"
    assert enriched["route_metadata"]["formal_backend_authorized"] is False


@pytest.mark.parametrize(
    ("text", "expected_role", "expected_family"),
    [
        ("The equilibrium condition clears the market.", "equilibrium_condition", "symbolic_exposition"),
        ("We use a first-order linearization.", "approximation_linearization", "symbolic_exposition"),
        ("The estimator minimizes the objective function.", "estimator_objective", "symbolic_exposition"),
        ("According to the source, the empirical result is positive.", "source_reported_result", "source_reconstruction"),
        ("We derive the following result; therefore it holds locally.", "local_derived_claim", "formal_proof_candidate"),
        ("This is a heuristic conjecture.", "conjecture_heuristic", "human_review"),
    ],
)
def test_bounded_role_matrix_preserves_route_veto_boundary(text, expected_role, expected_family) -> None:
    from mathdevmcp.document_exposition import enrich_targets_with_exposition_roles

    target = {"label": "eq:role", "text": "x = y", "exposition_context": {"paragraphs": [{"text": text}]}}
    enriched = enrich_targets_with_exposition_roles([target])[0]

    assert expected_role in enriched["equation_roles"]
    assert enriched["route_metadata"]["family"] == expected_family
    assert enriched["route_metadata"]["formal_backend_authorized"] is (expected_family == "formal_proof_candidate")


def _project_fixture(name: str) -> tuple[dict, dict]:
    plan = plan_math_document_rigor_audit(
        PILOT_FIXTURES / name / "document.tex",
        focus_labels=["eq:leontief"],
        max_labels=1,
        context_before=4,
        context_after=1,
    )
    projection = build_exposition_projection(plan["target_selection"]["targets"], [])
    return projection["targets"][0], projection["issues"][0]


@pytest.mark.parametrize(
    ("fixture_name", "missing_id"),
    [
        ("missing_dimension", "dimension_or_domain_declaration"),
        ("missing_identity_definition", "identity_definition"),
        ("missing_path_interpretation", "path_interpretation"),
    ],
)
def test_negative_exposition_fixtures_reproduce_missing_surface(fixture_name, missing_id) -> None:
    target, _issue = _project_fixture(fixture_name)
    surface = target["exposition_surface_diagnostics"]

    assert missing_id in surface["missing_required_ids"]
    assert surface["non_claim"].startswith("These are bounded source-surface observations")


def test_distant_assumption_does_not_silently_close_local_neumann_obligation() -> None:
    target, issue = _project_fixture("distant_assumption")
    surface = target["exposition_surface_diagnostics"]

    assert "assumption_or_restriction" in surface["missing_required_ids"]
    assert "neumann_convergence" in issue["unresolved_obligations"]
    assert issue["status"] != "resolved_by_existing_context"
