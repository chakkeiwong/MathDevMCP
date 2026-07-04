import json
from pathlib import Path

from mathdevmcp.downstream_usefulness_prompts import validate_downstream_prompt_contract


def _write_prompt(root: Path, name: str, text: str) -> str:
    path = root / "prompts" / name
    path.parent.mkdir()
    path.write_text(text)
    return str(path.relative_to(root))


def test_validator_rejects_a_task_only_evaluator_leakage(tmp_path: Path) -> None:
    rel_path = _write_prompt(
        tmp_path,
        "case__A_task_only.txt",
        '{"question": "Can we prove X?", "evidence_class_for_evaluator": "backend_certificate"}',
    )
    manifest = {
        "prompts": [
            {
                "prompt_id": "case__A_task_only",
                "case_id": "case",
                "condition": "A_task_only",
                "path": rel_path,
            },
            {
                "prompt_id": "case__B_evidence_only",
                "case_id": "case",
                "condition": "B_evidence_only",
                "path": rel_path,
            },
            {
                "prompt_id": "case__C_human_framed",
                "case_id": "case",
                "condition": "C_human_framed",
                "path": rel_path,
            },
        ]
    }

    errors = validate_downstream_prompt_contract(manifest, root=tmp_path)

    assert "case__A_task_only: A_task_only prompt leaks forbidden payload term evidence_class_for_evaluator" in errors


def test_validator_accepts_minimal_repaired_abc_case(tmp_path: Path) -> None:
    a_path = _write_prompt(tmp_path, "case__A_task_only.txt", '{"question": "Can we prove X?"}')
    b_path = str(Path(a_path).with_name("case__B_evidence_only.txt"))
    c_path = str(Path(a_path).with_name("case__C_human_framed.txt"))
    (tmp_path / b_path).write_text('{"question": "Can we prove X?", "evidence_class": "backend_certificate"}')
    (tmp_path / c_path).write_text(
        '{"question": "Can we prove X?", "evidence_class": "backend_certificate", '
        '"human_framed_packet_reasoning": "Use scoped evidence only."}'
    )
    manifest = {
        "prompts": [
            {"prompt_id": "case__A_task_only", "case_id": "case", "condition": "A_task_only", "path": a_path},
            {"prompt_id": "case__B_evidence_only", "case_id": "case", "condition": "B_evidence_only", "path": b_path},
            {"prompt_id": "case__C_human_framed", "case_id": "case", "condition": "C_human_framed", "path": c_path},
        ]
    }

    assert validate_downstream_prompt_contract(manifest, root=tmp_path) == []


def test_current_phase4_manifest_records_known_a_leakage() -> None:
    root = Path(__file__).resolve().parents[1]
    manifest_path = root / ".mathdevmcp/downstream_agent_usefulness/prompt_manifest.json"
    if not manifest_path.exists():
        return

    errors = validate_downstream_prompt_contract(json.loads(manifest_path.read_text()), root=root)

    a_errors = [error for error in errors if "A_task_only prompt leaks forbidden payload term" in error]
    assert len(a_errors) == 18


def test_v2_scored_artifacts_remain_bounded_regression_guard() -> None:
    root = Path(__file__).resolve().parents[1]
    v2_root = root / ".mathdevmcp/downstream_agent_usefulness_v2"
    scored = json.loads((v2_root / "scored_responses_candidate.json").read_text(encoding="utf-8"))
    manifest = json.loads((v2_root / "response_manifest_candidate.json").read_text(encoding="utf-8"))
    contract = json.loads((v2_root / "scoring_contract_v2_collection.json").read_text(encoding="utf-8"))

    assert scored["metadata"]["contract"] == "downstream_agent_usefulness_v2_scored_responses_candidate"
    assert manifest["metadata"]["contract"] == "downstream_agent_usefulness_v2_response_manifest_candidate"
    assert contract["metadata"]["contract"] == "downstream_agent_usefulness_v2_collection_scoring_contract"

    rows = scored["rows"]
    responses = manifest["responses"]
    assert len(rows) == 18
    assert manifest["metadata"]["response_count"] == 18
    assert len(responses) == 18
    assert {row["response_artifact"] for row in rows} == {response["response_path"] for response in responses}

    assert scored["hard_veto_summary"] == {
        "A_task_only": 0,
        "B_evidence_only": 0,
        "C_human_framed": 0,
        "total": 0,
    }
    assert {condition: summary["rows"] for condition, summary in scored["condition_summary"].items()} == {
        "A_task_only": 6,
        "B_evidence_only": 6,
        "C_human_framed": 6,
    }
    assert {condition: summary["required_passes"] for condition, summary in scored["condition_summary"].items()} == {
        "A_task_only": 6,
        "B_evidence_only": 5,
        "C_human_framed": 6,
    }
    assert all(not response["claude_response_worker"] for response in responses)
    assert all(response["no_retry"] for response in responses)
    assert all(not response["malformed_output"] for response in responses)

    rule = scored["minimum_candidate_rule"]
    assert rule["primary_comparator"] == "B_evidence_only"
    assert rule["candidate"] == "C_human_framed"
    assert rule["aggregate_only_forbidden"] is True
    assert rule["candidate_rule_pass"] is True
    assert rule["improved_cases"] == ["V2-PRP-01-gaussian-score-review-packet"]
    assert contract["collection_scope"]["collection_authorized_by_this_contract"] is False
    assert contract["condition_comparison_rule"]["aggregate_only_forbidden"] is True
    assert contract["scoring_order"] == [
        "record_malformed_output_status",
        "apply_hard_vetoes",
        "score_primary_required_dimensions",
        "score_explanatory_dimensions",
        "score_candidate_only_stressors_as_explanatory",
        "compute_per_case_b_vs_c_delta",
        "summarize_hard_vetoes_before_pass_counts",
    ]
    assert "release_public_scientific_product_claim" in contract["hard_vetoes"]

    non_claim_text = "\n".join(scored["limitations"] + contract["non_claims"] + manifest["non_claims"])
    assert "not a public benchmark" in non_claim_text
    assert "not release" in non_claim_text
    assert "not scientific" in non_claim_text
    assert "not product capability" in non_claim_text
