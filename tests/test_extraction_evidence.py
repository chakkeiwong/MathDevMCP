from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path

import pytest

from mathdevmcp import extraction_evidence
from mathdevmcp.evidence_manifest import EvidenceValidationError, content_digest
from mathdevmcp.extraction_evidence import (
    P02_BASE_ORACLE_REF,
    P02_EVIDENCE_ROOT_REF,
    P02_GIT_OID_RE,
    P02_ORACLE_REF,
    _parser_veto,
    _coverage_comparison,
    _project_identity_from_envelope,
    build_mutation_matrix,
    implementation_allowlist,
    load_profile,
    load_recovery_oracle,
    validate_parser_raw_output,
    validate_parser_comparison,
    validate_parser_version_receipt,
    validate_run_manifest,
    validate_pure_extractor_module_bytes,
    verify_entry,
    verify_parser_timeout_gate,
)


ROOT = Path(__file__).resolve().parent.parent
PURE_MODULE = ROOT / "src/mathdevmcp/parser_capability_extractors.py"


def _pure_contract() -> dict:
    return load_profile(ROOT)[0]["parser_capability_contract"]


def _replace_once(raw: bytes, old: bytes, new: bytes) -> bytes:
    assert raw.count(old) == 1
    return raw.replace(old, new, 1)


def test_recovery_overlay_and_entry_close_exactly() -> None:
    effective, materialized = load_profile(ROOT)
    base = json.loads((ROOT / P02_BASE_ORACLE_REF).read_text(encoding="utf-8"))
    recovery = load_recovery_oracle(ROOT)
    entry = verify_entry(ROOT)

    assert len(recovery["profile_patch"]) == 11
    assert effective["schema_version"] == base["schema_version"]
    assert effective["parser_capability_contract"]["schema_version"] == "p02r2_parser_capability_contract@1"
    assert effective["parser_fidelity_profile"]["executables"]["latexml"]["version_timeout_seconds"] == 60
    assert effective["parser_fidelity_profile"]["executables"]["latexml"]["source_timeout_seconds"] == 180
    assert effective["parser_fidelity_profile"]["executables"]["pandoc"]["version_timeout_seconds"] == 30
    assert effective["parser_fidelity_profile"]["executables"]["pandoc"]["source_timeout_seconds"] == 30
    assert all(
        "timeout_seconds" not in executable
        for executable in effective["parser_fidelity_profile"]["executables"].values()
    )
    assert materialized["obligation_count"] == 17
    assert len(implementation_allowlist(ROOT)) == 23
    assert "src/mathdevmcp/parser_capability_extractors.py" in implementation_allowlist(ROOT)
    assert entry["record"]["revision"] == "P02R3"
    assert entry["record"]["recovery_oracle_ref"] == P02_ORACLE_REF
    assert entry["sha256"] == "ebdf525b2196d2fffbaba7862278f7ef54796cc983ee7f326a6df71813a539d2"
    assert P02_EVIDENCE_ROOT_REF == ".local/mathdevmcp/evidence/p02r3-20260712"


def test_effective_non_claims_match_canonical_persisted_order() -> None:
    effective, _ = load_profile(ROOT)
    non_claims = effective["governance_action_profile"]["round_close_schema"]["non_claims"]
    persisted = json.loads(
        extraction_evidence.canonical_json_bytes({"non_claims": non_claims}).decode("utf-8")
    )["non_claims"]

    assert non_claims == persisted
    assert set(non_claims) == {
        "no_mathematical_certification",
        "no_semantic_resolution",
        "no_backend_execution",
        "no_publication_eligibility",
        "no_source_document_edit",
        "no_complete_latex_coverage",
        "no_phase03_execution",
        "no_release_readiness",
    }


def test_pure_extractor_module_passes_exact_static_and_runtime_contract() -> None:
    result = validate_pure_extractor_module_bytes(PURE_MODULE.read_bytes(), _pure_contract())
    assert result["module_sha256"] == content_digest(PURE_MODULE.read_bytes())
    assert list(result["functions"]) == [
        "_p02r2_extract_latexml_structural_label_set",
        "_p02r2_extract_pandoc_math_label_set",
    ]


@pytest.mark.parametrize(
    "mutator",
    [
        lambda raw: b'"""hidden module state"""\n' + raw,
        lambda raw: _replace_once(raw, b"import json\n", b"import json\nimport os\n"),
        lambda raw: _replace_once(raw, b"import json\n", b"import json\nSTATE = 1\n"),
        lambda raw: _replace_once(
            raw,
            b"def _p02r2_extract_pandoc_math_label_set(specialist_stdout_json):",
            b"def _p02r2_extract_pandoc_math_label_set(specialist_stdout_json=b''):",
        ),
        lambda raw: _replace_once(
            raw,
            b"    if type(specialist_stdout_json) is not bytes:\n",
            b"    open('/tmp/forbidden')\n    if type(specialist_stdout_json) is not bytes:\n",
        ),
        lambda raw: _replace_once(
            raw,
            b"    labels = set()\n",
            b"    helper = lambda value: value\n    labels = set()\n",
        ),
        lambda raw: _replace_once(
            raw,
            b"    labels = set()\n",
            b"    import os\n    labels = set()\n",
        ),
    ],
)
def test_pure_extractor_module_rejects_unreviewed_capabilities(mutator) -> None:
    with pytest.raises(EvidenceValidationError):
        validate_pure_extractor_module_bytes(mutator(PURE_MODULE.read_bytes()), _pure_contract())


def test_pure_extractors_reject_malformed_and_recover_only_raw_structural_labels() -> None:
    pure = validate_pure_extractor_module_bytes(PURE_MODULE.read_bytes(), _pure_contract())
    latexml = pure["functions"]["_p02r2_extract_latexml_structural_label_set"]
    pandoc = pure["functions"]["_p02r2_extract_pandoc_math_label_set"]

    assert latexml(b'<document labels="LABEL:eq:one LABEL:eq:extra"/>', b"") == {
        "raw_observable_field": "document_structural_label_set",
        "observed_value": ["eq:extra", "eq:one"],
    }
    with pytest.raises(ValueError):
        latexml(b'<document labels="LABEL:eq:one"/>', b"Error: target malformed")
    assert pandoc(
        b'{"blocks":[{"c":[{"t":"DisplayMath"},"x\\\\label{eq:one}"]'
        b',"t":"Math"}],"meta":{},"pandoc-api-version":[1]}\n'
    ) == {
        "raw_observable_field": "document_structural_label_set",
        "observed_value": ["eq:one"],
    }


def test_raw_output_schema_rejects_duplicates_and_expected_value_leakage() -> None:
    registry = _pure_contract()["extractor_registry"]["p02r2_pandoc_math_label_set_v1"]
    with pytest.raises(EvidenceValidationError):
        validate_parser_raw_output(
            {"raw_observable_field": "document_structural_label_set", "observed_value": ["x", "x"]},
            registry=registry,
        )
    with pytest.raises(EvidenceValidationError):
        validate_parser_raw_output(
            {
                "raw_observable_field": "document_structural_label_set",
                "observed_value": ["x"],
                "expected_value": ["x"],
            },
            registry=registry,
        )


def test_requested_label_coverage_treats_extras_as_explanatory_and_missing_as_contradiction() -> None:
    digest = "0" * 64
    extras = _coverage_comparison(
        ["eq:incremental-cash-flow", "eq:incremental-npv", *[f"eq:extra-{index:03d}" for index in range(296)]],
        ["eq:incremental-cash-flow", "eq:incremental-npv"],
        projection_ref="round/parser/expected-values/case.json",
        projection_sha256=digest,
    )
    assert extras["matches_expected"] is True
    assert extras["missing_requested_value"] == []
    assert len(extras["unscoped_extra_value"]) == 296

    risky = _coverage_comparison(
        ["eq:foc-b", "eq:foc-k", *[f"eq:extra-{index:03d}" for index in range(114)]],
        ["eq:foc-b", "eq:foc-k"],
        projection_ref="round/parser/expected-values/case.json",
        projection_sha256=digest,
    )
    assert risky["matches_expected"] is True
    assert len(risky["unscoped_extra_value"]) == 114

    missing = _coverage_comparison(
        ["eq:foc-b"],
        ["eq:foc-b", "eq:foc-k"],
        projection_ref="round/parser/expected-values/case.json",
        projection_sha256=digest,
    )
    assert missing["matches_expected"] is False
    assert missing["missing_requested_value"] == ["eq:foc-k"]


def test_version_receipt_requires_profile_timeout_and_closed_schema(tmp_path: Path) -> None:
    round_ref = f"{P02_EVIDENCE_ROOT_REF}/result-rounds/rr01"
    profile = {
        "environment": {"PATH": "/usr/bin:/bin", "HOME": "RR/parser/home"},
        "executables": {
            "pandoc": {
                "version_argv": ["/usr/bin/pandoc", "--version"],
                "version_timeout_seconds": 30,
                "source_timeout_seconds": 30,
            }
        },
    }
    receipt_dir = tmp_path / round_ref / "parser/receipts"
    receipt_dir.mkdir(parents=True)
    stdout = b"pandoc 2.9.2.1\n"
    (receipt_dir / "pandoc-version.stdout").write_bytes(stdout)
    (receipt_dir / "pandoc-version.stderr").write_bytes(b"")
    record = {
        "argv": ["/usr/bin/pandoc", "--version"],
        "backend": "pandoc",
        "environment": {"PATH": "/usr/bin:/bin", "HOME": f"{round_ref}/parser/home"},
        "exit_code": 0,
        "schema_version": "p02r2_parser_version_invocation_receipt@1",
        "stderr": {
            "byte_count": 0,
            "present": True,
            "ref": f"{round_ref}/parser/receipts/pandoc-version.stderr",
            "sha256": content_digest(b""),
        },
        "stdout": {
            "byte_count": len(stdout),
            "present": True,
            "ref": f"{round_ref}/parser/receipts/pandoc-version.stdout",
            "sha256": content_digest(stdout),
        },
        "timed_out": False,
        "timeout_seconds": 30,
        "wall_time_ns": 1,
    }
    assert validate_parser_version_receipt(
        tmp_path, record, round_ref=round_ref, backend="pandoc", profile=profile
    ) == record
    wrong_timeout = deepcopy(record)
    wrong_timeout["timeout_seconds"] = 10
    with pytest.raises(EvidenceValidationError):
        validate_parser_version_receipt(
            tmp_path, wrong_timeout, round_ref=round_ref, backend="pandoc", profile=profile
        )


def test_mutation_matrix_is_93_plus_5_and_envelope_projection_is_non_vacuous() -> None:
    effective, _ = load_profile(ROOT)
    golden = effective["golden_identity_vector"]
    result = build_mutation_matrix(ROOT, "rr01")
    assert result["must_change_count"] == result["must_change_pass_count"] == 93
    assert result["must_not_change_count"] == result["must_not_change_pass_count"] == 5
    assert _project_identity_from_envelope(
        golden["identity_payload"],
        golden["non_identity_test_envelope"],
        golden["exclude_from_identity_payload"],
    ) == golden["identity_payload"]
    with pytest.raises(EvidenceValidationError):
        _project_identity_from_envelope(
            golden["identity_payload"],
            {**golden["non_identity_test_envelope"], "leaked_identity_field": True},
            golden["exclude_from_identity_payload"],
        )


def test_git_object_id_width_is_separate_from_artifact_sha256() -> None:
    assert P02_GIT_OID_RE.fullmatch("a" * 40)
    assert P02_GIT_OID_RE.fullmatch("a" * 64)
    assert P02_GIT_OID_RE.fullmatch("a" * 39) is None
    assert P02_GIT_OID_RE.fullmatch("A" * 40) is None


def test_latest_receipt_index_orders_numeric_snapshots_past_sequence_nine(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    round_ref = f"{P02_EVIDENCE_ROOT_REF}/result-rounds/rr01"
    receipt_dir = tmp_path / round_ref / "receipts"
    receipt_dir.mkdir(parents=True)
    for sequence in range(1, 13):
        (receipt_dir / f"receipt-index-{sequence:02d}.json").write_bytes(b"{}")
    terminal = [
        {"sequence": sequence, "check_id": f"action-{sequence}"}
        for sequence in range(1, 13)
    ]

    def fake_verify(root: Path, ref: str) -> dict:
        sequence = int(Path(ref).stem.rsplit("-", 1)[1])
        return {
            "record": {
                "head_sequence": sequence,
                "receipts": terminal[:sequence],
            }
        }

    monkeypatch.setattr(extraction_evidence, "verify_receipt_index", fake_verify)
    latest = extraction_evidence.latest_receipt_index(tmp_path, round_ref)
    assert latest is not None
    assert latest["record"]["head_sequence"] == 12

    (receipt_dir / "receipt-index-2.json").write_bytes(b"{}")
    with pytest.raises(EvidenceValidationError, match="not canonical"):
        extraction_evidence.latest_receipt_index(tmp_path, round_ref)


@pytest.mark.parametrize(
    "status",
    ["timed_out", "nonzero_exit", "malformed_output", "valid_not_source_mappable"],
)
def test_p02r3_limitation_only_status_does_not_set_parser_veto(status: str) -> None:
    assert _parser_veto([{"capability_status": status, "contradictions": []}]) is False


@pytest.mark.parametrize(
    "status",
    ["source_mutated", "invocation_mismatch", "missing_artifact", "version_mismatch"],
)
def test_p02r3_evidence_integrity_status_sets_parser_veto(status: str) -> None:
    assert _parser_veto([{"capability_status": status, "contradictions": []}]) is True


def test_p02r3_independent_contradiction_sets_parser_veto_for_limitation() -> None:
    assert _parser_veto(
        [{"capability_status": "valid_not_source_mappable", "contradictions": ["exact_requested_label_set"]}]
    ) is True


def test_p02r3_timeout_gate_fails_without_turning_limitation_into_veto(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(
        extraction_evidence,
        "_collect_parser_states",
        lambda *args, **kwargs: (
            {
                "latexml": {"record": {"timed_out": False}},
                "pandoc": {"record": {"timed_out": False}},
            },
            {},
            [
                {"record": {"timed_out": True}, "status": "timed_out"},
                {"record": {"timed_out": False}, "status": "valid_not_source_mappable"},
            ],
            {},
        ),
    )

    gate = verify_parser_timeout_gate(tmp_path, "round", "manifest")

    assert gate == {
        "all_invocations_completed_within_ceiling": False,
        "source_timeout_count": 1,
        "timed_out_invocation_count": 1,
        "version_timeout_count": 0,
    }
    assert _parser_veto([{"capability_status": "timed_out", "contradictions": []}]) is False


@pytest.mark.parametrize(
    ("mutation", "expected_status"),
    [("version_mismatch", "version_mismatch"), ("missing_artifact", "missing_artifact")],
)
def test_p02r3_source_integrity_failure_dominates_timeout(
    tmp_path: Path,
    mutation: str,
    expected_status: str,
) -> None:
    round_ref = f"{P02_EVIDENCE_ROOT_REF}/result-rounds/rr01"
    source_ref = "source.tex"
    source_sha256 = content_digest(b"source")
    profile = {
        "environment": {"PATH": "/usr/bin:/bin", "HOME": "RR/parser/home"},
        "executables": {
            "pandoc": {
                "fidelity_argv_template": ["/usr/bin/pandoc", "SOURCE"],
                "source_timeout_seconds": 30,
            }
        },
    }
    refs = extraction_evidence._expected_parser_artifact_refs(round_ref, "pandoc", source_ref)
    stdout_ref = str(refs["stdout"])
    stderr_ref = str(refs["stderr"])
    for ref in (stdout_ref, stderr_ref):
        path = tmp_path / ref
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"")

    def binding(ref: str) -> dict:
        return {
            "byte_count": 0,
            "present": True,
            "ref": ref,
            "sha256": content_digest(b""),
        }

    version = {
        "ref": f"{round_ref}/parser/receipts/pandoc-version-raw.json",
        "sha256": "1" * 64,
        "version_matches": mutation != "version_mismatch",
    }
    record = {
        "argv": ["/usr/bin/pandoc", source_ref],
        "backend": "pandoc",
        "case_token": extraction_evidence._parser_case_token(source_ref),
        "environment": {"PATH": "/usr/bin:/bin", "HOME": f"{round_ref}/parser/home"},
        "exit_code": None,
        "log": None,
        "output": binding(stdout_ref),
        "schema_version": "p02r2_parser_source_invocation_receipt@1",
        "source_ref": source_ref,
        "source_sha256_after": source_sha256,
        "source_sha256_before": source_sha256,
        "stderr": binding(stderr_ref),
        "stdout": binding(stdout_ref),
        "timed_out": True,
        "timeout_seconds": 30,
        "version_receipt_ref": version["ref"],
        "version_receipt_sha256": version["sha256"],
        "wall_time_ns": 1,
    }
    if mutation == "missing_artifact":
        (tmp_path / stdout_ref).unlink()
        missing = {"byte_count": None, "present": False, "ref": stdout_ref, "sha256": None}
        record["stdout"] = missing
        record["output"] = missing

    state = extraction_evidence._source_state(
        tmp_path,
        round_ref,
        "pandoc",
        source_ref,
        extraction_evidence.canonical_json_bytes(record),
        version,
        profile,
        {"source_sha256": source_sha256},
        {},
    )

    assert state["status"] == expected_status
    assert state["status"] != "timed_out"


def test_p02r3_comparison_rejects_unchecked_veto_summary() -> None:
    profile = {
        "schema_version": "synthetic_profile@1",
        "source_allowlist": ["source.tex"],
        "executables": {"latexml": {}},
    }
    contract = {
        "primary_backend": "current",
        "required_invocation_count": 0,
        "required_source_invocation_count": 0,
        "required_version_invocation_count": 0,
    }
    case = {
        "case_token": "0" * 64,
        "current_fidelity": {},
        "expected_value_ref": "round/expected.json",
        "expected_value_sha256": "0" * 64,
        "schema_version": "p02r2_parser_case_comparison@1",
        "selected_backend": "current",
        "selected_version": "p02_lightweight_locator@1",
        "selection_reason": "current_exact_reconstruction_retained; specialists_are_diagnostic_only",
        "source_ref": "source.tex",
        "source_sha256": "0" * 64,
        "specialists": [{"capability_status": "timed_out", "contradictions": []}],
    }
    record = {
        "case_count": 1,
        "cases": [case],
        "current_reconstruction_exact": True,
        "implementation_manifest_ref": "round/implementation-round-sha256.txt",
        "implementation_manifest_sha256": "0" * 64,
        "invocation_count": 0,
        "materially_better_specialist_count": 0,
        "non_claims": extraction_evidence.PARSER_NON_CLAIMS,
        "parser_veto": True,
        "phase": "P02",
        "profile_schema_version": "synthetic_profile@1",
        "pure_extractor_module_ref": "src/mathdevmcp/parser_capability_extractors.py",
        "pure_extractor_module_sha256": "0" * 64,
        "result_round": "rr01",
        "revision": "P02R3",
        "schema_version": "p02r2_parser_comparison@1",
        "selected_backend_counts": {"current": 1, "latexml": 0},
        "source_invocation_count": 0,
        "version_invocation_count": 0,
        "version_receipts": [],
    }

    with pytest.raises(EvidenceValidationError, match="veto differs"):
        validate_parser_comparison(record, profile=profile, contract=contract)


def test_p02r3_run_manifest_requires_bound_measured_parser_versions() -> None:
    effective, _ = load_profile(ROOT)
    parser_profile = effective["parser_fidelity_profile"]
    round_ref = f"{P02_EVIDENCE_ROOT_REF}/result-rounds/rr01"
    evidence = {}
    inventory = []
    for backend in parser_profile["executables"]:
        receipt_ref = f"{round_ref}/parser/receipts/{backend}-version-raw.json"
        digest = ("1" if backend == "latexml" else "2") * 64
        evidence[backend] = {
            "evidence_type": "measured_parser_version_receipt",
            "measured_version": parser_profile["executables"][backend]["measured_version"],
            "version_matches": True,
            "version_receipt_ref": receipt_ref,
            "version_receipt_sha256": digest,
        }
        inventory.append(
            {
                "byte_count": 1,
                "logical_ref": receipt_ref,
                "role": f"{backend}_parser_version_receipt",
                "sha256": digest,
            }
        )
    inventory.append(
        {
            "byte_count": 1,
            "logical_ref": f"{round_ref}/parser/parser-comparison.json",
            "role": "differential_parser_fidelity_comparison",
            "sha256": "4" * 64,
        }
    )
    record = {
        "artifact_inventory": inventory,
        "device_execution": {"gpu_initialized": False, "gpu_requested": False},
        "ended_at_utc": "2026-07-12T00:00:01Z",
        "entry_record_ref": "entry.json",
        "entry_record_sha256": "0" * 64,
        "environment": {},
        "external_tool_considerations": [
            {
                "availability_version_evidence": {
                    "evidence_type": "embedded_version",
                    "measured_version": "p02_lightweight_locator@1",
                },
                "certifying_status": "noncertifying_extraction",
                "role": "primary exact source reconstruction",
                "selected": True,
                "tool": "current_byte_preserving_scanner",
            },
            {
                "availability_version_evidence": evidence["latexml"],
                "certifying_status": "diagnostic_only_unless_source_mappable",
                "role": "diagnostic structural parser",
                "selected": False,
                "tool": "LaTeXML",
            },
            {
                "availability_version_evidence": evidence["pandoc"],
                "certifying_status": "diagnostic_only_unless_source_mappable",
                "role": "diagnostic structural parser",
                "selected": False,
                "tool": "Pandoc",
            },
            {
                "availability_version_evidence": {
                    "evidence_type": "not_invoked",
                    "measured_version": None,
                },
                "certifying_status": "forbidden_by_phase02_boundary",
                "role": "later semantic or mathematical checking",
                "selected": False,
                "tool": "SymPy_Sage_Lean_and_proof_search_backends",
            },
        ],
        "frozen_source_digests": {},
        "git_commit": "0" * 40,
        "governance_receipt_family_ref": f"{round_ref}/receipts",
        "implementation_delta_digest": "0" * 64,
        "implementation_entry_manifest_sha256": "0" * 64,
        "implementation_round_manifest_sha256": "0" * 64,
        "non_claims": ["no_claim"],
        "phase": "P02",
        "plan_ref": "plan.md",
        "plan_sha256": "0" * 64,
        "pre_candidate_receipt_index_ref": f"{round_ref}/receipts/receipt-index-17.json",
        "pre_candidate_receipt_index_sha256": "0" * 64,
        "random_seed_policy": {},
        "result_ref": f"{round_ref}/P02-result.json",
        "result_round": "rr01",
        "result_sha256": "0" * 64,
        "schema_version": "p02_extraction_run_manifest@1",
        "source_data_version": "synthetic",
        "started_at_utc": "2026-07-12T00:00:00Z",
        "wall_time_ns": 1,
    }

    assert validate_run_manifest(record, parser_profile=parser_profile) == record

    fallback = deepcopy(record)
    fallback["external_tool_considerations"][1]["availability_version_evidence"] = "not measured in blocked round"
    with pytest.raises(EvidenceValidationError, match="LaTeXML version evidence"):
        validate_run_manifest(fallback, parser_profile=parser_profile)

    wrong_version = deepcopy(record)
    wrong_version["external_tool_considerations"][1]["availability_version_evidence"]["measured_version"] = "unknown"
    with pytest.raises(EvidenceValidationError, match="LaTeXML version evidence"):
        validate_run_manifest(wrong_version, parser_profile=parser_profile)

    unbound = deepcopy(record)
    unbound["artifact_inventory"][0]["sha256"] = "3" * 64
    with pytest.raises(EvidenceValidationError, match="LaTeXML version receipt is unbound"):
        validate_run_manifest(unbound, parser_profile=parser_profile)

    blocked = deepcopy(record)
    blocked["artifact_inventory"] = []
    for item in blocked["external_tool_considerations"]:
        if item["tool"] in {"LaTeXML", "Pandoc"}:
            item["availability_version_evidence"] = {
                "evidence_type": "not_measured_in_blocked_round",
                "measured_version": None,
                "version_matches": None,
                "version_receipt_ref": None,
                "version_receipt_sha256": None,
            }
    assert validate_run_manifest(blocked, parser_profile=parser_profile) == blocked

    omitted_comparison = deepcopy(blocked)
    omitted_comparison["artifact_inventory"] = [
        item
        for item in record["artifact_inventory"]
        if item["role"] != "differential_parser_fidelity_comparison"
    ]
    with pytest.raises(EvidenceValidationError, match="parser evidence is incomplete"):
        validate_run_manifest(omitted_comparison, parser_profile=parser_profile)


def test_initializer_receipt_predecessor_nullability_matches_round_position() -> None:
    profile = extraction_evidence.governance_profile(ROOT)

    def initializer_receipt(result_round: str) -> dict:
        round_ref = f"{P02_EVIDENCE_ROOT_REF}/result-rounds/{result_round}"
        bindings = {key: "bound" for key in profile["receipt_binding_keys"]["init_round"]}
        if result_round == "rr01":
            for key in extraction_evidence.INIT_PREDECESSOR_BINDING_KEYS:
                bindings[key] = None
        return {
            "schema_version": "p02_command_receipt@1",
            "phase": "P02",
            "result_round": result_round,
            "sequence": 1,
            "check_id": "init_round",
            "execution_class": "governance_native",
            "handler_id": profile["actions"]["init_round"]["handler_id"],
            "external_argv": extraction_evidence.external_argv(round_ref, "init_round"),
            "child_argv": None,
            "child_environment_sha256": None,
            "started_at_utc": "2026-07-12T00:00:00Z",
            "ended_at_utc": "2026-07-12T00:00:01Z",
            "wall_time_ns": 1,
            "exit_code": 0,
            "stdout_ref": f"{round_ref}/logs/init-round.stdout",
            "stdout_sha256": "0" * 64,
            "stdout_byte_count": 0,
            "stderr_ref": f"{round_ref}/logs/init-round.stderr",
            "stderr_sha256": "0" * 64,
            "stderr_byte_count": 0,
            "prior_receipt_sha256": None,
            "bindings": bindings,
        }

    rr01 = initializer_receipt("rr01")
    assert extraction_evidence.validate_command_receipt(rr01, profile=profile) == rr01

    partial_rr01 = deepcopy(rr01)
    partial_rr01["bindings"]["predecessor_round_close_ref"] = "unexpected"
    with pytest.raises(EvidenceValidationError, match="rr01 initializer has a predecessor"):
        extraction_evidence.validate_command_receipt(partial_rr01, profile=profile)

    rr02 = initializer_receipt("rr02")
    assert extraction_evidence.validate_command_receipt(rr02, profile=profile) == rr02
    rr02["bindings"]["predecessor_terminal_receipt_index_sha256"] = None
    with pytest.raises(EvidenceValidationError, match="successor initializer has a null predecessor"):
        extraction_evidence.validate_command_receipt(rr02, profile=profile)
