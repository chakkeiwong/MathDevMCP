import hashlib
from pathlib import Path

from mathdevmcp.math_document_rigor import (
    _gaps_from_fix_report,
    audit_math_document_rigor,
    plan_math_document_rigor_audit,
    render_math_document_rigor_markdown,
)


def _write_fixture(path: Path) -> None:
    path.write_text(
        r"""
\section{Valuation}
We define a toy NPV object.
\begin{equation}
\label{eq:toy-npv}
NPV = CF_0 + \beta CF_1
\end{equation}

\section{Identification}
\begin{equation}
\label{eq:toy-estimand}
\mathbb{E}[Y(1)-Y(0)]
\end{equation}
""",
        encoding="utf-8",
    )


def test_plan_math_document_rigor_audit_selects_exact_file_targets(tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    _write_fixture(tex)

    result = plan_math_document_rigor_audit(tex, max_labels=1)

    assert result["metadata"] == {"schema_version": "1.0", "contract": "math_document_rigor_audit_plan"}
    assert result["document_inventory"]["equation_localization"]["row_count"] == 2
    assert result["target_selection"]["selected_count"] == 1
    assert result["target_selection"]["partial_coverage"] is True
    assert result["target_selection"]["targets"][0]["label"] == "eq:toy-npv"
    assert result["tool_uses"][0]["tool"] == "locate_equations_in_file"


def test_plan_math_document_rigor_audit_dedupes_focus_labels(tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    _write_fixture(tex)

    result = plan_math_document_rigor_audit(tex, focus_labels=["eq:toy-npv", "eq:toy-npv"])

    assert result["target_selection"]["selected_count"] == 1
    assert [target["label"] for target in result["target_selection"]["targets"]] == ["eq:toy-npv"]


def test_plan_math_document_rigor_audit_selects_one_row_per_label(tmp_path: Path) -> None:
    tex = tmp_path / "multirow.tex"
    tex.write_text(
        r"""
\section{Valuation}
\begin{align}
\label{eq:multi}
a &= b \\
c &= d
\end{align}
""",
        encoding="utf-8",
    )

    result = plan_math_document_rigor_audit(tex, focus_labels=["eq:multi"])

    assert result["target_selection"]["selected_count"] == 1
    assert [target["label"] for target in result["target_selection"]["targets"]] == ["eq:multi"]


def test_audit_math_document_rigor_returns_agent_consumable_report(tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    output_md = tmp_path / "rigor.md"
    output_json = tmp_path / "rigor.json"
    _write_fixture(tex)

    result = audit_math_document_rigor(
        tex,
        output_md=output_md,
        output_json=output_json,
        focus_labels=["eq:toy-npv"],
        max_labels=1,
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "math_document_rigor_audit"}
    assert result["coverage"]["target_file_only"] is True
    assert result["coverage"]["selected_count"] == 1
    assert result["backend_provenance"]["certification_boundary"]
    assert any(item["tool"] == "doctor_report" for item in result["tool_uses"])
    assert result["gaps"] == []
    assert result["proposals"] == []
    assert result["issues"][0]["status"] == "resolved_by_existing_context"
    assert result["source_reports"]["raw_route_gaps"]
    markdown = output_md.read_text(encoding="utf-8")
    assert "# Actionable Math Document Rigor Audit" in markdown
    assert "## Issue Ledger" in markdown
    assert "Detailed evidence pointer" in markdown
    assert "## Backend Provenance" not in markdown
    assert "## Backend Provenance" in result["forensic_markdown"]
    assert "Location:" in markdown
    assert "Boundary:" in markdown
    assert output_json.exists()


def test_render_math_document_rigor_markdown_preserves_non_claims(tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    _write_fixture(tex)
    result = audit_math_document_rigor(tex, focus_labels=["eq:toy-npv"], max_labels=1)

    markdown = render_math_document_rigor_markdown(result)

    assert "not a proof of the document" in markdown
    assert "leandojo_not_certificate" in markdown


def test_audit_math_document_rigor_restricts_delegated_audit_to_exact_file(tmp_path: Path) -> None:
    old = tmp_path / "old_version.tex"
    final = tmp_path / "final_submission.tex"
    old.write_text(
        r"""
\section{Old}
\begin{equation}
\label{eq:shared}
old = 1
\end{equation}
""",
        encoding="utf-8",
    )
    final.write_text(
        r"""
\section{Final}
\begin{equation}
\label{eq:shared}
final = 2
\end{equation}
""",
        encoding="utf-8",
    )

    result = audit_math_document_rigor(final, focus_labels=["eq:shared"], max_labels=1)
    markdown = result["markdown"]

    assert "final_submission.tex" in markdown
    assert "old_version.tex" not in markdown
    audit_tool_use = next(item for item in result["tool_uses"] if item["tool"] == "audit_and_propose_fix")
    assert audit_tool_use["arguments"]["root"] == str(tmp_path)
    assert audit_tool_use["arguments"]["target_file"] == final.name
    assert audit_tool_use["arguments"]["source_digest"] == hashlib.sha256(final.read_bytes()).hexdigest()


def test_audit_math_document_rigor_selects_requested_backend_env(monkeypatch, tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    _write_fixture(tex)
    seen = {}

    def fake_doctor_report(*, backend_config=None):
        seen["doctor_env"] = backend_config.conda_env if backend_config else None
        return {"ok": True, "python": {"executable": "python"}, "capabilities": {"lean_dojo": {"status": "available", "environment_scope": "backend_python", "backend_env": seen["doctor_env"]}}, "metadata": {"schema_version": "1.0", "contract": "doctor_report"}}

    def fake_lean_readiness(root, *, backend_config=None):
        seen["readiness_env"] = backend_config.conda_env if backend_config else None
        return {"status": "ready_with_caveats", "lean_dojo": {"status": "available", "environment_scope": "backend_python", "backend_env": seen["readiness_env"]}, "metadata": {"schema_version": "1.0", "contract": "lean_readiness"}}

    monkeypatch.setattr("mathdevmcp.math_document_rigor.doctor_report", fake_doctor_report)
    monkeypatch.setattr("mathdevmcp.math_document_rigor.lean_readiness", fake_lean_readiness)

    result = audit_math_document_rigor(tex, focus_labels=["eq:toy-npv"], backend_env="mathdevmcp-backends")

    assert seen["doctor_env"] == "mathdevmcp-backends"
    assert seen["readiness_env"] == "mathdevmcp-backends"
    assert result["backend_provenance"]["doctor"]["capabilities"]["lean_dojo"]["environment_scope"] == "backend_python"


def test_audit_math_document_rigor_reuses_exact_audit_fix_evidence(monkeypatch, tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    _write_fixture(tex)
    digest = hashlib.sha256(tex.read_bytes()).hexdigest()
    reused = {
        "workflow": "audit_and_propose_fix",
        "evidence": [
            {
                "low_level": {
                    "source": {"file": tex.name, "source_digest": digest},
                    "coverage": {
                        "audit_complete": True,
                        "audited_labels": [{"label": "eq:toy-npv"}],
                    },
                    "agent_handoff": {"proposal_details": []},
                    "tool_uses": [],
                }
            }
        ],
    }

    def fail_recompute(*args, **kwargs):
        raise AssertionError("audit_and_propose_fix should not be recomputed")

    monkeypatch.setattr("mathdevmcp.math_document_rigor.audit_and_propose_fix", fail_recompute)

    result = audit_math_document_rigor(
        tex,
        focus_labels=["eq:toy-npv"],
        max_labels=1,
        audit_fix_result=reused,
    )

    tool_use = next(item for item in result["tool_uses"] if item["tool"] == "audit_and_propose_fix")
    assert tool_use["arguments"]["reused_exact_evidence"] is True


def test_audit_math_document_rigor_rejects_reused_evidence_without_source_file(tmp_path: Path) -> None:
    tex = tmp_path / "toy.tex"
    _write_fixture(tex)
    reused = {
        "workflow": "audit_and_propose_fix",
        "evidence": [
            {
                "low_level": {
                    "source": {"source_digest": hashlib.sha256(tex.read_bytes()).hexdigest()},
                    "coverage": {
                        "audit_complete": True,
                        "audited_labels": [{"label": "eq:toy-npv"}],
                    },
                }
            }
        ],
    }

    import pytest

    with pytest.raises(ValueError, match="source file does not match"):
        audit_math_document_rigor(
            tex,
            focus_labels=["eq:toy-npv"],
            max_labels=1,
            audit_fix_result=reused,
        )


def test_gaps_from_fix_report_preserves_singular_evidence_ref() -> None:
    gaps, proposals = _gaps_from_fix_report(
        {
            "agent_handoff": {
                "proposal_details": [
                    {
                        "target": "obligation_1",
                        "location": "paper.tex > line 10",
                        "problem": "Missing derivation step.",
                        "rationale": "The equality needs an explicit route.",
                        "proposed_fix": "Insert the intermediate equality.",
                        "evidence_ref": "proof_audit_v2:eq:target:obligation_1",
                        "validation": {"status": "attempted_not_certified"},
                    }
                ]
            }
        }
    )

    assert gaps[0]["evidence_refs"] == ["proof_audit_v2:eq:target:obligation_1"]
    assert proposals[0]["evidence_refs"] == ["proof_audit_v2:eq:target:obligation_1"]


def test_gaps_from_fix_report_adds_backend_evidence_fallback() -> None:
    gaps, proposals = _gaps_from_fix_report(
        {
            "agent_handoff": {
                "proposal_details": [
                    {
                        "target": "obligation_2",
                        "location": "paper.tex > line 20",
                        "summary": "Formalize the missing obligation.",
                        "evidence_ref": "proof_audit_v2:eq:target:obligation_2",
                    }
                ]
            }
        }
    )

    assert gaps[0]["backend_evidence"]["status"] == "not_certified"
    assert "reason" in gaps[0]["backend_evidence"]
    assert proposals[0]["backend_evidence"]["status"] == "not_certified"


def test_gaps_from_fix_report_preserves_concrete_math_payload() -> None:
    gaps, proposals = _gaps_from_fix_report(
        {
            "agent_handoff": {
                "proposal_details": [
                    {
                        "kind": "split_derivation_step",
                        "target": "obligation_5",
                        "location": "paper.tex > line 770",
                        "problem": "The derivation row is not split into a safe proof obligation.",
                        "rationale": "The equality needs a local derivation.",
                        "proposed_fix": "Replace the split row with `x = y`. Then prove: show x equals y.",
                        "proof_target": "x = y",
                        "derivation_plan": "Use the definition of x and substitute y.",
                        "math_fix": {
                            "equation": "x = y",
                            "replacement_latex": "\\begin{equation}\n  x = y\n\\end{equation}",
                            "derivation_obligation": "Use the definition of x and substitute y.",
                        },
                        "evidence_ref": "proof_audit_v2:eq:target:obligation_5",
                        "validation": {"status": "attempted_not_certified", "reason": "SymPy attempted."},
                    }
                ]
            }
        }
    )

    assert gaps[0]["substantive_classification"] == "concrete_repair"
    assert gaps[0]["replacement_latex"].startswith("\\begin{equation}")
    assert gaps[0]["proof_target"] == "x = y"
    assert "substitute y" in gaps[0]["derivation_plan"]
    assert proposals[0]["substantive_classification"] == "concrete_repair"
    assert proposals[0]["math_fix"]["equation"] == "x = y"


def test_gaps_from_fix_report_demotes_review_boundary_to_diagnostic() -> None:
    gaps, proposals = _gaps_from_fix_report(
        {
            "agent_handoff": {
                "proposal_details": [
                    {
                        "kind": "add_review_boundary",
                        "target": "obligation_3",
                        "location": "paper.tex > line 834",
                        "problem": "The claim still needs human review before certification.",
                        "rationale": "Typed obligation requires human review.",
                        "proposed_fix": "Add a local review boundary before treating this claim as derived or implemented.",
                        "evidence_ref": "proof_audit_v2:eq:target:obligation_3",
                    }
                ]
            }
        }
    )

    assert gaps[0]["substantive_classification"] == "diagnostic_abstention"
    assert "Add a local review boundary" not in proposals[0]["proposed_fix"]
    assert proposals[0]["required_evidence_before_repair"]
    assert proposals[0]["smallest_next_audit"]["tool"] == "audit_and_propose_fix"


def test_gaps_from_fix_report_preserves_colon_label_in_next_audit() -> None:
    _gaps, proposals = _gaps_from_fix_report(
        {
            "agent_handoff": {
                "proposal_details": [
                    {
                        "kind": "split_derivation_step",
                        "target": "obligation_1",
                        "location": "paper.tex > line 10",
                        "problem": "Missing derivation step.",
                        "rationale": "The equality needs an explicit route.",
                        "proof_target": "x = y",
                        "derivation_plan": "Substitute the definition.",
                        "math_fix": {
                            "equation": "x = y",
                            "replacement_latex": "\\begin{equation}\n  x = y\n\\end{equation}",
                        },
                        "evidence_ref": "proof_audit_v2:eq:incremental-npv:obligation_1",
                    }
                ]
            }
        }
    )

    assert proposals[0]["smallest_next_audit"]["label"] == "eq:incremental-npv"


def test_gaps_from_fix_report_demotes_malformed_replacement_latex() -> None:
    gaps, proposals = _gaps_from_fix_report(
        {
            "agent_handoff": {
                "proposal_details": [
                    {
                        "kind": "split_derivation_step",
                        "target": "obligation_5",
                        "location": "paper.tex > line 20",
                        "problem": "The derivation row is not split into a safe proof obligation.",
                        "rationale": "The equality needs a local derivation.",
                        "proof_target": "x = \\left[ y",
                        "derivation_plan": "Close the conditional expectation and justify the equality.",
                        "math_fix": {
                            "equation": "x = \\left[ y",
                            "replacement_latex": "\\begin{equation}\n  x = \\left[ y\n\\end{equation}",
                        },
                        "evidence_ref": "proof_audit_v2:eq:incremental-npv:obligation_5",
                    }
                ]
            }
        }
    )

    assert gaps[0]["substantive_classification"] == "diagnostic_abstention"
    assert "failed conservative" in gaps[0]["why_not_concrete"]
    assert proposals[0]["required_evidence_before_repair"]


def test_render_math_document_rigor_markdown_separates_concrete_and_diagnostic_ledgers() -> None:
    result = {
        "tex_path": "paper.tex",
        "coverage": {
            "status": "selected_scope_complete",
            "selected_count": 1,
            "available_labeled_equation_count": 1,
            "gap_count": 2,
            "proposal_count": 2,
            "concrete_repair_count": 1,
            "diagnostic_abstention_count": 1,
        },
        "backend_provenance": {
            "doctor": {
                "python": {"executable": "python"},
                "capabilities": {"lean_dojo": {"status": "available", "environment_scope": "backend_python", "backend_env": "mathdevmcp-backends"}},
            },
            "certification_boundary": "Certification boundary.",
        },
        "document_inventory": {
            "line_count": 10,
            "section_count": 1,
            "equation_localization": {"row_count": 1},
            "labeled_equation_count": 1,
            "label_ref_hygiene": {"duplicate_labels": [], "missing_refs": []},
        },
        "tool_uses": [],
        "gaps": [],
        "proposals": [],
        "proposal_ledgers": {
            "concrete_repairs": [
                {
                    "id": "proposal_concrete",
                    "label": "obligation_1",
                    "location": "paper.tex > line 10",
                    "problem": "Missing equality derivation.",
                    "why_mathematically_problematic": "The equality is used without derivation.",
                    "proposed_fix": "Replace the affected displayed math with the replacement LaTeX below.",
                    "replacement_latex": "\\begin{equation}\n  x = y\n\\end{equation}",
                    "proof_target": "x = y",
                    "derivation_plan": "Substitute the definition.",
                    "backend_evidence": {"status": "attempted_not_certified", "reason": "backend attempted"},
                    "smallest_next_audit": {"tool": "audit_derivation_v2_label", "label": "eq:x", "purpose": "rerun"},
                    "evidence_refs": ["proof_audit_v2:eq:x:obligation_1"],
                }
            ],
            "diagnostic_abstentions": [
                {
                    "id": "proposal_diagnostic",
                    "label": "obligation_2",
                    "location": "paper.tex > line 20",
                    "problem": "Human review required.",
                    "why_mathematically_problematic": "The source is not formalized.",
                    "proposed_fix": "Do not edit the document from this item alone; first satisfy the required evidence before repair.",
                    "why_not_concrete": "A review boundary is not an edit.",
                    "required_evidence_before_repair": ["Exact replacement LaTeX."],
                    "actionable_abstention": {
                        "blocker_kind": "conditional_expectation",
                        "safe_wording": "Do not edit this item yet.",
                        "missing_obligations": [
                            {
                                "id": "conditional_law_defined",
                                "kind": "probability_condition",
                                "mathematically_missing": "A conditional law.",
                                "why_missing": "Expectation notation needs a law.",
                                "closes": "Defines the expectation.",
                            }
                        ],
                        "possible_assumption_sets": [
                            {
                                "id": "kernel_integrability_condition",
                                "role": "general sufficient condition",
                                "assumptions": ["A conditional kernel exists."],
                                "closes": "The expectation is finite.",
                            }
                        ],
                        "how_derivation_can_work": [
                            {"step": "Define law", "detail": "Fix the kernel."}
                        ],
                        "next_audit": {"tool": "audit_and_propose_assumptions", "purpose": "Generate assumptions."},
                        "non_claim": "Diagnostic only.",
                    },
                    "backend_evidence": {"status": "not_certified", "reason": "no certificate"},
                    "smallest_next_audit": {"tool": "audit_and_propose_fix", "label": "eq:x", "purpose": "regenerate"},
                    "evidence_refs": ["proof_audit_v2:eq:x:obligation_2"],
                }
            ],
        },
        "non_claims": [],
    }

    markdown = render_math_document_rigor_markdown(result)
    concrete = markdown.split("## Concrete Repair Ledger", 1)[1].split("## Diagnostic Abstention Ledger", 1)[0]
    diagnostic = markdown.split("## Diagnostic Abstention Ledger", 1)[1].split("## Gap And Proposal Ledger", 1)[0]

    assert "Replacement LaTeX:" in concrete
    assert "Proof target:" in concrete
    assert "Derivation route:" in concrete
    assert "Why not concrete:" not in concrete
    assert "Why not concrete:" in diagnostic
    assert "Required evidence before repair:" in diagnostic
    assert "Mathematically missing obligations:" in diagnostic
    assert "Possible sufficient assumption sets:" in diagnostic
    assert "How the derivation can work under the assumptions:" in diagnostic
    assert "Add a local review boundary" not in concrete
