import hashlib
import json
import subprocess
import sys
from pathlib import Path

from mathdevmcp.negative_evidence import build_negative_evidence_packet
from mathdevmcp.numeric_runner import run_numeric_diagnostic_plan
from mathdevmcp.proof_audit_v2 import audit_derivation_v2_for_label
from mathdevmcp.proof_packet import build_proof_packet_label


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_proof_packet_bundles_audit_graph_and_boundary():
    packet = build_proof_packet_label(str(FIXTURES), "eq:proof-audit-single", summary_only=True)

    assert packet["metadata"] == {"schema_version": "1.0", "contract": "proof_packet"}
    assert packet["status"] == "verified"
    assert packet["proof_audit_v2"]["metadata"]["contract"] == "proof_audit_v2_result"
    assert packet["dependency_graph"]["metadata"]["contract"] == "dependency_graph"
    assert "Only nested deterministic backend certificates" in packet["certification_boundary"]


def test_proof_packet_identity_excludes_nondeterministic_parser_runtime() -> None:
    first = build_proof_packet_label(str(FIXTURES), "eq:proof-audit-single", summary_only=True)
    second = build_proof_packet_label(str(FIXTURES), "eq:proof-audit-single", summary_only=True)

    assert first == second
    benchmark = first["proof_audit_v2"]["parser_policy"]["benchmark_report"]
    assert benchmark["durable_identity_exclusions"]
    assert all("runtime_seconds" not in item for item in benchmark["results"])


def test_negative_evidence_packet_classifies_mismatch():
    audit = audit_derivation_v2_for_label(str(FIXTURES), "eq:proof-audit-false", summary_only=True)
    packet = build_negative_evidence_packet("eq:proof-audit-false", audit)

    assert packet["metadata"] == {"schema_version": "1.0", "contract": "negative_evidence_packet"}
    assert packet["status"] == "mismatch"
    assert packet["likely_cause"] == "formula_error_or_backend_refutation"
    assert packet["actions"]


def test_exact_source_status_propagates_to_proof_and_negative_packets(tmp_path: Path) -> None:
    import hashlib

    source = tmp_path / "current.tex"
    source.write_text(r"\begin{equation}\label{eq:shared} x = y + z \end{equation}", encoding="utf-8")
    digest = hashlib.sha256(source.read_bytes()).hexdigest()

    proof = build_proof_packet_label(
        str(tmp_path),
        "eq:shared",
        file=source.name,
        source_digest=digest,
        summary_only=True,
    )
    negative = build_negative_evidence_packet("eq:shared", proof["proof_audit_v2"])

    assert proof["source"]["source_binding_status"] == "accepted_exact_source"
    assert proof["source"]["specialist_parser_readiness"] == "selected_for_proof_audit"
    assert negative["evidence"]["source_binding_status"] == "accepted_exact_source"
    assert "inconclusive:source_label_missing" not in negative["evidence"]["substatus_counts"]


def test_exact_non_equality_target_is_manual_formalization_not_missing(tmp_path: Path) -> None:
    source = tmp_path / "relation.tex"
    source.write_text(
        r"\begin{equation}\label{eq:ci} X \perp\!\!\!\perp Y \mid Z\end{equation}",
        encoding="utf-8",
    )
    digest = hashlib.sha256(source.read_bytes()).hexdigest()

    proof = build_proof_packet_label(
        str(tmp_path),
        "eq:ci",
        file=source.name,
        source_digest=digest,
        summary_only=True,
    )
    obligation = proof["proof_audit_v2"]["obligations"][0]

    assert proof["source"]["normalized_target"]["kind"] == "conditional_independence"
    assert obligation["source_text"] == proof["source"]["target"]
    assert obligation["provenance"]["relation_kind"] == "conditional_independence"
    assert obligation["substatus"] == "unverified:manual_formalization_required"
    assert "source_label_missing" not in obligation["substatus"]


def test_numeric_plan_records_reproducibility_metadata():
    result = run_numeric_diagnostic_plan(
        {"kind": "logdet_domain_check", "artifact": {"matrix": [[2.0, 0.0], [0.0, 3.0]]}, "seed": 7}
    )

    assert result["metadata"] == {"schema_version": "1.0", "contract": "numeric_diagnostic_plan_result"}
    assert result["reproducibility"]["seed"] == 7
    assert "not mathematical proof" in result["reproducibility"]["diagnostic_boundary"]


def test_cli_proof_packet_writes_optional_output(tmp_path: Path):
    output = tmp_path / "packet.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "proof-packet-label",
            "eq:proof-audit-single",
            "--root",
            str(FIXTURES),
            "--summary-only",
            "--output",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    assert json.loads(output.read_text(encoding="utf-8"))["metadata"]["contract"] == "proof_packet"
