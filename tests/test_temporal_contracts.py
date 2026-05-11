from pathlib import Path
import json
import subprocess
import sys

from mathdevmcp.mcp_facade import call_mcp_tool, list_mcp_tools
from mathdevmcp.temporal_contracts import audit_temporal_contract


FIXTURES = Path(__file__).resolve().parent.parent / "benchmarks" / "fixtures"
ROOT = FIXTURES.parent.parent

SGU_BINDINGS = {
    "mu_t": {
        "code_names": ["mu_cur"],
        "forbidden_code_names": ["mu_next"],
        "role": "current state/preference wedge",
    },
    "lambda_tp1": {
        "code_names": ["lam_next"],
        "forbidden_code_names": [],
        "role": "future policy-implied marginal utility",
    },
}


def test_temporal_contract_detects_wrong_mu_next_binding():
    result = audit_temporal_contract(
        str(FIXTURES),
        "sec:sgu_marginal_utility_timing_fixture",
        str(FIXTURES / "dsge_temporal_bad.py"),
        SGU_BINDINGS,
    )

    findings = {finding["symbol"]: finding for finding in result["findings"]}
    assert result["status"] == "mismatch"
    assert findings["mu_t"]["status"] == "mismatch"
    assert findings["mu_t"]["forbidden_matches"] == ["mu_next"]
    assert findings["lambda_tp1"]["status"] == "matched"
    assert "does not solve or validate the DSGE model" in result["verification_boundary"]
    assert result["metadata"] == {"schema_version": "1.0", "contract": "temporal_contract_audit"}


def test_temporal_contract_accepts_fixed_current_mu_binding():
    result = audit_temporal_contract(
        str(FIXTURES),
        "sec:sgu_marginal_utility_timing_fixture",
        str(FIXTURES / "dsge_temporal_fixed.py"),
        SGU_BINDINGS,
    )

    findings = {finding["symbol"]: finding for finding in result["findings"]}
    assert result["status"] == "consistent"
    assert findings["mu_t"]["status"] == "matched"
    assert findings["mu_t"]["matched_names"] == ["mu_cur"]
    assert findings["lambda_tp1"]["matched_names"] == ["lam_next"]


def test_mcp_facade_exposes_temporal_contract_audit():
    tools = {tool["name"]: tool for tool in list_mcp_tools()}
    result = call_mcp_tool(
        "audit_temporal_contract",
        {
            "root": str(FIXTURES),
            "label": "sec:sgu_marginal_utility_timing_fixture",
            "code": str(FIXTURES / "dsge_temporal_bad.py"),
            "required_bindings": SGU_BINDINGS,
        },
    )

    assert tools["audit_temporal_contract"]["output_contract"] == "temporal_contract_audit"
    assert result["status"] == "mismatch"
    assert result["ok"] is True


def test_cli_audit_temporal_contract_reports_contract():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "audit-temporal-contract",
            "sec:sgu_marginal_utility_timing_fixture",
            str(FIXTURES / "dsge_temporal_bad.py"),
            "--root",
            str(FIXTURES),
            "--required-bindings",
            json.dumps(SGU_BINDINGS),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["metadata"] == {"schema_version": "1.0", "contract": "temporal_contract_audit"}
    assert payload["status"] == "mismatch"
