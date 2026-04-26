from pathlib import Path
import os
import shutil
import subprocess

from mathdevmcp.lean_export import export_lean_obligations
from mathdevmcp.proof_audit import audit_derivation_for_label


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def _single_obligation():
    audit = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-single", backend="sympy")
    return audit["obligations"]


def test_export_lean_obligations_builds_stable_nat_skeleton():
    result = export_lean_obligations(_single_obligation(), namespace="MathDevMCP", target="Nat")

    assert result["status"] == "skeleton_only"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "lean_export_result"}
    artifact = result["artifacts"][0]
    assert artifact["theorem_name"] == "mathdevmcp_obligation_1"
    assert "namespace MathDevMCP" in artifact["lean_source"]
    assert "theorem mathdevmcp_obligation_1 (a b : Nat) : a + b = b + a := by" in artifact["lean_source"]
    assert "sorry" in artifact["lean_source"]
    assert artifact["formalization_status"] == "skeleton_only"
    assert artifact["source_obligation_id"] == "obligation_1"


def test_lean_skeleton_with_sorry_compiles_but_is_not_verified(tmp_path):
    result = export_lean_obligations(_single_obligation(), namespace="MathDevMCP", target="Nat")
    source = result["artifacts"][0]["lean_source"]
    lean_file = tmp_path / "Skeleton.lean"
    lean_file.write_text(source, encoding="utf-8")

    env = dict(os.environ)
    env["PATH"] = f"{Path.home() / '.elan' / 'bin'}:{env.get('PATH', '')}"
    lean = shutil.which("lean", path=env["PATH"])
    assert lean is not None
    completed = subprocess.run([lean, str(lean_file)], check=False, capture_output=True, text=True, env=env)

    assert completed.returncode == 0, completed.stderr
    assert result["artifacts"][0]["certified"] is False
    assert result["counts"]["verified"] == 0


def test_export_lean_obligations_marks_kalman_notation_as_needing_human_formalization():
    audit = audit_derivation_for_label(str(FIXTURES), "eq:proof-audit-kalman", backend="sympy")
    result = export_lean_obligations(audit["obligations"], namespace="MathDevMCP", target="Nat")

    artifact = result["artifacts"][0]
    assert artifact["formalization_status"] == "needs_human_formalization"
    assert artifact["certified"] is False
    assert artifact["lean_source"] == ""
    assert "source_text" in artifact


def test_export_lean_obligations_surfaces_missing_types_for_raw_target():
    result = export_lean_obligations(_single_obligation(), namespace="MathDevMCP", target="raw")

    artifact = result["artifacts"][0]
    assert artifact["formalization_status"] == "missing_type_assumptions"
    assert artifact["missing_assumptions"] == ["target type for symbols"]
    assert artifact["certified"] is False


def test_export_lean_obligations_sanitizes_theorem_names_and_preserves_provenance():
    obligations = [
        {
            "id": "bad id/one",
            "lhs": "x + y",
            "rhs": "y + x",
            "source_text": "x + y = y + x",
            "classification": "sympy",
            "status": "verified",
            "evidence": [],
            "provenance": {"label": "eq:test", "file": "doc.tex", "line_start": 3, "line_end": 3},
        }
    ]

    result = export_lean_obligations(obligations, namespace="MathDevMCP", target="Nat")

    artifact = result["artifacts"][0]
    assert artifact["theorem_name"] == "mathdevmcp_bad_id_one"
    assert artifact["provenance"] == obligations[0]["provenance"]
