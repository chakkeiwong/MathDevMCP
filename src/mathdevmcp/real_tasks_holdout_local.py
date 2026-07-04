from __future__ import annotations

"""Local helper for discovering non-committed holdout manifests."""

from pathlib import Path
from typing import Any

from .contracts import attach_contract


def _default_local_holdout_path(root_path: Path) -> Path:
    return root_path / ".local" / "mathdevmcp" / "holdout_local_cases.json"


def _default_local_holdout_candidate_answers_path(root_path: Path) -> Path:
    return root_path / ".local" / "mathdevmcp" / "holdout_local_candidate_answers.json"


def _template_holdout_path(root_path: Path) -> Path:
    return root_path / "benchmarks" / "real_tasks" / "manifests" / "holdout_local_cases.template.json"


def _template_holdout_candidate_answers_path(root_path: Path) -> Path:
    return root_path / "benchmarks" / "real_tasks" / "fixtures" / "holdout_local_candidate_answers.template.json"


def discover_local_holdout_manifest(root: str | Path | None = None, manifest_path: str | Path | None = None) -> dict:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    default_path = _default_local_holdout_path(root_path)
    path = Path(manifest_path).resolve() if manifest_path is not None else default_path

    if not path.exists():
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "No local holdout manifest was discovered. This is expected until a user populates one locally.",
                "path": str(path),
                "exists": False,
                "policy_boundary": [
                    "Holdout-local manifests are local evaluation artifacts and are not committed by default.",
                    "Absence of a local holdout manifest is not a benchmark failure.",
                ],
            },
            "real_task_holdout_local_discovery",
        )

    return attach_contract(
        {
            "status": "consistent",
            "reason": "A local holdout manifest path exists. Discovery is structural only and does not imply holdout evaluation has been run.",
            "path": str(path),
            "exists": True,
            "policy_boundary": [
                "This discovery result is not holdout evaluation evidence.",
                "A discovered local manifest remains outside the committed public benchmark surface.",
            ],
        },
        "real_task_holdout_local_discovery",
    )


def discover_local_holdout_candidate_answers(root: str | Path | None = None, candidate_path: str | Path | None = None) -> dict:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    default_path = _default_local_holdout_candidate_answers_path(root_path)
    path = Path(candidate_path).resolve() if candidate_path is not None else default_path

    if not path.exists():
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "No local holdout candidate-answer file was discovered. This is expected until a user populates one locally.",
                "path": str(path),
                "exists": False,
                "policy_boundary": [
                    "Local holdout candidate answers are local evaluation artifacts and are not committed by default.",
                    "Absence of a local candidate-answer file is not a benchmark failure.",
                ],
            },
            "real_task_holdout_local_candidate_discovery",
        )

    return attach_contract(
        {
            "status": "consistent",
            "reason": "A local holdout candidate-answer path exists. Discovery is structural only and does not imply holdout evaluation has been run.",
            "path": str(path),
            "exists": True,
            "policy_boundary": [
                "This discovery result is not holdout evaluation evidence.",
                "A discovered local candidate-answer file remains outside the committed public benchmark surface.",
            ],
        },
        "real_task_holdout_local_candidate_discovery",
    )


def initialize_local_holdout_manifest(root: str | Path | None = None, manifest_path: str | Path | None = None) -> dict:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    template_path = _template_holdout_path(root_path)
    destination = Path(manifest_path).resolve() if manifest_path is not None else _default_local_holdout_path(root_path)

    if destination.exists():
        return attach_contract(
            {
                "status": "consistent",
                "reason": "Local holdout manifest already exists; initializer refused to overwrite it.",
                "path": str(destination),
                "created": False,
                "overwrote_existing": False,
                "policy_boundary": [
                    "Existing local holdout manifests are preserved by default.",
                    "Initialization is a scaffold action, not holdout evaluation evidence.",
                ],
            },
            "real_task_holdout_local_initialization",
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
    return attach_contract(
        {
            "status": "consistent",
            "reason": "Local holdout manifest scaffold initialized from the committed template.",
            "path": str(destination),
            "created": True,
            "overwrote_existing": False,
            "template_path": str(template_path),
            "policy_boundary": [
                "This initializer creates a local scaffold only and does not produce holdout evaluation evidence.",
                "The created file remains a non-committed local artifact unless the user explicitly promotes it.",
            ],
        },
        "real_task_holdout_local_initialization",
    )


def initialize_local_holdout_candidate_answers(root: str | Path | None = None, candidate_path: str | Path | None = None) -> dict:
    root_path = Path(root).resolve() if root is not None else Path(__file__).resolve().parents[2]
    template_path = _template_holdout_candidate_answers_path(root_path)
    destination = Path(candidate_path).resolve() if candidate_path is not None else _default_local_holdout_candidate_answers_path(root_path)

    if destination.exists():
        return attach_contract(
            {
                "status": "consistent",
                "reason": "Local holdout candidate-answer file already exists; initializer refused to overwrite it.",
                "path": str(destination),
                "created": False,
                "overwrote_existing": False,
                "policy_boundary": [
                    "Existing local holdout candidate-answer files are preserved by default.",
                    "Initialization is a scaffold action, not holdout evaluation evidence.",
                ],
            },
            "real_task_holdout_local_candidate_initialization",
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(template_path.read_text(encoding="utf-8"), encoding="utf-8")
    return attach_contract(
        {
            "status": "consistent",
            "reason": "Local holdout candidate-answer scaffold initialized from the committed template.",
            "path": str(destination),
            "created": True,
            "overwrote_existing": False,
            "template_path": str(template_path),
            "policy_boundary": [
                "This initializer creates a local candidate-answer scaffold only and does not produce holdout evaluation evidence.",
                "The created file remains a non-committed local artifact unless the user explicitly promotes it.",
            ],
        },
        "real_task_holdout_local_candidate_initialization",
    )
