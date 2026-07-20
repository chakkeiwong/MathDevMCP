from pathlib import Path

from mathdevmcp.derive_from import derive_from
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from tests.test_context_and_fixtures import EXPECTED_BENCHMARK_SUMMARY, EXPECTED_BENCHMARK_TOTAL


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"
ROOT = FIXTURES.parent.parent


def test_list_mcp_tools_includes_implementation_brief():
    tools = {tool["name"]: tool for tool in list_mcp_tools()}
    names = set(tools)

    assert "implementation_brief" in names
    assert "latex_label_lookup" in names
    assert "check_equality" in names
    assert "lean_check" in names
    assert "audit_implementation_label" in names
    assert "compare_label_code" in names
    assert "benchmark_gate" in names
    assert "workbench_benchmark_quality" in names
    assert "audit_kalman_recursion" in names
    assert "typed_obligation_label" in names
    assert "release_corpus_manifest" in names
    assert "validate_release_corpus" in names
    assert "governance_policy" in names
    assert "release_readiness" in names
    assert "derive_from" in names
    assert "prove_or_counterexample" in names
    assert "assumptions_for" in names
    assert "audit_and_propose_assumptions" in names
    assert "audit_and_propose_derivations" in names
    assert "debug_derivation" in names
    assert "audit_math_to_code" in names
    assert "audit_report_claim_boundary" in names
    assert "prepare_review_packet" in names
    assert "high_level_workflow_quality" in names
    assert "external_tool_first_plan" in names
    assert "domain_templates" in names
    assert "suggest_domain_templates" in names
    assert "generate_template_obligations" in names
    assert "claim_support_packet" in names
    assert "proof_packet_label" in names
    assert "negative_evidence_label" in names
    assert "capability_registry" in names
    assert tools["compare_label_code"]["deprecated"] is True
    assert tools["compare_label_code"]["replacement"] == "audit_implementation_label"
    assert tools["check_proof_obligation"]["deprecated"] is True
    assert tools["check_proof_obligation"]["replacement"] == "check_equality"
    compare_doc_code = tools["compare_doc_code"]
    assert "filesystem paths" in compare_doc_code["description"]
    assert "not raw text" in compare_doc_code["description"]
    assert "document text against code text" not in compare_doc_code["description"]
    assert tools["derive_from"]["output_contract"] == "high_level_workflow_result"
    assert tools["derive_from"]["certifying_capable"] is True
    assert tools["audit_and_propose_assumptions"]["output_contract"] == "audit_assumption_report_result"
    assert tools["audit_and_propose_derivations"]["output_contract"] == "derivation_audit_report_result"
    assert tools["audit_math_to_code"]["certifying_capable"] is False
    assert tools["audit_report_claim_boundary"]["output_contract"] == "report_claim_boundary_audit"
    assert tools["external_tool_first_plan"]["output_contract"] == "external_tool_first_plan_result"
    assert tools["prepare_review_packet"]["certifying_capable"] is False


def test_agent_capability_registry_exposes_resolver_vocabulary_and_operator_boundary() -> None:
    result = call_mcp_tool("capability_registry", {})

    assert result["ok"] is True
    assert "label_scoped_obligation" in result["resolver_catalog"]["target_collections"]
    assert "global_evidence_ref_records" in result["resolver_catalog"]["global_collections"]
    assert {item["capability"] for item in result["intentional_cli_only"]} >= {
        "parser_benchmarks",
        "release_validation",
    }


def test_agent_domain_template_tools_are_available_through_facade() -> None:
    catalog = call_mcp_tool("domain_templates", {})
    suggestions = call_mcp_tool(
        "suggest_domain_templates",
        {"label": "eq:terminal-value-base", "equation_text": "terminal value attrition discount rate"},
    )
    obligations = call_mcp_tool(
        "generate_template_obligations",
        {"template_id": "valuation_terminal_value_v1", "label": "eq:terminal-value-base"},
    )

    assert catalog["metadata"]["contract"] == "domain_template_catalog"
    assert suggestions["matches"][0]["id"] == "valuation_terminal_value_v1"
    assert obligations["status"] == "unverified"


def test_call_mcp_tool_high_level_derive_from_preserves_library_contract():
    library_result = derive_from("a + b = b + a", givens=["a,b are scalars"])
    mcp_result = call_mcp_tool(
        "derive_from",
        {"target": "a + b = b + a", "givens": ["a,b are scalars"]},
    )

    assert mcp_result["ok"] is True
    assert {key: value for key, value in mcp_result.items() if key != "ok"} == library_result
    assert mcp_result["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_result"}
    assert "givens_not_formal_assumptions" in {item["code"] for item in mcp_result["non_claims"]}


def test_call_mcp_tool_high_level_surfaces_preserve_boundaries():
    proof = call_mcp_tool("prove_or_counterexample", {"claim": "A*B = B*A"})
    assumptions = call_mcp_tool("assumptions_for", {"target": "logdet(A)"})
    assumption_report = call_mcp_tool(
        "audit_and_propose_assumptions",
        {"question": "Audit assumptions", "target": "logdet(A)"},
    )
    derivation_report = call_mcp_tool(
        "audit_and_propose_derivations",
        {"question": "Audit derivations", "target": "logdet(A) = trace(A)"},
    )
    debug = call_mcp_tool("debug_derivation", {"steps": ["logdet(A)", "trace(A)", "trace(A)"]})
    code = call_mcp_tool("audit_math_to_code", {"math": "logdet(S)", "code": "def f(S):\n    return logdet(S)\n"})
    packet = call_mcp_tool("prepare_review_packet", {"question": "Review", "evidence": [proof]})
    boundary = call_mcp_tool(
        "audit_report_claim_boundary",
        {
            "claim": "The report passed review and is not a proof.",
            "evidence_snippets": ["Review result: passed."],
        },
    )

    assert proof["metadata"]["contract"] == "high_level_workflow_result"
    assert proof["status"] == "refuted"
    assert proof["counterexamples"]
    assert assumptions["status"] == "missing_assumptions"
    assert "route_assumptions_not_global_minimality" in {item["code"] for item in assumptions["non_claims"]}
    assert assumption_report["metadata"]["contract"] == "audit_assumption_report_result"
    assert assumption_report["proposals"][0]["validation"]["status"] == "validated_by_rule"
    assert derivation_report["metadata"]["contract"] == "derivation_audit_report_result"
    assert derivation_report["proposals"][0]["validation"]["status"] == "blocked_by_missing_assumptions"
    assert derivation_report["tool_uses"][0]["tool"] == "plan_backend_routes"
    assert derivation_report["route_plans"][0]["metadata"]["contract"] == "backend_route_plan_result"
    assert debug["status"] == "gap_found"
    assert "gap_localization_not_global_failure" in {item["code"] for item in debug["non_claims"]}
    assert code["status"] == "structural_match"
    assert code["certification_source"] == "none"
    assert "structural_evidence_not_proof" in {item["code"] for item in code["non_claims"]}
    assert packet["status"] == "diagnostic_only"
    assert packet["certification_source"] == "none"
    assert "diagnostic_evidence_not_proof" in {item["code"] for item in packet["non_claims"]}
    assert boundary["metadata"]["contract"] == "report_claim_boundary_audit"
    assert boundary["mathematical_claim"] is False
    assert boundary["document_evidence_needed"]


def test_mcp_facade_search_latex_respects_file_filter(tmp_path):
    (tmp_path / "d446.tex").write_text(r"\section{Shared phrase old}", encoding="utf-8")
    (tmp_path / "d447.tex").write_text(r"\section{Shared phrase current}", encoding="utf-8")

    result = call_mcp_tool("search_latex", {"root": str(tmp_path), "query": "shared phrase", "file": "d447.tex"})

    assert result
    assert {item["file"] for item in result} == {"d447.tex"}


def test_mcp_facade_latex_label_lookup_respects_file_filter(tmp_path):
    (tmp_path / "old.tex").write_text(r"\begin{equation}\label{eq:shared} old = 1 \end{equation}", encoding="utf-8")
    (tmp_path / "final.tex").write_text(r"\begin{equation}\label{eq:shared} final = 2 \end{equation}", encoding="utf-8")

    result = call_mcp_tool("latex_label_lookup", {"root": str(tmp_path), "label": "eq:shared", "file": "final.tex"})

    assert result["ok"] is True
    assert result["file"] == "final.tex"
    assert any("final = 2" in paragraph["text"] for paragraph in result["paragraphs"])


def test_call_mcp_tool_derivation_report_preserves_extracted_targets() -> None:
    result = call_mcp_tool(
        "audit_and_propose_derivations",
        {
            "question": "Audit extracted risky-debt target",
            "root": str(ROOT / "docs"),
            "labels": ["prop:risky-pricing"],
        },
    )

    assert result["metadata"]["contract"] == "derivation_audit_report_result"
    assert result["coverage"]["extracted_target_count"] == 1
    assert result["coverage"]["fallback_target_count"] == 0
    assert result["target_extraction"]["label_results"][0]["targets"][0]["label"] == "eq:risky-pricing"
    assert result["route_plans"][0]["source"]["label"] == "eq:risky-pricing"
    assert result["route_plans"][0]["metadata"]["contract"] == "backend_route_plan_result"
    assert "Route planning is diagnostic only" in result["route_plans"][0]["boundary"]


def test_call_mcp_tool_report_selectors_reach_high_level_workflows(tmp_path) -> None:
    import hashlib

    source = tmp_path / "current.tex"
    source.write_text(r"\begin{equation}\label{eq:shared} x = 2 \end{equation}", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()

    assumptions = call_mcp_tool(
        "audit_and_propose_assumptions",
        {
            "question": "Audit exact",
            "root": str(tmp_path),
            "labels": ["eq:shared"],
            "file": source.name,
            "source_digest": digest,
        },
    )
    derivations = call_mcp_tool(
        "audit_and_propose_derivations",
        {
            "question": "Audit exact",
            "root": str(tmp_path),
            "labels": ["eq:shared"],
            "file": source.name,
            "source_digest": digest,
        },
    )

    assert assumptions["coverage"]["label_selection"][0]["selection_status"] == "selected"
    assert derivations["coverage"]["label_selection"][0]["selection_status"] == "selected"


def test_call_mcp_tool_prepare_review_packet_preserves_phase6_packet_fields():
    derived = call_mcp_tool(
        "derive_from",
        {"target": "a + b = b + a", "givens": ["a,b are scalars"]},
    )
    code = call_mcp_tool(
        "audit_math_to_code",
        {
            "math": "logdet(Sigma) + trace(Cov)",
            "code": "def f(S):\n    return logdet(S) + trace(S)\n",
            "aliases": {"Sigma": "S", "Cov": "S"},
        },
    )
    packet = call_mcp_tool(
        "prepare_review_packet",
        {
            "question": "Review derivation and implementation context",
            "evidence": [derived, code],
            "source": {"context_summary": "MCP surface preservation fixture."},
        },
    )
    low_level = packet["evidence"][0]["low_level"]
    non_claim_codes = {item["code"] for item in low_level["non_claims"]}

    assert packet["ok"] is True
    assert packet["status"] == "diagnostic_only"
    assert packet["certification_source"] == "none"
    assert low_level["backend_checks"]
    assert low_level["nested_evidence_summary"]
    assert low_level["route_plans"]
    assert low_level["trace_maps"]
    assert low_level["residual_gaps"]
    assert low_level["decision_criteria"]
    assert low_level["risk_register"]
    assert low_level["agent_handoff"]["scoped_question"] == "Review derivation and implementation context"
    assert low_level["agent_handoff"]["evidence_ledger"]
    assert low_level["agent_handoff"]["veto_risks"]
    assert packet["agent_handoff"] == low_level["agent_handoff"]
    assert "diagnostic_route_and_trace_context_not_proof" in non_claim_codes
    assert "not recertified" in low_level["backend_checks"][0]["boundary"]
    assert "not semantic proof" in low_level["trace_maps"][0]["boundary"]


def test_call_mcp_tool_prepare_review_packet_can_return_compact_handoff():
    derived = call_mcp_tool(
        "derive_from",
        {"target": "a + b = b + a", "givens": ["a,b are scalars"]},
    )
    handoff = call_mcp_tool(
        "prepare_review_packet",
        {
            "question": "Review compact MCP handoff",
            "evidence": [derived],
            "handoff": True,
        },
    )

    assert handoff["scoped_question"] == "Review compact MCP handoff"
    assert {
        "status",
        "reason",
        "evidence_ledger",
        "assumption_gap_ledger",
        "veto_risks",
        "non_claim_boundary",
        "next_actions",
        "next_artifact",
        "certification_boundary",
    }.issubset(handoff)
    assert handoff["evidence_ledger"]
    assert handoff["non_claim_boundary"]
    assert "not a proof certificate" in handoff["certification_boundary"]
    assert "metadata" not in handoff
    assert "workflow" not in handoff


def test_call_mcp_tool_end_to_end_review_handoff_preserves_evidence_risks_and_boundaries():
    derived = call_mcp_tool(
        "derive_from",
        {"target": "a + b = b + a", "givens": ["a,b are scalars"]},
    )
    code = call_mcp_tool(
        "audit_math_to_code",
        {
            "math": "logdet(Sigma) + trace(Cov)",
            "code": "def f(S):\n    return logdet(S) + trace(S)\n",
            "aliases": {"Sigma": "S", "Cov": "S"},
        },
    )

    full_packet = call_mcp_tool(
        "prepare_review_packet",
        {
            "question": "Review transport derivation and code handoff",
            "evidence": [derived, code],
            "source": {
                "context_summary": "End-to-end fixture: backend derivation evidence plus structural code audit."
            },
        },
    )
    compact = call_mcp_tool(
        "prepare_review_packet",
        {
            "question": "Review transport derivation and code handoff",
            "evidence": [derived, code],
            "source": {
                "context_summary": "End-to-end fixture: backend derivation evidence plus structural code audit."
            },
            "handoff": True,
        },
    )

    low_level = full_packet["evidence"][0]["low_level"]
    compact_without_wrapper = {key: value for key, value in compact.items() if key != "ok"}
    risk_codes = {item["code"] for item in compact["veto_risks"]}
    non_claim_codes = {item["code"] for item in compact["non_claim_boundary"]}

    assert full_packet["status"] == "diagnostic_only"
    assert full_packet["certification_source"] == "none"
    assert compact["ok"] is True
    assert compact_without_wrapper == full_packet["agent_handoff"]
    assert compact["scoped_question"] == "Review transport derivation and code handoff"
    assert compact["source_context"] == "End-to-end fixture: backend derivation evidence plus structural code audit."
    assert compact["evidence_ledger"]
    assert compact["assumption_gap_ledger"]
    assert {"route_plans_are_diagnostic", "trace_maps_are_structural"}.issubset(risk_codes)
    assert "review_packet_not_proof_certificate" in non_claim_codes
    assert "not a proof certificate" in compact["certification_boundary"]
    assert compact["next_actions"]
    assert low_level["route_plans"]
    assert low_level["trace_maps"]
    assert low_level["backend_checks"]


def test_call_mcp_tool_high_level_workflow_quality_returns_threshold_report():
    result = call_mcp_tool("high_level_workflow_quality", {"root": str(ROOT)})

    assert result["metadata"] == {"schema_version": "1.0", "contract": "high_level_workflow_quality_report"}
    assert result["status"] == "quality_thresholds_passed"
    assert result["total_cases"] == 14
    assert result["workflow_count"] == 6
    assert all(result["seeded_gate_thresholds"].values())
    assert all(result["mutation_results"].values())



def test_call_mcp_tool_compare_label_code_returns_traceable_result():
    result = call_mcp_tool(
        "compare_label_code",
        {
            "root": str(FIXTURES),
            "label": "prop:transport-mismatch",
            "code": str(FIXTURES / "doc_consistency_bad.py"),
            "required_terms": ["logdet"],
        },
    )

    assert result["status"] == "mismatch"
    assert result["doc_context"]["file"] == "doc_consistency_bad.tex"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "label_consistency_result"}
    assert result["provenance"]["label"] == "prop:transport-mismatch"
    assert result["ok"] is True


def test_call_mcp_tool_audit_implementation_label_returns_rich_audit_while_alias_stays_legacy():
    args = {
        "root": str(FIXTURES),
        "label": "prop:transport-mismatch",
        "code": str(FIXTURES / "doc_consistency_bad.py"),
        "required_terms": ["logdet"],
    }

    preferred = call_mcp_tool("audit_implementation_label", args)
    legacy = call_mcp_tool("compare_label_code", args)

    assert preferred["metadata"] == {"schema_version": "1.0", "contract": "implementation_audit_result"}
    assert legacy["metadata"] == {"schema_version": "1.0", "contract": "label_consistency_result"}
    assert preferred["status"] == "mismatch"
    assert legacy["status"] == "mismatch"


def test_call_mcp_tool_preferred_label_and_equality_names_work():
    context = call_mcp_tool("latex_label_lookup", {"root": str(FIXTURES), "label": "prop:transport-logdet"})
    equality = call_mcp_tool("check_equality", {"lhs": "(a+b)*(a-b)", "rhs": "a*a - b*b"})

    assert context["metadata"] == {"schema_version": "1.0", "contract": "latex_paragraph_context"}
    assert context["label"] == "prop:transport-logdet"
    assert equality["metadata"] == {"schema_version": "1.0", "contract": "proof_obligation_result"}
    assert equality["status"] in {"equivalent", "verified", "inconclusive"}


def test_call_mcp_tool_implementation_brief_returns_consistent_result():
    result = call_mcp_tool(
        "implementation_brief",
        {
            "root": str(FIXTURES),
            "query": "transport log-determinant identity",
            "code": str(FIXTURES / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
        },
    )

    assert result["status"] == "consistent"
    assert result["selected_label"] == "prop:transport-logdet"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "implementation_brief"}
    assert result["partial_certification_summary"]["overall_status"] == "diagnostic_only"
    assert result["ok"] is True


def test_call_mcp_tool_implementation_brief_reuses_cache(tmp_path):
    cache = tmp_path / "mcp_workflow_cache.json"

    cold = call_mcp_tool(
        "implementation_brief",
        {
            "root": str(FIXTURES),
            "query": "transport log-determinant identity",
            "code": str(FIXTURES / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "cache": str(cache),
        },
    )
    warm = call_mcp_tool(
        "implementation_brief",
        {
            "root": str(FIXTURES),
            "query": "transport log-determinant identity",
            "code": str(FIXTURES / "doc_consistency_good.py"),
            "required_terms": ["logdet"],
            "cache": str(cache),
        },
    )

    assert cold["cache"] == {"path": str(cache), "hit": False}
    assert warm["cache"] == {"path": str(cache), "hit": True}
    assert warm["status"] == "consistent"


def test_call_mcp_tool_implementation_brief_reports_partial_certification():
    result = call_mcp_tool(
        "implementation_brief",
        {
            "root": str(FIXTURES),
            "query": "transport identity",
            "label": "prop:transport-mismatch",
            "code": str(FIXTURES / "doc_consistency_bad.py"),
            "required_terms": ["logdet"],
            "lhs": "log_pi + logdet",
            "rhs": "log_pi + logdet",
        },
    )

    summary = result["partial_certification_summary"]
    assert result["status"] == "mismatch"
    assert summary["overall_status"] == "partial_certification"
    assert summary["certified"] == ["scoped derivation equality"]
    assert "full LaTeX/code contract" in summary["not_certified"]
    assert "label search" in summary["diagnostic_only"]
    assert summary["recommended_next_tool"] == "audit_temporal_contract"


def test_call_mcp_tool_audit_kalman_recursion_returns_ast_evidence():
    result = call_mcp_tool(
        "audit_kalman_recursion",
        {"code": str(FIXTURES / "doc_kalman_recursion_bad.py")},
    )

    assert result["status"] == "mismatch"
    assert result["missing_operations"] == ["covariance_update"]
    assert result["ast_operation_graph"]["metadata"] == {"schema_version": "1.0", "contract": "ast_operation_graph"}
    assert result["ok"] is True


def test_call_mcp_tool_typed_obligation_label_returns_dimension_diagnostics():
    result = call_mcp_tool(
        "typed_obligation_label",
        {"root": str(FIXTURES), "label": "eq:dept-state-space-likelihood"},
    )

    assert result["status"] == "unverified"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "typed_obligation_label_diagnostic"}
    assert result["typed_diagnostic"]["metadata"] == {"schema_version": "1.0", "contract": "typed_math_obligation_diagnostic"}
    assert result["ok"] is True



def test_call_mcp_tool_run_benchmarks_aggregates_results():
    result = call_mcp_tool("run_benchmarks", {"root": str(ROOT)})

    assert result["total"] == EXPECTED_BENCHMARK_TOTAL
    assert result["passed"] == EXPECTED_BENCHMARK_TOTAL
    assert result["metadata"] == {"schema_version": "1.0", "contract": "benchmark_results"}
    assert all("details" in item for item in result["results"])
    assert result["summary"] == EXPECTED_BENCHMARK_SUMMARY
    assert result["workbench_quality"]["status"] == "quality_thresholds_passed"
    assert result["ok"] is True



def test_call_mcp_tool_benchmark_gate_returns_ci_shape():
    result = call_mcp_tool("benchmark_gate", {"root": str(ROOT)})

    assert result == {
        "ok": True,
        "passed": True,
        "total": EXPECTED_BENCHMARK_TOTAL,
        "passed_count": EXPECTED_BENCHMARK_TOTAL,
        "failed_count": 0,
        "summary": EXPECTED_BENCHMARK_SUMMARY,
        "policy": {
            "name": "all_benchmarks_must_pass",
            "required_pass_rate": 1.0,
            "allow_category_failures": {},
            "description": "Every benchmark case must pass; no category-specific failure budget is currently allowed.",
        },
        "metadata": {"schema_version": "1.0", "contract": "benchmark_gate"},
    }


def test_call_mcp_tool_workbench_benchmark_quality_returns_threshold_report():
    result = call_mcp_tool("workbench_benchmark_quality", {"root": str(ROOT)})

    assert result["metadata"] == {"schema_version": "1.0", "contract": "workbench_benchmark_quality_report"}
    assert result["status"] == "quality_thresholds_passed"
    assert result["total_cases"] == 15
    assert all(result["seeded_gate_thresholds"].values())
    assert all(result["mutation_results"].values())


def test_call_mcp_tool_release_surfaces_return_contracts():
    corpus = call_mcp_tool("validate_release_corpus", {"root": str(FIXTURES)})
    governance = call_mcp_tool("governance_policy", {})
    release = call_mcp_tool("release_readiness", {"root": str(ROOT)})

    assert corpus["metadata"] == {"schema_version": "1.0", "contract": "release_corpus_validation_report"}
    assert corpus["status"] == "consistent"
    assert governance["metadata"] == {"schema_version": "1.0", "contract": "governance_policy"}
    assert release["metadata"] == {"schema_version": "1.0", "contract": "release_readiness_report"}
    assert release["benchmark_gate"]["passed"] is True
    assert release["ok"] is True



def test_call_mcp_tool_returns_structured_error_for_unknown_tool():
    result = call_mcp_tool("missing_tool", {})

    assert result == {
        "ok": False,
        "error": {"type": "unknown_tool", "message": "Unknown MathDevMCP tool: missing_tool"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }



def test_call_mcp_tool_returns_structured_error_for_invalid_arguments():
    result = call_mcp_tool("compare_label_code", {"root": str(FIXTURES), "label": "prop:transport-mismatch"})

    assert result == {
        "ok": False,
        "error": {"type": "invalid_arguments", "message": "Missing required string argument: code"},
        "metadata": {"schema_version": "1.0", "contract": "error"},
    }


def test_call_mcp_tool_reports_recoverable_missing_label_stage():
    result = call_mcp_tool(
        "compare_label_code",
        {
            "root": str(FIXTURES),
            "label": "sec:missing-label",
            "code": str(FIXTURES / "doc_consistency_good.py"),
        },
    )

    assert result["ok"] is False
    assert result["error"] == {"type": "tool_execution_error", "message": "MathDevMCP tool failed during execution: compare_label_code"}
    assert result["diagnostics"]["stage"] == "retrieve_label"
    assert result["diagnostics"]["exception_type"] == "KeyError"
    assert result["diagnostics"]["recoverable"] is True
    assert "search_latex" in result["diagnostics"]["suggested_action"]
    assert result["diagnostics"]["input_summary"]["code"]["looks_like_path"] is True


def test_call_mcp_tool_reports_recoverable_missing_code_stage():
    result = call_mcp_tool(
        "audit_implementation_label",
        {
            "root": str(FIXTURES),
            "label": "prop:transport-logdet",
            "code": str(FIXTURES / "missing_code_file.py"),
        },
    )

    assert result["ok"] is False
    assert result["error"]["type"] == "tool_execution_error"
    assert result["diagnostics"]["stage"] == "read_code"
    assert result["diagnostics"]["exception_type"] == "FileNotFoundError"
    assert result["diagnostics"]["input_summary"]["code"]["exists"] is False
