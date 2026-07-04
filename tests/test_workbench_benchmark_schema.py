from mathdevmcp.workbench_benchmark_schema import (
    EXPECTED_SEEDED_WORKBENCH_TOOLS,
    FIXED_MUTATION_FAMILY,
    REQUIRED_RUN_MANIFEST_FIELDS,
    SEEDED_GATE_REQUIRED_ORACLES,
    external_manifest,
    load_external_adapted_manifest,
    seeded_case,
    validate_external_adapted_manifest_document,
    validate_external_adapted_manifest,
    validate_run_manifest,
    validate_workbench_benchmark_case,
    workbench_benchmark_quality_report,
)

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def _run_manifest() -> dict:
    return {field: f"value:{field}" for field in REQUIRED_RUN_MANIFEST_FIELDS}


def _seeded_cases() -> list[dict]:
    cases = []
    for oracle in sorted(SEEDED_GATE_REQUIRED_ORACLES):
        cases.append(
            seeded_case(
                id=f"case:{oracle}",
                tool=f"tool:{oracle}",
                oracle_class=oracle,
                expected_status=oracle,
                expected_abstention=oracle.endswith("nonclaim") or oracle in {"structural_only", "diagnostic_only", "impact_inconclusive"},
                negative_control=oracle
                in {
                    "abstained_missing_assumptions",
                    "backend_unavailable_nonclaim",
                    "structural_only",
                    "diagnostic_only",
                    "applicability_gap",
                    "applicability_conflict",
                    "impact_inconclusive",
                },
                gated=True,
            )
        )
    return cases


def test_workbench_benchmark_case_requires_supported_oracle_class() -> None:
    case = seeded_case(
        id="case:bad",
        tool="derive_or_refute",
        oracle_class="proved_scoped",
        expected_status="proved",
        expected_abstention=False,
        negative_control=False,
        gated=True,
    )

    assert validate_workbench_benchmark_case(case) == []
    case["oracle_class"] = "proofish"
    assert validate_workbench_benchmark_case(case) == ["oracle_class is unsupported"]


def test_external_adapted_manifest_requires_provenance_and_starts_nongating() -> None:
    manifest = external_manifest(
        id="proofnet:001",
        source_family="ProofNet",
        original_id="proofnet-original-001",
        local_path=".localresources/proofnet/001.json",
        license_status="academic_license_confirmed",
        redistribution="local_only",
        privacy_class="licensed_external_local",
        oracle_class="diagnostic_only",
        transformation_notes="Adapted as proof-gap task.",
        source_specific_caveats=("ProofNet source proof style may not map to local backend routes.",),
        review_status="unreviewed",
        gate_status="diagnostic_only",
        gated=False,
    )

    assert validate_external_adapted_manifest(manifest) == []
    manifest["gated"] = True
    assert validate_external_adapted_manifest(manifest) == ["external adapted cases must start with gated=false"]


def test_external_adapted_manifest_rejects_missing_caveats_and_public_redistribution_mismatch() -> None:
    manifest = external_manifest(
        id="theoremqa:001",
        source_family="TheoremQA",
        original_id="theoremqa-original-001",
        local_path=".localresources/workbench-benchmarks/theoremqa/001.json",
        license_status="academic_license_confirmed",
        redistribution="redistributable_public",
        privacy_class="licensed_external_local",
        oracle_class="applicability_gap",
        transformation_notes="Adapted as theorem applicability task.",
        source_specific_caveats=("Question answering oracle must be converted to explicit assumptions.",),
        review_status="unreviewed",
        gate_status="diagnostic_only",
        gated=False,
    )

    assert validate_external_adapted_manifest(manifest) == [
        "public redistribution requires public_redistributable_adapted privacy_class"
    ]
    manifest["redistribution"] = "local_only"
    manifest["source_specific_caveats"] = []
    assert validate_external_adapted_manifest(manifest) == [
        "source_specific_caveats must be a non-empty list of strings"
    ]


def test_external_adapted_manifest_template_validates_as_diagnostic_only() -> None:
    report = load_external_adapted_manifest(
        ROOT / "benchmarks" / "workbench_external" / "external-adapted-case-manifest.template.json"
    )

    assert report["metadata"] == {"schema_version": "1.0", "contract": "external_adapted_manifest_validation"}
    assert report["status"] == "consistent"
    assert report["entry_count"] == 3
    assert report["reporting_rules"]["combine_with_seeded_totals"] is False
    assert "not public redistribution permission" in report["non_claims"][1]


def test_external_adapted_manifest_document_rejects_gating_and_aggregation_claims() -> None:
    document = {
        "entries": [
            external_manifest(
                id="putnambench:001",
                source_family="PutnamBench",
                original_id="putnam-original-001",
                local_path=".localresources/workbench-benchmarks/putnambench/001.json",
                license_status="academic_license_confirmed",
                redistribution="local_only",
                privacy_class="licensed_external_local",
                oracle_class="diagnostic_only",
                transformation_notes="Adapted as review-packet task.",
                source_specific_caveats=("Formalization route must be reviewed.",),
                review_status="unreviewed",
                gate_status="diagnostic_only",
                gated=False,
            )
        ],
        "reporting_rules": {
            "combine_with_seeded_totals": True,
            "allow_leaderboard_claims": True,
            "allow_release_gate_by_default": True,
        },
    }

    report = validate_external_adapted_manifest_document(document)

    assert report["status"] == "mismatch"
    assert {finding["kind"] for finding in report["findings"]} == {
        "external_seeded_total_mix_forbidden",
        "leaderboard_claims_forbidden",
        "release_gate_by_default_forbidden",
    }


def test_run_manifest_requires_auditable_fields() -> None:
    manifest = _run_manifest()

    assert validate_run_manifest(manifest) == []
    del manifest["backend_matrix"]
    assert validate_run_manifest(manifest) == ["run manifest missing backend_matrix"]


def test_quality_report_fails_when_pass_rate_would_be_only_signal() -> None:
    result = {
        "id": "case:single",
        "category": "math_debugging_workbench",
        "observed_status": "proved",
        "passed": True,
        "expected_abstention": False,
        "quality_checks": {"boundary_preserved": True, "oracle_class_supported": True},
    }
    report = workbench_benchmark_quality_report(
        [
            seeded_case(
                id="case:single",
                tool="derive_or_refute",
                oracle_class="proved_scoped",
                expected_status="proved",
                expected_abstention=False,
                negative_control=False,
                gated=True,
            )
        ],
        results=[result],
        deterministic_rerun=([result], [result]),
        expected_tools={"derive_or_refute"},
        mutation_results={name: True for name in FIXED_MUTATION_FAMILY},
        run_manifest=_run_manifest(),
    )

    assert report["metadata"] == {"schema_version": "1.0", "contract": "workbench_benchmark_quality_report"}
    assert report["status"] == "quality_thresholds_failed"
    assert report["seeded_gate_thresholds"]["negative_control_rate_at_least_40_percent"] is False
    assert "not established by pass rate alone" in report["boundary"]


def test_quality_report_passes_with_required_oracles_and_mutation_family() -> None:
    cases = _seeded_cases()
    results = [
        {
            "id": case["id"],
            "category": "math_debugging_workbench",
            "observed_status": case["expected_status"],
            "passed": True,
            "expected_abstention": case["expected_abstention"],
            "quality_checks": {"boundary_preserved": True, "oracle_class_supported": True},
        }
        for case in cases
    ]
    report = workbench_benchmark_quality_report(
        cases,
        results=results,
        deterministic_rerun=(results, results),
        expected_tools={case["tool"] for case in cases},
        mutation_results={name: True for name in FIXED_MUTATION_FAMILY},
        run_manifest=_run_manifest(),
    )

    assert report["status"] == "quality_thresholds_passed"
    assert report["negative_control_rate"] >= 0.40
    assert all(report["seeded_gate_thresholds"].values())


def test_quality_report_fails_when_results_do_not_align_or_rerun_drifts() -> None:
    cases = _seeded_cases()
    first_results = [
        {
            "id": case["id"],
            "category": "math_debugging_workbench",
            "observed_status": case["expected_status"],
            "passed": True,
            "expected_abstention": case["expected_abstention"],
            "quality_checks": {"boundary_preserved": True, "oracle_class_supported": True},
        }
        for case in cases[:-1]
    ]
    second_results = [dict(result) for result in first_results]
    second_results[0]["observed_status"] = "drifted"

    report = workbench_benchmark_quality_report(
        cases,
        results=first_results,
        deterministic_rerun=(first_results, second_results),
        expected_tools={case["tool"] for case in cases},
        mutation_results={name: True for name in FIXED_MUTATION_FAMILY},
        run_manifest=_run_manifest(),
    )

    assert report["status"] == "quality_thresholds_failed"
    assert report["seeded_gate_thresholds"]["case_result_ids_align"] is False
    assert report["seeded_gate_thresholds"]["deterministic_rerun_stable"] is False
    assert report["result_alignment"]["missing_results"] == [cases[-1]["id"]]


def test_expected_seeded_workbench_tool_set_is_explicit() -> None:
    assert EXPECTED_SEEDED_WORKBENCH_TOOLS == {
        "assumptions_required",
        "classify_math_claim",
        "code_implements_equation",
        "derive_or_refute",
        "generate_math_tests",
        "literature_local_audit",
        "localize_proof_gap",
        "math_change_impact",
        "math_review_packet",
        "prove_or_refute",
        "reconcile_notation",
    }
