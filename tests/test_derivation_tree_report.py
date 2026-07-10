from mathdevmcp.derivation_search_tree import (
    AssumptionSet,
    BackendAttempt,
    BlockerNode,
    DerivationStep,
    PatchCandidate,
    SourceSpan,
    build_initial_search_tree,
    certifying_backend_attempt,
    make_search_node,
)
from mathdevmcp.derivation_tree_report import render_derivation_tree_report
from mathdevmcp.external_tool_policy import external_tool_first_plan


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


def test_tree_report_renders_location_problem_why_tools_patch_and_blockers() -> None:
    plan = external_tool_first_plan("x + 1 = 1 + x", capabilities=CAPABILITIES, integrations=INTEGRATIONS)
    node = make_search_node(
        node_id="root",
        target="x + 1 = 1 + x",
        status="partial",
        external_tool_plan=plan,
        source_span=SourceSpan(file="paper.tex", line_start=7, label="eq:comm"),
        assumptions=[
            AssumptionSet(
                id="ring_addition",
                assumptions=["x belongs to a commutative additive group."],
                status="proposed",
                source="test",
            )
        ],
        backend_attempts=[
            BackendAttempt(
                id="sympy_attempt",
                tool="sympy",
                status="unknown",
                evidence_kind="diagnostic",
                certification_status="diagnostic",
                input_summary="x + 1 = 1 + x",
            )
        ],
        derivation_steps=[
            DerivationStep(
                id="step_1",
                claim="x + 1 = 1 + x",
                justification="commutativity of addition",
                checker="sympy",
                checker_status="diagnostic",
            )
        ],
        blockers=[
            BlockerNode(
                id="blocker_cert",
                kind="backend_certificate_required",
                problem="No scoped backend certificate is attached.",
                why="Diagnostic evidence cannot prove the branch.",
                required_next_evidence="Run a certifying backend check.",
                source="test",
            )
        ],
        patch_candidates=[
            PatchCandidate(
                id="patch_assumption",
                kind="add_assumption",
                location={"file": "paper.tex", "line_start": 7, "label": "eq:comm"},
                proposed_text="State that x lives in a commutative additive group.",
                rationale="The algebraic rewrite uses commutativity.",
                validation_status="diagnostic",
            )
        ],
    )
    tree = {
        "metadata": {"schema_version": "1.0", "contract": "derivation_search_tree_result"},
        "status": "partial",
        "root": node,
        "non_claims": [{"code": "source_tree_not_proof", "text": "Tree is diagnostic."}],
    }

    report = render_derivation_tree_report(tree)
    section = report["sections"][0]
    markdown = report["markdown"]

    assert report["metadata"]["contract"] == "derivation_tree_report_result"
    assert section["location"] == "paper.tex > eq:comm > line 7"
    assert "partially resolved" in section["problem"]
    assert "Diagnostic evidence cannot prove" in section["mathematical_why"]
    assert section["tools_used"][0]["id"] == "sympy_attempt"
    assert section["assumptions"][0]["id"] == "ring_addition"
    assert section["proposed_patches"][0]["id"] == "patch_assumption"
    assert section["blockers"][0]["id"] == "blocker_cert"
    assert "Location:" in markdown
    assert "Problem:" in markdown
    assert "Why:" in markdown
    assert "Proposed fix:" in markdown
    assert "Remaining blockers:" in markdown
    assert "`tree_report_not_patch_or_proof`" in markdown


def test_tree_report_does_not_fabricate_patch_when_tree_lacks_candidate() -> None:
    tree = build_initial_search_tree(
        "x + 1 = 1 + x",
        source_span=SourceSpan(file="paper.tex", line_start=10, label="eq:no-patch"),
        capabilities=CAPABILITIES,
        integrations=INTEGRATIONS,
    )

    report = render_derivation_tree_report(tree)
    section = report["sections"][0]

    assert section["proposed_patches"] == []
    assert "No patch candidate is present" in section["warnings"][0]
    assert "No patch candidate supplied by the tree." in report["markdown"]


def test_tree_report_preserves_certifying_status_without_blocker() -> None:
    plan = external_tool_first_plan("a + b = b + a", capabilities=CAPABILITIES, integrations=INTEGRATIONS)
    node = make_search_node(
        node_id="root",
        target="a + b = b + a",
        status="proved",
        external_tool_plan=plan,
        backend_attempts=[
            certifying_backend_attempt(
                attempt_id="sympy_cert",
                tool="sympy",
                status="proved",
                input_summary="a + b = b + a",
                output_ref="artifact://sympy/sympy_cert.json",
            )
        ],
    )
    tree = {
        "metadata": {"schema_version": "1.0", "contract": "derivation_search_tree_result"},
        "status": "proved",
        "root": node,
        "non_claims": [],
    }

    report = render_derivation_tree_report(tree)
    section = report["sections"][0]

    assert section["status"] == "proved"
    assert section["promotion"]["can_promote"] is True
    assert section["blockers"] == []
    assert "scoped certifying evidence" in section["problem"]
    assert "No patch candidate is present" not in report["markdown"]


def test_tree_report_exposes_malformed_proved_status_guard_errors() -> None:
    plan = external_tool_first_plan("x = x", capabilities=CAPABILITIES, integrations=INTEGRATIONS)
    node = make_search_node(
        node_id="root",
        target="x = x",
        status="proved",
        external_tool_plan=plan,
        backend_attempts=[
            BackendAttempt(
                id="diagnostic_attempt",
                tool="sympy",
                status="unknown",
                evidence_kind="diagnostic",
                certification_status="diagnostic",
                input_summary="x = x",
            )
        ],
    )
    tree = {
        "metadata": {"schema_version": "1.0", "contract": "derivation_search_tree_result"},
        "status": "proved",
        "root": node,
        "non_claims": [],
    }

    report = render_derivation_tree_report(tree)
    section = report["sections"][0]

    assert section["promotion"]["can_promote"] is False
    assert "does not support" in section["problem"]
    assert "Promotion guard rejected" in section["mathematical_why"]
    assert "proved status requires scoped certifying backend evidence" in report["markdown"]
    assert "can_promote=False" in report["markdown"]


def test_tree_report_renders_child_branches_and_budget_blocker() -> None:
    plan = external_tool_first_plan("A*B = B*A", capabilities=CAPABILITIES, integrations=INTEGRATIONS)
    child = make_search_node(
        node_id="branch_counterexample",
        target="A*B = B*A",
        status="budget_exhausted",
        external_tool_plan=plan,
        blockers=[
            BlockerNode(
                id="blocker_budget",
                kind="budget_exhausted",
                problem="Budget exhausted before Lean check.",
                why="The smoke profile only allowed one attempt.",
                required_next_evidence="Increase budget.",
                source="controller",
            )
        ],
    )
    root = make_search_node(
        node_id="root",
        target="A*B = B*A",
        status="partial",
        external_tool_plan=plan,
        children=[child],
    )
    tree = {
        "metadata": {"schema_version": "1.0", "contract": "derivation_search_tree_result"},
        "status": "partial",
        "root": root,
        "non_claims": [],
    }

    report = render_derivation_tree_report(tree)

    assert [section["id"] for section in report["sections"]] == ["root", "branch_counterexample"]
    assert report["sections"][1]["blockers"][0]["kind"] == "budget_exhausted"
    assert "`branch_counterexample`" in report["markdown"]
    assert "Increase budget." in report["markdown"]
