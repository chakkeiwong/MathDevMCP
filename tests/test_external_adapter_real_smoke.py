from __future__ import annotations

import os
from pathlib import Path

import pytest

from mathdevmcp.derivation_search_orchestrator import BranchSearchBudget, run_branch_search
from mathdevmcp.derivation_search_tree import build_branch_record, validate_branch_tree
from mathdevmcp.external_adapter_contract import p04_injected_result_from_adapter
from mathdevmcp.sage_adapter import (
    SagePolynomialObligation,
    generate_sage_polynomial_script,
    run_sage_polynomial_obligation,
    verify_sage_execution_manifest,
)


pytestmark = pytest.mark.requires_external_tool

EXPECTED_SAGE_PATH = "/usr/bin/sage"
EXPECTED_SAGE_VERSION_PREFIX = "9.5"


def _external_smoke_enabled() -> bool:
    return os.environ.get("MATHDEVMCP_ENABLE_EXTERNAL_SMOKE") == "1"


def _smoke_tree(script: str) -> dict:
    obligation_digest = "5" * 64
    root = build_branch_record(
        obligation_digest=obligation_digest,
        target="Phase 05 synthetic specialist root",
        typed_assumptions=[],
        generator={"kind": "root"},
        formalization_plan={"backend": "none", "action_kind": "backend"},
        state="formalization_blocked",
        blockers=[
            {
                "id": "blocker_root_not_executed",
                "kind": "synthetic_root",
                "problem": "The synthetic root is not a mathematical target.",
                "why": "Only the exact child is in the specialist smoke scope.",
                "required_next_evidence": "None in Phase 05.",
                "source": "p05_real_smoke",
                "evidence_refs": [],
            }
        ],
    )
    child = build_branch_record(
        obligation_digest=obligation_digest,
        target="(x + 1)**2 = x**2 + 2*x + 1",
        typed_assumptions=[
            {
                "id": "domain_x",
                "kind": "domain",
                "symbol": "x",
                "domain": "QQ",
            }
        ],
        generator={
            "kind": "rule_generated",
            "rule_id": "p05_sage_polynomial_smoke",
            "source_refs": ["tests/test_external_adapter_real_smoke.py"],
        },
        formalization_plan={
            "backend": "sage",
            "action_kind": "backend",
            "native_input": script,
            "timeout_seconds": 30,
        },
        state="ready",
        parent=root,
        blockers=[
            {
                "id": "blocker_sage_specialist_execution",
                "kind": "specialist_execution_required",
                "problem": "No current Sage executable evidence is bound to this child.",
                "why": "Phase 05 requires one genuine non-SymPy specialist action.",
                "required_next_evidence": "Run the exact Sage script and verify its manifest.",
                "source": "p05_real_smoke",
                "evidence_refs": [],
            }
        ],
    )
    root["children"].append(child)
    assert validate_branch_tree(root) == []
    return root


def test_sage_exact_polynomial_branch_live_smoke() -> None:
    if not _external_smoke_enabled():
        pytest.skip("trusted external smoke is disabled; a skip is a Phase 05 capability veto")

    configured_path = os.environ.get("MATHDEVMCP_SAGE_PATH")
    artifact_value = os.environ.get("MATHDEVMCP_P05_ARTIFACT_ROOT")
    assert configured_path == EXPECTED_SAGE_PATH
    assert artifact_value, "MATHDEVMCP_P05_ARTIFACT_ROOT is required"
    artifact_root = Path(artifact_value)
    assert artifact_root.is_absolute()
    assert Path("/tmp") in artifact_root.parents
    assert not artifact_root.exists(), "artifact root must be fresh"
    assert not artifact_root.is_symlink()

    obligation = SagePolynomialObligation(
        branch_id="placeholder_rebound_below",
        branch_lineage=("placeholder_rebound_below",),
        obligation_digest="5" * 64,
        target="(x + 1)**2 = x**2 + 2*x + 1",
        lhs="(x + 1)**2",
        rhs="x**2 + 2*x + 1",
        variable="x",
        domain="QQ",
    )
    script = generate_sage_polynomial_script(
        obligation, expected_version_prefix=EXPECTED_SAGE_VERSION_PREFIX
    ).decode("ascii")
    root = _smoke_tree(script)
    child = root["children"][0]
    bound_obligation = SagePolynomialObligation(
        branch_id=child["id"],
        branch_lineage=tuple(child["lineage"]),
        obligation_digest=child["obligation_digest"],
        target=child["target"],
        lhs="(x + 1)**2",
        rhs="x**2 + 2*x + 1",
        variable="x",
        domain="QQ",
    )

    def executor(request: dict) -> dict:
        adapter_result = run_sage_polynomial_obligation(
            bound_obligation,
            executable=configured_path,
            expected_version_prefix=EXPECTED_SAGE_VERSION_PREFIX,
            timeout_seconds=request["timeout_ms"] / 1_000,
            max_output_bytes=1_048_576,
            max_artifact_bytes=10_485_760,
            artifact_root=artifact_root,
        )
        assert adapter_result["status"] == "certified", adapter_result["reason"]
        assert adapter_result["live_tool_executed"] is True
        assert adapter_result["can_promote"] is True
        assert adapter_result["evidence"]["manifest_verified"] is True
        verified = verify_sage_execution_manifest(
            adapter_result["evidence"]["manifest_ref"]
        )
        assert verified["manifest_sha256"] == adapter_result["evidence"]["manifest_sha256"]
        return p04_injected_result_from_adapter(
            adapter_result,
            request,
            closed_blocker_ids=["blocker_sage_specialist_execution"],
        )

    result = run_branch_search(
        root,
        executor=executor,
        budget=BranchSearchBudget(
            max_targets=1,
            max_depth=1,
            max_nodes=2,
            max_attempts_total=1,
            max_attempts_per_branch=1,
            max_wall_time_seconds=45,
            max_tool_timeout_seconds=30,
            max_retrieval_calls=0,
            max_agent_calls=0,
            max_input_bytes=1_048_576,
            max_output_bytes_per_attempt=1_048_576,
            max_artifact_bytes=10_485_760,
        ),
    )
    final_child = result["final_tree"]["children"][0]
    assert final_child["state"] == "proved"
    assert final_child["blockers"] == []
    assert result["final_tree"]["state"] == "formalization_blocked"
    assert result["publication_mode"] == "disabled"
    recorded = next(
        value for key, value in result["artifacts"].items() if "/result/" in key
    )
    assert recorded["test_only"] is False
    assert recorded["live_tool_executed"] is True
    assert recorded["manifest_verified"] is True
    assert recorded["live_manifest_verification"]["integrity_state"] == "verified"
