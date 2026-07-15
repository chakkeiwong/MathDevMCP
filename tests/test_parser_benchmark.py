from pathlib import Path

import hashlib
import json
import os

import pytest

from mathdevmcp.parser_benchmark import (
    P02_FIDELITY_FIELDS,
    P02_RESULT_ROUND_PARENT,
    compare_p02_fidelity_vectors,
    compare_parser_backends,
    run_p02_parser_fidelity,
    run_parser_backend,
)
from mathdevmcp.evidence_manifest import EvidenceValidationError, canonical_json_bytes, content_digest
from tests.p02_no_backend_guard import BackendGuard, guard_is_active


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_parser_backend_current_preserves_labels_and_provenance():
    result = run_parser_backend(FIXTURES, "current")

    assert result["status"] == "parsed"
    assert result["metadata"] == {"schema_version": "1.0", "contract": "parser_backend_result"}
    assert result["labels_found"] >= 1
    assert result["quality_checks"]["label_preservation"] is True
    assert result["quality_checks"]["provenance_available"] is True
    assert "eq:proof-audit-single" in result["labels"]


def test_parser_backend_current_preserves_department_corpus_labels():
    result = run_parser_backend(FIXTURES, "current")

    assert "eq:dept-state-space-recursion" in result["labels"]
    assert "eq:dept-hmc-leapfrog" in result["labels"]
    assert "eq:macro-filter-likelihood" in result["labels"]
    assert result["details"]["missing_expected_labels"] == []
    assert result["details"]["expected_label_recall"] == 1.0
    assert result["details"]["generated_like_labels"] == []
    assert result["details"]["provenance_score"] == 1.0
    assert result["details"]["environment_count"] >= 1
    assert result["details"]["environment_type_counts"]["equation"] >= 1
    assert "doc_macro_filter_main.tex" in result["details"]["tex_files_scanned"]
    assert result["details"]["per_file_metrics"]["doc_macro_filter_main.tex"]["include_targets"] == ["doc_macro_filter_model"]
    assert result["details"]["include_status"]["resolved"]
    assert result["details"]["macro_summary"]["total_macro_definitions"] >= 1


def test_parser_backend_latexml_runs_or_reports_inconclusive():
    if guard_is_active():
        pytest.skip("legacy broad parser runner is outside the guarded Phase 02 profile")
    result = run_parser_backend(FIXTURES, "latexml")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "parser_backend_result"}
    assert result["status"] in {"parsed", "inconclusive"}
    if result["status"] == "parsed":
        assert result["quality_checks"]["label_preservation"] is True
        assert result["labels_found"] >= 1


def test_parser_backend_latexml_honors_executable_override(monkeypatch, tmp_path):
    if guard_is_active():
        pytest.skip("executable overrides are forbidden by the guarded Phase 02 profile")
    fake_latexml = tmp_path / "latexml"
    fake_latexml.write_text(
        "#!/usr/bin/env sh\n"
        "echo fake latexml >&2\n"
        "exit 2\n",
        encoding="utf-8",
    )
    fake_latexml.chmod(0o755)
    monkeypatch.setenv("MATHDEVMCP_LATEXML_PATH", str(fake_latexml))

    result = run_parser_backend(FIXTURES, "latexml")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "parser_backend_result"}
    assert result["status"] == "inconclusive"
    assert result["details"]["fatal_errors"]


def test_parser_backend_pandoc_runs_or_reports_inconclusive():
    if guard_is_active():
        pytest.skip("legacy broad parser runner is outside the guarded Phase 02 profile")
    result = run_parser_backend(FIXTURES, "pandoc")

    assert result["metadata"] == {"schema_version": "1.0", "contract": "parser_backend_result"}
    assert result["status"] in {"parsed", "inconclusive"}
    if result["status"] == "parsed":
        assert result["quality_checks"]["label_preservation"] is True
        assert result["labels_found"] >= 1


def test_compare_parser_backends_returns_ci_friendly_summary():
    if guard_is_active():
        pytest.skip("legacy recursive comparison is outside the guarded Phase 02 profile")
    result = compare_parser_backends(FIXTURES, backends=["current", "latexml", "pandoc"])

    assert result["ok"] is True
    assert result["metadata"] == {"schema_version": "1.0", "contract": "parser_benchmark_report"}
    assert {item["backend"] for item in result["results"]} == {"current", "latexml", "pandoc"}
    assert result["summary"]["total"] == 3
    assert result["summary"]["parsed"] >= 1
    assert result["summary"]["label_preserving"] >= 1
    assert set(result["summary"]["backend_comparison_matrix"]) == {"current", "latexml", "pandoc"}
    assert result["summary"]["backend_comparison_matrix"]["current"]["role_hint"] == "candidate_for_proof_audit"


def test_parser_backend_reports_duplicate_labels(tmp_path):
    (tmp_path / "duplicate.tex").write_text(
        r"""
\begin{equation}
a = a
\label{eq:duplicate}
\end{equation}

\begin{equation}
b = b
\label{eq:duplicate}
\end{equation}
""",
        encoding="utf-8",
    )

    result = run_parser_backend(tmp_path, "current")

    assert result["status"] == "parsed"
    assert result["details"]["duplicate_label_findings"] == ["eq:duplicate"]


def test_parser_backend_missing_expected_labels_do_not_get_rescued_by_generated_labels(tmp_path):
    (tmp_path / "generated.tex").write_text(
        r"""
\begin{equation}
a = a
\label{generated:eq:required}
\end{equation}
""",
        encoding="utf-8",
    )

    result = run_parser_backend(tmp_path, "current", expected_labels=["eq:required"])

    assert result["details"]["missing_expected_labels"] == ["eq:required"]
    assert result["details"]["generated_like_labels"] == ["generated:eq:required"]
    assert result["quality_checks"]["label_preservation"] is False


def test_p02_fidelity_comparison_is_lexicographic_not_a_scalar_score() -> None:
    assert tuple(P02_FIDELITY_FIELDS) == (
        "exact_requested_label_set",
        "exact_owner_label_spans",
        "exact_owned_row_spans",
        "exact_excluded_sibling_spans",
        "exact_nested_environment_stack",
        "exact_source_byte_roundtrip",
        "explicit_uncertainty_localization",
    )
    result = compare_p02_fidelity_vectors([1, 0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1, 1])
    assert result["relation"] == "current_materially_better"
    assert result["first_differing_field"] == "exact_requested_label_set"


def test_p02r3_guard_registry_is_exact_and_uses_call_class_timeouts() -> None:
    round_ref = P02_RESULT_ROUND_PARENT / "rr01"
    guard = BackendGuard(round_root=round_ref, action="parser_fidelity_tests", formal=True)

    assert len(guard._expected_parser_calls) == 28
    assert sum(key.endswith(":version") for key in guard._expected_parser_calls) == 2
    environment = {
        key: value.replace("RR", round_ref.as_posix())
        for key, value in guard._parser_profile["environment"].items()
    }
    for backend, executable in guard._parser_profile["executables"].items():
        kwargs = {
            "capture_output": True,
            "check": False,
            "cwd": ROOT,
            "env": environment,
            "timeout": executable["version_timeout_seconds"],
        }
        assert guard._parser_call_key(list(executable["version_argv"]), kwargs) == f"{backend}:version"
        assert guard._parser_call_key(
            list(executable["version_argv"]),
            {**kwargs, "timeout": executable["version_timeout_seconds"] - 1},
        ) is None
        assert guard._parser_call_key(
            list(executable["version_argv"]),
            {**kwargs, "text": False},
        ) is None
        source_ref = guard._parser_profile["source_allowlist"][0]
        source_key = f"{backend}:{source_ref}"
        source_kwargs = {**kwargs, "timeout": executable["source_timeout_seconds"]}
        assert guard._parser_call_key(guard._expected_parser_calls[source_key], source_kwargs) == source_key
        assert guard._parser_call_key(
            guard._expected_parser_calls[source_key],
            {**source_kwargs, "timeout": executable["version_timeout_seconds"]},
        ) == (source_key if executable["source_timeout_seconds"] == executable["version_timeout_seconds"] else None)
    assert guard._subprocess_is_forbidden(["printf", "ignored"], {"shell": True}) == (
        True,
        "shell_command",
    )
    assert guard._subprocess_is_forbidden(
        ["/usr/bin/env", "-i", "PATH=/usr/bin:/bin", "/usr/bin/lean", "Main.lean"],
        {},
    ) == (True, "wrapped_mathematical_backend_executable")
    assert guard._subprocess_is_forbidden(["/usr/bin/env", "/bin/bash", "script.sh"], {}) == (
        True,
        "shell_executable",
    )
    assert guard._subprocess_is_forbidden(
        ["/usr/bin/env", "python", "-c", "import sympy"],
        {},
    ) == (True, "unreviewed_python_subprocess")
    assert guard._subprocess_is_forbidden(
        ["/usr/bin/env", "/opt/runtime/python3.12", "-c", "print('not executed')"],
        {},
    ) == (True, "unreviewed_python_subprocess")
    assert guard._argv(("/usr/bin/latexml",), {}) == ["/usr/bin/latexml"]


@pytest.mark.parametrize("name", ["system", "execv", "spawnv", "posix_spawn"])
def test_p02r2_guard_intercepts_direct_os_process_launch(monkeypatch: pytest.MonkeyPatch, name: str) -> None:
    if not hasattr(os, name):
        pytest.skip(f"os.{name} is unavailable on this platform")
    guard = object.__new__(BackendGuard)
    guard._patches = []

    def forbidden(kind, target, details):
        raise RuntimeError(f"blocked:{kind}:{target}:{details['positional_count']}")

    guard.forbidden = forbidden
    guard._patch_os_process_launch()
    try:
        with pytest.raises(RuntimeError, match=rf"blocked:python_entry_point:os\.{name}"):
            getattr(os, name)("not-executed")
    finally:
        for owner, attribute, original, replacement in reversed(guard._patches):
            if getattr(owner, attribute) is replacement:
                setattr(owner, attribute, original)


def test_p02r2_runner_seals_raw_calls_before_observations_and_projections(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from mathdevmcp import extraction_evidence
    from mathdevmcp import parser_benchmark

    round_ref = (P02_RESULT_ROUND_PARENT / "rr01").as_posix()
    round_path = tmp_path / round_ref
    round_path.mkdir(parents=True)
    (round_path / "implementation-round-sha256.txt").write_bytes(b"synthetic manifest\n")
    sources = [f"synthetic/source-{index:02d}.tex" for index in range(13)]
    for index, source_ref in enumerate(sources):
        path = tmp_path / source_ref
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(f"source {index}\n".encode("utf-8"))
    profile = {
        "executables": {
            "latexml": {
                "path": "/synthetic/latexml",
                "version_argv": ["/synthetic/latexml", "--VERSION"],
                "fidelity_argv_template": [
                    "/synthetic/latexml",
                    "--log=RR/parser/latexml/CASE.log",
                    "--destination=RR/parser/latexml/CASE.xml",
                    "SOURCE",
                ],
                "version_timeout_seconds": 60,
                "source_timeout_seconds": 180,
            },
            "pandoc": {
                "path": "/synthetic/pandoc",
                "version_argv": ["/synthetic/pandoc", "--version"],
                "fidelity_argv_template": ["/synthetic/pandoc", "SOURCE"],
                "version_timeout_seconds": 30,
                "source_timeout_seconds": 30,
            },
        },
        "source_allowlist": sources,
        "environment": {"HOME": "RR/parser/home", "PATH": "/synthetic"},
        "fidelity_vector_fields_in_priority_order": list(P02_FIDELITY_FIELDS),
    }
    events: list[str] = []
    calls: list[tuple[list[str], int]] = []

    def fake_run(root, argv, *, environment, timeout):
        assert root == tmp_path
        assert environment == {
            "HOME": f"{round_ref}/parser/home",
            "PATH": "/synthetic",
        }
        calls.append((list(argv), timeout))
        if argv[0] == "/synthetic/latexml" and argv[1] != "--VERSION":
            log_ref = argv[1].split("=", 1)[1]
            output_ref = argv[2].split("=", 1)[1]
            (tmp_path / log_ref).write_bytes(b"")
            (tmp_path / output_ref).write_bytes(b"<document/>")
        if argv[1] == "--version" or argv[1] == "--VERSION":
            stdout = f"{Path(argv[0]).name} synthetic-version\n".encode("utf-8")
        elif argv[0] == "/synthetic/pandoc":
            stdout = b'{"blocks":[],"meta":{},"pandoc-api-version":[1]}\n'
        else:
            stdout = b""
        return 0, stdout, b"", False, 1

    source_receipt_keys = {
        "argv",
        "backend",
        "case_token",
        "environment",
        "exit_code",
        "log",
        "output",
        "schema_version",
        "source_ref",
        "source_sha256_after",
        "source_sha256_before",
        "stderr",
        "stdout",
        "timed_out",
        "timeout_seconds",
        "version_receipt_ref",
        "version_receipt_sha256",
        "wall_time_ns",
    }

    def raw_receipts() -> list[Path]:
        return sorted((round_path / "parser/receipts").glob("*-raw.json"))

    def fake_observations(root, received_round_ref, manifest_ref):
        assert root == tmp_path
        assert received_round_ref == round_ref
        assert manifest_ref == f"{round_ref}/implementation-round-sha256.txt"
        receipts = raw_receipts()
        assert len(receipts) == 28
        versions = {}
        for backend in profile["executables"]:
            path = round_path / f"parser/receipts/{backend}-version-raw.json"
            record = json.loads(path.read_text(encoding="utf-8"))
            extraction_evidence.validate_parser_version_receipt(
                tmp_path,
                record,
                round_ref=round_ref,
                backend=backend,
                profile=profile,
            )
            versions[backend] = {
                "ref": path.relative_to(tmp_path).as_posix(),
                "sha256": content_digest(path.read_bytes()),
            }
        source_records = []
        for path in receipts:
            if "-version-raw.json" in path.name:
                continue
            record = json.loads(path.read_text(encoding="utf-8"))
            extraction_evidence.validate_parser_source_receipt(
                tmp_path,
                record,
                round_ref=round_ref,
                backend=record["backend"],
                source_ref=record["source_ref"],
                version=versions[record["backend"]],
                profile=profile,
            )
            source_records.append(record)
        assert len(source_records) == 26
        assert all(set(record) == source_receipt_keys for record in source_records)
        forbidden = {
            "requested_labels",
            "expected_labels",
            "observed_labels",
            "fidelity_vector",
            "comparison_to_current",
            "capability_status",
            "current",
            "oracle",
        }
        assert all(not (set(record) & forbidden) for record in source_records)
        assert not any((round_path / "parser/expected-values").iterdir())
        events.append("raw-observations")
        return [
            {
                "ref": f"{round_ref}/parser/observations/pandoc-synthetic-raw-output.json",
                "record": {
                    "raw_observable_field": "document_structural_label_set",
                    "observed_value": ["eq:synthetic", "eq:unscoped-extra"],
                },
            }
        ]

    def fake_projections(root, received_round_ref):
        observation_ref = f"{round_ref}/parser/observations/pandoc-synthetic-raw-output.json"
        assert (tmp_path / observation_ref).is_file()
        assert len(raw_receipts()) == 28
        events.append("expected-projections")
        return [
            {
                "ref": f"{round_ref}/parser/expected-values/synthetic-exact-requested-label-set.json",
                "record": {
                    "expected_value": ["eq:synthetic"],
                    "observable_field": "exact_requested_label_set",
                    "schema_version": "p02r2_expected_label_value_projection@1",
                    "source_ref": sources[0],
                    "source_sha256": content_digest((tmp_path / sources[0]).read_bytes()),
                },
            }
        ]

    comparison = {"schema_version": "synthetic_p02r2_parser_comparison@1"}

    def fake_comparison(root, received_round_ref, manifest_ref):
        projection_ref = f"{round_ref}/parser/expected-values/synthetic-exact-requested-label-set.json"
        assert (tmp_path / projection_ref).is_file()
        events.append("comparison")
        return comparison

    def fake_verify(root, comparison_ref, manifest_ref):
        raw = (tmp_path / comparison_ref).read_bytes()
        assert raw == canonical_json_bytes(comparison)
        events.append("verify")
        return {"ref": comparison_ref, "sha256": content_digest(raw), "record": comparison}

    def fake_timeout_gate(root, received_round_ref, manifest_ref):
        assert root == tmp_path
        assert received_round_ref == round_ref
        assert manifest_ref == f"{round_ref}/implementation-round-sha256.txt"
        return {
            "all_invocations_completed_within_ceiling": True,
            "source_timeout_count": 0,
            "timed_out_invocation_count": 0,
            "version_timeout_count": 0,
        }

    monkeypatch.setattr(parser_benchmark, "_p02_root", lambda: tmp_path)
    monkeypatch.setattr(parser_benchmark, "_p02_load_profile", lambda root: profile)
    monkeypatch.setattr(parser_benchmark, "_p02_run", fake_run)
    monkeypatch.setattr(extraction_evidence, "build_parser_raw_observations", fake_observations, raising=False)
    monkeypatch.setattr(extraction_evidence, "build_expected_value_projections", fake_projections, raising=False)
    monkeypatch.setattr(extraction_evidence, "build_parser_comparison", fake_comparison, raising=False)
    monkeypatch.setattr(extraction_evidence, "verify_parser_comparison", fake_verify, raising=False)
    monkeypatch.setattr(extraction_evidence, "verify_parser_timeout_gate", fake_timeout_gate, raising=False)

    result = run_p02_parser_fidelity(round_ref)

    assert len(calls) == 28
    assert [timeout for argv, timeout in calls if argv[0] == "/synthetic/latexml" and argv[1] == "--VERSION"] == [60]
    assert [timeout for argv, timeout in calls if argv[0] == "/synthetic/latexml" and argv[1] != "--VERSION"] == [180] * 13
    assert [timeout for argv, timeout in calls if argv[0] == "/synthetic/pandoc"] == [30] * 14
    assert result["version_invocation_count"] == 2
    assert result["source_invocation_count"] == 26
    assert result["observation_artifact_count"] == 1
    assert result["projection_artifact_count"] == 1
    assert result["timed_out_invocation_count"] == 0
    assert events == ["raw-observations", "expected-projections", "comparison", "verify"]


def test_p02r2_generator_rejects_parser_tampering_before_bundle_build(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    from scripts import generate_p02_extraction_evidence as generator
    from mathdevmcp import extraction_evidence

    round_ref = (P02_RESULT_ROUND_PARENT / "rr01").as_posix()
    monkeypatch.setenv("MATHDEVMCP_P02_ACTION", "generate_extraction_bundle")
    monkeypatch.setenv("MATHDEVMCP_P02_DISPATCH_DEPTH", "1")
    monkeypatch.setenv("MATHDEVMCP_P02_ROUND_ROOT", round_ref)
    monkeypatch.setattr(generator, "_root", lambda: tmp_path)

    class SyntheticGuard:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, traceback):
            return False

    monkeypatch.setattr(
        generator,
        "_load_install_guard",
        lambda root, round_ref: lambda **kwargs: SyntheticGuard(),
    )
    refs = {
        "bundle_index": f"{round_ref}/extraction-bundle/bundle-index.json",
        "obligations": f"{round_ref}/extraction-bundle/obligations.json",
        "reconstruction_summary": f"{round_ref}/extraction-bundle/reconstruction-summary.json",
        "parser_comparison": f"{round_ref}/parser/parser-comparison.json",
        "mutation_matrix": f"{round_ref}/summaries/mutation-ambiguity-matrix.json",
        "backend_ledger_index": f"{round_ref}/ledgers/backend-ledger-index.json",
    }
    monkeypatch.setattr(extraction_evidence, "extraction_artifact_refs", lambda value: refs)
    build_calls: list[str] = []
    monkeypatch.setattr(
        extraction_evidence,
        "verify_parser_comparison",
        lambda *args, **kwargs: (_ for _ in ()).throw(EvidenceValidationError("tampered parser comparison")),
        raising=False,
    )
    monkeypatch.setattr(
        extraction_evidence,
        "build_obligation_bundle",
        lambda *args, **kwargs: build_calls.append("obligations"),
    )
    monkeypatch.setattr(
        extraction_evidence,
        "build_reconstruction_summary",
        lambda *args, **kwargs: build_calls.append("reconstruction"),
    )
    monkeypatch.setattr(
        extraction_evidence,
        "build_mutation_matrix",
        lambda *args, **kwargs: build_calls.append("mutation"),
    )

    with pytest.raises(EvidenceValidationError, match="tampered parser comparison"):
        generator.main(["--round-root", round_ref])

    assert build_calls == []
    assert all(not (tmp_path / ref).exists() for key, ref in refs.items() if key != "parser_comparison")


def test_p02r3_generator_loads_exact_manifest_bound_guard(tmp_path: Path) -> None:
    from scripts import generate_p02_extraction_evidence as generator

    round_ref = (P02_RESULT_ROUND_PARENT / "rr01").as_posix()
    guard_raw = (ROOT / generator.GUARD_REF).read_bytes()
    guard_path = tmp_path / generator.GUARD_REF
    guard_path.parent.mkdir(parents=True)
    guard_path.write_bytes(guard_raw)
    manifest_path = tmp_path / round_ref / "implementation-round-sha256.txt"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_bytes(f"{content_digest(guard_raw)}  {generator.GUARD_REF}\n".encode())

    install_guard = generator._load_install_guard(tmp_path, round_ref)

    assert callable(install_guard)
    assert install_guard.__module__ == "_mathdevmcp_p02_no_backend_guard"
    guard_path.write_bytes(guard_raw + b"\n")
    with pytest.raises(EvidenceValidationError, match="initialized round manifest"):
        generator._load_install_guard(tmp_path, round_ref)


def test_formal_p02_parser_action_runs_the_exact_reviewed_profile() -> None:
    round_root = os.environ.get("MATHDEVMCP_P02_ROUND_ROOT")
    action = os.environ.get("MATHDEVMCP_P02_ACTION")
    if round_root is None or action != "parser_fidelity_tests":
        pytest.skip("the real specialist comparison runs only inside the formal parser-fidelity action")

    result = run_p02_parser_fidelity(round_root)

    assert result["version_invocation_count"] == 2
    assert result["source_invocation_count"] == 26
    assert result["projection_artifact_count"] == 13
    assert result["comparison_ref"] == f"{round_root}/parser/parser-comparison.json"
    assert result["comparison"]["parser_veto"] is False
    assert result["comparison"]["current_reconstruction_exact"] is True
    assert result["timeout_gate"]["all_invocations_completed_within_ceiling"] is True
    assert result["timed_out_invocation_count"] == 0
