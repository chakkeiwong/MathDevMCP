from __future__ import annotations

"""Validation helpers for downstream-agent usefulness prompt fixtures."""

from collections import Counter, defaultdict
from pathlib import Path
import re
from typing import Any


CONDITIONS: tuple[str, ...] = ("A_task_only", "B_evidence_only", "C_human_framed")

A_FORBIDDEN_PAYLOAD_TERMS: tuple[str, ...] = (
    "evidence_class_for_evaluator",
    "expected_output_family_for_evaluator",
    "observed_status",
    "evidence_class",
    "decisive_backend_evidence",
    "counterexample",
    "proof_or_derivation_steps",
    "gap_ledger",
    "assumption_ledger",
    "machine_evidence_ledger",
    "human_framed_packet_reasoning",
    "recommended_next_action",
)

B_FORBIDDEN_PAYLOAD_TERMS: tuple[str, ...] = (
    "human_framed_packet_reasoning",
    "narrative_answer",
    "recommended_next_action",
)


def _contains_payload_term(text: str, term: str) -> bool:
    pattern = rf"(?<![A-Za-z0-9_]){re.escape(term)}(?![A-Za-z0-9_])"
    return re.search(pattern, text) is not None


def validate_downstream_prompt_contract(
    prompt_manifest: dict[str, Any],
    *,
    root: str | Path = ".",
) -> list[str]:
    """Return deterministic prompt-condition contract errors.

    The validator is intentionally stricter than JSON schema validation. It
    checks the A/B/C information boundary used by the local downstream-agent
    usefulness benchmark so evaluator-only labels cannot leak into task-only
    prompts.
    """
    errors: list[str] = []
    if not isinstance(prompt_manifest, dict):
        return ["prompt_manifest must be an object"]

    prompts = prompt_manifest.get("prompts")
    if not isinstance(prompts, list):
        return ["prompts must be a list"]

    root_path = Path(root)
    counts: Counter[str] = Counter()
    by_case: dict[str, set[str]] = defaultdict(set)
    prompt_ids: set[str] = set()

    for index, prompt in enumerate(prompts):
        if not isinstance(prompt, dict):
            errors.append(f"prompts[{index}] must be an object")
            continue
        prompt_id = prompt.get("prompt_id")
        condition = prompt.get("condition")
        case_id = prompt.get("case_id")
        rel_path = prompt.get("path")
        if not isinstance(prompt_id, str) or not prompt_id:
            errors.append(f"prompts[{index}].prompt_id must be a non-empty string")
            continue
        if prompt_id in prompt_ids:
            errors.append(f"{prompt_id}: duplicate prompt_id")
        prompt_ids.add(prompt_id)
        if condition not in CONDITIONS:
            errors.append(f"{prompt_id}: condition must be one of {', '.join(CONDITIONS)}")
            continue
        if not isinstance(case_id, str) or not case_id:
            errors.append(f"{prompt_id}: case_id must be a non-empty string")
        else:
            by_case[case_id].add(condition)
        counts[condition] += 1
        if not isinstance(rel_path, str) or not rel_path:
            errors.append(f"{prompt_id}: path must be a non-empty string")
            continue
        path = root_path / rel_path
        if not path.exists():
            errors.append(f"{prompt_id}: prompt file does not exist: {rel_path}")
            continue
        text = path.read_text(encoding="utf-8")
        if condition == "A_task_only":
            leaked = [term for term in A_FORBIDDEN_PAYLOAD_TERMS if _contains_payload_term(text, term)]
            for term in leaked:
                errors.append(f"{prompt_id}: A_task_only prompt leaks forbidden payload term {term}")
        elif condition == "B_evidence_only":
            leaked = [term for term in B_FORBIDDEN_PAYLOAD_TERMS if _contains_payload_term(text, term)]
            for term in leaked:
                errors.append(f"{prompt_id}: B_evidence_only prompt leaks human-framing term {term}")

    for condition in CONDITIONS:
        if counts[condition] == 0:
            errors.append(f"condition {condition} has no prompts")

    for case_id, seen in sorted(by_case.items()):
        missing = [condition for condition in CONDITIONS if condition not in seen]
        if missing:
            errors.append(f"{case_id}: missing conditions {', '.join(missing)}")

    return errors
