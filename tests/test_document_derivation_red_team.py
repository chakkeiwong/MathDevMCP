from __future__ import annotations

from copy import deepcopy
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import pytest

import tests.p09_no_live_backend_guard as p09_guard


ROOT = Path(__file__).resolve().parent.parent
RUNNER = ROOT / "scripts/run_p09_final_red_team.py"


def _load_runner():
    spec = importlib.util.spec_from_file_location("p09_final_red_team_runner", RUNNER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


p09 = _load_runner()


def _canonical(value) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def test_guard_attestation_accounts_for_non_call_outcomes_without_duplicates() -> None:
    saved = (
        list(p09_guard._PASSED_NODEIDS),
        list(p09_guard._FAILED_NODEIDS),
        list(p09_guard._SKIPPED_NODEIDS),
    )
    try:
        p09_guard._PASSED_NODEIDS.clear()
        p09_guard._FAILED_NODEIDS.clear()
        p09_guard._SKIPPED_NODEIDS.clear()

        p09_guard.pytest_runtest_logreport(
            SimpleNamespace(
                nodeid="test_module.py::test_setup_skip",
                when="setup",
                passed=False,
                failed=False,
                skipped=True,
            )
        )
        for when in ("call", "call"):
            p09_guard.pytest_runtest_logreport(
                SimpleNamespace(
                    nodeid="test_module.py::test_teardown_failure",
                    when=when,
                    passed=True,
                    failed=False,
                    skipped=False,
                )
            )
        p09_guard.pytest_runtest_logreport(
            SimpleNamespace(
                nodeid="test_module.py::test_teardown_failure",
                when="teardown",
                passed=False,
                failed=True,
                skipped=False,
            )
        )

        assert p09_guard._PASSED_NODEIDS == []
        assert p09_guard._FAILED_NODEIDS == [
            "test_module.py::test_teardown_failure"
        ]
        assert p09_guard._SKIPPED_NODEIDS == ["test_module.py::test_setup_skip"]
    finally:
        p09_guard._PASSED_NODEIDS[:] = saved[0]
        p09_guard._FAILED_NODEIDS[:] = saved[1]
        p09_guard._SKIPPED_NODEIDS[:] = saved[2]


def test_runner_parser_has_candidate_review_final_lifecycle() -> None:
    parser = p09.build_parser()
    create = parser.parse_args(["create-candidate"])
    verify = parser.parse_args(
        [
            "verify-candidate",
            "--run-root",
            ".local/mathdevmcp/evidence/p09-20260715/example",
            "--expected-candidate-decision-digest",
            "1" * 64,
        ]
    )
    finish = parser.parse_args(
        [
            "finalize",
            "--run-root",
            ".local/mathdevmcp/evidence/p09-20260715/example",
            "--review-record",
            "docs/reviews/example.md",
            "--review-outcome",
            "agree",
        ]
    )
    final = parser.parse_args(
        [
            "verify-final",
            "--run-root",
            ".local/mathdevmcp/evidence/p09-20260715/example",
            "--expected-decision-digest",
            "2" * 64,
        ]
    )

    assert create.handler is p09.create_candidate
    assert verify.handler is p09.verify_candidate
    assert finish.handler is p09.finalize
    assert final.handler is p09.verify_final

    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "verify-candidate",
                "--run-root",
                ".local/mathdevmcp/evidence/p09-20260715/example",
            ]
        )
    with pytest.raises(SystemExit):
        parser.parse_args(
            [
                "verify-final",
                "--run-root",
                ".local/mathdevmcp/evidence/p09-20260715/example",
            ]
        )


def test_candidate_digest_excludes_only_its_digest_field() -> None:
    candidate = {
        "schema_version": "p09_candidate_decision@1",
        "status": "SAFE_AND_SUBSTANTIVELY_USEFUL",
        "publication_enabled": False,
    }
    digest = p09._candidate_decision_digest(candidate)
    sealed = {**candidate, "candidate_decision_digest": digest}

    assert p09._candidate_decision_digest(sealed) == digest
    changed = {**sealed, "publication_enabled": True}
    assert p09._candidate_decision_digest(changed) != digest


def test_predecessor_artifact_inventory_requires_exact_ordered_refs(
    tmp_path: Path,
) -> None:
    p09._write_new(tmp_path / "first.json", {"value": 1})
    p09._write_new(tmp_path / "second.json", {"value": 2})
    refs = ("first.json", "second.json")
    inventory = [p09._binding(tmp_path / ref, ref) for ref in refs]
    decision = {
        "artifact_inventory": inventory,
        "artifact_inventory_digest": p09._sha256(inventory),
    }

    assert p09._require_artifact_inventory(tmp_path, decision, refs) == inventory
    for changed in (
        {**decision, "artifact_inventory": inventory[:-1]},
        {**decision, "artifact_inventory": [*inventory, inventory[0]]},
        {**decision, "artifact_inventory": list(reversed(inventory))},
    ):
        changed["artifact_inventory_digest"] = p09._sha256(
            changed["artifact_inventory"]
        )
        with pytest.raises(p09.IntegrityVeto, match="inventory refs"):
            p09._require_artifact_inventory(tmp_path, changed, refs)


def test_predecessor_code_bindings_reject_missing_extra_and_reordered(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    expected = {
        "scripts/run_p08c1_target_fidelity_replay.py": p09.P08C1_CODE_DIGESTS[
            "scripts/run_p08c1_target_fidelity_replay.py"
        ],
        "src/mathdevmcp/document_derivation_tree.py": p09.P08C1_CODE_DIGESTS[
            "src/mathdevmcp/document_derivation_tree.py"
        ],
    }
    bindings = [
        {"ref": ref, "sha256": digest, "byte_count": index + 1}
        for index, (ref, digest) in enumerate(expected.items())
    ]
    by_ref = {item["ref"]: item for item in bindings}
    monkeypatch.setattr(p09, "_binding", lambda _path, ref: dict(by_ref[ref]))
    assert p09._require_code_bindings(
        {"code_bindings": bindings}, expected, gate="test"
    ) == bindings
    for changed in (
        bindings[:-1],
        [*bindings, bindings[0]],
        list(reversed(bindings)),
    ):
        with pytest.raises(p09.IntegrityVeto, match="code-binding inventory"):
            p09._require_code_bindings(
                {"code_bindings": changed}, expected, gate="test"
            )


def test_complete_p08_snapshot_inventory_reconstructs() -> None:
    record = p09._reconstruct_p08_code_snapshot()

    assert record["status"] == "pass"
    assert record["code_identity_digest"] == p09.P08_CODE_IDENTITY_DIGEST
    assert record["snapshot_file_count"] == 144
    assert set(record["required_refs"]) <= {
        item["ref"] for item in p09._tree_inventory(p09.P08AB_ROOT / "code-snapshot")
    }


def test_unverified_module_bytes_never_execute(tmp_path: Path) -> None:
    marker = tmp_path / "executed"
    module = tmp_path / "untrusted.py"
    module.write_text(
        f"from pathlib import Path\nPath({str(marker)!r}).write_text('bad')\n",
        encoding="utf-8",
    )

    with pytest.raises(p09.IntegrityVeto, match="bytes drifted before load"):
        p09._load_verified_module("p09_untrusted_probe", module, "0" * 64)

    assert not marker.exists()


def test_replay_modules_require_fixed_accepted_identity_before_load(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    attested = {
        ref: digest
        for mapping in (p09.P08C1_CODE_DIGESTS, p09.P08D_CODE_DIGESTS)
        for ref, digest in mapping.items()
    }
    attested["scripts/run_p08c1_target_fidelity_replay.py"] = "0" * 64
    loaded: list[str] = []
    monkeypatch.setattr(
        p09,
        "_load_verified_module",
        lambda name, path, digest: loaded.append(name),
    )

    with pytest.raises(p09.IntegrityVeto, match="accepted or attested identity"):
        p09._perform_reconstruction(
            {},
            [],
            [],
            {
                "code_bindings": [
                    {"ref": ref, "sha256": digest} for ref, digest in attested.items()
                ]
            },
        )

    assert loaded == []


def test_runtime_identity_records_scoped_reproducibility_inputs() -> None:
    identity = p09._expected_guarded_test_runtime_identity()

    assert identity["python_executable"] == p09.P09_PYTHON
    assert identity["python_version"] == p09.P09_PYTHON_VERSION
    assert identity["root_distribution_versions"] == {
        "anyio": "4.13.0",
        "httpx": "0.28.1",
        "mcp": "1.27.0",
        "pydantic": "2.12.5",
        "pytest": "9.0.2",
    }
    assert identity["module_origins"]["p09_runner"] == str(RUNNER.resolve())


def test_runtime_version_mismatch_is_environment_block(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(p09.Path, "cwd", lambda: p09.WORKSPACE)
    monkeypatch.setattr(p09.platform, "python_version", lambda: "3.11.changed")
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "-1")
    monkeypatch.setenv("PYTHONHASHSEED", "0")
    monkeypatch.setenv("PYTHONDONTWRITEBYTECODE", "1")
    monkeypatch.setenv("PYTHONPATH", "src")
    monkeypatch.setattr(p09.sys, "dont_write_bytecode", True)
    monkeypatch.setattr(p09.sys, "executable", p09.P09_PYTHON)

    with pytest.raises(p09.ClassificationBlock, match="pinned Python version"):
        p09._runtime_boundary()


def test_guard_attestation_counters_are_measured() -> None:
    saved = list(p09_guard._FORBIDDEN_ATTEMPTS)
    try:
        p09_guard._FORBIDDEN_ATTEMPTS[:] = [
            {"sequence": 1, "kind": "network", "target": "socket.socket"},
            {
                "sequence": 2,
                "kind": "document_audit",
                "target": "mathdevmcp.document_derivation_tree.audit_document_derivation_tree",
            },
            {
                "sequence": 3,
                "kind": "mathematical_backend",
                "target": "mathdevmcp.lean_check.check_lean_source",
            },
        ]
        record = p09_guard.guard_attestation()
        assert record["forbidden_attempt_count"] == 3
        assert record["network_attempt_count"] == 1
        assert record["document_audit_invocation_count"] == 1
        assert record["mathematical_backend_attempt_count"] == 1
    finally:
        p09_guard._FORBIDDEN_ATTEMPTS[:] = saved


def test_child_guard_counters_and_post_import_aliases_are_measured() -> None:
    attempts = [
        {"sequence": 1, "kind": "process", "target": "os.fork"},
        {"sequence": 2, "kind": "network", "target": "socket.create_server"},
        {
            "sequence": 3,
            "kind": "document_audit",
            "target": "mathdevmcp.cli.high_level_audit_document_derivation_tree",
        },
        {
            "sequence": 4,
            "kind": "mathematical_backend",
            "target": "mathdevmcp.mcp_facade.check_lean_source",
        },
    ]
    record = __import__(
        "tests.p09_guarded_cli_entry", fromlist=["_guard_attestation"]
    )._guard_attestation(attempts)

    assert record["forbidden_attempt_count"] == 4
    assert record["process_attempt_count"] == 1
    assert record["network_attempt_count"] == 1
    assert record["document_audit_invocation_count"] == 1
    assert record["mathematical_backend_attempt_count"] == 1


def test_child_guard_patches_loaded_audit_and_backend_aliases() -> None:
    child = __import__(
        "tests.p09_guarded_cli_entry", fromlist=["_patch_loaded_aliases"]
    )
    attempts: list[dict] = []
    audit_module = SimpleNamespace(audit_document_derivation_tree=lambda: None)
    backend_module = SimpleNamespace(check_lean_source=lambda: None)
    modules = {
        "mathdevmcp.audit_alias": audit_module,
        "mathdevmcp.backend_alias": backend_module,
    }
    child._patch_loaded_aliases(attempts, modules)

    with pytest.raises(child.GuardError):
        audit_module.audit_document_derivation_tree()
    with pytest.raises(child.GuardError):
        backend_module.check_lean_source()
    assert [item["kind"] for item in attempts] == [
        "document_audit",
        "mathematical_backend",
    ]


def test_p08a_decision_is_cross_bound_to_reconstructed_records(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_load = p09._load

    def changed(path: Path):
        record = original_load(path)
        if path == p09.P08AB_ROOT / "p08a/decision.json":
            record["source_manifest_digest"] = "0" * 64
            record["decision_digest"] = p09._decision_digest(record)
        return record

    monkeypatch.setattr(p09, "_load", changed)
    monkeypatch.setitem(p09.P08_DECISIONS, "p08a", changed(p09.P08AB_ROOT / "p08a/decision.json")["decision_digest"])
    runner = p09._load_verified_module(
        "p09_test_p08_runner_cross_binding",
        p09.P08AB_ROOT / "code-snapshot/scripts/run_p08_frozen_validation.py",
        p09.P08_SNAPSHOT_DIGESTS["scripts/run_p08_frozen_validation.py"],
    )
    with pytest.raises(p09.IntegrityVeto, match="source/context boundary"):
        p09._reconstruct_p08a(runner)


def _assert_p08a_p08b_chain_reconstructs_exactly_without_backend_import() -> None:
    runner = p09._load_verified_module(
        "p09_test_p08_runner_exact",
        p09.P08AB_ROOT / "code-snapshot/scripts/run_p08_frozen_validation.py",
        p09.P08_SNAPSHOT_DIGESTS["scripts/run_p08_frozen_validation.py"],
    )
    adapter = p09._load_verified_module(
        "p09_test_p08_adapter_exact",
        p09.P08AB_ROOT / "code-snapshot/src/mathdevmcp/sympy_derivative_adapter.py",
        p09.P08_SNAPSHOT_DIGESTS["src/mathdevmcp/sympy_derivative_adapter.py"],
    )

    p08a = p09._reconstruct_p08a(runner)
    p08b = p09._reconstruct_p08b(runner, adapter)

    assert p08a["decision_digest"] == p09.P08_DECISIONS["p08a"]
    assert p08b["decision_digest"] == p09.P08_DECISIONS["p08b"]
    assert p08b["backend_checked"] is True
    assert p08b["live_backend_execution_count_in_p09"] == 0
    assert "sympy" not in sys.modules


def test_p08a_p08b_chain_reconstructs_exactly_without_backend_import() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "from tests.test_document_derivation_red_team import "
            "_assert_p08a_p08b_chain_reconstructs_exactly_without_backend_import as check; check()",
        ],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def test_p08b_missing_structural_budget_field_is_integrity_veto(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original_load = p09._load

    def changed(path: Path):
        record = original_load(path)
        if path.name == "manifest.json" and "eq_cashflow_rate_derivative" in str(path):
            record.pop("fixed_overhead_bytes")
        return record

    monkeypatch.setattr(p09, "_load", changed)
    runner = p09._load_verified_module(
        "p09_test_p08_runner_structural",
        p09.P08AB_ROOT / "code-snapshot/scripts/run_p08_frozen_validation.py",
        p09.P08_SNAPSHOT_DIGESTS["scripts/run_p08_frozen_validation.py"],
    )
    adapter = p09._load_verified_module(
        "p09_test_p08_adapter_structural",
        p09.P08AB_ROOT / "code-snapshot/src/mathdevmcp/sympy_derivative_adapter.py",
        p09.P08_SNAPSHOT_DIGESTS["src/mathdevmcp/sympy_derivative_adapter.py"],
    )
    with pytest.raises(p09.IntegrityVeto, match="closed-schema"):
        p09._reconstruct_p08b(runner, adapter)


def test_guarded_case_cannot_pass_without_matching_test_node() -> None:
    case_id = "private_error_data"
    required = p09.TEST_CASE_NODEIDS[case_id]
    attestation = {
        "collected_nodeids": [],
        "passed_nodeids": [],
        "case_evidence": {
            case_id: {
                "required_nodeids": list(required),
                "passed_nodeids": [],
                "passed": True,
            }
        }
    }

    with pytest.raises(p09.IntegrityVeto, match="case evidence is incomplete"):
        p09._attested_case(attestation, case_id)


def test_guarded_case_rejects_spoofed_prefix_node() -> None:
    case_id = "sibling_parent_evidence_reuse"
    required = list(p09.TEST_CASE_NODEIDS[case_id])
    spoofed = required[-1] + "-spoofed"
    attestation = {
        "collected_nodeids": [required[0], spoofed],
        "passed_nodeids": [required[0], spoofed],
        "case_evidence": {
            case_id: {
                "required_nodeids": required,
                "passed_nodeids": [required[0], spoofed],
                "passed": True,
            }
        },
    }

    with pytest.raises(p09.IntegrityVeto, match="case evidence is incomplete"):
        p09._attested_case(attestation, case_id)


def test_current_code_closure_includes_transitive_contract_dependency() -> None:
    refs = p09._current_code_refs()

    assert "src/mathdevmcp/contracts.py" in refs
    assert "src/mathdevmcp/document_derivation_response.py" in refs
    assert len(refs) == len(set(refs))
    assert refs == p09_guard._guard_code_refs()


def test_material_input_inventory_binds_sources_comparators_and_p00() -> None:
    inventory = p09._material_input_inventory()

    assert [item["ref"] for item in inventory] == list(p09.MATERIAL_INPUT_DIGESTS)
    assert all(
        item["sha256"] == p09.MATERIAL_INPUT_DIGESTS[item["ref"]]
        for item in inventory
    )


def test_guard_code_closure_detects_end_of_session_drift(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    first = [{"ref": "x", "sha256": "1" * 64, "byte_count": 1}]
    second = [{"ref": "x", "sha256": "2" * 64, "byte_count": 1}]
    monkeypatch.setattr(p09_guard, "_CODE_BINDINGS_START", first)
    monkeypatch.setattr(p09_guard, "_code_bindings", lambda: second)

    assert p09_guard._CODE_BINDINGS_START != p09_guard._code_bindings()


@pytest.mark.parametrize("route", ["process", "network", "document_audit"])
def test_candidate_execution_guard_blocks_live_routes(route: str) -> None:
    attempts: list[dict[str, str]] = []
    with pytest.raises(p09.ClassificationBlock):
        with p09._execution_guard(attempts):
            if route == "process":
                p09.subprocess.run(["true"])
            elif route == "network":
                p09.socket.getaddrinfo("localhost", 80)
            else:
                from mathdevmcp import document_derivation_tree

                document_derivation_tree.audit_document_derivation_tree("ignored.tex")

    assert len(attempts) == 1
    assert attempts[0]["kind"] == route


@pytest.mark.parametrize(
    ("error_type", "expected_status"),
    [(p09.IntegrityVeto, "UNSAFE"), (p09.ClassificationBlock, "BLOCKED")],
)
def test_first_reconstruction_failure_writes_durable_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    error_type: type[Exception],
    expected_status: str,
) -> None:
    output_parent = tmp_path / "p09"
    monkeypatch.setattr(p09, "WORKSPACE", tmp_path)
    monkeypatch.setattr(p09, "OUTPUT_PARENT", output_parent)
    monkeypatch.setattr(p09, "P08AB_ROOT", tmp_path / "accepted/p08ab")
    monkeypatch.setattr(p09, "P08C_ROOT", tmp_path / "accepted/p08c")
    monkeypatch.setattr(p09, "P08C1_ROOT", tmp_path / "accepted/p08c1")
    monkeypatch.setattr(p09, "P08D_ROOT", tmp_path / "accepted/p08d")
    monkeypatch.setattr(p09, "_runtime_boundary", lambda: None)
    monkeypatch.setattr(p09, "_all_predecessor_inventories", lambda: {})
    monkeypatch.setattr(
        p09,
        "_current_code_bindings",
        lambda: [{"ref": "runner", "sha256": "1" * 64, "byte_count": 1}],
    )
    monkeypatch.setattr(p09, "_head_commit", lambda: "2" * 40)
    monkeypatch.setattr(
        p09,
        "_load_guarded_test_attestation",
        lambda: {
            "code_bindings": [
                {"ref": "runner", "sha256": "1" * 64, "byte_count": 1}
            ],
            "attestation_digest": "3" * 64,
        },
    )

    def fail(*args, **kwargs):
        raise error_type("synthetic first-run failure")

    monkeypatch.setattr(p09, "_perform_reconstruction", fail)
    result = p09.create_candidate(SimpleNamespace())
    run_root = tmp_path / result["run_root"]

    assert result["status"] == expected_status
    assert {path.name for path in run_root.iterdir()} == {
        "guarded-test-attestation.json",
        "reconstruction-ledger.json",
        "adversarial-matrix.json",
        "evidence-ledger-reconciliation.json",
        "run-manifest.json",
        "candidate-decision.json",
    }
    candidate = p09._load(run_root / "candidate-decision.json")
    assert candidate["status"] == expected_status
    assert candidate["candidate_decision_digest"] == result["candidate_decision_digest"]


def test_review_record_requires_exact_unique_candidate_bindings() -> None:
    expected = {
        "run_root": ".local/mathdevmcp/evidence/p09-20260715/run",
        "candidate_decision_digest": "1" * 64,
        "candidate_file_sha256": "2" * 64,
        "candidate_artifact_inventory_digest": "3" * 64,
    }
    text = "\n".join(
        p09.REVIEW_BINDING_PREFIXES[key] + value for key, value in expected.items()
    )
    p09._require_review_bindings(text, expected)

    with pytest.raises(p09.IntegrityVeto, match="candidate_file_sha256"):
        p09._require_review_bindings(text.replace("2" * 64, "4" * 64), expected)
    with pytest.raises(p09.IntegrityVeto, match="run_root"):
        p09._require_review_bindings(
            text + "\n" + p09.REVIEW_BINDING_PREFIXES["run_root"] + expected["run_root"],
            expected,
        )


@pytest.mark.parametrize(
    ("drift", "message"),
    (
        ("code", "current code changed"),
        ("material", "predecessor evidence changed"),
        ("direct_material", "material inputs changed or were unbound"),
    ),
)
@pytest.mark.parametrize(
    ("candidate_status", "classification"),
    (
        ("SAFE_AND_SUBSTANTIVELY_USEFUL", "complete"),
        ("UNSAFE", "unsafe"),
        ("BLOCKED", "blocked"),
    ),
)
def test_candidate_live_state_drift_is_rejected_for_every_status(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    drift: str,
    message: str,
    candidate_status: str,
    classification: str,
) -> None:
    predecessor_inventory = {"material_inputs": []}
    reconstruction = {
        "classification": classification,
        "predecessor_inventory_unchanged": True,
        "predecessor_inventory_before": predecessor_inventory,
        "predecessor_inventory_after": predecessor_inventory,
        "gates": {
            key: {
                "status": "pass",
                **({"backend_checked": True} if key == "p08b" else {}),
            }
            for key in ("p08a", "p08b", "p08c", "p08c1", "p08d")
        },
        "guarded_test_attestation_digest": "4" * 64,
    }
    candidate = {
        "status": candidate_status,
        "mathematical_backend_execution_count": 0,
        "document_audit_execution_count": 0,
        "forbidden_attempt_count": 0,
    }
    manifest = {
        "schema_version": "p09_run_manifest@1",
        "run_id": tmp_path.name,
        "run_root": "synthetic",
        "candidate_classification": candidate_status,
        "current_code_bindings": [{"ref": "x", "sha256": "1" * 64, "byte_count": 1}],
        "current_code_bindings_digest": p09._sha256(
            [{"ref": "x", "sha256": "1" * 64, "byte_count": 1}]
        ),
        "forbidden_attempts": [],
        "blocked_imports": [],
        "mathematical_backend_execution_count": 0,
        "document_audit_execution_count": 0,
        "network_execution_count": 0,
        "material_input_bindings": [],
        "material_input_bindings_digest": p09._sha256([]),
    }
    test_attestation = {
        "all_passed": True,
        "code_bindings": [{"ref": "x", "sha256": "1" * 64, "byte_count": 1}],
        "runtime_identity": {"runtime": "bound"},
    }
    test_attestation["attestation_digest"] = p09._sha256(test_attestation)
    reconstruction["guarded_test_attestation_digest"] = test_attestation[
        "attestation_digest"
    ]
    records = {
        "guarded-test-attestation.json": test_attestation,
        "reconstruction-ledger.json": reconstruction,
        "adversarial-matrix.json": {
            "all_passed": True,
            "guarded_test_attestation_digest": test_attestation[
                "attestation_digest"
            ],
        },
        "evidence-ledger-reconciliation.json": {"unexplained_discrepancies": []},
        "run-manifest.json": manifest,
    }
    monkeypatch.setattr(p09, "WORKSPACE", tmp_path.parent)
    manifest["run_root"] = tmp_path.relative_to(tmp_path.parent).as_posix()
    monkeypatch.setattr(p09, "_load_candidate", lambda root: candidate)
    monkeypatch.setattr(p09, "_load", lambda path: records[path.name])
    monkeypatch.setattr(
        p09,
        "_all_predecessor_inventories",
        lambda: (
            {"material_inputs": [{"ref": "changed"}]}
            if drift == "material"
            else predecessor_inventory
        ),
    )
    monkeypatch.setattr(
        p09,
        "_material_input_inventory",
        lambda: ([{"ref": "changed"}] if drift == "direct_material" else []),
    )
    monkeypatch.setattr(
        p09, "_expected_guarded_test_runtime_identity", lambda: {"runtime": "bound"}
    )
    monkeypatch.setattr(
        p09,
        "_current_code_bindings",
        lambda: [
            {
                "ref": "x",
                "sha256": ("2" if drift == "code" else "1") * 64,
                "byte_count": 1,
            }
        ],
    )

    with pytest.raises(p09.IntegrityVeto, match=message):
        p09._verify_candidate_state(tmp_path, require_live_state=True)


def test_hard_bound_positive_entry_never_maps_to_capability_incomplete() -> None:
    gates = {
        key: {"status": "pass"}
        for key in ("p08a", "p08b", "p08c", "p08c1", "p08d")
    }
    gates["p08b"]["backend_checked"] = True
    reconstruction = {
        "classification": "complete",
        "predecessor_inventory_unchanged": True,
        "gates": gates,
    }
    adversarial = {"all_passed": True}
    reconciliation = {"unexplained_discrepancies": []}

    assert (
        p09._candidate_status(reconstruction, adversarial, reconciliation)
        == "SAFE_AND_SUBSTANTIVELY_USEFUL"
    )
    broken = deepcopy(reconstruction)
    broken["gates"]["p08b"]["backend_checked"] = False
    assert p09._candidate_status(broken, adversarial, reconciliation) == "UNSAFE"
    assert "SAFE_BUT_CAPABILITY_INCOMPLETE" not in {
        p09._candidate_status(reconstruction, adversarial, reconciliation),
        p09._candidate_status(broken, adversarial, reconciliation),
    }


def _assert_p08b_assumption_mutation_is_rejected_without_backend_import() -> None:
    adapter = p09._load_verified_module(
        "p09_test_preserved_adapter",
        p09.P08AB_ROOT
        / "code-snapshot/src/mathdevmcp/sympy_derivative_adapter.py",
        p09.P08_SNAPSHOT_DIGESTS["src/mathdevmcp/sympy_derivative_adapter.py"],
    )
    request = p09._load(
        p09.P08AB_ROOT
        / "p08b/backend/eq_cashflow_rate_derivative/native-input.json"
    )
    mutated = deepcopy(request)
    mutated["typed_assumptions"] = [
        item
        for item in mutated["typed_assumptions"]
        if item["id"] != "nonzero_one_plus_rt"
    ]
    mutated["request_digest"] = p09._sha256(
        {
            key: value
            for key, value in mutated.items()
            if key != "request_digest"
        }
    )

    with pytest.raises(Exception, match="typed assumptions"):
        adapter.validate_derivative_request(mutated)
    assert "sympy" not in sys.modules


def test_p08b_assumption_mutation_is_rejected_without_backend_import() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "from tests.test_document_derivation_red_team import "
            "_assert_p08b_assumption_mutation_is_rejected_without_backend_import as check; check()",
        ],
        cwd=ROOT,
        env={**os.environ, "PYTHONPATH": str(ROOT / "src")},
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stdout + completed.stderr


def _valid_contract(tmp_path: Path) -> dict:
    artifact_root = tmp_path / "artifacts"
    artifact_root.mkdir()
    payload = {
        "artifact_root": str(artifact_root),
        "collection": p09_guard.FIXED_COLLECTION,
        "page_token": "private-token",
    }
    env = p09_guard._child_environment(tmp_path)
    return {
        "argv": [sys.executable, "-I", "-B", str(p09_guard.BOOTSTRAP)],
        "cwd": p09_guard.WORKSPACE,
        "env": env,
        "input_bytes": _canonical(payload),
        "timeout": 30,
        "shell": False,
        "invocation_count": 0,
    }


@pytest.mark.parametrize(
    "mutation",
    [
        "argv",
        "executable",
        "bootstrap",
        "shell",
        "cwd",
        "environment",
        "collection",
        "timeout",
        "second_invocation",
        "missing_root",
        "out_of_root",
        "symlink_root",
    ],
)
def test_parent_guard_rejects_every_cli_contract_widening(
    tmp_path: Path, mutation: str
) -> None:
    contract = _valid_contract(tmp_path)
    payload = json.loads(contract["input_bytes"].decode("utf-8"))
    if mutation == "argv":
        contract["argv"].append("extra")
    elif mutation == "executable":
        contract["argv"][0] = "/usr/bin/python3"
    elif mutation == "bootstrap":
        contract["argv"][-1] = str(ROOT / "src/mathdevmcp/cli.py")
    elif mutation == "shell":
        contract["shell"] = True
    elif mutation == "cwd":
        contract["cwd"] = tmp_path
    elif mutation == "environment":
        contract["env"] = {**contract["env"], "PYTHONPATH": str(ROOT / "src")}
    elif mutation == "collection":
        payload["collection"] = "blocker_records"
        contract["input_bytes"] = _canonical(payload)
    elif mutation == "timeout":
        contract["timeout"] = 31
    elif mutation == "second_invocation":
        contract["invocation_count"] = 1
    elif mutation == "missing_root":
        Path(payload["artifact_root"]).rmdir()
    elif mutation == "out_of_root":
        payload["artifact_root"] = str(ROOT)
        contract["input_bytes"] = _canonical(payload)
    elif mutation == "symlink_root":
        root = Path(payload["artifact_root"])
        root.rmdir()
        target = tmp_path / "target"
        target.mkdir()
        root.symlink_to(target, target_is_directory=True)

    with pytest.raises(p09_guard.P09GuardError):
        p09_guard._validate_cli_contract(**contract)


def test_mutated_artifact_fails_closed_on_direct_facade_server_and_guarded_cli(
    tmp_path: Path,
) -> None:
    p08d_path = ROOT / "scripts/run_p08d_frozen_payload_replay.py"
    p08d = p09._load_verified_module(
        "p09_test_p08d_runner", p08d_path, p09._sha256(p08d_path.read_bytes())
    )
    audits = p08d._frozen_inputs()
    request = p08d._request("card")
    artifact_root = tmp_path / "resolver-artifacts"

    from mathdevmcp.document_derivation_response import (
        compile_document_derivation_response,
        resolve_document_derivation_records,
    )
    from mathdevmcp.mcp_facade import call_mcp_tool
    from mathdevmcp.mcp_server import (
        resolve_document_derivation_records as server_resolve,
    )

    page = compile_document_derivation_response(
        audits["card"], request, artifact_root=artifact_root, target_limit=20
    )
    token = page["page"]["page_token"]
    destination = (
        artifact_root
        / "document-derivation"
        / page["audit_result_id"]
        / page["audit_request_id"]
        / "detailed.json"
    )
    payload = bytearray(destination.read_bytes())
    payload[-1] ^= 1
    destination.write_bytes(payload)

    with pytest.raises(ValueError) as direct:
        resolve_document_derivation_records(
            token,
            p09_guard.FIXED_COLLECTION,
            artifact_root=artifact_root,
        )
    facade = call_mcp_tool(
        "resolve_document_derivation_records",
        {
            "page_token": token,
            "collection": p09_guard.FIXED_COLLECTION,
            "artifact_root": str(artifact_root),
        },
    )
    server = server_resolve(
        token,
        p09_guard.FIXED_COLLECTION,
        str(artifact_root),
    )
    cli = p09_guard.run_guarded_cli_probe(
        page_token=token,
        artifact_root=artifact_root,
        test_root=tmp_path,
    )

    private_values = (token, str(artifact_root))
    serialized = "\n".join(
        (
            str(direct.value),
            json.dumps(facade, sort_keys=True),
            json.dumps(server.model_dump(by_alias=True, exclude_none=True), sort_keys=True),
            json.dumps(cli, sort_keys=True),
        )
    )
    assert facade["ok"] is False
    assert facade["error"]["type"] == "invalid_arguments"
    assert server.isError is True
    assert cli["cli_returncode"] == 2
    assert cli["guard_attestation"]["forbidden_attempt_count"] == 0
    assert all(value not in serialized for value in private_values)
    assert "Traceback" not in serialized
    assert p09_guard.guard_attestation()["guarded_cli_invocation_count"] == 1

    with pytest.raises(p09_guard.P09GuardError, match="invocation count"):
        p09_guard.run_guarded_cli_probe(
            page_token=token,
            artifact_root=artifact_root,
            test_root=tmp_path,
        )


def test_no_overwrite_writer_rejects_conflicting_repeated_identity(
    tmp_path: Path,
) -> None:
    path = tmp_path / "record.json"
    p09._write_new(path, {"value": 1})

    with pytest.raises(p09.P09Error, match="never overwrites"):
        p09._write_new(path, {"value": 2})


def test_staged_finalization_retry_requires_byte_identical_state(
    tmp_path: Path,
) -> None:
    path = tmp_path / "review-adjudication.json"
    first = p09._write_new_or_require_identical(path, {"value": 1})
    retry = p09._write_new_or_require_identical(path, {"value": 1})

    assert retry == first
    with pytest.raises(p09.IntegrityVeto, match="differs from retry state"):
        p09._write_new_or_require_identical(path, {"value": 2})
