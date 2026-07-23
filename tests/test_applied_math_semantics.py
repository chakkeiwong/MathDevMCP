import json
from copy import deepcopy
from pathlib import Path

import pytest

from mathdevmcp.applied_math_audit import audit_applied_math_document
from mathdevmcp.applied_math_semantics import build_semantic_audit, validate_semantic_artifact


ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "tests" / "fixtures" / "applied_math_semantics" / "corpus.json"
CORPUS = json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def _extractor(body: str):
    def extract(_path):
        return {
            "extraction": {
                "parser_outputs": [{
                    "parser_name": "pdftotext",
                    "parser_version": "fixture-1",
                    "parse_status": "ok",
                    "body_text": body,
                }]
            },
            "warnings": [],
        }
    return extract


@pytest.mark.parametrize("case", CORPUS["cases"], ids=lambda case: case["id"])
def test_frozen_semantic_corpus_exact_oracle(tmp_path: Path, case: dict) -> None:
    pdf = tmp_path / f"{case['id']}.pdf"
    pdf.write_bytes(case["id"].encode("ascii"))
    result = audit_applied_math_document(
        [pdf],
        pdf_extractor=_extractor(case["body_text"]),
        response_mode="detailed",
        artifact_root=tmp_path / "artifacts",
    )
    oracle = case["oracle"]
    labels = [item["label"] for item in result["equation_blocks"]]
    roles = {item["label"]: item["role"]["value"] for item in result["semantic_profiles"]}
    hypotheses = [item["kind"] for item in result["relation_hypotheses"]]
    checks = [item["kind"] for item in result["semantic_checks"]]
    semantic_findings = [
        item for item in result["findings"]
        if item.get("semantic_refs")
    ]
    finding_checks = [item["evidence"]["semantic_check"] for item in semantic_findings]

    assert labels == oracle["block_labels"]
    assert roles == oracle["profile_roles"]
    assert hypotheses == oracle["hypotheses"]
    assert checks == oracle["checks"]
    assert finding_checks == oracle["finding_checks"]
    assert result["semantic_validation_errors"] == []
    assert all(item["evidence_chain"]["source_packets"] for item in semantic_findings)
    assert all(item["disposition"] not in oracle["forbidden_dispositions"] for item in result["findings"])


def test_semantic_collections_are_pageable(tmp_path: Path) -> None:
    from mathdevmcp.applied_math_audit import page_applied_math_audit_records

    case = CORPUS["cases"][0]
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"fixture")
    result = audit_applied_math_document(
        [pdf],
        pdf_extractor=_extractor(case["body_text"]),
        response_mode="detailed",
        artifact_root=tmp_path / "artifacts",
    )
    for collection in ("equation_blocks", "semantic_profiles", "relation_hypotheses", "semantic_checks"):
        page = page_applied_math_audit_records(
            result["artifact"]["path"], result["artifact"]["sha256"], collection, limit=1
        )
        assert page["records"]


def test_compact_response_reports_semantic_collection_counts(tmp_path: Path) -> None:
    case = CORPUS["cases"][0]
    pdf = tmp_path / "paper.pdf"
    pdf.write_bytes(b"fixture")

    result = audit_applied_math_document(
        [pdf],
        pdf_extractor=_extractor(case["body_text"]),
        response_mode="compact",
        artifact_root=tmp_path / "artifacts",
    )

    assert result["semantic_summary"] == {
        "equation_block_count": 2,
        "semantic_profile_count": 2,
        "relation_hypothesis_count": 1,
        "semantic_check_count": 1,
        "validation_error_count": 0,
    }


def test_math_fragments_do_not_interrupt_declared_equation_sequence(tmp_path: Path) -> None:
    body = """A new team enters with initial capital based on team-held assets.
Ux = alpha * team-held assets
(M.0)
The following linearized equations describe the team law of motion and starting capital.
Vx = beta * accumulated value
(M.1)
(Qx (zt-1 + kx,t-1) + Vx Ax (zt-1
(M.2)
ux = alpha * team-held assets
(M.3)
Policy and exogenous processes
The linearized response index is
hx = delta * zx
(M.4)
"""
    pdf = tmp_path / "sequence.pdf"
    pdf.write_bytes(b"sequence")

    result = audit_applied_math_document(
        [pdf],
        pdf_extractor=_extractor(body),
        response_mode="detailed",
        artifact_root=tmp_path / "artifacts",
    )

    roles = {item["label"]: item["role"]["value"] for item in result["semantic_profiles"]}
    assert roles["M.3"] == "ownership_linearization"
    assert roles["M.4"] == "linearized_relation"
    hypotheses = [item for item in result["relation_hypotheses"] if item["kind"] == "ownership_preservation"]
    assert len(hypotheses) == 1
    labels_by_profile = {item["id"]: item["label"] for item in result["semantic_profiles"]}
    assert [labels_by_profile[item] for item in hypotheses[0]["profile_refs"]] == ["M.0", "M.3"]


def test_unresolved_linearized_ownership_scope_abstains(tmp_path: Path) -> None:
    body = """A new division starts with a share of assets held by that division.
W_t = rho[P_t K^d_t + S_t B^d_t]
(N.1)
The following equation is the linearized starting value.
rho
(P K^d_t + S B^d_t)
(N.2)
and
w_t =
"""
    pdf = tmp_path / "ownership.pdf"
    pdf.write_bytes(b"ownership")

    result = audit_applied_math_document(
        [pdf],
        pdf_extractor=_extractor(body),
        response_mode="detailed",
        artifact_root=tmp_path / "artifacts",
    )

    checks = {item["kind"]: item for item in result["semantic_checks"]}
    assert checks["ownership_scope_unresolved"]["outcome"] == "abstention"
    assert not [item for item in result["findings"] if item.get("semantic_refs")]


def test_semantic_relations_do_not_cross_source_packets(tmp_path: Path) -> None:
    first = tmp_path / "first.pdf"
    second = tmp_path / "second.pdf"
    first.write_bytes(b"first")
    second.write_bytes(b"second")
    bodies = {
        first: "The level response index is defined by\nH_t = alpha + beta X_t.\n(A.1)",
        second: "Linearizing the response index yields\nh_t = gamma x_t.\n(A.2)",
    }

    result = audit_applied_math_document(
        [first, second],
        pdf_extractor=lambda path: _extractor(bodies[Path(path)])(path),
        response_mode="detailed",
        artifact_root=tmp_path / "artifacts",
    )

    assert not [item for item in result["relation_hypotheses"] if item["kind"] == "level_to_linearized"]
    assert not [item for item in result["findings"] if item.get("semantic_refs")]


def test_distant_unreferenced_equations_do_not_pair(tmp_path: Path) -> None:
    body = "\n".join(
        [
            "The level response index is defined by",
            "H_t = alpha + beta X_t.",
            "(A.1)",
            *[f"This is unrelated prose line number {index}." for index in range(80)],
            "Linearizing the response index yields",
            "h_t = gamma x_t.",
            "(A.2)",
        ]
    )
    pdf = tmp_path / "distant.pdf"
    pdf.write_bytes(b"distant")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert not [item for item in result["relation_hypotheses"] if item["kind"] == "level_to_linearized"]


def test_distant_explicitly_referenced_equations_can_pair(tmp_path: Path) -> None:
    body = "\n".join(
        [
            "The level response index is defined by",
            "H_t = alpha + beta X_t.",
            "(A.1)",
            *[f"This is unrelated prose line number {index}." for index in range(80)],
            "Linearizing the response index in (A.1) yields",
            "h_t = gamma x_t.",
            "(A.2)",
        ]
    )
    pdf = tmp_path / "distant-reference.pdf"
    pdf.write_bytes(b"distant-reference")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    hypotheses = [item for item in result["relation_hypotheses"] if item["kind"] == "level_to_linearized"]
    assert len(hypotheses) == 1
    assert hypotheses[0]["relation_basis"]["basis"] == "explicit_label_cross_reference"


@pytest.mark.parametrize(
    "reference",
    [
        "Unlike the unrelated accounting equation (A.1), we linearize this response index as",
        "See equation (A.1); no mathematical relation is intended for this response index",
    ],
)
def test_negative_or_nonrelational_label_reference_does_not_pair(tmp_path: Path, reference: str) -> None:
    body = "\n".join([
        "The level response index is defined by", "H_t = alpha + beta X_t.", "(A.1)",
        *[f"Unrelated prose {index}." for index in range(80)],
        reference, "h_t = gamma x_t.", "(A.2)",
    ])
    pdf = tmp_path / "negative-reference.pdf"
    pdf.write_bytes(b"negative-reference")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert not [item for item in result["relation_hypotheses"] if item["kind"] == "level_to_linearized"]


@pytest.mark.parametrize(
    "body",
    [
        "The level bond return is\nj_t = alpha + beta x_t.\n(A.1)\nThe unrelated linearized equity return is\nj_t = gamma z_t.\n(A.2)",
        "The customer response index is\nh_t = alpha + beta x_t.\n(A.1)\nThe different employee response index is linearized as\nh_t = gamma z_t.\n(A.2)",
        "A new team starts with team-held assets.\nw_t = rho k_t.\n(A.1)\nThe linearized starting capital of a different division uses aggregate holdings.\nw_t = rho k_t.\n(A.2)",
    ],
)
def test_same_symbol_different_object_does_not_pair(tmp_path: Path, body: str) -> None:
    pdf = tmp_path / "different-object.pdf"
    pdf.write_bytes(b"different-object")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert not result["relation_hypotheses"]
    assert not [item for item in result["findings"] if item.get("semantic_refs")]


def test_equation_block_never_crosses_form_feed(tmp_path: Path) -> None:
    body = "x_t = alpha y_t\n\fCurrent-page prose only.\n(A.1)"
    pdf = tmp_path / "pages.pdf"
    pdf.write_bytes(b"pages")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    block = result["equation_blocks"][0]
    assert block["anchor"]["page"] == 2
    assert "x_t =" not in block["raw_text"]
    assert "x_t =" not in block["formula_text"]


def test_label_before_form_feed_does_not_borrow_next_page_formula(tmp_path: Path) -> None:
    body = "Current-page prose only.\n(A.1)\n\f x_t = alpha y_t"
    pdf = tmp_path / "pages-after.pdf"
    pdf.write_bytes(b"pages-after")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    block = result["equation_blocks"][0]
    assert block["anchor"]["page"] == 1
    assert "x_t =" not in block["formula_text"]


@pytest.mark.parametrize(
    "movement",
    ["m_t = z_t - r_t-1", "m_t + r_t-1 = z_t"],
)
def test_equivalent_normalization_layouts_do_not_emit_sign_tension(tmp_path: Path, movement: str) -> None:
    body = f"Acknowledging that M_t/M_t-1 R_t-1 = 1, we linearize the pricing kernel as\n{movement}.\n(B.1)"
    pdf = tmp_path / "normalization.pdf"
    pdf.write_bytes(b"normalization")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert "normalization_sign_tension" not in [item["kind"] for item in result["semantic_checks"]]
    assert not [item for item in result["findings"] if item.get("semantic_refs")]


def test_normalization_timing_tension_is_term_specific(tmp_path: Path) -> None:
    body = "Acknowledging that M_t/M_t-1 R_t-1 = 1, we linearize the pricing kernel as\nm_t = - r_t + z_t.\n(B.2)"
    pdf = tmp_path / "normalization-timing.pdf"
    pdf.write_bytes(b"normalization-timing")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert "normalization_timing_tension" in [item["kind"] for item in result["semantic_checks"]]


def test_multiple_return_movements_force_normalization_abstention(tmp_path: Path) -> None:
    body = "Acknowledging that M_t/M_t-1 R_t-1 = 1, we linearize the pricing kernel as\nm_t = - r_t-1 + r_t + z_t.\n(B.3)"
    pdf = tmp_path / "normalization-ambiguous.pdf"
    pdf.write_bytes(b"normalization-ambiguous")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert "normalization_movement_unresolved" in [item["kind"] for item in result["semantic_checks"]]
    assert not [item for item in result["findings"] if item.get("semantic_refs")]


@pytest.mark.parametrize(
    "movement",
    ["m_t = z_t - (r_t-1)", "m_t = z_t - 1*r_t-1", "m_t = z_t - (1/2) * r_t-1"],
)
def test_parenthesized_or_scalar_negative_return_is_not_positive(tmp_path: Path, movement: str) -> None:
    body = f"Acknowledging that M_t/M_t-1 R_t-1 = 1, we linearize as\n{movement}.\n(B.4)"
    pdf = tmp_path / "normalization-scalar.pdf"
    pdf.write_bytes(b"normalization-scalar")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert "normalization_sign_tension" not in [item["kind"] for item in result["semantic_checks"]]


@pytest.mark.parametrize(
    "normalization",
    ["M_t/M_t-1 R^a_t-1 R^b_t = 1", "M_t/M_t-1 R = 1"],
)
def test_unresolved_normalization_time_abstains(tmp_path: Path, normalization: str) -> None:
    body = f"Acknowledging that {normalization}, we linearize as\nm_t = - r^a_t-1 + z_t.\n(B.5)"
    pdf = tmp_path / "normalization-time-unresolved.pdf"
    pdf.write_bytes(b"normalization-time-unresolved")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert "normalization_timing_unresolved" in [item["kind"] for item in result["semantic_checks"]]
    assert "no_semantic_tension_nominated" not in [item["kind"] for item in result["semantic_checks"]]


def test_integer_timing_shifts_are_not_truncated(tmp_path: Path) -> None:
    body = "Acknowledging that M_t/M_t-2 R_t-2 = 1, we linearize as\nm_t = - r_t-2 + z_t.\n(B.6)"
    pdf = tmp_path / "normalization-lag-two.pdf"
    pdf.write_bytes(b"normalization-lag-two")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    checks = [item["kind"] for item in result["semantic_checks"]]
    assert "normalization_timing_tension" not in checks
    assert "normalization_timing_unresolved" not in checks
    assert "no_semantic_tension_nominated" in checks


@pytest.mark.parametrize(
    "return_token",
    ["r_t-", "r_t-1.5", "r_t-2a", "r_{t-2x}", "r_{t-}", "r_{t-1.5}", "r_t--2", "r_t+-2"],
)
def test_malformed_return_dates_abstain_without_prefix_matching(tmp_path: Path, return_token: str) -> None:
    body = f"Acknowledging that M_t/M_t-2x R_t-2x = 1, we linearize as\nm_t = - {return_token} + z_t.\n(B.7)"
    pdf = tmp_path / "normalization-malformed-date.pdf"
    pdf.write_bytes(b"normalization-malformed-date")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    checks = [item["kind"] for item in result["semantic_checks"]]
    assert "no_semantic_tension_nominated" not in checks
    assert "normalization_sign_tension" not in checks
    assert "normalization_movement_unresolved" in checks


def test_incidental_coefficient_overlap_is_not_equivalence(tmp_path: Path) -> None:
    body = """The level response index is defined by
H_t = alpha + beta X_t.
(D.1)
Linearizing the response index yields
h_t = alpha + gamma x_t.
(D.2)"""
    pdf = tmp_path / "coefficients.pdf"
    pdf.write_bytes(b"coefficients")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert "coefficient_family_mismatch" in [item["kind"] for item in result["semantic_checks"]]


def test_conflicting_ownership_scope_abstains(tmp_path: Path) -> None:
    body = """A new unit starts with aggregate holdings and assets held by the unit.
W_t = rho K_t.
(E.1)
The linearized starting value uses aggregate holdings and unit-held assets.
w_t = rho k_t.
(E.2)"""
    pdf = tmp_path / "ownership-conflict.pdf"
    pdf.write_bytes(b"ownership-conflict")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert "ownership_scope_unresolved" in [item["kind"] for item in result["semantic_checks"]]
    assert not [item for item in result["findings"] if item.get("semantic_refs")]


def test_dropped_ownership_qualifier_does_not_count_as_preservation(tmp_path: Path) -> None:
    body = """A new unit starts with assets held by the unit.
W_t = rho[P_t K^u_t + S_t B^u_t].
(F.1)
The linearized starting value is
w_t = rho(P_t K_t + S_t B_t).
(F.2)"""
    pdf = tmp_path / "ownership-dropped.pdf"
    pdf.write_bytes(b"ownership-dropped")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert "ownership_scope_unresolved" in [item["kind"] for item in result["semantic_checks"]]
    assert "ownership_scope_preserved" not in [item["kind"] for item in result["semantic_checks"]]


def test_specific_owner_does_not_pair_with_unresolved_different_owner(tmp_path: Path) -> None:
    body = """A new team starts with team-held assets.
w_t = rho k_t.
(G.1)
The linearized starting capital of another division uses aggregate holdings.
w_t = rho k_t.
(G.2)"""
    pdf = tmp_path / "ownership-different-object.pdf"
    pdf.write_bytes(b"ownership-different-object")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    checks = [item["kind"] for item in result["semantic_checks"]]
    assert "ownership_scope_mismatch" not in checks
    assert "ambiguous_relation_candidates" in checks
    assert not [item for item in result["findings"] if item.get("semantic_refs")]


def test_duplicate_labels_in_one_source_fail_semantic_validation(tmp_path: Path) -> None:
    body = "x_t = alpha y_t\n(A.1)\nz_t = beta y_t\n(A.1)"
    pdf = tmp_path / "duplicate.pdf"
    pdf.write_bytes(b"duplicate")
    result = audit_applied_math_document(
        [pdf], pdf_extractor=_extractor(body), response_mode="detailed", artifact_root=tmp_path / "artifacts"
    )
    assert any("duplicate labels" in item for item in result["semantic_validation_errors"])
    assert not [item for item in result["findings"] if item.get("semantic_refs")]


def _semantic_payload(body: str = CORPUS["cases"][0]["body_text"]):
    packet = {
        "id": "packet:source:test",
        "kind": "source_text",
        "raw_text": body,
        "authentication_state": "parser_candidate_only",
        "anchor": {"source_id": "test", "path": "test.pdf", "sha256": "a" * 64},
    }
    return build_semantic_audit([packet]), [packet]


@pytest.mark.parametrize(
    "mutate,expected",
    [
        (lambda value: value["relation_hypotheses"][0]["block_refs"].append("block:missing"), "block references"),
        (lambda value: value["relation_hypotheses"][0]["source_packet_refs"].append("packet:missing"), "source packet"),
        (lambda value: value["semantic_findings"][0]["evidence_chain"]["source_packets"].append("packet:missing"), "packet references"),
        (lambda value: value["semantic_findings"][0]["evidence_chain"].update({"check": "semantic-check:missing"}), "evidence chain"),
        (lambda value: value["semantic_profiles"][0].update({"authentication_state": "source_authenticated"}), "inheritance"),
        (lambda value: value["equation_blocks"][0]["anchor"].update({"sha256": "b" * 64}), "source anchor"),
    ],
)
def test_semantic_validator_rejects_corrupted_graph(mutate, expected: str) -> None:
    payload, packets = _semantic_payload()
    corrupt = deepcopy(payload)
    mutate(corrupt)
    errors = validate_semantic_artifact(corrupt, packets)
    assert any(expected in item for item in errors)


def test_semantic_builder_withholds_findings_on_validation_failure(monkeypatch) -> None:
    import mathdevmcp.applied_math_semantics as semantics

    monkeypatch.setattr(semantics, "validate_semantic_artifact", lambda value, packets: ["corrupt"])
    payload, _ = _semantic_payload()
    assert payload["validation_errors"] == ["corrupt"]
    assert payload["semantic_findings"] == []


@pytest.mark.parametrize(
    "mutate",
    [
        lambda value: value["semantic_profiles"][0]["role"].update({"value": "linearized_relation"}),
        lambda value: value["semantic_profiles"][0]["material_coefficient_families"].update({"value": ["gamma"]}),
        lambda value: value["relation_hypotheses"][0].update({"relation_basis": {"basis": "explicit_label_cross_reference", "source_packet_ref": "missing", "page_distance": 999, "line_distance": 999}}),
        lambda value: value["semantic_checks"][0].update({"outcome": "no_tension"}),
        lambda value: value["semantic_findings"][0]["evidence"].update({"semantic_check": "leading_sign_mismatch"}),
        lambda value: value["semantic_findings"][0]["evidence_chain"].update({"result": {"disposition": "confirmed_defect", "semantic_outcome": "no_tension"}}),
    ],
)
def test_semantic_validator_rejects_semantic_value_tampering(mutate) -> None:
    payload, packets = _semantic_payload()
    corrupt = deepcopy(payload)
    mutate(corrupt)
    assert any("canonical reconstruction" in item for item in validate_semantic_artifact(corrupt, packets))
