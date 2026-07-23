from pathlib import Path

import pytest

from mathdevmcp.applied_math_audit import audit_applied_math_document, page_applied_math_audit_records
from mathdevmcp.applied_math_ir import (
    APPLIED_MATH_IR_SCHEMA,
    build_pdf_evidence_packets,
    validate_claim_ir,
    verify_independent_transcription,
)
from mathdevmcp.applied_math_adapters import AdapterOutcome, discover_local_source_package, run_dynare_source_adapter
from mathdevmcp.applied_math_formalization import formalize_equality
from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools


def test_applied_math_audit_has_general_coverage_and_artifact(tmp_path: Path) -> None:
    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"""\section{Model}
        We estimate a causal treatment effect under an identification assumption.
        \begin{equation}\label{eq:objective}
        V_t = \max E_t[\beta V_{t+1}]\end{equation}
        The posterior uses 200 draws and the appendix gives additional equations.
        """,
        encoding="utf-8",
    )
    result = audit_applied_math_document([tex], response_mode="detailed", artifact_root=tmp_path / "artifacts")
    assert result["metadata"]["contract"] == "applied_math_audit"
    assert result["coverage"]["all_obligations_have_disposition"] is True
    assert result["artifact"]["bytes"] > 0
    assert result["source"]["records"][0]["structured_objects"]["equations"][0]["id"] == "eq:objective"
    assert any(item["family"] == "identification_causality" and item["status"] == "selected" for item in result["obligations"])
    assert result["claim_ir"]["schema"] == APPLIED_MATH_IR_SCHEMA
    assert result["claim_ir_validation_errors"] == []
    assert any(item["kind"] == "equation" for item in result["evidence_packets"])


def test_applied_math_audit_promotes_only_literal_source_conflicts(tmp_path: Path) -> None:
    tex = tmp_path / "paper.tex"
    tex.write_text(
        "The appendix states 500 x 200 = 10,000 draws. "
        "The full set of equations is available on github. "
        "The steady state is zero and the variable is a log-deviation. "
        "The figure reports confidence intervals and credible sets.",
        encoding="utf-8",
    )
    result = audit_applied_math_document([tex], response_mode="detailed", artifact_root=tmp_path / "artifacts")
    assert any(item["disposition"] == "confirmed_defect" for item in result["findings"])
    assert {item["family"] for item in result["findings"]} >= {
        "algorithm_numerics",
        "document_completeness",
        "approximation_linearization",
        "probability_statistics",
    }
    assert result["coverage"]["disposition_counts"]["confirmed_defect"] == 1
    assert all(item.get("evidence_chain") for item in result["findings"])


def test_pdf_packets_preserve_page_identity_and_empty_pages() -> None:
    packets = build_pdf_evidence_packets(
        source_id="source-a",
        path="paper.pdf",
        sha256="a" * 64,
        body_text="first page\n500 x 200 = 10,000\fsecond page without equation",
        parser_name="pdftotext",
        parser_version="24",
    )
    pages = [item for item in packets if item["kind"] == "page"]
    assert [item["anchor"]["page"] for item in pages] == [1, 2]
    candidate = next(item for item in packets if item["kind"] == "equation_candidate")
    assert candidate["anchor"]["page"] == 1
    assert candidate["extraction"]["manual_visual_review_required"] is True

    bbox_packets = build_pdf_evidence_packets(
        source_id="source-b",
        path="paper.pdf",
        sha256="b" * 64,
        body_text="x = y",
        parser_name="pdftotext-bbox",
        parser_version="24",
    )
    bbox_candidate = next(item for item in bbox_packets if item["kind"] == "equation_candidate")
    assert bbox_candidate["authentication_state"] == "parser_candidate_only"
    assert bbox_candidate["extraction"]["visual_crop"] is None


def test_claim_ir_validation_rejects_unresolved_node_reference() -> None:
    errors = validate_claim_ir(
        {
            "schema": APPLIED_MATH_IR_SCHEMA,
            "version": "1.0",
            "nodes": [{"id": "object:a"}],
            "edges": [
                {
                    "source": "object:a",
                    "target": "object:missing",
                    "status": "explicit",
                    "evidence_refs": [],
                }
            ],
        }
    )
    assert any("unknown node" in error for error in errors)


def test_local_source_discovery_is_digest_bound_and_non_authoritative(tmp_path: Path) -> None:
    paper = tmp_path / "paper.tex"
    paper.write_text("paper", encoding="utf-8")
    (tmp_path / "model.mod").write_text("var y;", encoding="utf-8")
    result = discover_local_source_package(paper)
    assert result["status"] == "candidates_found"
    candidate = result["candidates"][0]
    assert candidate["sha256"]
    assert "authoritative" in result["non_claim"]


def test_local_source_discovery_does_not_follow_symlinks(tmp_path: Path) -> None:
    paper = tmp_path / "paper.tex"
    paper.write_text("paper", encoding="utf-8")
    outside = tmp_path.parent / "outside-secret.yaml"
    outside.write_text("secret", encoding="utf-8")
    (tmp_path / "linked.yaml").symlink_to(outside)
    result = discover_local_source_package(paper)
    assert all(item["path"] != str(tmp_path / "linked.yaml") for item in result["candidates"])


def test_artifact_identity_includes_all_sources(tmp_path: Path) -> None:
    first = tmp_path / "first.tex"
    second = tmp_path / "second.tex"
    third = tmp_path / "third.tex"
    first.write_text("first", encoding="utf-8")
    second.write_text("second", encoding="utf-8")
    third.write_text("third", encoding="utf-8")
    one = audit_applied_math_document([first, second], artifact_root=tmp_path / "artifacts")
    two = audit_applied_math_document([first, third], artifact_root=tmp_path / "artifacts")
    assert one["artifact"]["path"] != two["artifact"]["path"]


def test_changed_parser_output_cannot_overwrite_prior_artifact(tmp_path: Path) -> None:
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"fixture")
    bodies = iter(("x_t = alpha y_t\n(A.1)", "x_t = gamma y_t\n(A.1)"))

    def extractor(_path):
        return {
            "extraction": {
                "parser_outputs": [{
                    "parser_name": "pdftotext",
                    "parser_version": "fixture",
                    "parse_status": "ok",
                    "body_text": next(bodies),
                }]
            },
            "warnings": [],
        }

    first = audit_applied_math_document([pdf], pdf_extractor=extractor, artifact_root=tmp_path / "artifacts")
    first_bytes = Path(first["artifact"]["path"]).read_bytes()
    second = audit_applied_math_document([pdf], pdf_extractor=extractor, artifact_root=tmp_path / "artifacts")

    assert first["artifact"]["path"] != second["artifact"]["path"]
    assert first["artifact"]["sha256"] != second["artifact"]["sha256"]
    assert Path(first["artifact"]["path"]).read_bytes() == first_bytes
    assert page_applied_math_audit_records(
        first["artifact"]["path"], first["artifact"]["sha256"], "equation_blocks"
    )["status"] == "resolved"


def test_dynare_adapter_is_typed_and_records_failures(tmp_path: Path) -> None:
    model = tmp_path / "model.mod"
    model.write_text("var y; model; y = y; end;", encoding="utf-8")
    (tmp_path / "src" / "dynaremcp").mkdir(parents=True)

    def runner(command, env, timeout):
        assert command[3] in {"analyze-model-source", "extract-symbol-table", "list-equations", "inspect-timing"}
        if command[3] in {"extract-symbol-table", "list-equations"}:
            assert command[4] == "--model-path"
        return AdapterOutcome(tuple(command), 1, "", "unavailable", 0.001)

    result = run_dynare_source_adapter(model, dynare_root=tmp_path, runner=runner)
    assert result["status"] == "completed_with_abstentions"
    assert len(result["operations"]) == 4
    assert all(item["input"]["sha256"] for item in result["operations"])


def test_compact_artifact_preserves_full_claim_ir(tmp_path: Path) -> None:
    tex = tmp_path / "paper.tex"
    tex.write_text(
        r"\begin{equation}\label{eq:a}a=b\end{equation}", encoding="utf-8"
    )
    result = audit_applied_math_document(
        [tex], response_mode="compact", artifact_root=tmp_path / "artifacts"
    )
    assert "claim_ir" not in result
    artifact = Path(result["artifact"]["path"])
    import json

    detailed = json.loads(artifact.read_text(encoding="utf-8"))
    assert detailed["claim_ir"]["schema"] == APPLIED_MATH_IR_SCHEMA
    assert detailed["claim_ir_validation_errors"] == []
    assert detailed["evidence_packets"]
    page = page_applied_math_audit_records(
        artifact, result["artifact"]["sha256"], "claim_ir_nodes", limit=1
    )
    assert page["metadata"]["contract"] == "applied_math_audit_record_page"
    assert page["records"][0]["record_sha256"]


def test_applied_math_paging_rejects_tampering_and_unknown_collection(tmp_path: Path) -> None:
    tex = tmp_path / "paper.tex"
    tex.write_text("500 x 200 = 10,000", encoding="utf-8")
    result = audit_applied_math_document([tex], artifact_root=tmp_path / "artifacts")
    with pytest.raises(ValueError, match="collection"):
        page_applied_math_audit_records(result["artifact"]["path"], result["artifact"]["sha256"], "raw")
    with pytest.raises(ValueError, match="SHA-256"):
        page_applied_math_audit_records(result["artifact"]["path"], "0" * 64, "findings")


def test_generic_relationship_candidates_have_unique_ids_and_explicit_limits(tmp_path: Path) -> None:
    pdf_text = (
        "The level long bond return uses price and bonds.\n"
        "R = (xi + kappa Q) / Qlag. (C.1)\f"
        "Linearizing the long bond return and price relation yields\n"
        "r + qlag = kappa q. (C.2)"
    )

    def extractor(path):
        return {
            "extraction": {
                "parser_outputs": [
                    {
                        "parser_name": "pdftotext",
                        "parser_version": "test",
                        "parse_status": "ok",
                        "body_text": pdf_text,
                    }
                ]
            },
            "warnings": [],
        }

    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"fixture")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=extractor, response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    ids = [item["id"] for item in result["findings"]]
    assert len(ids) == len(set(ids))
    assert all(edge["status"] == "inferred" for edge in result["claim_ir"]["edges"])


def test_applied_math_audit_marks_dynare_as_optional_and_not_applicable(tmp_path: Path) -> None:
    tex = tmp_path / "marketing.tex"
    tex.write_text("A marketing experiment estimates a treatment effect.", encoding="utf-8")
    py = tmp_path / "analysis.py"
    py.write_text("effect = 1", encoding="utf-8")
    result = audit_applied_math_document([tex], code_paths=[py], artifact_root=tmp_path / "artifacts")
    assert result["routes"][0]["specialist"] == "DynareMCP"
    assert result["routes"][0]["status"] == "not_applicable"
    assert any(item["code"] == "dynare_optional_adapter" for item in result["non_claims"])


def test_applied_math_audit_accepts_dynare_code_as_optional_route(tmp_path: Path) -> None:
    tex = tmp_path / "model.tex"
    tex.write_text("\u000a linearized model with steady state and timing", encoding="utf-8")
    mod = tmp_path / "model.mod"
    mod.write_text("var y; model; y = y; end;", encoding="utf-8")
    result = audit_applied_math_document([tex], code_paths=[mod], artifact_root=tmp_path / "artifacts")
    assert result["routes"][0]["applicable"] is True
    assert "inspect_timing" in result["routes"][0]["operations"]


def test_applied_math_audit_rejects_invalid_sources() -> None:
    with pytest.raises(ValueError, match="non-empty list"):
        audit_applied_math_document([])
    with pytest.raises(ValueError, match="non-empty list"):
        audit_applied_math_document("paper.tex")


def test_applied_math_audit_is_exposed_through_facade() -> None:
    names = {item["name"] for item in list_mcp_tools()}
    assert "audit_applied_math_document" in names
    result = call_mcp_tool("audit_applied_math_document", {"sources": [__file__], "artifact_root": "/tmp/mathdevmcp-applied-test"})
    assert result["ok"] is True
    assert result["metadata"]["contract"] == "applied_math_audit"


def test_formalization_requires_authenticated_source_and_explicit_relation() -> None:
    parser_only = formalize_equality(
        "x + 1", "x + 2", source_state="parser_candidate_only", source_relation_explicit=True
    )
    assert parser_only["status"] == "backend_abstention"
    assert parser_only["reason_code"] == "unauthenticated_transcription"

    implicit = formalize_equality(
        "x + 1", "x + 2", source_state="source_authenticated", source_relation_explicit=False
    )
    assert implicit["status"] == "supported_tension"
    assert implicit["reason_code"] == "relation_not_explicit_in_source"


def test_formalization_closed_target_and_rejection_limits() -> None:
    mismatch = formalize_equality(
        "1 + 1", "3", source_state="source_authenticated", source_relation_explicit=True
    )
    assert mismatch["status"] == "confirmed_defect"
    assert mismatch["backend"] == "sympy"
    unsafe = formalize_equality(
        "__import__('os')", "1", source_state="source_authenticated", source_relation_explicit=True
    )
    assert unsafe["status"] == "backend_abstention"
    assert unsafe["reason_code"] == "formalization_rejected"
    huge = formalize_equality(
        "9**999", "1", source_state="source_authenticated", source_relation_explicit=True
    )
    assert huge["status"] == "backend_abstention"


def test_independent_transcription_requires_digest_and_independent_agreement() -> None:
    from hashlib import sha256

    transcription = "x + 1 = x + 2"
    digest = sha256(transcription.encode()).hexdigest()
    accepted = verify_independent_transcription(
        reviewer_id="reviewer",
        extractor_id="extractor",
        source_anchor={"sha256": "a" * 64, "region_sha256": "b" * 64, "page": 1},
        transcription=transcription,
        transcription_sha256=digest,
        decision="agree",
        review_record={
            "record_id": "review-1",
            "reviewer_id": "reviewer",
            "extractor_id": "extractor",
            "source_anchor": {"sha256": "a" * 64, "region_sha256": "b" * 64, "page": 1},
            "transcription_sha256": digest,
            "decision": "agree",
        },
    )
    assert accepted["state"] == "independently_verified_transcription"
    rejected = verify_independent_transcription(
        reviewer_id="extractor",
        extractor_id="extractor",
        source_anchor={"sha256": "a" * 64, "region_sha256": "b" * 64, "page": 1},
        transcription=transcription,
        transcription_sha256=digest,
        decision="agree",
        review_record={
            "record_id": "review-2",
            "reviewer_id": "extractor",
            "extractor_id": "extractor",
            "source_anchor": {"sha256": "a" * 64, "region_sha256": "b" * 64, "page": 1},
            "transcription_sha256": digest,
            "decision": "agree",
        },
    )
    assert rejected["state"] == "parser_candidate_only"


def test_orchestrator_wires_closed_formalization_to_bound_source_packet(tmp_path: Path) -> None:
    tex = tmp_path / "closed.tex"
    tex.write_text("The displayed arithmetic is 500 x 200 = 10,000.", encoding="utf-8")
    result = audit_applied_math_document([tex], response_mode="detailed", artifact_root=tmp_path / "artifacts")
    finding = next(item for item in result["findings"] if item["family"] == "algorithm_numerics")
    assert finding["disposition"] == "confirmed_defect"
    assert finding["evidence_chain"]["source_packets"]
    assert finding["diagnostics"]["formalization"]["status"] == "confirmed_defect"
    assert finding["diagnostics"]["formalization"]["backend"] == "sympy"
    assert result["claim_ir_validation_errors"] == []


def test_pdf_parser_arithmetic_cannot_be_promoted_to_confirmed_defect(tmp_path: Path) -> None:
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"pdf-fixture")

    def extractor(_path):
        return {
            "extraction": {
                "parser_outputs": [{
                    "parser_name": "pdftotext",
                    "parser_version": "test",
                    "parse_status": "ok",
                    "body_text": "500 x 200 = 10,000",
                }]
            },
            "warnings": [],
        }

    result = audit_applied_math_document(
        [pdf], pdf_extractor=extractor, response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    arithmetic = next(item for item in result["findings"] if item["family"] == "algorithm_numerics")
    assert arithmetic["disposition"] == "supported_tension"
    assert arithmetic["diagnostics"]["formalization"]["reason_code"] == "unauthenticated_transcription"


def test_formalization_abstains_on_unresolved_denominator_domain() -> None:
    result = formalize_equality(
        "x / x", "1", source_state="source_authenticated", source_relation_explicit=True
    )
    assert result["status"] == "backend_abstention"
    assert result["reason_code"] == "domain_conditions_required"
