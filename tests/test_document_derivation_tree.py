import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import mathdevmcp.document_derivation_tree as document_tree
from mathdevmcp.document_derivation_tree import (
    audit_document_derivation_tree,
    extract_document_derivation_obligations,
)
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.mcp_server import audit_document_derivation_tree as server_audit_document_derivation_tree


ROOT = Path(__file__).resolve().parent.parent


def _write_fixture(path: Path) -> None:
    path.write_text(
        r"""
\section{Generic valuation}
\begin{equation}
\label{eq:npv}
\Delta \NPV_i(a)
=
\E\left[
  \sum_{h=0}^{H}\delta_h \Delta CF_{i,h}(a)
  \mid \mathcal{I}_{i0}
\right].
\end{equation}

\section{Generic dynamic program}
\begin{align}
\label{eq:bellman}
V_t^{\star}(s)
&=
\max_{a\in\mathcal{A}(s)}
\left\{
r_t(s,a)
+ \delta \E[V_{t+1}^{\star}(s')\mid s,a]
\right\} \\
J_c(s)
&=
\E\left[
  \sum_{h=t}^{H}\delta^{h-t} c_h(s_h,a_h)
  \mid s_t=s
\right].
\end{align}
""",
        encoding="utf-8",
    )


def test_document_derivation_tree_builds_semantic_packets_before_backend_attempts(tmp_path: Path) -> None:
    tex = tmp_path / "generic.tex"
    _write_fixture(tex)

    result = audit_document_derivation_tree(tex, focus_labels=["eq:npv"], max_attempts=1)

    assert result["metadata"]["contract"] == "document_derivation_tree_audit"
    assert result["coverage"]["semantic_packet_count"] == 1
    target = result["targets"][0]
    packet = target["semantic_work_packet"]
    assert "npv_accounting_identity" in packet["semantic_domains"]
    assert "conditional_expectation" in packet["semantic_domains"]
    assert packet["full_display_source"] == packet["source_text"]
    assert packet["display_source_span"]["labels"] == ["eq:npv"]
    assert "conditional_expectation" in packet["operator_inventory"]
    assert "summation" in packet["operator_inventory"]
    assert r"\NPV" in packet["symbol_inventory"]["latex_commands"]
    assert packet["symbol_inventory_compatibility"]["macros"] == packet["symbol_inventory"]["latex_commands"]
    assert packet["lhs_rhs_candidates"][0]["source"] == "row"
    assert packet["lhs_rhs_candidates"][1]["source"] == "full_display"
    assert packet["missing_obligations"]
    assert packet["possible_assumption_sets"]
    assert packet["how_derivation_can_work"]
    branches = target["tree"]["assumption_branches"]
    assert branches
    first_branch = branches[0]
    assert first_branch["closes_obligations"]
    assert first_branch["derivation_route_under_assumptions"]
    assert first_branch["external_tool_first_ledger"]
    assert any(item["tool"] == "sympy" for item in first_branch["external_tool_first_ledger"])
    assert first_branch["backend_attempts"] == []
    assert any(
        blocker["kind"] == "branch_bound_backend_execution_required"
        for blocker in first_branch["blockers"]
    )
    assert first_branch["translation_attempts"]
    assert first_branch["translation_blockers"]
    assert first_branch["backend_evidence"]["translation_blocker_count"] > 0
    assert first_branch["expansion_records"]
    assert target["tree"]["branch_ranking"]["metadata"]["contract"] == "repair_branch_ranking_result"
    assert target["tree"]["branch_ranking"]["top_branch_id"] is None
    assert target["tree"]["branch_ranking"]["nondominated_branch_ids"]
    assert (
        target["tree"]["branch_ranking"]["selected_action"]["action_kind"]
        == "blocked_for_human_or_formalization_choice"
    )
    assert target["tree"]["recursive_expansion"]["status"] == "expanded"
    assert target["tree"]["recursive_expansion"]["expanded_node_count"] > 0
    assert target["tree"]["recursive_expansion"]["budget"]["max_nodes"] == 2
    compiler = target["tree"]["tool_grounded_proposal_compiler"]
    assert compiler["compiled_after_recursive_expansion"] is True
    assert compiler["final_tree_digest"] == target["tree"]["final_tree_digest"]
    assert compiler["expanded_node_ids"]
    assert set(compiler["expanded_node_ids"]) == set(
        target["tree"]["recursive_expansion_ranking"]["ranked_node_ids"]
    )
    assert any(item["status"] == "blocked_before_execution" for item in first_branch["translation_attempts"])
    assert "not a proof certificate" in first_branch["non_claim"]
    assert first_branch["formalization_stubs"]
    assert any(stub["backend"] == "lean" for stub in first_branch["formalization_stubs"])
    assert all("certify" in stub["certification_boundary"] for stub in first_branch["formalization_stubs"])
    assert any(stub["unsupported_constructs"] for stub in first_branch["formalization_stubs"])
    assert target["tree"]["patch_candidates"]
    proposals = target["tree"]["document_ready_repair_proposals"]
    assert proposals == []
    gap_reports = target["tree"]["document_gap_reports"]
    assert gap_reports
    assert gap_reports[0]["metadata"]["contract"] == "document_gap_report"
    assert gap_reports[0]["closure_status"] == "blocked_at_exact_node"
    assert gap_reports[0]["location"].endswith("eq:npv > line 4")
    assert gap_reports[0]["context_branch_id"] in target["tree"]["branch_ranking"]["nondominated_branch_ids"]
    assert gap_reports[0]["context_branch_selection_authority"] == "serialization_only_nondominated_context"
    assert gap_reports[0]["missing_or_unresolved_assumptions"]
    assert gap_reports[0]["proposed_assumptions"]
    assert gap_reports[0]["remaining_blockers_before_certification"]
    assert "blocked_latex" in gap_reports[0]["candidate_edit_blocked"]
    assert "This is a gap report, not a repair proposal." in gap_reports[0]["non_claims"]
    assert target["tree"]["patch_candidates"][0]["location"]["labels"] == ["eq:npv"]
    assert target["tree"]["patch_candidates"][0]["applicable"] is False
    assert "For this displayed equality, assume" in target["tree"]["patch_candidates"][0]["candidate_text_blocked"]
    assert target["tree"]["backend_attempts"]
    assert any(blocker["source"] == "semantic_work_packet" for blocker in target["tree"]["blockers"])
    assert any(blocker["source"] == "document_derivation_tree_formalization_stub" for blocker in target["tree"]["blockers"])
    assert result["coverage"]["promoted_count"] == 0
    assert "Mathematically missing obligations" in result["markdown"]
    assert "Possible sufficient assumption sets" in result["markdown"]
    assert "Candidate assumption branches" in result["markdown"]
    assert "Branch backend attempts" not in result["markdown"]
    assert "Backend attempts" in result["markdown"]
    assert "Translation attempts" in result["markdown"]
    assert "Translation blockers" in result["markdown"]
    assert "Branch ranking" in result["markdown"]
    assert "Document-ready repair proposals" in result["markdown"]
    assert "Document gap reports" in result["markdown"]
    assert "document_gap_report" in result["markdown"]
    assert "Why no proposed edit is emitted" in result["markdown"]
    assert "Expansion records" in result["markdown"]
    assert "Blocked patch candidates (non-applicable)" in result["markdown"]
    assert "Formalization stubs" in result["markdown"]
    assert "How the derivation can work" in result["markdown"]
    assert "Full display target" in result["markdown"]
    assert "document_tree_audit_not_document_proof" in result["markdown"]


def test_document_tree_consumes_label_scoped_obligation_without_backend() -> None:
    tex = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_final_submission.tex"

    result = extract_document_derivation_obligations(tex, focus_labels=["eq:incremental-cash-flow"])

    assert result["status"] == "extracted"
    assert result["backend_request_count"] == 0
    assert result["publication_enabled"] is False
    assert result["adapter_eligible_target_count"] == result["obligation_count"] == 1
    obligation = result["obligations"][0]
    assert obligation["obligation_digest"] == "7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0"
    assert obligation["operator_inventory"] == ["equality"]
    assert obligation["excluded_spans"][0]["excluded_sibling_label"] == "eq:incremental-npv"


def test_document_tree_prop_container_keeps_foc_children_separate_without_backend() -> None:
    tex = ROOT / "docs/risky-debt-maliar-deep-learning-lecture-note.tex"

    result = extract_document_derivation_obligations(tex, focus_labels=["prop:interior-foc"])

    assert result["status"] == "extracted"
    assert result["backend_request_count"] == 0
    assert [item["label"] for item in result["obligations"]] == ["eq:foc-k", "eq:foc-b"]
    assert len({item["obligation_digest"] for item in result["obligations"]}) == 2
    assert [target["label"] for target in result["targets"]] == ["eq:foc-k", "eq:foc-b"]
    assert all(target["parent_label"] == "prop:interior-foc" for target in result["targets"])


def test_document_derivation_tree_handles_multiline_bellman_as_generic_case(tmp_path: Path) -> None:
    tex = tmp_path / "generic.tex"
    _write_fixture(tex)

    result = audit_document_derivation_tree(tex, focus_labels=["eq:bellman"], max_attempts=1)

    assert result["targets"]
    domains = [domain for target in result["targets"] for domain in target["semantic_work_packet"]["semantic_domains"]]
    assert "bellman_value_recursion" in domains
    packets = [target["semantic_work_packet"] for target in result["targets"]]
    assert all("J_c(s)" not in packet["grouped_target"] for packet in packets)
    assert all(packet["grouped_target"] == packet["normalized_target"]["display_text"] for packet in packets)
    assert any("V_t^{\\star}(s)" in packet["full_display_source"] for packet in packets)
    assert any(packet["display_source_span"]["line_end"] > packet["display_source_span"]["line_start"] for packet in packets)
    assert all(packet["display_row_count"] == 1 for packet in packets)
    blockers = [blocker for target in result["targets"] for blocker in target["tree"]["blockers"]]
    assert not any(blocker["kind"] == "grouped_multiline_obligation_required" for blocker in blockers)
    assert "Group all rows for the label" not in result["markdown"]


def test_document_derivation_tree_writes_markdown_and_json(tmp_path: Path) -> None:
    tex = tmp_path / "generic.tex"
    output_md = tmp_path / "tree.md"
    output_json = tmp_path / "tree.json"
    _write_fixture(tex)

    result = audit_document_derivation_tree(
        tex,
        focus_labels=["eq:npv"],
        output_md=output_md,
        output_json=output_json,
        max_attempts=1,
    )

    assert result["output_md"] == str(output_md)
    assert result["output_json"] == str(output_json)
    assert output_md.exists()
    assert output_json.exists()
    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["metadata"]["contract"] == "document_derivation_tree_audit"
    assert "markdown" not in payload


def test_document_derivation_tree_builds_context_packet_for_proposition_label() -> None:
    tex = ROOT / "docs" / "risky-debt-maliar-deep-learning-lecture-note.tex"

    result = audit_document_derivation_tree(
        tex,
        focus_labels=["prop:interior-foc", "eq:foc-k", "eq:foc-b"],
        max_attempts=1,
    )

    assert result["coverage"]["missing_focus_labels"] == []
    assert result["coverage"]["context_target_labels"] == ["prop:interior-foc"]
    assert result["coverage"]["context_target_count"] == 1
    packet = result["context_targets"][0]
    assert packet["label"] == "prop:interior-foc"
    assert [target["label"] for target in packet["equation_targets"]] == ["eq:foc-k", "eq:foc-b"]
    assert any("interior" in item for item in packet["hypotheses"])
    assert "Proposition/Context Packets" in result["markdown"]
    assert "prop:interior-foc" in result["markdown"]


def test_document_derivation_tree_context_graph_classifies_stated_and_missing_foc_assumptions() -> None:
    tex = ROOT / "docs" / "risky-debt-maliar-deep-learning-lecture-note.tex"

    result = audit_document_derivation_tree(
        tex,
        focus_labels=["prop:interior-foc", "eq:foc-k", "eq:foc-b"],
        max_attempts=1,
    )

    assert result["coverage"]["context_graph_count"] == 3
    assert result["coverage"]["context_graph_status_counts"]["stated"] >= 1
    assert result["coverage"]["context_graph_status_counts"]["nearby_stated"] >= 1
    assert result["coverage"]["context_graph_status_counts"]["missing"] >= 1
    assert result["coverage"]["context_graph_status_counts"]["unresolved"] >= 1
    context_graph = result["context_targets"][0]["context_graph"]
    context_nodes = {node["id"]: node for node in context_graph["nodes"]}
    assert context_nodes["assumption_interior_action"]["status"] == "stated"
    assert context_nodes["assumption_relevant_functions_differentiable"]["status"] == "stated"
    assert context_nodes["requirement_conditional_integrability"]["status"] in {"missing", "unresolved"}
    assert context_nodes["requirement_expectation_derivative_interchange"]["status"] in {"missing", "unresolved"}
    assert context_nodes["requirement_conditional_integrability"]["source_refs"]
    assert "Local context graph" in result["markdown"]
    assert "Context graph statuses" in result["markdown"]


def test_document_derivation_tree_context_graph_reconciles_row_with_parent_proposition_context() -> None:
    tex = ROOT / "docs" / "risky-debt-maliar-deep-learning-lecture-note.tex"

    result = audit_document_derivation_tree(
        tex,
        focus_labels=["eq:foc-k"],
        max_attempts=1,
    )

    graph = result["targets"][0]["semantic_work_packet"]["context_graph"]
    nodes = {node["id"]: node for node in graph["nodes"]}
    assert nodes["assumption_interior_action"]["status"] == "nearby_stated"
    assert nodes["assumption_relevant_functions_differentiable"]["status"] == "nearby_stated"
    assert (
        nodes["route_assumption_target_function_is_differentiable_on_the_stated_domain"]["status"]
        == "nearby_stated"
    )
    assert nodes["route_assumption_conditional_expectation_law_is_defined_and_the_random_payoff_terms_are_integrable"]["status"] == "missing"
    assert nodes["route_assumption_differentiation_under_the_conditional_expectation_is_justified_and_no_omitted_transition_derivative_terms_are_present"]["status"] == "missing"
    assert graph["non_claim"].startswith("The context graph is deterministic source-evidence accounting")


def test_document_derivation_tree_branches_cite_typed_repair_obligations() -> None:
    tex = ROOT / "docs" / "risky-debt-maliar-deep-learning-lecture-note.tex"

    result = audit_document_derivation_tree(
        tex,
        focus_labels=["eq:foc-k"],
        max_attempts=1,
    )

    target = result["targets"][0]
    packet = target["semantic_work_packet"]
    typed = packet["typed_repair_obligation"]
    branches = target["tree"]["assumption_branches"]

    assert result["coverage"]["typed_repair_obligation_count"] == 1
    assert typed["metadata"]["contract"] == "typed_repair_obligation"
    assert typed["target_label"] == "eq:foc-k"
    assert "expectation" in typed["unresolved_constructs"]
    assert "derivative_expectation_interchange" in typed["unresolved_constructs"]
    assert typed["encodability"]["status"] == "blocked_pending_typed_assumptions"
    assert any(hint["backend"] == "manual_formalization" for hint in typed["route_hints"])
    assert branches
    assert all(typed["id"] in branch["typed_obligation_ids"] for branch in branches)
    assert all("expectation" in branch["typed_unresolved_constructs"] for branch in branches)
    assert target["tree"]["typed_repair_obligations"][0]["id"] == typed["id"]
    assert "Typed repair obligation" in result["markdown"]
    assert "Typed obligation ids" in result["markdown"]


def test_document_derivation_tree_keeps_simple_algebra_root_evidence_out_of_child(tmp_path: Path) -> None:
    tex = tmp_path / "simple.tex"
    tex.write_text(
        r"""
\section{Algebra}
\begin{equation}
\label{eq:simple}
x + 1 = 1 + x
\end{equation}
""",
        encoding="utf-8",
    )

    result = audit_document_derivation_tree(tex, focus_labels=["eq:simple"], max_attempts=2)
    target = result["targets"][0]
    tree = target["tree"]
    branch = tree["assumption_branches"][0]

    assert target["status"] == "partial_evidence"
    assert tree["backend_attempts"][0]["status"] == "proved"
    assert tree["backend_attempts"][0]["applicable_to_document_branch"] is False
    assert branch["backend_attempts"] == []
    assert branch["backend_evidence"]["raw_promotion"]["can_promote"] is False
    assert branch["backend_evidence"]["effective_document_promotion"]["can_promote"] is False
    assert branch["backend_evidence"]["binding_status"] == "no_branch_evidence"
    assert tree["branch_ranking"]["top_branch_id"] == branch["id"]
    assert tree["branch_ranking"]["rankings"][0]["outcome"] == "blocked_with_specific_next_evidence"
    assert branch["status"] == "unexecuted_branch_pending_bound_request"
    assert any(
        item["backend"] == "sympy" and item["status"] == "not_attempted_in_current_budget"
        for item in branch["translation_attempts"]
    )
    assert branch["translation_blockers"] == []
    assert any(
        blocker["kind"] == "branch_bound_backend_execution_required"
        for blocker in branch["blockers"]
    )
    assert "Branch backend attempts" not in result["markdown"]
    assert "status `proved`, evidence `certifying_backend`" in result["markdown"]
    assert tree["document_ready_repair_proposals"] == []
    assert tree["document_partial_evidence_reports"] == []
    gaps = tree["document_gap_reports"]
    assert gaps[0]["metadata"]["contract"] == "document_gap_report"
    assert gaps[0]["failure_classification"] == "branch_execution_pending"
    assert gaps[0]["failure_classifications"] == [
        "branch_execution_pending",
        "formalization_blocked",
    ]
    compiler = tree["tool_grounded_proposal_compiler"]
    assert compiler["metadata"]["contract"] == "tool_grounded_proposal_compiler_result"
    assert compiler["grounding_policy"] == "strict"
    assert compiler["status"] == "compiled"
    assert compiler["publication_mode"] == "disabled"
    assert compiler["validation_errors"] == []
    assert compiler["repair_proposal_count"] == 0
    assert compiler["gap_report_count"] == 1
    assert compiler["partial_evidence_count"] == 0
    assert compiler["compiled_items"][0]["publishable_as_repair"] is False
    assert compiler["compiled_items"][0]["publishable_as_gap_report"] is True
    assert compiler["compiled_items"][0]["reportable_as_partial_evidence"] is False
    assert compiler["compiled_items"][0]["evidence_refs"]
    assert compiler["compiled_items"][0]["remaining_blocker_ids"]
    assert any(
        "branch_bound_execution_required" in blocker_id
        for blocker_id in compiler["compiled_items"][0]["remaining_blocker_ids"]
    )
    assert compiler["final_tree_digest"] == tree["final_tree_digest"]
    assert result["coverage"]["tool_grounded_compiler_validation_error_count"] == 0
    assert result["coverage"]["promoted_count"] == 0
    assert result["coverage"]["raw_promoted_count"] == 1


def test_document_compiler_observes_serializable_final_tree_and_is_idempotent(
    tmp_path: Path,
    monkeypatch,
) -> None:
    tex = tmp_path / "expansion.tex"
    _write_fixture(tex)
    captured: list[tuple[dict, dict]] = []
    compile_report = document_tree._compile_tool_grounded_proposal_report

    def capture_final_tree(packet: dict, tree: dict, **kwargs):
        captured.append((deepcopy(packet), deepcopy(tree)))
        return compile_report(packet, tree, **kwargs)

    monkeypatch.setattr(document_tree, "_compile_tool_grounded_proposal_report", capture_final_tree)
    result = audit_document_derivation_tree(tex, focus_labels=["eq:npv"], max_attempts=1)

    assert len(captured) == 1
    packet, final_tree = captured[0]
    json.dumps(final_tree, sort_keys=True)
    first = compile_report(packet, deepcopy(final_tree))
    second = compile_report(packet, deepcopy(final_tree))
    public_compiler = result["targets"][0]["tree"]["tool_grounded_proposal_compiler"]

    assert first == second
    assert first["compiled_after_recursive_expansion"] is True
    assert first["expanded_node_ids"]
    assert first["final_tree_digest"] == public_compiler["final_tree_digest"]
    assert first["final_tree_digest"] == result["targets"][0]["tree"]["final_tree_digest"]
    assert first["publication_mode"] == "disabled"
    assert first["repair_proposal_count"] == 0


def test_document_derivation_tree_branch_backend_evidence_names_foc_translation_blockers() -> None:
    tex = ROOT / "docs" / "risky-debt-maliar-deep-learning-lecture-note.tex"

    result = audit_document_derivation_tree(
        tex,
        focus_labels=["eq:foc-k"],
        max_attempts=1,
    )
    branch = result["targets"][0]["tree"]["assumption_branches"][0]
    blocker_kinds = {blocker["kind"] for blocker in branch["translation_blockers"]}

    assert branch["status"] == "blocked_before_backend_certification"
    assert branch["backend_attempts"] == []
    assert branch["backend_evidence"]["raw_promotion"]["can_promote"] is False
    assert branch["backend_evidence"]["effective_document_promotion"]["can_promote"] is False
    assert branch["agent_hypothesis_expansions"]
    assert all(
        group["metadata"]["contract"] == "agent_hypothesis_expansion_set"
        for group in branch["agent_hypothesis_expansions"]
    )
    assert any(
        candidate["status"] == "candidate_pending_tree_verification"
        for group in branch["agent_hypothesis_expansions"]
        for candidate in group["candidates"]
    )
    assert any(record["kind"] == "rule_hypothesis_candidate" for record in branch["expansion_records"])
    assert not any(record["kind"] == "agent_hypothesis_candidate" for record in branch["expansion_records"])
    assert result["targets"][0]["tree"]["branch_ranking"]["rankings"][0]["outcome"] == "blocked_with_specific_next_evidence"
    assert result["targets"][0]["tree"]["branch_ranking"]["rankings"][0]["veto_entry_ids"]
    assert all(
        "score" not in item and "score_components" not in item
        for item in result["targets"][0]["tree"]["branch_ranking"]["rankings"]
    )
    assert "conditional_law_translation_required" in blocker_kinds
    assert "integrability_translation_required" in blocker_kinds
    assert "derivative_expectation_interchange_required" in blocker_kinds
    assert "missing_domain_or_assumption_required" in blocker_kinds
    assert any(
        item["status"] == "blocked_before_execution" and item["blocker_ids"]
        for item in branch["translation_attempts"]
    )
    assert "conditional law" in result["markdown"].lower()
    assert "derivative-under-expectation" in result["markdown"].lower()


def test_document_derivation_tree_blocked_foc_renders_gap_report_not_repair_proposal() -> None:
    tex = ROOT / "docs" / "risky-debt-maliar-deep-learning-lecture-note.tex"

    result = audit_document_derivation_tree(
        tex,
        focus_labels=["eq:foc-k"],
        max_attempts=1,
    )

    target = result["targets"][0]
    assert target["tree"]["document_ready_repair_proposals"] == []
    gap_report = target["tree"]["document_gap_reports"][0]
    compiler = target["tree"]["tool_grounded_proposal_compiler"]

    assert gap_report["metadata"]["contract"] == "document_gap_report"
    assert gap_report["closure_status"] == "blocked_at_exact_node"
    assert compiler["metadata"]["contract"] == "tool_grounded_proposal_compiler_result"
    assert compiler["status"] == "compiled"
    assert compiler["repair_proposal_count"] == 0
    assert compiler["gap_report_count"] == 1
    assert compiler["validation_errors"] == []
    assert compiler["compiled_items"][0]["publishable_as_repair"] is False
    assert compiler["compiled_items"][0]["publishable_as_gap_report"] is True
    assert compiler["compiled_items"][0]["remaining_blocker_ids"]
    assert compiler["compiled_items"][0]["evidence_refs"]
    assert "proposed_edit" not in gap_report
    assert gap_report["context_branch_id"] in target["tree"]["branch_ranking"]["nondominated_branch_ids"]
    assert gap_report["ranking"]["outcome"] == "blocked_with_specific_next_evidence"
    assert any(item["status"] == "missing" for item in gap_report["missing_or_unresolved_assumptions"])
    assert any(item["status"] == "nearby_stated" for item in gap_report["already_stated_assumptions"])
    assert gap_report["context_branch_selection_authority"] == "serialization_only_nondominated_context"
    nondominated = set(target["tree"]["branch_ranking"]["nondominated_branch_ids"])
    assert any(
        branch["id"] in nondominated
        and any("conditional kernel" in assumption for assumption in branch["assumptions"])
        for branch in target["tree"]["assumption_branches"]
    )
    assert any("conditioning object is `z`" in step["detail"] for step in gap_report["derivation_route_under_assumptions"])
    assert "Repair assumptions for" in gap_report["candidate_edit_blocked"]["blocked_latex"]
    assert gap_report["backend_evidence"]["status"] == "typed_translation_blocked"
    assert any(
        blocker["kind"] == "conditional_law_translation_required"
        for blocker in gap_report["remaining_blockers_before_certification"]
    )
    assert gap_report["source_refs_for_missing_or_unresolved"]
    assert "Document-ready repair proposals" in result["markdown"]
    assert "None generated from the ranked branch evidence" in result["markdown"]
    assert "Document gap reports" in result["markdown"]
    assert "Tool-grounded proposal compiler" in result["markdown"]
    assert "publishable_as_repair=`False`" in result["markdown"]
    assert "document_gap_report" in result["markdown"]
    assert "Why this is a derivation problem" in result["markdown"]


def test_document_derivation_tree_middle_bar_conditioning_object_is_not_corrupted(tmp_path: Path) -> None:
    tex = tmp_path / "middlebar.tex"
    tex.write_text(
        r"""
\section{Middle bar}
\begin{equation}
\label{eq:middle}
\Delta \NPV_i =
\E\left[
  \Delta CF_i
  \,\middle|\, \mathcal{I}_{id}
\right].
\end{equation}
""",
        encoding="utf-8",
    )

    result = audit_document_derivation_tree(tex, focus_labels=["eq:middle"], max_attempts=1)

    branch = result["targets"][0]["tree"]["assumption_branches"][0]
    route_text = " ".join(step["detail"] for step in branch["derivation_route_under_assumptions"])
    blocked_text = result["targets"][0]["tree"]["document_gap_reports"][0]["candidate_edit_blocked"]["blocked_latex"]

    assert "conditioning object is `\\mathcal{I}_{id}`" in route_text
    assert "dle\\|" not in route_text
    assert "\\mathcal{I}_{id}" in blocked_text


def test_document_derivation_tree_mcp_facade_and_server_expose_tool(tmp_path: Path) -> None:
    tex = tmp_path / "generic.tex"
    _write_fixture(tex)

    tools = {tool["name"]: tool for tool in list_mcp_tools()}
    facade = call_mcp_tool(
        "audit_document_derivation_tree",
        {
            "tex_path": str(tex),
            "focus_labels": ["eq:npv"],
            "max_attempts": 1,
            "search_mode": "agent_guided",
            "grounding_policy": "strict",
            "workers": 1,
            "response_mode": "detailed",
        },
    )
    server = server_audit_document_derivation_tree(
        str(tex),
        focus_labels=["eq:npv"],
        max_attempts=1,
        search_mode="agent_guided",
        grounding_policy="strict",
        workers=1,
        response_mode="detailed",
    )
    assert server.isError is False
    assert server.content[0].text == (
        "MathDevMCP structured result; read structuredContent."
    )
    assert server.structuredContent is not None
    server_payload = server.structuredContent

    assert tools["audit_document_derivation_tree"]["output_contract"] == "document_derivation_response"
    assert facade["metadata"]["contract"] == "document_derivation_response"
    assert server_payload["metadata"]["contract"] == "document_derivation_response"
    assert facade["audit_metadata"]["contract"] == "document_derivation_tree_audit"
    assert server_payload["audit_metadata"]["contract"] == "document_derivation_tree_audit"
    assert facade["response_mode"] == server_payload["response_mode"] == "detailed"
    assert facade["search_mode"] == server_payload["search_mode"] == "agent_guided"
    assert facade["grounding_policy"] == server_payload["grounding_policy"] == "strict"
    assert facade["execution"]["workers_used"] == server_payload["execution"]["workers_used"] == 1
    assert (
        facade["targets"][0]["tree"]["tool_grounded_proposal_compiler"]["metadata"]["contract"]
        == "tool_grounded_proposal_compiler_result"
    )
    assert (
        server_payload["targets"][0]["tree"]["tool_grounded_proposal_compiler"]["metadata"]["contract"]
        == "tool_grounded_proposal_compiler_result"
    )


def test_document_derivation_tree_parallel_workers_preserve_logical_order(tmp_path: Path) -> None:
    tex = tmp_path / "generic.tex"
    _write_fixture(tex)

    serial = audit_document_derivation_tree(
        tex,
        focus_labels=["eq:npv", "eq:bellman"],
        max_attempts=1,
        workers=1,
    )
    parallel = audit_document_derivation_tree(
        tex,
        focus_labels=["eq:npv", "eq:bellman"],
        max_attempts=1,
        workers=2,
    )

    assert serial["execution"]["mode"] == "serial"
    assert parallel["execution"]["mode"] == "parallel"
    assert parallel["execution"]["workers_used"] == 2
    assert parallel["execution"]["failure_count"] == 0
    serial_summary = [
        (
            target["label"],
            target["row_index"],
            target["status"],
            target["tree"]["branch_ranking"].get("top_branch_id"),
            target["tree"]["tool_grounded_proposal_compiler"].get("status"),
            target["tree"]["tool_grounded_proposal_compiler"].get("repair_proposal_count"),
            target["tree"]["tool_grounded_proposal_compiler"].get("gap_report_count"),
        )
        for target in serial["targets"]
    ]
    parallel_summary = [
        (
            target["label"],
            target["row_index"],
            target["status"],
            target["tree"]["branch_ranking"].get("top_branch_id"),
            target["tree"]["tool_grounded_proposal_compiler"].get("status"),
            target["tree"]["tool_grounded_proposal_compiler"].get("repair_proposal_count"),
            target["tree"]["tool_grounded_proposal_compiler"].get("gap_report_count"),
        )
        for target in parallel["targets"]
    ]
    assert parallel_summary == serial_summary
    assert [target["label"] for target in parallel["targets"]] == [target["label"] for target in serial["targets"]]


def test_cli_audit_document_derivation_tree_writes_artifacts(tmp_path: Path) -> None:
    tex = tmp_path / "generic.tex"
    output_md = tmp_path / "tree.md"
    output_json = tmp_path / "tree.json"
    _write_fixture(tex)

    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-document-derivation-tree",
            str(tex),
            "--focus-label",
            "eq:npv",
            "--max-attempts",
            "1",
            "--search-mode",
            "agent_guided",
            "--grounding-policy",
            "strict",
            "--workers",
            "1",
            "--output-md",
            str(output_md),
            "--output-json",
            str(output_json),
            "--response-mode",
            "detailed",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads(completed.stdout)
    assert payload["metadata"]["contract"] == "document_derivation_response"
    assert payload["audit_metadata"]["contract"] == "document_derivation_tree_audit"
    assert payload["response_mode"] == "detailed"
    assert payload["search_mode"] == "agent_guided"
    assert payload["grounding_policy"] == "strict"
    assert payload["execution"]["mode"] == "serial"
    assert "tool_grounded_proposal_compiler" in {item["tool"] for item in payload["tool_uses"]}
    assert (
        payload["targets"][0]["tree"]["tool_grounded_proposal_compiler"]["metadata"]["contract"]
        == "tool_grounded_proposal_compiler_result"
    )
    assert output_md.exists()
    assert output_json.exists()
    markdown = output_md.read_text(encoding="utf-8")
    assert "Search mode: `agent_guided`" in markdown
    assert "Grounding policy: `strict`" in markdown
    assert "Execution: `serial`" in markdown
