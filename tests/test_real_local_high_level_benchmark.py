import json
from pathlib import Path

from mathdevmcp.agent_handoff_packet import validate_agent_handoff_packet
from mathdevmcp.real_local_high_level_benchmark import (
    REQUIRED_REVIEW_PACKET_FIELDS,
    build_real_local_high_level_baseline_report,
    build_real_local_high_level_final_matrix,
    build_real_local_high_level_packet_report,
    build_real_local_high_level_route_availability_report,
    load_real_local_high_level_benchmark_manifest,
)


ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "benchmarks" / "real_tasks" / "holdout_local" / "real_local_high_level_workflow_benchmark_cases.json"


def test_real_local_high_level_benchmark_manifest_validates_schema_and_boundaries() -> None:
    result = load_real_local_high_level_benchmark_manifest(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_high_level_workflow_benchmark_manifest"
    assert result["status"] == "consistent"
    assert result["summary"]["case_total"] == 9
    assert result["summary"]["workflow_total"] == 6
    assert result["summary"]["negative_control_total"] == 5
    assert result["summary"]["aggregate_accuracy"] is None
    assert set(result["summary"]["workflow_coverage"]) == {
        "assumptions_for",
        "audit_math_to_code",
        "debug_derivation",
        "derive_from",
        "prepare_review_packet",
        "prove_or_counterexample",
    }
    assert any("local/non-gating" in item for item in result["policy_boundary"])

    for case in result["cases"]:
        assert case["tier"] == "holdout_local"
        assert set(case["minimal_packet_schema"]["required_fields"]) == REQUIRED_REVIEW_PACKET_FIELDS
        assert case["human_framing"]["local_background"]
        assert case["human_framing"]["minimal_formula_scaffold"]
        assert case["human_framing"]["decision_criteria"]
        assert case["human_framing"]["what_would_change_conclusion"]
        assert case["scoring_rubric"]["aggregate_accuracy"] is None
        assert "case_status" not in case
        assert "accuracy" not in case
        assert "gold_answer" not in case
        for source_file in case["source_snapshot"]["source_files"]:
            assert not Path(source_file["path"]).is_absolute()


def test_real_local_high_level_benchmark_manifest_rejects_missing_negative_control_semantics(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    del payload["metadata"]["negative_control_status_semantics"]["backend_unavailable"]
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_real_local_high_level_benchmark_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(item["kind"] == "negative_control_status_semantics_incomplete" for item in result["findings"])


def test_real_local_high_level_benchmark_manifest_rejects_incomplete_packet_schema(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][0]["minimal_packet_schema"]["required_fields"].remove("non_claims")
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_real_local_high_level_benchmark_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(
        item["kind"] == "minimal_packet_schema_incomplete" and item.get("case_id") == "RLHLB-01-ift-sign-gap"
        for item in result["findings"]
    )


def test_real_local_high_level_benchmark_manifest_rejects_aggregate_accuracy_field(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][0]["scoring_rubric"]["aggregate_accuracy"] = 1.0
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_real_local_high_level_benchmark_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(item["kind"] == "aggregate_accuracy_forbidden" for item in result["findings"])


def test_real_local_high_level_benchmark_manifest_rejects_bad_negative_control_status(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][0]["negative_control"]["expected_status"] = "proved"
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_real_local_high_level_benchmark_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(item["kind"] == "negative_control_expected_status_invalid" for item in result["findings"])


def test_real_local_high_level_benchmark_manifest_rejects_negative_control_status_evidence_mismatch(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][5]["expected_evidence_classes"] = ["source_anchor", "backend_certificate", "route_availability"]
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_real_local_high_level_benchmark_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(item["kind"] == "negative_control_expected_status_forbidden_evidence" for item in result["findings"])


def test_real_local_high_level_benchmark_manifest_requires_workflow_result_artifacts(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    del payload["metadata"]["workflow_evidence_contracts"]["derive_from"]["result_artifact"]
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_real_local_high_level_benchmark_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(item["kind"] == "workflow_evidence_contract_missing_fields" for item in result["findings"])


def test_real_local_high_level_benchmark_manifest_requires_route_availability_for_routing_only(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"][5]["expected_evidence_classes"].remove("route_availability")
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_real_local_high_level_benchmark_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(item["kind"] == "negative_control_expected_status_missing_evidence" for item in result["findings"])


def test_real_local_high_level_benchmark_manifest_enforces_frozen_case_count(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"] = payload["cases"][:-1]
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = load_real_local_high_level_benchmark_manifest(ROOT, path)

    assert result["status"] == "inconclusive"
    assert any(item["kind"] == "case_count_not_frozen_expected_count" for item in result["findings"])


def test_real_local_high_level_route_availability_report_covers_all_frozen_cases() -> None:
    result = build_real_local_high_level_route_availability_report(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_high_level_workflow_route_availability_report"
    assert result["status"] == "consistent"
    assert result["summary"]["case_total"] == 9
    assert result["summary"]["packet_stub_total"] == 9
    assert result["summary"]["source_adapter_present"] == 5
    assert result["summary"]["source_adapter_absent"] == 0
    assert result["summary"]["aggregate_accuracy"] is None
    assert "Route availability is pre-baseline routing evidence only." in result["policy_boundary"]

    by_case = {item["case_id"]: item for item in result["route_ledger"]}
    assert by_case["RLHLB-01-ift-sign-gap"]["source_adapter"]["adapter_route"] == "ift_sign_consistency"
    assert by_case["RLHLB-05-kalman-score-same-scalar"]["source_adapter"]["adapter_route"] == "kalman_score_same_scalar"
    assert by_case["RLHLB-06-state-space-code-missing-solve"]["source_adapter"]["state"] == "not_applicable"
    assert by_case["RLHLB-06-state-space-code-missing-solve"]["code_equation_route"]["state"] == "available"
    assert by_case["RLHLB-07-proof-boundary-review-packet"]["review_packet_route"]["state"] == "available"
    assert by_case["RLHLB-08-hmc-value-only-boundary"]["formal_backend"]["backend"] == "lean"
    assert "negative_control_requires_boundary_preservation" in by_case["RLHLB-08-hmc-value-only-boundary"]["residual_unresolved"]


def test_real_local_high_level_route_availability_packet_stubs_satisfy_phase2_schema() -> None:
    result = build_real_local_high_level_route_availability_report(ROOT, MANIFEST)

    for item in result["packet_stubs"]:
        packet = item["packet"]
        assert set(packet) >= REQUIRED_REVIEW_PACKET_FIELDS
        assert packet["question"]
        assert packet["source_anchors"]
        assert isinstance(packet["assumptions"], list)
        assert isinstance(packet["backend_checks"], list)
        assert isinstance(packet["counterexamples"], list)
        assert isinstance(packet["gaps"], list)
        assert isinstance(packet["actions"], list)
        assert isinstance(packet["evidence_classes"], list)
        assert any("not a proof" in text for text in packet["non_claims"])
        assert all(
            text.startswith("Forbidden claim not made:") or "not a proof" in text or "does not evaluate" in text
            for text in packet["non_claims"]
        )


def test_real_local_high_level_route_availability_does_not_turn_unavailable_backend_into_refutation(monkeypatch) -> None:
    import mathdevmcp.real_local_high_level_benchmark as benchmark

    monkeypatch.setattr(benchmark, "_module_available", lambda name: False)
    result = benchmark.build_real_local_high_level_route_availability_report(ROOT, MANIFEST)

    assert result["status"] == "consistent"
    symbolic_states = {item["symbolic_backend"]["state"] for item in result["route_ledger"]}
    assert "backend_unavailable" in symbolic_states
    for item in result["route_ledger"]:
        assert item["symbolic_backend"]["state"] != "refuted"
        packet = next(stub["packet"] for stub in result["packet_stubs"] if stub["case_id"] == item["case_id"])
        assert "Phase 3 route availability does not evaluate the mathematical case." in packet["non_claims"]


def test_real_local_high_level_route_availability_rejects_invalid_manifest(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"] = payload["cases"][:4]
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = build_real_local_high_level_route_availability_report(ROOT, path)

    assert result["status"] == "inconclusive"
    assert result["summary"]["case_total"] == 0
    assert any(item["kind"] == "manifest_inconclusive" for item in result["findings"])


def test_real_local_high_level_baseline_runs_all_frozen_cases_without_accuracy_metric() -> None:
    result = build_real_local_high_level_baseline_report(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_high_level_workflow_baseline_report"
    assert result["status"] == "completed"
    assert result["summary"]["case_total"] == 9
    assert result["summary"]["aggregate_accuracy"] is None
    assert result["route_report_summary"]["case_total"] == 9
    assert len(result["results"]) == 9
    assert "Aggregate rates are diagnostic only and are not promotion criteria." in result["policy_boundary"]

    by_case = {item["case_id"]: item for item in result["results"]}
    assert by_case["RLHLB-06-state-space-code-missing-solve"]["observed_status"] == "structural_mismatch"
    assert by_case["RLHLB-07-proof-boundary-review-packet"]["observed_status"] == "diagnostic_only"
    assert by_case["RLHLB-08-hmc-value-only-boundary"]["failure_class"] == "correct_abstention_or_route_gap"
    assert by_case["RLHLB-08-hmc-value-only-boundary"]["expected_status_family"] == "insufficient_evidence"
    assert by_case["RLHLB-08-hmc-value-only-boundary"]["route_reference"]["formal_backend_state"] == "available_requires_explicit_source"
    assert by_case["RLHLB-09-affine-recovery-assumption-limit"]["observed_status"] == "missing_assumptions"
    assert result["summary"]["unexpected_status_family"] == 0


def test_real_local_high_level_baseline_is_deterministic_for_statuses_and_evidence_classes() -> None:
    left = build_real_local_high_level_baseline_report(ROOT, MANIFEST)
    right = build_real_local_high_level_baseline_report(ROOT, MANIFEST)

    left_projection = [
        (item["case_id"], item["observed_status"], item["observed_evidence_classes"], item["failure_class"])
        for item in left["results"]
    ]
    right_projection = [
        (item["case_id"], item["observed_status"], item["observed_evidence_classes"], item["failure_class"])
        for item in right["results"]
    ]
    assert left_projection == right_projection


def test_real_local_high_level_baseline_preserves_negative_control_boundaries() -> None:
    result = build_real_local_high_level_baseline_report(ROOT, MANIFEST)

    negative = [
        item
        for item in result["results"]
        if item["case_id"]
        in {
            "RLHLB-01-ift-sign-gap",
            "RLHLB-06-state-space-code-missing-solve",
            "RLHLB-07-proof-boundary-review-packet",
            "RLHLB-08-hmc-value-only-boundary",
            "RLHLB-09-affine-recovery-assumption-limit",
        }
    ]
    assert len(negative) == 5
    for item in negative:
        assert all(item["boundary_checks"].values())
        assert item["expected_status_family"] is not None
        assert item["failure_class"] != "boundary_violation"


def test_real_local_high_level_baseline_stops_on_invalid_manifest(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"] = payload["cases"][:4]
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = build_real_local_high_level_baseline_report(ROOT, path)

    assert result["status"] == "inconclusive"
    assert result["summary"]["case_total"] == 0


def test_real_local_high_level_packet_report_builds_durable_packets_for_all_cases() -> None:
    result = build_real_local_high_level_packet_report(ROOT, MANIFEST)

    assert result["metadata"]["contract"] == "real_local_high_level_workflow_packet_report"
    assert result["status"] == "consistent"
    assert result["summary"]["case_total"] == 9
    assert result["summary"]["packet_total"] == 9
    assert result["summary"]["packet_findings"] == 0
    assert result["summary"]["aggregate_accuracy"] is None
    assert result["baseline_summary"]["unexpected_status_family"] == 0
    assert "Durable packets are review artifacts and not a proof certificate by themselves." in result["policy_boundary"]
    assert any("downstream-agent reliability" in item for item in result["policy_boundary"])

    by_case = {item["case_id"]: item for item in result["packets"]}
    assert set(by_case) == {
        "RLHLB-01-ift-sign-gap",
        "RLHLB-02-kalman-loglik-assumptions",
        "RLHLB-03-joseph-equivalence",
        "RLHLB-04-affine-pricing-recursion",
        "RLHLB-05-kalman-score-same-scalar",
        "RLHLB-06-state-space-code-missing-solve",
        "RLHLB-07-proof-boundary-review-packet",
        "RLHLB-08-hmc-value-only-boundary",
        "RLHLB-09-affine-recovery-assumption-limit",
    }
    for item in result["packets"]:
        packet = item["packet"]
        assert validate_agent_handoff_packet(packet) == []
        assert set(packet) >= REQUIRED_REVIEW_PACKET_FIELDS
        assert all(item["completeness"].values())
        assert packet["source_anchors"]
        assert packet["human_framing"]["local_background"]
        assert packet["human_framing"]["minimal_formula_scaffold"]
        assert packet["human_framing"]["decision_criteria"]
        assert packet["human_framing"]["what_would_change_conclusion"]
        assert packet["backend_checks"]
        assert packet["evidence_classes"]
        assert any("local/non-gating" in text for text in packet["non_claims"])
        assert any(text.startswith("Forbidden claim not made:") for text in packet["non_claims"])
        reasoning = packet["reasoning"]
        assert reasoning["conclusion"]
        assert len(reasoning["why"]) >= 4
        assert reasoning["human_framing"]["local_background"]
        assert reasoning["human_framing"]["minimal_formula_scaffold"]
        assert reasoning["human_framing"]["decision_criteria"]
        assert reasoning["human_framing"]["what_would_change_conclusion"]
        assert reasoning["source_context"]
        assert reasoning["formalization"]
        assert reasoning["decisive_evidence"]
        assert reasoning["why_conclusion_follows"]
        assert any("Source context:" in line for line in reasoning["why"])
        assert any("Human framing:" in line for line in reasoning["why"])
        assert any("Why the conclusion follows:" in line for line in reasoning["why"])
        assert any("Boundary:" in line for line in reasoning["why"])
        assert "Conclusion:" in reasoning["answer_text"]
        assert "Human framing:" in reasoning["answer_text"]
        assert "Local background refresher:" in reasoning["answer_text"]
        assert "Minimal formula scaffold:" in reasoning["answer_text"]
        assert "Decision criteria:" in reasoning["answer_text"]
        assert "What would change the conclusion:" in reasoning["answer_text"]
        assert "Source context:" in reasoning["answer_text"]
        assert "Encoded obligation or artifact:" in reasoning["answer_text"]
        assert "Decisive evidence:" in reasoning["answer_text"]
        assert "Why the conclusion follows:" in reasoning["answer_text"]
        assert reasoning["answer_text"].count("\n") >= 3
        assert reasoning["limits"]

    assert by_case["RLHLB-04-affine-pricing-recursion"]["observed_status"] == "inconclusive"
    assert by_case["RLHLB-04-affine-pricing-recursion"]["packet"]["gaps"]
    assert by_case["RLHLB-04-affine-pricing-recursion"]["packet"]["reasoning"]["remaining_gaps"]
    assert by_case["RLHLB-08-hmc-value-only-boundary"]["observed_status"] == "inconclusive"
    assert by_case["RLHLB-08-hmc-value-only-boundary"]["packet"]["gaps"]
    assert by_case["RLHLB-09-affine-recovery-assumption-limit"]["observed_status"] == "missing_assumptions"
    assert by_case["RLHLB-09-affine-recovery-assumption-limit"]["packet"]["assumptions"]
    assert by_case["RLHLB-09-affine-recovery-assumption-limit"]["packet"]["reasoning"]["assumptions_needed"]
    assert "source-backed semantic assumptions" in by_case["RLHLB-09-affine-recovery-assumption-limit"]["packet"]["reasoning"]["answer_text"]
    assert "Missing term(s): solve." in by_case["RLHLB-06-state-space-code-missing-solve"]["packet"]["reasoning"]["answer_text"]
    assert "A log determinant alone does not account for the size of the forecast error." in by_case[
        "RLHLB-06-state-space-code-missing-solve"
    ]["packet"]["reasoning"]["answer_text"]
    assert "semantic placeholders" in by_case["RLHLB-09-affine-recovery-assumption-limit"]["packet"]["reasoning"]["answer_text"]


def test_real_local_high_level_packet_report_stops_on_invalid_manifest(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"] = payload["cases"][:4]
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = build_real_local_high_level_packet_report(ROOT, path)

    assert result["status"] == "inconclusive"
    assert result["summary"]["case_total"] == 0
    assert any(item["kind"] == "baseline_inconclusive" for item in result["findings"])


def test_real_local_high_level_final_matrix_matches_packet_report_cases() -> None:
    matrix = build_real_local_high_level_final_matrix(ROOT, MANIFEST)
    packets = build_real_local_high_level_packet_report(ROOT, MANIFEST)

    assert matrix["metadata"]["contract"] == "real_local_high_level_workflow_final_matrix"
    assert matrix["status"] == "consistent"
    assert matrix["summary"]["case_total"] == 9
    assert matrix["summary"]["matrix_total"] == 9
    assert matrix["summary"]["boundary_violations"] == 0
    assert matrix["summary"]["unexpected_status_family"] == 0
    assert matrix["summary"]["aggregate_accuracy"] is None
    assert [row["case_id"] for row in matrix["matrix"]] == [item["case_id"] for item in packets["packets"]]

    by_case = {row["case_id"]: row for row in matrix["matrix"]}
    for row in matrix["matrix"]:
        assert row["status_scope"] == "local_regression_only_not_promoted"
        assert row["actual_route"]["packet_complete"] is True
        assert row["remaining_limitation"]
    assert by_case["RLHLB-08-hmc-value-only-boundary"]["repair_round"] == "phase05_semantic_placeholder_guard"
    assert by_case["RLHLB-09-affine-recovery-assumption-limit"]["repair_round"] == "phase05_semantic_placeholder_guard"
    assert "explicit_missing_assumptions_preserved" in by_case["RLHLB-09-affine-recovery-assumption-limit"]["remaining_limitation"]


def test_real_local_high_level_final_matrix_stops_on_invalid_manifest(tmp_path: Path) -> None:
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["cases"] = payload["cases"][:4]
    path = tmp_path / "bad_manifest.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = build_real_local_high_level_final_matrix(ROOT, path)

    assert result["status"] == "inconclusive"
    assert result["summary"]["case_total"] == 0
    assert any(item["kind"] == "packet_report_inconclusive" for item in result["findings"])
