import json
import os
from pathlib import Path
import subprocess
import sys

from mathdevmcp.mcp_facade import call_mcp_tool
from mathdevmcp.release_policy import backend_environment_policy, release_readiness_report
from mathdevmcp.release_corpus import validate_release_corpus_manifest


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_release_readiness_defaults_to_base_profile(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_LATEXML_PATH", "/definitely/missing/latexml")
    monkeypatch.delenv("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", raising=False)
    monkeypatch.setenv("MATHDEVMCP_BACKEND_CONDA_ENV", "definitely-missing-backend-env")

    report = release_readiness_report(ROOT)

    assert report["metadata"] == {"schema_version": "1.0", "contract": "release_readiness_report"}
    assert report["profile"] == "base"
    assert report["profile_policy_version"]
    assert "benchmark_gate" in report["required_capabilities"]
    assert "latexml" in report["optional_capabilities"]
    assert report["status"] in {"ready", "ready_with_caveats"}
    assert any(caveat["kind"] == "latexml_optional_backend_unavailable" for caveat in report["caveats"])
    assert not any(caveat["kind"] == "private_corpus_not_configured" for caveat in report["caveats"])
    assert not any(caveat["kind"] == "lean_version_or_toolchain_caveat" for caveat in report["caveats"])
    assert not any(caveat["kind"] == "dependency_conflicts" for caveat in report["caveats"])
    assert not any(blocker["kind"] == "latexml_required_backend_unavailable" for blocker in report["blockers"])
    assert not any(blocker["kind"] == "backend_lean_dojo_unavailable" for blocker in report["blockers"])
    assert report["doctor_summary"]["capabilities"]["lean"]["kind"] == "executable"


def test_public_profile_omits_strict_profile_caveat_noise(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_LATEXML_PATH", "/definitely/missing/latexml")
    monkeypatch.delenv("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", raising=False)
    monkeypatch.setenv("MATHDEVMCP_BACKEND_CONDA_ENV", "definitely-missing-backend-env")

    report = release_readiness_report(ROOT, profile="public")
    caveat_kinds = {caveat["kind"] for caveat in report["caveats"]}

    assert report["profile"] == "public"
    assert report["status"] in {"ready", "ready_with_caveats"}
    assert "mcp_surface_consistency" in report["required_capabilities"]
    assert "private_corpus_manifest" in report["optional_capabilities"]
    assert "latexml_optional_backend_unavailable" not in caveat_kinds
    assert "private_corpus_not_configured" not in caveat_kinds
    assert "lean_version_or_toolchain_caveat" not in caveat_kinds
    assert "dependency_conflicts" not in caveat_kinds
    assert report["doctor_summary"]["capabilities"]["latexml"]["kind"] == "executable"


def test_backend_environment_policy_records_base_vs_strict_boundary():
    policy = backend_environment_policy()

    assert policy["metadata"] == {"schema_version": "1.0", "contract": "backend_environment_policy"}
    assert "do not require LeanDojo" in policy["base_policy"]
    assert "[mcp]" in policy["mcp_policy"]
    assert "toolchain download failures" in policy["lean_policy"]
    assert policy["profiles"]["base"]["requires_backend"] is False
    assert policy["profiles"]["backend"]["requires_backend"] is True


def test_latexml_profile_blocks_when_backend_unavailable(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_LATEXML_PATH", "/definitely/missing/latexml")

    report = release_readiness_report(ROOT, profile="latexml")

    assert report["profile"] == "latexml"
    assert report["status"] == "not_ready"
    assert "latexml" in report["required_capabilities"]
    assert any(blocker["kind"] == "latexml_required_backend_unavailable" for blocker in report["blockers"])


def test_private_and_full_profiles_block_without_private_manifest(monkeypatch):
    monkeypatch.delenv("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", raising=False)
    private_report = release_readiness_report(ROOT, profile="private-corpus")
    full_report = release_readiness_report(ROOT, profile="full")

    assert private_report["status"] == "not_ready"
    assert any(blocker["kind"] == "private_corpus_manifest_required" for blocker in private_report["blockers"])
    assert full_report["status"] == "not_ready"
    assert any(blocker["kind"] == "private_corpus_manifest_required" for blocker in full_report["blockers"])


def test_backend_profile_uses_configured_backend_env(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_BACKEND_CONDA_ENV", "mathdevmcp-backends")
    report = release_readiness_report(ROOT, profile="backend")

    assert report["profile"] == "backend"
    assert "lean_dojo_backend_env" in report["required_capabilities"]
    assert "private_corpus_not_configured" not in {caveat["kind"] for caveat in report["caveats"]}
    backend_blockers = [blocker for blocker in report["blockers"] if blocker["kind"] == "backend_lean_dojo_unavailable"]
    if backend_blockers:
        assert report["status"] == "not_ready"
        assert backend_blockers[0]["backend_conda_env"] == "mathdevmcp-backends"
        assert "setup_backend_env.sh" in backend_blockers[0]["install_hint"]
    else:
        assert report["status"] in {"ready", "ready_with_caveats"}


def test_backend_profile_defaults_to_documented_backend_env(monkeypatch):
    monkeypatch.delenv("MATHDEVMCP_BACKEND_CONDA_ENV", raising=False)

    report = release_readiness_report(ROOT, profile="backend")

    assert report["profile"] == "backend"
    backend_blockers = [blocker for blocker in report["blockers"] if blocker["kind"] == "backend_lean_dojo_unavailable"]
    if backend_blockers:
        assert backend_blockers[0]["backend_conda_env"] == "mathdevmcp-backends"
    else:
        assert report["status"] in {"ready", "ready_with_caveats"}


def test_backend_profile_omits_active_env_conflict_when_backend_env_isolated(monkeypatch):
    import mathdevmcp.release_policy as release_policy

    def fake_backend_check(module: str, *, package: str):
        assert module == "lean_dojo"
        assert package == "lean-dojo"
        return True, "4.20.0", "Python module lean_dojo imports in backend env"

    real_doctor = release_policy.doctor_report()

    def fake_doctor_report():
        payload = dict(real_doctor)
        payload["conflicts"] = ["active pydantic conflict from application environment"]
        return payload

    monkeypatch.setattr(release_policy, "_run_backend_python_with_default_env", fake_backend_check)
    monkeypatch.setattr(release_policy, "doctor_report", fake_doctor_report)

    report = release_policy.release_readiness_report(ROOT, profile="backend")

    caveat_kinds = {caveat["kind"] for caveat in report["caveats"]}
    assert "dependency_conflicts" not in caveat_kinds
    assert report["doctor_summary"]["conflicts"] == ["active pydantic conflict from application environment"]
    assert not any(blocker["kind"] == "backend_lean_dojo_unavailable" for blocker in report["blockers"])


def test_backend_profile_keeps_active_env_conflict_when_backend_env_missing(monkeypatch):
    import mathdevmcp.release_policy as release_policy

    def fake_backend_check(module: str, *, package: str):
        return False, None, "No backend Python interpreter is configured."

    real_doctor = release_policy.doctor_report()

    def fake_doctor_report():
        payload = dict(real_doctor)
        payload["conflicts"] = ["active pydantic conflict from application environment"]
        return payload

    monkeypatch.setattr(release_policy, "_run_backend_python_with_default_env", fake_backend_check)
    monkeypatch.setattr(release_policy, "doctor_report", fake_doctor_report)

    report = release_policy.release_readiness_report(ROOT, profile="backend")

    caveat_kinds = {caveat["kind"] for caveat in report["caveats"]}
    assert "dependency_conflicts" in caveat_kinds
    assert any(blocker["kind"] == "backend_lean_dojo_unavailable" for blocker in report["blockers"])
    assert report["doctor_summary"]["conflicts"] == ["active pydantic conflict from application environment"]


def test_release_readiness_cli_accepts_profile(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_LATEXML_PATH", "/definitely/missing/latexml")
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "mathdevmcp.cli",
            "release-readiness",
            "--root",
            str(ROOT),
            "--profile",
            "latexml",
        ],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert payload["profile"] == "latexml"
    assert payload["status"] == "not_ready"


def test_mcp_release_readiness_accepts_profile(monkeypatch):
    monkeypatch.setenv("MATHDEVMCP_LATEXML_PATH", "/definitely/missing/latexml")

    report = call_mcp_tool("release_readiness", {"root": str(ROOT), "profile": "latexml"})

    assert report["ok"] is True
    assert report["profile"] == "latexml"
    assert report["status"] == "not_ready"


def test_private_manifest_template_is_valid_json():
    data = json.loads((ROOT / "examples" / "private-corpus-manifest.template.json").read_text(encoding="utf-8"))

    assert "entries" in data
    assert {entry["domain"] for entry in data["entries"]}.issuperset(
        {"dsge_macro_finance", "stochastic_volatility", "sde_pde_numerics", "ml_llm_objective", "bayesian_elbo_vi", "computational_physics_mcmc"}
    )
    assert all(entry["privacy_class"] == "private_external" for entry in data["entries"])


def test_private_corpus_script_help_and_missing_manifest_behavior():
    help_result = subprocess.run(
        [str(ROOT / "scripts" / "validate_private_corpus.sh"), "--help"],
        check=False,
        capture_output=True,
        text=True,
    )
    missing = subprocess.run(
        [str(ROOT / "scripts" / "validate_private_corpus.sh"), str(ROOT)],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src"), "MATHDEVMCP_PRIVATE_CORPUS_MANIFEST": ""},
    )

    assert help_result.returncode == 0
    assert "MATHDEVMCP_PRIVATE_CORPUS_MANIFEST" in help_result.stdout
    assert missing.returncode == 2
    assert "private_paths_redacted" in missing.stderr


def test_validate_private_corpus_script_accepts_external_manifest(tmp_path):
    private_root = tmp_path / "private-corpus"
    private_root.mkdir()
    (private_root / "doc.tex").write_text(
        r"""
\section{Private Synthetic DSGE}
\begin{equation}
\label{eq:private-euler-equation}
E_t[m_{t+1} R_{t+1}] = 1
\end{equation}
""",
        encoding="utf-8",
    )
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "id": "private_dsge_local",
                        "domain": "dsge_macro_finance",
                        "privacy_class": "private_external",
                        "document_root": str(private_root),
                        "code_roots": [],
                        "expected_labels": ["eq:private-euler-equation"],
                        "expected_operations": ["expectation"],
                        "expected_abstentions": ["calibration_review"],
                        "seeded_false_confidence_cases": [],
                        "required_parser_backends": ["current"],
                        "release_gate_enabled": True,
                        "notes": "Synthetic temp private manifest for tests.",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    result = subprocess.run(
        [str(ROOT / "scripts" / "validate_private_corpus.sh"), str(ROOT), str(manifest)],
        check=False,
        capture_output=True,
        text=True,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["metadata"] == {"schema_version": "1.0", "contract": "private_corpus_validation_report"}
    assert payload["private_paths_redacted"] is True
    assert "<redacted-private-path>" in result.stdout
    assert str(private_root) not in result.stdout


def test_release_corpus_private_manifest_missing_root_is_blocking(tmp_path):
    manifest = tmp_path / "manifest.json"
    missing_root = tmp_path / "missing"
    manifest.write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "id": "missing_private",
                        "domain": "dsge_macro_finance",
                        "privacy_class": "private_external",
                        "document_root": str(missing_root),
                        "code_roots": [],
                        "expected_labels": ["eq:private-euler-equation"],
                        "expected_operations": ["expectation"],
                        "expected_abstentions": ["calibration_review"],
                        "seeded_false_confidence_cases": [],
                        "required_parser_backends": ["current"],
                        "release_gate_enabled": True,
                        "notes": "Missing path should block private profile.",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    validation = validate_release_corpus_manifest(FIXTURES, private_manifest=manifest)

    assert validation["status"] == "mismatch"
    assert any(finding["kind"] == "private_document_root_missing" for finding in validation["findings"])


def test_release_readiness_blocks_malformed_private_manifest(tmp_path, monkeypatch):
    manifest = tmp_path / "manifest.json"
    missing_root = tmp_path / "missing"
    manifest.write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "id": "missing_private",
                        "domain": "dsge_macro_finance",
                        "privacy_class": "private_external",
                        "document_root": str(missing_root),
                        "code_roots": [],
                        "expected_labels": ["eq:private-euler-equation"],
                        "expected_operations": ["expectation"],
                        "expected_abstentions": ["calibration_review"],
                        "seeded_false_confidence_cases": [],
                        "required_parser_backends": ["current"],
                        "release_gate_enabled": True,
                        "notes": "Missing path should block release readiness.",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", str(manifest))

    report = release_readiness_report(ROOT, profile="private-corpus")

    assert report["status"] == "not_ready"
    assert any(blocker["kind"] == "release_corpus_validation_failed" for blocker in report["blockers"])


def test_full_profile_passes_with_external_private_manifest(tmp_path, monkeypatch):
    private_root = tmp_path / "external-private-corpus"
    private_root.mkdir()
    (private_root / "code").mkdir()
    (private_root / "doc.tex").write_text(
        r"""
\section{External Sanitized Private Corpus}
\begin{equation}
\label{eq:private-euler-equation}
E_t[m_{t+1} R_{t+1}] = 1
\end{equation}
""",
        encoding="utf-8",
    )
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "entries": [
                    {
                        "id": "private_dsge_external_release_gate",
                        "domain": "dsge_macro_finance",
                        "privacy_class": "private_sanitized_external",
                        "document_root": str(private_root),
                        "code_roots": [str(private_root / "code")],
                        "expected_labels": ["eq:private-euler-equation"],
                        "expected_operations": ["expectation", "euler_residual"],
                        "expected_abstentions": ["private_calibration_assumption_review"],
                        "seeded_false_confidence_cases": ["missing_discount_factor_seed"],
                        "required_parser_backends": ["current"],
                        "release_gate_enabled": True,
                        "notes": "Temporary sanitized external corpus for full-profile tests.",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("MATHDEVMCP_PRIVATE_CORPUS_MANIFEST", str(manifest))

    report = release_readiness_report(ROOT, profile="full")

    assert report["profile"] == "full"
    assert not any(blocker["kind"] == "private_corpus_manifest_required" for blocker in report["blockers"])
    assert not any(blocker["kind"] == "private_corpus_release_gated_entries_missing" for blocker in report["blockers"])
