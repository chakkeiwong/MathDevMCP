from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts/run_p08d_frozen_payload_replay.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("p08d_payload_runner", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


p08d = _load_runner()


def test_runner_requires_explicit_cpu_only_boundary(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)

    with pytest.raises(p08d.ReplayError, match="CUDA_VISIBLE_DEVICES=-1"):
        p08d._runtime_boundary()


def test_runner_binds_passing_p08c1_inputs() -> None:
    audits = p08d._frozen_inputs()

    assert [target["label"] for target in audits["card"]["targets"]] == [
        "eq:panel-npv-functional",
        "eq:incremental-cash-flow",
        "eq:incremental-npv",
    ]
    assert [target["label"] for target in audits["risky"]["targets"]] == [
        "eq:foc-k",
        "eq:foc-b",
    ]


def test_runner_parser_keeps_create_and_verify_explicit() -> None:
    parser = p08d._parser()
    create = parser.parse_args(["create"])
    verify = parser.parse_args(
        [
            "verify",
            "--run-root",
            ".local/mathdevmcp/evidence/p08-20260714/p08d/example",
            "--expected-decision-digest",
            "1" * 64,
        ]
    )

    assert create.handler is p08d._create
    assert verify.handler is p08d._verify
    assert verify.expected_decision_digest == "1" * 64
