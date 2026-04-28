from pathlib import Path

from mathdevmcp.parser_policy import decide_parser_policy
from mathdevmcp.proof_audit_v2 import audit_derivation_v2_for_label


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


def test_proof_audit_v2_downgrades_when_parser_policy_is_blocked():
    result = audit_derivation_v2_for_label(
        str(FIXTURES),
        "eq:proof-audit-single",
        parser_expected_labels=["eq:not-in-release-corpus"],
    )

    assert result["status"] == "inconclusive"
    assert result["counts"]["inconclusive"] == 1
    assert result["obligations"][0]["status"] == "inconclusive"
    assert any(action["kind"] == "fix_parser_provenance_before_certification" for action in result["high_priority_actions"])
