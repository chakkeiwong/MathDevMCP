from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import py_compile
import subprocess
import sys
from types import SimpleNamespace

import pytest

from mathdevmcp.document_derivation_response import (
    build_document_derivation_audit_request,
    compile_document_derivation_response,
    expand_document_derivation_action,
    validate_document_derivation_response,
)
from mathdevmcp.failure_ledgers import (
    build_status_entry,
    rank_repair_branches_partial_order,
    select_next_discriminating_action,
)


ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts/run_p08c_frozen_workflow.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("p08c_runner_for_tests", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


p08c = _load_runner()


def _source_ref(label: str) -> dict:
    return {
        "file": "paper.tex",
        "label": label,
        "line_start": 10,
        "line_end": 10,
        "evidence_ref": f"source://{label}",
        "snippet": "x / x = 1",
    }


def _raw_audit(document: str = "card") -> tuple[dict, dict]:
    binding = p08c.SOURCE_BINDINGS[document]
    targets = []
    for index, label in enumerate(binding["target_labels"]):
        target_id = f"target-{index}"
        blocker = {
            "id": f"blocker-{index}",
            "kind": "missing_assumption",
            "problem": "A nonzero-domain condition is not yet stated.",
            "why": "Division is undefined on the singular set.",
            "required_next_evidence": "Record a source-bound nonzero-domain statement.",
            "evidence_refs": [f"evidence://blocker/{index}"],
            "source_refs": [_source_ref(label)],
        }
        scope = {
            "obligation_id": f"obligation-{index}",
            "target": f"target expression {index}",
            "candidate_conclusion": f"target expression {index}",
            "branch_ids": [f"branch-{index}"],
            "source_spans": [
                {
                    "file": "paper.tex",
                    "start_byte": index * 10,
                    "end_byte": index * 10 + 9,
                    "label": label,
                }
            ],
            "closed_blocker_scope": ["missing_assumption"],
        }
        ledger = build_status_entry(
            status="missing_assumption",
            origin_id=f"attempt-{index}",
            target_id=target_id,
            scope=scope,
            problem=blocker["problem"],
            why=blocker["why"],
            source_refs=[f"source://{label}"],
            evidence_refs=[f"evidence://blocker/{index}"],
        )
        branch = {
            "id": f"branch-{index}",
            "obligation_id": f"obligation-{index}",
            "target": f"target expression {index}",
            "candidate_conclusion": f"target expression {index}",
            "exact_verified_evidence": False,
            "ledgers": [ledger],
            "typed_assumptions": [],
            "covered_obligation_ids": [f"obligation-{index}"],
            "execution_cost": None,
        }
        action = select_next_discriminating_action(
            rank_repair_branches_partial_order([branch]),
            [ledger],
        )
        targets.append(
            {
                "id": target_id,
                "row_id": f"row-{index}",
                "row_index": index,
                "label": label,
                "location": f"paper.tex > {label} > line {10 + index}",
                "claim_type": "algebraic_identity",
                "status": "blocked",
                "publication_mode": "disabled",
                "promotion": {"can_promote": False, "reason": "publication disabled"},
                "failure_classifications": ["mathematical_gap"],
                "veto_ids": ["document_repair_publication_quarantined"],
                "semantic_work_packet": {
                    "id": f"packet-{index}",
                    "label_scoped_obligation": {
                        "obligation_id": f"obligation-{index}",
                        "obligation_digest": f"{index:064x}",
                    },
                    "typed_repair_obligation": {
                        "id": f"typed-obligation-{index}",
                        "math_obligation": {"id": f"math-obligation-{index}"},
                    },
                    "source_span": {
                        "file": "paper.tex",
                        "start_byte": index * 10,
                        "end_byte": index * 10 + 9,
                    },
                    "target": f"target expression {index}",
                },
                "tree": {
                    "backend_attempts": [],
                    "assumptions": [
                        {
                            "id": f"assumption-{index}",
                            "status": "missing",
                            "text": "x != 0",
                            "role": "domain_condition",
                            "evidence_refs": [f"evidence://assumption/{index}"],
                            "source_refs": [_source_ref(label)],
                        }
                    ],
                    "blockers": [blocker],
                    "branch_ranking": {"selected_action": action},
                    "tool_grounded_proposal_compiler": {
                        "status": "compiled",
                        "publication_mode": "disabled",
                        "repair_proposal_count": 0,
                        "document_ready_repair_proposals": [],
                        "compiled_items": [
                            {
                                "id": f"gap-{index}",
                                "publishable_as_repair": False,
                                "publishable_as_gap_report": True,
                            }
                        ],
                        "validation_errors": [],
                    },
                },
            }
        )
    audit = {
        "metadata": {"schema_version": "1.0", "contract": "document_derivation_tree_audit"},
        "status": "diagnostic_complete",
        "tex_path": binding["ref"],
        "backend_env": "mathdevmcp-backends",
        "search_mode": "agent_guided",
        "grounding_policy": "strict",
        "publication_mode": "disabled",
        "publication_veto_ids": ["document_repair_publication_quarantined"],
        "veto_ids": ["document_repair_publication_quarantined"],
        "failure_classifications": ["mathematical_gap"],
        "promotion": {"can_promote": False, "reason": "publication disabled"},
        "execution": {
            "mode": "serial",
            "workers_requested": 1,
            "workers_used": 1,
            "target_count": len(targets),
            "failure_count": 0,
            "failures": [],
        },
        "coverage": {
            "status": "partial_coverage",
            "selected_rows": len(targets),
            "missing_focus_labels": [],
            "context_target_labels": binding["context_labels"],
            "context_target_count": len(binding["context_labels"]),
            "tool_grounded_compiler_validation_error_count": 0,
            "document_ready_repair_proposal_count": 0,
            "promoted_count": 0,
            "raw_promoted_count": 0,
        },
        "targets": targets,
        "context_targets": [{"label": label} for label in binding["context_labels"]],
        "non_claims": [
            {"code": "not_document_proof", "text": "This diagnostic is not a document proof."},
            {"code": "publication_disabled", "text": "No returned item is an applicable edit."},
        ],
    }
    request = build_document_derivation_audit_request(
        binding["ref"],
        focus_labels=binding["focus_labels"],
        max_labels=30,
        budget_profile="smoke",
        max_attempts=0,
        backend_env="mathdevmcp-backends",
        search_mode="agent_guided",
        grounding_policy="strict",
        workers=1,
    )
    return audit, request


def _responses(tmp_path: Path, document: str = "card") -> tuple[dict, dict, dict, dict, Path]:
    audit, request = _raw_audit(document)
    artifact_root = tmp_path / document
    compact = compile_document_derivation_response(
        audit,
        request,
        response_mode="compact",
        artifact_root=artifact_root,
        target_limit=20,
    )
    detailed = compile_document_derivation_response(
        audit,
        request,
        response_mode="detailed",
        artifact_root=artifact_root,
        target_limit=20,
    )
    return audit, request, compact, detailed, artifact_root


def test_live_verified_parent_reconstructs_without_writing() -> None:
    before = p08c._tree_identity(ROOT / p08c.PARENT_REF)
    binding = p08c._verify_parent()
    after = p08c._tree_identity(ROOT / p08c.PARENT_REF)

    assert before == after
    assert binding["parent_tree_digest"] == p08c.PARENT_TREE_DIGEST
    assert binding["p08a_decision_digest"] == p08c.P08A_DECISION_DIGEST
    assert binding["p08b_decision_digest"] == p08c.P08B_DECISION_DIGEST
    assert binding["publication_enabled"] is False


def test_parent_tree_identity_detects_added_file_without_touching_live_parent(
    tmp_path: Path,
) -> None:
    source = ROOT / p08c.PARENT_REF
    copied = tmp_path / "parent"
    import shutil

    shutil.copytree(source, copied)
    baseline = p08c._tree_identity(copied)
    (copied / "injected.txt").write_text("injected\n", encoding="utf-8")
    assert p08c._tree_identity(copied) != baseline


def test_raw_success_gate_rejects_caught_worker_failure_and_compiler_error() -> None:
    audit, _ = _raw_audit()
    audit["execution"]["failure_count"] = 1
    audit["execution"]["failures"] = [{"label": audit["targets"][0]["label"]}]
    audit["targets"][0]["claim_type"] = "worker_failure"
    audit["targets"][0]["failure_classifications"] = ["engineering_error"]
    audit["coverage"]["tool_grounded_compiler_validation_error_count"] = 1

    with pytest.raises(p08c.Phase08CError, match="raw audit boundary"):
        p08c._verify_raw_audit("card", audit)


def test_raw_success_gate_rejects_any_nested_backend_attempt() -> None:
    audit, _ = _raw_audit()
    audit["targets"][0]["tree"]["children"] = [{"backend_attempts": [{"status": "proved"}]}]

    with pytest.raises(p08c.Phase08CError, match="backend attempts"):
        p08c._verify_raw_audit("card", audit)


@pytest.mark.parametrize(
    ("key", "value"),
    [
        ("publication_enabled", True),
        ("can_promote", True),
        ("publishable_as_repair", True),
        ("applicable_to_document_branch", True),
        ("document_ready_repair_proposals", [{"id": "repair"}]),
        ("repair_proposal_count", 1),
        ("formal_proof_certified", True),
    ],
)
def test_recursive_authority_boundary_rejects_nested_escape(key: str, value) -> None:
    audit, _ = _raw_audit()
    audit["targets"][0]["tree"]["nested_escape"] = {key: value}
    with pytest.raises(p08c.Phase08CError, match="authority|repair|proof"):
        p08c._verify_raw_audit("card", audit)


def test_independent_projection_matches_compiler_and_detects_action_mutation(
    tmp_path: Path,
) -> None:
    audit, request, compact, detailed, artifact_root = _responses(tmp_path)
    assert validate_document_derivation_response(audit, compact) == []
    assert validate_document_derivation_response(audit, detailed) == []
    projection = compact["targets"][0]
    selected = audit["targets"][0]["tree"]["branch_ranking"]["selected_action"]
    assert expand_document_derivation_action(
        projection["selected_action"], compact["veto_ids"]
    ) == selected
    assert projection["content_identity"]["semantic_work_packet_id"] == "packet-0"

    changed = deepcopy(compact)
    changed["targets"][0]["selected_action"]["action"]["action_id"] = "mutate-0"
    changed["canonical_byte_count"] = len(
        json.dumps(changed, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    errors = validate_document_derivation_response(audit, changed)
    assert any("action" in error for error in errors)


def test_persisted_detailed_artifact_is_independently_reconstructed(tmp_path: Path) -> None:
    audit, request, compact, detailed, artifact_root = _responses(tmp_path)
    compact_artifact = compact["artifact"]
    detailed_artifact = detailed["artifact"]
    for field in ("state", "schema_version", "sha256", "byte_count", "authority"):
        assert compact_artifact[field] == detailed_artifact[field]
    assert detailed_artifact["logical_uri"].startswith("mathdevmcp-artifact://")
    assert detailed_artifact["media_type"] == "application/json"
    compatible_detailed = deepcopy(detailed)
    compatible_detailed["artifact"] = deepcopy(compact_artifact)
    continuation = tmp_path / "continuation"
    target = continuation / "detailed-artifacts/card"
    target.parent.mkdir(parents=True)
    artifact_root.rename(target)
    p08c._verify_persisted_detailed_artifact(
        continuation,
        "card",
        audit,
        request,
        compact,
        compatible_detailed,
    )
    artifact = compact["artifact"]
    path = (
        continuation
        / "detailed-artifacts/card/document-derivation"
        / compact["audit_result_id"]
        / compact["audit_request_id"]
        / "detailed.json"
    )
    raw = bytearray(path.read_bytes())
    raw[-1] ^= 1
    path.write_bytes(bytes(raw))
    with pytest.raises(p08c.Phase08CError):
        p08c._verify_persisted_detailed_artifact(
            continuation,
            "card",
            audit,
            request,
            compact,
            compatible_detailed,
        )
    assert artifact["state"] == "verified"


def test_probe_allowlist_accepts_only_registered_exact_templates() -> None:
    assert p08c._classify_probe([p08c.CONDA, "env", "list"]) == "conda_env_list"
    assert p08c._classify_probe(["/usr/bin/pandoc", "--version"]) == "executable_version"
    code = p08c._probe_python_code("sympy", "sympy")
    assert (
        p08c._classify_probe([p08c.BACKEND_PYTHON, "-c", code])
        == "backend_python_package_version"
    )
    assert p08c._classify_probe(["/usr/bin/sage", "-c", "2+2"]) is None
    assert p08c._classify_probe([p08c.BACKEND_PYTHON, "-c", "import sympy"]) is None


def test_persisted_probe_counts_are_reconstructed_from_document_bindings() -> None:
    probes = [
        {"document": document, "classification": classification}
        for document in p08c.SOURCE_BINDINGS
        for classification, expected_count in p08c.EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT.items()
        for _ in range(expected_count)
    ]
    expected = {
        document: dict(p08c.EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT)
        for document in p08c.SOURCE_BINDINGS
    }
    assert p08c._probe_counts_by_document(probes) == expected

    probes[0]["document"] = "unregistered"
    with pytest.raises(p08c.Phase08CError, match="document/classification binding"):
        p08c._probe_counts_by_document(probes)


@pytest.mark.parametrize(
    "private_path",
    [
        "/home/researcher/result.json",
        "/tmp/result.json",
        "/usr/local/bin/tool",
        "/opt/tool/result.json",
        "/var/cache/result.json",
        "/run/user/result.json",
        "/mnt/data/result.json",
        "/srv/project/result.json",
    ],
)
def test_independent_transport_scan_covers_all_registered_local_roots(private_path: str) -> None:
    assert p08c.LOCAL_ABSOLUTE_PATH_FRAGMENT.search(f"artifact={private_path}")
    assert p08c.LOCAL_ABSOLUTE_PATH_FRAGMENT.search(f"file://{private_path}")
    assert not p08c.LOCAL_ABSOLUTE_PATH_FRAGMENT.search(
        "mathdevmcp://external-tool-adapter/sympy/attempt-1"
    )


def test_registered_doctor_probe_call_graph_is_exact_and_nonmathematical(monkeypatch) -> None:
    monkeypatch.setattr(os, "environ", dict(p08c.EXPECTED_ENVIRONMENT))
    with p08c._guarded_probes() as ledger:
        from mathdevmcp.doctor import doctor_report

        report = doctor_report()
    counts = {
        classification: sum(item["classification"] == classification for item in ledger)
        for classification in p08c.EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT
    }
    assert counts == p08c.EXPECTED_PROBE_CLASS_COUNTS_PER_DOCUMENT
    assert all(item["mathematical_input"] is False for item in ledger)
    assert report["ok"] is True


def test_guard_rejects_unregistered_process_and_network_before_launch(monkeypatch) -> None:
    launches: list[list[str]] = []

    class FakeProcess:
        pass

    def fake_popen(argv, **kwargs):
        launches.append(argv)
        return FakeProcess()

    monkeypatch.setattr(subprocess, "Popen", fake_popen)
    with p08c._guarded_probes() as ledger:
        with pytest.raises(p08c.Phase08CError, match="rejected before launch"):
            subprocess.run(
                ["/usr/bin/sage", "-c", "2+2"],
                check=False,
                capture_output=True,
                text=True,
                timeout=10,
            )
        with pytest.raises(p08c.Phase08CError, match="network"):
            import socket

            socket.create_connection(("example.com", 443))
    assert launches == []
    assert [item["allowed"] for item in ledger] == [False, False]


def test_guard_allows_registered_probe_and_records_bounded_output(monkeypatch) -> None:
    stdout_read, stdout_write = os.pipe()
    stderr_read, stderr_write = os.pipe()
    os.write(stdout_write, b"conda environments:\n")
    os.close(stdout_write)
    os.close(stderr_write)

    class FakeStream:
        def __init__(self, fd: int) -> None:
            self._fd = fd

        def fileno(self) -> int:
            return self._fd

        def close(self) -> None:
            try:
                os.close(self._fd)
            except OSError:
                pass

    class FakeProcess:
        def __init__(self) -> None:
            self.stdout = FakeStream(stdout_read)
            self.stderr = FakeStream(stderr_read)
            self.returncode = 0

        def wait(self, timeout=None):
            return 0

        def poll(self):
            return 0

    monkeypatch.setattr(subprocess, "Popen", lambda *args, **kwargs: FakeProcess())
    with p08c._guarded_probes() as ledger:
        completed = subprocess.run(
            [p08c.CONDA, "env", "list"],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    assert completed.returncode == 0
    assert completed.stdout == "conda environments:\n"
    assert ledger[0]["classification"] == "conda_env_list"
    assert ledger[0]["allowed"] is True
    assert ledger[0]["stdout_byte_count"] == len(b"conda environments:\n")


def test_source_cache_policy_allows_inert_pyc_but_rejects_cache_surprise(
    tmp_path: Path, monkeypatch
) -> None:
    source_root = tmp_path / "src"
    package = source_root / "mathdevmcp"
    cache = package / "__pycache__"
    cache.mkdir(parents=True)
    (package / "module.py").write_text("VALUE = 'source'\n", encoding="utf-8")
    (cache / "module.cpython-311.pyc").write_bytes(b"inert")
    monkeypatch.setattr(p08c, "SOURCE_ROOT", source_root)
    p08c._verify_source_tree_cache_policy()
    (cache / "surprise.py").write_text("VALUE = 'bad'\n", encoding="utf-8")
    with pytest.raises(p08c.Phase08CError, match="cache contains an unexpected file"):
        p08c._verify_source_tree_cache_policy()


def test_source_only_flags_bypass_poisoned_pyc_and_sitecustomize(tmp_path: Path) -> None:
    source = tmp_path / "probe.py"
    source.write_text("VALUE = 'poison'\n", encoding="utf-8")
    py_compile.compile(
        str(source),
        doraise=True,
        invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH,
    )
    source.write_text("VALUE = 'source'\n", encoding="utf-8")
    (tmp_path / "sitecustomize.py").write_text(
        "from pathlib import Path; Path('sitecustomize-ran').write_text('yes')\n",
        encoding="utf-8",
    )
    script = (
        f"import sys; sys.path.insert(0, {str(tmp_path)!r}); "
        "import probe; print(probe.VALUE)"
    )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(tmp_path)
    completed = subprocess.run(
        [
            p08c.P08_PYTHON,
            "-I",
            "-S",
            "-B",
            "-X",
            "pycache_prefix=/dev/null",
            "-c",
            script,
        ],
        cwd=tmp_path,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert completed.returncode == 0
    assert completed.stdout == "source\n"
    assert not (tmp_path / "sitecustomize-ran").exists()


def test_exact_continuation_file_set_rejects_extra_or_transplanted_file(
    tmp_path: Path,
) -> None:
    continuation = tmp_path / "continuation"
    (continuation / "code-snapshot/scripts").mkdir(parents=True)
    (continuation / "code-snapshot/scripts/runner.py").write_text("x\n", encoding="utf-8")
    (continuation / "code-identity.json").write_text("{}", encoding="utf-8")
    (continuation / "decision.json").write_text("{}", encoding="utf-8")
    (continuation / "artifact.json").write_text("{}", encoding="utf-8")
    identity = {"files": [{"ref": "scripts/runner.py"}]}
    decision = {"artifact_inventory": [{"ref": "artifact.json"}]}
    p08c._verify_exact_continuation_files(continuation, identity, decision)
    (continuation / "extra.json").write_text("{}", encoding="utf-8")
    with pytest.raises(p08c.Phase08CError, match="file set"):
        p08c._verify_exact_continuation_files(continuation, identity, decision)


def test_parser_requires_literal_decision_digest_for_verify() -> None:
    parser = p08c.build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["verify", "--continuation-root", "continuations/id"])
    args = parser.parse_args(
        [
            "verify",
            "--continuation-root",
            "continuations/id",
            "--expected-decision-digest",
            "1" * 64,
        ]
    )
    assert args.expected_decision_digest == "1" * 64


@pytest.mark.parametrize(
    ("args", "message"),
    [
        (
            SimpleNamespace(
                parent_run_root="latest",
                continuation_root=p08c.CONTINUATION_PARENT_REF,
                budget_profile="smoke",
                max_attempts=0,
                workers=1,
                target_limit=20,
            ),
            "literal reviewed parent",
        ),
        (
            SimpleNamespace(
                parent_run_root=p08c.PARENT_REF,
                continuation_root=p08c.CONTINUATION_PARENT_REF,
                budget_profile="standard",
                max_attempts=0,
                workers=1,
                target_limit=20,
            ),
            "request controls",
        ),
    ],
)
def test_create_rejects_implicit_parent_or_request_drift_before_artifact_creation(
    args: SimpleNamespace, message: str
) -> None:
    with pytest.raises(p08c.Phase08CError, match=message):
        p08c._create(args)


def test_main_rejects_ordinary_nonisolated_startup() -> None:
    completed = subprocess.run(
        [p08c.P08_PYTHON, str(RUNNER), "verify", "--continuation-root", "x", "--expected-decision-digest", "1" * 64],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert completed.returncode == 2
    assert "runtime is not isolated and source-only" in completed.stderr


def test_main_rejects_env_drift_under_isolated_flags() -> None:
    env = dict(p08c.EXPECTED_ENVIRONMENT)
    env["EXTRA_UNREVIEWED"] = "1"
    completed = subprocess.run(
        [
            p08c.P08_PYTHON,
            "-I",
            "-S",
            "-B",
            "-X",
            "pycache_prefix=/dev/null",
            str(RUNNER),
            "verify",
            "--continuation-root",
            "x",
            "--expected-decision-digest",
            "1" * 64,
        ],
        cwd=ROOT,
        env=env,
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )
    assert completed.returncode == 2
    assert "environment differs" in completed.stderr


def test_completed_phase08c_continuation_remains_immutable_and_bound() -> None:
    continuation = (
        ROOT
        / p08c.CONTINUATION_PARENT_REF
        / "20260714T080342Z-3a1e3445eeab"
    )
    decision = json.loads((continuation / "decision.json").read_text(encoding="utf-8"))

    assert decision["status"] == "INCOMPLETE_P08C_PRODUCT_CRITERION"
    assert decision["continuation_binding_digest"] == (
        "ab95aa4e9843d9bd2dc934c7a6215c26139aaefbb686f4e3ba2517fe584bd726"
    )
    assert decision["decision_digest"] == (
        "0c23863c391ef07d7b3f1911bdcee912e640e368343650f168c0bba7e888bbd3"
    )
    assert decision["mathematical_backend_attempt_count"] == 0
    assert decision["publication_enabled"] is False
