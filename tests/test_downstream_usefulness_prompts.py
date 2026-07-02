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
