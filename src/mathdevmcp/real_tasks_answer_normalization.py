from __future__ import annotations

"""Bounded answer normalization for a tiny whitelist of public real-task cases."""

from typing import Any

from .contracts import attach_contract
from .real_tasks_scoring import _normalize_text


_SUPPORTED_CASES = {
    "MF-03-hmc-helper-nonclaim-boundary",
    "MF-04-short-hmc-acceptance-veto-diagnosis",
    "DH-06-densesoap-source-contract-mismatch",
}


def _find_claims(answer_text: str, candidates: list[str]) -> list[str]:
    normalized = _normalize_text(answer_text)
    return [item for item in candidates if _normalize_text(item) in normalized]


def _normalize_mf03(case_id: str, answer_text: str) -> dict:
    normalized = _normalize_text(answer_text)
    required_anchors = [
        "numerical-stability helpers",
        "mass-matrix",
        "ESS",
        "R-hat",
        "not structural-identification tests",
    ]
    missing = [item for item in required_anchors if _normalize_text(item) not in normalized]
    if missing:
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "MF-03 answer is missing required lexical anchors for safe normalization.",
                "case_id": case_id,
                "candidate": None,
                "diagnostics": {
                    "normalization_path": "mf03_whitelist",
                    "missing_anchors": missing,
                },
            },
            "real_task_answer_normalization",
        )
    return attach_contract(
        {
            "status": "consistent",
            "reason": "MF-03 answer normalized using the bounded whitelist path.",
            "case_id": case_id,
            "candidate": {
                "case_id": case_id,
                "status": "consistent",
                "substatus": "helper_nonclaim_boundary_preserved",
                "labels": [],
                "evidence_class": "engineering_helper_regression",
                "summary_text": answer_text,
                "claims": _find_claims(
                    answer_text,
                    [
                        "These tests establish structural identification.",
                        "These tests validate the posterior.",
                        "These tests prove sampler convergence for the model.",
                    ],
                ),
                "next_actions": ["Use separate model-level diagnostics for identification or posterior claims."],
            },
            "diagnostics": {
                "normalization_path": "mf03_whitelist",
                "missing_anchors": [],
            },
        },
        "real_task_answer_normalization",
    )


def _normalize_mf04(case_id: str, answer_text: str) -> dict:
    normalized = _normalize_text(answer_text)
    required_anchors = [
        "inconclusive",
        "trusted same-process GPU execution",
        "trusted execution provenance",
        "not authorized",
    ]
    missing = [item for item in required_anchors if _normalize_text(item) not in normalized]
    if missing:
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "MF-04 answer is missing required lexical anchors for safe normalization.",
                "case_id": case_id,
                "candidate": None,
                "diagnostics": {
                    "normalization_path": "mf04_whitelist",
                    "missing_anchors": missing,
                },
            },
            "real_task_answer_normalization",
        )
    return attach_contract(
        {
            "status": "consistent",
            "reason": "MF-04 answer normalized using the bounded whitelist path.",
            "case_id": case_id,
            "candidate": {
                "case_id": case_id,
                "status": "inconclusive",
                "substatus": "trusted_gpu_provenance_blocked",
                "labels": [],
                "evidence_class": "diagnostic_blocked_execution_note",
                "summary_text": answer_text,
                "claims": _find_claims(
                    answer_text,
                    [
                        "short HMC pilot gate closure: authorized",
                        "synthetic or empirical HMC pilot: authorized",
                        "overnight or full estimation launch: authorized",
                    ],
                ),
                "next_actions": ["fix the diagnostic blocker or revise under Claude/Codex review"],
            },
            "diagnostics": {
                "normalization_path": "mf04_whitelist",
                "missing_anchors": [],
            },
        },
        "real_task_answer_normalization",
    )


def _normalize_dh06(case_id: str, answer_text: str) -> dict:
    normalized = _normalize_text(answer_text)
    required_anchors = [
        "diagnostic only",
        "material default mismatch",
        "step/cadence mismatch",
        "no official soap parity claim",
    ]
    missing = [item for item in required_anchors if _normalize_text(item) not in normalized]
    if missing:
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "DH-06 answer is missing required lexical anchors for safe normalization.",
                "case_id": case_id,
                "candidate": None,
                "diagnostics": {
                    "normalization_path": "dh06_whitelist",
                    "missing_anchors": missing,
                },
            },
            "real_task_answer_normalization",
        )
    return attach_contract(
        {
            "status": "consistent",
            "reason": "DH-06 answer normalized using the bounded whitelist path.",
            "case_id": case_id,
            "candidate": {
                "case_id": case_id,
                "status": "mismatch",
                "substatus": "diagnostic_only_source_contract_mismatch",
                "labels": [],
                "evidence_class": "diagnostic_source_contract_mismatch",
                "summary_text": answer_text,
                "claims": _find_claims(
                    answer_text,
                    [
                        "official SOAP parity is established",
                        "default optimizer policy should be promoted",
                        "downstream DSGE/HMC readiness is established",
                    ],
                ),
                "next_actions": ["Keep both TensorFlow DenseSOAP surfaces diagnostic-only unless a new bounded optimizer plan is approved."],
            },
            "diagnostics": {
                "normalization_path": "dh06_whitelist",
                "missing_anchors": [],
            },
        },
        "real_task_answer_normalization",
    )


def normalize_real_task_answer(case_id: str, answer_text: str) -> dict:
    if case_id not in _SUPPORTED_CASES:
        return attach_contract(
            {
                "status": "inconclusive",
                "reason": "This case is not supported by the bounded normalization prototype.",
                "case_id": case_id,
                "candidate": None,
                "diagnostics": {
                    "normalization_path": "unsupported_case",
                    "missing_anchors": [],
                },
            },
            "real_task_answer_normalization",
        )
    if case_id == "MF-03-hmc-helper-nonclaim-boundary":
        return _normalize_mf03(case_id, answer_text)
    if case_id == "MF-04-short-hmc-acceptance-veto-diagnosis":
        return _normalize_mf04(case_id, answer_text)
    return _normalize_dh06(case_id, answer_text)
