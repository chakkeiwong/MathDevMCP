from pathlib import Path
import hashlib

import pytest

from mathdevmcp.parser_policy import (
    decide_parser_policy,
    project_parser_policy_expected_labels,
    select_p02_parser_backend,
)
from mathdevmcp.proof_audit_v2 import _durable_parser_policy, audit_derivation_v2_for_label
from tests.p02_no_backend_guard import guard_is_active


ROOT = Path(__file__).resolve().parent.parent
FIXTURES = ROOT / "benchmarks" / "fixtures"


def test_parser_policy_records_optional_backend_caveats_without_blocking_current():
    policy = decide_parser_policy(str(FIXTURES), backends=["current", "definitely_missing_backend"])

    assert policy["metadata"] == {"schema_version": "1.0", "contract": "parser_policy_decision"}
    assert policy["status"] == "selected_for_proof_audit"
    assert policy["selected_backend"] == "current"
    assert any(role["backend"] == "definitely_missing_backend" and role["role"] == "measured_optional" for role in policy["backend_roles"])
    assert policy["caveats"]
    assert policy["blocking_findings"] == []


def test_parser_policy_blocks_when_expected_label_is_missing():
    policy = decide_parser_policy(str(FIXTURES), backends=["current"], expected_labels=["eq:not-in-release-corpus"])

    assert policy["status"] == "selected_for_context_only"
    assert any(finding["kind"] == "missing_expected_labels" for finding in policy["blocking_findings"])


def test_shared_parser_measurement_projects_to_exact_per_label_policy() -> None:
    shared = decide_parser_policy(
        str(FIXTURES),
        backends=["current"],
        expected_labels=["eq:proof-audit-single", "eq:not-in-release-corpus"],
    )

    for label in ("eq:proof-audit-single", "eq:not-in-release-corpus"):
        projected = project_parser_policy_expected_labels(shared, [label])
        direct = decide_parser_policy(str(FIXTURES), backends=["current"], expected_labels=[label])
        assert _durable_parser_policy(projected) == _durable_parser_policy(direct)


def test_proof_audit_v2_downgrades_when_parser_policy_is_blocked():
    if guard_is_active():
        pytest.skip("proof-audit backend execution is outside the Phase 02 extraction boundary")
    result = audit_derivation_v2_for_label(
        str(FIXTURES),
        "eq:proof-audit-single",
        parser_expected_labels=["eq:not-in-release-corpus"],
    )

    assert result["status"] == "inconclusive"
    assert result["counts"]["inconclusive"] == 1
    assert result["obligations"][0]["status"] == "inconclusive"
    assert result["source_binding_status"] == "accepted_exact_source"
    assert result["specialist_parser_readiness"] == "selected_for_context_only"
    assert result["obligations"][0]["substatus"] == "unverified:parser_limit"
    assert any(action["kind"] == "fix_parser_provenance_before_certification" for action in result["high_priority_actions"])


def test_exact_v8_source_binding_is_not_reported_as_missing() -> None:
    source = ROOT / "docs/credit-card-npv-component-proposal/credit_card_npv_component_proposal_v8.tex"
    digest = hashlib.sha256(source.read_bytes()).hexdigest()

    result = audit_derivation_v2_for_label(
        str(source.parent),
        "eq:incremental-cash-flow",
        file=source.name,
        source_digest=digest,
        summary_only=True,
    )

    assert result["source_binding_status"] == "accepted_exact_source"
    assert result["specialist_parser_readiness"] == "selected_for_proof_audit"
    assert "inconclusive:source_label_missing" not in result["substatus_counts"]
    assert all(item["source_binding_status"] == "accepted_exact_source" for item in result["obligations"])


def test_true_missing_label_retains_source_label_missing_substatus() -> None:
    result = audit_derivation_v2_for_label(str(FIXTURES), "eq:not-present", summary_only=True)

    assert result["source_binding_status"] == "source_label_missing"
    assert result["substatus_counts"] == {"inconclusive:source_label_missing": 1}


def test_p02_parser_policy_ignores_success_counts_and_runtime_proxies() -> None:
    decision = select_p02_parser_backend(
        {"parser_version": "p02_lightweight_locator@1", "fidelity_vector": [1, 1, 1, 1, 1, 1, 1]},
        [
            {
                "backend": "latexml",
                "parser_version": "0.8.6",
                "fidelity_vector": [1, 0, 0, 0, 0, 0, 0],
                "source_mappable": False,
                "non_promotional_diagnostics": {"parse_succeeded": True, "label_count": 999, "runtime_seconds": 0.001},
            }
        ],
        frozen_identity=True,
    )

    assert decision["status"] == "current_retained"
    assert decision["selected_backend"] == "current"
    assert decision["proxy_metrics_used_for_selection"] == []
    assert decision["vetoes"] == []


def test_p02_correctly_classified_limitation_does_not_veto_exact_current() -> None:
    decision = select_p02_parser_backend(
        {"parser_version": "p02_lightweight_locator@1", "fidelity_vector": [1, 1, 1, 1, 1, 1, 1]},
        [
            {
                "backend": "pandoc",
                "parser_version": "2.9.2.1",
                "capability_status": "valid_not_source_mappable",
                "limitation_codes": ["no_independent_source_offsets", "global_label_set_only"],
                "diagnostic_observations": {"exact_requested_label_set": True},
                "promotional_fields": [],
                "contradictions": [],
                "eligible_for_selection": False,
            }
        ],
        frozen_identity=True,
    )

    assert decision["status"] == "current_retained"
    assert decision["vetoes"] == []


@pytest.mark.parametrize("status", ["timed_out", "nonzero_exit", "malformed_output"])
def test_p02_runtime_and_malformed_limitations_do_not_veto_exact_current(status: str) -> None:
    limitation = {
        "timed_out": "timeout",
        "nonzero_exit": "nonzero_exit",
        "malformed_output": "malformed_label_ownership",
    }[status]
    decision = select_p02_parser_backend(
        {"parser_version": "p02_lightweight_locator@1", "fidelity_vector": [1, 1, 1, 1, 1, 1, 1]},
        [
            {
                "backend": "latexml",
                "parser_version": "0.8.6",
                "capability_status": status,
                "limitation_codes": [limitation],
                "diagnostic_observations": {},
                "promotional_fields": [],
                "contradictions": [],
                "eligible_for_selection": False,
            }
        ],
        frozen_identity=True,
    )

    assert decision["status"] == "current_retained"
    assert decision["vetoes"] == []


@pytest.mark.parametrize(
    "status",
    ["source_mutated", "invocation_mismatch", "missing_artifact", "version_mismatch"],
)
def test_p02_evidence_integrity_failures_still_veto(status: str) -> None:
    decision = select_p02_parser_backend(
        {"parser_version": "p02_lightweight_locator@1", "fidelity_vector": [1, 1, 1, 1, 1, 1, 1]},
        [
            {
                "backend": "latexml",
                "parser_version": "0.8.6",
                "capability_status": status,
                "limitation_codes": [status],
                "diagnostic_observations": {},
                "promotional_fields": [],
                "contradictions": [],
                "eligible_for_selection": False,
            }
        ],
        frozen_identity=True,
    )

    assert decision["status"] == "blocked_by_specialist_evidence"
    assert decision["vetoes"] == [{"backend": "latexml", "code": status}]


def test_p02_limitation_cannot_hide_promotion_or_invalid_byte_observation() -> None:
    base = {
        "backend": "latexml",
        "parser_version": "0.8.6",
        "capability_status": "timed_out",
        "limitation_codes": ["timeout"],
        "diagnostic_observations": {},
        "promotional_fields": [],
        "contradictions": [],
        "eligible_for_selection": False,
    }
    current = {"parser_version": "p02_lightweight_locator@1", "fidelity_vector": [1] * 7}

    with pytest.raises(ValueError, match="promotional or eligible"):
        select_p02_parser_backend(
            current,
            [{**base, "diagnostic_observations": {"exact_requested_label_set": True}, "promotional_fields": ["exact_requested_label_set"]}],
            frozen_identity=True,
        )
    with pytest.raises(ValueError, match="invalid specialist bytes"):
        select_p02_parser_backend(
            current,
            [{**base, "diagnostic_observations": {"exact_requested_label_set": True}}],
            frozen_identity=True,
        )


def test_p02_independent_requested_label_contradiction_vetoes() -> None:
    decision = select_p02_parser_backend(
        {"parser_version": "p02_lightweight_locator@1", "fidelity_vector": [1, 1, 1, 1, 1, 1, 1]},
        [
            {
                "backend": "pandoc",
                "parser_version": "2.9.2.1",
                "capability_status": "valid_not_source_mappable",
                "limitation_codes": ["no_independent_source_offsets", "global_label_set_only"],
                "diagnostic_observations": {"exact_requested_label_set": False},
                "promotional_fields": [],
                "contradictions": ["exact_requested_label_set"],
                "eligible_for_selection": False,
            }
        ],
        frozen_identity=True,
    )

    assert decision["status"] == "blocked_by_specialist_evidence"
    assert decision["vetoes"] == [
        {
            "backend": "pandoc",
            "code": "independent_specialist_contradiction",
            "fields": ["exact_requested_label_set"],
        }
    ]


def test_p02_new_input_can_select_better_source_mappable_specialist() -> None:
    decision = select_p02_parser_backend(
        {"parser_version": "p02_lightweight_locator@1", "fidelity_vector": [1, 0, 0, 0, 0, 0, 0]},
        [
            {
                "backend": "latexml",
                "parser_version": "0.8.6",
                "fidelity_vector": [1, 1, 1, 0, 0, 0, 1],
                "source_mappable": True,
            }
        ],
        frozen_identity=False,
    )

    assert decision["status"] == "specialist_selected"
    assert decision["selected_backend"] == "latexml"


def test_p02_frozen_identity_requires_review_before_better_specialist_rewrite() -> None:
    decision = select_p02_parser_backend(
        {"parser_version": "p02_lightweight_locator@1", "fidelity_vector": [1, 0, 0, 0, 0, 0, 0]},
        [
            {
                "backend": "pandoc",
                "parser_version": "2.9.2.1",
                "fidelity_vector": [1, 1, 0, 0, 0, 0, 0],
                "source_mappable": True,
            }
        ],
        frozen_identity=True,
    )

    assert decision["status"] == "oracle_amendment_required"
    assert decision["selected_backend"] == "current"
    assert any(item["code"] == "frozen_identity_requires_oracle_amendment" for item in decision["vetoes"])
