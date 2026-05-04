import json
import subprocess
import sys
from pathlib import Path

from mathdevmcp.claim_support import build_claim_support_packet, classify_claim


ROOT = Path(__file__).resolve().parent.parent


def test_claim_support_classifies_assumption_and_keeps_boundary():
    packet = build_claim_support_packet(
        "Assume the SDF is strictly positive.",
        claim_id="claim:sdf-positive",
        assumption=True,
        linked_labels=["eq:sdf"],
    )

    assert packet["metadata"] == {"schema_version": "1.0", "contract": "claim_support_packet"}
    assert packet["claim_status"] == "model_assumption"
    assert "not mathematical proof" in packet["evidence_boundary"]
    assert packet["linked_labels"] == ["eq:sdf"]


def test_claim_support_classifies_empirical_regularities_as_needing_data():
    packet = build_claim_support_packet("The basis is persistent in the data.", empirical=True)

    assert packet["claim_status"] == "empirical_regularity"
    assert any(finding["kind"] == "requires_data_evidence" for finding in packet["findings"])


def test_claim_support_uses_citations_without_calling_them_proof():
    packet = build_claim_support_packet(
        "This theorem is standard in affine term structure models.",
        citations=[{"id": "duffie-kan"}],
    )

    assert packet["claim_status"] == "theorem_from_cited_source"
    assert "not mathematical proof" in packet["evidence_boundary"]


def test_claim_support_cli_reports_contract():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "claim-support",
            "Assume the measurement error is Gaussian.",
            "--claim-id",
            "claim:measurement",
            "--assumption",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["metadata"]["contract"] == "claim_support_packet"


def test_classify_claim_defaults_to_open_problem():
    assert classify_claim("Could this extension hold under weaker restrictions?") == "open_problem"
