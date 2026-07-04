import json
from pathlib import Path

from mathdevmcp.real_local_source_adapters import (
    build_source_obligation_ir,
    evaluate_affine_recursion_adapter,
    evaluate_ift_sign_adapter,
    evaluate_joseph_equivalence_adapter,
    evaluate_kalman_likelihood_adapter,
    evaluate_kalman_score_adapter,
    extract_source_packets,
    run_source_adapter_report,
)


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "benchmarks" / "real_tasks" / "holdout_local" / "high_level_pilot_cases.json"


def test_extract_source_packets_preserves_bounded_provenance() -> None:
    report = extract_source_packets(ROOT, MANIFEST)

    assert report["metadata"]["contract"] == "real_local_source_packet_report"
    assert report["status"] == "consistent"
    assert report["summary"] == {"case_total": 5, "packet_total": 9, "aggregate_accuracy": None}
    assert "Packet status must not clear adapter_required." in report["policy_boundary"]
    for packet in report["packets"]:
        assert not Path(packet["source_path"]).is_absolute()
        assert packet["line_start"] <= packet["line_end"]
        assert packet["extracted_line_start"] == packet["line_start"]
        assert packet["extracted_line_end"] == packet["line_end"]
        assert packet["line_count"] == packet["line_end"] - packet["line_start"] + 1
        assert len(packet["content_sha256"]) == 64
        assert packet["excerpt"]
        assert "not proof" in " ".join(packet["policy_boundary"]).lower()


def test_extract_source_packets_rejects_absolute_manifest_path(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][0]["source_snapshot"]["source_files"][0]["path"] = "/tmp/source.tex"
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = extract_source_packets(ROOT, path)

    assert report["status"] == "inconclusive"
    assert report["summary"]["packet_total"] == 8
    assert any("relative" in item["detail"] for item in report["findings"])


def test_extract_source_packets_rejects_bad_line_range(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][0]["source_snapshot"]["source_files"][0]["line_range"] = "589-536"
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = extract_source_packets(ROOT, path)

    assert report["status"] == "inconclusive"
    assert any("line_range" in item["detail"] for item in report["findings"])


def test_extract_source_packets_rejects_oversized_context() -> None:
    report = extract_source_packets(ROOT, MANIFEST, context_before=3)

    assert report["status"] == "inconclusive"
    assert report["summary"]["packet_total"] == 0
    assert all("context line counts" in item["detail"] for item in report["findings"])


def test_extract_source_packets_allows_reviewed_small_context() -> None:
    report = extract_source_packets(ROOT, MANIFEST, context_before=1, context_after=1)

    assert report["status"] == "consistent"
    assert report["summary"]["packet_total"] == 9
    assert all(packet["context_before"] == 1 for packet in report["packets"])
    assert all(packet["context_after"] == 1 for packet in report["packets"])
    assert all(packet["line_count"] >= packet["line_end"] - packet["line_start"] + 1 for packet in report["packets"])


def test_build_source_obligation_ir_preserves_channel_separation() -> None:
    report = build_source_obligation_ir(ROOT, MANIFEST)

    assert report["metadata"]["contract"] == "real_local_source_obligation_ir_report"
    assert report["status"] == "consistent"
    assert report["summary"] == {
        "case_total": 5,
        "obligation_total": 5,
        "pre_adapter_required": 5,
        "aggregate_accuracy": None,
    }
    routes = {item["case_id"]: item["adapter_route"] for item in report["obligations"]}
    assert routes["RLHL-01-ift-gradient-bias-sign"] == "ift_sign_consistency"
    assert routes["RLHL-04-kalman-prediction-error-loglik"] == "kalman_prediction_error_loglik"
    assert routes["RLHL-06-joseph-covariance-equivalence"] == "joseph_covariance_equivalence"
    assert routes["RLHL-07-affine-pricing-master-recursion"] == "affine_pricing_master_recursion"
    assert routes["RLHL-10-kalman-score-same-scalar-contract"] == "kalman_score_same_scalar"
    for obligation in report["obligations"]:
        assert obligation["pre_adapter_status"] == "adapter_required"
        assert "status" not in obligation["source_channel"]
        assert obligation["probe_channel"]["may_clear_adapter_required"] is False
        assert obligation["residual_adapter_channel"]["may_clear_from_probe_or_tests"] is False
        assert "source anchors" in obligation["residual_adapter_channel"]["clearance_requirements"]
        assert obligation["source_channel"]["source_anchors"]
        assert obligation["source_channel"]["packet_hashes"]
        assert "not proof" in " ".join(obligation["policy_boundary"]).lower()


def test_build_source_obligation_ir_keeps_missing_terms_diagnostic_only(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][0]["source_snapshot"]["source_files"] = payload["cases"][0]["source_snapshot"]["source_files"][:1]
    payload["cases"][0]["source_snapshot"]["source_files"][0]["line_range"] = "536-536"
    payload["cases"][0]["source_obligation"]["question"] = "Can we prove the sign relation?"
    path = tmp_path / "reduced_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = build_source_obligation_ir(ROOT, path)
    obligation = next(item for item in report["obligations"] if item["case_id"] == "RLHL-01-ift-gradient-bias-sign")

    assert report["status"] == "consistent"
    assert obligation["pre_adapter_status"] == "adapter_required"
    assert obligation["source_channel"]["missing_terms"]
    assert obligation["probe_channel"]["may_clear_adapter_required"] is False


def test_evaluate_ift_sign_adapter_reports_source_linked_inconsistency_candidate() -> None:
    result = evaluate_ift_sign_adapter(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_source_adapter_result"
    assert result["case_id"] == "RLHL-01-ift-gradient-bias-sign"
    assert result["adapter_route"] == "ift_sign_consistency"
    assert result["status"] == "inconsistency_candidate"
    assert result["checks"]["theorem_negative_sign_present"] is True
    assert result["checks"]["proof_positive_sign_present"] is True
    assert result["checks"]["adjoint_negative_convention_present"] is True
    assert result["checks"]["probe_not_used_for_clearance"] is True
    assert result["clearance"]["adapter_required_cleared"] is True
    assert result["clearance"]["cleared_by"] == "source_anchored_local_schema_check"
    assert "executable_probe" in result["clearance"]["not_cleared_by"]
    assert result["source_anchors"]
    assert any("whole DSGE note" in item for item in result["non_claims"])


def test_evaluate_ift_sign_adapter_does_not_clear_when_proof_sign_is_absent(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][0]["source_snapshot"]["source_files"] = payload["cases"][0]["source_snapshot"]["source_files"][:1]
    payload["cases"][0]["source_snapshot"]["source_files"][0]["line_range"] = "536-562"
    path = tmp_path / "no_proof_final_sign.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = evaluate_ift_sign_adapter(ROOT, path)

    assert result["status"] == "human_review_required"
    assert result["checks"]["proof_positive_sign_present"] is False
    assert result["clearance"]["adapter_required_cleared"] is False


def test_evaluate_kalman_likelihood_adapter_requires_spd_assumption_in_packet() -> None:
    result = evaluate_kalman_likelihood_adapter(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_source_adapter_result"
    assert result["case_id"] == "RLHL-04-kalman-prediction-error-loglik"
    assert result["adapter_route"] == "kalman_prediction_error_loglik"
    assert result["status"] == "human_review_required"
    assert result["checks"]["linear_gaussian_present"] is True
    assert result["checks"]["chain_rule_present"] is True
    assert result["checks"]["gaussian_predictive_present"] is True
    assert result["checks"]["logdet_term_present"] is True
    assert result["checks"]["quadratic_term_present"] is True
    assert result["checks"]["positive_definite_or_spd_present"] is False
    assert result["checks"]["mask_or_observed_components_present"] is True
    assert result["checks"]["no_observation_skip_present"] is True
    assert result["clearance"]["adapter_required_cleared"] is False
    assert any("nonlinear filters" in item for item in result["non_claims"])


def test_evaluate_kalman_likelihood_adapter_clears_with_spd_assumption_packet(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][1]["source_snapshot"]["source_files"].append(
        {
            "path": "../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex",
            "line_range": "32-39",
            "role": "innovation regularity assumption",
        }
    )
    path = tmp_path / "likelihood_with_spd.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = evaluate_kalman_likelihood_adapter(ROOT, path)

    assert result["status"] == "source_supported"
    assert result["checks"]["positive_definite_or_spd_present"] is True
    assert result["clearance"]["adapter_required_cleared"] is True
    assert result["clearance"]["cleared_by"] == "source_anchored_local_schema_check"


def test_evaluate_kalman_likelihood_adapter_does_not_clear_without_mask_boundary(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][1]["source_snapshot"]["source_files"] = payload["cases"][1]["source_snapshot"]["source_files"][:1]
    path = tmp_path / "dense_only_likelihood.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = evaluate_kalman_likelihood_adapter(ROOT, path)

    assert result["status"] == "human_review_required"
    assert result["checks"]["mask_or_observed_components_present"] is False
    assert result["checks"]["no_observation_skip_present"] is False
    assert result["clearance"]["adapter_required_cleared"] is False


def test_evaluate_joseph_equivalence_adapter_reports_source_support() -> None:
    result = evaluate_joseph_equivalence_adapter(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_source_adapter_result"
    assert result["case_id"] == "RLHL-06-joseph-covariance-equivalence"
    assert result["adapter_route"] == "joseph_covariance_equivalence"
    assert result["status"] == "source_supported"
    assert result["checks"]["joseph_form_present"] is True
    assert result["checks"]["compact_form_present"] is True
    assert result["checks"]["kalman_gain_present"] is True
    assert result["checks"]["spd_condition_present"] is True
    assert result["checks"]["equivalence_claim_present"] is True
    assert result["checks"]["numerical_caveat_present"] is True
    assert result["clearance"]["adapter_required_cleared"] is True
    assert result["clearance"]["cleared_by"] == "source_anchored_local_schema_check"
    assert any("compact form preserves" in item for item in result["non_claims"])


def test_evaluate_joseph_equivalence_adapter_does_not_clear_without_gain_relation(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][2]["source_snapshot"]["source_files"] = payload["cases"][2]["source_snapshot"]["source_files"][:1]
    path = tmp_path / "joseph_without_gain.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = evaluate_joseph_equivalence_adapter(ROOT, path)

    assert result["status"] == "human_review_required"
    assert result["checks"]["kalman_gain_present"] is False
    assert result["checks"]["spd_condition_present"] is False
    assert result["clearance"]["adapter_required_cleared"] is False


def test_evaluate_affine_recursion_adapter_reports_source_support() -> None:
    result = evaluate_affine_recursion_adapter(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_source_adapter_result"
    assert result["case_id"] == "RLHL-07-affine-pricing-master-recursion"
    assert result["adapter_route"] == "affine_pricing_master_recursion"
    assert result["status"] == "source_supported"
    assert result["checks"]["state_transition_present"] is True
    assert result["checks"]["exponential_affine_ansatz_present"] is True
    assert result["checks"]["pricing_expectation_present"] is True
    assert result["checks"]["conditional_normality_present"] is True
    assert result["checks"]["gaussian_mgf_present"] is True
    assert result["checks"]["b_recursion_present"] is True
    assert result["checks"]["a_recursion_present"] is True
    assert result["checks"]["initial_conditions_present"] is True
    assert result["checks"]["coefficient_collection_present"] is True
    assert result["clearance"]["adapter_required_cleared"] is True
    assert any("empirical pricing validity" in item for item in result["non_claims"])


def test_evaluate_affine_recursion_adapter_does_not_clear_without_mgf(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][3]["source_snapshot"]["source_files"][0]["line_range"] = "242-292"
    path = tmp_path / "affine_without_mgf.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = evaluate_affine_recursion_adapter(ROOT, path)

    assert result["status"] == "human_review_required"
    assert result["checks"]["gaussian_mgf_present"] is False
    assert result["checks"]["coefficient_collection_present"] is False
    assert result["clearance"]["adapter_required_cleared"] is False


def test_evaluate_kalman_score_adapter_reports_source_support() -> None:
    result = evaluate_kalman_score_adapter(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_source_adapter_result"
    assert result["case_id"] == "RLHL-10-kalman-score-same-scalar-contract"
    assert result["adapter_route"] == "kalman_score_same_scalar"
    assert result["status"] == "source_supported"
    assert result["checks"]["innovation_derivatives_present"] is True
    assert result["checks"]["inverse_derivative_rule_present"] is True
    assert result["checks"]["score_contribution_present"] is True
    assert result["checks"]["solve_relation_present"] is True
    assert result["checks"]["solve_score_present"] is True
    assert result["checks"]["source_label_present"] is True
    assert result["checks"]["trace_or_factor_caveat_present"] is True
    assert result["checks"]["value_oracle_present"] is True
    assert result["checks"]["same_scalar_boundary_present"] is True
    assert result["checks"]["prior_transform_boundary_present"] is True
    assert result["clearance"]["adapter_required_cleared"] is True
    assert any("HMC validity" in item for item in result["non_claims"])


def test_evaluate_kalman_score_adapter_does_not_clear_without_same_scalar_packet(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][4]["source_snapshot"]["source_files"] = payload["cases"][4]["source_snapshot"]["source_files"][:1]
    path = tmp_path / "score_without_same_scalar.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = evaluate_kalman_score_adapter(ROOT, path)

    assert result["status"] == "human_review_required"
    assert result["checks"]["value_oracle_present"] is False
    assert result["checks"]["same_scalar_boundary_present"] is False
    assert result["clearance"]["adapter_required_cleared"] is False


def test_run_source_adapter_report_preserves_residual_gap_and_no_accuracy() -> None:
    report = run_source_adapter_report(ROOT, MANIFEST)

    assert report["metadata"]["contract"] == "real_local_source_adapter_report"
    assert report["status"] == "partial"
    assert report["summary"] == {
        "case_total": 5,
        "source_supported": 3,
        "inconsistency_candidate": 1,
        "human_review_required": 1,
        "adapter_required_residual": 1,
        "aggregate_accuracy": None,
    }
    assert len(report["source_obligation_ledger"]) == 5
    assert len(report["adapter_result_ledger"]) == 5
    assert report["probe_reference"]["may_clear_adapter_required"] is False
    assert report["residual_gap_ledger"] == [
        {
            "case_id": "RLHL-04-kalman-prediction-error-loglik",
            "adapter_route": "kalman_prediction_error_loglik",
            "status": "adapter_required",
            "reason": "The bounded source packets did not contain all required likelihood derivation and domain-assumption evidence.",
            "missing_checks": ["positive_definite_or_spd_present"],
            "next_action": "review_source_packet_scope_or_extend_manifest_under_governance",
        }
    ]
    assert "No single aggregate source/probe accuracy metric is emitted." in report["policy_boundary"]


def test_run_source_adapter_report_can_pass_with_governed_spd_packet_extension(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][1]["source_snapshot"]["source_files"].append(
        {
            "path": "../BayesFilter/docs/chapters/ch05_prediction_error_decomposition.tex",
            "line_range": "32-39",
            "role": "innovation regularity assumption",
        }
    )
    path = tmp_path / "source_report_with_spd.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    report = run_source_adapter_report(ROOT, path)

    assert report["status"] == "passed"
    assert report["summary"]["adapter_required_residual"] == 0
    assert report["summary"]["aggregate_accuracy"] is None
    assert report["residual_gap_ledger"] == []
