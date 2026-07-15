from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts/run_p08c1_target_fidelity_replay.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("p08c1_target_fidelity_runner", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


p08c1 = _load_runner()


def test_immutable_p08c_cash_flow_mismatch_is_explicit() -> None:
    extraction = p08c1._require_frozen_inputs()
    obligations = p08c1._obligations_by_label(extraction)

    diagnostic = p08c1._stale_p08c_diagnostic(obligations)

    assert diagnostic["classification"] == "continuation_row_only_target_fidelity_defect"
    assert diagnostic["p08a_obligation_digest"] == (
        "7301b910ea0fe118e3ad38d2d69c6c9cd6e924aba15fb1e1147e710bdfe2b5a0"
    )
    assert diagnostic["p08c_lhs"] is None
    assert diagnostic["p08c_rhs"] is None
    assert diagnostic["exact_obligation_record_match"] is False


def test_replay_requires_explicit_cpu_only_boundary(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)

    with pytest.raises(p08c1.ReplayError, match="CUDA_VISIBLE_DEVICES=-1"):
        p08c1._require_runtime_boundary()


def test_git_record_hashes_binary_status_output() -> None:
    record = p08c1._git_record()

    assert len(record["commit"]) == 40
    assert record["dirty"] is True
    assert len(record["status_sha256"]) == 64
