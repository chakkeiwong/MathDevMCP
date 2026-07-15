import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import mathdevmcp.document_derivation_tree as document_tree
from mathdevmcp.derivation_branch_controller import can_derive_with_budget
from mathdevmcp.document_derivation_tree import audit_document_derivation_tree
from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.mcp_server import audit_document_derivation_tree as server_audit_document_derivation_tree


ROOT = Path(__file__).resolve().parent.parent
RAW_PROMOTION_PATH = "targets[*].tree.assumption_branches[*].backend_evidence.raw_promotion"
INLINE_RAW_PROMOTION_PATH = (
    "targets[*].record.tree.assumption_branches[*].backend_evidence.raw_promotion"
)
RAW_PROMOTED_COUNT_PATH = "coverage.raw_promoted_count"


def _write_equations(path: Path, equations: list[tuple[str, str]]) -> None:
    path.write_text(
        "\n".join(
            "\\begin{equation}\n"
            f"\\label{{{label}}}\n"
            f"{expression}\n"
            "\\end{equation}"
            for label, expression in equations
        ),
        encoding="utf-8",
    )


def _normalized_path(path: tuple[str, ...]) -> str:
    normalized = ""
    for part in path:
        if part == "[*]":
            normalized += part
        elif normalized:
            normalized += f".{part}"
        else:
            normalized = part
    return normalized


def _walk(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = (*path, str(key))
            yield child_path, key, child
            yield from _walk(child, child_path)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child, (*path, "[*]"))


def _assert_document_quarantine(payload: dict[str, Any]) -> None:
    raw_paths: set[str] = set()
    for path, key, value in _walk(payload):
        normalized = _normalized_path(path)
        if key == "publishable_as_repair":
            assert value is False, normalized
        if key in {"proposed_edit", "proposed_text"}:
            raise AssertionError(f"applicable edit key leaked at {normalized}")
        if key == "promoted_count":
            assert value == 0, normalized
        if key == "raw_promotion":
            raw_paths.add(normalized)
            assert normalized in {RAW_PROMOTION_PATH, INLINE_RAW_PROMOTION_PATH}
            assert isinstance(value, dict)
            assert not any(
                nested in value
                for nested in {
                    "promotion",
                    "effective_document_promotion",
                    "raw_promotion",
                    "promoted_count",
                    "raw_promoted_count",
                }
            )
        if key == "raw_promoted_count":
            raw_paths.add(normalized)
            assert normalized == RAW_PROMOTED_COUNT_PATH
        if key == "can_promote" and value is True:
            assert _normalized_path(path[:-1]) in {
                RAW_PROMOTION_PATH,
                INLINE_RAW_PROMOTION_PATH,
            }, normalized
    assert raw_paths <= {
        RAW_PROMOTION_PATH,
        INLINE_RAW_PROMOTION_PATH,
        RAW_PROMOTED_COUNT_PATH,
    }


def _single_report(result: dict[str, Any]) -> dict[str, Any]:
    tree = result["targets"][0]["tree"]
    reports = [*tree["document_partial_evidence_reports"], *tree["document_gap_reports"]]
    assert len(reports) == 1
    return reports[0]


def test_simple_algebra_root_evidence_does_not_become_child_repair_evidence(tmp_path: Path) -> None:
    tex = tmp_path / "simple.tex"
    _write_equations(tex, [("eq:simple", "x + 1 = 1 + x")])

    result = audit_document_derivation_tree(tex, focus_labels=["eq:simple"], max_attempts=2)
    target = result["targets"][0]
    branch = target["tree"]["assumption_branches"][0]
    compiler = target["tree"]["tool_grounded_proposal_compiler"]
    gap = target["tree"]["document_gap_reports"][0]

    assert result["publication_mode"] == compiler["publication_mode"] == "disabled"
    assert result["coverage"]["promoted_count"] == 0
    assert result["coverage"]["raw_promoted_count"] == 1
    assert result["coverage"]["document_ready_repair_proposal_count"] == 0
    assert result["coverage"]["document_partial_evidence_report_count"] == 0
    assert result["coverage"]["document_gap_report_count"] == 1
    assert target["status"] == "partial_evidence"
    assert target["promotion"]["can_promote"] is False
    assert target["tree"]["backend_attempts"][0]["status"] == "proved"
    assert target["tree"]["backend_attempts"][0]["applicable_to_document_branch"] is False
    assert branch["backend_attempts"] == []
    assert branch["backend_evidence"]["raw_promotion"]["can_promote"] is False
    assert branch["backend_evidence"]["effective_document_promotion"]["can_promote"] is False
    assert branch["backend_evidence"]["binding_status"] == "no_branch_evidence"
    assert compiler["repair_proposal_count"] == 0
    assert compiler["partial_evidence_count"] == 0
    assert compiler["gap_report_count"] == 1
    assert compiler["document_ready_repair_proposals"] == []
    assert compiler["compiled_items"][0]["publishable_as_repair"] is False
    assert compiler["compiled_items"][0]["publishable_as_gap_report"] is True
    assert compiler["compiled_items"][0]["reportable_as_partial_evidence"] is False
    assert compiler["final_tree_digest"] == target["tree"]["final_tree_digest"]
    assert gap["metadata"]["contract"] == "document_gap_report"
    assert gap["failure_classification"] == "branch_execution_pending"
    assert gap["failure_classifications"] == [
        "branch_execution_pending",
        "formalization_blocked",
    ]
    assert gap["backend_evidence"]["binding_status"] == "no_branch_evidence"
    _assert_document_quarantine({key: value for key, value in result.items() if key != "markdown"})
    assert "Document gap reports" in result["markdown"]
    assert "Publication mode: `disabled`" in result["markdown"]


def test_x_over_x_preserves_nonzero_requirement_after_raw_backend_success(tmp_path: Path) -> None:
    tex = tmp_path / "division.tex"
    _write_equations(tex, [("eq:division", "x / x = 1")])

    result = audit_document_derivation_tree(tex, focus_labels=["eq:division"], max_attempts=2)
    report = _single_report(result)

    assert result["coverage"]["raw_promoted_count"] == 1
    assert result["coverage"]["promoted_count"] == 0
    assert any("denominator is nonzero" in item["text"] for item in report["missing_or_unresolved_assumptions"])
    assert report["failure_classifications"] == [
        "mathematical_blocked",
        "branch_execution_pending",
        "formalization_blocked",
    ]
    assert report["candidate_edit_blocked"]["applicable"] is False


def test_latex_sqrt_preserves_real_domain_requirement(tmp_path: Path) -> None:
    tex = tmp_path / "sqrt.tex"
    _write_equations(tex, [("eq:sqrt", r"\sqrt{x}^{2} = x")])

    result = audit_document_derivation_tree(tex, focus_labels=["eq:sqrt"], max_attempts=2)
    report = _single_report(result)

    assert any(
        "square-root argument is nonnegative" in item["text"]
        for item in report["missing_or_unresolved_assumptions"]
    )
    assert "mathematical_blocked" in report["failure_classifications"]
    assert result["coverage"]["promoted_count"] == 0


def test_sibling_root_attempts_remain_outside_each_child_branch(tmp_path: Path) -> None:
    tex = tmp_path / "collisions.tex"
    _write_equations(tex, [("eq:left", "x + 1 = 1 + x"), ("eq:right", "y + 1 = 1 + y")])

    result = audit_document_derivation_tree(
        tex,
        focus_labels=["eq:left", "eq:right"],
        max_attempts=2,
    )
    attempt_ids = []
    for target in result["targets"]:
        branch = target["tree"]["assumption_branches"][0]
        root_attempt = target["tree"]["backend_attempts"][0]
        attempt_ids.append(root_attempt["id"])
        assert root_attempt["document_evidence_binding"] == "legacy_unbound"
        assert root_attempt["applicable_to_document_branch"] is False
        assert branch["backend_attempts"] == []
        assert branch["backend_evidence"]["binding_status"] == "no_branch_evidence"
        assert branch["backend_evidence"]["effective_document_promotion"]["can_promote"] is False
        assert target["tree"]["document_partial_evidence_reports"] == []
        gap = target["tree"]["document_gap_reports"][0]
        assert gap["target_label"] == target["label"]
        assert gap["backend_evidence"]["binding_status"] == "no_branch_evidence"
    assert attempt_ids == ["sympy_algebra_attempt", "sympy_algebra_attempt"]
    assert result["coverage"]["raw_promoted_count"] == 2
    assert result["coverage"]["promoted_count"] == 0
    _assert_document_quarantine({key: value for key, value in result.items() if key != "markdown"})


def test_edit_target_mismatch_cannot_bypass_compiler_quarantine() -> None:
    matching = {
        "id": "legacy_ready_shaped_match",
        "target_label": "eq:right",
        "location": "synthetic.tex > eq:right",
        "context_branch_id": "branch_right",
        "closure_status": "closed_by_exact_manifest",
        "proposed_edit": {
            "target_label": "eq:right",
            "latex": "y + 1 = 1 + y",
        },
        "problem": "Synthetic ready-shaped proposal",
        "why": "Exercise exact edit-target validation independently of publication mode.",
        "backend_evidence": {
            "promotion": {"can_promote": True, "evidence_refs": ["legacy_collision_ref"]}
        },
        "promotion_decision": None,
        "evidence_refs": ["legacy_collision_ref"],
        "remaining_blockers_before_certification": [],
        "metadata": {"contract": "context_aware_executable_repair_proposal"},
    }
    mismatched = {
        **matching,
        "id": "legacy_ready_shaped_mismatch",
        "proposed_edit": {**matching["proposed_edit"], "target_label": "eq:left"},
    }

    matching_errors = document_tree._validate_ready_proposal(matching)
    mismatched_errors = document_tree._validate_ready_proposal(mismatched)
    matching_compiled = document_tree._compiled_item(
        matching,
        item_type="repair_proposal",
        publishable=True,
        validation_errors=matching_errors,
    )
    mismatched_compiled = document_tree._compiled_item(
        mismatched,
        item_type="repair_proposal",
        publishable=True,
        validation_errors=mismatched_errors,
    )

    assert matching_compiled["publication_mode"] == mismatched_compiled["publication_mode"] == "disabled"
    assert matching_compiled["publishable_as_repair"] is mismatched_compiled["publishable_as_repair"] is False
    assert "proposed_edit" not in matching_compiled and "proposed_edit" not in mismatched_compiled
    assert matching_compiled["target_label"] == mismatched_compiled["target_label"] == "eq:right"
    assert document_tree.DOCUMENT_PUBLICATION_VETO_ID in matching_compiled["veto_ids"]
    assert document_tree.DOCUMENT_PUBLICATION_VETO_ID in mismatched_compiled["veto_ids"]
    assert document_tree.EDIT_TARGET_MISMATCH_VETO_ID not in matching_compiled["veto_ids"]
    assert document_tree.EDIT_TARGET_MISMATCH_VETO_ID in mismatched_compiled["veto_ids"]
    assert "evidence_binding_error" not in matching_compiled["failure_classifications"]
    assert mismatched_compiled["failure_classification"] == "evidence_binding_error"
    assert "evidence_binding_error" in mismatched_compiled["failure_classifications"]
    assert not any(document_tree.EDIT_TARGET_MISMATCH_VETO_ID in error for error in matching_errors)
    assert any(document_tree.EDIT_TARGET_MISMATCH_VETO_ID in error for error in mismatched_errors)
    assert any("verified Phase 06 promotion decision" in error for error in matching_errors)
    assert not any("can_promote" in error for error in matching_errors)


def test_p02_extraction_paths_remain_quarantined_without_backend_calls() -> None:
    tex = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex"

    result = document_tree.extract_document_derivation_obligations(
        tex,
        focus_labels=["eq:incremental-cash-flow", "eq:incremental-npv"],
    )

    assert result["backend_request_count"] == 0
    assert result["publication_mode"] == "disabled"
    assert result["publication_enabled"] is False
    assert result["claim_eligibility"] == "ineligible"
    assert [item["label"] for item in result["obligations"]] == [
        "eq:incremental-cash-flow",
        "eq:incremental-npv",
    ]
    assert all(item["adapter_eligible"] is True for item in result["obligations"])


def test_adapter_exception_is_engineering_error_not_only_math_gap(
    tmp_path: Path, monkeypatch
) -> None:
    tex = tmp_path / "adapter.tex"
    _write_equations(tex, [("eq:adapter", "x + 1 = 1 + x")])

    def fail_adapter(*args, **kwargs):
        raise RuntimeError("synthetic adapter failure")

    monkeypatch.setattr("mathdevmcp.external_tool_adapters.derive_or_refute", fail_adapter)
    result = audit_document_derivation_tree(tex, focus_labels=["eq:adapter"], max_attempts=1)
    target = result["targets"][0]

    assert target["tree"]["backend_attempts"][0]["status"] == "adapter_error"
    assert "engineering_error" in target["failure_classifications"]
    assert result["coverage"]["failure_classification_counts"]["engineering_error"] == 1
    assert "engineering_error" in result["markdown"]
    assert target["promotion"]["can_promote"] is False


def test_serial_and_parallel_worker_exceptions_are_engineering_errors(
    tmp_path: Path, monkeypatch
) -> None:
    tex = tmp_path / "workers.tex"
    _write_equations(tex, [("eq:one", "x + 1 = 1 + x"), ("eq:two", "y + 1 = 1 + y")])

    def fail_worker(*args, **kwargs):
        raise RuntimeError("synthetic worker failure")

    monkeypatch.setattr(document_tree, "_target_result_for_row", fail_worker)
    for workers in (1, 2):
        result = audit_document_derivation_tree(
            tex,
            focus_labels=["eq:one", "eq:two"],
            max_attempts=1,
            workers=workers,
        )
        assert result["execution"]["failure_count"] == 2
        assert all(target["failure_classification"] == "engineering_error" for target in result["targets"])
        assert all(target["tree"]["controller"]["promotion"]["can_promote"] is False for target in result["targets"])
        assert all(target["tree"]["tool_grounded_proposal_compiler"]["repair_proposal_count"] == 0 for target in result["targets"])
        assert all(target["tree"]["blockers"][0]["failure_classification"] == "engineering_error" for target in result["targets"])
        assert "engineering_error" in result["markdown"]


def test_library_facade_server_and_cli_have_quarantine_parity(tmp_path: Path) -> None:
    tex = tmp_path / "surface.tex"
    _write_equations(tex, [("eq:surface", "x + 1 = 1 + x")])
    arguments = {"tex_path": str(tex), "focus_labels": ["eq:surface"], "max_attempts": 2}

    library = audit_document_derivation_tree(tex, focus_labels=["eq:surface"], max_attempts=2)
    facade = call_mcp_tool("audit_document_derivation_tree", arguments)
    server = server_audit_document_derivation_tree(str(tex), focus_labels=["eq:surface"], max_attempts=2)
    assert server.structuredContent is not None
    server_payload = server.structuredContent
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-document-derivation-tree",
            str(tex),
            "--focus-label",
            "eq:surface",
            "--max-attempts",
            "2",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
    )
    assert completed.returncode == 0, completed.stderr
    cli = json.loads(completed.stdout)

    for payload in (library, facade, server_payload, cli):
        assert payload["publication_mode"] == "disabled"
        assert payload["coverage"]["promoted_count"] == 0
        assert payload["coverage"]["document_ready_repair_proposal_count"] == 0
        _assert_document_quarantine({key: value for key, value in payload.items() if key != "markdown"})


def test_emergency_kill_switch_returns_before_source_access_on_all_surfaces(
    tmp_path: Path, monkeypatch
) -> None:
    missing = tmp_path / "does-not-exist.tex"
    monkeypatch.setenv("MATHDEVMCP_DISABLE_DOCUMENT_DERIVATION_TREE", "1")

    library = audit_document_derivation_tree(missing)
    facade = call_mcp_tool(
        "audit_document_derivation_tree",
        {"tex_path": str(missing), "response_mode": "detailed"},
    )
    server = server_audit_document_derivation_tree(str(missing), response_mode="detailed")
    assert server.structuredContent is not None
    server_payload = server.structuredContent
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-document-derivation-tree",
            str(missing),
            "--response-mode",
            "detailed",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src"), "MATHDEVMCP_DISABLE_DOCUMENT_DERIVATION_TREE": "1"},
    )
    assert completed.returncode == 0, completed.stderr
    cli = json.loads(completed.stdout)

    for payload in (library, facade, server_payload, cli):
        assert payload["status"] == "document_derivation_tree_disabled_pending_publication_safety"
        assert payload["failure_classification"] == "engineering_error"
        assert payload["execution"]["pipeline_entered"] is False
        assert payload["targets"] == []
        assert payload["tool_uses"] == []
        assert payload["coverage"]["promoted_count"] == 0


def test_emergency_kill_switch_default_compact_is_semantically_identical_across_cli_mcp(
    tmp_path: Path, monkeypatch
) -> None:
    missing = tmp_path / "does-not-exist.tex"
    monkeypatch.setenv("MATHDEVMCP_DISABLE_DOCUMENT_DERIVATION_TREE", "1")

    facade = call_mcp_tool("audit_document_derivation_tree", {"tex_path": str(missing)})
    server = server_audit_document_derivation_tree(str(missing))
    assert server.structuredContent is not None
    server_payload = server.structuredContent
    completed = subprocess.run(
        [sys.executable, "-m", "mathdevmcp.cli", "audit-document-derivation-tree", str(missing)],
        check=False,
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "PYTHONPATH": str(ROOT / "src"),
            "MATHDEVMCP_DISABLE_DOCUMENT_DERIVATION_TREE": "1",
        },
    )
    assert completed.returncode == 0, completed.stderr
    cli = json.loads(completed.stdout)
    facade_without_ok = {key: value for key, value in facade.items() if key != "ok"}
    server_without_ok = {
        key: value for key, value in server_payload.items() if key != "ok"
    }

    assert facade_without_ok == server_without_ok == cli
    assert cli["response_mode"] == "compact"
    assert cli["metadata"]["contract"] == "document_derivation_response"
    assert cli["status"] == "document_derivation_tree_disabled_pending_publication_safety"
    assert cli["publication_mode"] == "disabled"
    assert cli["targets"] == []


def test_lower_level_controller_contract_remains_raw_and_unchanged() -> None:
    def algebra(target, *, lhs=None, rhs=None, backend="auto"):
        return {
            "status": "proved",
            "reason": "Synthetic scoped algebra result.",
            "metadata": {"schema_version": "1.0", "contract": "derive_or_refute_result"},
        }

    tree = can_derive_with_budget(
        "a + b = b + a",
        max_attempts=1,
        capabilities={"sympy": {"available": True}, "sage": {"available": False}, "lean": {"available": False}},
        integrations={},
        algebra_runner=algebra,
    )

    assert tree["status"] == "proved"
    assert tree["controller"]["promotion"]["can_promote"] is True


def test_phase01_document_surfaces_remain_ineligible_and_publication_false(tmp_path: Path) -> None:
    tex = tmp_path / "phase01-surface.tex"
    _write_equations(tex, [("eq:phase01", "x + 1 = 1 + x")])

    result = audit_document_derivation_tree(tex, focus_labels=["eq:phase01"], max_attempts=2)
    target = result["targets"][0]
    tree = target["tree"]
    branch = tree["assumption_branches"][0]
    report = tree["document_gap_reports"][0]
    compiler = tree["tool_grounded_proposal_compiler"]
    compiled = compiler["compiled_items"][0]
    surfaces = [
        result,
        target,
        tree,
        tree["backend_attempts"][0],
        branch["backend_evidence"],
        report,
        report["backend_evidence"],
        compiler,
        compiled,
    ]

    for surface in surfaces:
        assert surface["evidence_schema_version"] == "0-legacy"
        assert surface["integrity_binding_status"] == "unbound_legacy_evidence"
        assert surface["integrity_binding_verified"] is False
        assert surface["claim_eligibility"] == "ineligible"
        assert surface["publication_enabled"] is False

    for path, key, value in _walk(result):
        if key == "claim_eligibility":
            assert value == "ineligible", _normalized_path(path)
        if key == "publication_enabled":
            assert value is False, _normalized_path(path)
        assert value != "exact_manifest_eligible", _normalized_path(path)

    assert branch["backend_attempts"] == []
    assert branch["backend_evidence"]["raw_promotion"]["can_promote"] is False
    assert result["coverage"]["promoted_count"] == 0
    assert result["publication_mode"] == "disabled"
