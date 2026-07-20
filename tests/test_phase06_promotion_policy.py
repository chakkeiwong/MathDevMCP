from __future__ import annotations

from copy import deepcopy
import hashlib
import json

import pytest

import mathdevmcp.document_derivation_tree as document_tree
from mathdevmcp.evidence_manifest import canonical_json_bytes, content_digest
from mathdevmcp.external_adapter_contract import (
    reader_verified_claim_evidence_record,
    reverify_registered_adapter_claim_evidence,
)
from mathdevmcp.failure_ledgers import build_ledgers, build_status_entry
from mathdevmcp.promotion_policy import (
    build_test_only_aggregate_gate,
    evaluate_phase06_promotion,
    verify_phase06_promotion_decision,
)

from tests.test_claim_evidence_normalization import _sage_fixture


SOURCE_BYTES = b"(x + 1)**2 = x**2 + 2*x + 1"
SOURCE_TARGET = SOURCE_BYTES.decode("ascii")


def _fixture(tmp_path, *, mode="disabled"):
    tmp_path.mkdir(parents=True, exist_ok=True)
    native = _sage_fixture(tmp_path)
    normalized = reverify_registered_adapter_claim_evidence(
        adapter_result=native["adapter_result"],
        p04_branch=native["branch"],
        p04_request=native["p04_request"],
        p04_result=native["p04_result"],
    )
    source_digest = hashlib.sha256(SOURCE_BYTES).hexdigest()
    owned_span = {
        "file": "synthetic/source.tex",
        "label": "eq:sage",
        "start_byte": 0,
        "end_byte": len(SOURCE_BYTES),
    }
    assumption = native["branch"]["typed_assumptions"][0]
    assumption_digest = native["branch"]["typed_assumption_digests"][0]
    source = {
        "schema_version": "p06_current_source@1",
        "logical_id": "synthetic/source.tex",
        "bytes": SOURCE_BYTES,
        "digest": source_digest,
        "label": "eq:sage",
        "owned_spans": [owned_span],
        "obligation_digest": native["branch"]["obligation_digest"],
        "normalized_target": native["branch"]["target"],
        "assumption_support": [
            {
                "assumption_id": assumption["id"],
                "assumption_digest": assumption_digest,
                "support_status": "source_supported",
                "source_refs": [
                    {
                        **owned_span,
                        "source_digest": source_digest,
                    }
                ],
                "candidate_edit_statement": None,
            }
        ],
    }
    extraction = {
        "schema_version": "p06_extraction_binding@1",
        "state": "validated",
        "adapter_eligible": True,
        "ambiguity_ids": [],
        "source": {
            "digest": source_digest,
            "label": "eq:sage",
            "owned_spans": [owned_span],
        },
    }
    edit_text = SOURCE_TARGET
    edit = {
        "schema_version": "p06_candidate_edit@1",
        "kind": "replace_exact_target",
        "text": edit_text,
        "edit_digest": hashlib.sha256(edit_text.encode("utf-8")).hexdigest(),
        "source_digest": source_digest,
        "label": "eq:sage",
        "placement": owned_span,
        "claim_scope": {"kind": "exact_target", "target": native["branch"]["target"]},
    }
    gate = (
        build_test_only_aggregate_gate(
            phase_decision_digests=[f"{index + 1:x}" * 64 for index in range(7)]
        )
        if mode == "experimental_exact_manifest"
        else None
    )
    policy = {
        "schema_version": "p06_promotion_policy_input@1",
        "publication_mode": mode,
        "publication_enabled": mode == "experimental_exact_manifest",
        "explicit_mode": mode == "experimental_exact_manifest",
        "certifying_backend_roles": ["scoped_specialist_certificate"],
        "accepted_input_classes": ["exact_univariate_polynomial_identity_over_QQ"],
        "compact_omission_veto_ids": [],
        "test_only_aggregate_gate": gate,
        "allow_test_only_experimental_policy": mode == "experimental_exact_manifest",
    }
    return {
        "normalized_claim_evidence": normalized,
        "current_source": source,
        "extraction": extraction,
        "branch": native["branch"],
        "candidate_edit": edit,
        "ledgers": build_ledgers([]),
        "policy": policy,
    }


def _evaluate(fixture):
    return evaluate_phase06_promotion(**fixture)


def _replace_with_redigested_normalized_record(fixture, mutate):
    record = reader_verified_claim_evidence_record(
        fixture["normalized_claim_evidence"]
    )
    mutate(record)
    record["normalization_digest"] = content_digest(
        {key: record[key] for key in record if key != "normalization_digest"}
    )
    fixture["normalized_claim_evidence"] = record


def _redigest_decision(decision):
    decision["promotion_decision_digest"] = content_digest(
        {
            key: decision[key]
            for key in decision
            if key not in {"promotion_decision_digest", "reconstruction"}
        }
    )
    decision["reconstruction"] = {
        "algorithm": "canonical_sha256_excluding_digest_and_reconstruction",
        "recomputed_digest": decision["promotion_decision_digest"],
        "matches": True,
    }
    return decision


def test_fully_bound_positive_is_exact_eligible_but_disabled_is_report_only(tmp_path):
    fixture = _fixture(tmp_path)
    before = deepcopy(fixture)
    decision = _evaluate(fixture)
    assert decision["claim_eligibility"] == "exact_manifest_eligible"
    assert decision["decision"] == "publish_evidence_report"
    assert decision["publication_enabled"] is False
    assert decision["applicable_repair"] is None
    assert decision["vetoes"] == []
    assert [item["id"] for item in decision["invariant_results"]][-1] == "deterministic_decision_reconstruction"
    assert all(item["passed"] for item in decision["invariant_results"][:10])
    assert decision["invariant_results"][10]["passed"] is False
    assert decision["invariant_results"][11]["passed"] is True
    assert verify_phase06_promotion_decision(decision) == decision
    assert fixture == before


@pytest.mark.parametrize(
    ("invariant_id", "mutate"),
    [
        ("current_source_binding", lambda value: value["current_source"].update(bytes=b"changed")),
        ("validated_unambiguous_extraction", lambda value: value["extraction"].update(state="ambiguous", adapter_eligible=False, ambiguity_ids=["a1"])),
        ("exact_branch_binding", lambda value: _replace_with_redigested_normalized_record(value, lambda record: record["branch"].update(id="other"))),
        ("complete_assumption_support_and_encoding", lambda value: value["current_source"].update(assumption_support=[])),
        ("certifying_backend_role_and_input_class", lambda value: value["policy"].update(certifying_backend_roles=["other"])),
        ("actual_non_test_backend_execution", lambda value: _replace_with_redigested_normalized_record(value, lambda record: record["execution"].update(live_tool_executed=False))),
        ("registered_reader_evidence_integrity", lambda value: _replace_with_redigested_normalized_record(value, lambda record: record.update(manifest_family="caller_defined"))),
        ("scoped_terminal_outcome", lambda value: _replace_with_redigested_normalized_record(value, lambda record: record["outcome"].update(placeholder_free=False))),
        ("candidate_edit_binding_and_scope", lambda value: value["candidate_edit"].update(text="different")),
        ("empty_typed_veto_sets", lambda value: value["policy"].update(compact_omission_veto_ids=["omitted_action"])),
    ],
)
def test_one_negative_mutation_per_claim_invariant_is_ineligible(tmp_path, invariant_id, mutate):
    fixture = _fixture(tmp_path)
    mutate(fixture)
    decision = _evaluate(fixture)
    by_id = {item["id"]: item for item in decision["invariant_results"]}
    assert by_id[invariant_id]["passed"] is False
    assert decision["claim_eligibility"] == "ineligible"
    assert decision["publication_enabled"] is False
    assert decision["applicable_repair"] is None


def test_engineering_evidence_and_mathematical_ledgers_each_veto(tmp_path):
    for status, evidence_state, expected_field in (
        ("adapter_error", None, "engineering_error_ids"),
        ("certified", "manifest_mismatch", "evidence_integrity_error_ids"),
        ("missing_assumption", None, "mathematical_veto_ids"),
    ):
        fixture = _fixture(tmp_path / expected_field)
        scope = {
            "obligation_id": fixture["branch"]["obligation_digest"],
            "target": fixture["branch"]["target"],
            "candidate_conclusion": fixture["branch"]["target"],
            "branch_ids": [fixture["branch"]["id"]],
            "source_spans": [fixture["current_source"]["owned_spans"][0]],
            "closed_blocker_scope": [status],
        }
        entry = build_status_entry(
            status=status,
            evidence_state=evidence_state,
            origin_id=f"origin-{expected_field}",
            target_id="eq:sage",
            scope=scope,
            problem="Synthetic veto.",
            why="Exercise typed veto separation.",
        )
        fixture["ledgers"] = build_ledgers([entry])
        decision = _evaluate(fixture)
        assert decision[expected_field] == [entry["entry_id"]]
        assert decision["claim_eligibility"] == "ineligible"


def test_publication_flag_cannot_override_failed_invariant(tmp_path):
    fixture = _fixture(tmp_path, mode="experimental_exact_manifest")
    fixture["candidate_edit"]["text"] = "different"
    decision = _evaluate(fixture)
    assert decision["invariant_results"][10]["passed"] is True
    assert decision["claim_eligibility"] == "ineligible"
    assert decision["decision"] != "eligible_experimental_repair"
    assert decision["publication_enabled"] is True
    assert decision["applicable_repair"] is None


def test_toggle_mode_does_not_change_claim_eligibility(tmp_path):
    disabled = _evaluate(_fixture(tmp_path / "disabled"))
    experimental = _evaluate(_fixture(tmp_path / "experimental", mode="experimental_exact_manifest"))
    assert disabled["claim_eligibility"] == experimental["claim_eligibility"] == "exact_manifest_eligible"
    assert disabled["decision"] == "publish_evidence_report"
    assert experimental["decision"] == "eligible_experimental_repair"
    assert experimental["publication_enabled"] is True
    assert experimental["applicable_repair"] is None


def test_publication_mode_and_runtime_flag_are_independent(tmp_path):
    fixture = _fixture(tmp_path, mode="experimental_exact_manifest")
    fixture["policy"]["publication_enabled"] = False
    decision = _evaluate(fixture)

    assert decision["publication_mode"] == "experimental_exact_manifest"
    assert decision["publication_enabled"] is False
    assert decision["claim_eligibility"] == "exact_manifest_eligible"
    assert decision["invariant_results"][10]["passed"] is False
    assert decision["decision"] == "publish_evidence_report"
    assert verify_phase06_promotion_decision(decision) == decision


def test_redigested_normalized_json_has_no_reader_authority(tmp_path):
    fixture = _fixture(tmp_path)
    _replace_with_redigested_normalized_record(fixture, lambda record: None)
    decision = _evaluate(fixture)

    assert decision["claim_eligibility"] == "ineligible"
    assert decision["invariant_results"][0]["passed"] is False
    assert decision["invariant_results"][3]["passed"] is False
    assert decision["invariant_results"][6]["passed"] is False
    assert decision["decision"] == "reject"


def test_test_only_aggregate_gate_has_no_program_authority(tmp_path):
    fixture = _fixture(tmp_path, mode="experimental_exact_manifest")
    gate = fixture["policy"]["test_only_aggregate_gate"]
    assert gate["program_authority"] is False
    forged = deepcopy(fixture)
    forged["policy"]["test_only_aggregate_gate"]["program_authority"] = True
    decision = _evaluate(forged)
    assert decision["claim_eligibility"] == "exact_manifest_eligible"
    assert decision["decision"] == "publish_evidence_report"
    assert decision["publication_enabled"] is True
    assert decision["applicable_repair"] is None


def test_cached_can_promote_status_and_partial_closure_have_no_authority(tmp_path):
    fixture = _fixture(tmp_path)
    fixture["branch"]["can_promote"] = True
    fixture["branch"]["status"] = "partially_closed_by_backend"
    decision = _evaluate(fixture)
    assert decision["claim_eligibility"] == "ineligible"
    assert "exact_branch_binding" in decision["vetoes"]


def test_legacy_document_branch_remains_report_only(tmp_path):
    fixture = _fixture(tmp_path)
    fixture["branch"] = {
        "id": fixture["branch"]["id"],
        "status": "proved",
        "can_promote": True,
        "typed_assumptions": fixture["branch"]["typed_assumptions"],
    }
    decision = _evaluate(fixture)
    assert decision["claim_eligibility"] == "ineligible"
    assert decision["decision"] in {"publish_gap", "reject"}


def test_decision_recomputes_identically_from_persisted_fixture_bytes(tmp_path):
    fixture = _fixture(tmp_path)
    first = _evaluate(fixture)
    persisted = canonical_json_bytes(first)
    reopened = json.loads(persisted.decode("utf-8"))
    assert verify_phase06_promotion_decision(reopened)["promotion_decision_digest"] == first["promotion_decision_digest"]
    second = _evaluate(fixture)
    assert canonical_json_bytes(second) == persisted


def test_decision_digest_tamper_is_rejected(tmp_path):
    decision = _evaluate(_fixture(tmp_path))
    decision["reason"] = "caller mutation"
    with pytest.raises(ValueError, match="digest mismatch"):
        verify_phase06_promotion_decision(decision)


def test_redigested_internal_semantics_forgery_is_rejected(tmp_path):
    decision = _evaluate(_fixture(tmp_path))
    decision["claim_eligibility"] = "ineligible"
    decision["decision"] = "reject"
    payload = {
        key: decision[key]
        for key in decision
        if key not in {"promotion_decision_digest", "reconstruction"}
    }
    decision["promotion_decision_digest"] = content_digest(payload)
    decision["reconstruction"]["recomputed_digest"] = decision["promotion_decision_digest"]
    with pytest.raises(ValueError, match="semantics mismatch"):
        verify_phase06_promotion_decision(decision)


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (
            lambda decision: decision["engineering_error_ids"].append(
                "forged_engineering_veto"
            ),
            "typed-veto invariant",
        ),
        (lambda decision: decision.update(manifest_refs=[]), "lacks a manifest ref"),
        (
            lambda decision: decision["candidate_edit"].update(text="corrupted"),
            "candidate edit digest mismatch",
        ),
        (
            lambda decision: decision["candidate_edit"]["placement"].update(
                end_byte=-1
            ),
            "candidate edit placement is invalid",
        ),
        (
            lambda decision: decision["invariant_results"][-1].update(passed=False),
            "reconstruction invariant must pass",
        ),
        (lambda decision: decision.update(reason="altered reason"), "semantics mismatch"),
    ],
)
def test_redigested_persisted_decision_mutations_are_rejected(
    tmp_path, mutate, message
):
    decision = _evaluate(_fixture(tmp_path))
    mutate(decision)
    _redigest_decision(decision)

    with pytest.raises(ValueError, match=message):
        verify_phase06_promotion_decision(decision)


def test_persisted_decision_is_internal_consistency_only_for_product_repair(tmp_path):
    fixture = _fixture(tmp_path)
    decision = _evaluate(fixture)
    proposal = {
        "id": "persisted_only_ready_shape",
        "target_label": "eq:sage",
        "location": "synthetic/source.tex > eq:sage",
        "context_branch_id": fixture["branch"]["id"],
        "closure_status": "closed_by_exact_manifest",
        "proposed_edit": {"target_label": "eq:sage", "latex": SOURCE_TARGET},
        "problem": "Synthetic persisted-only proposal.",
        "why": "Exercise the native-reevaluation boundary.",
        "promotion_decision": decision,
        "evidence_refs": [decision["manifest_refs"][0]["manifest_ref"]],
        "remaining_blockers_before_certification": [],
        "metadata": {"contract": document_tree.DOCUMENT_READY_REPAIR_PROPOSAL_CONTRACT},
    }

    errors = document_tree._validate_ready_proposal(proposal)

    assert any("native evidence reevaluation" in error for error in errors)
