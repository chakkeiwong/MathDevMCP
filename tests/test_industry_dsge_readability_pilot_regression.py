from __future__ import annotations

import json
from pathlib import Path

import pytest

from mathdevmcp.latex_index import build_index, extract_paragraph_context_for_label
from mathdevmcp.math_document_rigor import audit_math_document_rigor


ROOT = Path(__file__).resolve().parent.parent
PILOT_ROOT = ROOT / "tests/fixtures/industry_dsge_readability_pilot"
REPAIRED = PILOT_ROOT / "repaired/document.tex"
MISSING_NEUMANN = PILOT_ROOT / "missing_neumann_condition/document.tex"
FOCUS_LABELS = ["eq:leontief", "eq:domar", "eq:bcrm-production", "eq:bcrm-material"]


@pytest.fixture(scope="module")
def repaired_audit(tmp_path_factory: pytest.TempPathFactory) -> dict:
    output_root = tmp_path_factory.mktemp("industry-dsge-repaired-audit")
    output_md = output_root / "audit.md"
    output_json = output_root / "audit.json"
    result = audit_math_document_rigor(
        REPAIRED,
        output_md=output_md,
        output_json=output_json,
        focus_labels=FOCUS_LABELS,
        max_labels=len(FOCUS_LABELS),
        validation_backends=["sympy"],
    )
    return {"result": result, "output_md": output_md, "output_json": output_json}


@pytest.fixture(scope="module")
def missing_neumann_audit(tmp_path_factory: pytest.TempPathFactory) -> dict:
    output_root = tmp_path_factory.mktemp("industry-dsge-negative-audit")
    result = audit_math_document_rigor(
        MISSING_NEUMANN,
        output_md=output_root / "audit.md",
        output_json=output_root / "audit.json",
        focus_labels=["eq:leontief"],
        max_labels=1,
        validation_backends=["sympy"],
    )
    return result


def _gaps_for_label(result: dict, label: str) -> list[dict]:
    marker = f":{label}:"
    return [
        gap
        for gap in result.get("gaps", [])
        if any(marker in str(ref) for ref in gap.get("evidence_refs", []))
    ]


def _reported_roles(target: dict) -> set[str]:
    roles: set[str] = set()
    for key in ("claim_type", "role"):
        if isinstance(target.get(key), str):
            roles.add(str(target[key]))
    routing = target.get("routing_role")
    if isinstance(routing, dict) and isinstance(routing.get("role"), str):
        roles.add(str(routing["role"]))
    for key in ("roles", "equation_roles", "semantic_roles"):
        value = target.get(key)
        if isinstance(value, list):
            roles.update(str(item) for item in value)
    return roles


def _issue_ledger(result: dict) -> list[dict]:
    for key in ("issues", "issue_ledger", "semantic_issues"):
        value = result.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _subevidence_names(issue: dict) -> set[str]:
    value = issue.get("subevidence", issue.get("obligations", []))
    if not isinstance(value, list):
        return set()
    names: set[str] = set()
    for item in value:
        if isinstance(item, str):
            names.add(item)
        elif isinstance(item, dict):
            for key in ("id", "kind", "name", "obligation"):
                if isinstance(item.get(key), str):
                    names.add(str(item[key]))
    return names


def test_fixture_freezes_the_repaired_context_and_matched_negative_control() -> None:
    repaired = REPAIRED.read_text(encoding="utf-8")
    missing = MISSING_NEUMANN.read_text(encoding="utf-8")

    assert set(FOCUS_LABELS) == {
        "eq:leontief",
        "eq:domar",
        "eq:bcrm-production",
        "eq:bcrm-material",
    }
    assert all(f"\\label{{{label}}}" in repaired for label in FOCUS_LABELS)
    assert "\\Omega\\in\\mathbb{R}^{J\\times J}_{+}" in repaired
    assert "\\rho(\\Omega)<1" in repaired
    assert "then $I-\\Omega$ is invertible" in repaired
    assert "Neumann series" in repaired
    assert "source-stated maintained" in repaired
    assert "\\section{A quantitative multisector DSGE: \\BCRM{} (2009)}" in repaired
    assert "\\label{eq:leontief}" in missing
    assert "\\rho(\\Omega)<1" not in missing
    assert "is invertible" not in missing


def test_repaired_context_closes_issue_while_negative_control_stays_open(
    repaired_audit: dict,
    missing_neumann_audit: dict,
) -> None:
    repaired_gaps = _gaps_for_label(repaired_audit["result"], "eq:leontief")
    missing_gaps = _gaps_for_label(missing_neumann_audit, "eq:leontief")

    assert not any(gap.get("label") == "invertibility_required" for gap in repaired_gaps)
    assert any(gap.get("label") == "invertibility_required" for gap in missing_gaps)


def test_context_closure_cites_resolving_spans(repaired_audit: dict) -> None:
    issues = [
        item
        for item in _issue_ledger(repaired_audit["result"])
        if str(item.get("issue_id", item.get("id", ""))).startswith("eq:leontief/")
    ]
    assert len(issues) == 1
    support = issues[0].get("existing_context_support")

    assert issues[0].get("status") == "resolved_by_existing_context"
    assert isinstance(support, list) and support
    assert all(
        isinstance(item, dict)
        and isinstance(item.get("line_start"), int)
        and isinstance(item.get("line_end"), int)
        and item["line_start"] <= item["line_end"]
        and item.get("text")
        for item in support
    )
    assert any("\\rho(\\Omega)<1" in item["text"] for item in support)


def test_role_first_routing_distinguishes_equation_semantics(repaired_audit: dict) -> None:
    targets = {
        item["label"]: item for item in repaired_audit["result"]["target_selection"]["targets"]
    }

    assert {"definition", "conditional_identity"}.issubset(_reported_roles(targets["eq:leontief"]))
    assert "maintained_assumption" in _reported_roles(targets["eq:bcrm-production"])
    assumption_evidence = next(
        item
        for item in targets["eq:bcrm-production"]["equation_role_evidence"]
        if item["role"] == "maintained_assumption"
    )
    assert assumption_evidence["authority"] == "source_evidenced_role"
    assert targets["eq:bcrm-production"]["route_metadata"]["family"] == "symbolic_exposition"
    assert "numeric_diagnostic_without_numeric_artifact" in targets["eq:bcrm-production"]["route_metadata"]["route_vetoes"]
    assert any(
        "source-stated maintained" in span["text"]
        and isinstance(span["line_start"], int)
        and span["line_start"] <= span["line_end"]
        for span in assumption_evidence["source_spans"]
    )


def test_leontief_route_evidence_has_one_semantic_issue(repaired_audit: dict) -> None:
    result = repaired_audit["result"]
    issues = [
        issue
        for issue in _issue_ledger(result)
        if str(issue.get("issue_id", issue.get("id", ""))).startswith("eq:leontief/")
    ]

    assert len(issues) == 1
    assert {
        "dimension_contract",
        "invertibility",
        "neumann_convergence",
    }.issubset(_subevidence_names(issues[0]))


def test_symbolic_exposition_does_not_request_numeric_solve(
    missing_neumann_audit: dict,
) -> None:
    gaps = _gaps_for_label(missing_neumann_audit, "eq:leontief")

    assert not any(gap.get("kind") == "add_diagnostic_check" for gap in gaps)
    assert "linear_solve_residual_check" not in json.dumps(missing_neumann_audit, sort_keys=True)


def test_inverse_wording_uses_correct_general_requirement(repaired_audit: dict) -> None:
    markdown = repaired_audit["output_md"].read_text(encoding="utf-8")
    forensic = repaired_audit["result"]["forensic_markdown"]

    assert "invertible or positive-definite" not in markdown
    assert "invertible or positive-definite" not in forensic
    assert "invertibility" in markdown or "nonsingularity" in markdown


def test_macro_bearing_section_preserves_hierarchy() -> None:
    index = build_index(REPAIRED.parent)

    assert index["labels"]["eq:bcrm-production"]["section_path"] == [
        r"A quantitative multisector DSGE: \BCRM{} (2009)",
        "Question and model architecture",
    ]


def test_status_counts_only_actionable_repairs_as_proposals(repaired_audit: dict) -> None:
    result = repaired_audit["result"]
    fix_report = result["source_reports"]["audit_and_propose_fix"]

    assert result["coverage"]["proposal_count"] == result["coverage"]["concrete_repair_count"]
    assert fix_report["status"] != "proposal_ready"


def test_negative_fixture_gets_noncertifying_exposition_patch(
    missing_neumann_audit: dict,
) -> None:
    actionable = [
        proposal
        for proposal in missing_neumann_audit.get("proposals", [])
        if proposal.get("status") in {"actionable_patch", "actionable_assumption_text"}
    ]
    assert len(actionable) == 1
    patch = actionable[0]
    patch_text = "\n".join(
        str(patch.get(key, ""))
        for key in ("candidate_patch", "assumption_statement", "replacement_latex", "proposed_fix")
    )

    assert patch.get("patch_class") == "candidate_exposition_patch_not_certificate"
    assert "\\rho(\\Omega)<1" in patch_text
    assert "invertible" in patch_text
    assert "Neumann" in patch_text


def test_actionable_human_report_is_bounded(repaired_audit: dict) -> None:
    result = repaired_audit["result"]
    actionable = result.get("actionable_markdown", result["markdown"])

    assert len(actionable.splitlines()) < 200
    assert "## Backend Provenance" not in actionable
    assert "artifact" in actionable.lower() or "evidence" in actionable.lower()


def test_high_level_audit_binds_bounded_context_and_symbolic_task(repaired_audit: dict) -> None:
    result = repaired_audit["result"]
    tool_use = next(
        item
        for item in result["tool_uses"]
        if item.get("tool") == "audit_derivation_v2_label"
        and item.get("arguments", {}).get("label") == "eq:leontief"
    )

    assert tool_use["arguments"]["paragraph_context"] is True
    assert tool_use["arguments"]["before"] == 4
    assert tool_use["arguments"]["after"] == 1
    assert tool_use["arguments"]["task_context"] == "symbolic_exposition"


def test_repaired_fixture_has_no_actionable_repairs_and_raw_evidence_is_preserved(
    repaired_audit: dict,
) -> None:
    result = repaired_audit["result"]
    fix_report = result["source_reports"]["audit_and_propose_fix"]

    assert result["coverage"]["gap_count"] == 0
    assert result["coverage"]["proposal_count"] == 0
    assert result["coverage"]["concrete_repair_count"] == 0
    assert result["coverage"]["resolved_by_existing_context_count"] == 3
    assert fix_report["status"] == "no_proposal"
    assert result["source_reports"]["raw_route_gaps"]


def test_dependent_domar_inverse_reuses_the_stated_leontief_condition(repaired_audit: dict) -> None:
    issues = [
        item
        for item in _issue_ledger(repaired_audit["result"])
        if str(item.get("issue_id", "")).startswith("eq:domar/")
    ]

    assert len(issues) == 1
    assert issues[0]["status"] == "resolved_by_existing_context"
    assert not issues[0]["unresolved_obligations"]
    assert any("\\rho(\\Omega)<1" in item["text"] for item in issues[0]["existing_context_support"])


def test_actionable_and_forensic_reports_remain_separate(repaired_audit: dict) -> None:
    result = repaired_audit["result"]
    written = repaired_audit["output_md"].read_text(encoding="utf-8")

    assert written == result["actionable_markdown"] == result["markdown"]
    assert "## Backend Provenance" not in result["actionable_markdown"]
    assert "## Backend Provenance" in result["forensic_markdown"]
    assert "source_reports" in result["actionable_markdown"]
